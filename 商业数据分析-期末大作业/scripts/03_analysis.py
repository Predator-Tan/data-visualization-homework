# -*- coding: utf-8 -*-
"""
03_analysis.py —— 第 3 步：商业分析模型（核心）
================================================
输入：data/clean/orders_clean.csv
输出：outputs/tables/ 下的各模型结果表 + 模型结论汇总

实现 6 个商业分析模型（评分标准要求 ≥3 个）：
  1. RFM 客户价值模型（八分类，中位数切分）
  2. 同期群留存分析（按首次下单月份分群）
  3. 帕累托 / ABC 分类（子类别销售贡献）
  4. 波士顿矩阵（子类别：份额 × 同比增速）
  5. 环比 / 同比分析（月度销售额）
  6. 时间序列预测 SARIMA（月度销售预测 + 95% 置信区间 + MAPE/RMSE 回测）

运行方式：python scripts/03_analysis.py
"""
import warnings
warnings.filterwarnings("ignore")  # 忽略 statsmodels 的收敛提示

import pandas as pd
import numpy as np
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CLEAN = ROOT / "data" / "clean"
OUT = ROOT / "outputs" / "tables"
OUT.mkdir(parents=True, exist_ok=True)

# 分析参考日期：数据截止到 2026-12-30，取 2026-12-31 作为“今天”
REF_DATE = pd.Timestamp("2026-12-31")
conclusions = []   # 汇总所有模型的商业结论


def record(name, text):
    """记录一条商业结论"""
    conclusions.append(f"【{name}】{text}")
    print(f"  ✓ {text}")


# ============================================================
# 模型 1：RFM 客户价值八分类
# ============================================================
def model_rfm(df):
    print("\n▶ 模型1：RFM 客户价值八分类")
    # R=最近一次购买距今多少天，F=订单次数，M=累计消费金额
    rfm = df.groupby("Customer ID").agg(
        R=("Order Date", lambda s: (REF_DATE - s.max()).days),
        F=("Order ID", "nunique"),
        M=("Sales", "sum"),
    ).reset_index()

    # 用中位数做高低切分（评分标准要求：说明切分依据）
    # R 越小越好（越近），故 R<=中位数记 1；F、M 越大越好，故 >中位数记 1
    r_med, f_med, m_med = rfm["R"].median(), rfm["F"].median(), rfm["M"].median()
    rfm["R_高"] = (rfm["R"] <= r_med).astype(int)   # 1=近期活跃
    rfm["F_高"] = (rfm["F"] > f_med).astype(int)    # 1=高频
    rfm["M_高"] = (rfm["M"] > m_med).astype(int)    # 1=高价值

    # 三位二进制 → 八类客户
    seg_map = {
        (1,1,1): "重要价值客户", (1,1,0): "重要发展客户",
        (1,0,1): "重要保持客户", (1,0,0): "一般发展客户",
        (0,1,1): "重要挽留客户", (0,1,0): "一般保持客户",
        (0,0,1): "一般价值客户", (0,0,0): "一般挽留客户",
    }
    rfm["客户类型"] = list(zip(rfm["R_高"], rfm["F_高"], rfm["M_高"]))
    rfm["客户类型"] = rfm["客户类型"].map(seg_map)

    rfm.to_csv(OUT / "rfm_result.csv", index=False, encoding="utf-8-sig")
    dist = rfm["客户类型"].value_counts()
    record("RFM", f"客户分 8 类，中位数切分：R≤{r_med}天 / F>{f_med}次 / M>${m_med:.0f}；"
                  f"规模最大的两类为“{dist.index[0]}”{dist.iloc[0]}人、“{dist.index[1]}”{dist.iloc[1]}人")
    return rfm


# ============================================================
# 模型 2：同期群留存分析
# ============================================================
def model_cohort(df):
    print("\n▶ 模型2：同期群留存分析")
    # 每个客户首次下单月份 = 同期群
    first_month = df.groupby("Customer ID")["订单月"].min().rename("首次月")
    c = df[["Customer ID", "订单月", "Order ID"]].merge(first_month, on="Customer ID")
    # 月份偏移：第 0 月 = 首次下单当月
    c["偏移月"] = (pd.PeriodIndex(c["订单月"], freq="M").astype("int64")
                   - pd.PeriodIndex(c["首次月"], freq="M").astype("int64"))
    # 同期群大小
    cohort_size = c.groupby("首次月")["Customer ID"].nunique()
    # 留存矩阵：每个 (首次月, 偏移月) 有多少客户下单
    matrix = c.groupby(["首次月", "偏移月"])["Customer ID"].nunique().unstack()
    # 除以同期群大小 → 留存率
    retention = matrix.divide(cohort_size, axis=0).round(4)

    retention.to_csv(OUT / "cohort_retention.csv", encoding="utf-8-sig")
    # 找最近一个完整同期群的第 12 个月留存率作为业务结论
    if retention.shape[1] > 12:
        c12 = retention.iloc[:, 12].dropna()
        record("同期群", f"各同期群第 12 个月平均留存率 {c12.mean():.1%}；"
                         f"首购后第 2 个月平均留存 {retention.iloc[:, 1].mean():.1%}（流失最快）")
    else:
        record("同期群", f"留存矩阵已生成，覆盖 {retention.shape[1]} 个偏移月")
    return retention


# ============================================================
# 模型 3：帕累托 / ABC 分类
# ============================================================
def model_pareto(df):
    print("\n▶ 模型3：帕累托 / ABC 分类")
    sales = df.groupby("Sub-Category")["Sales"].sum().sort_values(ascending=False)
    total = sales.sum()
    cum = sales.cumsum() / total
    # ABC：A 类累计≤70%，B 类 70%~90%，C 类 >90%
    def abc(x):
        return "A" if x <= 0.70 else ("B" if x <= 0.90 else "C")
    abc_df = pd.DataFrame({
        "Sub-Category": sales.index,
        "销售额": sales.values,
        "占比": (sales / total).round(4),
        "累计占比": cum.round(4),
        "ABC类别": cum.map(abc),
    }).reset_index(drop=True)
    abc_df.to_csv(OUT / "pareto_abc.csv", index=False, encoding="utf-8-sig")

    n_a = (abc_df["ABC类别"] == "A").sum()
    record("帕累托", f"{n_a} 个子类别（占 {n_a/len(abc_df):.0%}）贡献了约 70% 销售额，"
                     f"头部是 {abc_df.iloc[0]['Sub-Category']}（${abc_df.iloc[0]['销售额']:,.0f}）")
    return abc_df


# ============================================================
# 模型 4：波士顿矩阵（BCG）
# ============================================================
def model_bcg(df):
    print("\n▶ 模型4：波士顿矩阵（份额 × 同比增速）")
    sub = df.groupby(["Sub-Category", "订单年"])["Sales"].sum().unstack(fill_value=0)
    # 份额 = 该子类别全期销售额 / 总销售额
    share = sub.sum(axis=1) / sub.sum(axis=1).sum()
    # 增速 = 2026 年相对 2025 年的同比增速
    growth = (sub[2026] - sub[2025]) / sub[2025].replace(0, np.nan)
    bcg = pd.DataFrame({"市场份额": share.round(4), "同比增速": growth.round(4)}).reset_index()

    # 以中位数划分四象限
    s_med, g_med = bcg["市场份额"].median(), bcg["同比增速"].median()
    def quad(r):
        if r["市场份额"] >= s_med and r["同比增速"] >= g_med: return "明星"
        if r["市场份额"] >= s_med and r["同比增速"] <  g_med: return "现金牛"
        if r["市场份额"] <  s_med and r["同比增速"] >= g_med: return "问题"
        return "瘦狗"
    bcg["象限"] = bcg.apply(quad, axis=1)
    bcg.to_csv(OUT / "bcg_matrix.csv", index=False, encoding="utf-8-sig")

    star = bcg[bcg["象限"] == "明星"]["Sub-Category"].tolist()
    cow = bcg[bcg["象限"] == "现金牛"]["Sub-Category"].tolist()
    record("波士顿矩阵", f"明星业务：{','.join(star) or '无'}；现金牛：{','.join(cow)}（份额高、增速趋稳）")
    return bcg


# ============================================================
# 模型 5：环比 / 同比分析
# ============================================================
def model_mom_yoy(df):
    print("\n▶ 模型5：环比 / 同比分析（月度销售额）")
    monthly = df.groupby("订单月")["Sales"].sum().rename("销售额").reset_index()
    monthly["环比增速"] = monthly["销售额"].pct_change().round(4)      # 与上月比
    monthly["同比增速"] = monthly["销售额"].pct_change(12).round(4)    # 与去年同月比
    monthly.to_csv(OUT / "monthly_sales.csv", index=False, encoding="utf-8-sig")

    # 结论：取最近一个月的环比、同比
    last = monthly.iloc[-1]
    record("环比同比", f"最新月 {last['订单月']} 销售额 ${last['销售额']:,.0f}，"
                       f"环比 {last['环比增速']:+.1%}、同比 {last['同比增速']:+.1%}")
    return monthly


# ============================================================
# 模型 6：时间序列预测 SARIMA
# ============================================================
def model_sarima(df):
    print("\n▶ 模型6：SARIMA 月度销售预测（含置信区间与回测）")
    from statsmodels.tsa.statespace.sarimax import SARIMAX

    monthly = df.groupby("订单月")["Sales"].sum()
    monthly.index = pd.PeriodIndex(monthly.index, freq="M").to_timestamp()
    monthly = monthly.asfreq("MS")  # 固定为月初频率，补齐无缺失

    # 前 42 个月训练，后 6 个月测试（回测验证）
    train, test = monthly.iloc[:42], monthly.iloc[42:]
    # 月度数据含年度季节性(12)，采用 SARIMA(1,1,1)x(1,1,1,12)
    model = SARIMAX(train, order=(1, 1, 1), seasonal_order=(1, 1, 1, 12),
                    enforce_stationarity=False, enforce_invertibility=False)
    fit = model.fit(disp=False)

    # 预测测试期，并取 95% 置信区间
    forecast = fit.get_forecast(steps=len(test))
    pred = forecast.predicted_mean
    ci = forecast.conf_int(alpha=0.05)
    ci.columns = ["下界", "上界"]

    # 回测误差
    mape = np.mean(np.abs((test.values - pred.values) / test.values)) * 100
    rmse = np.sqrt(np.mean((test.values - pred.values) ** 2))

    result = pd.DataFrame({
        "月份": test.index.strftime("%Y-%m"),
        "实际": test.values.round(2),
        "预测": pred.values.round(2),
        "下界": ci["下界"].values.round(2),
        "上界": ci["上界"].values.round(2),
    })
    result.to_csv(OUT / "sarima_forecast.csv", index=False, encoding="utf-8-sig")

    record("SARIMA", f"回测 MAPE={mape:.1f}%、RMSE={rmse:,.0f}，预测含 95% 置信区间；"
                     f"最新月预测 ${pred.iloc[-1]:,.0f}（实际 ${test.iloc[-1]:,.0f}）")
    return result, fit


def main():
    df = pd.read_csv(CLEAN / "orders_clean.csv", parse_dates=["Order Date", "Ship Date"])

    model_rfm(df)
    model_cohort(df)
    model_pareto(df)
    model_bcg(df)
    model_mom_yoy(df)
    model_sarima(df)

    # 汇总所有商业结论，供论文引用
    with open(OUT / "模型结论汇总.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(conclusions))
    print(f"\n{'='*50}\n共完成 6 个模型，结论已写入 outputs/tables/模型结论汇总.txt")


if __name__ == "__main__":
    main()

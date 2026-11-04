# -*- coding: utf-8 -*-
"""
04_visuals.py —— 业务模型图 + 探索性分析图（科研级样式）
================================================
生成 9 张科研级图表，采用 Seaborn 科学样式、统计元素与子图。
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

matplotlib.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]
matplotlib.rcParams["axes.unicode_minus"] = False
sns.set_theme(style="whitegrid", font="Microsoft YaHei")

ROOT = Path(__file__).resolve().parent.parent
CLEAN = ROOT / "data" / "clean"
TBL = ROOT / "outputs" / "tables"
FIG = ROOT / "outputs" / "figures"
FIG.mkdir(parents=True, exist_ok=True)

# 科学配色
C1, C2, C3, C4 = "#3B6FB6", "#E07B39", "#D62728", "#2CA02C"
PALETTE = ["#4E79A7", "#F28E2B", "#E15759", "#76B7B2", "#59A14F", "#EDC948", "#B07AA1"]


def save(fig, name):
    fig.savefig(FIG / name, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  已保存 {name}")


# ============ fig01 RFM 客户价值（分面气泡图 + 象限线） ============
def fig_rfm():
    rfm = pd.read_csv(TBL / "rfm_result.csv")
    r_med, m_med = rfm["R"].median(), rfm["M"].median()
    g = sns.relplot(data=rfm, x="R", y="M", size="F", hue="客户类型",
                    sizes=(15, 200), alpha=0.7, palette="tab10",
                    height=6, aspect=1.3)
    ax = g.ax
    ax.axvline(r_med, color="gray", ls="--", lw=1)
    ax.axhline(m_med, color="gray", ls="--", lw=1)
    ax.set_xlabel("最近消费距今天数 R（天）", fontsize=12)
    ax.set_ylabel("累计消费金额 M（美元）", fontsize=12)
    ax.set_title("图1 RFM 客户价值八分类气泡散点图（虚线=中位数阈值）",
                 fontsize=14, fontweight="bold")
    ax.legend(loc="center left", bbox_to_anchor=(1.02, 0.5), fontsize=8, title="客户类型")
    save(g.fig, "fig01_RFM客户价值气泡图.png")


# ============ fig02 同期群留存热力图（带数值标注） ============
def fig_cohort():
    ret = pd.read_csv(TBL / "cohort_retention.csv", index_col=0)
    ret = ret.iloc[:, :13]
    fig, ax = plt.subplots(figsize=(11, 6))
    sns.heatmap(ret * 100, annot=True, fmt=".0f", cmap="RdYlGn", linewidths=0.5,
                center=30, cbar_kws={"label": "留存率 %"}, ax=ax,
                annot_kws={"size": 7})
    ax.set_title("图2 同期群留存率热力图（单位 %，颜色越深留存越高）",
                 fontsize=14, fontweight="bold")
    ax.set_xlabel("首次购买后的月份偏移", fontsize=12)
    ax.set_ylabel("首次购买月份（同期群）", fontsize=12)
    save(fig, "fig02_同期群留存热力图.png")


# ============ fig03 帕累托图（双轴 + 80/20 参考线） ============
def fig_pareto():
    p = pd.read_csv(TBL / "pareto_abc.csv")
    fig, ax1 = plt.subplots(figsize=(12, 6))
    bars = ax1.bar(p["Sub-Category"], p["销售额"], color=C1, alpha=0.85, label="销售额")
    ax1.set_ylabel("销售额（美元）", fontsize=12)
    ax1.tick_params(axis="x", rotation=45, labelsize=9)
    ax2 = ax1.twinx()
    ax2.plot(p["Sub-Category"], p["累计占比"] * 100, color=C3, marker="o", lw=2,
             label="累计销售额占比 %")
    ax2.axhline(70, color="gray", ls="--", lw=1.2, alpha=0.8)
    ax2.text(0.5, 71.5, "70% 分界线", color="gray", fontsize=9)
    ax2.set_ylabel("累计占比 %", fontsize=12)
    ax2.set_ylim(0, 105)
    ax1.set_title("图3 帕累托分析：子类别销售额贡献（前6类占70%销售额）",
                  fontsize=14, fontweight="bold")
    ax1.legend(loc="upper left"); ax2.legend(loc="center right")
    save(fig, "fig03_帕累托图.png")


# ============ fig04 波士顿矩阵（气泡图：大小=销售额） ============
def fig_bcg():
    b = pd.read_csv(TBL / "bcg_matrix.csv")
    # 气泡大小用市场份额映射
    sizes = (b["市场份额"] * 3000).clip(30, 1000)
    colors = {"明星": C3, "现金牛": C1, "问题": C2, "瘦狗": "#999999"}
    fig, ax = plt.subplots(figsize=(10, 7))
    for q, grp in b.groupby("象限"):
        ax.scatter(grp["市场份额"], grp["同比增速"], s=grp["市场份额"] * 4000,
                   color=colors[q], alpha=0.65, edgecolors="black", linewidth=0.5,
                   label=q)
        for _, r in grp.iterrows():
            ax.annotate(r["Sub-Category"], (r["市场份额"], r["同比增速"]),
                        fontsize=8, ha="left", va="bottom")
    ax.axhline(b["同比增速"].median(), color="gray", ls="--", lw=1)
    ax.axvline(b["市场份额"].median(), color="gray", ls="--", lw=1)
    ax.axhline(0, color="black", lw=1)
    ax.set_xlabel("市场份额（全期销售额占比）", fontsize=12)
    ax.set_ylabel("同比增速（2026 vs 2025）", fontsize=12)
    ax.set_title("图4 波士顿矩阵：子类别份额 × 增速（气泡大小=份额）",
                 fontsize=14, fontweight="bold")
    ax.legend(loc="upper left", fontsize=9)
    ax.grid(alpha=0.3)
    save(fig, "fig04_波士顿矩阵.png")


# ============ fig05 环比同比（柱+线+阴影双轴） ============
def fig_mom_yoy():
    m = pd.read_csv(TBL / "monthly_sales.csv")
    m["订单月"] = pd.to_datetime(m["订单月"])
    fig, ax1 = plt.subplots(figsize=(13, 6))
    ax1.bar(m["订单月"], m["销售额"] / 1000, color=C1, alpha=0.7, label="月度销售额（千美元）")
    ax1.set_ylabel("销售额（千美元）", fontsize=12)
    ax2 = ax1.twinx()
    ax2.plot(m["订单月"], m["同比增速"] * 100, color=C3, lw=2, marker="o", ms=3,
             label="同比增速 %")
    ax2.axhline(0, color="gray", lw=0.8, ls="--")
    ax2.fill_between(m["订单月"], 0, m["同比增速"] * 100, alpha=0.15, color=C3)
    ax2.set_ylabel("同比增速 %", fontsize=12)
    ax1.set_title("图5 月度销售额与同比增速（阴影=增速正负区间）",
                  fontsize=14, fontweight="bold")
    l1, lb1 = ax1.get_legend_handles_labels()
    l2, lb2 = ax2.get_legend_handles_labels()
    ax1.legend(l1 + l2, lb1 + lb2, loc="upper left", fontsize=9)
    save(fig, "fig05_销售额环比同比趋势.png")


# ============ fig06 SARIMA 预测 + 残差子图 ============
def fig_sarima():
    m = pd.read_csv(TBL / "monthly_sales.csv")
    f = pd.read_csv(TBL / "sarima_forecast.csv")
    actual = pd.Series(m["销售额"].values, index=pd.to_datetime(m["订单月"]))
    pred_idx = pd.to_datetime(f["月份"])
    resid = (f["实际"] - f["预测"]).values

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 9), sharex=False,
                                   gridspec_kw={"height_ratios": [3, 1]})
    ax1.plot(actual.index, actual.values / 1000, color=C1, lw=2, label="实际销售额")
    ax1.plot(pred_idx, f["预测"] / 1000, color=C3, lw=2, marker="o", ms=4, label="SARIMA 预测")
    ax1.fill_between(pred_idx, f["下界"] / 1000, f["上界"] / 1000,
                     color=C3, alpha=0.2, label="95% 置信区间")
    ax1.set_ylabel("销售额（千美元）", fontsize=12)
    ax1.set_title("图6 SARIMA 月度销售预测（含 95% 置信区间）", fontsize=14, fontweight="bold")
    ax1.legend(loc="upper left", fontsize=9)
    ax1.grid(alpha=0.3)
    ax2.bar(pred_idx, resid / 1000, color=["#D62728" if v > 0 else "#2CA02C" for v in resid],
            alpha=0.7, label="预测残差")
    ax2.axhline(0, color="black", lw=0.8)
    ax2.set_ylabel("残差（千美元）", fontsize=12)
    ax2.set_xlabel("月份", fontsize=12)
    ax2.set_title("预测残差（实际 − 预测）", fontsize=12)
    ax2.legend(fontsize=9)
    save(fig, "fig06_SARIMA销售预测置信区间.png")


# ============ fig07 区域销售与利润（分组柱+利润率线） ============
def fig_explore():
    df = pd.read_csv(CLEAN / "orders_clean.csv", parse_dates=["Order Date"])

    reg = df.groupby("Region").agg(销售额=("Sales", "sum"), 利润=("Profit", "sum"))
    reg["利润率"] = reg["利润"] / reg["销售额"]
    fig, ax = plt.subplots(figsize=(9, 6))
    x = np.arange(len(reg))
    w = 0.35
    ax.bar(x - w/2, reg["销售额"] / 10000, w, color=C1, label="销售额（万美元）")
    ax.bar(x + w/2, reg["利润"] / 10000, w, color=C4, label="利润（万美元）")
    ax2 = ax.twinx()
    ax2.plot(x, reg["利润率"] * 100, color=C3, marker="D", lw=2, label="利润率 %")
    ax.set_xticks(x, reg.index)
    ax.set_ylabel("金额（万美元）", fontsize=12)
    ax2.set_ylabel("利润率 %", fontsize=12)
    ax.set_title("图7 四大区域销售额、利润与利润率", fontsize=14, fontweight="bold")
    l1, lb1 = ax.get_legend_handles_labels()
    l2, lb2 = ax2.get_legend_handles_labels()
    ax.legend(l1 + l2, lb1 + lb2, loc="upper right", fontsize=9)
    save(fig, "fig07_区域销售与利润.png")

    # fig08 类别利润贡献（横向条形+数值标注）
    cat = df.groupby("Category").agg(销售额=("Sales", "sum"), 利润=("Profit", "sum"))
    cat = cat.sort_values("利润")
    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.barh(cat.index, cat["利润"] / 10000, color=PALETTE[:3])
    for b, v in zip(bars, cat["利润"]):
        ax.text(v / 10000, b.get_y() + b.get_height()/2, f"  {v/10000:.1f}万",
                va="center", fontsize=10)
    ax.set_xlabel("利润（万美元）", fontsize=12)
    ax.set_title("图8 三大产品类别利润贡献", fontsize=14, fontweight="bold")
    ax.grid(axis="x", alpha=0.3)
    save(fig, "fig08_类别利润贡献.png")

    # fig09 月度订单量（折线+移动平均+趋势）
    ords = df.groupby("订单月")["Order ID"].nunique()
    ords.index = pd.to_datetime(ords.index)
    ma = ords.rolling(3).mean()
    fig, ax = plt.subplots(figsize=(13, 5))
    ax.plot(ords.index, ords.values, color=C1, lw=1.5, alpha=0.6, label="月度订单量")
    ax.plot(ma.index, ma.values, color=C3, lw=2.5, label="3个月移动平均")
    # 线性趋势
    x = np.arange(len(ords))
    k, b = np.polyfit(x, ords.values, 1)
    ax.plot(ords.index, k * x + b, color="gray", lw=1.5, ls="--", label="线性趋势")
    ax.set_ylabel("订单量", fontsize=12)
    ax.set_title("图9 月度订单量趋势（含移动平均与线性趋势）", fontsize=14, fontweight="bold")
    ax.legend(fontsize=9)
    save(fig, "fig09_月度订单量趋势.png")


def main():
    print("开始生成科研级图表……")
    fig_rfm(); fig_cohort(); fig_pareto(); fig_bcg(); fig_mom_yoy(); fig_sarima(); fig_explore()
    print(f"完成！9 张图输出到 outputs/figures/")


if __name__ == "__main__":
    main()

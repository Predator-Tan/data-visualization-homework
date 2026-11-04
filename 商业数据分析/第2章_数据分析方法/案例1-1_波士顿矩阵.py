# -*- coding: utf-8 -*-
"""
案例 1-1　波士顿矩阵（BCG）—— 原 Excel/Power BI 案例迁移为 Python
================================================================
教材：CDA 一级认证教材《商业数据分析（第4版）》第 2 章 2.1.1 分类分析
原案例：1-1波士顿矩阵.xlsx（Power BI/Excel 实现）

【项目内涵】
波士顿矩阵用两个指标给产品/品牌分类：市场占有率（横轴，反映企业实力）
和销售增长率（纵轴，反映市场引力）。以均值为分界，把 14 个品牌划分成
四类：明星（高份额高增长）、现金牛（高份额低增长）、问题（低份额高增长）、
瘦狗（低份额低增长），从而指导对不同品牌采取不同经营策略。

【本文件做法】
读入真实销售数据，计算 订单金额 = 单价×销量，按品牌汇总 7月/8月销售额，
得到每个品牌的市场占有率（销售额占比）与环比增长率，画四象限散点图。

数据：data-无答案/1-1波士顿矩阵.xlsx（销售表，9285 行）
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

matplotlib.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]
matplotlib.rcParams["axes.unicode_minus"] = False

# 原案例数据文件路径
DATA = Path(__file__).resolve().parent.parent / "data"
DATA = DATA / "1《CDA 一级认证教材：商业数据分析》" \
            / "第2章 数据分析方法/1、分析的基础范式/data-无答案/1-1波士顿矩阵.xlsx"
OUT = Path(__file__).resolve().parent

# 1. 读入数据
df = pd.read_excel(DATA, sheet_name="销售表")
df["销售日期"] = pd.to_datetime(df["销售日期"])
df["订单金额"] = df["单价"] * df["销量"]          # 销售额 = 单价 × 销量
df["月份"] = df["销售日期"].dt.month

# 2. 计算每个品牌的市场占有率（销售额占比）和环比增长率
share = df.groupby("品牌")["订单金额"].sum() / df["订单金额"].sum()   # 市场占有率
pivot = df.pivot_table(index="品牌", columns="月份", values="订单金额", aggfunc="sum")
growth = (pivot[8] - pivot[7]) / pivot[7]                              # 环比增长率

# 3. 分界阈值（与参考答案一致：均值）
share_mean = share.mean()          # 平均市场占有率 = 1/14
growth_mean = growth.mean()        # 平均环比增长率（约等于总市场环比）

# 4. 划分四象限
def quadrant(r):
    if r["份额"] >= share_mean and r["增长"] >= growth_mean: return "明星"
    if r["份额"] >= share_mean and r["增长"] <  growth_mean: return "现金牛"
    if r["份额"] <  share_mean and r["增长"] >= growth_mean: return "问题"
    return "瘦狗"

result = pd.DataFrame({"份额": share, "增长": growth}).reset_index()
result["象限"] = result.apply(quadrant, axis=1)

# 5. 画波士顿矩阵四象限图
colors = {"明星": "#E15759", "现金牛": "#4E79A7", "问题": "#F28E2B", "瘦狗": "#BAB0AC"}
fig, ax = plt.subplots(figsize=(9, 7))
for q, grp in result.groupby("象限"):
    ax.scatter(grp["份额"], grp["增长"], s=140, color=colors[q], label=q, alpha=0.85)
    for _, r in grp.iterrows():
        ax.annotate(r["品牌"], (r["份额"], r["增长"]), fontsize=10, ha="left", va="bottom")
ax.axhline(growth_mean, color="gray", ls="--", lw=1)
ax.axvline(share_mean, color="gray", ls="--", lw=1)
ax.set_xlabel("市场占有率（销售额占比）")
ax.set_ylabel("销售增长率（8月环比7月）")
ax.set_title("波士顿矩阵：14 个品牌的市场份额 × 增长率", fontsize=14, fontweight="bold")
ax.legend(loc="upper left")
ax.grid(alpha=0.3)
fig.savefig(OUT / "图1-1_波士顿矩阵.png", dpi=150, bbox_inches="tight", facecolor="white")
plt.close(fig)

# 6. 打印结果（对照参考答案）
print("总市场环比增长率：", round((pivot[8].sum()-pivot[7].sum())/pivot[7].sum(), 6))
print("品牌平均市场占有率：", round(share_mean, 6))
print("\n各品牌分类结果：")
for q in ["明星", "现金牛", "问题", "瘦狗"]:
    brands = result[result["象限"] == q]["品牌"].tolist()
    print(f"  {q}：{', '.join(brands) if brands else '无'}")
print("\n图已保存到", OUT / "图1-1_波士顿矩阵.png")

# -*- coding: utf-8 -*-
"""
案例 1-3　用户忠诚度模型（潜在用户 / 易流失用户识别）—— 迁移为 Python
================================================================
教材：第 2 章 2.1.1 分类分析   原案例：1-3用户忠诚度模型.xlsx

【项目内涵】
以"最近13周"为观察窗口：分析时点 2021-01-01，往前 13 周即 2020-10-02。
按"消费天数"（去重后的消费日期数）判定：
- 潜在用户：13周前消费 0 天，且 13周内只消费 1 天（首次购买的新客）
- 易流失用户：13周内消费 0 天（最近不再消费）
- 活跃用户：13周内消费 ≥2 天
据此识别需要"激活"和"挽回"的人群（与参考答案口径一致）。
"""
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

matplotlib.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]
matplotlib.rcParams["axes.unicode_minus"] = False

BASE = Path(__file__).resolve().parent.parent / "data" / "1《CDA 一级认证教材：商业数据分析》" / "第2章 数据分析方法/1、分析的基础范式"
DATA = BASE / "data-无答案/1-3用户忠诚度模型.xlsx"
OUT = Path(__file__).resolve().parent
CUTOFF = pd.Timestamp("2020-10-02")   # 最近13周起点

df = pd.read_excel(DATA, sheet_name="销售流水表")
df["消费日期"] = pd.to_datetime(df["消费日期"])

# 每个会员：13周前消费天数、13周内消费天数（消费天数=去重后的消费日期）
g = df.groupby("会员编号").agg(
    十三周前消费天数=("消费日期", lambda s: s[s < CUTOFF].nunique()),
    十三周内消费天数=("消费日期", lambda s: s[s >= CUTOFF].nunique()),
).reset_index()

# 分类（与参考答案口径一致）
def label(r):
    if r["十三周内消费天数"] == 0:
        return "易流失用户"      # 最近13周无消费
    if r["十三周前消费天数"] == 0 and r["十三周内消费天数"] == 1:
        return "潜在用户"        # 首次购买、只消费1天的新客
    return "活跃用户"

g["用户类别"] = g.apply(label, axis=1)

dist = g["用户类别"].value_counts()
print("用户分类结果：")
for k, v in dist.items():
    print(f"  {k}：{v} 人（{v/len(g):.1%}）")

# 可视化
fig, ax = plt.subplots(figsize=(7, 5))
ax.bar(dist.index, dist.values, color=["#F28E2B", "#E15759", "#4E79A7"])
for i, v in enumerate(dist.values):
    ax.text(i, v, str(v), ha="center", va="bottom", fontsize=12)
ax.set_ylabel("人数")
ax.set_title("用户忠诚度模型：潜在用户与易流失用户识别", fontsize=13, fontweight="bold")
fig.savefig(OUT / "图1-3_用户忠诚度.png", dpi=150, bbox_inches="tight", facecolor="white")
plt.close(fig)
print("\n图已保存到", OUT / "图1-3_用户忠诚度.png")

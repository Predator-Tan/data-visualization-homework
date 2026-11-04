# -*- coding: utf-8 -*-
"""第2章 统计制图原理（sale 数据）—— 迁移为 Python
教材第2章 3、统计制图原理：整理数据→明确信息→确定比较类型→确定图表类型。
本文件用 sale 数据（年/市场/销售额/利润）演示趋势图与对比图。"""
import pandas as pd, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from pathlib import Path
matplotlib.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]
matplotlib.rcParams["axes.unicode_minus"] = False
BASE = Path(__file__).resolve().parent.parent / "data" / "1《CDA 一级认证教材：商业数据分析》" / "第2章 数据分析方法/3、统计制图原理"
OUT = Path(__file__).resolve().parent

df = pd.read_csv(BASE / "sale.csv", encoding="gbk", header=None)
df.columns = ["year", "market", "sale", "profit"]
df["sale"] = pd.to_numeric(df["sale"], errors="coerce")
df["profit"] = pd.to_numeric(df["profit"], errors="coerce")

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
# 趋势：年度销售总额
df.groupby("year")["sale"].sum().plot(kind="line", marker="o", ax=axes[0], color="#4E79A7")
axes[0].set_title("趋势：年度销售总额")
# 对比：各市场销售
df.groupby("market")["sale"].sum().plot(kind="bar", ax=axes[1], color="#F28E2B")
axes[1].set_title("对比：各市场销售")
fig.suptitle("统计制图原理：趋势图 vs 对比图", fontsize=14, fontweight="bold")
fig.tight_layout()
fig.savefig(OUT / "图2-案例4_统计制图.png", dpi=150, bbox_inches="tight", facecolor="white"); plt.close(fig)
print("统计制图完成：年度趋势 + 市场对比")

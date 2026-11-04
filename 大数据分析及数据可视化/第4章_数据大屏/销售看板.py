# -*- coding: utf-8 -*-
"""
《Excel数据可视化》第四章 销售看板 迁移为 Python
================================================================
原书用 Excel 制作销售数据大屏，本文件用 matplotlib 复现：
KPI（总订单额/总利润/利润率）+ 月度趋势 + 区域销售 + 产品类别 + 快递公司。
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

matplotlib.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]
matplotlib.rcParams["axes.unicode_minus"] = False

BASE = Path(__file__).resolve().parent.parent / "data"
OUT = Path(__file__).resolve().parent / "figures"
PALETTE = ["#4E79A7", "#F28E2B", "#E15759", "#76B7B2", "#59A14F", "#EDC948"]

df = pd.read_excel(BASE / "第四章 销售看板参考.xlsx", sheet_name="销售明细")
df["订单日期"] = pd.to_datetime(df["订单日期"])
for c in ["订单额", "利润额"]:
    df[c] = pd.to_numeric(df[c], errors="coerce")
df = df.dropna(subset=["订单额"])

sales = df["订单额"].sum()
profit = df["利润额"].sum()

fig = plt.figure(figsize=(16, 9), facecolor="#F7F9FC")
fig.suptitle("销售数据大屏", fontsize=20, fontweight="bold", y=0.98)

# KPI 行
ax_kpi = fig.add_axes([0.05, 0.86, 0.9, 0.08])
ax_kpi.axis("off")
ax_kpi.text(0.05, 0.5, f"总订单额\n{sales/10000:.0f} 万", fontsize=16, fontweight="bold",
            va="center", color=PALETTE[0])
ax_kpi.text(0.35, 0.5, f"总利润\n{profit/10000:.0f} 万", fontsize=16, fontweight="bold",
            va="center", color=PALETTE[4])
ax_kpi.text(0.6, 0.5, f"利润率\n{profit/sales:.1%}", fontsize=16, fontweight="bold",
            va="center", color=PALETTE[2])
ax_kpi.text(0.8, 0.5, f"订单数\n{df['订单单号'].nunique():,}", fontsize=16, fontweight="bold",
            va="center", color=PALETTE[1])

# 1 月度销售趋势
ax1 = fig.add_subplot(2, 2, 1)
df.groupby("月份_销售")["订单额"].sum().plot(kind="line", marker="o", ax=ax1, color=PALETTE[0])
ax1.set_title("月度订单额趋势"); ax1.tick_params(axis="x", rotation=45)

# 2 区域销售
ax2 = fig.add_subplot(2, 2, 2)
df.groupby("区域")["订单额"].sum().sort_values(ascending=False).plot(kind="bar", ax=ax2, color=PALETTE[1])
ax2.set_title("各区域订单额")

# 3 产品类别
ax3 = fig.add_subplot(2, 2, 3)
df.groupby("产品类别")["订单额"].sum().plot(kind="pie", autopct="%.1f%%", ax=ax3)
ax3.set_title("产品类别销售占比"); ax3.set_ylabel("")

# 4 快递公司
ax4 = fig.add_subplot(2, 2, 4)
df.groupby("快递公司")["订单额"].sum().sort_values(ascending=False).head(8).plot(kind="barh", ax=ax4, color=PALETTE[3])
ax4.set_title("快递公司订单额 TOP8")

fig.tight_layout(rect=[0, 0, 1, 0.85])
fig.savefig(OUT / "大屏2_销售看板.png", dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
plt.close(fig)

print("销售看板完成：")
print(f"  总订单额 {sales:,.0f}，总利润 {profit:,.0f}，利润率 {profit/sales:.1%}")
print(f"  销售最高区域：{df.groupby('区域')['订单额'].sum().idxmax()}")
print("图已保存到", OUT / "大屏2_销售看板.png")

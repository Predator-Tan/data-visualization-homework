# -*- coding: utf-8 -*-
"""第2章 PowerBI 案例2：服装零售分析 —— 迁移为 Python
教材第2章 5、PowerBI基本操作/案例2：零售单(事实表)×店铺/员工/SKU等维度表，
做零售分析。本文件用 pandas 做月度销售趋势 + 店铺排行。"""
import pandas as pd, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from pathlib import Path
matplotlib.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]
matplotlib.rcParams["axes.unicode_minus"] = False
BASE = Path(__file__).resolve().parent.parent / "data" / "1《CDA 一级认证教材：商业数据分析》" / "第2章 数据分析方法/5、PowerBI基本操作/案例2/服装零售-原始数据.xlsx"
OUT = Path(__file__).resolve().parent

df = pd.read_excel(BASE, sheet_name="零售单")
df["订单日期"] = pd.to_datetime(df["订单日期"])
df["月份"] = df["订单日期"].dt.to_period("M").astype(str)
df["成交金额"] = pd.to_numeric(df["成交金额"], errors="coerce")

monthly = df.groupby("月份")["成交金额"].sum()
shop = df.groupby("店铺id")["成交金额"].sum().sort_values(ascending=False)

fig, axes = plt.subplots(1, 2, figsize=(13, 5))
monthly.plot(kind="line", marker="o", ax=axes[0], color="#4E79A7")
axes[0].set_title("月度成交金额趋势"); axes[0].set_ylabel("成交金额")
shop.head(10).plot(kind="bar", ax=axes[1], color="#F28E2B")
axes[1].set_title("店铺成交金额 TOP10"); axes[1].set_xlabel("店铺id")
fig.suptitle("服装零售分析", fontsize=14, fontweight="bold")
fig.tight_layout()
fig.savefig(OUT / "图2-案例2_服装零售.png", dpi=150, bbox_inches="tight", facecolor="white"); plt.close(fig)

print("服装零售分析完成：")
print(f"  订单总数 {len(df)}，总成交金额 {df['成交金额'].sum():,.0f}")
print("  成交金额最高的店铺：", shop.index[0], f"（{shop.iloc[0]:,.0f}）")

# -*- coding: utf-8 -*-
"""第2章 PowerBI 零售订单表 —— 迁移为 Python
教材第2章 5、PowerBI基本操作/零售订单表.xlsx：零售销售分析。"""
import pandas as pd, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from pathlib import Path
matplotlib.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]
matplotlib.rcParams["axes.unicode_minus"] = False
BASE = Path(__file__).resolve().parent.parent / "data" / "1《CDA 一级认证教材：商业数据分析》" / "第2章 数据分析方法/5、PowerBI基本操作"
OUT = Path(__file__).resolve().parent

df = pd.read_excel(BASE / "零售订单表.xlsx")
df["订单时间"] = pd.to_datetime(df["订单时间"])
df["月份"] = df["订单时间"].dt.to_period("M").astype(str)
df["实际支付"] = pd.to_numeric(df["实际支付"], errors="coerce")

monthly = df.groupby("月份")["实际支付"].sum()
city = df.groupby("城市")["实际支付"].sum().sort_values(ascending=False)
cat = df.groupby("商品类别")["实际支付"].sum()

fig, axes = plt.subplots(1, 3, figsize=(15, 5))
monthly.plot(kind="line", marker="o", ax=axes[0], color="#4E79A7")
axes[0].set_title("月度销售趋势")
city.head(8).plot(kind="bar", ax=axes[1], color="#F28E2B")
axes[1].set_title("城市销售 TOP8")
cat.plot(kind="pie", autopct="%.1f%%", ax=axes[2])
axes[2].set_title("商品类别占比")
fig.suptitle("零售订单分析", fontsize=14, fontweight="bold")
fig.tight_layout()
fig.savefig(OUT / "图2-案例5_零售订单分析.png", dpi=150, bbox_inches="tight", facecolor="white"); plt.close(fig)
print("零售订单分析完成：总订单", len(df), "笔，总支付", f"{df['实际支付'].sum():,.0f}，销售最高城市", city.index[0])

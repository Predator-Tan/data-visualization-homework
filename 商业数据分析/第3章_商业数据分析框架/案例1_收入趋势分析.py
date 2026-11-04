# -*- coding: utf-8 -*-
"""案例1 收入趋势分析 —— 原 Excel 案例迁移为 Python
教材第3章 3.4.1：从宏观到微观分析收入趋势——年度趋势→月度趋势→同比→下钻省份。"""
import pandas as pd, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from pathlib import Path
matplotlib.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]
matplotlib.rcParams["axes.unicode_minus"] = False
BASE = Path(__file__).resolve().parent.parent / "data" / "1《CDA 一级认证教材：商业数据分析》" / "第3章 商业数据分析框架"
OUT = Path(__file__).resolve().parent

df = pd.read_excel(BASE / "案例1：收入趋势分析/案例1：收入趋势分析原始数据.xlsx", sheet_name="原始数据")
df["年月"] = df["订单年份"].astype(str) + "-" + df["订单月份"].astype(str).str.zfill(2)

# 1. 年度销售趋势
annual = df.groupby("订单年份")["销售额"].sum()
# 2. 月度销售趋势（跨年合并，按月份汇总）
monthly = df.groupby("订单月份")["销售额"].sum()
# 3. 各省份销售（下钻）
province = df.groupby("销售省份")["销售额"].sum().sort_values(ascending=False)

fig, axes = plt.subplots(1, 3, figsize=(15, 5))
axes[0].bar(annual.index.astype(str), annual.values/10000, color="#4E79A7")
axes[0].set_title("年度销售趋势"); axes[0].set_ylabel("销售额(万)")
axes[1].plot(monthly.index, monthly.values/10000, marker="o", color="#F28E2B")
axes[1].set_title("月度销售趋势"); axes[1].set_xlabel("月份")
axes[2].barh(province.index[:8][::-1], province.values[:8][::-1]/10000, color="#59A14F")
axes[2].set_title("省份销售额 TOP8"); axes[2].set_xlabel("销售额(万)")
fig.suptitle("案例1：收入趋势分析（年度→月度→省份下钻）", fontsize=14, fontweight="bold")
fig.tight_layout()
fig.savefig(OUT / "图3-1_收入趋势分析.png", dpi=150, bbox_inches="tight", facecolor="white"); plt.close(fig)

print("年度销售额：", dict(round(annual).astype(int)))
print("销售最高省份：", province.index[0], f"（{province.iloc[0]/10000:.0f}万）")
print("图已保存")

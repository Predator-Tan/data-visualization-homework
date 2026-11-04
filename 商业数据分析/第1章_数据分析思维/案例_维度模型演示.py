# -*- coding: utf-8 -*-
"""第1章 数据分析思维 —— 维度模型演示（商场销售数据）迁移为 Python
教材第1章：维度模型 = 事实表 + 维度表（星型模型）。本案例演示
用 Python 对商场销售事实表按 城市/品牌/类别/时间 维度做聚合分析，
等价于 Power BI 的维度模型建模 + 拖拽分析。"""
import pandas as pd, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from pathlib import Path
matplotlib.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]
matplotlib.rcParams["axes.unicode_minus"] = False
BASE = Path(__file__).resolve().parent.parent / "data" / "1《CDA 一级认证教材：商业数据分析》" / "第1章 数据分析思维/维度模型演示"
OUT = Path(__file__).resolve().parent

fact = pd.read_excel(BASE / "商场销售数据表.xlsx", sheet_name="产品销售数据表")   # 事实表
city = pd.read_excel(BASE / "商场销售数据表.xlsx", sheet_name="商铺城市")         # 维度表
fact["销售额"] = pd.to_numeric(fact["销售额"], errors="coerce")
fact["订单日期"] = pd.to_datetime(fact["订单日期"])
fact["年度"] = fact["订单日期"].dt.year

# 多维聚合：按城市、按品牌、按类别、按年度
by_city = fact.groupby("商铺城市")["销售额"].sum().sort_values(ascending=False)
by_brand = fact.groupby("品牌名称")["销售额"].sum().sort_values(ascending=False)
by_cat = fact.groupby("产品类别")["销售额"].sum()
by_year = fact.groupby("年度")["销售额"].sum()

fig, axes = plt.subplots(2, 2, figsize=(13, 9))
by_city.plot(kind="bar", ax=axes[0, 0], color="#4E79A7"); axes[0, 0].set_title("按城市维度的销售额")
by_brand.plot(kind="bar", ax=axes[0, 1], color="#F28E2B"); axes[0, 1].set_title("按品牌维度的销售额")
by_cat.plot(kind="pie", autopct="%.1f%%", ax=axes[1, 0]); axes[1, 0].set_title("按类别维度的销售额")
by_year.plot(kind="line", marker="o", ax=axes[1, 1], color="#E15759"); axes[1, 1].set_title("按年度维度的销售额趋势")
fig.suptitle("维度模型演示：商场销售多维分析", fontsize=15, fontweight="bold")
fig.tight_layout()
fig.savefig(OUT / "图1-1_维度模型演示.png", dpi=150, bbox_inches="tight", facecolor="white"); plt.close(fig)

print("维度模型演示完成：")
print("  销售额最高城市：", by_city.index[0], f"（{by_city.iloc[0]:,.0f}）")
print("  销售额最高品牌：", by_brand.index[0], f"（{by_brand.iloc[0]:,.0f}）")
print("  年度销售额：", dict(round(by_year).astype(int)))

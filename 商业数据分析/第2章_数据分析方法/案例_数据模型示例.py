# -*- coding: utf-8 -*-
"""第2章 PowerBI 创建数据模型示例 —— 迁移为 Python
教材第2章 5、PowerBI基本操作/创建数据模型示例.xlsx：销售业绩(事实表)
×客户/城市/产品(维度表) 的星型模型，用 pandas 多表关联实现。"""
import pandas as pd, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from pathlib import Path
matplotlib.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]
matplotlib.rcParams["axes.unicode_minus"] = False
BASE = Path(__file__).resolve().parent.parent / "data" / "1《CDA 一级认证教材：商业数据分析》" / "第2章 数据分析方法/5、PowerBI基本操作"
OUT = Path(__file__).resolve().parent

fact = pd.read_excel(BASE / "创建数据模型示例.xlsx", sheet_name="销售业绩表")
client = pd.read_excel(BASE / "创建数据模型示例.xlsx", sheet_name="客户信息表")
city = pd.read_excel(BASE / "创建数据模型示例.xlsx", sheet_name="城市信息表")
product = pd.read_excel(BASE / "创建数据模型示例.xlsx", sheet_name="产品信息表")
fact["金额（$M）"] = pd.to_numeric(fact["金额（$M）"], errors="coerce")

# 星型模型：事实表 关联 三个维度表
df = fact.merge(client, on="客户ID", how="left") \
         .merge(city, on="城市编号", how="left") \
         .merge(product, on="产品编号", how="left")

# 按企业规模 / 企业性质 汇总销售额
by_scale = df.groupby("企业规模")["金额（$M）"].sum().sort_values(ascending=False)
by_nature = df.groupby("企业性质")["金额（$M）"].sum().sort_values(ascending=False)

fig, axes = plt.subplots(1, 2, figsize=(13, 5))
by_scale.plot(kind="bar", ax=axes[0], color="#4E79A7")
axes[0].set_title("各企业规模销售金额($M)")
by_nature.plot(kind="bar", ax=axes[1], color="#F28E2B")
axes[1].set_title("各企业性质销售金额($M)")
fig.suptitle("数据模型示例：星型模型多表关联分析", fontsize=14, fontweight="bold")
fig.tight_layout()
fig.savefig(OUT / "图2-案例6_数据模型.png", dpi=150, bbox_inches="tight", facecolor="white"); plt.close(fig)
print("数据模型示例完成：事实表", len(fact), "行 × 客户/城市/产品 3个维度表，多表关联汇总")

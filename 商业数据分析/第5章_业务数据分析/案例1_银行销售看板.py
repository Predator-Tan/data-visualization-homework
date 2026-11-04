# -*- coding: utf-8 -*-
"""第5章 银行 PowerBI 业务看板案例 —— 迁移为 Python
教材第5章：银行理财产品销售分析，原为 PowerBI 看板，用 Python 复现核心图表。"""
import pandas as pd, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from pathlib import Path
matplotlib.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]
matplotlib.rcParams["axes.unicode_minus"] = False
BASE = Path(__file__).resolve().parent.parent / "data" / "1《CDA 一级认证教材：商业数据分析》" / "第5章 业务数据分析/第5章  PowerBI业务看板案例-银行案例"
OUT = Path(__file__).resolve().parent

df = pd.read_excel(BASE / "银行案例数据 - 学员用.xlsx", sheet_name="销售数据")
df["购买金额"] = pd.to_numeric(df["购买金额"], errors="coerce")
df["收益"] = pd.to_numeric(df["收益"], errors="coerce")
df = df.dropna(subset=["购买金额"])

fig, axes = plt.subplots(2, 2, figsize=(13, 9))
# 1. 品类销售额
cat = df.groupby("品类编号")["购买金额"].sum().sort_values(ascending=False)
axes[0, 0].bar(cat.index, cat.values/10000, color="#4E79A7")
axes[0, 0].set_title("各品类销售额(万)"); axes[0, 0].set_xlabel("品类编号")
# 2. 年龄段分布
age = df["年龄"].value_counts()
axes[0, 1].pie(age.values, labels=age.index, autopct="%.1f%%", startangle=90)
axes[0, 1].set_title("客户年龄段分布")
# 3. 风险偏好分布
risk = df["风险编号"].value_counts()
axes[1, 0].bar(risk.index, risk.values, color="#F28E2B")
axes[1, 0].set_title("风险偏好分布")
# 4. 金额 vs 收益 散点
axes[1, 1].scatter(df["购买金额"], df["收益"], s=20, alpha=0.5, color="#59A14F")
axes[1, 1].set_xlabel("购买金额"); axes[1, 1].set_ylabel("收益"); axes[1, 1].set_title("金额与收益关系")
fig.suptitle("银行理财产品销售看板", fontsize=15, fontweight="bold")
fig.tight_layout()
fig.savefig(OUT / "图5-1_银行销售看板.png", dpi=150, bbox_inches="tight", facecolor="white"); plt.close(fig)

print("银行销售分析完成：")
print("  品类销售TOP：", dict(cat.head(3)))
print("  年龄段分布：", dict(age))
print("  总购买金额：", f"{df['购买金额'].sum():,.0f} 元")

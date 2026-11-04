# -*- coding: utf-8 -*-
"""案例3 电商平台的精准营销 —— 原 Excel 案例迁移为 Python
教材第3章 3.5.2：通过用户细分（性别/年龄/品类/支付方式）做精准营销。"""
import pandas as pd, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from pathlib import Path
matplotlib.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]
matplotlib.rcParams["axes.unicode_minus"] = False
BASE = Path(__file__).resolve().parent.parent / "data" / "1《CDA 一级认证教材：商业数据分析》" / "第3章 商业数据分析框架"
OUT = Path(__file__).resolve().parent

df = pd.read_excel(BASE / "案例3：电商平台的精准营销/案例3：电商平台的精准营销-原始数据.xlsx", sheet_name="原始数据")
df.columns = list(df.columns[:8]) + list(df.columns[8:])
df = df[["客户ID", "性别", "年龄", "品类", "数量", "支付方式"]]

# 用户细分：年龄分段
df["年龄段"] = pd.cut(df["年龄"], bins=[0, 25, 35, 45, 100], labels=["≤25", "26-35", "36-45", ">45"])
# 1. 品类分布  2. 支付方式分布  3. 年龄段分布
cat = df["品类"].value_counts()
pay = df["支付方式"].value_counts()
age = df["年龄段"].value_counts()

fig, axes = plt.subplots(1, 3, figsize=(15, 5))
axes[0].pie(cat.values, labels=cat.index, autopct="%.1f%%", startangle=90)
axes[0].set_title("品类分布")
axes[1].bar(pay.index, pay.values, color=["#4E79A7", "#F28E2B"])
axes[1].set_title("支付方式分布")
axes[2].bar(age.index.astype(str), age.values, color="#59A14F")
axes[2].set_title("年龄段分布")
fig.suptitle("案例3：电商精准营销——用户细分", fontsize=14, fontweight="bold")
fig.tight_layout()
fig.savefig(OUT / "图3-3_精准营销.png", dpi=150, bbox_inches="tight", facecolor="white"); plt.close(fig)

print("品类 TOP3：", dict(cat.head(3)))
print("支付方式：", dict(pay))
print("年龄段分布：", dict(age))
print("\n精准营销建议：针对", pay.index[0], "用户和", cat.index[0], "品类做差异化活动（如支付满减）")

# -*- coding: utf-8 -*-
"""引申方法③ 构成分析法（各产品销量占比）—— 迁移为 Python"""
import pandas as pd, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from pathlib import Path
matplotlib.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]
matplotlib.rcParams["axes.unicode_minus"] = False
BASE = Path(__file__).resolve().parent.parent / "data" / "1《CDA 一级认证教材：商业数据分析》" / "第2章 数据分析方法/2、由基础分析范式引申出的分析方法/data-无答案"
OUT = Path(__file__).resolve().parent

# 该表标题/表头占了前4行，真正的列名在第4行(索引3)
df = pd.read_excel(BASE / "3构成分析.xlsx", sheet_name="构成分析", header=3)
df = df[["产品类型", "销售量"]].dropna()
df.columns = ["产品", "销售量"]
df["销售量"] = pd.to_numeric(df["销售量"], errors="coerce")
df = df.dropna()
df["占比"] = df["销售量"] / df["销售量"].sum()

fig, ax = plt.subplots(figsize=(7, 7))
ax.pie(df["销售量"], labels=df["产品"], autopct="%.1f%%",
       colors=["#4E79A7", "#F28E2B", "#E15759", "#76B7B2", "#59A14F"], startangle=90)
ax.set_title("构成分析：各产品销售量占比", fontsize=14, fontweight="bold")
fig.savefig(OUT / "图_构成分析.png", dpi=150, bbox_inches="tight", facecolor="white"); plt.close(fig)
print("构成分析完成：")
print(df[["产品", "销售量", "占比"]].to_string(index=False))

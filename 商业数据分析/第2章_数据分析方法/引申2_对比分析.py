# -*- coding: utf-8 -*-
"""引申方法② 对比分析法（不同产品订单量对比）—— 迁移为 Python"""
import pandas as pd, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from pathlib import Path
matplotlib.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]
matplotlib.rcParams["axes.unicode_minus"] = False
BASE = Path(__file__).resolve().parent.parent / "data" / "1《CDA 一级认证教材：商业数据分析》" / "第2章 数据分析方法/2、由基础分析范式引申出的分析方法/data-无答案"
OUT = Path(__file__).resolve().parent

df = pd.read_excel(BASE / "2对比分析.xlsx", sheet_name="对比分析", header=1)
df = df[["产品类型", "订单量（单位：个）"]].dropna()
df.columns = ["产品", "订单量"]
df["订单量"] = pd.to_numeric(df["订单量"], errors="coerce")
df = df.dropna().reset_index(drop=True)

fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(df["产品"], df["订单量"], color="#4E79A7")
for b, v in zip(bars, df["订单量"]):
    ax.text(b.get_x()+b.get_width()/2, v, str(int(v)), ha="center", va="bottom")
ax.set_ylabel("订单量（个）"); ax.set_title("对比分析：不同产品订单量对比", fontsize=14, fontweight="bold")
fig.savefig(OUT / "图_对比分析.png", dpi=150, bbox_inches="tight", facecolor="white"); plt.close(fig)
print("对比分析完成。订单量最高：", df.loc[df["订单量"].idxmax(), "产品"])

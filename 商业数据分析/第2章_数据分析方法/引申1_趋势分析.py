# -*- coding: utf-8 -*-
"""引申方法① 趋势分析法（近10年订单量波动）—— 迁移为 Python"""
import pandas as pd, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from pathlib import Path
matplotlib.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]
matplotlib.rcParams["axes.unicode_minus"] = False
BASE = Path(__file__).resolve().parent.parent / "data" / "1《CDA 一级认证教材：商业数据分析》" / "第2章 数据分析方法/2、由基础分析范式引申出的分析方法/data-无答案"
OUT = Path(__file__).resolve().parent

df = pd.read_excel(BASE / "1趋势分析.xlsx", sheet_name="趋势图", header=1)
df = df[["year", "订单量（单位：个）"]].dropna()
df.columns = ["年份", "订单量"]
df["年份"] = pd.to_numeric(df["年份"], errors="coerce")
df["订单量"] = pd.to_numeric(df["订单量"], errors="coerce")
df = df.dropna()

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(df["年份"].astype(int), df["订单量"], marker="o", color="#4E79A7", linewidth=2)
ax.set_ylabel("订单量（个）"); ax.set_title("趋势分析：近 10 年订单量波动趋势", fontsize=14, fontweight="bold")
ax.grid(alpha=0.3)
fig.savefig(OUT / "图_趋势分析.png", dpi=150, bbox_inches="tight", facecolor="white"); plt.close(fig)
print("趋势分析完成。订单量最高年份：", int(df.loc[df["订单量"].idxmax(), "年份"]), "（", int(df["订单量"].max()), "个）")

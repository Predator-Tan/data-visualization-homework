# -*- coding: utf-8 -*-
"""引申方法⑤ 关系分析法（投入成本 vs 产出收益）—— 迁移为 Python"""
import pandas as pd, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from pathlib import Path
matplotlib.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]
matplotlib.rcParams["axes.unicode_minus"] = False
BASE = Path(__file__).resolve().parent.parent / "data" / "1《CDA 一级认证教材：商业数据分析》" / "第2章 数据分析方法/2、由基础分析范式引申出的分析方法/data-无答案"
OUT = Path(__file__).resolve().parent

raw = pd.read_excel(BASE / "5关系分析.xlsx", sheet_name="关系图", header=None)
# 在全表查找"产出收益"表头所在位置
pos = None
for r in range(raw.shape[0]):
    for c in range(raw.shape[1]):
        if "产出收益" in str(raw.iloc[r, c]):
            pos = (r, c); break
    if pos: break
r0, c0 = pos
df = raw.iloc[r0+1:, c0:c0+2].dropna()
df.columns = ["产出收益", "投入成本"]
df = df.astype(float)

r = df["投入成本"].corr(df["产出收益"])
fig, ax = plt.subplots(figsize=(8, 6))
ax.scatter(df["投入成本"], df["产出收益"], color="#4E79A7", alpha=0.7, s=40)
ax.set_xlabel("投入成本"); ax.set_ylabel("产出收益")
ax.set_title(f"关系分析：投入成本与产出收益（r={r:.3f}）", fontsize=14, fontweight="bold")
ax.grid(alpha=0.3)
fig.savefig(OUT / "图_关系分析.png", dpi=150, bbox_inches="tight", facecolor="white"); plt.close(fig)
print(f"关系分析完成：投入成本与产出收益的相关系数 r = {r:.3f}")

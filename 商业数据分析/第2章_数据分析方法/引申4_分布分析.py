# -*- coding: utf-8 -*-
"""引申方法④ 分布分析法（门店客流量分布 + 箱线图）—— 迁移为 Python"""
import pandas as pd, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from pathlib import Path
matplotlib.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]
matplotlib.rcParams["axes.unicode_minus"] = False
BASE = Path(__file__).resolve().parent.parent / "data" / "1《CDA 一级认证教材：商业数据分析》" / "第2章 数据分析方法/2、由基础分析范式引申出的分析方法/data-无答案"
OUT = Path(__file__).resolve().parent

# 门店客流量列（时点, 门店客流量）在第1、2列，表头在第2行
raw = pd.read_excel(BASE / "4分布分析.xlsx", sheet_name="分布分析", header=None)
# 定位"门店客流量"所在列，取该列数据
col_idx = None
for c in range(raw.shape[1]):
    if raw[c].astype(str).str.contains("门店客流量", na=False).any():
        col_idx = c; break
vals = raw.iloc[2:, col_idx].dropna()
vals = pd.to_numeric(vals, errors="coerce").dropna()

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
axes[0].hist(vals, bins=25, color="#76B7B2", edgecolor="white")
axes[0].set_xlabel("门店客流量"); axes[0].set_title("分布分析：门店客流量直方图")
axes[1].boxplot(vals, vert=True, patch_artist=True, boxprops=dict(facecolor="#4E79A7", alpha=0.6))
axes[1].set_ylabel("门店客流量"); axes[1].set_title("分布分析：门店客流量箱线图")
fig.suptitle("分布分析法", fontsize=14, fontweight="bold")
fig.savefig(OUT / "图_分布分析.png", dpi=150, bbox_inches="tight", facecolor="white"); plt.close(fig)

print("门店客流量统计：min=%.1f Q1=%.1f 中位数=%.1f Q3=%.1f max=%.1f 均值=%.1f" % (
    vals.min(), vals.quantile(0.25), vals.median(), vals.quantile(0.75), vals.max(), vals.mean()))

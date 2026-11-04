# -*- coding: utf-8 -*-
"""
案例 3-1　相关分析（两个变量的相关关系）—— 迁移为 Python
================================================================
教材：第 2 章 2.1.3 相关分析   原案例：3-1相关分析.xlsx

【项目内涵】
相关分析研究两个变量之间的相关关系，用相关系数 r 度量（-1~1），
并用散点图 + 回归线直观呈现。r 越接近 ±1 关系越强。
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats
from pathlib import Path

matplotlib.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]
matplotlib.rcParams["axes.unicode_minus"] = False

BASE = Path(__file__).resolve().parent.parent / "data" / "1《CDA 一级认证教材：商业数据分析》" / "第2章 数据分析方法/1、分析的基础范式"
DATA = BASE / "data-无答案/3-1相关分析.xlsx"
OUT = Path(__file__).resolve().parent

df = pd.read_excel(DATA, sheet_name="原始数据")
df.columns = ["y", "x"]
x, y = df["x"], df["y"]

r = x.corr(y)                      # 皮尔逊相关系数
slope, intercept, r2, _, _ = stats.linregress(x, y)   # 线性回归

fig, ax = plt.subplots(figsize=(8, 6))
ax.scatter(x, y, color="#4E79A7", alpha=0.7, s=40)
xs = np.linspace(x.min(), x.max(), 100)
ax.plot(xs, slope * xs + intercept, color="#E15759", lw=2, label=f"回归线 y={slope:.3f}x+{intercept:.1f}")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_title(f"相关分析：x 与 y 的关系（相关系数 r={r:.4f}）", fontsize=14, fontweight="bold")
ax.legend()
fig.savefig(OUT / "图3-1_相关分析.png", dpi=150, bbox_inches="tight", facecolor="white")
plt.close(fig)

print(f"相关系数 r = {r:.4f}")
print(f"判定系数 R² = {r2:.4f}")
print(f"线性回归：y = {slope:.4f}x + {intercept:.4f}")
print("\n图已保存到", OUT / "图3-1_相关分析.png")

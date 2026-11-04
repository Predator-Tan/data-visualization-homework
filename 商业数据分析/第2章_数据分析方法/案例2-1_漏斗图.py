# -*- coding: utf-8 -*-
"""
案例 2-1　漏斗图（链式分析 / 转化率）—— 迁移为 Python
================================================================
教材：第 2 章 2.1.2 链式分析   原案例：2-1漏斗图.xlsx

【项目内涵】
漏斗分析把用户行为拆成一条自上而下的路径（浏览→收藏→加购→下单→支付），
逐环节计算转化率，定位流失最严重的环节，从而针对性优化。
"""
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

matplotlib.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]
matplotlib.rcParams["axes.unicode_minus"] = False

BASE = Path(__file__).resolve().parent.parent / "data" / "1《CDA 一级认证教材：商业数据分析》" / "第2章 数据分析方法/1、分析的基础范式"
DATA = BASE / "data-无答案/2-1漏斗图.xlsx"
OUT = Path(__file__).resolve().parent

# 使用"演示"表：阶段 / 用户数 / 转化率
df = pd.read_excel(DATA, sheet_name="演示", header=2)   # 表头在第3行
df.columns = ["阶段", "用户数", "转化率"]
df = df.dropna(subset=["用户数"])

fig, ax = plt.subplots(figsize=(8, 6))
y = range(len(df))
maxv = df["用户数"].max()
for i, (_, r) in enumerate(df.iterrows()):
    ax.barh(i, r["用户数"], color=plt.cm.Blues(0.4 + 0.5 * i / len(df)))
    ax.text(r["用户数"] + maxv * 0.02, i, f"{r['用户数']}（转化 {r['转化率']:.0%}）", va="center")
ax.set_yticks(list(y), df["阶段"])
ax.set_xlabel("用户数")
ax.set_title("漏斗图：用户行为各阶段转化", fontsize=14, fontweight="bold")
ax.invert_yaxis()
fig.savefig(OUT / "图2-1_漏斗图.png", dpi=150, bbox_inches="tight", facecolor="white")
plt.close(fig)

print("各阶段用户数与转化率：")
print(df.to_string(index=False))
print("\n图已保存到", OUT / "图2-1_漏斗图.png")

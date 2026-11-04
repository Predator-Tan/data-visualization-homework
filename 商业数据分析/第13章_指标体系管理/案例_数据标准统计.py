# -*- coding: utf-8 -*-
"""第13章 指标体系管理 —— 银行数据标准分布统计 迁移为 Python
教材第13章：基础数据标准编制模板.xlsx 含"标准分布统计"透视表
（各业务部门 × 数据主题 的标准数量），本文件用 Python 复现并可视化。"""
import pandas as pd, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
matplotlib.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]
matplotlib.rcParams["axes.unicode_minus"] = False
BASE = Path(__file__).resolve().parent.parent / "data" / "1《CDA 一级认证教材：商业数据分析》" / "第13章 指标体系管理"
OUT = Path(__file__).resolve().parent

df = pd.read_excel(BASE / "1、基础数据标准编制模板.xlsx", sheet_name="标准分布统计", header=3)
df = df.rename(columns={df.columns[0]: "数据主题"})
df = df[df["数据主题"].notna() & (df["数据主题"] != "Grand Total")]   # 去掉合计行
# 数值列转数字
num_cols = [c for c in df.columns if c != "数据主题" and "Grand" not in str(c)]
for c in num_cols:
    df[c] = pd.to_numeric(df[c], errors="coerce")
df = df.set_index("数据主题")[num_cols].fillna(0)

# 各数据主题总数
total = df.sum(axis=1)

fig, axes = plt.subplots(1, 2, figsize=(14, 6))
axes[0].bar(total.index, total.values, color="#4E79A7")
axes[0].set_title("各数据主题的标准数量")
axes[0].set_ylabel("标准数量")
for i, v in enumerate(total.values):
    axes[0].text(i, v, str(int(v)), ha="center", va="bottom")
# 热力图：部门 × 主题
sns.heatmap(df, annot=True, fmt=".0f", cmap="YlGnBu", ax=axes[1],
            cbar_kws={"label": "标准数量"})
axes[1].set_title("各部门 × 数据主题 标准分布")
axes[1].tick_params(axis="x", rotation=45)
fig.suptitle("银行数据标准分布统计", fontsize=15, fontweight="bold")
fig.tight_layout()
fig.savefig(OUT / "图13-1_数据标准统计.png", dpi=150, bbox_inches="tight", facecolor="white"); plt.close(fig)

print("各数据主题标准数量：", dict(total.astype(int)))
print("标准数量最多的部门：", df.sum(axis=0).idxmax(), f"（{int(df.sum(axis=0).max())}个）")

# -*- coding: utf-8 -*-
"""第2章 PowerBI 函数练习（学生考试案例）—— 迁移为 Python
教材第2章 5、PowerBI基本操作/函数练习/学生考试案例：考试成绩分析
（平均分/最高分/及格率），用 pandas 等价实现 DAX 聚合。"""
import pandas as pd, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from pathlib import Path
matplotlib.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]
matplotlib.rcParams["axes.unicode_minus"] = False
BASE = Path(__file__).resolve().parent.parent / "data" / "1《CDA 一级认证教材：商业数据分析》" / "第2章 数据分析方法/5、PowerBI基本操作/函数练习文件/学生考试案例"
OUT = Path(__file__).resolve().parent

df = pd.read_excel(BASE / "考试记录.xlsx")
for c in ["语文", "数学", "英语"]:
    df[c] = pd.to_numeric(df[c], errors="coerce")

# 各科统计
stat = df[["语文", "数学", "英语"]].agg(["mean", "max", "min"]).round(1)
stat.loc["及格率"] = (df[["语文", "数学", "英语"]] >= 60).mean().round(2)
# 每位学生总分排名
df["总分"] = df[["语文", "数学", "英语"]].sum(axis=1)
df["排名"] = df["总分"].rank(ascending=False, method="min").astype(int)

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
stat.loc[["mean", "max"]].T.plot(kind="bar", ax=axes[0], color=["#4E79A7", "#F28E2B"])
axes[0].set_title("各科平均分/最高分")
axes[0].set_ylabel("分数")
df["总分"].hist(bins=15, ax=axes[1], color="#59A14F", edgecolor="white")
axes[1].set_title("总分分布"); axes[1].set_xlabel("总分")
fig.suptitle("学生考试案例分析", fontsize=14, fontweight="bold")
fig.tight_layout()
fig.savefig(OUT / "图2-案例7_学生考试分析.png", dpi=150, bbox_inches="tight", facecolor="white"); plt.close(fig)

print("学生考试成绩分析：")
print(stat.to_string())
print(f"\n总分第一名：学号 {df.loc[df['总分'].idxmax(), '学号']}（{df['总分'].max():.0f} 分）")

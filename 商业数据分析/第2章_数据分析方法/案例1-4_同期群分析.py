# -*- coding: utf-8 -*-
"""
案例 1-4　同期群分析（留存率）—— 迁移为 Python
================================================================
教材：第 2 章 2.1.1 分类分析   原案例：1-4同期群分析.xlsx

【项目内涵】
按"注册日期"把用户分成同期群（cohort），观察每群用户在注册后
第 1 日、第 2 日……第 N 日的留存率（留存率 = 留存用户数 / 新增用户数），
从而衡量用户粘性与流失节奏。留存率高的群说明拉新质量好。
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

matplotlib.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]
matplotlib.rcParams["axes.unicode_minus"] = False

BASE = Path(__file__).resolve().parent.parent / "data" / "1《CDA 一级认证教材：商业数据分析》" / "第2章 数据分析方法/1、分析的基础范式"
DATA = BASE / "data-无答案/1-4同期群分析.xlsx"
OUT = Path(__file__).resolve().parent

df = pd.read_excel(DATA, sheet_name="用户登录明细")
df["注册日期"] = pd.to_datetime(df["注册日期"]).dt.normalize()
df["登录日期"] = pd.to_datetime(df["登录时点"]).dt.normalize()
# 第几日 = 登录日期 - 注册日期（天数），当日=第0日，次日=第1日
df["第几日"] = (df["登录日期"] - df["注册日期"]).dt.days

# 每日新增（注册）用户数
cohort_size = df.groupby("注册日期")["用户编号"].nunique()

# 留存矩阵：每个注册日 × 第几日 → 当日登录的独立用户数
matrix = df.groupby(["注册日期", "第几日"])["用户编号"].nunique().unstack()
retention = matrix.divide(cohort_size, axis=0)   # 留存率

# 只保留 0~15 日
retention = retention[[c for c in retention.columns if 0 <= c <= 15]]

# 画留存热力图
fig, ax = plt.subplots(figsize=(12, 5))
sns.heatmap(retention * 100, annot=False, cmap="YlGnBu", cbar_kws={"label": "留存率 %"}, ax=ax)
ax.set_title("同期群分析：按注册日期的留存率热力图", fontsize=14, fontweight="bold")
ax.set_xlabel("注册后第几日")
ax.set_ylabel("注册日期（同期群）")
fig.savefig(OUT / "图1-4_同期群分析.png", dpi=150, bbox_inches="tight", facecolor="white")
plt.close(fig)

# 次日、第7日平均留存率
print("注册用户总数：", cohort_size.sum())
print("次日平均留存率：", round(retention[1].mean() * 100, 1), "%")
print("第7日平均留存率：", round(retention[7].mean() * 100, 1), "%")
print("\n图已保存到", OUT / "图1-4_同期群分析.png")

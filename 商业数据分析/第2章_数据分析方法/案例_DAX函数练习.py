# -*- coding: utf-8 -*-
"""第2章 PowerBI 函数练习（人力案例）—— 迁移为 Python
教材第2章 5、PowerBI基本操作/函数练习/人力案例：用 DAX 函数做人力分析。
本文件用 pandas 等价实现：部门人数、平均职级、学历分布、在职状态。"""
import pandas as pd, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from pathlib import Path
matplotlib.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]
matplotlib.rcParams["axes.unicode_minus"] = False
BASE = Path(__file__).resolve().parent.parent / "data" / "1《CDA 一级认证教材：商业数据分析》" / "第2章 数据分析方法/5、PowerBI基本操作/函数练习文件/人力案例"
OUT = Path(__file__).resolve().parent

df = pd.read_excel(BASE / "员工信息.xlsx")
df["职级"] = pd.to_numeric(df["职级"], errors="coerce")

# DAX 函数 → pandas 等价
dept = df.groupby("部门").agg(人数=("员工工号", "count"), 平均职级=("职级", "mean")).round(1)
edu = df["文化程度"].value_counts()
status = df["员工状态"].value_counts()

fig, axes = plt.subplots(1, 3, figsize=(14, 5))
dept["人数"].sort_values().plot(kind="barh", ax=axes[0], color="#4E79A7")
axes[0].set_title("各部门人数")
edu.plot(kind="pie", autopct="%.1f%%", ax=axes[1])
axes[1].set_title("文化程度分布")
status.plot(kind="bar", ax=axes[2], color="#F28E2B")
axes[2].set_title("在职状态")
fig.suptitle("人力案例：DAX 函数 → pandas 等价实现", fontsize=14, fontweight="bold")
fig.tight_layout()
fig.savefig(OUT / "图2-案例3_人力分析.png", dpi=150, bbox_inches="tight", facecolor="white"); plt.close(fig)

print("人力案例完成：")
print("  部门人数：", dict(dept["人数"]))
print("  文化程度：", dict(edu))
print("  在职状态：", dict(status))

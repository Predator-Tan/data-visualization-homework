# -*- coding: utf-8 -*-
"""
《Excel数据可视化》第四章 人力资源可视化看板 迁移为 Python
================================================================
原书用 Excel 制作人力资源可视化看板，本文件用 matplotlib 复现：
KPI（总人数）+ 部门人数 + 年龄段 + 学历 + 性别 + 婚姻状况 多图组合大屏。
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

matplotlib.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]
matplotlib.rcParams["axes.unicode_minus"] = False

BASE = Path(__file__).resolve().parent.parent / "data"
OUT = Path(__file__).resolve().parent / "figures"
PALETTE = ["#4E79A7", "#F28E2B", "#E15759", "#76B7B2", "#59A14F", "#EDC948"]

df = pd.read_excel(BASE / "第四章 人力资源可视化看板.xlsx", sheet_name="202203人员基础信息")
df = df.dropna(subset=["员工编号"])

# 大屏布局：标题 + KPI + 2x3 图表
fig = plt.figure(figsize=(16, 9), facecolor="#F7F9FC")
fig.suptitle("人力资源可视化看板", fontsize=20, fontweight="bold", y=0.98)

# KPI
total = len(df)
ax_kpi = fig.add_axes([0.05, 0.86, 0.9, 0.08])
ax_kpi.axis("off")
ax_kpi.text(0.02, 0.5, f"员工总数：{total} 人", fontsize=18, fontweight="bold",
            va="center", color=PALETTE[0])
ax_kpi.text(0.5, 0.5, f"部门数：{df['部门'].nunique()} 个", fontsize=15, va="center")
ax_kpi.text(0.75, 0.5, f"平均年龄：{pd.to_numeric(df['年龄'], errors='coerce').mean():.0f} 岁",
            fontsize=15, va="center")

# 1 部门人数
ax1 = fig.add_subplot(2, 3, 1)
df["部门"].value_counts().plot(kind="bar", ax=ax1, color=PALETTE[0])
ax1.set_title("各部门人数"); ax1.tick_params(axis="x", rotation=45)

# 2 年龄段
ax2 = fig.add_subplot(2, 3, 2)
df["年龄段"].value_counts().plot(kind="pie", autopct="%.1f%%", ax=ax2)
ax2.set_title("年龄段分布"); ax2.set_ylabel("")

# 3 学历
ax3 = fig.add_subplot(2, 3, 3)
df["学历"].value_counts().plot(kind="bar", ax=ax3, color=PALETTE[3])
ax3.set_title("学历分布")

# 4 性别
ax4 = fig.add_subplot(2, 3, 4)
df["性别"].value_counts().plot(kind="pie", autopct="%.1f%%", ax=ax4,
                               colors=[PALETTE[0], PALETTE[2]])
ax4.set_title("性别分布"); ax4.set_ylabel("")

# 5 婚姻状况
ax5 = fig.add_subplot(2, 3, 5)
df["婚姻状况"].value_counts().plot(kind="bar", ax=ax5, color=PALETTE[1])
ax5.set_title("婚姻状况")

# 6 本月入转调
ax6 = fig.add_subplot(2, 3, 6)
df["本月入转调"].fillna("无").value_counts().plot(kind="bar", ax=ax6, color=PALETTE[4])
ax6.set_title("本月入转调")

fig.tight_layout(rect=[0, 0, 1, 0.85])
fig.savefig(OUT / "大屏1_人力资源看板.png", dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
plt.close(fig)

print("人力资源看板完成：")
print(f"  员工总数 {total} 人，部门 {df['部门'].nunique()} 个")
print("  部门分布：", dict(df["部门"].value_counts().head(5)))
print("图已保存到", OUT / "大屏1_人力资源看板.png")

# -*- coding: utf-8 -*-
"""第5章 WPS 归因分析案例（银行）—— 迁移为 Python
教材第5章：贷款申请量按渠道/月度归因，定位业务变化的驱动因素。"""
import pandas as pd, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from pathlib import Path
matplotlib.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]
matplotlib.rcParams["axes.unicode_minus"] = False
BASE = Path(__file__).resolve().parent.parent / "data" / "1《CDA 一级认证教材：商业数据分析》" / "第5章 业务数据分析/第5章 WPS归因分析案例-银行案例"
OUT = Path(__file__).resolve().parent

df = pd.read_excel(BASE / "归因分析数据.xlsx", sheet_name="贷款申请表")
df["申请日期"] = pd.to_datetime(df["申请日期"])
df["月份"] = df["申请日期"].dt.to_period("M").astype(str)

# 1. 渠道分布
channel = df["申请渠道"].value_counts()
# 2. 月度申请趋势（按渠道）
monthly = df.pivot_table(index="月份", columns="申请渠道", values="申请书编号（主键）", aggfunc="count", fill_value=0)

fig, axes = plt.subplots(1, 2, figsize=(13, 5))
axes[0].pie(channel.values, labels=channel.index, autopct="%.1f%%", startangle=90)
axes[0].set_title("贷款申请渠道分布")
monthly.plot(kind="bar", stacked=True, ax=axes[1])
axes[1].set_title("各渠道月度申请量（归因）"); axes[1].set_ylabel("申请量")
axes[1].tick_params(axis="x", rotation=45)
fig.suptitle("贷款申请归因分析", fontsize=14, fontweight="bold")
fig.tight_layout()
fig.savefig(OUT / "图5-2_归因分析.png", dpi=150, bbox_inches="tight", facecolor="white"); plt.close(fig)

print("归因分析完成：")
print("  渠道分布：", dict(channel))
print("  申请量最高的月份：", monthly.sum(axis=1).idxmax(), f"（{monthly.sum(axis=1).max()}笔）")

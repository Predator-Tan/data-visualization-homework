# -*- coding: utf-8 -*-
"""
案例 1-2　RFM 模型（用户价值八分类）—— 原 Excel/Power BI 案例迁移为 Python
================================================================
教材：CDA 一级认证教材《商业数据分析（第4版）》第 2 章 2.1.1 分类分析
原案例：1-2RFM模型.xlsx

【项目内涵】
RFM 用三个指标衡量用户价值：R（最近一次消费距今的时间间隔，越小越好）、
F（消费频次，越大越好）、M（消费金额，越大越好）。以三项指标的均值为阈值，
把用户分成 2×2×2=8 类（重要价值、重要发展、重要保持、重要挽留、
一般价值、一般发展、一般保持、一般挽留），用于对不同价值用户差异化运营。

【本文件做法】
分析时点取 2019-08-03，逐用户计算 R/F/M，用均值切分高低，映射到八类，
统计各类人数并绘制气泡图。
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

matplotlib.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]
matplotlib.rcParams["axes.unicode_minus"] = False

BASE = Path(__file__).resolve().parent.parent / "data" / "1《CDA 一级认证教材：商业数据分析》" / "第2章 数据分析方法/1、分析的基础范式"
DATA = BASE / "data-无答案/1-2RFM模型.xlsx"
OUT = Path(__file__).resolve().parent
REF_TIME = pd.Timestamp("2019-08-03")   # 分析时点

# 1. 读入并清洗
df = pd.read_excel(DATA, sheet_name="原始数据")
df["销售日期"] = pd.to_datetime(df["销售日期"])
df["销售金额"] = pd.to_numeric(df["销售金额"], errors="coerce")

# 2. 逐用户计算 R/F/M
rfm = df.groupby("用户编号").agg(
    R=("销售日期", lambda s: (REF_TIME - s.max()).days),  # 消费时间间隔
    F=("流水号", "nunique"),                              # 消费频次（不同订单次数）
    M=("销售金额", "sum"),                                # 消费金额
).reset_index()

# 3. 均值阈值切分（与参考答案一致）
r_m, f_m, m_m = rfm["R"].mean(), rfm["F"].mean(), rfm["M"].mean()
rfm["R程度"] = np.where(rfm["R"] <= r_m, "高", "低")   # 间隔小=最近活跃=高
rfm["F程度"] = np.where(rfm["F"] > f_m, "高", "低")
rfm["M程度"] = np.where(rfm["M"] > m_m, "高", "低")

# 4. 八分类映射
seg_map = {
    ("高","高","高"): "重要价值用户", ("高","低","高"): "重要发展用户",
    ("低","高","高"): "重要保持用户", ("低","低","高"): "重要挽留用户",
    ("高","高","低"): "一般价值用户", ("高","低","低"): "一般发展用户",
    ("低","高","低"): "一般保持用户", ("低","低","低"): "一般挽留用户",
}
rfm["用户类别"] = list(zip(rfm["R程度"], rfm["F程度"], rfm["M程度"]))
rfm["用户类别"] = rfm["用户类别"].map(seg_map)

# 5. 结果统计
dist = rfm["用户类别"].value_counts()
print("R均值=%.4f  F均值=%.4f  M均值=%.4f" % (r_m, f_m, m_m))
print("\n八类用户分布：")
for k, v in dist.items():
    print(f"  {k}：{v} 人（{v/len(rfm):.1%}）")

# 6. 气泡图（X=间隔，Y=金额，气泡大小=频次，颜色=类别）
fig, ax = plt.subplots(figsize=(10, 6))
for cat, grp in rfm.groupby("用户类别"):
    ax.scatter(grp["R"], grp["M"], s=grp["F"] * 3, alpha=0.5, label=f"{cat}({len(grp)})")
ax.axvline(r_m, color="gray", ls="--", lw=1)
ax.axhline(m_m, color="gray", ls="--", lw=1)
ax.set_xlabel("消费时间间隔 R（天）")
ax.set_ylabel("消费金额 M（元）")
ax.set_title("RFM 模型：用户价值八分类（气泡=消费频次）", fontsize=14, fontweight="bold")
ax.legend(loc="upper right", fontsize=7, ncol=2)
fig.savefig(OUT / "图1-2_RFM模型.png", dpi=150, bbox_inches="tight", facecolor="white")
plt.close(fig)
print("\n图已保存到", OUT / "图1-2_RFM模型.png")

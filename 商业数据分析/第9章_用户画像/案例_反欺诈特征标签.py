# -*- coding: utf-8 -*-
"""第9章 标签体系参考（反欺诈特征列表）—— 迁移为 Python
教材第9章 标签体系参考/操作风险类标签/反欺诈特征列表.xlsx：
线上APP营销获客的反欺诈特征字段。本文件统计特征类型（是否衍生）并展示。"""
import pandas as pd, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from pathlib import Path
matplotlib.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]
matplotlib.rcParams["axes.unicode_minus"] = False
BASE = Path(__file__).resolve().parent.parent / "data" / "1《CDA 一级认证教材：商业数据分析》" / "第9章 用户标签体系与用户画像专题/标签体系参考/操作风险类标签"
OUT = Path(__file__).resolve().parent

df = pd.read_excel(BASE / "反欺诈特征列表.xlsx", header=1)
df = df.dropna(subset=["序号"])

# 是否衍生 分布
derived = df["是否衍生"].value_counts()

fig, ax = plt.subplots(figsize=(7, 5))
ax.pie(derived.values, labels=[f"{'衍生' if k=='是' else '基础'}特征({v})" for k, v in derived.items()],
       autopct="%.1f%%", startangle=90, colors=["#F28E2B", "#4E79A7"])
ax.set_title("反欺诈特征列表：基础特征 vs 衍生特征", fontsize=13, fontweight="bold")
fig.savefig(OUT / "图9-2_反欺诈特征.png", dpi=150, bbox_inches="tight", facecolor="white"); plt.close(fig)

print("反欺诈特征列表：")
print(f"  特征总数：{len(df)} 个，其中衍生特征 {int(derived.get('是', 0))} 个、基础特征 {int(derived.get('否', 0))} 个")
print("  示例特征：", list(df["字段名"].head(8)))

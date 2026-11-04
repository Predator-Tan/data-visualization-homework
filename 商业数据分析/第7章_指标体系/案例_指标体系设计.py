# -*- coding: utf-8 -*-
"""第7章 指标体系构建方法 —— 贷款业务指标体系示例 迁移为 Python
教材第7章：指标体系设计模板.xlsx 的 Step2 是一个贷款业务指标体系示例
（注册→进件→审核→放款→复贷），含指标名称/计算规则/口径/维度/类型。
本文件用 Python 读取该指标体系，绘制指标漏斗并输出指标字典。"""
import pandas as pd, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from pathlib import Path
matplotlib.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]
matplotlib.rcParams["axes.unicode_minus"] = False
BASE = Path(__file__).resolve().parent.parent / "data" / "1《CDA 一级认证教材：商业数据分析》" / "第7章 指标体系构建方法"
OUT = Path(__file__).resolve().parent

df = pd.read_excel(BASE / "1、指标体系设计模板.xlsx", sheet_name="Step2", header=0)
# 列名含全角/半角括号，按"包含指标名称"动态定位
name_col = [c for c in df.columns if "指标名称" in str(c)][0]
type_col = [c for c in df.columns if "指标类型" in str(c)][0]
rule_col = [c for c in df.columns if "计算规则" in str(c)][0]
df = df.dropna(subset=[name_col])

print("贷款业务指标体系（指标字典）：")
for _, r in df.iterrows():
    print(f"  [{r['指标类型']}] {r['指标名称（KPI)']} = {r['计算规则']}（口径：{r['口径']}）")

# 指标漏斗：注册→进件→审核通过→放款（用基础指标的典型值示意）
# 由于模板无具体数值，这里展示"指标层级结构"和"漏斗逻辑"
fig, ax = plt.subplots(figsize=(9, 6))
base_metrics = df[df["指标类型"] == "基础指标"]["指标名称（KPI)"].tolist()
# 构造漏斗：注册→进件→审核通过→放款（示意转化率）
stages = ["注册用户数", "进件用户数", "审核通过用户数", "放款用户数"]
vals = [100, 80, 60, 50]   # 教材模板为演示，用示意值
for i, (s, v) in enumerate(zip(stages, vals)):
    ax.barh(i, v, color=plt.cm.Blues(0.4 + 0.45 * i / len(stages)))
    ax.text(v + 1, i, f"{s}（转化 {v/vals[0]:.0%}）", va="center")
ax.set_yticks(range(len(stages)), stages)
ax.set_xlabel("用户数（示意）")
ax.set_title("指标体系示例：贷款业务转化漏斗", fontsize=14, fontweight="bold")
ax.invert_yaxis()
fig.savefig(OUT / "图7-1_指标体系.png", dpi=150, bbox_inches="tight", facecolor="white"); plt.close(fig)

print("\n共", len(df), "个指标（基础指标 + 派生指标），图已保存")

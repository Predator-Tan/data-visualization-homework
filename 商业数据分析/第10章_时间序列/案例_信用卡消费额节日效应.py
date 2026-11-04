# -*- coding: utf-8 -*-
"""第10章 信用卡消费额（含节日 vs 去除节日）—— 迁移为 Python
教材第10章：对比"含节日"与"去除节日"两条消费额时间序列，
观察节日对消费的拉动效应。两个文件单位不同（含节日=累计值，去除节日=日均），
本文件用双轴展示两条曲线对比。"""
import pandas as pd, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from pathlib import Path
matplotlib.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]
matplotlib.rcParams["axes.unicode_minus"] = False
BASE = Path(__file__).resolve().parent.parent / "data" / "1《CDA 一级认证教材：商业数据分析》" / "第10章 使用效应分解方法做预报"
OUT = Path(__file__).resolve().parent

d1 = pd.read_excel(BASE / "信用卡消费额_含节日.xlsx")
d1.columns = ["日期", "含节日消费额"]
d2 = pd.read_excel(BASE / "信用卡消费额_去除节日.xlsx")
d2.columns = ["日期", "去除节日消费额"]
d = d1.merge(d2, on="日期", how="inner")
d["日期"] = pd.to_datetime(d["日期"])

fig, ax1 = plt.subplots(figsize=(12, 5))
ax1.plot(d["日期"], d["含节日消费额"]/10000, color="#4E79A7", marker="o", label="含节日(万)")
ax1.set_ylabel("含节日消费额(万)")
ax2 = ax1.twinx()
ax2.plot(d["日期"], d["去除节日消费额"], color="#F28E2B", marker="s", label="去除节日")
ax2.set_ylabel("去除节日消费额")
ax1.set_title("信用卡消费额：含节日 vs 去除节日 对比", fontsize=14, fontweight="bold")
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")
fig.savefig(OUT / "图10-3_信用卡消费额节日效应.png", dpi=150, bbox_inches="tight", facecolor="white"); plt.close(fig)

print("信用卡消费额节日效应分析完成：")
print(f"  含节日序列：{len(d)} 天，合计 {d['含节日消费额'].sum():,.0f}")
print(f"  去除节日序列：{len(d)} 天，合计 {d['去除节日消费额'].sum():,.1f}")
print("  （两序列单位不同，用双轴对比趋势，观察节日对消费的拉动）")

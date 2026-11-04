# -*- coding: utf-8 -*-
"""案例2 财务费用分析 —— 原 Excel 案例迁移为 Python
教材第3章 3.4.2：三大期间费用（管理/销售/财务）构成与环比 + 管理费用明细项环比。"""
import pandas as pd, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from pathlib import Path
matplotlib.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]
matplotlib.rcParams["axes.unicode_minus"] = False
BASE = Path(__file__).resolve().parent.parent / "data" / "1《CDA 一级认证教材：商业数据分析》" / "第3章 商业数据分析框架"
OUT = Path(__file__).resolve().parent
f = BASE / "案例2：财务费用分析/案例2：财务费用分析-原始数据.xlsx"

fee = pd.read_excel(f, sheet_name="财务三大期间费用数据").iloc[:, :4]
fee.columns = ["年份", "月份", "期间费用项", "金额"]
fee["期间费用项"] = fee["期间费用项"].str.strip()

# 三大期间费用 6月 vs 7月
pivot = fee.pivot_table(index="期间费用项", columns="月份", values="金额", aggfunc="sum")
pivot["环比"] = (pivot[7] - pivot[6]) / pivot[6]

# 管理费用明细环比
mgr = pd.read_excel(f, sheet_name="管理费用数据").iloc[:, :4]
mgr.columns = ["年份", "月份", "管理费用项", "金额"]
mgr["月份"] = pd.to_numeric(mgr["月份"], errors="coerce")
mgr["金额"] = pd.to_numeric(mgr["金额"], errors="coerce")
mgr = mgr.dropna(subset=["月份", "金额"])
mgr_p = mgr.pivot_table(index="管理费用项", columns="月份", values="金额", aggfunc="sum")
mgr_p["环比"] = (mgr_p[7] - mgr_p[6]) / mgr_p[6]

fig, axes = plt.subplots(1, 2, figsize=(13, 5))
pivot[[6, 7]].plot(kind="bar", ax=axes[0], color=["#4E79A7", "#F28E2B"])
axes[0].set_title("三大期间费用：6月 vs 7月"); axes[0].set_ylabel("金额(元)")
mgr_p[[6, 7]].plot(kind="bar", ax=axes[1], color=["#4E79A7", "#F28E2B"])
axes[1].set_title("管理费用明细：6月 vs 7月"); axes[1].set_ylabel("金额(元)")
fig.suptitle("案例2：财务费用分析", fontsize=14, fontweight="bold")
fig.tight_layout()
fig.savefig(OUT / "图3-2_财务费用分析.png", dpi=150, bbox_inches="tight", facecolor="white"); plt.close(fig)

print("三大期间费用环比：")
print((pivot["环比"]*100).round(1).astype(str) + "%")
print("\n管理费用明细环比：")
print((mgr_p["环比"]*100).round(1).astype(str) + "%")

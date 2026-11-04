# -*- coding: utf-8 -*-
"""
06_dashboard_screenshot.py —— 数据大屏静态截图（供论文附录/加分材料使用）
================================================================
用 matplotlib 复刻 Streamlit 大屏的核心内容，生成一张专业的数据大屏图。
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path

matplotlib.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]
matplotlib.rcParams["axes.unicode_minus"] = False

ROOT = Path(__file__).resolve().parent.parent
CLEAN = ROOT / "data" / "clean"
OUT = ROOT / "outputs" / "figures"
OUT.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(CLEAN / "orders_clean.csv", parse_dates=["Order Date"])

C_BG = "#0E1A2B"          # 暗色大屏背景
C_CARD = "#1B2B44"        # 卡片底色
C_TEXT = "#E8EEF7"        # 主文字
C_SUB = "#8CA3C0"         # 次文字
C_ACCENT = "#4FC3F7"      # 强调色
C2 = "#FFB74D"; C3 = "#EF5350"; C4 = "#66BB6A"

fig = plt.figure(figsize=(20, 11), facecolor=C_BG)
fig.suptitle("Superstore 商业数据分析大屏", fontsize=28, fontweight="bold",
             color=C_TEXT, x=0.05, ha="left", y=0.97)
fig.text(0.05, 0.94, "数据源：Tableau 官方 Sample-Superstore（2023–2026）｜ 全 Python 实现",
         fontsize=12, color=C_SUB)

# ============ KPI 卡片行 ============
sales = df["Sales"].sum()
profit = df["Profit"].sum()
kpis = [
    ("总销售额", f"${sales/10000:.0f}万", C_ACCENT),
    ("总利润", f"${profit/10000:.0f}万", C4),
    ("利润率", f"{profit/sales:.1%}", C2),
    ("订单数", f"{df['Order ID'].nunique():,}", C_ACCENT),
    ("客户数", f"{df['Customer ID'].nunique():,}", C4),
    ("退货率", f"{(df['Returned']=='Yes').mean():.1%}", C3),
]
n = len(kpis)
for i, (label, value, color) in enumerate(kpis):
    x = 0.03 + i * (0.94 / n)
    ax = fig.add_axes([x, 0.80, 0.94/n - 0.012, 0.11])
    ax.set_facecolor(C_CARD)
    ax.text(0.5, 0.62, value, ha="center", va="center", fontsize=22,
            fontweight="bold", color=color, transform=ax.transAxes)
    ax.text(0.5, 0.18, label, ha="center", va="center", fontsize=12,
            color=C_SUB, transform=ax.transAxes)
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values(): s.set_visible(False)

# ============ 图表区（2x2） ============
grid = [(0.03, 0.42, 0.46, 0.32), (0.51, 0.42, 0.46, 0.32),
        (0.03, 0.05, 0.46, 0.32), (0.51, 0.05, 0.46, 0.32)]

def style_ax(ax, title):
    ax.set_facecolor(C_CARD)
    ax.set_title(title, color=C_TEXT, fontsize=14, fontweight="bold", loc="left")
    ax.tick_params(colors=C_SUB, labelsize=9)
    for s in ax.spines.values(): s.set_color("#33507A")
    ax.grid(color="#22385C", alpha=0.4, lw=0.6)

# 1 月度销售趋势
ax = fig.add_axes(grid[0])
m = df.groupby("订单月")["Sales"].sum()
m.index = pd.to_datetime(m.index)
ax.plot(m.index, m.values/10000, color=C_ACCENT, lw=2)
ax.fill_between(m.index, 0, m.values/10000, color=C_ACCENT, alpha=0.25)
style_ax(ax, "月度销售趋势（万美元）")

# 2 类别结构
ax = fig.add_axes(grid[1])
cat = df.groupby("Category")["Sales"].sum()
ax.pie(cat.values, labels=cat.index, autopct="%.1f%%", colors=[C_ACCENT, C2, C4],
       textprops={"color": C_TEXT}, wedgeprops=dict(width=0.4))
style_ax(ax, "类别销售结构")

# 3 区域销售
ax = fig.add_axes(grid[2])
reg = df.groupby("Region")["Sales"].sum().sort_values(ascending=False)
ax.bar(reg.index, reg.values/10000, color=[C_ACCENT, C2, C4, C3], alpha=0.85)
style_ax(ax, "各区域销售额（万美元）")

# 4 销售额-利润散点
ax = fig.add_axes(grid[3])
sample = df.sample(min(800, len(df)), random_state=42)
ax.scatter(sample["Sales"], sample["Profit"], s=8, alpha=0.5, c=C2)
ax.set_xlabel("销售额", color=C_SUB); ax.set_ylabel("利润", color=C_SUB)
style_ax(ax, "销售额 vs 利润 散点")

fig.savefig(OUT / "大屏截图.png", dpi=200, bbox_inches="tight", facecolor=C_BG)
plt.close(fig)
print("大屏截图已生成:", OUT / "大屏截图.png")

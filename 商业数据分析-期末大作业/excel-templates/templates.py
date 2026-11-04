# -*- coding: utf-8 -*-
"""
templates.py —— 《Excel数据可视化——从图表到数据大屏》模板复现
==============================================================
将书中的 Excel 图表模板，用 Python（Matplotlib）一一复现。
每个函数都标注了对应的书中模板编号，便于对照。

复现 12 个模板（书中共 30 个，此处选取代表性 12 个）：
  模板1  渐变柱形图        模板2  带均值柱形图
  模板5  层叠柱形图        模板6  蝴蝶图
  模板10 甘特图            模板11 平滑折线图
  模板13 对比折线图        模板14 单值圆环图
  模板20 南丁格尔圆环图    模板22 仪表盘图
  模板23 柱形折线图        模板28 滑珠图

运行方式：python excel-templates/templates.py
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.patches import Wedge
from pathlib import Path
from scipy.interpolate import make_interp_spline

matplotlib.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]
matplotlib.rcParams["axes.unicode_minus"] = False

ROOT = Path(__file__).resolve().parent.parent
CLEAN = ROOT / "data" / "clean"
FIG = Path(__file__).resolve().parent / "figures"
FIG.mkdir(parents=True, exist_ok=True)

PALETTE = ["#4E79A7", "#F28E2B", "#E15759", "#76B7B2",
           "#59A14F", "#EDC948", "#B07AA1", "#FF9DA7", "#9C755F", "#BAB0AC"]


def save(fig, name):
    fig.savefig(FIG / name, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  已保存 {name}")


df = None  # 全局清洗后数据，懒加载


def load():
    global df
    if df is None:
        df = pd.read_csv(CLEAN / "orders_clean.csv", parse_dates=["Order Date", "Ship Date"])
    return df


# ============================================================
# 模板1：渐变柱形图（区域销售额，颜色随数值渐变）
# ============================================================
def t01_gradient_bar():
    d = load()
    reg = d.groupby("Region")["Sales"].sum().sort_values()
    fig, ax = plt.subplots(figsize=(8, 5))
    colors = cm.Blues(np.linspace(0.45, 0.9, len(reg)))   # 蓝系由浅到深
    ax.bar(reg.index, reg.values / 1000, color=colors)
    ax.set_ylabel("销售额（千美元）")
    ax.set_title("渐变柱形图：各区域销售额", fontsize=14, fontweight="bold")
    save(fig, "t01_渐变柱形图.png")


# ============================================================
# 模板2：带均值柱形图（类别销量 + 均值线）
# ============================================================
def t02_bar_with_mean():
    d = load()
    cat = d.groupby("Category")["Quantity"].sum()
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(cat.index, cat.values, color=PALETTE[0], alpha=0.8)
    ax.axhline(cat.mean(), color=PALETTE[2], linestyle="--", linewidth=2,
               label=f"均值 {cat.mean():.0f}")
    ax.set_ylabel("销量")
    ax.set_title("带均值柱形图：各类别销量", fontsize=14, fontweight="bold")
    ax.legend()
    save(fig, "t02_带均值柱形图.png")


# ============================================================
# 模板5：层叠柱形图（各区域 × 类别销售额）
# ============================================================
def t05_stacked_bar():
    d = load()
    pivot = d.pivot_table(index="Region", columns="Category",
                          values="Sales", aggfunc="sum")
    fig, ax = plt.subplots(figsize=(8, 5))
    bottom = np.zeros(len(pivot))
    for i, cat in enumerate(pivot.columns):
        ax.bar(pivot.index, pivot[cat] / 1000, bottom=bottom / 1000,
               color=PALETTE[i], label=cat)
        bottom += pivot[cat].values
    ax.set_ylabel("销售额（千美元）")
    ax.set_title("层叠柱形图：各区域 × 类别销售额", fontsize=14, fontweight="bold")
    ax.legend()
    save(fig, "t05_层叠柱形图.png")


# ============================================================
# 模板6：蝴蝶图（区域 2025 vs 2026 销售额，左右对称）
# ============================================================
def t06_butterfly():
    d = load()
    s = d[d["订单年"].isin([2025, 2026])].pivot_table(
        index="Region", columns="订单年", values="Sales", aggfunc="sum")
    fig, ax = plt.subplots(figsize=(8, 5))
    y = np.arange(len(s))
    ax.barh(y, s[2025] / 1000, height=0.35, color=PALETTE[0], label="2025")
    ax.barh(y, -s[2026] / 1000, height=0.35, color=PALETTE[3], label="2026")
    ax.set_yticks(y, s.index)
    ax.set_xlabel("销售额（千美元，2026 为负向）")
    ax.set_title("蝴蝶图：区域销售额 2025 vs 2026", fontsize=14, fontweight="bold")
    ax.axvline(0, color="black", linewidth=1)
    ax.legend()
    save(fig, "t06_蝴蝶图.png")


# ============================================================
# 模板10：甘特图（抽样订单的 下单→发货 时间跨度）
# ============================================================
def t10_gantt():
    d = load()
    sample = d.sample(15, random_state=42).sort_values("Order Date")
    fig, ax = plt.subplots(figsize=(10, 6))
    for i, (_, r) in enumerate(sample.iterrows()):
        start = r["Order Date"]
        days = (r["Ship Date"] - r["Order Date"]).days
        ax.barh(i, days, left=start, height=0.5, color=PALETTE[1], alpha=0.8)
        ax.text(start, i + 0.25, f"  {r['Ship Mode']}", va="center", fontsize=8)
    ax.set_yticks(range(len(sample)), [f"订单{i+1}" for i in range(len(sample))])
    ax.set_xlabel("时间（下单→发货）")
    ax.set_title("甘特图：订单处理周期（下单到发货）", fontsize=14, fontweight="bold")
    save(fig, "t10_甘特图.png")


# ============================================================
# 模板11：平滑折线图（月度销售额，平滑曲线）
# ============================================================
def t11_smooth_line():
    d = load()
    m = d.groupby("订单月")["Sales"].sum()
    x = np.arange(len(m))
    y = m.values / 1000
    xs = np.linspace(x.min(), x.max(), 300)
    ys = make_interp_spline(x, y, k=3)(xs)   # 三次样条平滑
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(m.index, y, "o", color=PALETTE[0], markersize=3, alpha=0.6, label="实际值")
    ax.plot(xs, ys, color=PALETTE[0], linewidth=2, label="平滑曲线")
    ax.set_ylabel("销售额（千美元）")
    ax.set_title("平滑折线图：月度销售额趋势", fontsize=14, fontweight="bold")
    ax.legend()
    save(fig, "t11_平滑折线图.png")


# ============================================================
# 模板13：对比折线图（三大类别月度销售额对比）
# ============================================================
def t13_compare_line():
    d = load()
    pivot = d.pivot_table(index="订单月", columns="Category",
                          values="Sales", aggfunc="sum")
    fig, ax = plt.subplots(figsize=(12, 5))
    for i, cat in enumerate(pivot.columns):
        ax.plot(pivot.index, pivot[cat] / 1000, color=PALETTE[i],
                linewidth=2, marker="o", markersize=3, label=cat)
    ax.set_ylabel("销售额（千美元）")
    ax.set_title("对比折线图：三大类别月度销售额", fontsize=14, fontweight="bold")
    ax.legend()
    save(fig, "t13_对比折线图.png")


# ============================================================
# 模板14：单值圆环图（总体利润率 KPI，中心显示数值）
# ============================================================
def t14_donut():
    d = load()
    margin = d["Profit"].sum() / d["Sales"].sum()
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie([margin, 1 - margin], startangle=90, counterclock=False,
           colors=[PALETTE[3], "#E8E8E8"], wedgeprops=dict(width=0.35))
    ax.text(0, 0, f"{margin:.1%}", ha="center", va="center",
            fontsize=30, fontweight="bold", color=PALETTE[0])
    ax.text(0, -0.28, "总体利润率", ha="center", va="center", fontsize=12)
    ax.set_title("单值圆环图：总体利润率", fontsize=14, fontweight="bold")
    save(fig, "t14_单值圆环图.png")


# ============================================================
# 模板20：南丁格尔圆环图（各区域销售额，极坐标玫瑰图）
# ============================================================
def t20_nightingale():
    d = load()
    reg = d.groupby("Region")["Sales"].sum()
    theta = np.linspace(0, 2 * np.pi, len(reg), endpoint=False)
    fig, ax = plt.subplots(figsize=(7, 7), subplot_kw={"projection": "polar"})
    width = 2 * np.pi / len(reg)
    colors = PALETTE[: len(reg)]
    ax.bar(theta, reg.values / 1000, width=width, bottom=0, color=colors, alpha=0.8)
    ax.set_xticks(theta, reg.index)
    ax.set_title("南丁格尔圆环图：各区域销售额", fontsize=14, fontweight="bold", pad=20)
    save(fig, "t20_南丁格尔圆环图.png")


# ============================================================
# 模板22：仪表盘图（利润率 vs 目标 15%）
# ============================================================
def t22_gauge():
    d = load()
    val = d["Profit"].sum() / d["Sales"].sum()
    target = 0.15
    fig, ax = plt.subplots(figsize=(7, 5), subplot_kw={"projection": "polar"})
    # 半圆仪表盘：0 ~ pi
    theta = np.linspace(0, np.pi, 100)
    ax.plot(theta, np.ones_like(theta) * 1.0, color="#E8E8E8", linewidth=18)
    # 已达标部分
    fill = np.linspace(0, np.pi * min(val / target, 1), 50)
    ax.plot(fill, np.ones_like(fill), color=PALETTE[3], linewidth=18)
    # 指针
    ax.plot([np.pi * (1 - val / target), np.pi * (1 - val / target)], [0, 1],
            color=PALETTE[2], linewidth=3)
    ax.set_ylim(0, 1.2)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines["polar"].set_visible(False)
    ax.text(np.pi / 2, 0.55, f"{val:.1%}", ha="center", fontsize=26,
            fontweight="bold", color=PALETTE[0])
    ax.text(np.pi / 2, 0.2, f"目标 {target:.0%}", ha="center", fontsize=11, color="gray")
    ax.set_title("仪表盘图：利润率目标达成", fontsize=14, fontweight="bold", pad=15)
    save(fig, "t22_仪表盘图.png")


# ============================================================
# 模板23：柱形折线图（月度销售额柱 + 利润率折线，双轴）
# ============================================================
def t23_bar_line():
    d = load()
    m = d.groupby("订单月").agg(销售额=("Sales", "sum"), 利润=("Profit", "sum"))
    m["利润率"] = m["利润"] / m["销售额"]
    fig, ax1 = plt.subplots(figsize=(12, 5))
    ax1.bar(m.index, m["销售额"] / 1000, color=PALETTE[0], alpha=0.7, label="销售额（千美元）")
    ax1.set_ylabel("销售额（千美元）")
    ax2 = ax1.twinx()
    ax2.plot(m.index, m["利润率"] * 100, color=PALETTE[2],
             linewidth=2, marker="o", markersize=3, label="利润率 %")
    ax2.set_ylabel("利润率 %")
    ax1.set_title("柱形折线图：月度销售额与利润率", fontsize=14, fontweight="bold")
    ax1.legend(loc="upper left")
    ax2.legend(loc="upper right")
    save(fig, "t23_柱形折线图.png")


# ============================================================
# 模板28：滑珠图（各区域利润率 最低 vs 最高）
# ============================================================
def t28_dumbbell():
    d = load()
    g = d.groupby(["Region", "订单年"]).agg(销售额=("Sales", "sum"), 利润=("Profit", "sum"))
    g["利润率"] = g["利润"] / g["销售额"]
    r = g["利润率"].unstack()   # 行=区域，列=年份
    fig, ax = plt.subplots(figsize=(8, 5))
    y = np.arange(len(r))
    for i, region in enumerate(r.index):
        lo, hi = r.loc[region].min(), r.loc[region].max()
        ax.hlines(i, lo, hi, color="gray", linewidth=2)
        ax.plot(lo, i, "o", color=PALETTE[0], markersize=10)
        ax.plot(hi, i, "o", color=PALETTE[2], markersize=10)
    ax.set_yticks(y, r.index)
    ax.set_xlabel("利润率")
    ax.set_title("滑珠图：各区域利润率区间（蓝=低点，红=高点）", fontsize=14, fontweight="bold")
    save(fig, "t28_滑珠图.png")


def main():
    print("开始复现《Excel数据可视化》模板……")
    t01_gradient_bar()
    t02_bar_with_mean()
    t05_stacked_bar()
    t06_butterfly()
    t10_gantt()
    t11_smooth_line()
    t13_compare_line()
    t14_donut()
    t20_nightingale()
    t22_gauge()
    t23_bar_line()
    t28_dumbbell()
    print(f"完成！共 12 个模板复现，输出到 excel-templates/figures/")


if __name__ == "__main__":
    main()

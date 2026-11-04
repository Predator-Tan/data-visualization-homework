# -*- coding: utf-8 -*-
"""
《Excel数据可视化》第二章 图表模板 22-30 迁移为 Python
  22 仪表盘图  23 柱形折线图  24 目标柱形图  25 子弹图  26 柱形圆
  27 簇状柱形折线图  28 复合柱形图  29 滑珠图  30 对比滑珠图
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
FIG = Path(__file__).resolve().parent / "figures"
PALETTE = ["#4E79A7", "#F28E2B", "#E15759", "#76B7B2", "#59A14F", "#EDC948", "#B07AA1"]
F2 = "第二章 图表(后15).xlsx"


def save(fig, name):
    fig.savefig(FIG / name, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  ✓ {name}")


def read(sheet, cols):
    raw = pd.read_excel(BASE / F2, sheet_name=sheet, header=None)
    h = 1
    for i in range(min(6, len(raw))):
        vals = [str(v) for v in raw.iloc[i].tolist()]
        if all(any(t in v for v in vals) for t in cols):
            h = i; break
    return pd.read_excel(BASE / F2, sheet_name=sheet, header=h)[cols]


def num(df, cols):
    for c in cols:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    return df.dropna()


# 22 仪表盘图（半圆仪表，指针指向 76）
def t22():
    df = read("22 仪表盘图", ["指针数值"])
    v = df["指针数值"].dropna().iloc[0] if len(df) else 76
    v = float(v)
    fig, ax = plt.subplots(figsize=(7, 5), subplot_kw={"projection": "polar"})
    theta = np.linspace(0, np.pi, 100)
    ax.plot(theta, np.ones_like(theta), color="#DDD", lw=16)          # 底环
    fill = np.linspace(0, np.pi * min(v/100, 1), 60)
    ax.plot(fill, np.ones_like(fill), color=PALETTE[3], lw=16)        # 进度
    ax.plot([np.pi*(1-v/100)]*2, [0, 1], color=PALETTE[2], lw=3)      # 指针
    ax.set_ylim(0, 1.3); ax.set_xticks([]); ax.set_yticks([])
    ax.spines["polar"].set_visible(False)
    ax.text(np.pi/2, 0.45, f"{v:.0f}", ha="center", fontsize=30, fontweight="bold")
    ax.set_title("模板22：仪表盘图", fontsize=14, fontweight="bold", pad=12)
    save(fig, "模板22_仪表盘图.png")


# 23 柱形折线图（双轴：柱=销售量，线=同比）
def t23():
    df = num(read("23 柱形折线图", ["年份", "销售量", "同比"]), ["销售量", "同比"])
    fig, ax1 = plt.subplots(figsize=(8, 5))
    ax1.bar(df["年份"].astype(str), df["销售量"], color=PALETTE[0], alpha=0.8, label="销售量")
    ax2 = ax1.twinx()
    ax2.plot(df["年份"].astype(str), df["同比"], "o-", color=PALETTE[2], label="同比")
    ax1.set_ylabel("销售量"); ax2.set_ylabel("同比")
    ax1.set_title("模板23：柱形折线图", fontsize=14, fontweight="bold")
    save(fig, "模板23_柱形折线图.png")


# 24 目标柱形图（实际 vs 目标）
def t24():
    df = num(read("24 目标柱形图", ["商品", "实际销量", "目标销量"]), ["实际销量", "目标销量"])
    fig, ax = plt.subplots(figsize=(8, 5))
    x = np.arange(len(df))
    ax.bar(x, df["实际销量"], width=0.5, color=PALETTE[0], label="实际")
    ax.bar(x, df["目标销量"], width=0.25, color="none", edgecolor=PALETTE[2], lw=2, label="目标")
    ax.set_xticks(x, df["商品"]); ax.legend()
    ax.set_title("模板24：目标柱形图", fontsize=14, fontweight="bold")
    save(fig, "模板24_目标柱形图.png")


# 25 子弹图
def t25():
    df = num(read("25 子弹图", ["商品", "实际", "目标", "及格", "良好", "优秀"]),
             ["实际", "目标", "及格", "良好", "优秀"])
    fig, ax = plt.subplots(figsize=(9, 5))
    y = np.arange(len(df))[::-1]
    for i, (yy, r) in enumerate(zip(y, df.iterrows())):
        _, row = r
        # 背景段：及格/良好/优秀 累积
        ax.barh(yy, row["及格"], color="#DDD", height=0.4)
        ax.barh(yy, row["良好"], left=row["及格"], color="#BBB", height=0.4)
        ax.barh(yy, row["优秀"], left=row["及格"]+row["良好"], color="#999", height=0.4)
        ax.barh(yy, row["实际"], color=PALETTE[0], height=0.2)
        ax.plot(row["目标"], yy, "|", color=PALETTE[2], ms=14, mew=3)
    ax.set_yticks(y, df["商品"]); ax.set_xlabel("销量")
    ax.set_title("模板25：子弹图", fontsize=14, fontweight="bold")
    save(fig, "模板25_子弹图.png")


# 26 柱形圆（环形柱状）
def t26():
    df = num(read("26 柱形圆", ["区域", "销量"]), ["销量"])
    mx = df["销量"].max()
    theta = np.linspace(0, 2*np.pi, len(df), endpoint=False)
    fig, ax = plt.subplots(figsize=(7, 7), subplot_kw={"projection": "polar"})
    ax.bar(theta, df["销量"], width=0.5, color=PALETTE[:len(df)], alpha=0.85)
    ax.set_xticks(theta, df["区域"])
    ax.set_title("模板26：柱形圆", fontsize=14, fontweight="bold", pad=20)
    save(fig, "模板26_柱形圆.png")


# 27 簇状柱形折线图（柱=2022/2021，线=同比）
def t27():
    df = num(read("27 簇状柱形折线图", ["区域", "2022销量", "2021销量", "同比去年"]),
             ["2022销量", "2021销量", "同比去年"])
    fig, ax1 = plt.subplots(figsize=(8, 5))
    x = np.arange(len(df))
    ax1.bar(x-0.2, df["2022销量"], width=0.4, color=PALETTE[0], label="2022")
    ax1.bar(x+0.2, df["2021销量"], width=0.4, color=PALETTE[3], label="2021")
    ax2 = ax1.twinx()
    ax2.plot(x, df["同比去年"], "o-", color=PALETTE[2], label="同比")
    ax1.set_xticks(x, df["区域"]); ax1.legend(loc="upper left")
    ax1.set_title("模板27：簇状柱形折线图", fontsize=14, fontweight="bold")
    save(fig, "模板27_簇状柱形折线图.png")


# 28 复合柱形图（月度 + 季度）
def t28():
    df = num(read("28 复合柱形图", ["月份", "月度销量", "季度销量"]), ["月度销量", "季度销量"])
    fig, ax = plt.subplots(figsize=(8, 5))
    x = np.arange(len(df))
    ax.bar(x, df["月度销量"], width=0.4, color=PALETTE[0], label="月度销量")
    ax.bar(x, df["季度销量"], width=0.4, bottom=df["月度销量"], color=PALETTE[4], label="季度销量")
    ax.set_xticks(x, df["月份"]); ax.legend()
    ax.set_title("模板28：复合柱形图", fontsize=14, fontweight="bold")
    save(fig, "模板28_复合柱形图.png")


# 29 滑珠图（完成率位置）
def t29():
    df = num(read("29 滑珠图", ["区域", "完成率"]), ["完成率"])
    fig, ax = plt.subplots(figsize=(8, 5))
    y = np.arange(len(df))
    ax.hlines(y, 0, 1, color="#DDD", lw=6)              # 轨道
    ax.plot(df["完成率"], y, "o", color=PALETTE[0], ms=14)  # 滑珠
    ax.set_yticks(y, df["区域"]); ax.set_xlim(0, 1)
    ax.set_title("模板29：滑珠图", fontsize=14, fontweight="bold")
    save(fig, "模板29_滑珠图.png")


# 30 对比滑珠图（2022 vs 2021 完成率）
def t30():
    df = num(read("30 对比滑珠图", ["区域", "2022完成率", "2021完成率"]), ["2022完成率", "2021完成率"])
    fig, ax = plt.subplots(figsize=(8, 5))
    y = np.arange(len(df))
    for i, (yy, r) in enumerate(zip(y, df.iterrows())):
        _, row = r
        ax.hlines(yy, row["2021完成率"], row["2022完成率"], color="gray", lw=2)
        ax.plot(row["2021完成率"], yy, "o", color=PALETTE[3], ms=11, label="2021" if i == 0 else "")
        ax.plot(row["2022完成率"], yy, "o", color=PALETTE[0], ms=11, label="2022" if i == 0 else "")
    ax.set_yticks(y, df["区域"]); ax.set_xlim(0, 1); ax.legend()
    ax.set_title("模板30：对比滑珠图", fontsize=14, fontweight="bold")
    save(fig, "模板30_对比滑珠图.png")


if __name__ == "__main__":
    print("开始复现模板 22-30……")
    t22(); t23(); t24(); t25(); t26(); t27(); t28(); t29(); t30()
    print("模板 22-30 完成，图见 figures/")

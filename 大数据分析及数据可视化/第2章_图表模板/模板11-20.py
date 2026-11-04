# -*- coding: utf-8 -*-
"""
《Excel数据可视化》第二章 图表模板 11-20 迁移为 Python
  11 平滑折线图  12 菱形走势图  13 对比折线图  14 单值圆环图  15 水球图
  16 波浪水球图  17 玉玦图      18 跑道图      19 南丁格尔圆饼图 20 南丁格尔圆环图
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.interpolate import make_interp_spline

matplotlib.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]
matplotlib.rcParams["axes.unicode_minus"] = False

BASE = Path(__file__).resolve().parent.parent / "data"
FIG = Path(__file__).resolve().parent / "figures"
PALETTE = ["#4E79A7", "#F28E2B", "#E15759", "#76B7B2", "#59A14F", "#EDC948", "#B07AA1"]
F1 = "第二章 图表(前15).xlsx"
F2 = "第二章 图表(后15).xlsx"


def save(fig, name):
    fig.savefig(FIG / name, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  ✓ {name}")


def read(file, sheet, cols):
    raw = pd.read_excel(BASE / file, sheet_name=sheet, header=None)
    h = 1
    for i in range(min(6, len(raw))):
        vals = [str(v) for v in raw.iloc[i].tolist()]
        if all(any(t in v for v in vals) for t in cols):
            h = i; break
    return pd.read_excel(BASE / file, sheet_name=sheet, header=h)[cols]


def num(df, cols):
    for c in cols:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    return df.dropna()


# 11 平滑折线图
def t11():
    df = num(read(F1, "11 平滑折线图", ["月份", "销量"]), ["销量"])
    x = np.arange(len(df)); y = df["销量"].values
    xs = np.linspace(x.min(), x.max(), 200)
    ys = make_interp_spline(x, y, k=3)(xs)
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(df["月份"], y, "o", color=PALETTE[0])
    ax.plot(xs, ys, color=PALETTE[0], lw=2)
    ax.set_title("模板11：平滑折线图", fontsize=14, fontweight="bold")
    save(fig, "模板11_平滑折线图.png")


# 12 菱形走势图
def t12():
    df = num(read(F1, "12 菱形走势图", ["月份", "完成率"]), ["完成率"])
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(df["月份"], df["完成率"], "D-", color=PALETTE[1], lw=2, ms=8)
    ax.set_ylim(0, 1); ax.set_title("模板12：菱形走势图", fontsize=14, fontweight="bold")
    save(fig, "模板12_菱形走势图.png")


# 13 对比折线图
def t13():
    df = num(read(F1, "13 对比折线图", ["月份", "2021年", "2022年"]), ["2021年", "2022年"])
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(df["月份"], df["2021年"], "o-", color=PALETTE[0], label="2021年")
    ax.plot(df["月份"], df["2022年"], "s-", color=PALETTE[2], label="2022年")
    ax.legend(); ax.set_title("模板13：对比折线图", fontsize=14, fontweight="bold")
    save(fig, "模板13_对比折线图.png")


# 14 单值圆环图
def t14():
    df = num(read(F1, "14 单值圆环图", ["完成率", "占位"]), ["完成率"])
    v = df["完成率"].iloc[0]
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie([v, 1-v], startangle=90, counterclock=False, colors=[PALETTE[3], "#E8E8E8"],
           wedgeprops=dict(width=0.35))
    ax.text(0, 0, f"{v:.0%}", ha="center", va="center", fontsize=28, fontweight="bold")
    ax.set_title("模板14：单值圆环图", fontsize=14, fontweight="bold")
    save(fig, "模板14_单值圆环图.png")


# 15 水球图：圆形内水位
def t15():
    df = num(read(F1, "15 水球图", ["完成率"]), ["完成率"])
    v = df["完成率"].iloc[0]
    fig, ax = plt.subplots(figsize=(6, 6))
    theta = np.linspace(0, 2*np.pi, 200)
    ax.plot(np.cos(theta), np.sin(theta), color=PALETTE[0], lw=3)
    # 水位：用底部填充
    y0 = -1 + 2*v
    ax.fill_between(np.linspace(-1, 1, 100), -1, np.interp(np.linspace(-1, 1, 100), [-1, 1], [-1, y0]),
                    color=PALETTE[3], alpha=0.6)
    ax.text(0, 0, f"{v:.0%}", ha="center", va="center", fontsize=26, fontweight="bold")
    ax.set_xlim(-1.3, 1.3); ax.set_ylim(-1.3, 1.3); ax.axis("off")
    ax.set_title("模板15：水球图", fontsize=14, fontweight="bold")
    save(fig, "模板15_水球图.png")


# 16 波浪水球图：水位加波浪
def t16():
    df = num(read(F2, "16 波浪水球图 ", ["完成率"]), ["完成率"])
    v = df["完成率"].iloc[0]
    fig, ax = plt.subplots(figsize=(6, 6))
    theta = np.linspace(0, 2*np.pi, 200)
    ax.plot(np.cos(theta), np.sin(theta), color=PALETTE[0], lw=3)
    y0 = -1 + 2*v
    x = np.linspace(-1, 1, 200)
    wave = y0 + 0.04*np.sin(8*np.pi*x)
    ax.fill_between(x, -1, wave, color=PALETTE[3], alpha=0.6)
    ax.plot(x, wave, color=PALETTE[0], lw=1)
    ax.text(0, 0, f"{v:.0%}", ha="center", va="center", fontsize=26, fontweight="bold")
    ax.set_xlim(-1.3, 1.3); ax.set_ylim(-1.3, 1.3); ax.axis("off")
    ax.set_title("模板16：波浪水球图", fontsize=14, fontweight="bold")
    save(fig, "模板16_波浪水球图.png")


# 17 玉玦图：年龄分布圆环
def t17():
    df = num(read(F2, "17 玉玦图", ["年龄", "占比"]), ["占比"])
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.pie(df["占比"], labels=df["年龄"], autopct="%.1f%%", startangle=90,
           colors=PALETTE[:len(df)], wedgeprops=dict(width=0.4))
    ax.set_title("模板17：玉玦图", fontsize=14, fontweight="bold")
    save(fig, "模板17_玉玦图.png")


# 18 跑道图：部门人数横向进度条
def t18():
    df = read(F2, "18 跑道图", ["部门", "人数"])
    df["人数"] = pd.to_numeric(df["人数"], errors="coerce")
    df = df.dropna()
    mx = df["人数"].max() * 1.2
    fig, ax = plt.subplots(figsize=(8, 5))
    y = np.arange(len(df))
    ax.barh(y, [mx]*len(df), height=0.5, color="#EEEEEE")   # 跑道背景
    ax.barh(y, df["人数"], height=0.5, color=PALETTE[0])     # 实际人数
    ax.set_yticks(y, df["部门"]); ax.set_xlim(0, mx)
    ax.set_title("模板18：跑道图", fontsize=14, fontweight="bold")
    save(fig, "模板18_跑道图.png")


# 19 南丁格尔圆饼图（极坐标玫瑰图）
def t19():
    df = num(read(F2, "19 南丁格尔圆饼图", ["部门", "人数占比"]), ["人数占比"])
    theta = np.linspace(0, 2*np.pi, len(df), endpoint=False)
    fig, ax = plt.subplots(figsize=(7, 7), subplot_kw={"projection": "polar"})
    ax.bar(theta, df["人数占比"], width=2*np.pi/len(df), color=PALETTE[:len(df)], alpha=0.85)
    ax.set_xticks(theta, df["部门"])
    ax.set_title("模板19：南丁格尔圆饼图", fontsize=14, fontweight="bold", pad=20)
    save(fig, "模板19_南丁格尔圆饼图.png")


# 20 南丁格尔圆环图（极坐标圆环玫瑰图）
def t20():
    df = num(read(F2, "20 南丁格尔圆环图", ["年龄", "人数占比"]), ["人数占比"])
    theta = np.linspace(0, 2*np.pi, len(df), endpoint=False)
    fig, ax = plt.subplots(figsize=(7, 7), subplot_kw={"projection": "polar"})
    ax.bar(theta, df["人数占比"], width=2*np.pi/len(df), bottom=0.2,
           color=PALETTE[:len(df)], alpha=0.85)
    ax.set_xticks(theta, df["年龄"])
    ax.set_title("模板20：南丁格尔圆环图", fontsize=14, fontweight="bold", pad=20)
    save(fig, "模板20_南丁格尔圆环图.png")


if __name__ == "__main__":
    print("开始复现模板 11-20……")
    t11(); t12(); t13(); t14(); t15(); t16(); t17(); t18(); t19(); t20()
    print("模板 11-20 完成，图见 figures/")

# -*- coding: utf-8 -*-
"""
《Excel数据可视化——从图表到数据大屏》第二章 图表模板 1-10 迁移为 Python
================================================================
原书用 Excel 实现 30 种图表模板，本文件用 matplotlib 复现 1-10 号模板。

模板清单：
  1 渐变柱形图    2 带均值柱形图   3 渐变圆角柱形图  4 标注柱形图
  5 层叠柱形图    6 蝴蝶图         7 蝴蝶图(占比)    8 数值百分比
  9 对比柱形图    10 甘特图
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from pathlib import Path

matplotlib.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]
matplotlib.rcParams["axes.unicode_minus"] = False

BASE = Path(__file__).resolve().parent.parent / "data"
FIG = Path(__file__).resolve().parent / "figures"
PALETTE = ["#4E79A7", "#F28E2B", "#E15759", "#76B7B2", "#59A14F", "#EDC948", "#B07AA1"]
F = "第二章 图表(前15).xlsx"


def save(fig, name):
    fig.savefig(FIG / name, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  ✓ {name}")


def read_sheet(sheet, target_cols):
    """自动检测表头行并读取指定列"""
    raw = pd.read_excel(BASE / F, sheet_name=sheet, header=None)
    header_row = 1
    for i in range(min(6, len(raw))):
        vals = [str(v) for v in raw.iloc[i].tolist()]
        if all(any(t in v for v in vals) for t in target_cols):
            header_row = i
            break
    df = pd.read_excel(BASE / F, sheet_name=sheet, header=header_row)
    return df[target_cols]


def num(df, cols):
    for c in cols:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    return df.dropna()


# 1 渐变柱形图：柱形颜色随数值由浅到深
def t01():
    df = num(read_sheet("1 渐变柱形图", ["区域", "销售量"]), ["销售量"])
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(df["区域"], df["销售量"], color=cm.Blues(np.linspace(0.45, 0.9, len(df))))
    ax.set_title("模板1：渐变柱形图", fontsize=14, fontweight="bold")
    save(fig, "模板01_渐变柱形图.png")


# 2 带均值柱形图
def t02():
    df = num(read_sheet("2 带均值柱形图", ["区域", "销售量"]), ["销售量"])
    mean = df["销售量"].mean()
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(df["区域"], df["销售量"], color=PALETTE[0], alpha=0.8)
    ax.axhline(mean, color=PALETTE[2], ls="--", lw=2, label=f"均值 {mean:.0f}")
    ax.legend(); ax.set_title("模板2：带均值柱形图", fontsize=14, fontweight="bold")
    save(fig, "模板02_带均值柱形图.png")


# 3 渐变圆角柱形图
def t03():
    df = num(read_sheet("3 渐变圆角柱形图", ["商品", "销量"]), ["销量"])
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(df["商品"], df["销量"], color=cm.Greens(np.linspace(0.5, 0.9, len(df))))
    ax.set_title("模板3：渐变圆角柱形图", fontsize=14, fontweight="bold")
    save(fig, "模板03_渐变圆角柱形图.png")


# 4 标注柱形图
def t04():
    df = num(read_sheet("4 标注柱形图", ["月份", "销量"]), ["销量"])
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(df["月份"], df["销量"], color=PALETTE[3])
    for b, v in zip(bars, df["销量"]):
        ax.text(b.get_x()+b.get_width()/2, v, str(int(v)), ha="center", va="bottom")
    ax.set_title("模板4：标注柱形图", fontsize=14, fontweight="bold")
    save(fig, "模板04_标注柱形图.png")


# 5 层叠柱形图
def t05():
    df = num(read_sheet("5 层叠柱形图", ["季度", "销售额", "利润额"]), ["销售额", "利润额"])
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(df["季度"], df["销售额"], label="销售额", color=PALETTE[0])
    ax.bar(df["季度"], df["利润额"], bottom=df["销售额"], label="利润额", color=PALETTE[4])
    ax.legend(); ax.set_title("模板5：层叠柱形图", fontsize=14, fontweight="bold")
    save(fig, "模板05_层叠柱形图.png")


# 6 蝴蝶图
def t06():
    df = num(read_sheet("6 蝴蝶图", ["区域", "2022年销量", "2021年销量"]), ["2022年销量", "2021年销量"])
    fig, ax = plt.subplots(figsize=(8, 5))
    y = np.arange(len(df))
    ax.barh(y, df["2022年销量"], height=0.35, color=PALETTE[0], label="2022")
    ax.barh(y, -df["2021年销量"], height=0.35, color=PALETTE[3], label="2021")
    ax.set_yticks(y, df["区域"]); ax.axvline(0, color="k", lw=1)
    ax.legend(); ax.set_title("模板6：蝴蝶图", fontsize=14, fontweight="bold")
    save(fig, "模板06_蝴蝶图.png")


# 7 蝴蝶图（占比版）
def t07():
    df = num(read_sheet("7 蝴蝶图", ["区域", "2022年", "2021年"]), ["2022年", "2021年"])
    fig, ax = plt.subplots(figsize=(8, 5))
    y = np.arange(len(df))
    ax.barh(y, df["2022年"], height=0.35, color=PALETTE[0], label="2022年占比")
    ax.barh(y, -df["2021年"], height=0.35, color=PALETTE[1], label="2021年占比")
    ax.set_yticks(y, df["区域"]); ax.axvline(0, color="k", lw=1)
    ax.legend(); ax.set_title("模板7：蝴蝶图（占比）", fontsize=14, fontweight="bold")
    save(fig, "模板07_蝴蝶图占比.png")


# 8 数值百分比
def t08():
    df = num(read_sheet("8 数值百分比", ["区域", "销量", "同比去年"]), ["销量", "同比去年"])
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(df["区域"], df["销量"], color=PALETTE[0])
    for b, v, r in zip(bars, df["销量"], df["同比去年"]):
        ax.text(b.get_x()+b.get_width()/2, v, f"{v}\n{r:+.1%}", ha="center", va="bottom", fontsize=9)
    ax.set_title("模板8：数值百分比", fontsize=14, fontweight="bold")
    save(fig, "模板08_数值百分比.png")


# 9 对比柱形图
def t09():
    df = num(read_sheet("9 对比柱形图", ["商品", "2021销量", "2022销量"]), ["2021销量", "2022销量"])
    fig, ax = plt.subplots(figsize=(8, 5))
    x = np.arange(len(df))
    ax.bar(x-0.2, df["2021销量"], width=0.4, color=PALETTE[0], label="2021")
    ax.bar(x+0.2, df["2022销量"], width=0.4, color=PALETTE[1], label="2022")
    ax.set_xticks(x, df["商品"]); ax.legend()
    ax.set_title("模板9：对比柱形图", fontsize=14, fontweight="bold")
    save(fig, "模板09_对比柱形图.png")


# 10 甘特图
def t10():
    df = read_sheet("10 甘特图", ["项目名称", "开始日期", "项目天数"])
    df["开始日期"] = pd.to_datetime(df["开始日期"])
    df["项目天数"] = pd.to_numeric(df["项目天数"], errors="coerce")
    df = df.dropna()
    fig, ax = plt.subplots(figsize=(9, 5))
    for i, (_, r) in enumerate(df.iterrows()):
        ax.barh(i, r["项目天数"], left=r["开始日期"], height=0.5, color=PALETTE[i % 7])
    ax.set_yticks(range(len(df)), df["项目名称"])
    ax.set_xlabel("日期"); ax.set_title("模板10：甘特图", fontsize=14, fontweight="bold")
    save(fig, "模板10_甘特图.png")


if __name__ == "__main__":
    print("开始复现模板 1-10……")
    t01(); t02(); t03(); t04(); t05(); t06(); t07(); t08(); t09(); t10()
    print("模板 1-10 完成，图见 figures/")

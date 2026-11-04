# -*- coding: utf-8 -*-
"""
《Excel数据可视化》第三章 动态图表 迁移为 Python
================================================================
原书用 Excel 控件（滚动条/下拉框）+ 公式实现动态图表，
本文件用 Plotly 交互式图表（下拉菜单切换数据）等价复现 6 个动态图表：
  1 动态柱形图  2 动态跑道图  3 动态南丁格尔圆环图
  4 动态组合图  5 动态玉玦图  6 动态滑珠图
"""
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent / "data"
OUT = Path(__file__).resolve().parent / "figures"
XLSM = "第三章 动态图表.xlsm"


def read(sheet, key_col):
    """自动检测表头行：找到第一列值含 key_col 的那行作为表头"""
    raw = pd.read_excel(BASE / XLSM, sheet_name=sheet, header=None)
    h = 0
    for i in range(min(6, len(raw))):
        vals = [str(v) for v in raw.iloc[i].tolist()]
        if any(key_col in v for v in vals):
            h = i; break
    df = pd.read_excel(BASE / XLSM, sheet_name=sheet, header=h)
    df.columns = [str(c) for c in df.columns]
    return df


def save_html(fig, name):
    fig.write_html(OUT / name)
    print(f"  ✓ {name}")


# 1 动态柱形图：下拉选择区域，显示该区域各月销量
def dynamic_bar():
    df = read("1 动态柱形图", "月份")  # 月份 × 6 区域
    regions = ["华北", "华南", "东北", "西北", "西南", "华东"]
    fig = go.Figure()
    for i, r in enumerate(regions):
        fig.add_trace(go.Bar(x=df["月份"], y=df[r], name=r, visible=(i == 0)))
    buttons = [dict(label=r, method="update",
                    args=[{"visible": [j == i for j in range(len(regions))]}])
               for i, r in enumerate(regions)]
    fig.update_layout(title="动态柱形图：选择区域查看各月销量",
                      updatemenus=[dict(buttons=buttons, x=1.15, y=1.15)])
    save_html(fig, "动态1_柱形图.html")


# 2 动态跑道图：下拉选择月份
def dynamic_track():
    df = read("2 动态跑道图", "部门")
    depts = df["部门"].tolist()
    months = ["1月", "2月", "3月", "4月"]
    fig = go.Figure()
    for i, m in enumerate(months):
        vals = pd.to_numeric(df[m], errors="coerce").fillna(0)
        fig.add_trace(go.Bar(y=depts, x=vals, name=m, orientation="h", visible=(i == 0)))
    buttons = [dict(label=m, method="update",
                    args=[{"visible": [j == i for j in range(len(months))]}])
               for i, m in enumerate(months)]
    fig.update_layout(title="动态跑道图：选择月份查看各部门人数", barmode="overlay",
                      updatemenus=[dict(buttons=buttons, x=1.15, y=1.15)])
    save_html(fig, "动态2_跑道图.html")


# 3 动态南丁格尔圆环图：下拉选择周期
def dynamic_nightingale():
    df = read("3 动态南丁格尔圆环图", "周期")
    periods = ["近7天", "近30天"]
    sources = ["首页推荐", "关注页面", "搜索", "个人主页", "其他来源"]
    fig = go.Figure()
    for i, p in enumerate(periods):
        vals = pd.to_numeric(df[df["周期"] == p][sources].iloc[0], errors="coerce")
        fig.add_trace(go.Barpolar(r=vals, theta=sources, name=p, visible=(i == 0)))
    buttons = [dict(label=p, method="update",
                    args=[{"visible": [j == i for j in range(len(periods))]}])
               for i, p in enumerate(periods)]
    fig.update_layout(title="动态南丁格尔圆环图：选择周期查看流量来源",
                      updatemenus=[dict(buttons=buttons, x=1.15, y=1.15)])
    save_html(fig, "动态3_南丁格尔圆环图.html")


# 4 动态组合图：柱(销售额) + 线(利润率)
def dynamic_combo():
    # 该表结构：第1列=标签，第2~5列=类别数据，第3行销售额、第5行利润率
    raw = pd.read_excel(BASE / XLSM, sheet_name="4 动态组合图", header=None)
    cats = raw.iloc[2, 2:6].dropna().tolist()
    sales = pd.to_numeric(raw.iloc[3, 2:6], errors="coerce")
    margin = pd.to_numeric(raw.iloc[5, 2:6], errors="coerce")
    fig = go.Figure()
    fig.add_trace(go.Bar(x=cats, y=sales, name="销售额", yaxis="y"))
    fig.add_trace(go.Scatter(x=cats, y=margin, name="利润率", yaxis="y2", mode="lines+markers"))
    fig.update_layout(title="动态组合图：销售额与利润率",
                      yaxis=dict(title="销售额"), yaxis2=dict(title="利润率", overlaying="y", side="right"))
    save_html(fig, "动态4_组合图.html")


# 5 动态玉玦图：下拉选择周期（与南丁格尔同数据，玉玦=圆环分段）
def dynamic_jade():
    df = read("6 VBA动态玉玦图", "周期")
    periods = ["近7天", "近30天"]
    sources = ["个人主页", "搜索", "关注页面", "首页推荐"]
    fig = go.Figure()
    for i, p in enumerate(periods):
        vals = pd.to_numeric(df[df["周期"] == p][sources].iloc[0], errors="coerce")
        fig.add_trace(go.Pie(labels=sources, values=vals, name=p, hole=0.5, visible=(i == 0)))
    buttons = [dict(label=p, method="update",
                    args=[{"visible": [j == i for j in range(len(periods))]}])
               for i, p in enumerate(periods)]
    fig.update_layout(title="动态玉玦图：选择周期查看流量来源构成",
                      updatemenus=[dict(buttons=buttons, x=1.15, y=1.15)])
    save_html(fig, "动态5_玉玦图.html")


# 6 动态滑珠图：下拉选择月份，显示各区域完成率
def dynamic_dumbbell():
    df = read("7 动态滑珠图", "区域")
    regions = df["区域"].tolist()
    months = ["1月", "2月", "3月", "4月", "5月", "6月"]
    fig = go.Figure()
    for i, m in enumerate(months):
        vals = pd.to_numeric(df[m], errors="coerce")
        fig.add_trace(go.Bar(y=regions, x=vals, name=m, orientation="h", visible=(i == 0)))
    buttons = [dict(label=m, method="update",
                    args=[{"visible": [j == i for j in range(len(months))]}])
               for i, m in enumerate(months)]
    fig.update_layout(title="动态滑珠图：选择月份查看各区域完成率",
                      updatemenus=[dict(buttons=buttons, x=1.15, y=1.15)])
    save_html(fig, "动态6_滑珠图.html")


if __name__ == "__main__":
    print("开始复现 6 个动态图表……")
    dynamic_bar(); dynamic_track(); dynamic_nightingale(); dynamic_combo(); dynamic_jade(); dynamic_dumbbell()
    print("动态图表完成，交互式 HTML 见 figures/")

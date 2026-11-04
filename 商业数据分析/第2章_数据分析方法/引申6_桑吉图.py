# -*- coding: utf-8 -*-
"""引申方法⑥ 流向分析（桑吉图）—— 迁移为 Python
教材 2.2.6 流向分析法：呈现流量/资源的流向与转化。用 Plotly 桑基图实现。"""
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent / "data" / "1《CDA 一级认证教材：商业数据分析》" / "第2章 数据分析方法/2、由基础分析范式引申出的分析方法/data-无答案"
OUT = Path(__file__).resolve().parent

df = pd.read_excel(BASE / "6桑吉图.xlsx", sheet_name="Sheet1")
df = df[["来源", "目标", "流量"]].dropna()
df["流量"] = pd.to_numeric(df["流量"], errors="coerce")

# 构建桑基图的节点与链接
labels = list(pd.unique(df[["来源", "目标"]].values.ravel()))
idx = {name: i for i, name in enumerate(labels)}
source = df["来源"].map(idx)
target = df["目标"].map(idx)
value = df["流量"]

fig = go.Figure(go.Sankey(
    node=dict(pad=15, thickness=20, line=dict(color="black", width=0.5),
              label=labels, color="#4E79A7"),
    link=dict(source=source, target=target, value=value)))
fig.update_layout(title="流向分析：网站流量桑吉图", font=dict(size=12))
fig.write_html(OUT / "图_桑吉图.html")
print("桑吉图完成，已保存为交互式 HTML：", OUT / "图_桑吉图.html")
print("节点：", " → ".join(labels[:6]), "...")

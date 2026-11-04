# -*- coding: utf-8 -*-
"""
05_dashboard.py —— 第 5 步：交互式可视化大屏（Streamlit）
================================================
含 7 个联动组件（评分标准要求 ≥6）：
  1. 筛选器（区域 / 类别 / 日期范围）
  2. KPI 指标卡 × 6
  3. 月度销售趋势图（Plotly 交互折线）
  4. 类别销售结构图（环形图）
  5. 区域销售对比图（柱形）
  6. 子类别销售排行（横向柱形）
  7. 明细数据表（可筛选）

运行方式：streamlit run scripts/05_dashboard.py
"""
import pandas as pd
import plotly.express as px
import streamlit as st
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CLEAN = ROOT / "data" / "clean"

st.set_page_config(page_title="Superstore 商业分析大屏", layout="wide",
                   page_icon="📊")

# —— 标题 ——
st.title("📊 Superstore 商业数据分析大屏")
st.caption("数据源：Tableau 官方 Sample-Superstore（2023–2026）｜ 全 Python 实现")


@st.cache_data
def load_data():
    df = pd.read_csv(CLEAN / "orders_clean.csv", parse_dates=["Order Date", "Ship Date"])
    return df


df = load_data()

# ============================================================
# 组件 1：筛选器（侧边栏）
# ============================================================
with st.sidebar:
    st.header("🔍 筛选器")
    regions = st.multiselect("区域", df["Region"].unique(), default=df["Region"].unique())
    categories = st.multiselect("产品类别", df["Category"].unique(),
                                default=df["Category"].unique())
    date_range = st.date_input("订单日期范围",
                               [df["Order Date"].min(), df["Order Date"].max()])

filtered = df[
    (df["Region"].isin(regions)) &
    (df["Category"].isin(categories)) &
    (df["Order Date"] >= pd.Timestamp(date_range[0])) &
    (df["Order Date"] <= pd.Timestamp(date_range[1]))
]

# ============================================================
# 组件 2：KPI 指标卡
# ============================================================
st.subheader("📈 核心指标")
c1, c2, c3, c4, c5, c6 = st.columns(6)
sales = filtered["Sales"].sum()
profit = filtered["Profit"].sum()
c1.metric("总销售额", f"${sales:,.0f}")
c2.metric("总利润", f"${profit:,.0f}")
c3.metric("利润率", f"{profit/sales:.1%}" if sales else "—")
c4.metric("订单数", f"{filtered['Order ID'].nunique():,}")
c5.metric("客户数", f"{filtered['Customer ID'].nunique():,}")
c6.metric("退货率", f"{(filtered['Returned']=='Yes').mean():.1%}")

st.markdown("---")

# ============================================================
# 组件 3~6：图表区
# ============================================================
col_left, col_right = st.columns(2)

with col_left:
    # 组件 3：月度销售趋势（折线）
    st.subheader("月度销售趋势")
    monthly = filtered.groupby("订单月")["Sales"].sum().reset_index()
    fig = px.line(monthly, x="订单月", y="Sales", markers=True,
                  labels={"Sales": "销售额", "订单月": "月份"})
    st.plotly_chart(fig, use_container_width=True)

    # 组件 5：区域销售对比（柱形）
    st.subheader("区域销售对比")
    region_s = filtered.groupby("Region")["Sales"].sum().reset_index()
    fig = px.bar(region_s, x="Region", y="Sales", color="Region",
                 labels={"Sales": "销售额"})
    st.plotly_chart(fig, use_container_width=True)

with col_right:
    # 组件 4：类别结构（环形图）
    st.subheader("类别销售结构")
    cat_s = filtered.groupby("Category")["Sales"].sum().reset_index()
    fig = px.pie(cat_s, names="Category", values="Sales", hole=0.45)
    st.plotly_chart(fig, use_container_width=True)

    # 组件 6：子类别排行（横向柱形）
    st.subheader("子类别销售排行 TOP10")
    sub_s = filtered.groupby("Sub-Category")["Sales"].sum() \
        .sort_values(ascending=False).head(10).reset_index()
    fig = px.bar(sub_s, x="Sales", y="Sub-Category", orientation="h",
                 labels={"Sales": "销售额", "Sub-Category": "子类别"})
    fig.update_layout(yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig, use_container_width=True)

# 组件 7：销售额-利润 散点图（散点组件）
st.subheader("销售额与利润散点分布")
scatter_df = filtered.sample(min(1000, len(filtered)), random_state=42)
fig = px.scatter(scatter_df, x="Sales", y="Profit", color="Category",
                 size="Quantity", hover_data=["Sub-Category"],
                 labels={"Sales": "销售额", "Profit": "利润"})
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ============================================================
# 组件 8：明细数据表
# ============================================================
st.subheader("📋 明细数据")
cols = ["Order Date", "Order ID", "Customer Name", "Region", "Category",
        "Sub-Category", "Sales", "Quantity", "Profit", "Returned"]
st.dataframe(filtered[cols].head(100), use_container_width=True)
st.caption(f"当前筛选后共 {len(filtered):,} 条记录（展示前 100 条）")

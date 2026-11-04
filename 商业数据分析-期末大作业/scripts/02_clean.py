# -*- coding: utf-8 -*-
"""
02_clean.py —— 第 2 步：数据清洗与治理
================================================
输入：data/raw/orders.csv、people.csv、returns.csv
输出：data/clean/orders_clean.csv、people_clean.csv、returns_clean.csv
      outputs/tables/清洗报告.csv

清洗内容（对应评分标准 2.1）：
  1. 缺失值识别与处理
  2. 重复值检测与去除
  3. 异常值识别（负销售额、极端利润等）
  4. 类型与日期格式统一
  5. 多表主外键对齐（Orders×People 按区域、Orders×Returns 按订单号）
  6. 派生指标字段（年月、季度、利润率等）

运行方式：python scripts/02_clean.py
"""
import pandas as pd
import numpy as np
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
CLEAN = ROOT / "data" / "clean"
OUT = ROOT / "outputs" / "tables"
CLEAN.mkdir(parents=True, exist_ok=True)
OUT.mkdir(parents=True, exist_ok=True)


def load():
    """读取三个原始 CSV"""
    orders = pd.read_csv(RAW / "orders.csv")
    people = pd.read_csv(RAW / "people.csv")
    returns = pd.read_csv(RAW / "returns.csv")
    # 日期列统一转成标准 datetime 类型
    for col in ["Order Date", "Ship Date"]:
        orders[col] = pd.to_datetime(orders[col])
    return orders, people, returns


def clean_missing(df):
    """缺失值统计与处理"""
    n_before = len(df)
    missing = df.isna().sum()
    missing = missing[missing > 0]
    # 订单主表里若有关键字段缺失（如日期/客户/销售额），直接删除；其余可用前值/众数填充
    for col in df.columns:
        if df[col].isna().sum() == 0:
            continue
        if col in ["Order Date", "Customer ID", "Sales"]:
            df = df.dropna(subset=[col])          # 关键字段缺失 → 删行
        elif df[col].dtype in ["float64", "int64"]:
            df[col] = df[col].fillna(df[col].median())  # 数值字段 → 中位数填充
        else:
            df[col] = df[col].fillna(df[col].mode()[0])  # 类别字段 → 众数填充
    return df, missing, n_before - len(df)


def clean_duplicates(df):
    """重复值检测（按整行完全重复去重，Row ID 应为唯一）"""
    n_before = len(df)
    df = df.drop_duplicates()
    return df, n_before - len(df)


def detect_outliers(df):
    """异常值识别：
       1) 销售额为负（理论上不该有）
       2) 数量为 0 或负
       3) 利润率超出 3 倍标准差（极端离群）
    这里采用『识别并标记』而非粗暴删除，保留可解释性。"""
    flags = pd.DataFrame(index=df.index)
    flags["负销售额"] = df["Sales"] < 0
    flags["非正数量"] = df["Quantity"] <= 0

    # 利润率 = 利润 / 销售额，用 3σ 原则识别极端离群值
    df["利润率"] = df["Profit"] / df["Sales"].replace(0, np.nan)
    margin_mean, margin_std = df["利润率"].mean(), df["利润率"].std()
    flags["极端利润率"] = (df["利润率"] - margin_mean).abs() > 3 * margin_std

    n_outlier_rows = int(flags.any(axis=1).sum())
    return df, flags, n_outlier_rows


def merge_tables(orders, people, returns):
    """多表关联（主外键对齐）：
       - Orders ⋈ People   按 Region 关联，得到每个订单的区域经理
       - Orders ⋈ Returns  按 Order ID 关联，标记订单是否退货"""
    # Returns 表里同一订单号可能重复，先去重保证左连接不膨胀
    ret = returns.drop_duplicates(subset=["Order ID"])
    orders = orders.merge(ret, on="Order ID", how="left")          # 左连接：保留所有订单
    orders["Returned"] = orders["Returned"].fillna("No")           # 未退货记为 No

    orders = orders.merge(people, on="Region", how="left")          # 按区域连区域经理
    return orders


def derive_features(df):
    """派生分析用字段"""
    df["订单年"] = df["Order Date"].dt.year
    df["订单月"] = df["Order Date"].dt.to_period("M").astype(str)   # 形如 2023-01
    df["订单季度"] = df["Order Date"].dt.to_period("Q").astype(str)  # 形如 2023Q1
    df["发货天数"] = (df["Ship Date"] - df["Order Date"]).dt.days
    return df


def main():
    orders, people, returns = load()

    # —— 清洗前规模 ——
    print("【1】原始规模")
    print(f"  Orders  {orders.shape[0]} 行；People {people.shape[0]} 行；Returns {returns.shape[0]} 行")

    # —— 缺失值 ——
    orders, missing, n_missing = clean_missing(orders)
    print(f"\n【2】缺失值：删除 {n_missing} 行关键字段缺失记录")
    if len(missing):
        print("  缺失字段分布：\n", missing.to_string())

    # —— 重复值 ——
    orders, n_dup = clean_duplicates(orders)
    print(f"\n【3】重复值：去除 {n_dup} 行完全重复记录")

    # —— 异常值 ——
    orders, flags, n_out = detect_outliers(orders)
    print(f"\n【4】异常值：识别出 {n_out} 行存在异常（负销售额/非正数量/极端利润率），已保留并标记")

    # —— 多表关联 ——
    orders = merge_tables(orders, people, returns)
    print("\n【5】多表关联完成：已关联区域经理(People) 与退货标记(Returns)")

    # —— 派生字段 ——
    orders = derive_features(orders)
    print("\n【6】派生字段完成：订单年/月/季度、发货天数、利润率")

    # —— 保存清洗结果（CSV + SQLite，便于复用与验证）——
    orders.to_csv(CLEAN / "orders_clean.csv", index=False, encoding="utf-8-sig")
    people.to_csv(CLEAN / "people_clean.csv", index=False, encoding="utf-8-sig")
    returns.to_csv(CLEAN / "returns_clean.csv", index=False, encoding="utf-8-sig")
    # 同时导出 SQLite 数据库
    import sqlite3
    conn = sqlite3.connect(CLEAN / "superstore.db")
    orders.to_sql("orders_clean", conn, if_exists="replace", index=False)
    people.to_sql("people_clean", conn, if_exists="replace", index=False)
    returns.to_sql("returns_clean", conn, if_exists="replace", index=False)
    conn.close()

    # —— 输出清洗报告 ——
    report = pd.DataFrame({
        "项目": ["原始订单行数", "缺失值删除行数", "重复值删除行数",
                 "异常值标记行数", "关联后字段数", "清洗后行数"],
        "数值": [len(orders) + n_missing + n_dup, n_missing, n_dup,
                 n_out, orders.shape[1], len(orders)],
    })
    report.to_csv(OUT / "清洗报告.csv", index=False, encoding="utf-8-sig")

    print(f"\n【完成】清洗后 Orders 共 {len(orders)} 行 x {orders.shape[1]} 列")
    print(f"        已保存到 data/clean/ 和 outputs/tables/清洗报告.csv")


if __name__ == "__main__":
    main()

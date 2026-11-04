# -*- coding: utf-8 -*-
"""第2章 PowerBI ETL 练习（拆分列/数据清洗/合并）—— 迁移为 Python
教材第2章 5、PowerBI基本操作/ETL练习：拆分列、数据清洗、横向/纵向合并。
本文件用 pandas 等价实现这些 Power Query 操作。"""
import pandas as pd
from pathlib import Path
BASE = Path(__file__).resolve().parent.parent / "data" / "1《CDA 一级认证教材：商业数据分析》" / "第2章 数据分析方法/5、PowerBI基本操作/ETL练习文件"

# 1. 拆分列：收货地址 → 省/市/区；数量 → 数字+单位
df = pd.read_excel(BASE / "ETL演示数据/拆分列示例数据.xlsx").dropna(how="all")
df["省"] = df["收货地址"].str[:3]
df["市"] = df["收货地址"].str[3:6]
df["区"] = df["收货地址"].str[6:]
df["数量数字"] = df["数量"].str.extract(r"(\d+)").astype(int)
df["数量单位"] = df["数量"].str.extract(r"([件本个]+)")
print("1. 拆分列（收货地址→省/市/区，数量→数字+单位）：")
print(df[["订单号", "省", "市", "区", "数量数字", "数量单位"]].head(3).to_string(index=False))

# 2. 数据清洗：去除重复行 + 缺失值
clean = pd.read_excel(BASE / "ETL演示数据/数据清洗示例数据.xlsx").dropna(how="all")
n_before = len(clean)
clean = clean.drop_duplicates()
print(f"\n2. 数据清洗：去重 {n_before - len(clean)} 行，缺失值 {clean.isna().sum().sum()} 处")

# 3. 纵向合并（两个字段一致的表格上下堆叠）
q1 = pd.read_excel(BASE / "合并演示数据/纵向合并演示-各字段名称一致.xlsx", sheet_name="第一季度")
q2 = pd.read_excel(BASE / "合并演示数据/纵向合并演示-各字段名称一致.xlsx", sheet_name="第二季度")
merged = pd.concat([q1, q2], ignore_index=True)   # 等价 Power Query 追加查询
print("\n3. 纵向合并（第一季度 + 第二季度）：")
print(merged.to_string(index=False))
print("   （横向合并用 pd.merge(..., how='left') 按主键关联，等价 Power Query 合并查询）")

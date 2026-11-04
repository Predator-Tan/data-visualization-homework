# -*- coding: utf-8 -*-
"""第2章 WPS 数据透视表练习 —— 迁移为 Python
教材第2章 WPS电子表格/透视表练习：Excel 数据透视表 → pandas pivot_table。"""
import pandas as pd
from pathlib import Path
BASE = Path(__file__).resolve().parent.parent / "data" / "1《CDA 一级认证教材：商业数据分析》" / "第2章 数据分析方法/WPS电子表格/4、WPS电子表格的公式与函数"

df = pd.read_excel(BASE / "2透视表&条件格式&引用&查找练习.xlsx", sheet_name="数据透视表")
df["销售金额"] = pd.to_numeric(df["销售金额"], errors="coerce")
df = df[["销售地区", "销售人员", "品名", "销售金额"]].dropna()

# 等价 Excel 数据透视表：按 地区×人员 汇总销售金额
pivot = df.pivot_table(index="销售地区", columns="销售人员", values="销售金额", aggfunc="sum", fill_value=0)
print("数据透视表（等价 Excel 透视表）：各地区 × 各销售人员的销售金额")
print(pivot.round(0).to_string())
print("\n总计：", f"{df['销售金额'].sum():,.0f}")
print("销售冠军：", df.groupby('销售人员')['销售金额'].sum().idxmax())

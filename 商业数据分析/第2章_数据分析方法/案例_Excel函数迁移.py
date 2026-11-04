# -*- coding: utf-8 -*-
"""第2章 Excel 基础操作（常用函数）—— 迁移为 Python
教材第2章 4、EXCEL基础操作：电子表格常用函数（IF/COUNTIF/SUMIF/日期/MOD等）。
本文件演示这些 Excel 函数在 pandas 里的等价写法。"""
import pandas as pd
import numpy as np
from pathlib import Path
BASE = Path(__file__).resolve().parent.parent / "data" / "1《CDA 一级认证教材：商业数据分析》" / "第2章 数据分析方法/4、EXCEL基础操作"

df = pd.read_excel(BASE / "1、电子表格常用函数（WPS和EXCEL）.xlsx", sheet_name="常用函数应用")

print("Excel 常用函数 → pandas 等价：")
print("  IF(条件, A, B)        → np.where(条件, A, B)")
print("  AND(a,b) / OR(a,b)    → (a) & (b) / (a) | (b)")
print("  COUNTIF(范围,条件)     → (df['列']==条件).sum()")
print("  SUMIF(范围,条件,求和)  → df[df['列']==条件]['求和列'].sum()")
print("  VLOOKUP(查找值,区域,列) → 用 merge 或 map 按主键关联")
print("  取整/MOD               → np.floor / % 取余")
print("  文本截取               → .str[:n] 等")

# 实测 VLOOKUP 精确查找：商品编码 → 商品名称（等价 VLOOKUP）
lookup = pd.read_excel(BASE / "2、电子表格查找引用函数（WPS和EXCEL）.xlsx",
                       sheet_name="1.VLOOKUP精确查找")
# 左表是待查商品编码，右表是"编码→名称"对照表
src = lookup.iloc[:, 0].dropna().astype(int)            # 待查的商品编码列
mapping = lookup.iloc[:, 6:8].dropna()                  # 编码、名称对照表
mapping.columns = ["商品编码", "商品名称"]
mapping["商品编码"] = pd.to_numeric(mapping["商品编码"], errors="coerce")
result = pd.DataFrame({"商品编码": src}).merge(mapping, on="商品编码", how="left")
print("\n实测 VLOOKUP（商品编码 → 商品名称）：")
print(result.dropna().head(5).to_string(index=False))

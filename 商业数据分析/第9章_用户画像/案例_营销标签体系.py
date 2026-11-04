# -*- coding: utf-8 -*-
"""第9章 标签体系参考（营销类标签）—— 迁移为 Python
教材第9章 标签体系参考/客户运营类标签/营销类标签.xlsx：银行营销标签体系。
本文件读取标签结构（选项卡/节/字段），统计标签分类。"""
import pandas as pd
from pathlib import Path
BASE = Path(__file__).resolve().parent.parent / "data" / "1《CDA 一级认证教材：商业数据分析》" / "第9章 用户标签体系与用户画像专题/标签体系参考/客户运营类标签"

df = pd.read_excel(BASE / "营销类标签.xlsx", header=None)
# 表结构：第2列=选项卡，第3列=节，第4列=编号，第5列=字段
tab_col, field_col = 2, 5
tabs = [t for t in df.iloc[2:, tab_col].dropna().unique() if t not in ("选项卡", "No.")]
fields = [f for f in df.iloc[2:, field_col].dropna() if f != "字段"]
print("营销类标签体系分析：")
print(f"  选项卡（标签大类）：{list(tabs)}")
print(f"  标签字段总数：{len(fields)} 个")
print("  示例标签：", fields[:10])

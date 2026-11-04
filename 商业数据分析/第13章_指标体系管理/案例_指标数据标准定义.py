# -*- coding: utf-8 -*-
"""第13章 指标体系管理 —— 指标数据标准编制模板 迁移为 Python
教材第13章 2、指标数据标准编制模板.xlsx：银行指标标准定义
（编号/业务主题/分类/中文名称/业务口径/技术口径SQL），本文件读取并展示。"""
import pandas as pd
from pathlib import Path
BASE = Path(__file__).resolve().parent.parent / "data" / "1《CDA 一级认证教材：商业数据分析》" / "第13章 指标体系管理"
OUT = Path(__file__).resolve().parent

df = pd.read_excel(BASE / "2、指标数据标准编制模板.xlsx", sheet_name="标准定义", header=1)
df = df.dropna(subset=["编号"])
# 关键列：编号/业务主题/一级分类/中文名称/指标业务口径/技术口径
cols = [c for c in ["编号", "业务主题", "一级分类", "中文名称", "指标业务口径", "技术口径"] if c in df.columns]
print("银行指标数据标准定义（示例）：")
print(df[cols].head(6).to_string(index=False))

# 各业务主题指标数统计
if "业务主题" in df.columns:
    theme = df["业务主题"].value_counts()
    print("\n各业务主题指标数量：", dict(theme))
print(f"\n共 {len(df)} 条指标标准定义")

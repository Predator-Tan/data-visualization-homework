# -*- coding: utf-8 -*-
"""第8章 SQL 语言基础 —— 用 pandas 等价实现 SQL 查询
教材第8章：SQL 查询语句（select/where/order by/distinct/group by/join）。
本文件用 pandas 一一对应实现，展示"SQL → Python"的迁移。"""
import pandas as pd
from pathlib import Path
BASE = Path(__file__).resolve().parent.parent / "data" / "1《CDA 一级认证教材：商业数据分析》" / "第8章 SQL语言基础与Mysql入门/1、Windows系统下将数据导入到MySQL的三种方法/方式1/mysql_csv"

sale = pd.read_csv(BASE / "sale.csv", encoding="gbk", header=None)
sale.columns = ["year", "market", "sale", "profit"]   # 原文件无表头，手动指定
sale["year"] = pd.to_numeric(sale["year"], errors="coerce")
sale["sale"] = pd.to_numeric(sale["sale"], errors="coerce")
sale["profit"] = pd.to_numeric(sale["profit"], errors="coerce")
print("sale 表列名：", list(sale.columns), "| 行数：", len(sale))

print("\n1. 选择指定列  select year,market,sale,profit from sale")
print(sale[["year", "market", "sale", "profit"]].head(3).to_string(index=False))

print("\n2. 删除重复行  select DISTINCT year from sale")
print("  ", sale["year"].unique())

print("\n3. 过滤  where year=2012")
print(sale[sale["year"] == 2012].head(3).to_string(index=False))

print("\n4. 排序  order by year")
print(sale.sort_values("year").head(3).to_string(index=False))

print("\n5. 分组汇总  select market, sum(sale), avg(profit) group by market")
g = sale.groupby("market").agg(总销售=("sale", "sum"), 平均利润=("profit", "mean")).round(1)
print(g.to_string())

print("\nSQL → pandas 迁移完成（SELECT / DISTINCT / WHERE / ORDER BY / GROUP BY）")

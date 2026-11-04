# -*- coding: utf-8 -*-
"""
01_load.py —— 第 1 步：加载原始数据并转为 CSV
================================================
数据源：Tableau 官方「Sample - Superstore」示例数据（合规获取，非爬虫）
原始文件：data/raw/superstore.xls（内含 3 张工作表）
输出：   data/raw/orders.csv、people.csv、returns.csv

运行方式：python scripts/01_load.py
"""
import pandas as pd
from pathlib import Path

# 路径设置：脚本在 scripts/ 下，项目根目录是上一级
ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
RAW.mkdir(parents=True, exist_ok=True)

XLS_PATH = RAW / "superstore.xls"


def main():
    # 1. 用 pandas 读取 .xls 文件里的三张工作表
    #    engine="xlrd" 表示用 xlrd 库解析老式 .xls 格式
    orders = pd.read_excel(XLS_PATH, sheet_name="Orders", engine="xlrd")
    people = pd.read_excel(XLS_PATH, sheet_name="People", engine="xlrd")
    returns = pd.read_excel(XLS_PATH, sheet_name="Returns", engine="xlrd")

    # 2. 保存为 CSV 文件（utf-8-sig 编码，Excel 双击打开中文不乱码）
    orders.to_csv(RAW / "orders.csv", index=False, encoding="utf-8-sig")
    people.to_csv(RAW / "people.csv", index=False, encoding="utf-8-sig")
    returns.to_csv(RAW / "returns.csv", index=False, encoding="utf-8-sig")

    # 3. 打印每张表的规模，方便核对
    print("=" * 50)
    print("原始数据加载完成，规模如下：")
    print(f"  Orders  （订单主表）  : {orders.shape[0]:>6} 行 x {orders.shape[1]:>2} 列")
    print(f"  People  （区域经理表） : {people.shape[0]:>6} 行 x {people.shape[1]:>2} 列")
    print(f"  Returns （退货表）     : {returns.shape[0]:>6} 行 x {returns.shape[1]:>2} 列")
    print("已输出到 data/raw/ 目录（CSV 格式）")
    print("=" * 50)


if __name__ == "__main__":
    main()

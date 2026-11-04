# -*- coding: utf-8 -*-
"""第2章 PowerBI 案例1：分省销售分析 —— 迁移为 Python
教材第2章 5、PowerBI基本操作/案例1：订单表×订单明细×商品表×商品类型表 多表关联，
做分省销售分析。本文件用 pandas 等价实现多表 join + 分省汇总。"""
import pandas as pd, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from pathlib import Path
matplotlib.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]
matplotlib.rcParams["axes.unicode_minus"] = False
BASE = Path(__file__).resolve().parent.parent / "data" / "1《CDA 一级认证教材：商业数据分析》" / "第2章 数据分析方法/5、PowerBI基本操作/案例1"
OUT = Path(__file__).resolve().parent

def rd(f):
    try: return pd.read_csv(BASE / f, encoding="gbk")
    except: return pd.read_csv(BASE / f, encoding="utf-8-sig")

order = rd("订单表.csv")          # OrderID, EmployeeID, ShipProvince, OrderDate
detail = rd("订单表明细表.csv")    # 订单ID, 产口ID, 销售金额, 销售成本
product = rd("商品表.csv")         # ProductID, ProductName, CategoryID
emp = rd("雇员表.csv")            # EmployeeID, FullName, Age, gender, City, store

# 多表关联：明细 → 订单(取省份) → 商品(取品名)
df = detail.merge(order, left_on="订单ID", right_on="OrderID", how="left") \
           .merge(product, left_on="产口ID", right_on="ProductID", how="left")
df["销售金额"] = pd.to_numeric(df["销售金额"], errors="coerce")

# 分省销售额
province = df.groupby("ShipProvince")["销售金额"].sum().sort_values(ascending=False)

fig, ax = plt.subplots(figsize=(11, 5))
province.plot(kind="bar", ax=ax, color="#4E79A7")
ax.set_ylabel("销售金额"); ax.set_title("分省销售分析：各省销售金额", fontsize=14, fontweight="bold")
fig.tight_layout()
fig.savefig(OUT / "图2-案例1_分省销售.png", dpi=150, bbox_inches="tight", facecolor="white"); plt.close(fig)
print("分省销售分析完成：")
print(f"  销售金额最高的省份：{province.index[0]}（{province.iloc[0]:,.0f}）")
print(f"  涉及 {province.count()} 个省份，{len(df)} 条明细记录")

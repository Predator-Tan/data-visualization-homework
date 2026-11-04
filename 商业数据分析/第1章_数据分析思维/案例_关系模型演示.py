# -*- coding: utf-8 -*-
"""第1章 数据分析思维 —— 关系模型演示（银行多表关联）迁移为 Python
教材第1章：关系型数据模型 = 多张表通过主外键关联。原用 Power BI 演示，
本文件用 pandas 多表 join 等价实现：account 是外键中心，关联 loan、order 表。"""
import pandas as pd, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from pathlib import Path
matplotlib.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]
matplotlib.rcParams["axes.unicode_minus"] = False
BASE = Path(__file__).resolve().parent.parent / "data" / "1《CDA 一级认证教材：商业数据分析》" / "第1章 数据分析思维/关系模型演示-不建议用poweBI操作关系型数据模型"
OUT = Path(__file__).resolve().parent

def rd(f):
    try: return pd.read_csv(BASE / f, encoding="gbk")
    except: return pd.read_csv(BASE / f, encoding="utf-8-sig")

accounts = rd("accounts.csv"); loans = rd("loans.csv"); order = rd("order.csv")

# 关系模型：account_id 是多张表的外键（loan.account_id → accounts.account_id）
loan_stat = loans.groupby("account_id").agg(贷款笔数=("loan_id", "count"), 贷款总额=("amount", "sum"))
order_stat = order.groupby("account_id").agg(转账笔数=("order_id", "count"), 转账总额=("amount", "sum"))
merged = accounts.merge(loan_stat, on="account_id", how="left") \
                .merge(order_stat, on="account_id", how="left").fillna(0)

# 按地区(前10个)汇总
by_district = merged.groupby("district_id")[["贷款总额", "转账总额"]].sum()

fig, axes = plt.subplots(1, 2, figsize=(13, 5))
by_district["贷款总额"].head(10).plot(kind="bar", ax=axes[0], color="#4E79A7")
axes[0].set_title("各区域贷款总额"); axes[0].set_xlabel("区域编号")
by_district["转账总额"].head(10).plot(kind="bar", ax=axes[1], color="#F28E2B")
axes[1].set_title("各区域转账总额"); axes[1].set_xlabel("区域编号")
fig.suptitle("关系模型演示：银行多表关联分析", fontsize=14, fontweight="bold")
fig.tight_layout()
fig.savefig(OUT / "图1-2_关系模型演示.png", dpi=150, bbox_inches="tight", facecolor="white"); plt.close(fig)

print("关系模型演示完成：")
print(f"  accounts({len(accounts)}) 通过 account_id 关联 loans({len(loans)}) 和 order({len(order)})")
print("  完成跨表统计（各区域贷款/转账总额）")

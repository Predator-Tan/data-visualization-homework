# -*- coding: utf-8 -*-
"""第9章 信用卡客户画像（原 SQL + Excel 案例）—— 迁移为 Python
教材第9章 9.4：用 SQL 关联多表 + Excel 盒须图做信用卡用户画像，
本文件用 pandas 等价实现多表关联，并绘制画像图表。"""
import pandas as pd, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from pathlib import Path
matplotlib.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]
matplotlib.rcParams["axes.unicode_minus"] = False
BASE = Path(__file__).resolve().parent.parent / "data" / "1《CDA 一级认证教材：商业数据分析》" / "第9章 用户标签体系与用户画像专题/data"
OUT = Path(__file__).resolve().parent

# 多表关联（等价 SQL 的 left join）：card → disp → clients
clients = pd.read_csv(BASE / "clients.csv", encoding="gbk")
card = pd.read_csv(BASE / "card.csv", encoding="gbk")
disp = pd.read_csv(BASE / "disp.csv", encoding="gbk")

merged = card.merge(disp[["disp_id", "client_id", "account_id"]], on="disp_id", how="left") \
              .merge(clients, on="client_id", how="left")
merged["issued"] = pd.to_datetime(merged["issued"], format="%Y-%m-%d", errors="coerce")
merged["birth_date"] = pd.to_datetime(merged["birth_date"], format="%Y-%m-%d", errors="coerce")
merged["发卡年龄"] = ((merged["issued"] - merged["birth_date"]).dt.days / 365).round(1)  # SQL: datediff/365

# 画像维度：性别分布、发卡年龄分布、卡类型分布
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
merged["sex"].value_counts().plot(kind="bar", ax=axes[0], color=["#4E79A7", "#E15759"])
axes[0].set_title("性别分布")
merged["发卡年龄"].dropna().hist(bins=20, ax=axes[1], color="#76B7B2", edgecolor="white")
axes[1].set_title("发卡年龄分布"); axes[1].set_xlabel("年龄")
merged["type"].value_counts().plot(kind="bar", ax=axes[2], color="#F28E2B")
axes[2].set_title("卡类型分布")
fig.suptitle("信用卡客户画像", fontsize=15, fontweight="bold")
fig.tight_layout()
fig.savefig(OUT / "图9-1_信用卡客户画像.png", dpi=150, bbox_inches="tight", facecolor="white"); plt.close(fig)

print("信用卡客户画像完成：")
print("  客户总数：", merged["client_id"].nunique())
print("  性别分布：", dict(merged["sex"].value_counts()))
print("  发卡平均年龄：", round(merged["发卡年龄"].mean(), 1))
print("  卡类型分布：", dict(merged["type"].value_counts()))

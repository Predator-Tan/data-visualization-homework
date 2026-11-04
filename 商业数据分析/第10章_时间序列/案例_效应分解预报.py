# -*- coding: utf-8 -*-
"""第10章 使用效应分解方法做预报 —— AirPassengers 迁移为 Python
教材第10章：把时间序列分解为 趋势+季节+随机 三个效应，再据趋势和季节做预报。"""
import warnings; warnings.filterwarnings("ignore")
import pandas as pd, numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from pathlib import Path
matplotlib.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]
matplotlib.rcParams["axes.unicode_minus"] = False
BASE = Path(__file__).resolve().parent.parent / "data" / "1《CDA 一级认证教材：商业数据分析》" / "第10章 使用效应分解方法做预报"
OUT = Path(__file__).resolve().parent

df = pd.read_csv(BASE / "AirPassengers.csv")
df["DATE"] = pd.to_datetime(df["DATE"], format="%m/%d/%Y")
s = df.set_index("DATE")["AIR"].asfreq("MS")

# 1. 效应分解：趋势 + 季节 + 随机
res = seasonal_decompose(s, model="multiplicative", period=12)

fig, axes = plt.subplots(4, 1, figsize=(12, 10), sharex=True)
res.observed.plot(ax=axes[0], color="#4E79A7"); axes[0].set_title("原始序列（月乘客数）")
res.trend.plot(ax=axes[1], color="#E15759"); axes[1].set_title("趋势效应")
res.seasonal.plot(ax=axes[2], color="#F28E2B"); axes[2].set_title("季节效应（12个月）")
res.resid.plot(ax=axes[3], color="#76B7B2"); axes[3].set_title("随机效应")
fig.suptitle("效应分解法：航空乘客量分解", fontsize=14, fontweight="bold")
fig.savefig(OUT / "图10-1_效应分解.png", dpi=150, bbox_inches="tight", facecolor="white"); plt.close(fig)

# 2. 预报：趋势外推（线性回归）+ 季节因子重复
trend = res.trend.dropna()
t = np.arange(len(trend))
k, b = np.polyfit(t, trend.values, 1)              # 趋势线性外推
seasonal_factor = res.seasonal[-12:]               # 最近一个完整季节周期
future_t = np.arange(len(trend), len(trend) + 12)
forecast = (k * future_t + b) * seasonal_factor.values   # 趋势 × 季节因子

fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(s.index, s.values, color="#4E79A7", label="历史实际")
ax.plot(pd.date_range(s.index[-1], periods=13, freq="MS")[1:], forecast,
        color="#E15759", marker="o", label="效应分解法预测")
ax.set_ylabel("乘客数"); ax.legend()
ax.set_title("效应分解法预报：未来 12 个月预测", fontsize=14, fontweight="bold")
fig.savefig(OUT / "图10-2_效应分解预报.png", dpi=150, bbox_inches="tight", facecolor="white"); plt.close(fig)

print("效应分解完成。未来12个月预测均值：", round(forecast.mean()))
print("图已保存到", OUT)

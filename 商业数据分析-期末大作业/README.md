# 基于 Superstore 销售数据的商业数据分析项目

> 《商业数据分析》期末大作业 ｜ 全 Python 实现（未使用 Power BI / Tableau / Excel 出图）

本项目完成从「合规数据获取 → 数据清洗 → 商业分析模型 → 可视化复现 → 交互式大屏 → 商业洞察」的端到端商业数据分析流程。

---

## 一、数据来源与合规声明

| 项目 | 说明 |
|---|---|
| 数据源名称 | Tableau 官方「Sample - Superstore」 |
| 官方链接 | https://public.tableau.com/app/sample-data/sample_-_superstore.xls |
| 获取方式 | 官方公开数据文件直接下载（白名单方式，**非爬虫**） |
| 获取日期 | 2026-10-23 |
| 授权/License | Tableau 官方公开示例数据，仅用于教学与学习 |
| 数据规模 | Orders 订单主表 **10,194 行**（≥500，达标）；People 4 行；Returns 296 行 |
| 时间范围 | 2023-01 ～ 2026-12（48 个月，4 年） |
| 抽样说明 | 使用全量数据，未抽样（随机种子不适用） |
| 导出格式 | CSV（data/clean/*.csv）+ SQLite（data/clean/superstore.db） |

**多表关联**：`Orders`（订单事实表）⋈ `People`（区域经理维度表，按 Region）⋈ `Returns`（退货表，按 Order ID）。

---

## 二、项目目录结构

```
superstore-analysis/
├── data/
│   ├── raw/                原始数据（superstore.xls → 3 个 CSV）
│   └── clean/              清洗后数据（orders_clean.csv 等）
├── scripts/
│   ├── 01_load.py          第1步：加载原始数据并转 CSV
│   ├── 02_clean.py         第2步：数据清洗（缺失/重复/异常/多表关联/派生字段）
│   ├── 03_analysis.py      第3步：6 个商业分析模型
│   ├── 04_visuals.py       第4步：业务模型图 + 探索性分析图（9 张）
│   └── 05_dashboard.py     第5步：交互式大屏（Streamlit，8 个组件）
├── excel-templates/        《Excel数据可视化》模板复现（12 个）
│   ├── templates.py
│   └── figures/
├── outputs/
│   ├── figures/            业务图表（fig01～fig09）
│   └── tables/             模型结果表（RFM、同期群、帕累托、BCG、SARIMA 等）
├── docs/                   期末大论文、数据来源合规声明、数据字典
├── requirements.txt        依赖清单
├── run_all.py              一键复现入口
└── README.md               本文件
```

---

## 三、一键复现

```bash
# 1. 安装依赖（国内建议加清华镜像）
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 2. 一键复现全部分析（加载→清洗→模型→图表→模板复现）
python run_all.py

# 3. 启动交互式大屏
python -m streamlit run scripts/05_dashboard.py
```

---

## 四、商业分析模型（6 个，评分要求 ≥3）

| 模型 | 类别 | 关键结论 |
|---|---|---|
| RFM 客户价值八分类 | 用户与客群 | 中位数切分，8 类客户；「一般挽留客户」196 人最多 |
| 同期群留存分析 | 用户与客群 | 第 12 月平均留存率 22.3%，次月流失最快 |
| 帕累托 / ABC 分类 | 结构与价值 | 6 个子类别（35%）贡献 70% 销售额，头部 Chairs |
| 波士顿矩阵 | 结构与价值 | 明星：Accessories/Binders/Copiers/Phones |
| 环比 / 同比分析 | 趋势与对比 | 最新月销售额环比 -28.1%、同比 -12.6% |
| SARIMA 时间序列预测 | 预测与预警 | 回测 MAPE=17.9%、RMSE=18,008，含 95% 置信区间 |

---

## 五、图表索引

**业务模型图（outputs/figures/）**

| 编号 | 名称 | 对应模型 |
|---|---|---|
| fig01 | RFM 客户价值气泡图 | RFM |
| fig02 | 同期群留存热力图 | 同期群 |
| fig03 | 帕累托图 | 帕累托/ABC |
| fig04 | 波士顿矩阵 | BCG |
| fig05 | 销售额环比同比趋势 | 环比/同比 |
| fig06 | SARIMA 销售预测置信区间 | SARIMA |
| fig07 | 区域销售与利润 | 探索性 |
| fig08 | 类别利润贡献 | 探索性 |
| fig09 | 月度订单量趋势 | 探索性 |

**Excel 模板复现（excel-templates/figures/）**——对照《Excel数据可视化——从图表到数据大屏》

| 编号 | 模板名 | 编号 | 模板名 |
|---|---|---|---|
| t01 | 渐变柱形图 | t13 | 对比折线图 |
| t02 | 带均值柱形图 | t14 | 单值圆环图 |
| t05 | 层叠柱形图 | t20 | 南丁格尔圆环图 |
| t06 | 蝴蝶图 | t22 | 仪表盘图 |
| t10 | 甘特图 | t23 | 柱形折线图 |
| t11 | 平滑折线图 | t28 | 滑珠图 |

---

## 六、交互式大屏（Streamlit）

8 个联动组件：区域/类别/日期筛选器、6 个 KPI 指标卡、月度销售趋势折线、类别结构环形图、区域销售柱形、子类别排行、销售额-利润散点图、明细数据表。

启动方式：`python -m streamlit run scripts/05_dashboard.py`

---

## 七、分工说明

本作业由 **本人独立完成**（1 人小组）。

## 八、AI 使用披露

本项目使用 AI 工具辅助代码编写与文档排版（工具：Claude Code；环节：脚本初稿、图表参数调优、README 撰写；关键提示词示例：「用 pandas 实现 RFM 八分类并用中位数切分」）。全部结果均经本人理解、核对与复现验证。

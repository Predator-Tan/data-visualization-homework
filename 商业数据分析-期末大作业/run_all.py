# -*- coding: utf-8 -*-
"""
run_all.py —— 一键复现入口
================================================
依次执行：数据加载 → 清洗 → 分析模型 → 业务图表 → Excel模板复现
运行方式：python run_all.py
交互大屏需单独启动：streamlit run scripts/05_dashboard.py
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PY = sys.executable   # 当前 Python 解释器

STEPS = [
    ("1/5 加载数据（xls → csv）", "scripts/01_load.py"),
    ("2/5 数据清洗与治理",       "scripts/02_clean.py"),
    ("3/5 商业分析模型（6个）",  "scripts/03_analysis.py"),
    ("4/5 业务模型图表（9张）",  "scripts/04_visuals.py"),
    ("5/5 Excel模板复现（12个）", "excel-templates/templates.py"),
]


def main():
    for name, script in STEPS:
        print(f"\n{'='*60}\n▶ 正在执行：{name}\n{'='*60}")
        result = subprocess.run([PY, str(ROOT / script)], cwd=str(ROOT))
        if result.returncode != 0:
            print(f"❌ 步骤失败：{script}")
            sys.exit(result.returncode)
    print(f"\n{'='*60}")
    print("✅ 全部步骤完成！图表输出见 outputs/figures/ 和 excel-templates/figures/")
    print("   交互大屏请运行：streamlit run scripts/05_dashboard.py")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()

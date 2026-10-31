# -*- coding: utf-8 -*-
"""
SYSINT-TOPIC-CHAIN-ALIGN-02-L01 · 迁移版数据准备（主仓内运行）
与任务工作区版差异：
  1. ORCH 常量改为相对主仓根解析（不再写本机绝对路径）
  2. 输出 prepared.json 相对路径版
产物唯一入口：本目录三个 py 顺序执行，xlsx 在主仓内重新生成（超链接为 file:// 指向主仓真实文件）。
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
# 主仓根：本目录 = agent-delivery/agent-handoffs/系统集成-SYSINT/SYSINT-TOPIC-CHAIN-ALIGN-02-L01/产物/_work
ORCH = os.path.abspath(os.path.join(HERE, "../", "../", "../", "../", "../", "../"))  # 同 prepare_data.py：6 层上溯到主仓根

XLSX_573 = os.path.join(ORCH, "agent-delivery/metrics/指标入库详情-合并-20261028-三系统.xlsx")
CSV_SUPPORT = os.path.join(ORCH, "agent-delivery/工程过程/04-系统集成/02-对接三要素/调研/指标支持.csv")
CSV_TABLES = os.path.join(ORCH, "agent-delivery/工程过程/04-系统集成/02-对接三要素/调研/表清单.csv")
CSV_FIELDS = os.path.join(ORCH, "agent-delivery/工程过程/04-系统集成/02-对接三要素/调研/字段清单.csv")
XLSX_CMP = os.path.join(ORCH, "agent-delivery/agent-handoffs/系统集成-SYSINT/SYSINT-CMP-02-L01/九新三要素93指标对照表-20261026.xlsx")

if __name__ == "__main__":
    # 复用同目录原版逻辑：仅替换路径常量后 exec
    src = os.path.join(HERE, "prepare_data.py")
    code = open(src, encoding="utf-8").read()
    # 屏蔽原版常量（原文件用同名常量），用本文件的值
    for name in ("XLSX_573", "CSV_SUPPORT", "CSV_TABLES", "CSV_FIELDS", "XLSX_CMP"):
        globals()[name] = globals()[name]
    ns = dict(globals())
    ns["__file__"] = src
    ns["ORCH"] = ORCH
    ns["XLSX_573"] = XLSX_573
    ns["CSV_SUPPORT"] = CSV_SUPPORT
    ns["CSV_TABLES"] = CSV_TABLES
    ns["CSV_FIELDS"] = CSV_FIELDS
    ns["XLSX_CMP"] = XLSX_CMP
    ns["HERE"] = HERE  # 输出 json 仍落本目录
    exec(compile(code, src, "exec"), ns)

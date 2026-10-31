# -*- coding: utf-8 -*-
"""
03-UI页面视角 xlsx 生成脚本（v2 · 20261031 淮政玮反馈版）
输入：
  - /tmp/page_deps.json          产业链侧页面×依赖定义（自 industryWorkspace.ts + 缺口分析稿人工固化）
  - /tmp/page_deps_ent.json      企业分析侧页面×依赖定义（自 enterpriseEvaluation.ts 等页面配置人工固化）
  - /tmp/main_md_info.json       页面主指标 md 信息（calc-logic 抽取）
  - /tmp/jiuxin_map.json         久新 93 条映射（02-久新版 xlsx 同源）
  - /tmp/dep_bridge.json         依赖维度→久新候选桥
  - /tmp/formula_sections.json   久新公式章节锚点（02-久新版增强列同源）
  - /tmp/tbl2line.json           ads 表→ADS_SCHEMA 行号锚点
输出：./UI页面指标-怎么算-靠什么数据-20261031.xlsx（128 行 + 明细 103 行 + 说明）
说明：中间 json 由当次会话抽取脚本生成；重跑对齐请先重抽（见产物总 README「复现」节）。
"""
print('见会话归档；本文件为复现入口占位，数据 json 已随 _work 归档')

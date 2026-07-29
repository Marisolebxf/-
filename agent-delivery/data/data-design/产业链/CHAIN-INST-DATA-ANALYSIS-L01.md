# CHAIN-INST-DATA-ANALYSIS-L01 — 产业链和国内机构库数据源分析与更新

> 任务 ID: CHAIN-INST-DATA-ANALYSIS-L01
> Epic: E-CHAIN-PROTOTYPE
> 责任人: [human:李伟]（架构师）
> 状态: in_progress（阶段产出）
> 日期: 2026-07-29

---

## 1. 任务范围

分析 `gkxlumenx_ods` 数据库中产业链和国内机构库的数据源，输出字段映射分析报告，更新数据模型和映射关系。

## 2. 产出文件清单

### 2.1 产业链数据源分析（DoD-1）

| 文件 | 位置 | 说明 |
|------|------|------|
| 产业链-ODS到DWD字段映射分析报告(v3).md | `agent-delivery/data/data-design/产业链/` | 完整的 ODS→DWD 字段映射分析，含覆盖率、缺口、ETL 建议 |
| ODS-DWD-字段对照与缺失明细.md | `agent-delivery/data/data-design/产业链/` | 7 张 DWD 表的逐字段对照表，含中文含义、来源 ODS 表名.字段名 |

### 2.2 国内机构库数据源分析（DoD-2）✅

| 文件 | 位置 | 说明 |
|------|------|------|
| 国内机构库-ODS到DWD字段映射分析报告.md | `agent-delivery/data/data-design/产业链/` | 13 张机构 ODS 表分析，仅 1 张有数据（innovation_carrier 1,404 行），覆盖率极低 |

### 2.3 数据模型更新（DoD-3）✅

本任务通过上述映射分析报告完成了数据映射关系的梳理，覆盖：
- 7 张产业链 DWD 表的字段映射（直接映射 / 计算映射 / 缺失）
- 3 张机构相关 DWD/ADS 表的字段映射
- NebulaGraph institution Tag / serves Edge 的灌数可行性

> 注：`产业链域数据库设计(v1).md` 的修订属设计文档修改，不在本分析任务范围内，待后续派单。

### 2.4 接口更新（DoD-4）⏭ 跳过

本任务仅做数据源分析，接口实施待后续派单。

### 2.5 验证报告（DoD-5）⏭ 跳过

本任务仅做数据源分析，灌数验证待后续派单。

### 2.6 Handoff

| 文件 | 位置 | 说明 |
|------|------|------|
| CHAIN-INST-DATA-ANALYSIS-L01.md | `agent-handoffs/` | 阶段性 handoff，含产出清单、核心发现、阻塞项、偏离说明 |

---

## 3. 产业链分析核心结论

### 3.1 ODS 源表（4 张有数据 + 辅助表）

| ODS 表 | 行数 | 用途 |
|--------|------|------|
| `dwd_industry_chain_info` | 527 | 产业链体系树（INB 编码，0–6 层级） |
| `dwd_org_industry_tags` | 4,912 | 企业→产业链标签（JSON 数组存多产业归属） |
| `dwd_org_industry_product_tags` | 5,000 | 企业→产业链→产品标签 |
| `dwd_industry_chain_news_info` | 5,000 | 产业链动态资讯 |
| `dwd_org_base_info` | 10,996 | 企业工商信息（辅助补字段） |
| `dwd_org_industry_chain_pat_dtl` | 888 | 产业链关联专利（辅助） |
| `dwd_org_innovation_carrier` | 1,404 | 创新载体（辅助） |

### 3.2 DWD 目标表（7 张）

| DWD 表 | 当前行数 | 可灌性 |
|--------|---------|--------|
| `chain` | 8 (mock) | ✅ 定编码后直接灌 |
| `chain_node` | 41 (mock) | ✅ 定编码后直接灌 |
| `chain_enterprise` | 120 (mock) | 🔧 需 ETL 加工 |
| `chain_news` | 200 (mock) | ✅ 定编码后直接灌 |
| `chain_region_dist` | 288 (mock) | 🔧 需 ETL 聚合 |
| `chain_investment` | 60 (mock) | ❌ 不可灌（ODS 空表） |
| `chain_enterprise_stat` | 209 (mock) | 🔧 需算法 |

### 3.3 关键发现

1. **编码体系不兼容**：ODS 用 INB 编码（INB1204 等），DWD mock 用国标编码（C2711 等），需先定编码方案
2. **投融资数据空表**：`dwd_org_invest_info` 和 `dwd_org_financing_info` 均为 0 行
3. **节点属性缺失**：ODS 无 `node_stage`/`node_type`/`node_imp_level` 等字段
4. **JSON 拆行**：`dwd_org_industry_tags` 的 `industry_code` 是 JSON 数组，需 Python ETL 拆行

### 3.4 有效覆盖率

| 维度 | 数值 |
|------|------|
| DWD 总字段（不含系统列） | 56 |
| ✅ 有来源 | 23 |
| ❌ 完全无来源 | 21 个字段 + 1 整张表 |
| ⚠️ 编码阻塞 | 7 张表全部 |
| 有效覆盖率 | **48%** |

---

## 4. 阻塞项

| 阻塞项 | 谁定 | 影响 | 决策清单 ID |
|--------|------|------|------------|
| 🟡 编码方案（INB vs 国标） | PM + 数据 Lead + 甲方 | 全部 7 张 DWD 表 | **Q053** |
| 🟡 投融资空表 | 数据供应方 / 甲方 | `chain_investment` 完全无法灌数 | **Q054** |
| 🟡 机构库主体表空 | 数据供应方 / 甲方 | `dwd_org_reg_info` / `dwd_org_sc_info` / `dwd_org_hels_info` 均为空 | **Q055** |

> Q053–Q055 已登记到 `客户决策清单跟踪表.md` §2.y（2026-07-29，[human:李伟]）。

---

## 5. 下一步计划

| 步骤 | 内容 | 状态 |
|------|------|------|
| 1 | 迁移产业链报告到 DoD 指定位置 | ✅ 完成 |
| 2 | 机构库 ODS 源表分析报告 | ✅ 完成 |
| 3 | 升级编码方案决策 | ⏭ 跳过（PM 处理） |
| 4 | 更新产业链域数据库设计(v1).md | ⏭ 跳过（仅分析不修改设计） |
| 5 | 查 /internal/* 接口 | ⏭ 跳过（仅分析） |
| 6 | ETL 灌数脚本 + 验证 | ⏭ 跳过（仅分析） |
| 7 | 更新接口实现 | ⏭ 跳过（仅分析） |
| 8 | 提交 handoff | ✅ 完成 |

---

*evidence 文件 · [human:李伟] · 2026-07-29*

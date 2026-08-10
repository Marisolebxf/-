# CHAIN-INST-DATA-ANALYSIS-L01 — 阶段性 Handoff

> 任务 ID: CHAIN-INST-DATA-ANALYSIS-L01
> Epic: E-CHAIN-PROTOTYPE
> 责任人: [human:李伟]（架构师）
> 日期: 2026-07-29
> 状态: in_progress（分析阶段完成，实施阶段待派单）

---

## 1. 范围与实现

### 1.1 任务目标

分析 `gkxlumenx_ods`（`111.198.38.90:34306`）中产业链和国内机构库的数据源，输出字段映射分析报告，识别数据缺口和阻塞项。

### 1.2 任务范围界定

本任务**仅做数据源分析**，不含：
- 修改设计文档（`产业链域数据库设计(v1).md`）
- 编写 ETL 灌数脚本
- 修改 /internal/* 接口实现
- 执行灌数验证

以上实施工作待后续派单。

---

## 2. 产出清单

### 2.1 产业链数据源分析（DoD-1 ✅）

| 文件 | 位置 | 说明 |
|------|------|------|
| 产业链-ODS到DWD字段映射分析报告(v3).md | `agent-delivery/data/data-design/产业链/` | 完整 ODS→DWD 映射分析，含覆盖率、缺口、ETL 建议 |
| ODS-DWD-字段对照与缺失明细.md | `agent-delivery/data/data-design/产业链/` | 7 张 DWD 表逐字段对照，含中文含义 + `表名.字段名` |

### 2.2 国内机构库数据源分析（DoD-2 ✅）

| 文件 | 位置 | 说明 |
|------|------|------|
| 国内机构库-ODS到DWD字段映射分析报告.md | `agent-delivery/data/data-design/产业链/` | 13 张机构 ODS 表分析，仅 1 张有数据 |

### 2.3 数据映射关系更新（DoD-3 ✅）

上述报告即为本任务的映射关系产出，已覆盖：
- 7 张产业链 DWD 表的字段映射
- 3 张机构相关 DWD/ADS 表的字段映射
- NebulaGraph institution Tag / serves Edge 的灌数可行性

### 2.4 evidence 索引

| 文件 | 位置 |
|------|------|
| CHAIN-INST-DATA-ANALYSIS-L01.md | `agent-delivery/data/data-design/产业链/` |

---

## 3. 核心发现

### 3.1 产业链

| 维度 | 结果 |
|------|------|
| ODS 有数据表 | 4 张（chain_info / org_industry_tags / org_industry_product_tags / chain_news_info） |
| 辅助表 | 3 张（org_base_info / industry_chain_pat_dtl / innovation_carrier） |
| DWD 目标表 | 7 张（chain / chain_node / chain_enterprise / chain_news / chain_region_dist / chain_investment / chain_enterprise_stat） |
| 有效覆盖率 | **48%**（v2 预期为 95%） |
| 完全无法灌数 | `chain_investment`（投融资 ODS 空表） |

### 3.2 机构库

| 维度 | 结果 |
|------|------|
| ODS 有数据表 | **仅 1 张**（`dwd_org_innovation_carrier`，1,404 行） |
| 机构主体表 | `dwd_org_reg_info` / `dwd_org_sc_info` / `dwd_org_hels_info` **全空** |
| 机构→产业链关联 | ❌ 不存在（innovation_carrier 无 industry_code 字段） |
| 机构成果数据 | 12 个字段中 11 个无源 |
| 可灌范围 | 仅 `realdata_research_org_stat` 的 4 个基础字段 + Nebula `institution` Tag |

---

## 4. 阻塞项与风险

| 编号 | 阻塞项 | 严重度 | 谁定 | 影响 | 决策清单 ID |
|------|--------|--------|------|------|------------|
| GAP-01 | 编码体系不兼容（INB vs 国标） | 🔴 | PM + 数据 Lead + 甲方 | 全部 7 张 DWD 表 | **Q053** |
| GAP-02 | 投融资 ODS 空表 | 🔴 | 数据供应方 / 甲方 | `chain_investment` 完全无法灌数 | **Q054** |
| GAP-03 | 节点属性缺失（node_stage/node_type 等） | 🟡 | — | `chain_node.position` 等 | —（数据缺口，非决策项） |
| INST-01 | 机构主体表全空 | 🔴 | 数据供应方 / 甲方 | 机构库多数字段无源 | **Q055** |
| INST-02 | 机构→产业链关联缺失 | 🔴 | — | `chain_institution_stat` 无法按链统计 | —（待数据到位后由算法建立映射） |
| INST-03 | 机构成果数据缺失 | 🔴 | — | `org_achievement_year` 11/12 字段无源 | —（同 INST-01，数据到位后解决） |

> Q053–Q055 已登记到 `客户决策清单跟踪表.md` §2.y（2026-07-29，[human:李伟]）。

---

## 5. 偏离说明

| 项 | DoD 原文 | 实际处理 | 原因 |
|----|---------|---------|------|
| DoD-4 | 更新 /internal/* 接口以支持新数据源 | ⏭ 跳过 | 本任务仅做分析，接口实施待后续派单 |
| DoD-5 | 验证数据接入和处理流程 | ⏭ 跳过 | 同上，灌数实施待后续派单 |

---

## 6. 产物清单

| 类型 | 文件 | 位置 |
|------|------|------|
| 分析报告 | 产业链-ODS到DWD字段映射分析报告(v3).md | `agent-delivery/data/data-design/产业链/` |
| 字段对照 | ODS-DWD-字段对照与缺失明细.md | 同上 |
| 分析报告 | 国内机构库-ODS到DWD字段映射分析报告.md | 同上 |
| evidence | CHAIN-INST-DATA-ANALYSIS-L01.md | 同上 |
| handoff | 本文件 | `agent-delivery/agent-handoffs/产业链分析-CHAIN/CHAIN-INST-DATA-ANALYSIS-L01.md` |

---

## 7. 验收证据

- ✅ 产业链 4 张 ODS 表结构已梳理（527 + 4,912 + 5,000 + 5,000 行）
- ✅ 机构库 13 张 ODS 表已排查（仅 1 张有数据）
- ✅ 7 张 DWD + 3 张机构目标表字段映射已完成
- ✅ 数据缺口和阻塞项已识别（6 项）
- ✅ 产出文件已放置到 DoD 指定位置

---

## 8. 架构合规自检

| 铁律 | 状态 |
|------|------|
| D3 契约面=ADS，Java 只读 | ✅ 分析未涉及 Java |
| D7 数据契约先行 + Mock 先行 | ✅ 分析覆盖 ODS→DWD 链路 |
| ODS 只读引用 | ✅ 全程只读查询 |
| 不越层 | ✅ 分析范围限于 ODS→DWD |

---

## 9. 下一步建议

| 优先级 | 动作 | 负责 |
|--------|------|------|
| P0 | 编码方案决策（INB vs 国标） | PM + 数据 Lead |
| P0 | 向供应方索要投融资数据 | PM |
| P0 | 向供应方索要机构主体表数据 | PM |
| P1 | 派单 ETL 灌数脚本（chain/chain_node/chain_news 三表） | coordinator |
| P1 | 派单 /internal/* 接口更新 | coordinator |
| P2 | 建立机构→产业链映射（NLP 或人工标注） | algorithm-agent |

---

*handoff · [human:李伟] · 2026-07-29 · CHAIN-INST-DATA-ANALYSIS-L01*

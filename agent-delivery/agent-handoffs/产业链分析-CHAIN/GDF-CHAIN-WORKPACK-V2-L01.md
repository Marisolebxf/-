# GDF-CHAIN-WORKPACK-V2-L01 · 产业链维 GDF 派单包 v2 — 10-19 基线对齐

> 交付日期：2026-10-20（晚）· 监管：`human:徐滕强`

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:徐滕强` |
| claim_type | `pull`（随 V4 同批派单） |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `off`（definition/派单文档类任务） |

## 1. 范围与实现

架构师指令（随企业 v4 同批）：产业链包按 10-19 基线核查更新为 v2。

**核查结论：变更面小**——产业链四表全部在 10-19 清单、行数不变（链树 1,296 / tags 2,197,216 估 / 产品 73,313 / 资讯 94,997）。

交付（commit `4072d369`，随 V4 同批）：

1. `GDF-CHAIN-WORKPACK-v2`（v1 整包继承 + 四处修订）：
   - 00/README/CHANGELOG：版本 v2.0、状态升"可对外投递"
   - 02：版本头注 + summary 加 v2.0 基线说明（与 ENT v4 拆分对称声明继续有效）
   - 09：**live 实证修订**——`dwd_industry_chain_info` 含 `parent_name` 列（§3.1/§3.2 注记"不映射、JOIN 派生"）；10-19 纪要所列 `t_id`/`id`/`code_company_count` live 不存在不作源；头注版本块 v1.0→v2.0、派单包指针改指本目录
   - 06：派工标题对齐 v2.0
2. 逐卷内容级排查（00/03/04/06/09/10/11/README）：03 连接已是 10-19 新地址；04/10/11 无受变更影响引用；链树表 pk_id 主键体系经 SHOW CREATE TABLE 确认（ODS 重建同步修正）

## 2. 偏离说明

无——变更面与预期一致（四表不变，仅注记与版本收口）。

## 3. 产物清单

| 产物 | 位置 |
|---|---|
| v2 包全套（12 文件） | `agent-delivery/data/GDF/派单包/产业链/GDF-CHAIN-WORKPACK-v2/` |
| git commit | `4072d369` @ origin/dev（随 V4 同批） |

## 4. 验收证据

- ODS 链四表随 62 张重建终验：17/16/15/18 列与 live 零差异（含链树 pk_id 主键 + parent_name + utf8mb4_bin）
- v2 包终检：YAML OK、09 v2.0 头注在、无 v1.0 版本残留（仅合理历史引用）

## 5. 架构合规自检

| 铁律 | 状态 |
|---|---|
| INB 主键（Q053） | ✅ 不变 |
| B2 禁洗 / news_event 禁灌 | ✅ 不变 |
| 与 ENT 拆分对称（§1.3 ↔ ENT §1.6） | ✅ 双向声明已闭合 |
| commit 标记 | ✅ `[agent:data]`（随 V4 批次） |

## 6. 遗留与移交

- CHAIN-B3-ENTITY-REL 依赖 ENT `enterprise_base`（v4 基线下不阻塞前置）
- `dwd_org_industry_tags` tags 拆行规则不变；GDF 施工按 v2 包 09 执行

# GDF-ENT-WORKPACK-V4-L01 · 企业维 GDF 派单包 v4 — 10-19 基线切换

> 交付日期：2026-10-20（晚）· 监管：`human:徐滕强`

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:徐滕强` |
| claim_type | `pull`（架构师口头派单"重新生成 v4/v2"后补单） |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `off`（definition/派单文档类任务） |
| 说明 | 文档包生成，无代码缩量目标；包内容完整性优先 |

## 1. 范围与实现（对照派单指令）

架构师指令：三方真源 10-19 发生表变更/删除，旧派单包可能不可用，按新表信息重新生成企业 v4、产业链 v2。

交付（commit `4072d369`，43 文件 +8131/-1699）：

1. **`GDF-ENT-WORKPACK-v4`（62 张，基线 = 10-19 承诺清单 176 表 ∩ 企业域 + live 实证）**，v3 整包继承后按四项拍板改造：
   - **拍板①（2026-10-20 徐滕强）stock_base 移出**：10-19 删除清单第 3 号（曾有 1,080 行）；`is_listed` 回归 `dwd_org_base_info.listing_status`，`listed_code`/`listed_market` 改源 `stock_finance_info`，`stock_noun` 置空（09 §3.1/§3.1.2 v4 注）
   - **拍板② 国外母子换源 `dwd_agg_subsidiary_info`**（live 19,810 行）替代从未存在的 `dwd_forg_subsidiary_info`——A1 阻塞解除；09 §3.21 新 mapping；**诚实声明：eid→org_id 实测命中率仅 6.3%（952/15,112）**，精确匹配+治理清单，禁造 ID；ES `forg_relations` 母子段解冻（12 号文注记）
   - **拍板③ 专利 5 张新侧表 mirror_only**（priority_filings 20,709 / claim 10,578 / description 15,900 / transfer 21,193 / family 16,235）：`enterprise_patent_detail` 无承接列不 ADD；transfer 走 `detail_json` 另拍板
   - **拍板④ enterprise_base 主键 = id、org_id 唯一键**（推翻 10-12 org_id 主键方案）：data-design 工商表 v3.1 + v4/10 快照 + 正式库（ALTER 已执行验证）+ demo 库（本已正确）四方同步
2. **全卷对齐**（不只版本号）：00（Q-WP3 确认表 7 处旧阻塞/旧口径修正）、01/02（62 张含 v3.1.6 扩入 5 张+专利四分表补登记）、05（全量重做 62 张 P0=15/P1=33/P2=14）、06（重写）、07（3 处）、09（§1.6 拆分对称声明、§3.13.5-补司法回补、§3.20 年报资产、§3.21、§3.15.7 废止横幅、E3/E1' 勘误、62 张口径）、10（data-design 最新版重同步含唯一键与主键拍板）、11（v3→v4 变更对照表）、12（母子解冻+上市字段来源注）、13（换源解除+v4 差集）；16 号文移出（留 v3 包归档）
3. **口径澄清（实测依据）**：10-19 纪要"Excel 多出"列（t_id/区划码等 153 表）live 库不存在——一律以 live 结构施工；chain_dtl/pat_dtl 从未出现在任何一版承诺清单（非"承诺后被删"），score/segment_key 置 NULL、chain_patent 不灌，需供应方新增承诺
4. **ODS 62 张全量重建**（`ODS建表DDL-live重建/`）：每张 `SHOW CREATE TABLE` 直出自 live gkx，同名同构一字不差；已执行并终验 62/62 表逐表列数零差异。**过程弯路（如实记录）**：首批用 7 月沙箱快照致 32 张不一致→手写 DDL 有 COLLATE/派生表名 bug→最终 SHOW CREATE TABLE 直出+两轮修复（assignees 表名、利润表 22 列执行截断）全部闭环
5. 总 README 重排（v4/v2 现行、v3/v1 降历史）

## 2. 偏离说明

- 投递 zip 取消（用户拍板：由人在例会/飞书口头告知 GDF）
- git 提交等全部验证通过后放行（用户拍板，实际 23:05 放行完成）

## 3. 产物清单

| 产物 | 位置 |
|---|---|
| v4 包全套（16 文件） | `agent-delivery/data/GDF/派单包/企业/GDF-ENT-WORKPACK-v4/` |
| ODS 重建 SQL ×3 | `agent-delivery/data/GDF/ODS建表DDL-live重建/` |
| 设计稿主键修订 | `agent-delivery/data/data-design/企业/DWD表结构设计-企业工商表-MySQL-v3.1.md` |
| git commit | `4072d369` @ origin/dev |

## 4. 验收证据

- ODS 终验：62/62 表、逐表列数 vs live SHOW CREATE TABLE 实测记录**零差异**（含 income_statement 128 列、forg_base 31 列、链树 17 列）
- enterprise_base 主键：正式库实测 PRIMARY=id + uk_enterprise_base_org_id，无残留
- v4 包终检：YAML 语法/无重复表/关键节全在/零旧残留/敏感信息零命中
- 交叉验证：10-19 纪要结论与 live information_schema 逐项核对（上游材料本身以 live 为准过滤）

## 5. 架构合规自检

| 铁律 | 状态 |
|---|---|
| 调用链（前端→Java→Python） | ✅ 包内 12/14 卷不变更边界 |
| D12 demo/lumen 隔离 | ✅ ODS 重建只动 `gkxlumenx_ods`（产线），GDF 不连 demo |
| D8/D9/D10 | ✅ 不涉及前端；指标口径未动 |
| 对外集成物人评审 | ✅ 用户全程逐项审查（多轮指正已修：00 旧表残留、06 旧版本、10 快照过期、链树结构错误） |
| commit 标记 | ✅ `[agent:data]` |

## 6. 遗留与移交

- Q3 专利匹配：维持严格精确匹配（拍板），实测命中率数据落库后再议放宽
- chain_dtl/pat_dtl：需供应方新增承诺（当前永不伪造置空）
- E5 逐字段复验：09 头注已声明进行中，发现项随后续小版本回写
- 投递 GDF：由用户在例会/飞书口头告知（含"作业地址已切 10.50.11.76"）

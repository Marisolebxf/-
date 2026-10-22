# GDF-ENT-WORKPACK-V4R2-L01 · 企业维派单包 v4.0.1/v4.0.2 — GDF round1/round2 核对响应合并

> 交付日期：2026-10-21（晚，v4.0.1）· 2026-10-22（v4.0.2，round2 问询 31 题）· 监管：`human:徐滕强`

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:徐滕强` |
| claim_type | `pull`（GDF round1 核对回传后，徐滕强确认建单处理） |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `off`（派单文档修订类任务） |

## 1. 范围与实现

**触发**：GDF 侧回传 v4 包第 1 轮核对材料（7 文件：核对报告 + 10 条澄清清单 [blocking 3] + 4 附录），结论=贴源层放行（61/62 表、288 列零缺失）；加工层 555 需逻辑列缺 277（50%）；62 张表 0 张声明抽取方式；母子表 §3.21 六个映射列与正式库 DDL 硬冲突。

**交付（合并回 v4 包，git 待推）**：

### round2 十条澄清逐条回复

| # | 条目 | 回复结论 |
|---|---|---|
| P-05 | 母子 6 列与 DDL 不符 | §3.21 替换：目标列=正式库实际 8 列 org_id/sub_org_id/sub_name/sub_country_code/sub_country_name/create_time/update_time（原 parent_org_id 等 6 列废止）；ename/source_table 入治理清单；UK 冲突取 updated_time 最新 |
| P-04 | 277 列无加工逻辑 | 四类处置：193 列签"本期不洗"（§1.7 集中清单，签字徐滕强）；专利宽表 6 列本轮补映射（§3.14.1.2~1.5）；base 32 列引 Q-WP3-29 既有拍板；财务 6 比率列升级甲方（cannotAnswer） |
| P-03 | 13 张表无 section 映射 | 专利四分表本轮补 §3.14.1.2~1.5；§3.1.3 org_product 独立小节；其余 9 张映射实际存在（§3.12/§3.18/§1.2/§3.14.1.1），§2.4.1 指路表给确切位置 |
| P-01 | tag_dict 空 / code_region 就绪 | tag_dict 本期不灌（tag_category 全 NULL）；code_region 确认使用 |
| P-02 | 09 含 2 张非贴源表映射行 | §3.15.7 清理 + §3.9 旧名改注（历史对照入附录） |
| P-06 | org_rel 无 DDL | 10/ 工商表尾部补 as-built DDL |
| P-08 | 23 张表无源/无口径 | §1.7 集中声明"本期不洗"（与 P-04① 同一清单） |
| P-09 | 行过滤落点与脏数据 | §1.8 新增规则表 |
| S-04 | forg_college 口径不一 | 移入 pending_source_requests |
| S-06 | 62 张无抽取方式声明 | 02 新增 extract_mode/watermark_column/lookback/schedule 4 字段；统一策略=首次全量+T+1 updated_time 增量（>= 水位-1 天，upsert 幂等）；增量不过滤 is_deleted；每周 COUNT 对账 |

### 变更文件清单

| 文件 | 变更 |
|---|---|
| 09 | §3.21 替换（对齐 DDL）；§3.14.1.2~1.5 新增；§3.1.3 新增；§1.7/§1.8 新增；§2.4.1 指路表；§3.15.7/§3.9 清理；头注升 v4.0.1 |
| 02 | 抽取策略 4 字段；forg_college 移 pending；summary v4.0.1 |
| 05 | P0/P1 表头加 3 列（extract_mode/watermark/last_wm） |
| 10/ 工商 v3.1 | 尾部追加 org_rel as-built DDL |
| CHANGELOG | v4.0.1 全量记录 |

### 关联（非本单但同期完成）

- Bugbot 审查 3 发现全修复（default_filter 与增量策略矛盾→已废止改注释；05 表头未实际加列→已补；patent_history 指向 §4.1→改 §3.14.2）
- round2 vs 派单包逐项对账：脚本对账零差异
- GDF round1 核对的回复函 5 文件（round2/ 目录，GDF 回传目录旁）

## 2. 偏离说明

- API/python 调用案例：用户拍板不放本单，后置（GDF 需先明确测试目的）
- 财务 6 比率列：cannotAnswer 升级甲方（铁律 8），拍板前返回空
- 投递 zip：沿用 V4 拍板取消（口头/飞书告知）

## 3. 产物清单

| 产物 | 位置 |
|---|---|
| v4.0.1 修订版包 | `agent-delivery/data/GDF/派单包/企业/GDF-ENT-WORKPACK-v4/` |
| round2 回复包 5 文件 | GDF 回传目录 round2/（发 GDF） |
| git commit | 待推送（本单 git 推送等验证放行） |

## 4. 验收证据

- Bugbot 审查：3 发现全部修复并终检通过
- round2 vs 派单包逐项对账：脚本对账零差异
- YAML 语法全过（02 v4.0.1）
- P-03 三层核实：招投标/港澳台映射实际存在（§3.12/§3.18），仅专利四分表真缺（已补）
- §3.21 母子表正式库 8 列实测（2026-10-20 information_schema）

## 5. 架构合规自检

| 铁律 | 状态 |
|---|---|
| 调用链不变更 | ✅ 本单纯文档修订 |
| D12 隔离 | ✅ 不涉及 demo |
| D8/D9/D10 | ✅ 不涉及前端；指标口径未动 |
| commit 标记 | ✅ `[agent:data]`（待推） |

## 6. 遗留与移交

- API/python 案例第二轮提供（GDF 先明确测试目的）
- 财务 6 比率列口径升级甲方拍板
- E5 复验：GDF 附录 B 反哺后收口（277 列结论已落 §1.7）
- task-registry.yaml 本地态由 coordinator/淮政玮提交（MCP 写入的本地改动不归 data-agent 管）

---

## 7. v4.0.2 追加交付（2026-10-22，GDF round2 问询 31 题拍板合入）

**触发**：GDF 回传 round2（`交付客户-round2/`：00 核对回复 + 01 回填表 31 题 + 附录）；加工层口径 34/36 齐、6 表 13 字段缺映射、3 表关联没写清、3 汇总表待确认洗不洗、2 表缺 DDL。

### 31 题拍板落点（全部 human:徐滕强 逐题拍板）

| 组 | 结论 | 落点 |
|---|---|---|
| Q1~Q3 洗不洗争议 | 3 张全洗，36 张不变 | `09`§4.2/§4.3 SQL 重写（JOIN `gkxlumenx_dim.code_region`）；新增 §4.4 patent_history 7 指标聚合 |
| Q4/Q31 物理删除 | 源不物理删 + 季度全量比对 | `09`§1.8 追加一行 |
| Q6~Q13 news 8 字段 | data_source 直接映射；industry_category/region 关联 base；5 列 NULL | `09`§3.5 |
| Q14 gender / Q16 event_date / Q18 bid_type / Q23 headquarters_address | 留空不洗 / 复核确认 | `09`§3.2/§3.8/§3.12/§3.1.2 |
| Q15 end_date | LEAD 窗口推导 | `09`§3.6 |
| Q17 patent data_source | `table_data_source` 直接映射 | `09`§3.14.1 |
| Q19 财务三源 | `(org_id,data_year,data_source)` 共存不覆盖 | `09`§3.3 |
| Q20 forg_extra | 主档建行、product 只补 NULL | `09`§3.15.2/3 |
| Q21 母子未命中 | 整行丢弃进治理清单 | `09`§3.21 |
| Q22 经营范围 | 源 `main_activities`（注释「公司经营范围」）→ 落 `business_scope`，目标 main_activities 留空 | `09`§3.1.2/§3.1.3 |
| Q25 研发投入 | `yftrje`→`rd_investment`、`yfrysl`→`rd_staff_count` 全部期共存放开洗 | `09`§3.20 |
| Q26~Q28 tag 三题 | tag_value 备用不写；JOIN 键 `org_tag=tag_dict.tag_name`；tag_dict 我方维护灌 7 行种子 | `09`§3.9 |
| Q29/Q30 缺 DDL | org_rel 复核在位；risk_summary as-built DDL 补 §7.1（现网逐列核对） | `10/` 两份 v3.1 |

### 数据库变更（正式库 gkxlumenx_dwd 已执行并核验）

1. `enterprise_tag` 唯一键 `uk_ent_tag` → `(org_id, tag_code)`（原键含 tag_value 全 NULL 失效，T+1 重跑膨胀；用户拍板）
2. `tag_dict` 灌入 demo 7 行种子（外资/瞪羚/高新/上市/专精特新/科技型中小企业/独角兽）

### 设计文档同步（data-design/企业/，用户抽查发现漏同步后补齐）

- 工商表 v3.1：uk_ent_tag 改键 / 换源注 2 处 / §9 org_rel as-built DDL
- 指标汇总表 v3.1：§7.1 risk_summary as-built DDL
- ETL-Mapping：§3.9 标签段重写（源表正名/JOIN 键/tag_value）/§3.1.2 经营范围改 business_scope / stock_base 换源注 / §4.2~4.4 改指路派单包 09

### 交付物（发 GDF）

`交付客户-round2/round3/`：01-回填表-第2轮-已回填.md + answers-round2.json + GDF-ENT-WORKPACK-v4 副本（19 文件）

### 自检证据

- §3.20 无重复行（yftrje/yfrysl/nsze 顺序核验）
- 正式库 information_schema 复核：enterprise_tag 新键 2 列 ✅、tag_dict 7 行 ✅
- 15 张不洗风险表逐张对源库/demo 库零散抽查：全部无源，判定一致（有源 9 张全洗、无源 15 张全不洗）
- round3 副本与主仓一致性：重新复制后 grep 头部 v4.0.2 ✅

### cost

| 字段 | 值 |
|---|---|
| ponytail | `off`（派单文档修订类任务，同本单主体） |

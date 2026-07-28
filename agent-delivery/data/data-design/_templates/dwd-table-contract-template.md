# DWD 表设计契约模板（Phase 1）

> **用途**：项目自研 DWD 表的设计真源模板。架构师按业务需求填此契约；**不与甲方 ODS（供应库 `dwd_*`）一一对应**。  
> **阶段**：Phase 1（现在 ~ 2026-08-20，ODS 未稳定）— 只治理项目 DWD 设计；Phase 2（8/20 后）由 GDF 对照本契约的 `ods_mapping_expectation` 做映射。  
> **权威规约**：`agent-delivery/data-lineage-policy.md` §2.2  
> **连接真源**（只读 ODS）：`agent-delivery/data/third-party-source/gkx-mysql-raw/CONNECTION.md`（密码禁止写入本文件）  
> **维护**：lineage-subcoord（Phase 1）主导；architect-agent 审设计；data-agent 建表时遵循。

---

## 使用方式

1. 复制本文件到 `data/data-design/{要素}/`，重命名为 `dwd_{table_name}.md`
2. 填「表头元数据」与「字段定义」；每个业务字段必须有 `ods_mapping_expectation`
3. 把契约路径登记到本要素的索引表（若有）
4. metric 的 `source_tables[]` 引用本表名；`mapping_status` 在 Phase 1 统一标 `⏳ pending_ods`

---

## 表头元数据

```yaml
table: dwd_example_entity          # 项目自研 DWD 表名（勿照抄供应库表名）
layer: DWD
element: ENT                       # ENT/CHAIN/ORG/TECH/TALENT/SVC/POLICY/SS/IC/INNOV/COMMON
design_owner: architect            # 设计负责人角色
design_phase: phase1               # phase1 | phase2
ods_dependency: none               # Phase 1 固定 none；Phase 2 映射完成后可改为 mapped
related_metrics: []                # 引用本表的 metric_id 列表
bid_refs: []                       # bid-reference 章节号
acceptance_units: []               # DS-XX 列表
status: draft                      # draft | review | approved
updated: "YYYY-MM-DD"
```

### 业务说明

| 项 | 内容 |
|----|------|
| 中文表名 | （填） |
| 一句话用途 | （填：支撑哪些页面/指标） |
| 粒度 | （如：一企业一行 / 一项目一行） |
| 主键 | （填） |
| 业务键 | （填；见 `gkx-platform-business-keys.md`） |
| 与供应库关系 | **非一一对应**。供应库 `dwd_*` = 本项目 ODS；本表为项目自研 DWD |

---

## 字段定义

> `confidence`：`high`=语义明确、易映射；`medium`=可能有命名差异；`low`=供应侧可能缺失（Phase 2 重点核对）

```yaml
fields:
  - name: id
    type: bigint
    nullable: false
    business_def: 代理主键
    metric_ref: null
    ods_mapping_expectation:
      expected_from: "供应侧主表代理键或可推导唯一键"
      confidence: high
      note: ""

  - name: biz_code
    type: varchar(64)
    nullable: false
    business_def: 业务主键（示例：统一社会信用代码）
    metric_ref: null
    ods_mapping_expectation:
      expected_from: "甲方 dwd_* 中企业/主体主表的代码类字段"
      confidence: high
      note: ""

  - name: name
    type: varchar(255)
    nullable: false
    business_def: 主体名称
    metric_ref: null
    ods_mapping_expectation:
      expected_from: "甲方 dwd_* 中对应主体的名称/标题类字段"
      confidence: high
      note: ""

  # —— 复制下面块继续追加业务字段 ——
  # - name:
  #   type:
  #   nullable:
  #   business_def:
  #   metric_ref:          # 若直接支撑某指标，填 metric_id；否则 null
  #   ods_mapping_expectation:
  #     expected_from:     # 期望从 ODS 哪类字段来（语义描述，不绑死具体表名）
  #     confidence: high|medium|low
  #     note:
```

### 字段一览（给人读的表）

| # | 字段名 | 类型 | 可空 | 业务定义 | metric_ref | expectation.confidence | expectation.expected_from |
|---|--------|------|------|----------|------------|------------------------|---------------------------|
| 1 | id | bigint | 否 | 代理主键 | — | high | 供应侧主表代理键 |
| 2 | biz_code | varchar(64) | 否 | 业务主键 | — | high | 主体代码类字段 |
| 3 | name | varchar(255) | 否 | 主体名称 | — | high | 名称/标题类字段 |

---

## Phase 2 映射验收清单（8/20 后勾选）

- [ ] GDF 已为本表产出 ODS→项目 DWD 字段级 mapping
- [ ] lineage-subcoord 已验证完整度
- [ ] 引用本表的全部 metric：`mapping_status` 已从 `⏳` 升级为 `✅` 或 `❌`
- [ ] 若有 `❌`：已登记 `data-gap-catalog.yaml` + `客户决策清单跟踪表.md`（🟡）
- [ ] UI 已移除本表相关指标的 ⏳ OdsPendingBadge（或转为 ⚠️）

---

## 变更记录

| 日期 | 变更 | 作者 |
|------|------|------|
| | 初稿 | |

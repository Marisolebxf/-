# GDF-ENT-WORKPACK-V3-L01 · 企业维 GDF 派单包 v3

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:徐滕强` |
| claim_type | `pull` |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `N/A`（定义 / 数据派单文档） |

## 范围与实现

- 对照企业维范围，形成 `agent-delivery/data/GDF/派单包/企业/GDF-ENT-WORKPACK-v3/` 现行施工包（v3.0 **可对外投递**），含 `13-现网DDL差集-GDF开工必读.md`。
- Wave A 清单收口为 48 张（P0=16、P1=26、P2=6），另列 1 张供应方待核实表。
- 财务金额目标单位统一为“万元”；GDF 须按 live 字段含义、样本和单位证据决定换算，未知单位不得直接入目标表。  
- 国内 `enterprise_finance_history` 补回 `total_assets` / `total_liabilities`（源表有；年末时点存量，ES 取最新一年）。
- live 核验无 `dwd_org_industry_chain_dtl`；本期先用 `dwd_org_industry_tags` 覆盖可得字段，并保留供应方补表请求。
- live `gkx.dwd_org_financing_info` 已有数据，直接纳入贴源 / Mapping，不再以“迁金融库”作为阻塞项。
- 专利按申请人、权利人完整角色表做企业名称精确匹配，新增 `enterprise_patent_org_rel`；未命中不造 `org_id`，进入治理清单。
- 港澳台企业纳入 `enterprise_base`；恢复 `region_id`，`enterprise_code` 改为可空。无 `org_id` 记录不得伪造，进入治理清单。
- 重出 `05-WaveA-验收检查表.md`，纳入单位证据、DDL 差集、专利关系、港澳台和拒绝清单验收。
- DWD→ES 写入 `lumen-etl-es-py` → 物理索引 `gkx_enterprise_v1` / `gkx_enterprise_global_v1`（别名 `gkx_enterprise`）；`12` 已写入模块水位 + Painless 更新逻辑，不再只给指针。Java、前端禁止直写。
- DWD→图谱：`14` 写明菜单 A/B/C + `op_id` 投影 Nebula；GDF/灌数禁止写图；正式 lumen 写图链不在本叶编造。
- `OPEN-ENT-FLOW-01/04` 与 `OPEN-ENT-GRAPH-*` 保持独立任务，本叶只引用真实状态，不伪装为已补齐。

## 监管人确认记录

2026-09-02，`human:徐滕强` 确认：

1. 财务统一到万元，由 GDF 基于实际数据判定换算；
2. `chain_dtl` 先核验存续与分层；
3. 核清“迁金融库”的物理库含义；
4. 专利多个企业名称均需匹配，必要时补目标关系字段 / 表；
5. 新任务重出验收表；
6. 先核实 `OPEN-ENT-FLOW-01/04` 是否完成；
7. 港澳台纳入本期，信用代码允许为空，不得伪造；恢复企业主表 `region_id`。

## 偏离说明

- `dwd_org_industry_chain_dtl` 当前不在 live `gkx`，不能按既有源表施工；以 `industry_tags` 作为本期可执行路径，缺失源继续独立追踪。
- 澳门存在缺 `org_id` 记录。本包不生成新主键，只接收可回连企业主档的记录；其余进入治理清单。
- `OPEN-ENT-FLOW-01/04` 不合并进本叶，避免把历史未完成项误报为本包已交付。

## 验收证据

- `02-WaveA-贴源表清单.yaml`：Ruby YAML 解析通过。
- `git diff --check`：通过。
- 陈旧口径扫描：无“40 张”“§8 未裁表”“专利本波不做”“港澳台暂不”等残留。
- live 核验摘要：`gkx` 无 `dwd_org_industry_chain_dtl`；`dwd_org_industry_tags` 18,818 行；`dwd_org_financing_info` 42,104 行；港、台各 40,000 行且均有 `org_id`；澳门 792 行，其中 396 行有 `org_id`。  
- 2026-09-02 两库已落地：`enterprise_base.region_id`、正式库 `enterprise_code` 可空、`enterprise_patent_org_rel`、财务 `total_assets`/`total_liabilities`。  
- live `gkx` 48 张施工表 45 张可见；未见 `dwd_org_tag_info`（仅见 `dwd_org_tech_tag`）、`dwd_forg_subsidiary_info`、`dwd_org_industry_chain_dtl`。  
- 正式库 `enterprise_patent_detail` / `enterprise_news` / `enterprise_bid` 等仍缺 `10/` 设计列，GDF 按 `13` 只 ADD 不 DROP。本叶不包含 Wave A/B 已导入绿。

## 架构合规自检

- D1 算法只在 Python：✅ 本叶不在 Java 实现算法。
- D2 前端 → Java → Python：✅ 未改变调用链。
- D3 NebulaGraph：✅ 图谱只认 Nebula；`14` 禁止 Neo4j / Java 直连 nGQL / 灌数建图。
- D4 可观测性：✅ 本叶为定义包，无运行时代码变更。
- D5 CI/CD：✅ 文档定义任务，`cicd: skip`。
- D6 demo 只读 merge：✅ 未修改或合并 demo / lumen 业务仓。
- D7 共享聚合核心：✅ 未改变共享服务边界。
- D8 ADS 先行 / Mock：✅ DWD、ES 边界明确，未伪造 live 完成态。
- D9 数据血缘：✅ 财务单位、来源、转换和未命中治理均保留追溯。
- D10 交互规范：✅ 不涉及 UI。
- D11 架构基线：✅ DWD→ES 写入方保持 `lumen-etl-es-py`。
- D12 demo / lumen 隔离：✅ 未引入任何 lumen→demo 依赖。

## CI/CD

- 分支：`dev`
- commit：本轮随监管人「就要推送」提交 `origin/dev`
- pipeline：`cicd: skip`（仅编排文档）
- K8s rollout：不适用
- 验证：YAML 解析、`git diff --check`、口径扫描均通过

## 成本

- actual_tokens：80,000（会话估算；平台未提供精确计量）
- model_used：Cursor Auto（混合模型）
- actual_cost：$0（平台未提供本任务可归因计费，非“零消耗”）
- cost_warn：green（计费不可归因）

## 产物清单

- `agent-delivery/data/GDF/派单包/企业/GDF-ENT-WORKPACK-v3/`
- `agent-delivery/data/GDF/派单包/README.md`
- `agent-delivery/data/GDF/派单包/企业/GDF-ENT-WORKPACK-v2/README.md`
- `agent-delivery/agent-handoffs/企业战略分析-ENT/GDF-ENT-WORKPACK-v2-投递说明.md`
- 本 handoff

## 遗留风险

- `dwd_org_industry_chain_dtl` 是否补供仍依赖供应方。
- 财务源单位必须由 GDF 用真实数据和单位证据核验后回签。
- 专利名称精确匹配与港澳台无 `org_id` 记录会产生治理清单，不应以造 ID 提高覆盖率。
- 本 handoff 不代表 Wave A/B 已导入成功，也不代表 ES 已重建、图谱已灌绿，也不代表 `OPEN-ENT-FLOW-01/04` / `OPEN-ENT-GRAPH-*` 已完成。

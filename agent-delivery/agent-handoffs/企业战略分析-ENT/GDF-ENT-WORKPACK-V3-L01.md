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
- 国内 `enterprise_finance_history` 补回 `total_assets` / `total_liabilities`（源表有；年末时点存量，按年写入 `financials`）。
- live 核验无 `dwd_org_industry_chain_dtl`；本期先用 `dwd_org_industry_tags` 覆盖可得字段，并保留供应方补表请求。
- live `gkx.dwd_org_financing_info` 已有数据，直接纳入贴源 / Mapping，不再以“迁金融库”作为阻塞项。
- 专利按申请人、权利人完整角色表做企业名称精确匹配，新增 `enterprise_patent_org_rel`；未命中不造 `org_id`，进入治理清单。
- 港澳台企业纳入 `enterprise_base`；恢复 `region_id`，`enterprise_code` 改为可空。无 `org_id` 记录不得伪造，进入治理清单。
- 重出 `05-WaveA-验收检查表.md`，纳入单位证据、DDL 差集、专利关系、港澳台和拒绝清单验收。
- DWD→ES：`12` 17 模块分开触发；写库 `lumen-etl-es-py`。GDF 表成功后异步打模块，回执关单（`15`）。
- DWD→图谱：`14` 日批按表→`op_id`；菜单仍给人用。GDF/灌数不写 nGQL。
- `15` 钉死：GDF→Java→Python；长任务异步。**当前投递态 = §6.1**（飞书值班 + 本侧转发 + 轮询 status）。§4 `/ent/v1` + webhook **未落地**（`OPEN-ENT-GDF-TRIGGER` / `CALLBACK` / `ETL-JOBID`）。
- 代码评审补齐（2026-09-02）：父 README 去掉 draft；`13` 第 6 步对齐触发；`12` §3.4 字段级策略；`09` 复核范围诚实句；`08` 非施工真源；口令脱敏；`finance.py` 写出资产/负债。
- `OPEN-ENT-FLOW-01/04` 与 `OPEN-ENT-GRAPH-*` 保持独立，不伪装已关。
- Q-WP3-18：供应链本期不做。`dwd_org_sc_info` **标为潜在可能**（双边企业+信用代码，要素库无表，`type` 1/2 未确认）；不贴不洗 `enterprise_supply_chain`；不触发 ES `supply_chain` / `ENT_RE_SUPPLY`。缺源不硬造。
- Q-WP3-19：链专利本期不洗。设计源 `dwd_org_industry_chain_pat_dtl` 现网/要素库均无；禁止 `dwd_patent` + IPC 硬挂。明细 / `patent_org_rel` / 按年计数照旧。
- Q-WP3-20：国外股东维持洗进 `enterprise_forg_invest`（无单独国外投资表）。
- Q-WP3-21：并购事件表可贴源不洗；不建 DWD；当事人表不贴。
- Q-WP3-22：利润两列都洗（`total_profit` ADD；`pure_profit`→已有 `net_profit`）。收入两列源都有，分开洗，不合成。固定资产仍 ADD `total_fixed_assets`。ES `finance.py` 现把利润总额双写进 `pure_profit`，改读另开。
- Q-WP3-23（2026-09-03 改口）：专利详情按设计稿宽列 **可 ADD**；现网 `patent_name`/`publish_date`/`ipc_code` 不 DROP。IPC 源=`main_classification_ipcr`。DDL 另开对齐叶。
- Q-WP3-24：extra 七列只 ADD 再洗；源列不同名但意义一致即可。
- Q-WP3-25：资讯洗进 `title`/`publish_time`/`summary`（summary=全文）；只 ADD `original_url`。ES news 改读另开。
- Q-WP3-26：招投标洗进 `bid_title`/`bid_amount`/`event_date`；**项目编号必洗**，ADD `project_no`。公告类型不映射。ES bid 改读另开。
- Q-WP3-27：投资被投只认 `inv_org_id`；不 ADD 信用代码列。名称/金额/占比洗进现网同义列。
- Q-WP3-28（2026-09-03 改口）：history 按设计稿 ADD `patent_invention_count` / `latest_*`；计数能算则洗。
- Q-WP3-29：库/稿对齐总真源未锁；demo 不当真源。改名跟正式库；设计写丢的补稿；正式库后加列保留并回写设计稿。

## 监管人确认记录

2026-09-02，`human:徐滕强` 确认：

1. 财务统一到万元，由 GDF 基于实际数据判定换算；
2. `chain_dtl` 先核验存续与分层；
3. 核清“迁金融库”的物理库含义；
4. 专利多个企业名称均需匹配，必要时补目标关系字段 / 表；
5. 新任务重出验收表；
6. 先核实 `OPEN-ENT-FLOW-01/04` 是否完成；
7. 港澳台纳入本期，信用代码允许为空，不得伪造；恢复企业主表 `region_id`。
8. 供应链缺已确认真源则不洗、不灌 ES、不上图；`dwd_org_sc_info` 只标潜在可能，不得把 `type` 1/2 或现网 mock 硬造成供应商/客户。
9. 链专利缺 `dwd_org_industry_chain_pat_dtl` 则不洗 `enterprise_chain_patent`，不得用 IPC 硬挂产业链。
10. 国外股东维持进 `enterprise_forg_invest`；并购只贴源不洗。
11. 财务：净利润与利润总额都洗；营业收入与主营收入源两列都有则分开，不合成；正式库只 ADD 缺列。
12. 专利详情按设计稿宽列可 ADD；现网同义列不 DROP；不写不存在的 ipc/cpc 列。
13. extra 缺列只 ADD；源列允许不同名，意义一致即可，禁止猜。
14. 资讯：`summary` 吃全文；不 ADD 与现网同义的设计列；链接只 ADD。
15. 招投标：项目编号必洗（ADD `project_no`）；公告类型无列则空着，不塞 `bid_type`。
16. 投资：被投键=`inv_org_id`；`inv_external_id` 是信用代码，不落。
17. 专利按年汇总按设计稿可 ADD `invention_count` / `latest_*`；计数能算则洗。
18. 库/稿对齐：demo 不当真源；正式库后加列保留并回写设计稿（Q-WP3-29）。

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
- D4 可观测性：✅ 本叶以定义包为主；`lumen-etl-es-py` 仅补 finance 字段写出，未改观测契约。
- D5 CI/CD：✅ 文档定义任务，`cicd: skip`。
- D6 demo 只读 merge：✅ 未改 demo；正式仓仅改 `lumen-etl-es-py` finance 写出，未 merge demo。
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
- 本 handoff 不代表 Wave A/B 已导入成功，也不代表 ES 已重建、图谱已灌绿，也不代表 `OPEN-ENT-FLOW-01/04` / `OPEN-ENT-GRAPH-*` / `OPEN-ENT-GDF-TRIGGER` / `CALLBACK` / `ETL-JOBID` 已完成。
- `09` 未对 48 张源表逐字段复验；`dwd_org_tag_info` / `dwd_forg_subsidiary_info` 未书面改口前对应洗数仍阻塞。
- 协作人：派单包写 `辜少彬`；registry 若写 `辛少彬` 以 registry 为准，本叶不改 collaborator。
- **列契约以 `DATA-ENT-DWD-ALIGN-DOC-L01` 为准**（2026-09-03 修订 `09`/`10`/`13` 升 v3.1）。本叶不打回，保持 `ready_to_sign`。

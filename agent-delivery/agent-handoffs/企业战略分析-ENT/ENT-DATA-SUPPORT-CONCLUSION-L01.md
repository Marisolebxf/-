# ENT-DATA-SUPPORT-CONCLUSION-L01 · 企业域三方承诺表到业务指标数据支撑结论

## 任务认领

| 字段 | 值 |
|---|---|
| claimed_by | `agent:architect-agent` |
| supervised_by | `human:徐滕强` |
| claim_type | `coordinator_dispatch` |

## Ponytail

| 字段 | 值 |
|---|---|
| ponytail | `N/A` |
| 说明 | 定义/分析任务，不写业务代码；未省略 D9、架构合规或证据要求。 |

## 图即契约

| 字段 | 值 |
|---|---|
| diagram_id | `ENT-STORAGE-FLOW`（沿用 `storage/ENT/01-data-flow.md`，本叶未改图） |
| 图 diff | 无；本叶只校验 ODS→DWD→ADS/ES/Nebula 各节点是否具备真实数据支撑。 |
| 会签态 | `approved`（只引用既有数据流图状态，不代表本结论已冻结） |

## 范围与实现

- 依据供应方 4 份 Excel 原始工作簿、2026-08-21 live `gkx` 快照、2026-08-22 `demo_gkxlumenx_ods` 只读探测、GDF v2.1 Mapping、项目 DWD/ADS 和运行代码，形成单一结论文件。
- 逐表核对 53 张企业直接相关 Excel 承诺表：
  - 国内机构 33；
  - 国外机构 8；
  - 产业链 4；
  - 全球专利 7；
  - 国内政策 1。
- 逐项核对王惠报告 60 个唯一 `metric_id`，单列 20 个 UI-hit P0 指标。
- 对外主口径已调整为三类：A 结构+数据完整支持 / B 结构支持暂无可用数据 / C 结构不支持（缺表或缺维度）；业务表与指标分列。
- 六态子码保留为证据，不再当主结论。未将 `join_sparse` 误判为缺表。
- 单列可反馈供应方的缺表（C）、空表（B）、别名、关联键和同 cohort 补数要求。

## 核心结论

1. 业务表：Excel 53 张为 A=43 / B=9 / C=1；加上链位明细后 C=2。
2. 指标：60 个唯一 ID 为 A=10 / B=23 / C=27；20 个 P0 为 A=2 / B=9 / C=9。
3. 国内主档单表计数、区域、深圳、规模可进 A；股东/投资/专利/科技标签表是 A，对应指标因对不上主档是 B。
4. 国外 7 张核心表是 B（空或全删），不是缺表。
5. 链位、市场份额、供应关系、分位基准、科研人员关系属 C。
6. `enterprise_risk_summary` 长/宽表冲突与 demo/formal 实例分裂仍在，不改变三类数据判定。

## 问题清单

- `dwd_research_institute_base_info`：Excel 承诺但缺表。
- `dwd_org_industry_chain_dtl`：GDF/指标依赖但当前基线不可用。
- `dwd_org_tag_info` 与 Excel `dwd_org_tech_tag` 冲突。
- 国外主档、股东、高管、子公司、产品、高校、科研机构无有效业务行。
- `dwd_org_industry_tags` 物理 20,000 行但 `is_deleted=0` 精确计数为 0；产品标签 0 行。
- 企业主键、统一社会信用代码、产业标签 `credit_code` 和项目 `enterprise_code` 尚未形成可验证转换。
- 当前跨表样本 `representativeness=unknown`，不能用于填充率、准确率和结果验收。

## 验证结果

- Excel 承诺全集：219 个去重英文表名；2026-08-21 live `gkx` 匹配 141、缺 78。
- 国内机构 33 表：demo ODS 32 张非空、1 张缺失。
- 国外机构 8 表：7 张无有效业务行；国外年报财务非空但缺主体主档。
- 产业链 4 表：字典/资讯非空；企业标签有效行为 0，企业产品标签 0 行。
- 全球专利 7 表：均非空；企业归属关联稀疏。
- 60 个唯一指标 ID 已全量列项；20 个 P0 已逐项给出源表、DWD/ADS、样本和结论。
- 实库确认企业风险、区域、行业汇总表均 0 行；风险长/宽表冲突经 ORM 源码复核成立。

## 偏离说明

- 未创建任何实施叶，未修改历史企业任务状态，符合用户“先分析生成 Spec/结论”的要求。
- 未修改代码、数据库、GDF 作业或现有 DDL。
- 结论文件标为“预冻结评审版”：事实结论可直接用于反馈上游；C01–C12 的结构/业务裁决仍需人工会签。

## 遗留风险与下一闸门

- Gate A：企业负责人、架构师、数据负责人裁决 12 项结构冲突。
- Gate B：供应方提供同 cohort 数据，至少 30 个国内企业覆盖主档及 5 类关联数据。
- Gate C：逐字段 Mapping 验证。
- Gate D：60 指标/20 P0 真实数据验证。
- Gate E：同一 `batch_id`、同一 DWD 实例下验证 ADS/ES/Nebula 和业务链路。

## 架构合规自检

| 决策 | 结果 | 说明 |
|---|---|---|
| D1 算法只在 Python | ✅ | 仅识别 Python 算法/ADS 重算接口缺口。 |
| D2 前端→Java→Python | ✅ | 业务在线链路不变；GDF 内部调度按已确认例外直接调用 Python `/internal/*`。 |
| D3 NebulaGraph | ✅ | 图谱目标保持 NebulaGraph，未引入 Neo4j。 |
| D4 可观测性 | ✅ | 下一阶段内部作业要求任务状态、`batch_id` 和 trace 证据。 |
| D5 CI/CD | N/A | 文档定义任务，未修改业务仓。 |
| D6 demo 只读 merge | ✅ | 未执行 demo→lumen merge。 |
| D7 共享聚合核心 | ✅ | 未改变 topic/metrics 共享边界。 |
| D8 数据策略 | ✅ | ADS/DWD 先定义、三方源 Mapping 后装载。 |
| D9 数据血缘 | ✅ | 60 指标、来源、DWD、样本和就绪状态均纳入结论。 |
| D10 交互规范 | N/A | 不涉及 UI 交互。 |
| D11 demo/lumen 隔离 | ✅ | 明确指出 demo/formal 混用风险，未允许正式链路回落 demo 服务。 |
| D12 正式链路隔离 | ✅ | 要求正式运行统一使用 lumen 服务和正式 DWD 实例。 |

## CI/CD

- 分支：本地 `dev` 工作区（未提交）
- commit：无；用户本轮未要求 commit/push
- pipeline：`cicd: skip`（定义文档）
- K8s rollout：N/A
- 验证：Excel 结构检查、live 报告交叉核对、demo ODS 与 DWD 只读 SQL 探测、运行 ORM 源码核对

## 成本

| 字段 | 值 |
|---|---|
| actual_tokens | `150000`（会话估算） |
| model_used | `GPT-5.6 Sol` |
| actual_cost | `$0.00`（Cursor bundled，无法取得独立 API 账单） |
| cost_warn | `green` |

## 涉及文件

- `agent-delivery/data/data-design/storage/ENT/ENT-三方数据底层支撑结论-20260822.md`
- `agent-delivery/agent-handoffs/企业战略分析-ENT/ENT-DATA-SUPPORT-CONCLUSION-L01.md`


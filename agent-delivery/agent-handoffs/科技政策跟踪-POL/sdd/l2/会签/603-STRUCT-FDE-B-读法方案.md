# 603-STRUCT-FDE · 波次 B · 读法方案

总单：`POL-L2-PC1-STRUCT-FDE-L01`。监管：`human:淮政玮`。身份：`agent:arch-agent`。日期：2026-11-10。  
产品真源：说明书「#### 603」+ 会签线框。本页只定档与读法，不改正文、不写建表、不写 OpenAPI、不改业务仓。

## 1. 定档

**中。** 监管人 2026-11-10 裁定 **1A 升中**（见 `603-STRUCT-FDE-C-异议闭合.md`）：同页签内「选 → 抽 → 看」闭环与再抽门控、摘要失败保留、两表 seed 边界须按中档交付（线框版本号 `vFDE-603-2026-11-10` + 监管人书面复核），技术路径仍复用已有 `POST /display/v1/policy/parse/clauses`（display → Feign `clauseEnrich` → Python `/internal/policy/clauses/enrich`）与 `GET …/governance/results`，不新建 ADS、不抬新读口。不到「重」（需规叶不增删、IA 不改）。

## 2. 动哪些层

| 层 | 本轮 |
|---|---|
| 展示前端（`lumen-ui-science-pc` `views/policy/governance`） | **动（主）**：标签「政策选择」+ 可搜；同行「结构化抽取」；未结构化不加载摘要；live 适配器灌两表 seed。**本波不验收** `603-qry-1` 页内「结构化政策快速检索」区块（后波；FE DoD / 合规用例不闭合该项） |
| display `PolicyParseController` / `PolicyParseService` | **确认复用** `POST /v1/policy/parse/clauses`（网关后即 `/display/v1/policy/parse/clauses`）；本轮**不改**实现 |
| STRUCT-API 正文 | **后波改文档**：声明治理页复用该资源作单条抽取触发；**不新开**第三条公开资源、不改 OpenAPI 字段表 |
| element `governance/results`（含 `policySummary.hasClauses`） | **不动**实现；选政策 / 抽完后仍靠带 `policyId` 的同资源刷新摘要 |
| Python enrich（`/internal/policy/clauses/enrich`） | **不动** |
| ADS / DWD / Storage / GDF | **不动**（零建表、不重开 C2） |

## 3. 「已结构化」判定

与现行 `hasClauses` / 条款行一致，不另造标志。

| 时机 | 读哪条 |
|---|---|
| 选中政策后 | `GET /display/v1/policy/governance/results?policyId=` → `structure.policySummary`；`hasClauses === true` 才加载业务摘要 |
| 判定口径 | element 现口径：`policy_text_parse.structured_elements` 文本含 `"clauses"`（有条款结构）→ `hasClauses`；无 parse 行 → `false`。前端 `structured: Boolean(live.hasClauses)` 与此对齐 |
| 点「结构化抽取」 | 只调已有 `POST …/parse/clauses`（body `policy_id`），逻辑同中台「抽取条款」转发 enrich；不直连 Python、不打开中台 |
| 抽取成功后 | **再拉**同条 `governance/results?policyId=`；以刷新后的 `hasClauses` 开门，不以条款树 UI 冒充治理摘要。失败 / 进行中：摘要区不假装已结构化 |

禁止：未结构化时用「未结构化」摘要卡冒充已加载；禁止拆解页条款树充当本页摘要。

## 4. 两表非空（Wave0 seed）

| 项 | 裁定 |
|---|---|
| Wave0 前端 seed 灌入 live 适配器 | **可接受**（说明书 603-tax-1 / 603-map-1 已定）。mock 轨已有 `policyPcSeed.structureTaxonomy` / `fieldMappings`；live `fetchGovernanceLive` 现把 `fieldMappings: []` 且缺 `structureTaxonomy`，会签后实现须在适配器合并 seed，打开页签即有行 |
| 接口空数组冒充「无规范」 | **禁止**。两表是规范体系常驻呈现，不是「当前库零命中」；不得因 live 漏字段或回空数组整表空白 |
| 后端是否为本两表新建读口 / ADS | **否**。本轮不扩 `governance/results` 返回两表，不建字典表 |

## 5. 影响清单回应

| 产物 | 何时动 |
|---|---|
| `POL-L2-PC1-STRUCT-ARCH.md` | **会签前改正文一小段**：标「治理页可触发单条抽取，以说明书 2026-11-10 #### 603 为准」；旧「只读呈现、不重跑 / 点名排除本叶触发 parse/clauses」句标已被取代。**不改**时序主读（仍 `governance/results`）、不重开 GDF、不迁中台页。非实现后再 as-built 才补。 |
| `POL-L2-PC1-STRUCT-API.md` | 与 ARCH 同批：声明治理页复用 `POST /display/v1/policy/parse/clauses`；仍不拆第三条资源 |
| STRUCT-DATA / METRIC | 后波清掉「两表可空 / 仅 mock 有数」旧句；无 DDL |
| 合规演示用例 | **会签通过后**按 603-sel-1～603-qry-1 写期望（选 → 抽 → 看；两表有数；未结构化不加载摘要），再重跑 §6.5 |
| FE 治理页 | **会签通过后**才改代码；未会签不得先改前端 |
| 说明书 PC-1 导语 / §11.2 只读旧句 | 后波与 ARCH 对齐时再改（影响清单已点名；本波 B 不改正文） |

## 6. 未闭合 / 停机项

架构停机：**无**（不触新建正式库表、不触铁律豁免；中档成立）。

决策卡（监管人 2026-11-10 已拍 **2A**）：**已选且已结构化时，「结构化抽取」允许再抽**——进行中不可第二遍；失败保留上次成功摘要 + 失败提示；成功再拉 `hasClauses`；仍走同一 `parse/clauses`，不另开资源。

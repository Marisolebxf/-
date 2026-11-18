# KG-GRAPH-POLICY-05 · 政策线与空态裁定（送审）

- 日期：2026-11-17；执行：`agent:data-agent`；监管：`human:徐滕强`；任务负责人：陈芸飞。
- 任务已通过 MCP 认领并开工；最新任务卡交付日期为 11-20，取代旧派单日期。
- 性质：数据事实核查与接口裁定建议，供徐滕强复核、李周接入 D 包；不是接口/页面验收通过记录，不代替真人签收。
- 复核更新（2026-11-18）：徐滕强已确认 §4 中 M12/M13/M14/M16 为 C 档、`MISSING_STABLE_ID`；稳定 ID 补齐后重开补边；M19/M20 分别由 M01/M02 承载、不重复灌。16 行原因码对照已获同意交 API-04 接入。接口与页面尚未联调，任务保持 `integration`，不标完成。
- 本轮只读，不补数、不新建空间、不改点边，不执行模型抽取。数据库连接参数、账号和密码均不进入交付物。

## 1. 结论

1. 合规空间 `demo_gkx_chain` 实测 `policy` **20,000 点**；政策侧 `policy_apply_to`、`policy_relate`、`regulate`、`cite` 均为 **0**。但不能把“政策无必须关系边”说成“政策完全没有边”：政策到产业链/环节的 `apply_to` 历史存量有 **10,957** 条，不能计入 M12–M14。
2. **M12/M13/M14 定 C 档建议，`MISSING_STABLE_ID`**。政策主表并非“没有 related_entities 列”：列实际存在且 20,000 行为有效 JSON，但企业/人才槽全部为空、科研机构槽不存在；19,989 行 org 槽只有名称字符串，不能当科研机构 ID。
3. **M16 定 C 档建议，`MISSING_STABLE_ID`**。`pedigree` 列存在，2 行含政策名称文本，0 行包含已约定的 `上位政策:{policy_id}` token。不能写成“物理字段不存在”。ADS 的 401 条 cite 中，398 条来自 mock 批号、3 条来自演示种子，均不作为合规补边原料。
4. **16 条空态关系均完成当日按 Tag/端点计数，全部为 0**。数据处置建议为 14 条 C、2 条 D（M19/M20 按已签收裁定由 M02/M01 承载，不重复建边）。编号、方向和边型保留。
5. 本轮可直接写入的、已有可靠证据且端点可对齐的政策关系候选为 **0**；未触发 1,000 条 dry-run 或补数。未来有候选时仍须先 dry-run、徐滕强确认，再按批号补写。

## 2. 真源、环境与口径纠偏

关系身份以 [T07 已签收总账](../对接文档/燕大/T07/KG-COMPLY-LOAD-T07-M01-M24入图验收总表-送审稿.md)、[T07 对账口径](../KG-COMPLY-T07-总账对账口径.md) 为准；历史存量处置以 [T06 正式签收](../KG-COMPLY-答复-陈芸飞-T06验收与三项裁定-20261112.md) 为准。没有沿用 11-07 已作废的“M02 为 0”和“weight 为空”说法。

| 旧材料表述 | 本轮核对后的适用口径 |
|---|---|
| M12–M14 为机构/企业/产业 | M12 政策→企业；M13 政策→人才；M14 政策→科研机构。产业链/环节边不在这三条中 |
| M05/M18/M19/M20 均为同源重复 | 签收证据仅支持 M19↔M02、M20↔M01 同源；M05 是本期无供数，M18 是指定端点组合无供数 |
| 政策 2 万点，一条边也没有 | 必须关系空；政策→产业链/环节参照边非空，单列 |
| M16 无字段就用 MISSING_SOURCE_FIELD | 当前有 pedigree，但没有可对齐目标 ID；采用 MISSING_STABLE_ID，详述真实原因 |
| 有 seed cite 就能补图 | 先核 provenance；这三条是展示样例，不能提升为真实引用证据 |

本轮数据环境依据仓库《开发环境清单》的 MySQL 项及合规图库说明定位，分别核对 `gkxlumenx_*` 与 `demo_gkxlumenx_*`，没有跨库合并行数；**不是此前聊天中测试的深势地址**。图库仅有 `demo_gkx_chain` 一个空间。

任务卡写 ADS `59,904 / 21,792 / 19,677`；本轮两个库前缀均无法复现。差异可能涉及环境、时点或筛选，现有证据不足以归因，**不声称数据被删除或任务卡写错**。溯源时能定位到的是 2026-11-17 补建卡备注（任务卡显示当日 16:29 更新）；仓库中未找到载有这组三项旧值的独立文档，也未记录该快照的环境、执行时间或 SQL。因此不能可靠地给出旧快照 SQL。以下是本轮 ADS 精确复数语句，供复核时用相同口径比对，**它们不代表旧快照当时使用的语句**：

```sql
SELECT COUNT(*) FROM gkxlumenx_ads.policy_entity;
SELECT COUNT(*) FROM gkxlumenx_ads.policy_graph_edge;
SELECT COUNT(*) FROM gkxlumenx_ads.policy_graph_node;
SELECT COUNT(*) FROM demo_gkxlumenx_ads.policy_entity;
SELECT COUNT(*) FROM demo_gkxlumenx_ads.policy_graph_edge;
SELECT COUNT(*) FROM demo_gkxlumenx_ads.policy_graph_node;
```

本报告结论限定于本次明确库名、时间和查询；如果旧值来自另一环境，应在该环境重跑后修订。未核验所有可能存在的外部源。

## 3. 源侧对账与字段依据

均为 `COUNT(*)` 精确计数，不使用 information_schema 的 TABLE_ROWS 估计值。DWD 业务读取统一过滤 `is_deleted=0`；三个 ADS 图表没有该列。

| 来源 | 实测行数 | 解释 |
|---|---:|---|
| `gkxlumenx_ads.policy_entity` | 7,517 | 抽取实体行，不等于政策点数 |
| `gkxlumenx_ads.policy_graph_edge` | 3,738 | mock 批 3,726 + seed 批 12 |
| `gkxlumenx_ads.policy_graph_node` | 818 | policy 606 + 其他类型，不等于图库节点数 |
| `demo_gkxlumenx_ads.policy_entity` | 0 | 该 ADS 表为空，不代表 DWD 政策为空 |
| `demo_gkxlumenx_ads.policy_graph_edge` | 12 | 全部 seed 批，其中 cite 3 |
| `demo_gkxlumenx_ads.policy_graph_node` | 20,007 | policy 20,001 + industry 3 + tech 3；不等于图库有效 policy 20,000 |
| `gkxlumenx_dwd.policy_base_info` | 0 | 非 demo 主表为空 |
| `demo_gkxlumenx_dwd.policy_base_info` | 20,000 | active=20,000，distinct policy_id=20,000 |
| 图 `policy` Tag | 20,000 | 当日 MATCH 实数 |

完整列名/类型/注释清单见 [02-schema-count-results.json](KG-GRAPH-POLICY-05/02-schema-count-results.json) 的 `policy_columns`，已覆盖上述 ADS/DWD 表，无需用样本猜 schema。

| 字段/结构 | 全量核验 | 对补边的影响 |
|---|---|---|
| `policy_id` | 20,000 个非重复政策 ID | 政策端可用；规则 `pol:{policy_id}`，仍需 FETCH 检查目标 Tag |
| `related_entities` | 20,000 行合法 JSON；keys 全为 org/talent/service/industry/enterprise | 存在容器不代表有稳定 ID |
| `$.enterprise` / `$.talent` | 非空数组各 0 行 | 无企业/人才端点候选 |
| `$.research` | 所有 JSON 均无该 key | 无科研机构适用对象 |
| `$.org[0]` | 19,989 行 STRING，11 行空 | 名称不等于科研机构 ID，也不等于适用关系 |
| `publish_organization` / `execution_entity` | 非空各 19,989 行；无独立科研机构 ID 列 | 不能据发文名称推断 M14；M10 同样缺稳定发布者 ID |
| `pedigree` | 非空 2 行，均为政策标题文本；约定 ID token 0 行 | 不可直接造 cite；不能按标题猜 ID |
| `elements` | 非空 0 行 | 无补充 ID 证据 |
| `ext1`–`ext5` | 样本分别表现为类型、地区码/地名、关键词 | 仅样本性质，未声称全量排除隐藏 ID；没有已确认的目标 ID 映射契约，不作为本期补边依据 |

来源质量额外记录：DWD 中 `source='demo-mock'` **3,469 行**。因此 20,000 是物理节点/记录数量，不能宣称“20,000 条均为真实政策”；本轮不清理存量，也不扩大为全量真实性验收。

### 3.1 ADS 引用候选为什么不能补

- 非 demo ADS cite=401，分为 `mock_20260623` 398、`seed-240-relation-20261112` 3；demo ADS cite=3，均为后者。
- [政策关联分析 DATA §10](../../../../agent-handoffs/科技政策跟踪-POL/sdd/l2/POL-L2-DS12-SIM-DATA.md) 明确这些是允许的 **ADS 最小演示种子**；[11-12 闭合简报](../../../../agent-handoffs/科技政策跟踪-POL/sdd/简报/2026-11-12-政策关联分析-需规分句闭合.md) 记录了种子批次和读面回退。该授权不是合规图库真实引用关系证据。
- 3 对种子为 `18318861→18318862`、`18363390→18363391`、`18407696→18407697`。前两对端点存在但源侧 pedigree 为空；第三对缺目标政策：DWD 和图库 FETCH 都仅命中六个候选端点中的五个。
- 这三对的 `props={}`，没有逐关系证据。拒绝原因独立存在：种子来源不合规、无引用证据，另有 1 对缺目标 Tag。即使补齐目标节点也不使关系自动可信。
- 处置：401 条不进入合规写入计划；没有删除或更改 ADS 中的演示数据。

## 4. 政策关系逐条裁定建议及重开条件

这里的 C 是数据侧“不支持”的建议档位；接口实际返回 501、页面是否正确展示，仍由 API-04/FE-08 验证，不能据本报告宣称端到端已实现。

| 关系 | 图中实有 | 档位 / reason.code | 需源侧补什么 | 补齐后可开工条件 |
|---|---:|---|---|---|
| M12 `policy_apply_to` policy→enterprise | 0 | C / `MISSING_STABLE_ID` | policy_id、企业 org_id、适用关系证据/来源 | 企业 VID 使用存量 `ent:{org_id}`，不是企业名称或未经映射信用代码；两端 Tag 存在、语义确为适用 |
| M13 `policy_apply_to` policy→person | 0 | C / `MISSING_STABLE_ID` | policy_id、人才 talent_id、适用关系证据/来源 | 对齐既有 `person:` 身份，验证两端存在，不按人名拼 VID |
| M14 `policy_apply_to` policy→research | 0 | C / `MISSING_STABLE_ID` | policy_id、科研机构 institution_id、适用关系证据/来源 | 对齐既有 research Tag 的 `inst:` VID；区分发文机构、服务机构、科研机构 |
| M16 `cite` policy→policy | 0 | C / `MISSING_STABLE_ID` | source_policy_id、cited_policy_id、引用原文证据、provenance | 排除 mock/seed，来源真实可追溯；两端均为 policy Tag；方向保持引用者→被引用者 |
| M11 `policy_relate` policy↔policy | 0 | C / `MISSING_SOURCE_FIELD` | 经确认的双端 policy_id 关联表、关联语义及来源 | 不将有向 cite 或产业关联直接改名；无向投影按既有规范复核 |
| `regulate` 政策侧（非 M） | 0 | C / `MISSING_STABLE_ID` | 被规范对象稳定 ID、类型、规范关系证据 | 现有 600 条为 mock 且端点 `org:名称`；不映射成 M14，不新增 M 编号 |
| M10 `publish` research→policy | 0 | C / `MISSING_STABLE_ID` | 发布者科研机构稳定 ID 与 policy_id 对照及发布证据 | 普通行政机关名称不能当科研机构；保持 research→policy 方向 |

需要新关系映射时，先确认源数据契约和稳定 ID，按 [VID 裁定](../KG-COMPLY-VID-L01-VID前缀实测与裁定.md) 沿用存量编号。不得自动把 `enterprise:名称` 改成 `ent:名称`。首批最多 1,000 条 dry-run，逐条记录证据、目标存在性、重复/跳过原因；徐滕强确认后方可写 `batch=kg100-policy-01`。本轮该批号未使用。

**徐滕强于 2026-11-18 确认**：M12/M13/M14/M16 本期均按 C 档与 `MISSING_STABLE_ID` 返回 501；企业、人才、科研机构及政策引用的稳定 ID 补齐后再重开补边。M19/M20 仍分别由 M02/M01 承载，不重复灌。本段是数据裁定会签，不代表 API 已实现或页面联调通过。

## 5. 16 条空态定档与 reason.code 对照

所有“实有”均为 [06-empty16-results.json](KG-GRAPH-POLICY-05/06-empty16-results.json) 当日执行结果，不用其他端点组合的边数充数。非政策行的源侧原因沿用 T03/T04/T05/T07 已签收证据，**未重新读取其供应库**。

徐滕强已批准 M12/M13/M14/M16 的档位与 `MISSING_STABLE_ID` 原因码，及 M19/M20 的替代关系口径；下表其余新增枚举仍是交给 D 包的建议映射。原因码尚未写入 API；`reason.code` 与旧派单的 `unsupported.code` 取同一值，外层字段以 API 契约为准，不并行发明两套原因。

| 编号 | 边型 | 起点→终点 | 实有 | 档 | reason.code | 依据/页面说明 | 闭环责任 |
|---|---|---|---:|---|---|---|---|
| M03 | cooperate | person→research | 0 | C | `ENDPOINT_TYPE_MISMATCH` | T03：源有 202,795 行，机构端为企业，不满足科研机构端点；不能写“无源” | 宋飞扬核源；徐滕强复核；李周接口 |
| M05 | belong | research→research | 0 | C | `SOURCE_NOT_PROVIDED` | T05/T07：本期无科研机构隶属供数；不是已证实的同源重复 | 数据供方/徐滕强；李周接口 |
| M06 | cite | paper→paper | 0 | C | `SOURCE_NOT_PROVIDED` | T04/T07：无符合论文引用语义的供数 | 韩梦蕊/徐滕强；李周接口 |
| M07 | participate | person→project | 0 | C | `RELATION_SEMANTICS_MISMATCH` | T04：资助成果署名不能证明直接参与项目 | 韩梦蕊/徐滕强；李周接口 |
| M10 | publish | research→policy | 0 | C | `MISSING_STABLE_ID` | 发布名称无科研机构稳定 ID | 陈芸飞/徐滕强；李周接口 |
| M11 | policy_relate | policy↔policy | 0 | C | `MISSING_SOURCE_FIELD` | 无已确认的政策关联 ID 对供数，不拿 cite 替代 | 陈芸飞/徐滕强；李周接口 |
| M12 | policy_apply_to | policy→enterprise | 0 | C | `MISSING_STABLE_ID` | **徐滕强已确认**；需企业稳定 ID 与适用证据 | 陈芸飞/徐滕强；李周接口 |
| M13 | policy_apply_to | policy→person | 0 | C | `MISSING_STABLE_ID` | **徐滕强已确认**；需人才稳定 ID 与适用证据 | 陈芸飞/徐滕强；李周接口 |
| M14 | policy_apply_to | policy→research | 0 | C | `MISSING_STABLE_ID` | **徐滕强已确认**；科研机构稳定 ID，org 名称不能替代 | 陈芸飞/徐滕强；李周接口 |
| M16 | cite | policy→policy | 0 | C | `MISSING_STABLE_ID` | **徐滕强已确认**；pedigree 有标题但无目标 ID；mock/seed 不作引用证据 | 陈芸飞/徐滕强；李周接口 |
| M18 | participates | institution→segment | 0 | C | `SOURCE_NOT_PROVIDED` | 本期无该端点供数；34,769 条机构→机构不是 M18 | 数据供方/徐滕强；李周接口 |
| M19 | research_coop | research→research | 0 | D | `DUPLICATE_RELATION` | T03 已裁本期只建 M02；**徐滕强已确认**由 M02 承载，保留 M19 编号 | 唐绍祖既有裁定；李周接口 |
| M20 | talent_coop | person→person | 0 | D | `DUPLICATE_RELATION` | T03 已裁本期只建 M01；**徐滕强已确认**由 M01 承载，保留 M20 编号 | 唐绍祖既有裁定；李周接口 |
| M21 | service_provide | institution→enterprise | 0 | C | `SOURCE_NOT_PROVIDED` | T05/T07：本期无服务关系供数 | 数据供方/徐滕强；李周接口 |
| M23 | supply | enterprise→enterprise | 0 | C | `SOURCE_NOT_PROVIDED` | T05/T07：本期无供给关系供数，supplies 不混入 | 数据供方/徐滕强；李周接口 |
| M24 | parent_sub | enterprise→enterprise | 0 | C | `SOURCE_NOT_PROVIDED` | T05/T07：本期无母子关系供数 | 数据供方/徐滕强；李周接口 |

名单共 16 行，不含 M22。M22 继续沿用原“有数但形态不可用 501”裁定，本轮不重算其连通片、不改编号。B 档只适用于已有可用供数/接口但特定查询未命中，不能把本表关系能力缺失包装成 `200 + 0`。

## 6. 影响的叶子与消费边界

| 叶子 | 本轮数据结论 | 档位处理 |
|---|---|---|
| 106 政策实体识别构建 | policy 点可读，物理 20,000；含 mock 来源风险，真实性不能仅靠点数证明 | 不因关系空直接降成空 Tag；A 档仍须接口/页面及来源验收，不在本报告冒签 |
| 107 政策实体关系抽取 | 必须关系 M11/M12/M13/M14/M16 当前不可合规补齐 | 对应缺失关系分支建议 C/501，并逐条显示原因；产业参照边可单列展示，不能顶替必须关系 |
| 400–402 等通用查询中选择政策关系 | 缺关系能力；不是任意查询都应 501 | 仅受影响关系分支使用本表；其他实体/关系路径保持原契约，由 API-04 映射 |
| API-04 16 条关系原因码对照 | 徐滕强已同意交李周接入 | 接口实现/契约核对归 API-04；由李周据本表接线，页面联调仍待完成 |
| DS12 240 政策关联读面 | 存在独立 ADS 演示种子授权 | 不追溯改写该页面数据；明确其展示样例不能用于本次合规入图验收 |

建议给用户的文案：M12“暂无可核验的政策适用企业关系，缺企业稳定标识”；M13 换“人才”；M14 换“科研机构”；M16“引用文本尚未关联到可核验政策标识”。M19/M20 显示“本期由 M02/M01 承载，不重复建边”。文案和枚举待 API-04 对齐契约，不代表已部署。

## 7. 证据、复现与限制

- [只读执行器](KG-GRAPH-POLICY-05/readonly_probe.py)：凭据仅从 `POLICY_MYSQL_*` / `POLICY_GRAPH_*` 环境变量获取；输出不含连接参数。MySQL read-only transaction + 20s statement limit；图库 25s 客户端超时，MATCH 必须带 Tag，逐条串行，失败即停。
- `01`：环境内表发现、空间、schema、SHOW STATS（统计缓存，不当实时事实）。
- `02`：完整字段清单、两套 ADS/DWD 精确计数、政策 Tag 与主要边计数。
- `03`：边端点类型、批次、节点分组、字段非空与样本。
- `04`：JSON 全量结构核验、源字段/批次、种子证据；其中一个分组查询别名 `tags` 被解析器拒绝，原始错误保留。
- `05`：将别名改为 `endpoint_tags` 后重跑成功；另核种子六端点与 DWD 来源。
- `06`：16 条关系按 Tag+端点逐条精确计数，全部成功且为 0。

运行方式（先按环境清单配置环境变量，勿将值写入脚本或 Git）：

```text
python readonly_probe.py 02-schema-count-queries.json 02-schema-count-results.json
python readonly_probe.py 06-empty16-queries.json 06-empty16-results.json
```

每个文件包含执行 SQL/nGQL、开始时间、状态、耗时和原始行。复跑应另指定输出文件保存新时点，不覆盖本轮证据。依赖 `pymysql` 与 `nebula3-python`，本轮通过 uv 临时环境运行，未修改项目依赖。

SHOW STATS 的 apply_to/support 各 10,964，与 Tag 锚定有效端点查询各 10,957 相差 7。本轮未全图扫定位该差异，不能武断归因为脏边或统计过期；按有效 policy→chain/segment 口径引用 10,957，并保留两份原始证据。此差异不改变 M12–M14 的端点定义或零计数。

交付范围是证据和裁定建议：未实现 API/页面、不发送飞书、不宣称联调通过。后续由徐滕强复核源计数差异和原因码，李周对接 API-04；未经真人签收不得将本任务标为 done。

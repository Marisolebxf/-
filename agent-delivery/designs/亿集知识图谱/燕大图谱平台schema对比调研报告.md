# 燕大知识图谱平台 Schema 对比调研报告

| 项 | 内容 |
|---|---|
| 任务来源 | 淮政玮（会议待办）：「将燕大知识图谱平台导出的 schema，与当前项目业务需求中定义的图谱 schema 进行逐项核对匹配」 |
| 调研对象 | [http://10.50.183.56:8093/schema](http://10.50.183.56:8093/schema)（亿级科技知识图谱引擎，燕大团队开发） |
| 对比基准 | 总集需规：`gkx-orchestration/agent-delivery/bid-reference/`（科技专题服务算法库、科技信息展示系统和科技专题服务系统、SRS-07 亿级科技知识图谱引擎） |
| 我方代码 | `repos/lumen-algo-py`、`repos/demo-svc-topic-py`、`repos/demo-algo-science`、`repos/demo-algo-ent-analysis`、`repos/lumen-ui-science-pc`、`repos/lumen-ui-topic` |
| 调研日期 | 2026-10-23 |
| 调研方式 | Playwright 深度遍历平台 16 个页面 + 直连平台 20 余个 REST API 抓取全量 Schema/脚本/任务/审核数据；对照我方 3 系统 Nebula 代码与需规 SRS |
| 证据归档 | 本目录 `code/`（46 份抽取脚本、6 份 API 快照、19 张页面截图、Schema 全量导出） |

demo 库按产业、产业节点能命中的条数（2026-10-24 实查，上图前的关联事实）：

| 要素 | 实查 |
|---|---|
| 政策 | [产业检索政策条数](../../qa/test-cases/SDWJSF-KJZTFWSFK/policy-政策分析/产业检索政策条数-20261024.md) |
| 企业 | [产业检索企业条数](../../qa/test-cases/SDWJSF-KJZTFWSFK/enterprise-企业分析/产业检索企业条数-20261024.md) |
| 服务机构 | [产业检索服务机构条数](../../qa/test-cases/SDWJSF-KJZTFWSFK/svc-产业服务分析/产业检索服务机构条数-20261024.md) |

---

## 1. 执行摘要

1. **燕大平台是一个完整的「图谱构建 + 治理 + 查询」一体化引擎**，而非单纯图数据库封装。其 Schema 管理页将「实体/关系定义、属性分类、DDL 自动执行、抽取脚本版本化绑定、构建任务编排、人工审核」串成闭环，这恰是我方 3 个系统都缺失的图谱中台能力。
2. **Schema 层面与我方需规匹配度约 60%**：17 类实体、33 类关系对论文/专利/项目/机构/人才/产业链覆盖充分；**政策（Policy）、服务机构（ServiceOrg）、技术链（TechChain）三类需规核心实体缺失**，需在复用时自行扩展。
3. **最可直接复用的三件套**：① Schema 管理 API（含脚本上传/下载/执行状态）；② 统一溯源属性规约（`source_table/source_record_id/ingest_batch/confidence/match_method/match_evidence`）；③ 9 个「科技专家/人才知识推理构建服务」接口（与需规 SRS-07 逐条对应，2 个已 ready）。
4. **建议合作分工**：底层图谱构建/治理/推理服务复用燕大；上层图谱可视化、图算法指标计算（PageRank/中心性/网络密度）、四大展示模块由我方承担，通过其 `graph-console/query`（nGQL）与 `graph-search/subgraph` 接口对接。

---

## 2. 燕大平台全景

### 2.1 平台定位与规模

| 维度 | 现状 |
|---|---|
| 平台名称 | 亿级科技知识图谱引擎（「亿级科技知识图谱平台」） |
| Schema 版本 | `tech-kg-schema-v1.8`（2026-07-11 发布） |
| 主图空间 | `gkx_local_1`（描述：gkx_dwd_local 本地 DWD 库全量 e2e），另有 dev/techkg 等 18 个空间 |
| 数据规模 | 实体 87.54 万（+17/日）、关系 61.88 万（+6/日） |
| 实体构成 | 论文 74.2 万（80%）、机构基础信息 6.2 万（7%）、科技专家 4.9 万（5%）、技术主题 3.2 万（4%）、其余 5% |
| 关系构成 | 论文署名 35%、专家合著 25%、论文引用 24%、风险事件 4%、其余 12% |
| 底层图库 | NebulaGraph（DDL 为 `CREATE TAG/EDGE` nGQL；vid 为 FIXED_STRING，脚本中有 64 字节 bounded_vid 逻辑） |
| 数据源 | MySQL DWD 库 `gkx_dwd_local`（约 60+ 张 dwd_ 表，国内/海外机构要素库、论文、专利、项目、政策源表） |

### 2.2 功能模块清单（页面级）

| 模块 | 路由 | 能力要点 |
|---|---|---|
| 平台总览 | `/overview` | 资产总览、昨日增量、资产变更流水（精确到源表/执行 ID）、构建任务状态 |
| **Schema 管理** | `/schema` | 标准实体/关系两类卡片；新增、属性编辑、**查看脚本/更换脚本**、DDL 自动执行与状态、拓扑图 |
| 图谱构建 | `/graph-build` | 任务列表（多脚本串行 chain / 单脚本）、调度（单次/cron）、执行历史 |
| 人工审核 | `/manual-review` | 入库决策队列（低置信度数据人工放行）、抽取失败重跑 |
| 配置管理 | `/configurations` | MySQL 数据源（60+ 条）、LLM 配置（GLM 系列，bigmodel 接入）、图空间管理 |
| 综合查询 | `/graph-query` | **nGQL 控制台**（禁止 DDL）+ 图算法作业（PageRank/Louvain/Degree） |
| 实体列表 | `/graph-query/entities` | 按类型分页浏览实体及公共属性 |
| 图谱可视化 | `/graph-query/visualization` | 子图探索（depth/limit/direction 参数），schema 拓扑图 |
| 推理构建服务 | `/expert-direct` 等 9 页 | 与需规 SRS-07 九项一一对应（详见 §5.4） |

### 2.3 核心 API 面板（实测）

```
GET  /api/v1/schema-management/schemas?kind=entity|relation&includeDetails=true&graphSpace=…
GET  /api/v1/schema-management/schemas/topology?graphSpace=…
GET  /api/v1/schema-management/schemas/{id}/script        # 抽取脚本下载
POST /api/v1/schema-management/schemas/entities|relations # multipart 建 Schema
GET  /api/v1/graph-search/spaces | /entity-search/types|entities
GET  /api/v1/graph-search/subgraph/{vid}?depth=&limit=&direction=
POST /api/v1/graph-console/query        # {"space","statement"} 执行 nGQL（禁 DDL）
GET  /api/v1/workflow-system/jobs       # 构建任务
GET  /api/v1/manual-reviews/production/queue
GET  /api/v1/kg-construction/{service}  # 9 个推理服务元数据
GET  /api/v1/mysql-datasources | /llm-config/llm-configs | /graph-spaces
GET  /api/v1/platform/overview?space=…
```

> 平台未暴露公开 OpenAPI（`/docs`、`/openapi.json` 均回落前端页），但总集库中已有我方整理的 76 路径 API 文档：`gkx-orchestration/agent-delivery/designs/亿集知识图谱/亿级科技知识图谱API文档.md`（2026-08-04 核对版），与本轮实测一致。

---

## 3. Schema 逐项核对

### 3.1 燕大实体（17 类 TAG）与我方需规要素映射

需规七大要素（算法库需规 §产业全要素图谱）：**产业、技术、企业、人才、科研机构、政策、服务机构**。

| # | 燕大实体 | 中文 | 属性数 | 核心业务属性（去溯源共性行） | 对应需规要素 | 匹配判定 |
|---|---|---|---|---|---|---|
| 1 | `Person` | 科技专家 | 50 | name_zh/en、person_kind、h_index、citation_nums、paper_nums、research_fields、work_experience_*、education_background_*、is_academician | 人才 | ✅ 完全匹配（字段极全，含简历/头衔/学术指标） |
| 2 | `Organization` | 机构 | 50 | org_type、org_kind、listing_status、registered_capital、stock_code、industry_class、legal_rep、main_products | 企业+科研机构 | ⚠️ 单实体混合企业与科研机构（`dwd_org_base_info`+高校表+研究所表同 Tag），需规要求企业/科研机构分要素建模 |
| 3 | `OrganizationBase` | 机构基础信息 | 17 | organization_id | （辅助） | ✅ 作为论文/专利/项目的机构归属顶点 |
| 4 | `Paper` | 论文 | 32 | doi、publication_year、document_type、is_oa、output_awards | 科技成果（展示系统） | ✅ |
| 5 | `Patent` | 专利 | 48 | 专利号/申请号/授权号、main_ipcr/main_cpc、patent_value、simple_family_number | 科技成果 | ✅（IPCR/CPC 分类、专利价值评估齐全） |
| 6 | `PatentFamily` | 专利同族 | 18 | family_number | — | ✅ 同族布局分析可用 |
| 7 | `Project` | 项目 | 46 | project_number、project_level、funded_amount、discipline_code、approval_year、9 类产出计数 | 科技成果/项目 | ✅ |
| 8 | `Report` | 科技成果 | 24 | report_category、report_type、abstract、keywords | 科技成果 | ✅ 软科学成果展示可对接 |
| 9 | `Journal` | 期刊 | 33 | issn、impact_factor、jcr_zone、is_sci、top、annual_publication | — | ✅ 期刊分级指标现成 |
| 10 | `Keyword` | 技术主题 | 18 | keyword | 技术 | ⚠️ 仅关键词级，无层级/上下游，**技术链缺失** |
| 11 | `IndustryChain` | 产业链 | 17 | chain_code、chain_name | 产业 | ✅ |
| 12 | `IndustryNode` | 产业链节点 | 23 | node_id、node_type、level、node_seq、node_imp_level、node_stage、node_path | 产业 | ✅ 节点层级/重要性/阶段齐全 |
| 13 | `Product` | 产品 | 19 | category、description | 产业（企业产品） | ✅ |
| 14 | `News` | 新闻资讯 | 21 | title、content、release_date、original_url | 产业动态/资讯指标 | ✅ |
| 15 | `Event` | 事件 | 26 | event_type、title、case_no、case_cause、occur_date、amount | 风险事件（指标展示-黑名单） | ✅ 覆盖 15 类工商/风险/招投标事件表 |
| 16 | `ScholarOrganization` | 学者任职机构 | 18 | name_cn/en、org_kind | 人才（辅助） | ✅ 任职边端点桩节点，机构库落地后同名消歧合并 |
| 17 | `DataSource` | 数据来源 | 18 | tier(DWD)、library、table_cn_name | — | ✅ **把数据源表作为图内实体**，可视化中可溯源到表，设计可取 |
| — | ❌ Policy | 政策 | — | — | **政策** | ❌ **缺失**。会议纪要明确「政策类关联关系不足待核对，本次仅 1 份政策文档」 |
| — | ❌ TechChain | 技术链 | — | — | **技术** | ❌ 缺失，需规技术链深度分析模型无承载实体 |
| — | ❌ ServiceOrg | 服务机构 | — | — | **服务机构** | ❌ 缺失（我方 `entan/svcgraph` 已有 institution+service 建模） |

### 3.2 燕大关系（33 类 EDGE）核对

**事实型关系（relationCategory=fact）31 类 + 推理边 2 类（ALUMNI、COLLEAGUE，已写入图库但未注册进 Schema 管理页）：**

| 分组 | 关系（起点→终点） | 关键属性 | 需规对应 |
|---|---|---|---|
| 人才-机构 | AFFILIATED_WITH 任职、STUDIED_AT 就读、EXECUTIVE_OF 高管、LEGAL_REP_OF 法定代表 | work_experience_date/position/department；degree、education_date；position | 人才画像-关联画像 ✅ |
| 企业股权控制 | INVESTS_IN、SHAREHOLDER_OF、ACTUAL_CONTROLLER_OF、BENEFICIAL_OWNER_OF、SUBSIDIARY_OF、ACQUIRES | investment_ratio、ownership_percentage、direct/total_pct | 企业关系图谱 ✅（属性比我方 `parent_sub(weight,props)` 细一个量级） |
| 论文网络 | AUTHORED_BY(author_order,is_corresponding,citations)、CITES(sequence)、PUBLISHED_IN、HAS_KEYWORD、COAUTHOR_WITH(co_paper_count,relation_time)、REFERENCED_BY | — | 学术合作网络/中心性指标 ✅ |
| 专利网络 | INVENTED_BY、APPLIED_BY、OWNED_BY、MEMBER_OF_FAMILY | sequence、role、is_current、subject_type、resolution_status | 专利-发明人-机构图谱 ✅ |
| 项目网络 | FUNDED_BY(amount,category)、LEADS、HAS_PARTICIPANT、HAS_OUTPUT(output_type)、OUTPUT_OF | — | 项目-机构-学者关系 ✅ |
| 产业链 | HAS_NODE、CHILD_OF、DOWNSTREAM_OF、BELONGS_TO_NODE(chain_score)、COVERS_CHAIN | chain_score | 产业链全景/上下游 ✅ |
| 资讯/风险 | HAS_NEWS、INVOLVED_IN(role) | role | 风险事件监测 ✅ |
| **推理边** | ALUMNI（shared_institutions、dimensions_json、paper_count、patent_count）、COLLEAGUE（organization、department、effective_period、overlap_months、confidence） | — | 需规 9 接口中的校友/同事关系，燕大已落图 ✅ |
| ❌ 缺失 | 政策-主体（扶持/适用/监管）、服务机构-产业/企业/政府、技术链上下游、人才-政策 | — | 算法库政策/服务机构/技术链深度分析模型无承载 |

### 3.3 属性设计规约（燕大全量 Schema 的公共约定）

每个 TAG/EDGE 均携带 9~13 个**溯源与治理属性**，是我方现有建模完全没有的：

```
source_table        来源表（NOT NULL，必填）
source_record_id    源记录主键/稳定键
ingest_batch        摄取批次（se-{sourceId前8位}）
ingest_time         摄取时间
source_system       来源系统（恒为 gkx）
source_url          原文链接（多候选链取值）
source_update_time  源更新时间
confidence          动态置信度（见下）
match_method        端点匹配方式（source_primary_key / org_name_md5 / …）
match_evidence      匹配证据说明（审计可读）
vid / organization_base / extra_json（超长 JSON 降级为 sha256 摘要）
```

配套算法（摘自 `code/scripts_entity/entity_Person__person_entity_step.py`）：

- **动态置信度**：`0.40(DWD 溯源) + 0.20(稳定机构ID) + 0.10(external_id/credit_no) + 0.20(展示身份属性) + 0.10(地域/时间)`，封顶 1.0 —— 低置信度自动进人工审核队列；
- **bounded_vid**：vid 超 64 字节截断并追加 `_md5` 后缀，规避 Nebula FIXED_STRING 溢出；
- **person_vid**：`person_md5(kind|org_id|name|birth_date|country)`，各分量 NFKC+casefold 归一化，天然实体消歧；
- **merge_protect**：机构域写前读旧值做属性合并保护，防覆盖；
- **虚拟源拦截**：`data_source/source_system` 含 mock/stub/test 标记的行不建点。

---

## 4. 与我方系统 Schema 对比

### 4.1 我方图谱功能分布

| 系统/模块 | 位置 | 图谱能力 |
|---|---|---|
| 科技专题服务算法库（lumen-algo-py） | `lumen_common/algorithms/chain/graph_project.py`；`vendor/entan-py/entan/` | 产业链图谱灌链（DWD→Nebula `demo_gkx_chain`）、服务机构图谱写算子、向量索引 rebuild |
| 算法 demo（demo-algo-science / demo-algo-ent-analysis） | `chainan/graph/`、`entan/graph/` | 同款 Tag/Edge DDL、nebula_loader/nebula_query、增量更新 |
| 科技专题服务系统（demo-svc-topic-py） | `gkx_common/nebula_graph.py`、`gkx_search_service/views/enterprise_graph.py` | 企业关系子图查询/节点拓展 API（首屏 1 跳 + 点击 expand） |
| 科技信息展示系统（lumen-ui-science-pc） | `src/lib/graph/`（17 个模块）、`KnowledgeGraphCanvas.vue`、`GraphChart.vue` | 图谱可视化：路径回放/路径对比、关键词过滤、实体排序、手动录入、视图状态 |
| 科技专题服务前端（lumen-ui-topic） | `EnterpriseRelationGraph.vue` | 企业关系图组件 |

### 4.2 Schema 逐项对比

| 对比项 | 燕大 | 我方（chain/svcgraph） | 差距评估 |
|---|---|---|---|
| 实体 Tag | 17 类富模型，每类 17~50 业务属性 | chain: 4 类（chain/segment/enterprise/institution）；svcgraph: 5 类（enterprise/industry/research/talent/service），业务属性仅 name/type/weight，**其余塞 `props` JSON 字符串** | ❌ 我方属性弱：无法在图库层做属性索引/过滤（nebula `props string` 不可 WHERE）；燕大模型可直接升级我方查询能力 |
| 关系 Edge | 33 类，边属性带金额/比例/次序/时段 | chain: 4 类（belongs_to/participates/supplies/depends_on）；svcgraph: 7 类 | ⚠️ 我方语义粗（如 parent_sub 无持股比例），但已覆盖「供需/上下游」语义，燕大无 supplies 类边 |
| VID 策略 | md5 归一化 + bounded 64B + 消歧键 | `ent:{org_id}` / `ind:{产业名}` 等前缀拼接，**中文名直接进 vid**（`ind:软件`） | ⚠️ 我方产业名 vid 有长度/规范化风险，建议引入燕大 md5 方案 |
| 溯源 | 10 字段标准规约 + match_evidence | 无 | ❌ 全缺。需规「数据溯源与详情展示」（人才画像 §关联画像）要求可溯源，燕大规约可照抄 |
| 置信度 | 动态评分 + 低置信人工审核 | 无 | ❌ 全缺。需规「知识图谱可信度量化评估，评估过关才入库」正是此机制 |
| Schema 元数据 | 平台化管理（版本/DDL 状态/脚本绑定/拓扑 API） | 代码硬编码 TAG_DDL/EDGE_DDL 字典 | ❌ 我方无 Schema 管理界面；改 schema 需发版 |
| 图空间治理 | 多空间 + 绑定 + demo/prod 分离（同我方 demo_ 前缀守卫思路一致） | `demo_gkx_chain` + NonDemoNebulaSpaceError 守卫 | ✅ 双方理念一致，可互认 |
| 政策要素 | ❌ 无 | 我方 demo-algo-ent-analysis `polan/` 有政策图谱 | ✅ **我方占优**，可作为互补输出 |
| 服务机构要素 | ❌ 无 | 我方 `entan/svcgraph*` 九类写算子（SVC_RE_*） | ✅ **我方占优** |

### 4.3 功能差异（平台级）

| 能力 | 燕大 | 我方现状 | 结论 |
|---|---|---|---|
| Schema 可视化管理 + 脚本版本绑定 | ✅ 完整 | ❌ 无 | **直接复用或嵌入燕大页面** |
| 构建任务编排（串行链/调度/失败重试） | ✅ workflow-system | ❌ 手工跑脚本 | 复用燕大 |
| 人工审核闭环（MR 工单） | ✅ | ❌ 无 | 复用燕大；需规「删除需审批」可基于此扩展 |
| nGQL 查询控制台（禁 DDL） | ✅ | ❌ 仅后端 API | 复用；注意其「支持查询及写入、DDL 禁止」的权限面设计 |
| 图算法作业（PageRank/Louvain/Degree） | ✅ 内置 3 种 | ✅ 我方指标库更全（M_SVC_GRAPH_CENTRALITY/DENSITY/INFLUENCE：度/接近/中介中心性、网络密度、影响力） | **我方占优**，需规「算法展示」要求 6+ 种算法，燕大 3 种不够，双方互补 |
| 图谱可视化前端 | ⚠️ 基础力导向+侧栏 | ✅ 强（路径回放/对比、多维过滤、手动录入） | **我方占优** |
| 9 个推理构建服务 | ✅ 2 ready + 7 scaffold（与 SRS-07 一一对应） | ❌ 无 | 短期直接调燕大接口，中期我方自研对齐 |
| 子图查询 API | ✅ `subgraph/{vid}?depth&limit&direction` | ✅ 我方 `graph/subgraph`（org_id, steps 1~3）+ expand | 接口形状接近，对接成本低，建议统一参数风格 |

---

## 5. 可借鉴项清单（按系统 → 模块 → 功能）

### 5.1 科技专题服务算法库（lumen-algo-py）——收益最大

| # | 借鉴点 | 燕大参照 | 落地方式 |
|---|---|---|---|
| A1 | **图谱属性富化**：把 `props string` JSON 拆为图库原生列 | Organization 50 属性、Patent 48 属性、INVESTS_IN 持股比例等 | 在 `graph_project.py` TAG_DDL/EDGE_DDL v5 终裁时按燕大口径扩列；企业深度分析模型（股权穿透、实控人）直接依赖这些列 |
| A2 | **溯源属性规约 10 字段** | 全部 46 份脚本统一实现 | 抽取 `lumen_common/graph/provenance.py` 工具函数，灌链时统一注入 |
| A3 | **动态置信度评分** | `entity_confidence()`（0.3~1.0 五档加权） | 移植到灌链算子，低置信边落 `pending` 而非直接上图 |
| A4 | **VID 规范**：NFKC+casefold 归一 + md5 + bounded 64B | `person_vid()`/`bounded_vid()`/`md5_hex()` | 修复 `ind:{中文产业名}` 类 vid 隐患 |
| A5 | 人才关系边设计 | COAUTHOR_WITH(co_paper_count, relation_time)、ALUMNI、COLLEAGUE（overlap_months+confidence） | 人才深度分析模型的关系层直接对齐，接口互通 |
| A6 | 产业链节点属性 | IndustryNode.level/node_seq/node_imp_level/node_stage/node_path + BELONGS_TO_NODE.chain_score | 我方 chain.segment 增补 stage/level/重要性属性，支撑「产业链关键环节识别」「瓶颈堵点识别」模型 |

### 5.2 科技专题服务系统（demo-svc-topic-py）

| # | 借鉴点 | 落地方式 |
|---|---|---|
| B1 | **子图 API 参数对齐**（depth/limit/direction both） | `enterprise_graph.py` 的 subgraph/expand 增加 direction 与 depth≥3 支持，前端图谱组件可直接切换燕大数据源 |
| B2 | **DataSource 实体入图** | 企业图谱首屏挂「数据来源」节点，点击溯源到 dwd 表元数据（需规「数据资源-应用视窗」可复用） |
| B3 | 风险事件边 `INVOLVED_IN(role)` + Event 实体 | 企业风险标签页直接消费，替代当前 Mock |

### 5.3 科技信息展示系统（lumen-ui-science-pc / lumen-ui-topic）

| # | 借鉴点 | 落地方式 |
|---|---|---|
| C1 | Schema 拓扑 API（`schemas/topology`）驱动图例 | 我方 KnowledgeGraphCanvas 的实体/边图例与颜色由 schema 元数据动态生成，而非硬编码 |
| C2 | 实体类型统计接口（`entity-search/types` 返回 count+label） | 「科技知识图谱-分析展示」模块的资产构成卡片 |
| C3 | 资产变更流水（`platform/overview` 的 assetChangeRows，含源表/任务 ID/时间） | 「指标展示-异常数据监测」的数据新鲜度提示 |

### 5.4 跨系统：9 个推理构建服务对账（需规 SRS-07 ↔ 燕大）

| 需规功能（excel_row） | 燕大页面/API | 燕大状态 | 我方对策 |
|---|---|---|---|
| 科技专家/人才直接关系 | `/expert-direct` → `kg-construction/expert-direct-relations` | scaffold | 依赖 Person 直接边（AFFILIATED_WITH 等），我方可基于同一图库自研 |
| 科技单节点间接关系 | `/node-indirect` | scaffold | 需路径分析——用我方算法库路径能力补 |
| 科技两点合作成果 | `/two-point-achievement` → `expert-cooperation-achievements` | **ready** | 直接调用 |
| 科技专家同事关系 | `/expert-colleague` → COLLEAGUE 边已落图 | **ready（边）+scaffold（API）** | 直接读 COLLEAGUE 边 |
| 科技专家校友关系 | `/expert-alumni` → `expert-alumni-relations` | **ready** | 直接调用 |
| 科技专家论文合作关系 | `/paper-cooperation` | scaffold | COAUTHOR_WITH 现成，差 API 封装 |
| 重点关注科技企业关系 | `/enterprise-relation` | scaffold | 依赖企业股权 6 边，已齐 |
| 科技产业链点TOP-N事件关系 | `/industry-chain-event` | scaffold | Event+INVOLVED_IN+影响力算法（我方 M_SVC_GRAPH_INFLUENCE 可补） |
| 科技产业链全景图 | `/industry-chain-panorama` → `industry-chain-panorama` | scaffold | 我方 `chain/panorama.py` 已有全景能力，**双方对齐口径后由我方主导** |

---

## 6. Schema 管理页面深度解读（重点任务项）

`/schema` 页面结构与交互（截图见 `code/screenshots/01_schema_full.png`）：

1. **双 Tab**：`标准实体`（17 卡片）/ `关系`（33 卡片）；卡片显示中文 label、属性计数（如 Organization `+50`）、DDL 执行状态、脚本运行状态（lastRunStatus=ok / stale 标记）。
2. **每张卡片操作**：`查看脚本`（弹窗展示绑定的 Python 抽取脚本，可下载）、`更换脚本`（multipart 上传新版本，自动记录 uploadedBy/uploadedAt/sha256/etag）、`···`（编辑属性/删除/版本历史）。
3. **属性编辑器**：每条属性含 `name/dataType/required/rule/category/locked`，category 分 `required（主键与审计必填）/ core（业务核心）/ provenance（溯源）/ dynamic（置信度）`——**属性分类学**是我方建模文档可直接借鉴的规范。
4. **DDL 自动化**：保存 Schema 即生成 `CREATE TAG/EDGE IF NOT EXISTS …` + 索引（如 `idx_scholarorganization_name ON ScholarOrganization(name(64))`）并执行，回填 ddlStatus/ddlError/ddlExecutedAt。
5. **脚本约定**：单文件自包含（由 `build_portable_steps.py` 从原模块生成），入口统一 `@step("name") def emit(payload)`，输入 `payload["rows"]`（平台喂数管道注入 MySQL 分页行），输出 `{"entities"|"edges": [...], "failures": [...], "stats": {...}}`；行级失败不中断，进 failures 列表可人工重跑。
6. **构建编排**：Schema 脚本不直接调度，而是在 `/graph-build` 组成 chain 任务（实测存在「实体链」1 条 +「关系链 A/B」2 条，共 27 个 Schema 串行），支持单次/cron、执行历史与异常态。

> 借鉴要点：**「Schema 定义 = 结构 DDL + 抽取脚本 + 运行状态」三位一体的元数据模型**，以及「行级失败白盒化（failures 数组）+ 人工审核闭环」，是我方图谱数据工程目前完全空白、且需规（可信度评估入库、删除审批）明确要求的能力。

---

## 7. 结论与建议

### 7.1 逐项核对结论（回应任务原文）

- **已匹配可复用**：人才（Person 50 属性）、企业/机构（Organization 50 属性 + 6 条股权边）、论文/专利/项目/期刊/产业链/事件/资讯/产品/成果共 15 类实体与 31 类关系，与需规「产业全要素图谱 + 科技专家/人才知识推理构建服务 + 展示系统知识图谱模块」的主体重合度高，**可直接作为我方三个系统的统一图底座**。
- **部分匹配需适配**：Organization 混装企业/高校/研究所 → 我方按需规拆 `enterprise / research_institution` 两视图（可用 org_type 派生 Tag 或视图层分流）；Keyword 无层级 → 技术链需我方补充建模。
- **缺失需扩展**：**政策实体及扶持/适用/监管关系**（燕大明确未做，我方 polan 已有底子，可反向输出）；**服务机构实体及其 8 类关系**（我方 svcgraph 已实现）；**技术链实体**（双方都缺，建议共商口径）。

### 7.2 行动建议（按优先级）

1. **本周可做**：向燕大申请 gkx_local_1 只读账号与 `graph-console/query` 白名单；我方 `enterprise_graph.py` 增加燕大数据源适配器（子图 API 参数已对齐 80%）。
2. **两个迭代内**：lumen-algo-py 引入溯源/置信度规约（§3.3）与 VID 规范（A4）；chain TAG_DDL v5 终裁时采纳 IndustryNode 四属性 + chain_score。
3. **联合设计**：政策与服务机构两要素由我方出 Schema 草案（沿用燕大属性分类学与溯源规约），提交燕大平台注册，实现「燕大引擎跑我方模型」。
4. **需规对账会**：携带本报告 §5.4 九接口对账表与燕大确认 ready/scaffold 边界，明确哪些由我方自研（间接关系、TOP-N 事件、全景图）。

### 7.3 风险提示

- 燕大平台自述「仅适配中等复杂度场景，数据溯源颗粒度低于 GDF 平台」；其 Schema 空间存在大量测试空间（60+ 数据源含大量脏配置），接入时须锁定 `gkx_local_1` 并确认生产空间规划。
- `graph-console/query` 当前「支持查询及数据写入」，若前端直连存在越权写风险，我方接入层必须收敛为只读账号。
- 燕大 9 接口 7 个仍为 scaffold，排期依赖其团队，需规交付前应以我方算法库能力兜底。

---

## 附录：证据清单（本目录 `code/`）

| 目录 | 内容 |
|---|---|
| `api_snapshots/yanda_schema_full_export.json` | 17 实体 + 33 关系全量定义（含每条属性、DDL、来源表、脚本元数据） |
| `api_snapshots/yanda_schema_export.md` | 人读版 Schema 导出表 |
| `api_snapshots/workflow_jobs.json` | 3 条构建链任务定义（27 个 Schema 串行编排） |
| `scripts_entity/`（17 份）· `scripts_relation/`（29 份） | 「查看脚本」抓取的全部抽取脚本（溯源/置信度/VID 算法在此） |
| `screenshots/`（19 张） | 平台总览、Schema 管理、构建、人工审核、配置、查询、可视化、9 个推理页截图 |

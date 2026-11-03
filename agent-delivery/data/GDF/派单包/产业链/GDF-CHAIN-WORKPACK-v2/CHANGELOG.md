# CHANGELOG — GDF-CHAIN-WORKPACK（v2 目录）

> v2 目录自 v2.0 起新记；v1.x 历史见 `../GDF-CHAIN-WORKPACK-v1/CHANGELOG.md`。

## v2.2.7 — 2026-11-02

- **入向量库由 GDF 配脚本**：问 9 指向 `script/README.md`。GDF 在平台上配置 `industry_embed.py` 的 `rebuild`，直接写库 `gkxlumen` 的 `gkxlumen_industry_anchor`。不调用 `POST /internal/industry/embed/rebuild`。副本里的 `DB_NAME=default` 和 demo 读库闸门，配作业前改掉。上图仍只走调度触发和轮询。
- **问 12 的点数改为锚点条数**：入向量库看 `industry_chain` 53 行、`industry_chain_node` 1,220 行里有名称的行是否都写入集合。不再用图上 `chain` / `segment` 顶点数和 `vertices_written`。

## v2.2.6 — 2026-11-02

- **正式集合已建**：Milvus 库 `gkxlumen` 中创建 `gkxlumen_industry_anchor` 并 load。768 维、COSINE、主键 `vid`、动态字段打开，0 条。库 `default` 的同名集合未动。

## v2.2.5 — 2026-11-02

- **上图改为调度对接**：链树 DWD `success` 后，GDF 调用燕大知识图谱引擎的入图调度任务触发接口，引擎立刻返回已收下。GDF 轮询任务状态直到成功或失败。不调用 `POST /internal/v1/chain/graph/project`，不在 GDF 节点跑入图脚本。写入 `23` 问 8、问 10 和 `12` §5.1、§5.4。

## v2.2.4 — 2026-11-02

- **向量隔离改为 Milvus 数据库**：正式库 `gkxlumen`（现网已建，当前 0 个集合）。demo 仍用库 `default`。集合名两边都是 `gkxlumen_industry_anchor`。v2.2.2 的异名集合 `gkx_chain_industry_anchor` 作废。`lumen-algo-py` 的 `dbName` 仍是 `default`，正式 rebuild 改库之前禁止执行。

## v2.2.3 — 2026-11-02

- **23 按现网核对结果改答复**：分表只看 `parent_name`；`chain_tier` 只在链表写 `L0`/`L1`；`sort_no` 取码末两位；`future_industry_flag` 写 0，不 JOIN 簇表。正式库关系表当前 0 行，demo 为 913 行。
- **正式向量集合三处共用**：`gkx_chain_industry_anchor` 由产业链 `12` 创建。政策 C1、技术节点产业映射、子学科产业关联都用这一集合，不另建。政策脚本默认前缀改为 `gkx_chain_industry_`。写入 `23` 问 9 下表。

## v2.2.2 — 2026-11-02

- **12 号向量集合与算法中台 demo 隔离**：正式集合 `gkx_chain_industry_anchor`（前缀 `gkx_chain_industry_`）。demo 中台按钮仍写 `gkxlumen_industry_anchor`（前缀 `gkxlumen_industry_`，对应 `demo_gkx_chain`）。同一台 Milvus，集合名分开。正式批不读、不写 demo 集合。答复记入 `23` 问 9 下表。

## v2.2.1 — 2026-11-02（二次确认）

- **12 号契约补全**（round2 问 8~13 全部答复）：图空间正式定名 **`gkx_chain`**（徐滕强拍板，全文替换占位名）；新增 §5 接口契约（上图/rebuild 路径、请求响应字段、`index_version`=yyyyMMddHHmmss、点数稳定四连判 + 两条已知边界、GDF 编排落点）；章节顺延（验收→6、关系→7）。
- **23 号答复同步更新**：问 8~13 从「待架构师确认」改「已答复」；开工判定表「12 后加工」从待 round2 改**可起草**。
- 09 OPEN-CHAIN-FLOW-02 关闭。
- 正式图谱由 GDF 专门代码读写；我方算法侧 demo 闸门（assert_demo_nebula_space 等）不进 GDF 契约，其正式化改造另行派单（algo 域）。
- 同日补齐 12 文首、第 1 节警告和 23 遗留表残留：问 8~13 五项已定，正式空间 `gkx_chain`（lumen）。淮政玮确认。
- `script/` 放入 `lumen-algo-py` 上图与 rebuild 原文（`graph_project.py`、`industry_embed.py` 及两条路由），供 GDF 对照 §5。不在 GDF 节点执行。

## v2.3.2 — 2026-11-03（问 9~10 脚本参数化真交付）

- **`script/industry_embed.py`**：全环境变量化；去掉 `lumen_common`/`polan`；`MILVUS_DB_NAME` 未配或 `default` 拒绝写入；词表默认读 `gkxlumenx_dwd`；`python industry_embed.py` 自检通过。
- **`script/README.md`**：参数表（必配/可选）重写；GDF 配作业只设环境变量、不改代码。
- 误建 `CHAIN-EMBED-PARAM-L01` 已撤销；问 9~10 以本版脚本为准。

## v2.3.1 — 2026-11-03（round2 问 4 与问 5~10 拍板落稿）

- **问 4 `stage_code`（徐滕强）**：维持三等分派生（末两位 1-4/5-8/9+ → upstream/midstream/downstream）；排序含义登记 🟡 待供应方确认，不符则重算刷新。09§3.0 与 OPEN-CHAIN-MAP-01 同步。
- **问 5~8（徐滕强）**：原子接口方案与 definition_id **转我方架构师确认**（数据侧不代答引擎能力），确认结果随 round3 给出；幂等基线语义先行书面承诺。
- **问 9~10（徐滕强，路线 A）**：承诺脚本全参数化 + 依赖内联（**v2.3.2 已落地脚本**；不另派 algo）。
- 23 号答复 §8 问 4/5~8/9~10 全部按拍板更新。11 问至此**全部闭环**。

## v2.3 — 2026-11-03

- **round2 答复落稿**（`23`§8，11 问）：①链树层级修正——`node.chain_id` 改填所属 L1 链（沿父级向上，命中率 100% 验收）、`parent_node_id` 补直接父级（L2 165 行 NULL）、边表改真父子 **1,055 条** `parent_child`（废弃兄弟相邻 913 条方案，书面更正）；②`stage_code` 定 NULL（同级序号≠上中下游）；③原子入图接口接受，引擎侧改造 round3 给承诺；④脚本全参数化（DB_NAME/collection/表名/闸门等），交付即运行；⑤`_SPACE_OK` 口径澄清（demo 域实现不进 GDF DAG）。
- GDF 附注三处不一致修正：02 tags 行解析写法、CHANGELOG v2.2 条 flag 表述、12§5.1 JSON 段定位。
- 09 头注升 v2.3；OPEN-CHAIN-MAP-01 更新（stage_code=NULL）。12/后加工暂不配置（等原子接口 + definition_id）。

## v2.2 — 2026-11-02

- **round1 核对签收与 20 题答复**：新增 `23-核对签收与答复.md`（有问必答，对照 GDF round1 提问清单编号）。
- **09 链树映射重写（§3.1~3.4）**：真源列语义实测修正——`industry_code` 主键（`industry_link_code` 实为父级码，废止主键用法）、`industry_name` 名称（`industry_link_name` 实为父名）、`parent_name` 为层级序号 0..7（作分层判定源）、`level` 列全 0 禁用；分层改 L0+L1 链表（53 行）/ L2~L7 节点表（1,220 行）；`parent_node_id` 填直接父级、不跳级；`sort_no`=同链码序、`stage_code` 三等分采用（**v2.3 已改 NULL**）；`future_industry_flag` 写 0、不 JOIN 簇表（**v2.3 勘误：本条原记「按簇表派生」与 23 问 17 定稿不符**）；挂接列按单引号列表字面量解析 + 脏值治理规则。
- **10/ DDL 真源钉死**：新增 `dwd-chain.md` 复制件（库名全局改 `gkxlumenx_dwd`）为四表唯一结构真源；删除旧 `链树四表.md`；v5 文档作废；README 重写真源声明。
- **12 修订**：图空间名/上图与 rebuild 契约/点数稳定判定标注待架构师确认（round2 补）；`demo_gkx_chain` 为占位禁施工；跳过写 `skip` 已定。
- **环境红线入包（2026-11-02 架构师新规）**：GDF 只读真源 `gkx` + `gkxlumenx_*` 正式库，禁读 demo；码表一次性修数由我方执行；正式库数据旧/缺以真源为准施工、业务问题咨询我方。
- **数据侧已执行**：正式库链树两表清空重灌（53/1,220）；簇表/学科映射表同步就位。ODS tags 表仅约 1,000 行为同步作业缺陷，补灌后重测命中率（问 7 待 round2 补充答复）。
- 02 / 03 / 04 / 06 / 11 未改动。

## v2.1 — 2026-10-31

- **新增 `12-DWD后加工-产业链入向量库.md`**（架构师要求：产业入向量库入派单包；政策的抽产业依赖产业入库）。
- 口径全部引用既有决策，无新拍板：`storage/CHAIN/01-data-flow.md` §9 产业锚点向量面 + `CROSS-VEC-长任务总控` §0 #2/#3/#16/#17/#19。
- 要点：链表洗完（B1）+ 上图 VID 稳定后**整库一次 rebuild**（我方算法侧自动执行，GDF 只管顺序与回执）；每日批串行 Wave B → 上图 → rebuild → Job A；回执须带 `industry_index_version`（跳过诚实写 `skip`）。
- 明确下游依赖关系：政策包 `12`（POLICY-C1 抽产业）检索的锚点集合即本环节产物；锚点未就绪时政策 C1 `no_match` 为设计内空态。
- 09 / 02 / 06 **未改动**（Mapping 真源与贴源清单不变）。

## v2.0 — 2026-10-20

- 基线对齐 **10-19 三方承诺清单**：四表全部在册、行数不变（链树 1,296 / tags 2,197,216 估 / 产品 73,313 / 资讯 94,997）。
- live 实证：`dwd_industry_chain_info` 真实含 `parent_name` 列（text）→ 09 §3.1/§3.2 加"不映射、JOIN 派生"注记；纪要所列 `t_id`/`id`/`code_company_count` **live 无此列，不作源**（Excel 说明领先于库，与 ENT v4 同一澄清）。
- 与 ENT v4.0 的拆分对称声明继续有效（按目标表拆责任；CHAIN 09 §1.3 ↔ ENT 02/09 §1.6）。
- 其余（INB 主键、B3 依赖 enterprise_base、B2 禁洗等）全部继承 v1.0。
- **全卷对齐补遗（2026-10-20 晚，审查发现）**：09 头部版本块 v1.0→v2.0 + 派单包指针改指本目录；06 派工标题 v2.0。逐卷扫描（00/02/03/04/06/09/10/11/README）：03/04/10/11 无受 10-19 变更影响引用，维持继承。

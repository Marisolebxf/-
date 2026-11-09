# GDF 派单包（人类可读）

> GDF 数据中台团队**不使用 Cursor**。对外沟通用本目录工作包 + 飞书/例会，不用智能体派单话术。
> **2026-10-20 基线切换**：三方承诺清单更新为 10-19 版（176 表，架构师入仓 `gkx-mysql-raw/加工/GKX数据源表差异分析摘要-20261019.md`）；企业、产业链两包随之升版。

| 工作包                                                                         | 范围                                                                                                                                                                        | 版本                                                                                                                          |
| --------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| [企业/GDF-ENT-WORKPACK-v4](企业/GDF-ENT-WORKPACK-v4/) | 贴源 + Mapping + **写 ES**（`gkx_enterprise`）+ 图谱日批触发；**10-19 基线**（stock_base 移出 / 国外母子换源 `dwd_agg_subsidiary_info` / 专利侧表 +5 mirror_only） | **v4.0**（2026-10-20）· **现行企业包（可对外投递）** · Owner **徐滕强** · 含 `16-缺口分析回复工作包`（继承） |
| [产业链/GDF-CHAIN-WORKPACK-v2](产业链/GDF-CHAIN-WORKPACK-v2/) | 产业链四表贴源+洗链树/`entity_rel`；分析六表只贴不洗；**10-19 基线对齐**（四表行数不变；链树 live 实证 `parent_name` 列）。正式产业锚点写 Milvus 库 `gkxlumen` 的集合 `gkxlumen_industry_anchor`（已建，0 条） | **v2.2.7**（2026-11-02）· **现行产业链包（可对外投递）** |
| [政策/GDF-POLICY-WORKPACK-v2](政策/GDF-POLICY-WORKPACK-v2/) | 贴源 + Mapping → 一张 `policy_base_info`；B 成功后由 GDF Python 节点跑 `scripts/` 里的产业抽取与条款结构化。C1 只读 Milvus 库 `gkxlumen` 的 `gkxlumen_industry_anchor`。`17`–`20` 写 MDC / Graph / MRC / 灌数闸门，MDC 脚本未进包。取数不过滤 `is_deleted` / `is_history`。不含 ES | **v2.0.8**（2026-11-02）· **现行政策包** · Owner **淮政玮** · 任务 `GDF-POLICY-WORKPACK-V2-L01` |
| [技术节点产业映射/GDF-TECH-NODE-WORKPACK](技术节点产业映射/GDF-TECH-NODE-WORKPACK/) | 按页只读久新 Doris `ads_technology_profile` 同步技术节点，再按名称向量最近邻关联产业节点。落表 `gkxlumenx_dwd.dwd_tech_node_industry_map`。产业锚点只认库 `gkxlumen` 的 `gkxlumen_industry_anchor`。两张映射里先做本包 | **首版**（2026-10-31 成包）· **2026-11-02 已对 GDF 发出** · **优先开工** · 任务 `SYSINT-06-20-L01` · 监管人 **徐滕强** · in_progress · 未建作业，已执行建表 |
| [子学科产业关联/GDF-SUBFIELD-TOPIC-WORKPACK](子学科产业关联/GDF-SUBFIELD-TOPIC-WORKPACK/) | 子学科目录同步（本侧 `SUBFIELD_CATALOG`）+ 人工触发后把未映射子学科关联到本侧产业节点。落表 `gkxlumenx_dim.subfield_topic_map`。产业锚点只认库 `gkxlumen` 的 `gkxlumen_industry_anchor`。排在技术节点产业映射之后 | **首版**（2026-10-31 成包）· **2026-11-02 已对 GDF 发出** · 任务 `SYSINT-06-19-L01` · 监管人 **淮政玮** · in_progress · 未建作业，已执行建表 |
| [宏观行业/GDF-MACRO-WORKPACK-v1](宏观行业/GDF-MACRO-WORKPACK-v1/) | **市场研究红标第 1（P0）**。宏观行业要素库六表：贴源 + Mapping 到 `gkxlumenx_dwd` 六张 `macro_*`（事实表带区划反解列，ADS 只取 `area_code_type=1`）；②a 城市宏观截面写 `gkxlumenx_ads.macro_city_section`；落地实效结果面代理（②b）仅附录，不调度，不写正本三维。不并入政策包，不含金融与行业分析 | **v1.0.0**（2026-11-09 成包）· 可投递草稿 · 未建表、未灌数、未核现网 · 任务 `GDF-MACRO-WORKPACK-L01`（跑通叶 `SYSINT-06-05-L01`）· Owner **淮政玮** |
| [服务机构/GDF-SVC-WORKPACK](服务机构/GDF-SVC-WORKPACK/) | GDF 配一趟后加工：读供应方四张 `dwd_org_*`，写圈定池、投融资事件、卡面和基础指标 A1–A6。文件按 `00`/`06`/`08`/`09`/`12`/`15` 拆开，无贴源清单。不写图库，不含内容运营 | **首版**（2026-11-02）· **2026-11-02 已签收** · 发出日期未记 · 任务 `SYSINT-06-21-01-L03` · 监管人 **淮政玮** · 未建作业，未执行建表，未灌数 · 不是可对端 |
| [金融数据/GDF-FIN-WORKPACK-v1](金融数据/GDF-FIN-WORKPACK-v1/) | 金融要素库物理表 **31 张**（行数报告列 32 行，`dwd_corp_basic_info` 重复）。P0/P1 共 19 张洗入 11 张 `gkxlumenx_dwd.fin_*`；P2 行情/期权/外汇 6 张与公募基金 0 行 3 张只贴不洗；融资/投资/并购 3 张归企业包不重复配。② 4 张金融 ADS 草稿（Java 只读）。与落地实效无关，不与宏观包并包。结构以 live `gkx` 为准；DWD/ADS 建表草稿未签收 | **v1.0**（2026-11-09 首版成包）· 任务 `GDF-FIN-WORKPACK-L01`（WBS-06-04B）· 监管人 **淮政玮** · 市场研究红标第 2 · 跑通叶 `SYSINT-06-04-L01` · **未建表、未灌数、未发出、不代表跑通** |

### 裁定 / 只贴（非 Mapping 包，不可当作业投递）

| 目录 | 范围 | 版本 |
| --- | --- | --- |
| [行业分析/GDF-INDANA-SCOPE-v1](行业分析/GDF-INDANA-SCOPE-v1/) | **裁定，不是 Mapping 包**：行业分析六表现行**只贴 ODS**（施工入口仍是产业链 v2 Wave A），**禁止洗项目 DWD**（`CHAIN-B2-INDANA`）；`companies` 102 行禁用覆盖维；解禁条件占位，须李伟 / 架构书面；**不解禁不开 `GDF-INDANA-WORKPACK`** | **v1.0**（2026-11-09）· 任务 `GDF-INDANA-SCOPE-L01`（WBS-06-06B）· 市场研究红标第 3 |

本索引每个维度只留现行包。历史包不在表内。

正式产业锚点只在 Milvus 库 `gkxlumen`、集合 `gkxlumen_industry_anchor`。demo 的同名集合在库 `default`。写入只在产业链包 `12`。政策 C1、技术节点产业映射、子学科产业关联只读这一库。企业包、服务机构包不读写这个集合。

发出日期以 [工程侧发送记录](../../../工程过程/04-系统集成/06-GDF数据治理集成/对接文档/工程侧/README.md) 为准。技术节点产业映射、子学科产业关联两包的发出日期都是 **2026-11-02**。两张映射里先做技术节点产业映射（`SYSINT-06-20-L01`），子学科产业关联（`SYSINT-06-19-L01`）排在其后。服务机构包 2026-11-02 已签收，发出日期未记。

企业建表 / ALTER：**只认企业 v4 包内** `10-DWD-MySQL-DDL/`（与 v3.1 快照一致）。
Mapping：各域只认各自现行包 README 指定的 `09-*Mapping明细*`；短版导读不作施工真源。
**三方源结构以 live** `gkx` **为准**；10-19 Excel 纪要中"Excel 多出"列（t_id/区划码等）live 库不存在，不作源（ENT v4 CHANGELOG / CHAIN v2 09 头注均已声明）。

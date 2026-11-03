# 产业领域 ↔ 学科领域 ↔ 三要素 关联总览（2026-11-02）

> **目的**：把「产业领域怎么和学科领域关联、怎么和三要素关联」的**现状机制**整理成单一真源，供**展示系统（DS-01 科技全域态势）与专题（产业链/全景）做综合分析检查时对照，保证两侧口径一致**。
> **铁律（沿 `SYSINT-INDDISC-02-L01`）**：领域对领域**没有可确认映射**，本文只记录现状与通道，**不把任何一处写成"已对齐"**；`subfield_topic_map` 的 LLM 行、`M_ORG_INDUSTRY_COVER` 的 mock 口径均不得当领域字典引用。
> **关联任务**：`SYSINT-INDDISC-02-L01`（WBS-02-13，淮政玮）、`SYSINT-TFMAP-02-L01`（WBS-02-08，已签收）、`SYSINT-TECHMAP-02-L01`（WBS-02-12）、`SYSINT-SIT-02-L01`（WBS-02-02 三要素供数）、`SYSINT-TOPIC-CHAIN-ALIGN-02-L01`（WBS-02-11）。

---

## 0. 一句话结论

**产业领域与学科领域之间没有"领域对领域"的官方映射**（两套编码、无同名 ID、无对齐字典）。当前**唯一实际打通的通道**是 `subfield_topic_map`（WBS-02-08）：子学科 `subfield_id` --LLM 关联--> 产业节点（带 `industry_id` / `cluster_id`）。展示系统 DS-01 的「产业→学科反查」下拉与专题全景的「主流技术路线」**读的是同一张表**——这就是两侧综合分析必须保持一致的锚点。

## 1. 三套编码体系（禁止混用）

| 编码 | 体系 | 真源 | 用在哪 |
|---|---|---|---|
| `CL-SEI-*/CL-FUT-*`、`INB*` | **产业**：深圳 10+5 产业集群 / L0 产业 | 种子 `seeds/industry-cluster-sz-10+5-2026.yaml`；现网 `{INNOV_DIM_SCHEMA}.industry_cluster` + `industry_cluster_map`；前端冻结副本 `lumen-ui-science-pc/src/lib/industryCluster/seed.ts` | 展示「产业分类」级联（`IndustrySelect`）、DS-01 筛选一级下拉（`/industry-domains`） |
| `D-*` | **技术领域**：`dim_tech_domain` | innov `/v1/graph/domains` | 科创事件领域筛选（`/fields`）——**与产业、子学科均不同源** |
| `subfield_id` | **学科**：久新 OpenAlex 子学科 252 行 | `ads_discipline_subfield`（上排 `field_id` 26 行 / `domain_id` 4 行，下探 `topic_id` 4516 行，均**非挂钩口径**） | 政策三页「技术领域」多选、DS-01 筛选二级下拉（`/subfields`）、学科真实计数 `ads_geo_yearly_discipline_metrics`（1,015 万行） |

> 后端 `SituationController` 注释明令：`/industry-domains`（CL/INB）与 `/fields`（D-*）**两套编码禁止混用**（第 1071-1072 行）。

## 2. 当前唯一打通的关联通道：`subfield_topic_map`

```
产业集群 CL-* ──(industry_cluster_map)── L0 产业 INB*
     │                                    │
     │              subfield_topic_map（WBS-02-08，390 行 / 130 个已映射子学科）
     │              子学科 subfield_id ──LLM──> 产业节点 node_id
     │              （行上带本侧 industry_id、cluster_id）
     ▼                                    ▼
DS-01 筛选二级下拉 /subfields        专题全景「主流技术路线」（WBS-02-09）
（产业领域 → 学科领域反查，              （产业节点反查技术路线 =
 source="subfield_topic_map"）           子学科中文名 + subfield_id）
```

- **展示侧用法**：`POST /display/v1/situation/subfields`，入参 `clusterId`（可加 `industryId`），经 innov `subfieldByIndustry` 反查 `subfieldIds` + `items`，响应里显式带 `source: "subfield_topic_map"`。
- **专题侧用法**：全景图谱按产业节点查「主流技术路线」，读同一张映射表（WBS-02-09，先在算法中台实现后迁 `lumen-ui-topic`）。
- **性质声明**：表内行是 **LLM 对产业节点的关联结果，不是领域字典**；130 条未逐条复核，**不得标已对齐**。要当领域映射用必须另做核对。

## 3. 领域对领域映射：官方结论 = 不可映射（`SYSINT-INDDISC-02-L01` §3）

| 左侧 | 右侧 | 结论 |
|---|---|---|
| 展示 `cluster_id`（CL-\*） | `subfield_id` | 不可映射：两套编码，集群表无 `subfield_id`，子学科表无 `cluster_id` |
| 展示 `industry_id`（INB\*） | `subfield_id` | 不可映射：INB\* 是深圳集群 L0，非子学科主键体系 |
| 久新 `ads_industry.industry_id` | `subfield_id` | 不可映射：门类—小类层级，非 OpenAlex 子学科 |
| `ads_institution_industry` | `ads_discipline_subfield` | 不可映射：机构产业表（135 万行）**无 `subfield_id`**；机构学科表 `ads_institution_discipline_profile`（723 万行）**无 `industry_id`**——两张结果表不能互相当筛选条件 |
| `M_ORG_INDUSTRY_COVER` | 展示 CL-\*/INB\* | 不可映射：候选表是久新产业分类，口径未对齐（D1 draft / D4 mock） |
| `field_id` / `domain_id`（上一级） | 任一侧 | **排除**（2026-11-01 李伟口径：久新侧只用 `subfield_id`） |
| `technology_node_id` / `tech_id` | 任一侧 | **排除**（属 WBS-02-12 与正式技术目录，不是学科） |

**展示侧「产业领域」五处出处（真源待 `human:李伟` 指定，互不合并）**：① `industry_cluster`+`industry_cluster_map`（**筛选字典**，唯一确认）；② `dwd_industry_chain_info`（目录类，角色待定）；③ `dwd_org_industry_tags`（主体↔链标签，`INB*` 多码未拆行，ENT-P0-2 未回复）；④ `dwd.enterprise_industry`（**仅指标口径**，企业画像）；⑤ 久新 `ads_institution_industry`（产业分类非学科）。详见 `方案-SYSINT-INDDISC-02-L01.md` §2.4。

## 4. 三要素挂载

「三要素」两侧定义不同，做综合分析检查时**必须先分清语境**：

| 语境 | 三要素 | 任务 |
|---|---|---|
| 展示·科技发展态势八页 | **技术 / 技术链（产业链）/ 科研机构** | `SYSINT-SIT-02-L01`（WBS-02-02）；三要素供数公共件 `api/situation/honestEmpty.ts` |
| 展示·科技人才态势四子页 | 同上口径的人才侧供数 | `SYSINT-TAL-02-L01`（WBS-02-01） |
| 专题侧 | **技术链 / 人才 / 科研机构**（深度叶写死不开） | WBS-02-03 不建；缺口由 WBS-02-10/02-11 收口 |

**产业↔学科挂钩任务挂三要素**：李拜六 2026-11-01「展示系统的产业领域无法和学科领域做挂钩」→ 淮政玮「我在三要素集成中处理」→ 归 `SYSINT-INDDISC-02-L01`（WBS-02-13），**先跳过未执行**（李伟 2026-11-01 指示，DS-01 的 D2/D3 不依赖它）。

三要素各自的关联表：

| 要素 | 与产业/学科的关联载体 | 状态 |
|---|---|---|
| 技术（技术路线） | `dwd_tech_node_industry_map`（`technology_node_id` ↔ 产业链 `node_id`，WBS-02-12） | 建设中；全景「主流技术路线」最终改读此表（替代子学科映射） |
| 技术链（产业链） | `dwd_industry_chain_info`（目录）+ `dwd_org_industry_tags`（主体↔链） | 角色待定（§3 五处出处之②③） |
| 科研机构 | 产业侧 `ads_institution_industry`（无 subfield_id）；学科侧 `ads_institution_discipline_profile`（无 industry_id）；机构挂学科结果 723 万行 | **两侧不能互筛**（领域对领域结论）；`M_ORG_INDUSTRY_COVER` 口径 draft/mock |

## 5. 展示系统（DS-01 全域态势）实际链路

| 前端动作 | 端点 | 数据源 | 编码 |
|---|---|---|---|
| 一级下拉「产业分类」 | `POST /industry-domains` | innov `/v1/meta/industry-clusters`（DIM 集群表） | CL-\*/INB\* |
| 二级下拉「学科领域」（产业→学科反查） | `POST /subfields` | **`subfield_topic_map`**（响应带 `source`） | subfield_id |
| 事件「领域」筛选 | `POST /fields` | `dim_tech_domain`（innov `/v1/graph/domains`） | D-\* |
| 前端种子与解析 | `src/lib/industryCluster/`（seed/resolve/deepCascade） | 种子 yaml 冻结副本 + 别名表（`FUTURE_CODE_ALIASES` 与 Java `IndustryClusterLogic` 同表） | CL-\*/INB\* |
| 领域筛选生效范围 | `/events`：地域+领域**真实参与**（display 侧就地过滤）；`/map` 企业侧：`selectedFieldValues` **不参与**（企业主表无领域列） | — | — |

## 6. 专题侧实际链路

| 页面/功能 | 数据源 | 任务 |
|---|---|---|
| 全景图谱「主流技术路线」 | 现读 `subfield_topic_map`（产业节点反查技术路线=子学科）；**终态改读 `dwd_tech_node_industry_map`**（WBS-02-12 落地后） | WBS-02-09 |
| 政策三页「技术领域」多选 | 久新 ADS 字典内部 API（`subfield_id` 中文选项） | `SYSINT-DICT-02-L01`（WBS-02-07） |
| 产业链分析三要素嵌入指标 | 与久新 ADS 对照：**93 条口径均"还没有/未对齐"** | `SYSINT-TOPIC-CHAIN-ALIGN-02-L01`（WBS-02-11） |
| 产业集群列表接口 | 读 `{INNOV_DIM_SCHEMA}` 两张 DIM 表，**不读久新** | — |

## 7. 展示 ↔ 专题 一致性检查清单（综合分析对照用）

1. **共同锚点唯一**：两侧凡涉及「产业→学科/技术路线」，必须落在 `subfield_topic_map`（或其继任 `dwd_tech_node_industry_map`）**同一张表**，不得一侧读表、一侧读字典接口各说一套。
2. **三套编码禁混**：CL-\*/INB\*（产业）、D-\*（技术领域）、`subfield_id`（学科）——任何跨编码"翻译"必须在唯一翻译层（参考 `/map` `/overview` `/compare` 同源原则），不得散落各端点。
3. **文案陷阱**：展示/专题部分列名写「产业领域」但只是**指标口径**（`dwd.enterprise_industry`、`M_ORG_INDUSTRY_COVER`），不是筛选字典；检查时先问"这一列读哪张表"，不按列名对齐。
4. **LLM 行不得当字典**：`subfield_topic_map` 130 条是 LLM 关联结果；专题与展示若各自抽样复核，须用同一版本行数（390 行 / 130 子学科）核对，防止两侧不同步。
5. **诚实空态**：映射不到（`pending_vendor` 集群、未映射子学科、93 条未对齐指标）时两侧统一"空 + 原因说明"，不补 0、不回落 mock 冒充。
6. **变更同步**：真源一旦由李伟指定（§3 五处出处择一）、或 WBS-02-12 继任表上线，**本文 §2/§5/§6 与两侧实现须同步更新**，避免总览与代码漂移。

## 8. 出处索引

| 主题 | 文档 |
|---|---|
| 领域对领域结论 / 五处出处 | `工程过程/04-系统集成/02-对接三要素/方案-SYSINT-INDDISC-02-L01.md`（§2.4 / §3）；handoff `agent-handoffs/SYSINT-INDDISC-02-L01.md` |
| 子学科→产业节点（唯一通道） | `工程过程/04-系统集成/02-对接三要素/WBS.md` WBS-02-08/09/12 行 |
| 产业集群种子 | `agent-delivery/data/data-design/storage/CHAIN/seeds/industry-cluster-sz-10+5-2026.yaml`；前端 `src/lib/industryCluster/seed.ts` |
| 展示侧端点 | `lumen-svc-platform/gkxlumen-display/.../SituationController.java`：`/industry-domains`（L1077）、`/subfields`（L1147）、`/fields`（L1218 起）、`/events`（L1345） |
| 三要素供数 | `agent-handoffs/科技发展态势-TS/SITUATION-ENT-D-维度打通任务单草案.md`（D4 节）；`lumen-ui-science-pc/src/api/situation/honestEmpty.ts` 头注 |
| 专题指标对照 | `agent-handoffs/系统集成-SYSINT/SYSINT-TOPIC-CHAIN-ALIGN-02-L01/` |

> 本文档为编排仓口径记录，未改任何业务仓。维护责任随 `SYSINT-INDDISC-02-L01`（淮政玮）；两侧综合分析检查若发现本文与代码不符，以代码 + `方案-SYSINT-INDDISC-02-L01.md` 为准并回改本文。

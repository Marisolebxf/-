# 方案 · 产业挂钩对齐久新集群×学科映射（`SYSINT-CLSMAP-02-L01`）

> 2026-11-04 久新库重扫（[调研记录](./调研/调研记录.md) §0「和产业挂钩」）确认：久新已建好 `ads_sz_gkx_industry_cluster*` 三张表，113 条「集群×子学科」映射（67 个子学科，全部 `review_status=approved`，release `sz_gkx_industry_20261027_v1`），且子学科 ID 与我方 `subfield_topic_map` 完全同源（67/67 已在表中）。
> 本方案 = 我方产业挂钩方式切到与久新一致：**集群维度读久新已审映射，不再让集群×学科由 LLM 或人工另起一套**。
> 监管人：`human:淮政玮`。执行：`agent:algorithm-agent`（数据与 Java）+ `agent:api-agent`（lumen 读侧）。协作：`agent:frontend-agent`。

## 0. 现状与差距（为什么改）

| 维度 | 久新（真源） | 我方现状 | 差距 |
|---|---|---|---|
| 集群目录 | `ads_sz_gkx_industry_cluster` 15 集群 | `dim.industry_cluster` 15 集群 | 一致（同套深圳 10+5） |
| 集群→L0 产业 | 按产业名称挂 39 个（每集群 1–7 个） | `industry_cluster_map` 仅 15 行（12 条 L0，Q068 🟡） | 我方缺 6 集群的 L0，且产业名↔INB 码无对照 |
| 集群×子学科 | 113 条已审（CORE 78 / SUPPORTING 31 / APPLICATION 4，带 `mapping_weight`） | **没有这张表**。集群×学科是 `industry_cluster_map` + `subfield_topic_map` 两跳拼出来的，口径是 LLM 的 | 我方缺官方集群×学科层 |
| Topic×集群（产业链位置） | `ads_sz_gkx_industry_cluster_topic` 3,098 条，带 `UPSTREAM/MIDSTREAM/DOWNSTREAM` | 无 | 本叶不接（留给技术节点叶 WBS-02-12） |
| 子学科→产业节点 | 无（他们不做这层） | `subfield_topic_map` 390 行，LLM 关联 | 保留，是久新没有的增量 |

与既有叶的关系：
- **不推翻** WBS-02-08（`subfield_topic_map`）：它是「子学科→产业节点」层，久新没有；政策页技术领域→产业转换（`SYSINT-TFMAP` 消费）继续读它。
- **不顶替** WBS-02-13/14（INDDISC 口径澄清与展示侧联动）：那两叶消费的是子学科反查；本叶把集群×学科这一层的真源换成久新，反查结果会更准（覆盖 41 行现成吻合 + 30 行裁决后可用）。
- **衔接** WBS-02-05 调研（真源证据）与 WBS-02-12（技术节点叶，topic 那张表留给它）。

## 1. 目标形态（改造后）

1. 新建本侧镜像表 `demo_gkxlumenx_dim.cluster_subfield_map`（一行 = 一条久新已审映射）：

   ```sql
   cluster_code     varchar(32)  -- CL-SEI-01…（对齐 industry_cluster.cluster_id）
   subfield_id      varchar(64)  -- sub_<hex32>（与 subfield_topic_map.subfield_id 同源）
   subfield_name_zh varchar(512)
   openalex_subfield_id varchar(32)
   relation_type    varchar(32)  -- CORE / SUPPORTING / APPLICATION
   mapping_weight   decimal(9,6)
   mapping_method   varchar(64)
   review_status    varchar(24)  -- 只收 approved
   cluster_release_id varchar(64)  -- sz_gkx_industry_20261027_v1
   data_version     bigint
   update_time      datetime(3)
   ```

   逻辑键 `(cluster_code, subfield_id)`；按行 upsert，不整表清空；release 变化时旧行保留、新 release 追加，查询只取最新 `cluster_release_id`。

2. **同步**通道沿用 WBS-02-08 模式：`lumen-topic-py` 字典通道加 `op=cluster_subfield_page`（只读 Doris `ads_sz_gkx_industry_cluster_subfield`，每页 ≤500）→ `gkx-innov` `POST /v1/cluster-subfield-maps/sync` 按行 upsert。**不在页面直连久新**。久新表是全量小表（113 行），单次同步即可，不需要分批按钮循环。

3. **查询只读这张镜像表**（不再两跳拼接）：改造现有只读端点 `GET /v1/meta/industry-clusters/industry-subfields`（`IndustryClusterService.subfieldsForIndustry`）——数据源从「`industry_cluster_map` → `subfield_topic_map`」改为「`cluster_subfield_map`」。无映射集群（久新没挂的）返回空 + `emptyReason`，不回落拼接、不回落全量。

4. **消费方切换**（全部只读，接口签名不变）：
   - `lumen-svc-platform` `gkxlumen-display` `POST /v1/situation/subfields`（展示侧产业→子学科反查，TS-INDDISC-01 P1 已上线的那条）——下游 innov 端点不变，数据自动变准；
   - 展示态势页「产业领域 → 学科领域（细化）」级联；
   - 政策页技术领域→产业（`PolicyAnalysisConfigPage`，经 `subfield_topic_map`）**不动**——那是另一层。

5. **裁决清单**（人工，30 行 SUB-ONLY）：`cross_coverage.py` 输出里「我方 `subfield_topic_map` 关联的产业 ∉ 该集群 L0」的 30 行，逐条标注「信久新（收进集群口径）/ 信我方（保留产业节点关联、不进集群）/ 待定」。裁决结果写回 `industry_cluster_map`（把该集群缺的 L0 补上）或 `subfield_topic_map`（改关联），不改镜像表。**镜像表是久新的如实快照，不在里面手改。**

6. **Topic 级产业链位置不在本叶**：`ads_sz_gkx_industry_cluster_topic`（3,098 条，含上/中/下游）留给 WBS-02-12 技术节点叶或另立叶，本叶只做集群×子学科。

## 2. 分步交付

| 步 | 内容 | 仓 |
|---|---|---|
| ① | `lumen-topic-py` 字典通道加 `cluster_subfield_page` op；`gkx-innov` 加 `cluster_subfield_map` upsert + `GET /v1/cluster-subfield-maps/stats` | `lumen-topic-py`、`demo-svc-platform` |
| ② | `IndustryClusterService.subfieldsForIndustry` 切数据源到镜像表（表空时回落旧两跳并带 `source` 标注，防止切换期空窗） | `demo-svc-platform`（镜像读侧同步给 lumen `gkxlumen-innov`） |
| ③ | 展示侧回归：`/v1/situation/subfields` 反查结果与 113 条一致；6 个无映射集群诚实空态 | `lumen-svc-platform`、`lumen-ui-science-pc` |
| ④ | 30 行 SUB-ONLY 裁决会（淮政玮 + 李伟），裁决写回 L0 或产业关联；镜像表重扫时自动对齐 | `gkx-orchestration`（记录） |

## 3. DoD（任务定义里引用）

- 镜像表落库且只含 `review_status=approved` 行，行数与久新 release 一致（113）；密码不进 git。
- 同步是幂等 upsert，按 `(cluster_code, subfield_id)`，不整表清空；重复执行行数不变。
- `industry-subfields` 反查改为读镜像表；9 个 mapped 集群返回的子学科集合与久新 113 条完全一致；6 个无映射集群返回空 + 原因，不回落全量。
- 展示态势页回归：CL-SEI-01 反查子学科由 LLM 拼接口径变为久新已审口径，接口签名不变；政策页 `subfield_topic_map` 路径零改动。
- 30 行裁决清单产出并交监管人；不裁决不阻塞 ①②③ 上线（镜像表是快照，裁决影响的是 L0/产业关联表）。
- 诚实性：切换期回落旧口径时必须带 `source` 标注；不得把拼接口径冒充久新已审口径。

## 4. 明确不做

- 不重跑 LLM 生成集群×学科（久新已审就是真源）。
- 不改 `subfield_topic_map` 的生成逻辑（WBS-02-08 产物）。
- 不接 Topic×集群表（WBS-02-12 域）。
- 不在本叶动政策三页提交逻辑（已由 SYSINT-TFMAP 消费另行完成）。
- 不在镜像表手工修数。

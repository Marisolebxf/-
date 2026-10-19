# SCI-INT-A10 handoff：科技指数系统集成项

| 项 | 值 |
|---|---|
| task_id | SCI-INT-A10（spike） |
| 执行 | agent:product-agent（协作 architect-agent；coordinator_dispatch） |
| 监管人 | human:淮政玮 |
| 对端 | 北京久新（旧路径沿用「九新」写法） |
| ponytail | N/A（spike 分析，无代码） |
| 日期 | 2026-10-19 |

## 1. 范围与实现

- **范围**：需规 `bid-reference/srs/02-科技信息展示系统/科技发展态势/科技指数.md`，excel_row 162–180（seq 159–177），共 19 个 SRS 叶。对应 3 个 DS 页面：DS-08-INDICATOR（162–166）、DS-08-VIZ（167–173）、DS-08-RANK（174–180）。
- **实现**：按 `产物/_card-template.yaml` 输出 21 张页面级卡片（号段 INT-A-*-900～927）。row 167「专家 H 指数排行」拆成排行读面（久新）和专家详情/筛选维（三方库）两张；row 174「科技成果综合排名」拆成排名分值和成果实体主数据两张。
- **输入**：`产物/_prep/A10-pack.yaml`、C-index、global-findings、B01 集成模式；只读核对了 lumen-ui-science-pc `views/situation/tech-index`（四个 Tab、models、api、types、mock）、lumen-svc-platform（无 tech-index 和 `/situation/v1` 端点）、lumen-algo-py（无对应 `/internal` 路由，只有 vendor/innov-py 这份 demo 拷贝）。
- **MCP**：页面上 5 个未关联指标都用 `metric-get` 复核过：M_INNOV_EXPERT_HINDEX、M_INNOV_EXPERT_ACTIVITY（third_party）；M_INNOV_SCIINDEX_VALUE、M_INNOV_SCIINDEX_INFLUENCE、M_INNOV_SCIINDEX_RANK_SCORE（STAT）。五个都是 D1=draft、D4=mock，source_tables=pending_ods，formula 处于 pending_cosign（等 human:唐绍祖 签字）。

### 1.1 页面指标挂叶

| metric_id | 挂到的 SRS 行 |
|---|---|
| M_INNOV_EXPERT_HINDEX | 167 |
| M_INNOV_EXPERT_ACTIVITY | 170 |
| M_INNOV_SCIINDEX_VALUE | 168（区域分布）、164（计算方法说明引用其 formula） |
| M_INNOV_SCIINDEX_INFLUENCE | 169 |
| M_INNOV_SCIINDEX_RANK_SCORE | 174–179（分类、详情、历史、对比、搜索都读同一套已落库分值） |

### 1.2 派单关注点结论

1. **专家 H 指数 / 活跃度属 TAL**。对象是专家，也就是人才主体，主键跟随 C01 的候选 `dwd_scholar.scholar_id`（INT-C-TAL-001，供应方 P0-1 未定）。
   - **H 指数**：计算归属在对端。久新 DS-08-VIZ-001 随 API-162「人才学术力评估」一起交付（C01 INT-C-TAL-049，IP-08）。注册口径明确写着「禁止伪展开 Hirsch 公式，数据源默认外采只读」，所以我方不实现 H 指数算法，只做排序和筛选读面。三方库 `dwd_scholar.h_index` 是供应方已经算好的列，作为降级或对照源；两者谁为主由 OI-C01-15 决定（PM / 郭万迎）。
   - **活跃度**：计算归属同样在对端（久新 DS-08-VIZ-004，IP-08）。过渡期我方可以按注册口径用 STAT 自建「月度论文数」分子（IP-01，原料为 INT-C-TAL-006/007）。项目参与和学术活动不进公式：项目参与表行数未知，学术活动全链路无源，这两项在页面上置灰并加 ⚠️。
   - **前端现状需要纠正**：`getExpertActivityScores` 用 `publications*0.38`、`citations/210` 等硬编码系数在前端合成六维活跃度，等于算法放在前端（R-A10-2），正式实现必须删除，改为后端出数。
2. **排名历史快照（IP-11）**：
   - **存哪**：lumen 正式库 ADS 层新建行级快照表（候选名 `ads_sci_index_rank_snapshot`）。不复用 IP-11 的通用 JSON 快照，因为历史曲线、分类、搜索、对比都要按 achievement_id 和 period 过滤。不上 Nebula，默认也不建 ES 索引。只有一个写者：如果是外部发布值，由 lumen-etl-es-py / GDF 导入；如果我方自建，由 lumen-algo-py 批 Job 写入。Java 只读。
   - **粒度**：一行对应 (period_id, board, achievement_id)，字段含 rank、total_score、四个一级指标分、prev_rank、rank_delta、weight_version、algo_version、snapshot_id、source、data_as_of。period 按注册口径默认自然年，但前端现在按日期点画曲线，粒度待 DN-A10-04。
   - **版本**：append-only。权重或算法换版时另起 weight_version / algo_version，不回改历史行。幂等键为 (period_id, board, achievement_id, weight_version)，weight_version 指向指标体系版本表（INT-A-X-900）。
   - **新表即 structure_escalation**（INT-A-X-924）→ human:李伟，并入 DN-07；如果排名数据来自久新，还涉及 DN-09（落库合规）。
3. **科技指数本体的生产方未定**：注册口径写「综合合成在智库后台（Q-TINDEX-01 待登）」，但三方库、久新 51 行（本页只有 VIZ-001/004 两条人才行）、我方 Java 和 Python 都查不到指数值、影响力时序或成果综合分的来源。草案按 IP-01「外部发布值导入 ADS」处理，counterpart 写 `other:智库后台（未定）`，登记 DN-A10-01；如果最后改为我方自建，SCIINDEX_VALUE 和 RANK_SCORE 就没有算法 owner（algo_owner_missing）。

### 1.3 需要久新提供的能力（全部待确认）

- **已有久新行 2 条**：DS-08-VIZ-001（专家 H 指数排行）、DS-08-VIZ-004（专家活跃度）。两条都已由 C01 并入 API-162，本叶不新增久新行。
- **新增久新能力需求：0 项**。科技指数、影响力和成果排名的生产方是否改由久新承担，在 DN-A10-01 中一并问。

## 2. 偏离说明

- **INNOV 指标填在 metric_domain_other**：5 个页面指标的域都是 INNOV（非三要素），按模板放进 `metric_domain_other`，`metric_ids` 留空。
- **counterpart 用 other:**：科技指数相关卡写 `other:智库后台（Q-TINDEX-01，未定）` 或 `other:科技指数评价体系发布方（未定）`，因为发布方不明，不推测成久新或我方。
- **B01 C7 的修正**：B01 记录 DS-08-VIZ-001/004 没有独立 metric_id；实际 INNOV 域已有 M_INNOV_EXPERT_HINDEX / ACTIVITY，只是 srs_refs 未回填。写入 CF-A10-4，不改 registry。
- **专家评议 Tab 超出范围**：lumen 页面第四个 Tab「专家评议」（PeerReviewTab）没有对应的 SRS 叶（招标描述提到同行评议专家智库），本叶不出卡，登记 DN-A10-08。

## 3. 产物清单

| 产物 | 路径 |
|---|---|
| 集成卡片 | `agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/产物/SCI-INT-A10.yaml` |
| 自检脚本 | `agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/产物/_work/A10-check.py` |
| 本 handoff | `agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/SCI-INT-A10.md` |

未改业务仓、seed、矩阵或 task-registry.yaml，未执行 git commit/push。

## 4. 验收证据

自检命令为 `python 产物/_work/A10-check.py`。脚本先用 yaml.safe_load 解析，再核对 P00 中 leaf=A10 的范围、差集、号段 9xx、id 唯一、IP 编号、页面归属、三要素卡的四段调用链、调用链里没有 demo-*（D12）、久新行在 P00 内、5 个页面指标全部挂接，以及 summary 一致性。实际输出：

```
scope_count=19 covered_rows=19 diff=[]
cards: 21 {'X': 16, 'TAL': 3, 'TECH': 1, 'ORG': 1}
jiuxin_rows: ['DS-08-VIZ-001', 'DS-08-VIZ-004']
metric_missing: 4 ['INT-A-TAL-911', 'INT-A-TAL-914', 'INT-A-X-904', 'INT-A-X-923']
structure_escalation: 7 ['INT-A-TAL-910', 'INT-A-TAL-914', 'INT-A-X-900', 'INT-A-X-912', 'INT-A-X-913', 'INT-A-X-920', 'INT-A-X-924']
patterns: {'IP-01': 10, 'IP-08': 2, 'IP-09': 2, 'IP-10': 1, 'IP-11': 1, 'IP-12': 2, 'IP-13': 3}
OK
```

**范围 19 / 已出卡 SRS 行数 19 / 差集 0**

### 4.1 统计

- **卡片**：共 21 张，其中 TAL 3、TECH 1、ORG 1、X 16。
- **久新依赖**：2 条（DS-08-VIZ-001 / 004），新增 0 条。
- **metric_missing（4 张）**：指标权重数值（904）、专家详情中的被引次数和论文数（911）、活跃度分维度（914）、成果四个一级指标得分与权重贡献（923）。
- **algo_owner_missing**：M_INNOV_SCIINDEX_VALUE、M_INNOV_SCIINDEX_RANK_SCORE（如果不是外部发布）。
- **structure_escalation（7 张，升级 human:李伟）**：
  - INT-A-X-900：指标体系配置表和版本表。
  - INT-A-TAL-910、INT-A-TAL-914：专家 H 指数和活跃度结果快照，并入 IP-11 候选快照表。
  - INT-A-X-912：区域指数值表。
  - INT-A-X-913：影响力时序表。
  - INT-A-X-920：综合排名表。
  - INT-A-X-924：排名历史快照表（主承接卡）。
  - 912、913、920、924 建议合成一个 `ads_sci_index_*` 族，一并评审。
- **decision_needed**：新增 DN-A10-01～09；引用 OI-C01-15、OI-C01-03、OI-C02-02、OI-C03-02、DN-01、DN-03、DN-07、DN-09、DN-A08-13、Q069。
- **risks**：R-A10-1～9，其中 high 级 3 项。

### 4.2 关键冲突与待决

- **CF-A10-1**：H 指数和活跃度在 registry 的 algorithm_type 是 third_party，久新行写的是 MODEL（同 B01 C2）。
- **CF-A10-2**：SCIINDEX_* 登记为 STAT，但 definition 写「差集 other_system」「综合合成在智库后台」，类型和生产方不一致。
- **CF-A10-3**：前端四个榜单按高校/企业/科研机构拆分，而 SRS 175 要求按科技领域、成果类型、机构类型、地域组合筛选。
- **CF-A10-4**：B01 C7 的说法已过时，见第 2 节。

### 4.3 最大 3 个开放项

1. **科技指数、影响力、成果综合分的生产方和指标体系权重**（DN-A10-01 / 02，同类 DN-03）：这决定 DS-08 三个页面的全部数值来源，现在任何一层都查不到真源。
2. **「科技成果」对象范围和统一成果 ID**（DN-A10-03）：论文、专利、项目三套主键，C02 也没有 technology_id。排名快照的 achievement_id 跨期是否稳定，直接决定历史曲线、对比和详情下钻能否成立。
3. **专家 H 指数和活跃度的主源**（OI-C01-15 + DN-01）：久新 VIZ-001/004 的形态和 SLA 都待确认，`dwd_scholar.h_index` 能否作为降级源也未定；人才主键同样受 C01 P0-1 阻塞。

## 5. 架构合规自检

| 铁律 | 结论 |
|---|---|
| 1 算法只在 Python | ✅ 方案里的算法都在对端或 lumen-algo-py 批 Job，Java 只读 ADS。⚠️ 现状违规：前端合成活跃度、派生领域趋势系数、派生成果总分和名次，已写入 R-A10-2 |
| 2 调用链：前端 → Java → Python /internal | ✅ 久新两条行走 Python 适配层（IP-08），Java 不感知久新，前端不直连 |
| 3 只用 NebulaGraph | ✅ 本页不需要图谱，快照不上图 |
| 4 可观测 | ⚠️ 前端已有 `ts-tech-index-track` + createTraceId；但 `/situation/v1/tech-index/dataset` 后端不存在，api 层 real 用裸 fetch（R-A10-8），链路无法贯通，由实现叶补齐 |
| 5 CI/CD | N/A（分析叶，cicd skip） |
| 6 demo 只读 | ✅ demo 只作对照；vendor/innov-py 的 AHP+熵权和 AVG(h_index) 标为不可复用（R-A10-7） |
| 7 共享聚合核心 | ✅ Java 门面模块归属引用 DN-07 |
| 8 ADS 先行 + Mock | ✅ 无源项走 IP-10 / 置灰加 ⚠️。⚠️ 现状：index.vue 用 mock 种子初始化，IndicatorTab 和 IndicatorDetailPanel 直接 import `@/mock`，违反 IP-13（R-A10-1）；模拟实时随机扰动（R-A10-4） |
| 9 D8 | N/A（不改 UI） |
| 10 D9 | ✅ 5 个页面指标都已挂叶，无注册的统计数字记为 metric_missing（4 张）。⚠️ 现状：页面没有任何 ⓘ 和角标（R-A10-5） |
| 11 D10 | N/A（不改 UI）；轮播可暂停、键盘可达写进 915 的 test_points |
| 12 D12 | ✅ 所有卡片调用链里都没有 demo-*（脚本断言）。风险：vendor/innov-py 是 demo 拷贝，禁止复用（R-A10-7） |
| 禁读 registry YAML | ✅ task 和 metric 都只通过 MCP 查询 |

## 6. cost

| 字段 | 值 |
|---|---|
| actual_tokens | 260000（估算） |
| model_used | claude-opus-5.5 |
| actual_cost | 6.0（USD，估算） |
| cost_warn | yellow |

cost_warn 记为 yellow：token 消耗约为预算 90k 的 2.9 倍，主要花在 C-index 全文和 metric-get 复核上；单任务金额低于 $10 暂停线。

# SYSINT-POL-ADS-REQ-L01 · 政策扶持读数对 ADS 的需求

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 长任务总控 `PORTAL-POL-长任务总控.md` 已授权。本叶只写需求。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `N/A` |
| 说明 | 定义需求。没有删需求行，没有改契约、种子或业务仓。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本叶按契约和存储稿原文写，未用压缩代替。 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | 不适用 |
| 图 diff | 未改存储流图 |
| 会签态 | 存储稿 `POLICY-STORE-MYSQL-ADS` / `POLICY-STORE-MYSQL-DWD` 的 frontmatter 仍是 `draft` |
| 说明 | 本叶不改图。 |

## 范围与实现

三组读数都还没有「Java 能只读的正式 ADS 已灌通」这一态。demo 库 `demo_gkxlumenx_ads` 有 16 张表的契约稿，状态 draft。`SYSINT-06-17-L01` 无派单包、无执行结果。`SYSINT-06-03-L01` 不写 ADS。`SYSINT-ADS-02-L01` 仍在做三要素主数据。本叶不实现加工，不把 mock 写成已接入。

门户十条不另建结果表。已签收的算法从政策主数据、产业链节点、政策–产业关联现算。正式链要读的是这三张的行，不是十条新 ADS 表。

## 偏离

无。契约 `PORTAL-CMS-政策扶持.md` 未改。

## 1. 力度排名（需规 96）

| 要的数 | 建议落点 | 现在还没有 |
|---|---|---|
| 省级、城市政策力度排名。排序只用 `M_POLICY_INTENSITY_SCORE`，不另注册排名 ID | `demo_gkxlumenx_ads.policy_intensity`（契约稿已列 `M_POLICY_INTENSITY_*`） | 正式 ADS 未灌通。`SYSINT-ADS-02-L01` 未完成。没有执行结果证明这张表已有可排序的分。CMS 不填名次和分数 |

## 2. 十条指标

算法读行，不读下面这些相近表来填数：`policy_level_dist`、`policy_timeseries`、`policy_national_dist`、`policy_sz_dist`、`policy_focus`。

| # | 要的数 | 建议落点 | 现在还没有 |
|---|---|---|---|
| 1 | 全国政策数量，以及有发布月份的连续性 | `policy_base_info` 中 `is_deleted=0` 的 `publish_date` | 国内政策贴源包未跑通（`SYSINT-06-17-L01`）。DWD 列名是 `publish_date`，不是单独的连续性结果列 |
| 2 | 各省政策数量对比，以及分省连续性 | 同上，地区列 `region` 解析到省 | 同上。`policy_national_dist` 是按省计数，不作为本条落点 |
| 3 | 重点城市政策数量对比及连续性 | 同上，城市名与已登记名单对齐：深圳市、广州市、北京市、上海市、杭州市、南京市、天津市、重庆市、合肥市、青岛市 | 同上。名单在 demo `settings_policy.yaml` 的 `portal_gaps.key_cities`，正式 ADS 没有这张名单表 |
| 4 | 全国政策发布密度 | 同上，按自然月计条数。分母口径 `natural_month` | 没有发布密度 ADS 表。分母只登记在 demo 配置，不在 ADS |
| 5 | 省发布密度 | 同上，省 × 自然月 | 同第 4 行 |
| 6 | 市发布密度 | 同上，名单内城市 × 自然月 | 同第 4 行 |
| 7 | 产业链各节点政策覆盖 | `policy_industry_rel`（`is_deleted=0`）加产业链节点表 | 关联表在 demo 抽取记录里约 2 万条政策只看到 17 条更新。节点表不在政策 ADS 16 张里。正式链未确认可读的节点行 |
| 8 | 深圳政策数量及趋势 | `policy_base_info.region` 含「深圳」，`publish_date` 分月 | 同第 1 行。`policy_sz_dist` 是按区存量，不作为本条落点 |
| 9 | 深圳各区发布情况 | `region` 以「广东省深圳市」开头的行，按区切片；区县空的归「市本级/未分区」 | 同第 1 行。没有单独的各区发布 ADS 表 |
| 10 | 深圳产业链节点政策覆盖 | 第 7 行的关联，再限定深圳政策 | 同第 7 行 |

## 3. 时间线五个字段（需规 97 与深圳最新政策）

| 契约字段 | 建议落点 | 现在还没有 |
|---|---|---|
| `policy_id` | DWD `policy_base_info.policy_id`。Java 只读时需要 ADS 上有同样业务键 | 正式 ADS 没有政策主数据镜像。`SYSINT-06-03-L01` 明确不写 ADS |
| `title` | DWD `title` | 同上 |
| `publish_time` | DWD 现列是 `publish_date`，不是 `publish_time` | 契约字段名和现列名不一致。本叶不改列 |
| `region_name` | DWD 现列是 `region` | 同上 |
| `source_url` | DWD 现列是 `url` | 同上。没有单独的源地址列 |

深圳最新政策用同一组字段，地区限定深圳。无记录则空列表。不新造运营导语。

## 4. 后续加工（本叶不开工）

| 后续 | 说明 |
|---|---|
| `SYSINT-06-17-L01` | 国内政策贴源加 Mapping。没有派单包和执行结果之前不算跑通。不并进 `SYSINT-06-03-L01` |
| 关联与节点 | `policy_industry_rel` 有效行和产业链节点行到位之后，第 7、10 条才能有覆盖数。不在本叶建新表 |
| 排名分 | `policy_intensity` 有 `M_POLICY_INTENSITY_SCORE` 的行之后，排名才有序。不另建排名表 |

## 产物清单

- 本 handoff

## 验收证据

- 三组都有建议落点和「现在还没有」
- 未改 `PORTAL-CMS-政策扶持.md`、指标种子、就绪度矩阵、`SYSINT-06-03-L01`
- 未生成 CDC，未写业务仓

## 架构合规自检

| 项 | 结果 |
|---|---|
| 调用链仍是前端 → Java → Python `/internal/*` | ✅ |
| Java 不写算法、不直连 nGQL | ✅ |
| 不调用 demo 服务进 lumen | ✅ |
| 未把 mock 写成已接入 | ✅ |
| 未新造对象存储桶 | ✅ |
| 未改 Nebula 为生产图 | ✅ |
| 本叶无业务代码 | ✅ |

## cost

| 字段 | 值 |
|---|---|
| actual_tokens | 未单列计量 |
| model_used | 未单列 |
| actual_cost | 未单列 |
| cost_warn | green |

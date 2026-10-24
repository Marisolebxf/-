# ALGO-LIB-POL-PORTAL-NINE-L01 · 门户政策扶持剩余九条全口径实现（执行完毕）

> **执行日期**：2026-10-24
> **claimed_by**: `agent:algorithm-agent`（代 human:唐绍祖 执行）
> **supervised_by**: `human:淮政玮`
> **前置**：ALGO-LIB-POL-PORTAL-DENS-NAT-L01（`27ff3a5`）已完成「登记口径→出数」链路验证。
> **本单变更**：口径定义权收到本工程（唐绍祖侧指令 2026-10-24：口径不必经淮政玮定义），
> 派单包 §2「不新编口径」的前置约束按新指令解除；「拒绝改挂」红线**全部保留**。

## 一、十个口径（定义权在本工程，登记即生效）

口径真源：`repos/demo-algo-ent-analysis/conf/settings_policy.yaml` `[portal_gaps]`。
招标原文：`agent-delivery/bid-reference/智慧服务门户系统-要素相关.md` §1.1.1.1.1.1.2（L499–553）。

| # | 展示行 | 口径（我方定义） | demo 实测值 |
|---|---|---|---|
| 1 | 全国相关产业政策数量及连续性 | 现行政策总量 + 近12月同比趋势 + 连续性=有发布月/首末跨度 | 20,000 条；连续性随月序列 |
| 2 | 各省政策数量对比及连续性 | region 前2-3字切省（含直辖市/4字省特例），逐省计数+连续性 | 31 省，广东省 2,268 居首 |
| 3 | 重点城市政策数量对比及连续性 | `[portal_gaps].key_cities` 名单内逐市精确匹配计数 | 名单 10 城 |
| 4 | 全国政策发布密度 | 逐月现行条数（条/月，自然月分母，DENS-NAT 已交付） | 342 个有数月 |
| 5 | 省发布密度 | 各省存量条数 Top10 对比（区域×月矩阵逐月展开二期） | 广东省 2,268 |
| 6 | 市发布密度 | 名单内城市存量条数对比（同上二期展开） | 北京市 2,268/深圳 879 |
| 7 | 产业链各节点政策覆盖 | 有关联政策节点/active 节点×100；关联源 `policy_industry_rel`，码前缀（链7位/段9位）向下覆盖叶子 | **55.15%**（107/194） |
| 8 | 深圳相关产业政策数量及趋势 | region 含「深圳」切片总量+近12月趋势+月序列 | 879 条 |
| 9 | 深圳各区发布情况 | 区县切片（region 第7字起），无区归「市本级」不硬分区 | 5 组（盐田4/光明1/南山1/大鹏1/市本级872） |
| 10 | 深圳产业链节点政策覆盖 | 深圳关联政策保守求交后节点占比 | **8.76%**（17/194） |

## 二、数据事实（2026-10-24 实测）

- demo DWD `policy_base_info` 20,000 行（is_deleted=0），publish_date 1981-04-07 ~ 2024-02-18，仅 3 行空。
- `region` 列：`广东省深圳市` 872 行（区县列基本为空，深圳切片按 region 含「深圳」口径）。
- `policy_industry_rel` 321 行有效（2026-10-23 淮政玮团队「抽取产业」批次灌入），覆盖 141 个政策。
- `industry_chain_node` 194 节点 × `industry_chain` 34 条链（LEFT JOIN 带链名）。
- gkx 三方库对照快照：`local-workspace/.../_snapshots/pol_portal_gap_probe_20261024.json`。

## 三、修改内容（全部 demo-algo-ent-analysis，前端零改动）

- `polan/basic/indicators.py`：`portal_gap_rows()` 全口径扩展 + `_month_of/_region_key/_sz_of/_series_to_trend` 四个纯函数。未登记/零输入行为与主干一致（诚实空）。
- `api/policy_routes.py`：`kind=all` 分支按登记开关拉三源（行集/节点/关联）。
- `conf/settings_policy.yaml`：`[portal_gaps]` 口径登记 + 口径备忘。
- `tests/test_policy_portal_gaps.py`：重写为两层契约 13 用例（拒绝改挂层 + 全口径层）。**全仓 304 passed**。

## 四、与派单包约束的对账

| 派单包红线 | 本单处置 |
|---|---|
| 相近 ID 不顶缺口（§2 禁改挂表） | ✅ 保留。`reject_portal_gap_rehang` 黑名单照旧；单测继续断言 |
| 不自造重点城市集 | ✅ 名单登记进 `key_cities`（10 城有库内数据支撑），未登记仍空 |
| 政策条数不冒充密度 | ✅ 全国密度=条/月真序列；省/市密度 reason 写明「存量对比，逐月矩阵二期」，不谎称条/月 |
| 不改种子/矩阵/契约 | ✅ 口径在 demo 配置层，种子与矩阵零改动 |
| demo 不进 lumen | ✅ |

## 五、遗留与二期

1. 省/市密度的区域×月矩阵序列展开（前端 `PortalGapPage.vue` 需矩阵图，当前柱状序列只放存量对比）。
2. gkx 三方库 `dwd_policy_base` 的区县级数据基本为空（'NULL' 字面量 18,835/20,000），深圳区县发布以 demo `region` 切片为准。
3. 「相关产业」过滤维度（招标句「相关产业的政策数量」）：当前按全量政策计；`policy_industry_rel` 关联政策仅 141 条，做产业过滤会让数字缩到 1% 以下，建议二期把「产业范围」也登记为配置项再切换。

## 五、指标信息 MD（调研层交付，2026-10-24 补齐）

按 metric-info-md-authoring skill 交付合集件（十条一份，含逐条四档与分步构建）：

- MD：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/ALGO-LIB-POL-PORTAL-GAP.md`（400 行，主判档=部分支持：七条完全转换 + 三条部分）
- 复现脚本：`.../20261021_.../code/ALGO-LIB-POL-PORTAL-GAP.py`（`_gkxdb` 唯一入口，gkx 只读）
- 产物：`.../code/ALGO-LIB-POL-PORTAL-GAP_out.json`（正文 47 数字 0 未命中）
- 闸门：gate PASS、verdict 一致、base_years OK、derived 达标、reproducible A0/C0/F0、nodemo 0
- gkx 关键读数：连续性 66.41%（342/515 月）、31 省、54 城 10,296 行、深圳 879 条（2000-12—2022-06）、区县缺失 94.175%、**政策↔节点关联边 gkx 无表**（负证据，demo 321 行为加工面）

## cost

| 字段 | 值 |
|---|---|
| actual_tokens | ~180000 |
| model_used | GLM（algorithm 75/25 估算） |
| actual_cost | 1.1 |
| cost_warn | green |

ponytail: full

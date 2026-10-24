# LUMEN-POLICY-TS-CALIBER-L01 · 政策时序口径差异表

> 管线：[`LUMEN-POLICY-TS-长任务总控.md`](./LUMEN-POLICY-TS-长任务总控.md)  
> 本叶只核对差异，不改 seed、不改公式、不改代码。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:product-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 长任务总控已授权。lock 24h。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `N/A` |
| 说明 | 定义叶，无代码。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本叶无大日志。 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | `POLICY-STORAGE-FLOW` |
| 图 diff | 未改图。时序仍只读 ADS `policy_industry_rel` + DWD `policy_base_info`。 |
| 会签态 | `approved`（`storage/POLICY/01-data-flow.md` frontmatter；本叶不翻签） |

## 查询限制

`metric-registry` MCP 未挂载，本叶没有调用 `metric-get`。下表公式来自在线结果板 `timeseries_board.py` 与批处理 `polan/basic/indicators.py` 文件头注释（该注释写明对照 seed）。未把 D1–D4 写成 8 件套，也未改 seed。

## 差异表

| 卡片 / 字段 | 批处理 `indicators.py`（seed 对照注释） | 在线结果板现在 | 本轮临时口径（总控 §0，已拍板） |
|---|---|---|---|
| 政策总数 | 全表 `is_deleted=0` 的条数，不是单产业切片 | `len(policies)`，集合来自关联表 | 保持在线切片：该 VID 有效关联行数。`M_POLICY_TOTAL_COUNT` |
| 政策密度指数 | `M_POLICY_TIMESERIES` 是各年 `publish_count` + `growth_rate` + `continuity_rate` 序列，没有「一个密度指数」 | headline `M_POLICY_TIMESERIES` = 跨度最后一年的发布条数 | 卡片改名为「最近一年发布量」，值仍是最后一年 `publish_count`。禁止再把这个数叫密度指数，也不再写入 headline 的 `M_POLICY_TIMESERIES` |
| 年度增长率 | `(本期-上期)/上期×100`；上期为 0 或空则为空 | 最近一个发布量 > 0 的年份相对上一日历年；上一年为 0 时已是空 | 与批处理相同。界面「—」，禁止显示 0 |
| 有效政策占比 | `status=1` 且（`expire_date` 空或 ≥ 今天）/ 总数 × 100 | 只要不是 0/失效/废止/无效就算有效，`status` 空也算有效 | 收紧到与批处理相同：仅 `status=1`（及字符串 `"1"`）且未过期 |
| 连续性 | 注释写「连续非空期数/总期数」；代码是累计有发布年数/已过年数 | 与批处理代码相同，不是连续段 | 本轮四张卡不含此项，不改 |
| 关联集合 | 批处理不按产业过滤 | `policy_industry_rel` 等值 | 保持。错配不在时序 SQL 里用标题滤掉 |
| 匹配对象 | 无 | 缺省为 VID | 有 `industry_name` 时用中文名 |

样本 `POLICY-20261024-005`（5 条、末年 2、增长率「—」、有效 100）与上表「在线结果板现在」一致：末年发布量被标成密度指数；增长率「—」是上一年为 0，不是丢字段；有效 100 是空状态也被算成有效。

## 下游约束

- B1 只改 `timeseries_board` / Job 读 `industry_name`。不改 `indicators.run()`。
- B2 只抽样校准抽取门槛。不重跑 2 万条。
- 不改 `M_POLICY_*` seed。

## 测试结果

- 无代码。对照阅读 `timeseries_board.py` headline / `is_valid` 与 `indicators.py` 第 9–11、120–141 行。

## 遗留风险

- 正式 8 件套未从 MCP 读出。若 seed 正文与 `indicators.py` 注释不一致，以 seed 为准，本叶不改口径。
- 密度指数的归一化定义仍未由甲方拍板。本轮用改名回避伪指数。

## CI/CD（必填）

- 分支：`gkx-orchestration` 本地，尚未提交
- commit：无
- pipeline：无业务 CI
- 部署：无
- dev URL：无

## 可观测性

- 无新埋点

## 涉及文件

- `agent-delivery/agent-handoffs/政策模块-E7/LUMEN-POLICY-TS-CALIBER-L01.md`
- `agent-delivery/agent-handoffs/政策模块-E7/LUMEN-POLICY-TS-长任务总控.md`

## 架构合规

| 铁律 | 结果 |
|------|------|
| 算法只在 Python | ✅ 本叶不写算法 |
| 不改 seed | ✅ |
| D9 | ✅ 不把临时卡片说成已对齐的密度指数 |

## cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 18000 |
| model_used | grok-4.7 |
| actual_cost | 未按价表计算（无 Console 分离值，价表无 grok-4.7） |
| cost_warn | green |
| 说明 | source: session_estimate。低于黄线。 |

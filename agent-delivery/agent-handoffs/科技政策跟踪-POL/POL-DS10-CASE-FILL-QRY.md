# POL-DS10-CASE-FILL-QRY · 多维检索查询合规演示用例填充

ponytail: N/A（文档）

## 任务认领

| 字段 | 值 |
|---|---|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 任务已是 in_progress。本会话不改 task-registry，不标 done |

## Ponytail

| 字段 | 值 |
|---|---|
| ponytail | `N/A`（文档） |
| 说明 | 只填本叶用例和本 handoff。未改业务仓，未改索引，未改另外三份用例 |

## 查了哪些表

查库时间 2026-11-07 16:09:26。主机 `10.50.11.76`，用户 `gkxlumenx`，取自 `lumen-algo-py/scripts/seed/seed_synth_elem.py` 缺省。口令只进本次进程，未打印，未写入文件。只读 SELECT，未 `--apply`。

展示实际读面（`lumen-svc-platform` 与它委托的 Python）：

| 用途 | 代码 | 库.表 | 本次结果 |
|---|---|---|---|
| 197、198、200 检索 | `PolicyPanoramaController.search` → `PolicyFacadeServiceImpl.search` → `polan.search.search_policies` | `demo_gkxlumenx_dwd.policy_base_info` | 未删除 20008 行。平面头未传，`apply_plane` 用 demo |
| 详情 | `PolicyPanoramaService.detail` → Python docs | 同上。目录有行，不读 `gapfill_policy_qry_doc` | 抽到 cn-gov-7067354 的 `title`、`content` 开头 |
| 统计 | `PolicyPanoramaService.stats` → Python indicators / metrics | `demo_gkxlumenx_ads.policy_level_dist` 等 5 张 | 行数都不为 0，不回退 `gapfill_policy_qry_stat`。197–202 的期望不引用统计卡 |
| 199 排序 | `PolicyPanoramaQueryController.rank` → `_load_rank_rows` | `gkxlumenx_gapfill.gapfill_policy_qry_rank` | relevance / timeliness / importance 各 6 行 |
| 201 历史 | `JdbcPolicyUserBehaviorStore.listHistory` | `gkxlumenx_topic_policy.policy_search_history` | 62 行。用户 184 最新 `id` 42 |
| 201 收藏 | `JdbcPolicyUserBehaviorStore.listFavorites` | `gkxlumenx_topic_policy.policy_favorite` | 3 行。用户 184 有 cn-gov-6999382、cn-gov-7067354 |
| 202 导出 | `PolicyFacadeServiceImpl.share` 只在写入时插 `policy_share_export`，GET 不读 | 表不存在 | 没有导出原文 |

对照未采用：`gkxlumenx_dwd.policy_base_info` 40000 行。展示默认平面不读这张。`gapfill_policy_qry_doc` 有 6 行标题，检索路径在目录有行时不读它；只用来对照名次表的 `policy_id`。

## 每条序号

| 序号 | 数据情况 | 输入 | 原句出处 |
|---|---|---|---|
| 197 | 可演 | 关键词「人工智能」，地区「深圳市」（请求 `region=深圳`） | `demo_gkxlumenx_dwd.policy_base_info`：`title`、`policy_id`、`publish_organization`、`publish_date`、`province`、`city`。`COUNT(*)` 8。首条 18358631 |
| 198 | 可演 | 关键词「固态电池」，部门「科技部」，年 2023 至 2023。不选状态「有效」 | 同上。`publish_organization`、`keywords`、`publish_year`、`title`、`policy_type`、`rank`。唯一行 cn-gov-5737584 |
| 199 | 可演 | 排序「相关性」，请求 `factor=relevance` | `gkxlumenx_gapfill.gapfill_policy_qry_rank`：`policy_id`、`rank_no`、`rank_dim`、`gap_item`。第一条 GF-POL-QRY-004，`gap_item`「无排序模型；只存名次，无分数」。同号标题在 `gapfill_policy_qry_doc.title` 为「深圳市科技创新促进条例」，rank 响应不带 title |
| 200 | 可演 | 效力级别「国家级」，二次筛选政策类型「意见」 | `demo_gkxlumenx_dwd.policy_base_info`：`rank` 等于明文「国家级」，`policy_type`「意见」，`title`、`publish_date`。2 行，首条 cn-gov-7041785 |
| 201 | 可演 | 已登录用户 184 | `policy_search_history.query_json`：`id` 42 为 `{"keyword":["电池"],"q":["电池"]}`。`policy_favorite.policy_id`：cn-gov-6999382、cn-gov-7067354。打开后者的标题与正文开头在 `policy_base_info.title`、`content` |
| 202 | 覆盖不到 | 导出 Excel | 契约资源 `panorama/share` 写明未见。`policy_share_export` 不存在。不把检索目录编成导出文件 |

契约里 199、201、202 曾标 501 或未见。199、201 这次库内有展示会读的行，所以记可演。202 仍然没有可展示的导出记录。D4 未改。

效力级别下拉送出的「国家级」只等于 `rank` 明文，命中 5 行。`rank` 为 `["国家级"]` 的 2174 行不会被这条等值条件命中。海外、政策类别「科创政策」、状态「有效」在该目录上的命中是 0，本用例不选这些值。

## 产物

- `agent-delivery/工程过程/04-系统集成/05-展示系统集成/合规演示用例/POL-L2-DS10-QRY-合规演示用例.md`
- 本 handoff

可演 5 行，覆盖不到 1 行，设计无资源 0 行。未改索引、未改其他用例、未改业务仓、未 commit、未 push。

## CI/CD

- 未 commit，未 push
- 未改业务仓，无 pipeline

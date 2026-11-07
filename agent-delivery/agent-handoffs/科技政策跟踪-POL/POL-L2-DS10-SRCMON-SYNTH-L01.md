# POL-L2-DS10-SRCMON-SYNTH-L01 · 立即同步改为 LLM 合成政策入库 + 产业补码 / 条款结构化

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:api-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |
| 说明 | 用户当次对话下达：删 540 条调试数据；「立即同步」改成 LLM 合成 50 条（全国随机、深圳居多、覆盖各类型），并调用已实现的产业抽取与条款结构化；中台政策 Mock 页加「Mock 50 条数据」「删除所有 Mock 数据」 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 复用 `polan.industry_enrich.enrich_one`、`polan.clause_job.structure_one` 与它们自带的写库函数，不重写算法。单飞只在进程内，已用 ponytail 注释标出上限。D9 MockBadge 保留，可观测沿用既有 Feign / entan-py 链路 |

## 决策与例外

- 落点：DWD `policy_base_info`，`source_plane='domestic'`。列表里真实行和合成行混排，检索和统计都计入。以上由用户在当次对话中选定。
- **D16 例外**：合成行直接写 DWD。`human:淮政玮` 于 2026-11-07 在对话中批准，只限本任务。
- 540 条调试数据（`source_plane='debug'`，`etl_batch_id='debug_one_map_20261107_v1'`），以及 ADS `policy_industry_rel` 里的 540 条 `DEBUG-ONEMAP%` 已删除。删除前的备份在 agent 本地 store，未进 git。删除后 DWD 剩 domestic 20007 条、global 1 条。

## 修改内容

- **lumen-algo-py**（`vendor/entan-py`）
  - 新增 `polan/mockgen/synth.py`：
    - 代码排配额：深圳约 60%（其中约 40% 是区级），国家级约 15%，其余随机落到 24 个省市；10 种政策类型、12 个主题轮转。
    - LLM 只写文字。每 5 条调用一次，并发 5 路。含禁用词、缺标题或缺正文的条目丢弃。
    - 写入 ODS `dwd_policy_base` + DWD `policy_base_info`，然后逐条调用 `enrich_one` 和 `structure_one`。
    - 三个标记：`SYN` 前缀、`source='llm-synth'`、`SYNTH-` 批次号。删除只按这三个标记执行。
    - 没有 LLM 密钥时直接返回 `failed`，不造行。
  - `polan/sync_history.py`：「立即同步」先写一条 `running` 历史，再在后台合成，结束后回写真实计数和说明。`running` 超过 30 分钟的自动标成 `failed`。同进程已有合成在跑时，不新开，返回 `已有同步在进行`。
  - `api/policy_routes.py`：新增 `POST|GET|DELETE /v1/policy/mock/synth`。
  - `polan/graph/entity.py`：从 demo 迁入 `_TITLE_STOP`、`title_match_tokens`，以及带 `title` 参数的 `match_industry_anchors`。之前 lumen 侧 `polan.industry_enrich` 因为缺这些符号导入失败。`split_anchor_tokens` 加了 `min_len` 参数，默认 3，产业向量索引的别名不变。
- **demo-algo-ent-analysis**：`polan/mockgen/synth.py` 与 lumen 同文；`api/policy_routes.py` 加同样的三条路由。
- **lumen-svc-platform**：element 的 `INGEST_SQL` 增加计算列 `(source = 'llm-synth') AS is_mock`。
- **lumen-ui-science-pc**（未推，待人工确认）：
  - `trendLive.ts`：入库行加 `isMock`；新增 `hasRunningSync` 和 `syncStatusTag`（running / success / partial / failed）。
  - `TrendTab.vue`：「立即同步」后每 4 秒轮询同步历史，没有 `running` 行后刷新入库列表；进入页面时若已有在跑的作业，也会接着轮询。合成行挂 MockBadge。顺手修了入库表标题列、状态列漏配 `slotName`，导致标题点不开详情、状态标签不生效的问题。
  - 自检 `FE-POL-TREND-LIVE.test.mjs` 补了对应断言。
- **每次条数 50 → 10**（2026-11-07 用户追加要求）：`synth.DEFAULT_COUNT=10`，立即同步与中台按钮同改；10 条恰好让 10 种政策类型每次各出现一次。
- **历史版本（2026-11-07 用户追加：「生成的10条中，随机5条，生成其历史版本」；用户选定 每次都做 / 旧版独立行 + 变更行 / 修新旧对比弹窗）**：
  - `synth.py`：入库和补码完成后，随机挑一半，每 5 条调一次 LLM 写上一版（标题、文号、摘要、关键词、分条正文、要点，以及 3～6 条 新增/修改/删除 变更）。旧版发布日由代码定，比新版早 365～1095 天。旧版作为独立行写 ODS/DWD：`policy_id` = 新版 id 加 `-H1`，`status=已废止`，三个合成标记不变，也跑补码和条款结构化。变更行写 `gkxlumenx_gapfill.gapfill_policy_version_diff`（`policy_id` 用新版，`fill_method=llm-synth`，`gap_item=213 政策新旧对比`，`is_mock=1`）。历史版写失败只记进 `errors`，不影响新版计数。返回值新增 `history_versions` 和 `diff_rows`。`delete_all` 增加删除变更行（按合成 `policy_id` 加 `fill_method=llm-synth`）。self_check 补了历史版断言。demo 仓同文。
  - element 新增 `GET /v1/element/policy/versions`：读 DWD 新版与 `-H1` 历史版成对的行，`policy_id` 可空，`limit` 默认 50、上限 200。display 新增 Feign、Service 和 `GET /display/v1/policy/panorama/versions`。element 单测补了一条。
  - lumen-ui-science-pc（未推，待人工确认）：`api/policy.ts` 加 `panoramaVersions`；`compareLive.ts` 加 `mapVersionPairs`；新增 `components/useVersionPairs.ts`，CompareTab 和 VersionCompareModal 共用。真实模式下，政策下拉只列有历史版的政策，两个时点就是旧版和新版的发布日，打开时预填但仍需点「查询对比」。不再借用其它政策的发布日当候选。
  - 文档：`CMP-DATA` 第 3 节（含 2026-11-07 变更段）、`CMP-API` 第 3 节和空态表、`CMP-ARCH` 第 3 节表格、流程第 3 步、5.1，以及 `TREND-ARCH` 4.1。
- **落地实效（2026-11-07 用户追加：「生成的10条中也要包含政策对应的落地实效相关的数据」；用户选定 组合方案、新旧版都给）**：
  - 现状：没有落地实效的 gapfill 表。落地实效是已有模型 `polan.eval.effect.run()` 按省级区域算出、写入 ADS `policy_effect`（`impl_effect`）和 `policy_metric_timeseries`（`M_POLICY_IMPLEMENTATION_EFFECT`）的，口径为「该省有效政策占比×100」。
  - `synth.py`：
    - 正文生成和旧版生成的提示词里加 `feedbacks`，每条政策 2～3 条受众反馈，不增加 LLM 调用。
    - `build_feedbacks` 过滤渠道（三选一）、禁用词，评分夹到 1～5，反馈时间由代码落在实施期内。
    - 反馈写 `gkxlumenx_gapfill.gapfill_policy_audience_feedback`（`fill_method=llm-synth`）。
    - 写完后调用一次 `effect.run()`。旧版加 `expire_date` = 新版发布日前一天，已有 `policy_open` 据此判它无效。没改共享函数，因为政策效果挂在合规展示台。
    - 返回值新增 `feedback_rows`、`effect_refreshed`。`delete_all` 增删反馈行，删完后重算一次。
    - 自检补了反馈和重算断言。demo 仓同文。
  - Java 与前端不改：209 读 `policy_effect`，210 读整张反馈表。
- **demo-ui-system-test**：政策 Mock 页加「Mock 10 条数据」（二次确认 → POST → 轮询 GET → 刷新列表）和「删除所有 Mock 数据（N）」（二次确认 → DELETE）两个按钮，API 写在 `src/api/policy/index.ts`。
- **设计文档**：
  - 签过字的分册不改原文，只在对应小节末尾追加「2026-11-07 变更」段：`l2/POL-L2-DS10-TREND-ARCH.md` 4.1 和 203 行、`TREND-DATA` 第 2 节、`TREND-API` 第 2 节、`TREND-METRIC` 6.1。
  - 索引类文档只改一行：说明书 203 行、`调用链与边界.md`、`契约输入清单.md`、`指标与501.md`、`QRY-ARCH`、`QRY-DATA`。

## 测试结果

- lumen-algo-py：
  - `pytest tests -k "industry or anchor or entity or graph or clause or policy"`：275 passed，2 skipped。
  - `tests/test_policy_sync_history.py`：6 passed，新增「拒绝第二次」用例。
  - `python -m polan.mockgen.synth`：self_check OK。
- 真实库冒烟（本机，用假 LLM 跑 3 条）：
  - ODS 和 DWD 各写入 3 条；条款结构化 3 条，ADS `policy_text_parse` 也是 3 行。
  - 产业补码 0 条。原因是本机连不上向量检索，`enrich_one` 按设计返回 `search_degraded`、不写入。
  - `delete_all` 删除 3 条主表、3 条 ODS、3 条 text_parse，删完剩余 0 条。上次失败遗留的 2 条 SYN 行也一并清掉了。
- element `INGEST_SQL` 在 10.50.11.76 上直接执行通过，`is_mock` 列返回 0/1。本机没有 Maven，没做编译，靠 CI 编译。
- lumen-ui-science-pc：`node FE-POL-TREND-LIVE.test.mjs` 全绿；`pnpm type-check` 退出码 0。
- demo-ui-system-test：`vue-tsc --noEmit` 对本次改的两个文件无报错（仓内其它文件原本就有类型错误）；本机没有 eslint 配置，未跑 lint。
- 历史版本：
  - `python -m polan.mockgen.synth` 在两个仓都 OK，`test_policy_sync_history.py` 6 passed。
  - 真实库冒烟：假 LLM 跑 4 条，生成历史版 2 条、变更行 4 条；成对 SQL 取出 2 对，旧版状态都是 `已废止`，两个日期都是 `YYYY-MM-DD` 字符串。之后只按该批次号清理（gapfill 4 行、DWD 6 行、ODS 6 行），库里原有 44 条合成行未动。
  - `FE-POL-CMP-LIVE.test.mjs` 全绿，`pnpm type-check` 退出码 0。element 本机无 Maven，靠 CI 编译。
- 落地实效：
  - 两个仓的 self_check OK，`test_policy_sync_history.py` 6 passed。
  - 真实库冒烟：假 LLM 跑 4 条，生成历史版 2 条、变更行 2 条、受众反馈 12 条，`effect.run()` 实际重算。旧版 `expire_date` 都早于新版发布日。之后只按批次号清理（反馈 12 行、变更 2 行、DWD 6 行、ODS 6 行），再重算一次，本批的影响消失。冒烟前的落地实效是 19:36 算的，当时没计入 21:10 入库的 44 条合成政策；现在库里的值已计入这 44 条。
- **未做**：线上真实 LLM 端到端（还没在 dev 上点「立即同步」）。

## 遗留风险

- **demo-platform-entan-py 没有 LLM 密钥**：K8s 上只查了环境变量名，没看值。lumen 的 `gkxlumen-platform-entan-py` 配了 `ENTAN_LLM_*` / `GKX_LLM_*`、`EMBED_*`、`MILVUS_*`。demo 的 `demo-platform-entan-py` 只有 `EMBED_*` 和 `MILVUS_*`。中台 Mock 页如果走 demo pod，会返回「未配置 LLM 密钥，未生成」。补密钥需要人来决定（Secret 或 CI 变量）。
- 单飞只在单个进程内：lumen 和 demo 两个 pod、或多副本时，可能同时各跑一批。删除操作会拒绝在本进程合成进行时执行，但拦不住其它进程正在进行的合成。
- 合成行计入检索和统计后，205/206 的数值会变；相关指标 D4 仍是 mock。
- 历史版本已有的 44 条合成行没有补做（只对之后新合成的生效）。手工灌的 5 条 `CMP-GAPFILL` 变更行，对应政策在 DWD 里没有 `-H1` 行，所以不会出现在真实模式的新旧对比下拉里。
- 每次合成多一次 LLM 调用（5 条一组），耗时约增加三分之一。
- 落地实效是省级的，按「有效政策占比」算。真实政策 20008 条状态为空（判为无效），只有 584 条为「有效」，所以各省值普遍很低（广东约 26，多数省 0～2）。合成政策状态都是「有效」，会把所在省的值往上推。国家级合成政策没有省份，不计入。
- `effect.run()` 每次全量重算全部区域。合成与删除会改写 209 的数值，D4 仍是 mock。
- 跳板机 `/tmp/admin-kc.yaml` 是别的会话留下的 root 属主文件，本会话无权删除，需要有权限的人清理。

## CI/CD（必填）

- 分支：`origin/dev`
- commit：
  - lumen-algo-py `fed2815`（merge `b326c6e`）
  - demo-algo-ent-analysis `17f277d`（merge `15a0929`）
  - lumen-svc-platform `6f84f35`
  - lumen-ui-science-pc `85ba93c`、demo-ui-system-test `5f29754`（2026-11-07 `human:淮政玮` 确认「推」后推送）
- pipeline / rollout：未查看，push 后由 CI 自动触发。
- dev 验证：待 rollout 后在展示系统「政策动向跟踪 → 立即同步」实测。

## 可观测性（建议）

- 沿用 `gkxlumen-platform-entan-py` 既有 instrument；后台线程里的写库不挂请求 span（HTTP 先返回）。

## 涉及文件

- `repos/lumen-algo-py/vendor/entan-py/polan/mockgen/synth.py`（新）
- `repos/lumen-algo-py/vendor/entan-py/polan/sync_history.py`
- `repos/lumen-algo-py/vendor/entan-py/polan/graph/entity.py`
- `repos/lumen-algo-py/vendor/entan-py/api/policy_routes.py`
- `repos/lumen-algo-py/tests/test_policy_sync_history.py`
- `repos/demo-algo-ent-analysis/polan/mockgen/synth.py`（新）
- `repos/demo-algo-ent-analysis/api/policy_routes.py`
- `repos/lumen-svc-platform/gkxlumen-element/.../PolicyGapfillController.java`
- `repos/lumen-ui-science-pc/src/views/policy/panorama/{trendLive.ts,components/TrendTab.vue,FE-POL-TREND-LIVE.test.mjs}`
- `repos/demo-ui-system-test/src/{api/policy/index.ts,views/policy/pages/PolicyMockPage.vue}`
- `agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/**`（上列 10 份）

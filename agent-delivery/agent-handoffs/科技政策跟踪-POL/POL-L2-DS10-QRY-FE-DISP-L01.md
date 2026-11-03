# POL-L2-DS10-QRY-FE-DISP-L01 · 展示政策检索接上排序、收藏与导出

ponytail: full

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `human:淮政玮` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch`。开工时已是 `in_progress` |
| 说明 | 本会话不改 task-registry，不把任务标成 done。用户授权提交并推送 `origin/dev` |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 只在现有政策检索页挂展示门面。未另开页，未改专题前端、Java、Python、网关和图。未新造 metric_id，未改 D4。未用 YAGNI 跳过已有请求客户端、空响应诚实空列表和 Mock 开关 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | `POL-L2-DS10-QRY-ARCH` |
| 图 diff | 未改图。浏览器仍只打 `/display/v1/policy/panorama/**` |
| 会签态 | 架构稿记 `draft`（源文件无 frontmatter） |
| 说明 | 图文冲突以图为准。本单没有改去打 `/policy/topic/v1/policy` 或 `/topic/v1/policy` |

## 范围与实现

页面仍是展示系统 `/display/policy/panorama`（`src/views/policy/panorama/index.vue`）。布局、主色和组件视觉未改。`USE_MOCK=true` 时目录仍走本机 `queryEngine`，收藏仍走 localStorage，导出仍走本机 xlsx / 打印窗。`USE_MOCK=false` 时政策检索只打展示门面。

1. **目录与详情**  
   检索条件经 `GET /display/v1/policy/panorama/search`。打开检索结果走 `GET /display/v1/policy/panorama/{id}/detail`。空列表保持空，不用 `policySeed` 填。详情没有正文、条款或强度分时显示空，不补种子全文。

2. **智能排序**（已有结果时下拉可用）  
   `USE_MOCK=false` 的下拉只有默认、相关性 `relevance`、时效性 `timeliness`、重要性 `importance`。默认用当次 search 顺序。后三项 `GET /display/v1/policy/panorama/rank`，query 带 `factor` 和当次检索条件。按返回 `policy_id` 重排当前卡片，不渲染 `smartScore`。名次为空或 `honesty.empty` 时保留已经显示的目录，并提示「该排序暂无名次」。下拉不含发布时间、效力级别、浏览量。

3. **检索历史与收藏**  
   数据只来自 favorites 系列。空则空。检索成功后 `POST /display/v1/policy/panorama/favorites/history`，体是当次查询条件，不传 `user_id`。点历史：`POST /display/v1/policy/panorama/favorites/history/{id}/search`，用返回目录替换当前结果。收藏：`POST /display/v1/policy/panorama/favorites`，体里 `policy_id`。打开收藏：`GET /display/v1/policy/panorama/favorites/{policyId}`，进已有详情。匿名或 honesty 含 `unavailable:anonymous` 时提示请先登录，不造假收藏。没有取消收藏接口，本页不在本地删掉服务端收藏行。

4. **导出与分享**  
   `GET /display/v1/policy/panorama/share`，带当次检索条件，`format=excel|pdf`，`channel=link`。页面只展示返回的 `share_url` 和 honesty 说明。邮件不可用时写明不发信。响应没有文件字节就不声称已下载。目录为空不生成空文件，也不调用本机 `exportPoliciesExcel` / `exportPoliciesPdf`。

动向、舆情、比对、订阅的数据源未改。`seedInboxItems` 未改。治理、解析、仿真、比对数据集的 `contractPending` 未改。

## 偏离

- 高级检索里的 NOT 没有独立查询参数。`USE_MOCK=false` 时不在浏览器里用种子集求 NOT，只把正向条件交给 `search`。
- 二次筛选的类型和地域进入 `search`。日期区间仍在当次目录上按字符串收窄，不另造名单。
- 未传 `limit`。目录长度以 `search` 响应为准。
- 指标卡上的落地实效 `92.5` 和覆盖地区 `32` 是原页写死的数。本单不改布局，也没有改去打 `stats`。
- rebase 时保留了同日走查 `ba44ef1` 的指标行置顶和弹层关闭。收藏数字在 `USE_MOCK=false` 时改为服务端条数。

## 产物清单

`lumen-ui-science-pc` `origin/dev` `b35f87af492142e0275118d48ebc599882810cf0`

- `src/api/policy.ts`
- `src/views/policy/panorama/index.vue`
- `src/views/policy/panorama/components/ShareModal.vue`
- `src/views/policy/panorama/components/PolicyContentDetailDrawer.vue`
- `src/views/policy/panorama/search/displaySearchResultUtils.ts`
- `src/views/policy/panorama/search/displayPanoramaQuery.ts`
- `src/views/policy/panorama/search/displayPanoramaQuery.selfcheck.mjs`
- 本 handoff

## 测试结果

- `node src/views/policy/panorama/search/displayPanoramaQuery.selfcheck.mjs`：通过。覆盖 factor 映射、名次为空不清空已有目录、收藏空列表不造数、匿名不展示假收藏、`USE_MOCK=false` 不走本机文件生成。
- `node src/views/policy/panorama/FE-POL-01A.test.mjs`：通过。
- `pnpm exec vue-tsc --build`：退出码 0。未执行 `pnpm install`。
- 未在浏览器点选检索、排序、收藏、导出和分享。

## 遗留风险

专题门面收藏和导出仍可能解不出用户，返回匿名空列表。前端只展示空和「请先登录」，不回退 localStorage 或种子。分享响应只有链接时，本页不下文件。排序不依赖用户，但仍要网关和登录令牌转发后才能看到实包目录。

## CI/CD

- 分支：`lumen-ui-science-pc` `origin/dev`
- commit：`b35f87a` `feat(policy): 关闭 Mock 时政策检索改走展示全景门面 [agent:frontend-agent]`
- push：已推到 `origin/dev`（`b4a5f4c..b35f87a`）
- 本 handoff 在 `gkx-orchestration` `origin/dev`
- 本会话未查 Pipeline，未做 rollout

## 架构合规自检

- 调用链：`USE_MOCK=false` 时政策检索只打 `/display/v1/policy/panorama`，不直连 Python，不打 `/policy/topic/v1/policy` 或 `/topic/v1/policy`
- D9：未新造 metric_id，未改 D4
- D12：展示前端只经已有网关前缀
- 可观测：沿用现有 request 的 `X-Trace-Id`，未另加埋点包

## 未改动的页面

政策动向跟踪、政策舆情评估、政策重点比对、订阅中心的数据源未改。治理、解析、仿真、分析、比对数据集接口仍是契约占位。专题仓 `lumen-ui-topic` 未改。

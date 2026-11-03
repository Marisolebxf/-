# POL-L2-DS10-QRY-FE-L01 · 专题政策查询页接上排序、收藏与导出

ponytail: full

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `human:淮政玮` |
| supervised_by | `human:淮政玮` |
| claim_type | 任务已是 in_progress。本会话不改 task-registry，不把任务标成 done |
| 说明 | 用户授权提交并推送 `origin/dev` |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 只在现有政策查询页挂已有门面。未另开页，未改展示系统、Java、Python，未新造 metric_id，未改 D4 |

## 范围与实现

页面仍是专题系统 `/policy/search`（`src/views/policy/PolicySearchPage.vue`）。检索框仍是原来的 SearchHub。三块都走已有网关前缀 `/policy/topic/v1/policy`。

1. **智能排序**（已有结果时出现）  
   `a-select`：默认、相关性 `relevance`、时效性 `timeliness`、重要性 `importance`。默认仍用当次 search 顺序。后三项 `GET /policy/topic/v1/policy/rank`，query 带 `factor` 和当次检索条件。按返回的 `policy_id` 重排当前卡片，不渲染 `smartScore`。名次为空或 `honesty.empty` 时保留已经显示的目录，并提示「该排序暂无名次」。下拉不含发布时间、效力级别、浏览量。

2. **检索历史与收藏**  
   页上按钮「检索历史」「收藏」，数据只来自 `GET /policy/topic/v1/policy/favorites`。空则空。检索成功后 `POST /policy/topic/v1/policy/favorites/history`，体是当次查询条件，不传 `user_id`。点历史：`POST /policy/topic/v1/policy/favorites/history/{id}/search`，用返回目录替换当前结果。结果卡「收藏」：`POST /policy/topic/v1/policy/favorites`，体里 `policy_id`。打开收藏：`GET /policy/topic/v1/policy/favorites/{policyId}`，进已有详情抽屉。匿名或 honesty 含 `unavailable:anonymous` 时提示请先登录，不造假收藏。原「最近检索」芯片仍走 localStorage，没有改名为检索历史。

3. **导出与分享**（已有结果时出现）  
   按钮：导出 Excel、导出 PDF、复制分享链接。`GET /policy/topic/v1/policy/share`，带当次检索条件，`format=excel|pdf`，`channel=link`。页面只展示返回的 `share_url` 和 honesty 说明。邮件不可用时写明不发信。响应没有文件字节就不声称已下载。目录为空不生成空文件。

`USE_MOCK` 下这三块的 mock 返回空列表、空收藏、空文件，不用 fixture 填数。

## 偏离

无。未改展示系统，未改 Java，未改 Python。

## 产物清单

`lumen-ui-topic` `origin/dev` `669c09887d2a19b38565c16c692c99f724b8778c`

- `src/api/policy/paths.ts`
- `src/api/policy/types.ts`
- `src/api/policy/index.ts`
- `src/views/policy/policySearchModel.ts`
- `src/views/policy/policySearchModel.selfcheck.mjs`
- `src/views/policy/PolicySearchPage.vue`
- `src/mock/policy/policyApi.ts`
- `src/mock/register.ts`
- 本 handoff

## 测试结果

- `node src/views/policy/policySearchModel.selfcheck.mjs`：通过。覆盖 factor 映射、名次为空不清空已有目录、收藏空列表不造数、匿名不展示假收藏。
- `vue-tsc --build`：退出码 0。
- `pnpm type-check` 未跑完：该命令先执行 pnpm install，因 core-js / es5-ext 的 ignored builds 退出。锁文件改动已还原，未进入提交。
- 未在浏览器点选这三块。本地 `VITE_APP_USE_MOCK=false`，页面要网关和登录后才能看到实包目录。

## 遗留风险

排序、收藏、导出依赖已登录用户和门面实包。匿名时页面提示请先登录，列表保持空。分享响应只有链接，本页不下文件。

## CI/CD

- 分支：`lumen-ui-topic` `origin/dev`
- commit：`669c098` `feat(policy): 专题查询页接上排序收藏与导出 [agent:frontend-agent]`
- push：已推到 `origin/dev`（`cd943ab..669c098`）
- 本 handoff 在 `gkx-orchestration` `origin/dev`
- 本会话未查 Pipeline

## 架构合规自检

- 调用链：只打 `/policy/topic/v1/policy`，不直连 Python，不打 `/display/v1/policy`
- D9：未新造 metric_id，未改 D4
- D12：专题前端只经已有政策门面前缀
- 可观测：沿用现有 request 的 trace，未另加埋点包

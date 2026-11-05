# POL-L2-DS12-EST-TEST-L01 · 政策效果推演 · 效果预估 · 集成测试

- 任务：`POL-L2-DS12-EST-TEST-L01`（WBS 行 `WBS-05-23-L2-08F`）
- 日期：2026-11-06
- 监管：`human:淮政玮`
- 执行：`agent:qa-agent`
- 认领：任务已是 `claimed_by=supervised_by=human:淮政玮`，状态 `in_progress`。本轮不改 task-registry，不把任务标成 done
- 用户故事：`US-DS-POL-06`
- 上游：`sdd/l2/POL-L2-DS12-EST-API.md`、`sdd/l2/POL-L2-DS12-EST-DATA.md`

## 任务认领

| 字段 | 值 |
|---|---|
| claimed_by | `human:淮政玮` |
| supervised_by | `human:淮政玮` |
| claim_type | 注册表已由淮政玮认领并处于 `in_progress`。本会话不改状态 |
| 说明 | 执行角色 `agent:qa-agent`。不 commit，不 push |

## Ponytail

| 字段 | 值 |
|---|---|
| ponytail | `full` |
| 说明 | 用例只覆盖 SRS 232–236。数据准备复用已有灌数脚本，不另写第二套 SQL。测不到的接口不记通过 |

ponytail: full

## 范围与实现

对效果预估五叶做集成测试设计和能测则测：

1. 用例：`agent-delivery/工程过程/04-系统集成/05-展示系统集成/测试用例/POL-L2-DS12-EST-TEST-L01.md`
2. 截图 11 张：同目录 `测试用例/POL-L2-DS12-EST-TEST-L01/`
3. 数据：`python scripts/seed_gapfill_policy_sim_forecast.py --check` 退出码 0，预期 6 行。环境没有 `LUMEN_ALGO_MYSQL_PASSWORD`，未执行 `--apply`

未改 lumen 业务仓代码。`--check` 覆写的 SQL 与仓内已有文件一致，git 无新差异。

## 测试结果

| 项 | 结果 |
|---|---|
| `--check` | 通过。`gapfill_policy_sim_forecast` 6 行：未出台仿真 2、新出台预测 2、区域空间 2。`policy_id` 为 `18363390`、`18407696`。无全国行。`is_mock=1`。SQL 不写 ODS/DWD/ADS |
| `--apply` | **未执行** |
| 条件不齐不发请求 | 本机已测到。四参数全空、新出台无编号、区域无名称都不 POST |
| 请求体收口 | 已测到。未出台只带已填项；新出台只带 `policy_id`；区域无类型时不传 `policy_type`，选了才传；多维评估与利益攸关方只传 `kind` |
| 意见不写回 | 已测到。提示「意见留在本页，未写入接口」，jobs body 不含意见正文 |
| 「利益低关方」 | 页面与灌数 SQL 都没有这五个字 |
| HTTP 成功且 records 空、不返回 501 | **未测到**。线上带登录为 HTTP 404，`path=/v1/policy/simulation/jobs`。本机代理为 HTTP 401「访问令牌不存在」，随后若干次 XHR status 0。响应里没有 501，也没有把 6 行读回来 |
| 界面 | `USE_MOCK=false` 的本机页按步截了空态。没有用 fixture 把五叶填成有数 |

## 偏离

| 偏离 | 说明 |
|---|---|
| 未灌库 | 进程环境没有库口令。预期 SQL 与 6 行口径写在用例 DP-02、DP-03，未连库执行 |
| 接口成功空列表 | 线上 display 没有这条映射（404）。不把页面空文案记成 200 空列表 |
| 截图环境 | 图来自本机 `http://127.0.0.1:3000`，地址带 `review=1`，页头有「演示数据」。五叶结果区仍是真轨空态。线上页登录后见过同一空文案，页签随后被切走，未把那次画面留成最终截图 |
| 页头四个数字 | 86.5 / 78 / 7 / 3 不是本五叶 jobs 的 records。用例 OBS-01 |

## 产物清单

| 产物 | 路径 |
|---|---|
| 测试用例 | `agent-delivery/工程过程/04-系统集成/05-展示系统集成/测试用例/POL-L2-DS12-EST-TEST-L01.md` |
| 截图 11 张 | `agent-delivery/工程过程/04-系统集成/05-展示系统集成/测试用例/POL-L2-DS12-EST-TEST-L01/` |
| 本 handoff | `agent-delivery/agent-handoffs/科技政策跟踪-POL/POL-L2-DS12-EST-TEST-L01.md` |
| 代码改动 | 无 |

## 架构合规自检

| 铁律 | 结果 |
|---|---|
| 调用链 前端 → Java，不直连 Python | ✅ 用例只打 `/display/v1/policy/simulation/jobs` |
| 五叶同步读、不建任务 | ✅ 请求体按此断言；线上 404 说明当前进程还没挂上这条映射 |
| D16 只写 gapfill | ✅ 脚本目标只有 `gkxlumenx_gapfill.gapfill_policy_sim_forecast`。本轮未执行写入 |
| 不写 ODS/DWD/ADS | ✅ |
| 空态不伪闭合 | ✅ 未把 401/404 记成有数，也未用 fixture 截出有数 |
| 不改 lumen 代码、不 commit、不 push | ✅ |

## Cost

| 字段 | 值 |
|---|---|
| actual_tokens | 110000 |
| model_used | grok-4.7 |
| actual_cost | 0.55 |
| cost_warn | green |

估算，按同目录近期 handoff 的 grok-4.7 单价（约 40000 token = 0.20 美元）折算。未回写注册表。

## CI/CD

- 分支：未提交，未推送
- commit：无
- pipeline：无
- 部署：无。未改业务仓

## 遗留

1. 有 `LUMEN_ALGO_MYSQL_PASSWORD` 后再 `--apply`，并用用例 DP-03 的 SQL 核对 6 行
2. display 发布含 `POST /v1/policy/simulation/jobs` 之后，复测 TC-API-11：空与未知 kind 应为 HTTP 成功、records 空、不返回 501；灌库后 232–234 对得上的请求应返回对应行
3. 本机 `VITE_ENABLE_MOCK_AUTH=true` 且 `USE_MOCK=false` 时请求不带登录令牌，打到网关是 401。复测成功空列表要用已登录的线上或会转发令牌的环境

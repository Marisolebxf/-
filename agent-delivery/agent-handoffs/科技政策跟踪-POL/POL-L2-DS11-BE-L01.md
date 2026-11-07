# POL-L2-DS11-BE-L01 · DS11 评价页后端读面与白名单接线 · handoff

- 任务：`POL-L2-DS11-BE-L01`（feature，P1，监管人 `human:淮政玮`）
- 执行：`agent:cursor-orchestrator`（2026-11-08 接手在办单，用户授权自主推进/推送/部署）
- 仓：`lumen-svc-platform`，分支 `dev`
- 强度：ponytail full

## 范围与实现

首轮演示样本 LOOP（§6.5，2026-11-08）暴露 4 笔 QUERY 缺口，本单修复并二轮复测全部通过：

| 缺口 | 根因 | 修复 | commit |
|---|---|---|---|
| 224/225 shells 空列表（BUG-01） | element `SHELL_SQL` 选 DATA 分册旧列名 `topic_or_metric`/`caption`，真表为 `subject_name`/`caption_text`，SQL 撞 Unknown column 被吞成空列表 | 列名对齐线上真表（灌数脚本 `seed_gapfill_policy_eval_shell` 为准） | `0a6b0d9` |
| 222 模板选用空列表（GAP-01） | 无 kind=模板选用 分支、无模板表读面；`shells` 只绑 `scheme_name`，用例契约键 `template` 落不进 | element 新增 `/evaluation/template` 只读 `gapfill_policy_eval_template`；display shells 增 kind 路由并绑 `template` 参数 | `0a6b0d9` + `e0ede48` |
| 226 误建异步任务 | jobs 对 `policy_text_parse` 走 `asyncClient.create`，触发异步链（契约红线：`parse.run` 会清空整张 `ads.policy_text_parse`） | 改走 element `simulation?kind=文本解析` 同步只读 ADS summary；element 侧支持无 policy_id 全表读 | `0a6b0d9` |
| 230/231 空列表 | 本地代码（11-03 `e8471c0` 已含互动意见/方案报告分支）未部署 | 随 `0a6b0d9` 部署自然生效，无额外改动 | — |

## 产物

- `lumen-svc-platform` commit：`0a6b0d9`（6 文件）、`e0ede48`（2 文件），均推 `origin/dev`
- 测试：`PolicyGapfillEvaluationTest`（壳表列名断言 + 模板端点用例）、`PolicyEvaluationServiceTest`（模板路由 + 226 只读不建任务断言）
- CI/部署：element digest 镜像 `0a6b0d95`、display digest `c2ed4dc0` 均 rollout 绿（K8s dev，ns `zhipu-tts`）

## 验收证据（二轮网关全链路，2026-11-08）

- 222：模板「区域政策效果季度对比」2 行（季度/地区/柱状、季度/地区/热力）✅
- 224/225：7 行（解读 4 + 多媒体 3）✅
- 226：同步只读 20125 行 summary，无 taskId、无任务创建 ✅
- 230：3 条意见行 ✅；231：records 1 + opinions 3 ✅
- 首轮已过项（219/220/223/227/228/229）未回归
- 三验收 handoff：`POL-L2-DS11-{VIZ,READ,PLAN}-DEMO-ACCEPT-LOOP.md` 第二轮运行记录

## 架构合规自检

- 调用链：前端 → gateway → display → element（@Inner + @NoToken 配对）→ gkxlumenx_gapfill / ads 只读 ✅
- display 不直连 Python、不直连库 ✅（226 改经 element，比旧链路更合规）
- 无行则空、不造 0、不返回 501 ✅（模板名不在表内返回空，不生成文件）
- 不新造 metric_id、不改 D4 ✅
- Java 不写算法、不打分 ✅

ponytail: 226 选择经 element 复用既有 `simulation` 读面而非新建端点——两处（按 policy 读、全表读）已收敛在一个 SQL 常量上；若后续摘要需要过滤参数，再拆独立端点。

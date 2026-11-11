# POL-FACTOR-GAPFILL-L01 · 政策详情「支持强度构成」四维灌数（全链）

> 来源：用户看板截图——政策内容详情抽屉「支持强度构成（资金/税收/土地/人才）」四格恒显「—」。
> 用户裁定：走 D16 gapfill mock 灌数，中台仿「条款结构化」形式直接灌，需新建 gapfill 表。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm-agent`（Python/seed）+ `agent:frontend-agent`（中台页/详情透传） |
| supervised_by | `human:淮政玮`（当前会话用户） |
| claim_type | `pull`（用户当会话直接派单 self-claim） |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 复用 `ClausePage.vue`/`clause_job.py` 既有范式，未新造框架；D9 诚实性（不伪闭合、全维 NULL 不落行）完整保留；无新依赖。 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | SVC-STORAGE-FLOW（无图改动：只新增 gapfill 表读写边，链路仍是 前端→display→element→MySQL） |
| 图 diff | 新增读边：element 读 `gkxlumenx_gapfill.gapfill_policy_support_factors`；新增写边：Python polan 灌数 → 同表 |
| 会签态 | draft（无架构变更，不触发会签） |

## 问题清单

- 抽屉 `PolicyContentDetailDrawer.vue` 读 `policy.factors.{fund,tax,land,talent}`，但 live 链路 `mapSearchItem` 把 `doc.factors` 丢了 → 前端恒「—」（本叶修）。
- `M_POLICY_INTENSITY_SCORE` 官方口径=三维五项，与四维展示完全是两件事；四维属 QPOL-02 Wave 0 mock 指标，不得占用正式 metric_id → 行内 `metric_id=NULL`。

## 修改内容

**Python（lumen-algo-py，已推 dev，merge 97f352b）**
- `vendor/entan-py/polan/factors_gapfill.py`：表 DDL/upsert/读取 + 关键词规则打分（每维命中一处 +20 封顶 100；全维 NULL 返回 NULL 不写 0）+ `run_check()` 自检。
- `vendor/entan-py/polan/factors_job.py`：按钮 enrich（≤20 条）+ 后台跑批（对标 clause_job：单飞拒绝、游标续跑、max_count、batch_size 缺省 1000）；LLM 兜底仅 force 且全维 NULL 时调，模型只判维度（分值固定 60），无密钥/抽空跳过不写假值。
- `vendor/entan-py/api/policy_factor_routes.py` + `main.py`：`POST /v1/policy/factors/enrich`、`POST /v1/policy/factors/jobs`（轮询带 job_id）。
- `scripts/mysql/gapfill_policy_factors.sql`：DDL（CREATE IF NOT EXISTS 幂等）。
- `scripts/seed/seed_gapfill_policy_factors.py`：`--check` 断言自检（绿）/ `--apply` 建表+按规则灌演示政策（缺省最新 20 条，`--policy-ids` 指定；全维 NULL 不落行）。

**Java（lumen-svc-platform，本地不编译，按用户裁定交 CI）**
- `gkxlumen-element` `PolicyGapfillController`：`@Inner GET /v1/element/policy/support-factors?policy_id=`（只读 gapfill 表，`LIMIT 1`）。
- `gkxlumen-display` `RemoteElementClient` + `PolicyPanoramaService.detail()`：detail 响应 `attachFactors` 把 `{fund,tax,land,talent,is_mock,fill_method,…}` 贴进 `doc.factors`。

**中台前端（demo-ui-system-test，本地 commit 未 push，待人工确认推送）**
- `src/views/policy/pages/FactorsPage.vue`：对标 `ClausePage.vue` 全套交互（policy_id 逗号多条、抽取力度分按钮、增量/全量、force、最大数量、每批条数、续跑、进度行、结果表四维 tag/未命中显 —）；SeedHelpBadge 说明含 D16/🧪 口径。
- `src/api/policy/index.ts`：`structurePolicyFactors` / `structurePolicyFactorJob` / `pollPolicyFactorJob`。
- `src/router/index.ts` + `policyMenuConfig.ts`：`/policy/factors` 「支持强度构成」注册（条款结构化之后）。

**展示前端（lumen-ui-science-pc，本地 commit 未 push，待人工确认推送）**
- `src/views/policy/panorama/search/displayPanoramaQuery.ts`：`mapSearchItem` 透传 `item.factors`（对象形状才收，同 `clauses` 一行），修 live 详情四维恒「—」。
- `displayPanoramaQuery.selfcheck.mjs`：补 2 条 factors 透传断言。

## 测试结果

- Python `run_check()` 绿（关键词边界/计分封顶/全 NULL）。
- 跑批引擎内联自测绿：两页游标续跑（cursor=`B`）、processed/coded/skipped 计数、job_id 轮询快照、单飞第二份 rejected。
- seed `--check` 绿（四维关键词 8/6/6/6 条，边界用例全过）。
- 中台 `pnpm build` 绿（本仓无 type-check/lint 脚本，build 即门禁）。
- 展示前端 `node --experimental-strip-types displayPanoramaQuery.selfcheck.mjs` 绿。
- Java：本地不编译（用户裁定「java本地禁用的」「不需要本地编译Java」），语法走人工 review，编译由 CI。

## 遗留风险

- gapfill 表与 seed 尚未在演示库执行（需 `LUMEN_ALGO_MYSQL_PASSWORD`，--apply 或中台页面任一通道）。
- Java 两服务未部署前，detail 的 `factors` 仍缺 → 抽屉仍显「—」（等待 CI rollout）。
- 关键词规则是朴素启发式（`ponytail:` 已在代码内标注天花板），QPOL-02 甲方归一时可能换 LLM/结构化抽取，届时只改 `FACTOR_KEYWORDS` 或 `score_one` 兜底分支。

## CI/CD（必填）

- 分支：lumen-algo-py `dev`（已推）；demo-ui-system-test / lumen-ui-science-pc `dev`（本地 commit，待人工确认推送）
- commit：algo-py merge `97f352b`（含 `[agent:algorithm]` 两个功能 commit）；中台 `[agent:frontend] FactorsPage`；展示 `[agent:frontend] factors 透传`
- pipeline URL / ID：algo-py CI 触发后看 GitLab pipeline（devops Phase A path-based 增量）
- 部署 namespace / 镜像 tag：CI 自动（algo-py api）；Java 两服务随 svc-platform CI
- K8s rollout：待 CI
- dev 测试 URL / 命令与结果：中台 `/policy/factors` 页面按钮灌数 → 全景详情抽屉看四维

## 可观测性（建议）

- OTEL_SERVICE_NAME：gkxlumen-element / gkxlumen-display（沿用现有 Agent，无新增埋点面）
- traceId（dev 抽样）：灌数后打开详情抽屉抽一条

## 涉及文件

见上文「修改内容」逐仓清单。

## 客户决策联动

- QPOL-02 增补一行 Wave 0 mock 口径说明（四维 keyword 规则 + D16 gapfill + 🧪 不摘），正式权重/口径仍待甲方归一。

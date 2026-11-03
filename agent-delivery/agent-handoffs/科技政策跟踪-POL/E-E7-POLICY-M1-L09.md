# E-E7-POLICY-M1-L09 · 专题政策门面 · 检索历史与收藏

| 字段 | 值 |
|---|---|
| claimed_by | agent:api-agent |
| supervised_by | human:淮政玮 |
| 状态 | 代码与 handoff 已落本地。未 commit，未 push，未改 task-registry，未标 done |
| ponytail | full |

展示侧 `GET /display/v1/policy/panorama/favorites` 只委托本门面 `GET /topic/v1/policy/favorites`。浏览器仍打展示路径。本单不改 `gkxlumen-display`，也不新建展示侧用户表。

## 范围与实现

历史和收藏是登录用户的行为记录，不是指标。身份取现有鉴权 `SecurityUtils.getUser().getId()`，忽略请求体里的 `user_id`。没有记录时两个列表都是空数组，不造收藏，不把 localStorage 当实现。

门面基路径 `/topic/v1/policy`。下列入口都写在 `GET /{id}` 之前，避免被详情兜底吃掉：

| 方法 | 路径 | 行为 |
|---|---|---|
| GET | `/topic/v1/policy/favorites` | 当前用户的 `history` 与 `favorites` |
| POST | `/topic/v1/policy/favorites/history` | 只存检索条件 |
| POST | `/topic/v1/policy/favorites/history/{id}/search` | 用已存条件调用已有 `search` |
| POST | `/topic/v1/policy/favorites` | 只存政策 id |
| GET | `/topic/v1/policy/favorites/{policyId}` | 确认是本人收藏后调用已有 `docs/{id}` |

历史表只留用户和检索条件（另有主键，用来点名再执行哪一条）。收藏表主键就是用户和政策 id。不存目录快照，不存 `search_time` / `create_time`。请求体里的 `items` 这类结果对象不写入历史。再次执行不另查一份目录；打开收藏不另写详情查询。

库地址未配置或写不进库时返回空列表或空 item，`honesty.fabricated=false`。不写 ADS。

## 偏离

- 数据分册第 7 节声明本叶不写 DDL，且不把未签收 SQL 当作用数表。本单是实现单，按该节收成两张行为表，放在独立库 `gkxlumenx_topic_policy`，因为 ADS 会话只读。这不是派单包 17 的统计表。
- 展示公开资源仍只有那一条 GET。写入和「再执行 / 打开」留在门面。展示接通前，display 仍可能 501；接通后应只委托上面的 GET，没有记录时由本入口返回空列表，不再 501。
- JDBC 每次新开连接，无池。库地址空则不连。升级路径：并进已有 Druid，且不要拿掉 ADS 的 READ ONLY。列表最多返回 20 条历史、100 条收藏，更早的行仍在表里。

## 产物清单

- `repos/lumen-svc-platform/db/9x_gkxlumenx_topic_policy.sql`
- `gkxlumen-topic-policy-biz`：`PolicyFacadeController`（历史与收藏入口，位于 `/{id}` 之前）、`PolicyFacadeService` / `PolicyFacadeServiceImpl`（只追加或修正 favorites/history）、`PolicyUserBehaviorStore`、`JdbcPolicyUserBehaviorStore`
- 测试：`PolicyFacadeControllerTest`、`PolicyFacadeServiceImplTest`
- 未改 `lumen-algo-py`，未删 rank、share、search、docs、metrics

## 验收证据

只跑了改到的两个测试类，未跑全仓：

`mvn -pl gkxlumen-topic-policy/gkxlumen-topic-policy-biz -am test -Dtest=PolicyFacadeControllerTest,PolicyFacadeServiceImplTest`

- `PolicyFacadeControllerTest`：Tests run: 18, Failures: 0, Errors: 0
- `PolicyFacadeServiceImplTest`：Tests run: 31, Failures: 0, Errors: 0
- 合计 Tests run: 49, Failures: 0, Errors: 0, Skipped: 0。BUILD SUCCESS（2026-11-03）

空列表：已登录且没有记录时 HTTP 成功（`R.code=0`），`data.history=[]`，`data.favorites=[]`，`honesty.empty=true`，`honesty.fabricated=false`，`degraded=false`。这不是 501。匿名或库不可用同样是这两个空数组，不造记录。

## 架构合规自检

1. ✅ 调用链：展示 GET 只委托本门面；再次执行走已有 `search`；打开收藏走已有 `docs/{id}`。Java 不直连 Python 以外的算法入口。
2. ✅ 算法只在 Python。历史与收藏不打分、不进 `/internal/policy` 的计算。
3. ✅ 不写 nGQL，不碰 Nebula。
4. ✅ D12：不调用 `demo-*`。
5. ✅ D9：不是指标，不造 `metric_id`，不改 D4，空列表不造假收藏。
6. ✅ 身份沿用已有鉴权用户 id。不建 `display_user_*`。不把 localStorage 当实现。
7. ✅ 不写 ADS。表只存用户、检索条件、政策 id。
8. ✅ D14：本单不写对象存储，不新造桶。
9. ✅ 未拆掉 search、docs、metrics、rank、share。失败时不把空列表标成 fabricated。

## Cost 回填

| 字段 | 值 |
|---|---|
| actual_tokens | 20000 |
| model_used | cursor-grok-4.5 |
| actual_cost | 0.11 |
| cost_warn | green |

无控制台分项。按本单 `estimated_tokens` 20000、api-agent 80/20、B 档 `$3/$15` 回填：`20000×0.80×3/1e6 + 20000×0.20×15/1e6 = 0.108`，记 `0.11`。

ponytail: full

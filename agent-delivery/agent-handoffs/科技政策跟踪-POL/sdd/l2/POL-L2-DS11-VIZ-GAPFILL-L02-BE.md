# POL-L2-DS11-VIZ-GAPFILL-L02-BE · 政策分析评价 · Tab1 七可视化块读面接口

- 任务：`POL-L2-DS11-VIZ-GAPFILL-L02-BE`
- 日期：2026-11-12
- 监管：`human:淮政玮`
- 认领：`agent:api-agent`（主会话代认领，in_progress；registry 状态推进与 commit/push 由主会话收口）
- 强度：ponytail full
- 仓：`lumen-svc-platform` dev @ `a882de5c`（工作区干净起步）
- 上游：`2026-11-12-BE-viz读面侦察笔记.md`（落点）、`POL-L2-DS11-VIZ-GAPFILL-L02-DATA.md`（七表列清单 / 拣行键 / gap_item 闭集唯一真源，本单 §2/§3/§4/§5 只引用不改写）、`POL-L2-DS11-VIZ-API.md`（已按 FE 说明书缺口 1 增补 §10）
- 配套：`2026-11-12-FE-viz接线说明书.md`（FE 侧按本单路由接线）

## 1. 范围与实现

入口=③独立资源（监管人 2026-11-12 03:48 裁定）：display 加 `GET /v1/policy/evaluation/viz`（参数 `block`），element 加 `@Inner @GetMapping("/evaluation/viz")`，Feign 方法 `@NoToken` 配对。七块同步只读，不进 `JOB_SUB_TYPES` 异步白名单，不动既有 counts/shells/jobs 行为，路由避让既有 `/evaluation/counts|shells|template|trend|partition|scheme`（已 grep 全仓确认 `evaluation/viz`、`policyEvaluationViz`、`eval_viz` 零占用）。

复刻既有 evaluation 读面模式，零新建类、零框架改动：element 在 `PolicyGapfillController` 加 SQL 常量七条 + block→SQL Map + 一个端点方法；display 在 `PolicyEvaluationController` / `PolicyEvaluationService` / `RemoteElementClient` 各加一处。

## 2. 路由表（两层）

| 层 | 方法与路径 | 说明 |
|---|---|---|
| 浏览器 | `GET /display/v1/policy/evaluation/viz?block=<块键>` | 网关 StripPrefix=1 → display `/v1/**` |
| display | `GET /v1/policy/evaluation/viz`（`PolicyEvaluationController.viz`） | BFF：闭集校验后透传，不连库 |
| element | `GET /v1/element/policy/evaluation/viz`（`PolicyGapfillController.evaluationViz`，`@Inner`） | `JdbcTemplate` 只读，SQL 占位 `{gapfill}` → `gkxlumenx_gapfill` |

## 3. block → 表 → 拣行键映射（真源 DATA §2/§3，此处为接线对照）

| block | 表（`{gapfill}.`） | gap_item | 块内拣行键（保留未启用） |
|---|---|---|---|
| `metric` | `gapfill_policy_eval_viz_metric` | DS11-VIZ 评估指标体系卡 | `dim_key` 唯一 |
| `portrait` | `gapfill_policy_eval_viz_portrait` | DS11-VIZ 三联画像 | `portrait_type`（政策/企业/人才） |
| `geo` | `gapfill_policy_eval_viz_geo` | DS11-VIZ 地理分布图 | `region_name` |
| `region_impl` | `gapfill_policy_eval_viz_region_impl` | DS11-VIZ 分地区落实率 | `region_name` |
| `topic_heat` | `gapfill_policy_eval_viz_topic_heat` | DS11-VIZ 话题热力图 | `topic_name` + `stat_month` |
| `topic_sentiment` | `gapfill_policy_eval_viz_topic_sentiment` | DS11-VIZ 情感分布 | `scope_kind` + `topic_name` |
| `bubble` | `gapfill_policy_eval_viz_bubble` | DS11-VIZ 产业影响力气泡图 | `bubble_name`；`category` 图例从行长出 |

七块无用户筛选：一次请求整块读（无 WHERE 维度条件），排序写死在 SQL（topic_sentiment 用 `FIELD(scope_kind,'总体','分话题')` 让总体行在前）。SQL 列清单逐表写死（禁 `SELECT *`），含 D16 血缘六列 `is_mock, metric_id, gap_item, fill_method, gapfill_batch_id, generated_at`；`metric_id` 随行返回但灌数侧留空（DATA §5，不伪造 D9 血缘）。计数列经 `ElementDao.normalize()` 保证 JSON int；NULL 分值列保持 NULL 不造 0。

## 4. 请求/响应形状

成功（HTTP 200）：

```json
{
  "code": 0,
  "msg": null,
  "data": {
    "records": [
      { "id": 1, "dimKey": "覆盖广度", "dimLabel": "覆盖广度", "scoreValue": 82.5,
        "weightPct": 20.0, "pendingRef": "QPOL-02", "isMock": 1, "metricId": null,
        "gapItem": "DS11-VIZ 评估指标体系卡", "fillMethod": "manual",
        "gapfillBatchId": "…", "generatedAt": "…" }
    ]
  }
}
```

（行内列名 snake_case 由 `ElementDao` 统一转 camelCase；上例为 block=metric。`code` 封装随平台 `R`。）

空态（HTTP 200，恒不 501/404）——触发条件：`block` 缺省 / 空白 / 闭集外、表未建、库不存在、表无行、element 侧查询失败、display→element Feign 失败：

```json
{ "code": 0, "msg": null, "data": { "records": [] } }
```

## 5. 自检证据（全部绿）

| 项 | 命令 | 结果 |
|---|---|---|
| element 编译 | `mvn -pl gkxlumen-element -am -DskipTests compile` | BUILD SUCCESS（exit 0） |
| display 编译 | `mvn -pl gkxlumen-display -am -DskipTests compile` | BUILD SUCCESS（exit 0） |
| element 自检 | `PolicyGapfillEvaluationTest` | Tests run: 6, Failures: 0, Errors: 0 |
| display 自检 | `PolicyEvaluationServiceTest` | Tests run: 16, Failures: 0, Errors: 0 |

自检断言覆盖（不连库，mock `ElementDao` / Feign）：

- element（`vizRoutesSevenBlocksToOwnTablesAndStaysEmptyOutsideClosedSet`）：七个合法 block 各查一次自己的表（SQL 含表名 + `{gapfill}.` + 血缘六列 + 无 `SELECT *`、无写语句）；闭集外 `effect` / 空白 / 缺参不查表直接空 records（总查询次数=7）。
- display（`vizPassesBlockThroughAndAlwaysReturns200EmptyShape`）：闭集内透传 block 并解包 records；闭集外/空白/缺参不落下游（`verify(never)`）；Feign 抛异常降级空 records 不上抛；不建异步任务。
- display（`vizFeignMethodIsAnnotatedNoTokenPairedWithInnerEndpoint`）：`policyEvaluationViz` 带 `@NoToken`（缺它则下游 `@Inner` 切面拒绝、表现为 200 但恒空——侦察笔记 §4 红线 1）且路径为 `/v1/element/policy/evaluation/viz`。
- display 路由形状断言并入既有 `servicePathsFollowPanoramaStripPrefix`（`/viz` 挂在 `/v1/policy/evaluation` 下）。

环境备注：本机系统 Maven 3.6.0 低于编译插件要求（≥3.6.3），本次编译/测试用临时下载到用户目录的 Maven 3.9.9（`%USERPROFILE%\tools\apache-maven-3.9.9`），未改动仓内任何构建配置。

## 6. 架构合规自检

| 铁律 | 自检 |
|---|---|
| 调用链（前端→Java REST→不越层） | ✅ display→element 只读缺项表，不调 Python，不直连算法 |
| `@Inner` + `@NoToken` 配对 | ✅ element 端点 `@Inner`；Feign 方法 `@NoToken`，并有反射断言测试锁住配对 |
| display BFF 只读不连库 | ✅ 库访问只在 element（`ElementDao`），display 无 JdbcTemplate/数据源改动 |
| block 闭集 | ✅ display `VIZ_BLOCKS` 与 element `VIZ_SQL_BY_BLOCK` 同一七键闭集；闭集外不查表 |
| 空态恒 200 不 501 | ✅ 闭集外/无行/表未建/下游失败全落 `records: []`，测试断言覆盖 |
| viz 不进异步白名单 | ✅ 未动 `JOB_SUB_TYPES` / `JOB_KINDS` / `PolicyAnalysisTypes`；viz 为独立 GET 同步读 |
| 既有读面零扰动 | ✅ 未改 counts/shells/jobs/trend/partition/scheme/template 任何分支；diff 仅新增（193 行新增 / 2 行改动为注释与方法插入） |
| D16 缺项读面惯例 | ✅ `listOrEmpty`（不建表不插入）、血缘六列入 SELECT、`is_mock` 原样返回、D4 仍 mock |
| 命名区分（专题侧 PolicyVizServiceImpl） | ✅ 本链路为 display→element 直读 `gapfill_policy_eval_viz_*`，不触专题侧 `gapfill_policy_viz_*` 族 |
| 不 commit / 不 push | ✅ 产物停本地工作区，主会话收口 |

## 7. 新增/修改文件清单

| 文件 | 改动 |
|---|---|
| `gkxlumen-element/src/main/java/.../controller/PolicyGapfillController.java` | +七条 VIZ SQL 常量（列清单写死）、`VIZ_SQL_BY_BLOCK` 闭集 Map、`@Inner @GetMapping("/evaluation/viz")` 端点、类注释补一句 |
| `gkxlumen-display/src/main/java/.../controller/PolicyEvaluationController.java` | +`GET /viz` 端点、类注释补 viz 一句 |
| `gkxlumen-display/src/main/java/.../service/PolicyEvaluationService.java` | +`VIZ_BLOCKS` 闭集常量、`viz(block)` 分支（闭集校验→透传→降级空） |
| `gkxlumen-display/src/main/java/.../feign/RemoteElementClient.java` | +`@NoToken @GetMapping("/v1/element/policy/evaluation/viz")` Feign 方法 |
| `gkxlumen-element/src/test/java/.../controller/PolicyGapfillEvaluationTest.java` | +viz 七表分发/闭集空态/只读断言用例 |
| `gkxlumen-display/src/test/java/.../service/PolicyEvaluationServiceTest.java` | +viz 透传/空态/Feign 降级/@NoToken 配对断言用例；路由形状测试补 `/viz` |

文档（编排仓，同停本地）：

| 文件 | 改动 |
|---|---|
| `agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/l2/POL-L2-DS11-VIZ-API.md` | 增补 §10（viz 端点契约：闭集、委托链、空态），不改 §1–§9 原文（FE 说明书缺口 1） |
| 本 handoff | 新建 |

## 8. 偏离说明

- 无契约偏离。block 闭集、表名、gap_item、拣行键、空态口径与 DATA 单及已拍板契约逐条一致。
- element 侧未新建 `PolicyEvalVizController`（任务允许的备选）：七块 SQL 同构差异小，同 Controller 加一个 Map 分发即可，少一个类（ponytail）。

## 9. 遗留与下游

- 表未建/未灌数前线上即诚实空态（`records: []`），无功能损坏；灌数单 `POL-L2-DS11-VIZ-GAPFILL-L02`（data-agent）建表灌行后读面自动有数，**BE 不需要随灌数再改代码**。
- FE 侧按 `2026-11-12-FE-viz接线说明书.md` 接线（`fetchPolicyEvalViz<Block>` 落 `policyEvaluationViz.ts`，`optional:true`，空态分支已就位）。
- API 分册 §10 已补；契约冻结（枚举/DTO）仍归 `BE-POL-CONTRACT-01`，本单未越权。
- 权重行 `pending_ref=QPOL-02` 随行返回，前端 ⚠️「待甲方确认」角标数据源已备（D9 诚实性）。

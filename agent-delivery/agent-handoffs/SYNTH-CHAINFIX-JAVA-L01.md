# SYNTH-CHAINFIX-JAVA-L01 Handoff — 跨层链路修复第②站（JAVA 段）

- **任务**：SYNTH-CHAINFIX-JAVA-L01（跨层链路修复②：JAVA 段；③站 FE 依赖本单 HTTP 语义与错误码表）
- **执行**：agent:api（claimed_by=agent:api-agent，supervised_by=human:徐滕强）
- **仓**：`lumen-svc-platform`（origin/dev，**已 commit 未 push**：`f4b2ccb`，等人工确认推送）
- **强度**：ponytail: full（最短 diff；不新增依赖；复用既有 R 包络/Feign/Adapter 样板；公共 R 类未动）
- **契约输入**：`SYNTH-CHAINFIX-PY-L01.md` §2 冻结签名清单（①站）+ `SYNTH-L2-COLLAB.md` v1.0.8 §3
- **日期**：2026-11-06

## 1. 范围与实现（逐项修法）

### A. collaboration Adapter（P1-3）✅
| 改动点 | 文件 | 修法 |
|---|---|---|
| 协同白名单 | `async/support/analysis/SynthCollaborationAnalysisTypes.java`（新） | `COLLABORATION="region_innovation_collaboration"`；`WHITELIST`/`isSynthCollaboration`/`isAnalysis`/`normalizeWindow`/三段 `fingerprint(region,compare,window)`——全仿 elements 类，报告键 v1 不开放，无 weight_profile（册 §3.1） |
| Adapter | `async/service/adapter/analysis/SynthCollaborationAnalysisAdapterImpl.java`（新） | 仿 `SynthElementsAnalysisAdapterImpl` 三点差异：①`analysisTypes()`=协同键；②`buildExecuteBody` `leaf="collaboration"`；③批号提取=`result.snapshotId` 尾段（`batch:深圳市|全国重点城市|最近3年|{calc_batch_id}` → `calcBatchFromSnapshotId()` 静态助手；`task:{task_id}`/`none` → null 兜底 taskId）；`code!=0`/Feign 失败 → `IllegalStateException`（任务 failed 不写演示 JSON） |
| 注册表路由 | `AnalysisAdapterRegistryImpl` | **零改动自动进路由**（Spring 构造注入全量 Adapter 按 `analysisTypes()` 注册） |
| 任务链接线 | `AnalysisTaskServiceImpl` | 协同键接入三段指纹门（与要素同门：`analysis_fp`/`analysis_fp_leg` 双写）→ `findReusableCollaborationTask`（running 优先/当天 success 可复用/`normalizedCollaborationFp` 非三段不命中）→ subType=协同键 → 三段冻结（region/compare/window 归一顶层冗余 + object_summary）→ `applySvcSyncResult` 批号顶层冻结（缺失兜底 taskId）+ input_payload 窗归一兜底 |
| 单测 | `SynthCollaborationAnalysisAdapterImplTest`（10 例）+ `AnalysisAdapterRegistrySynthTest`（2 例） | 注册表含协同键、三白名单键互不干扰、create 202 路径（execute body leaf 校验）、非法键拒、批号提取四分支 |

### B. 图谱契约对齐（P1-4）✅
| 改动点 | 文件 | 修法 |
|---|---|---|
| 删 gapfill_batch_id | `SynthCollabGraphService.java`（重写 286→净删） | 参数/回显/空图构造全部移除 `gapfill_batch_id`（v1.0.8 已废止）；**删 `resolveBatchBinding`+`metaGraphBatch` 二跳预解析**（snapshotDerivesBatch 残留）——批次绑定（snapshotId 精确读 meta / 未传 is_latest）已下沉 Python 单点，绑定=snapshotId 或 is_latest，Java 不再经 batch-snapshot 解析图批；旧 `SNAPSHOT_BATCH_MISMATCH` 400 分支随之删除 |
| 读路径透传 | 同上 | `readGraph` → `collaborationGraph(query)` 补 `entity_types`/`relation_types`（逗号多选原样透传）+ `limit_nodes`/`limit_edges`（Integer 透传）；`industry` 语义注释=industry_code 精确匹配（Python 过滤）；校验全在 Python（非法 400 原文透传） |
| Feign 签名注释 | `RemoteSynthPythonClient.collaborationGraph` | javadoc 对齐 PY §2.1：参数集/无 gapfill_batch_id/端点已挂载（原「404 诚实降级」注释废止） |
| 测试同步 | `SynthCollabGraphServiceTest`（9 例重写） | 删 gapfill 双传/mismatch 用例；新增：snapshotId 透传（无二跳）、meta_missing 空图合法 200、industry/entity/relation/limit 五参透传、可选参数缺省不传、边对象无 year、`doesNotContainKey("gapfill_batch_id")` |

### C. collab 快照门面（P2-c 新断链）✅
| 改动点 | 文件 | 修法 |
|---|---|---|
| 门面服务 | `SynthCollaborationSnapshotService.java`（新） | 仿 elements 门面：region/compare 必填 400 → 窗归一（缺省最近3年）→ 转发 Python `/internal/v1/synth/collaboration/batch-snapshot`（snapshot_id 透传）；**九列外壳原样回显**（snapshotId/cache_key/computedAt/methodVersion/calc_batch_id/graph_batch_id/region/compare/window/publishedAt/isLatest/batchMetaReason），meta 行内回读为权威、Java 不改写；无批（calc_batch_id=null）→ 404；`batchMetaReason=batch_meta_missing` → 404 不回落最新批 |
| 控制器端点 | `SynthSnapshotController` | 新增 `GET /topic/v1/synth/collaboration/batch-snapshot`（region/compare/window/snapshotId 四参；网关剥 /topic 后 FE 契约 URL 不变） |
| 单测 | `SynthCollaborationSnapshotServiceTest`（7 例） | 九列含 isLatest 断言、参数透传+窗归一、400 errorCode、无批 404、无映射 404 禁回落、Python 400 原文、上游错/坏包络 502 |

### D. HTTP 语义修正（P1-7）✅
| 改动点 | 文件 | 修法 |
|---|---|---|
| 局部出口助手 | `SynthSnapshotResponses.java`（新） | `badRequest(errorCode)`→400 / `snapshotNotFound()`→404+SNAPSHOT_NOT_FOUND / `upstreamError(ref,ex)`→502+UPSTREAM_ERROR；**公共 R 类未动**（body 仍 R 包络 code=1），仅 synth 三服务+控制器局部 ResponseEntity 化 |
| 控制器 | `SynthSnapshotController`（四端点全改） | 返回类型 `R<...>` → `ResponseEntity<R<...>>`；swagger 注释补 400/404/502 语义与空图合法 200 例外 |
| 活力服务 | `SynthVitalitySnapshotService` | 400：REGION_AND_COMPARE_REQUIRED/WINDOW_INVALID/WEIGHT_PROFILE_INVALID（含 Python 400 原文透传）；404：无批条件/显式批 PY 200 空壳 `batch_reason=batch_not_published`（**PY 新契约**，不回落）；502：非 400 上游错/网络错/坏包络（code!=0/data 缺失）/半批不一致（原 500 语义） |
| 要素服务 | `SynthElementsSnapshotService` | 同款三分：400 errorCode+Python 原文；404=calc_batch_id=null；502=网络错/坏包络/半批不一致（原来全吞成 SNAPSHOT_NOT_FOUND 的上游错不再误报） |
| 图谱服务 | `SynthCollabGraphService` | 必填三键/窗非法 → 400（REGION_COMPARE_WINDOW_REQUIRED/WINDOW_INVALID）；**空图是合法 200**（无 meta 200+batch_meta_missing / 有 meta 无行 200+no_year_on_source，仅「快照不存在」才 404——本单图谱路径无 404 分支）；Python 400 → 400 原文 |
| 测试锚 | 三个 ServiceTest | R 断言改 ResponseEntity（`getStatusCode()`/`getBody()`）；新增 400 码表/404/502/`batch_not_published` 用例 |

### E. 500 区分（P2-a）✅
- 全部走 `SynthSnapshotResponses.upstreamError` → **HTTP 502 + body.msg=UPSTREAM_ERROR**（选 ResponseEntity 502，与 D 一致；不泄漏上游堆栈/内容，logRef 仅进日志）。
- 覆盖：Feign 非 400 状态（上游 5xx/404）、RuntimeException（网络断）、坏包络（code!=0/data 缺失）、五表半批不一致（活力）/八表半批不一致（要素）。
- 测试锚：`upstreamNon400AndNetworkErrorsReturn502UpstreamError` 等 8 个新断言。

## 2. ⚡ FE 对齐清单（③站对接依据）

> **③站 FE 按本表接线；HTTP 码语义与 PY 契约一致，勿另造。**

### 2.1 错误 HTTP 码语义（三表通用，body 恒为 R 包络 `{code,msg,data}`，失败 code=1）
| HTTP | 语义 | body.msg | FE 行为 |
|---|---|---|---|
| 200 | 成功/空图合法 | — / reason | 正常渲染；空图按 reason 展示不可用 |
| 400 | 参数缺失/非法 | `REGION_AND_COMPARE_REQUIRED` / `REGION_COMPARE_WINDOW_REQUIRED` / `WINDOW_INVALID` / `WEIGHT_PROFILE_INVALID` / Python 原文（`REGION_UNMAPPED: …`/`LIMIT_INVALID: …`/`ENTITY_TYPE_INVALID`/`RELATION_TYPE_INVALID` 等） | 表单校验提示，不发重试 |
| 404 | 快照/批不存在 | `SNAPSHOT_NOT_FOUND` | 进 no_batch 空态，引导「开始分析」 |
| 502 | 上游异常 | `UPSTREAM_ERROR` | 「服务暂不可用，请稍后重试」分支 |

### 2.2 collab 快照门面（新断链，原缺失接口）
- **URL**：`GET /topic/v1/synth/collaboration/batch-snapshot?region=&compare=&window=[&snapshotId=]`
  - `region`/`compare` 必填；`window` 1y/3y/5y 或中文（空=最近3年）；`snapshotId` 可选（task:{task_id}，无映射 404 不回落）
- **响应 data 九列外壳**：`snapshotId / cache_key / computedAt / methodVersion / calc_batch_id / graph_batch_id / region / compare / window / publishedAt / isLatest(0|1|null) / batchMetaReason` + `result`
- FE 消费 `isLatest`/`region`/`compare`/`window` 展示快照标识；`result._meta` 不消费

### 2.3 graph 契约（对齐 PY §2.1/§2.2，Java 已透传）
- **URL**：`GET /topic/v1/synth/collaboration/graph?region=&compare=&window=[&snapshotId=][&industry=][&entity_types=][&relation_types=][&limit_nodes=][&limit_edges=]`
- **无 `gapfill_batch_id` 参数（已废止）**；`industry`=`industry_code` 精确匹配；`entity_types`=`enterprise,institution,talent` 逗号多选；`relation_types`=`co_patent,co_project,talent_flow`；`limit_nodes`≤200/`limit_edges`≤500（越界 Python 400）
- **响应 data**：`{region,compare,window,snapshotId,calc_batch_id,graph_batch_id,nodes[],edges[](无year),truncated,reason}`；节点键 `industry`(=industry_code 值)/`industryLabel`/`degree`；边键 `relationType`/`sourceEventId`/`weight`
- **空图合法 200**：`reason=batch_meta_missing`（无 meta）/`no_year_on_source`（有 meta 无行）→ FE 展示「暂无图谱数据」不可用态，**不是错误**；截断提示读 `truncated=true`
- 400=参数非法（msg 原文）、502=上游异常；**图谱路径无 404**

### 2.4 vitality snapshot weight_profile 透传要求
- `GET /topic/v1/synth/vitality/batch-snapshot` 增 `weight_profile`（`INDEX_MAIN|WEIGHT_MAIN|EQUAL`，**大小写敏感**，缺省 INDEX_MAIN，非法 400）
- **回显口径=实际计算档**（PY 行内回读双标）：显式批回溯（`snapshotId=snap:{calc_batch_id}`）时批冻结档可能与请求档不同，FE **必须沿用响应内 `weight_profile` 与 `cache_key` 第四段**渲染（禁 EQUAL 算标 INDEX_MAIN），报告页同请求一致铁律不变
- 显式批未发布 → 404 `SNAPSHOT_NOT_FOUND`（响应外壳 `batch_reason=batch_not_published` 时 Java 已转 404）

### 2.5 任务链（协同键新增）
- `POST /topicAsync/topic/v1/analysis/tasks` `analysisType="region_innovation_collaboration"` 已可创建（白名单+三段指纹门+当天复用+leaf=collaboration 透传 Python）
- 协同无 weight_profile 段；三段指纹=region|compare|window（窗归一中文）

## 3. 自检结果（全绿）

| 自检 | 结果 |
|---|---|
| `mvn -pl gkxlumen-topic -am compile/test`（JDK 21） | ✅ BUILD SUCCESS，**44 tests 0 fail 0 error**（synth 4 套件 35 例 + 既有 9 例不回归） |
| `mvn -pl gkxlumen-topic-async-service-biz -am compile/test`（JDK 21） | ✅ BUILD SUCCESS，**217 tests 0 fail 0 error**（协同 Adapter 10 例+注册表 2 例+既有 task/policy/chain/svc 全量不回归） |
| 存量红隔离复验 | `RiskSupplyReportAssemblerTest`（risk 报告包，非本单范围）在**不含本单改动的干净 dev 基线同样红**（`git stash` 后复验确认；commit `7b555a3` 引入 `List.of` 不可变集合 add 越界），与本单无关、按边界未动，需另开修单 |

## 4. 架构合规自检（铁律逐条）

| 铁律 | 合规 |
|---|---|
| ①算法只在 Python | ✅ Java 零公式；批次绑定/筛选/截断全在 Python |
| ②调用链 前端→Java REST→Python /internal/* | ✅ 四端点均经 Feign `RemoteSynthPythonClient`/`RemoteSynthJobPythonClient`（仅 lumen-algo-py，D12 合规） |
| ⑤CI/CD | ✅ 本地 commit 未 push（等人工确认）；push 后 CI 验证 |
| ⑦共享聚合核心 | ✅ 只读 ADS（经 Python），Java 不直连库 |
| ⑩D9 血缘 | ✅ 空态诚实回显 reason，无伪数值；weight_profile 回显以 PY 批档为权威 |
| ⑫demo/lumen 隔离 | ✅ 未触碰任何 demo-* 引用 |
| D8/D10 | ✅ 门面 URL 不变（网关剥 /topic），FE 契约兼容；swagger 注释补语义 |
| 多会话保护 | ✅ 未动他人 WIP；stash 验证用 push -u 且即时 pop 恢复完整（git status 复核 15 文件齐） |

## 5. 偏离说明

1. **图谱服务删除旧「Python 端点 404 → 空图 graph_upstream_unavailable」降级分支**：PY 段 CHAINFIX-C 已挂载端点，且按 D/E 项该场景现应归 502 UPSTREAM_ERROR（端点未挂载=上游异常），不再伪空图。
2. **活力「无批条件 → 404」语义与 PY 兜底批并存**：PY 新契约下 latest 路由恒回 mock 兜底批（code=0），latestBatchId=null 的 404 分支实际仅在 PY 数据缺失时触发——保留分支作防御，不删（最短 diff）。
3. **存量红 `RiskSupplyReportAssemblerTest` 不修**：不在本单边界（risk 报告包 vs synth 链路），已基线复验为存量问题，建议 coordinator 另派 bugfix 单。
4. **协同任务线 `applySvcSyncResult` 冻结沿用 svc 同步链既有分支**：policy/vitality/elements/collaboration 四键共用同一同步 Execute 通道（`else if (policyJob || synthVitalityJob || synthElementsJob || synthCollaborationJob)`），无新增分派路径。

## 6. 产物清单

| 类型 | 产物 |
|---|---|
| commit | `f4b2ccb`（dev，15 文件 +1642/−598；**未 push**，等人工确认） |
| 新文件（6） | `SynthSnapshotResponses.java`、`SynthCollaborationSnapshotService.java`、`SynthCollaborationAnalysisTypes.java`、`SynthCollaborationAnalysisAdapterImpl.java` + 三测试类 |
| 改文件（9） | `SynthSnapshotController`、`SynthCollabGraphService`、`SynthVitalitySnapshotService`、`SynthElementsSnapshotService`、`AnalysisTaskServiceImpl`、`RemoteSynthPythonClient`（注释）+ 四测试类 |

## 7. 验收证据

- §3 两模块 mvn test 输出（topic 44 绿 / async-biz 217 绿）。
- 存量红基线复验：stash 后干净基线 `RiskSupplyReportAssemblerTest` 同样红，排除本单引入。
- CI：未 push，push 后由 GitLab CI 验证；K8s dev 行为变化 = synth 四端点 HTTP 码精确化 + collab 门面新端点上线（FE 站接线后端到端可见）。

## 8. cost（待 task-update-fields 回填）

| 字段 | 值 |
|---|---|
| actual_tokens | ≈150k（含读 PY 契约/现状代码/三轮测试迭代） |
| model_used | glm-5.3-Flash |
| actual_cost | ≈$0.7（< $10 阈值，不触发复盘） |
| cost_warn | false |

## 9. 移交③站（FE）注意事项

1. **错误分支三态化**：FE 既有 `code===1` 判失败逻辑需升级为 HTTP 状态码判定（400/404/502），`msg` 直接可作展示文案（errorCode 或 Python 原文）。
2. collab 快照门面 URL（§2.2）为本单新断链，FE 接线前该页数据源缺失；`isLatest` 为新回显列。
3. graph 前端过滤（kindFilter/edgeFilter）应改为服务端透传参数（§2.3），本地过滤保留兼容期可但截断计数会失真。
4. `WeightProfileSwitch` 切档后必须以响应 `weight_profile`/`cache_key` 回显为准刷新（§2.4），禁止前端记档。
5. 协同任务键（§2.5）任务列表 subType=协同键，FE 任务中心标签可用 LABELS「区域创新协同分析」。

# LUMEN-INTEL-ELEM-BE-L01 · handoff

- 任务：综合智能分析要素 — Java 任务键 + Adapter + 快照门面（lumen-svc-platform）
- Epic：E8-综合智能分析 ｜ 执行：agent:api-agent ｜ 监管：human:徐滕强
- 仓：`repos/lumen-svc-platform`（origin/dev；**本地 commit `e6a28fe`，未 push**——按 2026-11-05 用户裁定默认人工确认后推）
- 日期：2026-11-05
- 强度：ponytail full（完整复用 0fdc245 活力线类结构/包络/错误处理，不另起炉灶）

## 1. 范围与实现（对照 ELEM 册 v1.0.6 §3 / 派单 4 项 / PY handoff）

| 派单项 | 实现 |
|---|---|
| ① 任务键白名单 `region_innovation_elements` 入 SynthAnalysisTypes（仿 vitality） | ✅ `SynthElementsAnalysisTypes`：白名单**仅分析键**；报告键 v1 不开放（ELEM 册 §3 报告=前端基于真实快照渲染 PDF，不经任务链）；三段指纹 `region\|compare\|window`（无 weight_profile 段）；`normalizeWindow` 与活力同轨（1y/3y/5y 或中文 → 中文，缺省最近3年） |
| ① params 六键 region/compare/window 透传（elements 无 weight_profile） | ✅ `SynthElementsAnalysisAdapterImpl.buildExecuteBody`：task_id/leaf=elements/region/compare/window（归一中文）；**不下发 weight_profile**（等权由 seed 灌 `synth_elem_weight`、Python 装包只读已灌行，禁 Java 补 1/3）；page_size/element_types 属快照线参数，任务线不透传（Python execute 分支也不收） |
| ② Adapter：execute 透传 Python `/internal/v1/synth/jobs/execute`（leaf=elements） | ✅ `SynthElementsAnalysisAdapterImpl`（仿 `SynthVitalityAnalysisAdapterImpl`）：复用 `RemoteSynthJobPythonClient`（同一 POST 端点，Python 按 leaf 分派）；code!=0/Feign 4xx/5xx → 任务 failed 不写演示 JSON；`data.status` 缺省补 succeeded |
| ② 任务成功批号冻结 | ✅ Python elements 包 `calc_batch_id` 在 **result 体内**（外壳无此键，与活力不同）→ Adapter `normalizeSucceeded` 提升到 data 顶层；`AnalysisTaskServiceImpl.applySvcSyncResult` elements 分支顶层冻结进 targetParams（缺失兜底 taskId，与活力同款）；input_payload 窗归一兜底 |
| ③ 快照门面 `GET /topic/v1/synth/elements/batch-snapshot` | ✅ `SynthElementsSnapshotService` + `SynthSnapshotController` 扩端点（ELEM 册判定：**扩展快照 API 不新增独立路由**，同 `/topic/v1/synth` 前缀）；`@Inner(value=false)` 同活力；page_size/element_types 透传 Python |
| ③ Feign Python internal 端点 | ✅ `RemoteSynthPythonClient` 增 `elementsBatchSnapshot`（`/internal/v1/synth/elements/batch-snapshot`，SpringQueryMap）；复用既有 client（url 继承 `gkxlumen.topic.algo-base-url`），不新建 Feign 接口 |
| ④ 单测（白名单/params 透传/快照 200 与 400 透传/DTO 字段齐含 panorama/elements 键与 vitality 键互不干扰） | ✅ 3 个新测试类共 20 用例（详见 §4），模式仿 VIT-FP 3 个测试类样板 |

### 关键设计决定（与活力线的同与异）

| 点 | 活力线 | 要素线（本单） |
|---|---|---|
| 指纹段数 | 四段（+weight_profile_norm） | **三段**（无 profile；窗归一中文后拼） |
| 复用门 | `findReusableVitalityTask` + legacy 三段识别 + legacy_unknown 永不复用 | `findReusableElementsTask`：按 analysisType 过滤 elements 任务、冻结 fp 归一（窗归一）比对；**非三段形状返 null 不猜**（活力四段误挂不命中） |
| 快照 latest 路由 | Java 两跳：`latest-batch` → 按批装包（五表同批校验 AR-6/TC-2） | **单跳**：Python 装包自带「同条件最新 succeeded 批」（`MAX(calc_batch_created_at)`，PY handoff §1）；无 latest-batch 端点可用，Java 不自建批索引 |
| 无批次语义 | Python latest code!=0 → Java 404 | Python **200+calc_batch_id=null**（snapshotId 尾 `\|none`）→ **404 判定在 Java**（派单明确：404 判定留给本单 Java Adapter/门面） |
| snapshotId 直读 | `snap:{calc_batch_id}`（Java 拼） | Python `batch:{city}\|{compare}\|{window}\|{calc_batch_id}`（Python 生成，Java 原样透传回显） |

## 2. 偏离说明

1. **Python 400 语义走 FeignException 而非包络**：Python `synth_elements_routes` 拒绝时返回 HTTP 400（`JSONResponse(status_code=400)`），仓库无自定义 ErrorDecoder → Feign 抛 `FeignException`（body 在 contentUTF8）。Java 门面 `FeignException.status()==400` 时取响应体原文 `R.failed(content)` 透传（前端可见 REGION_UNMAPPED/ELEMENT_TYPE_INVALID 等）；500/连接异常按 404 语义。单测用 `FeignException.errorStatus` 构造真实形态。
2. **快照不校验五表同批（活力 AR-6/TC-2 的对应物降为外壳批号一致性）**：Python elements 装包本身按「最新 succeeded 批」同批读 8 表（PY handoff §1），Java 门面保留「外壳 calc_batch_id == result.calc_batch_id」一致性校验（不一致整包拒发）；五表逐表同批断言已由 Python 自检覆盖（check_synth_elements.py [4]），Java 不重复做库级校验（D12：契约面=Python internal，Java 不直连库）。
3. **报告键不登记**：派单背景给的三叶任务键表含 `region_innovation_elements_report`；ELEM 册 v1.0.6 §3 明确「报告=前端基于真实快照渲染 PDF、`*_report` 任务键 v1 不依赖」→ 白名单只有分析键（YAGNI；后续若产品要求报告任务化再扩）。
4. **`object_summary` 无 profile 段**：要素冻结 meta `object_summary` 为 `region · compare · window` 三段（活力四段带 profile）。

## 3. 产物清单（commit `e6a28fe`，10 files +1396/-14）

| 文件 | 动作 | 说明 |
|---|---|---|
| `gkxlumen-topic-async-service/.../support/analysis/SynthElementsAnalysisTypes.java` | 新增 | 白名单/键判定/窗归一/三段指纹 |
| `gkxlumen-topic-async-service/.../adapter/analysis/SynthElementsAnalysisAdapterImpl.java` | 新增 | 校验/leaf=elements 透传/批号提升冻结 |
| `gkxlumen-topic-async-service/.../impl/analysis/AnalysisTaskServiceImpl.java` | 修改 | 要素三段指纹门 + jobMeta 三段冻结 + 同步 Execute 链 + applySvcSyncResult 批号顶层冻结 + `findReusableElementsTask`/`normalizedElementsFp` |
| `gkxlumen-topic/.../feign/RemoteSynthPythonClient.java` | 修改 | +`elementsBatchSnapshot` |
| `gkxlumen-topic/.../service/synth/SynthElementsSnapshotService.java` | 新增 | 快照门面（归一/透传/400 透传/404 判定/一致性） |
| `gkxlumen-topic/.../controller/synth/SynthSnapshotController.java` | 修改 | +`/elements/batch-snapshot` 端点 |
| 3 个测试类（async-biz 2 + topic 1） | 新增 | 见 §4 |

他人 WIP 未触碰：`gkxlumen-cms/**`、`gkxlumen-topic-policy/**`、`helm/**`、`db/9zz_*.sql` 等 11 个脏文件原样保留在工作区。

## 4. 验收证据（两模块全绿）

```
mvn -pl gkxlumen-topic-async-service/gkxlumen-topic-async-service-biz -am test
  → Tests run: 205, Failures: 0, Errors: 0, Skipped: 0   BUILD SUCCESS
  （原 192 + 新 13：SynthElementsAnalysisTypesTest 5 / SynthElementsAnalysisAdapterImplTest 9
    / AnalysisTaskServiceImplElementsFpGateTest 8——缺省窗归一+三段冻结+复用+批号冻结+force）

mvn -pl gkxlumen-topic -am test
  → Tests run: 16, Failures: 0, Errors: 0, Skipped: 0    BUILD SUCCESS
  （原 9 活力快照不回归 + 新 7：SynthElementsSnapshotServiceTest——200 同构 DTO 字段齐含 panorama
    /page_size+element_types 透传断言/Java 400/Python 400 透传/无批 404/上游异常与坏包络 404/批号不一致拒发）
```

单测覆盖对照派单 ④：白名单 ✅（5）、params 透传 ✅（Adapter body 不带 weight_profile + 快照 query 带 page_size/element_types）、快照 200 与 400 透传 ✅、DTO 字段齐含 panorama ✅（MOCK-INV §1 23 键逐一 containsKey + panorama[] 三键 DTO）、elements 键与 vitality 键互不干扰 ✅（双向 isAnalysis/isSynth* 反例）。

## 5. DTO 与 Python 响应字段对照结论

Python `build_elements_snapshot` → Java 门面 `data` **原样透传，零改写**（`Map<String,Object>` 全键保留，仅 `methodVersion` putIfAbsent 兜底）：

| Python 外壳字段 | Java data | 说明 |
|---|---|---|
| `snapshotId`（不可变 `batch:深圳市\|全国重点城市\|最近3年\|{batch}`） | ✅ 原样 | snapshotId 入参时按该批读（Python 侧行为） |
| `cache_key`（`elem:city\|compare\|window` 三段） | ✅ 原样 | 与总纲「要素三段 cache_key」一致 |
| `computedAt` / `methodVersion`（synth-elements-v1.0） / `calc_batch_id` | ✅ 原样 | 无批 calc_batch_id=null → Java 转 SNAPSHOT_NOT_FOUND |
| `result`（ElementResult 22 顶层字段） | ✅ 原样 | compositeIndex/typeIndex/levelIndex/domainIndex/evaluationDimensions(+Reason)/deltaVsCompare/yoy/typeScores/levelScores/domainScores/lensWeights/indicators/ranks/trend/strengths/weaknesses/contributions/methodDigest/batchComputedAt/source/snapshotId |
| `result.panorama[]`（ELEM 册 §2 DTO） | ✅ 原样 | element_type/total_count/top_n[]；page_size/element_types 由 Java 透传生效 |
| `result.panoramaReason` / `result.cache_key` / `result.calc_batch_id` / `result.methodVersion` / `result.metrics` / `result.evaluationDimensionsReason` | ✅ 原样 | PY 扩展字段全保留（MOCK-INV 回写归 Python 线） |

任务线：`execute_elements_job` 出参 `{task_id, leaf, status, stages, result, methodVersion}` + Adapter 增补 `accepted/task_id/calc_batch_id` → `applySvcSyncResult` 落 `result_payload`（含 panorama[]）+ 顶层 `calc_batch_id`。前端 #105 resultData 拿到的即 ElementResult 全量。

## 6. 架构合规自检（公约 §2 铁律）

| 铁律 | 自检 |
|---|---|
| 1 算法只在 Python | ✅ Java 零公式；装包/panorama 汇聚全在 entan-py |
| 2 调用链 | ✅ 前端→Java /topic/v1/synth/**（网关剥 /topic）→Python /internal/*；Feign 仅 lumen-algo-py，禁 demo-*（D12） |
| 3 NebulaGraph | N/A（无图谱） |
| 4 可观测性 | ✅ 快照 trace 日志（snapshotId+耗时，ELEM 册 §5）；任务线审计/日志沿用 |
| 5 CI/CD | 本地 commit **未 push**（按 fe-manual-confirm-push 闸门等确认；本仓为 Java 后端仓，规则按派单「不 push」执行） |
| 6 demo2 只读 merge | N/A |
| 7 共享聚合核心 | ✅ Java 只读 ADS 面（经 Python）；不写 nGQL |
| 8 ADS 先行+Mock | ✅ 只读 ADS 8 表；is_mock=1 预填批由 Python/数据线负责 |
| 9 D8 前端规范 | N/A（未动 FE） |
| 10 D9 血缘 | ✅ DTO 逐字段透传含 metrics 置信度元数据；四维固定 []+reason=metric_not_registered（137② blocked，不接数据源）；UI 侧角标归 FE 线 |
| 11 D10 交互规范 | N/A |
| 12 demo/lumen 隔离 | ✅ 未调任何 demo-* 服务 |
| 13 D14 对象存储 | N/A |
| 14 D16 gapfill 边界 | ✅ 未写任何库 |
| 15 D17 合规算法 | ✅ 未触碰唐绍祖锁定闭包；M_SYNTH_187_1–190_1 只消费 |
| 16 D18 签收条件 | ✅ 接口只读 Python 装包结果，无 Java 写死 mock |

## 7. ponytail 自检

ponytail: full——全部复用 0fdc245 活力线既有类/模式（Types/Adapter/Service/Controller/Feign 五件 + FingerprintGateTest 模式），最小 diff（AnalysisTaskServiceImpl 3 处分支扩展 + Controller/Feign 各 1 处追加）；无新依赖、无新抽象；唯一「不复制」的是活力 latest-batch 两跳（Python elements 无该端点，装包自带 latest 路由，少一次往返）；自检=两模块全量 mvn test（含既有 192+9 回归）。

## 8. cost（按 budget-estimate.md 四字段）

| 字段 | 值 |
|---|---|
| actual_tokens | ~210000 |
| model_used | glm-5.3-Flash（Cursor 内） |
| actual_cost | ~$0.30 |
| cost_warn | false（< $10 阈值） |

## 9. 后续依赖（不属本单）

- push 与 K8s dev rollout：等人工确认（本次 commit `e6a28fe` 停本地）
- FE 要素三页接线（`LUMEN-INTEL-FE-ELEM`）：快照 URL `/topic/v1/synth/elements/batch-snapshot` 已就绪；四维区块缺失态+红问号；panorama 全景模块读 `result.panorama[]`
- MOCK-INV 契约回写（panorama 字段登记）：随该文档下次修订并入（Python 线同待办）
- coordinator 回填 task-registry 状态与 cost 字段

# LUMEN-INTEL-VIT-FP-SNAP-L01 · 活力叶四段指纹 + legacy 识别 + 不可变 snapshotId

- 日期：2026-11-05
- claimed_by：`agent:api-agent`；supervised_by：`human:徐滕强`
- Epic：E8-综合智能分析；仓：`lumen-svc-platform`（分支 `dev`）
- 契约真源：`agent-delivery/agent-handoffs/综合智能分析-SYNTH/sdd/l2/SYNTH-L2-VIT-AI-TABLES.md` §3（v1.0.6）+ `LUMEN-INTEL-SDD-SIGNOFF-L01.md`（AR-3/AR-6/TC-2 已采纳）

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full`（复用既有指纹门/同步链/归一模式增量改；仅 2 个新主类 + 1 控制器 + 1 Feign；无新依赖；pom 仅钉既有 surefire 3.2.5 惯例） |

## 一、范围与实现（对照派单 7 条）

| # | 要求 | 落点（类#方法） |
|---|---|---|
| 1 | **analysis_fp 四段** `region\|compare\|window\|weight_profile_norm`；枚举 `INDEX_MAIN\|WEIGHT_MAIN\|EQUAL`，缺省归一 `INDEX_MAIN`；窗中文归一入指纹 | `SynthVitalityAnalysisTypes#normalizeWeightProfile`（枚举+缺省归一，大小写敏感，非法返 null→400）· `#vitalityFingerprint`（四段拼接）· `SynthVitalityFingerprints#normalizeFingerprint`（三段旧式补第四段/四段校验；窗复用既有 `normalizeWindow`）· 接线 `AnalysisTaskServiceImpl#create`（活力分支：归一→非法 `WEIGHT_PROFILE_INVALID`/`WINDOW_INVALID` 400→四段 fp 双写） |
| 2 | **旧任务 legacy 识别**：三段历史任务按冻结权重向量/methodVersion 识别（对照表容差 0：EQUAL=0.25×4、INDEX_MAIN=0.30/0.30/0.20/0.20、WEIGHT_MAIN=0.30/0.35/0.20/0.15）；无法确认→`legacy_unknown` 永不自动复用；新 INDEX_MAIN（含缺省）不得命中 legacy 或向量不符任务 | `SynthVitalityFingerprints#legacyProfileOf`（识别序：显式 `weight_profile` → 权重向量精确匹配 `matchVector`（`Double.compare` 容差 0）→ methodVersion 档位名）· `#extractWeightVector`/`#parseVector`（dimScores 四键位+顶层直挂+包络嵌套，扁平两级不递归）· 复用门 `AnalysisTaskServiceImpl#findReusableVitalityTask`+`#normalizedVitalityFp`（三段旧任务禁按缺省补 INDEX_MAIN——那是请求归一规则不是存量识别规则；legacy_unknown 连 running 单飞也不命中） |
| 3 | **snapshotId 不可变** `snap:{calc_batch_id}`；同条件重跑新 ID，旧 ID 仍可读 | `SynthVitalitySnapshotService#batchSnapshot`（snapshotId 传入→直读该批不经索引）· `#readBatch`（批号=快照唯一性；响应回拼 `snap:{calc_batch_id}`）· 批号真源：成功任务冻结 `calc_batch_id`（`applySvcSyncResult` 活力分支提取 Python 包络批号，缺失兜底 taskId；`SynthVitalityAnalysisAdapterImpl#normalizeSucceeded` 同步兜底） |
| 4 | **cache_key 分离**：稳定键仅作最新成功快照索引；重跑成功改指新 snapshotId | `SynthVitalitySnapshotService`：`cache_key=region\|compare\|window\|weight_profile_norm`（响应回显）；未传 snapshotId → `#latestCalcBatchId`（Python 按 ADS 批次状态取最新 succeeded 批，排序键 `calc_batch_created_at`）→ 重跑成功 latest 天然改指新批；索引介质=ADS 批次状态（AR-3 裁定：任务链 Java 真源，不在 Java 造 meta 表，latest 查询走 Python 读 ADS） |
| 5 | **五表同批一致性（AR-6/TC-2）** | `SynthVitalitySnapshotService#readBatch`：装包回读批号 ≠ 请求批号 → 拒发整批（500 语义 R.failed）+ `synth vitality batch inconsistent` warn；写入侧同批由 Python seed 同 `calc_batch_id` 承担（Java 只读）；同请求 index/dim/weight/rank 同 profile 由 `weight_profile` 参数贯穿 execute body→装包→响应回显 |
| 6 | **快照接口响应**：snapshotId/cache_key/computedAt/methodVersion/weight_profile/calc_batch_id/result，字段名与 VitalityResult 契约对齐（MOCK-INV 为准） | `SynthSnapshotController` `GET /topic/v1/synth/vitality/batch-snapshot`（region/compare/window/weight_profile/snapshotId）→ 网关 GlobalFilter 剥 /topic → `gkxlumen-topic` `/v1/synth/...`（裸 /topic 路由 lb://gkxlumen-topic，前端契约 URL 不变，与 innov industry-clusters 同落点模式）；`result` 原样透传 Python 装包体（`vitalityIndex/dimScores/...` 不重写）；缺批 404 语义 `SNAPSHOT_NOT_FOUND`（FE `IntelBatchSnapshotNotFound`→no_batch）；404 走 R.failed 包络（网关统一 200 包装，FE 按 `ok=false` 判空态，行为与 404 语义等价——见偏离 2） |
| 7 | **单测**：fp 归一（缺省/EQUAL/非法 400）、legacy（TEMP_WEIGHTS→legacy_unknown）、A/B 批 snapshotId 不撞旧 ID 可读、cache_key 改指 | `SynthVitalityFingerprintsTest`（12 用例：缺省归一/EQUAL≠INDEX_MAIN/非法枚举·窗·形状 400/显式档位/向量精确匹配+维序敏感+TEMP_WEIGHTS unknown/methodVersion 仅档位名/嵌套向量）· `AnalysisTaskServiceImplVitalityFpGateTest`（8 用例：缺省冻结四段+下游带 profile/非法档 400/EQUAL 不复用 INDEX_MAIN/legacy_unknown 禁复用含 running/向量识别可复用/同档当天复用/成功批冻结 calc_batch_id）· `SynthVitalitySnapshotServiceTest`（9 用例：默认归一+cache_key/非法档/非法窗/region 必填/A·B 批不撞+旧 ID 可读+cache_key 同值覆盖/不一致拒发/缺批 404/上游异常不泄漏/EQUAL 独立 cache_key） |

下游透传链：`SynthVitalityAnalysisAdapterImpl#buildExecuteBody` 增 `weight_profile` 透传（Python 按方案配对读表并回批号）；`downstreamParams` 剥 `analysis_fp_leg` 不进下游。

## 二、偏离说明

1. **快照门面落 `gkxlumen-topic` 而非 `gkxlumen-topic-chain`**：派单只说「仓内既有代码上增量改」。FE 契约 URL 是裸 `/topic/v1/synth/vitality/batch-snapshot`，按现行网关配置（`/topic/**` → `lb://gkxlumen-topic`，GlobalFilter 剥第一段）该 URL 只能由 `gkxlumen-topic` 承接——与 innov 承接 `/topic/v1/meta/industry-clusters` 完全同款（前置具体路由优先）。不改网关配置、不改 FE，前端零感知。as-built：`SynthSnapshotController@RequestMapping("/topic/v1/synth")`。
2. **404 语义经 R.failed 包络**：仓内 `R` 包络惯例（网关统一 200 包装 + `ok=false`）。FE `synthBatch.ts` 现按 HTTP 404 抛 `IntelBatchSnapshotNotFound`，但 catch 兜底任何异常同样进 no_batch（`resolveVitalityInstantResult` catch-all→null），行为等价；FE 后续把 `ok=false||status===404` 判空态即可（一行，属 FE 联调单）。
3. **latest-batch / batch-snapshot 的 Python internal 端点**（`/internal/v1/synth/vitality/latest-batch`、`/internal/v1/synth/vitality/batch-snapshot`）属算法并行线（`LUMEN-INTEL-VIT-PY-L01` 装包读表改造），Java 侧已按 VIT 册 §1/§3 契约定型 Feign（`RemoteSynthPythonClient`）；Python 未上线前快照接口诚实 404（`SNAPSHOT_NOT_FOUND`），不阻塞本单验收（D18：Java 不直连 ADS，读表必须经 Python）。
4. **formatter 全量刷**：`spring-javaformat:apply` 扫全模块刷出大量既有格式漂移，已按「本单不触碰文件还原」处理，commit 只含本单 11 文件；两模块既有文件的少量格式修正随本单文件带入（编译与 192 测试验证无损）。

## 三、冲突检查（多会话保护）

- `git status` 开工检查：工作区已有 `gkxlumen-cms/OpsContentService*`、`gkxlumen-cms/TopicPolicyPublishedController.java`、`gkxlumen-topic-policy/RemoteCmsPublishedClient.java` 三个**他人在途**未提交改动 → 本单零触碰（无交集文件），已原样保留，未 add/checkout。
- 本单提交 `0fdc245` 不含任何他人文件；未 push（coordinator 统一推）。

## 四、验收证据

- 编译：`mvn compile -pl gkxlumen-topic-async-service/gkxlumen-topic-async-service-biz,gkxlumen-topic -am` SUCCESS（JDK21）。
- 单测：两模块全量 `mvn test` → **Tests run: 192, Failures: 0, Errors: 0, Skipped: 0**（async-biz 183 + topic 9）；其中本单新增 25（Fingerprints 12 + FpGate 8 + Snapshot 9），既有 167 全过零回归。BUILD SUCCESS。
- 关键断言自证（测试名可溯）：`defaultProfileNormalizesToIndexMainAndFreezes`（缺省=INDEX_MAIN+冻结四段）、`invalidProfileRejected400`（非法枚举/大小写敏感 400）、`equalDoesNotReuseIndexMainTask`（四段不同不复用）、`defaultDoesNotReuseLegacyUnknown`+`legacyUnknownNotReusedEvenWhenRunning`（缺省/running 均不复用旧任务）、`vectorIdentifiedLegacyProfileReuses`（0.30/0.30/0.20/0.20→INDEX_MAIN 可复用）、`recognizesVectorExactMatchOnly`（TEMP_WEIGHTS 0.30/0.30/0.25/0.15→legacy_unknown）、`batchAandBSnapshotIdsDistinctAndOldIdStillReadable`（A/B 不撞+旧 ID 读旧批+cache_key 同值覆盖）、`inconsistentBatchRejectedWholeBatchFailed`（AR-6 回读批号不符整批拒发）。
- 观测（VIT 册 §5）：`SynthVitalitySnapshotService` 装包成功/缺失/不一致/上游故障四类 trace log（cacheKey/snapshotId/costMs/batch 批号），Adapter 包络日志补 `calcBatchId`。

## 五、架构合规自检（公约 §2 摘要）

| 铁律 | 结论 |
|---|---|
| D1 调用链：FE→Java REST→Python `/internal/*` | ✅ 快照经 `RemoteSynthPythonClient`（entan-py），任务经既有 `RemoteSynthJobPythonClient`；无越层 |
| D2 Java 禁算法 | ✅ Java 只做归一/指纹/识别/索引路由（平台逻辑），指数公式全在 Python |
| D3 契约面=ADS，Java 只读 | ✅ 五表读取全在 Python 侧（latest/batch 两 internal 端点）；Java 不写 ADS |
| D8/D9/D10 | ➖ 本单后端；响应体含 `weight_profile` 回显供 FE D9 角标消费 |
| D12 demo/lumen 隔离 | ✅ Feign 仅 `lumen-algo-py`，无 demo-* |
| D18 禁写死 mock | ✅ 快照一律读批；无预计算→404 空态，不造 JSON |
| git 策略 | ✅ dev 直推合规 commit（`[agent:api]`），本单不 push 交 coordinator |

## 六、cost 回填

| 字段 | 值 |
|---|---|
| actual_tokens | ~150000 |
| model_used | glm-5.3-Flash |
| actual_cost | ~0.6 |
| cost_warn | false |

## 七、遗留与依赖

- Python 侧两 internal 端点（latest/batch 装包）待 `LUMEN-INTEL-VIT-PY-L01`；联调时若端点路径/包络有出入，改 `RemoteSynthPythonClient` 一处即可。
- FE 空态判定建议（偏离 2）转 FE 联调单；`USE_MOCK=true` 面 FE 自 mock 不受影响。
- AR-6 写入侧（seed 同 `calc_batch_id`+同批次时间戳写五表、失败整批 failed）由算法线 seed 落实，Java 只做读取侧回读校验（本单已落）。

## 八、涉及文件（commit `0fdc245`）

新增：
- `gkxlumen-topic-async-service/gkxlumen-topic-async-service-biz/src/main/java/com/topcomm/gkxlumen/topic/async/support/analysis/SynthVitalityFingerprints.java`
- `gkxlumen-topic/src/main/java/com/topcomm/gkxlumen/topic/service/synth/SynthVitalitySnapshotService.java`
- `gkxlumen-topic/src/main/java/com/topcomm/gkxlumen/topic/controller/synth/SynthSnapshotController.java`
- `gkxlumen-topic/src/main/java/com/topcomm/gkxlumen/topic/feign/RemoteSynthPythonClient.java`
- 测试：`SynthVitalityFingerprintsTest.java`、`AnalysisTaskServiceImplVitalityFpGateTest.java`、`SynthVitalitySnapshotServiceTest.java`

修改：
- `SynthVitalityAnalysisTypes.java`（weight_profile 枚举/归一 + 四段 fp）
- `AnalysisTaskServiceImpl.java`（活力四段指纹门 + legacy 感知复用 + 冻结四段/profile + 成功批冻结 calc_batch_id + fp 窗归一兜底）
- `SynthVitalityAnalysisAdapterImpl.java`（execute body 透传 weight_profile + 包络 calc_batch_id 兜底）
- `gkxlumen-topic/pom.xml`（surefire 3.2.5，与 async-biz 同款注释）

CI：未 push，push 后走 `backend:image:topic-async-service` / `backend:image:topic`（`cicd` 非 skip，deploy 链见 .gitlab-ci.yml 527 行自动发清单）。

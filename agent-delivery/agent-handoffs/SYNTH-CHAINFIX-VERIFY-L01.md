# SYNTH-CHAINFIX-VERIFY-L01 Handoff — 跨层链路修复定向 live 复测（独立复测记录）

- **任务**：SYNTH-CHAINFIX-VERIFY-L01（四站修复 PY `4828c06` / JAVA `f4b2ccb` / FE `9c4694d`+`4397e0c` / DOCS 推 origin/dev 后的定向 live 复测；只测本轮修复点，不重跑全量金路径）
- **执行**：agent:qa（claimed_by=agent:qa-agent，supervised_by=human:徐滕强）
- **时间**：2026-11-06 15:19 – 15:55（UTC+8）
- **性质**：只测试不改代码；零业务 commit / 零 push（本 handoff 亦不 push，按派单）
- **ponytail**: full（逐项判定按派单卡；期望未发生必红；SSH 同意图 ≤2、禁探活；502 停机模拟不可行如实注明）
- **证据等级**：A=集群内 live 实测（跳板机 zphz-jump，kubeconfig `/tmp/kubeconf`；Python 直打 `10.96.3.124:8000`、async-service `10.96.0.84:7094`）；B=已发布镜像/代码链；C=外部可达性

## 0. 结论速览

**15 断言：12 绿 · 1 红 · 3 未测（另 1 项按派单预告跳过）**。

- **红 1**：步骤 1(e) 显式 `snapshotId=snap:mock_20261106_vit_seed` 直读——回显档标 `EQUAL` 但数值 `75.1478` 是该批 **INDEX_MAIN** 行的（EQUAL 行应为 74.9981）→ 档标签与数值行错位，**违反「禁 EQUAL 算标 INDEX_MAIN」回显口径铁律**（C1 · Python 层）。
- **未测 3（同一根因）**：Java 门面层三项（collab 门面九列 / Java graph 契约 / P1-7 400/404 本体）——`gkxlumen-topic` pod **未滚动**（镜像 `latest`、10-31 启动；该模块 `deploy:topic` 仅 `FULL_PIPELINE=true` 才发布，日常 dev push 不含），且集群内直打该 svc 全部 401 认证掩蔽（不存在路径也 401，无法绕过）。
- Python/FE/async-service 侧修复点全部 live 验证通过；协同任务链端到端在 dev 实跑成功。

## 1. deploy 状态（步骤 0）

| 仓 | commit | pipeline | deploy 结果 | K8s pod 滚动确认 |
|---|---|---|---|---|
| lumen-algo-py | `4828c06` | 4029：`py:test`✅ → 5 image✅ → **`deploy:entan-api`✅（05:04）**、`deploy:api`✅、`deploy:worker`✅（`deploy:entan-worker`/`deploy:innov`=manual 未跑，不影响 entan-py） | ✅ | `gkxlumen-platform-entan-py-68bf4d5f66-4xfcv` image=`9e363f67`（dev HEAD；后续 `30685b5`/`9e363f6` 两 commit 均未动 `vendor/entan-py`，`git diff --stat` 验证）started=06:32 ✅ |
| lumen-svc-platform | `f4b2ccb` | 4030 本身 image/deploy 全 skipped；**同 dev 线后续 pipeline 4034（`2745799`，`git merge-base --is-ancestor` 验证 f4b2ccb 为其祖先）将 9 服务 deploy ✅（06:44–06:47）** | ✅（含本单代码） | `topic-async-service` image=`27457998` started=06:44 ✅；**⚠️ `gkxlumen-platform-topic`（门面层）image=`latest` started=2026-10-31 未滚**——`deploy:topic` 挂 `deploy_full_only_rules`（CI L77-85：仅 `FULL_PIPELINE=true`），不在日常自动发清单 |
| lumen-ui-topic | `4397e0c` | 4035：build✅ → image✅ → **`deploy:k8s`✅（07:20:36）** | ✅ | `gkx-lumen-topic-6486c74c85-q5pfc` image=`4397e0c1` started=07:20:30 ✅ |

> pipeline `status=manual` 为该仓 CI 设计（deploy 后置 manual 点名 + e2e allow_failure），按 job 级状态判定，不影响 deploy 绿结论（E1/E0 同口径先例）。

## 2. 逐项判定表

### 步骤 1 活力三档（P1-1）——4 绿 1 红

> 全部集群内直打 `GET http://10.96.3.124:8000/internal/v1/synth/vitality/batch-snapshot?region=深圳市&compare=全国重点城市&window=最近3年`（URL 百分号编码；E1 先例：中文未编码会请求行损坏）。

| # | 断言 | 判定 | 证据（HTTP 码 + 响应摘要） |
|---|---|---|---|
| 1a | 缺省 → 200，`weight_profile=INDEX_MAIN` 且 `vitalityIndex≈75.1478`（seed 真批非 74.9981 旧值） | 🟢 | HTTP 200 code=0；`snapshotId=snap:mock_20261106_vit_seed`、`calc_batch_id=mock_20261106_vit_seed`、`batch_reason=null`、外壳/`result.weight_profile` 均=`INDEX_MAIN`、**`vitalityIndex=75.1478`**；dimScores 四维 score 出数（industry 77.7925/policy 92.3/talent 56.2/tech 73.7，weight 0.3/0.2/0.2/0.3，confidence=ads_batch）；indicators 12 行（`ind-hte` rawValue=15683 score=100；缺维行 `caliber=missing` score=null confidence=null 不补 0）；gradeNote=「ADS 批次装包(synth_vit_* 同批同 profile 只读…)」——**seed 真批替代 mock_vit_latest 兜底已生效** |
| 1b | `weight_profile=EQUAL` → 200 回显 EQUAL 且 ≈74.9981 | 🟢 | HTTP 200；外壳/`result.weight_profile`=`EQUAL`、**`vitalityIndex=74.9981`**、同批同 seed、cache_key 第四段=EQUAL |
| 1c | `weight_profile=WEIGHT_MAIN` → 200 回显 ≈74.4224 | 🟢 | HTTP 200；`weight_profile=WEIGHT_MAIN`、**`vitalityIndex=74.4224`** |
| 1d | `weight_profile=bogus` → HTTP 400 | 🟢 | **HTTP 400**；`{"code":1,"msg":"WEIGHT_PROFILE_INVALID: 'bogus'(合法值:INDEX_MAIN/WEIGHT_MAIN/EQUAL,大小写敏感)"}`——真 HTTP 码（非 200 包错）已生效 |
| 1e | 显式 `snapshotId=snap:mock_20261106_vit_seed` 直读 → 按行内档回显出数 | 🔴 | HTTP 200 出数，但**回显档与数值行错位**：外壳/`result.weight_profile`=`EQUAL` 而 `vitalityIndex=75.1478`（该数值属批内 INDEX_MAIN 行；EQUAL 行值=74.9981，见 1b 同批对照）。违反 CHAINFIX-PY §2.3「profile 从行内回读并回显」+「禁 EQUAL 算标 INDEX_MAIN」——标签标了 EQUAL、数值却来自 INDEX_MAIN 行，两者未同源。根因指向 `api/synth_vitality_routes.py` `_batch_profile()`（回读行内档）与 `_ads_read()`（按档取数）不同源：前者解析出的档与后者实际过滤/取值的档不一致 |

### 步骤 2 协同任务链（P1-3）——绿

| 断言 | 判定 | 证据 |
|---|---|---|
| POST 任务（`region_innovation_collaboration`，经 async-service `10.96.0.84:7094`）→ 受理且非「不支持类型」 | 🟢 | `POST /topic/v1/analysis/tasks` body=`{analysisType:region_innovation_collaboration, params:{region:深圳市,compare:全国重点城市,window:最近3年}}` → HTTP 200（PigX R 包络惯例，非字面 202；受理语义以 code=0 为准）、`code=0`、`taskId=ANA-20261106-001`、`subType=region_innovation_collaboration`——白名单已放行，无「不支持类型」拒绝 |
| 轮询终态 | 🟢 | 响应即终态 `status=success`（同步终态模型）；`reused=false`、`batchComputedAt=2026-11-06 15:28:44` 为本请求实跑；三段指纹 `analysis_fp=深圳市\|全国重点城市\|最近3年` 双写（`analysis_fp_leg` 同值，CHAINFIX-JAVA §1.A 落地） |
| `resultData` 含 snapshotId | 🟢 | `targetParams.result_payload.snapshotId=batch:深圳市\|全国重点城市\|最近3年\|none`（`calc_batch_id=null` 时 snapshotId 尾段兜底 `none`；批号顶层冻结 `calc_batch_id=ANA-20261106-001` 兜底 taskId 路径，与②站 handoff §1.A③ 一致）；`relationInput` 真数（jointPatent=6477/talentFlow=18553）；空态诚实（`clustersReason=cluster_rule_unclosed`/`strategiesReason=strategy_llm_unavailable`/effectEval `reason=batch_not_published` openRef=Q-SYNTH-C-03，缺行 null 不补 0） |

### 步骤 3 协同门面 + graph（P1-4/P2-c）——Python 侧 3 绿，Java 门面 2 未测

> Java 门面 `http://10.96.2.89:7092/topic/v1/synth/**` 直打全部 401「访问令牌不存在」（对照：不存在路径同 401 → 认证掩蔽一切，无 token 无法区分路由），且 pod 为 10-31 旧镜像（§1 ⚠️）。

| # | 断言 | 判定 | 证据 |
|---|---|---|---|
| 3a | Python graph：非法 `limit_nodes=999` → 400 LIMIT_INVALID | 🟢 | `GET 10.96.3.124:8000/internal/v1/synth/collaboration/graph?...&limit_nodes=999` → **HTTP 400** `{"msg":"LIMIT_INVALID: limit_nodes=999(1~200)"}` |
| 3b | Python graph：必填缺失 → 400 | 🟢 | 缺 region → **HTTP 400** `REGION_UNMAPPED: ''(当前映射:深圳/广州/东莞/惠州)` |
| 3c | Python graph：正常 → 200 空图 `reason=batch_meta_missing`（非 graph_upstream_unavailable）；无 gapfill_batch_id | 🟢 | HTTP 200 code=0；`nodes=[] edges=[] truncated=false reason=batch_meta_missing`；data 顶层键集 `[calc_batch_id,compare,edges,graph_batch_id,nodes,reason,region,snapshotId,truncated,window]` **不含 `gapfill_batch_id`**——Python 端点已实现且旧降级 reason 消失 ✅ |
| 3d | Java 门面 `GET /topic/v1/synth/collaboration/batch-snapshot` → 200 九列含 isLatest | ⚪ 未测 | 401 掩蔽 + `gkxlumen-topic` pod 未滚动（本单新门面不在旧镜像）——双阻碍，见 §3 |
| 3e | Java graph 门面透传（entity/relation/limit 400 原文） | ⚪ 未测 | 同上 |

### 步骤 4 elements 回读（P1-5）——绿（含 1 观察项）

| # | 断言 | 判定 | 证据 |
|---|---|---|---|
| 4a | 显式 `snapshotId=snap:mock_20261105_elem_seed` → 按批回读不跳最新 | 🟢 | HTTP 200；`snapshotId=batch:深圳市\|全国重点城市\|最近3年\|mock_20261105_elem_seed`、`calc_batch_id=mock_20261105_elem_seed`、`batch_reason=null`、compositeIndex=77.6829/typeIndex=85.8575（与 E1 基线一致）——旧批精确回读 ✅ |
| 4b | 观察：elements 传不存在批（`snap:mock_20261106_vit_seed`） | 🟡 注记 | HTTP 200 回落条件批 `mock_20261105_elem_seed`（跨域批号视为无该批行→回落条件批）。elements 域无「显式批不存在→空壳」契约（活力域有 `batch_not_published` 空壳），域间行为不一致；派单未列此项，不动判定，登记为域间口径注记交 coordinator 定夺 |

### 步骤 5 HTTP 语义抽测（P1-7）——2 未测（Java 层）+ Python 层注记；502 跳过

| # | 断言 | 判定 | 证据 |
|---|---|---|---|
| 5a | 活力缺 region → HTTP 400 | ⚪ 未测 | **P1-7 本体在②站 Java 门面**（`SynthVitalitySnapshotService` REGION_AND_COMPARE_REQUIRED）；pod 未滚 + 401 掩蔽。Python 层注记：路由参数有缺省值（`region="深圳"` 等，源码 L294），缺参归一 200 属①站设计分工，非缺陷 |
| 5b | elements 不存在快照 → HTTP 404 | ⚪ 未测 | 同上（404 owner=`SynthElementsSnapshotService` SNAPSHOT_NOT_FOUND）。Python 层注记：不存在批 200 回落（见 4b） |
| 5c | Python 停机 → 502 | ⏭ 跳过 | 停机模拟不可行（会影响同 pod 其它叶且恢复有风险），按派单预告注明。502 分支已有②站 8 个单测断言锚（CHAINFIX-JAVA §1.E） |
| — | 补充：400 真码族已实测 | 🟢 | weight_profile 非法/limit 越界/region 未映射三例均真 HTTP 400（1d/3a/3b）——「②站已改真 HTTP 码」在 Python 上游侧成立；Java 门面 400 透传语义待 3d/3e 补测一并确认 |

### 步骤 6 FE 冒烟（构建产物级）——3 绿

| # | 断言 | 判定 | 证据 |
|---|---|---|---|
| 6a | dev 前端 URL 200 | 🟢 | `GET http://10.50.69.111:30892/` → HTTP 200；entry `assets/index-RXzDSG5X.js` |
| 6b | FE pod 新镜像 | 🟢 | `gkx-lumen-topic` pod image=`gkx-lumen-topic:4397e0c1` started=07:20:30（deploy:k8s 07:20:36 完成后滚动） |
| 6c | 构建产物 grep `weight_profile`（新 bundle 已发布） | 🟢 | entry chunk hits=1；`RegionalInnovationVitality-CwkcYOJy.js`：weight_profile×1 + 三档枚举（INDEX_MAIN×9/WEIGHT_MAIN×2/EQUAL×2）+「快照档」×1/「权重档」×4 文案——F1 三档 UI/回显代码在 prod bundle；`CollabWorkbenchView-XAtikkyg.js` isLatest×1——F7 isLatest 代码在 prod bundle ✅ |

## 3. 红项失败分类（C1–C6）与修单建议

### 红项 1（步骤 1e）：显式批直读档标签与数值行错位 — **C1（产品/代码 · Python 层）**

- **缺陷包**：
  - 复现：`GET http://10.96.3.124:8000/internal/v1/synth/vitality/batch-snapshot?region=深圳市&compare=全国重点城市&window=最近3年&snapshotId=snap:mock_20261106_vit_seed` → 200 `{weight_profile:"EQUAL", result.vitalityIndex:75.1478}`（期望 EQUAL↔74.9981 或按批内既有档自洽）
  - 期望 / 现象：按行内档回显**出数且档与数值同源**；实际标签 EQUAL、数值 INDEX_MAIN 行
  - 怀疑层：**Python（algorithm）**——`lumen-algo-py/vendor/entan-py/api/synth_vitality_routes.py` `_batch_profile()`（行内档回读）与 `_ads_read()`（按档取数）两处对「批内档」解析不同源（批内三档并存，回读取到的档 ≠ 取数用的档）
  - 修单：`lumen-algo-py` bugfix 一叶（算法侧小改）：显式批路径上「档解析」与「五表取数」用同一 profile 变量贯穿（`_batch_profile` 结果必须作为 `_ads_read` 的唯一档入参，禁止二次回落请求档/首行档）；补自检断言「显式批直读时 result.vitalityIndex == 该档 index 行 value」。边界：仅动 `synth_vitality_routes.py` 读取路径与自检脚本，不动 seed/DDL/算法包
  - 影响面：仅显式 `snapshotId` 回溯路径（FE 报告页/回跳直读场景）；三档常规路径（1a/1b/1c）不受影响
- **X-Trace-Id**：读路径直打（非任务链），无业务 trace；以复现命令代缺陷包 trace（同 E1 先例）

### 部署缺口（非测试红项，阻断 3 个未测项）— **C2（环境/发布配置）**

- **现象**：`gkxlumen-topic`（Java 门面层，`SynthSnapshotController` 所在）pod 镜像 `latest`、2026-10-31 启动——`f4b2ccb` 的 collab 门面新端点 + 四端点 HTTP 语义修正**均未在 dev 运行**；`deploy:topic` job 规则=`deploy_full_only_rules`（仅 `FULL_PIPELINE=true`），日常 dev push 自动发清单不含该模块（CI 注释：「完整运行才含 gateway/auth/upms/metrics/topic」）
- **影响**：步骤 3d/3e/5a/5b 四项断言无法 live 执行；FE F4（400/404/502 分支）在 dev 实际仍走旧 Java 行为
- **处置建议（coordinator）**：
  1. 新建 pipeline 带 `FULL_PIPELINE=true`（或等价点名方式）触发 `backend:image:topic` + `deploy:topic`，滚 `gkxlumen-topic:27457998`；
  2. 滚后补测 3d/3e/5a/5b 四项（外层 401 需 dev 测试 token，E1 §7.5 遗留项一并解决）；
  3. 如门面层发布节奏需常态化，建议将 `gkxlumen-topic` 移入日常自动发清单（架构师/coordinator 裁量，本单不改 CI）

## 4. 架构合规自检

| 铁律 | 自检 |
|---|---|
| 只测试不改代码 | ✅ 零代码改动；跳板机仅写 /tmp 探针文件（用后可删） |
| 调用链证据分层 | ✅ Python /internal 直打（A 级）+ async-service 任务链（A 级）+ FE bundle 静态分析（B 级）；未越层写数据 |
| D12 demo/lumen 隔离 | ✅ 全部打 lumen 集群（zhipu-tts 命名空间），未触碰 demo 服务 |
| 期望未发生必红 | ✅ 1e 判红未以「200 出数」收成 PASS（回显口径是派单明示断言） |
| 失败分类先于派修 | ✅ C1×1 + C2×1，只出缺陷包不动代码 |
| SSH 熔断（禁探活，同意图 ≤2） | ✅ 全程 1 个连接复用，无探活命令；单命令失败（MCP namespace 名打错一次）即纠正重试，未连续空转 |
| commit 标注 | ✅ 本单无 commit / 无 push |

## 5. registry 回填

- 状态维持 `claimed`→`in_progress`（QA 复测单无独立 registry 叶时按派单挂靠；AV/推进由 coordinator 执行）。
- 本 handoff 只落盘不 push（派单「不 push」）。

## 6. cost

```yaml
ponytail: full
model_used: glm-5.3-Flash
estimated_tokens: 90000
actual_cost: 0.30
cost_warn: false
```

## 7. 移交 coordinator

1. **C1 修单**（Python）：红项 1 按 §3 派 `lumen-algo-py` bugfix；deploy 绿后只复测 1e 一断言。
2. **C2 发布**：`gkxlumen-topic` 门面层按 §3 滚动（FULL_PIPELINE 或点名），滚后补测 3d/3e/5a/5b（需 dev 测试 token 打外层 401 之后的门面，E1 §7.5 遗留一并闭环）。
3. 观察项 4b（elements 跨域批回落 vs 活力批空壳，域间不一致）：交 coordinator/架构师定夺是否统一口径。
4. algo-py pipeline 4029 的 `deploy:entan-worker`/`deploy:innov` 仍 manual 未点——不影响本单（entan-py=api pod 已滚），如 worker 侧有消费方再点名。

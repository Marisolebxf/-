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

## 8. C1 修复记录（SYNTH-CHAINFIX-C1-L01）

- **任务/执行**：SYNTH-CHAINFIX-C1-L01（bugfix · algorithm-agent 认领，supervised_by=human:黄敬洲；task-registry 已建单并推进 backlog→ready→claimed→in_progress）
- **时间**：2026-11-06 15:37 – 15:57（UTC+8）
- **修复 commit**：`68c70bf`（lumen-algo-py · dev · **本地已 commit 未 push**，按派单「不 push」）
- **触碰文件**（仅 2 个，工作区其他会话未提交改动未被触碰）：
  - `vendor/entan-py/api/synth_vitality_routes.py`
  - `vendor/entan-py/scripts/check_synth_vitality.py`
- **diff 摘要**（96 insertions / 15 deletions，同一 profile 变量贯穿，评审建议落地）：
  1. `_batch_profile()`：回读 SQL 改 `GROUP BY weight_profile_code ORDER BY weight_profile_code ASC LIMIT 1`——原 `calc_batch_created_at DESC` 在同批多档（seed 一批三档、created_at 同刻）下返回档**不确定**，是 1e 错位的根因之一；ASC 定锚后回读档确定化。
  2. `_read_rows(by_batch=True)`：WHERE 由 `batch+calc_status` 改为 `batch+weight_profile_code(=回读档)+calc_status`——原不过滤档导致 `idx_rows[0]` 按表扫描序取行（live 抽到 INDEX_MAIN 行 75.1478 而标签抽到 EQUAL），标签与数值**各选各的行**；现在取数行与回读档强制同源。
  3. `_ads_read()` 直读分支：`effective_profile = _batch_profile(...)` 回读档作为唯一档入参传 `_read_batch_result` → 外壳 `weight_profile` / `result.weight_profile` / dimScores 权重 / `M_SYNTH_VIT_WEIGHT` metric 全部用同一变量（无第二处解析点，grep 全仓确认调用点唯一）。
  4. 锚定语义注记：同批多档时回读锚 = `profile_code` ASC 字典序最小档（本 seed 批即 EQUAL；'E'<'I'<'W'）。回显档可能 ≠ 请求档，但**标签=实际读取档**恒成立，符合铁律「按哪档读标哪档」。
- **自检证据**（check_synth_vitality 全绿 `{"ok": true, "passes": "all"}`，新增 **[9] C1 断言组 15 条全 PASS**）：
  - 断言设计按修单要求：直读 seed 批（`calc_batch_id=mock_20261106_vit_seed`）分别带 `weight_profile=WEIGHT_MAIN/EQUAL/INDEX_MAIN` 三种请求 → 回显档=行内实际档（三请求锚集均为 `['EQUAL']`，确定无漂移）；`vitalityIndex` 与该档 seed 合成正本 `compose_index(label)` 互证（74.9981 精确一致，禁 EQUAL 标签出 INDEX_MAIN 75.1478）；WEIGHT metric 权重同档（0.25×4）。
  - 数值正本按文件路径加载仓根 `scripts/seed/seed_synth_vit.py`（check 的 sys.path 不含仓根，不走包 import）；seed 批就绪探测走应用自身 TestClient（本机可直连库，无需密码探针门控）。
  - 邻叶回归：`check_synth_elements.py` ✅（首跑偶发 2003 超时，重试绿）、`check_synth_collab.py` ✅（凭据经 `conf/settings.yaml db.mysql_password` 派生环境变量注入，未回显未硬编码）。
- **live 复测指引（待 coordinator）**：push `68c70bf` → pipeline → `deploy:entan-api` 滚 pod 后，重跑红项 1e 一条断言即可：`GET .../vitality/batch-snapshot?...&snapshotId=snap:mock_20261106_vit_seed` → 期望 `weight_profile` 与 `result.vitalityIndex` 同源（锚 EQUAL↔74.9981，或批内任一档自洽即可，不再出现 EQUAL 标↔75.1478 值）。
- **架构合规自检**：调用链未动（仍 Java→Python `/internal/*`，读 ADS 只读）✅；D18 无新增 mock 直返（读路径修复，非造数）✅；仅动读路径+自检脚本，未动 seed/DDL/算法包（修单边界遵守）✅；多会话保护（未 reset/未碰他人未提交文件，精确 add）✅；commit 带 `[agent:algorithm]` 标记 ✅。

```yaml
ponytail: full
model_used: glm-5.3-Flash
estimated_tokens: 120000
actual_cost: 0.35
cost_warn: false
```

## 9. C2 修复记录（SYNTH-CHAINFIX-C2-L01 · devops）

- **任务/执行**：SYNTH-CHAINFIX-C2-L01（发布配置修单 · agent:devops，supervised_by=human:徐滕强；registry 无独立叶，按派单挂靠 VERIFY 单，与 §0 口径一致）
- **时间**：2026-11-06 15:37 – 16:15（UTC+8）
- **修复 commit**（均已推 `origin/dev`，plumbing 构造——不触并行会话工作区与未提交文件）：
  1. `b2dbaf0` — 规则主体：`backend:image:topic`（`*image_full_only_rules` 锚点）与 `deploy:topic`（自带 rules 覆盖锚点）各加 `TOPIC_RELEASE=true` 门；`FULL_PIPELINE` 变量 description 补点名说明。
  2. `306b9c5` — 修正 commit 1 的次生缺陷：deploy:topic 曾加「普通 dev → manual」兜底规则，但普通 pipeline 中 `backend:image:topic` 是 `when: never`（job 不存在），`needs` 非 optional → **GitLab 拒绝创建整条 pipeline**（下述 4040/4044/4045/4049 四条秒败的根因）。已删该兜底；点名发布 = 建 pipeline 带 `TOPIC_RELEASE=true`（镜像+deploy 全自动，无需再点 manual）。
- **规则 diff 要点**（最终态）：`backend:image:topic` 在 `FULL_PIPELINE==true` 后插入 `- if: '$CI_COMMIT_BRANCH == "dev" && $TOPIC_RELEASE == "true"'`；`deploy:topic` rules 展开为 MR-never / tag(prod,manual) / FULL_PIPELINE(auto) / TOPIC_RELEASE(auto) / never——其余冷门服务（graph/datacatalog/metrics/gateway/auth/upms）零影响（YAML 展开断言验证 6 个 deploy 无 TOPIC_RELEASE 泄漏、无普通 dev 自动泄漏）。
- **过程事故与取证**：
  - commit 1 推送后，其 pipeline（4040）及他人 3 条 push pipeline（4044/4045/4049）**创建即 failed、0 job**（started_at=null、duration=0）。lint 按 ref 校验 `valid: true`（43 jobs）掩盖了无变量场景。
  - 根因定位：MCP `create_pipeline`（无变量对照实验）返回 400 `'deploy:topic' job needs 'backend:image:topic' job, but ... does not exist in the pipeline ... use needs:optional`。
  - 本地三场景模拟断言（普通 dev / TOPIC_RELEASE / FULL_PIPELINE）：image↔deploy needs 配对全部 OK 后才推 `306b9c5`；修复后常规 pipeline **4051 创建成功并 running**，job 列表正确排除 topic 两 job（回归验证）。
- **本轮手动触发（发布验证）**：本会话建 `TOPIC_RELEASE=true` pipeline 被 API 404 阻塞（GitLab `/api/v4/projects/:id/pipeline` 路由对 git 凭据不可用，同意图 2 次即停，未走面板）。**并行会话（同账号）按 VERIFY §3 建议 1 发起 FULL_PIPELINE pipeline 4050** 完成本轮触发——`deploy:topic`（job 27589）**success**：08:09:28→08:10:30（61.7s），runner `gkx-lumen`。
- **pod 滚动确认（K8s 实测，SSH zphz-jump）**：
  - 滚动前：`gkxlumen-platform-topic-6d46ccd6d9-2xtzx` 镜像 `latest`、5d20h（10-31 启动）——与 VERIFY §1 记录一致；
  - 滚动后：唯一 pod `gkxlumen-platform-topic-58b7d979f7-ccb8q`，`img=harbor.test.com/zp-tts/gkxlumen-topic:ba2f3feb`（pipeline 4050 产物 = dev HEAD ba2f3feb，含 `f4b2ccb` 全部门面改动），`started=2026-11-06T08:09:29Z`，`ready=true`；旧 pod 已被替换。
  - 跳板机 kubeconfig 副本已按技能收工清单删除（`/tmp/admin-kc.yaml`）。
- **多会话保护自检**：本地 dev 有他会话领先提交（`ee2f156`）与 5 个未提交业务文件（cms/analysis）——全程未触碰；两次均用 `git hash-object/mktree/commit-tree` 在最新 `origin/dev` 之上构造单文件提交，push 前 fetch 复核基线未移动（1 次 base 移动即重锚）。
- **架构合规自检**：调用链无改动 ✅；D12 不适用（纯 CI 配置）✅；发布路径沿用仓内 helm/set-image 惯例（`TOPIC_RELEASE` 对齐 `RESTART_TOPIC_ASYNC` 先例）✅；commit 均带 `[agent:devops]` ✅；SSH 禁探活、同意图 ≤2（kubeconfig 属主坑 1 次修正即过）✅。
- **遗留/移交**：
  1. VERIFY §3 四项补测（3d/3e/5a/5b）现可执行：pod 已滚 `ba2f3feb`，仍需 dev 测试 token 过外层 401（E1 §7.5 遗留，建议派 qa）；
  2. 后续 `gkxlumen-topic` 单服务发布：GitLab UI → Run pipeline → dev + `TOPIC_RELEASE=true`；
  3. 全量 16 镜像 pipeline 4050 仍在 running（graph/datacatalog 首次烘焙较慢），不影响本单 topic 结论。

```yaml
ponytail: full
model_used: glm-5.3-Flash
estimated_tokens: 130000
actual_cost: 0.40
cost_warn: false
```

## 10. 补测记录（C1/C2 落地后 · 2026-11-06 16:14–16:40 · qa）

- **触发**：SYNTH-CHAINFIX-C1-L01（PY `68c70bf`）与 C2（topic 门面 pod 滚 `ba2f3feb`）落地后的派单补测（5 项：T1 C1 复测 / T2 门面九列 / T3 graph 经 Java / T4 elements 404 / T5 400 语义）。**只测试不改代码**；零 commit / 零 push。
- **前置确认（A 级）**：`gkxlumen-platform-entan-py-78c86f5bcb-bb6zm` image=`68c70bfa` started=08:06:09Z ✅；`gkxlumen-platform-topic-58b7d979f7-ccb8q` image=`ba2f3feb` started=08:09:29Z ✅（kubectl 实测，pod 唯一）。

### 10.1 鉴权口径修正（推翻上轮「401 掩蔽」判断）

上轮 401 根因 = **旧镜像（10-31）里根本没有 synth 路由**：`PermitAllUrlProperties` 按 `@Inner(value=false)` 注解在启动时注册 ignoreUrls（permitAll），不存在路径落 `anyRequest().authenticated()` → 401。新 pod 已含 `SynthSnapshotController`（`/topic/v1/synth/**` 四端点全部 `@Inner(false)`），**集群内直打免 token**——上轮「需 dev 测试 token」（§7.5/E1 遗留）的预判不成立，本轮直打全部命中路由。

### 10.2 逐项判定（5 项：2 绿 1 绿(PY层) 4 红阻·同根因；证据路径见 10.5）

| 项 | 断言 | 判定 | 证据 |
|---|---|---|---|
| **T1a** | C1 复测 1e：`snapshotId=snap:mock_20261106_vit_seed`（带 `weight_profile=WEIGHT_MAIN`）→ 回显档=实际档 + 74.9981 禁 75.1478 | 🟢 | HTTP 200 code=0；`snapshotId=snap:mock_20261106_vit_seed`、外壳/`result.weight_profile` 均=`EQUAL`、**`vitalityIndex=74.9981`**、`cache_key` 第四段=`EQUAL`、`batch_reason=null`——**EQUAL 锚 ↔ 74.9981 同源，错位已修复**；上轮红项 1e 闭环 |
| **T1b** | 同直读改请求 `weight_profile=INDEX_MAIN` → 回显档仍 EQUAL（标签=实际读取档恒成立） | 🟢 | HTTP 200；请求 INDEX_MAIN、回显仍 `EQUAL`+`74.9981`——请求档不改变行内实际档，符合 C1 修单 §8 锚定语义（锚=`profile_code` ASC 最小档，'E'<'I'<'W'） |
| **T2** | Java 门面 collab batch-snapshot → 200 + 九列（snapshotId/calc_batch_id/graph_batch_id/cache_key/region/compare/window/publishedAt/isLatest） | 🔴 阻断 | HTTP **502** `UPSTREAM_ERROR`（R 包络）——Java→Python 调用失败，见 10.3 C3；**非门面代码缺陷**（本地校验分支已另行实测语义正确：缺 region/compare → 400 `REGION_AND_COMPARE_REQUIRED`） |
| **T3a** | Java graph 门面 → 200 空图 reason=batch_meta_missing 或 no_year_on_source | 🔴 阻断 | 同上 502（C3）；本地分支已证：缺 window → 400 `REGION_COMPARE_WINDOW_REQUIRED`（graph 必填语义在位） |
| **T3b** | graph 带 `gapfill_batch_id`（参数已废止）→ 400 或 400 级 | 🔴 阻断 | 同上 502（C3）。⚠️ **预期风险预登记**：Python graph 形参清单（`synth_collab_routes.py` L64-75）无 `gapfill_batch_id`，FastAPI 默认忽略未知 query 参数 → C3 修复后复测**大概率 200 正常空图而非 400**。契约「无此参数」= 正确态；「带废参数须 400」若为硬要求需另立校验单 |
| **T4a** | elements 显式不存在批 `snapshotId=snap:never_exists` → HTTP 404 SNAPSHOT_NOT_FOUND | 🔴 阻断+预判缺陷 | 同上 502（C3）。⚠️ **代码级预判（C3 修复后仍会红）**：`SynthElementsSnapshotService` **无 `batch_not_published→404` 映射分支**（grep 全 service 仅活力服务有，L199-203）；Python 层实测（T4b）该场景回 `calc_batch_id=never_exists`（非 null）+ `batch_reason=batch_not_published` → Java 现行逻辑不触发「calc_batch_id 空→404」→ 预期 **200 空壳而非 404**。修法建议：elements 服务照活力服务补一条同款映射（小改），随 C3 修单一并派 |
| **T4b**（补充佐证） | Python elements 层：显式不存在批 → 200 空壳 + batch_reason（不回落） | 🟢 | HTTP 200；`snapshotId=batch:深圳市\|全国重点城市\|最近3年\|never_exists`、`batch_reason=batch_not_published`、**未回落**最新批 `mock_20261105_elem_seed`——PY 域语义正确（契约分工：空壳在 PY、404 在 Java，Java 侧缺映射见 T4a 预判） |
| **T5** | 活力缺 region（或 window 非法）→ HTTP 400 errorCode（非 200） | 🟢 | 缺 region（`region=`空串，注：路由形参带默认值，完全不传参不会进 Java 校验分支，空串为等效触发）→ **HTTP 400** `{"code":1,"msg":"REGION_AND_COMPARE_REQUIRED"}`；加测 `window=bogus` → **HTTP 400** `WINDOW_INVALID`——5b 400 语义全绿 |

**汇总：T1 ✅（C1 修复 live 生效）· T5 ✅ · T4 Python 层佐证 ✅ · T2/T3a/T3b/T4a 🔴（同一环境根因 C3，非门面代码缺陷；门面本地校验语义已另行取证）**

### 10.3 红项分类：C3（环境/发布配置 · 阻断 4 项）

- **缺陷包**：`gkxlumen-platform-topic` Deployment env `TOPIC_ALGO_BASE_URL=http://127.0.0.1:8000`（deploy yaml 实测）——容器内 127.0.0.1 无 Python；Java 日志 `synth collaboration snapshot/collab graph/elements snapshot upstream failed status=-1`（16:32:33–16:32:46，与探针时刻吻合）→ 502 UPSTREAM_ERROR。502 本身 = E 项设计语义**正确**（连接级失败转 502 不泄漏堆栈），错在寻址配置。
- **对照**：同集群 `topic-async-service` 同类键指向 `http://gkxlumen-platform-entan-py:8000`（deploy env 实测）；仓内 helm configs 亦无 `gkxlumen-topic`（biz）的 Nacos 配置文件（仅 policy/innov/async/chain 有），`RemoteSynthPythonClient` 的首选键 `gkxlumen.topic.synth.algo-base-url` 全仓无定义 → 生效值就是 env 的 127.0.0.1。
- **修法建议（coordinator 派单，二选一）**：① deploy/helm 给 `gkxlumen-platform-topic` 注入 `TOPIC_ALGO_BASE_URL=http://gkxlumen-platform-entan-py:8000`（与 async-service 同款）；② 新增 helm config `gkxlumen-topic-biz-dev.yml` 定义 `gkxlumen.topic.algo-base-url`（策略口径同 `gkxlumen-topic-policy-biz-dev.yml` 先例）。修后需重启 topic pod，并复测 T2/T3a/T3b/T4a 四项（T4a 预计另需 10.2 所列 elements 404 小改）。

### 10.4 架构合规自检

只测试不改代码 ✅（零 commit/push）；调用链证据分层 ✅（PY `/internal` 直打 + Java 门面直打，未越层写数据）；D12 ✅（全打 lumen 集群 zhipu-tts，未触 demo）；期望未发生必红 ✅（T2/T3/T4a 判红未以「路由通了」折算 PASS）；失败分类先于派修 ✅（C3×1 + 预判缺陷×1 + 预期风险注记×1）；SSH 熔断 ✅（禁探活，各意图 ≤2 次：kubeconfig 属主修正 1 次即过；SFTP 上传失败后改 heredoc 1 次即成，未连续空转）。

### 10.5 证据路径（集群内直打，跳过外层网关——无 token 场景按派单指引执行）

- 跳板机 zphz-jump；kubeconfig=`/tmp/admin-kc.yaml`（sudo 副本，收工已删）
- Python 直打：`http://10.96.3.124:8000`（svc `gkxlumen-platform-entan-py`，pod 68c70bfa）
- Java 门面直打：`http://10.96.2.89:7092`（svc `gkxlumen-platform-topic`，pod ba2f3feb）
- 探针脚本 `/tmp/synth_retest.sh`（9 请求 + JSON 摘要，中文 URL 百分号编码，收工已删）；Java pod 日志：`kubectl logs gkxlumen-platform-topic-58b7d979f7-ccb8q -n zhipu-tts`（status=-1 WARN 行）

```yaml
ponytail: full
model_used: glm-5.3-Flash
estimated_tokens: 110000
actual_cost: 0.32
cost_warn: false
```

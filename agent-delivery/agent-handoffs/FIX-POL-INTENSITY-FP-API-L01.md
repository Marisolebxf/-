# FIX-POL-INTENSITY-FP-API-L01 Handoff

政策 Job 服务端补 `analysis_fp` 兜底：display `toAsyncCreateBody` 缺指纹自动派生。

- **task-id**: FIX-POL-INTENSITY-FP-API-L01
- **执行**: agent:api-agent · **监管**: human:淮政玮 · **认领类型**: pull
- **仓**: lumen-svc-platform（gkxlumen-display）
- **强度**: ponytail full
- **状态**: 改动停在本地工作区，**未 commit / 未 push**，等人工验收（AGENTS.md 验收闸门）

## 范围与实现

线上 bug（trace `2c4a45ceebc0b53b5b28cceaac53cc63`，与前端单 `FIX-POL-INTENSITY-FP-L02` 的 `4fa75276…` 同根因）：
`POST /display/v1/policy/panorama/jobs` 全链 HTTP 200，但 async-service 返回业务 `code:1 "analysis_fp 不能为空"`、`taskId:null`。
根因：async-service（2026-09-02 `6b91104` 起）对**全部政策类任务**走 `createFingerprintGatedTask` 强校验 64 位 SHA-256 指纹；
而前端仅 223/226（evaluationWiring.ts）带指纹，209/212/214/218 入口（intensityJobBodyOf 等）全缺 → 必挂。
「偶尔能成功」= 按钮分：带指纹的入口能成，不带的必挂，与区域个数无关。

**选方案 A（服务端兜底）**：与前端单（方案 B，另一会话已认领 in_progress）不同仓互补——前端带了就透传，服务端只在缺失时派生。

### 改动（3 文件，+106/-1 行）

1. `PolicyPanoramaService.java`
   - 新增静态 `ensureFingerprint(out)`：`analysis_fp` 缺失时按 `analysisType + params` 规范化 JSON（TreeMap 递归键排序，list 保序）派生 SHA-256 小写 hex 注入；已带指纹原样透传。
   - `deriveFingerprint`：`CANONICAL_JSON.writeValueAsString(List.of(analysisType, sortedParams))` → `hexSha256`；失败返回 null 不注入（由 async 闸门照常拒绝，错误不吞）。
   - `toAsyncCreateBody` 尾部调用 `ensureFingerprint`；白名单不变（含 `policy_region_diff`）。
2. `PolicyEvaluationService.java`
   - `toAsyncCreateBody` 同样在尾部调 `PolicyPanoramaService.ensureFingerprint(out)`（自保留白名单闭集，不委托整方法，避免把 223/226 类型集并到全景）。
3. `PolicyPanoramaServiceTest.java`
   - `missingFingerprintIsDerivedAndProvidedOnesPassThrough`：缺指纹→64 位小写 hex；同条件（键序不同）→指纹一致；不同条件→指纹不同；带指纹→透传。
   - `evaluationJobsAlsoGetDerivedFingerprint`：evaluation 缺指纹兜底；带指纹透传；`policy_region_diff`（全景专属）在 Evaluation 仍拒绝（白名单不扩大）。

## 验证（远程编译环境，本机无 JDK/Maven）

- Jenkins 跳板机 `/tmp/lumen-svc-verify`（JDK17 + maven 3.9.16）浅克隆 origin/dev（`df497dc`），snippet 传 patch 后 `git apply`（CRLF→LF 修正后干净落地）。
- `mvn -pl gkxlumen-display -am test -Dtest='PolicyPanoramaServiceTest,PolicyEvaluationServiceTest'`：
  **`Tests run: 27, Failures: 0, Errors: 0` → BUILD SUCCESS**（Evaluation 13 绿 + Panorama 14 绿）。
- 验证用临时 clone / 日志 / 3 个 GitLab snippet 已全部删除（snippet 1/2/3 HTTP 204）。

### 中间轮次（已修复）

第一轮 2 个失败均为**测试断言写错**（非生产代码问题）：`policy_focus_ads` 不属 Panorama 白名单（改用 `policy_effect` 测透传）；`policy_intensity` 本就在 Evaluation 白名单（改用 `policy_region_diff` 测闭集）。

## 架构合规自检

- 调用链：前端 → display REST → async `/topic/v1/analysis/tasks` → Python `/internal/policy/jobs/execute`，未越层 ✅
- Java 不做算法：SHA-256 指纹派生是请求规范化/幂等控制，非 NLP/图谱/模型推理 ✅
- D9/D18：无 mock、无硬编码数据；指纹口径 = analysisType+params 规范化 JSON，确定性可复算 ✅
- I2-12 语义：同条件同指纹当天幂等复用、单飞不破坏；`force` 仍可绕过当天成功复用 ✅
- 多会话保护：未触碰 `lumen-ui-science-pc`（前端单另一会话 in_progress 中）✅

## 偏离说明

无。派单包内 touched_files 与实际一致。

## 后续 / 开放项

- 验收通过后 commit message 建议：`fix(policy): display 补政策 Job 缺省 analysis_fp 兜底派生 [agent:api-agent]`
- 前端单 FIX-POL-INTENSITY-FP-L02 修完后，两单互不冲突：前端带指纹 → 服务端透传原值。
- 生产发布：走 origin/dev 常规 CI（K8s dev rollout）。
- 遗留（不在本单）：BenchmarkCompareModal「部分字段获取失败」横幅 = element `gapfill_policy_eval_shell` 缺列，独立问题。

## cost

- actual_tokens: ~90000（含远程编译多轮等待）
- model_used: glm-5.3-flash
- actual_cost: ~0.9
- cost_warn: green

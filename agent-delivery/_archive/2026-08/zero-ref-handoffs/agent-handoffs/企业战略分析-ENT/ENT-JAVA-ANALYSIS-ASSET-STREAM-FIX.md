# ENT-JAVA-ANALYSIS-ASSET-STREAM-FIX — 分析任务 /asset 下载返回空 JSON {} 修复

> **task-id**：`ENT-JAVA-ANALYSIS-ASSET-STREAM-FIX`
> 派单：`[agent:qa-agent]` → **api-agent**（监管 `human:侯佳伟`）
> 日期：2026-08-07
> 仓：`lumen-svc-platform` / `gkxlumen-topic-async-service`
> commit：`00550e4` — `fix(topic-async): asset 返回类型改为 ResponseEntity<StreamingResponseBody> 修复空 JSON {}`
> 分支：`origin/dev`

---

## 1. 根因（QA 已确认）

`AnalysisTaskController.asset` 方法返回类型声明为 `ResponseEntity<?>`（通配符泛型）。
当 `shouldProxy` 路径返回 `ResponseEntity.ok().body(StreamingResponseBody)` 时，由于泛型被擦除为 `?`，
Spring 的 `StreamingResponseBodyReturnValueHandler` **无法匹配**该返回值（它要求
`ResponseEntity<StreamingResponseBody>` 具体泛型），于是 fallback 到普通 `HttpEntityProcessor`，
把 `StreamingResponseBody` lambda 当成普通 POJO 交给 Jackson 序列化。

`StreamingResponseBody` 是函数式接口（仅 `writeTo(OutputStream)` 方法），无可序列化字段 →
Jackson 输出 `{}`（2 字节空 JSON）。

**现象**：`GET /api/topicAsync/topic/v1/analysis/tasks/{id}/asset` 返回 `Content-Length=2` 的 `{}`，
而 MinIO 直连可读完整结果（QA 证据 EVAL-20260807-006 resultSize=4682、REC-20260807-007 resultSize=5122）。

**Service 层无问题**：`AnalysisAssetServiceImpl.writeResult` 是纯 MinIO 流拷贝
（`input.transferTo(output)`），代码正确。问题仅在 Controller 返回类型声明。

---

## 2. 改动点

### 2.1 `AnalysisTaskController.java`

| 位置 | 修改前 | 修改后 |
|---|---|---|
| 方法签名 | `public ResponseEntity<?> asset(...)` | `public ResponseEntity<StreamingResponseBody> asset(...)` |
| 404 路径 ×3 | `ResponseEntity.notFound().build()` | `ResponseEntity.<StreamingResponseBody>notFound().build()` |
| 302 路径 ×1 | `ResponseEntity.status(302)...build()` | `ResponseEntity.<StreamingResponseBody>status(302)...build()` |
| 流式路径 ×1 | 不变（已 `ResponseEntity.ok().body(body)`） | 不变 |

核心：把 `?` 改为 `StreamingResponseBody`，404/302 路径用显式泛型方法调用
`ResponseEntity.<StreamingResponseBody>notFound()` / `ResponseEntity.<StreamingResponseBody>status(302)`
保持类型信息不丢，让 `StreamingResponseBodyReturnValueHandler` 正确识别并走流式写出。

### 2.2 新增测试 `AnalysisTaskControllerAssetTest.java`

3 个用例（Standalone MockMvc，不依赖 Spring Context / DB / Nacos）：

1. `assetReturnsStreamingBodyNotEmptyJson` — **核心回归**：构造 success 任务 + 模拟 Service 写出已知 JSON，
   断言响应体 ≠ `{}` 且包含实际内容（score/taskId）。
2. `assetReturns404WhenTaskNotFound` — 任务不存在返回 404。
3. `assetReturns404WhenTaskNotSuccess` — 非 success 状态返回 404。

**测试报告**：`Tests run: 3, Failures: 0, Errors: 0, Skipped: 0`（2.793s）

---

## 3. 验证证据

| 项 | 证据 |
|---|---|
| commit | `00550e4` 已 push `origin/dev`（`1921761..00550e4 dev -> dev`） |
| 编译 | Maven 3.9.6 + JDK 17（Zulu 17.0.9），`-pl ...async-service-biz -am test` 通过 |
| 单测 | surefire 报告 `Tests run: 3, Failures: 0, Errors: 0` |
| 回归断言 | `assertNotEquals("{}", body)` + `assertTrue(body.contains("\"score\":87"))` |

> 联调实测待 K8s dev rollout 后由 QA 复测 EVAL-20260807-006 / REC-20260807-007 两个任务的 `/asset` 端点。

---

## 4. 架构合规自检

| 规则 | 合规 |
|---|---|
| 调用链 前端→Java REST→Python /internal/* | ✅ 不变（Java 代理 MinIO 流，未越层） |
| 算法只在 Python | ✅ 不涉及算法 |
| 图谱 NebulaGraph | ✅ 不涉及 |
| 可观测性 | ✅ 审计日志 `analysisAuditLogger.audit` 保留 |
| CI/CD | ✅ push origin/dev 触发 pipeline |
| commit 标记 | ✅ `[agent:api-agent]` |
| 不改配置文件 | ✅ 仅改 Controller + 新增 Test |

---

## 5. cost

| 字段 | 值 |
|---|---|
| actual_tokens | ~25_000 |
| model_used | glm-5.2 |
| actual_cost | ~$0.15 |
| cost_warn | ok（< $10） |

---

## 6. 状态

- task-registry 当前状态：`ready`（MCP task-registry 服务本次会话不可用，无法直接 `task-claim` / `task-update-status`）
- 代码已完成 + push + 单测通过，待 coordinator 将状态推进到 `integration`（bugfix 路径 AV-0 目标 `pending_test`）
- 联调实测待 K8s dev rollout 后 QA 复测

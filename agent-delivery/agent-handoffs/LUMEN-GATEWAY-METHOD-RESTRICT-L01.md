# LUMEN-GATEWAY-METHOD-RESTRICT-L01 · 网关仅放行 GET/POST — 前端 16 处 PUT/DELETE 调用与后端 Controller 整改（含 Feign 链路）

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `human:孔东` |
| supervised_by | `human:孔东` |
| claim_type | `pull` |
| 说明 | 孔东会话内执行；2026-11-05 17:08 经 MCP 转 `in_progress`。**孔东裁定 2026-11-04：改动停本地工作区，未经确认不 commit/push** |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 纯 method/路由整改：复用仓内既有动词尾惯例（`/cancel`、`/publish`、`/unpublish`、`/delete`），零新增抽象/依赖；mock 按 api-id 分发与 method 无关，确认零改动成立。未用 YAGNI 跳过任何公约项（本任务不触 D8/D9/D10 视觉与指标） |

## 范围裁定（用户 2026-11-05 17:22）

- **只做 lumen-ui-topic 前端 + lumen-svc-platform 对应后端**（DoD 圈定文件集）
- science-pc（policy.ts 订阅 PUT/DELETE 2 处、display→policy Feign 链路）**范围外不动**

## 修改内容

### 路由规则（对齐仓内既有动词尾惯例，防 Spring 同 URL 跨 method 歧义映射）

| 旧 | 新 |
|----|----|
| `DELETE .../{id}` | `POST .../{id}/delete` |
| `DELETE .../batch` | `POST .../batch/delete` |
| `PUT .../{id}`（更新） | `POST .../{id}/update` |
| `DELETE`（模板归档） | `POST .../{id}/archive` |
| `PUT .../{id}/default` | `POST .../{id}/default`（仅换 method） |

### 前端 lumen-ui-topic（16 处调用 + paths 注释同步）

- `src/api/enterprise/compare.ts` ×6：#93 移除单个 / #94 批量清空 / #G1 招引移除 / #G2 招引批量 / #G3 培育移除 / #G4 培育批量
- `src/api/enterprise/evaluation.ts` ×3：#119 更新 `/update`、#120 归档 `/archive`、#121 设默认（method 换 post）
- `src/api/enterprise/analysisTask.ts` ×1：#G6 删除 `/{taskId}/delete`
- `src/api/industry/chainUx.ts` ×2：产业篮移除单个 / 批量
- `src/api/service/index.ts` ×2：#S4 机构移除 / #S5 批量
- `src/api/cms/cmsOps.ts` ×2：update → `/{id}/update`、delete → `/{id}/delete`
- `src/api/enterprise/paths.ts`、`src/api/service/paths.ts`：契约注释同步（不留 PUT/DELETE 死路由描述）
- **Mock 零改动**：`defineApi` 按 `id` 注册分发（`src/utils/http.ts`），与 URL/method 无关，入参对象字段未变（user_id 仍走 query）——`src/mock/register.ts` 及各 mock 实现无需变更

### 后端 lumen-svc-platform（10 Controller/Feign + 1 测试）

| 文件 | 改动 |
|------|------|
| `CompareBasketController` | 8 处 DELETE → POST（items 单/批、招引/培育单/批、org-items 单/批） |
| `ChainUxInternalController`（Feign 落点） | 2 处 DELETE → POST |
| `AnalysisTaskController` | #G6 DELETE → POST `/tasks/{taskId}/delete` |
| `EvaluationTemplateController` | #119 PUT→POST `/update`、#120 DELETE→POST `/archive`、#121 PUT→POST `/default` |
| `IndustryChainUxController`（topic-chain 门面） | 2 处 DELETE → POST |
| `SvcCompareBasketController` | 2 处 DELETE → POST |
| 4 × CMS OpsController（OpsContent / TopicPolicy / TopicPanorama / TopicService） | 各 PUT→POST `/update`、DELETE→POST `/delete` |
| Feign：`RemoteChainUxClient` / `RemoteOrgCompareBasketClient` / `RemoteTopicSvcService` / `RemoteTopicAsyncService` | 同步注解与路径（调用方经 method 签名调用，签名参数不变，无调用方代码改动） |
| `IndustryChainUxControllerTest` | mockmvc delete → post 新路由 |
| 各文件清理无用 `@PutMapping`/`@DeleteMapping` import | — |

## 测试结果

- 前端 `npm run type-check`（vue-tsc）：**绿**（17.5s）
- 前端 `npm run build`：**绿**（built in 24.97s，仅既有 chunk 大小警告）
- 前端自检 `node scripts/portal-wire-check.mjs`：`portalWire ok`
- 前端自检 `analysis-task-gate.test.mts`（alias-loader）：**11/11 pass**
- Mock 路由防漏：`src/api` 全目录 grep `method: 'put'|'delete'` → **0 残留**
- 后端防漏：任务圈定 Controller/Feign grep `@(Put|Delete)Mapping` → **0 残留**；test 目录仅剩 policy 订阅（范围外）
- **后端 mvn 编译：未执行**（本机无 JDK/Maven；按孔东裁定停本地不推，编译验证待确认后 push 走 CI）

## 遗留风险

1. **前后端需同批发布**：路由已改，旧后端收到新 POST 路由会 404/405；联调须前后端同版本（DoD 联调项待 dev 环境部署后执行）
2. **范围外 PUT/DELETE 仍存在**（网关真正收紧前需另行处理，本任务不覆盖）：
   - `lumen-ui-science-pc/src/api/policy.ts` 订阅 update/cancel 2 处（经网关 `/display/v1/policy/panorama/subscriptions`；对应 display `PolicyPanoramaSubscriptionController`、`RemotePolicySubscriptionClient`、policy `PolicyFacadeController` 及其测试）
   - `lumen-ui-admin`（upms 后台）大量 PUT/DELETE（约 125 处；admin 是否经同一网关收紧策略需确认）
   - `gkxlumen-auth` 登出 `DELETE /token/logout`（admin 前端在用；topic/science 前端未调用）
3. OpenAPI 契约文档（`API-ENT-full-catalog.md` 等）中 #93/#94/#G1–G4/#G6/#119–121 的 method 描述未逐条更新——契约文档属编排仓存量文档，建议由 coordinator 安排文档 agent 统一刷新（本次已同步前端 paths.ts 注释与后端 swagger `@Operation`）
4. dev 环境联调验证（DoD 第 3 条）与网关侧旧 method 405 确认（DoD 第 4 条）待部署后补

## CI/CD（必填）

- 分支：两仓 `dev`（**已确认提交并推送**，孔东 2026-11-05 17:40 放行）
- commit：
  - lumen-ui-topic：`c83b559`（merge 后 `5c50701` 推送，`0a87fef..5c50701 dev -> dev`）
  - lumen-svc-platform：`6db7c51`（`3e75227..6db7c51 dev -> dev`）
  - git author 已按 `.env` 修正为仓级 `kongdong <dong.kong@aminer.cn>`（原全局误拼 `kondong`）
- pipeline：push 已触发 GitLab CI（后端编译验证在此补上；链接待 CI 出结果后由 coordinator/QA 回填）
- K8s rollout / dev URL：待 CI 部署后执行 DoD 第 3 条联调验证

## 涉及文件

**lumen-ui-topic**（9）：
- `src/api/enterprise/compare.ts`、`evaluation.ts`、`analysisTask.ts`、`paths.ts`
- `src/api/industry/chainUx.ts`
- `src/api/service/index.ts`、`paths.ts`
- `src/api/cms/cmsOps.ts`

**lumen-svc-platform**（15）：
- `gkxlumen-topic-enterprise`：`CompareBasketController`、`ChainUxInternalController`
- `gkxlumen-topic-async-service`：`AnalysisTaskController`、`EvaluationTemplateController`、`RemoteTopicAsyncService`
- `gkxlumen-topic-chain`：`IndustryChainUxController`、`RemoteChainUxClient`、`IndustryChainUxControllerTest`
- `gkxlumen-topic-svc`：`SvcCompareBasketController`、`RemoteOrgCompareBasketClient`、`RemoteTopicSvcService`
- `gkxlumen-cms`：`OpsContentController`、`TopicPolicyOpsController`、`TopicPanoramaOpsController`、`TopicServiceOpsController`

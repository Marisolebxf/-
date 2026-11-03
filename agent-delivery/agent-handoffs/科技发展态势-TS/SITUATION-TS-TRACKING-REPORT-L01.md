# SITUATION-TS-TRACKING-REPORT-L01 · 评估报告（HTML/PDF 生成、版式字体、导出图、复用与最近报告、清理）

> 任务：`SITUATION-TS-TRACKING-REPORT-L01` ｜ 状态：`integration`（等人工走查）｜ agent：`frontend-agent`
> 监管人：`human:孔东` ｜ 仓：`lumen-ui-science-pc` + `lumen-svc-platform` ｜ 日期：2026-11-03
> 设计说明真源：`repos/lumen-ui-science-pc/docs/tracking-真评估接入设计.md`（§7–§12）

## 1. 目标

结果页「下载报告」产出**可交付**的评估报告（HTML/PDF），并能复用、能自查历史产物、能清理。

## 2. 落地实现

| 环节 | 文件 · 方法 | 说明 |
|---|---|---|
| 采集 | `ResultDashboard#collectViewPayload()`（`defineExpose`） | 把五个视图转 base64 PNG，交给报告模板（服务端渲染不了 echarts） |
| 前端调用 | `src/api/situation/tracking.ts` · `generateTrackingReport` / `fetchTrackingReports` / `deleteTrackingReport` | 生成、列表、清理三件 |
| 弹窗 | `components/ReportExportDialog.vue` | 格式选择 + 「最近报告」（**上限 5 条**）+ 下载 + 清理（两段式确认） |
| display 网关 | `TrackingController#generateReport` / `#listReports` / `#deleteReport` / `#downloadReport` | `POST /report`、`GET /reports`、`POST /report-remove`、`GET /report/{id}/download`（文件流代理，中文文件名 `Content-Disposition`） |
| 域服务 | `TrackingEvaluationReportService#generate` / `list` / `deleteReport` + `TrackingReportRenderer` | 逻辑删除 `status=deleted` + 删本地产物；渲染模板 + 中文字体 |
| 表 | `tech_evaluation_report` | `report_id / run_id / format / storage / file_path / file_size / title / file_name / created_at / status` |

关键决定（已落地，不许回退）：

1. **复用优先**：同一 `runId + format` 已有产物 → `findReusable()` 直接返回（本地文件缺失才重生成），响应带 `reused=true`，前端提示「未重复生成」。
2. **OSS 对象不随清理删除**：`deleteReport` 只删本地产物 + 逻辑删除记录，OSS 由存储侧生命周期回收；返回 `note` **如实写明删了什么**，不谎报"已全部删除"。
3. **清理不进评估历史**：清理只影响报告产物指针，`tech_evaluation_history` 不动。
4. **二次确认两段式**（「清理」→「确认清理」）：不嵌套 Modal —— Arco 静态 `Modal.confirm` 在该组件树里 `onOk` 不触发（实测后端日志无任何请求），已改。

## 3. 实测证据（2026-11-03）

| 项 | 结果 |
|---|---|
| 生成 | `POST /report` → 本地存储 `1574 KB` HTML，`tech_evaluation_report` 落库 |
| 复用 | 同 run 同格式二次生成 → `reused=true`，未重复渲染 |
| 列表上限 | `GET /reports` 回 5 条；弹窗标「（最多 5 条）」 |
| 下载 | `GET /report/{id}/download` → 文件流，中文名正常（`filename*=UTF-8''…`） |
| 清理 | UI 两段式确认 → `POST /report-remove` → 提示「已清理「…html」：已删除本地产物并从列表移除」；DB `status='deleted'` 留痕（实测 active 5 / deleted 2） |

## 4. 遗留与风险

1. PDF 依赖服务端渲染环境（字体已内置，但换机器需确认字体包随包发布）。
2. 报告 `fileSize` 经 JSON 是**字符串**，前端已 `Number()` 兜住（别再写 `typeof === 'number'` 判断）。
3. 清理只删本地产物；若运行在 OSS 存储，对象保留 → 走查时需确认产品是否接受（当前按"保留"实现并明示）。
4. 演示轨（`USE_MOCK=true`）本模块**无 mock 注册**，会显式抛 `Missing API mock registration`（诚实失败），已在 `mock-ledger.md` 登记。

## 5. 纪律

⚠️ 人工验收闸门：改动全部停本地工作区，**未 commit / 未 push**，等 `human:孔东` / `human:唐绍祖` 走查通过后推送。

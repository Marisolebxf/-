# LUMEN-SVC-JAVA-SVC-REPORT-ARTIFACT-L01 · 服务链 8 分析页报告下载产物链（Java 侧）

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:api-agent` |
| supervised_by | `human:徐滕强` |
| claim_type | `pull` |
| 说明 | 认领/锁定 2026-10-26 20:44 +08:00，lock_until 2026-10-27 00:44 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 最小 diff：3 个主代码文件 + 1 个新测试文件；未加新依赖；未动前端；未动 Demo。未用 YAGNI 跳过架构铁律（Java 本地渲染不经 Python、不直连算法、结果只读父快照）。 |

## 问题清单（背景）

- 前端 `SvcAnalysisReportPanel.vue` 对服务链 8 叶子发 `{leaf}_report`（如 `shortboard_report`）创建产物任务；
  Java `ArtifactAnalysisTypes` 白名单仅注册企业域 6 类，`AnalysisTaskServiceImpl.create()` 返回
  「功能尚未开放或不支持的 analysisType：shortboard_report」。
- Demo 原型报告下载是纯前端渲染，不走 Java 异步任务链；lumen 复刻走 Java ARTIFACT 链，后端未跟进 8 个 svc 类型。

## 修改内容

1. `support/artifact/ArtifactAnalysisTypes.java`
   - `REPORT_TYPES` 扩充 8 个 svc 报告类型：`org_coverage_report / org_trend_report / tech_power_report /
     shortboard_report / graph_report / shenzhen_report / attract_report / cultivate_report`
     （`SVC_REPORT_TYPES` 常量单列，`SVC_LEAF_LABELS` 提供中文标签，真源对齐前端 `serviceDomainReports REPORT_LABEL`）。
   - `parentAnalysisTypeOf()` 增加 svc 分支 → `svc:analysis:{leaf}`（canonical），供父任务类型匹配校验。
   - 新增 `svcLeafOf()`：产物类型反查 svc 叶子（复用 `SvcAnalysisTypes.leafOf`，不新造解析）。
2. `support/analysis/AnalysisTaskIdGenerator.java`
   - `PREFIX` 映射补 8 个 `{leaf}_report → REP`（taskId 形如 `REP-YYYYMMDD-NNN`）。
3. `service/impl/artifact/ArtifactSnapshotReaderImpl.java`（核心）
   - `loadSvcPayload()`：svc 父任务结果唯一真源是 `target_params.result_payload`（`applySvcCallbackResult` /
     `applySvcSyncResult` 写入；`resultAssetId=res-{taskId}` 非 MinIO 键、`resultBucket` 为空），
     原有 MinIO / `result_data` 两条路径均取不到，svc 走独立读取分支。
   - 八叶子章节装配 `buildSvcSections()`：shortboard（六环节强度 + 短板结论）、org_trend（heat 研判 +
     series 点数）、tech_power / attract / cultivate（排名行）、org_coverage（coverage_matrix.orgs 广度深度 +
     depth 榜）、graph（节点/边/密度摘要）、shenzhen（compare.cities 逐城指标 + 梯队）。
   - `extractSvcOrgNames()` / `resolveSvcConclusion()` / `buildSvcExportTable()` 对应 svc 名单、结论与导出表；
     空态（`status=empty`）诚实写「结果为空态」结论，不编数值。
4. 下载链路零改动：`AnalysisTaskController.asset()` 的代理下载、文件名、Content-Type 全部由
   `ArtifactAnalysisTypes.isArtifact()` 判定，白名单扩充后自动生效。

## 测试结果

- 新增 `ArtifactSnapshotReaderImplSvcTest`（4 例）：shortboard gap→章节、attract 行→章节+导出表、
  空 result_payload 诚实抛错、8 类型注册+父类型映射。
- 更新 `ArtifactAnalysisTypesTest`：11 类注册断言 + svc 无导出形态。
- 模块回归：`gkxlumen-topic-async-service-biz` 132 tests，0 failures 0 errors（JDK21，
  `surefire:test` 3.2.5；注：本机默认 surefire 2.12.4 不支持 JUnit5，与本次改动无关）。
- `spring-javaformat:apply` 后重跑仍全绿。

## 验收证据

- 本地改动：lumen-svc-platform `dev` 工作区，3 主文件 modified + 1 测试 new（未 commit，按
  lumen 人工验收闸门待监管人走查后推送）。
- 前端契约零改动：`lumen-ui-topic` 仍发 `analysisType={leaf}_report, params={parentTaskId, format:'pdf'}`。

## 遗留风险 / 边界

- svc 报告仅 PDF（`requireFormat` 报告仅 pdf），与前端一致；如后续要 xlsx 导出需另开类型+导出表定制。
- graph / shenzhen 叶子 payload 若整体为空（nodes/compare 均缺），章节仅剩「任务信息」，结论走通用兜底——
  与算法侧「诚实空态」一致，不属缺陷。
- 父任务校验沿用既有逻辑：`parentAnalysisTypeOf` 精确等值匹配 canonical `svc:analysis:{leaf}`；
  svc 父任务落库即 canonical（create 时归一化），无历史别名脏数据风险。

## CI/CD（必填）

- 分支：`dev`（本地待验收）
- commit：验收通过后按 `[agent:api-agent]` 提交推送
- pipeline URL / ID：待推送后触发
- K8s rollout：待 CI

## 架构合规自检

- ✅ 调用链：报告渲染在 Java 本地（ARTIFACT 链），不经 Python/算法
- ✅ 算法只在 Python：Java 只读父任务快照组装章节，零算法
- ✅ 可观测：复用既有审计（create/asset_download audit）与 SSE 进度
- ✅ demo/lumen 隔离（D12）：仅改 lumen-svc-platform，未引用 demo-*
- ✅ D9：报告为展示产物，不新增统计指标，不涉 8 件套

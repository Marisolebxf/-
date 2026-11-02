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

## 代码评审修复（2026-10-27 上午，评审子代理 + 人工复核）

评审结论「需修后合」，发现并修复 4 项（关键项已在 `lumen-algo-py` 算法源码核实）：

1. **[Critical] org_coverage / shenzhen 报告被 legacy 槽劫持**：`leaves.py` 的
   `leaf_org_coverage` 无条件 `payload.update(_legacy_slots(gap=...))`（`leaves.py:84`），`leaf_shenzhen`
   亦注入 gap/tech 等 legacy 键。原「按键瀑布猜叶」会让这两类报告命中 shortboard 章节，渲染错叶内容。
   → 修复：`buildSvcSections()` 与 `resolveSvcConclusion()` 改为按父叶子
   `SvcAnalysisTypes.leafOf()` 精确派发（未知叶子只留任务信息章，诚实不猜）。
   → 新增测试 `orgCoverageReportNotHijackedByLegacyGapSlots`（断言有覆盖章、无短板章）。
2. **[Important] 默认形态深圳载荷键不匹配**：不带 industry 的 `leaf_shenzhen` 走 `szcompare.py`：
   `sz_compare.cities`（行键 `city`）+ 顶层 `tier`；原代码只读 `compare.cities`（`city_name`）。
   → 修复：`appendSvcShenzhenSection()` 兼容 `compare`/`sz_compare` 双形态 + `city_name`/`city`
   双行键 + compare 内/顶层 tier 兜底。
   → 新增测试 `shenzhenReportReadsDefaultSzCompareShape`（sz_compare 形态 + 顶层 tier）。
3. **[Minor] org_coverage 导出表优先级与注释相反**：原来优先长表 `matrix`（org×field 逐格可达数千行）。
   → 修复：优先 `coverage_matrix.orgs`（org 级摘要），注释同步。
4. **[Minor] `java.util.Set/Iterator` 全限定名风格**：并入文件头 import。

评审修复后验证（内网 nexus 断连、surefire 缓存随 macOS 重启清空，改用手工
javac + JUnit Platform Launcher 直跑）：主源码 87 class 编译零错；artifact 包 4 个测试类
12/12 全绿（含新增 2 例）。

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

- 分支：`dev`
- commit：`a590b69`（2026-10-27 经监管人徐滕强要求推送在线验证：含评审修复版，artifact 包 12/12 测试绿）
- pipeline URL / ID：已触发，待 CI 绿
- K8s rollout：待 CI

## 架构合规自检

- ✅ 调用链：报告渲染在 Java 本地（ARTIFACT 链），不经 Python/算法
- ✅ 算法只在 Python：Java 只读父任务快照组装章节，零算法
- ✅ 可观测：复用既有审计（create/asset_download audit）与 SSE 进度
- ✅ demo/lumen 隔离（D12）：仅改 lumen-svc-platform，未引用 demo-*
- ✅ D9：报告为展示产物，不新增统计指标，不涉 8 件套

## 追加修复（2026-10-28，用户报「技术力评估选历史任务生成报告报错」）

### 根因（与"选历史任务"无关，任何长标题报告都会触发）

线上实例 `REP-20261028-001`（父 `SVC-20261027-006`）在"文件生成完成"节点失败：
`Data truncation: Data too long for column 'result_asset_id'`。

- `analysis_task.result_asset_id` 为 varchar(128)（`db/9x_gkxlumenx_topic_enterprise.sql:197`）；
- 2026-10-27 文件名规范化把中文标题拼进文件名 → MinIO objectKey =
  `gkx-analysis-results/analysis/tech_power_report/{parentTaskId}/{taskId}/{中文标题_时间戳_taskId}.pdf`，
  固定前缀已 ~80 字符，中文标题（UTF-8 每字 3 字节按字符计 1）叠加后超过 128；
- PDF 已成功上传 MinIO，死在最后回写 DB 指针一步 → 任务 failed。属上一波文件名改动的回归。

### 修复（commit `946853c`，dev）

1. `AnalysisAssetServiceImpl`：新增 `artifactObjectKey()` —— 文件名段剥成 ASCII
   （`[^A-Za-z0-9._-]→_`），全中文剥空退化为 taskId，整长硬上限 128（超长截中段保扩展名）。
   **下载显示名不受影响**：Controller 下载文件名优先读 `result_data` 摘要的完整中文 `fileName`，
   objectKey 仅兜底。
2. `AnalysisAssetServiceImplTest`：新增 2 例回归（中文长标题 ≤128 且纯 ASCII；超长 ASCII 截断保扩展名）。
3. `gkxlumen-topic-async-service-biz/pom.xml`：显式钉 surefire 3.2.5 —— 默认 2.12.4 不认 JUnit5
   会把 `*Test` 静默跑成 0 个（对齐 topic-svc-biz / cms 既有做法）；修复后全模块 145 测试真实执行全绿。
4. 顺带：失败任务 `REP-20261028-001` 的 PDF 已在 MinIO 但 DB 指针未落，需用户点「重新生成」
   重跑一次（新代码下会成功）；无需数据修复。

### 追加验证

- 本地：`mvn -pl gkxlumen-topic-async-service-biz test` → **145 tests, 0 failures**（surefire 3.2.5）
- CI：pipeline 3181（commit `946853c`），backend:build 排队中

## 追加交付（2026-11-02 · 政策 + 服务链块式 PDF 对齐前端报告页）

### 范围

- 新增 `DomainBlockReportModel`、`ReportText`（泄漏/Q-GAP/环节中文）、`PolicyBlockReportAssembler` / `PolicyBlockReportModel`、`SvcBlockReportAssembler` / `SvcBlockReportModel`。
- Thymeleaf `analysis/domain-block-report.html`：封面 + KPI/文字/条形/表格块；空态仅「当前任务没有可展示的结果数据」。
- `ArtifactRenderServiceImpl`：`policy:report:export` 与 svc `{leaf}_report` 走 `domain-block-report`。
- `ArtifactAnalysisTypes`：`policy:report:export`；`AnalysisTaskServiceImpl` 校验政策父任务。
- 测试：`PolicySvcReportModelTest`（区域平铺、深圳落地实效性、svc 趋势明细/引进环节中文）；本机未装 JDK/mvn，CI 为准。

### 验收

- 联调通过：PDF 章节标题与 `lumen-ui-topic` `policyBlockReportDocument` / `svcBlockReportDocument` 一致。
- **未纳入本 commit**：同仓其它会话脏改（chain/eval 模板等）保持工作区未提交。

### cost 追加

| actual_tokens | model_used | actual_cost | cost_warn |
|---------------|------------|-------------|-----------|
| +120000 | composer | +0.30 | false |

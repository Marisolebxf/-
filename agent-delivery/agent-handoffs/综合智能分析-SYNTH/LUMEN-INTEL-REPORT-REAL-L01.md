# LUMEN-INTEL-REPORT-REAL-L01 · 综合智能分析三叶报告查看与 Java PDF

孔东已确认三页报告查看结构。本交接覆盖第一步块式 HTML 与第二步 Java PDF。代码推 `origin/dev`，任务进入联调。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `human:孔东` |
| supervised_by | `human:孔东` |
| claim_type | `pull` |
| 说明 | 前端仓 `lumen-ui-topic`，Java 产物在 `lumen-svc-platform`，协作 `api-agent` |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 复用企业块式报告页与 `domain-block-report`，未另起模板或导出栈。未跳过报告章节、空态「暂无数据」和调用链。 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | 无新增图。复用既有产物任务到 `ArtifactRenderServiceImpl` 的渲染边 |
| 图 diff | 未改图。三叶 `*_report` 落到同一 PDF 模板 |
| 会签态 | 无新图，不自填 |
| 说明 | 未改存储流、未改 ODS/DWD/ADS |

## 问题清单

- 第一步报告页已由孔东确认结构和展示样式，第二步按该页章节做 PDF。
- 没有父分析任务的跑批结果只能打开 HTML，下载仍截当前页。Java 产物要求父任务已成功。
- 协同 PDF 只收录结果快照里的节点和边，不另查图谱接口。
- 本机 Maven 解析不到私服 `gkxlumen-common-bom:5.12.0`，Java 单测未在本机跑通。

## 修改内容

第一步（已确认）：活力、要素、协同报告页改为块式 HTML，覆盖结果块。页签和折叠按原顺序平铺。要素四透镜展开为连续节。空态写「暂无数据」，开发提示词不进正文。

第二步：

- `SynthBlockReportModel` 按已确认章节组装 `analysis/domain-block-report`。柱状和折线展开为条形或表。只读父任务结果，不重新调算法。
- 产物类型：`region_innovation_vitality_report`、`region_innovation_elements_report`、`region_innovation_collaboration_report`。父类型分别为对应的三叶分析键。任务号前缀 `REP`。
- 报告页在有父任务时把 `pdf-source` 交给现有 Java 下载。
- 三页「生成分析报告」先查同一父任务下 `success` / `running` 的报告。已有则只打开报告页，不新建任务。Java 创建侧仍按用户、类型、父任务、格式幂等。

## 测试结果

- `node src/views/intelligence/intelVit.selfcheck.mjs` → ok
- `node src/views/intelligence/elements/element.selfcheck.mjs` → ok
- `node src/views/intelligence/collaboration/collab.selfcheck.mjs` → ok
- `npm run type-check`（vue-tsc）→ 通过
- Java：`ArtifactRenderServiceImplTest` 等已补三叶样例，本机因私服 BOM 缺失未执行

## 遗留风险

- 报告列表只看第一页 50 条。页外的已有报告仍由 Java 幂等复用，不会另建成功任务。
- 跑批秒开结果没有父任务，PDF 仍是页面截图。
- Java 单测需在能解析私服的环境补跑。

## CI/CD（必填）

- 分支：`lumen-ui-topic` `dev`，`lumen-svc-platform` `dev`，`gkx-orchestration` `dev`
- commit：`lumen-ui-topic` `33a76a9`；`lumen-svc-platform` `40bc5f0`；编排仓为本交接提交
- pipeline URL / ID：push 后由 GitLab CI 生成，本交接写于 push 前
- 部署 namespace / 镜像 tag：随两业务仓既有 dev 流水线
- K8s rollout：待流水线
- dev 测试 URL / 命令与结果：本地 type-check 与三页自检已过；线上联调未做

## 可观测性（建议）

- OTEL_SERVICE_NAME：沿用 `gkxlumen-topic-async-service` 既有产物任务审计，未新增埋点
- traceId（dev 抽样）：无
- Tempo / Loki：无

## 架构合规自检

- 调用链：前端只调 Java 分析任务接口；PDF 渲染不调 Python
- 算法只在 Python：报告组装只读已有快照
- 图谱：未改 Nebula，协同 PDF 不直连图库
- 可观测：未新增前端埋点；产物创建沿用既有审计
- D12：未调用 demo 服务
- D8/D10：阅读页沿用已确认的块式报告，未另起控件
- D9：报告不改指标口径，不把评审角标写入正文

## 成本

| 字段 | 值 |
|------|-----|
| model_used | `grok-4.7` |
| actual_tokens | 本会话无 Console 精确计数，不回写估数 |
| actual_cost | 价表无 grok-4.7 档，不回写 |
| cost_warn | `green`（未超过已知阈值；成本未计价） |

## 涉及文件

- `lumen-ui-topic`：`src/components/report/synthBlockReportDocument.ts`，三页报告与工作台，`useSynthTaskBridge.ts`，`reportPdfExport.ts`，`analysisTask.ts`，mock 产物复用，三份 selfcheck
- `lumen-svc-platform`：`SynthBlockReportModel.java`，`ArtifactRenderServiceImpl.java`，`ArtifactAnalysisTypes.java`，三叶 `Synth*AnalysisTypes.java`，`AnalysisTaskIdGenerator.java`，对应单测
- 未纳入提交：`OneMapDebugView.vue` 与 `routes.ts` 中的一张图调试路由（文件自标禁止提交）；编排仓门户对接文档的未提交改动

# 综合智能分析（E8 三叶）demo→lumen 复刻 · 接口需求 + 任务拆解

- 时间：2026-10-27
- 作者：frontend-agent（监管：human:侯佳伟）
- 任务：`LUMEN-INTEL-FE-REPLICA-L0`（父单，本文档为其交付物；子单见 §6）
- 源仓：`repos/demo-ui-topic`（React + Arco React 版）；目标仓：`repos/lumen-ui-topic`（Vue3 `<script setup>` + Arco Design Vue + UnoCSS + Pinia + Vite）
- 格式对齐：`产业链分析-CHAIN/API-CHAIN-BIZ-UX-CATALOG.md`（字段表 + HTTP/JSON 示例）
- 溯源：demo 侧实现 = `SYNTH-MOD-{VITALITY|ELEMENT|COLLAB}-V1-HIFI` 三叶（dev 分支已评审）；产品定义 Pack1 五件套见本目录

## 0. 复刻范围界定（防漏防多）

### 0.1 复刻范围（三叶 × 3 路由 = 9 条路由）

| 叶 | 菜单（L2） | 工作台 | 任务过程页 | 报告页 |
|---|---|---|---|---|
| 活力 | `menu:topic:intel:vitality` | `/intelligence/vitality` | `/intelligence/vitality/tasks/:taskId` | `/intelligence/vitality/report` |
| 要素 | `menu:topic:intel:elements` | `/intelligence/elements` | `/intelligence/elements/tasks/:taskId` | `/intelligence/elements/report` |
| 协同 | `menu:topic:intel:collab` | `/intelligence/collaboration` | `/intelligence/collaboration/tasks/:taskId` | `/intelligence/collaboration/report` |

### 0.2 明确排除（demo 存量但非本轮范围）

- `pages/intelligence/` 下旧一代 SYNTH-REGION 文件（`synthStore/synthModel/synthShared/IntelReviewMount/IntelMetricBadges/intelReviewData/intelReadinessSeed/intelligence.css`）——**未挂路由的遗留实现**，唯一被新叶引用的是 `synthData.ts` 的 `COLLAB_CORR_SERIES` 常量（关联散点序列），复刻时作为数据搬入新 mock，**不搬组件**
- demo 侧 `operations/SystemTaskOperationsPage`（运维页，lumen 已有 `SystemTaskFloat` 全局浮层体系）

## 1. 前端架构方案（lumen 侧落位）

```text
src/
├─ views/intelligence/
│  ├─ VitalityWorkbenchView.vue        # F-VIT-01 工作台（活力分析 / 分析记录 双 Tab）
│  ├─ VitalityTaskPage.vue             # F-VIT-02 过程页（五阶段）
│  ├─ VitalityReportPage.vue           # 报告页
│  ├─ ElementsWorkbenchView.vue        # + Task/Report 同构三件
│  ├─ CollabWorkbenchView.vue          # + Task/Report 同构三件
├─ components/intelligence/
│  ├─ IntelMetricMount.vue             # ⓘ 挂载（MetricSpecCard/MissingDefBadge/PendingBadge/MockBadge 排列）
│  ├─ MissingDefBadge.vue              # D1 missing 红问号（治理引用，不显伪 8 件套）
│  ├─ SynthContextBar.vue              # CT-SYN-CTX 三叶共享上下文条
│  ├─ SynthAnalysisRecordsPanel.vue    # 分析记录 Tab 面板（analysisTaskList 过滤版）
│  ├─ SynthMethodDrawer.vue            # 方法抽屉壳（三叶内容各自传入）
├─ composables/
│  ├─ useSynthCtx.ts                   # URL>localStorage>默认；windowToUrl 映射
│  ├─ useSynthTaskBridge.ts            # 四决策/恢复（Q-ANALYSIS-01，附录 E）
├─ mock/intel/
│  ├─ index.ts                         # 三叶 mock 统一注册（register.ts 引）
│  ├─ vitalityMock.ts                  # DEFAULT_BATCH_RESULT + buildTaskResult 确定性推导
│  ├─ elementMock.ts / collabMock.ts   # 同上；COLLAB_CORR_SERIES 随迁
│  ├─ synthReadinessSeed.ts            # D1–D4 只读镜像（头注释注真源+同步任务ID）
```

### 1.1 共享内核机制（必须逐条对齐 demo）

| 机制 | demo 实现 | lumen 落法 |
|---|---|---|
| 分析上下文 | `synthCtx.ts`（`region/compare/window`，URL>localStorage>默认；replace 回写） | `useSynthCtx` composable，storage key 不变 `topic-synth-workbench` |
| 四结果态 | `instant`（默认+跑批秒开）/`task`/`dirty`/`no_batch` | 同构；`mode` URL 参数同语义 |
| 任务四决策 | `startOrResumeSynthAnalysis`：resume_processing / resume_result / queue_full / started | `useSynthTaskBridge`，数据源从 demo 双轨 localStorage 改为 **统一任务中心 #102–#109** |
| 过程页五阶段 | 900ms 演进，**无百分比**；排队可撤回；完成不自动跳 | SSE #109 事件流（mock 发射器已有）；阶段文案逐字搬 |
| 分析记录 | 系统任务总线按 taskType 过滤 + 复制配置 + 关联报告计数 | `analysisTaskList` + `analysisTaskRunning`；报告关联键 `snapshot:{taskId}` |
| 报告触发 | `data-system-report-trigger` 数据属性契约 | 复用 `systemReportContract` + `SystemReportReader`；template-id：`synth-{leaf}-report-v1` |
| 评审门控 | 叶子 `ReviewModeProvider/ReviewOnly`（`gkx-topic-review-mode`） | 全局 `useReviewStore` + `isReviewFeatureEnabled`（key `ent_review_mode`）；角标自闸 |
| D9 角标 | MetricMount（ⓘ/红问号/Pending/Mock，draft 橙点） | `IntelMetricMount`；seed 数据从 `intelReadinessSeed.ts` + 三叶 metricSeed 移植 |
| 确定性 mock | 无随机数；task 结果按 region/window 推导 | 同构搬入 `mock/intel/`；`USE_MOCK=false` 时禁用 |
| 埋点 | `track('synth_vit_*')` 等 | 仓内 observability 埋点方案对齐现有 views 惯例 |

### 1.2 治理引用（诚实态，禁删）

`Q-SYNTH-01/02/03`、`Q-SYNTH-V-01`、`Q-SYNTH-E-01/E-02`、`Q-SYNTH-C-01/C-02/C-03/C-04`；「临时权重·待甲方确认」「演示加权·非机器学习」「固定演示快照·非正式算法」Tag；协同叶禁止「密度×强度」当权威公式、关联散点禁止因果表述（样本<3 不出系数）。

## 2. 接口需求拆解

### 2.1 复用既有接口（不新增，仅扩白名单）

统一任务中心（真源：`企业战略分析-ENT/API-ENT-full-catalog.md` §4.Q #102–#109；lumen 已在 `api/enterprise/analysisTask.ts` 全量接入）：

| # | 接口 | intel 复刻用途 | 需要的改动 |
|---|---|---|---|
| #102 | `POST {GW}/ent/topic/v1/analysis/tasks` | 三叶「开始分析」建任务 | `AnalysisTaskCreateRequest.analysisType` 白名单 **+6 键**（见 2.2） |
| #103 | `POST .../tasks/list` | 分析记录 Tab 分页列表 | 无 |
| #104 | `GET .../tasks/{taskId}` | 过程页任务详情 + 切回恢复 | 无 |
| #105 | `GET .../tasks/{taskId}/result` | 结果快照（resultData = LeafResult JSON） | 无 |
| #107 | `POST .../tasks/{taskId}/cancel` | 排队撤回 | 无 |
| #108 | `GET .../tasks/running?user_id=` | 同条件去重（resume 判定） | 无 |
| #109 | SSE `.../tasks/stream` | 过程页五阶段事件流 | mock 发射器 stages 用 intel 五阶段文案 |
| 报告 | `*_report` 模式（同 `eval_report`） | 三叶「生成分析报告」 | 白名单 +3 report 键 |

metrics catalog（`GET /metrics/v1/catalog`，Wave 1 目标态）：8 件套 + 四维就绪度；过渡期前端走 `synthReadinessSeed` 只读镜像（真源：`agent-delivery/metrics/registry/metric-readiness-matrix-SYNTH.yaml` 若无则由 data-agent 补登，镜像头注释注明）。

**上下文字典**：region（9 项）/compare（5 项）/window（3 项）demo 为静态硬编码——复刻保持硬编码，**不新增字典接口**。

### 2.2 analysisType 扩展（Java/Python 透传键）

```text
region_innovation_vitality          # 活力分析任务
region_innovation_elements          # 要素分析任务
region_innovation_collaboration     # 协同分析任务
region_innovation_vitality_report   # 活力报告（template: synth-vitality-report-v1）
region_innovation_elements_report   # 要素报告（template: synth-element-report-v1）
region_innovation_collaboration_report  # 协同报告（template: synth-collaboration-report-v1）
```

params（#102 create 的 `params` JSON，三叶同构）：

```json
{
  "region": "深圳",
  "compare": "全国重点城市",
  "window": "3y"
}
```

去重指纹 `analysis_fp` = `region|compare|window`（与 demo `synthCtxFingerprint` 一致）。

### 2.3 新增接口（唯一真实新增：跑批快照）

```text
GET {GW}/topic/v1/synth/{leaf}/batch-snapshot     leaf ∈ vitality | elements | collaboration
Query: region, compare, window(1y|3y|5y)
```

响应（成功）：

```json
{
  "code": 0, "ok": true, "msg": "ok",
  "data": {
    "snapshotId": "batch:深圳|全国重点城市|最近3年",
    "computedAt": "2026-08-10 02:00",
    "methodVersion": "vDemo-vitality",
    "result": { "...": "LeafResult JSON，与 #105 resultData 同构" }
  }
}
```

- `404 / code!=0`（无快照）→ 前端进 `no_batch` 态，引导「开始分析」
- 前端 mock：`registerApiMock('synthVitalityBatch'|'synthElementBatch'|'synthCollabBatch')`，**仅默认三元组**（深圳×全国重点城市×最近3年）返回快照，其余 404（对齐 demo `hasVitalityBatchSnapshot`）
- Java（topic-chain 门面）→ Feign Python `/internal/v1/synth/{leaf}/batch-snapshot`；Wave 0 ADS 未建，Python 返回 404 占位即可
- **P1 档**：无此接口前端可跑（退化为全部走任务），不阻塞复刻

### 2.4 调用链合规（公约 §2 D12）

```text
前端(lumen-ui-topic) → gkxlumen-platform-gateway → lumen-svc-topic(Java)
  → /internal/* → lumen-algo-py（Python）
```

禁止前端直调 demo 服务 / Python。

## 3. 权限与菜单

- `perms/matrix.ts`：已有 `MENU_INTEL_VITALITY: 'menu:topic:intel:vitality'`；**补** `MENU_INTEL_ELEMENTS: 'menu:topic:intel:elements'`、`MENU_INTEL_COLLAB: 'menu:topic:intel:collab'`
- `router/menu.ts` navGroups 新增分组「综合智能分析」（icon 建议 `analysis`，NavIconKey 需扩枚举）；过程页/报告页 `showInMenu: false`
- 任务过程页路由需支持 `/intelligence/{leaf}/tasks/:taskId` 动态段（现有 navItem 体系外手工注册）

## 4. 验收基线（五维 DoD，真源 `templates/fe-replica-visual-dod.md`）

| 维 | 标准 |
|---|---|
| 布局 | 对齐 demo 三叶已评审页（工作台条件栏/结果面/方法抽屉/记录 Tab；过程页五阶段；报告七段式） |
| 交互 | 四结果态、任务四决策、切回恢复、排名卡点击切区域、三叶互跳带上下文、协同图谱过滤/高亮/子图统计、报告触发契约 |
| 样式 | Arco Design Vue + UnoCSS 原子类；主色 `#165DFF`、页面底色 `#D8E7FC`、卡片/边框对齐 demo `--sci-*` token 语义 |
| 评审 | D9 角标全套（ⓘ/红问号/Pending/Mock/draft 橙点）；评审模式关闭 DOM 零泄漏（无 metric_id/Q0xx/GAP 字样） |
| Mock | 统一走 `registerApiMock`；确定性数据；`USE_MOCK=false` 不注册、无 fixture 填数 |

另：防漏扫描按 `产品实现规程.md` 附录 D（D.1–D.5）+ 附录 E（E.1–E.5 异步工作区）执行，handoff 附扫描摘要。

## 5. 明确不做（YAGNI 边界）

- 不搬 demo 旧 SYNTH-REGION 一代组件（见 §0.2）
- 不为 region/compare/window 建字典接口
- 不做跑批结果管理后台（Java 侧 Wave 0 Python 404 占位即可）
- 指标 8 件套正式化 / readiness 矩阵登记 = data-agent 职责，前端只读镜像

## 6. 任务拆解与依赖

| ID | 标题 | repo | 依赖 | 类型 |
|---|---|---|---|---|
| `LUMEN-INTEL-FE-REPLICA-L0` | 复刻总纲（本文档） | gkx-orchestration | — | tech_task |
| `LUMEN-INTEL-FE-L0` | 菜单/路由/权限 + NavIconKey | lumen-ui-topic | L0 | feature |
| `LUMEN-INTEL-FE-L1` | useSynthCtx + mock/intel（三叶确定性数据+readinessSeed+metricSeed 扩段+统一注册） | lumen-ui-topic | L0 | feature |
| `LUMEN-INTEL-FE-L1B` | 任务中心扩展（AnalysisType+6、路由分支、任务桥 composable、记录面板） | lumen-ui-topic | L1 | feature |
| `LUMEN-INTEL-FE-VIT` | 活力三页（工作台/过程页/报告页+方法抽屉+共享件） | lumen-ui-topic | L1B | feature |
| `LUMEN-INTEL-FE-ELEM` | 要素三页（三透镜/四维评分/贡献路径） | lumen-ui-topic | L1B | feature |
| `LUMEN-INTEL-FE-COLLAB` | 协同三页（图谱/关联散点/集群/策略） | lumen-ui-topic | L1B | feature |
| `LUMEN-INTEL-FE-AV` | 防漏扫描+附录E自检+selfcheck+评审泄漏验证+handoff | lumen-ui-topic | VIT+ELEM+COLLAB | feature |
| `LUMEN-INTEL-BE-1` | Java 白名单+6键透传 / Python internal 占位 / 跑批快照接口 / 报告模板 | lumen-svc-topic + lumen-algo-py | L0（本文档为需求输入） | feature |

依赖链：`L0 → L1 → L1B → {VIT ∥ ELEM ∥ COLLAB} → AV`；BE-1 与前端 L1B 后并行。

## 7. 变更记录

| 日期 | 变更 | 作者 |
|---|---|---|
| 2026-10-27 | 初版（复刻解析 + 接口拆解 + 9 单拆解） | frontend-agent |

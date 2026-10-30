# QA-TOPIC-BUGFIX-FE-L01 · 专题系统测试缺陷修复 — 前端

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `human:孔东` |
| supervised_by | `human:孔东` |
| claim_type | `pull` |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full` |

## 范围与实现

仓库：`repos/lumen-ui-topic`，分支 `dev`。本次归档 commit 覆盖 bug-registry 20261026–20261028 中**前端可闭合**项；B 类数据缺口、028-005 Java 500 根因、028-011 菜单卡死（暂缓）见后端单 `QA-TOPIC-BUGFIX-API-L01` / `QA-TOPIC-BUGFIX-API-DICT-L01`。

### BUG 对照（前端已改）

| BUG-ID | 处理 | 主要文件 |
|--------|------|----------|
| 027-002 | 饼图/清单入口 tag 字典译名 | `TypeRegionPanel.vue`, `useKeyEnterpriseAnalysis.ts` |
| 027-003 | 对比篮/列表 tags_flat 去重 + 字典未知 code 隐藏 + 展示名去重 | `entTagDisplay.ts`, `entTagDictionary.ts`, `EntTagChip.vue`, `CompareItemCard.vue`, `ResultList.vue`, `EntityIdentityHeader.vue`, `RecommendationSection.vue`, `ScaleChip.vue`（见文末追加节） |
| 027-004 | 识别依据空态 | `EvidenceModal.vue` |
| 027-006 | Arco Alert 改用默认 slot（无效 `content` 属性导致空正文） | `EvalConfigPanel.vue`, `EvalQualityPanel.vue` |
| 027-007 | 对标城市码→中文兜底 | `CityBenchmarkPanel.vue` |
| 028-001 | 区域固定文案 | `EnterpriseSzStatus.vue` |
| 028-002/003 | 环节「全部环节」+ node_stage 兜底 + 清单收窄 | `ChainLocatePanel.vue`, `useSzStatusAnalysis.ts`, mock |
| 028-004 | 详情抽屉 name_cn | `EnterpriseSzStatus.vue` |
| 028-005 | 关系图谱 500→空态（根因仍 Java） | `EnterpriseProfileTabPanel.vue` |
| 028-006/008 | 招引/培育筛选与权重 label | `recruitDisplay.ts`, `RecruitResultPanel.vue` |
| 028-007/009 | 窄屏详情侧栏语义 | `RecruitResultPanel.vue` |
| 028-010 | 全景切回图谱 refresh | `IndustryPanoramaPage.vue`, `IndustryPanoramaGraph.vue` |
| 028-012 | 周期参数评审文案门控 | `IndustryDiagnosisPage.vue` |
| 027-001 | 产业多选撑开 | `IndustryClusterSelect.vue` |

### 未在本仓闭合 / 待复测

| BUG-ID | 说明 |
|--------|------|
| 026-001/002 | 默认条件无清单/地图数据 → **API-L01** |
| 027-005/008 | 识别依据/对标指标数据缺口 → **API-L01** |
| 028-011 | 侧栏卡死 → 暂缓，待专单 |
| A 类 VO 中文名 | 前端兜底保留，根因 **API-DICT-L01** |

## 架构合规自检

- D12：仅调 Java gateway，无 demo 直连 ✅
- D8/D9/D10：未删 metric/review 门控 ✅
- 调用链：未越层 ✅

## 验收证据

- 本地：`npm run type-check`、eslint（改动文件）绿
- K8s dev 30892：待孔东走查 + 对应 FUNC 用例复测

## 产物

- 代码：`lumen-ui-topic` dev 分支 commit（见 commit message）
- 后端派单：`agent-handoffs/QA-TOPIC-BUGFIX-API-DICT-L01.md`、`QA-TOPIC-BUGFIX-API-L01.md`

## cost（待签收回填）

| actual_tokens | model_used | actual_cost | cost_warn |
|---------------|------------|-------------|-----------|
| TBD | TBD | TBD | false |

---

## 追加修改（2026-10-30 · 企业标签栏）

孔东走查：企业查询列表 / 推荐区 / 详情抽屉 / 对比篮 **资质+规模标签** 重复 code、字典外 code 裸显（如 `key_enterprise`）、规模 tag 样式不统一。

| 项 | 实现 |
|----|------|
| `tags_flat` | code **去重**；`meta/tags` 已加载时 **未知 code 不展示**；按 **展示名再去重**（多 code 同中文名只留一枚） |
| 规模 `enterprise_scale` | `ScaleChip` 与资质 tag 同形态：`a-tag size="small" color="orange"`（无 bordered） |
| 027-003 | 对比篮由仅 Set 去重升级为与列表共用 `codesForDisplay` |

### 涉及文件（`lumen-ui-topic`，待走查后 commit）

| 路径 | 说明 |
|------|------|
| `src/utils/entTagDisplay.ts` | 展示用 code 列表纯函数 |
| `src/utils/entTagDisplay.selfcheck.mjs` | 最小自检：`node src/utils/entTagDisplay.selfcheck.mjs` |
| `src/stores/entTagDictionary.ts` | `hasTagCode` / `codesForDisplay` |
| `src/components/common/EntTagChip.vue` | 字典加载后未知 code 不渲染 |
| `src/components/common/ScaleChip.vue` | 规模 orange 实心 tag |
| `src/components/search/ResultList.vue` | 列表卡片；资质/规模/领域 **单行 80% 宽** 换行区（见下节） |
| `src/components/search/RecommendationSection.vue` | 初始态推荐 |
| `src/components/search/EntityIdentityHeader.vue` | 抽屉/画像头 |
| `src/components/enterprise/CompareItemCard.vue` | 对比篮卡片 |

### 与 BUG 台账

- **027-003**：本追加为同一缺陷的 **展示层收口**（registry 已 fixed，待 30892 复测 verified）。
- 非新 BUG 编号；不扩 bug-registry。

### 验收

- 企业查询：推荐企业与结果卡片、详情抽屉、对比篮 — 标签无重复中文、无字典外 code、规模为橙色实心 tag。
- 自检：`node src/utils/entTagDisplay.selfcheck.mjs` 通过。

### 代码状态

- 已 push **`lumen-ui-topic` `origin/dev` → `a8dfca5`**（基线 `0a923f6` 之后）。

---

## 追加修改（2026-10-30 · 查询结果卡片标签布局）

走查：卡片宽度充足时，资质/规模与 **核心技术领域** 标签分两行浪费纵向空间；换行时行距过紧。

| 项 | 实现 |
|----|------|
| 布局 | `ResultList.vue`：两类标签合并为 **同一** `flex-wrap` 容器，`w-[80%] max-w-full` |
| 间距 | 同行 `gap-x-1`，换行 `gap-y-2`，避免上下两行 tag 贴在一起 |
| 显隐 | `cardShowTagStrip`：仅当 schema 标签或领域 tag 有值时渲染 |

### 涉及文件

| 路径 | 说明 |
|------|------|
| `src/components/search/ResultList.vue` | `domainTagsOf` / `cardShowTagStrip`；合并标签条 |

**未改**：`RecommendationSection.vue` 仍为两行（初始态推荐区）；若需对齐可另开小改。

---

## 追加修改（2026-10-30 · 企业详情专利 Tab 表格列宽）

走查：详情抽屉「专利」Tab 日期、状态列过窄（原 100px / 80px），日期如 `2020-02-15` 与状态文案易挤。

| 列 | 原宽 | 新宽 |
|----|------|------|
| 日期 | 100 | **128** |
| 状态 | 80 | **112** |

| 路径 | 说明 |
|------|------|
| `src/components/enterprise/EnterpriseProfileTabPanel.vue` | 专利 Tab `a-table` columns |

### 与 BUG 台账

- 体验优化，**无新 BUG-ID**；不修改 `bug-registry.yaml`。

### 代码状态（汇总 · 2026-10-30 追加批次）

| 范围 | 状态 |
|------|------|
| 标签字典/ScaleChip/对比篮/抽屉头/推荐区 | 已含于 `a8dfca5` |
| 查询结果卡片单行标签 + 专利列宽 | 已含于 `a8dfca5` |
| commit hash | **`lumen-ui-topic` `a8dfca5`**（编排 handoff `a5729cf0`） |

---

## 追加修改（2026-10-30 · 报告正文去工程名）

走查：企业评估/域分析报告「数据来源与生成说明」中出现 **`lumen-ui-topic`**，与业务无关。

| 项 | 实现 |
|----|------|
| 系统名 | `systemReportContract.ts`：`REPORT_SYSTEM_PRODUCT_NAME = 科技专题服务系统`；`reportGenerationSideLine` / `reportSourceAndGenerationLine` |
| 企业域报告 | `enterpriseDomainReports.ts` 四处来源说明 |
| 服务链报告 | `serviceDomainReports.ts` 一处 |
| 评估报告 v2 | `evalReportDocument.ts` ⑦ 节 bullets |

**未改**：`portal/messenger` / `route-sync` / `sessionExpired` 的 `source` 标识（门户协议，非页面文案）。

### 验收

- 产业诊断/企业评估等报告阅读器「生成侧」为 **科技专题服务系统**，全文无 `lumen-ui-topic`。
- `node src/components/report/reportExport.selfcheck.mjs` 通过。

### 代码状态

- 已 push **`lumen-ui-topic` `a8dfca5`**。

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
| 027-003 | 对比篮标签去重 | `CompareItemCard.vue` |
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

# LUMEN-SVC-FE-WORKSPACE-VISUAL-C1 · 派单厚包

> 监管：`human:侯佳伟` · 长任务已授权 · **人令：必须按 demo-ui-topic 原型复刻，禁止功能空壳**  
> 仓：`lumen-ui-topic` · `origin/dev` · ponytail **full**

## 问题

WORKSPACE-L01 仅短板 Job + Alert/Empty 简壳；与 Demo `ServiceOrgAnalysisPage` / `ServiceChainEcosystemPage` / `ServiceRecommendPage` / `ServiceMaintenancePage` 偏差过大。

## 硬验收

1. **机构分析** `/service/institution-judgment`：三 workspace（field/trend/capability）+ 页内「当前分析/记录」双 Tab；上下文条（领域/已选机构/对比篮）；过程壳/结果区结构对齐 Demo。无 Job 白名单时：**UI 全套保留**，结果诚实空 + 待核验，禁止只 Alert+Empty。
2. **生态** `/service/chain-analysis`：短板已接线则加满 Demo 配置区/结果结构；图谱/深圳 Tab **结构对齐**（metro/图区骨架），无白名单不伪跑。
3. **招引/培育** `/service/institution-decision`：双 Tab + 配置面板 + 结果/记录壳对齐 Demo。
4. **维护** `/service/maintenance`：分区 Tab + 列表壳对齐 Demo（写侧可 disabled）。
5. 样式：移植必要 `serviceCenter.css` class（context-bar / workbench / eco-metro 等），对照 Demo + `industryDiagnosis.css`。
6. handoff V1–V7；只调 Java；D12；commit `[agent:frontend-agent]`。

## 真源

- Demo：`repos/demo-ui-topic/src/app/pages/service-center/Service{OrgAnalysis,ChainEcosystem,Recommend,Maintenance}Page.tsx` + 子视图 + `serviceCenter.css`
- 现错：`repos/lumen-ui-topic/src/views/service-center/Service{OrgAnalysis,ChainAnalysis,Recommend,Maintenance}Page.vue`
- 兄弟过程壳：本仓 CHAIN `IndustryAnalysisProcessShell` / `industryDiagnosis.css`

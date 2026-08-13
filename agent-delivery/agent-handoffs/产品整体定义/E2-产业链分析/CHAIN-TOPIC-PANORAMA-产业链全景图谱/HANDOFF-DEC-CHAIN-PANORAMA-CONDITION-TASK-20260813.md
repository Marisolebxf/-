# HANDOFF · 全景条件分层与预跑秒开

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:product-agent`（用户签字后落实 Demo） |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |
| ponytail | `full` |
| 说明 | 无独立 ready registry 任务；未劫持 `CHAIN-UX-L06`。现场体验修订，已写 DEC 并改 `demo-ui-topic`。 |

## 范围

全景图谱「本次工作上下文」：分析对象 = 0 级产业，所属产业链 = 1 级链，数据截至可选择。默认预跑秒开；改条件后「开始分析」套分析过程壳。本页无「查看报告」、无「查看分析记录」。

## 产物

- DEC：`DEC-CHAIN-PANORAMA-CONDITION-TASK-20260813.md`（签字 `human:淮政玮`）
- 五件套 v1.6：USM / IA / UX-SPEC / Wireframe / TRACE
- Demo：`IndustryPanoramaPage.tsx`、`industryPanoramaModel.ts`、`industryChainTaskType.ts`、`industryAnalysisShell.tsx`
- 自检：`node --test tests/industry-panorama-five-pack.test.mjs tests/industry-panorama-contract.test.mjs`

## 体验入口

`http://localhost:5173/industry-center/panorama`

默认应直接出图（推荐产业 + 第一条可用链 + 最新数据截至）。改产业/链/时间后出现「开始分析」，进入分析过程壳；完成后点「查看分析结果」刷新图谱。本页无「查看报告」。

## 非目标

未改诊断/区域/深圳页内 Select；未改企业篮。

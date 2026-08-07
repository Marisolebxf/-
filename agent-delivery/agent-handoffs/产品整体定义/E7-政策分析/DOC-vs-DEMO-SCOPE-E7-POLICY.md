# 文档 vs Demo 范围 · E7 政策分析

> 基于 `templates/doc-vs-demo-scope-template.md`  
> **状态**：`draft`（证据已按 2026-08-07 Demo 初填；S-04/S-05 为缺口）  
> **Demo 前缀**：`/policy/*`、系统 Shell 对比篮/任务浮层  
> **走查**：`WALKTHROUGH-E7-POLICY.md`  
> **日期**：2026-08-07

## 1. 主表

| ID | 能力 | 文档 | 分类 | Demo 证据 | 备注 |
|---|---|---|---|---|---|
| S-01 | 政策查询（智能/查政策/高筛）只入篮 | US-E7-POL 查询故事；UX-SPEC J-E7 | `demo_must` | `PolicyTopicSearchPage` 等 | 无深度分析直达 |
| S-02 | 门户政策扶持展示只入篮 | US-E7-POL-08；TAB-MERGE-A；NO-GLOBAL-FILTER；STATS-MAP-DENSITY；STATS-INDUSTRY-COMPARE；RANK-PRESENTATION；SHENZHEN-MIRROR | `demo_must` | 四 Tab；map 地图/列表双视图；深圳 S1 四段镜像（无力度榜）+各区对照+共享产业 | 产业禁空；对照仅 stats≤5 且同级；全国档无对照；展示对比≠发起分析；力度仅概览 P-20 |
| S-03 | 系统对比篮·产业 Tab 发起政策三项 | US-E7-POL-05；DEC-E7-POLICY-LAUNCH-FROM-INDUSTRY-BASKET | `system_shared` | `IndustryCompareBasketPanel` + Registry 三项；**无政策 Tab** | 走查 B；已修订 |
| S-04 | 三项分析配置→任务→结果 | US/UX；SYS-JOBS | `demo_must` + `system_shared` | `PolicyAnalysisWorkspace` + `policyTaskType.ts`（Gate 内） | 走查 C 人工点验 |
| S-05 | 报告 HTML→PDF | US；ENT-EXPORT | `system_shared` | 三页 `data-report-*` + `policy:report:{template}` | 走查 D 人工点验 |
| S-06 | 维护管理·门户内容样例工作流 | US-E7-POL-09；ENT-OPS | `demo_must` | `/policy/maintenance` 门户组 | 状态机可点通 |
| S-07 | 维护管理·其余菜单项（对齐 ENT-OPS） | US-E7-POL-09；GAP | `placeholder` | 菜单可达+占位 | **禁止删组删项**；勿称已交付 |
| S-08 | 展示系统政策跟踪 / 核增对比结果页 | IA 不承接 | `out_of_round` | — | 非本包 |
| S-09 | 独立政策任务中心/下载中心 | IA 不承接 | `out_of_round` | — | 用系统浮层+资产 |
| S-10 | 旧 policy-center 批次任务 | — | `out_of_round` | `taskType: policy_analysis_batch` | **勿**作 E7 金样例 |

## 2. 系统能力引用

| 系统能力 | 接入卡 | 金样例验收 |
|---|---|---|
| SYS-ANALYSIS-JOBS | `SYS-CAPABILITY-ADAPTER-E7-POLICY.md` §3 | ☐ G1–G7 |
| ENT-COMPARE | 同上 §4 | ☐ 入篮→分发→返回 |
| ENT-EXPORT | 同上 §5 | ☐ HTML 再 PDF |

## 3. 维护管理拆栏（防「写了没跑出来」）

| 组 | 分类 | 验收标准 |
|---|---|---|
| 门户内容（编辑/审/发） | `demo_must` | draft→审核→发布可点；前台只读消费已发布 |
| 主体/配置/其它对齐 ENT-OPS 的项 | `placeholder` | 左侧菜单在、进入见占位说明 |
| 未在 INDEX/GAP 登记的「文档想象项」 | `defined_only` 或删文档 | 不得进 Demo 话术 |

## 4. 样式

| 项 | ☐ |
|---|---|
| Design.md §14 覆盖查询/篮分发后配置/过程/结果/维护样例 | |
| UX-UE §19 | |
| 未遵守点列入 as-built 或当轮修 | |

## 5. 政策分析下一步建议顺序

1. **接线**三分析页 SYS-JOBS（`POLICY-TASK-TYPE-CONTRACT.md`）→ 走查 C 过 G1–G7。  
2. 报告弹层对齐 ENT-EXPORT → 走查 D。  
3. 回归对比篮**产业 Tab**政策三项（S-03；确认无政策 Tab）→ 走查 B。  
4. Design/UX 走查三项分析页（走查 E），不改系统壳。  
5. 维护管理只承诺 S-06；S-07 占位话术说清（走查 F）。

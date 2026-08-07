# 系统能力接入登记卡 · E7 政策分析

> 基于 `templates/sys-capability-adapter-card-template.md`  
> **状态**：`draft`（对比篮已接；专题三页 SYS-JOBS / 报告触发 **已接线**——§3.3；G1–G7 待人工点验）  
> **业务包**：`E7-政策分析/`  
> **配套**：`POLICY-TASK-TYPE-CONTRACT.md` · `WALKTHROUGH-E7-POLICY.md` · `DOC-vs-DEMO-SCOPE-E7-POLICY.md`  
> **金样例域**：enterprise（任务/篮/报告）+ industry-center（`chain:{module}:{key}`）  
> **日期**：2026-08-07

## 0. 元数据

| 字段 | 值 |
|---|---|
| module_key | E7-POLICY |
| 系统壳 Owner | 高颖；架构会签按需 |
| 关联 ASC / DEC | `DEC-E7-POLICY-LAUNCH-FROM-INDUSTRY-BASKET-20260807`（产业 Tab 发起；**移除政策 Tab**） |

## 1. 接入范围

| 系统能力 | 本域 | 说明 |
|---|---|---|
| SYS-ANALYSIS-JOBS | **是** | 三项分析 + 报告任务；壳不改 |
| ENT-COMPARE | **是** | **产业 Tab** 发起政策三项；无政策文档 Tab |
| ENT-EXPORT | **是** | 政策只交内容协议与 fingerprint |
| SearchScaffold / ENT-OPS 壳 | **是** | 查询工作台 + 维护管理菜单形态 |

## 2. 对象与键

| 项 | 取值 |
|---|---|
| object_type（分析） | `industry` |
| 稳定键 | `industry_id`（URL：`object_ids[]`） |
| 对比篮发起 tab | `industry`（`IndustryCompareBasketPanel` 挂政策三项） |
| 政策 Tab | **已移除** |
| 单次容量 | 1 个产业 |
| 存储隔离 | 禁止读写企业 enterprise storage key |
| 入篮宿主（产业） | 产业查询；政策查询仅暂存文档 |

## 3. SYS-JOBS 适配

### 3.1 task_type 登记（与 `policyAnalysisRegistry` 对齐 · 2026-08-07）

| 分析/报告 | Registry key | route | task_type（稳定值） | 过程/结果 | 完成后 |
|---|---|---|---|---|---|
| 政策时序分析 | `policy_timeseries` | `/policy/overview` | `policy:overview:policy_timeseries` | 配置→过程→结果 | 停进度页，手动查看结果（对齐产业链） |
| 区域政策对比 | `policy_region_compare` | `/policy/analysis` | `policy:analysis:policy_region_compare` | 同上 | 同上 |
| 深圳政策现状 | `policy_sz_3d` | `/policy/recommendation` | `policy:recommendation:policy_sz_3d` | 同上 | 同上 |
| 政策分析报告 | — | 结果页弹层 | `policy:report:{template_id}` | ENT-EXPORT | 个人资产投影 |

> 格式：`policy:{surface}:{analysisKey}`。细则见 `POLICY-TASK-TYPE-CONTRACT.md`。  
> **禁止**把 `object_ids` / 地区 / 权重拼进 task_type。  
> **禁止**照抄旧 `policy-center` 的 `policy_analysis_batch`。

### 3.2 金样例场景（相对企业）

| # | 场景 | 实测 | 差异 |
|---|---|---|---|
| G1 | 提交后离页，浮层可见 | ☐ 待点验 | Workspace 已 submit |
| G2 | 同 task_type 恢复原任务 | ☐ 待点验 | findResumable 已接 |
| G3 | 不同分析可并行 | ☐ 待点验 | 三 key 三 task_type |
| G4 | 完成后停进度页/与 UX-SPEC 一致 | ☐ 待点验 | 手动「查看分析结果」 |
| G5 | 失败重试新 task_id | ☐ 待点验 | 返回配置再提交 |
| G6 | 与对比篮互斥展开 | ☐ 壳层可回归 | 与企业/产业共用 Shell |
| G7 | 不串企业 task/storage | ☐ 待点验 | `policy:*` 前缀隔离 |

### 3.3 as-built（2026-08-07）

| 位置 | 现状 | 备注 |
|---|---|---|
| `PolicyAnalysisWorkspace` + `policyTaskType.ts` | 配置→过程→结果；稳定 `policy:{surface}:{key}` | Gate 内挂载 |
| 三结果页导出 | `data-report-task-type=policy:report:{template}` + fingerprint | 走查 D |
| `pages/policy-center` | 仍有 `policy_analysis_batch` | 非 E7 金样例 |
| `IndustryCompareBasketPanel` | 产业 Tab 挂政策三项分发 | 走查 B（修订） |
| `PolicyCompareBasketPanel` | **已删除** | 政策 Tab 移除 |

## 4. ENT-COMPARE 适配

| 项 | 取值 |
|---|---|
| 分发三项 | Registry：`policy_timeseries` / `policy_region_compare` / `policy_sz_3d` |
| 分发参数 | `source=compare-basket` + `object_type=industry` + `object_ids[]` + `object_names[]` + `analysis_type` |
| 目标页 | 「来自对比篮 · 产业」；调整对象 → 产业 Tab |
| 混选 | 政策三项仅产业对象；产业链不可发起政策分析 |

## 5. ENT-EXPORT 适配

| 项 | 取值 |
|---|---|
| 本域职责 | `report_template_id`、章节数据、fingerprint 输入 |
| 禁止 | 跳过 HTML 直出 PDF；独立政策下载中心；改 Reader 壳 |

## 6. 样式挂载

| 检查 | ☐ |
|---|---|
| Design.md §14（查询/配置/过程/结果/维护） | |
| UX-UE §19 | |
| 对照企业过程页 + 系统浮层视觉 diff | |

## 7. 政策开工检查（本轮优先）

1. **先接线**专题三页 → `submitSystemAnalysisTask`（§3.1），再跑 `WALKTHROUGH-E7-POLICY.md` C 段。  
2. 对比篮**产业 Tab**挂政策三项：走查 B 段回归；确认无政策 Tab。  
3. 报告：结果页走系统弹层，勿仅 Toast（走查 D）。  
4. 维护管理：DOC-vs-DEMO 拆清「门户样例必跑 vs 菜单占位」。  
5. 壳层 bug → 回系统包修；业务适配 bug → 留在 E7。

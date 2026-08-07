# 政策 task_type 契约（对齐产业链金样例）

> 实现目标文件建议：`demo-ui-topic/src/app/pages/policy/policyTaskType.ts`  
> 权威分析键：`policyAnalysisRegistry.ts` 的 `PolicyAnalysisKey`

## 稳定格式

```text
policy:{surface}:{analysisKey}
```

参数（对象列表、地区、时间、权重）只进 route query / 配置快照，**禁止**拼进 task_type。

## Registry 对照（as-built 2026-08-07）

| analysisKey | 标题 | route | 建议 task_type |
|---|---|---|---|
| `policy_timeseries` | 政策时序分析 | `/policy/overview` | `policy:overview:policy_timeseries` |
| `policy_region_compare` | 区域政策对比 | `/policy/analysis` | `policy:analysis:policy_region_compare` |
| `policy_sz_3d` | 深圳政策现状分析 | `/policy/recommendation` | `policy:recommendation:policy_sz_3d` |

报告：

```text
taskType = policy:report:{report_template_id}
```

导出控件须带 `data-system-report-trigger`，并设置 `data-report-task-type` / `data-report-fingerprint` / `data-report-template-id`。

## as-built（2026-08-07）

| 位置 | 现状 |
|---|---|
| `policyTaskType.ts` + `PolicyAnalysisWorkspace`（经 Gate） | 已 `submitSystemAnalysisTask`；完成后停过程页，手动查看结果 |
| 三结果页导出 | `data-report-task-type=policy:report:{template}` + fingerprint |
| `pages/policy-center` AnalysisPage | 仍有 `policy_analysis_batch` —— **非** E7 金样例；勿照抄 |

## 恢复辅助（实现时对齐产业链）

建议提供与 `industryChainTaskType.ts` 同构的：

- `policyAnalysisTaskType(surface, analysisKey)`
- `findActivePolicyAnalysisTask` / `findResumablePolicyAnalysisTask`
- 完成后停进度页、手动「查看分析结果」再进结果（除非本域 UX 另批）

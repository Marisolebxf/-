# 19 — POLICY-MRC：实时指标

> **读者**：GDF。MRC = 指标实时计算。用户在页面上触发才算。  
> **本包不配 T+1，不放脚本，不把 repro 拷进 `scripts/`。**

| 指标 | 结果表（已有，本包不写） |
|---|---|
| `M_POLICY_MATCH` 政策匹配推送 | `gkxlumenx_ads.policy_match` |
| `M_POLICY_SIMULATE` 政策效果推演 | `gkxlumenx_ads.policy_simulate` |
| `M_POLICY_DS_11_POLICY_EVAL_012` 智能摘要与结论推送 | 不在本包落表 |
| `M_POLICY_DS_11_POLICY_EVAL_015` 实施路径与风险辅助 | 不在本包落表 |

匹配、推演同时在 `17` 第 3 节（QPOL-03、QPOL-02）。规则未签之前，在线链也不用未签权重去算、不去灌数。

GDF 不要为这四条建 Python 节点，不要把它们挂到 Wave B 成功之后。

## 血缘

这四条是业务操作时才算的实时指标，计算不在 GDF 平台展开，所以不能从 GDF 自己的作业里直接取出血缘。

讨论结论：可以把计算的血缘导入 GDF 的「工位」。导入之后，GDF 用接口对外提供指标血缘，不限于这四条。三类来源（平台上 Python 脚本自身可知的、经 API 调入的、业务实时计算的）写在 [21-数据血缘.md](21-数据血缘.md)。本章仍不配 T+1，不建节点。接口未接通。

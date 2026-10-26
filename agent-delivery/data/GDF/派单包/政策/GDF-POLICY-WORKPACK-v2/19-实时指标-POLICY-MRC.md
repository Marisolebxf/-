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

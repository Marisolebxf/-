# SCI-INT-P00 · 底座：卡片模板 + 283 叶 / 93 指标基线清单

- 状态：in_progress → integration（AV-0）；task_type=chore
- 执行：`agent:coordinator-agent` · 监管 `human:淮政玮` · claim_type=coordinator_dispatch
- ponytail: N/A（分析叶，`ponytail off`）

## 1. 范围与实现

按 `SCI-INT-总派单.md` §4「P00 底座」：

| 产物 | 内容 |
|------|------|
| `产物/P00-baseline.yaml` | SRS 283 行（excel_row / seq / name / path / 归属叶 A01–A15 / DS 页面映射）+ 指标 93 条（metric_id / domain / algorithm_type / 归属叶 B02–B09）+ 久新 51 行（row_id / 维度 / 交付形态 / 确认状态） |
| `产物/_card-template.yaml` | 总派单 §2 卡片 schema 原样（加注释） |
| `产物/_work/P00-check.py` | 生成 baseline + assert：SRS 196+87、每个 A 叶行数 = 范围、SRS 文件内所有块都有归属、指标 32+39+22 且唯一、STAT 6 / MODEL 3、久新 51 行唯一且 SQL 3 / Python 6 / API 42 |

指标清单与类型取自 MCP `metric-registry` `metric-query`（domain=TALENT/TECH/ORG，2026-10-18），未读 registry 文件。

## 2. 验收证据

```
python 产物/_work/P00-check.py
OK srs=283 metrics=93 jiuxin=51
```

| 计数 | 范围 | 已入基线 | 差集 |
|------|------|----------|------|
| SRS 叶 | 283 | 283 | 0 |
| 指标 | 93 | 93 | 0 |
| 久新行 | 51 | 51 | 0 |

## 3. 偏离说明

无。产物文件名按 §4 用 `P00-baseline.yaml`，不用 `SCI-INT-P00.yaml`。

## 4. 架构合规自检

| 铁律 | 结论 |
|------|------|
| 算法只在 Python / 调用链 / Nebula / 可观测 / CI | ✅ 不涉及（纯清单） |
| D8 / D9 / D10 | ✅ 不涉及；指标类型来自 MCP，未自填 |
| D12 demo/lumen 隔离 | ✅ 未改任何业务仓 |
| 注册表 MCP 规约 | ✅ 任务 / 指标均走 MCP |

## 5. cost

- actual_tokens: ~60k · model_used: claude-opus（coordinator 会话） · actual_cost: ~$1.5 · cost_warn: green

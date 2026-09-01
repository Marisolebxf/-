# POLICY-PDR-G1-INGEST · 政策维度门 1 故事入库 + 拆单提案

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:coordinator-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `N/A`（定义·编排入库，不写业务代码） |

## 范围与实现

依赖 `POLICY-METRIC-OPEN-L01` / `POLICY-UX-L01` 均已 `done`。按 `gkx-story-library-ingest` 跑门 1 流水线，**未 merge `task-registry`**，实现叶保持 `proposed`。

| 模块 | 故事入库 | 提案 |
|------|----------|------|
| `E7-政策分析` | 11 条（`US-E7-POL-01`～`09`，含 `01b`/`01c`） | `POLICY-MOD-E7-*` 5 leaf + 1 Theme |
| `DS10-12-科技政策跟踪` | 11 条（`US-DS-POL-01`～`11`） | `DS-POL-TRACK-*` 5 leaf + 1 Theme |

命令：

```text
node scripts/pdr-gate1-story-pipeline.mjs --module E7-政策分析
node scripts/pdr-gate1-story-pipeline.mjs --module DS10-12-科技政策跟踪
```

## 偏离说明

- 模板原先无政策 `module_map`，已补 `E7-政策分析` / `DS10-12-科技政策跟踪`，避免合成 `ENT-MOD-*` 前缀。
- 脚本默认 `suggested_yaml.epic=E-ENT-SCRUM-PDR`；入库后已把本批提案 epic 改为 `E-POLICY-PDR`。
- `DS-POL-TRACK-FE-WIRE-L01` 默认仓是 `lumen-ui-topic`；已改为 `lumen-ui-science-pc`（展示 D12）。
- `US-E7-POL-08` 抽取 WARN「无正文」：USM 有完整 As/Want 句，但含破折号 `——`，提取正则未吃到。故事已入库，正文空，人工可补。
- **禁止**把本批 leaf 标 `ready`；须飞书「建单已采纳」才 merge 成 registry `backlog`；`ready` 仍等门 3 `*-DG-G3`。

## 产物清单

| 文件 | 说明 |
|------|------|
| `agent-delivery/user-story-library.yaml` | 91 → **113** 条（+22） |
| `agent-delivery/story-impl-proposals.yaml` | 90 → **102**（+12） |
| `agent-delivery/story-impl-templates.yaml` | 政策两行 `module_map` |
| 本 handoff | `agent-handoffs/政策模块-E7/POLICY-PDR-G1-INGEST.md` |

## 验收证据

- 流水线两次 exit 0
- 故事库含 `E7-政策分析` 11、`DS10-12-科技政策跟踪` 11
- 提案 `status=proposed`，`skip_create=false`（Theme `skip_create=true`）
- 未跑 `--project-feishu`（未投影飞书待审建单）

## 架构合规自检

| # | 铁律 | 结果 |
|---|------|------|
| 1 | 算法只在 Python | ✅ 未写算法 |
| 2 | 调用链 | ✅ 提案 API 仍走 Java |
| 3 | 图谱 Nebula | ✅ 未改图谱仓 |
| 4 | 可观测性 | ✅ N/A |
| 5 | CI/CD | ✅ 无业务仓 push |
| 6 | demo2 不 merge lumen | ✅ 未改 demo/lumen 代码 |
| 7 | 共享聚合 | ✅ 提案不直连 Python |
| 8 | ADS/Mock | ✅ N/A |
| 9 | Design.md | ✅ N/A |
| 10 | D9 | ✅ 不改 seed |
| 11 | D10 | ✅ N/A |
| 12 | D12 | ✅ 展示 FE 提案仓改为 science-pc |

## Cost 回填

| 字段 | 值 |
|------|-----|
| actual_tokens | 18000 |
| model_used | cursor-grok-4.6 |
| actual_cost | 0.4 |
| cost_warn | green |

## 建议下一状态

definition → **done**（入库 DoD 已满足）。实现叶不得标 ready。

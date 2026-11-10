# POL-L2-PC1-STRUCT-FDE-L01 · 603 政策库结构化 · K8s 冒烟收口

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:coordinator-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `N/A`（本文件为冒烟/会签收口，非本会话写码） |

## 范围与实现

- 需规 603：政策选择+关键字、同排结构化抽取、`hasClauses` 门控摘要、分类标签/字段映射表非空。
- 前端落地 `822bd15`；本会话只做已发布页冒烟 + `governance/results` API。
- 合规演示用例：`工程过程/04-系统集成/05-展示系统集成/合规演示用例/POL-L2-PC1-STRUCT-合规演示用例.md`。

## 偏离说明

- 用例样本 `18319069` 现网 `hasClauses=false`，摘要走「尚未结构化」门控（仍可验门控）。「选定已结构化即出摘要」需另挑真已结构化 id。

## 产物清单

- Handoff：本文件
- 已部署前端：`gkx-lumen-pc:822bd15b` @ `http://10.50.69.111:30891/policy/policy-governance`

## 验收证据

| 项 | 结果 |
|---|---|
| 603-sel-1 政策选择 | ✅ 条件栏标签「政策选择」 |
| 同排抽取 | ✅ 「结构化抽取」按钮可见 |
| 门控空态 | ✅ 「该政策尚未结构化，请先点击「结构化抽取」」 |
| 两表非空 | ✅ 分类标签体系 / 字段映射均有多行 |
| KPI | ✅ 页眉库结构化 0.2% ≈ API `coverageRate=0.002` |
| API results | ✅ 200，`structuredPolicyCount=41` |

联调通过。

## 架构合规自检

- 调用链：浏览器 → gateway → display `/display/v1/policy/governance/**`（抽取经 display parse）✅
- 算法只在 Python：抽取条款走 display→算法，Java 不跑 NLP ✅
- Nebula：本叶不涉及图谱写 ✅
- D8 / D10：沿用已推 Arco FE，本会话未改 UI ✅
- D9：页眉覆盖率读接口，未手写改绿 ✅
- D12：只验 lumen，未调 demo-* ✅
- 可观测 / CI：已发布镜像点验，无新码需补埋点 ✅

## Cost 回填

| 字段 | 值 |
|------|-----|
| actual_tokens | 20000 |
| model_used | cursor-grok-4.5 |
| actual_cost | 0.4 |
| cost_warn | green |

## 遗留风险

- 已结构化摘要与失败保留摘要需另样；本波 UI 门控+两表已过。

## CI/CD（必填）

- 分支：`origin/dev`（`lumen-ui-science-pc`）
- commit：`822bd15`
- 部署：`zhipu-tts` / `gkx-lumen-pc:822bd15b` / NodePort `30891`
- K8s rollout：成功

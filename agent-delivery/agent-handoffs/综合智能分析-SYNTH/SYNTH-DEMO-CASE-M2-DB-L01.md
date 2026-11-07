# SYNTH-DEMO-CASE-M2-DB-L01 Handoff — M2 demo 库 SYNTH 数据情况调研

- **任务**：`SYNTH-DEMO-CASE-M2-DB-L01`（长任务 M2 叶，总控：`../SYNTH-合规演示用例-长任务总控.md`）
- **执行**：agent:data-agent（子智能体，本会话 coordinator 收口）
- **监管**：`supervised_by=human:徐滕强`；`claim_type=coordinator_dispatch`
- **仓**：`gkx-orchestration`（origin/dev）
- **强度**：ponytail: full（零新依赖：database-mcp 既有连接只读查询；产物单文件）
- **日期**：2026-11-07

## 1. 范围与实现

按总控 §3 清单对 demo 库（`demo_gkxlumenx_ads` 27 表 + `demo_gkxlumenx_ai` 1 表，实例 `10.50.11.76:3306`）完成 28/28 表实查：行数 / region×window 分布 / 最新批次与 `calc_status` / `is_mock` 比例 / 覆盖缺口。只读，零写库，口令未入任何文件。

关键结论（详见调研报告 §0/§6）：

1. 全部数据 `is_mock=1`；窗口仅「最近3年」有活力/要素行；1y/5y 仅 137 四维表（4城×3窗×4维=48）全覆盖。
2. 协同 ADS 六结果表全空 → 演示走 gapfill 三表输入 + 实时计算；`synth_collab_batch_meta` 有深圳/广州快照可做坏快照用例。
3. 三类数据缺陷：非深圳行 `region_name` 误标「深圳」（region_code 正确）；深圳双批次冗余（查询须按 `calc_batch_created_at` 取最新）；`synth_elem_index` 四城同源扰动。
4. `synth_vit_trend` 表不存在——趋势由 `synth_vit_index` 2022/2023 历史批次承载（总控 §3 清单据此修正）。
5. 8 项覆盖缺口已列报告 §6，供 M3 逐条判定、M4 归并。

## 2. 对账

与 `sdd/reconciliation/需规功能一致性审计-20261107.md` 行数声明 **7/7 零差异**（四维 48 / 关系年 35 / 产出 20 / 孤立 8 / 活力 gapfill 三表各 4）。

## 3. 产物清单

- `agent-delivery/agent-handoffs/综合智能分析-SYNTH/合规演示用例/data-survey-20261107.md`（365 行；唯一产物）
- 本 handoff

## 4. 验收证据

- 28 表实查记录 + 对账结论见调研报告各节（database-mcp 只读连接 `gkx-mysql/demo-gkxlumenx-ods`）
- 受阻表：0；SSH 路径按熔断纪律 2 次后停用（无 mysql 客户端），未空转

## 5. 架构合规自检

- ✅ 只读 demo 库；未写 ODS/DWD/ADS/正式 `gkxlumenx_*`
- ✅ 未改业务仓、未改 `metrics/registry/` seed
- ✅ 未触碰 ssh-executor 探活禁令（同一意图 ≤2 次即停）
- ✅ 凭据未落盘
- ✅ cicd: skip（纯编排仓文档）

## 6. cost

| 字段 | 值 |
|---|---|
| actual_tokens | ~85000 |
| model_used | glm-5.3-flash |
| actual_cost | 0.10（估算：子智能体读库+写报告） |
| cost_warn | green |

## 7. ponytail

ponytail: full——复用 database-mcp 既有分组连接与仓内 seed SQL 元数据，未新增连接配置文件；报告单文件交付，§0 速览直接供 M3 消费，无重复对账段。

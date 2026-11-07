# SYNTH-DEMO-CASE-M1-USM-L01 Handoff — M1a 三叶 USM 动作×条件枚举用例总册

- **任务**：`SYNTH-DEMO-CASE-M1-USM-L01`（长任务 M1a 叶，总控：`../SYNTH-合规演示用例-长任务总控.md`）
- **执行**：agent:product-agent（子智能体，本会话 coordinator 收口）
- **监管**：`supervised_by=human:徐滕强`；`claim_type=coordinator_dispatch`
- **仓**：`gkx-orchestration`（origin/dev）
- **强度**：ponytail: full（单文件产物；CASE 编号规范照总控 §4，无新框架）
- **日期**：2026-11-07

## 1. 范围与实现

按总控 §2/§4 产出 `合规演示用例/00-用例总册.md`（229 行）：三叶 USM 动作清单（活力 16 / 要素 16 / 协同 18 条，均回指页面实码）× 条件枚举矩阵，共 **47 条 CASE**：

| 叶 | 编号 | 计数 | 基准 | 关键覆盖 |
|---|---|---|---|---|
| 活力 | CASE-VIT-01~16 | 16 | ≥14 | 双权重档 + WEIGHT_MAIN 直达 + legacy_unknown 反例 + 非法档 400 + 非默认 404 + 失败批只读 |
| 要素 | CASE-ELEM-01~14 | 14 | ≥12 | 137 四维 pending_registration + 全景分类默认限定 + 三透镜/贡献/报告 + force 重跑 |
| 协同 | CASE-COLLAB-01~17 | 17 | ≥15 | 坏快照 batch_meta_missing + 产业筛选服务端过滤 + LLM 降级 + 报告 PDF + gapfill_transitional |

## 2. 合规自检（子智能体自检 + coordinator 抽查）

- 既有 reason 值逐字保留：`batch_meta_missing` / `no_year_on_source` / `cluster_rule_unclosed` / `IntelBatchSnapshotNotFound` / `legacy_unknown`（grep 抽查命中）
- 过渡标识三件套落进期望列：`is_mock=1` / `pending_registration` / `gapfill_transitional`
- 未编造正式指标名；未改 registry/业务仓（coordinator 核验 git status 零业务仓改动）

## 3. 给下游的交接

- M1b：按本册 CASE 编号拆 `vitality-cases.md` / `element-cases.md` / `collab-cases.md` 并细化步骤与数据依赖列，编号零漂移
- M3：数据依赖去重清单（ADS vit 5 张 / elem 8 张 / `_ai` 四维 1 张 / 活力 gapfill 3 张 / 协同 gapfill 3 张 / 协同 ADS 8 张 / DWD 汇聚源）→ 与 M2 调研报告 §0/§6 逐条判定

## 4. 产物清单

- `agent-delivery/agent-handoffs/综合智能分析-SYNTH/合规演示用例/00-用例总册.md`（唯一产物）
- 本 handoff

## 5. 架构合规自检

- ✅ 纯编排仓文档；cicd: skip
- ✅ 未改 `metrics/registry/` seed；未改业务仓
- ✅ 用例期望与功能合规过渡口径（功能合规过渡设计-137与C05）一致

## 6. cost

| 字段 | 值 |
|---|---|
| actual_tokens | ~120000 |
| model_used | glm-5.3-flash |
| actual_cost | 0.15 |
| cost_warn | green |

## 7. ponytail

ponytail: full——单文件交付；CASE 表格列直接复用总控 §4 字段规范；无新增目录层级（沿用总控指定落点）。

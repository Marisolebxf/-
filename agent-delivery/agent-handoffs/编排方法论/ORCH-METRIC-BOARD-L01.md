# ORCH-METRIC-BOARD-L01 · Handoff

> **任务**：飞书「指标与数据开发进度」看板 — Bitable 新表 + 出站同步脚本
> **agent**：coordinator-agent · **监管**：human:淮政玮 · **完成**：2026-08-01
> **状态**：review（待监管人在飞书侧配置视图并确认）

## 1. 范围与实现

2026-08-01 项目负责人（淮政玮）会话内批准建单：单独建一个指标与数据开发进度看板，展示各指标进展、数据设计情况、数据源情况，供整体开发团队对齐。

实现：与任务看板同一 Bitable 应用（`JI94bBxwsaIzyMsMBrYcPJscnDc`）内新建数据表「指标与数据开发进度」（`tblw8ZPW6geOuyqt`），一行 = 一个 metric_id，20 列覆盖 D1~D4 四维 + 综合就绪 + 卡点责任方。真源 = readiness 矩阵 + cfg_metric 种子 + gap catalog，飞书只读投影不回写。

## 2. 产物清单

| 产物 | 路径 |
|------|------|
| 配置（列字典/显示映射/视图建议） | `agent-delivery/feishu-metric-board.yaml`（table_id 已回填） |
| 同步脚本（自动建表建列 + upsert） | `scripts/sync-feishu-metric-board.mjs` |
| 使用指南 | `agent-delivery/feishu-metric-board.md` |
| 看板实体 | Bitable 表 `tblw8ZPW6geOuyqt`（147 条已写入） |

## 3. 验收证据

- 真跑建表 + 首同步：`147 条：新建 147，更新 0` → `[done] 看板已同步`
- 幂等复跑：`新建 0，更新 147`（按「指标ID」upsert，无重复行）
- dry-run 抽样核对 3 条（M_ENT_MARKET_SHARE / M_ENT_PATENT_GRANT_COUNT / M_CHAIN_MARKET_SIZE）：四维状态、缺口文案、综合就绪、卡点责任方均与真源一致
- 覆盖：147 = cfg_metric 种子 129（ENT 49 / CHAIN 60 / POLICY 19 / TNIE 1）∪ ENT 矩阵独有 18（KEYPANO/STAR/GAP-* 未注册条目）；四维已评估 53

## 4. 与建单时点的偏离说明

1. **范围扩大（129→147 & 全域）**：建单时按「ENT 49」估计；实测 metrics 目录含 CHAIN/POLICY/TNIE 种子，且执行期间 `ENT-READINESS-MATRIX-ENT-L01`（另一会话）已把 EVAL 13 条矩阵扩成 ENT 全域 53 条并定稿 v1.3 入 policy §2.3。同步脚本按 glob 全量吸收，零边际成本，符合「整体对齐」目标。非 ENT 域标「待四维评估」，矩阵补齐后重跑自动升级。
2. **v1.3.1 增补态适配**：新矩阵引入 D2 `pending`（待首评）与 `n/a`，脚本显示映射已支持。
3. **验收单元列**：原设计单选，因各域编号体系不同（E-2x/C-xx）改文本列。

## 5. 待办（非本任务范围）

- [ ] 监管人在飞书 UI 配置 5 个建议视图（见 feishu-metric-board.md §3，一次性手工操作）
- [ ] CHAIN/POLICY 域 readiness 矩阵产出后重跑同步（矩阵任务另行建单）
- [ ] 可选：把本脚本挂入投影机 board-sync-watch 周期（当前为手动触发，矩阵变更频度低，暂不必要）

## 6. 架构合规自检

- 编排资产变更，无业务代码；cicd: skip_design_only ✅
- 真源分层不变：git YAML 唯一真源，飞书只读投影（与 feishu-bitable.yaml 决策一致）✅
- 无密钥入库（FEISHU_* 仅从 .env 读取；pre-commit 扫描通过）✅
- commit 标注 [agent:coordinator-agent] ✅

# ENT-READINESS-MATRIX-ENT-L01 — 企业全域就绪度矩阵 + 口径侧 Excel→YAML 正式化规约

> 状态：✅ 交付（2026-08-01）· agent:data-agent · 监管 human:淮政玮（项目负责人，视同验收）
> 依赖：D9-READINESS-MODEL-L01（v1.3 模型定稿）

## 1. 范围与实现

用户指令两条：①企业维度按 9 个 METRIC-OPEN 任务结果刷新到 demo-ui-topic（本任务供数据真源，FE 侧见 ENT-MOD-ENT-READINESS-UI-L01）；②王惠派单/提交格式强调 **Excel 正式化为一个 YAML 真源**。

### 1.1 `metrics/registry/metric-readiness-matrix-ENT.yaml`（新建，企业全域 53 条）

- 吸收原 `metric-readiness-matrix-ENT-EVAL.yaml`（13 条原样保留，**旧文件已删除**，避免双真源）
- 新增 40 条：SEARCH 3 / RISK 8（含 seed 补充 NODE_CENTRALITY）/ RECRUIT 9（含 GAP-* 4）/ KEYPANO 8 / STAR 5 / SHENZHEN 7
- D1/D3 按 policy §2.3.2 迁移映射从各模块 gap catalog 的 `mapping_status`/`pending_ref` 推导
- **诚实性**：非 EVAL 模块 D2 一律 `pending`（未评估，v1.3.1 新枚举），禁伪标 ready；`d1=missing` 的 GAP-* 条目 d2~d4 = n/a
- 汇总：D1 aligned 10 / draft 38 / missing 5；D2 ready 11 / partial 1 / missing 1 / pending 35 / n/a 5；D3 full 24 / partial 23 / none 1 / n/a 5；D4 mock 48 / n/a 5

### 1.2 `data-lineage-policy.md` v1.3.1

- D2 枚举增 `pending`（批量登记初始态）
- 矩阵真源改**每要素域一个文件**（`metric-readiness-matrix-{要素域}.yaml`，首例 ENT）
- §2.3.2 增**口径侧提交与正式化**规约（下节）

### 1.3 王惠派单/提交格式（用户要求②）

- `metrics/README.md`（新建）：§2.1 派单话术必含 4 条 / §2.2 data-agent 正式化 6 步 / §2.3 验收清单
- `智能体编排与派单手册.md` §9.6：口径侧派单硬要求块
- 核心规则：**Excel 只是工作底稿，不进仓、不作真源**；每次提交由 data-agent 正式化为对应要素域唯一 YAML 真源（matrix + seed 增量）；禁止平行状态表

## 2. 发现的问题（登记不掩盖）

| 问题 | 位置 | 待办 |
|------|------|------|
| COMPARE registry 标 done 但 gap catalog / 核对记录磁盘缺失（仅派单包） | matrix `coverage_notes` | coordinator 补验证据或订正状态 |
| KEYPANO 8 条（M_ENT_KEYPANO_*）/ STAR 4 条 metric_id 未注册 cfg_metric-ENT-seed | matrix `d1_note` 逐条标注 | 王惠正式化时注册（KEYPANO 归 Q047） |
| OPS 产物为 15 条 capability 非统计指标 | matrix 头注 | 不入四维矩阵，CMS 写侧另行管理 |
| cfg seed 中未被 METRIC-OPEN 触达的 E-20~E-22 部分条目未入矩阵 | matrix 头注 | 待王惠 Excel→YAML 正式化时补齐 |

## 3. 产物清单

- `agent-delivery/metrics/registry/metric-readiness-matrix-ENT.yaml`（新建）；`metric-readiness-matrix-ENT-EVAL.yaml`（删除）
- `agent-delivery/data-lineage-policy.md`（v1.3.1）
- `agent-delivery/metrics/README.md`（新建）
- `agent-delivery/智能体编排与派单手册.md`（§9.6 增补）
- FE 消费侧：demo-ui-topic 契约测试已改指向 ENT.yaml 并全绿（见 ENT-MOD-ENT-READINESS-UI-L01）

## 4. 架构合规自检

设计类任务（cicd: skip_design_only）。不涉及调用链/图谱/算法边界；D9 血缘铁律强化（四维真源唯一化 + 不伪闭合）✅；D10 不涉及；commit 标 `[agent:data-agent]` ✅。

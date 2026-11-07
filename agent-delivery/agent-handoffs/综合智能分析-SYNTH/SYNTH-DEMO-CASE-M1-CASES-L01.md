# SYNTH-DEMO-CASE-M1-CASES-L01 Handoff — M1b 三叶用例细化（47 条零漂移 + 33 处 M2 事实修正）

- **任务**：`SYNTH-DEMO-CASE-M1-CASES-L01`（长任务 M1b 叶，总控：`../SYNTH-合规演示用例-长任务总控.md`）
- **执行**：agent:doc-agent（子智能体，本会话 coordinator 收口）
- **监管**：`supervised_by=human:徐滕强`；`claim_type=coordinator_dispatch`
- **仓**：`gkx-orchestration`（origin/dev）
- **强度**：ponytail: full（三文件交付；六要素结构复用，无新模板框架）
- **日期**：2026-11-07

## 1. 范围与实现

按总册 47 条 CASE 拆分细化三份叶册（编号零漂移）：

| 文件 | 行数 | CASE |
|---|---:|---|
| `合规演示用例/vitality-cases.md` | 508 | VIT-01~16（16） |
| `合规演示用例/element-cases.md` | 460 | ELEM-01~14（14） |
| `合规演示用例/collab-cases.md` | 555 | COLLAB-01~17（17） |

每条含六要素：需规叶引用 / 前置条件 / 操作步骤（URL 参数与 `useSynthCtx.ts` 实码一致）/ 期望结果（含 404/空态/失败分支）/ 数据依赖（含 M2 实际状态）/ 演示备注。

## 2. 对照 M2 的数据事实修正（33 处，叶册内带「（对照M2修正）」标注）

要点（全清单见子智能体汇报）：
- 活力非默认窗收敛为「404/引导开始分析」（G-01）；深圳双批次按 `calc_batch_created_at` 取最新（D-02）；趋势改读 `synth_vit_index` 历史年批（`synth_vit_trend` 表不存在）
- 要素 137 四维=三窗全齐唯一数据面（48 行，`pending_registration`）；ELEM-09 全景为全域汇聚不按城过滤（G-08）；ELEM-12/13 趋势=诚实空态
- 协同全部展示面走 gapfill_transitional + 实时计算；坏快照用不存在 snapshotId 构造（不拿历史快照冒充）；co_project 数字卡=诚实 0 值（G-07）
- 城市名展示风险（D-01）与四城同源扰动（D-03）逐条注记，D 系=缺陷非缺口，M4 登记修复项

## 3. 合规自检（coordinator 抽查复核）

- CASE 头计数 16/14/17 与总册零漂移 ✅（grep `^## CASE-` 复核）
- reason 值 11 个逐字在册 ✅（`metric_not_registered` / `batch_meta_missing` / `legacy_unknown` 等抽查命中）
- 总册未动、零 git 操作、零业务仓改动 ✅

## 4. 给下游的交接

- M3：`condition-fill-matrix.yaml` 逐格判定 47 条；`supported` 带表名+行数证据，`gap` 引 G-01~G-08（D 系走 M4 缺陷登记，不算 gap）
- M4：缺口归并以 M2 §6 + 叶册标注为增量输入；D-01~D-03 数据缺陷单独列修复建议
- M5：LOOP 轮次编排以「演示备注=能演示出结果」的 CASE 优先排轮，诚实空态/拦截类放验证轮

## 5. 产物清单

- 三份叶册（唯一新增产物）+ 本 handoff；总册与 data-survey 未改动

## 6. 架构合规自检

- ✅ 纯编排仓文档；cicd: skip
- ✅ 未改 `metrics/registry/` seed；未改业务仓
- ✅ 多会话保护：其他会话 M/?? 文件未触碰

## 7. cost

| 字段 | 值 |
|---|---|
| actual_tokens | ~140000 |
| model_used | glm-5.3-flash |
| actual_cost | 0.18 |
| cost_warn | green |

## 8. ponytail

ponytail: full——三文件按总册编号机械展开；六要素小节复用统一结构；无新增索引层（叶册附录 A 即修正索引）。

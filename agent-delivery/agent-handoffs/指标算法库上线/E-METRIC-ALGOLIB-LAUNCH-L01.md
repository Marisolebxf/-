# E-METRIC-ALGOLIB-LAUNCH-L01 · 指标更新入库 + 科技专题服务算法库上线

## 1. 背景

- 需求文档：`local-workspace/docs/tasks/investiage/20261023_指标上线算法库系统/需求文档.md`
- 源成果：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/`（565 份学术 MD + `code/*.py` + `*_out.json`，11 道闸全绿，gkx-only）
- 已确认口径：
  - 565 全量进 seed（不只 MODEL/MIXED）；560 原始 + 4 件分解件（载体/突破）+ 1 件 `M_INNOV_RES_REGION_CI`
  - 「97」= `modelFlowRegistry.json` 的 97 个模型页，背后指标以 catalog `metricIds` ∩ 20261021 交付（约 263 个）为准

## 2. 任务拆解（两阶段，阶段间停下等用户决策）

### 阶段 1：S1 王惠入库流程（✅ 已完成，STOP 等决策）

| 件 | 落点 | 实际交付 |
|---|---|---|
| calc-logic MD | `agent-delivery/metrics/calc-logic/{DOMAIN}/{metric_id}.md` | 565（365 覆盖 + 200 新建，含 ORG/TALENT/TNIE 新域）+ 域 README 11 份 + 根 README |
| seed YAML | `agent-delivery/metrics/registry/cfg_metric-{DOMAIN}-seed.yaml` | 11 域 566 条（565 + 存量 seed-only `M_CHAIN_STAGE_HEALTH_SCORE`），9+3 字段全齐 |
| readiness | `agent-delivery/metrics/registry/metric-readiness-matrix-{DOMAIN}.yaml` | 11 域 + TNIE 新建共 12 份，566 行全量重生成 |
| 入库详情 xlsx | `agent-delivery/metrics/指标入库详情-合并-20261023.xlsx` | 566 行 × 29 列（含算法类型/入库时间/指标创建人=王惠） |
| MCP 回写 | `metric-srs-export` + `metric-progress-export` | 《指标需求来源.xlsx》目录 566 行；《指标与数据开发进度.xlsx》566 行 |
| 门禁自检 | `_work/gate_phase1.py` | G1~G6 全 PASS（见 §4） |
| playwright 冒烟 | 算法库 3100（=30897 部署版）5 页 + 科技专题 3000（=30888 本地等价）2 页 | 全部正常渲染，详见 §4 |

### 阶段 2（用户放行后）

1. 范围锁定：97 页 × ~263 指标
2. 分级实现：完全直接/转换 = 真实算（ENT/POLICY/SVC → `demo-algo-ent-analysis`；CHAIN/INNOV → `demo-algo-science`）；部分支持 = 真实算可得依赖 + mock 补缺失依赖；完全不支持 = 全 mock 本地表；均落 `data/precompute/{metric_id}.json`
3. 灌输接口：`POST /v1/system/precompute/run` + `GET /v1/system/precompute/status`
4. flowRegistry 真源：gkx 源表/字段 → 本地结果表 → 计算模块 → 前端
5. AlgoShell 顶栏灌输按钮 + 进度条（红变绿）
6. playwright 全量回归 97 测试页

## 3. 改动清单（执行中滚动更新）

### 阶段 0

- [x] `agent-delivery/task-registry.yaml` 新增任务条目 `E-METRIC-ALGOLIB-LAUNCH-L01`（status: in_progress）
- [x] 本 handoff 文件落盘

### 阶段 1（2026-10-23）

- [x] calc-logic：565 份 MD 生成/更新（`_work/gen_phase1_calc_logic.py`；台账 `_work/extract_ledger.json` 565 条）
- [x] seed：11 个域 YAML 全量重写（`_work/gen_phase1_seed.py`），1697 个折叠标量转单行双引号（`_work/patch_phase1_g3.py`，根治 lib/py 解析差异）
- [x] G3 修复：9 条 definition<50 字的合规化扩写（口径四要素取自 20261021 台账事实，无虚构数字）
- [x] readiness：12 份矩阵全量重生成（`_work/gen_phase1_readiness.py`；旧证据从 git HEAD 快照 `_work/_matrix_head/` 读取，防重跑自污染）
- [x] 域 README：11 份重生成 + 根 README 域表更新（`_work/gen_phase1_readme.py`）
- [x] 入库详情 xlsx：`指标入库详情-合并-20261023.xlsx`（`_work/gen_phase1_xlsx.py`）
- [x] MCP 回写：metric-srs-export（目录 566/明细 743/回填 338）+ metric-progress-export（566 行，overall：待结构设计 536 / 无数据源 30）
- [x] 门禁：`_work/gate_phase1.py` G1~G6 全 PASS
- [x] playwright 冒烟：算法库总览 + entan/basic + chain/panorama + innov/events + policy/basic；科技专题首页 + 深圳专题页

## 4. 自测记录

### 门禁 G1~G6（全 PASS）

- G1：calc-logic MD=583 = seed 566 + 孤儿白名单 17（见 §5）
- G2：`calc_logic_ref` 566/566 全部可解析且文件存在
- G3：seed 9+3 字段零缺陷（definition≥50 字、algorithm_type 枚举合法、无 UNKNOWN）
- G4：seed/readiness 目录 `demo_` 词串零命中（历史词汇消毒 + 存量件豁免登记）
- G5：readiness 566 行与 seed 一一对应，域归属零错位
- G6：PyYAML 与 `metric-registry-lib.mjs` 逐字段一致性 566+566 全等（双解析器）

### 双端渲染验证

- MCP `metric-summary`：total=566，D1 aligned=557/draft=9，D4 mock=566（诚实现状）
- 算法库 UI（本地 3100，对应部署 30897）：总览 + 4 个测试页截图正常（真实数据表、图表、指标列）
- 科技专题 UI（本地 3000，对应 demo 30888）：首页 + 深圳专题页截图正常，0 console 错误
- 远程 10.50.69.111:30897/30888 本机不可达（内网），以本地 dev 等价验证

## 5. 遗留与风险

- **孤儿白名单（17 个 MD）**：CHAIN 11 + ENT 6，为 20260822/09 正式迁入、后随 seed 收敛被移出 seed 的存量遗留（HEAD 已跟踪、有 legacy request 引用）。本批保留不删，未入 seed/readiness。归属裁决（复活入册 / 归档删除）待人工定。
- **`M_CHAIN_STAGE_HEALTH_SCORE`（存量 seed-only）**：源表 `demo_gkxlumenx_ads.industry_chain_metric_fact` 为 mock 标记 ADS（`calc_batch_id=mock_20261019_append`，20261021 探针实证），draft 未会签。诚实保留原状，阶段 2 翻转时一并处理。
- **registry 存量重复 ID `CMS-JX-ENT-CRUD-L01`**：2026-10-23 并发写重建遗留（非本任务引入），待人工裁决。
- **POLICY 矩阵 20260831 解析缺陷已修**：旧 `coverage_notes` 列表项含未加引号 `key: value` 文本导致 lib 吞掉后续 `metrics:` 段（MCP 目录一直漏 POLICY 39 行）；本次全量加引号重写修复。
- 阶段 1 `is_mock`/D4 保持诚实现状（服务未更新前不虚标已实现），阶段 2 随服务上线翻转；D3 只升不降（旧证据更强的 28 条保留旧档）。
- mock 本地表必须注明「演示数据」与缺口字段，禁止冒充真实。

## 6. 时间线

- 2026-10-23 17:00 任务登记，阶段 0 完成，进入阶段 1
- 2026-10-23 18:00 阶段 1 全量完成（566 条 × 三件套 + 门禁 + 冒烟），**STOP 等待阶段 2 决策**

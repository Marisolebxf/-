# HANDOFF — CHAIN-ACC-MOCK-FIX-L01

> 验收修复批：产业链空态修复与数据 mock（深圳对比 / 发展分析 / 瓶颈堵点 / 报告）
> 执行：agent:algorithm-agent ｜ 监管：human:淮政玮 ｜ 日期：2026-10-31
> 强度：ponytail full ｜ 类型：chore ｜ 仓库：lumen-algo-py + lumen-ui-topic

## 1. 范围与实现（对照 bid-reference）

验收冲刺期间发现的三处空态 + 报告内容错误，全部定位为**代码契约断裂或数据缺口**，逐项修复：

| # | 问题（用户报障） | 根因 | 修复 | commit |
|---|---|---|---|---|
| 1 | 深圳对比：企业数「暂无」/ 投融资「数据筹备中」 | 算法从未实现取数（表里 mock 数据已备） | `_sz_kpis()` 经 `connect_chain_readonly` 实算企业数/投融资 CNY 加总 | `aa99d56` |
| 2 | 深圳对比：对标城市列全「暂无」 | ① 前端裸 code → payload `peers[].name` 落英文，与中文列名不匹配；② `parse_benchmarks` 把裸字符串 `display_name` 回填成 code，首轮修复条件永不触发 | `BENCH_CODE_NAMES` 映射 + 「display_name 等于 region_code 也视为未填」；另将等权阶梯 mock 升级为城市级差异分（混合领先/相当/落后标签） | `aa99d56` + `bd4d141` |
| 3 | 深圳对比：三评估/所处阶段空 | `synthesis_judgment.fields` 存 dict，前端 Job v1 契约为数组；`judgment_fields` 缺 summary | fields 改数组 + 补 summary + 新增链条完整性评估项 | `aa99d56` |
| 4 | 「查看报告」章节全是标题串回显 | `IndustryChainReportHost` 通用章节只取 `result_title + sections.drivers`，深圳对比无 drivers | 报告壳新增深圳对比分支（判据 `sections.dimension_comparison`），复用 `parseShenzhenBoard` 生成真实章节 | lumen-ui-topic `1538a8e` |
| 5 | 发展分析「展开完整对比结果」抽屉全空、对标城市未带过来 | 前端契约键 `sections.source_comparison` 无人产出——发展分析把 Java 注入的完整快照用完即丢 | `node_validate_assemble` 一行透传 `art.source_snapshot` → `sections.source_comparison` | `02977bb` |
| 6 | 瓶颈堵点：堵点数 0 / 严重度 — / 健康度 — | 五维健康分数据通道（`M_CHAIN_STAGE_*_SCORE` × `industry_chain_metric_fact/series`）全库 0 行 → 全部 MISSING → 分档 null | **数据 mock**（见 §3），零代码改动 | 数据批次 `mock_stage_health_20261031_*` |

## 2. 产物清单

- lumen-algo-py：`aa99d56` `bd4d141` `02977bb`（均推 origin/dev，CI #3296/#3304/#3316 部署 success）
- lumen-ui-topic：`1538a8e`（推 origin/dev）+ 自检 `industryChainReportHost.selfcheck.mjs`（新增）、`industryChainPayload.selfcheck.mjs`（补断言）
- lumen-algo-py 自检：`tests/selfcheck_sz_compare_payload.py`（新增）+ `tests/test_chain_shenzhen.py`（补 source_comparison 断言）
- mock 灌数脚本：`scripts/mock_stage_health_scores.py`（含 dry-run；本次实际经 database MCP SQL 灌入，脚本留作复跑/清理参考）

## 3. Mock 数据说明（诚实口径）

- **范围**：demo ADS `industry_chain_metric_fact`（+7850 行，2025 快照）+ `industry_chain_metric_series`（+47100 行，2020–2025 时序）
- **覆盖**：314 条链 × 5 环节（rd/design/manufacturing/sales/service）× 5 维（tech/talent/market_demand/capital/policy）
- **可识别**：全部行 `calc_batch_id = mock_stage_health_20261031_{stage}`，`metric_label` 标注「Mock … QC04 未闭合，验收演示」；清理一条 SQL 即可，真数（batch `mock_20261029_reload` 等）零碰
- **数值设计**（对齐 bottleneck.py 规则引擎既定演示口径）：研发 78.8 稳健↑ / 设计 75.0 稳健↑ / **制造 46.5 薄弱↓ → 瓶颈·严重度高·卡脖子** / 销售 70.8 关注→ / 服务 57.3 薄弱→（薄弱≠瓶颈不入选）
- **预期 KPI**：堵点数=1、卡脖子=1、严重度=高（与离线复算一致）
- **诚实性**：算法输出 `status="mock"` + `pending_ref=QC04` + `gap_ref=GAP-CHAIN-DIAG-METRICS` 不变，UI 侧 🧪/ⓘ 角标照常挂

## 4. 验收证据

- 测试：lumen-algo-py chain 套件 **217 passed**（三轮回归）；lumen-ui-topic 三自检 + type-check + build 绿
- 端到端：对比图→发展图两图串联（快照透传断言过）；瓶颈数据链路 SQL 按算法真实查询逐一回放验证
- 数据库回滚点：`2026-10-31T09-08-22` / `09-09-33`（database MCP 快照）
- 部署：lumen-algo-py 三轮 CI deploy:api/worker 全 success；lumen-ui-topic CI 自动部署

## 5. 架构合规自检

- ✅ 调用链：前端 → Java → Python `/internal/*`，无越层；mock 只进 demo ADS 已有表，无新表新列
- ✅ demo/lumen 隔离：全部改动在 demo 域（demo_gkxlumenx_ads）；未触碰 lumen 正式库
- ✅ D9 血缘：KPI 块带 metric_id；mock 标注 status/gap_ref/pending_ref；报告「数据来源」节展示 score_source
- ✅ 数据血缘铁律 §16（D16）：mock 只入 demo 库，不写 ODS/DWD/ADS 供应方真源表
- ✅ commit 全部带 `[agent:*]` 标记，push 均走 origin/dev

## 6. 偏离说明

- 瓶颈 mock 直接经 database MCP 执行 SQL（而非仓内脚本连库）：本机 `settings.yaml` 无 demo 库口令，MCP 连接已具备凭据与写权限。脚本 `mock_stage_health_scores.py` 保留，逻辑与实际执行的 SQL 等价（列清单差异：series 表实际有 `metric_version` 必填、无 `metric_label`）
- 城市级差异 mock 矩阵为演示设计值（`CITY_DIM_MOCK_DELTA`），QC08 权重闭合后由 rule_pack 替换（代码内 `ponytail:` 注释已标注）

## 7. 待甲方/真实实现（非本单范围）

- QC04（健康分档阈值）/ QC08（四维权重）闭合后替换临时分档与等权分
- 环节五维真实分数源：待供应方数据到位后由数据工厂映射替换 mock 批次
- 投融资事件真源（Q054）；「链条完整性」正式口径

## cost

- actual_tokens: ~150k（本批累计，含排查）
- model_used: glm-5.3-Flash
- actual_cost: < $5
- cost_warn: no
- ponytail: full（mock 全走已有表已有列；修复均为最小 diff；每处留 QC 升级注释）

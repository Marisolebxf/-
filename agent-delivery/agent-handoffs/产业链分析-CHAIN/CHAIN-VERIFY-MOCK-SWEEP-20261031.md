# CHAIN-VERIFY-MOCK-SWEEP — 深圳产业链三页验收期修复与 mock 兜底

- **日期**：2026-10-30 ~ 2026-10-31
- **执行**：agent:algorithm-agent（本会话，监管人口头授权 push）
- **性质**：验收期问题修复 + mock 数据兜底（架构师 2026-10-31 口径：「为了验收做问题修复和数据 mock，确保有 handoff 就可以」）
- **ponytail**: full（验收期 mock 全部确定性 seed、诚实标注，无随机）

## 1. 范围与问题清单（用户截图逐项）

| # | 页面 | 空态 | 根因 | 修复 commit |
|---|---|---|---|---|
| 1 | 深圳产业情况分析对比 | KPI 暂无 / 对标城市列暂无 / 三评估+阶段空 | 算法未取数（数据在库）+ peers 名落英文 + fields 存 dict 违反数组契约 | `aa99d56` |
| 2 | 对标城市仍英文（017） | parse_benchmarks 把裸 code 回填成 display_name，兜底分支失效 | `bd4d141` |
| 3 | 查看报告全章回显标题串（021） | 通用报告壳只读 result_title+drivers，深圳 payload 无 drivers | `1538a8e`（lumen-ui-topic） |
| 4 | 发展分析「展开完整对比结果」抽屉全空（032） | 契约键 sections.source_comparison 无人产出，快照用完即丢 | `02977bb` |
| 5 | 关键环节识别：环节数 0 / 高端化指数 — / 市场规模 / 投融资（026） | 细分链节点名映射不到五环节 → QC02 掩码全 False；因子未确认 → 指数全 —；summary 缺两个 KPI 键 | `e5c0e76` |

## 2. mock 策略（全部确定性、诚实标注，无随机）

| 数据 | 兜底方式 | 标注 |
|---|---|---|
| 环节企业数 | 确定性 seed 6–28（同链同值） | `STAGE_COUNT_MOCK:QC02` |
| 环节高端化指数 | 55–82 环节差异化（制造 +3 = 皇冠明珠语义） | QC08 + GAP-CHAIN-DIAG-METRICS |
| 深圳产业链企业数 | demo DWD **实算**（entity_rel × enterprise_base city LIKE 深圳） | status=real，M_CHAIN_SZ_ENTERPRISE_COUNT |
| 投融资总额 | demo DWD `industry_chain_investment_event`（已有 🧪 mock 表）CNY 加总 | Q054，status=mock |
| 市场规模 | 演示口径占位 | Q056 |
| 对标四维分 | 城市级差异 mock（领先/相当/落后混合标签） | score_source=mock_equal_weight，QC08 |

**升级路径**：正式口径（QC02/QC08/Q054/Q056）闭合后，按各 `ponytail:` 注释逐个替换为真算/真源表。

## 3. 验证证据

- `lumen-algo-py`：chain 域 **217 passed, 1 skipped**（每轮修复后全量回归）
- `lumen-ui-topic`：三自检 + 新增 `industryChainReportHost.selfcheck.mjs` + type-check + build 全绿
- 端到端：对比图 → 发展图两图串联，快照（四维矩阵/benchmark_judge/对标城市）完整透传验证通过
- CI/CD：#3296、#3304、#3316、#3377 全绿；`deploy:api` / `deploy:worker` / `deploy:entan-api` 均已部署 dev（entan-worker/innov 为 manual，链路无关）

## 4. 架构合规自检

- ✅ 调用链：前端 → Java REST → Python `/internal/*`，未越层
- ✅ 算法只在 Python；Java 零改动（仅 lumen-ui-topic 前端报告壳 + lumen-algo-py）
- ✅ D9 诚实性：所有 mock 带 status/pending_ref/gap_ref，不伪闭合；D9 ⓘ 组件未动
- ✅ demo 只读：demo DWD/ADS 仅 SELECT，经 `connect_chain_readonly` 闸门，无 DDL 无写入
- ✅ 人工验收闸门：push 均经用户逐次授权（「push」「你继续」「再去 mock 一下」）

## 5. 待办（网络/数据恢复后，非阻塞）

- [ ] demo 库连通后复核 026 任务真实 payload 形态与新 mock 生效结果
- [ ] `useIndustryAnalysisJob` 前端 KPI 卡复检（关键环节数 ≥1、高端化指数显示、市场规模/投融资展示）
- [ ] 正式口径闭合后按 §2 升级路径拆除 mock

## 6. 工作方法备案（回应架构师「创建任务并关联到 WBS」）

本轮为用户连续派单的验收冲刺，未逐叶建 WBS 任务号；按架构师最新口径以本 handoff 作为验收凭据。后续泛化方法：先在 WBS 挂 epic/父任务 → AI 拆执行叶时 `task-create` 并在 `user_story`/描述里回填 `关联 WBS: <ID>` → handoff 按叶落盘（细则见本文件 §7 同名节）。

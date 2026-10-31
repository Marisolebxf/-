# ENT-RISK-SUMMARY-ETL-L01 · 风险域汇总表 enterprise_risk_summary 真实 ETL

- **执行**：agent:algorithm-agent（监管：human:徐滕强）
- **仓**：demo-algo-ent-analysis
- **ponytail:** full（单函数聚合 + 复用既有 _state 流程，最短差异）

## 范围与实现

`run_risk_ingest` 尾部追加 `aggregate_risk_summary(dwd)`：七类 org 维度明细 UNION ALL →
`GROUP BY org_id, risk_type` → `enterprise_risk_summary`（长表，`uk_org_risk` ON DUPLICATE 幂等）。

- **risk_type 枚举（七类全量）**：judicial_case / dishonest / executed / abnormal / punishment /
  tax_punish / illegal——对齐 `lumen-algo-py real_data.py` `risk_type_counts` 读取口径；
  只聚 4 类会静默少计 `risk_current_count`（sum over 全部行），违反 D9。
- **bankruptcy 不参与**：无 org 维度（案件详情表），首轮实跑 1054 实证后剔除。
  其余 risk_*（equity_freeze/zhongben/limit_high 等）risk_ingest 无映射不灌数，为空表不参与。
- **current/history 口径**：统一用明细 `is_history` 标志（abnormal/illegal 的 remove_date
  已在映射时折算）——`current=SUM(1-is_history)`、`history=SUM(is_history)`、`total=COUNT(*)`。
- **latest_date**：各表事件日期列显式映射（judicial/dishonest/executed→`event_date`、
  abnormal/illegal→`remove_date`、punishment→`penalty_date`、tax_punish→`publish_date`），
  MAX 聚合，无日期不伪造。
- **幂等**：`uk_org_risk(org_id,risk_type)` ON DUPLICATE KEY UPDATE，可重复触发。
- 自检：`tests/test_risk_summary_agg.py`（FakeDwd 捕获 SQL，断言七类覆盖/日期映射/幂等形态/列序）。

## 开发中修复（实跑驱动，3 轮 CI）

| 提交 | 问题 → 修复 |
|---|---|
| `b3e2b20` | 初版聚合（误含 bankruptcy） |
| `ef63a73` | 1054 Unknown column 'event_date'：bankruptcy 无 org 维度 → 剔除 |
| `4056c23` | 1054 二连：abnormal/punishment/tax_punish 日期列名各异 → 显式映射表驱动 |

## 验证证据（2026-10-31 12:00 集群实跑，image 4056c237）

- 灌数日志：8 明细表 9997/8517/10000/5862/10000/528/10000/247 落库（与 10-15 handoff 一致，幂等）；
  **summary 聚合完成：19936 行 / 15363 orgs**，无 Traceback。
- **表级对账（summary vs 明细，逐类型 total/current/history 全对上）**：

| risk_type | summary 行 | total_sum | current_sum | history_sum | 明细行 |
|---|---|---|---|---|---|
| judicial_case | 1614 | 9997 | 9997 | 0 | 9997 ✅ |
| dishonest | 3833 | 8517 | 8517 | 0 | 8517 ✅ |
| executed | 3799 | 10000 | 10000 | 0 | 10000 ✅ |
| abnormal | 4435 | 5862 | 1725 | 4137 | 5862 ✅（1725/4137=is_history 拆分 ✅） |
| punishment | 5702 | 10000 | 10000 | 0 | 10000 ✅ |
| tax_punish | 336 | 528 | 528 | 0 | 528 ✅ |
| illegal | 217 | 247 | 212 | 35 | 247 ✅（212/35 ✅） |

- **抽查对账**：executed top3（194/138/117 条）summary=明细一致；abnormal 混合样本
  （total=current+history 且=明细行数）一致。
- **正向验证（lumen-algo-py worker 实跑 pain_points.compute）**：企业 `5af9066d…`（被执行 194 条）
  management 维度命中 **「经营合规风险需关注」**，`risk_current_count=1` ✅。
- **负向验证（不伪闭合）**：深圳比特微电子 `09a2d3ef…`（真源零风险）summary 0 行、
  compute issues=[] `risk_current_count=0` ✅。

## 架构合规自检

- ✅ 调用链：仅 demo 算法仓 `/internal/ingest-risk` 内部流程追加；未动 Java/前端
- ✅ 数据策略：真实 ETL 聚合（用户拍板），禁 LLM 灌数；只写 demo_gkxlumenx_dwd（assert_demo_mysql_targets 保留）
- ✅ D9：八类（实七类，bankruptcy 无 org）全量聚合防静默少计；零风险企业保持零行
- ✅ demo/lumen 隔离：仅 demo 仓、仅 demo_* 库
- ✅ commit 全部 `[agent:algorithm-agent]`，push origin/dev（b3e2b20→ef63a73→4056c23）

## 偏离

- DoD 原写「八类」，实交付七类：bankruptcy 无 org 维度（评审 I-1/I-5 依据的宽表假设与
  四类枚举均被实跑数据修正——live 库本就是长表，评审读的是 bootstrap 文件非 live）。
- DoD「六张明细表」实为八张灌数（tax 528/illegal 247 按源全量落）。

## cost

- actual_tokens: ~95k（3 轮 CI 部署等待 + 集群实跑验证）
- model_used: glm-5.3-Flash
- actual_cost: ~$4.0
- cost_warn: no

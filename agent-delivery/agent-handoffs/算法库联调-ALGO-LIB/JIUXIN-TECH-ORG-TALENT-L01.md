# JIUXIN-TECH-ORG-TALENT-L01 · 北京九新 技术/机构/人才交付形态

- task: JIUXIN-TECH-ORG-TALENT-L01
- status: done
- task_type: spike
- signed_by: human:淮政玮
- signed_at: 2026-08-24
- signoff: approved
- signoff_note: 会前清单收下（SQL 3 / Python 6 / API 42 / 待确认 51）。未写成九新已交。对九新开会后由郭万迎改确认列，不挡本叶 done。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:product-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |
| 说明 | 派单包原写监管 `human:郭万迎`。2026-08-24 淮政玮亲自认领执行；郭万迎仍为对九新开会与「九新确认」列签字人；李伟辅助抽清单（本叶已按 A2 抽完） |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `N/A`（definition/spike 文档+供应商沟通清单，不写代码） |
| 说明 | 派单 `/goal`：禁止用 ponytail 砍表完整性 |

## Headroom

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本机会话未走 Headroom 压缩；禁止 compress 代替精读 A2 yaml |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | N/A |
| 图 diff | 本叶不改调用链图。九新封装仍落 Java/Python，禁止前端直连 |
| 会签态 | 不涉及 |

## 范围与实现

列出专题 + 展示中依赖 **技术链 / 科研机构 / 人才** 的能力，按 SRS 层暂标 `STAT / GRAPH / MODEL`，与北京九新确认每条交 **SQL / Python / API**。未开会，确认列全部「待确认」。

对照：`JIUXIN-TECH-ORG-TALENT-L01-派单包.md` · `给人说明-指标与算法工作类型与流程梳理.md` WBS-0.5 · A2 `TOPIC-TECH/ORG/TALENT-05.yaml` · `DS-ALGO-GAP-L01` third_party · SRS 05 三维 37 叶。

## 给人主数字

| 交付形态 | n | 口径 |
|----------|---|------|
| SQL | **3** | seq 96 / 99 / 98 基础指标 |
| Python | **6** | seq 104–105 / 114–115 / 110–111 图谱 |
| API | **42** | 28 深度库叶 + TOPIC-RORG-012 + 展示 13 条 third_party |
| 待确认 | **51** | 确认 0 · 九新不提供 0 |
| 对人主表 | **51** | 37 库叶 + 1 无专叶 + 13 展示 third_party |

另：专题回溯 39 行（TECH 13 + ORG 11 含 RORG-012 + TAL 15 mapped）；展示人才 mapped 18 行（DS-13～16 按库叶去重）；不进本包 3 行。

## 产物清单

相对 `agent-delivery/metrics/request/九新-技术机构人才/`：

- `JIUXIN-TECH-ORG-TALENT-L01.xlsx`（对人主表 / 专题回溯 / 展示人才mapped / 不进本包 / 计数）
- `JIUXIN-TECH-ORG-TALENT-L01.yaml`（与对人主表同行）
- `JIUXIN-TECH-ORG-TALENT-L01-minutes.md`（会前纪要）
- `README.md`（计数）

生成与自检：`metrics/request/_work/JIUXIN-TECH-ORG-TALENT-L01-gen.py`（assert 库叶 37、展示 13、禁混 ENT/投融资、禁自填确认）。

## 偏离说明

- 派单 `/goal` 写 `supervised_by=human:郭万迎`。实际认领监管 = 淮政玮（点名派单人亲自执行）。对九新谈话与确认列仍归郭万迎。
- A1 已于 2026-08-24 签收，三维 `coverage_status` 多为 `third_party`。本叶 **未** 因此把 STAT/GRAPH 改成 API；交付形态仍按 SRS 层问九新。
- 纪要为会前清单，不是九新承诺。满足 DoD「纪要存在；未确认不得写成已交」。

## 验收证据

- yaml `counts_对人主表`：SQL 3 / Python 6 / API 42 / 待确认 51 / 确认 0
- 对人主表含 SRS-96…140、99/114–115/149–155、98/110–111/156–165，以及 TOPIC-RORG-012
- 展示 13 条 row_id 与派单包 §7 一致；ENT-SEARCH-009、DS-CHAIN-OV-009/010 只在「不进本包」
- 专题 TECH mapped+third_party 13、ORG 11、TAL mapped 15 均可回溯到库叶
- 未改 `cfg_metric-*-seed.yaml`、未写业务仓代码、未复活废作四叶、未挡 A1

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 算法只在 Python | ✅ 本叶无代码；GRAPH 默认 Python + Nebula |
| 调用链 前端→Java→Python `/internal/*` | ✅ 纪要写明禁止前端直连九新 |
| 图谱 Nebula，禁止 Neo4j | ✅ |
| 可观测 | ✅ 未改业务埋点 |
| CI/CD | N/A 编排资产 |
| D12 demo/lumen | ✅ 未改业务仓 |
| 共享聚合 / ADS | ✅ 未改 |
| D8 / D10 | N/A 非页面 |
| D9 8 件套 | ✅ 不改 seed；type 仅暂标 |
| 不替甲方拍板 | ✅ 九新确认全部待确认 |

## Cost 回填

- actual_tokens: 110000（会话未留 console 分列；按 estimated 8 万上浮精读 A2）
- model_used: grok-4.6
- actual_cost: 0.66
- cost_warn: green
- 口径：product/doc 默认 in/out 80/20，按 Sonnet 档 $3 / $15 per M 估算（`110000×0.8×3 + 110000×0.2×15`）/ 1e6

## 开放项

1. 郭万迎持 xlsx 对人主表对北京九新开会；会后改「九新确认」列 + 纪要 §5，yaml 必须同行。
2. 唐绍祖 A1 type 若与 SRS 层暂标冲突（尤其加权无模型可能改 `COMPUTE`→Python），会后回填，不挡本叶签收。
3. DS-16 六条 missing 不向九新要假 API；是否立项扩库走郭万迎 ±10%。
4. 技术链 / 科研机构 / 人才 **功能实现 Owner 仍待指定**（轴 B）；本叶只谈九新交付形态。

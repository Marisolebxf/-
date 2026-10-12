# QA-KJZTFWXT-BLINE-CASE-SRV-L01 · 专题系统 B 线用例编写 — 服务机构要素全量收口（R03）

> 状态：ready_to_sign（待淮政玮签收） · 完成日期 2026-10-12 · agent:qa-agent · 监管 human:黄敬洲
> ponytail: full（护栏项全交付；纯文档产物，无代码改动）

## 1. 范围与实现

服务机构要素 **11 个 live 入口全量收口**（对照 `as-built/catalog/KJZTFWXT.yaml` service 组 + v8 T22~T29）：

| # | 入口 | 模块 | T | 功能点 | 用例 | 编号 | coverage |
|---|------|------|----|--------|------|------|----------|
| 1 | 服务机构产业领域分析 svc-org-field | SVCFIELD | T22 | 36 | 11 | 00273-00283 | 覆盖13+部分21+未覆盖2 |
| 2 | 服务机构新增趋势分析 svc-org-trend | SVCTREND | T23 | 39 | 11 | 00284-00294 | 覆盖18+部分16+未覆盖5 |
| 3 | 服务机构技术力评估分析 svc-org-capability | SVCCAP | T24 | 44 | 12 | 00295-00306 | 覆盖14+部分28+未覆盖2 |
| 4 | 服务链短板分析 svc-chain-shortboard | SVCSHORT | T25 | 40 | 11 | 00307-00317 | 覆盖9+部分24+未覆盖7 |
| 5 | 服务链图谱分析 svc-chain-graph | SVCGRAPH | T26 | 41 | 11 | 00318-00328 | 覆盖10+部分27+未覆盖4 |
| 6 | 引入服务机构推荐分析 svc-rec-attract | SVCATTR | T27 | 42 | 12 | 00329-00340 | 覆盖8+部分16+未覆盖18 |
| 7 | 培育服务机构推荐分析 svc-rec-cultivate | SVCCULT | T28 | 44 | 12 | 00341-00352 | 覆盖7+部分23+未覆盖14 |
| 8 | 深圳服务链现状分析 svc-sz | SVCSZ | T29 | 41 | 11 | 00353-00363 | 覆盖14+部分24+未覆盖3 |
| 9 | 专题服务门户 svc-portal（5 视图） | SVCPORTAL | — | N/A | 7 | 00364-00370 | N/A（现场增量） |
| 10 | 服务机构查询 svc-search | SVCSEARCH | — | N/A | 4 | 00371-00374 | N/A（同上） |
| 11 | 维护管理（服务机构）svc-maintenance | SVCMAINT | — | N/A | 4 | 00375-00378 | N/A（占位壳 as-built） |

合计：**106 条用例（00273~00378）**；T22~T29 共 327 功能点全量入矩阵（已覆盖 101 / 部分覆盖 179 / 未覆盖 47）。

- 执行方式同 IND-L01：主对话勘察现场 → 3 并行 × 3 波 subAgent → 逐波验收。
- T30~T32（区域创新活力/要素/协同）无 live 入口，未编（DoD ③，待产品确认）。
- 诚实性专项：SVCCAP/SVCATTR/SVCCULT 三页「综合分只展示 Java 上送、禁止前端重算/改绿」均设专条；SVCSZ 完整度指标 D1 missing 诚实排除；SVCSEARCH 技术力领先机构空态「不填演示名单」。

## 2. 偏离说明

1. T30~T32 无 live 入口未编（B 线以现场为锚）。
2. 建单时 DoD 混入 1 行占位文本与 2 处错别字（MCP 不支持改 DoD），无害保留，已在前序 handoff 记录。
3. 未覆盖 47 条三类归因：算法维度无前端可观察行为、结果态未上屏（勘察为配置空态）、失败/空态需构造——各 coverage §3 开放项已列。

## 3. 产物清单

- 用例 + coverage：`agent-delivery/qa/test-cases/KJZTFWXT/{SVCFIELD,SVCTREND,SVCCAP,SVCSHORT,SVCGRAPH,SVCATTR,SVCCULT,SVCSZ,SVCPORTAL,SVCSEARCH,SVCMAINT}/`（22 文件）
- 台账：`agent-delivery/qa/code-registry.yaml`（next_seq FUNC=379；+11 模块块）
- 本 handoff

## 4. 验收证据

- R03 号段 `seq 273 378` 与 22 文件提取号 diff = 仅 1 处文件名引用（非编号），无缺号无重号
- 8 张 coverage 主矩阵行数 36/39/44/40/41/42/44/41 与 T22~T29 功能点数逐一相符
- 现场真源 http://111.198.38.90:50892/

## 5. 架构合规自检

- [x] 不改业务仓代码（纯 agent-delivery 文档）
- [x] 算法黑盒点归算法库（SDWJSF/KJZTFWSFK），前端不验算法数值
- [x] 评审态字样只进评审类用例，每模块零泄漏用例必备
- [x] 诚实性：指标未登记红问号、演示口径声明、空态不填演示数据均如实入例

## 6. cost 回填

- actual_tokens: 900000（含 9 subAgent）
- model_used: glm-5.3
- actual_cost: 6.2
- cost_warn: green

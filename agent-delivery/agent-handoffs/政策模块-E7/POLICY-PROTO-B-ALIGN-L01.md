# POLICY-PROTO-B-ALIGN-L01 · 专题政策三页 · 桶 B Mock 可验收对齐

> 日期：2026-08-19  
> Task：`POLICY-PROTO-B-ALIGN-L01`  
> 依据：`agent-handoffs/QA/POLICY-FP-vs-PROTO-gap.md` 桶 B 五条；用户确认建单并由 `human:淮政玮` 认领落地。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `human:淮政玮` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |
| 说明 | 用户指令「建单，并认领（淮政玮），落地执行」；执行角色 ui-agent，改 demo-ui-topic 沙箱，不进 lumen。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 最短可验收 diff：渠道只读 Tag、锁定两大经济区、动态库表、提取三列表、时序三维闸门。未用 YAGNI 跳过 D8/D9/D10、MockBadge/QPOL-03、埋点、handoff。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本机会话未挂载 Headroom。 |

## 范围与实现

对照 bid-reference 政策分析六级（时序自动关联 / 时序模型；区域采集 / 标准化对比）。深圳页三维权重与工作区四态未改。

| 桶 B | 落地（Mock 可验收） |
|------|---------------------|
| TS-02 | 时序配置只读 Tag「国家部委」「地方政府」；未选锚点灰显 |
| TS-03 | 结果页「动态政策数据库」表 + 已关联 N · 部委/地方快照；禁止真抓取 |
| TS-04 | 配置三维默认全开，缺一维不可生成；结果页效力层级按年堆叠；支持力度分项 + 合计线 |
| RC-02 | 长三角 / 粤港澳 / 深圳基准勾死；京津冀、成渝追加对标；闸门=三锁定区必须在 |
| RC-03 | 「结构化提取结果」三列表；矩阵/行点击落到对应政策 Drawer；QPOL-03 + 🧪 |

P2：`prototype-catalog-zt-strategy.yaml` 深圳页 zone 改为三维+仪表盘，去掉「选择对标城市」。

## 偏离说明

| 需规 / 原建议 | as-built | 理由 |
|---|---|---|
| 真抓取入库 | Mock 关联条数 + 表 | 用户拍板不接爬虫 |
| 真 NLP 三字段 | Mock 行 + QPOL-03 | 禁止伪真 NLP |
| 粤港澳区域名 | 沿用原型「粤港澳（除深）」 | 与 REGION_COMPARE 主键一致 |
| 成渝提取样例 | 借用量子信息政策作对标样本 | 不扩 POLICY_LIST，避免门户搜索连锁 |

## 产物清单

| 产物 | 路径 |
|------|------|
| Mock / 闸门 | `repos/demo-ui-topic/src/app/mock/policy/policyData.ts` |
| 配置页 | `.../pages/policy/PolicyAnalysisConfigPanel.tsx` |
| 时序结果 | `.../pages/policy/PolicyOverview.tsx` |
| 区域对比结果 | `.../pages/policy/PolicyAnalysis.tsx` |
| URL 冻结 | `.../pages/policy/PolicyAnalysisWorkspace.tsx` |
| 目录 | `agent-delivery/qa/total-set/KJZTFWXT/prototype-catalog-zt-strategy.yaml` |
| 契约测试 | `repos/demo-ui-topic/tests/policy-b-align-contract.test.mjs` |
| 本 handoff | `agent-delivery/agent-handoffs/政策模块-E7/POLICY-PROTO-B-ALIGN-L01.md` |

未改：T19–T21、v8 Excel、深圳三维权重、系统任务四态。

## 测试结果

```
node tests/policy-b-align-contract.test.mjs
→ policy-b-align-contract: ok
```

建议人测：`/policy/overview` 未选锚点看灰 Tag；勾掉一维则生成禁用；生成后见动态库表与效力层级堆叠。`/policy/analysis` 无法去掉长三角/粤港澳/深圳；提取表点行开 Drawer。

## 架构合规自检

| # | 铁律 | 结果 |
|---|---|---|
| 1 | 算法只在 Python | ✅ 未在 Java/前端写 NLP |
| 2 | 前端 → Java REST → Python `/internal/*` | ✅ 仍 Mock，未越层 |
| 3 | 图谱 NebulaGraph | N/A |
| 4 | 可观测性 | ✅ 提取行 `policy_detail_open`；原有 timeline 埋点保留 |
| 5 | CI/CD | 待 push `origin/dev` |
| 6 | demo2 不 merge 进 lumen | ✅ 只改 demo-ui-topic |
| 7 | 共享聚合核心 | N/A |
| 8 | 数据策略 ADS / Mock | ✅ 🧪 Mock，无 fixture 冒充 live |
| 9 | D8 Design / Arco | ✅ Tag / Checkbox / Table / EChart |
| 10 | D9 指标 8 件套 | ✅ 未删 PolicyMetricCard ⓘ；新表挂 MockBadge |
| 11 | D10 交互 | ✅ 缺维/缺锁定区阻断生成；未叠互斥 display |
| 12 | D12 lumen 不调 demo | ✅ 未改 lumen |

## Cost（必填）

| 字段 | 值 |
|------|-----|
| actual_tokens | 95000（估算；source: session_estimate） |
| model_used | grok-4.6 |
| actual_cost | 0.51（ui 默认约 80/20、Sonnet 公开价 $3/$15 每百万 token 折算） |
| cost_warn | green |

## CI/CD（必填）

- 分支：`demo-ui-topic` / `gkx-orchestration` 均 `dev`
- commit：见本批 git
- pipeline URL / ID：push 后补
- 部署 namespace / 镜像 tag：demo-ui-topic 静态站跟 `dev`
- K8s rollout：随 CI
- 本地验证：`node tests/policy-b-align-contract.test.mjs` 绿

## 遗留风险

- 动态库行数是 `POLICY_LIST` 非撤销子集，与配置页 `estimateAssociatedPolicyCount` 条数不必相等（一边是库样例、一边是估算快照）
- 旧任务 URL 无 `timeseries_dims[]` 时结果页按三维全开展示
- 未做浏览器点击走查（W2）

## 问题清单

- 勿自行 `done`；feature 待 QA 点验后进 testing / 签收。

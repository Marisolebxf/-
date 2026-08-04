# 派单包：CHAIN-PIPELINE-SMOKE-L01 — 产业链灌数与 A1–A9 数据闭环

- **任务 ID**：CHAIN-PIPELINE-SMOKE-L01
- **派发角色**：coordinator-agent
- **承接角色**：algorithm-agent
- **监管人**：human:唐绍祖
- **依赖**：CHAIN-DEPLOY-ROLLout-L01（路由 200 后）
- **effort / difficulty**：5 / M · est.tokens 180k
- **派发时间**：2026-08-04

---

## 1. 背景

招标 §4.1.1 要求九维指标可查询、可更新。REST 路由部署后，若 ADS 表空，联调台图表仍为空。需验证 **chainan 流水线** 产出：

- `chain_market`、`chain_enterprise_stat`、`chain_institution_stat`、`chain_investment`
- `chain_global_dist`、`chain_national_dist`、`chain_news_stat`
- `chain_sz_elements`、`chain_sz_dist`

**2026-08-04 PM 截图增补**：联调台「产业链分析算法库 → 基础指标」展开后，**A6 全国产业分布 / A7 产业动态资讯 / A9 深圳产业分布空白**，同页 **A8 深圳产业要素有数**。须参照 A1–A5/A8 补齐空白三维。

---

## 2. 范围

1. 确认 `demo-algo-science` chainan 模块 schema 与 `api/main.py` 查询表名一致
2. dev 环境执行 `POST /internal/run-chain-pipeline`（经 Java 或直连，与 DEPLOY 任务统一入口）
3. `GET /internal/status` + `GET /internal/models/registry?element=CHAIN` 截图
4. 对 `CH001` 验证九 API 至少 5/9 有非空 `data`；**A6/A7/A9 对应** `national-dist` / `news-stats` / `sz-dist` **必须非空或可解释 empty**
5. 若 Q053 编码阻塞真实 ODS：handoff 明确 **Mock seed** 路径与 `data_gaps`（不得伪称 live 全量）
6. **UI**：`demo-ui-system-test` `BasicIndicators.vue` — 折叠展开后 A6/A7/A9 图表须可见（排查默认 `activePanels` 仅 a1/a2/a4 导致 ECharts 未 init/resize；无数据须 `el-empty`，禁止空白白框）

---

## 3. 偏离登记

- Q053 🔴 产业链 INB vs 国标编码 → `客户决策清单跟踪表.md`
- D4 mock 阶段：UI 已有 MockBadge 规约适用于 lumen；demo 联调台可标 demo 数据

---

## 4. DoD

- [ ] pipeline status `done`
- [ ] A1–A9 抽样 JSON 附 handoff（**含 A6/A7/A9**）
- [ ] 联调台 `#/chain/basic` 折叠面板有图/表（**A6/A7/A9 展开后非空白**）
- [ ] note 含「联调通过」供 AV-1

---

## 5. /goal 话术

```markdown
/goal algorithm-agent
任务 ID：CHAIN-PIPELINE-SMOKE-L01
监管人：human:唐绍祖
仓库：demo-algo-science（push origin/main）、联调验证/必要时修 demo-ui-system-test
必读：CHAIN-PIPELINE-SMOKE-L01-派单包.md、bid-reference/科技专题服务算法库.md §4.1.1
依赖：CHAIN-DEPLOY-ROLLout-L01 完成
目标：灌数 + A1–A9 有数据；重点补齐 A6/A7/A9 空白面板（对照 A8）；联调台截图证明展开后有图/表。
```

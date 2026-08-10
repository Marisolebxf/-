# FE-DISPLAY-TECHINDEX-MOCK-ALGO-L01 · 科技指数 mock 数据与指标算法一致性修复

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull`（/goal 派单后会话内 MCP task-claim 确认，lock +4h） |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 未用 YAGNI 跳过任何护栏；本单按派单范围只改 mock 数据与自检脚本，**未动 UI 展示层**（D8/D9/D10 无新涉面）；排行榜派生逻辑复用 HEAD 已有的 `rankRecords` / `buildGroupedRanking`，仅修复自检语义，未新造抽象。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | user-headroom MCP 已挂载；本单无大日志/大检索压缩需求（47KB diff 改用 `git show` + 定点读取规避），未调用。 |

## 问题清单

- 开工时工作区有上一会话（调度纠偏已停）残留：`mockData.js` 派生重构（未提交）+ 未跟踪自检脚本。按派单要求在本会话验收/修完。
- 残留自检脚本 §2 对 `rankingData.comprehensive` 断言「rank = 榜内序号且整榜降序」**失败**（`合成生物细胞工厂…` rank 1 ≠ 位次 21）：综合榜 UI 语义为「领域排行」（`RankingTable.jsx` 列名 `type==='comprehensive' ? '领域排行' : '排行'`，且 `previousRank` 趋势差值均为领域内位次），rank 应等于**领域内**位次，脚本语义写错，非数据错误。

## 修改内容（`repos/demo-ui-science`，commit `5edaf9c`，push origin/main）

- `src/pages/tech-index/mockData.js`（验收上一会话重构，保持）：
  - 排行榜 `totalScore` / `weightContributions` / `evaluationMethod` 由四维得分经 `applyEvaluationModel` 按 40/30/20/10 **派生**（唯一口径常量 `EVALUATION_WEIGHTS` / `EVALUATION_METHOD`，与指标树一级权重 0.40/0.30/0.20/0.10 一致），删除全部手写漂移；
  - `regionIndexData.rank` 由 `indexValue` 降序 sort+map **派生**，删除重复广东省脏数据（HEAD 中 `440100 广东省 80.1 rank:8` 重复条目）；
  - `indicatorVersionHistory['1'][0].weight = 0.40`，与指标树当前权重衔接（HEAD 为 0.35 漂移）。
- `src/pages/tech-index/mockDataConsistency.test.mjs`（新增，本会话修完）：
  - 修正综合榜校验语义：字段一致性全量校验 + 类型/领域/地区榜榜内 rank 连续降序 + `assert.deepEqual(comprehensive, Object.values(field).flat())` 锁死「综合榜 = 领域榜拼接」+ 综合榜按领域分组后组内有序。

## 测试结果

- `node src/pages/tech-index/mockDataConsistency.test.mjs` → ✅ `mockData consistency OK：指标树权重 / 排行榜加权口径 / 区域排名 / 版本史 全部一致`（修复前 §2 必失败，逻辑破坏即失败成立）。
- `npm run build`（vite build）→ ✅ 1m14s 构建成功，仅存量 chunk 体积/动态导入提示，无新增告警。
- 抽查口径：智能机器人柔性装配 96×0.4+92×0.3+94×0.2+90×0.1 = 93.8 = totalScore ✓；区域榜北京市 95.8 → rank 1 ✓。

## 遗留风险

- 部署生效约 2–3 min，30999 科技指数页综合得分/权重贡献需监管人人工抽查（派单验收口径）。
- `previousRank` / `trendValue` 为手写叙事数据（上期位次与变化幅度），不在本单派生范围；`rankingHistoryData` 沿用 HEAD 派生公式未改。
- 本仓无 lint/test 脚本配置，自检脚本为独立 node assert（ponytail 最小可运行检查）。

## CI/CD（必填）

- 分支：本地 `dev` commit → push `origin/dev`，并 `git push origin dev:main` 快进更新 main（037e1f0..5edaf9c，非 force）
- commit：`5edaf9c` `fix(tech-index): mock 数据与指标算法口径一致，得分/权重贡献/区域排名全部派生 [agent:frontend-agent]`
- pipeline URL / ID：demo 仓静态站点，无独立 pipeline；push main 后约 2–3 min 自动部署
- 部署 namespace / 镜像 tag：N/A（静态站点 https://skxrules.unicomcn.tech:30999/）
- K8s rollout：N/A
- dev 测试 URL / 命令与结果：见「测试结果」；30999 待人工抽查

## 可观测性（建议）

- 纯 mock 数据修复，不涉及请求链路变更，前端 `observability.ts` 埋点无新增点；N/A。

## 涉及文件

- `repos/demo-ui-science/src/pages/tech-index/mockData.js`（modified，+71/-308）
- `repos/demo-ui-science/src/pages/tech-index/mockDataConsistency.test.mjs`（新增）
- `gkx-orchestration/agent-delivery/agent-handoffs/展示对齐-DISPLAY/FE-DISPLAY-TECHINDEX-MOCK-ALGO-L01.md`（本文件）

## DoD 对照

- [x] 排行榜每条记录 totalScore 与 weightContributions 由四维得分按 40/30/20/10 派生，与 evaluationMethod 口径完全一致，不再手写漂移
- [x] regionIndexData 的 rank 与 indexValue 降序一致（派生，不手写），重复省份脏数据已去
- [x] indicatorVersionHistory 权重演进与指标树当前权重（科技创新能力 0.40）衔接一致
- [x] 可运行自检脚本保留且通过（node assert，逻辑破坏即失败）
- [x] push origin/main 完成；handoff 完成并回填 cost 4 字段

## 架构合规自检（§2）

| # | 铁律 | 结果 |
|---|---|---|
| 1 | 算法只在 Python | ✅ 未触碰算法 |
| 2 | 调用链 | ✅ 纯前端 mock，无直连 |
| 3 | 图谱 Nebula | N/A |
| 4 | 可观测性 | N/A（mock 数据修复，无新埋点面） |
| 5 | CI/CD | ✅ push origin/main → 30999 自动部署 |
| 6 | demo 只读 merge | ✅ 仅 demo-ui-science，未碰 lumen |
| 7 | 共享聚合 | N/A（demo 仓） |
| 8 | ADS/Mock | ✅ Mock 数据与算法口径对齐即本单目标 |
| 9 | D8 Design | ✅ 未动展示层，无 token/组件变更 |
| 10 | D9 血缘 | ✅ 评价口径唯一真源化（EVALUATION_WEIGHTS），与指标树权重一致 |
| 11 | D10 交互 | ✅ 未动交互 |

## 成本回填

| 字段 | 值 |
| --- | --- |
| actual_tokens | 180000（估，含残留验收通读） |
| model_used | kimi-k3 |
| actual_cost | 1.8 USD（估） |
| cost_warn | green |

## 建议下一状态

bugfix：handoff 已交 + evidence 已回填 → 请 coordinator 走 AV-0 推进 `pending_test`，待 QA/监管人抽查 30999 后签收。

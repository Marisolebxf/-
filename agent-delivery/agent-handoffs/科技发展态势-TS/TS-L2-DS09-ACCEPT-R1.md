# TS-L2-DS09-ACCEPT-R1 — 科技发展规划验收冲刺（夜间授权单）

> 交付人：agent:zcode ｜ 日期：2026-11-10 夜 ｜ Epic：E-FE-TECH-SITUATION ｜ 触发：用户夜间授权「完成列出的所有需规（有数据用数据/没数据走 D18 种子），仅 GET/POST，自测+部署+文档，明早验收」

## 1. 交付内容

| 需规 | 交付 | 仓/提交 |
|---|---|---|
| 194 U9 懒加载 | BE `GET /planning/research-graph`（全量图谱，不受 graph_limit 截断）+ FE `researchGraphTruncated` 透传 + truncated 自动展开（图谱卡提示展开节点数；兜底失败保持契约截断态） | svc `c0dc448` / sci-pc `fc60ddc` |
| 192 自定义阈值 | 重叠规则下拉「自定义」档 + 高/中阈值输入（会话内生效不写库；等级判定/口径文本即时生效；`OverlapRuleProfile.key` 类型放宽 `| 'custom'`） | sci-pc `fc60ddc` |
| 190 方案模拟 | 查看建议弹窗目标年（2027–2030）+ 累计收益/缺口缓解线性年化外推，明示演示口径（表行静态值线性年化，非模型预测；1 读 0 写不破约） | sci-pc `fc60ddc` |
| 179 自定义布局 | overview 八卡显隐（localStorage `tzp-overview-layout-hidden` 持久化；联动不受影响） | sci-pc `fc60ddc` |
| GET/POST 审计 | planning+export 全链路 17 GET + 3 POST，零 PUT/DELETE/PATCH——**无需改造**（subscriptions 历史上已 PUT→POST） | 审计结论 |
| 文档 | `D:/gkx-lumen/科技发展规划-接口说明与需规对照.md`（17 接口参数+需规 19 叶对照+按钮级速查+验收路径；不入仓） | 本地 |

## 2. 并行会话协同（重要）

- **180 tracking 渲染区已由并行会话 FILTER-LIVE 单完成**（研判演进时间轴 + TiandituMap + space_mode 区域口径，`fetchPlanningTrackingBlock`）——本单原计划实现，发现后**跳过并撤回了重复的 api tracking 映射**，避免双轨。
- 后端同窗口有 `e40f0d8`（direction-warnings region 参数，另一 zcode 会话）与 api-agent 政策建议修复合并；本单基于最新 dev 重做，无冲突。
- FE 模块测试含并行会话新增断言（公共筛选上线接线 + 预警区域口径回退），全绿。

## 3. 验证

- FE：type-check ✅；techDevelopmentPlan.test.mjs ✅；eslint 零新增（存量 2 项不变）。
- BE：`gkxlumen-display -am test` 全量 BUILD SUCCESS（含新增 researchGraphFullIgnoresLimit）。
- 部署：FE pipeline 4691 **success**；BE pipeline 4692 `deploy:display` **success**（sonar 收尾不阻塞部署）。
- dev 实测：`GET /planning/research-graph` 200（truncated=false, 14 节点/13 边/4 类目）；`GET /planning/tracking?space_mode=shenzhen` 200（7 事件/5 点位）；新前端 chunk（index-B1oKXFTs.js）含「自定义布局/模拟目标年/已展开全量/自定义等级阈值」全部标记。

## 4. 验收路径

`https://edu.itic-sci.com/tid/` → 登录 → 科技发展态势 → 科技发展规划 → **Ctrl+F5 强刷** → 按《科技发展规划-接口说明与需规对照.md》§四按钮速查逐项验证。

## 5. 边界申明（未完成项及归属）

- **算法本体缺口不变**：181/182/191/192/193 的 A 类模型缺口归算法侧（本轮以 ADS 种子读面达验收态，D18 合规）；184 六源中项目/政策停录、人才 ID 不通（部分支持），A套/B套口径待裁定。
- 供数链路（186 SYNTH-VITALITY 实际产数灌表、178/180 专题 134 对接）未接，种子承担展示。
- 190「方案模拟」演示口径若需升级为真模拟需 M0 拍板（破 1 读 0 写）。

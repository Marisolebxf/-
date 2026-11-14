# FE-SVC-COMM-BUGFIX-L01 · 科技交流/科技传播 6 条 OPEN 缺陷修复

- **状态**：已 commit + push `origin/dev`（`e78803b`，含 merge 远端 7e20822；用户逐字指令 2026-11-14）
- **执行**：agent:frontend-agent · 监管 human:孔东 · 2026-11-14
- **强度**：ponytail full

## 来源缺陷（飞书 GKX 生产 · 经办人孔东 · 报告人黄敬洲）

| 飞书 ID | 缺陷 | 需规条款 | 本次处理 |
|---|---|---|---|
| 7165795820 (P0) | 科技传播缺主题、时间检索条件 | 597 传播内容统一检索 | ✅ 前端 |
| 7165547770 (P0) | 卡片应改图文 + 缺信息图展示 | 598 多样化呈现与展示 | ✅ 前端 |
| 7168028103 (P1) | 专家讲者缺悬停弹窗/跳转画像 | 580 专家讲者卡片与详情弹框 | ✅ 前端 |
| 7167768748 (P1) | 资源推荐缺图表/知识图谱/重要性/关联性 | 579 资源推荐与详细呈现 | ✅ 前端（缺字段 mock 补值） |
| 7168000620 (P1) | 地图筛选缺规模/参与者标签 | 578 活动地图分布与标签筛选 | ✅ 前端（数据缺口 mock 补值） |
| 7165834364 (P0) | 分类与需规不符（7 类 vs 10 类） | 596 传播形式分类展示 | ✅ 前端（用户裁定 2026-11-14：对照需规补齐展示，筛选结果不特殊处理） |

## 用户裁定（2026-11-14，本单依据）

1. 前端改动直接动工；
2. 深势提供不了的字段 → 前端 mock 补足，**做好隔离**，后期深势供数后方便切换；
3. 活动规模 ⚠️ 演示补值角标收入评审模式（GapMockHint 组件自闸，关闭时 DOM 零泄漏）；
4. 专家卡片跳转按现状（站内重点人才画像），不改深势地址；
5. 7165834364：分类导航对照需规补齐展示，筛选结果不特殊处理。

## 实现（lumen-ui-science-pc，6 文件）

### 新增

- `src/views/service/serviceGapMock.ts` — 缺口补值层（**全仓唯一来源**）：
  深势 `/v1/exchange/list`、`/recommendation` 无 需规 578「规模/参与者」与 579「重要程度/关联性」字段。
  用 FNV-1a 确定性哈希派生（同 key 刷新值一致，演示可复现，禁随机数）；档位枚举而非编造数值。
  切换路径：深势字段到位 → 删本文件 + 页面 resolve 调用，同名真值字段直接替换。
- `src/views/service/serviceGapMock.selfcheck.mjs` — 确定性/值域/热度弱相关自检。
- `src/views/service/tech-comm-bugfix.test.mjs` — 5 条缺陷关键接线自检（mock 隔离约定 + 埋点）。

### 修改

- `src/views/service/tech-communication/index.vue`（交流页）：
  - 7168000620：筛选栏加「活动规模/参与者」两档位下拉（选项来自 serviceGapMock 枚举），前端过滤 + 地图视野联动；带 ⚠️ tooltip「深势接口暂未提供该维度，当前为演示补值」；
  - 7167768748：资源推荐区加 列表/图表/知识图谱 三视图切换——柱状图按活动聚合真实阅读量；知识图谱为 活动-资源-专家 三层力导向图（ECharts graph，仓内已注册），节点大小映射演示 importance，tooltip 带真实阅读量+关联性；列表补「重要程度 n/5 · 关联性 n/5」列；底部诚实标注演示补值；
  - 7168028103：专家卡 a-popover hover 弹窗（机构/领域/简介/标签/关联活动数），点击 `router.push('/talent/key-talent-profile', { keyword: 姓名 })`；
  - 补 `svc-exchange-track` CustomEvent 埋点（架构铁律 4）。
- `src/views/service/tech-communication-analysis/index.vue`（传播页）：
  - 7165795820：筛选栏加「主题」（快照 distinct subjectCategoryName → 反查 subjectCategoryId 走 BFF；查不到 id 不传参诚实全量）与「发布时间」四档（换算 publishStartTime 走 BFF）；
  - 7165547770：视图「卡片」→「图文」（需规术语）；新增「信息图」第三视图：四张大数字卡 + 分类占比环图 + 月度发布趋势线 + 浏览 Top10 榜（可点击进详情），全部由已有全量快照 allContents 聚合，无新接口无新依赖；
  - 7165834364：分类导航对照需规 593/596 补齐 10 类（接口真实 7 类 + 需规缺源 3 类「创新成果展览/科学人讲坛/信息素养大讲堂」哨兵 code 100/101/102，count=0）；点击缺源分类本地置空不发请求（实测对端非法 code 返 148888 业务错误会弹全局 toast）；11 卡 `span=2` 一行对齐原型；
  - 补 `svc-communication-track` 埋点。
- `src/views/talent/profile/index.vue`：消费 `query.keyword` 跨页定位（mock 态 onMounted 兜底；真实态 loadDataset 后定位），供交流页专家跳转。

## 验证证据

- `node src/views/service/serviceGapMock.selfcheck.mjs` → ✅ 全绿（确定性/值域/热度弱相关）
- `node src/views/service/tech-comm-bugfix.test.mjs` → ✅ 全绿（6 缺陷接线 + mock 隔离 + 埋点）
- `pnpm type-check` → ✅ exit 0（修一处 noUncheckedIndexedAccess）
- `pnpm build` → ✅ exit 0
- merge 远端 26 文件后再跑 type-check → ✅（无冲突，推送前复验）
- commit：`13ebaab`（8 文件 +757/-34）→ merge → push `e78803b` `origin/dev`

## 架构合规自检（§2 铁律）

- D8 ✅ 全部 Arco 控件（a-select/a-popover/a-tooltip/a-statistic），主色 165DFF，32px 控件高
- D9 ✅ 演示补值显式 ⚠️ 标注不冒充真数据；真实阅读量与补值字段分列展示；档位枚举不编人数
- D12 ✅ 未调任何 demo-* 服务
- 铁律 4 ✅ 两页新增 CustomEvent + createTraceId 埋点
- 铁律 2（调用链）✅ 只走既有 BFF /display/v1/exchange|communication/**，未新增越层调用
- mock 种子冻结 ✅ serviceGapMock 为确定性派生（非 Math.random），刷新一致

## 偏离与遗留

1. ~~未 commit/push~~ → 已完成（`e78803b` → `origin/dev`，用户逐字指令 2026-11-14 13:25）。
2. **深势字段到位后的切换**：删 serviceGapMock.ts + 两页 resolve 调用 + ⚠️ 标注，同名字段直连。
3. **缺源三类真数据**（7165834364 残余）：深势新增受控 contentType 后，删哨兵 code 100/101/102 与本地置空分支，`contentTypes` 表换真实枚举即可；映射表确认事宜不再阻塞前端。
4. 飞书 6 条缺陷回写说明：待部署 dev 并复测后进行（届时走 feishu-bugfix 流程或按孔东指令）。

## cost

- actual_tokens: ~200k（含前序汇总分析会话 + 本轮推送收尾）
- model_used: claude-sonnet-4-5（Cursor agent）
- actual_cost: ~$7
- cost_warn: false

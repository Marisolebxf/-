# FE-SVC-COMM-BUGFIX-L01 · 科技交流/科技传播 5 条 OPEN 缺陷修复

- **状态**：代码完成 + 三绿自检通过；前端仓改动停在本地工作区，等孔东确认提交（本机裁定 2026-11-12）
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
| 7165834364 (P0) | 分类与需规不符（7 类 vs 10 类） | 596 传播形式分类展示 | ⛔ 不在本单（需黄敬洲确认映射表后另开 BFF 单） |

## 用户裁定（2026-11-14，本单依据）

1. 前端改动直接动工；
2. 深势提供不了的字段 → 前端 mock 补足，**做好隔离**，后期深势供数后方便切换。

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
  - 补 `svc-communication-track` 埋点。
- `src/views/talent/profile/index.vue`：消费 `query.keyword` 跨页定位（mock 态 onMounted 兜底；真实态 loadDataset 后定位），供交流页专家跳转。

## 验证证据

- `node src/views/service/serviceGapMock.selfcheck.mjs` → ✅ 全绿（确定性/值域/热度弱相关）
- `node src/views/service/tech-comm-bugfix.test.mjs` → ✅ 全绿（5 缺陷接线 + mock 隔离 + 埋点）
- `pnpm type-check` → ✅ exit 0（修一处 noUncheckedIndexedAccess）
- `pnpm build` → ✅ exit 0
- `git status`（前端仓）→ 仅本任务 6 文件（3 M + 3 ??），无夹带

## 架构合规自检（§2 铁律）

- D8 ✅ 全部 Arco 控件（a-select/a-popover/a-tooltip/a-statistic），主色 165DFF，32px 控件高
- D9 ✅ 演示补值显式 ⚠️ 标注不冒充真数据；真实阅读量与补值字段分列展示；档位枚举不编人数
- D12 ✅ 未调任何 demo-* 服务
- 铁律 4 ✅ 两页新增 CustomEvent + createTraceId 埋点
- 铁律 2（调用链）✅ 只走既有 BFF /display/v1/exchange|communication/**，未新增越层调用
- mock 种子冻结 ✅ serviceGapMock 为确定性派生（非 Math.random），刷新一致

## 偏离与遗留

1. **未 commit/push**（孔东本机裁定）：改动停工作区，待孔东逐字指令提交。
2. **7165834364 分类映射**：等黄敬洲确认「需规 10 类 ↔ 深势 contentType」映射表后另开 BFF 任务（svc-platform）。
3. **深势字段到位后的切换**：删 serviceGapMock.ts + 两页 resolve 调用 + ⚠️ 标注，同名字段直连。
4. 飞书 5 条缺陷回写说明：待部署 dev 并复测后进行（届时走 feishu-bugfix 流程或按孔东指令）。

## cost

- actual_tokens: ~180k（含前序汇总分析会话）
- model_used: claude-sonnet-4-5（Cursor agent）
- actual_cost: ~$6
- cost_warn: false

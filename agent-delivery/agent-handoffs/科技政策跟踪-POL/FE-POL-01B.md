# FE-POL-01B · 科创政策全景 — 其余 4 Tab（动向/舆情/比对/订阅）整段复刻

> 交付日期：2026-11-02 · 仓：`repos/lumen-ui-science-pc` · 状态：**本地工作区交付，等人工走查**（2026-10-20 闸门：走查通过前不推 dev）

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:孔东` |
| claim_type | `pull`（开工登记见 task note 2026-11-02） |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 派单 `/goal` 强度 full。零新依赖（echarts/vue-echarts 仓内已装）；全部复用 S01/01A 基座（mock 种子冻结、PolicyStatCard、MockBadge、IndustrySelect、usePolicyTrack、评审层 store、trackingExport HTML 报告策略）。未跳过 D8（统计卡 Arco 化 + token 对齐）、D9（每个统计数字 ⓘ + Mock 🧪 角标；订阅中心无统计数字，demo 同款无角标）、D10（弹层全 Teleport to body、键盘可达、Arco 优先）、可观测（trackPolicyInteraction 沿用）、架构铁律（D12 零 demo 依赖） |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip`（本机未挂载） |

## 问题清单

- 无阻塞问题。4 个执行中判定：
  1. `IconEarth` 不存在于 Arco Vue icon 集 → 换 `IconCompass`（语义：领域指南针）
  2. seed 冻结文件 `policySubscriptionSeed.ts` 被 `policy.test.mjs` 逐字节比对锁定——类型修复不在 seed 内做（会破坏冻结），在消费组件 `SubscribeTab.vue` 本地类型化包装（`notifyLabel`）
  3. `formatNotifyLabel` 签名推断 `never[]`（@ts-nocheck 副作用）→ 同上消费点包装解决
  4. demo 订阅中心无统计数字、无 MockBadge → Vue 化保持一致（D9 角标只约束统计数字位）

## 修改内容

### 其余 4 Tab（`src/views/policy/panorama/`，15 文件新增）

**① 动向跟踪（`components/TrendTab.vue`）**
- 管线阶段同步（demo pipelineSteps 冻结：采集→解析→入库→去重→标引）+ 进行中进度语义（不显百分比）
- 采集任务表 / 权威源状态 / 最新入库政策列表 / 发布趋势统计
- 时间轴 + 热力/趋势 VCharts（容器显式高度防 init 0 高死锁，复刻经验 §3）
- 重点领域政策分析面板（`KeyFieldAnalysisPanel.vue` 卡片列表 + 深度报告弹窗）

**② 舆情评估（`components/SentimentTab.vue`）**
- 情感分布（正/中/负 % + 样本量，读 S01 镜像 metric_id ⓘ + Mock 🧪）
- 主题情感分布条形分解 / 多维检索跳转（回检索 Tab）
- 区域政策差异面板（`RegionalDifferencePanel.vue`：覆盖范围/支持力度/实施条件矩阵）
- 受众反馈收集（`FeedbackPanel.vue`：问卷/在线评价/意见征集三渠道 + 意见聚类 + 详情弹窗）
- 政策效果评估报告列表 + `EvaluationReportModal.vue`（维度得分 + 建议导出）
- 实施跟踪（`ImplementationTracker.vue`：指标值/目标/状态/趋势表）
- 匹配推送触发（`PolicyMatchPanel.vue` 弹窗承载）

**③ 重点比对（`components/CompareTab.vue`）**
- 六能力入口卡：新旧版本对比 / 详情对比 / 部门对比 / 标杆比对 / 报告生成导出 / 可视化
- 标杆地区预览条（进度分）
- 对比弹窗族 4 件（全部 Teleport to body）：
  - `ComparisonModal.vue`：多政策详情对比表 + 差异条形图 + 优劣分析 + 报告导出
  - `VersionCompareModal.vue`：时间轴 + diff 表（新增绿/删除红删除线/修改蓝）+ 变化统计 + 版本报告导出
  - `DepartmentCompareModal.vue`：跨区域选部门（≥2 闸门）+ 项目类别/技术类别堆叠条形图 + 清单表
  - `BenchmarkCompareModal.vue`：雷达/条形/热力可视化 + 标杆数据表 + PDF/Word 对标报告导出

**④ 订阅中心（`components/SubscribeTab.vue` + `components/SubscribeModal.vue`）**
- 双 Tab：我的订阅（CRUD：立即推送/修改/取消）+ 推送收件箱（未读 Badge/标已读/清空）
- 订阅条件：类别/行业（IndustrySelect）/部门/地区；频率日/周/月；通道系统通知/邮件/短信（后两者演示）
- 持久化：localStorage（D7 演示态，键名冻结 demo `gkx-policy-sub-*`）
- 推送摘要：`buildSubscriptionDigest`（频率前缀 + 命中数 + 前三标题 + 通道标签）

**⑤ 企业匹配与推送（`components/PolicyMatchPanel.vue`）**
- 按企业画像（行业/规模/阶段/研发预算）自动打分匹配（`matchPoliciesToEnterprise` 冻结语义：行业精确 52 分入围 + 规模/阶段/研发门槛加成 + 上限 99）
- 实时重算（草稿画像 watch）/ 推送配置（多通道）/ 一键订阅
- 深链 `?tab=match` 直达（index.vue：`initialTab='trend'` + 挂载后自动开匹配弹窗，demo initialOpenMatch 语义）

**⑥ 导出工具（`trackingExport.ts`）**
- `exportHtmlDoc` 基座：HTML `.doc` Word 生成 + 打印窗 PDF（与 01A `exportPoliciesPdf` 同策略，零新依赖）
- `exportDetailCompareReport` / `exportVersionCompareReport` / `exportEvaluationReport` / `exportBenchmarkReport` 四报告出口

**⑦ 最小自检（`FE-POL-01B.test.mjs`）**
- 订阅引擎：归一化（null/all/cascade path/叶子 key/混合形态）+ 条件求交（维内 OR 维间 AND 未选不限）+ 行业 key 精确匹配（legacy slug label 不在 industryFields → 不命中，冻结语义）+ 条件格式化 + 摘要
- 企业匹配评分：AI 企业必命中政策 1 / 得分 ∈ [50,99] / 入围必有理由 / 降序 / 空入参兜底
- 版本 diff 三态：政策 1 三版本锚点 + 删除态在场
- 深链：`tab === 'match'` 映射 + 自动开弹窗
- 组件锚点：4 Tab 结构 + 6 弹窗 Teleport + 匹配面板接引擎 + localStorage + 导出接线 + Mock 角标 ×3
- 运行：`node src/views/policy/panorama/FE-POL-01B.test.mjs`

## 测试结果（交付三绿）

| 门 | 结果 |
|---|---|
| 自检 ×3 | ✅ FE-POL-01B 全绿 + FE-POL-01A 回归全绿 + S01 `policy.test.mjs` 回归全绿 |
| `pnpm type-check` | ✅ 0 错（修复 17 处：MockBadge 导入路径 ×6 / IconEarth→IconCompass / TableColumnData key 属性 / row-key 函数签名 / meta possibly-undefined / stats 参数必填 / selectedPolicies 可选 / never[] 包装） |
| `pnpm build` | ✅ built in 27.93s |

**附录 D 防漏扫描**：互斥 display 叠加 0 / v-if+v-show 同节点 0 / USE_MOCK=false fixture 填数 0 / 新页菜单差集 0（01B 不建菜单，S01 已建）。

## 遗留风险

1. **收件箱真实外发**：邮件/短信通道为演示语义（Message 提示），真实外发需 BE 通道服务（未立项，YAGNI）
2. **对标报告 PDF**：走打印窗策略（浏览器打印 → 存 PDF），非服务端生成；若需服务端 PDF 另立单
3. **匹配评分权重**：冻结自 demo `policyMatchSeed`；若 BE-POL 后续提供匹配服务，前端换接（当前 mock 双轨）
4. **契约未冻结**：数据走 S01 mock 双轨；BE-POL-CONTRACT-01 定稿后统一替换，本单无新 api 面

## CI/CD（必填）

- 分支：`dev`（**本地未推**，等人工走查放行）
- commit：走查通过后按闸门流程推
- pipeline / K8s：push dev 后 CI 触发
- dev 验证命令：`node src/views/policy/panorama/FE-POL-01B.test.mjs && node src/views/policy/panorama/FE-POL-01A.test.mjs && node src/views/policy/policy.test.mjs && pnpm type-check && pnpm build`

## 可观测性（建议）

- 交互埋点：`trackPolicyInteraction('panorama', …)` 沿用 S01/01A 机制（page-mounted / open-detail / export / subscribe）
- pageview：路由 guard 自动覆盖

## 涉及文件

**新增（16）**
- `src/views/policy/panorama/`：`trackingExport.ts`、`FE-POL-01B.test.mjs`
- `components/`：`TrendTab.vue`、`SentimentTab.vue`、`CompareTab.vue`、`SubscribeTab.vue`、`SubscribeModal.vue`、`ComparisonModal.vue`、`VersionCompareModal.vue`、`DepartmentCompareModal.vue`、`BenchmarkCompareModal.vue`、`EvaluationReportModal.vue`、`FeedbackPanel.vue`、`ImplementationTracker.vue`、`RegionalDifferencePanel.vue`、`KeyFieldAnalysisPanel.vue`、`PolicyMatchPanel.vue`

**修改（2）**
- `src/views/policy/panorama/index.vue`（4 Tab 接线 + 订阅状态 + 深链 match + 对比篮）
- `src/views/policy/panorama/components/SubscribeTab.vue`（类型包装；详见问题清单 2/3）

# TOPIC-SYNTH-R3 · 综合智能分析 R3 — 区域创新分析（五件套 + 闭环重实现）Handoff

> **任务**：TOPIC-SYNTH-R3（E8-综合智能分析 · P3 批）
> **执行**：agent:frontend ｜ **监管**：human:淮政玮
> **日期**：2026-08-06
> **状态**：integration（联调确认后待 R4 总收口）

---

## 1. 范围与实现（对照 bid-reference）

范围真源：`agent-delivery/bid-reference/科技信息展示系统和科技专题服务系统.md` §1.1.1.2.4.2.8（8.1/8.2/8.3），共 **9 个三级项**，逐条闭合：

| # | 招标三级项 | 落点 | 结论 |
| --- | --- | --- | --- |
| 8.1.1 | 指标体系构建 | US-SYN-02：两层指标体系（4 维度 → 12 指标）分层展开，维度权重合计 100%，指标行含口径说明 | ✅ |
| 8.1.2 | 综合评价模型 | US-SYN-03：演示态加权合成模型（四维等权 + 对比集合内最大值归一），算法无定义卡 → D1 missing 诚实态 | ✅（演示口径，Q-SYNTH-01） |
| 8.1.3 | 区域指数计算与可视化 | US-SYN-03：指数总览卡 + 分项得分对比 + 区域排名榜（点击切换目标区域）+ 时间窗趋势曲线 | ✅ |
| 8.2.1 | 创新要素数据汇聚 | US-SYN-04：人才/资本/平台/项目四类要素规模卡 + 要素详情抽屉（构成明细、代表主体样例） | ✅ |
| 8.2.2 | 要素评价模型构建 | US-SYN-04：四维评价（规模/质量/结构/流动）雷达，目标区域 vs 对比均值；模型未定 → D1 missing | ✅（演示口径，Q-SYNTH-02） |
| 8.2.3 | 要素影响关联分析 | US-SYN-05：要素贡献度条形（降序合计 100%）+ 影响路径卡联动选中 | ✅（演示口径，Q-SYNTH-02） |
| 8.3.1 | 创新主体关系图谱 | US-SYN-06：ForceGraph 企业-科研机构-人才-高校-服务机构主体图谱，产业领域/主体类型筛选与统计区同步 | ✅ |
| 8.3.2 | 协同度计算模型 | US-SYN-07：协同指数（网络密度×强度均值演示合成）+ 联合专利/合作项目/人才流动三分项；算法未定 → D1 missing | ✅（演示口径，Q-SYNTH-03） |
| 8.3.3 | 协同效果评估 | US-SYN-07：协同集群识别（图谱联动高亮）+ 孤立主体清单 + 协同-产出相关性 + 报告触发 | ✅（演示口径，Q-SYNTH-03） |

叶子划分：本模块 9 个三级项同属"区域"分析对象、共享区域/时间窗上下文，判定为 **1 个叶子 SYNTH-REGION**（E8 README 已注明理由）。

## 2. 产物清单

### 2.1 五件套（编排仓 `agent-delivery/agent-handoffs/产品整体定义/E8-综合智能分析/`）

| 文件 | 说明 |
| --- | --- |
| `README.md` | E8 模块定位、叶子划分（单叶子理由）、开放项索引 |
| `SYNTH-REGION-区域创新分析/USM-SYNTH-REGION.md` | 7 故事（US-SYN-01~07），主路径/异常表/AC 共 34 条，粒度对齐 E2 金标准与 E7 叶子包 |
| `.../IA-SYNTH-REGION.md` | 稳定 ID、三页 IA、URL 契约（`region`/`window`/`element`/`industry`/`node`）、Frame 职责、跨模块出入口 |
| `.../Wireframe-SYNTH-REGION.md` | F-SYN-01~05 骨架：上下文条/活力总览/要素分析/协同图谱/要素抽屉/主体抽屉 + D9 角标图例 |
| `.../UX-SPEC-SYNTH-REGION.md` | 旅程、状态机（区域上下文/下钻链路/图谱选中）、异常/空态表、键盘可达、持久化契约（`topic-synth-`）、ReviewMode 集成 |
| `.../TRACE-SYNTH-REGION.yaml` | 9 项需求→故事→Frame→实现正反向核对、9 枚 `M_SYNTH_*` 指标注册、Q-SYNTH-01~03、CT-SYN-01~03 跨模块契约 |

### 2.2 实现（业务仓 `demo-ui-topic`，commit `905da04`，origin/dev）

12 文件变更（+2828 / −1509），`src/app/pages/intelligence/` 域重构：

| 文件 | 职责 |
| --- | --- |
| `synthData.ts` | 区域库/时间窗/指标体系/四类要素/协同图谱确定性 mock；图谱实体 ID 与企业库、服务机构库共用 ID 体系 |
| `synthModel.ts` | 指标得分/活力指数/排名/要素评价/贡献度/网络密度/中心性/协同指数/产出相关性推导（演示态公式，前端可复现） |
| `synthStore.ts` | reducer + localStorage（前缀 `topic-synth-`，版本化，损坏回落默认+提示）：区域/对比范围/时间窗/展开维度/图谱筛选 |
| `intelReadinessSeed.ts` / `intelReviewData.ts` | D9 指标 8 件套镜像 + 四维就绪度种子（9 枚 `M_SYNTH_*`）+ Q-SYNTH 开放项 |
| `IntelReviewMount.tsx` / `IntelMetricBadges.tsx` / `intelligence.css` | 评审层门控（reviewMode 自闸，业务态零泄漏） |
| `synthShared.tsx` | 三页共享：区域上下文条（区域/对比范围/时间窗 + 报告触发 `data-system-report-trigger`）、URL 同步 hook、雷达图、区块标题 |
| `RegionalInnovationVitality.tsx` | 活力页：指数总览卡 + 分项对比 + 区域排名榜（点击切换）+ 趋势 + 指标体系分层展开 + "下钻要素分析"入口 |
| `RegionalInnovationElements.tsx` | 要素页：四类要素规模卡 + 四维评价雷达 + 贡献度/影响路径联动 + 要素详情抽屉（URL `element` 分享恢复） |
| `RegionalInnovationCollaboration.tsx` | 协同页：主体关系图谱（筛选/选中持久化 + URL）+ 网络统计 + 协同指数 + 集群/孤立主体 + 产出相关性 + 跨模块下钻 |

### 2.3 跨模块互通（CT-* 契约，已登记 TRACE）

| 契约 | 内容 | 状态 |
| --- | --- | --- |
| CT-SYN-01 | 协同图谱企业节点（`entRef`=企业库真实 code）→ `/enterprise-center/profile/:code` 企业画像 | ✅ 已接通 |
| CT-SYN-02 | 协同图谱服务机构节点（`svcRef`=service-center 机构 ID）→ `/service/institution-judgment?org=` 机构画像抽屉 | ✅ 已接通 |
| CT-SYN-03 | "生成协同效率报告"复用系统报告面 `data-system-report-trigger` 机制 | ✅ 已接通 |

对比篮判断：region 是分析上下文而非可收藏实体，SYS-COMPARE-WORKSPACE 系统篮语义面向企业/机构等实体对象，**region 不入篮**；区域对比经上下文条"对比范围"完成（USM"不包含"已声明）。

### 2.4 决策登记

`客户决策清单跟踪表.md` 新增 **Q-SYNTH-01**（活力指数综合评价模型）、**Q-SYNTH-02**（要素评价模型 + 影响关联口径）、**Q-SYNTH-03**（协同度计算 + 效果评估口径），均 🟡 待算法 Lead + 甲方。

## 3. AC-US 自走查（34/34 通过）

| 故事 | AC | 结果 | 走查要点 |
| --- | --- | --- | --- |
| US-SYN-01 | 01-01 | ✅ | 上下文条三页共用 `SynthContextBar`，store 共享，切页保持一致 |
| | 01-02 | ✅ | 区域/对比范围/时间窗 localStorage 持久化（`topic-synth-context`），刷新保留 |
| | 01-03 | ✅ | URL `region`+`window` 直达恢复且优先于持久化（`useSynthUrlSync` 初始化优先级） |
| | 01-04 | ✅ | 非法 `region` 回落默认区域 + Message 提示，无空白页/NaN |
| US-SYN-02 | 02-01 | ✅ | 4 维度×12 指标含高企数量/专利申请授权/高质量论文等 Bid 列举维度，两层完整渲染 |
| | 02-02 | ✅ | 维度行显示权重、合计 100%；指标行含口径说明文本 |
| | 02-03 | ✅ | 展开/收拢入 store 持久化，刷新保留，不影响其他区 |
| | 02-04 | ✅ | 指标得分旁 ⓘ `M_SYNTH_INDICATOR_SCORE`（draft ⚠️ Q-SYNTH-01）+ 🧪；无数据行不渲染伪得分 |
| US-SYN-03 | 03-01 | ✅ | 指数=`computeVitality` 单一计算源，指数卡/分项/排名同一次结果，无两处不一致 |
| | 03-02 | ✅ | 指数旁红问号（`M_SYNTH_VITALITY_INDEX` D1 missing，只显 Q-SYNTH-01 治理引用）+ 🧪 |
| | 03-03 | ✅ | 排名卡点击切区域，全区重算，URL `region` 同步，刷新保留 |
| | 03-04 | ✅ | 排名榜降序与指数值一致，当前区域高亮 + "当前"标识 |
| | 03-05 | ✅ | 时间窗 3/5/8 年切换趋势数据点数一致 |
| | 03-06 | ✅ | "下钻要素分析"跳转要素页上下文一致，浏览器返回恢复原状态 |
| US-SYN-04 | 04-01 | ✅ | 规模卡数值=抽屉构成明细合计；旁挂 ⓘ `M_SYNTH_ELEMENT_SCALE`（aligned）+ 🧪 |
| | 04-02 | ✅ | 四维评价得分旁红问号（`M_SYNTH_ELEMENT_SCORE` D1 missing，Q-SYNTH-02）+ 🧪 |
| | 04-03 | ✅ | 雷达两系列图例独立开关，切区域重算 |
| | 04-04 | ✅ | URL `element` 分享恢复抽屉；关闭移除参数不重载主体 |
| | 04-05 | ✅ | 抽屉代表主体样例经 `resolveElementSamples` 从协同图谱解析，同一实体 ID 体系 |
| US-SYN-05 | 05-01 | ✅ | 贡献度降序合计 100%（±1 归整），与结论区 TOP 要素一致 |
| | 05-02 | ✅ | 贡献度旁红问号（`M_SYNTH_ELEMENT_CONTRIB` D1 missing，Q-SYNTH-02）+ 🧪 |
| | 05-03 | ✅ | 点击要素条影响路径卡更新+选中态；再点取消回引导态 |
| | 05-04 | ✅ | 结论区 🧪，数值均取自当前推导结果，无编造数值 |
| US-SYN-06 | 06-01 | ✅ | 图例与节点配色一致（KIND_META 单源）；筛选后图谱与节点/边/密度统计同步 |
| | 06-02 | ✅ | 企业节点→`/enterprise-center/profile/:code`（企业库真实 code）；服务机构节点→E7 机构画像 `?org=` 自动开抽屉 |
| | 06-03 | ✅ | 人才/高校节点本地抽屉 + "暂无跨模块统一画像"边界说明 |
| | 06-04 | ✅ | 密度/中心性旁 ⓘ（`M_SYNTH_COLLAB_DENSITY`/`M_SYNTH_COLLAB_CENTRALITY`，draft ⚠️ Q-SYNTH-03）+ 🧪 |
| | 06-05 | ✅ | 筛选持久化 + URL `industry`/`node` 参数刷新保留 |
| | 06-06 | ✅ | 中心性列表点击图谱节点选中高亮，再点取消 |
| US-SYN-07 | 07-01 | ✅ | 协同指数旁红问号（`M_SYNTH_COLLAB_INDEX` D1 missing，Q-SYNTH-03）+ 🧪；三分项逐项可见 |
| | 07-02 | ✅ | 集群卡点击图谱高亮成员与集群内边；成员 ID 与图谱一致 |
| | 07-03 | ✅ | 孤立主体列表=图谱无边/弱连接节点（同一数据推导），点击定位 |
| | 07-04 | ✅ | 相关性旁红问号（`M_SYNTH_COLLAB_OUTPUT_CORR` D1 missing）+ 🧪；结论数值与图表一致 |
| | 07-05 | ✅ | 报告按钮走 `data-system-report-trigger` 系统报告面机制，未新造弹窗 |

## 4. 架构合规自检（十条）

1. 算法只在 Python：✅ 纯前端 mock 演示；活力指数/要素评价/协同度均标演示态并登记 Q-SYNTH-01~03。
2. 调用链：✅ 无后端调用；正式接入按 IA §数据边界走 Java REST。
3. 图谱：✅ 前端 ECharts ForceGraph 演示，无 Neo4j；正式图谱按铁律走 NebulaGraph。
4. 可观测性：✅ 沿用本仓 `observability.ts`（`synth_report_trigger` 等埋点）。
5. CI/CD：✅ push origin/dev 触发流水线（本地 vite build + design:check 绿；远端状态见 §5）。
6. demo2 只读 merge：✅ 未触碰 lumen 仓。
7. 共享聚合核心：✅ 不涉及 Java 变更。
8. 数据策略：✅ 全 mock 确定性数据 + 🧪 标识。
9. 前端规范（D8）：✅ Arco React + ECharts，主色 `#165DFF`，Arco Icon 表状态、无 emoji 状态位；design:check 门禁通过（text-3xl 违例已修正）。
10. 数据血缘（D9）：✅ 9 指标注册（`M_SYNTH_*`），ⓘ+metric_id+四维就绪度角标走本仓评审层；VITALITY_INDEX/ELEMENT_SCORE/ELEMENT_CONTRIB/COLLAB_INDEX/COLLAB_OUTPUT_CORR D1 missing 红问号、INDICATOR_SCORE/COLLAB_DENSITY/COLLAB_CENTRALITY D1 draft ⚠️，禁止伪闭合。

## 5. 验收证据

- 业务仓 commit：`905da04`（`4c9d932..905da04`，origin/dev），12 文件 +2828/−1509，`[agent:frontend]`。
- 本地验证：`vite build` 通过（exit 0）；`design:check`（design contract + 两个 shell contract 测试）通过；改动文件 lint 0 错。本仓 `package.json` 无独立 tsc/type-check 脚本，类型门禁以 build + lint 为准（与 R1/R2 口径一致）。
- 远端 CI：push 已触发；当前会话令牌无 GitLab API 读权限，流水线绿灯待人工/后续确认（历史该仓 dev push 流水线均绿）。
- 决策登记：`客户决策清单跟踪表.md` Q-SYNTH-01/02/03。

## 6. 遗留风险与开放项

| 项 | 说明 | 去向 |
| --- | --- | --- |
| Q-SYNTH-01 | 活力指数综合评价模型无算法定义卡（指标正式清单/权重/归一化/合成公式），现为四维等权演示规则 | 待算法 Lead（唐绍祖）定义卡 + 甲方确认；落地前排名禁止对外决策展示 |
| Q-SYNTH-02 | 要素评价模型与影响关联口径未定（分类字典/四维权重/关联算法） | 同上；ELEMENT_SCORE/CONTRIB 保持 D1 missing |
| Q-SYNTH-03 | 协同度计算与协同效果评估口径未定（边权重/合成公式/产出关联方法） | 同上；COLLAB_INDEX/OUTPUT_CORR 保持 D1 missing |
| CI 绿灯确认 | 令牌无 API 权限，远端流水线状态未即时核验 | 监管人 GitLab 页面确认或 R4 补验 |
| 区域主数据 | 演示区域集（深圳+对标城市）为 mock，正式区域字典与行政区划精度关联 Q 表既有决策项 | R4 总收口时随数据侧对齐 |

## 7. Cost（已回填 registry）

| 字段 | 值 |
| --- | --- |
| actual_tokens | ~2,900,000 |
| model_used | claude-fable-5 |
| actual_cost | ~$8.7 |
| cost_warn | false |

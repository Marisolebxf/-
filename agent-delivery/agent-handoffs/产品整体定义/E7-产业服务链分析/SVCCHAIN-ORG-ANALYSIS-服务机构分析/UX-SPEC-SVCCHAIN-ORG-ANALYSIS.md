# UX-SPEC-SVCCHAIN-ORG-ANALYSIS｜服务机构分析 交互规格

> **版本**：v1.1-r2b（R2B 修订：新增 §2.4 对比篮、§9 企业检索对齐差异表；§2.2/§6/§8 同步）
> **交互权威**：`UX-UE 通用交互组件规范.md`；视觉 token 以 `Design.md` 为准
> **配套**：USM（故事与 AC）、Wireframe（结构与字段）、TRACE（追溯）

## 1. 用户旅程

```text
J1 采购/合作决策（GOV）：检索发现机构（三模式）→ 入篮/加入集合 → 确认领域+机构集合 →
   覆盖热力看重心 → 下钻画像核实 → 篮内勾选 2~5 家导入评估 → 形成遴选判断 → 返回来源
J2 投资/政策研判（INVEST/PARK）：进入趋势页签 → 选领域+时间窗 →
   看新增曲线 → 读热度研判（知悉演示口径）→ 下钻代表机构
```

## 2. 状态机

### 2.1 工作台外壳

```text
empty_selection ──选择机构确认──▶ ready ──切页签/领域──▶ ready（重算）
      ▲                            │
      └────────集合清空────────────┘
```

- `empty_selection`：三页签内容区显示 Empty + 主按钮"去选择机构"；指标条仍显示入库总数。
- `ready`：页签内容正常渲染；所有切换（tab/field/图型/时间窗）不回到 empty。

### 2.2 技术力评估

```text
configuring ──前置满足+开始评估──▶ evaluated
    ▲   │(改配置)                     │(改配置)
    │   └──────◀──────────────────────┘（结果标记"配置已变更，重新评估"）
```

前置校验（同时满足才可评估）：启用维度 ≥2；权重合计 =100%；对比机构 2~5 家。任一不满足：按钮禁用 + 按钮旁灰字原因；权重不满足另给"按比例归一"快捷钮。

【R2B】对比机构候选 = 系统对比篮 `service_org` 内容（唯一入口，AC-US-SVC-ORG-06-07）；篮空 → 对比对象区空态 + "去检索加入对比篮"；`source=compare-basket&org_ids[]` 进入时自动预选并滚动到评估区，无法解析的 id 汇总 Message。

### 2.3 机构画像抽屉

`closed ⇄ open(org_id)`；URL `org` 参数为唯一真源；参数非法 → 清参数 + Message，不进入 open。【R2B】抽屉头部提供"加入对比篮/已加入"切换按钮。

### 2.4 对比篮（R2B，系统层复用）

```text
入篮触点（检索行/集合与覆盖/抽屉/图谱节点/培育名单）
  ──addItem(service_org)──▶ 系统篮浮层 service_org Tab（列表/勾选/过滤/移除/清空）
  ──勾选2~5家·导入对比分析──▶ 保存 returnContext → 跳 R1 评估页(source=compare-basket)
  ──返回来源──▶ 恢复来源页关键词/筛选/滚动（会话内）
```

- 入篮/移篮为幂等切换（按钮态"加入对比篮 ⇄ 已加入"），跨页即时同步（系统篮统一存储）。
- 满篮拒绝写入 + Message；清空二次确认；上限沿用 `COMPARE_BASKET_MAX_ITEMS_PER_TYPE`。
- 面板同构 `PolicyCompareBasketPanel`；分发同构 `policyAnalysisRegistry`（服务机构注册表：分析项=技术力横向对比，对象约束 2~5）。

## 3. 反馈与错误恢复

| 场景 | 反馈 | 恢复 |
| --- | --- | --- |
| 集合变更（加入/移出/清空） | Message 轻提示 + 指标条联动 | 撤销=再次操作 |
| 评估完成 | 结果区滚动入视口，Message"评估完成" | — |
| 图表渲染异常 | 容器内 Alert + 重试按钮 | 点击重试重新渲染 |
| localStorage 恢复失败 | 回落默认 + Message"已恢复默认配置" | 重新配置 |
| URL 参数非法（field/org/tab） | 清除该参数 + Message | 页面按余下参数正常渲染 |

## 4. 键盘与无障碍

- 页签 Tabs：←/→ 切换，Enter 激活；`role=tablist/tab`，`aria-selected` 同步。
- 热力图行头、矩阵气泡、排名行、明细表机构名：Tab 可达、Enter 触发下钻，带 `aria-label="查看{机构名}画像"`。
- Modal/Drawer：打开焦点入内、Esc 关闭、关闭后焦点回触发元素；遮罩点击关闭仅限选择器 Modal（抽屉需显式关闭防误触）。
- 图表信息不只靠颜色：热力单元格内显示数值文本；曲线 hover/图例有文本；星级评级伴随文字评级。
- 演示态声明（🧪）在业务模式下用中文"演示口径"可读文案表达，不用图标独扛语义。

## 5. 响应式（medium_1440_1920）

- ≥1680：矩阵图与结论区并排；评估结果雷达 2×2 栅格。
- 1440：结论区换行至图下方；雷达 2×1；抽屉 480px 不变。
- 热力图机构 >8 行出现纵向滚动，行头列冻结。

## 6. 持久化契约（localStorage，前缀 `topic-svc-`）

| key | 内容 | 版本策略 |
| --- | --- | --- |
| `topic-svc-org-selection` | 已选机构 org_id[] | `v` 字段不符→回默认 |
| `topic-svc-field` | 主产业领域 field_id | 同上 |
| `topic-svc-tab` | 激活页签 | 同上 |
| `topic-svc-coverage-chart` | 覆盖图型 heatmap/matrix | 同上 |
| `topic-svc-trend-window` | 时间窗 3/5/8 | 同上 |
| `topic-svc-trend-compare` | 对比领域 field_id[]（≤2） | 同上 |
| `topic-svc-eval-config` | 维度启停/权重/自定义/对比机构/图型 | 同上 |

URL 参数（`tab/field/org`）优先级高于 localStorage；两者随交互双向同步。

【R2B 增补】：

- 对比篮内容持久化走系统篮统一存储（`compareBasketStore.ts`），**不**另建 `topic-svc-` key；篮 UI 会话（激活 Tab/关键词/滚动）走 `compareBasketUiSession`。
- 回跳上下文走 `compareBasketReturnContext` 同构机制（sessionStorage，一次性消费）。
- 检索页状态（模式/关键词/条件 DSL）会话内保留（sessionStorage），跨会话不承诺。

## 7. ReviewMode 集成

- 所有 D9 角标经 `ServiceReviewMount`（自建，模式对齐 industry-center）：`reviewMode=false` 时组件返回 null（自闸），DOM 零泄漏（无 metric_id/Q-*/GAP-* 字样）。
- mount_id 命名：`SVC-ORG-{FRAME}-{FIELD}-{KIND}`，如 `SVC-ORG-F02-DEPTH-METRIC`。
- 就绪度四维只读消费 `serviceReadinessSeed.ts`；D1 missing（`M_SVC_ORG_MARKET_HEAT`）点开只显 Q-SVCCHAIN-02 治理引用。

## 8. 机器可读交付契约

```yaml
frames:
  - {id: F-SVC-01, route: /service/institution-judgment, component: ServiceOrgAnalysisPage(shell)}
  - {id: F-SVC-02, route: "?tab=coverage", component: CoverageView}
  - {id: F-SVC-03, route: "?tab=trend", component: TrendView}
  - {id: F-SVC-04, route: "?tab=capability", component: CapabilityView}
  - {id: F-SVC-05, route: "?org=svc-org-*", component: OrgProfileDrawer}
  - {id: F-SVC-06, route: /service-center/search, component: "SearchScaffold + serviceOrgSearchConfig（R2B）"}
  - {id: F-SVC-07, route: 系统篮浮层 service_org Tab, component: "ServiceOrgCompareBasketPanel（R2B，同构 PolicyCompareBasketPanel）"}
stores:
  - {file: src/app/pages/service-center/serviceCenterStore.ts, pattern: reducer + localStorage, prefix: topic-svc-}
  - {file: src/app/components/common/compareBasketStore.ts, pattern: 系统篮统一存储（R2B 复用，type=service_org）}
data:
  - {file: src/app/pages/service-center/serviceCenterData.ts, deterministic: true}
dispatch:
  - {file: src/app/pages/service-center/serviceOrgAnalysisRegistry.ts, pattern: 同构 policyAnalysisRegistry（R2B）}
review:
  - {mount: ServiceReviewMount, readiness: serviceReadinessSeed.ts, reviewData: serviceReviewData.ts}
acceptance_source: USM-SVCCHAIN-ORG-ANALYSIS.md#4（AC-US-SVC-ORG-01..08）
```

## 9. 与企业检索模式的对齐与差异登记（R2B）

**对齐（同构，零改壳）**：同一 `SearchScaffold` 壳与 `ElementSearchConfig` 契约；三模式（keyword/smart/advanced）；字段库分类 + 运算符自适应 + D9 字段状态角标；结果卡片 schema 驱动；行级动作框架（`RowActionKey`）；结果内再筛选；对比篮/回跳上下文机制（`compareBasketStore` / `compareBasketUiSession` / `compareBasketReturnContext` 直接复用）。

**差异（显式登记，均有理由）**：

| # | 点 | 企业 | 服务机构 | 理由 |
| --- | --- | --- | --- | --- |
| 1 | 整页画像路由 | `/development/enterprise/:code` 整页画像 | 抽屉画像（F-SVC-05），不设整页路由 | 服务机构画像字段量级小（无经营/风险/招投标数据源），整页会大面积空态；D9 诚实态优先 |
| 2 | 行级动作 | compare/addToList/favorite/export/deepAnalysis/viewProfile | compare/加入分析集合/viewProfile | `addToList`（招引/培育名单）归 RECOMMEND 叶子避免双入口；export 沿用工作台级导出；"加入分析集合"为本模块特有（驱动覆盖/趋势视图） |
| 3 | 评分排序 | 综合竞争力（D1 aligned 链路） | 技术力分（D1 draft ⚠️ Q-SVCCHAIN-01） | 服务机构评分模型未拍板，排序可用但带 ⚠️🧪，不伪装正式口径 |
| 4 | 智能检索 NL 解析 | 企业字段词典 | 服务机构字段词典（类型/环节/领域） | 同一解析框架（`SmartSearchParser`），词典按要素注入 |
| 5 | 对比篮分发目标 | 多分析项（评估/风险等） | 单分析项（R1 技术力横向对比，2~5 家） | 服务机构当前仅一个对比型分析承接方；注册表结构保留扩展位 |
| 6 | 招引候选入篮 | 企业均在库可入篮 | 外部机构（RECOMMEND 招引名单）不可入篮 | 外部机构无画像/技术力数据（DEV-SVC-REC-01） |

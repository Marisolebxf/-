# 完整方案 · 展示系统「多维检索查询」复用专题「政策查询」

> **致**：沈悦（评审 / 体验把关）  
> **抄送建议**：高颖（DS10-12 Owner）· 孔东（权限/壳层，如并行）· 架构师（分轨合规）  
> **状态**：**approved** · v1.1 · 2026-08-08（沈悦确认 §14 五项）  
> **前序澄清**：展示系统**没有对比篮**；页内勾选 ≠ 系统对比篮  
> **替代**：同目录旧稿 `PLAN-展示多维检索复用专题政策查询.md`（内容并入本文件，以本文件为准）

---

## 0. 一句话结论

**复用专题政策查询的「检索工作台内核」（模式 / 字段库 / FilterDSL / queryEngine / SearchHub），嵌入展示科创政策全景的「检索全景」Tab；保留展示独有的左图右表、收藏分享导出与页内勾选对比；禁止引入对比篮、禁止跳转专题路由、禁止共用 storage。**

### 0.1 已批决策（沈悦 · 2026-08-08）· 实施铁律

| # | 决策 | 锁定值 | 实施约束 |
| --- | --- | --- | --- |
| D1 | 方案 | **批准方案 B**（嵌入式同构） | 禁止整页跳 `/policy/search` |
| D2 | 栈 + 视觉 | **检索条 Arco（B2）**；列表/图暂 AntD | **必须保留**专题同款搜索区视觉：蓝色渐变底 + 橙黄 CTA 按钮（见 §8.1.1） |
| D3 | 智能检索 | **Wave0 上线** | 模式可见；结果/解析标 🧪 Mock |
| D4 | 页内勾选上限 | **5** | 满 5 提示；禁止引入对比篮；Wireframe 原「演示 10」以本决策覆盖为 5 |
| D5 | 主模式文案 | **「关键词搜索」**（原批「多维检索」；2026-08-08 沈悦改序时调整） | Tab 顺序：`智能检索` → `关键词搜索` → `高级检索`；默认落在智能检索 |

```text
DEC-DS10-SEARCH-REUSE-20260808
  approved_by: 沈悦（会话确认）
  scheme: B_embed_isomorphic
  stack: arco_search_hub + antd_list_charts
  visual: enterprise-search-hero blue-bg + yellow/orange CTA (#ff7d00 族)
  smart_mode: on_wave0_mock
  page_compare_limit: 5
  mode_order: [智能检索, 关键词搜索, 高级检索]
  default_mode: smart
  mode_label_keyword: 关键词搜索
```
---

## 1. 背景与动机

| 项 | 说明 |
| --- | --- |
| 展示需求 | Bid `§1.1.1.1.4.2.1.1` **多维检索查询**（科创政策全景子功能） |
| 专题已落地 | E7 `/policy/search`：复用企业/产业同构的 `ElementSearchWorkbench` + `SearchHub`（`DEC-E7-SEARCH-REUSE`） |
| 痛点 | 展示 `PolicyPanorama` 自研 AntD 筛选/高级检索，与专题检索体验分裂，后续双维护成本高 |
| 目标 | Wave0 在 `demo-ui-science` 对齐检索交互；V2 再考虑抽共享包与正式仓 |

---

## 2. 产品边界（必读）

### 2.1 三系统分轨（不可破）

| 系统 | 路由空间 | 本方案角色 |
| --- | --- | --- |
| 科技信息展示 | `/display/policy/*`（Demo 菜单页 `policy-panorama`） | **改造目标**：多维检索区 |
| 科技专题服务 | `/policy/search` | **复用源**：检索内核与交互模式 |
| 智慧服务门户 | `/policy-portal/*` | **不在范围**（另轨） |

### 2.2 对比篮硬约束

| | 专题服务系统 | 科技信息展示系统 |
| --- | --- | --- |
| 系统对比篮 `ENT-COMPARE` | 有（政策分析经**产业 Tab**发起） | **无** |
| 政策查询是否加篮 | 政策查询本身不入政策篮（US-01c） | N/A |
| 多选对比能力 | — | **仅页内勾选** → 重点比对 Tab 或核增多维对比页 |
| 文案 | 「加入对比篮」等 | **禁止**出现「对比篮」；用「加入比对 / 勾选对比」 |

实现侧：展示可用本地 state 或 `sessionStorage` key `display-policy-compare-slots`，**不得**读写专题篮 storage，不得挂篮浮层。

### 2.3 目标用户故事对照

| 展示 US-DS-POL-01 | 专题 US-E7-POL-01c |
| --- | --- |
| 多维检索并浏览全景（图+列表），支撑决策/申报定位 | 在专题查询中核对关联政策语料（辅助，非主路径） |
| Bid 含收藏、分享、导出、二次筛选、智能排序 | 不入篮、不发起三项分析 |
| 同页还有动向 / 舆情 / 重点比对 Tab | 独立查询页 |

→ **交互壳可同构；页面职责与出口必须分叉。**

---

## 3. 需求能力映射（Bid 子功能 → 复用策略）

展示叶子 `1.1.1.1.4.2.1.1` 子功能：

| Bid 子项 | 能力 | 复用策略 |
| --- | --- | --- |
| 4.2.1.1.1 多维度检索条件 | 类别/领域/部门/地区等 | ✅ 字段库对齐 + SearchHub/Filter |
| 4.2.1.1.2 高级检索 | 效力/状态/布尔组合 | ✅ `advanced` 模式 + ConditionBuilder |
| 4.2.1.1.3 检索结果智能排序 | 相关/时效/级别等 | ✅ sortOptions（展示 config 自填） |
| 4.2.1.1.4 二次筛选与分类 | 结果区 refine | ✅ refineFieldKeys / 列表侧筛选 |
| 4.2.1.1.5 检索历史与收藏 | 历史 + 收藏 | ⚠️ 交互复用；**storage 前缀隔离** |
| 4.2.1.1.6 导出与分享 | Excel/PDF/链接 | ✅ 展示宿主保留；专题无则不抄 |

全景页其它 Tab（动向/舆情/重点比对）及核增四页：**不在本方案改造范围**，仅约定检索结果「页内勾选」可流向重点比对 / DS-PC-03。

---

## 4. 方案选型

| 方案 | 描述 | 结论 |
| --- | --- | --- |
| A. 展示跳转专题 `/policy/search` | 零开发 | **否决**（破分轨、丢全景图、无展示收藏分享合同） |
| **B. 嵌入式同构** | 拷贝/对齐检索内核，嵌进全景 `#search` | **采用** |
| C. 只抄视觉不抄引擎 | 继续双套逻辑 | 不推荐 |
| D. 立刻抽 npm 共享包 | 长期优 | Wave0 不做；列入 V2 |

**选定：方案 B（嵌入式同构）+ Wave0 仓内拷贝最小集。**

---

## 5. 目标架构

```text
┌─ 科创政策全景（展示 · DS-10）─────────────────────────────────────┐
│ Tab: [检索全景*] [政策动向] [舆情评估] [重点比对]                    │
├─ 检索全景 #search ───────────────────────────────────────────────┤
│                                                                   │
│  ┌─ 复用层（源自专题 search 模块）─────────────────────────────┐  │
│  │ SearchHub（智能检索 / 关键词搜索 / 高级检索）                 │  │
│  │ FilterPanel + ConditionBuilder + queryEngine + FieldLibrary │  │
│  │ RecentSearchPanel（key: gkx-policy-display-search-recents） │  │
│  └────────────────────────────┬────────────────────────────────┘  │
│                               │ FilterDSL + keyword + sort         │
│                               ▼                                    │
│  ┌─ 展示宿主（不复用专题整页）────────────────────────────────┐  │
│  │ 左：全景图（类别/地图/部门，点击反写 DSL）                   │  │
│  │ 右：结果列表/卡片 + 排序/二次筛选                            │  │
│  │ 详情抽屉 · 收藏 · 分享 · 导出                                │  │
│  │ 页内勾选 → 重点比对 Tab 或「升级」核增多维对比页              │  │
│  └────────────────────────────────────────────────────────────┘  │
│                                                                   │
│  �  │
│                                                                   │
│  ✗ 无系统对比篮  ✗ 不写 ENT-COMPARE  ✗ 不跳 /policy/search        │
└───────────────────────────────────────────────────────────────────┘
```

数据流：

```text
用户输入 → SearchHub 产出 { mode, keyword, dsl, sort }
        → runQuery(records) → filteredRecords
        → 左图聚合(filteredRecords) + 右列表(filteredRecords)
        →（可选）pageCompareIds[] → Tab#benchmark 或 PC-03 slots
```

---

## 6. 复用清单与非复用清单

### 6.1 从专题复用（源：`repos/demo-ui-topic`）

| 层级 | 资产 | 源路径 |
| --- | --- | --- |
| 类型契约 | `SearchMode` / `FilterDSL` / `ElementSearchConfig` / `FieldDef` … | `src/app/components/search/types.ts` |
| 引擎 | `runQuery` | `.../queryEngine.ts` |
| 壳 | `SearchHub` / `FilterPanel` / `ConditionBuilder` / `RecentSearchPanel` / `SearchContentSurface` / `ElementSearchWorkbench` | 同目录 |
| 可选 | `ResultToolbar` / `ResultList`（若列表也同构） | 同目录 |
| 数据形态 | `POLICY_FIELD_LIBRARY` / `POLICY_HOT_TAGS` / 记录结构 | `src/app/mock/policy/policySearchData.ts` |
| 智能解析 | `parsePolicyQuery` | `src/app/mock/policy/policySmartParser.ts` |
| 编排参考 | `PolicyTopicSearchPage.tsx`（只读参考，不整页搬） | `src/app/pages/policy/` |

**落地位置（展示）**：`repos/demo-ui-science/src/shared/search/`  
**配置**：`src/pages/policy-tracking/search/displayPolicySearchConfig.js`（或 `.ts`）

### 6.2 明确不复用

| 项 | 原因 |
| --- | --- |
| `PolicyTopicSearchPage` 整页 | 无全景图；出口合同不同 |
| 系统对比篮 / 加篮按钮 / 篮 storage | 展示无对比篮 |
| 三项分析发起 / 深度分析 CTA | 专题产业篮路径；展示无此出口 |
| `gkx-policy-topic-search-recents:v1` | storage 必须隔离 |
| 门户 `/policy-portal/search` 实现 | 另轨 |
| 专题 `rowActions` 默认集 | 须换成展示动作集 |

### 6.3 展示宿主必须自建/保留

- 左栏全景可视化（ECharts）与图→筛联动  
- 四 Tab 壳与动向/舆情/重点比对（本方案不改逻辑，只接勾选流入）  
- 收藏 / 分享 / 导出（Bid 要求）  
- 分轨说明条（相对专题 `/policy/*`）  
- D9：`MetricSpecTrigger` / Mock / Pending（可与评审壳计划合并）  
- 页内勾选上限：**5**（`DEC-DS10-SEARCH-REUSE-20260808`；覆盖 Wireframe 原演示 10 / 旧 Demo 3）

---

## 7. 配置合同（展示专用）

```ts
/** displayPolicySearchConfig — 与专题 POLICY_TOPIC_SEARCH_CONFIG 同构、出口分叉 */
{
  elementKey: 'policy-display',
  label: '政策',
  route: '/display/policy/panorama',          // 文档锚点，非独立路由页
  searchModes: ['smart', 'keyword', 'advanced'], // 默认 smart
  modeLabels: {
    smart: '智能检索',
    keyword: '关键词搜索',
    advanced: '高级检索',
  },
  pageCompareLimit: 5,     // 已批 D4
  fieldLibrary: DISPLAY_POLICY_FIELD_LIBRARY, // 含 Bid：类别/领域/部门/地区/效力/状态
  recommendedFieldKeys: ['category', 'industry', 'department', 'region', 'level', 'status'],
  sortOptions: [
    { key: 'relevance', label: '相关度' },
    { key: 'publishDate', label: '发布时间' },
    { key: 'level', label: '政策级别' },
    { key: 'supportStrength', label: '支持强度', metricId: 'M_POLICY_SUPPORT_STRENGTH' },
  ],
  refineFieldKeys: ['category', 'region', 'level', 'status'],
  rowActions: ['viewDetail', 'togglePageCompare', 'favorite', 'share'],
  forbidActions: ['compareBasket', 'addToBasket', 'launchAnalysis', 'deepAnalysis'],
  storage: {
    recent: 'gkx-policy-display-search-recents:v1',
    favorite: 'gkx-policy-display-favorites:v1',
    pageCompare: 'display-policy-compare-slots', // 页内勾选，非篮
  },
  boundaryCopy:
    '本区属科技信息展示系统 · 多维检索；与专题 /policy/search 分轨。展示系统无对比篮。',
}
```

字段库须覆盖 Bid 维度，并与现 `policyData.js` 的 category/industry/department/region/level 可映射（Wave0 可 adapter，不必一次换数据源）。

---

## 8. UI / 技术落地要点

### 8.1 栈策略（Wave0）· 已批 B2

专题检索组件为 **React + Arco**；展示全景页为 **React + AntD**。

| 选项 | 做法 | 状态 |
| --- | --- | --- |
| B1 | 拷贝 SearchHub 等并改为 AntD 控件封装 | 不采用 |
| **B2** | 检索条区域局部引入 Arco，列表/图暂留 AntD | **已批** |
| B3 | 只复用 `types`+`queryEngine`，UI 仍用手写 AntD | 退路（仅 B2 阻塞时） |

`#search` 顶部检索岛用 Arco `SearchHub` + `enterprise-search-hero` 视觉；下方图+表保持现有 AntD/ECharts。

#### 8.1.1 搜索区视觉合同（已批 · 必须保持）

复用专题企业/政策查询 hero 样式，**不得**改成扁平白底蓝按钮：

| 元素 | 规范（对齐 `demo-ui-topic` `theme.css` `.enterprise-search-hero`） |
| --- | --- |
| 背景 | 蓝色渐变 `linear-gradient(90deg, rgba(22,93,255,0.94), rgba(64,128,255,0.9))` + 可选底图 |
| 模式 Tab | 居中 pill；active 白底主色字 |
| 搜索按钮 CTA | 橙黄系 `#ff7d00`（hover `#f77200` / active `#d25f00`） |
| 输入区 | 白底圆角控件，浮在蓝底之上 |
| 作用域 | 展示侧 class 可用 `policy-display-search-hero`，token 与上表等价 |

实施时从专题拷贝对应 CSS 变量/`enterprise-search-hero` 规则到展示仓，或共享样式片段；验收以截图对照专题政策查询搜索区。

### 8.2 改造文件（预期）

| 动作 | 路径 |
| --- | --- |
| 新增 | `demo-ui-science/src/shared/search/**`（从专题拷贝最小集） |
| 新增 | `.../policy-tracking/search/displayPolicySearchConfig.*` |
| 新增 | `.../policy-tracking/search/displayPolicyFieldLibrary.*` |
| 新增 | `.../policy-tracking/search/useDisplayPolicyQuery.*`（DSL→filtered） |
| 大改 | `.../policy-tracking/PolicyPanorama.jsx`（#search 区替换） |
| 适配 | `policyData.js` ↔ 记录 shape adapter（若字段名不一致） |
| 文档 | 本方案 + Wireframe/UX-SPEC 一句同构说明 + 交付覆盖 |

### 8.3 与图的联动规则

1. 唯一事实源：`{ keyword, dsl, sort }`  
2. `filteredRecords` 同时驱动列表与图聚合  
3. 点击图块 = 合并对应维度条件到 dsl 并触发查询  
4. 「清空」同时重置 Hub 与图选中态  

### 8.4 页内勾选（非篮）规则

1. 列表 Checkbox / 「加入比对」→ `pageCompareIds`  
2. 上限：**5**（已批）；满则 Message「最多勾选 5 项进行比对」，不进篮  
3. 「去重点比对」切换 Tab `#benchmark` 并带入勾选  
4. 「升级多维对比」→ 核增页，写入 `display-policy-compare-slots`（同样遵守上限 5）  
5. UI 文案禁止「对比篮」「加篮」

---

## 9. 实施计划（可派单）

### Phase 0 · 评审确认 · ✅ 已完成（沈悦 2026-08-08）

- [x] 批准方案 B + 栈策略 B2  
- [x] 模式文案与顺序：「智能检索 → 关键词搜索 → 高级检索」（默认智能检索）  
- [x] 智能检索 Wave0 上线（🧪）  
- [x] 页内勾选上限 **5**  
- [x] 搜索区保持蓝底 + 橙黄 CTA  
- [x] 不做对比篮（硬约束）

### Phase 1 · 内核迁入 · ✅ 2026-08-08

- [x] `src/shared/search/queryEngine.js` 迁入  
- [x] 无专题篮/路由依赖  
- [x] queryEngine / smartParser fixture 冒烟  
- [x] 仓内已有 Arco，检索岛 B2 落地  

### Phase 2 · 全景嵌入 · ✅ 2026-08-08

- [x] `displayPolicySearchConfig` + DisplayPolicySearchHub + 蓝底橙黄样式  
- [x] `PolicyPanorama` #search 接入；布尔高级式保留为辅入口  
- [x] recent key `gkx-policy-display-search-recents:v1`  
- [x] 页内勾选上限 5 +「无对比篮」文案  
- [x] 分轨 Alert  
- [x] `npm run build` 通过  

### Phase 3 · 对照验收与文档 · 0.5–1d

- [ ] Bid `4.2.1.1.1`～`4.2.1.1.6` 检查表打勾  
- [ ] 分轨用例：无跳转专题、无篮 UI、无 topic recent key 写入  
- [ ] 更新 Wireframe §2 / UX-SPEC 检索条说明  
- [ ] handoff：`DS10-SEARCH-REUSE-L01.md`  
- [ ] 交付覆盖 `implementation-coverage` 增补条目  

### Phase 4 · V2（后置，不阻塞）

- [ ] 抽 `@gkxlumen/element-search`（或 mono package）供 topic + science 共用  
- [ ] API：`GET /v1/policy/search`，`client=display|topic` 仅投影动作不同  
- [ ] `lumen-ui-science-pc` 按同一 config 落地  

---

## 10. 建议任务 ID

| ID | 标题 | 仓 | 依赖 |
| --- | --- | --- | --- |
| `DS10-SEARCH-REUSE-L00` | 检索内核迁入 demo-ui-science + 去篮依赖 | demo-ui-science | 本方案批准 |
| `DS10-SEARCH-REUSE-L01` | 全景 #search 嵌入同构检索 + 图列表联动 | demo-ui-science | L00 |
| `DS10-SEARCH-REUSE-L02` | Bid 4.2.1.1 验收 + 五件套/覆盖回写 | orchestration + science | L01 |

> 建单走 task-registry MCP；本文件不直接改 registry。

---

## 11. 验收用例（给测试 / 沈悦走查）

| ID | 步骤 | 通过标准 |
| --- | --- | --- |
| A1 | 打开科创政策全景 → 检索全景 | 三模式顺序「智能检索 → 关键词搜索 → 高级检索」；默认「智能检索」；**蓝底+橙黄搜索按钮** |
| A2 | 选类别+地区查询 | 左图与右表同为过滤结果 |
| A3 | 高级筛选布尔条件 | 列表命中正确；可清除 |
| A4 | 智能检索 | 解析 chip 可见；结果 🧪 |
| A5 | 收藏 / 历史 / 分享 / 导出 | 可用；存储仅为 `gkx-policy-display-*` |
| A6 | 勾选至第 6 项 | 阻止并提示上限 5；无对比篮 |
| A7 | 勾选 2–5 项 → 去重点比对 | 进入比对 Tab；无篮浮层 |
| A8 | 升级多维对比 | 进入核增页；display slots；≤5 |
| A9 | 全文搜索「对比篮」「查政策」 | 「对比篮」无；Tab 为「智能检索 / 关键词搜索 / 高级检索」 |
| A10 | 路由 | 不导航至 `/policy/search` |
| A11 | 清 topic storage | 展示检索不受影响 |

---

## 12. 风险与缓解

| 风险 | 缓解 |
| --- | --- |
| Arco 引入与 AntD 并存样式冲突 | 检索岛独立 class 作用域；对照 Design.md 主色 `#165DFF` |
| 字段名与旧 mock 不一致 | adapter 层；不一次打穿数据重构 |
| 误做成对比篮 | Code review 检查 forbidActions + 文案扫描（A8） |
| 与「评审模式/权限壳复用」计划交叉 | 检索可先独立合入；角标门控后续挂 ReviewOnly |
| 范围膨胀到动向/舆情/核增 | 本方案 DoD 仅 #search；其它 Tab 只接勾选流入 |

---

## 13. 不做清单（签字用）

1. 不给展示系统做系统对比篮。  
2. 不整页跳转专题政策查询完成展示检索。  
3. 不共用 recent/favorite/basket storage。  
4. 不删除 Bid 要求的收藏/分享/导出。  
5. 不把专题查询改成带全景图的展示页。  
6. 不把门户检索纳入本迭代。  
7. 不在 Wave0 强行抽跨仓 npm 包。  

---

## 14. 决策记录（沈悦已确认 · 2026-08-08）

| # | 问题 | 确认 |
| --- | --- | --- |
| 1 | 批准方案 B（嵌入式同构）？ | **是** |
| 2 | 栈策略 B2 + 保持蓝底黄/橙按钮搜索区？ | **是**（视觉合同见 §8.1.1） |
| 3 | 智能检索 Wave0 上线？ | **是**（🧪） |
| 4 | 页内勾选上限？ | **5** |
| 5 | Tab 文案与顺序？ | **智能检索 → 关键词搜索 → 高级检索**（默认智能检索；原「多维检索」改称「关键词搜索」） |

→ 可派 `DS10-SEARCH-REUSE-L00` 开工；实施不得偏离 §0.1。

---

## 15. 参考真源

| 类型 | 路径 |
| --- | --- |
| 展示 Bid | `bid-reference/科技信息展示系统和科技专题服务系统.md` §1.1.1.1.4.2.1.1 |
| 核增（并列，非本方案主体） | `bid-reference/科技信息展示系统(政策对比功能升级)核增需求.md` |
| 展示五件套 | `产品整体定义/DS10-12-科技政策跟踪/` |
| 专题查询故事 | `E7-政策分析/USM-E7-政策分析.md` US-01c |
| 专题检索实现 | `repos/demo-ui-topic/src/app/pages/policy/PolicyTopicSearchPage.tsx` |
| 专题检索壳 | `repos/demo-ui-topic/src/app/components/search/*` |
| 展示现状 | `repos/demo-ui-science/src/pages/policy-tracking/PolicyPanorama.jsx` |
| 分轨 | DS10-12 UX-SPEC §1 分轨铁律；IA §3.2 |

---

**文档维护**：批准后将状态改为 `approved`，并在 DS10-12 PACK note 挂本路径；实施以 handoff `DS10-SEARCH-REUSE-L01` 关闭。

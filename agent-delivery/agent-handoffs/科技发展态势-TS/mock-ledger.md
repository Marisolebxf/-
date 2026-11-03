# 科技发展态势 · 代码层 mock 台账（跨页公共）

> 📌 **交叉引用**：整体对接进度（哪些已对接 / 真实 / mock / 缺口 / 等算法上线）见
> **`SITUATION-ENT-INTEGRATION-STATUS-20261103.md`**（2026-11-03 全端点实测）。本文件只管 mock 的逐条清理动作，不重复状态汇总。

> **任务**：`SITUATION-ENT-MOCK-LEDGER-L01`（WBS-05-18-11）· 监管人 `human:李伟`
> **性质**：只登记不实现。**真源以代码里的 `source="mock"` 字段为准**；本台账用于「去 mock 接真数」时逐条清理，不复制业务代码。
> **纪律**：mock 必须集中单一模块；不得写库、不得改数据源；mock 不参与排名 / 计分 / 导出。

## 登记表头（跨页复用，新增页按同一列填写）

| 列 | 含义 |
|---|---|
| 数据块 | 页面 / 接口 / 图表的数据面（例：科技全域态势 `/situation/map` 要素 chips） |
| 要素 key | mock 命中的契约 key（例：`journal` / `meeting`） |
| mock 文件与方法 | 唯一落点（类名 + 方法名），必须可定位 |
| 生成规则 | 值的来源与生成方式（冻结种子 / 固定映射 / 推导口径）；**禁止随机数** |
| mock_version | 与代码常量一致，种子或规则变化必须递增 |
| 真实源接替条件 | 什么数据到位后可以摘掉 mock，接到哪个源 |
| 清理条件 / 动作 | 接真数时要删/改的具体位置，确保不残留 |
| 建单任务 ID | registry 任务 ID，便于追溯建单依据与验收记录 |

## D3 登记（2026-11-01）

| 数据块 | 要素 key | mock 文件与方法 | 生成规则 | mock_version | 真实源接替条件 | 清理条件 / 动作 | 建单任务 ID |
|---|---|---|---|---|---|---|---|
| 科技全域态势 `/situation/map` 要素 chips（`factorItems[]`） | `journal`（期刊）/ `meeting`（会议） | `lumen-svc-platform` · `gkxlumen-display` · `com.topcomm.gkxlumen.display.support.SituationMockProvider`（`countOf` / `unitOf` / `metadata`），接线点 `SituationController#buildFactorItems` | 冻结常量：`journal=7200 种`、`meeting=1280 场`；出处 `demo-ui-science/src/data.js` factorItems（2026-11-01 快照）；无随机、无 DB、无外部调用 | `d3-v1` | 数仓接入「顶级会议 / 期刊名单」（`ADS_SCHEMA.md` 6.30.0 §24.10 当前列为缺失；`ads_venue_profile` / `ads_conference_profile` / `ads_journal_profile` 三表不存在） | 把 Provider 的 `countOf/unitOf` 换成 Feign 真实调用（调用点不变）；契约里的 `mock / mockReason / mockVersion` 一并删除；`SituationMockProvider` 整文件可删 | `SITUATION-ENT-D3-L01` |
| 科技全域态势 `/situation/overview` 要素卡（`stats[]` / `factorCards[]`） | `journal_total`（期刊）/ `meeting_total`（会议） | 同上 · `SituationController#buildStats` / `#buildFactorCards`（装配方法 `mockStat` / `mockCard`） | 与上一行同源同值（要素级总量，非城市级、非年度序列）；`series` 保持 `null` | `d3-v1` | 同上 | 同上（`mockStat` / `mockCard` 两个私有装配方法随 Provider 一并移除） | `SITUATION-ENT-D3-L01` |
| 科技全域态势 `/situation/map` 区域图层（`regions[].layerKeys`） | `journal` / `meeting` / `service` | 同上 · `SituationController#buildMap`（`MOCK_FACTOR_ORDER` → `mockLayerKeys`） | **只做图层存在标记**：key 进 `layerKeys`，**不进 `metrics`**（不给城市编造数值）；也不参与 `heatKey` 热力分档 | `d3-v1` | 同上（`service` 见下一行） | 移除 `buildMap` 里的 `mockLayerKeys` 追加块；城市级真数到位后再按真实 `metrics` 落值 | `SITUATION-ENT-D3-L01` / `INFLUENCE-FIX-L01` |
| 科技全域态势 `/situation/map` 要素 chips · **服务机构**（2026-11-01 用户裁定接线） | `service` | `SituationMockProvider`（`countOf` / `unitOf` / `metadata`，`REASONS` 逐要素原因），接线点 `SituationController#buildFactorItems` + `MOCK_FACTOR_ORDER` | 冻结常量：`service=6200 家`；出处 `demo-ui-science/src/data.js` factorItems；无随机、无 DB、无外部调用。⚠️ 必须同时进 `MOCK_FACTOR_ORDER`（`regions[].layerKeys`）——前端 `effectiveFactorKeys` 取 `layerKeys` ∩ 勾选集，只填 `factorItems` 则要素永远不可达 | `d3-v1` | CMS `v_cms_svc`（内容运营中心）真实计数端点 + display 侧 CMS 客户端 | 删 `COUNTS/UNITS/REASONS` 的 `service` 项与 `MOCK_FACTOR_ORDER` 的 `service`；`sourceOf("service")` 改回真实 CMS 标注 | `INFLUENCE-FIX-L01` |
| 前端评审角标 `MockBadge` | 任意带 `mock=true` 的卡片数值 | `lumen-ui-science-pc` · `src/review/MockBadge.vue`（挂载点 `views/situation/overview/components/OverviewTab.vue`） | 消费后端 `mock / mockReason / mockVersion`；仅在 `REVIEW_FEATURE.enabled=true` 时渲染（根部 `v-if`，DOM 零泄漏） | `d3-v1` | 后端 `mock` 字段消失即无角标可渲染 | 按 `src/review/README.md` 清理清单：删挂载点 → 删组件 → 删导出；检索 `MockBadge` / `.mock-badge` 归零 | `SITUATION-ENT-D3-L01` |

## 影响力登记（2026-11-01，INFLUENCE-FIX-L01）

> 缺口依据：`agent-delivery/metrics/指标入库详情-合并-20261028-三系统.xlsx` 已登记 5 类对象级影响力指标
> （`M_INNOV_PAPER_INFLUENCE` / `M_INNOV_JOURNAL_INFLUENCE` / `M_INNOV_PATENT_INFLUENCE` /
> `M_INNOV_SCHOLAR_INFLUENCE` / `M_SVC_ORG_TECH_SCORE`：支持度为「部分支持 / 完全转换支持」），
> 但**对象级影响力算法服务未上线、且无 dwd 通道** → 这三行是「算法未就绪」而非「指标未定义」。

| 数据块 | 要素 key | mock 文件与方法 | 生成规则 | mock_version | 真实源接替条件 | 清理条件 / 动作 | 建单任务 ID |
|---|---|---|---|---|---|---|---|
| 科技全域态势 `/situation/influence` 技术产出卡（含论文 / 期刊 / 专利 3 个子类） | `paper` / `journal` / `patent`（子类 key） | `SituationMockProvider#technologyOutputCard`（种子 `TECH_OUTPUT_SEEDS` / `TECH_OUTPUT_ITEMS`），接线点 `SituationController#influence` | 冻结种子取自 `demo-ui-science/src/data.js` `influenceFactorCards`（2026-11-01 快照）；`count` 与 `averageScore` 按筛选签名（地域 × 年份跨度 × 领域）确定性缩放（`influenceScopeScale`，charCode 哈希，**禁用 Math.random**）；分统一 `clampScore` 至 0–99.9 一位小数 | `influence-v1` | `M_INNOV_PAPER_INFLUENCE` / `M_INNOV_JOURNAL_INFLUENCE` / `M_INNOV_PATENT_INFLUENCE` 的算法服务上线（`原始计数 → P99.9 缩尾 → log1p → 组内 min-max → ×100 → 多维加权`） | 删 `technologyOutputCard` 与 `TECH_OUTPUT_*` 常量；契约 `mock / mockReason / mockVersion` 删除；`influence` 装配改为 Feign 调算法服务 | `INFLUENCE-FIX-L01` |
| 同上 · 专家卡 | `scholar` | `SituationMockProvider#influenceCard("scholar")`（种子 `SCHOLAR_ITEMS`） | 同上确定性缩放；4 条冻结种子 | `influence-v1` | `M_INNOV_SCHOLAR_INFLUENCE`（完全转换支持）算法服务接线 | 删 `influenceCard` 的 scholar 分支与 `SCHOLAR_ITEMS` | `INFLUENCE-FIX-L01` |
| 同上 · 服务项目卡 | `service` | `SituationMockProvider#influenceCard("service")`（种子 `SERVICE_ITEMS`） | 同上确定性缩放；3 条冻结种子。✅ 2026-11-01 已接线：服务机构要素在 `/situation/map` `factorItems` `active=true` 且进 `regions[].layerKeys`，前端 `effectiveFactorKeys` 含 `service`，本卡页面可达（默认 5 类卡） | `influence-v1` | `M_SVC_ORG_TECH_SCORE` 算法服务 + 服务机构数据源（CMS `v_cms_svc`）双到位 | 删 `influenceCard` 的 service 分支与 `SERVICE_ITEMS` | `INFLUENCE-FIX-L01` |

## 检索方式（走查 / 去 mock 时用）

- 后端：`grep -rn "SituationMockProvider\|MOCK_VERSION" lumen-svc-platform/gkxlumen-display/src`
- 前端：`grep -rn "MockBadge\|\.mock-badge" lumen-ui-science-pc/src`
- 契约：接口响应里出现 `mock: true` 即为 mock 点位（`source="mock"` 为真源标记）

## 待登记（后续页面）

- 其它页面若引入代码层 mock，按本表头追加一行，并在 handoff 里引用本台账；未登记不得合入。

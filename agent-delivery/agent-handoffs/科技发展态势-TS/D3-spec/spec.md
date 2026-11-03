# SITUATION-ENT-D3-L01 · 规格说明（期刊 / 会议代码层 mock）

> 任务：`SITUATION-ENT-D3-L01`（WBS-05-18-10）+ 台账 `SITUATION-ENT-MOCK-LEDGER-L01`（WBS-05-18-11）
> 监管人：`human:李伟`　执行：api-agent　状态：待批准（规格阶段）
> 依据：`SITUATION-ENT-D-维度打通任务单草案.md` §3-D3 / §3-台账 / §5 D-B；`AGENTS.md` D9 契约；`ADS_SCHEMA.md` 6.30.0 §24.10
> 人工验收闸门：完工**不 commit / 不 push**，改动停本地等走查。

---

## 1. 已核实事实（决定实现边界）

| 事实 | 证据 |
|---|---|
| 期刊 / 会议真无源 | `ADS_SCHEMA.md` §24.10 明列缺失；`ads_venue_profile` / `ads_conference_profile` / `ads_journal_profile` 三表不存在；`ads_talent_research_achievement` 902,667 行 `COUNT(DISTINCT venue)=0` |
| 我方数据源已诚实声明无源 | `gkx_show_service/views/geo_indicator.py` 的 `UNSUPPORTED_FACTORS` 已含 `journal` / `meeting`（`no_source`） |
| py 服务禁止 mock 回填 | `monitor_indicator.py` 头部设计约束：「全链路真实……久新缺数一律出空态 + emptyReason，**不用 mock 回填**」 |
| 页面契约在 display 层装配 | `SituationController` 的 `FACTORS`（11 要素）、`buildFactorItems`、`buildStats`、`buildFactorCards`、`buildRegions` 全在 display |
| 前端要素可用性由 `regions[].layerKeys` 推导 | `situationModel.ts#getAvailableFactorKeys`；不可用要素会被提示「暂无数据」 |
| 前端要素数量展示面 | 总览右侧要素卡（`OverviewTab.vue` 第 501 行 `item.displayValue ?? item.value`），筛选栏下拉只显示名称不显示数量 |
| 评审层唯一开关 | `src/review/feature.ts` `REVIEW_FEATURE.enabled`（当前 `true` = 走查态）；关闭后角标不进 DOM |

## 2. 关键决策

1. **落仓 = `lumen-svc-platform`（display 层 Provider），不改 `lumen-topic-py`。**
   理由：py 是数据源层，已把 journal/meeting 声明为 `no_source`，在其中返 mock 会破坏该层「缺数不造」的诚实约束；display 是页面契约装配层，journal/meeting 也只是页面要素，不是久新表。后续接真数时，只需把 Provider 换成真实 Feign 调用，py 层无需回滚。
2. **mock 集中单一模块**：新增 `SituationMockProvider`，业务组件内零散常量一律不落。
3. **可见数据面**：`/map` 要素 chips（`factorItems`）+ `/overview` 要素卡（`stats` / `factorCards`）。`/map` 的 `regions[].layerKeys` 追加 journal/meeting（**只标记存在、不编造城市数值**），保证可参与筛选/图例，不触发「暂无数据」提示。
4. **不做**：`/compare` 年度曲线、`/influence` 排名、导出数据、CMS 服务机构、专利；也不给任何城市编造 journal/meeting 计数。
5. **mock 值冻结自 demo 种子**，确定性、无随机：
   | key | 名称 | 单位 | count | 出处 |
   |---|---|---|---|---|
   | `meeting` | 会议 | 场 | `1280` | `demo-ui-science/src/data.js` factorItems（2026-11-01 快照） |
   | `journal` | 期刊 | 种 | `7200` | 同上 |
   `source="mock"`、`mockReason="数仓文档 §24.10 列为缺失：顶级会议/期刊名单未接入"`、`mockVersion="d3-v1"`。

## 3. 后端改动（repo: lumen-svc-platform）

### 3.1 新增 `gkxlumen-display/.../display/support/SituationMockProvider.java`

Spring `@Component`，唯一 mock 出口，暴露：

```java
public static final String SOURCE = "mock";
public static final String MOCK_REASON = "数仓文档 §24.10 列为缺失：顶级会议/期刊名单未接入";
public static final String MOCK_VERSION = "d3-v1";

boolean supports(String factorKey);           // journal / meeting
Long countOf(String factorKey);               // 7200 / 1280，其它 null
String unitOf(String factorKey);              // 种 / 场
Map<String,Object> metadata(String factorKey); // {mock:true, mockReason, mockVersion}
boolean inScope(List<String> enabledFactors, String factorKey); // 空=不限，否则包含
```

### 3.2 改 `SituationController.java`

- 注入 `private final SituationMockProvider mockProvider;`（`@RequiredArgsConstructor` 已存在）。
- `buildFactorItems(...)` 增加 `SituationMockProvider` 入参；在 11 要素循环后，对 `journal` / `meeting` 覆盖：
  `active=true`、`count=countOf`、`source="mock"`、并 put `mock=true` / `mockReason` / `mockVersion`。
- `buildStats(...)` / `buildFactorCards(...)` 增加 provider 入参，在现有 6 项后追加：
  - stat：`journal_total`（期刊/种）、`meeting_total`（会议/场）
  - card：同 key，`available=true`、`color` 取 `colorOf`、并带 `mock/mockReason/mockVersion`
  - 顺序放在 `institution` 卡之后，不改变既有卡顺序。
- `buildRegions(...)` 增加 provider 入参：
  - `layerOrder` 在真实要素之后追加当前范围内（`inScope`）的 mock 要素；
  - 构建 `layers` 时：真实值命中照旧进 `metrics`；mock 要素只进 `layers`、**不进 `metrics`**（不编造城市数值）；
  - `heatKey` 只从「有数值的图层」中选（企业开启时仍是 enterprise），避免 mock key 当热力基准导致全城低热；无任何数值时沿用现有默认分档逻辑。
- 类头注释同步：期刊/会议标注「代码层 mock（SituationMockProvider，d3-v1）」，与 D-D 修正后的注释口径一致。

### 3.3 契约新增字段（向后兼容）

- `map.factorItems[]` 增加可选：`mock?: true`、`mockReason`、`mockVersion`（`source` 固定 `"mock"`）。
- `overview.stats[]` / `overview.factorCards[]` 增加同名字段。
- 真实要素不带这些字段（不伪标）。

## 4. 前端改动（repo: lumen-ui-science-pc）

1. `src/types/situation.ts`
   - `FactorItem` 增加可选 `mock?: boolean`、`mockReason?: string`、`mockVersion?: string`。
   - `OverviewStat` / `OverviewFactorCard` 增加同组可选字段（仅为读 `mock` 用，不改变既有必填）。
2. 新增 `src/review/MockBadge.vue`
   - 根部 `v-if="isReviewFeatureEnabled()"`（DOM 零泄漏，非 CSS 隐藏）；
   - Arco `Tooltip` + `IconExperiment`，颜色 `#7C3AED`，图标-only 紧凑样式，`class="mock-badge"`；
   - props：`reason?: string`、`version?: string`；Tooltip 文案含 reason + `mock_version`；
   - **不出现「示例/演示/模拟」等业务文案**，只做评审角标。
3. `src/review/index.ts` 追加 `export { default as MockBadge } from './MockBadge.vue'`。
4. `src/views/situation/overview/components/OverviewTab.vue`
   - 卡值处（第 501 行附近）改为值 + `<MockBadge v-if="item.mock" :reason="item.mockReason" :version="item.mockVersion" />`；
   - 不改其他布局/样式。
5. `src/review/README.md`
   - 「包含什么」表加 `MockBadge`；「上线清理清单」加 `.mock-badge` / `MockBadge` 检索项与删除说明。
6. **禁止**改动 `views/situation/**` 其他文件、`styles/*.css`；禁止把 mock 常量散落到业务组件。

## 5. 明确不做 / 不得做

- 不写任何数据库、不改数据源、不在 py 落 mock。
- 不把 mock 计数写进 `regions[].metrics`（不给城市编造数值）。
- 不把 mock 值用于排名、计分、对比曲线、导出。
- 非评审模式（`REVIEW_FEATURE.enabled=false`）页面不得出现「mock / 示例 / 演示」字样或角标节点。
- 不把 Top-N 或 mock 值当真实统计口径对外声明。

## 6. 验证清单（必须逐项有证据）

| # | 验证 | 通过标准 |
|---|---|---|
| V1 | display 编译 | `mvn -o -q -DskipTests compile` 退出码 0 |
| V2 | `/display/v1/situation/map`（body `{"enabledFactorKeys":["journal","meeting"]}`） | journal=`7200`/meeting=`1280`，`active=true`，`source="mock"`，`mock=true`；`regions[]` 的 `layerKeys` 含 journal/meeting 且 `metrics` **无**这两个键 |
| V3 | `/display/v1/situation/overview` | `stats`/`factorCards` 含 `期刊 7,200 种`、`会议 1,280 场`，字段带 `mock=true` |
| V4 | 真实要素未受影响 | paper/patent/scholar/project/institution/topic/result 的 `source` 不变、无 `mock` 字段 |
| V5 | 前端类型门 | `pnpm type-check` 退出码 0 |
| V6 | 前端构建 | `pnpm build` 成功 |
| V7 | 页面实跑（:3000） | 要素卡出现期刊/会议两个数；评审角标仅在对应数字旁；无「mock/示例/演示」业务字样 |
| V8 | 评审关闭零泄漏 | 临时把 `REVIEW_FEATURE.enabled` 置 `false`，页面无 `.mock-badge` 节点、无 mock 字样；验证后恢复 `true`（走查态） |
| V9 | 台账 / handoff | `mock-ledger.md` 首条登记 + `SITUATION-ENT-D3-L01.md` 含 ponytail + cost 四字段 |

## 7. 交付物

- 代码：上述后端 2 个文件、前端 5 个文件。
- 文档：`agent-handoffs/科技发展态势-TS/mock-ledger.md`（新建，跨页台账表头 + 首条 D3 登记）、`.../SITUATION-ENT-D3-L01.md`（handoff）。
- 治理：`task-registry.yaml` 两单状态与 repo 回写、`WBS.md` 第 175/176 行回写。
- **不 commit / 不 push。**

## 8. 回滚方式

- 代码：删除 `SituationMockProvider.java`，还原 `SituationController` 对应行、前端 5 处；或把 Provider 的 `supports()` 返回 `false` 即可整体停用 mock（无需改契约）。
- 文档：台账保留「已停用」记录，不删除历史（便于追溯）。

## 9. 需要批准的决策点

1. mock 落 **display 层**而非 py（§2-1）。
2. mock 值 7200 / 1280 取自 demo 冻结种子（§2-5）。
3. `/map regions.layerKeys` 追加 journal/meeting 但**不给城市数值**（§3.2）。
4. `/compare` / 排名 / 导出**不接 mock**（§5）。
5. 前端新增 `MockBadge`（评审层集中管理）并挂总览要素卡。

批准后按 `tasks.md` 逐项执行。

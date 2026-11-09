# SITUATION-IM · API 契约 01（三个创新监测页面 · 只读打通）

> **状态**：`provisional` · **版本**：`v0.3` · **日期**：2026-10-28 · **监管人**：`human:李伟`
> **v0.3 变更（2026-10-28，灌数后实测）**：① 新增 **§4.7 数据真源与换算规则**（`sub_scores` 真实键名、`city_code` 双形态归一、`stat_period` 为 `YYYY-MM`、地域粒度只到市本级）；② 新增 **COLLATE 纪律**（`ERROR 1267` 修复裁定：SQL 层显式 `COLLATE`，禁止 `ALTER TABLE`）；③ 登记数据性质 `source=benchmark_manual_pack` → **D4=mock** 依据。
> **v0.2 变更（2026-10-28）**：`human:李伟` 批准「innov 侧新增 `/internal/*` 只读端点」（A0 §4.3 升级请求）→ 新增 **§4.6 innov 侧 /internal/* 清单**；§8 Open Item 1 由「待批」转「已批准」。
> **上位**：`SITUATION-IM-三个创新监测页面整体打通-跑任务提示词.md`（裁定 U1–U12）
> **参考**：`SITUATION-ENT-API-CONTRACT-01.md`（结构与 bump 纪律同构）· `API-TS-M4.md` / `API-TS-M5.md` / `API-TS-M6.md`（草案，命名取它、粒度/方法以本文件为准）
> **原则**：**前端结构为准** —— 字段级以 `lumen-ui-science-pc/src/types/{situation,bayArea,shenzhenInnovation}.ts` 现有 Dataset 字段为真源，本契约只定**端点 / 入参 / 信封 / 偏离**，不重复抄字段清单。

---

## 1. 范围与裁定

| 项 | 结论 |
|---|---|
| 链路（U1） | 前端 → `/display/**` → `gkxlumen-display`（Feign）→ `gkxlumen-element` / **`gkxlumen-innov`**（U3 启用）。**禁止前端直连 `/innov/**`** |
| 命名（U2） | 采用草案前缀：`global-innovation` / `bay-innovation` / `shenzhen-innovation` |
| 粒度（U2） | **区块端点**：按数据块切，**共 15 个只读端点**（M4 5 + M5 5 + M6 5；不是三份整包 dataset，也不是草案的全部细端点） |
| 方法（U2） | **统一 POST**（草案里 GET 的端点一律改 POST，见 §5 偏离表） |
| 写面（U5） | **本次不实现**，`deferred`，见 §6 |
| **真源地位（C4=①）** | `human:李伟` 2026-10-28 裁定：本契约是 **M4/M5/M6 本期施工真源**；`BE-TS-CONTRACT-02`（WBS-05-15）批 3 会签时由监管人把 §5《偏离表》回灌 `API-TS-M4/M5/M6.md`。**双真源期间以本契约为准**，发现冲突按本契约执行并在 handoff 记账 |
| **innov 新增端点（U13）** | `human:李伟` 2026-10-28 批准：允许在 `gkxlumen-innov` 侧**新增 `/internal/*` 只读端点**补齐 A0 §4.1 的 7 项缺失能力。**纪律**：逐叶按需新增、不批量造；新增端点一律 `@Inner(true)`，display 侧 `@NoToken` 与之配对；**列不存在时如实空态 + `emptyReason`，禁止伪造数值**。明细 §4.6 |
| 服务内前缀 | `/v1/situation/**`；网关对外 `/display/v1/situation/**`（axios baseURL 已含 `/api`） |
| 就绪度（U6–U9） | 每块响应体带 `metric_id`；前端查 INNOV 只读镜像渲染角标，**禁止前端硬编码状态** |

## 2. 通用入参（所有端点一致）

```jsonc
{
  "regionPaths": [["guangdong","shenzhen","nanshan"]], // 地域级联，string[][]；重要过滤维度
  "activeRegionKey": "shenzhen",                        // 地图点选/关键词候选；scopeOf 优先读 regionPaths，再退回本字段
  "searchTerm": "",                                     // 名称模糊
  "timeRange": { "startYear": 2016, "endYear": 2026 },  // 注册年 / 统计年区间，按各端点口径
  "domains": [],                                        // 学科领域多选；空 = 全部
  "types": [],                                          // 类型多选（载体/指标/要素），空 = 全部
  "page": 1, "size": 20                                 // 可选；不需要分页的端点忽略
}
```

- **入参翻译唯一层**：`scopeOf(params)`。凡是涉及地域的端点**必须**走 `scopeOf`，禁止各端点自己解析（历史坑：各认一半入参导致 KPI 不动，见 `SituationController.java:310-324`）。
- 未知字段忽略，不报错；缺失字段按「全域」处理。

## 3. 通用出参信封

```jsonc
{
  "code": 0, "msg": "ok",
  "data": {
    // ↓ 端点专属字段（见 §4）
    "emptyReason": null,      // null=有数据；否则为枚举：NO_DATA / UNREACHABLE / NOT_READY
    "scopeLabel": "深圳市 / 南山区",  // scopeLabelOf(scope)：实际生效范围，便于排障与页面标注
    "asOf": "2026-10-28",     // 数据截止
    "metricIds": ["M_INNOV_ACHIEVE_VALUE"]  // 本块统计数字对应的 metric_id（可能多值）
  }
}
```

- **分区降级**：下游挂 → 仍 HTTP 200，字段保持结构完整但为空 + `emptyReason=UNREACHABLE`，不 5xx。
- **逐块兜**：一个数据块对应一个端点；某块失败**不得**波及其它块（前端用 `Promise.allSettled` 装配）。
- **数值序列化**：所有数值字段强制 `int` / `double`（防 Jackson 把 Long 转 String 导致 ECharts 画不出曲线）。
- **诚实性**：无源数字一律不出或显式空态，禁止以其它信号冒充。

## 4. 端点清单（15 个只读）

| # | 服务内路径（POST） | 承载（→ 前端 Dataset 字段） | 主要数据源 | 状态 |
|---|---|---|---|---|
| 1 | `/v1/situation/global-innovation/achievements` | `innovations`（成果列表 + 地图落点；detail / realtime 共用） | innov 成果表 + enterprise | 待实装 |
| 2 | `/v1/situation/global-innovation/realtime` | 实时 KPI + 趋势 + 领域分布 | innov + enterprise_domain_dist | 待实装 |
| 3 | `/v1/situation/global-innovation/carriers` | `carriers`（ranking + detail 的载体） | innov 载体 + enterprise_score | 待实装 |
| 4 | `/v1/situation/global-innovation/alerts` | `alerts`（monitor） | innov | 待实装 |
| 5 | `/v1/situation/global-innovation/cities` | `cities`（10/11 城五维 + 政策建议） | innov + algorithm | 待实装 |
| 6 | `/v1/situation/bay-innovation/achievements` | `points`（湾区 11 城成果点） | innov | 待实装 |
| 7 | `/v1/situation/bay-innovation/capability` | `capacities`（四维 + 历史 + 构成） | innov + algorithm | 待实装 |
| 8 | `/v1/situation/bay-innovation/swot` | `swotData`（四象限 + 因素） | algorithm | 待实装 |
| 9 | `/v1/situation/bay-innovation/indicators` | `indicators`（6 指标 + 11 城构成 + 口径） | algorithm + innov | 待实装 |
| 10 | `/v1/situation/bay-innovation/alerts` | `alerts`（预警中心） | innov | 待实装 |
| 11 | `/v1/situation/shenzhen-innovation/carriers` | `carriers` | innov + enterprise | 待实装 |
| 12 | `/v1/situation/shenzhen-innovation/indicator-systems` | `indicators`（10 系三级 + 构成 + 历史） | algorithm | 待实装 |
| 13 | `/v1/situation/shenzhen-innovation/field-distribution` | `domains`（8 领域 × 4 指标 + 空间集聚） | innov + enterprise_domain_dist | 待实装 |
| 14 | `/v1/situation/shenzhen-innovation/city-benchmark` | `compareCities`（8 城四维 + 缺口 + 外推） | algorithm | 待实装 |
| 15 | `/v1/situation/shenzhen-innovation/operation-timeline` | 运行监测时间轴 | innov（数据侧维护） | 待实装 |

> 说明：M4 的 `realtime` 与 `detail` 共用 `innovations` 的不同投影，因此按**数据块**切是 5 个而不是按 Tab 的 5 个（两者恰好相等；若后续 Tab 复用关系变化，以数据块为准）。

**每个端点实现时必须写「哪些入参真的生效」的诚实声明注释**（照 `SituationController.java:310-324`），例如某维度因主表无对应列不参与过滤，必须明示。

### 4.6 innov 侧新增 `/internal/*` 清单（**已批准 · U13**）

> **背景**：A0 体检（`agent-handoffs/科技发展态势-IM/SITUATION-IM-A0-L01.md` §4.1）查出 7 项能力在 `gkxlumen-innov` 不存在。
> **批准**：`human:李伟` 2026-10-28 批准新增 `gkxlumen-innov` 侧 `/internal/*` 只读端点（U13）。
> **统一纪律**：① 一律 `@Inner(true)`，display 侧 `@NoToken` 与之配对（照 element 同款写法）；② **逐叶按需新增，禁止一次性批量造 7 个**；③ 源列不存在时如实空态 + `emptyReason`，**禁止伪造数值**（= C3=①）；④ 每新增一个端点必须同步 bump 本节与本文件版本。

| # | 候选端点（草案） | 补齐能力 | 首用叶 | 状态 |
|---|---|---|---|---|
| 1 | `POST /internal/innov/v1/shenzhen/carriers` | 深圳载体 + 行政区层级 + `talents`/`rdInvestment` | **C1（pilot 首叶）** | 待实装 |
| 2 | `POST /internal/innov/v1/shenzhen/domains` | 领域四维分布（企业数/专利/研发投入/人才） | C3 | 待实装 |
| 3 | `POST /internal/innov/v1/cities/benchmark` | 城市对标（8 城四维 + 缺口外推包装） | C4 | 待实装 |
| 4 | `POST /internal/innov/v1/achievements/*` | 创新成果聚合（按城市/区域） | C6 / C11 | 待实装 |
| 5 | `POST /internal/innov/v1/indicator-systems/*` | 指标树 + 城市×指标序列 + provenance | C2 / C9 | 待实装（依赖算法侧，按 C3=①） |
| 6 | `POST /internal/innov/v1/alerts`、`/subscriptions` | alerts 列表读 + 订阅规则（**写面仍 deferred**） | C10 / C14 | 待实装 |
| 7 | `POST /internal/innov/v1/relations/flyline` | 关联飞线 / 传播路径 | C6 | 待实装 |

> ⚠️ **澄清**：display → innov 走 **Feign 不经网关**，因此 innov 现有 34 个 REST 端点**无需改 `@Inner`**；本节的 `@Inner(true)` 只针对**新增**端点（照 `gkxlumen-element` 现有 internal 端点的写法惯例）。

### 4.7 数据真源与换算规则（**灌数后实测 · 2026-10-28**）

> 来源：`agent-handoffs/科技发展态势-IM/SITUATION-IM-A0-L01.md` §1.2。
> **所有 C 段端点实现必须遵守**；违反第 5 条会直接 `ERROR 1267`，违反第 6 条等于伪造数据口径。

| # | 规则 | 说明 |
|---|---|---|
| 1 | **`sub_scores` 键名分两套，不可混用** | 载体（carrier）：`output / quality / activity / performance`；城市（city）：`output / resource / environment / institution`。**城市四维是 `institution` 而非草案里的 `mechanism`**，禁止按草案旧名拆 key。 |
| 2 | **`city_code` 必须归一** | 实测双形态并存（`CN-4403` 与 `CN4403`；国际城 `GB-LON` 与 `GBLON`）。`city_index` 主键是 `city_code`（**不是 `city_id`**）。归一失败时返回空态，不得用另一个城市的数据填充。 |
| 3 | **`stat_period` 是 `varchar(7)` 的 `YYYY-MM`** | 不是年份。跨期比较按年月处理；不得当整数比较。现存 5 期：`2022-12` ~ `2026-06`。 |
| 4 | **地域粒度只到市本级** | 深圳载体的 `admin_code` 全部为 `440300`；`dim_admin_division` 无区级数据。传入区级码时应返回**空列表 + `emptyReason`**，不得谎称支持区级筛选。 |
| 5 | **COLLATE 必须显式书写** | `ads.carrier_index`(utf8mb4_0900_ai_ci) 与 `dim.carrier`(utf8mb4_general_ci) 排序规则不同，直接 JOIN 抛 `ERROR 1267`。新端点一律写：`i.carrier_id COLLATE utf8mb4_general_ci = c.carrier_id`。**禁止用 `ALTER TABLE` 解决**（属结构变更，须按总控 §0.1 第 4 条单独升级）。裁定：`human:李伟` 2026-10-28 方案 A。 |
| 6 | **数据性质 D4=mock，必须标注** | `city_index.indicator_values.source = benchmark_manual_pack`（人工基准包，由 `innovPy` P1–P9 批处理灌入），非真实数仓实算。评审层按 mock 标注，**不得以「实算」口径呈现**。 |

**城市覆盖（实测 73 城）**：`CN-4403`（深圳）/ `CN-4401`（广州）/ `CN-4419`（东莞）均在 `city_index` 内
→ 原判定为空态的 **M6 `CompareTab`** 与湾区相关能力，**转为有源**。

## 5. 偏离表（相对草案 `API-TS-M4/M5/M6`）

| 草案 | 本契约 | 理由 |
|---|---|---|
| `/global-innovation/realtime`（GET） | POST | 统一 POST，对齐 M1 同构写法（`api/situation/index.ts` `const post = ...`） |
| `/bay-innovation/capability` `swot` `indicators`（GET） | POST | 同上 |
| `/shenzhen-innovation/indicator-systems` `field-distribution` `city-benchmark` `operation-timeline`（GET） | POST | 同上 |
| 草案里的粒度合并为一个 `dataset` | 按数据块拆分 | 支持分区降级与增量交付（U2）。详见提示词 §2.3 |
| 草案含 `carriers/{carrier_id}` 详情端点 | deferred | U5：本次不实现；Tab 当前消费列表即可 |
| 草案含 `alerts/{id}/read`、`push-records`、`monitor/subscriptions` | deferred | U5：写面需真 token 与 app_user 家族，本地 permitAll 无法验证用户隔离 |

## 6. Deferred（本次不实现，保留条目）

| 端点 | 方法 | 依赖 |
|---|---|---|
| `/global-innovation/alerts/{alert_id}/read` | POST | 写面 + 用户隔离（app_user 家族） |
| `/global-innovation/push-records`（列表） | GET | 同上 |
| `/global-innovation/push-records/{record_id}/read` | POST | 同上 |
| `/global-innovation/monitor/subscriptions` | GET / PUT | 同上 |
| `/global-innovation/carriers/{carrier_id}` | GET | 详情形态，Tab 暂不消费 |
| `/shenzhen-innovation/carriers/{carrier_id}` | GET | 同上 |

## 7. 实装对照表（每叶完工回填一行）

| 任务 ID | 端点 | 版本 | 实测行数/样本 | 空态原因 | 回填日期 |
|---|---|---|---|---|---|
| — | — | — | — | — | — |

## 8. Open Items（开工后 A0 定）

> **2026-10-28 A0 已定性**（`agent-handoffs/科技发展态势-IM/SITUATION-IM-A0-L01.md`）：第 1、2、4 条已关闭，第 3 条仍待 pilot。

1. ✅ **已定性 + 已批准（2026-10-28 `human:李伟`，U13）** —— 需 innov 新增 `/internal/*` 补齐 7 项缺失能力（成果聚合 / 指标树+城市×指标序列+provenance / 领域四维 / alerts+订阅 / SWOT 全套 / 关联飞线 / 结论生成）。**逐个端点清单见 §4.6**；纪律：逐叶按需、不批量造、`@Inner(true)` + display 侧 `@NoToken` 配对、无源列如实空态。此前标注的 `blocked` 状态**已解除**，受影响 C 叶恢复正常排队。
   - 缺失七项：创新成果聚合 / 指标树+城市×指标序列+provenance / 领域四维分布 / alerts+订阅 / SWOT 全套 / 关联飞线 / 结论生成。
   - ⚠️ **澄清**：display → innov 走 **Feign 不经网关**，因此**现有端点无需改 `@Inner`**；新增的 `/internal/*` 建议加 `@Inner(true)`（照 element 同款写法）。
2. ✅ **已产出** —— 见 A0 报告 §6：三页对齐约 **55 条** metric_id（按验收单元分组列表）；映射不上的点位（`IndicatorTab` / `IndicatorsTab` 全 Tab、监测/订阅类）按 **D1 missing 红问号**，禁止伪 8 件套。
3. ⏳ **仍待 pilot** —— M4 `realtime` 的 D2 轮询语义（草案首版 30s）是否本次实现，待 M6 pilot 跑通后定（勾选表 C5=①）。
4. ✅ **已定性** —— 算法侧未就位：SWOT、指标体系、指标 provenance 无算法服务。处置按 **C3=①**：空态 + `emptyReason` + 端点 Javadoc 写明口径，**不得默默按 demo 数值返回**；有源的是城市 `sub_scores` / `indicator_values`（`ads_city_index` JSON 列，可直接读）。

## 9. 变更纪律

改契约 → **先 bump 本文件版本** → 再同步 `types/*.ts` 与 mock 种子（`defineApi` 双轨两侧对齐），**禁止两处漂移**。每份叶 handoff 必须回写 §7 一行。

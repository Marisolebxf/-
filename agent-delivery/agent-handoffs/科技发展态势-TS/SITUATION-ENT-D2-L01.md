# SITUATION-ENT-D2-L01 · 非企业要素落点分档打通（市域色阶 + 机构榜单）

> **任务**：科技全域态势·非企业要素落点——论文 / 人才 / 项目 / 机构 / 课题 / 成果走市域色阶，机构出榜单；机构不做对象级点位（实测久新坐标=城市质心）；顺带修 `SituationController` 5 处失真注释
> **角色**：`agent:api-agent` · 监管人：`human:李伟`
> **状态**：`backlog → in_progress → integration`（改动停本地，**未 commit / 未 push**，待人工验收）
> **上位**：[SITUATION-ENT-D-维度打通任务单草案 v4](./SITUATION-ENT-D-维度打通任务单草案.md) §3-D2 · §1.1 / §1.2 · §5 D-A / D-B / D-C / D-D
> **挂接**：WBS §4.3（WBS-05-18-09） · 2026-11-01

---

## 一、交付内容（git 改动面 = 4 文件；前端零改动）

| 仓 | 文件 | 改动 | 说明 |
|---|---|---|---|
| `lumen-topic-py` | `gkx_show_service/views/geo_indicator.py`（未跟踪新文件） | 新增 `POST /internal/gkx-show/geo/factor-metrics` | 久新「要素 → 市域聚合」唯一入口：`scope=gba` / `level=CITY` / `cities` / `factors`；出 `items`（每城 `metrics` 包）+ `missing` + `unsupported` + `notes` |
| `lumen-topic-py` | `gkx_show_service/views/monitor_indicator.py`（未跟踪新文件） | `/monitor/carrier-list` 增 `cities` 过滤 | 展示系统「深圳市」→ 久新 `city_name`「深圳」归一（`strip()` + `rstrip("市")`）；并补注释：机构经纬度为城市质心，不可作点位 |
| `lumen-svc-platform` | `gkxlumen-display/.../feign/RemoteShowPythonClient.java`（未跟踪新文件） | 新增 Feign `geoFactorMetrics` | `@NoToken`；Javadoc 明示「只出市域聚合、不做对象级点位」 |
| `lumen-svc-platform` | `gkxlumen-display/.../controller/SituationController.java`（修改） | `/map` 重写 + 5 处注释修正 | 见 §三 / §五；`/overview`、`/compare`、`/cluster`、`/influence`、`/timeline`、`/events` **逻辑未动** |

**`lumen-ui-science-pc` 零改动**：本任务全程只读该仓（未编辑任何文件）。仓内现存未提交改动来自其它任务，与本单无关。
本次未改 UI 展示效果：`regions` 结构不变（仍为 `MapRegion[]`），仅在 `layerKeys` / `metrics` 里按勾选要素增列；额外字段为新增，前端不消费也无副作用。

## 二、探底结论（A 段，久新实库实测）

| 事实 | 证据 |
|---|---|
| `ads_geo_yearly_metrics` 只有 `paper_count` / `project_count` / `talent_count` / `institution_count` | 31 列全量核对（`SELECT * LIMIT 1`）；**无 `patent_count`** |
| `ads_patent_profile` 无地域列；`ads_institution_patent` 是「机构代表专利 Top20」抽样 | 抽样表不足以构成市域色阶 → 专利不上色阶（不造数） |
| `ads_location.name_zh` 用简称（深圳 / 广州），`location_level` 可 CITY | 与 element / 展示系统「深圳市」口径不一致 → 双向归一 |
| `ads_institution_profile` 有 `lat/lng` 但为城市质心 | 深圳 129 家（有坐标）去重后**仅 1 个坐标** → 机构不做点位（D-A 裁定） |
| `ads_institution_profile.city_name` 存「深圳」而非「深圳市」 | 旧 `inGba("深圳市")` 会过滤掉全部机构——伪点位本就无效 |
| `ads_research_problem_region_yearly_metrics` 有 `problem_id` / `location_id` / `location_level` / `statistics_year` 及各计数 | 课题可按市域、按年聚合（按 `problem_id` 去重） |
| `ads_research_outcome_institution` 有 `city_location_id`，**无年份列** | 1,220 行 / MVP 342 条（按 `outcome_id` 去重）；成果计数**不按年** |
| `ads_venue_profile` 等三表不存在 | 期刊 / 会议真无源（`ADS_SCHEMA.md` §24.10） |

## 三、实现口径（分档 / 降级 / 诚实性）

**落点能力分档（与草案 §0-2 一致）**：

| 要素 | 落点能力 | 本单实现 |
|---|---|---|
| `enterprise` | **对象级点位**（全要素里唯一） | 维持 element 点位；`regions` 保留企业计数 |
| `paper` / `scholar` / `project` / `institution` | 市域色阶 | 久新 `ads_geo_yearly_metrics` SUM 四列（按最新完整年） |
| `topic` | 市域色阶 | `problem_id` 去重计数（按年） |
| `result` | 市域色阶 | `outcome_id` 去重计数（**不按年**，notes 如实声明） |
| `institution`（补充） | 榜单（非点位） | `carrier-list` 按 `cited_by_count` 排序 Top20 → `institutionRanking` |
| `patent` | 仅全局 KPI | `unsupportedFactors` + `notes` 说明「无市域计数源」 |
| `service` | CMS `v_cms_svc` | 本单不上市域色阶（久新无表，CMS 另有通道） |
| `journal` / `meeting` | 真无源 | 留空（D3 `SITUATION-ENT-D3-L01` 另单 mock） |

**取值与联动规则**：

- 年份：`max(statistics_year) - 1`（避开未完整收尾的当年；本次实测 year=2025，`as_of=2026-09-18`）；
- `enabledFactorKeys` **空 = 不限**（全部有源要素在范围内）；非空 = 只算勾选交集；勾选里无久新可支持要素 → **不调久新**（不浪费查询，也不出假数）；
- `regions.layerKeys` 随勾选联动（企业优先、其余按 `paper→scholar→project→institution→topic→result` 顺序），且 chips 与 `layerKeys` 一致（`topic` / `result` 用湾区累加值点亮 chips，避免「卡无计数、地图有数」）；
- 热力基准：企业开启时沿用企业数（原行为不变），否则用首个久新要素；
- 城市 key 统一 element 口径（「深圳市」），久新「深圳」补后缀；无坐标城市不上图（不落 0,0）；全要素无值的城市不出空区域；
- **缺数一律 `null`**（不补 0）；`missing` 区分 `no_source`（无源）与 `no_data`（有实体无值）；
- 降级：久新不可达 → `regions` 仍由 element 出数、`institutionRanking` 为空、`notes` 不出现（不报错、不白屏）；
- **`objectPoints` 只保留企业点位**：机构伪点位已按 D-A 裁定删除（不拿城市质心冒充 129 家机构）。

## 四、验证结果

| 项 | 命令 / 方法 | 结果 |
|---|---|---|
| py 语法 | `python -m py_compile geo_indicator.py monitor_indicator.py` | ✅ `py_compile OK` |
| 市域聚合（实库） | 直调 `factor_metrics({scope:gba, level:CITY, cities:9市})` | ✅ `count=8` · `year=2025` · `as_of=2026-09-18`；`unsupported=[]`；`missing=香港/澳门(no_source) + 中山(no_data)` |
| 专利降级 | `factors:["patent"]` | ✅ `count=0`，`unsupported=[{factor:"patent", empty_reason:"no_source", detail:…}]`，**未发查询** |
| 机构榜单（实库） | 直调 `carrier_list({cities:9市, limit:20, sort_by:"cited_by_count"})` | ✅ `count=20`；榜首 深圳大学 21,482 篇 / 491,794 被引 → 南科大 17,213 / 375,952 → 中科院深圳先进院 7,263 / 196,602 |
| Java 编译 | `mvn -o -q -pl gkxlumen-display -am -DskipTests compile`（JDK 17） | ✅ exit 0；`SituationController.class` / `RemoteShowPythonClient.class` 均于 2026-11-01 15:20 重新产出 |
| 打包 + 重启 | `mvn -o -pl gkxlumen-display -am -DskipTests package` → `java -jar`；py 重启 uvicorn | ✅ `BUILD SUCCESS`（1m19s）；py `/healthz` = `jiuxin_readonly_channel: up`；display `:7099` 10s 内监听 |
| 新端点 HTTP 自检 | `POST :8082/internal/gkx-show/geo/factor-metrics` | ✅ 路由已注册；`count=8` / `year=2025` / `as_of=2026-09-18` |
| `/map` 勾选组合 | `enabledFactorKeys` = `[]` / `["paper","scholar"]` / `["institution"]` / `["patent"]` | ✅ 默认 9 区域（`enterprise,paper,…`）；双要素 8 区域（`paper,scholar` 双图层）；机构 8 区域单图层 + 榜单 20 条；专利 0 区域 + notes 含「专利无市域计数源」 |
| 页面实跑 | `http://127.0.0.1:3000/trend/tech-overall-situation`（mock 登录） | ✅ 渲染正常、无白屏、无报错弹窗；只勾「论文」悬停深圳市气泡 = **「深圳市 · 论文 影响力 24904.0」**（24,904 = 后端 2025 论文值）；仅勾「专利」地图无城市气泡（空态）；地图上无机构点位 |

**实库返回明细（`factor_metrics`，2025 年）**：

| 城市 | paper | scholar | project | institution | topic | result |
|---|---:|---:|---:|---:|---:|---:|
| 广州 | 44,556 | 13,245 | 14,504 | 190 | 3 | 5 |
| 深圳 | 24,904 | 6,462 | 9,143 | 113 | 7 | 227 |
| 东莞 | 3,092 | 868 | 1,154 | 19 | 1 | — |
| 佛山 | 2,489 | 704 | 842 | 16 | — | — |
| 珠海 | 2,109 | 669 | 700 | 13 | — | — |
| 江门 | 515 | 157 | 156 | 6 | — | — |
| 惠州 | 493 | 162 | 178 | 3 | — | — |
| 肇庆 | 301 | 121 | 68 | 3 | — | — |

> `—` = 该年度无聚合值（JSON 里为 `null`，不是 0）。

**打包排障记录**：首次 `package` 失败于 `spring-boot-maven-plugin:repackage`——运行中的 display 进程锁住 `target/gkxlumen-display.jar`（Windows 文件锁，无法 rename 为 `.original`）。先 `Stop-Process` 再打包即成功（`BUILD SUCCESS`）。

**页面实跑遗留观察（非本单缺陷，走查时确认）**：
1. 地图城市气泡本身**只渲染圆点**（`FactorMapSection.buildMarkerHtml` 对区域点不输出 label）；市域计数体现在**悬停提示**「城市 · 要素名 影响力 N」里。其中「影响力」是前端既有文案，N 为 `regions[*].value` 的解析值（企业「N 家」、久新要素「论文 N」）。本单不改前端，故不改该标签。
2. `notes` / `institutionRanking` / `unsupportedFactors` **前端目前无消费**：所以「专利无市域计数源」只存在于接口返回，页面看不到说明；机构榜单也未上屏。若要展示须另开前端单（见 §六-6）。
3. `objectPoints` 在「只勾非企业要素」时仍返回企业点位（99 条）——D1/C4 既有行为（本单只加了湾区过滤）；默认缩放级别前端不渲染，缩放到对象级阈值才显示。是否随勾选联动需前端/产品裁定，**本单未改**（避免越界）。

**服务重启备注（后续走查可复用）**：本机 `GKX_JIUXIN_*` 在**用户级**环境变量里（`GKX_JIUXIN_ENABLED=1`），但新开的 shell 进程不继承；重启 py 前须从 User 作用域注入（`[Environment]::GetEnvironmentVariable($n,"User")` → `Set-Item env:$n`），否则久新通道回落空态（接口会返回空 `items`）。display 用 `java -jar target/gkxlumen-display.jar --spring.profiles.active=local`，打包前必须先停旧进程，否则 repackage 报「Unable to rename」。

## 五、契约变化（新增字段，前端零改动）

`/v1/situation/map` 返回新增：

| 字段 | 类型 | 说明 |
|---|---|---|
| `regions[*].layerKeys` | `string[]` | 随勾选要素联动（企业 + 久新 6 要素中该城有值者） |
| `regions[*].metrics` | `{factorKey: number}` | 市域聚合值（`null` 不写入） |
| `institutionRanking` | `array` | `rank` / `key` / `name` / `city` / `type` / `paperCount` / `citedByCount` / `talentCount` / `projectCount` / `establishedYear` |
| `unsupportedFactors` | `array`（仅非空时） | `{factor, empty_reason, detail}`，专利等无市域源要素 |
| `notes` | `string[]` | 诚实说明（机构质心 / 专利缺源 / 课题口径 / 成果口径与不按年） |

`regions[*].value` 文案：企业「N 家」，久新要素「要素中文名 N」（热力基准对应）。
已有字段（`key/label/name/level/coordinates/viewportZoom/legend/objectPoints/regionCascadeOptions`）**结构不变**；`objectPoints` 由「企业 + 机构」变为**仅企业**（机构本来就不是对象级点位）。

## 六、遗留缺口与后续建议

1. **专利无市域计数源**：`ads_geo_yearly_metrics` 无 `patent_count`、`ads_patent_profile` 无地域列、`ads_institution_patent` 仅 Top20 抽样。本页专利只出全局 KPI；若后续要求市域专利色阶，需数仓补 `patent_count` 或专利-地域桥接全量表（**建议提数仓需求，不要拿抽样表凑色阶**）。
2. **课题 2025 数据偏少**（深圳仅 7、广州 3、多数城市空）：`ads_research_problem_region_yearly_metrics` 最新完整年覆盖不均，走查时可能看到「多数城无色阶」，属数据现状而非缺陷；可在页面 notes 或走查说明里给出。
3. **成果不按年**：`ads_research_outcome_institution` 无年份列，市域成果计数是累计口径（MVP 342 条子集），不可与论文/项目的年度值横向比较。
4. **香港 / 澳门无源**、**中山无数据**：`missing` 已如实返回，不上图。
5. **服务机构（CMS `v_cms_svc`）**：本单未接市域色阶，需确认展示侧是否已有现成 CMS 聚合端点后再接。
6. **前端消费**：`institutionRanking` / `notes` / `unsupportedFactors` 目前无视图消费（本单不改 UI）。若要展示机构榜单卡，须另开前端单（走查裁定后）。

## 七、给验收人的走查前置

1. 本地服务**已由本单重启并可用**（py `:8082` = 新构建、`jiuxin_readonly_channel: up`；display `:7099` = 新 jar）——若进程被关，按 §四末「服务重启备注」重起；
2. 打开 `http://127.0.0.1:3000/trend/tech-overall-situation`（mock 任意账密登录）；
3. 勾选论文 / 人才 / 项目 / 组织机构 / 课题 / 成果后**悬停城市圆点**，观察提示「城市 · 要素名 影响力 N」中的要素名与 N（地图气泡本身只有圆点、无文字）；多要素同时勾选时 `layerKeys` 多套（气泡颜色取首个图层色）；
4. 仅勾「专利」：地图无城市色阶（空态），属预期——接口 notes 有「专利无市域计数源」，但**页面不显示 notes**（前端未消费，见 §四遗留观察 2）；
5. 期望值对照 §四表格（2025 年口径）；机构不再以点位出现。

## 八、Cost 四字段

| 字段 | 值 |
|------|-----|
| actual_tokens | ≈ 210k（估，含实库探底、端点实现、Java 重写、打包排障与浏览器实跑） |
| model_used | auto |
| actual_cost | ≈ $1.5（估） |
| cost_warn | green（<$10） |

ponytail: full（探底推翻草案「专利有市域列」假设后改为诚实降级；机构坐标经实测证伪伪点位；py 语法 / 实库直调 / Java 编译 / 打包重启 / 页面实跑五项全部真实执行，页面证据为悬停原文「深圳市 · 论文 影响力 24904.0」；页面上看不到 notes 等限制已如实记录，未以「应该能跑」替代验证）

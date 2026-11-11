# SVC-L2-ECO 创新生态服务 · 演示样本循环（LOOP）计划与 R1/R2 判定

> 依据：`产品实现规程.md` §6.5（含 §6.5.7）。用例真源：`../合规演示用例/SVC-L2-ECO-合规演示用例.md`（9 行 557–565）。
> 实现备案：`../合规演示用例/SVC-L2-ECO-实现方案-20261110.md`（S1 数据 / S2 后端 / S3 前端 / S4 部署态与浏览器复核）。
> 监管人：human:李伟。

## 状态行（每轮回写）

| 轮次 | 日期 | 探测 | 对得上 | 缺口 | 子任务 | 结论 |
|---|---|---|---|---|---|---|
| R1 | 2026-11-11 | 网关 4 端点全 200（内网 + 生产双通道） | 9 行逐行对照：**7 可演 / 2 部分可演 / 0 缺口**（G4 撤销 + 559 经需规原文核对升 ✅，见下） | 561 企业/专利/人才/结构统计表待供数（需规真项）；558 区级时序已代码闭环待 display 部署 | — | **R1 完成，可申请签收** |
| R2 | 2026-11-11 | 本地四绿（pytest 13 / test.mjs / vue-tsc / mvn compile）；**未部署**，网关仍未含新端点 | human 裁定二项落地：**A 接种子**（561「人才结构」四指标接 demo 库 `is_demo=1`，每块强制 `seeded=true`，SVC_005 无字段恒空）+ **B 加高企列**（561 下钻表 3 列→4 列，`enterprise_base.is_high_tech=1`）；另修专利趋势口径（`filing_year` 8 行 → `filing_date` 覆盖 99.99%） | 部署未发布（show-py / display manual / FE 三镜像待人工确认推送）；探针未跑部署态；人才区级列仍无粒度 | S1–S6 已闭环（S6=561 余量补口） | R2 代码完成 |
| R3 | 2026-11-11 10:14 | 部署态复核：`eco_s4_probe.py` **46/46 PASS**（含 4 项区级下钻守恒、4 项趋势、6 项人才种子）；生产 bundle `index-DfQOnxBt.js`（37KB，旧 R1 版 23KB）**R2 独有串 5/5 命中** | 558 由「代码闭环待部署」转**已部署实测**：FE `600e58a`（pipeline **#4851 五 job 全绿**，含 `deploy:k8s`）+ 智库字段修复 `df1cc43`；三仓均已生效（探针打生产网关全通） | 561 人才区级列仍无粒度（`talent_*` 无区县字段）；真实高企/专利/人才台账待供数 | 前端 `vue-tsc --build --force` 全量 0 错（增量缓存会假绿，须带 `--force`） | **R3 完成：8 可演 / 1 部分可演 / 0 缺口，可申请签收** |
| R4 | 2026-11-11 | 无新增网关探测（沿用 R3 部署态）；human 逐屏核对 5 张截图提 6 类反馈 | 口径收敛 8 项：筛选补「全部」+ 所在区改省市区三级联动、名录/详情/地图去推断与无源括注、561 下钻表移除人才列、移除 `SVC_005` 岗位层次卡、演示标注改评审模式门控、旭日图锁初始态 | 无新增设计缺口；**G6/G7 撤销**（该维度不演，非补齐），余 G8 真实台账 | FE `eebdbec` / py `deefe61` / java `e1c2002` | **R4 完成：维持 8 可演 / 1 部分可演 / 0 设计缺口** |

## 1. 探测（每轮第一笔，只读）

- `GET {网关}/display/v1/service/ecology/meta`，头 `Authorization: Bearer <本机 token>` + `systemCode: display`；配套 `overview`、`carriers`、`carrier?carrierId=`。
- 网关：内网 `http://10.50.69.111:30895`；生产 `https://edu.itic-sci.com/tid/api`（必须带 `/tid`）。token 读 `%USERPROFILE%\.gkx\display-loop-token`，不打印。
- **熔断**：401/424 → 验收单 blocked、通知 human:李伟、停止；404 → 「接口映射不存在」停止。200 才进对照。
- **性能红线**：meta/overview/carriers 均 < 1s，超 15s 记性能缺陷。

## 2. 用例集（R1 全量对照，9 行）

判定以各行「期望输出」为准；页面侧证据为生产 `https://edu.itic-sci.com/tid/service/innovation-ecology-service` 同源构建 + 本地真网关复核截图。

| 行 | 内容 | 判定要点（实测） | 结论 |
|---|---|---|---|
| 557 | 数据梳理分析页签（数据源台账） | 4 组来源：载体行真实 4,984 条（来源 stic 公示、取得 2026-11-10、映射 `demo_gkxlumenx_ads.ads_innovation_carrier`）；**R2 起高企行转真实**（`dwd.enterprise_base.is_high_tech=1`，已归区 24,317 / 全库 27,936）；**人才行转演示种子**（`dwd.talent_*` 且 `is_demo=1`，行内标「演示种子」）；专利行为明细条数并标「演示灌数」（64.8 万行仅 5 个申请日期）。仍无供数项保持「—（待供数）」，无编造数字 | ✅ 可演 |
| 558 | 载体详情基本信息 + 创新发展趋势折线 | 基本信息 7 字段齐（名称/类型/级别/分层/年度/依托单位/信用代码）+ 区与坐标带推断标注；切区域后地图只显该区点位（district 过滤联动）；**趋势随载体所在区联动已代码闭环**（新增 `/ecology/trend?district=` 区级真实序列，南山 1,118 条→28 年序列，`sum(yearSeries)+yearMissingCount=total` 守恒；抽屉带缓存，未分区/取数失败回落全库并如实标注）——show-py 已部署，**display `/trend` 已于 2026-11-11 10:14 部署生效（FE #4851 五 job 全绿），R3 部署态实测通过** | ✅ 可演（R3 部署态实测） |
| 559 | KPI + 饼图 + 折线 + 区县下钻 | KPI 六卡真实（含未分区 1909、坐标 3592）；类型饼图 10+ 类扇区和=4,984；年度折线 31 年；下钻表为「行政区/载体数/占比」3 列。**2026-11-11 human 核对需规原文**：seq 559 仅要求「创新载体/孵化载体分布、数量、流动统计 + 趋势动态更新」，现实现全部覆盖；「折线 3 条 + 下钻 6 列（企业数/专利/人才）」系用例演绎自 seq 561 主题，归还 561 | ✅ 可演（按需规原文） |
| 560 | 地图点位 + 详情抽屉 | 真坐标 circleMarker 按级别配色（国红/省橙/市蓝/孵化绿），点气泡开抽屉；抽屉含坐标 + 多媒体 + 新闻三块 | ✅ 可演 |
| 561 | 专题指标下钻表 + 点行联动地图 | 下钻表 9 区 + 其他地区 + 未分区单列（实测）；点行按区回跳名录——过滤器实测见 562，点击联动为同一 handler（代码核对）。**需规原文核对（2026-11-11）**：seq 561 点名「人才结构、企业数量、专利项目、结构调整」以趋势图 + 统计表格集中展示，企业/专利/人才为**真需规项**。**R2 落地**：下钻表 3 列 → **4 列**（行政区/载体数/占比/高新技术企业），高企列 = `enterprise_base.is_high_tech=1` 按注册地归区，未认定即真实 0、全区无标识才显「—」（不补 0）；专题趋势图 2 条（企业注册年度 47 年点 / 专利申请年度 `filing_date` 取年，灌数标「演示灌数」）；**人才结构四指标接 demo 库 `is_demo=1` 演示种子**（旭日 10 学科×5 院校×2 学院 / 结构 3 项 / 供需 12 技术域 / 流动 5 类），每块强制 `seeded=true` + 种子来源，页面打「演示种子」标；种子越界值（博士占比 124%）剔除并计数 `dropped=1`，不改写为 100。**仍缺口**：人才列无区县粒度（恒「—」，不按机构注册区折算）；SVC_005 岗位层次种子表无字段（恒空态给 reason）；企业/专利真实台账待供数 | ⚠️ 部分（人才区级列无粒度 + 真实台账待供数；结构与趋势已出图） |
| 562 | 图层/类型/规模/状态联动 + 重置 | 图层派生（innovation/incubation）→ 计数 4,376/608 实时联动；级别 445/2,473/2,066、类型 561、区 1,118、年度 424、关键词 42 全部命中；规模/状态无源 → 下拉置灰 + tooltip 直读后端 `missingFilters` | ✅ 可演 |
| 563 | 接口开发设计页签（接口目录） | 页签目录 **12 行**（分组/方法/路径/说明/时延/状态/操作）：4 条基础端点 + `district-indicators`（企业/专利/高企三条字段映射）+ `trend-indicators`（企业/专利两条）+ `talent-panorama`（演示种子）+ 1 条「人才区级列·待供数」显式空态行；顶部显式「前端演示目录…不请求真实后端，不作为接口已通的证据」；「模拟调用」只刷本地时间戳 | ✅ 可演 |
| 564 | 详情多媒体四类齐给 | 坐标（真坐标见地图点位）/ 图片「暂无图片资料（无源）」/ 视频「暂无视频资料（无源）」/ 新闻「暂无资讯。（无源）」四类各自空态，不互相替代 | ✅ 可演 |
| 565 | 三组筛选快速切换三者一致 | 后端 `consistency` 三元组（carriers/overview/meta 全 4,984，实测）页面脚注透出；多次筛选切换实测计数均随当次条件生效（未做并发压测）；请求取消与错误态不保留旧数据沿用仓内 request 层统一实现（代码核对） | ✅ 可演 |

**合计：8 可演 / 1 部分可演 / 0 缺口**（R3 部署态终判）。558 于 R3 由「代码闭环待部署」升 ✅（FE #4851 五 job 全绿 + 探针 46/46 + bundle R2 独有串 5/5）；561 维持 ⚠️——R2 已由「完全无数据」变为「4 列有 3 列有数 + 2 条趋势 + 人才种子」，余下「人才区级列、SVC_005 岗位层次、真实台账」仍是缺口，缺口不随发布消失。

- 561 余量（需规真项，R2 后）：已交付区级企业数 / 高新技术企业数 / 专利明细数三列 + 企业注册年度、专利申请年度两条趋势 + 人才结构四指标（种子）。**待供数/待补**：① 人才区级粒度（`talent_*` 无区县字段 → 恒「—」）；② 真实高企/专利/人才台账（现为 `enterprise_base` 标识 + demo 种子）；③ SVC_005 岗位层次（种子表无 `job_level`）。
- **R2 诚实性口径备案**：① 人才四块**全部** `seeded=true` 且来源写明 `is_demo=1`，正式供数后表内 `is_demo=0` 时端点自动落回 `seeded=false`，前端无需改；② 种子缺陷（博士占比 124%）**剔除并计数**，页面显式提示「已剔除 N 项越界占比，不画进图也不改写为 100%」；③ 高企列区分「未认定=真实 0」与「全区无标识=—」，两行相加守恒（pytest 断言逐行验）。
- 558 区级时序（已由本方自闭环，不再依赖外部供数）：`/ecology/trend` 端点已交付（python `453d88c` + java `35d3786` + FE `f10f4f7`），数据源即本表 `district_name × approve_year`，南山 1,118 条/28 年、守恒校验通过。**卡点已解（2026-11-11 10:14）**：display `/trend` 部署生效，探针扩至 46 项全绿 → 558 升 ✅ → **8 可演 / 1 部分 / 0 缺口**。FE `f10f4f7` 曾因并行 agent `situation/innovationEvaluation` 的 `strategyGuideCards` 类型错（`TS2741`）被 skip deploy，该错已由 `df1cc43` 修复（恢复 demo 冻结种子，非改类型为 optional），随 `600e58a` 一并上线（pipeline #4851）。踩坑备案：`vue-tsc --build` 走增量缓存会**假绿**，本地验证一律用 `vue-tsc --build --force`。

## 3. 后端调用与数据链

| 项 | 值 |
|---|---|
| 网关端点 | `/display/v1/service/ecology/{carriers,overview,carrier-detail,meta}`（display `EcoController` 转发 show-py `views/eco.py`）；R1 增 `trend`、`district-indicators`、`trend-indicators`；**R2 增 `talent-panorama`**（Java `ecoTalentPanorama` @NoToken + `EcoController#talentPanorama`） |
| 数据源 | `demo_gkxlumenx_ads.ads_innovation_carrier`，4,984 行（stic 创新 3,399 + 孵化 496 三源合并去重） |
| 一致性 | `carriersTotal = overviewTotal = metaTotal = 4,984`（同表 COUNT，天然一致） |
| 定位覆盖 | 区已定位 3,075（深圳九区 2,851 + 其他地区 224）、未分区 1,909；坐标 3,592（72.1%） |
| 富化标注 | `districtSource/geoSource` = `GEOCODED_AMAP`（高德推断）/`MANUAL_AMAP`（人工核录）/`ORG_ADDRESS`（机构地址带出），页面全量展示 |

## 4. R1 复核证据

| 证据 | 结果 |
|---|---|
| 探针 `../合规演示用例/eco_s4_probe.py` | **R3 部署态实跑 46/46 PASS**（延迟 meta 579ms / overview 295ms / carriers 359ms / district-indicators 3624ms / trend-indicators 725ms / talent 229ms，红线 15s）。R1 基线为 30 个断言点、实跑 29 PASS（1 项 `geo_rows` 为空时跳过）。**R2 已扩到 46 项**（+16：区级下钻 6〔高企列源声明/逐行 ≤ 企业数/高企守恒/企业守恒/人才列恒空/有行〕+ 专题趋势 4〔企业序列/专利来源 filing_date/灌数必带说明/区级 scope〕+ 人才种子 6〔四块可用/种子来源/每块 seeded/SVC_005 恒空/占比 0–100/旭日叶节点〕）——R3 已在三镜像发布后跑完，全绿 |
| 生产 bundle 校验 `../合规演示用例/eco_prod_bundle_check.py` | **R3 实测**：入口引用 44 个 chunk 全量扫描（不早停），ECO 页 chunk 由 `index-DiixTRrF.js` → `index-DjEsyT9A.js`(23KB，R1) → **`index-DfQOnxBt.js`(37KB)**；基线串 6/6、**R2 独有串 5/5**（`talent-panorama` / `M_SCIUI_SVC_001` / `演示灌数` / `人才结构四指标` / `is_high_tech`）→ 判定「生产已发布 R2 版」。脚本已改为**分层判定**（`R1_BASELINE` 只定位 chunk、`R2_ONLY` 才判版本）：早前拿「演示种子 / 高新技术企业」当 R2 特征是**误判源**——前者在 knowledge-graph 等页同样出现，后者 R1 台账文案里本就有 |
| 浏览器实测（本地 dev 真网关，等价生产同源构建） | **R3 补测人才页签**：`http://127.0.0.1:5288`（`VITE_APP_API_URL=http://10.50.69.111:30895`，源码 = 生产构建 `600e58a`）+ localStorage `access_token`（`display-loop-token`，绕 SSO 直连网关）；**8 个 canvas 全部非零尺寸**（434×300 ×6、434×380、918×300），页签内可见「人才学科旭日图 M_SCIUI_SVC_001 演示种子」「人才结构要点 M_SCIUI_SVC_002 · 2024 年演示种子」「学科分布对比 M_SCIUI_SVC_004 · 2024 年演示种子」「岗位层次细分 M_SCIUI_SVC_005｜演示种子表无岗位/职称层级字段（`talent_profile` 仅机构名与论文指标），供数后另接」「人才流动（需规 559「流动」）按流动类型 · 城市级口径演示种子」；台账四行真数据（高企 24,317 / 专利 532,792 / 载体 4,984），人才行标「降级·演示种子」。截图 `../合规演示用例/eco-talent-dev-20261111.png`。R1 已测：KPI 六卡、名录真数据行、详情抽屉（溯源+推断标注+邮箱空态）、趋势折线、多媒体四类空态、区县下钻（南山 1118/22.4%、未分区 1909）、地图双模式（南山区 200 真坐标点 / 深圳 choropleth）、接口目录+模拟调用 |
| 生产页直连 | 仍卡门户 SSO（`edu.itic-sci.com` → 统一用户中心，无测试账号）；本轮以「bundle 特征串 + 本地同源 dev 全页实测」双证据替代，生产 R2 版已由 #4851 部署并经 bundle 独有串 5/5 确认。门户账号到位后按同法补一次生产截图即可归档 |

## 5. 演示问答（口径备案，被问就照此答）

1. **区/坐标哪来的**：stic 公示只给机构名，区与坐标由大模型抽取 + 高德解析补全，属**推断值**；R4 起页面只展示值本身，不再挂「高德推断 / 高德解析」括注（来源留在数据层，前端不承载）。不接受推断值是数据缺口，是口径。
2. **为什么有 1,909 条「未分区」**：公示原文未给区且无法可靠推断，如实单列，不摊派、不补 0。
3. **地图为什么只画 200 个点**：点位模式取当前区最新 200 条（Python 端上限），页面明示；要看全量用「区聚合」choropleth（九区全覆盖）。
4. **为什么没有邮箱**：全库无邮箱字段，恒显「—」，不造数、不加「无源」括注。
5. **规模/状态为何置灰**：SRS 要求但无源，后端 `missingFilters` 显式声明，前端据此置灰并给 tooltip，属既定无源项。
6. **56x 接口目录页的「模拟调用」**：前端演示目录，点它不请求后端，不能当接口已通证据；真实已上线端点见目录中「已上线」四行。
7. **下钻表有哪几列**：R4 后 3 列——企业数（`enterprise_base.district`）、高新技术企业（`is_high_tech=1`，未认定即真实 0）、专利数（明细条数）。原「人才数（万人）」列已按需规 561 原文移除（561 只点名「人才结构」，结构在人才态势页签用四图呈现，且人才库无区县字段）——**不为凑列按机构注册区反推**。
8. **人才四张图是真数据吗**：不是。`talent_*` 全表 `is_demo=1` 演示种子，每块带 `seeded=true` + 种子来源，页面统一「演示种子」标；正式供数后自动落回 `seeded=false`。**被问「为什么不接真数据」就照此答**。
9. **专利趋势为什么标「演示灌数」**：64.8 万行仅落在 5 个申请日期（2020-02-15 等），是批量灌数痕迹，年度分布只能作形态示意；端点按 `filing_date` 去重天数 ≤60 自动打标，不冒充真实申请量。
10. **博士占比为什么图上没有**：种子数据该项 124%，越出 0–100，属种子缺陷；端点剔除并计数（`dropped=1`），页面显式说明剔除几项，**不改写为 100% 也不静默吞掉**。

## 6. 变更与回滚

- 前端 `lumen-ui-science-pc`：`9ba2584`（整页）→ `4ec5162`（slotName + 地图区选择）→ `5f46db4`（LOOP 补齐 557/563/564/558）→ `f10f4f7`（558 区级趋势）→ `9c91d1e`（R2：`types/eco.ts` + `api/service/eco.ts` + `ecoCarrierModel.ts` 4 个图表构造 + `index.vue` 人才页签/高企列/演示灌数标 + `eco-carrier.test.mjs`）→ **`600e58a`（3 个图表函数签名补 `\| undefined`，修 pipeline #4837/#4842 的 3 个 `TS2345`；pipeline #4851 五 job 全绿含 `deploy:k8s`）**。同行 `df1cc43` 为智库侧 `strategyGuideCards` 字段恢复（`TS2741`，与本页无耦合但阻塞同一构建）→ **`eebdbec`（R4：筛选补「全部」+ 省市区三级联动、去推断/无源括注、人才列与 `SVC_005` 卡移除、演示标注改评审模式门控、旭日图 `nodeClick:false`；4 文件 +130/−63）**。
- 后端 `lumen-topic-py`：`06f7a48` → `ad85ffc`（emptyReason 五处）→ `453d88c`（558 trend）→ **`1015c12`（R2：`eco.py` 的 `_hightech_counts_by_district` / `_patent_date_span` / `_build_sunburst` / `_talent_block` / `_build_talent_panorama` + `/talent-panorama` 端点；`main.py` 根路由登记；`tests/test_gkx_show_eco_boot.py` 13 例；pipeline #4835 success）** → **`deefe61`（R4：`_filters` 增 `districts` 多值 IN / `districtMissing` 空区过滤；carrier 详情 note 去推断标注要求）**。
- `lumen-svc-platform`：`0030682` → `35d3786`（558 trend）→ **`6f79b68`（R2：`RemoteShowPythonClient#ecoTalentPanorama` + `EcoController#talentPanorama`；deploy 为 manual 阶段，已手动发布，探针走生产网关全通即证）** → **`e1c2002`（R4：`EcoController#carriers` 透传 `districts` / `districtMissing`）**。
- 回滚：页面路由回落 `DevelopingView` 仅需还原 `src/router/menu.ts` 一行映射；后端四端点可独立下线（前端空态兜底，不白屏）。

## 7. M4 缺口补记（2026-11-11）

> 本页 M4 迟于 M5：2026-11-08 M4 建单时本页整叶 blocked，按范围排除（见裁定单范围行）；11-11 解锁重进 M3 后 M5 先行跑至 R3。补记只归纳既有实测，不回溯改写 R3 判定。

- 裁定位置：`../合规演示用例/展示系统-第一批-M4缺口裁定单.md` 第六节（G1–G5 处置 + G6–G8 新登记 + 口径与话术）。
- G1 页面未落地 / G2 契约未冻结 / G5 563 分项接口：**已闭环**（对应 R1 五页签实测、七组端点、563 目录 12 行）。
- G3 ADS 供数未到：**部分闭环**（558 由本页自闭环、561 人才接 `is_demo=1` 种子），真实台账转 G8。
- G4 561「人才结构 / 结构调整」：**撤销**（human 2026-11-11 裁定，需规原文 6 列不含该两项）。
- G6 人才区级粒度 / G7 `SVC_005` 岗位层次 / G8 真实台账：**新登记，建议修复（数据补），责任方数仓/供方**；三条均有实测降级路径，不阻塞签收，待授权人裁定（M4 单第十一项 a/b/c）。
- 与 M5 口径一致：本计划 R3 判「0 缺口」指 M3 口径的**设计缺口**为 0；G6–G8 属**供数深度缺口**，不进 M5 gap 降级表，改由 M4 单列跟踪——两处口径已交叉引用，不冲突。

## 8. R4 记录：human 逐屏核对后的口径收敛（2026-11-11）

> 起因：human:李伟 2026-11-11 用 5 张截图逐屏核对本页，提出 6 类反馈。处置原则统一为一条——**需规没要求、又无数据支撑的列/卡/标注，一律去掉，不留「空态占位」**；判据回到需规原文（557 / 559 / 561），不新增演绎项。
> 本节是 R4 的唯一凭据：**后续任何人看到「人才列没了 / 岗位层次卡没了 / 没有推断标注」都不算缺漏，先读本节**。

| # | human 反馈 | 处置 | 判据 |
|---|---|---|---|
| 1 | 级别 / 类型 / 所在区都要有「全部」 | 级别、类型补显式「全部级别 / 全部类型」选项（原仅靠 allow-clear 占位）；所在区改 `a-cascader` 省市区三级联动，根节点「全部地区」 | 筛选可达全量，否则用户回不到初始态 |
| 2 | 区名带「（高德推断）」 | 名录列只出区名；`districtSourceLabel` / `geoSourceLabel` 停止渲染 | 标注是内部口径，页面不承载 |
| 3 | 要能选整省 / 整市 | 级联 `全部地区 / 广东省→深圳市→九区 / 其他地区 / 未分区`；`districtScope()` 折算为单区 `district`、多区 `districts`、或 `districtMissing` | human 要求；后端同步支持 |
| 4 | 详情里「（高德解析）」「（全库无源）」 | 详情 7 字段去括注，空值统一「—」；后端 note 文案同步改写 | 同上 |
| 5 | 无数据的两列 | 561 下钻表移除「人才数（万人）」列（4 列→3 列），**保留高新技术企业列** | 561 原文只点名「人才结构」未点名人数；人才库无区县字段恒空；高企列由 557 点名 |
| 6 | 无数据的图 | 移除 `SVC_005` 岗位层次细分卡 | 561 未点名「岗位层次」，种子表无该字段，恒空态 |
| 7 | 「演示种子 / 演示灌数」常驻 | 种子 alert、卡角标、灌数标、脚注改由 `useReviewStore().reviewMode` 门控 | 演示标注只在评审模式可见，对外演示视图零泄漏 |
| 8 | 旭日图下钻后回不到初始态 | `nodeClick: false` 锁初始态 | 交互可逆性 |

**与 M4 缺口的关系（重要）**：

- **G6（人才区级粒度）撤销**：列已删，不再需要区级人才人数。
- **G7（`SVC_005` 岗位层次）撤销**：卡已删，不再需要种子表补 `job_level`。
- **G8（真实台账）保留**：561 转全仍待供数，页面继续标「演示灌数 / 演示种子」（仅评审模式）。
- 撤销 ≠ 补齐：561 判「部分可演」的原因是 G8，不是 G6/G7。M4 单 6.2 / 6.3 / 6.4 与用例文档缺口表已同步改写。

**代码落点（R4）**：

| 仓 | commit | 内容 |
|---|---|---|
| `lumen-ui-science-pc` | `eebdbec` | `index.vue` + `ecoCarrierModel.ts` + `types/eco.ts` + `eco-carrier.test.mjs`，4 文件 +130/−63 |
| `lumen-topic-py` | `deefe61` | `_filters` 增 `districts`（逗号多值 IN，空名剔除不产生 `IN ()`）与 `districtMissing`；carrier 详情 note 去推断标注要求 |
| `lumen-svc-platform` | `e1c2002` | `EcoController#carriers` 入参与转发 `districts` / `districtMissing` |

**验证（R4）**：

- `node src/views/service/eco-carrier/eco-carrier.test.mjs` 通过（新增 8 条断言：全部项 / `a-cascader` + `districtCascade` / `__all__` 根节点 / `districtMissing` / 无 `districtSourceLabel` / 无「无源」括注 / `nodeClick:false` / 无人才列）。
- `vue-tsc --build --force` 本页 0 错（同目录 `think-tank/TabFilterBar.vue` 3 错为他人未提交改动，与本页无关）。
- `pytest tests/test_gkx_show_eco_boot.py` **13 passed**。
- 本地 dev 真网关实测（`127.0.0.1:5288` + `VITE_APP_API_URL=http://10.50.69.111:30895` + localStorage `access_token`）：级联三级实测 `全部地区 | 广东省 | 未分区（1909）` / `深圳市 | 其他地区（750）` / 南山区 1118·宝安区 500·龙岗区 306 等九区；名录「所在区」列纯区名；详情抽屉无任何括注、空值「—」；人才页签无 `SVC_005`、无演示标注（`reviewMode=1` 对照后标注出现）。截图 `../合规演示用例/eco-r4-filter-cascade-20261111.png`、`eco-r4-talent-clean-20261111.png`。

**遗留**：~~`districts` / `districtMissing` 需部署后才生效~~ **已于 2026-11-11 生产实测生效**（见 §9 验证：`districts`=九区→2,851、`districtMissing`→1,383、baseline→4,984）。

## 9. R5 记录：human 二次逐屏核对的六项收口（2026-11-11）

> 起因：human 在 R4 构建上二次核对，提 6 项。其中第 1 项**不是口径问题，是真 BUG**（取错值导致查 0 条），必须记清楚，防止后续被当成「后端没部署」搪塞过去。

| # | human 反馈 | 根因 / 事实（实测） | 处置 |
|---|---|---|---|
| 1 | 地区筛选选完没有数据 | **真 BUG**：`a-cascader` 未设 `path-mode`，Arco 单选默认 `pathMode=false`，v-model 回的是**标量**（`'南山区'`）；`districtScope()` 直接 `p[2]` 索引字符串 → 取到第三个字「区」→ 查 `district_name='区'` = 0 条 → **空表**。深圳九区名全为 3 字，故「选哪个都空」 | 加 `path-mode`（v-model 回完整路径 `['广东省','深圳市','南山区']`）+ `Array.isArray` 防御（标量降级为空路径，不按字符索引）；watch 同步防御 |
| 2 | 每个选项后面的数字去掉 | 级别 / 类型 / 级联 label 拼了 `（count）` | 三处 label 去计数，只留名称 |
| 3 | 去掉企业规模、运营状态筛选项 | 562 原文有「规模/状态联动」，但两字段全库无源，R4 前是置灰占位 | 移除两个筛选项 + `missingScaleTip` / `missingStatusTip` 计算属性，不留假控件 |
| 4 | 「区县下钻（已定位口径）」去括注 | 内部术语外露 | 标题改「区县下钻」；地图说明「区聚合 = 已定位口径」→「区聚合按注册地归口」 |
| 5 | 高新技术企业列是否该留 | **需规 561 未点名该列**（561 点名人才结构/企业数量/专利项目/结构调整）；**但数据有**：2026-11-11 实测 `district-indicators` → 南山 3,877 / 福田 3,961 / 龙华 2,117 …，`columnStatus.highTechCount.available=true`，仅未分区行恒「—」 | **保留**（条件「没要求 **且** 没数据」不成立）。该列系 R2 human 裁定「B 加高企列」所加，且 557 点名区级高企数。若后续要按 561 严格收口（只留行政区/载体数/占比），删列即可，无副作用 |
| 6 | 详情「联系方式为富化回填…（addressSource/phoneSource 见方案）；邮箱无数据时显「—」，不造值」 | 后端 carrier 详情 `note` 硬带该句 | 删除整条 `note`（前端 `v-if="detail.note"` 自然不渲染） |

**代码落点（R5，未提交推送，待 human 确认）**：

| 仓 | 文件 | 内容 |
|---|---|---|
| `lumen-ui-science-pc` | `eco-carrier/index.vue` | `path-mode` + 数组防御；三处 label 去计数；删规模/状态筛选块与两个 computed；下钻标题去括注；地图说明改「注册地归口」；接口目录 desc 去「无源」；文件头/抽屉注释同步 |
| `lumen-ui-science-pc` | `eco-carrier/eco-carrier.test.mjs` | 规模/状态断言反转为「已移除」；新增 8 条（去计数 ×3、`path-mode`、数组防御 ×2、标题、计数残留） |
| `lumen-topic-py` | `gkx_show_service/views/eco.py` | carrier 详情不再输出 `note` |

**验证（R5）**：

- `node eco-carrier.test.mjs` 通过；`vue-tsc --build --force` 本页 0 错（`think-tank/TabFilterBar.vue` 3 错仍是他人未提交改动）。
- `pytest tests/test_gkx_show_eco_boot.py` **13 passed**。
- **后端接口生产实测**（`http://10.50.69.111:30895`，`display-loop-token`）：`carriers` baseline 4,984 / `district=南山区` 1,118 / `districts=九区` 2,851 / `districtMissing` 1,383 / `district-indicators` 11 行 `highTechCount` 非空 —— 证明 `districts` / `districtMissing` **已在生产生效**，空表与后端无关。
- **浏览器 E2E 未跑（如实声明）**：本机 Node v20.18.0 低于 vite 要求的 20.19+，`pnpm dev` / `npx vite` 均无法启动，`install_binary` 装 Node 22 报 `EPERM`；R4 当时的 dev 实测环境本轮不可复现。故「级联选后有数据」目前是**代码闭环 + 后端接口实测**双重证据，端到端待部署后点一次确认。

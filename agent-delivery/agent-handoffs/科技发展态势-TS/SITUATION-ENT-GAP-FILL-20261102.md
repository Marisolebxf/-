# SITUATION-ENT-GAP-FILL-20261102 · DS-01 缺口补登记（收藏服务端 / 要素卡趋势 / 趋势预测）

> **任务**：DS-01 科技全域态势（WBS-05-18）缺口补登记，2026-11-02
> **角色**：`agent:api-agent`（`auto` 模型）· 监管人：`human:李伟`
> **授权留痕**：`human:李伟` 2026-11-02 指令「缺少的 WBS 都补上」→ 按路径 2（无 task-create MCP，参考 SITUATION-IM C2=①）直接更新 `task-registry.yaml`，建 `SITUATION-ENT-SPARK-L01` / `SITUATION-ENT-FOLLOW-SVR-L01` / `SITUATION-ENT-TREND-FEAT-L01` 三条 **backlog** 单；本文件为三单共用 handoff。
> **状态**：登记 + 方案分析，**未开工实现**；改动停本地未 commit / 未 push。

---

## 一、要素收藏：统一建设已存在，DS-01 已复用，缺服务端（`FOLLOW-SVR-L01`）

### 1.1 核查结论

| 问题 | 事实 |
|---|---|
| 系统是否有收藏统一建设？ | **有**。`repos/lumen-ui-science-pc/src/components/export/useFollow.ts`（FE-TS-S01 底座产物，原 S05）：全局唯一 composable，`FollowItem` 键结构 `sourcePage:type:objectId`、去重 / 取消 / 持久化 |
| DS-01 是否复用？ | **是**。`overview/index.vue:23` `import { useFollow } from '@/components/export/useFollow'`、`:126` 解构使用；`factorTagStore.ts`（标签目录）与收藏项共用对象键；公共底座 `components/workbench/FilterBar.vue:178` 收藏夹按钮、`InsightDetailDrawer.vue` follow 按钮同源 |
| 是否符合规则？ | **符合**。①「同一交互第 2 处出现即封装」——封装已存在且被复用；② D4 决策（`useFollow.ts:2-6` 注释）早已裁定「**服务端接口为主 + localStorage 缓存乐观更新；接口未就绪（mock 关）纯本地降级**」，升级路径写明 `defineApi('tsFollowList')` + 乐观更新回写 |
| 现状差距 | `useFollow.ts:48-49` ponytail 自述：「首版服务端接口未出（BE-TS-CONTRACT-01 冻结前），以 localStorage 为唯一真源；上限：单机单浏览器」——即**不真实**（换浏览器 / 清缓存即丢，多端不同步） |
| 后端可否复用既有收藏？ | `gkxlumen-app-server` 有 `AppArticleCollectEntity`（`app_article_collect` 表：userId + articleId + 审计四件套 + delFlag，MyBatis-Plus + 租户表）——但属 App 端 CMS 文章收藏，**域不同（app-server vs display）、对象不同（文章 vs 科创要素），不直接复用**；建表 / CRUD 模式可参照 |

### 1.2 做真实收藏的最小路径

1. **前端零结构改动**：`useFollow` 对外接口（`items / isFollowed / toggleFollow / removeFollow`）不变，内部把「localStorage 唯一真源」升级为 D4 已定决策「服务端为主 + localStorage 乐观更新 + 失败降级」；`factorTagStore`（标签目录）一并服务端化。
2. **后端新增（⚠️ 2026-11-02 归属二次校正）**：
   - **不得落 display**：`gkxlumen-display/src/main/resources/application.yml:23` 明写「**职责边界：只读。不直连业务库**」；display 当前 Mapper/Entity 数为 **0**，是纯读 BFF。
   - **也不是 upms**（本节前稿写 `gkxlumen-upms` / `sys_user_follow` 系误判，已改正）：按 `ARCH-DISPLAY-01.md:513` 既有设计「`/display/v1/trend/favorites`、`/tags` | 收藏/标签 | **写 `app_user`**」+ `:87` D3 铁律「Java 仅读 `*_ads` + **`app_user` 读写**」，归属是 **app 库的 `app_*` 表族**（`db/999gkxlumenx_app.sql`，现有 9 表：`app_article / app_article_category / app_article_collect / app_page / app_tabbar / app_role / app_social_details / app_user / app_user_role`）。
   - **表结构无既有设计**：全仓无收藏表 DDL；`BE-TS-CONTRACT-01` 未产出（`useFollow.ts:6/48` 自述"接口未就绪"）；架构文档 `:88/:104` 引用的「§10.5」实际内容是「异步任务与导出」，属**引用错位**，收藏没有独立设计章节。
   - **自拟方案（须评审）**：新建 `app_user_follow`，字段按 `useFollow.ts` 的 `FollowItem` 9 字段反推（`source_page / type / object_type / object_id / title / summary / tags / followed_at`）+ 参照同库 `app_article_collect` 的审计四件套 + `del_flag` + `tenant_id`；唯一键 `(tenant_id, user_id, source_page, type, object_id)`（`app_article_collect` 只有主键、靠代码查重，新表应补唯一键防并发重复）；标签目录另建 `app_user_tag`（对应 `/tags`）。
   - **表名 / 唯一键 / tags 承载方式三项为自拟，无既有依据**，需 `human:李伟` 评审后由运维执行 DDL（本轮未执行任何 DDL、未建表）。
3. **依赖**：端点纳入 `BE-TS-CONTRACT-01` 契约（该单 M0 未评审）；用户态用 SSO（auth 10-31 已接授权码登录，`userId` 可取）；upms 建表授权。
   **当前状态**：`backlog`，等归属裁定（本单未开工实现）。

## 二、要素卡年度趋势 spark：口径权衡与方案（`SPARK-L01`）

### 2.1 现象与根因

- demo 原型：每张 KPI 要素卡下方有 2020–2026 逐年趋势线（如「专家学者 21.8 万」红线，`overviewData.js` mock 种子）。
- lumen 现页：**8 张要素卡 `series=null`，全部显示「暂无趋势数据」**——`SituationController.buildFactorCards`（:3643-3670）每个 `card(...)` 传 `series=null`。
- 根因（:3636-3641 注释）：卡上数值是**存量 / 去重总量**，现有年度序列是**增量 / 年度 SUM**，「存量卡 + 增量线」混在一条 sparkline 属口径混搭，宁可不画。

### 2.2 数据可得性（实测代码依据）

| 要素 | 卡上数值口径 | 年度序列 | 同源性 |
|---|---|---|---|
| 企业 | 存量 189,115（element 总量） | ❌ 无存量序列；`/trend` 只有注册年**增量** | 等 ADS 逐年存量快照（`C6-L01` 已挂契约：year+total_count，2020–2026，末点=存量总量） |
| 论文 / 人才 / 项目 / 机构 | `overview-kpi`（文档主表**去重**计数） | ✅ `monitor/yearly-trend`（py :358-435）：`ads_geo_yearly_metrics` 按 `statistics_year` **SUM**，出 `paper/talent/institution/project_count`，缺年 null | ⚠️ **口径差**：py 注释（:373-374）「跨国合作论文在多国各计一次，COUNTRY 级 SUM ≠ 全球去重总数」 |
| 专利 | `kpi.patent_count` | ❌ yearly-trend 无 `patent_count` | 无源 |
| 期刊 / 会议 | D3 mock 卡 | ❌ 无 | 无源 |

### 2.3 方案（怎么做最合适）

- **方案 A（推荐，立即可做）**：论文 / 人才 / 项目 / 机构四卡接 `monitor/yearly-trend` 序列（`addTrendSeries` 同款：缺年 null 断点，不补 0），series 附 `caliberNote` 如实标注「年度地域聚合口径（含跨国重复计入），与卡上去重总量有差，看趋势形态不看绝对值」；**前端零改动**（`sparkOptionOf` / `buildFactorSparkOption` 已就绪）。
- **方案 B（企业卡，口径最正）**：等 ADS 逐年存量回补（C6 契约已写好），接上后卡上数值 == spark 末点，前端零改动。
- **方案 C（无源要素）**：专利 / 期刊 / 会议维持「暂无趋势数据」空态，不编序列。
- **不采用**：拿注册年增量给存量企业卡硬画（口径混搭，即当前不画的原因）；拿 demo mock 种子补数（违反 USE_MOCK=false 零 fixture）。

### 2.4 实施记录（2026-11-02 完工，status = integration）

**后端 `SituationController.java`**
- `/overview`：`yearlyRows` 保留 `monitorYearlyTrend` 全量年度行（原只取最新完整年），与 `latestYear` 共用同一次调用，不多打一次网络。
- 新增 `sparkSeriesOf(rows, valueKey, factorKey, seriesName, caliberNote)`：
  - **排除不完整年**（`year < 当前年`，与 `latestFullYearOf` 同规则）——实测若含 2026，talent 会从 159,546 断崖到 36,730，被读成「暴跌」；
  - **近 10 年窗口**（首年 = 末完整年 − 9），只截显示窗口、不抽样不改值，窗口内缺年 null 断点、不补 0；
  - 值一律 `num()` 落 **int**（`Long` 会被平台 Jackson 序列化成字符串数组，前端画不出线且无明显报错）；
  - 整列缺值返回 null（前端出「暂无趋势数据」），不造全断点空折线。
- `buildFactorCards` 加 `yearlyRows` 参数：论文 / 人才挂 `SPARK_CALIBER_DIFF_NOTE`（卡值走文档主表去重、序列走地域表按年 SUM，不同源）；项目 / 机构挂 `SPARK_CALIBER_SAME_NOTE`（同源，末点即卡上数值）；企业 / 专利 / 期刊 / 会议仍 `series=null` 不造数。

**前端**
- `types/situation.ts`：`TrendSeriesData` 增 `caliberNote?: string`。
- `chartBuilders.buildFactorSparkOption`：tooltip 末尾追加口径说明（`max-width:230px` 自动换行），不让 spark 末点被当成卡上绝对值读。

**实测证据（7101 独立实例，`--spring.profiles.active=local`）**

| 卡 | 卡值 | 序列末点（2025） | 判定 |
|---|---|---|---|
| talent_total | 159,546 | 159,546 | 同源，一字不差 ✓ |
| project_total | 392,032 | 392,032 | 同源，一字不差 ✓ |
| institution_total | 48,444 | 48,444 | 同源，一字不差 ✓ |
| paper_total | 858,620 | 1,287,996 | 不同源，`caliberNote` 如实标注 ✓ |
| enterprise / patent / journal / meeting | — | `null` | 空态不造数 ✓ |

- 序列年份 = 2016–2025（10 点，无 2026 断崖）。
- 编译：`javac` 全量 25 个源文件（classpath 取运行中 fat jar 的 206 个依赖）**EXIT=0**；`vue-tsc --build` **EXIT=0**。
- 运行时：`POST /v1/situation/overview` `code=0`，数值同上表；验证后已停 7101、清理 `tmp_verify` / `tmp_out` / argfile，生产 :7099 未受影响。
- ⚠️ **本机 maven 不可用**：内部 `gkxlumen-common-bom:5.12.0` 在本地仓库缺 pom、且无 `settings.xml` 私服配置，`mvn -o` / 联网 / `-llr` 三种方式均卡在依赖解析（非代码错误）。故未走 `mvn package`，编译验证改由 javac + 运行中 jar 依赖完成，**非跳过验证**。

## 三、趋势预测 / 异常监测：需规超 demo 差集，补登记待裁定（`TREND-FEAT-L01`）

- 需规 excel_row 15《监测数据趋势变化查看功能》四子项：时间轴趋势 ✅（`GRANULARITY-FIX-L01` + 本轮 `SPARK-L01` 方案）、趋势预测 ❌、异常监测（异常点 / 突变点自动识别标记）❌、多时间维度 ✅。
- demo 原型无预测 / 异常监测形态，也无数据源支撑（需趋势算法与历史断面数据）——属需规超 demo 差集，登记 backlog，**是否纳入本期待监管人裁定**。

## 四、订阅：已有登记，不重复建单

- DS-01 需规 16 项**无订阅**；订阅属创新监测三页（DS-04/05/06，WBS-05-19），WBS :137 已登记「订阅 / 推送的对端宋泉未确认则该块空态」，且 `BayInnovationController.java:398` 写面端点按 U5 裁定 deferred 二期。按规约出空态即可，无新增动作。

## 五、本轮登记清单

| WBS 行 | 单 ID | 状态 | handoff |
|---|---|---|---|
| WBS-05-18-15 | `SITUATION-ENT-SPARK-L01` | **integration**（11-02 完工） | 本文件 §二 + §2.4 实施记录 |
| WBS-05-18-16 | `SITUATION-ENT-FOLLOW-SVR-L01` | backlog（待裁定表归属 upms） | 本文件 §一 |
| WBS-05-18-17 | `SITUATION-ENT-TREND-FEAT-L01` | backlog（待裁定是否本期） | 本文件 §三 |

- 同步更新：`WBS.md` §4.3（三行）+ §1 第 66 行摘要；`task-registry.yaml` 三条单。
- 前后端代码仓本轮**零改动**（纯登记 + 方案分析）。

## 六、Ponytail + Cost

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 只登记事实与方案不写代码：收藏统一建设核查以代码 import 链为证；趋势方案逐要素标注数据可得性与口径差（跨国 SUM ≠ 去重总数照抄 py 注释），无源要素维持空态不造数；订阅已有登记不重复建单 |

| 字段 | 值 |
|------|-----|
| estimated_tokens | 40000 |
| actual_tokens | ~60000（估算） |
| model_used | Auto |
| actual_cost | ~$0.6（估算） |
| cost_warn | green |

## 七、改动停本地

本轮仅 `WBS.md` / `task-registry.yaml` / 本文件三个文档改动，**未 commit / 未 push**，随 6 条 integration 单一并等 `human:李伟` 走查。

---

## 八、2026-11-02 晚补记：三项 WBS 可完成性裁定 + 筛选联动修复 + 关键词检索需规核对

> 触发：`human:李伟` 2026-11-02 问「spark 趋势、影响力 Tab、趋势预测 这三个哪个可以做完；筛选项并没有刷新实时监控这边的卡片数据；确认需规是否要求关键词检索，没有就先去除掉」。
> 本轮改动停本地，**未 commit / 未 push**。

### 8.1 三项 WBS 哪个可以做完（结论：只有 spark 能真做完，另两项被数据源/裁定卡住）

| 项 | 单 | registry 状态 | 能否做完 | 依据 |
|---|---|---|---|---|
| spark 趋势 | `SITUATION-ENT-SPARK-L01` | `integration` | ✅ **代码已完工，本轮本地实测复核通过** | §2.4 实施记录；本地 `:7099 /overview` 实测 8 卡中 paper/talent/project/institution 四卡 `sparkYears=10`，enterprise/patent/journal/meeting 四卡 `sparkYears=0` 保持诚实空态。剩企业卡待 ADS 逐年存量回补（C6 契约已挂），属**明确的数据源依赖**，非代码缺口 |
| 影响力 Tab | `INFLUENCE-FIX-L01` + `METRIC-LIB-ALGO-INFLUENCE-L01` | 均 `integration` | ⚠️ **代码已完工但含 mock**，不能算全做完 | `INFLUENCE-FIX-L01` §四 7 条后端 + 4 条前端验证、`METRIC-LIB-ALGO-INFLUENCE-L01` §三取数口径对照表：期刊/专家已接算法库 precompute 真数，**论文/专利/服务项目 3 卡仍是 `influence-v1` 代码层 mock**（算法库无 precompute 产物 / CMS 源未接），本地 `/influence` 实测 `anyMock=true`。去 mock 需算法侧产物 + CMS 数据源，**不是本页前端能做完的** |
| 趋势预测 / 异常监测 | `SITUATION-ENT-TREND-FEAT-L01` | `backlog` | ❌ **做不完，且不该现在做** | 需规 excel_row 15 确有此二子项，但 demo 原型无形态、需趋势算法与历史断面数据源；DoD 第一句是「`human:李伟` 裁定纳入本期或明确不做」。**裁定未下 + 数据源无着落，禁止造数硬做** |

> 一句话：spark 可以推到验收；影响力 Tab 只能推到「带 mock 的验收」并在台账保留接真条件；趋势预测必须等裁定。

### 8.2 筛选不刷新「实时数据监控」卡片：定位与修复

**后端已修过一轮，不是后端问题**：`SituationController.java` 的 `cardsOfFactors`（:1620，注释写明「2026-11-02 用户反馈：切换要素后实时监控卡片一动不动」）按 `enabledFactorKeys` 裁剪卡片集；`regionFactorsOf`（:3382）让选中城市改取该市真实计数；`scopeOf`（:330）统一翻译地域/关键词/领域。本地 `:7099` 实测三条：

| 筛选 | 卡片变化 |
|---|---|
| `enabledFactorKeys=["paper"]` | 8 卡 → **1 卡**（`paper_total`） |
| `activeRegionKey=shenzhen` | `scopeLabel=城市：深圳市`，企业 187,643→**95,525**、论文 858,620→**24,904**、机构 48,444→**113** |
| `searchTerm=华为` | `scopeLabel=关键词：华为`，企业 187,643→**10** |

**真正根因在前端渲染层**：`OverviewTab.vue` 的 `tabDataKey` 只由「stats 数量 + factorCards 数量 + visibleSlices 的 key 名」拼成，且 `:key="tabDataKey"` 绑在整棵子树根节点，用途是规避 dev 模式 props 深链更新不触发重渲染。筛选改变的是**卡片数值**（地域/关键词/年份/要素），卡片数量与 key 名往往不变 → `tabDataKey` 不变 → 子树不重挂 → 屏幕停留在上一份 dataset 的数值，表现为「筛选了但卡片没动」。

**修复**（`lumen-ui-science-pc/src/views/situation/overview/components/OverviewTab.vue`）：`tabDataKey` 改为纳入数值签名——`stats` 的 key:value、`factorCards` 的 key:value:spark 年数:末点值、`visibleSlices` 的 value/rawValue、`trendSeries` 的年轴与序列长度，以及 `isEmpty` / `trendGranularity` / `scopeLabel` / `fieldScopeLabel`。任何一次异步数据到达都会触发重挂。重挂的是根 div 子树而非组件实例，`chartType` / 隐藏卡 / 拖拽顺序等本地 ref 状态不丢失。

**验证**：`read_lints` 该文件 0 错误；`npm run type-check` 仍**无法执行**——并行会话的 pnpm 重装未完成（`.bin/vue-tsc.cmd` 存在但顶层 `vue-tsc`/`vue` 目录未建、`.pnpm` 内 `@volar/typescript/lib/quickstart/runTsc` 找不到），待链接完成后须补跑。后端 `:7099` 实测（上表）已证明数据链路通畅。

### 8.3 关键词检索：需规**明确要求**，不去除

需规真源 `bid-reference/srs/02-科技信息展示系统/科技发展态势/科技全域态势.md`：

- **序号 4「搜索要素定位」（excel_row 7）** 三个子项：① 搜索框交互（输入企业名称/机构类型/地址，实时触发检索）；② 智能匹配机制（**后台**对重点企业/服务机构/科研机构模糊或精确匹配，生成候选结果列表）；③ 历史记录缓存（保存搜索历史、快速重选）。
- 现状 UI（`SituationFilterBar.vue` 的 `top-keyword-search`：输入 + 候选面板 + `KEYWORD_HISTORY_KEY` 历史 + 范围摘要 + 防抖）与 `searchTerm` 全链路接线均对应需规，**且本地实测 `searchTerm=华为` 真实影响后端取数**（企业数 187,643→10）。

结论：**需规有要求，不删除**。另需注意 `SCI-INT-A01` 已把「要素搜索」登记为 **X-004 缺口**：现状是「前端在已加载样本内做匹配，没有后端检索」，需新建三要素检索索引（Java 门面 → Python → ES）。即**功能保留、后端检索能力是既有缺口**，与本轮「去留」判定无冲突；不新建单、不重复登记。

### 8.4 本轮改动清单

| 仓 | 文件 | 改动 |
|---|---|---|
| `lumen-ui-science-pc` | `src/views/situation/overview/components/OverviewTab.vue` | `tabDataKey` 纳入数值签名（修筛选不刷新卡片） |
| `gkx-orchestration` | 本文件 §八 | 三项裁定 + 根因 + 需规核对留痕 |
| `gkx-orchestration` | `task-registry.yaml` | 相关单 note 追加本轮结论 |

> 关键词检索**零改动**（需规要求保留）；趋势预测**零改动**（待裁定）；spark / 影响力 Tab **零代码改动**（代码此前已完工，本轮只做本地实测复核）。

---

## 九、2026-11-03 补记：指标表更新 + 关键词检索后台实现（X-004 MVP）

> 触发：`human:李伟` 2026-11-03「@metrics 先更新这个再检查……`M_INNOV_PATENT_INFLUENCE` / `M_INNOV_PROJECT_INFLUENCE` 我看算法已经有了；关键词检索 要做后台实现」。
> 承接 §8.3 的结论（需规要求保留关键词检索、X-004 是既有缺口）——本轮把「保留」推进为**补后台实现**，不是结论反转。
> **改动停本地，未 commit / 未 push**。

### 9.1 指标入库详情表更新（先做）

文件：`agent-delivery/metrics/指标入库详情-合并-20261028-三系统.xlsx`

| Sheet | 行 | 指标 |
|---|---|---|
| 科技展示系统 | 228 / 244 | `M_INNOV_PATENT_INFLUENCE` / `M_INNOV_PROJECT_INFLUENCE` |
| 科技专题算法库 | 236 / 252 | 同上 |

**落表方式**：只在备注列 O 写入「[2026-11-03 算法已有·human:李伟 指认] + 证据 + 层级边界」，共 4 格。

- **不新增状态列**：`metrics/README.md` 明确 xlsx 不是四维就绪度真源（`registry/` YAML 才是），禁止造平行状态表。
- **不改绿**「数据支持度=部分支持」「更新频率=待确认(pending)」：这两列取 calc-logic md 抬头四档真源；「算法已有」是另一个维度，不能据此改数据口径。
- 算法侧实证：`calc-logic/INNOV/{id}.md` + `repro/{id}.py` + `repro/out/{id}_out.json` 均在仓；`demo-algo-science` 有 catalog 登记、`POST /v1/innov/metric/{id}/compute(status=available)`、`data/precompute/{id}.json` 静态快照、评审目录 `status: available`。
- **层级边界（如实写入备注）**：快照是 2026-10-22 离线复跑结果经通用 `/compute` 壳返回（代理 SQL 兜底），非按口径在线算法服务；`lumen-algo-py` 无该指标在线实现；`metric-readiness-matrix-INNOV.yaml` 仍 `d4=mock`「算法服务未上线」；展示端 `/v1/situation/influence` 专利卡仍 `influence-v1` mock（样本覆盖 0.012%，不能全库排名）。与 `INFLUENCE-FIX-L01` §1「五类指标均已登记，但对象级算法服务未上线 → 缺的用 mock 补齐」一致。
- 备份：`%TEMP%/指标入库详情-合并-20261028-三系统-备份-20261103.xlsx`；读回校验：仅 4 格变化，D/K 列未动、2046 个超链接完好、0 公式。

### 9.2 关键词检索后台实现（X-004 MVP，零新索引 / 零 ETL）

**范围约束**：`SCI-INT-A01` X-004 契约草案标注 `structure_escalation: true`（新建三要素 ES 索引需 human 批准）。本轮**不新建索引**，复用现有 `gkx_enterprise` + `gkx_svc_org` 两个对象级索引打通全链路；科研机构/人才/论文/专利/项目等无索引要素返回**诚实空类目 + 原因**，不造数、不回落本地伪结果。索引补齐仍待批准。

链路：`SituationFilterBar` → `fetchSituationFactorSearch` → `POST /display/v1/situation/factors/search` → Java 门面 → Feign(`@NoToken`) → `POST :8080/internal/gkx-search/factors` → ES。

| 仓 | 文件 | 改动 |
|---|---|---|
| `lumen-topic-py` | `gkx_search_service/views/factor_search.py` | **新增**端点：双索引 wildcard/phrase 检索、wildcard 元字符转义、候选带 `source`、分类 `available` 标记、覆盖度；ES 不可用抛 `RealDataUnavailable` → main.py 既有 handler 转 503 |
| `lumen-topic-py` | `gkx_search_service/main.py` | import + `include_router` + 根 endpoint 清单登记 |
| `lumen-svc-platform` | `display/feign/RemoteFactorSearchPythonClient.java` | **新增** Feign（`@NoToken`，本地直连 `${gkxlumen.factor-search.python-base-url:}`，生产走服务发现 `gkxlumen-platform-search-py`） |
| `lumen-svc-platform` | `display/controller/SituationFactorSearchController.java` | **新增独立 Controller**：参数校验（keyword ≤80、limit ≤20）、下游异常兜底为 `degraded=true + 空 items`；**故意不改动并行会话正在动的 `SituationController.java`**，两者共用 `/v1/situation` 前缀但路径不重叠 |
| `lumen-svc-platform` | `resources/application-local.yml` | 加 `gkxlumen.factor-search.python-base-url: http://127.0.0.1:8080` |
| `lumen-ui-science-pc` | `types/situation.ts` / `api/situation/index.ts` | 新增检索入出参类型与 `defineApi` 端点（独立端点，不挂进 6 个态势端点签名） |
| `lumen-ui-science-pc` | `views/situation/overview/index.vue` | 候选改双轨：真实轨走后台（独立 260ms 防抖 + seq 防竞态），演示轨 `USE_MOCK=true` 保留 demo 冻结种子；加载/降级状态；选中候选时 `regionKey` 为空不误清用户地域 |
| `lumen-ui-science-pc` | `components/SituationFilterBar.vue` | 新增 `keywordSearchLoading / Notice / Degraded` 三 props，面板区分「正在检索 / 服务不可用 / 真无匹配」，降级时面板仍展开 |
| `lumen-ui-science-pc` | `mock/modules/situation.ts` / `mock/register.ts` | 演示轨 `tsSituationFactorSearch` 兜底注册（返回诚实空态，不编造候选） |

**诚实性守住的线**：下游不可用返回 `degraded=true` + 空候选 + 明确原因（前端显示「检索服务不可用，未生成候选（不回落本地伪结果）」），与「真的无匹配」区分；无索引要素标 `available=false` + 原因；不把聚合数值冒充候选；`USE_MOCK=true` 演示轨是本地冻结种子、不冒充真实结果。

### 9.3 验证与未验证（如实）

| 验证 | 结果 |
|---|---|
| Python `py_compile`（factor_search.py / main.py） | ✅ EXIT=0 |
| Python 端点导入自检 | ✅ 路由 `POST /internal/gkx-search/factors` 注册成功、`CATEGORY_DEFS` 与 wildcard 转义正确 |
| Java `javac`（fat jar 内嵌 206 依赖 + 35 class 作 classpath） | ✅ **EXIT=0**（首次 `-proc:none` 关掉 Lombok 导致 `log` 找不到，去掉该开关后通过；非代码缺陷） |
| `application-local.yml` YAML 解析 | ✅ 新配置读出 |
| 前端 `read_lints`（6 个改动文件） | ✅ 0 error / 0 warning |
| `npm run type-check`（vue-tsc） | ❌ **仍跑不了**：`node_modules` 顶层 `vue`/`vue-tsc`/`typescript` 链接未建（并行会话 pnpm install 链接阶段未完成），报 `MODULE_NOT_FOUND vue-tsc/bin/vue-tsc.js`。待链接完成后补跑 |
| 端到端（前端 → Java → Python → ES） | ❌ **未验证**：实测 ES `:9200`、topic-py `:8080/7091`、display `:7099` 当时均 DOWN；vite `:3000` 与 show-py `:8082` 存活 |

**要跑通端到端需要**：起 ES（含 `gkx_enterprise` / `gkx_svc_org` 索引）→ `lumen-topic-py` 下 `uvicorn gkx_search_service.main:app --port 8080` → 重启 display（`local` profile，已配直连）→ 页面输入关键词验候选、并断 ES 验降级文案。

### 9.4 待裁定 / 后续

1. **X-004 `structure_escalation`**：科研机构 / 人才 / 论文 / 专利 / 项目的对象级检索索引新建 + ETL 灌数仍需 `human:李伟` 批准；本轮未做。
2. **指标去 mock**：`M_INNOV_PATENT_INFLUENCE` / `M_INNOV_PROJECT_INFLUENCE` 的「算法已有」到「在线算法服务上线 / 展示端接真数」之间仍差 dwd 层与算法服务上线（§9.1 层级边界）；`metric-readiness-matrix-INNOV.yaml` 的 `d4` **未改绿**，需算法侧产物到位后由责任方更新。
3. `npm run type-check` 待依赖链接完成后补跑；端到端冒烟待服务起齐。

---

## 十、2026-11-03 补记：23 个新算法指标可支持性 + 11 要素重新连库复核

> 触发：`human:李伟` 2026-11-03 指定 23 个 `M_INNOV_*` 指标「看看有什么可以新支持的」+「11 个要素重新连库分析有没有可用的」+「久新库按在线文档看看有没有更新」。
> **性质**：只读核查 + 裁定建议，**零代码改动、零改绿、零 commit**。凭据来自 `_local/dw-docs/README.md`（私有、永不提交），未写入任何仓内文件。

### 10.1 在线文档版本（按 README §3.1 先跑 sync）

- 执行 `_local/dw-docs/sync.ps1`：本地记录 `6.30.0` → 远端最新 `6.30.0`，**结论「无更新」**（同步时间刷新为 2026-11-03 01:30）。
- 6.30.0 = 2026-10-31 版；仓内旧副本仍是 `2026-10-22-ADS_SCHEMA-5.11.0.md`，跨度 60 个版本，差异摘要已在 `DIFF-5.11.0-to-6.30.0.md`（本轮复核，无新增段落需补）。
- 6.30.0 §24.10「当前缺失数据项」**仍列「顶级会议/期刊名单」**（缺 Venue 稳定 ID/级别/学科/有效期/来源版本）——与库侧一致，见 §10.3。

### 10.2 久新库实测（47.93.119.170:29030 / `gkx_technology_analysis_dev` / test2 只读）

- `SELECT VERSION()` = `5.7.99`（Doris）；`SHOW TABLES` = **216 张，全为 `ads_`**（与 2026-11-02 `LIBRARY-PROBE` 一致，无新增表）。只读账号无 `information_schema` 权限。
- 11 要素按表名关键词命中：`scholar/talent` 47、`institution` 34、`topic/research_problem` 70、`project` 5、`paper` 8、`patent` 31、`result/outcome` 17；**`meeting/conference/venue` 0、`journal` 0、`service/svc/cms` 0、`enterprise` 0**。
- 全库列名扫描：含 `conference/journal/venue/publication_type` 的表**仅 2 张且都不可用作真源**——`ads_research_outcome_profile` 的 `simulated_journal_impact_factor`（6.29/6.30 明标 `AI_ESTIMATED_NOT_BACKTESTED` 模拟）、`ads_talent_research_achievement.venue`（对象级成果附属字段）。`ads_paper_profile` 38 列里只有 `paper_type` / `primary_source_id`，**无会议/期刊类型区分列**。
- 关键对象级表实测行数：`ads_paper_profile` 4,000,000、`ads_patent_profile` 1,768,955、`ads_project_profile` **1,838,841**、`ads_talent_profile` 100,000、`ads_institution_profile` 83,745、`ads_research_outcome_profile` 342、`ads_geo_yearly_metrics` 171,736、`ads_research_problem_region_yearly_metrics` 156,613、`ads_research_outcome_institution` 1,220。
- 结论：**3 个 mock 要素（期刊/会议/服务机构）在 6.30.0 库里依然零真源**，`SITUATION-ENT-D3-L01` / `INFLUENCE-FIX-L01` 的去 mock 接替条件（§9.2 台账）**未达成，维持 mock 不改绿**。但 `paper/patent/project/talent/institution/outcome` 的**对象级明细表可用**，为 X-004 关键词检索扩类目提供了「不新建索引」的第二条路（见 §10.4 待裁定 3）。

### 10.3 三方 `gkx` 原始库实测（183.240.141.251:3318 / gkx_reader_zp / dwd）

- 280 张表**全为 `dwd_*`，零 `ads_*`**；与久新 ADS 是两个不同库，不可混用。
- 11 要素相关：`dwd_zh_paper`/`dwd_en_paper`(19)、`dwd_patent*`(15)、`dwd_scholar*`(8)、`dwd_zh_project`/`dwd_en_project`(7)、`dwd_zh_journal`/`dwd_en_journal`(2)、`dwd_event`(1)、`dwd_news_base`/`dwd_policy_base` 等齐备；**`dwd_conference*` 零命中**（与算法库 `M_INNOV_CONFERENCE_INFLUENCE` 判「完全不支持」互为印证）。
- 该库是 23 个算法 precompute 产物的取数源（多数 `db: gkx@183.240.141.251:3318`），非展示侧直连对象。

### 10.4 23 个指标可支持性分级（算法库 `data/precompute/` + `innov/metrics/catalog.py`）

xlsx 分布：「科技专题算法库」sheet 23/23、「科技展示系统」15/23、「科技专题系统」4/23；catalog.py 104 条中 23 条全登记；**23/23 均有 `precompute/*.json`**（manifest `E-METRIC-ALGOLIB-LAUNCH-L01 阶段2`，2026-10-25 烘焙）。但产物 ≠ 可消费真值，按 `data_support_level` 分三档：

| 档 | 指标 | 可否新支持 |
|---|---|---|
| **A 完全转换支持 / 有可消费分值或榜单** | `M_INNOV_SCHOLAR_INFLUENCE`（21316 学者 + Top + tiers）、`M_INNOV_JOURNAL_INFLUENCE`（2796 中文刊）、`M_INNOV_ENTERPRISE_INFLUENCE`（top20）、`M_INNOV_ORG_INFLUENCE`（top25）、`M_INNOV_PROJECT_INFLUENCE`（58453 项评分 + 年度序列）、`M_INNOV_PATENT_INFLUENCE`（样本级分布）、`M_INNOV_EVENT_IMPORTANCE`（分档 + by_year）、`M_INNOV_DS_01_EVENTS_001/002`（stats + top10）、`M_INNOV_DS_FACTORS_014/015`（top10）、`M_INNOV_FACTOR_CLUSTER` / `M_INNOV_DS_FACTORS_016`（clusters 4）、`M_INNOV_FACTOR_FORECAST`（论文/项目 Holt 序列 + 回测） | 前 6 个已接影响力 Tab 或可作**新增「项目（含课题）影响力」卡**；后 5 个是**趋势预测 / 异常 / 聚类 / 事件** 的候选真源，但见下方口径限制 |
| **B 部分支持但无直接可消费数列**（审计/参数型产物） | `M_INNOV_DS_FACTORS_012`（对齐 project）、`M_INNOV_DS_FACTORS_018`（对齐 forecast）、`M_INNOV_DS_FACTORS_019` / `M_INNOV_FACTOR_ANOMALY`（~60KB 多模式参数，未见结果榜） | 需先解析 `modes/recommended_mode` 再定，**不直接出数** |
| **C 完全不支持（探针/判否产物，禁止出数）** | `M_INNOV_CONFERENCE_INFLUENCE`、`M_INNOV_DS_FACTORS_008`（会议）、`M_INNOV_EVENT_ATTENTION`、`M_INNOV_EVENT_INFLUENCE`、`M_INNOV_DS_01_EVENTS_003` / 重要性等级（`dwd_event` 仅 20 行、10 必需字段 0 存在） | **不能新支持**；会议/事件类缺口是数据侧（无会议实体、无事件流），非页面能解 |

**必须随产物一起披露的口径限制**（否则会把「有产物」误读成「可上线」）：
- 会议：`conference_entities=0`，`dwd_zh_journal` 是期刊名录且 `publication_type` 全为「期刊」，`ads_paper_profile` 无会议区分列 → 会议影响力/会议趋势**无序列可建**。
- 趋势预测 `M_INNOV_FACTOR_FORECAST`：seed 要求会议/项目/专利/期刊四类，**实际仅论文(16 期)、项目(13 期)可做 Holt**；专利 6 期 <8 期门槛且 2017–2020 零行不得补 0；期刊/会议无年度件数；论文 2024 为入库批（实测 32,379 远超 80% 区间）已排除。判「部分支持」。
- 专利影响力：被引副表 2 万件按 `pn` 只对上 355 件 = 语料 **0.0121%**，只能样本级分布，不能全库排名。
- 事件类：`dwd_event` 20 行 / 2 天 / 医药论坛名录，不是科创事件流；`M_INNOV_DS_01_EVENTS_003` 明写「禁止用新闻/政策串伪事件」。
- 聚类 `M_INNOV_FACTOR_CLUSTER` 产物含 `conference_gap` 字段，即自认会议维缺。

### 10.5 对既有裁定的影响（**均未擅自变更**）

| 既有裁定 | 本轮复核 | 建议 |
|---|---|---|
| 趋势预测 `TREND-FEAT-L01` 维持 backlog | 现在**有** `M_INNOV_FACTOR_FORECAST` 产物，但只覆盖论文/项目 2/4 类且带入库批陷阱 | 可从「数据不具备」改为「数据部分具备、待裁定是否做窄口径（仅论文+项目）」；**仍需你拍板**，未改 registry |
| 异常监测 / 聚类 | 有产物（clusters 4 / 多模式参数），但 `d4=mock`、无在线服务 | 同上，待裁定 |
| 影响力 Tab「项目卡缺位」 | `M_INNOV_PROJECT_INFLUENCE` 产物最实（58,453 项评分 + 年度序列），且 xlsx「科技展示系统」sheet 有 `M_INNOV_DS_FACTORS_012 要素影响力（项目/课题）` | **最值得新支持的一项**：可新增「项目（含课题）影响力」卡；但需先定产品口径与 `d4` 归属，未接线 |
| 会议/期刊/服务机构去 mock | 6.30.0 文档 §24.10 + 库侧双侧确认仍无源 | 维持 mock，不改绿 |
| X-004 关键词检索扩类目 | 之前只复用 `gkx_enterprise` + `gkx_svc_org` 两个 ES 索引；本次发现久新 ADS 有 5 张对象级明细表（paper/patent/project/talent/institution 共 ~770 万行） | 提供「走久新只读通道直查对象级表」的**第二条路**，可绕开 `structure_escalation` 新建索引；但 A3 裁决要求久新访问只走 `gkx_show_service/jiuxin.py`、且该通道现仅 2 个端点 → **需裁定是否新开检索端点**，未做 |

### 10.6 待裁定 / 未做（如实）

1. 上述 4 项裁定（趋势窄口径、项目影响力卡、异常/聚类、久新直查扩类目）**全部停在建议**，未改 registry 状态、未改 `d4`、未动任何代码。
2. 23 个指标 `d4` 在 `metric-readiness-matrix-INNOV.yaml` 仍全为 `mock`「算法服务未上线」；precompute 是离线静态快照经通用 `/compute` 壳返回，非在线服务，层级边界同 §9.1。
3. 久新 ES `:9200` / search-py `:8080` 本地 DOWN；本次连库为直连远端只读库，未起服务、未做端到端。
4. `_local/dw-docs/` 不在任何 git 仓内；`VERSION.txt` 因 sync 刷新了时间戳，内容仍 `6.30.0`（无实质变更）。



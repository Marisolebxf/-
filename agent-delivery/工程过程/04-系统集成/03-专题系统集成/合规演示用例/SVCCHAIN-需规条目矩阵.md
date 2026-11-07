# SVCCHAIN-需规条目矩阵（产业服务链分析 · 24 基准 + 3 补充行）

> **任务**：`SVCCHAIN-DC-M1-USM-L01`（长任务总控 `SVCCHAIN-合规演示用例-长任务总控.md` 段 M1；agent=product-agent；监管人=human:徐滕强；强度=ponytail off 定义轨）
> **日期**：2026-11-07
> **条目清点结论**：**27 行 = 24 基准行 + 3 补充行**。24 基准 = 专题服务系统 §1.1.1.2.4.2.7 的 16 个三级项（7.1.1–7.8.2）+ 门户 §33 的 8 个编号项（97–104）。补充 3 行 = §33 的 33.2/33.3/33.4 三个**无编号二级叶项**——依据见 §3「条目清点对照」，不补则这三条例需规在矩阵无行，违反总控「需规条目 100% 落行」门。

---

## 1. 需规真源与编号口径

| 真源 | 内容 | 本矩阵取法 |
|---|---|---|
| `bid-reference/科技信息展示系统和科技专题服务系统.md` §1.1.1.2.4.2.7（L5031–5158） | 产业服务链分析 8 个二级功能 × 各 2 个三级项 = **16 个三级项** | 序号 7.1.1–7.8.2，一行一条 |
| `bid-reference/智慧服务门户系统-要素相关.md` §1.1.1.1.1.1.1（L420–486，「专题服务」） | 门户 5 个二级项：全球服务机构概况 / 服务机构产业分布 / 服务机构区域分布 / 服务机构技术能力 / 深圳产业服务介绍；其中概况与深圳介绍下含 **8 个编号子项** | 编号 97–104（coverage-matrix-E7E8 既定口径） |
| `bid-reference/srs/01-智慧服务门户系统/集群服务/科技专题服务.md`（seq 88–92，excel_row 91–95） | 同上五项的 SRS 结构化版 | 交叉验证用（97–104 为 Excel 行内子项编号，非 srs seq） |
| `bid-reference/srs/04-科技专题服务系统/科技专题战略分析/产业服务链分析.md`（seq 117–132，excel_row 120–135） | 16 个三级项 SRS 结构化版 | 交叉验证用 |

> **编号勘误登记**：任务书称「§1.1.1.1.1.1.1.33（展示系统『专题服务』）」。主 bid 文件《科技信息展示系统和科技专题服务系统.md》**无**智慧服务门户章节（该文件只含展示系统 §1.1.1.1 与专题服务系统 §1.1.1.2）；「§33」编号与「97–104」子项号是团队 `coverage-matrix-E7E8-专题战略分析重跑.md` 对 Excel 需规行的既定引用口径，bid 原文真源 = `智慧服务门户系统-要素相关.md` §1.1.1.1.1.1.1 + `srs/01-智慧服务门户系统/集群服务/科技专题服务.md`。矩阵按此登记出处，不改团队引用习惯。

## 2. 需规条目矩阵（27 行）

> 列说明：**页面与路由** = as-built 实勘锚点（`qa/as-built/scripts/KJZTFWXT/service/{域}/coverage.md` + `demo-ui-topic/src/app/routes.tsx`）；**USM 引用** = `US-SVC-*` 故事号（五件套追溯主键）；**入口动作** = 用户到达并产出该条目结果的操作串；**条件枚举** = 每项标真源出处，禁止臆造值。

### 2.1 ORG 域 · 服务机构分析（7.1–7.3，6 行）

| 需规序号 | 需规名（bid 原文短名） | 域 | 页面与路由（as-built 锚点） | USM 引用 | 入口动作 | 输入或选择条件枚举（真源出处） | 关联指标 M_SVC_* | 关联 Q/GAP |
|---|---|---|---|---|---|---|---|---|
| 7.1.1 | 服务机构产业领域覆盖分析 | ORG | `/service/institution-judgment?workspace=field&tab=coverage`（as-built `org-field/` P0-01 直达；routes.tsx L314） | US-SVC-ORG-01、US-SVC-ORG-02 | 菜单「服务机构产业领域分析」→ 打开对比篮 picker 组装机构集合 → 选产业上下文 → 「开始分析」 | ① 产业集群下拉 15 项（`src/app/lib/industryCluster/seed.ts` `CLUSTER_SEED`：新一代信息技术…未来健康；默认=目录第一个集群第一个 L0，Q-SVCCHAIN-09 临时默认）；② 机构集合 1~50 家，经系统对比篮 `service_org` 勾选（USM US-01；篮上限 `compareBasketStore.ts` `COMPARE_BASKET_MAX_ITEMS_PER_TYPE=50`） | M_SVC_ORG_COVERAGE_BREADTH、M_SVC_ORG_COVERAGE_DEPTH、M_SVC_ORG_SELECTED_COUNT（TRACE-ORG metric_registration） | Q-SVCCHAIN-02（深度 draft）、Q-SVCCHAIN-09（产业过滤口径） |
| 7.1.2 | 服务机构产业领域分析结果呈现 | ORG | 同 7.1.1 路由（覆盖页签内图型切换；as-built `org-field/`） | US-SVC-ORG-02 | 覆盖结果页切换「热力图 / 矩阵图」（AC-US-SVC-ORG-02-01~03） | 图型 2 选 1：热力（机构×领域，色阶=深度五档）/ 矩阵（X=广度，Y=平均深度 0-100，四象限）；USM US-02 主路径 2 | M_SVC_ORG_COVERAGE_DEPTH | Q-SVCCHAIN-02 |
| 7.2.1 | 趋势可视化呈现 | ORG | `/service/institution-judgment?workspace=trend&tab=trend`（as-built `org-trend/`；routes.tsx workspace=`trend`） | US-SVC-ORG-04 | 菜单「服务机构新增趋势分析」→ 选主领域（可加对比领域）→ 「开始分析」 | ① 主领域 + 对比领域合计 ≤3 条曲线（USM US-04 主路径 1）；② 时间窗 3 档=近 3 年/近 5 年/近 8 年（`TrendView.tsx` L120-122 Select options） | M_SVC_ORG_NEW_COUNT | — |
| 7.2.2 | 市场热度判断 | ORG | 同 7.2.1 路由（趋势结果页研判面板；as-built `org-trend/`） | US-SVC-ORG-05 | 趋势分析完成 → 结果页研判面板读星级与依据行 | 演示规则：近段斜率+波动特征 → 热度评级分档（🧪）；序列 <3 年或全 0 不判（USM US-05 异常行） | M_SVC_ORG_MARKET_HEAT（D1 missing） | Q-SVCCHAIN-02；GAP-SVC-ORG-HEAT（as-built） |
| 7.3.1 | 多维度评价模型 | ORG | `/service/institution-judgment?workspace=capability&tab=capability`（as-built `org-capability/` P0-01 capability 深链） | US-SVC-ORG-06 | 菜单「服务机构技术力评估分析」→ 配置五维启停/权重（合计 100%）→ 从对比篮带入 2~5 家 → 「开始评估」 | ① 内置五维=专利数量/研发投入/核心专家/成功案例/标准制定（`serviceCenterData.ts` `CAPABILITY_DIM_DEFS`，对齐 bid 7.3.1 列举）；② 自定义维度候选 3=人才生态/市场商业化/湾区开放（同文件 `CUSTOM_DIM_CANDIDATES`）；③ 权重 0-100 整数、合计≠100 禁评估+按比例归一（USM US-06） | M_SVC_ORG_TECH_SCORE | Q-SVCCHAIN-01 |
| 7.3.2 | 自定义对比分析 | ORG | 同 7.3.1 路由（排名列表/雷达图结果区；as-built `org-capability/`） | US-SVC-ORG-06 | 「开始评估」出排名列表（可切雷达图）；对比对象唯一入口=对比篮导入（`source=compare-basket` + `org_ids[]`） | ① 对比机构 2~5 家（USM AC-06-02）；② 雷达维度轴=当前启用维度动态跟随（AC-06-04）；③ 归一基准=对比集合内最大值（Q-SVCCHAIN-01 演示口径） | M_SVC_ORG_TECH_SCORE | Q-SVCCHAIN-01 |

> ORG 域检索前置（非招标条目，R2B 用户口径产物）：服务机构查询 `/service-center/search`（as-built `search/`，23 用例 1:1 蓝本 01328~01350），三模式=关键词/智能检索/高级筛选；高级筛选字段库=`serviceOrgSearchData.ts` `SERVICE_ORG_FIELD_LIBRARY`（基本信息 5 字段/服务领域 1 字段/技术能力 5 字段）。作为 7.1.1/7.3.1 的机构发现入口，在 M3 用例主路径中作为前置步骤串写。

### 2.2 ECO 域 · 服务链生态（7.4/7.5/7.8，6 行）

| 需规序号 | 需规名（bid 原文短名） | 域 | 页面与路由（as-built 锚点） | USM 引用 | 入口动作 | 输入或选择条件枚举（真源出处） | 关联指标 M_SVC_* | 关联 Q/GAP |
|---|---|---|---|---|---|---|---|---|
| 7.4.1 | 全链路可视化呈现 | ECO | `/service/chain-analysis?workspace=chain&tab=chain`（as-built `chain-shortboard/` P0-01 直达；routes.tsx L313） | US-SVC-ECO-01 | 菜单「服务链生态分析·服务链短板分析」→ 选产业集群 → 「开始分析」 | ① 产业集群 15 项（`industryCluster/seed.ts`）；② 服务链六环节字典=研发与科研合作/知识产权与标准/技术转移与孵化/中试熟化/检测认证/市场化服务（`serviceEcosystemData.ts` L21 `CHAIN_STAGES`，CT-SVC-PT-01 唯一来源） | M_SVC_CHAIN_SEGMENT_ORG_COUNT、M_SVC_CHAIN_SEGMENT_AVG_DEPTH（TRACE-ECO） | Q-SVCCHAIN-02（环节平均深度 1A 挂起）、Q-SVCCHAIN-08；GAP-SVC-CHAIN-SEGMENT |
| 7.4.2 | 瓶颈堵点智能识别 | ECO | 同 7.4.1 路由（链路图高亮 + 识别面板；as-built `chain-shortboard/`） | US-SVC-ECO-02 | 分析完成 → 链路图高亮 + 识别面板逐条读判定与依据行 | 演示规则三判定：环节机构数 0→服务空白（红）、≤1→薄弱（橙）、平均深度<55→瓶颈（橙）（`客户决策清单跟踪表.md` Q-SVCCHAIN-03 临时默认；USM US-02 主路径 1） | M_SVC_CHAIN_BOTTLENECK（D1 missing） | Q-SVCCHAIN-03；GAP-SVC-CHAIN-BOTTLENECK |
| 7.5.1 | 关系网络构建 | ECO | `/service/chain-analysis?workspace=graph&tab=graph`（as-built `chain-graph/` P0-01 直达 graph/tab=graph） | US-SVC-ECO-03 | 图谱页签 → 选产业 → 模式确认 → 「开始分析」 → 图上过滤器探索 | ① 关系类型 4=投资/合作/竞争/人才流动（USM US-03 主路径 1）；② 节点主体=服务机构+企业/高校/资本（三类关联主体）；③ 聚焦=1 度邻域（AC-03-03） | —（TRACE-ECO REQ-SVC-ECO-GRAPH-BUILD metrics=[]，图谱为确定性演示数据集） | — |
| 7.5.2 | 图谱探索与统计 | ECO | 同 7.5.1 路由（统计面板 + 节点下钻；as-built `chain-graph/`） | US-SVC-ECO-04 | click 服务机构节点开画像抽屉（复用 R1 `OrgProfileDrawer`）；统计面板随过滤重算 | 统计三件：网络密度=2E/(N(N-1))（AC-04-02 标准公式）、度中心性 TOP5、生态影响力评分（D1 missing 不输出伪值，AC-04-04）；子网 <2 节点不算统计值 | M_SVC_GRAPH_DENSITY、M_SVC_GRAPH_CENTRALITY、M_SVC_GRAPH_INFLUENCE（D1 missing） | Q-SVCCHAIN-03；GAP-SVC-GRAPH-INFLUENCE |
| 7.8.1 | 深圳服务链现状分析·统一评价框架 | ECO | `/service/chain-analysis?workspace=shenzhen&tab=shenzhen`（as-built `sz/` P0-01 直达深链） | US-SVC-ECO-05 | 深圳现状页签 → 框架说明卡读指标构成与就绪度 | 对比指标 3 项=服务机构数量/平均技术力得分/服务网络密度（`serviceEcosystemData.ts` L180 `SZ_COMPARE_METRICS`）；服务链完整度 D1 missing 诚实排除不渲染（AC-05-02） | M_SVC_SZ_CHAIN_COMPLETENESS（1A 挂起） | Q-SVCCHAIN-04；GAP-SVC-SZ-CHAIN-COMPLETENESS；as-built `sz/` P0-13 另挂 Q-SVC-010/Q060/Q062 待确认角标 |
| 7.8.2 | 横向对比分析 | ECO | 同 7.8.1 路由（对比柱状图 + 梯队仪表盘；as-built `sz/` P0-13） | US-SVC-ECO-06 | 选对比指标（多选，默认全选可用项）→ 读五城市柱状图与梯队仪表盘 | ① 对比城市固定 5=深圳/全国平均/北京/上海/广州（`serviceEcosystemData.ts` L159 `COMPARE_CITIES`）；② 对比指标多选=框架 3 项（L180）；③ 城市基准值=确定性演示数据（L187 `CITY_METRIC_VALUES`；Q-SVCCHAIN-04 锁定深圳机构数跟圈定值） | M_SVC_SZ_COMPARE_METRIC、M_SVC_SZ_TIER | Q-SVCCHAIN-04、Q-SVC-010（深圳圈定） |

### 2.3 REC 域 · 机构招引培育（7.6/7.7，4 行）

| 需规序号 | 需规名（bid 原文短名） | 域 | 页面与路由（as-built 锚点） | USM 引用 | 入口动作 | 输入或选择条件枚举（真源出处） | 关联指标 M_SVC_* | 关联 Q/GAP |
|---|---|---|---|---|---|---|---|---|
| 7.6.1 | 招引模型与指标 | REC | `/service/institution-decision?workspace=attract&tab=attract`（as-built `rec-attract/` P0-01 深链双 Tab；routes.tsx L315） | US-SVC-REC-01 | 菜单「机构招引培育·引入服务机构推荐分析」→ 调四指标权重（可恢复默认/按比例归一） | ① 四指标=产业匹配度/技术领先性/发展潜力/对外合作意愿（`serviceRecommendData.ts` L10 `ATTRACT_INDICATORS`，对齐 bid 7.6.1）；② 默认权重 35/30/20/15（`serviceRecommendModel.ts` `DEFAULT_ATTRACT_WEIGHTS`）；③ 权重 0-100、合计≠100 禁生成（USM US-01） | M_SVC_REC_ATTRACT_SCORE | Q-SVCCHAIN-05 |
| 7.6.2 | 推荐名单生成 | REC | 同 7.6.1 路由（名单结果区 + 导出；as-built `rec-attract/`） | US-SVC-REC-02 | 选重点产业方向 → 「生成推荐名单」 → 导出 CSV | ① 重点产业方向=产业集群下拉 15 项（`ServiceRecommendPage.tsx` L520「重点产业方向」+ seed.ts）；② 名单列=名次/机构/所在地/服务环节/四指标分/综合分/推荐理由（L694 导出表头）；③ 部分 L0 无挂链数据→诚实空态（Q-SVC-011：INB1303/1306/1333 共 0 行） | M_SVC_REC_ATTRACT_SCORE、M_SVC_REC_CANDIDATE_CNT（不写 ADS） | Q-SVCCHAIN-05、Q-SVC-011 |
| 7.7.1 | 培育模型与筛选 | REC | `/service/institution-decision?workspace=cultivate&tab=cultivate`（as-built `rec-cultivate/` P0-01 直达；P0-20 兄弟工作区隔离） | US-SVC-REC-03 | 切培育页签 → 设机构类型/服务环节筛选 → 「生成培育名单」 | ① 机构类型多选 3=高校/科研院所/企业（`ServiceRecommendPage.tsx` L897-901 `ALL_ORG_TYPES`）；② 服务环节多选=机构主数据 segment 全集（L910 `allSegments()`，上游·研发…下游各环节）；③ 培育四维=现有规模/技术创新能力/服务成效/市场缺口（`CULTIVATE_DIMS` L20），默认权重 **25/30/25/20**（`serviceRecommendModel.ts` L31 `DEFAULT_CULTIVATE_WEIGHTS`；⚠️ 见 §3 勘误 2）；④ 筛选全空禁生成（L925） | M_SVC_REC_CULTIVATE_SCORE | Q-SVCCHAIN-05、Q-SVCCHAIN-08（培育筛领域） |
| 7.7.2 | 培育名单与建议 | REC | 同 7.7.1 路由（名单 + 建议标签 + 画像下钻；as-built `rec-cultivate/`） | US-SVC-REC-04 | 名单行下钻画像抽屉 / 加入对比篮 / 导出 CSV | ① 建议标签 3=资金支持/市场对接/人才引进（USM US-04 主路径 2，规则生成🧪）；② 名单仅含深圳本土在库机构（AC-04-01）；③ 展开行建议文本引用该行维度短板数值（AC-04-02） | M_SVC_REC_CULTIVATE_SCORE、M_SVC_REC_CANDIDATE_CNT | Q-SVCCHAIN-05、Q-SVC-011 |

### 2.4 PT 域 · 门户专题服务（§33，8 编号行 + 3 补充行）

| 需规序号 | 需规名（bid 原文短名） | 域 | 页面与路由（as-built 锚点） | USM 引用 | 入口动作 | 输入或选择条件枚举（真源出处） | 关联指标 M_SVC_* | 关联 Q/GAP |
|---|---|---|---|---|---|---|---|---|
| 97 | 服务机构数量分析（全球概况·数量） | PT | `/service-portal/overview`（as-built `portal/` P0-01 goto /service-portal；index 重定向 overview，routes.tsx L331-335） | US-SVC-PT-01 | 门户默认落地全球概况页；读 KPI 三项 + 数量分析区趋势折线 | ① KPI=全球总数/本年新增/覆盖领域数（全库口径不随交互变，AC-PT-01-01）；② 趋势年份轴=2018-2025（`servicePortalData.ts` `PORTAL_YEARS`/`GLOBAL_TOTAL_TREND` 8 点）；本年新增=相邻年差（Q-SVCCHAIN-06 侯佳伟锁定口径） | M_SVC_PT_GLOBAL_TOTAL | Q-SVCCHAIN-06、Q-SVCCHAIN-07（全球名录抽不出，暂写国内圈定值+「目前只有国内数据」提醒） |
| 98 | 服务机构类型分析（全球概况·类型） | PT | 同 97 路由（类型环形区） | US-SVC-PT-01 | 全球概况页读类型环形占比图 | 类型字典 3=高校/科研院所/企业（`serviceCenterData.ts` `OrgType`，与机构主数据同源；`GLOBAL_TYPE_DIST` 合计=全球总数） | M_SVC_PT_GLOBAL_TYPE_DIST | Q-SVCCHAIN-06（分档字典；侯佳伟 1A2A3B 同池出三类环图） |
| 99 | 服务机构规模分析（全球概况·规模） | PT | 同 97 路由（规模条形区） | US-SVC-PT-01 | 全球概况页读规模四档条形分布 | 规模四档=50 人以下/50-200 人/200-500 人/500 人以上（`servicePortalData.ts` L42 `GLOBAL_SCALE_DIST`；0 值档保留） | M_SVC_PT_GLOBAL_SCALE_DIST | Q-SVCCHAIN-06（人数=年报 `employees_number` 补数，锁 A 总则） |
| 100 | 深圳产业服务机构数量 | PT | `/service-portal/shenzhen`（as-built `portal-shenzhen/`；portal 内经页头「深圳产业服务介绍」页签进入，FUNC-05288） | US-SVC-PT-05 | 深圳介绍页签 → 顶部 KPI + 数量区趋势折线 | 深圳 KPI 三项（深圳口径）；历年趋势轴同 PORTAL_YEARS（`SZ_TOTAL_TREND`）；本年新增=相邻年差 | M_SVC_PT_SZ_TOTAL | Q-SVCCHAIN-06（深圳=圈定 `city` 深圳）、Q-SVC-010（圈定准入待甲方） |
| 101 | 产业机构类型统计（深圳） | PT | 同 100 路由（类型环形区） | US-SVC-PT-05 | 深圳介绍页读类型占比环形 | 类型 3 同 98（`SZ_TYPE_DIST`，合计=深圳总数） | M_SVC_PT_SZ_TYPE_DIST | Q-SVCCHAIN-06 |
| 102 | 产业机构产业领域分布（深圳） | PT | 同 100 路由（领域×环节矩阵条形区） | US-SVC-PT-05 | 深圳介绍页读领域分布矩阵条形（hover 机构数） | ① 产业轴=15 个产业集群；② 环节轴=六环节 `CHAIN_STAGES`（CT-SVC-PT-01 复用，禁另造第七档）；领域×环节计数字典=分析侧同源（Q-SVCCHAIN-08：无源列，六环节切不开为已登记缺口） | M_SVC_PT_SZ_FIELD_DIST | Q-SVCCHAIN-06、Q-SVCCHAIN-08 |
| 103 | 产业机构区域分布（深圳） | PT | 同 100 路由（十区地图 + 区排名列表） | US-SVC-PT-05 | 深圳介绍页读深圳各区地图圆点与排名列表 | 深圳十区字典全集含 0 值区：南山/福田/龙岗/宝安/龙华/光明/坪山/罗湖/大鹏新区/盐田（`servicePortalData.ts` L147 `SZ_DISTRICT_DIST`） | M_SVC_PT_SZ_REGION_ORG | Q-SVCCHAIN-06（区域归属口径）、Q-SVC-004（`district` 直字段已 🟢） |
| 104 | 重点产业服务机构 | PT | 同 100 路由（页尾重点板块卡片墙 → 详情抽屉；as-built `portal/` P1-06 非法 orgId 分支） | US-SVC-PT-06 | 点击重点机构卡片 → 四板块详情抽屉（KeyOrgDetailDrawer）；可「进入分析侧画像」/「加入对比篮」 | ① 遴选口径=技术力综合分 Top（演示态明示）；② 四板块=机构概况/当前规模/业务服务领域/业务分布区域（bid 104 列举；扩展档案 `KEY_ORG_PROFILES`：领导人/人数/年营收/业务点位占比） | M_SVC_PT_KEYORG_SCALE（+领域深度条挂 M_SVC_ORG_COVERAGE_DEPTH） | Q-SVCCHAIN-06（遴选参数未定） |
| *33.2* | *服务机构产业分布（结合产业链全景图）* | PT | `/service-portal/industry-distribution`（as-built `portal-industry/` FUNC-04988 深链） | US-SVC-PT-02 | 门户子导航切页 → 产业选择器（集群可选 L0）→ 环节条形/链路图 → 点环节展开代表机构 | ① 产业选择器=15 集群级联、可选到 L0；**禁止**自动带第一个 L0；无映射空态「无相关产业数据」（`resolveScope.ts` `UNMAPPED_CLUSTER_MESSAGE`）；② 六环节字典同 7.4.1（CHAIN_STAGES） | M_SVC_PT_CHAIN_NODE_ORG | Q-SVCCHAIN-06、Q-SVCCHAIN-08 |
| *33.3* | *服务机构区域分布（全球/全国地图）* | PT | `/service-portal/region-map`（as-built `portal-region/` FUNC-05088 深链） | US-SVC-PT-03 | 页签切换「全球分布 / 全国分布」→ 地图圆点 + 右侧排名列表 | 页签 2 级=全球/全国（默认全球，USM US-03 主路径 1）；Leaflet 比例圆点，点选联动列表高亮；全国页签附「进入深圳介绍」分流 | M_SVC_PT_REGION_ORG | Q-SVCCHAIN-06、Q-SVCCHAIN-07（现网仅国内/广东，国家行不造） |
| *33.4* | *服务机构技术能力（各产业 Top30）* | PT | `/service-portal/capability-rank`（as-built `portal-capability/` FUNC-05188 深链） | US-SVC-PT-04 | 产业页签切换 → Top30 榜单（行内入篮/下钻详情） | ① 产业页签=15 集群；无映射诚实空态不偷选有数产业；② 榜单 Top30（在库不足时诚实标注「在库 N 家，按实际数展示」）；③ 口径=分析侧五维**等权（各 20%）** `computeEvaluation` 同源（CT-SVC-PT-03 禁第二套口径） | M_SVC_ORG_TECH_SCORE（复用） | Q-SVCCHAIN-01 |

## 3. 条目清点对照（handoff 必读）

### 3.1 基准对照结论：27 行 = 24 + 3

| 清点项 | 基准 | 实点 | 差额 | 依据 |
|---|---|---|---|---|
| §1.1.1.2.4.2.7 三级项 | 16 | 16（7.1.1/7.1.2/7.2.1/7.2.2/7.3.1/7.3.2/7.4.1/7.4.2/7.5.1/7.5.2/7.6.1/7.6.2/7.7.1/7.7.2/7.8.1/7.8.2，bid L5047–5158 逐级实点；srs seq 117–132 交叉一致） | 0 | — |
| §33 编号项 | 8 | 8（97/98/99 属 33.1；100/101/102/103/104 属 33.5；`智慧服务门户系统-要素相关.md` L430/L460 列举原文一致；USM-PORTAL §6 反向核对一致） | 0 | — |
| §33 无编号二级叶项 | （未计入基准） | 3（33.2 产业分布 / 33.3 区域分布 / 33.4 技术能力——bid 原文中它们是**自身为叶的二级项**，不含编号子项） | +3 | coverage-matrix-E7E8 §三门户段 = 11 行（8 编号 + 33.2/33.3/33.4），为团队既定口径；若砍掉则三条例需规无行、M3 PT 覆盖表缺行，违反总控「需规条目 100% 落覆盖表行」。故以补充行（*斜体*标注）并入矩阵 |

**M3 消费口径**：SVC-PT-合规演示用例覆盖表按 PT 域 **11 行**落（8 编号 + 3 补充），其余域按各表行数落；四域合计 27 行。

### 3.2 勘误与另发现（按总控铁律登记）

1. **「§1.1.1.1.1.1.1.33」出处勘误**：主 bid 文件《科技信息展示系统和科技专题服务系统.md》不含智慧服务门户章节；门户「专题服务」bid 原文真源 = `bid-reference/智慧服务门户系统-要素相关.md` §1.1.1.1.1.1.1（L420–486），SRS 结构化版 = `bid-reference/srs/01-智慧服务门户系统/集群服务/科技专题服务.md`（seq 88–92）。「§33 / 序号 97–104」是 `coverage-matrix-E7E8-专题战略分析重跑.md` 与 R2C 五件套的既定引用口径（Excel 需规行内子项编号），矩阵沿用该口径并在 §1 登记真源链，不另造编号。
2. **培育默认权重文档-代码不一致**：USM-SVCCHAIN-RECOMMEND v1.0 US-03 写「默认权重 20/30/25/25」（现有规模/技术创新/服务成效/市场缺口），代码真源 `serviceRecommendModel.ts` L31 `DEFAULT_CULTIVATE_WEIGHTS = { scale:25, innovation:30, effect:25, marketGap:20 }`（25/30/25/20），as-built `rec-cultivate/` P0-20 实测「权重读数 25/30/25/20」双证。**矩阵以代码+as-built 为准**；建议 M4 或后续定义修订任务同步 USM 文档（本任务不改五件套）。
3. **as-built GAP 真源**：`qa/as-built/scripts/KJZTFWXT/service/` 下已登记 5 枚 `GAP-SVC-*`：GAP-SVC-ORG-HEAT / GAP-SVC-CHAIN-SEGMENT / GAP-SVC-CHAIN-BOTTLENECK / GAP-SVC-GRAPH-INFLUENCE / GAP-SVC-SZ-CHAIN-COMPLETENESS（全为 D1 missing/挂起指标的环境/数据缺口），矩阵对应行已引用；M4 缺口总表归并时以这 5 枚 + Q-SVCCHAIN-01~09 + Q-SVC-004/010/011 为既有引用集合，不新造编号。
4. **无指标条目**：7.5.1（关系网络构建）在 TRACE-ECO 中 metrics=[]（图谱为确定性演示数据集，无注册指标），矩阵如实留空——M3 该行「关联指标」列写「—」，期望输出不引用指标 ⓘ。
5. **检索域与维护域不在 24 基准内**：服务机构查询（`/service-center/search`，R2B 用户口径产物）与维护管理（`/service/maintenance`，ENT-OPS 壳占位）均非招标 §2.4.2.7/§33 条目，不设矩阵行；前者作为 ORG 域用例主路径的机构发现前置步骤串写（见 §2.1 表下注），后者与合规演示用例无关。

### 3.3 四域分布小结

| 域 | 行数 | 路由锚点 |
|---|---|---|
| ORG（服务机构分析） | 6 | `/service/institution-judgment`（workspace=field/trend/capability）+ 检索前置 `/service-center/search` |
| ECO（服务链生态） | 6 | `/service/chain-analysis`（workspace=chain/graph/shenzhen） |
| REC（机构招引培育） | 4 | `/service/institution-decision`（workspace=attract/cultivate） |
| PT（门户专题服务） | 11（8 编号 + 3 补充） | `/service-portal/{overview,industry-distribution,region-map,capability-rank,shenzhen}` |
| **合计** | **27** | — |

### 3.4 Job 任务键附录（M3 主路径/LOOP 计划消费）

服务域分析 Job `taskType` 前缀与枚举（`demo-ui-topic/src/app/pages/service-center/{serviceOrgAnalysisFlow,serviceEcoAnalysisFlow,serviceRecommendAnalysisFlow}.ts`）：

| 域 | taskType 枚举 | 路由参数形态 |
|---|---|---|
| ORG | `service_org_coverage` / `service_org_trend` / `service_org_capability` | `/service/institution-judgment?workspace={field\|trend\|capability}&tab={同}&analysis_fp=…&analysis_view={processing\|result}&task_id=…` |
| ECO | `service_eco_chain` / `service_eco_graph` / `service_eco_shenzhen` | `/service/chain-analysis?workspace={chain\|graph\|shenzhen}&tab={同}&analysis_fp=svc\|{kind}\|…` |
| REC | `service_recommend_attract` / `service_recommend_cultivate` | `/service/institution-decision?workspace={attract\|cultivate}&tab={同}` |

同用户同条件只允许一条在跑、切页签复用已成功结果（`serviceAnalysisTaskLookup.ts` 按 `analysis_fp` 指纹查找），与产品实现规程附录 E 单飞约束一致。

---

*产物路径：`agent-delivery/工程过程/04-系统集成/03-专题系统集成/合规演示用例/SVCCHAIN-需规条目矩阵.md`；handoff：`agent-delivery/agent-handoffs/E7-产业服务链分析/SVCCHAIN-DC-M1-USM-L01.md`。本文件为 M3 四叶（ORG/ECO/REC/PT）覆盖表与 LOOP 计划的条目基准输入。*

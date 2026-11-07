ponytail: full

# TS-DS01-CASE-FILL-L01 · DS-01 合规演示用例条件与数据情况回填

> **日期**：2026-11-07　|　**执行**：data-agent　|　**任务**：TS-DS01-CASE-FILL-L01
> **修改对象**：`agent-delivery/工程过程/04-系统集成/05-展示系统集成/合规演示用例/TS-L2-DS01-合规演示用例.md`（16 行零缺格）、`展示系统-第一批-索引.md`（DS-01 行 + 更新记录）
> **性质**：只读探测 + 文档回填。**零代码改动、零 commit/push**。

## 一、探测记录（网关 `http://10.50.69.111:30895`，StripPrefix=1，无 token，curl.exe `--max-time 40`，全部只读 POST）

| # | 端点 + 参数 | 状态 | 关键返回 |
|---|---|---|---|
| P1 | `/map {}` | 200（11.0s，72.8KB） | factorItems=11、regions=9、objectPoints=99、scopeLabel=全量样本；regionCascadeOptions 含深圳 9 区/广州 11 区/惠州 5 区县/佛山禅城区等 |
| P2 | `/overview {}` | 200（4.7s） | stats=9、factorCards=9、domainRows=6、trendSeries（新增企业 2015—2025 共 12 年，currentYear=2026）、trendGranularity=year、isEmpty=false |
| P3 | `/events {}` | 200（1.3s） | events=34；日期 2025-01-01 ~ 2026-06-04 |
| P4 | `/timeline {}` | 200 | years=[2025,2026]、events=34（与 /events 同源，对齐表 §6.1 已测，本轮复核一致） |
| P5 | `/map {"enabledFactorKeys":["paper"]}` | 200 | 其余 10 要素 active=false（图层切换生效）；objectPoints=0（论文无对象级点位，与后端 notes「只出市域聚合值」一致） |
| P6 | `/map {"regionPaths":[["深圳市"]]}` | 200 | scopeLabel=城市：深圳市；regions=1；objectPoints=100；factorItems 切为深圳市口径（企业 95,525 / 论文 24,904 / 专家 6,462 / 项目 9,143 / 机构 113 / 课题 7 / 成果 227） |
| P7 | `/overview {activeRegionKey:"深圳市", timeRange 2023-2026, ...}` | 200 | 区域参数被接受（stats 结构同基线） |
| P8 | `/events {importanceFilter:"high"}` | 200 | events=1（2026-05-04 invest 战略投资，importanceScore=67.16）→ 重要性筛选生效 |
| P9 | `/events {eventTypeValues:["financing"]}` | 200 | events=9 全 financing → 类型筛选生效 |
| P10 | `/timeline {"timeRange":{2025,2026}}` | 200 | years=[2025,2026]、rangeLabel=2025-2026、events=34 |
| P11 | `/influence {全量条件}` | 200 | cards=5、totalCount=50,631、anyMock=true；技术产出 1,514（mock）/ 企业 16,416 / 机构 7,842 / 专家 21,316 / 服务项目 3,543（demo 冻结种子 mock） |
| P12 | `/cluster {selectedFactorKey:"enterprise"}` | 200 | presets=4（高影响力/高增长/高转化率技术/高合作密度）、scopedItems=200；「高增长」簇诚实空态（emptyReason：enterprise_base.revenue_growth_rate 整列 NULL） |
| P13 | `/compare {selectedFactorKeys:["enterprise","paper"]}` | 200 | series=2（企业/论文各 11 年值）、years=2015—2025、availableFactorKeys=[enterprise,paper,scholar,project,institution] |
| P14 | `/factors/search {"keyword":"深圳","limit":10}` | 200 但 degraded=true | items=[]、reason=「检索服务不可用，请稍后重试」（search-py:8080 DOWN，与 11-03 台账 §一 一致） |
| P15 | `/events {regionPaths:[["深圳市"]], currentYear:"2025", timeRange 2025-2025}` | 200 | events=23 全 2025 年；scopeLabel=大湾区 |
| P16 | `/events {currentYear:"2025", timeRange 2025-2025}`（不带区域，P15 对照） | 200 | events=23 全 2025 年 → **与 P15 完全相同，regionPaths 不被 /events 消费（事件无地域筛选能力）** |
| P17 | `/overview {granularity:"month", ...}` | 200 | trendGranularity=month（粒度切换生效）、scopeLabel=注册年：2023-2026 |
| P18 | `/map {"timeRange":{2020,2026}}` | 200 | 企业 187,643 → 51,379（注册年过滤生效）、objectPoints=100、scopeLabel=注册年：2020-2026 |

> 探测波折：PowerShell 内联 `-d "{...}"` 引号转义被吃掉导致 6 次 400（第 1 轮）；改用 body 文件 `-d "@file"` 后 18 次全 200。后继者注意：本环境一律用 body 文件方式。

## 二、条件可选项全集枚举结果（全部出自实测响应，零编造）

- **地域（regionPaths）**：9 市 = 深圳市 / 广州市 / 东莞市 / 惠州市 / 佛山市 / 中山市 / 江门市 / 珠海市 / 肇庆市；区级级联 = 深圳 9 区（宝安/龙岗/南山/龙华/福田/光明/罗湖/坪山/盐田）、广州 11 区、惠州 5 区县、佛山禅城区等（regionCascadeOptions 实测）。
- **要素（enabledFactorKeys，11 类全集）**：scholar 专家学者 159,546 / institution 组织机构 48,444（2025年）/ enterprise 企业 187,643 / topic 课题 11 / project 项目 392,032（2025年）/ paper 论文 858,620 / patent 专利 71,043 / result 成果 232 / journal 期刊 3,401 / service 服务机构 43,296 / meeting 会议 1,280（⚠️ 唯一 mock）。
- **时间（timeRange）**：年度区间 startYear/endYear 任意组合（实测 2020—2026 生效）；compare 年轴 2015—2025（2026 进行中年度不计入）；overview 趋势轴 2015—2025 + currentYear 2026；事件窗 2025-01-01 ~ 2026-06-04。**日/月粒度无接口参数**（granularity 仅 overview 趋势分桶用，year/month 实测生效）。
- **事件类型（eventTypeValues，11 类实测出现）**：fund_project 获批立项 7 / financing 融资 9 / bid 中标 5 / achievement 成果发布 3 / biz_dynamic 合作动态 2 / tech_break 技术突破 2 / industry_event 产业活动 2 / invest 投资 1 / talent_flow 人才流动 1 / award 获奖 1 / policy 政策 1。
- **重要性（importanceFilter）**：all / high / medium / low；实测全量分布 高 1 / 中 11 / 低 22；每条带 importanceLevel（1/2/3）+ importanceScore。
- **比较对象（selectedFactorKeys）**：可用全集 = enterprise / paper / scholar / project / institution（availableFactorKeys 实测）；专利/期刊/会议/课题/成果/服务机构无年度序列不出曲线。
- **聚类对象（selectedFactorKey）**：仅 enterprise 企业；4 簇 = 高影响力 / 高增长（空态）/ 高转化率技术 / 高合作密度。
- **检索（factors/search）**：keyword + limit≤20 + matchMode=fuzzy/exact；当前 degraded=true（检索服务不可用）。

## 三、16 行判定清单（可演 11 / 覆盖不到 5 / 未填 0）

| 行 | 界面 | 判定 | 一句话依据 |
|---|---|---|---|
| 1 | 放大/缩小 | 可演 | 纯前端 Leaflet 能力，无业务接口 |
| 2 | 拖动平移 | 可演 | 同上；点位有 /map 200 支撑 |
| 3 | 复位 | 可演 | 纯前端视图状态重置 |
| 4 | 要素搜索定位 | 覆盖不到 | /factors/search degraded=true（search-py DOWN） |
| 5 | 11 类图层开关 | 可演 | /map enabledFactorKeys 实测生效；会议 mock 明示 |
| 6 | 实时数据监控 | 可演（部分） | 年度时间窗实测生效；日/月粒度无参数=覆盖不到 |
| 7 | 图层分组与组织 | 覆盖不到 | 重命名/颜色持久化依赖 M10 未建表（对齐表 #10） |
| 8 | 数据源灵活配置 | 覆盖不到 | 同上 M10 未建表 |
| 9 | 要素详情弹窗 | 覆盖不到 | 详情接口 BE-TS-CONTRACT-01 未冻结 |
| 10 | 统计指标展示 | 可演 | /overview 200：stats 9 + domainRows 6 + 12 年趋势；会议卡 mock 明示 |
| 11 | 分析面板 4 Tab | 可演（部分） | influence/cluster/compare 三端点 200；「实时数据监控」Tab 无独立接口=覆盖不到；两卡 mock 明示 |
| 12 | 时间轴趋势 | 可演（部分） | /timeline 200（2025/2026 年）；日/月/季粒度 + 预测/异常=覆盖不到（SRS 待裁定） |
| 13 | 地图可视化 | 可演 | /map 200：点位 99/100、9 市区级级联；机构质心/专利无色阶照 notes 讲 |
| 14 | 科创事件时间筛选 | 可演（部分） | /events 200：年份/类型筛选实测生效；**地域筛选不生效**（P15/P16 对照）+ 日/周/月粒度=覆盖不到 |
| 15 | 重要性分级 | 可演 | high→1 条 / all→34 条实测生效 |
| 16 | 事件详情查看 | 覆盖不到 | 详情接口未冻结；事件对象无 id 字段 |

> 索引统计口径：可演 11 = 纯可演 7（行 1/2/3/5/10/13/15）+ 部分可演 4（行 6/11/12/14，行内已注明覆盖不到边界）；覆盖不到 5（行 4/7/8/9/16）；未填 0。

## 四、文档订正记录（在执行授权「发现明显笔误可改」范围内）

1. 行 4 接口列 `GET /factors/search` → 改 `POST`（前端 `api/situation/index.ts` fetchSituationFactorSearch 实为 POST）。
2. 行 12/14/15 接口列「后端端点未实现（实测 404）」→ 改为「2026-11-07 网关实测 200」（对齐表 §6.3-2 已明示旧 404 结论过时）。
3. 备注第 2/3 条同步订正：趋势/事件端点已上线（附能力边界）；mock 口径更新为「仅会议 mock，期刊/服务机构已切真源」。
4. 未动：需规序号、行数、「界面/触发/请求/期望输出」列、主路径一句话。

## 五、遗留问题（需人工确认）

1. **⚠️ mock 口径与任务派单不一致（最需确认）**：派单与 11-03 台账均记「期刊 7,200 / 会议 1,280 / 服务机构 6,200 三要素 mock」；2026-11-07 网关实测为——期刊 3,401（source：久新期刊名录 dwd_zh_journal + dwd_en_journal，真实名录）、服务机构 43,296（source：我方 ADS svc_metric_fact / M_SVC_ORG_CNT）、仅会议 1,280 仍为 mock（响应 mock:true + mockReason 数仓 §24.10）。**服务端数据源在 11-03 之后已被切换**，本回填按实测证据填写。请确认：以实测为准是否正确；服务机构 43,296 与 ECO 页「正式库服务机构表 0 行、demo 库 43,296 行不可用」的对齐表 #11 口径是否冲突（svc_metric_fact 是否算正式可演源）。
2. **influence 卡片 6 → 5**：11-03 本机实测 6 卡（含项目卡），本轮网关实测 5 卡（项目卡未出现——其策略为取不到不出卡）。网关链路可能少了一路算法库调用，需后端确认是否环境问题。
3. **events 地域筛选不生效**：regionPaths 不被消费（P15/P16 对照同为 23 条），是「未实现」还是「事件本就无地域维度」需后端裁定；演示台词已按「不生效」写入行 14。
4. **行 6/12/14 的日/月粒度**：SRS 要求近 7 天/近 30 天/本月与日/月/季粒度，接口仅年度口径，属需求-实现差，是否登记新缺口交授权人裁定。
5. **factors/search 降级**：search-py 8080 未起，现场演示前需确认该服务是否拉起，否则行 4 只能演降级文案。

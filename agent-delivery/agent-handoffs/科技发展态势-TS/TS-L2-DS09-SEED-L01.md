# Data handoff：TS-L2-DS09-SEED-L01

- 时间：2026-11-09
- 执行：agent:zcode 会话代跑 data-agent（认领 `agent:data-agent`，监管人 `human:王梓真`）
- 任务：科技发展规划 · 灌数（demo 冻结种子 → `gkxlumenx_ads` 28 张 `ts_plan_*` + `gkxlumenx` 1 张 `sys_user_planning_push_record`）
- 行源真源：`lumen-ui-science-pc/src/mock/modules/techDevelopmentPlan.ts`（export 实位，文件头注释行号陈旧不依赖）+ `demo-ui-science/src/techDevelopmentPlan.js`（时间轴/点位投影）+ `ResearchTab.vue` L38/L53 常量段 + `techDevelopmentPlanModel.ts`（L460 报告模板/L740 星型边 builder 逻辑）
- 数据流图：`TS-DS09-OV-DATAFLOW-01`（OV-ARCH §3）——本单产物即图中「种子提取脚本（Python，一次性）→ 展示 ADS」节点，extract_seed.mjs（node 侧）+ seed_ts_plan.py（转换/灌数侧）共同构成该节点

## 1. 产物清单（gkx-orchestration 仓 `scripts/ts_plan_seed/`）

| 文件 | 内容 |
|---|---|
| `ddl/01_gkxlumenx_ads_ts_plan.sql` | 28 张 `ts_plan_*` 建表 DDL（OV 8 + KEY 9 + RES 11），列定义逐字冻结自三份 DATA 分册 §2（含 3 处可执行性勘误，见 §5） |
| `ddl/02_gkxlumenx_sys_user_planning_push_record.sql` | 订阅产物表（OV-DATA §5 A3 裁定）→ `gkxlumenx` upms 主库；初始 0 行 |
| `extract_seed.mjs` | 种子提取脚本（node ≥22 原生 TS 剥离 import mock 模块 + registerHooks resolve 钩子补 demo-ui-science 无扩展名目录导入；ResearchTab 常量段正则）→ dump `seed_dump.json`（生成物，不入 git）；内置 30 项提取自检 |
| `seed_ts_plan.py` | 灌数脚本：行构建（转换规则逐条对应分册 §4）→ 行级断言 → DDL 列长离线预检 → `--dry-run` / `--apply-ddl`（DROP+CREATE 幂等重建）/ 直接 TRUNCATE+INSERT（逐表独立连接+断连重试，适配内网链路偶发 2013）→ 落库后逐表行数验证 + DB 级禁灌/抽样断言 |

用法：`python seed_ts_plan.py --dry-run`；实灌 `INNOV_MYSQL_PASSWORD=… python seed_ts_plan.py [--apply-ddl]`（连接真源 `agent-handoffs/算法库联调-ALGO-LIB/algo-mysql-connection-info.md`，host 10.50.11.76:3306 / user gkxlumenx；密码只走环境变量）。

## 2. 执行证据（实际建表+灌数，非降级）

MySQL 10.50.11.76:3306（`gkxlumenx` 应用账号）连通可用 → **实际执行** `--apply-ddl` + 灌数；随后免 DDL 重跑一次验证幂等（exit=0，行数不变）。落库后逐表行数验证（脚本 `verify_db` 输出 + 独立 SQL 抽查双确认）：

| gkxlumenx_ads（utf8mb4） | 行数 | | gkxlumenx_ads | 行数 |
|---|---|---|---|---|
| ts_plan_hot_tech | 8 ✅ | | ts_plan_key_area_land | 6 ✅ |
| ts_plan_hot_tech_series | 128 ✅ | | ts_plan_key_area_plan | 3 ✅ |
| ts_plan_metric_system | 30 ✅ | | ts_plan_research_field | 5 ✅ |
| ts_plan_tracking_event | 8 ✅ | | ts_plan_research_company | 7 ✅ |
| ts_plan_tracking_point | 35 ✅ | | ts_plan_research_overlap | 6 ✅ |
| ts_plan_local_adv | 19 ✅ | | ts_plan_research_overlap_rule | 3 ✅ |
| ts_plan_talent_flow | 16 ✅ | | ts_plan_research_time_factor | 3 ✅ |
| ts_plan_key_area | 3 ✅ | | ts_plan_research_grade | 4 ✅ |
| ts_plan_key_area_carrier | 22 ✅ | | ts_plan_research_overlap_benchmark | 3 ✅ |
| ts_plan_key_area_carrier_type | 6 ✅ | | ts_plan_research_graph_node | 14 ✅ |
| ts_plan_key_area_district_baseline | 6 ✅ | | ts_plan_research_graph_edge | 13 ✅ |
| ts_plan_key_area_competitiveness | 5 ✅ | | ts_plan_research_insight | 4 ✅ |
| ts_plan_key_area_dimension | 5 ✅ | | ts_plan_research_report_template | 8 ✅ |
| ts_plan_key_area_benchmark | 5 ✅ | | **ts_plan_direction_warning** | **0 ✅（禁灌）** |

合计：OV 244 + KEY 61 + RES 70 = **375 行**（28 张 ts_plan_* 全建，`information_schema` 计数 28）；`gkxlumenx.sys_user_planning_push_record` 建表 12 列、**0 行**（真实推送产生，未 TRUNCATE 未 INSERT）。

**禁灌断言全部通过**（行级预检 + DB 级复验双层）：

| 断言 | 结果 |
|---|---|
| direction_warning 0 行；脚本对其零 INSERT/TRUNCATE 语句 | ✅ |
| overlap 恰 6 行（六企 C(6,2)=15 对 − 9 空对不灌；值域 45–72） | ✅ |
| 图谱专家类节点 0（demo category 4「专家」名实不符→patent；专家留位不灌） | ✅ |
| carrier 22 行 land_benefit 全 NULL（禁编造容积率/亩产；land 表 6 行同） | ✅ |
| grade threshold_low 依次 80/65/45/0 且 is_draft 全 1（U3 建议值） | ✅ |
| insight plan_id 序列 a/b/c/b（固化 resolveStrategyPlan：高→a / 含"追赶"→b / 其余→c） | ✅ |
| 分册抽样：tech1 heat=98/growth=45.2；12m/tech8 末期 76；「热度指数=98」卡；od_shenzhen 18932/21.7 + od_nodes 六节点齐（od_external 12458/16.2）；point(tdp-global-robot,hotspot) score=94；L001 NULL/A001='ai' 且 NULL 恰 7 行=L001/L004/P003/P005/I003/I004/A002 白名单；all=2856；南山=276；composite 78.5/'12.3%'；potential 挂 POTENTIAL；创新资源 92/innovation_resources；rendered_note 5 行同值；rank1 南山区 78.5；土地 125000/92/good；plan a '+18.6%'/3 actions；hot_tech rendered_note 全含「口径待 M0 定稿」 | ✅ |
| U6：talent record 行零个人姓名/头像（提取即弃，断言兜底） | ✅ |

## 3. 行源与转换要点（对应分册 §4）

- 提取走 **node import 实位**（分册推荐路径），零手工转录：mock.ts 原生 TS 剥离 import；demo.js 经其自有 `buildTechDevelopmentPlanDataset({})` 投影（空筛选 share=1，records 逐字不缩放）取 timeline/planRecords/mapRegions/legend；`overlapTimeScopeFactor` 藏在 dataset 工厂内经工厂函数取。
- 关键转换：`position=[lat,lng]` 拆列；OD 标签 `深圳|18,932人|↑21.7%` 拆 region/person_count/trend_pct 且 `talentDirectionNodes` 原组逐字冗余写入 6 条 stats 行 `od_nodes`；`netInflow '+1,248'`→1248 带符号；`flowType`→学术→产业/产业→学术；grade `patent '1,860'`→1860（DDL 为 INT，机械去千分位）；`metric_unit` 从 value 尾段机械拆分（'186.7亿'→'亿'，'98'→NULL）；insight plan_id 按 resolveStrategyPlan 固化；星型边 13 条按 model L740 builder（中心 N-01=深圳先进技术研究院）。
- `report_template` 8 行：报告 3 节 model L460–490 逐字占位符化 + 建议 3 节 ResearchTab 战略 Modal（demo L3358–3375）逐字 + 系统行 2（`page_caliber` 文案沿 KEY dimension.rendered_note 先例自拟用户可读句、零内部编号；`graph_limit`=U9 阈值 `{"node_limit":100,"edge_limit":300}`）。

## 4. 架构合规自检（§2 铁律逐条）

| 项 | 结论 |
|---|---|
| D18：表名/灌数方（Python 一次性）/读取接口三要素齐；接口不直返 mock（caliber_note=rendered_note 物理行源、OD 总量、时间轴、点位全表行携带） | ✅ |
| D18 库边界：不进 ODS/DWD/供应方 `gkx` 库；无 `gapfill_` 前缀；`gkxlumenx_ads` 展示 ADS + `gkxlumenx` 订阅产物表 | ✅ |
| D9：本单不注册 metric（四条 M_INNOV_KEYD_* 与 M_INNOV_PLAN_*/RES_* 均为赋号草稿·未签，只随行列注释携带；不写 cfg_metric seed） | ✅ |
| 不写第二套统计脚本：唯一脚本只搬运种子；warning_count/方向计数/六源均分/集聚度/密度派生一律不算（Java 读表现算） | ✅ |
| 不动 demo/lumen 两仓源码（只读事实源）；不改 task-registry（本单未动 MCP 状态/字段）；不碰 metrics seed | ✅ |
| 敏感信息：MySQL 密码仅环境变量，未写入任何可提交文件 | ✅ |
| 铁律 7（schema 三方评审）：DDL 非新设计，为三份已会签 DATA 分册冻结列定义的落地（3 处可执行性勘误见 §5，属笔误级修正，待 Java 实现单/架构知会） | ✅（附知会项） |

## 5. 对分册 DDL 的 3 处可执行性勘误（笔误级，Java 实现单建表必须采用）

| # | 表.列 | 分册原文 | 落地修正 | 原因 |
|---|---|---|---|---|
| 1 | `ts_plan_direction_warning.signal` | `signal varchar(64)` | `` `signal` varchar(64) ``（列名反引号） | `SIGNAL` 是 MySQL 保留字（5.5+），裸用 1064 语法错 |
| 2 | `ts_plan_tracking_event.row_kind` | `varchar(8)` | `varchar(16)` | 自身注释取值 `timeline_meta` 13 字符装不下（1406） |
| 3 | `ts_plan_local_adv.source` | `varchar(16)` | `varchar(32)` | 自身注释取值 `contract_draft_sample` 21 字符装不下（1406） |

其余 26 表列长全部实测可执行（脚本内置「DDL 列长离线预检」逐行校验，后续种子漂移会在上库前拦截）。

## 6. 待下游知会

1. **Java 实现单**（TS-L2-DS09 IMPL-JAVA 行）：建表 SQL 请直接采用 `scripts/ts_plan_seed/ddl/`（已含 3 处勘误）；`signal` 列在 MyBatis/JPA 映射时注意保留反引号或以 `` `signal` `` 转义。本单已代执行建表+灌数（demo/dev 环境 10.50.11.76），Java 复核以 `SELECT COUNT(*)` 对 §2 行数清单即可。
2. **OV-API 分册**：`overlapTimeScopeFactor` 键为中文（近1年/近3年/近5年），RES 表已落英文键 1y/3y/5y + 中文 label，映射归 API。
3. `direction_warning` 未注册期接口 501 空态信封不变；模型注册后由模型方 Python 写入（`generated_by` 列带出）。
4. seed_dump.json 为生成物不入 git；种子更新时 `node extract_seed.mjs` 重提取（30 项自检）后重跑灌数即幂等。

## 7. cost 估算与 ponytail 自检

- **cost 估算**：actual_tokens ≈ 420K（累计上下文；estimated 80K 为单轮估算口径），model=GLM-5.3-Highspeed，actual_cost ≈ $2.4，cost_warn=green（<$10 阈值）。按派单纪律未动 task-registry 字段，cost 回填留 coordinator。
- **ponytail 自检**：本单产物 = 2 DDL + 1 提取脚本 + 1 灌数脚本 + 1 handoff，全部落 `scripts/ts_plan_seed/` 与 `agent-handoffs/科技发展态势-TS/`；无第二套统计脚本；无仓外散落文件；demo/lumen 两仓零改动（git status 干净）；未 push（本地 commit，待监管人复核）。

ponytail: full

# TS-DS03-DEMO-ACCEPT-LOOP · DS-03 技术发展跟踪演示样本循环验收记录

> **验收单**：TS-DS03-DEMO-ACCEPT-LOOP（技术发展跟踪 / qa-agent）　|　**监管人**：human:李伟
> **依据**：`产品实现规程.md` §6.5；计划 `agent-delivery/工程过程/04-系统集成/05-展示系统集成/编排计划/TS-L2-DS03-LOOP计划.md`；用例真源 `agent-delivery/工程过程/04-系统集成/05-展示系统集成/合规演示用例/TS-L2-DS03-合规演示用例.md`
> **性质**：只读验收（GET/POST 查询体），零代码改动、零 commit/push；token 不落盘、不进本文档。

## 运行 2026-11-07 R1

- **执行**：qa-agent　|　**轮次**：R1（第一轮）
- **探测（第一笔）**：`POST http://10.50.69.111:30895/display/v1/tracking/meta`，头 `Authorization: Bearer <本机 token>`（读 `%USERPROFILE%\.gkx\display-loop-token`，len=32，内容不记录）+ `systemCode: display`，body `{}`，curl.exe `--max-time 40`。
  - 返回 **HTTP 401**：`{"code":401,"msg":"访问令牌不存在","data":"sso check-token failed","ok":false}`
  - 命中计划 §1 熔断（401/令牌失效文案）→ **停止，不进逐行对照、不建子任务**；验收单 `blocked`，note「token 失效，已通知 human:李伟」。
- **诊断补充（只读）**：同端点不带 token 复测亦 401（`Full authentication is required to access this resource`），说明网关当前为强制鉴权、且本机令牌在 SSO 查无记录；与用例文件 2026-11-07 M2/M3 实测注记「网关 StripPrefix=1，无 token」不一致——鉴权策略或令牌注册状态已变化，换发后须以新探测为准。（与同日 TS-DS01-DEMO-ACCEPT-LOOP R1 现象一致。）
- **逐行对照表（7 行可演）**：因探测熔断，7 行全部未发起请求，无接口证据，不判「对得上/对不上」，登记如下。

| 行 | 内容 | 端点 | 条件 | HTTP | 关键返回 | 判定 |
|---|---|---|---|---|---|---|
| 1 | meta/筛选维度（100 城市、26 年、15 集群枚举） | tracking/meta | body {} | 401 | 访问令牌不存在 | 未执行（探测熔断） |
| 2 | dataset 主查询（isEmpty=false、基线 20 条、currentYear=2025） | situation/tracking/dataset | — | 未发起 | 熔断（探测 401） | 未执行 |
| 3 | 年份/集群切换（timeRange 2020–2025、fieldValues CL-SEI-01） | situation/tracking/dataset | — | 未发起 | 熔断（探测 401） | 未执行 |
| 4 | Top-20 榜单（全局模型产出，有榜单数据；不随筛选变化为设计行为不判负） | situation/tracking/dataset | — | 未发起 | 熔断（探测 401） | 未执行 |
| 5 | 9 参数模板（模板可取、参数值域齐） | situation/tracking/parameter-templates | — | 未发起 | 熔断（探测 401） | 未执行 |
| 6 | 趋势/对比（26 年范围可取、返回有数） | situation/tracking/dataset | — | 未发起 | 熔断（探测 401） | 未执行 |
| 7 | 主路径端到端（开页→筛选→看榜→切年份 全链有数） | 上述串行 | — | 未发起 | 熔断（探测 401） | 未执行 |

- **覆盖不到 1 行（行 55 报告产物 items=0）**：已知不判行，本轮不涉及、不建补数单。
- **结论**：**blocked** —— 本机 `display-loop-token` 已被 SSO 判定不存在（令牌失效）。对得上 **0/7**（熔断未对照，**非样本缺口**，不做 DATA/QUERY/ALGO 分类、不建补数单）。
- **下一步建议**：监管人 human:李伟 换发新 token 写入 `%USERPROFILE%\.gkx\display-loop-token` 后触发 R2；R2 仍为只读全量 7 行对照，计划与用例不变。

## 订正（2026-11-07 晚）
- blocked 根因查明：**路径笔误**。控制器真实映射 `/v1/situation/tracking`，此前探测打 `/v1/tracking` 故 404；环境无问题。带有效 token 实测 `POST /display/v1/situation/tracking/meta` 200（timeline years 2000-2025、geoDrillLevels 有值；注意 meta 的 events/capabilities 为空数组，R2 需看 dataset）。计划文件路径已订正。验收单回 ready。token 寿命约 1 小时，R2 应尽快跑。

## R2 轮（2026-11-07 晚）

- **执行**：qa-agent　|　**轮次**：R2（第二轮）　|　时间约 21:49–21:56（Asia/Shanghai），token 有效（len=32，不落盘）
- **探测（第一笔）**：`POST /display/v1/situation/tracking/meta`，body `{}` → **HTTP 200**。timeline 26 年（2000–2025，currentYear=2025）；regionCascadeOptions=100 全球城市；mapTechnologyTypes=6 类；bubbleAxisOptions=12 维（被引数/人才数/项目数 max=0，已知口径）；parameterTemplates=9（5 系统内置 + 4 自定义落库）；historyMatrix=3 期 × 3 方法完整评分矩阵；`noSourceFields=["timeline.events","capabilities","methods","knowledgeBase"]` 后端如实声明无源。
- **实测请求（全部 200，只读）**：`dataset {}` 基线；`dataset {timeRange 2020–2025}`；`dataset {fieldValues:[CL-SEI-01]}`；`dataset {selectedMapTechnologyTypeKeys:[机器学习加速硬件架构], mapDrillLevel:country}`；`dataset {regionKeys:[深圳 loc_id]}`（首轮误用 `regionValues` 得 200 但 scopeNote「未选择」，查前端 `src/views/situation/tracking/index.vue` 确认参数名为 `regionKeys` 后重测生效）；`GET parameter-templates`。

### 逐行判定表（7 行可演）

| 行 | 内容 | 端点/条件 | HTTP | 关键返回 | 判定 |
|---|---|---|---|---|---|
| 1 | meta/筛选维度 | tracking/meta {} | 200 | 100 全球城市 ✓；26 年（2000–2025）✓；领域枚举由前端 `src/lib/industryCluster/seed.ts` 15 集群 seed 下发，后端 `fieldValues` 反查生效（见行 3） | 对得上 |
| 2 | dataset 主查询 | dataset {} | 200 | isEmpty=false、records=20、heatMatrix=20 话题 × 11 列（2015–2025，attention/activity 双值）、currentYear=2025、bubbles=20、mapRegions=100、relations=18、evaluationHistory=3 | 对得上 |
| 3 | 年份/集群切换 | dataset {timeRange 2020–2025}；{fieldValues:[CL-SEI-01]}；{regionKeys:[深圳]} | 200 | timeRange→years/heatMatrixYears 收窄为 6 列 ✓；CL-SEI-01→scopeEffectNote「已生效（反查 420 Topic / 12 子学科）」且 trendSeries 实变（2015 论文数 232090→16833）✓；深圳 regionKeys→scopeNote「已生效（按 location_id 过滤）」、trendSeries 实变（2015 论文数→1256）✓ | 对得上 |
| 4 | Top-20 榜单 | 上述各筛选响应比对 | 200 | 领域/区域/年份筛选后 records 话题名单不变——设计行为（scopeEffectNote 明示「六维/潜力/榜单为全局模型产出」），不判负；trendSeries/hotTopics 随筛选变化 | 对得上 |
| 5 | 9 参数模板 | GET parameter-templates | 200 | items=9（系统内置 5 + 自定义 4 已落库），note 明示落库口径；meta.parameterTemplates 同源 9 条、5 维权重/阈值齐全 | 对得上 |
| 6 | 趋势/对比 | dataset {} trendSeries；meta.historyMatrix | 200 | trendSeries 4 系列 × 26 年（论文/被引/人才 2015 起非 null，项目 2000 起）；historyMatrix 3 期 × 3 方法（overall+六维+阶段+风险），并排 ≤3 期恰好覆盖 | 对得上 |
| 7 | 主路径端到端 | meta→dataset 筛选→榜单→切年份 串行 | 200 | 全链有数，无空态断点 | 对得上 |

- **覆盖不到 1 行（行 55 报告产物）**：已知不判行，本轮不涉及、不建补数单。

### 缺口列表

- **无缺口**（0 项）。7/7 对得上，无 DATA/QUERY/ALGO 分类需求。

### 观察项（不判负，演示口径照讲）

1. meta 的 `timeline.events=[]`、`capabilities=[]`、`methods=[]`、`knowledgeBase` 双空——noSourceFields 如实声明无源，用例未期望其非空（行 52/53 为前端静态内容），按「对得上」处理。
2. bubbleAxis 12 维中「被引数/人才数/项目数」max=0，选中呈空态，演示避开（用例已知口径）；bubbles.investment 全为 RULE_SIMULATED/LOW（规则模拟投资估算），演示须明示非真实投资额。
3. `mapDrillLevel:country` 请求后响应回显 mapDrillLevel=country（层级标注 ✓），但 100 个 mapRegions 的 geoLevel 仍为 region 城市点位、未聚合出国家点位——用例口径仅要求「返回层级标注」，按对得上处理；如下钻交互演示需国家聚合视图，另行登记。
4. 筛选参数名以 `regionKeys` 为准（误传 `regionValues` 后端不报错、scopeNote 回「未选择」）；`timeRange` 传 `{startYear,endYear}` 对象生效。

- **结论（已被下方订正推翻）**：~~样本满足 R2~~ —— 接口级 7/7 对得上，但结论仅基于用例「数据情况」列，未做需规逐句核对；见下方订正段。

## R2 订正 · 需规核对（2026-11-07 深夜，监管人 human:李伟 裁定 B 路线）

签收前补做「需规原文 vs 空缺项」逐句比对（真源 `bid-reference/srs/02-科技信息展示系统/科技发展态势/技术发展跟踪.md` 序号 48–55），结论：**3 个需规明确功能点未覆盖，接口级「对得上」不等于需规满足 → 不签收，建缺口子任务，修复后跑 R3**。

### 非缺口锁口径（需规未要求，演示照讲，不建单）

| 空缺 | 需规依据 | 判定 |
|---|---|---|
| meta.timeline.events=[] | 48 行仅要「时间轴调整查看不同时期热度变化」→ heatMatrixYears 列轴收窄已实测生效；大事记事件层需规未提 | 非缺口，锁口径 |
| bubbles.investment 全 RULE_SIMULATED/LOW | 50 行「气泡大小代表技术规模**或**投资额」→ scale 技术规模有真实值，二选一即满足 | 非缺口，演示明示规则模拟估算 |
| capabilities=[] | 元信息字段，非需规功能点 | 非缺口 |

### 观察项（不阻塞）

- bubbleAxis 12 维中「被引数/人才数/项目数」max=0（50 行未点名维度全集，需规只要求「可调整坐标轴查看不同维度关系」）：演示避开，登记观察项，不进本轮缺口单。

### 缺口列表（3 项，ALGO 类，建子任务阻塞签收）

| 缺口 | 需规出处 | 需规原文 | 实测 | 子任务 |
|---|---|---|---|---|
| 方法自动推荐+案例库缺失 | 53 行 | 「支持方法选择建议功能，根据技术类型自动推荐最适合的评估方法组合，提供方法应用案例和最佳实践参考」 | meta.methods=[]、knowledgeBase={cases:[],bestPractices:[]}，noSourceFields 如实声明无源 | TS-DS03-LOOP-R2-Q01 |
| 区域发展建议缺失 | 49 行 | 「点击区域可查看该地区详细的技术评估报告和发展建议」 | mapRegions 有评估值/趋势/等级/证据来源文案，无发展建议字段 | TS-DS03-LOOP-R2-Q02 |
| 参数优化建议缺失 | 54 行 | 「系统会根据历史数据提供参数优化建议，帮助用户提高评估准确性」 | 无此能力（parameterTemplateSource 口径仅模板回填） | TS-DS03-LOOP-R2-Q03 |

- **裁定**：监管人 human:李伟 2026-11-07 选 B（严格等修）——3 项全建 ALGO 子任务，DS-03 **不签收**，验收单 `TS-DS03-DEMO-ACCEPT-LOOP` 挂 `blocked` 并 depends_on 上述 3 单；3 单修复部署后跑 R3 复测（重点行 49/53/54），全绿再提请签收。
- **下一步口令**：监管人说「可以派了」→ 派 Q01/Q02/Q03（be/algorithm 方向见各单 note）；说「推」→ 本记录与注册表变更随下一批推 origin/dev。

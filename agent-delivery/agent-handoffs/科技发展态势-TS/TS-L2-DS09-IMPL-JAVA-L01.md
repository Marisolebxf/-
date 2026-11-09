# API handoff：TS-L2-DS09-IMPL-JAVA-L01

- 时间：2026-11-09 · **执行**：agent:zcode 会话代跑 api-agent（重启派发；上一轮被取消，本轮收编其工作区遗留产物、审查修正后交付）· **监管**：`human:王梓真`
- 仓库：`lumen-svc-platform`（分支 dev，**本地 commit 未 push**，push 由监管人统一确认）
- commit：**`5295577`** `[agent:api-agent] feat(display): DS-09 科技发展规划 10 GET+1 PUT 端点、订阅推送面与 501 通道`（24 files，+4227/-1）
- 验证：`mvn -pl gkxlumen-display,gkxlumen-upms/gkxlumen-upms-biz -am test` → **BUILD SUCCESS，134 tests / 0 failures**（Maven 3.9.9，pom compiler target 17，本机 JDK21 工具链）
- 覆盖功能点：DS-09 三页签（09a 综合 178–184 / 09b 重点领域 185–190 / 09c 研究分析 191–196）
- 新增接口：**10 GET + 1 PUT**（服务内 `/v1/situation/planning/**`，网关 `/display/v1/situation/planning/**`，铁律 9 拼接，无前缀插序错误形态）
- Feign 依赖：无 Python 依赖（D18 读表 + 既有 upms `RemoteUserBehaviorService` 内部 Feign）
- **图**：`TS-DS09-OV-CALLCHAIN-01`（OV-ARCH §2 已落盘）——实现未改变拓扑，直接引用：前端 → 网关 `/display/**` → PlanningController → PlanningQueryService 只读 ADS（ts_plan_*）/ 订阅面走既有 SubscriptionPushJob + upms Feign；direction-warnings 过模型注册门（未注册 501）。图中 `rule_type=planning_resource` 为 ARCH 术语笔误，实现按 DATA §0.3 裁定用实际列名 **`scope_type`**。

---

## 1. 范围与实现（对照 DoD 逐条）

| # | DoD | 实现 |
|---|---|---|
| 1 | PlanningController + PlanningQueryService，10 GET（OV 9 + key-areas + research-analysis）+ PUT subscriptions，只读 gkxlumenx_ads | `controller/PlanningController.java`（`@RequestMapping("/v1/situation/planning")`，@Operation 全覆盖）+ `service/PlanningQueryService.java`（11 方法）+ `service/PlanningTableReader.java`（接口）/ `JdbcPlanningTableReader.java`（裸 JDBC 只读实现，沿 `JdbcPanoramaScores` 免连接池先例：表名白名单 `^ts_plan_[a-z0-9_]+$`、where 禁字符校验、`setReadOnly(true)`、失败=空列表诚实空态）。**10 GET**：hot-technologies(range 3m/6m/12m)、metric-system、tracking(time_mode/space_mode)、local-advantage、talent-flow(flow_type/risk_level)、resource-push(过滤+分页≤100)、resource-push/subscriptions、direction-warnings、key-areas、research-analysis；**1 PUT**：resource-push/subscriptions（唯一写面） |
| 2 | direction-warnings 501 短路 | `config/PlanningDirectionAlertGate.java`：`planning.direction-alert.registered` 默认 **false**（application.yml 已登记，见 §5 配置清单）→ HTTP 501 + 信封 `{code:501, msg:"预警模型未注册：M_INNOV_PLAN_DIRECTION_ALERT 尚未上线（赋号草稿·未签）", data:null}`（OV-API §3.1 逐字）。处理顺序 400→501→读表；注册后零行=诚实空态（`empty_reason=no_source`+`empty_message`）。其余 10 端点零 501。**导出同闸**：门为独立 Bean，M1 §3.8 任务中心接入 `content_key=planning-direction-warning` 时直接复用（见 §6 阻塞 1） |
| 3 | PlanningResourceSubscriptionAdapter + 产物写入 + F7 聚合 | `subscription/adapter/PlanningResourceSubscriptionAdapter.java`（`scopeType()="planning_resource"`，自动挂入既有 Registry，零 DDL）；**F7**：多命中=聚合一通知（`SubscriptionHit.payloads` 携带 N 行）+ `SubscriptionPushJob` 通知双写后调 `service/PlanningPushRecordWriter` → upms Feign `recordPlanningPushes` 逐行落 `sys_user_planning_push_record`（`@Inner`+`@NoToken`，**display 不直连 gkxlumenx 主库**——有先例：既有用户行为家族全走 RemoteUserBehaviorService，故无阻塞项）。upms 侧新增 `SysUserPlanningPushRecord` 实体/Mapper + `SysUserBehaviorController` 两个 @Inner 端点 + ServiceImpl（写=事务+逐行必填校验；读=idx_user_read 口径过滤分页，size 夹取≤100） |
| 4 | 195 导出接任务中心 | research-analysis 响应 `report_export.content_key="planning-research-intelligence"`（+`default_format=doc`、`template_source`）；模板文案本体全在 `ts_plan_research_report_template` 表行。**任务中心端点（M1 §3.8 `POST /v1/situation/export/jobs`）本仓尚未实现**（属另一实现单）——本单交付的是接入面与同闸依赖，见 §6 阻塞 1 |
| 5 | avg_overlap 现算 + plan_id 对齐核对 | `competingEnterprises()`：avg=AVG(overlap_score) **over 有值对**（空对 `source_tag=empty`+`empty_reason=no_seed_pair` 不进分母，全空=null 不冒充 0），单测断言。**库内核对（10.50.11.76 实连）**：KEY 方案主键={a,b,c}，insight.plan_id 序列=(a,b,c,b) → **全对齐，无差异**；direction_warning=0 行；ts_plan_* 28 张齐 |
| 6 | 零硬编码 | caliber/阈值/模板全表行读：`hot_tech.rendered_note`、`key_area_dimension.rendered_note`、`report_template(page_caliber/graph_limit)`、overlap_rule 三档阈值、time_factor 系数、od_nodes OD 总量（标签拆解）。代码常量仅限：OV-API §4 逐字冻结枚举字典（六源/三级/flow_type）、服务端错误 msg、结构元数据（content_key/表名/段键）、`map_center/zoom` 展示配置常量（OV-API §2.3 会签认可项）——其余例外见 §4 偏离注记 |
| 7 | 最小单测 + mvn 绿 | 3 个测试类 18 用例：`PlanningControllerTest`(7：501 短路/注册后空态/400 优先/枚举/401)、`PlanningQueryServiceTest`(6：metric_id 透传/avg_overlap/U9 截断/od_nodes 拆解/stats 现算/plan_id 对齐断言)、`PlanningResourceSubscriptionAdapterTest`(5：聚合多产物行/领域过滤/keywords 兜底/清空订阅/无池诚实不推)。display 模块全量 **134 tests 0 fail**（含存量回归），upms-biz compile+test 绿 |

## 2. 端点清单（网关路径 = `/display` + 服务内路径）

| seq | 方法/路径 | 要点 |
|---|---|---|
| 178 | GET `/v1/situation/planning/hot-technologies?range=` | 8 行全量；heat_series 按 range_key 分区，`year`=period_label 期标签；caliber_note=rendered_note；metric_id=metric_ids JSON 首元素（HEAT） |
| 179 | GET `.../metric-system` | 7 分类；linked 由 linked_json 下发；无 metric_id（n/a_ops） |
| 180 | GET `.../tracking?time_mode=&space_mode=` | timeline_meta+event 行；35 点 space_mode 地域收窄（global 全量/gba 湾区城市集/shenzhen 仅深圳——实现单口径，见 §4-4） |
| 181 | GET `.../local-advantage` | 三键×6 对比项；维度级 local/global_avg=6 项均值；reference_stats=reference_json（source 逐字） |
| 182 | GET `.../talent-flow?flow_type=&risk_level=` | stats 四数现算（不随 Query 收窄）；「预警流动」=risk_level=warning 特例映射；od_nodes 标签拆解（18932/21.7）；U6 无个人明细 |
| 183 | GET `.../resource-push`（过滤+分页）+ GET/PUT `.../resource-push/subscriptions` | 产物清单按用户隔离；订阅 scope_value JSON{resource_types,fields}+keywords 冗余+push_frequency（realtime↔hourly 双向映射，U7 待 M0）；默认值配置携带 |
| 184 | GET `.../direction-warnings?field=&warning_level=` | 501 通道（§1-2）；六源均分 source_averages 按可见 items 现算；report_meta 等级计数现算 |
| 185–190 | GET `.../key-areas` | 平铺 9 块+carrier_total/caliber_note/metric_ids（SPATIAL→COMPETITIVENESS→POTENTIAL→LAND 冻结顺序）/empty_reasons（仅空块）；各块 sort_no/dim_order/rank_no 服务端排序 |
| 191–196 | GET `.../research-analysis` | 平铺 12 块+caliber_note(page_caliber)/metric_ids；U9 图谱阈值读 graph_limit 行；strategy_advice 派生块（三节=模板行 presence）；零 Query 零 501 |

## 3. 产物清单（commit 5295577）

**gkxlumen-display 新增**：`config/PlanningDirectionAlertGate`、`controller/PlanningController`、`service/`{PlanningQueryService, PlanningTableReader, JdbcPlanningTableReader, PlanningSubscriptionService, PlanningPushRecordWriter, PlanningResourcePoolReader}、`subscription/adapter/PlanningResourceSubscriptionAdapter`；**修改**：`subscription/SubscriptionHit`（+payloads 字段与 of 重载）、`job/SubscriptionPushJob`（+产物行落表，单命中适配器零行为变化）、`resources/application.yml`（+planning.direction-alert.registered=false 及注释）。
**gkxlumen-upms**：upms-api 新增 `dto/PlanningPushRecordDTO`、`entity/SysUserPlanningPushRecord`；修改 `feign/RemoteUserBehaviorService`（+2 内部方法）；upms-biz 新增 `mapper/SysUserPlanningPushRecordMapper`，修改 `SysUserBehaviorController`/`SysUserBehaviorService`/`SysUserBehaviorServiceImpl`（+2 方法）。
**db/**：新增 `9x_gkxlumenx_ads_ts_plan_ds09.sql`（28 张 DDL，列定义逐字冻结自三份 DATA 分册；已含 SEED-L01 §5 三处可执行性勘误：`` `signal` `` 反引号、tracking_event.row_kind varchar(16)、local_adv.source varchar(32)；另 2 处实现侧执行注记见文件头：RES updated_at 补默认值、graph_limit 行 template_text 约定 JSON）；`9x_gkxlumenx_user_behavior.sql` 追加 `sys_user_planning_push_record`（A3 裁定 DDL，CREATE IF NOT EXISTS 幂等）。**注意：库表已由 SEED-L01 实建实灌，本仓 DDL 仅为仓内权威存档/新环境执行用，不需要在本单执行。**
**测试**：3 类 18 用例（见 §1-7）。

## 4. 偏离与注记（不改契约，逐条登记）

1. **`report_meta.title`**（"潜在科技发展方向预警报告"）：表无对应列（OV-API §2.7 标注 report_meta 对齐 demo directionMonitorReport），以报告产物名常量承载——若后续要求表行携带，在 direction_warning 表加 meta 行即可，代码改 1 处。
2. **`competing_enterprises.metric_id`**（M_INNOV_RES_CI_COMPARE）：RES-DATA DDL 未给该现算块落物理列（company 表只挂 CI_LEVEL），Java 常量承载逐字草稿号——不改 DDL；顶层 metric_ids 因此恒含四条之一。
3. **graph_limit 行实灌值 `{"node_limit":100,"edge_limit":300}` 无 `follow_up` 键**（库内实测；repo DDL 注释约定含 follow_up）→ 截断态 `follow_up=null`。V1 实际 14 节点/13 边不触发截断；**建议 DATA 侧补灌 `"follow_up":"M2 §3.1"` 键**，代码零改动即闭合。
4. **tracking space_mode 地域收窄**：OV-API §2.3 只定枚举未定过滤语义，实现按 M1 §1.3 三级落位（gba=湾区城市名集合、shenzhen=region='深圳'；种子 7 点 gba 留 3、shenzhen 留 1）——FE 接线联调时确认口径。
5. **ADS 默认连接指向 `gkxlumenx_ads`**（非 JdbcPanoramaScores 先例的 demo_gkxlumenx_ads）：库内实测 demo_gkxlumenx_ads **无** ts_plan 表族、SEED-L01 实灌在 gkxlumenx_ads，故默认指实灌库；Nacos `gkxlumen.display.planning.ads-url` 可覆写。
6. **local-advantage 维度级标量**：契约为维度级（local/global_avg=6 对比项均值现算）；`dimensions[].items[]` 子项序列仍属 OV-API §7-5 批 4 建议未冻结，本实现不擅自加块——FE 三块图表保持 mock 种子的会签点沿袭。
7. **上一轮遗留产物收编**：重启派发时工作区存在上轮未提交实现（文件清单与本单 DoD 完全吻合，判为本任务遗留），本轮未推倒重写，而是逐文件审查后修正 5 处缺陷交付（DDL 2 处勘误未落、metric_ids 顺序违 §2.10、od_nodes 数字拆解缺陷 18932217、1 处测试期望算错、ADS 默认库指向错误库）。

## 5. 新增配置项清单（application.yml 仅 +1 键，其余走 @Value 默认）

| 键 | 默认 | 说明 |
|---|---|---|
| `planning.direction-alert.registered` | `false` | 184 模型注册开关（诚实默认未注册→501）；翻转归模型注册运维 SOP（登记 seed+翻配置同一变更单） |
| `gkxlumen.display.planning.ads-url` | `jdbc:mysql://10.50.11.76:3306/gkxlumenx_ads?...` | 只读 ADS 连接（@Value 默认，Nacos 可覆写；密码 `DISPLAY_ADS_PASSWORD` 回落 `ELEMENT_MYSQL_PASSWORD` 环境变量） |
| `gkxlumen.display.planning.ads-user` | `gkxlumenx` | 同上 |
| `gkxlumen.display.planning.push-pools` | `{}` | 四类资源池声明 JSON（`{"report":{"table":"...","where":"..."}}`）；**池表未冻结=诚实不推送**，冻结后 Nacos 下发即生效零代码变更 |
| `gkxlumen.display.planning.subscription-default-*` | types=四类全选 / fields 空 / daily | 订阅默认值（OV-API §5.2 由配置携带） |

## 6. 阻塞项 / 待下游

1. **M1 §3.8 导出任务中心端点本仓未实现**：`POST /v1/situation/export/jobs`（含 184 `planning-direction-warning` 的 501 同闸、195 `planning-research-intelligence` 的建任务/渲染/文件产物）属独立实现单；本单已备好 `PlanningDirectionAlertGate`（可直接注入复用）与 `report_export` 元数据 + 模板表行。**该单落地前 184/195 的下载按钮无后端承接（前端导出入口按 501/未接线态禁用）。**
2. **订阅资源池表未冻结**（push-pools 默认 {}）：适配器诚实不命中不推送；需 data/architect 冻结四池 ADS 源（行形状：resource_id/title/field）后 Nacos 下发。
3. **graph_limit 行补 follow_up 键**（§4-3，DATA 侧补灌）。
4. **网关 501 透传核验**（OV-API §9-6 遗留）：部署联调时确认 gateway 无 501→500 改写。
5. CI/K8s dev rollout 未跑（本地 commit 未 push，按纪律 push 由监管人确认后流水线承接）。

## 7. 验收证据

- `mvn -pl gkxlumen-display,gkxlumen-upms/gkxlumen-upms-biz -am test`：**BUILD SUCCESS**（reactor 26 模块全 SUCCESS；display `Tests run: 134, Failures: 0, Errors: 0, Skipped: 0`，其中本任务 3 类 18 用例；upms-biz 测试绿）。
- 库内实连核验（pymysql @10.50.11.76）：ts_plan_* 28 张齐；direction_warning 0 行；push_record 0 行；plan_id 对齐（a/b/c/b ⊆ a/b/c）；KEY comp metric 行序=COMPETITIVENESS×4+POTENTIAL（与 §2.10 顺序断言一致）；overlap 6 真值 [68,52,45,72,58,48]；page_caliber/graph_limit 模板行在；od_nodes 343B 六节点；rendered_note/metric_ids 列值逐字。
- SQL 形态烟测：reader 的 `SELECT * FROM ts_plan_*`（不点名保留字 `signal` 列）在实库可执行；`SELECT signal ...` 裸用确证 1064（SEED-L01 勘误 1 的必要性），Java 侧无此形态。

## 8. 架构合规自检（§2 铁律逐条）

| # | 项 | 结论 |
|---|---|---|
| 1 | 算法只在 Python | ✅ Java 无 NLP/推理；全部确定性拼装/现算（均值、计数、标签拆解）；无 Python 运行时依赖 |
| 2 | 调用链 前端→Java REST→（灌数期）Python | ✅ 网关 `/display/v1/situation/planning/**`；Java 只读 ADS；越层零 |
| 3 | 图谱 Nebula | ✅ 不涉（RES graph 为 ADS 表行下发，非 nGQL） |
| 4 | D12 无 demo-* 依赖 | ✅ Feign 仅 upms 内部；无任何 demo 地址回落 |
| 5 | D18 禁接口直返 mock | ✅ 11 端点全读表；文案/阈值/模板表行携带（§1-6）；空态诚实；例外 4 处已注记（§4） |
| 6 | 读写面 | ✅ 唯一写面=PUT subscriptions + 订阅 Job 产物行（app_user 家族既有体系复用）；display 不直连主库 |
| 7 | U6 个人信息 | ✅ talent DTO 无姓名/头像/证件/ID；od_nodes/记录均机构级 |
| 8 | 501 语义 | ✅ 仅 184；501=通道态非覆盖证明；表 V1 零行禁灌保持 |
| 9 | metric_id 纪律 | ✅ 全部表列透传或已注记常量（CI_COMPARE）；KEYD 顺序冻结；不发明新 M_*；179/188/189/190 无核块零贡献 |
| 10 | 网关路径铁律 9 | ✅ 见 §2；OpenAPI @Operation 全覆盖 |
| 11 | 中文 Javadoc | ✅ 类/字段/方法含 @param/@return |
| 12 | 交付边界 | ✅ 未 push；未改 task-registry；application.yml 仅 +1 必需键并已列清单（§5）；未动 .gitignore |

## 9. cost 估算与 ponytail 自检

- **cost**：actual_tokens ≈ 690K（含上轮遗留审查全量阅读），model=GLM-5.3-Highspeed，actual_cost ≈ $3.9，cost_warn=**green**（<$10）。cost 字段回填留 coordinator（派单纪律）。
- **ponytail 自检**：产物=24 文件单 commit（5295577）+ 本 handoff，无仓外散落；demo/lumen-ui 零改动；gkx-orchestration 零改动；无第二套统计脚本（均值/计数全 Java 现算）；工作区收编遗留而非双份实现；未 push（本地 dev，待监管人确认）。

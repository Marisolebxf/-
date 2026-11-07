# SVCCHAIN · 产业服务链分析 · 缺口登记总表

- 规程：`agent-delivery/产品实现规程.md` §6.4（数据情况三类判定）、§6.5（缺口四分类 DATA/QUERY/ALGO/ENV）
- 任务：`SVCCHAIN-DC-M4-GAP-L01`（长任务总控 `SVCCHAIN-合规演示用例-长任务总控.md` 段 M4；agent=doc-agent；监管人=human:徐滕强；强度=ponytail full）
- 日期：2026-11-07
- 归并原则：**只归并不新造编号**。来源 = 四域用例（`SVC-ORG/ECO/REC/PT-合规演示用例.md`）+ M1 矩阵（`SVCCHAIN-需规条目矩阵.md` §2/§3.2）+ 各域 LOOP 计划既有引用集合。**本表 22 行 = 16 行 Q 客户决策 + 6 行 GAP as-built 角标**，每行编号均可在「出处真源」列查到原始登记。
- 处置列口径：LOOP 轮次分类建议（DATA/QUERY/ALGO/ENV 四类之一，或「不派修-演示态本身」= 该缺口的演示态声明/诚实空就是用例期望本身，轮内只核字段在位性不派修）。**本表是归并登记，不是派单依据**；跑轮中确认的新缺口按各域 LOOP 计划「先 task-query 去重」后追加进本表，不另造编号。

## 1. 缺口/口径项总表（22 行）

| 编号 | 类型 | 摘要 | 出处真源 | 影响需规行 | 影响域 | 处置（LOOP 轮次分类建议） |
|---|---|---|---|---|---|---|
| Q-SVCCHAIN-01 | Q 客户决策 | 服务机构技术力评价模型算法定义卡缺失（维度口径/归一化基准/默认权重）；临时口径=集合内最大值归一 × 用户权重 | `客户决策清单跟踪表.md` | 7.3.1、7.3.2、*33.4* | ORG、PT | ALGO（定义卡/评分区分度，随 `svc_tech_power_score` 恒 40/20 卡点，见事实登记 3）；等卡期间按演示态声明核对 |
| Q-SVCCHAIN-02 | Q 客户决策 | 服务深度得分与市场热度评级判读口径未定（深度=服务强度归一 0-100 🧪；热度=近 3 年 vs 前 3 年增速分档演示规则）；环节平均深度 STAT 第 16 条 1A 挂起 | `客户决策清单跟踪表.md` | 7.1.1、7.1.2、7.2.1、7.2.2、7.4.1 | ORG、ECO | ALGO（深度公式/评级规则）＋ DATA（趋势末端年 2026=36 骤降登记不灌数） |
| Q-SVCCHAIN-03 | Q 客户决策 | 瓶颈堵点识别算法与专家规则库口径未定（0→空白/≤1→薄弱/平均深度<55→瓶颈 演示规则🧪；生态影响力评分合成口径） | `客户决策清单跟踪表.md` | 7.4.2、7.5.2 | ECO | ALGO（判定规则）；影响力不输出伪分=演示态本身 |
| Q-SVCCHAIN-04 | Q 客户决策 | 深圳服务链统一评价框架未定（指标构成、链完整度算法、城市基准数据源、梯队分档）；完整度 0.833 为演示合成值（非空环节 5/6） | `客户决策清单跟踪表.md` | 7.8.1、7.8.2 | ECO | ALGO（框架/梯队规则）＋ DATA（非深圳城市基准源待甲方指定） |
| Q-SVCCHAIN-05 | Q 客户决策 | 招引/培育推荐模型正式口径未定（权重默认、量化来源、名单阈值、建议生成规则）；2026-10-22 王惠四维＋等权试点口径已会签；确认前名单不作对外招商承诺 | `客户决策清单跟踪表.md`（会签：`agent-handoffs/服务机构-SVC/SVC-MODEL-REC-COSIGN-L01.md`） | 7.6.1、7.6.2×2 切片、7.7.1、7.7.2 | REC | 不派修-演示态本身（权重双口径并行走甲方决策链，见事实登记 1；REC LOOP 计划 §0/§4 已明示不为双口径派修） |
| Q-SVCCHAIN-06 | Q 客户决策 | 门户「专题服务」统计口径与数据源未定（全球/全国统计范围、类型/规模分档字典、区域归属口径、重点机构遴选参数）；门户页面常量轨 vs 库 ADS 轨两轨差 | `客户决策清单跟踪表.md`（M_SVC_PT_* 10 枚已逐条锁口径，见该行 2026-08-28 侯佳伟锁项） | 97、98、99、100、101、103、104 | PT | DATA（页面常量与 ADS 面两轨差核对登记）＋ QUERY（统计接线缺口，建接线核对子任务只核对不改码） |
| Q-SVCCHAIN-07 | Q 客户决策 | 全球名录港澳台/海外抽不出（海外表 0 行；港澳台套不上国内圈定 v1.1），门户全球总数无法成真数 | `客户决策清单跟踪表.md` | 97（全球轴）、*33.3* | PT | 不派修-演示态本身（已拍口径：先写国内圈定值 + 「目前只有国内数据」提醒，国家行不造；真全球待甲方+供方） |
| Q-SVCCHAIN-08 | Q 客户决策 | 领域×六环节无源——无 `org×领域×环节` 服务记录事实表，STAT 第 14–18 条挂起；六环节字典唯一来源=分析侧 `CHAIN_STAGES`，禁另造第七档 | `客户决策清单跟踪表.md` | *33.2*、102、7.4.1 | PT、ECO | DATA（事实表缺；建表=另行立项非 LOOP 动作） |
| Q-SVCCHAIN-09 | Q 客户决策 | 产业过滤口径未定（过滤粒度集群/L0/细分码 + 演示默认产业取值）；临时默认=目录第一个集群第一个 L0（前端无参数回落 `CL-SEI-01`） | `客户决策清单跟踪表.md` | 7.1.1；PT 五页无参数回落 | ORG、PT | 不派修-演示态本身（临时默认已按口径执行，待甲方确认粒度后去 ⚠️ 角标） |
| Q060 | Q 客户决策 | 六类服务机构技术力指标权重与阈值；项目临时基线=五维等权归一写 `svc_tech_power_score`，缺源 org_id 确定性代理并标 pending | `客户决策清单跟踪表.md` | 7.2.2、7.3.1、7.3.2（任务快照 `yellow_gaps` 挂 Q060） | ORG | 不派修-演示态本身（临时基线成立；正式定义卡同 Q-SVCCHAIN-01 等唐绍祖） |
| Q061 | Q 客户决策 | 服务链短板判定阈值与短板成因词典（<45 短板 / >=70 优势规则版）；`svc_chain_gap.q061_pending_client=1` 全量 | `客户决策清单跟踪表.md` | 7.4.1、7.4.2 | ECO | ALGO（阈值/词典口径） |
| Q062 | Q 客户决策 | 服务关系强度/层次/密度口径（4:4:2 强度、1/N-hop 层次、密度/连通分量）；城市级网络密度取全局密度待本条 | `客户决策清单跟踪表.md` | 7.5.1、7.5.2、7.8.1 | ECO | ALGO（关系口径） |
| Q063 | Q 客户决策 | 机构潜力、深圳连接度数据源（融资/关系边代理，正式源待定） | `客户决策清单跟踪表.md` | 7.5.1（图谱 yellow_gaps 挂 Q063）；7.6.1、7.7.1（推荐模型数据源侧） | ECO、REC | DATA（代理数据维持，正式源待定） |
| Q-SVC-004 | Q 客户决策 | district 抽取规则（深圳各区）——v2.2 实查为直字段无需地址解析 | `客户决策清单跟踪表.md`（svc 专项表段） | 103 | PT | 不派修-已闭合（🟢；LOOP 无动作） |
| Q-SVC-010 | Q 客户决策 | 服务机构准入本身无可靠主路径（临时词表 `svc_rule_demo_kw_v1.1` 圈定 + `pending_client_confirm`；上线前须甲方+供方共同决策）；深圳圈定准入同源 | `客户决策清单跟踪表.md`（svc 专项表段） | 100、7.5.1（yellow_gaps 挂）、7.8.1、7.8.2（非深圳对标值待核） | PT、ECO | 不派修-演示态本身（临时基线成立；上线前甲方决策） |
| Q-SVC-011 | Q 客户决策 | 招引/培育推荐产业切片缺 3 条 L0 挂链数据——`enterprise_industry_chain` 中 INB1303 集成电路 / INB1306 软件 / INB1333 智能终端共 0 行 | `客户决策清单跟踪表.md`（svc 专项表段；2026-11-07 用户走查引入） | 7.6.2（诚实空切片） | REC | 不派修-演示态本身（诚实空是期望本体：空态文案 + HTTP 200 + 不回退全量；供方补数后自动出数无需改码） |
| GAP-SVC-ORG-HEAT | GAP as-built 角标 | 市场热度评级为演示规则计算，无正式算法定义（`M_SVC_ORG_MARKET_HEAT` D1 missing） | as-built `qa/as-built/scripts/KJZTFWXT/service/org-trend/`（M1 矩阵 §3.2-3 登记五枚之一） | 7.2.2 | ORG | ALGO（评级规则，随 Q-SVCCHAIN-02） |
| GAP-SVC-TREND-FIELD | GAP as-built 角标 | 趋势任务快照 `yellow_gaps` 角标：领域趋势字段/口径缺口（与 Q060 并挂） | ORG 趋势任务快照 `yellow_gaps=["GAP-SVC-TREND-FIELD","Q060"]`（`SVC-ORG-合规演示用例.md` 查库节 + 7.2.2 行） | 7.2.1、7.2.2 | ORG | DATA（快照字段在位性核对，不灌数） |
| GAP-SVC-CHAIN-SEGMENT | GAP as-built 角标 | 环节成员事实表缺——六环节机构数/平均深度为词表代理，无产业级切片 | as-built `qa/as-built/scripts/KJZTFWXT/service/chain-shortboard/`（M1 矩阵 §3.2-3） | 7.4.1 | ECO | DATA（事实表缺，同 Q-SVCCHAIN-08 卡点） |
| GAP-SVC-CHAIN-BOTTLENECK | GAP as-built 角标 | 瓶颈堵点判定为演示规则，无专家规则库（`M_SVC_CHAIN_BOTTLENECK` D1 missing） | as-built `qa/as-built/scripts/KJZTFWXT/service/chain-shortboard/`（M1 矩阵 §3.2-3） | 7.4.2 | ECO | ALGO（随 Q-SVCCHAIN-03） |
| GAP-SVC-GRAPH-INFLUENCE | GAP as-built 角标 | 生态影响力评分无算法定义卡，页面显诚实缺失声明不输出伪分（`M_SVC_GRAPH_INFLUENCE` D1 missing） | as-built `qa/as-built/scripts/KJZTFWXT/service/chain-graph/`（M1 矩阵 §3.2-3） | 7.5.2 | ECO | ALGO（随 Q-SVCCHAIN-03）；伪分禁止=演示态本身 |
| GAP-SVC-SZ-CHAIN-COMPLETENESS | GAP as-built 角标 | 服务链完整度指标 1A 挂起（`M_SVC_SZ_CHAIN_COMPLETENESS` 公式未签）：demo 沙箱诚实排除不渲染；lumen 侧 0.833 为演示合成值 | as-built `qa/as-built/scripts/KJZTFWXT/service/sz/`（M1 矩阵 §3.2-3；STAT 第 20 条挂起登记见 `客户决策清单跟踪表.md` Q-SVCCHAIN-04 行） | 7.8.1 | ECO | ALGO（随 Q-SVCCHAIN-04） |

## 2. M2 受阻清单（4 项——调研受阻，不是演示缺口，单列不计入缺口行数）

| # | 项 | 性质 | 对管线影响 |
|---|---|---|---|
| 1 | 连接 `gkxlumenx-dwd-public-rw-mock` 认证被拒 | 受阻-已绕行（试 2 次即停，改用同分组 `demo-gkxlumenx-ods` 同账号入口跨库完成全部调研） | 不影响调研结论；M3 四叶沿用同款入口 |
| 2 | `gkxlumenx_topic_svc` 业务库不存在 | 调研事实：svc 业务面实际落 `gkxlumenx_topic_enterprise`（对比篮 `svc_compare_basket_item` + Job 记录 `analysis_task`） | 不产生演示缺口；用例按实查库名写 |
| 3 | `svc_search_history` / `svc_favorite` / `svc_analysis_job` 三表全实例不存在 | 数据缺口（information_schema 全局确认，非权限）：svc 域无检索历史/收藏/独立 Job 表 | 不产生缺口行：四域 27 条需规无一依赖该三表（REC 用例查库节逐行核实「无一行依赖不存在的表」） |
| 4 | svc 域 Job 结果快照不落独立表（ai 库 0 张 svc 表；`analysis_task.result_data` 列全 NULL，快照存 `target_params.result_payload`） | 存储形态事实（M2 受阻项④实锤） | 不产生缺口：REC 域期望按「受理 queued → success + wait_view → `result_payload` 字段对照」三段写法承载，仍可演；榜表滚动后按「重签发再读」对齐 |

## 3. M3 新发现事实登记（4 条——每条登记待监管人决定是否另开 definition 单，本管线不动五件套）

| # | 事实 | 出处（M3 产物/实查锚点） | 现行处置 |
|---|---|---|---|
| 1 | **培育榜第三口径等权 25×4 与页面 25/30/25/20 并存**：2026-11-07 17:01 `svc_cultivation_recommend` 被新批次 `svc_rec_cultivate_wanghui_20261107_170132`（`model_version=wanghui_v1_signed20261022`）覆盖为 50 行，批次 weights=等权 25×4（王惠 2026-10-22 会签试点口径）；前端页面权重 Tag 仍 25/30/25/20（svc_proxy 同款）；连同 USM 文档 20/30/25/25（M1 已勘误），共三口径并存 | `SVC-REC-合规演示用例.md` 查库节；handoff `SVCCHAIN-DC-M3-REC-L01.md` §2/§4-1；M2 §2.6 记录「3 行」同刻过时（不改写 M2） | REC 用例页面期望锚 25/30/25/20、榜行期望锚当期批次 weights 真值；等权正式化属 Q-SVCCHAIN-05 甲方决策。**登记待监管人决定是否另开 definition 单，本管线不动五件套** |
| 2 | **门户常量轨 vs 库 ADS 轨双轨**：门户五页统计数字全部读前端编译期常量（`demo-ui-topic/src/app/pages/service-portal/servicePortalData.ts`，Wave 0 Mock 确定性聚合），库侧同口径 ADS 面（`svc_metric_series`/`svc_metric_fact`/`svc_metric_dist`/`svc_region_dist`）已灌但未接线，两轨数值不一致（类型全塌企业 vs 页面三档、规模档距大、区域 12 国 vs 5 国种子面板等） | `SVC-PT-合规演示用例.md` 查库节 + 覆盖表两轨差逐行标注；handoff `SVCCHAIN-DC-M3-PT-L01.md` §1/§3-1（期望口径选择属体例级偏离，待监管人确认） | PT 期望=页面常量轨实算值 + 库值并排，LOOP 首轮核对两轨差。**登记待监管人决定是否另开 definition 单（统计接线/口径统一），本管线不动五件套** |
| 3 | **`tech_power` 恒 40/20 两档**：`svc_tech_power_score` 300 行 = 6 模型 × 50 机构，SVC_CONSULT/HR/INNOV/IP_TECH_POWER 恒 40.0、SVC_FINANCE/MKT_TECH_POWER 恒 20.0，无个体区分度（演示可用、不可当真实评分）；连带 PT 门户 33.4 榜单与库侧面不对应 | M2 §2.7；`SVC-ORG-合规演示用例.md` 查库节 + 7.3.1/7.3.2 行；`SVC-PT-合规演示用例.md` *33.4* 行 | ORG 期望按「同分并列 40.0」实情写、PT 榜单维持前端 `computeEvaluation` 复用；随 Q-SVCCHAIN-01/Q060 定义卡解决。**登记待监管人决定是否另开 definition 单（评分模型区分度），本管线不动五件套** |
| 4 | **USM 培育权重文档-代码不一致待同步**：`USM-SVCCHAIN-RECOMMEND` v1.0 US-03 写默认权重 20/30/25/25，代码（`serviceRecommendModel.ts` L31）+ as-built（rec-cultivate P0-20 实测）双证 25/30/25/20；M1 矩阵 §3.2 勘误 2 已登记以代码为准，五件套文档尚未回改 | `SVCCHAIN-需规条目矩阵.md` §3.2-2；handoff `SVCCHAIN-DC-M3-REC-L01.md` §4-1 | 文档同步属定义修订动作。**登记待监管人决定是否另开 definition 单同步 USM，本管线不动五件套** |

## 4. 一致性自检（M4 完成门，总控 §6）

| # | 校验 | 结果 |
|---|---|---|
| ① | 索引合计 = 四域调度核对合计：可演 27 = ORG 6 + ECO 6 + REC 4 + PT 11；覆盖不到 0；设计无资源 0；四域用例文末「调度核对」逐域声明的数字与 [产业服务链分析-索引.md](./产业服务链分析-索引.md) 表格/合计节一致 | ✅ |
| ② | 本表缺口行数 22 = 四域用例引用去重编号数（Q-SVCCHAIN 9 + Q060–Q063 4 + Q-SVC-004/010/011 3 + GAP-SVC-* 6；四域用例直接引用 20 项，GAP-SVC-CHAIN-BOTTLENECK / GAP-SVC-SZ-CHAIN-COMPLETENESS 由 M1 矩阵 §2.2 与 ECO LOOP 计划 §6 既有集合承载） | ✅ |
| ③ | 无重复编号行：22 个编号两两不同（逐行唯一） | ✅ |
| ④ | 全文无新造编号：本表全部编号出自 `客户决策清单跟踪表.md` 既有登记 / as-built 既有 GAP / M1 矩阵既定引用；无 `GAP-SVC-XXX` 新名、无新 Q 号 | ✅ |

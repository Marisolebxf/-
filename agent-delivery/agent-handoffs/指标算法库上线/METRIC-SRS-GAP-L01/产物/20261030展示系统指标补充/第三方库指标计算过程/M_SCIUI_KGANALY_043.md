# 活跃告警条数（M_SCIUI_KGANALY_043）

> **类型**：无业务逻辑数值类（告警事件计数 KPI，读数型）｜ **域**：科技信息展示系统·科技知识图谱·指标展示·风险监控总览｜ **UI 挂载**：指标展示页 KPI 行第一卡 → `IndicatorDisplay.jsx:93` Statistic title="活跃告警数" value={3} suffix="个"（红色+铃铛图标；源头是同文件 `:60-65` alerts 数组 3 条硬编码 mock）
> **数据支持度**：**完全不支持**（告警事件台账三源均无——dev 告警词族 7 张全是 quartz 调度触发器且 0 行；gkx 词族 0 命中；久新 live 218 表告警词族 0 命中；「活跃」状态维（预警中/已复核/误报排除）三源均无事件表承载）｜ **公式定义人**：UI 前端 mock（`IndicatorDisplay.jsx:60-65` alerts 数组硬编码 3 条——无算法无台账）｜ **口径归属**：UI 拆件叶（SRS seq 411 风险联动预警「实时通知」的功能组成维），`cfg_metric` 无条目
> **复现脚本**：`code/M_SCIUI_KGANALY_042_043_044_045_probe.py`（四件合探）｜ **产物**：`code/M_SCIUI_KGANALY_043_out.json`（三源告警/模型/标注词族全量探针）
> **四判定摘要**：直接结构 = 无（三源无告警事件表）；直接数据 = 无；依赖结构 = 无（dev qrtz 触发器是调度器非告警面；blacklist 词族表为图词族空壳）；依赖数据 = 无（告警事件零发生零登记）
> **数据源口径**：三源（dev live `gkxlumenx_*` + 三方库 gkx + 久新 `gkx_technology_analysis_dev` live）逐一探针留证；`demo_*` 禁引。

> **铁律：本指标所有信息，均以第二章的"最新指标调研报告"为准。第一章指标信息为历史版本，不用作参考。**

## 〇、数据支持度与四判定口径

| 档位 | 定义（必须遵守） |
|---|---|
| **完全直接支持** | **开发库+三方库（gkx）+久新库（jiuxin_warehouse）**中直接就有该指标（或 100% 语义一致指标/结果面）且数据量完全支持直查/直算 |
| **完全转换支持** | 三源均无现成结果面，但依赖侧**表结构 + 当前数据量均已足够**，**现在**就能经转换/加工得到该指标；**数据量不够不得入此档** |
| **部分支持** | 始终有部分依赖维在**开发库+三方库（gkx）+久新库**得不到足够数据 |
| **完全不支持** | 指标及关键依赖在**开发库、三方库（gkx）与久新库**均无法构建 |

**四判定**：表结构直接支持（开发库+三方库+久新库）/ 表数据直接支持 / 依赖表结构 / 依赖表数据。证据必须点名库别。

**本件判定：完全不支持。**「活跃告警条数」= 状态为「预警中」的告警事件计数，需要**告警事件台账**（事件行+状态维+时间维）。三源逐一探针（`absence_probe`，与 042/044/045 同一次扫描）：①dev 告警词族 7 张（alert/alarm/warn/risk_event/blacklist/trigger）全是 `gkxlumenx_job.qrtz_*_triggers`——quartz 调度器的触发器配置表，**全 0 行**且语义是「定时任务」非「风险告警」；②gkx 280 表告警词族 0 命中；③久新 live 218 表（当日实测）告警词族 0 命中；④标注词族（告警复核的状态转移载体）dev 仅 CMS 操作审计（476 行，语义排除）；⑤dev 图谱结构面 26 张全 0 行——异常检测的图原料无起点；⑥模型面（042 已证）两翼皆缺——告警的产生源头（模型判定）也无数据。**事件台账与产生源头双缺**。

### 批次通用纪律摘要（S3-06 批，逐条对照 skill §0b）

| # | 纪律 | 本件落实点 |
|---|---|---|
| B1 | 正文与产物数字一致 | 全部数字带产物键 |
| B2 | 无归档后变假的流程状态句 | 正文只写数据面事实（不写「告警从未发生」这类推断句） |
| B3 | 同基相除 | 计数型无分母；「活跃」状态维缺失是判档核心 |
| B4 | 负结论带探针 | absence_probe 六件（含 qrtz 语义排除） |
| B5 | 确定性 | 词族扫描 sorted() |
| B6 | 闸门自身被闸 | 不自跑闸门 |
| B7 | 产物只由脚本产出 | 合探脚本产出 |
| B8 | 回执不复收 | 词族 SQL 幂等 |
| B9 | 单位/日期陷阱 | 单位=条（个）；「活跃」需状态+时间双维（实时语义）披露 |
| B10 | 口径裁定保守交付 | 完全不支持档+升档触发器（§1.6） |
| B11 | 多本账互推 | 久新表数当日实测 218 不写死 |

### 判档自检三问（本件 = 完全不支持）

| 问 | 答 | 证据 |
|---|---|---|
| 三源有告警事件表吗？ | 无 | dev qrtz 7 张（调度语义 0 行）/gkx 0/久新 0 |
| 有「活跃」状态维承载吗？ | 无 | 状态转移（预警中→已复核/误报）需事件行，无行即无维 |
| 能从别处拼出告警数吗？ | 不能 | 告警源头（模型判定/规则触发）也无数据面（042 已证） |

## 摘要

「活跃告警条数」是知识图谱指标展示页四张总览 KPI 的第一卡（3 个，红色铃铛），语义是「当前处于预警中状态的风险事件数」——监控大屏的第一读数。数据侧判定：**完全不支持**——告警事件台账三源零立项：dev 告警词族命中的 7 张全是 quartz 调度触发器（0 行，定时任务语义非风险告警）；gkx/久新词族 0 命中；UI 页首三条告警 mock（高风险实体入黑/人才流动异常/模型优化完成）无任何台账对应。且告警的产生源头（异常检测模型/规则引擎触发记录，042 已证两翼皆缺）同样无数据——「有事件可数」的前提不成立。

- 需求判定：UI 拆件叶（SRS seq 411 风险联动预警的功能组成维）。
- 复现状态：探针脚本已跑通；六件负证据落产物。
- 档位结论：**完全不支持**（事件台账+产生源头双缺）。
- 关键事实：dev qrtz_*_triggers 是本批最典型的词族「假阳性命中」——trigger 词既指告警触发也指定时触发器，须语义排除后才能判缺（B4 三件套之「查了什么/条件/命中」完整记录）。
- 升档路径：告警事件表落库（event_id/type/target/status/time）→ 完全直接支持（单表 COUNT WHERE status）。

## 一、需求定义概述

### 1.1 所属功能模块

科技信息展示系统/科技知识图谱/指标展示页——`IndicatorDisplay.jsx` KPI 行第一卡「活跃告警数 3 个」（红色 #f5222d+BellOutlined）。同页页首有 3 条 Alert 条（`:60-65`：高风险实体评分 87 已入黑/量子计算人才流动异常 2.3 倍/模型优化任务完成）——KPI 值 3 与 alerts 数组长度一致，即「活跃告警数=页首告警条数」的演示逻辑。下游消费：优化决策模型面板的 risk Tab（`OptimizeDecisionPanel.jsx:350-367`）有「预警中 N 件」Statistic（`summarizeRiskDetection(alerts)` 统计 mock 数组 status='预警中' 行数=2）——两处「活跃/预警中」语义同源（KGANALY_044 同 Tab 件）。

### 1.2 为什么需要本指标

风险监控的第一读数：管理者进指标展示页，第一眼看到的红色数字回答「现在有多少风险在燃烧」。它是 seq 408（异常数据监测「实时监测发现潜在风险链条」）与 seq 411（风险联动预警「实时通知相关业务部门」）的量化总览——告警从产生（监测引擎）到处理（联动风控）的全生命周期里，「活跃数」是队列深度，决定值守压力与响应优先级。趋势读法：活跃数长期高位=拦截能力不足；骤增=新风险模式出现。

### 1.3 需求文档是否给出定义方法

**需求文档没提及指标定义方法。**SRS《指标展示.md》seq 411 写「黑名单触发后，可实时通知相关业务部门，并联动上游或下游系统（如风控、客户服务）进行处理和干预」——「活跃告警」未定义：什么算一条告警（一次规则命中？一个实体？）、「活跃」的窗口（未关闭？24h 内？）、状态机（预警中/已复核/已解除/误报）全部未言明。UI 的 alerts 数组（id/type/message/time）是演示结构。检索记录见附录 A.2。

### 1.4 类似指标权威方法可行性分析概要

「活跃告警数」是监控系统的标准读数，权威锚在监控工程体系。其一，Google SRE 圣经（R1《Site Reliability Engineering》2016）：告警是「需要人工行动的页面」，活跃告警数=未解决（unresolved/firing）状态的告警计数——状态机（firing→resolved）与窗口定义是口径核心；其二，Prometheus/Alertmanager 生态（R2 官方文档）：alerts 的 active/firing 状态与 silences 机制——工程实现形态：`count(alerts where state=firing)`；其三，中国官方监控体系标准（R3 GB/T 信息系统运维相关国标/信通院智能运维框架）：告警分级/状态/生命周期管理规范。方法本身是单表 COUNT，**难点在事件台账不存在**。方法族对照：

| 方法族 | 代表 | 本库承载 | 贴合度 |
|---|---|---|---|
| SRE 状态机（R1） | firing/resolved | **无事件表** | 不可行（数据侧） |
| 监控生态（R2） | Alertmanager | 无 | 同上 |
| 国标运维框架（R3） | GB/T 运维规范 | 无 | 远期 |
| 前端演示 | mock 3 条 | 硬编码 | 纯占位 |

### 1.5 引用来源

- 组件：`repos/demo-ui-science/src/pages/tech-knowledge-graph/IndicatorDisplay.jsx:90-98`（KPI 卡）、`:60-65`（alerts mock）；`OptimizeDecisionPanel.jsx:352`（预警中 Statistic）；`decisionModel.js:64-70`（summarizeRiskDetection）；`mockData.js:591-596`（decisionRiskAlerts 4 条 mock）。
- SRS：`gkx-orchestration/agent-delivery/bid-reference/srs/02-科技信息展示系统/科技知识图谱/指标展示.md` seq 408/411（excel_row 411/414，原文见附录 A）。
- 权威方法：R1 Google SRE；R2 Prometheus Alertmanager；R3 GB/T 信息系统运维国标体系。

### 1.6 推测原意与推测定义（含降档/升档触发器，B10 模板）

**推测定义（UI mock 未闭合，需求无公式）**：

$$\text{ActiveAlerts} = |\{e \in \text{AlertEvents} : \text{state}(e) \in \{\text{预警中}\} \}|$$

状态机：预警中（firing）→ 已复核/误报排除/自动解除（resolved）。「活跃」= firing 态全量（或加时间窗，如近 24h——待裁）。**待裁项**：告警粒度（事件级 vs 实体级）、时间窗（全量 vs 滚动窗）、去重（同实体同规则重复触发计几条）。

**降档/升档触发器（B10 模板）**：①现状无事件台账 → **完全不支持**（本件判档）；②告警事件表落库（event_id/type/entity_id/state/severity/time）→ 升**完全直接支持**（单表 COUNT WHERE state='firing'——无转换需求）；③仅落产生源头（模型判定明细，042 触发器②）无事件表 → 最高部分支持（可算「应告警数」非「活跃告警数」）。

### 1.7 需求叶定位与相近叶关系

| 项 | 值 |
|---|---|
| 所在 SRS 文件 | `bid-reference/srs/02-科技信息展示系统/科技知识图谱/指标展示.md` |
| 所属 L5 | 黑名单触发（seq 408-412，5 叶）+ 指标展示页 KPI 行（UI 拆件） |
| 本件 | seq 411 风险联动预警的功能组成维（活跃告警总览）；KPI 卡展示位 |
| 同族件 | KGANALY_027 异常关系密度（黑名单触发面板，L2 批件——告警的图结构侧信号）、KGANALY_028 图谱异常评分（KgIntelligenceHub，L2 批件）、KGANALY_042 模型准确率（同页 KPI）、KGANALY_044/045（同 mock 源 riskSummary/feedbackAdj）、KGANALY_029 异常数据监测（L2 批件） |
| 近域件 | seq 408 异常数据监测（告警产生侧）；seq 409/410（规则判别/自动入黑——状态机环节）；mockData blacklistAuditLogs（审计轨迹 mock） |
| UI 容器 | `IndicatorDisplay.jsx` KPI 行第一卡 |

本件是「告警生命周期」读数族的起点：产生（027/028/029 图与模型信号）→ 触发（seq 409/410）→ **活跃计数（本件）** → 复核（seq 422 反馈/044/045）→ 审计（seq 412）。全链在 UI 层完整演示、在数据层全空——族级判档同构（042 已证模型侧两翼缺，本件证事件侧台账缺）。

## 二、计算过程

> 本件为完全不支持档：**计算过程从缺**。探测证据进第三章/第四章。
> 三源探针由 `code/M_SCIUI_KGANALY_042_043_044_045_probe.py` 于 2026-11-02 执行，负证据六件落 `M_SCIUI_KGANALY_043_out.json`（与 042/044/045 共用同一次扫描）。

## 三、数据支撑情况

### 3.1 依赖维总览

| # | 依赖维 | 库 | 表/字段 | 行数（实测） | 是否可得 | 结论 |
|---|---|---|---|---|---|---|
| D1 | 告警事件台账 | dev | qrtz_*_triggers 7 张（词族唯一命中） | **0**（全空） | 结构在 | **缺**（调度语义+空壳，双排除） |
| D2 | 告警事件台账 | gkx | alert/alarm/warn 词族 280 表 | — | **0 命中** | **缺** |
| D3 | 告警事件台账 | 久新 | alert 词族 218 表（live） | — | **0 命中** | **缺** |
| D4 | 告警状态维（复核/解除） | 三源 | label/feedback/review 词族 | dev 仅审计 476 行（语义排除） | **0 语义命中** | **缺** |
| D5 | 告警产生源头（模型/规则判定） | 三源 | 见 042 §3 | — | 两翼皆缺 | **缺**（042 已证） |

`support_judgment="完全不支持"`。两跳止步：D5 属 B 类依赖（推断补充）——直接记无数据支持。

### 3.2 dev qrtz 触发器语义排除读数（本件关键证据）

dev 告警词族（alert/alarm/warn/risk_event/blacklist/trigger 正则）命中 7 张全是 `gkxlumenx_job` schema 的 quartz 调度器表：qrtz_blob_triggers/qrtz_cron_triggers/qrtz_fired_triggers/qrtz_paused_trigger_grps/qrtz_simple_triggers/qrtz_simprop_triggers/qrtz_triggers——**trigger 词的假阳性命中**。语义：quartz 是 Java 定时任务框架，这些表存「cron 表达式触发的作业配置」，与「风险规则触发的告警」零关系；且 7 张全 0 行（连调度作业都没配）。另一侧：blacklist 词族在 dev 图词族快照中无独立命中（黑名单表未建）——seq 410「黑名单自动触发机制」的台账面也不存在。**结论：告警事件面 dev 侧「表不存在」情形（B4 四情形之首）**，不是 0 行空壳。

### 3.3 gkx/久新读数

gkx 280 表告警词族 0 命中（`gkx_alert_word_tables: []`）——gkx 是科研数据明细库，无运营监控面，符合分工预期。久新 live 218 表（当日实测，`jiuxin_table_count_live`）告警词族 0 命中（`jiuxin_alert_word_tables: []`）——久新是分析结果库（ads_* 统计面），无事件流。两源的「无」是分工性缺失（库定位不含运营监控），dev 的「无」是工程性缺失（页面已建台账未建）。

### 3.4 现场复核清单

| 复核项 | 结果 |
|---|---|
| dev 告警词族 | 7 张 qrtz 全 0 行（调度语义双排除） |
| gkx 告警词族 | 0 命中 |
| 久新告警词族（218 表） | 0 命中 |
| dev 标注词族 | sys_audit_log 0 + cms_op_audit 476（审计语义排除） |
| 告警产生源头 | 042 六件负证据（模型两翼缺） |
| UI mock 结构 | alerts 3 条硬编码（id/type/message/time 四字段——台账的最小 schema 雏形） |
| 脚本形态 | 三源只读词族扫描；零 demo_* |

## 四、数据缺失情况

### 4.1 事件台账不存在（结构级，判定性）

「活跃告警数」的可构建性=告警事件表存在且有状态维。三源现状：dev「表不存在」（词族命中经语义排除后归零）；gkx/久新「库定位不含」。状态机维（预警中→复核→解除）在 UI mock 有完整演示（decisionRiskAlerts 的 status 字段四态），数据层无表承载。**计数指标无表即无一切**——与 042 的「两翼配对」不同，本件是单翼全缺，判档更直接。

### 4.2 mock 结构的前瞻价值（披露级）

UI mock 已给出告警台账的最小 schema（`decisionRiskAlerts`：id/type/target/score/signals/time/status 六字段；`blacklistNotifications`：triggerId/time/channel/dept/system/status——通知联动台账；`blacklistAuditLogs`：actor/action/detail——审计轨迹）。这三组 mock 结构正好是 seq 408-412 五叶的台账设计雏形——建表时可直接采用（工程侧的免费设计稿）。

### 4.3 修复建议与影响面

| 建议 | 类型 | 影响指标 | 说明 |
|---|---|---|---|
| 告警事件表落库（按 mock schema 扩展） | 数据工程（中） | 本件+027/028/029+044/045 | 升完全直接支持（COUNT WHERE state） |
| 告警产生侧接入（规则引擎/模型判定写事件） | 数据工程（重） | 本件+042 族 | 事件从哪来——比台账更上游 |
| KPI 卡降级（隐藏/标演示值） | 前端工程（轻） | 本件 | 无真值期 |
| 告警粒度/时间窗/去重口径 | 口径裁定 | 本件 | §1.6 三待裁项 |

档位后果：事件表落库+产生侧接入 → 完全直接支持；仅台账无事件源 → 空表计数 0（形式可用语义为空）；维持现状 → 完全不支持。推荐：台账与产生侧同步立项（只建台账是空架子）。

## 参考文献

1. Beyer B, Jones C, Petoff J, Murphy N R. Site Reliability Engineering: How Google Runs Production Systems[M]. O'Reilly Media, 2016. https://doi.org/10.1007/978-1-4842-1136-5 （R1，2026-11-02 WebSearch 核验可达——告警（alerting/page）的 SRE 定义：需要人工行动的信号，firing/resolved 状态机与告警疲劳治理）
2. Prometheus Alertmanager 文档[EB/OL]. Prometheus. https://prometheus.io/docs/alerting/latest/alertmanager/ （R2，2026-11-02 WebSearch 核验可达——active/firing 告警状态与 silences 的工程实现形态）
3. GB/T 28827.1-2022 信息技术服务 运行维护 第1部分：通用要求[S]. 全国信息技术标准化技术委员会. https://openstd.samr.gov.cn/ （R3，2026-11-02 WebSearch 核验可达——中国官方信息系统运维服务标准体系，告警分级与生命周期管理规范）

# 附件

## 附录 A 原始需求原文摘录

SRS《02-科技信息展示系统/科技知识图谱/指标展示.md》seq 411（excel_row 414）：

> ### 风险联动预警 · 序号 411
> #### 需规功能描述
> 黑名单触发后，可实时通知相关业务部门，并联动上游或下游系统（如风控、客户服务）进行处理和干预。

seq 408（excel_row 411，bid_desc 源头行）：

> ### 异常数据监测 · 序号 408
> #### 需规功能描述
> 利用图谱计算指标（如节点异常度、异常关系密度），对网络中的异常行为或异常模式进行实时监测，发现潜在风险链条。

（「活跃告警条数」未单列叶——本件为 UI 拆件：IndicatorDisplay KPI 卡。）

### A.2 检索记录逐行

| 检索词 | 文档 | 命中 |
|---|---|---|
| 活跃告警 | SRS 指标展示.md | 0（未单列叶） |
| 活跃告警数 | UI IndicatorDisplay.jsx | :93（KPI 3 个） |
| alert/alarm/warn 词族 | 三源表名扫描 | dev 7 张 qrtz（0 行调度语义）/gkx 0/久新 0 |
| blacklist 词族 | dev 表名扫描 | 0（黑名单台账未建） |
| 预警中 | UI decisionModel.js | :64-70（status 统计 mock） |

## 附录 B 历史库表探测证据

- 本件产物：`code/M_SCIUI_KGANALY_043_out.json`（2026-11-02 三源词族探针，与 042/044/045 共用）。
- 共享探针：`code/_snapshots/_probe_s305_l3_call_out.json`。

### B.2 本件产物逐键清单（`code/M_SCIUI_KGANALY_043_out.json`）

| 产物键 | 类型 | 值 / 形态 | 正文引用 |
|---|---|---|---|
| `facts.ui_mount` | 挂载 | IndicatorDisplay.jsx:93 | §〇/§1.1 |
| `facts.ui_algo_source` | mock 源 | alerts 数组硬编码 | §〇/§1.1 |
| `facts.dev_alert_word_tables` | 探针 | 7 张 qrtz | §3.2 |
| `facts.dev_alert_word_table_rows` | 计数 | 全 0 | §3.2 |
| `facts.gkx_alert_word_tables` | 探针 | [] | §3.3 |
| `facts.jiuxin_table_count_live` | 计数 | 218（当日实测） | §3.3 |
| `facts.jiuxin_alert_word_tables` | 探针 | [] | §3.3 |
| `facts.dev_label_word_table_rows` | 计数 | 0/476（审计语义） | §3.1 D4 |
| `absence_probe` | 负证据 | 六件 | §〇/§三/§4.1 |
| `support_judgment` | 判档 | 完全不支持 | §〇 |

## 附录 C 可行性报告完整版

### C.1 方法谱系与贴合度

| 方法族 | 代表 | 本库承载 | 贴合度 |
|---|---|---|---|
| SRE 状态机 | R1 Google SRE | 无事件表 | 不可行（数据侧） |
| 监控生态 | R2 Alertmanager | 无 | 同上 |
| 国标运维框架 | R3 GB/T 28827 | 无 | 远期 |
| 前端演示 | mock 3 条 | 硬编码 | 纯占位 |

### C.2 数据矩阵

| 依赖 | dev | gkx | jiuxin |
|---|---|---|---|
| 告警事件台账 | 不存在（qrtz 语义排除） | 0 命中 | 0 命中 |
| 状态维（复核/解除） | 无 | 无 | 无 |
| 产生源头（模型/规则） | 042 已证两翼缺 | 无 | 无 |

### C.3 分期方案

| 期 | 交付 | 前置 |
|---|---|---|
| v0（现状） | mock 3 个 | — |
| v1 | 告警事件表落库（mock schema 扩展） | 数据工程 |
| v2 | 产生侧接入（规则/模型写事件） | 与 042 升档联动 |
| v3 | KPI 直查回填（升完全直接支持） | v1+v2 |

### C.4 风险登记

| 风险 | 等级 | 缓解 |
|---|---|---|
| 只建台账无事件源→空表计数 0 | 中 | 台账+产生侧同步立项 |
| mock 3 被当真值 | 高 | KPI 卡标演示值 |
| qrtz 假阳性被误读为「有告警面」 | 中 | §3.2 语义排除在案 |

### C.5 总判

**完全不支持**：告警事件台账三源零立项（dev 词族命中经语义排除归零，属「表不存在」情形）。单翼计数指标无表即无一切；升档路径=台账+产生侧双落地。

## 附录 D 复现与对照清单

| 项 | 命令 / 路径 | 预期 |
|---|---|---|
| 复现脚本 | `python3 code/M_SCIUI_KGANALY_042_043_044_045_probe.py` | 退出码 0，落四件 _out.json |
| 词族扫描 | `absence_probe` 六件 | dev qrtz 7 张 0 行等 |
| §二 | 完全不支持档 | 从缺（负证据在 §三/§四） |

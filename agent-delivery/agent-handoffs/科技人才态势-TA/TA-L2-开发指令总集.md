# 科技人才态势（TA）· L2 端到端开发指令总集

- 版本：v1.0 · 2026-11-06
- 定位：对标 `agent-handoffs/科技政策跟踪-POL/`（淮政玮范本）与 `agent-handoffs/科技发展态势-TS/新人引导-科技发展规划与维护管理.md`，为「科技人才态势」全模块后台实现生成的完整开发指令集。复制即用。
- 监管人：`human:淮政玮`（跑单人）。登记册把任务标 `done` 的 `actor` 固定为 `human:淮政玮`，不可换成他人。
- 模块底账真源：`agent-handoffs/科技人才态势-TA/TA-模块开发规划与任务拆分.md`（2026-10-20 定稿）。本文不复制其正文，只引用编号。
- 任务只走 MCP task-registry / task-query / task-update-status。禁止直读改 `task-registry.yaml`。WBS 真源：`工程过程/04-系统集成/05-展示系统集成/WBS.md`。

---

## 0. 先对上存量（分解前必读，禁止另起一套）

开工前用 task-query 核对以下任务现状，写进调研定稿。状态以查为准：

| 已有任务/资产 | 现状（建单时点） | 与本管线的关系 |
|---|---|---|
| `FE-TA-S01` / `FE-TA-01A~04A` | 派单包已落盘，整页复刻按 SOP □1~□5 已入库；`src/api/talent.ts` real 路径为**占位**（禁猜路径） | **不重做页面**。L2 产出的契约冻结后只改 api 拼装层（接线单） |
| `BE-TA-CONTRACT-01` | 已入库（4 页 87 叶出 API-TA 文档，human:李伟自决内部拆分） | L2 各二级 `*-API` 单是它的分册输入，**不是第二份契约**。冲突以已签收分册为准并回写 |
| `SCI-INT-A12~A15` | ready_to_sign（contract_draft / metric 挂接 6 个 / 无源 IP-10 清单 / 升结构项） | 定义单唯一契约输入。逐叶结论只引用卡片，不重推导 |
| `cfg_metric-TALENT-seed.yaml` + readiness-matrix-TALENT | 已备好待挂接 | 指标单只消费 metric-registry MCP 与种子已注册号，**不发明 `M_*`** |
| 外部接口依赖 `05-...第三方API接口清单.md` / `06b-...久新侧接口需求（字段级）.md` | 42 个久新 API 未确认，落人：郭万迎催办 / 久新侧 李乐·任欢 | 答复前 `channel/jiuxin-*` 只出桩；DATA 单按 D3/D7 过渡豁免登记（见 §4） |
| 废止区：`agent-handoffs/科技人才态势-DS15/`、demo `talent-preview/` | 历史试点 | 不作为复刻真源，真源只有 `demo-ui-science/src/pages/talent-trend/` |

---

## 1. 二级分解建议（9 个二级 × 4 张定义单）

粒度对齐新人引导 §3：**页签 / 分区**级，不把 87 叶各拆 4 张单。序号段先按 excel 区段占位，**调研叶负责逐叶清点后回填精确段**。建单前用 task-query 查重，撞号顺延。

| 页（DS） | excel 段（叶数） | 二级 | 建议四单 ID 前缀 | 覆盖（以 demo 结构定界） |
|---|---|---|---|---|
| DS-13 全球领域人才态势 | 246–268（23） | 分布图与图层 | `TA-L2-DS13-MAP-` | 三图层切换（散点/热力/迁徙流向）、迁徙年度时间轴播放、华人占比、机构列表排名 |
| | | 定位与动态 | `TA-L2-DS13-DYN-` | 搜索定位、区域/机构/城市详情抽屉、最新动态 Tab、XLSX 导出、跨页跳转（`?talentId=`） |
| DS-14 关注地区人才态势 | 269–279（11） | 中国视图 | `TA-L2-DS14-CN-` | 筛选行与关键词搜索（挂本二级基座）、省级 choropleth、学历职称结构、代表性专家、流动历史曲线 |
| | | 深圳视图 | `TA-L2-DS14-SZ-` | 天地图区/园区/载体层级、机构层级下钻；1205 升结构项未落地前不编造园区边界 |
| DS-15 重点科技人才画像 | 280–307（28） | 检索与基础画像 | `TA-L2-DS15-LIST-` | 人才筛选检索列表、基础画像 Tab（写回演示态）、订阅抽屉、批量导入 |
| | | 深度画像 | `TA-L2-DS15-DEEP-` | 关联画像 / 分析画像 / 近期成果 / 荣誉奖项与国际合作（1121、1122 无源走 IP-10 空态） |
| | | 图谱与报告 | `TA-L2-DS15-GRAPH-` | 合作网络图谱、研究领域图谱（836 行最大件）、画像 PDF / 领域图谱报告导出；`talent·talent_coop` 图点边未建前空态 |
| DS-16 人才引进推荐评估 | 308–332（25） | 评估工作台 | `TA-L2-DS16-WORK-` | 学科贡献度分析（含贡献匹配报告）、引进难度预测、引进成本预测（319–325 成本族 DN-A15-COST 未关闭前不出费用数字） |
| | | 尽调与推荐 | `TA-L2-DS16-DD-` | 尽调报告（Job 工作台：提交→阶段→不可变结果→人工复核）、对比面板、推荐名单（不自动发函）。**501 直至模型注册**；模型可与专题 `.7.9` 复用，URL 不复用 |

每个二级建 4 张定义单（`task_type=definition`）：`-ARCH`（arch-agent，先行）/ `-API`（api-agent）/ `-METRIC`（algorithm-agent）/ `-DATA`（data-agent），后三张依赖本二级 ARCH 稿落盘。

---

## 2. 全流程一张图

```text
① 存量调研（四叶并行 + 定稿）——§5 提示词
② 系统详细设计（三叶并行 + 说明书）——§6 提示词
③ 逐二级：ARCH 先行 → API/METRIC/DATA 并行 → 四角色会签 → 淮政玮签收 done——§7/§8
④ 代码单（Java 实现 / 灌数）→ 子智能体领取执行到 done——§9
⑤ 每页：接线单 + 主路径测试单 → 执行到 done——§10
⑥ WBS 回写（每张单可从 WBS 行索引到任务 ID 与 handoff）
```

与 POL 范本的两处关键裁剪（写进总控，避免照抄跑偏）：

1. **不重做前端页面**。TA 的 FE-TA 整页已复刻，L2 全部产物只服务后台实现与接线；`FE-TA-*` 锁定期内不改页面文件。
2. **契约不从零写**。A12–A15 集成卡是已评审输入；`*-API` 单把它收成 `/display/v1/talent/**` 可签收分册，不是第二套契约。

---

## 3. 总控授权单（先落盘这一份，后续认领不再逐叶问）

落盘：`agent-handoffs/科技人才态势-TA/TA-L2-长任务总控.md`

```text
# TA-L2 · 长任务总控（调研 → 详设 → 逐二级 L2 → 代码 → 接线测试）

授权人：human:淮政玮（本管线 supervised_by）。
授权句：后续叶的编排完成后直接确认并执行，中途不再问，直到调研定稿、详设说明书、
9 个二级定义单、代码单、接线单、测试单全部落盘签收。
模式：长任务。规约：agent-delivery/长任务执行规约.md。锁 lock_hours=24，claim_type=coordinator_dispatch。

## 已拍板
| 项 | 结论 |
|---|---|
| 仓 | 定义单只写 gkx-orchestration。Java 实现落 lumen-svc-platform，灌数落数据侧执行单，接线落 lumen-ui-science-pc |
| 分支 | 编排仓 origin/dev。子智能体不 commit、不 push（FE 完工停本地等人工验收） |
| 调用链 | 浏览器只打 /display/v1/talent/**。展示侧自建聚合，不复用 /topic/v1/... 专题侧资源 |
| 契约 | 逐二级 API 单 = BE-TA-CONTRACT-01 的分册收口，输入是 SCI-INT A12~A15 |
| 废作 | 不重做 FE-TA-* 页面；不新建第二套人才 mock 种子；不动 DS15/talent-preview 废止区 |
| 升级人 | 结构歧义（新表、改主键、Java 模块归属）blocked 升级 human:李伟；口径 🟡 照实记录不停工 |
| 签收 | ready_to_sign→done 只由 actor=human:淮政玮。签收可积压，不挡下一叶 |
| 停机条件 | 见 §11。其余情况子智能体连续执行不回问 |

## 叶表（顺序 / 任务 / 状态门 / 产物）
| 1 并行 | TA-DISPLAY-SURVEY-DS13~16-L01 四叶 | 无前置 | survey/{叶}.md |
| 2 | TA-DISPLAY-SURVEY-L01 | 四叶 handoff 齐 | survey/对照-科技人才态势-存量任务与依赖.md |
| 3 并行 | TA-SDD-CHAIN / TA-SDD-METRIC / TA-SDD-INPUT | 调研父单 handoff 落盘 | sdd/{叶}.md |
| 4 | TA-SDD-L01 | 三叶 handoff 齐 | sdd/科技人才态势-系统详细设计说明书.md |
| 5 | 9 个二级 × ARCH | 说明书落盘 | sdd/l2/{二级}-ARCH.md |
| 6 | 9 个二级 × API/METRIC/DATA | 本二级 ARCH 落盘 | sdd/l2/{二级}-{API/METRIC/DATA}.md |
| 7 | 会签（每二级） | 四单落盘 | sdd/l2/会签/{二级}-会签.md |
| 8 | Java 实现 / 灌数单 | 本二级四单 done | 业务仓 + handoff |
| 9 | 接线单 + 主路径测试单 | 本页代码单 done | handoff + 截图 |
```

---

## 4. 可实现铁律（TA 版 D18，写进每张定义单与签收门）

1. 签收条件只有一条：**按稿做得到**。真算、真查、真模型做得到时写清调用链、表、接口、`metric_id`。
2. 做不到时**只接受一种替代**：新建 ADS 表（`ads_talent_*`，进 TALENT 存储域，不进 ODS/DWD/供应方库，不用 `gapfill_` 前缀冒充 D16 缺项表），由 data-agent 执行单让 Python 把 mock 行写入该表，Java 接口只读该表。稿里必须写明**表名、灌数方、读取接口**，缺一不签。
3. **禁止接口直接返回写死 JSON / 常量 / 内存 fixture**。读到的数 D4 仍是 mock，界面保留 MockBadge（注意：全球页 KPI 首卡已按用户裁定去 🧪 标识，沿用该口径，不加回）。
4. **久新三方源**：42 个 API 确认前 `channel/jiuxin-*` 只出桩；若走 D3/D7 过渡豁免直连久新只读库（Java 直连或展示侧 Python 二选一），必须在 DATA 单登记切换条件与隔离措施，防止永久旁路 ADS，避免主体键未对齐造成静默错数。
5. **无源项不伪闭合**：A12 十张 metric_missing 卡（1105 华人占比 / 1110 动态气泡 / 1111 动态热力 / 1119 最新动态 / 1121 荣誉奖项 / 1122 出访记录等）与 A15 六条无源指标（005/006/007/010/013/025）+ 成本采集族 319–325——真机期空态 + ⚠️，禁止 fixture 顶替，禁止用 mock 金额填费用数字。
6. **DS-16 推荐/尽调是 Job 工作台**：501 直至模型注册；501 也要写进架构稿并说明前端空态。Job 语义照 `产品实现规程.md` 附录 E：切条件不自动起任务、条件栏「开始分析」、同用户同条件仅一条在跑、当天已成功直接打开结果；结果不可变 + 人工复核，不自动对接人事系统、不自动发函。
7. **迁徙不是 GPS 轨迹**：迁徙 = 关系边 + 时间属性，不设计轨迹回放引擎（产品明确不做）。
8. **人才主键未定**（C01 P0-1）：契约用 `talent_key` 占位；主键拍板前画像/推荐详情不开查，阻塞点写进 ARCH 与 API 单。
9. **隐私脱敏**（DN-A14-PRIVACY）未拍板前接口不返回敏感字段。
10. 算法只在 Python；Java 不打分、只读 ADS + Feign 调 `/internal/*`；图谱主存 Nebula 经 Java→Python 链路，前端不感知存储引擎。
11. 指标只经 metric-registry MCP 查询；不读 seed YAML 猜状态；类型未签的保持未签；调研写「未见」的，详设和 API 也写「未见」。

---

## 5. 阶段一 · 存量调研（四叶并行 + 定稿）

总派单落盘：`agent-handoffs/科技人才态势-TA/TA-DISPLAY-SURVEY-总派单.md`

`/goal` 头（四叶通用）：

```text
/goal arch-agent
身份：架构师。只写本叶文档。
强度：ponytail off（定义任务，不缩文档）
监管人：human:淮政玮
总控：agent-handoffs/科技人才态势-TA/TA-L2-长任务总控.md
仓：gkx-orchestration。不 commit，不 push，不改注册表，不改 WBS，不改 lumen/demo。
```

四叶：

| 任务 | 页 | 输入 | 产物 |
|---|---|---|---|
| `TA-DISPLAY-SURVEY-DS13-L01` | 全球领域人才态势 | SRS `bid-reference/srs/02-科技信息展示系统/科技人才态势/全球领域人才态势.md`（246–268）+ `FE-TA-01A` handoff + SCI-INT-A12 + demo `talent-trend/GlobalTalentPage` 族 | `survey/DS-13.md` |
| `TA-DISPLAY-SURVEY-DS14-L01` | 关注地区 | SRS `关注地区人才态势.md`（269–279）+ `FE-TA-02A` + SCI-INT-A13 | `survey/DS-14.md` |
| `TA-DISPLAY-SURVEY-DS15-L01` | 重点画像 | SRS `重点科技人才画像.md`（280–307）+ `FE-TA-03A` + SCI-INT-A14 | `survey/DS-15.md` |
| `TA-DISPLAY-SURVEY-DS16-L01` | 引进推荐评估 | SRS `人才引进推荐评估.md`（308–332）+ `FE-TA-04A` + SCI-INT-A15 + 外部接口 05/06b 两册 | `survey/DS-16.md` |

共同判定三档（沿 POL）：**可接统计读面**（STAT/COMPUTE，页面能挂 `metric_id`；D4=mock 必须写明）/ **501**（MODEL 未注册，DS-16 推荐与尽调属此档）/ **跨项索引**（专题 `.7.5` 画像同源、`.7.9` 推荐复用、久新三方通道。只写已有任务号，不设成展示新任务）。

定稿叶 `TA-DISPLAY-SURVEY-L01`：四叶 handoff 齐后合成 `工程过程/04-系统集成/05-展示系统集成/对照-科技人才态势-存量任务与依赖.md`。内容：每条需规叶 → 已覆盖任务（FE-TA / 集成卡 / 契约单）→ 缺口 → 「建议新建 / 建议并进已有单」；§1 的 9 个二级逐个回填精确序号段并标注「与 FE 复刻页区块的对应」。

---

## 6. 阶段二 · 系统详细设计（三叶并行 + 说明书）

总派单落盘：`agent-handoffs/科技人才态势-TA/TA-SDD-总派单.md`

必读（三叶通用）：`agent-handoffs/产品整体定义/科技信息展示系统-完整详细设计/06-功能-科技人才态势.md`、调研定稿、`agent-delivery/ARCH-DISPLAY-01.md`、`architecture-baseline.md`（含 D18）、四份 SCI-INT 卡、四册 survey。

共同禁令：不写 OpenAPI 字段表 / DTO / 枚举（留给 API 单）。不复用 `/topic/v1/...`。指标和任务只引用调研定稿里已出现的编号。

- `TA-SDD-CHAIN-L01` → `sdd/调用链与边界.md`：前端 → `/display/v1/talent/**` → 展示侧聚合 Java → Python `/internal/*` → ADS / 久新只读通道（豁免登记）/ Nebula。**书面裁定 Java 模块归属**：自建 `gkxlumen-element`（产品详细设计口径）还是 `gkxlumen-topic-talent`（WBS E5 条目口径）——两处真源冲突，本叶给出裁定建议并升级李伟确认。写清 DS-13/14/15 哪些区块同步读 ADS、哪些走 Job（仅 DS-16）。写清与专题画像（`.7.5`）、专题推荐（`.7.9`）的边界：模型可复用，资源不共写。
- `TA-SDD-METRIC-L01` → `sdd/指标与501.md`：按 4 页 9 二级列出区块、`metric_id`（6 个已挂接号 + 种子已注册号）、D4、三档判定。无源叶按 A12/A15 的 `metric_missing` 清单写明空态与 ⚠️。DS-16 全部 501 与空态。TALENT 存储域未建期间的挂接可空口径。
- `TA-SDD-INPUT-L01` → `sdd/契约输入清单.md`：交给 BE-TA-CONTRACT-01 收口用的输入。只列：资源路径（含 talent_key 占位）、同步或 Job、成功读什么、501/无源时空态、隐私脱敏限制字段、明确不做的字段表。

说明书 `TA-SDD-L01`：三叶 handoff 齐后合成 `sdd/科技人才态势-系统详细设计说明书.md`，含第 11 节「签收对照」（L2 签收以说明书该节为标准，同 POL 先例）。

---

## 7. 阶段三 · 逐二级 ARCH 先行

可复制提示词（替换 `{二级}` / `{页名}` / `{序号段}` / `{任务ID}`，任务 ID 形如 `TA-L2-DS13-MAP-ARCH`）：

```text
你是 arch-agent。监管人 human:淮政玮。本次是定义任务，不写业务代码。
任务：{任务ID}。为展示系统「科技人才态势 / {页名} · {二级}」（需规 excel {序号段}）编写后台实现架构设计。
强度不用于压缩本文档。图：必含本二级调用链与数据流各一张 Mermaid，diagram_id={任务ID}-SEQ。

必读：architecture-baseline.md（含 D18）、科技人才态势-系统详细设计说明书.md（含第 11 节）、
本二级 SRS 分册、SCI-INT-{A12|A13|A14|A15} 卡、调研定稿、WBS 中本行、
FE-TA-{01A|02A|03A|04A} handoff（只读，了解页面区块与 api 占位，不改页面）。
指标只经 MCP metric-registry 查询。

稿必须包含：范围与明确不做项、整体流程、每叶是真读 / 501 / D18 读表、
表名（ads_talent_* 进 TALENT 存储域）、灌数方、读取接口、metric_id、
与 FE 复刻页 api 占位路径的差异清单、人才主键占位与阻塞点。
做不到真算真查真模型时，只写「新建 ADS 表 + Python 灌 mock 行 + Java 只读」。
禁止接口直接返回 mock。久新源答复前只出桩。迁徙不设计轨迹引擎。DS-16 推荐/尽调 501 + Job 工作台语义。

产物落 agent-handoffs/科技人才态势-TA/sdd/l2/{任务ID}.md，并在 WBS 本行写上路径。
handoff 写全（模板 agent-delivery/templates/handoff-template.md，含图即契约、cost 回填）。
完成后把任务推到待签收，不要自己签 done。
```

---

## 8. 阶段三 · 三单并行 → 会签 → 签收

### 8.1 三单并行（ARCH 稿落盘后启动，同一条提示词开三个子智能体）

```text
你是 {api-agent | algorithm-agent | data-agent}。监管人 human:淮政玮。定义任务，不写业务代码。
任务：{任务ID}。二级「{页名} / {二级}」（excel {序号段}）。
硬依赖：本二级 ARCH 稿已落盘。与 ARCH 冲突时改自己的分册，不改调用链。

api-agent：路径（/display/v1/talent/**）、DTO、枚举、错误码（含 501 与无源空态码）。
  把 SCI-INT 卡 contract_draft 收成分册，差异列表写明；前端 api/talent.ts 的占位路径差异逐条列。
  talent_key 占位、DN-A14-PRIVACY 未拍板敏感字段不出。
algorithm-agent：只消费 metric-registry 与 SCI-INT 卡已挂 6 个 metric_id、种子已注册号。
  类型未签保持未签。不发明 M_* 写进 seed。每叶给 metric_id 或写明无统计数。
data-agent：ads_talent_* 表、字段、灌哪些 mock 行、谁灌、哪个接口读。
  D18 表不进 ODS/DWD/供应方库，不用 gapfill_ 前缀。久新直连豁免须登记切换条件与隔离措施。
  不写第二套统计脚本。灌数单只到「表结构 + 灌数清单」定义，执行在阶段四。

产物落 sdd/l2/{任务ID}.md，WBS 本行可索引。完成后待签收，不自签 done。
```

### 8.2 四角色会签

```text
按四角色会签「{页名} / {二级}」已落盘的 ARCH、API、METRIC、DATA。
分别以 arch-agent、api-agent、algorithm-agent、data-agent 各开一个子智能体，只读稿并写会签意见。
意见只判断：按稿能否实现、是否违反 D18（缺表名/灌数方/读取接口、接口直接返回 mock）、
是否与需规叶冲突、是否违反 §4 铁律（久新桩、无源伪闭合、轨迹引擎、隐私脱敏、Job 语义）。
同意或退回写到 sdd/l2/会签/{二级}-会签.md。四份都同意才进签收。退回则改稿后再会签，不另开任务。
```

### 8.3 签收

```text
你是 coordinator。先读 handoff 与会签记录。会签四角色未全部同意，不得签。
D18 不满足（缺表名、灌数方或读取接口，或接口直接返回 mock）不得签。
对照说明书第 11 节逐条核。
用 MCP task-update-status，id={任务ID}，status=done，actor=human:淮政玮。
签收后把 WBS 该行状态改为 done，写明签收日期。
不要签收无关任务。不要改业务代码。
```

---

## 9. 阶段四 · 代码单执行（签收后连续执行，中间不打扰）

```text
你是 coordinator。监管人 human:淮政玮。本二级四张定义单均已 done。
按已签收的架构拆实现单，MCP task-create 建单（建单不等于认领），每张写入 WBS：

1. Java 实现单：只读已签收的接口分册，落 lumen-svc-platform。Java 只读签收过的接口与表，
   不打分、不直读 ODS/DWD、不直连久新（除非 DATA 单登记过豁免）。
2. 灌数单（data-agent 执行）：按 DATA 稿建 ads_talent_* 表并灌 mock 行，Python 写 ADS，
   calc_batch_id 前缀 mock_。

编码单 /goal 必须含：架构铁律（§4 全文）、必读（含已签收的 sdd/l2 四稿）、
强度：ponytail full、图：必含 {diagram_id}。
范围只覆盖本二级。不认领 BE-TA-CONTRACT-01 整包。
然后启动子智能体以 human:淮政玮 认领并执行。同仓同时只跑一张编码单。
写完 handoff 后用 actor=human:淮政玮 标 done。签收失败则返工同一张单。
若执行中解锁出后续单，继续领取并执行，直到本二级代码单全部 done。
只有 §11 停机条件的情形才停下来问。
```

9 个二级可流水推进；DS-14 两视图、DS-15 三二级的灌数单共享 TALENT 域表结构，第一批灌数单先冻结 DDL，后续引用不重建。

---

## 10. 阶段五 · 接线与主路径测试（每页两张单）

```text
你是 coordinator。监管人 human:淮政玮。「{页名}」相关二级代码单已全部签收。
再建两张单，都写入 WBS，要求从 WBS 能点到任务 ID 和 handoff：

1. 接线单：前端只改 src/api/talent.ts 拼装层与 api 双轨 real 分支，把 FE-TA-{0xA} 已复刻页
   接到已签收接口。不重做页面、不动视图层结构。USE_MOCK=false 时零 fixture；
   501 与无源项走空态 + ⚠️；统计数旁保留 MetricSpecHint ⓘ；mock 态 MockBadge
   （全球页 KPI 首卡维持用户裁定的去 🧪 口径）。跨页跳转 ?talentId= 落 query。
2. 主路径测试单（qa-agent）：必须包括——
   - 合规交付主路径的数据准备（ads_talent_* 表已有 data-agent 灌入行，或如实记录 501/无源）
   - 关键路径验证（本页每个二级一条：如全球页=图层切换+时间轴播放+抽屉+导出）
   - 界面操作过程（登录走新人引导第 6 节统一账号，不另写账号）
   - 截图（能看出菜单、当前页签、关键数字或空态、501/Mock 角标）

两张单都执行到 handoff 完整，再用 actor=human:淮政玮 标 done。WBS 行更新为 done。
```

---

## 11. 停机条件（只有这些才打断跑单人）

- 要扩大需规范围，或要把「明确不做」项（独立人才本体、轨迹回放、未复核自动对接人事系统）做成实现。
- 真做不到，又写不出符合 §4.2 的表。
- Java 模块归属裁定（`gkxlumen-element` vs `gkxlumen-topic-talent`）被李伟否决。
- 人才主键 C01 P0-1 拍板结果与 talent_key 占位冲突。
- 同一文件已有别人的未提交改动，或任务锁冲突（含撞上孔东 FE-TA 锁定期文件）。
- 单任务成本超预算硬停；会签否决且否决点是业务口径而非稿写漏。

---

## 12. 完工标志

- 调研定稿、详设说明书、9×4 定义单、各二级 Java/灌数单、4 张接线单、4 张主路径测试单，全部在 WBS 有行且可索引到任务 ID 与 handoff。
- 定义单全部满足 D18；关 Mock 后接口读的是 `ads_talent_*` 表或明确的 501/无源空态，不是页面死数据。
- 每页主路径有操作记录与截图；无源项与成本族没有伪闭合数字。
- 收尾：教训追加进 TS 复刻经验清单（TA 附表）+ `模块快速开发SOP-以科技人才态势为例.md` §11 加一行；数据源映射条目推 `verified`；mock-ledger 登记 `ads_talent_*` 灌数项。

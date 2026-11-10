> 第一轮试跑产物（2026-11-10）。监管人要求按定稿规程重新试跑，本文件不再作为现行方案。重跑期间只作对照，不在上面续写。

# POL-L2-PC1-CLEAN-FDE-B · 602 定档与读法方案（波次 B）

- 起草：`agent:arch-agent`，**待** `data-agent` **/** `api-agent` **对抗审稿**
- 日期：2026-11-10
- 所属：FDE 试点 602（`POL-L2-PC1-CLEAN-FDE-L01`，波次 B，《产品实现规程》§4.2.4）
- 输入真源：说明书 PC-1「602 系统引用政策源数据清洗」2026-11-10 版（功能点 602-1～8）
- 状态：方案稿。读法触及团队铁律，**须人类架构师裁定**后才进波次 C；未裁定前 602 实现 leaf 不标 `ready`
- 本稿不写代码、不改注册表、不改说明书；不写 OpenAPI 字段（归 API 稿）

---

## 1. 定档：中档

| 判据（§4.2.1） | 602 实况 | 结论 |
|---|---|---|
| 新增交互 / 选择方式 / 区块 | 条件栏由单值或无选择改为「选择政策」多选，两条入口（智能搜索、ID 检索），已选集合可见可清空；规则行新增启停 | 命中「中」 |
| 数据源、读口条件变化 | 候选由 DWD `policy_base_info` 改为 ODS 贴源两表；读口条件由 `policyId` 单值 / `status` 改为 `id` 多值 + 六条规则启用标记 | 命中「中」 |
| IA 或主路径大改 / 增删需规叶 | 仍在「智能政策库构建 · 清洗」页签，需规句子不变，叶子不增删 | 不到「重」 |

**定档：中档**。按中档须：高保真升版 + 体验 Owner 书面复核 + 数据、架构确认读法 + 四角色会签。

另：本叶读法触及铁律（D3 只读 ADS），并可能新建正式库表，同时命中 §4.2.5 两条停机条件：「触碰团队铁律」→ 人类架构师裁定；「新建正式库表、新同步」→ 数据平台 Owner / 架构确认。

---

## 2. 现状核查（方案的事实基础）

| # | 核查项 | 结果 | 依据 |
|---|---|---|---|
| F1 | ODS 两表结构 | `dwd_policy_base`（国内，35 列，PK `id`）、`dwd_global_policy_base`（海外，PK `id`）；标题、文号、发文部门 / 机构、发布日期可直接作候选展示与检索列 | `storage/POLICY/sources/ods-ddl.md` |
| F2 | ODS→DWD 是否有清洗规则 | **没有**。映射几乎全部「直拷」，只按 `is_deleted=0`、`is_history=0` 读过滤；无去重、标准化、噪声、校验落库 | `etl/ods-to-dwd-mapping.md`、`etl/pipeline-ods-to-dwd.md` |
| F3 | 正式 ODS 写入 | Demo 管线对 `gkxlumenx_ods` **零写入**；正式贴源由 GDF Wave A 负责，产线 DAG 仍是 `OPEN-POLICY-FLOW-01` | `etl/pipeline-ods-to-dwd.md` |
| F4 | 政策 ES | 不建，无全文索引；检索走 SQL | `etl/pipeline-dwd-to-es.md` |
| F5 | `gkxlumen-element` 读 ODS 先例 | **无**。`ElementDao` 只有 `{dwd}` `{ads}` `{gapfill}` 三个占位，无 ODS 库配置 | `ElementDao.java` |
| F6 | element 读 DWD 现状 | 已在读：`PolicyGovernanceController` 读 `{dwd}.policy_base_info` 与 `{dwd}.script_state`；企业域也读 DWD。`application.yml` 登记为「临时豁免（技术债），违反 D3 与 D12」，默认库仍是 `demo_gkxlumenx_*` | `PolicyGovernanceController.java`、element `application.yml` |
| F7 | Python 贴源检索能力 | `lumen-algo-py`（entan-api 镜像）已有 `/internal/policy/search`（**读 DWD**，非 ODS）、`/internal/policy/query-intent`（LLM 意图拆解，失败降级）、`/internal/policy/status`（已能连 `conn.ods` 计 ODS 行数）。**无按 ODS 检索的路由** | `vendor/entan-py/api/policy_routes.py` |
| F8 | display → Python 先例 | 已有 `RemotePolicySyncClient` → `gkxlumen-platform-entan-py` `/internal/policy/*`（同步历史、条款拆解、仿真兜底） | `gkxlumen-display/.../RemotePolicySyncClient.java` |
| F9 | 六条规则命中事实 | **全仓无落库事实**（见 §3） | Grep 去重合并 / 噪声过滤 / 格式标准化 无实现 |

---

## 3. 「本批命中」现在有没有事实可读

### 3.1 `script_state` 六值能否映射到六条规则：**不能**

| 维度 | `script_state` | 602 六条规则 |
|---|---|---|
| 是什么 | C1 抽取产业、C2 条款结构化两个**后加工作业**的留痕，供增量跳过 | 贴源数据**清洗与质量校验** |
| 键 | `(job, policy_id)`，`policy_id` 是 **DWD** 键；没进 DWD 的 ODS 行没有记录 | 按 **ODS** `id`（两源） |
| 值 | `done / empty / no_match / degraded / failed / llm_unavailable`：作业结局 | 去重 / 标准化 / 噪声 / 完整性 / 一致性 / 准确性：规则命中 |

逐条对照：`degraded`、`llm_unavailable` 是 LLM 可用性；`no_match` 是产业词表未命中；`empty` 是正文无可抽内容；`failed` 是作业异常。没有一个值的语义等于六条规则中的任何一条。硬映射即 D9「伪闭合」，**禁止**。

结论：旧 ARCH 稿 §1、§3.1、§8「`script_state` 就是已落库的校验结果」与说明书 602 末段「对照第 6 项已落库的清洗事实汇总本批」**前提不成立**。`script_state` 应从 602 读口移出（它更贴近 603 结构化覆盖，归 603 稿处理）。

### 3.2 六条规则各自能不能真算

| 规则 | 作用范围（说明书） | 能否用 ODS 字段确定性计算 | 归类 |
|---|---|---|---|
| 去重合并 | 标题 + 文号 + 效力级别 | 能。规范化标题（去空白标点）+ `publish_code` + `rank` 在两表内及跨表找重 | 真算（规则） |
| 格式标准化 | 发布日期 / 文号 / PDF→文本 | 能。日期空或非法、`publish_year` 非 4 位、文号不合模式；附件为 PDF 且 `content` 空 → 待转文本 | 真算（规则） |
| 噪声过滤 | 扫描件乱码 / 重复附件 | 基本能。乱码按替换字符、非常用字符占比启发式；重复附件按 `appendix_link` / `appendix_name` 重复 | 真算（启发式，阈值须 data-agent 定） |
| 完整性校验 | 缺发布日期 / 缺发文机关 | 能。`publish_date`、`ministry` / `organ` 空值 | 真算（SQL 级） |
| 一致性校验 | 效力级别与发文主体冲突 | 部分能。`rank` 与 `ministry` 中区划 / 部委词表比对（海外表无 `rank`，记「不适用」） | 真算（词表规则） |
| 准确性校验 | 文号 / 日期 / 机关与原文不符 | **现在不能**。需原文（PDF / 外站）比对或模型抽取，无原文落库 | D18 mock 或空 |

所以：前五条都要**新建一个 Python 规则校验能力**才有命中数；准确性只能走 D18（新 ADS 表 + Python 写 mock 行 + 接口读表 + MockBadge）或诚实显示空。任何方案都绕不开这一点，区别只在「算完落不落库、谁来读」。

---

## 4. 读法方案

公共前提（各方案共用）：浏览器只打 `/display/v1/policy/**`；规则启停是**读条件**，不写库；「批次」= 用户这一选，不落批次表；停用规则行照列、命中为空；无事实为空不造 0。

### 方案 A：ADS 贴源目录 + ADS 命中事实表，Java 只读 ADS

| 项 | 内容 |
|---|---|
| 做法 | ① 新建 `gkxlumenx_ads.policy_source_catalog`（两源合一：`source_plane`、`id`、标题、文号、机关、发布日期等展示列），由数据工厂（GDF 或 Python ETL）从 ODS 定期同步；② 新建 `gkxlumenx_ads.policy_source_clean_hit`（`source_plane`、`id`、`rule_code`、`hit`、`sample_masked`、`is_mock`、`checked_at`、`batch_id`），Python 规则校验作业全量扫 ODS 写入；③ element 用 SQL 对目录表做标题 / 文号 / 机关 LIKE 与 ID 精确查，对事实表按已选 `id` + 启用 `rule_code` 汇总 |
| 动到 | 数据（2 张新 ADS 表 + 1 条新同步）、`lumen-algo-py`（规则校验作业）、`lumen-svc-platform` element + display、前端 |
| 铁律 | 不触 D3（Java 只读 ADS）。触 §4.2.5「新建正式库表、新同步」停机，须数据平台 Owner 确认 |
| 启停 / 本批汇总 | 好。`rule_code IN (...)` 即启停；汇总为纯 SQL 聚合 |
| 智能搜索 | 弱。Java 只能做 LIKE；要语义拆解得另调 Python `query-intent`，等于又走一次方案 B 的链 |
| 工作量 | 大（约 8–10 人日：两表 DDL 与 GDF 注册、同步作业、校验作业、element 两段 SQL、display 转发、前端） |
| 风险 | 目录是 ODS 的**副本**，有同步延迟，「候选只来自 ODS」变成「来自 ODS 的某时刻镜像」，须产品认可；目录表与 DWD 政策主表职能重叠，易被误当第二张主表；新同步链多一份一致性责任 |

### 方案 B：Python `/internal/*` 实时检索 + 实时汇总，Java Feign 转发

| 项 | 内容 |
|---|---|
| 做法 | `lumen-algo-py` 新增 `/internal/policy/source/search`（读 ODS 两表：关键词 / 文号 / 机关 LIKE、`id` 精确；复用 `query-intent` 做智能拆解）与 `/internal/policy/source/clean-batch`（入参已选 `id` 多值 + 启用规则；请求时对这批行即时跑六条规则，返回命中与脱敏样例）；display 经现有 entan-py Feign 转发，element 不参与 |
| 动到 | `lumen-algo-py`（两条路由 + 规则函数）、display（Feign 方法）、前端。不建表（准确性若要出数，仍需一张 D18 ADS 表） |
| 铁律 | 不触 D3（Java 不读库）、不触调用链（前端→Java→Python `/internal`）、D12 合规（entan-py 是 lumen 服务）。Python 读 ODS 是算法层正当读取 |
| 启停 / 本批汇总 | 好，入参即启停 |
| 智能搜索 | 好，直接复用 `query-intent` |
| 工作量 | 中（约 5–6 人日） |
| 风险 | ① 去重要拿已选行去全表比对，ODS 标题无索引（`title` 为 varchar(500) / text），同步请求内**全表扫描**，量大即超时；② 命中**不落库**：不可复查、无「更新时间」可言，批次状态只能是「本次请求算出」，与说明书「作业状态只读」「对照已落库事实」语义不符；③ 每次打开都重算，结果随 ODS 变动漂移，演示用例难固定 |

### 方案 C：书面豁免，element 直读 ODS

| 项 | 内容 |
|---|---|
| 做法 | element 增加 `{ods}` 占位与 ODS 库配置（只读账号授权），候选检索直接 SQL 读两表；规则命中**仍须** Python 校验作业落一张 ADS 事实表（Java 不得自己写去重 / 一致性规则，那是算法），element 读事实表汇总 |
| 动到 | `lumen-svc-platform` element（新数据源占位、配置、Nacos / Secret 授权）+ display、`lumen-algo-py`（校验作业）、数据（1 张 ADS 事实表）、前端 |
| 铁律 | **触 D3**（Java 扫 ODS），须人类架构师书面豁免；叠加 element 现有 D3 / D12 临时豁免，技术债加深 |
| 启停 / 本批汇总 | 好（同 A 的事实表部分） |
| 智能搜索 | 弱（同 A，只有 LIKE） |
| 工作量 | 中（约 5–7 人日；Nacos 配置须走 `gkx-nacos-shared-config` 单 dataId 发布） |
| 风险 | 开先例：后续各域都会以此要求 Java 读 ODS；ODS 是供应方贴源，字段变动直接打穿 Java；并没省掉事实表，换来的只是少一条 Feign |

### 方案 D：候选走 Python 检索，命中落 ADS 事实表由 element 读（混合）

| 项 | 内容 |
|---|---|
| 做法 | ① **候选**：同 B 的 `/internal/policy/source/search`（ODS 两表 + `query-intent`），display 经现有 entan-py Feign 转发；② **命中**：同 A 的 `gkxlumenx_ads.policy_source_clean_hit`，由 Python 规则校验作业**离线**全量扫 ODS 写入（去重在批内做全表比对，不进请求路径）；准确性按 D18 写 `is_mock=1` 行（或不写、显示空，见 §6 裁定点 3）；③ **本批汇总**：沿用现有 `GET /display/v1/policy/governance/results` → element，按已选 `id` 多值 + 启用 `rule_code` 对事实表做 SQL 聚合，返回规则行、失败样例、`MAX(checked_at)` 作更新时间、批次状态 |
| 动到 | 数据（1 张新 ADS 表）、`lumen-algo-py`（1 条检索路由 + 1 个校验作业）、`lumen-svc-platform` display（Feign 一个方法）+ element（`results` 改条件与 SQL，移出 `script_state`）、前端 |
| 铁律 | 不触 D3（element 只读 ADS 事实表；候选不经 Java 读库）、调用链合规、D12 合规、D18 合规（准确性 mock 进 ADS 表、接口读表）。仍触 §4.2.5「新建正式库表」停机，须数据平台 Owner 确认 |
| 启停 / 本批汇总 | 好。启停是 SQL 条件；停用行照列、命中空；无事实行即空，状态不写成功 |
| 智能搜索 | 好（复用 `query-intent`，失败降级为关键词） |
| ID 未命中 | Python 检索在 ODS 两表内查不到即返回「不在贴源」，不回退 DWD |
| 工作量 | 中（约 6–7 人日） |
| 风险 | ① 命中是「最近一次校验作业」的事实，新进 ODS 但未校验的行显示「无加工事实」→ 批次状态「部分」，须产品认可这一语义；② 新表须 GDF / DBA 建表与调度登记；③ 一个页面两条读链（候选走 Python，结果走 element），API 稿要写清 |

### 方案对照

| | A 全 ADS | B 全 Python 实时 | C 豁免直读 ODS | D 混合（推荐） |
|---|---|---|---|---|
| 触铁律 | 否 | 否 | **是（D3）** | 否 |
| 新建正式表 | 2 + 新同步 | 0（准确性另计） | 1 | 1 |
| 候选与 ODS 同步性 | 有延迟 | 实时 | 实时 | 实时 |
| 智能搜索 | 弱 | 好 | 弱 | 好 |
| 命中可复查、有更新时间 | 是 | **否** | 是 | 是 |
| 请求内性能 | 好 | **全表扫风险** | 好 | 好 |
| 工作量 | 大 | 中 | 中 | 中 |

---

## 5. 推荐：方案 D

1. **零铁律突破**：两条读链各走合规车道。Java 只读 ADS，读贴源的是算法层 Python，调用链与 D12 都在既有先例内（F8）。
2. **不复制 ODS**：候选直接查贴源，满足「候选只来自 ODS」字面，不新增目录同步，避免 A 的第二张「政策主表」。
3. **命中落库**：规则在 Python 离线跑、写 ADS，element 读表汇总，回到说明书「读已落库事实、不写死在接口里」的本意；B 的实时重算既慢又不可复查。
4. **增量最小**：只新建 1 张 ADS 表；`governance/results` 资源不换，只改条件；display 加一个 Feign 方法。

D 与说明书 602 现文的出入（须 product-agent 回写说明书）：

- 「element 按这些 `id` 只读上表两张 ODS」→ 改为「候选由 Python 读 ODS 检索；element 只读 ADS 命中事实表」。
- 「对照第 6 项已落库的清洗事实」→ 第 6 项无此事实（§3.1），改为「对照本叶新增的规则校验事实表」。
- 「不新建清洗管道」→ 需改：新增的是**只读校验作业**（不改 ODS / DWD，只写 ADS 事实表），不是重做贴源或 Mapping。

---

## 6. 必须由人类裁定的点

| # | 裁定点 | 裁定人 | 本稿建议 |
|---|---|---|---|
| 1 | 602 读法选 A / B / C / D；若选 C，须书面豁免 D3 | 人类架构师（监管人确认） | D |
| 2 | 新建正式 ADS 表 `policy_source_clean_hit`（表名、主键 `source_plane + id + rule_code`、调度频率） | 数据平台 Owner / 架构（监管人确认） | 同意新建；日更 |
| 3 | 准确性校验在无原文比对能力时：D18 写 mock 行（界面 MockBadge）还是显示空。若写 mock，是否允许与真算行同表用 `is_mock` 区分，还是另建一张 D18 表 | 人类架构师 + 产品 | 同表 `is_mock=1`，MockBadge；须架构师确认符合 D18「新建 ADS 表」字面 |
| 4 | 推翻 SDD 前提：`script_state` 不是六条规则的事实，602 读口移出 `script_state`；「不新建清洗管道」改为「新增只读校验作业」 | 监管人（产品口径）；涉及范围时转 PM | 同意移出并改写 |
| 5 | 批次状态口径：成功 / 部分 / 失败的判定（建议：已选全部 `id` 在全部启用规则下都有事实 = 成功；部分 `id` 无事实 = 部分；校验作业最近一趟失败 = 失败；全无事实 = 空） | 产品（不涉甲方则监管人拍） | 如左 |
| 6 | element 现存 D3 / D12 临时豁免（读 DWD、默认连 `demo_gkxlumenx_*`）是否在本叶顺带消除，或另开技术债单 | 人类架构师 | 另开技术债单；本叶不扩大豁免 |
| 7 | 噪声 / 一致性的启发式阈值与区划词表、失败样例脱敏规则 | data-agent 起草，监管人确认 | 归波次 C 数据稿 |

---

## 7. 留给审稿身份的重点（请逐条反驳）

| 审稿身份 | 请重点挑 |
|---|---|
| `data-agent` | 正式 `gkxlumenx_ods` 两表在 lumen 是否已有行（F3：正式贴源仍是 OPEN）；离线全表去重的耗时与调度窗口；国内 / 海外 `id` 是否碰撞（`ods-to-dwd-mapping.md` §2 OPEN）；事实表粒度与脱敏 |
| `api-agent` | 一页两条读链的契约表达；display 新增 Feign 方法与 `PolicyAlgoFeignTimeout` 超时是否够；`results` 改 `id` 多值后的长度上限与 GET 可行性（多选上限需产品给） |
| `algorithm-agent`（中档会签） | 规则校验作为 Python 作业的归属与可测性；`query-intent` 降级路径 |
| `product-agent`（中档会签） | §5 说明书改写三处；「无加工事实 → 部分」能否接受 |

## 8. 不做

- 不写 OpenAPI 字段、DDL、代码；不改注册表；不 git 提交。
- 不新造 `metric_id`（清洗命中是行聚合，不挂指标）。
- 不动 603–605 读面。

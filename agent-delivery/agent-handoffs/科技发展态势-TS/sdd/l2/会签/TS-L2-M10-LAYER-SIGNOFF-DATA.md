# TS-L2-M10-LAYER-SIGNOFF-DATA · 维护管理 · 图层与数据源 · 数据会签

- 角色：`agent:data-agent`（数据角色会签人）
- 日期：2026-11-06
- 对象：`TS-L2-M10-LAYER-DATA`（主审）；交叉核对 `TS-L2-M10-LAYER-ARCH` §2/§3、`TS-L2-M10-LAYER-API`、`TS-L2-M10-LAYER-METRIC`
- 监管：`human:刘剑锋`
- 范围：**只读核对**。不改被审文件，不动 task-registry / WBS，不建库、不灌数、不跑脚本、不 git 提交
- 事实源：`repos/demo-ui-science/src/pages/tech-situation-maintain/layerSourceState.js`、`repos/lumen-ui-science-pc/src/views/situation/maintain/maintainModel.ts`、`repos/lumen-ui-science-pc/src/mock/modules/situation.ts`（种子逐值核对）；`agent-delivery/data/data-design/storage/mysql-ddl-convention.md`（DDL 惯例）；`POL-L2-DS12-SIM-DATA.md` §1–§2（gapfill 先例）
- 结论：**有条件同意**（条件 2 项，见下）

## 0. 结论与条件

**有条件同意。** 种子 26 行逐值核对**全部一致**（§1 核对表）；列定义覆盖 API 分册全部 DTO 字段、逻辑外键闭合；不设列裁定与 ARCH/API/METRIC 三稿一致；分工形态与政策 gapfill 先例对齐。但稿内有两处必须修正后才可签收通过：

| # | 级别 | 条件 | 证据 |
|---|---|---|---|
| C1 | 必修 | **§6 残留旧裁定**：DATA 分册 `TS-L2-M10-LAYER-DATA.md:108`「不建库、不执行 DDL、不灌数（**建表归 Java 实现单**，种子归灌数单——**两单**待建单签收后起草）」仍是 2026-11-06 监管人裁定**前**的旧分工，与本稿 §1 分工表（`:33` DDL+种子 26 行一体归 data-agent 灌数单 Python）、ARCH §3.2（`TS-L2-M10-LAYER-ARCH.md:60`）及裁定本身矛盾。改法：该条改为「建表 DDL + 26 行种子一体归 data-agent 灌数单（Python），一单待建单签收后起草」，删去「建表归 Java 实现单」与「两单」表述 | DATA `:108` vs `:29`/`:33`；ARCH `:60` |
| C2 | 必修 | **库名 `gkxlumenx_config` 与既有库重名且归属描述失实**：该名在环境中已是 **Java 平台库（PigX/Nacos 配置库）**——`agent-delivery/agent-handoffs/算法库联调-ALGO-LIB/algo-mysql-connection-info.md:83-88` 明列「11 个 Java 平台库（PigX 多模块…）」含 `gkxlumenx_config`；`agent-delivery/ARCH-DISPLAY-01.md:1157` Nacos「配置库 `gkxlumenx_config`」；dev 已有 12 表在册（`agent-delivery/agent-handoffs/指标算法库上线/METRIC-SRS-GAP-L01/产物/20261030展示系统指标补充/第三方库指标计算过程/M_SCIUI_DATAOV_001.md:123`，12 表与 Nacos 标准表集吻合）；共享账号已 `GRANT ALL ON gkxlumenx_config.*`。DATA §1 称其「Python 侧管理的库（建议名，会签确认）」与现状不符，且向 Java 平台基础设施库混入业务配置表违反裁定本意（写库全归 Python、保持原有规矩）。**处置**：换名（建议 `gkxlumenx_show_config`；注意 `gkxlumenx_cfg` 亦已被占 11 表）或由监管人明示与 Nacos 表集共存的边界与权限隔离；定名后回填 DATA §1、ARCH §2 表格/§3.1/§4.1–4.2 图、API §1 内部委托段的库名字面 | algo-mysql-connection-info `:83-88`；ARCH-DISPLAY-01 `:1157`；M_SCIUI_DATAOV_001 `:123`；DEVOPS-LUMEN-DEMO-WAREHOUSE-L01 `:46` |

非阻断建议（随 C1/C2 一并处理或落灌数单）：

1. DATA §5 的 11 个颜色种子只以引用落款（「=M1 `entityColorByKey` 默认色冻结」），建议灌数单逐值落字——本会签已核对并整列表于 §1.4，可直接取用，防漂移。
2. 灌数单 DDL 沿用数据域 MySQL 惯例：`utf8mb4` / `utf8mb4_0900_ai_ci`、CREATE 内中文注释、逻辑外键不建物理 FK（`mysql-ddl-convention.md` 正文限定 ADS/DWD 批，对 `gkxlumenx_*_config` 新库不强制，惯例宜沿）。
3. API DTO `groupId`（bigint）与表列 `group_code`（varchar）是 id→code 经纬映射（读侧 join `layer_group` 带出，写侧解析），实现单注意落点；非错误，仅提示。

C1/C2 回填后由 data-agent 在本页追记一行确认即可转「同意会签」，无需重开签。

## 1. 种子 26 行逐值核对（3 源 + 3 组 + 9 图层 + 11 要素）

两仓逐字一致性先核：`layerSourceState.js` 与 `maintainModel.ts` 的种子段（SOURCE_TYPES / LAYER_OPTIONS / sources 3 行 / groups 3 行）**逐值一致**（差异仅在 seq 计数器实现，非种子）。

### 1.1 cfg_tech_datasource（3 行）

| source_code | source_name | source_type | target_layer_code | endpoint（原文） | enabled | group_code | 源 |
|---|---|---|---|---|---|---|---|
| `src-1` | 专利 API | API 接口 | `patent` | `https://mock.api/patents` | 1 | `grp-ip` | layerSourceState.js:12-22 / maintainModel.ts:74-84 |
| `src-2` | 论文主题库 | 数据库表 | `paper` | `dwd.paper_topic` | 1 | `grp-lit` | layerSourceState.js:23-33 / maintainModel.ts:85-95 |
| `src-3` | 机构填报 | 用户填报 | `institution` | `填报模板-机构台账` | 0 | `grp-org` | layerSourceState.js:34-44 / maintainModel.ts:96-106 |

- `source_type` 三值枚举 `API 接口`/`数据库表`/`用户填报` = SOURCE_TYPES（layerSourceState.js:1 / maintainModel.ts:68），中文冻结一致；种子三型各一、顺序一致
- `target_layer_code` 由源中文 `targetLayer`（专利/论文/组织机构）经 API §7 映射取 code（`patent`/`paper`/`institution`），映射与 factorItems key 一致
- `enabled` 1/1/0 = 源 true/true/false
- 源行上的 `lastSync` / `testStatus` 演示值（'2026-08-17 10:20'/'通过' 等）按 DATA §4 不迁移，与 API §0 一致
- endpoint 三条与源**逐字一致**（含 mock URL、表名、模板名原文）

### 1.2 cfg_tech_layer_group（3 行）

| group_code | group_name | color | sort_order | 源 |
|---|---|---|---|---|
| `grp-ip` | 知识产权图层组 | `#165DFF` | 1 | layerSourceState.js:47 / maintainModel.ts:109 |
| `grp-lit` | 文献图层组 | `#00B42A` | 2 | layerSourceState.js:48 / maintainModel.ts:110 |
| `grp-org` | 主体图层组 | `#F97316` | 3 | layerSourceState.js:49 / maintainModel.ts:111 |

名称/色值逐字一致；sort_order 1–3 按源 groups 数组序。

### 1.3 cfg_tech_layer（9 行）

| sort_order | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|
| layer_code | `paper` | `journal` | `patent` | `scholar` | `meeting` | `institution` | `topic` | `project` | `result` |
| layer_name | 论文 | 期刊 | 专利 | 专家学者 | 会议 | 组织机构 | 课题 | 项目 | 成果 |

- `layer_name` 九值与 LAYER_OPTIONS（layerSourceState.js:2 / maintainModel.ts:69）**逐字一致、同序**；`layer_code` 为 API §7 的中→英映射（源文件字面是中文枚举，英文 code 经 factorItems key 对齐，映射无冲突），DATA §2 与 API §7 同值同序
- `enabled` 全 1：demo LAYER_OPTIONS 为纯字符串数组，无图层禁用态，DATA「无初始禁用」裁定与源相符
- 种子总数 3+3+9+11 = **26 行**，DATA §0 算术正确；其对 ARCH 旧稿「8 数据源/9 图层组」的纠错属实（8=源表 8 列、9=图层枚举数），ARCH 现稿 §3.2/§4.2 已回填 3/3/9/11，两稿无残留冲突

### 1.4 cfg_factor_display（11 行）

| sort_order | factor_key | display_name（默认） | color（entityColorByKey） | 源 |
|---|---|---|---|---|
| 1 | `scholar` | 专家学者 | `#D96A78` | situation.ts:93 / :63 |
| 2 | `meeting` | 会议 | `#FFB84D` | :94 / :64 |
| 3 | `institution` | 组织机构 | `#47D9FF` | :95 / :65 |
| 4 | `enterprise` | 企业 | `#4A86FF` | :96 / :66 |
| 5 | `service` | 服务机构 | `#47E38C` | :97 / :67 |
| 6 | `topic` | 课题 | `#B58FFF` | :98 / :68 |
| 7 | `project` | 项目 | `#FF85BF` | :99 / :69 |
| 8 | `paper` | 论文 | `#FFD93D` | :100 / :70 |
| 9 | `journal` | 期刊 | `#6BCC78` | :101 / :71 |
| 10 | `patent` | 专利 | `#4DABFF` | :102 / :72 |
| 11 | `result` | 成果 | `#F77234` | :103 / :73 |

- 11 键/中文名/顺序与 `factorItems`（situation.ts:92-104）逐字一致；颜色与 `entityColorByKey`（situation.ts:62-74）逐值一致（DATA §5 未列字面值，本表为核对基线，灌数单取值即用此列）
- 源行 `active` 位（service/project/journal 为 false，其余 true）是 M1 地图运行态，按 DATA §5 不设列、不迁移——与 ARCH §0 序 9 裁定一致
- 源行 `count`/`source`（统计演示值）不属配置面，不迁移，正确

**种子核对结论：26 行无一处不一致。**

## 2. 列定义完备性与逻辑外键

| DTO（API 分册） | 表（DATA 分册） | 覆盖判定 |
|---|---|---|
| Layer：layerCode/layerName/enabled/sortOrder | cfg_tech_layer：layer_code/layer_name/enabled/sort_order | 全覆盖；layer_code 唯一；仅 enabled 可改与 API §2「只接受 layerCode+enabled」一致 |
| LayerGroup：id/groupCode/groupName/color/sortOrder | cfg_tech_layer_group：id/group_code/group_name/color/sort_order | 全覆盖；group_code 唯一 = API §3「groupCode 唯一」；group_name 不设唯一 = API「不强制唯一」 |
| Datasource：id/sourceCode/sourceName/sourceType/targetLayerCode/endpoint/enabled/groupId | cfg_tech_datasource：id/source_code/source_name/source_type/target_layer_code/endpoint/enabled/group_code | 全覆盖；endpoint varchar(512) = API ≤512 字；source_name varchar(64) = ≤64 字；source_type varchar(16) 容三值；group_code 可空 = API groupId 可空（传 null 改挂） |
| FactorDisplay：factorKey/factorName/color/sortOrder | cfg_factor_display：factor_key/display_name/color/sort_order | 全覆盖；factor_key 唯一；display_name varchar(64) 容 API ≤32 字校验；sort_order 冻结与 API「sortOrder 不可改」一致 |

- 长度核：color `#RRGGBB` 7 字符 < varchar(9)；source_type 最长「API 接口」6 字 < varchar(16)；layer/factor code 最长 `institution` 11 字 < varchar(32)；均闭合
- 逻辑外键闭合：`target_layer_code` 种子 patent/paper/institution ∈ cfg_tech_layer 9 值；`group_code` 种子 grp-ip/grp-lit/grp-org ∈ cfg_tech_layer_group 3 值；不建物理 FK 沿数据域惯例，组删除约束（409 GROUP_IN_USE）由 API 层承担，与 DATA §3/ARCH §2 一致
- 公共审计列 created_at/updated_at 由写方（Python）维护，与「写全归 Python」链路自洽
- 无遗漏 DTO 字段；API DTO 无一列在四表中无落点

## 3. 不设列裁定与 ARCH/API/METRIC 三稿一致性

| 不设列 | DATA | API | ARCH | METRIC | 判定 |
|---|---|---|---|---|---|
| `last_sync` | §4 不设（无同步动作） | §0「最后同步列移除或恒显 -」 | §2/§6 无 ETL/真同步 | —（不涉） | 一致 |
| `test_status` | §4 不设（探测不持久化） | §0/§4.1「探测结果只随本次响应返回，不落库」 | §2 probe「不落表，探测结果不持久化」 | §1「即时探测结果不构成指标口径」 | 一致 |
| `active` | §5 不设（M1 运行态） | §5 FactorDisplay 无该字段 | §0 序 9「本二级只承担配置面」 | —（不涉） | 一致 |
| `is_mock` | §1 无 | 无 | §3.6 真配置非 mock、不挂 MockBadge | §3「四表不设 is_mock」 | 一致 |
| `metric_id` | §1 无 | §8 不新造 | §2 全 N/A | §1 维持全 N/A | 一致 |
| D16 五件套（gap_item/fill_method/gapfill_batch_id/generated_at + 上述 is_mock） | §1 无 | 无 | §3.1 非 D16 缺项表、不混 gapfill 语义 | §3「无五件套行级列」 | 一致 |

种子「真配置」语义（非 mock 统计、不挂 MockBadge、与 demo 刻意一致即显式占位事实）在 DATA §1 / ARCH §3.6 / METRIC §3 三处表述一致，D4 无可动、D9 不适用成立。

## 4. 库选址与分工自洽（含 C2 问题的对齐结论）

- **分工自洽**：DDL+种子一体归 data-agent 灌数单（Python）、运行时写经 `/internal/gkx-show/maintain/config/**`（gkx_show_service）、读沿政策 gapfill 只读先例由领域服务直读——DATA §1 / ARCH §3 / API §1 三稿链路一致，符合 2026-11-06 监管人裁定与 D15（display 不直连 Python/DB）。唯一残留矛盾是 DATA §6 旧裁定（C1）
- **与 POL gapfill 先例形态对齐**：POL（`POL-L2-DS12-SIM-DATA.md` §1–§2）形态 = Python 脚本建表灌数（「谁写这张表：灌数单里的 Python 脚本。Java 与前端不建表、不灌数」）+ 仅 `gkxlumen-element` 只读。本二级同构（Python 建+灌、element 链路只读），差异仅在：POL 表是 `gapfill_` 前缀落 `gkxlumenx_gapfill` 带 D16 五件套（缺项统计行），本二级 `cfg_` 前缀、无五件套（配置真源行）——差异正当（见 §5），先例的「建/灌/读」三方分工完全对齐
- **库名（C2）**：`gkxlumenx_config` 已被 Java 平台侧占用（Nacos 配置库，dev 12 表在册），「Python 侧管理的库」描述失实，须换名或明示共用边界（证据见 §0 C2 行）。`cfg_` 前缀本身无冲突、语义清楚（配置真源，对齐 ENT-OPS 配置表命名惯例），保留

## 5. 「非 D16 缺项表、不进数仓分层」论证

**成立。** 理由核对：(1) D16 五件套与 `gapfill_` 前缀的语义是「缺项统计行的补齐溯源」，四表行是运营配置真源（可增删改、随写随读、十行级），非缺项补齐，不挂五件套语义正确（METRIC §2/§3 佐证）；(2) ODS/DWD/ADS 是统计加工分层，配置行无 ETL、无调度、无加工语义，不进分层正确（ARCH §6「数据源配置仅元数据登记」）；(3) POL 先例中缺项表走 `gkxlumenx_gapfill`，本二级若混入会污染缺项语义与 GDF 闸门口径——独立建库（换名后）是对的；(4) 不注册数据资产目录/指标注册表与「全 N/A」互为印证。

## 6. 事实错误清单（证据汇总）

| # | 错误 | 位置 | 证据 |
|---|---|---|---|
| 1 | 「建表归 Java 实现单……两单待建单签收后起草」残留旧裁定，与 §1/ARCH §3.2/监管裁定矛盾 | TS-L2-M10-LAYER-DATA.md:108 | 同文件 :29/:33；TS-L2-M10-LAYER-ARCH.md:60 |
| 2 | 「Python 侧管理的库 gkxlumenx_config（建议名）」与既有库重名且归属失实（实为 Java 平台库/Nacos 配置库，dev 12 表在册） | TS-L2-M10-LAYER-DATA.md:29；ARCH :46-50/:59/:78；API :32 | algo-mysql-connection-info.md:83-88；ARCH-DISPLAY-01.md:1157；M_SCIUI_DATAOV_001.md:123；DEVOPS-LUMEN-DEMO-WAREHOUSE-L01.md:46 |

种子值本身（§2–§5 各表列值）**无事实错误**；§0 对 ARCH 的 3/3/9/11 纠错正确且 ARCH 现稿已回填。

## 7. 签收边界

- 本页只读核对：不改被审四分册，不动 task-registry / WBS，不建库、不执行 DDL、不灌数、不跑脚本、不动 demo/lumen 两仓源码、不 git commit/push
- 灌数单（DDL+26 行种子，Python）与 Java 实现单、接线单均为后续待建单，本会签不代替其签收
- C1/C2 回填后由 `agent:data-agent` 在本页 §8 追记确认即转「同意会签」；签收（done）仍由监管 `human:刘剑锋` 做

## 8. v3 快审（2026-11-06）

**结论：通过（同意会签 v3 终版）。** v3 将四表挪回业务库、DDL+种子（26 行）+运行时 CRUD 全归 Java（实现单 SQL 变更脚本 + 领域服务）、Python 完全退出无灌数单——v2 两条件 C1/C2 分别已修与消解，全稿无 v2 残留断言，种子与列定义未漂移。本节即 §7 约定的 C1/C2 追记确认，v3 下转「同意会签」；签收（done）仍归监管 `human:刘剑锋`。

### 8.1 v3 变更影响面核对清单

| # | 核对项 | 结果 | 证据 |
|---|---|---|---|
| 1 | §1 总则与分工表为 v3 终版：四表全落**业务库**（`lumen-svc-platform` 现有业务库实例，schema 实现单定）；DDL+种子 26 行一体归 **Java 实现单 SQL 变更脚本**，运行时读写归 **Java 领域服务**（display 门面校验后 Feign 调用，D15 链路）；「Python 不参与」 | 通过 | DATA `:29`–`:35` |
| 2 | 生成方归属改写侧：`group_code`「新建 `grp-` + 序（**Java 写侧生成**）」、`source_code`「新建 `src-` + 序（**Java 写侧生成**）」 | 通过 | DATA `:62` / `:77` |
| 3 | 审计列写方：`created_at`/`updated_at`「由写方（**Java 领域服务**）维护」 | 通过 | DATA `:36` |
| 4 | §6 不做清单无灌数单：现文「DDL + 种子（26 行）+ 运行时 CRUD 全归 Java 实现单，一单待建……无 Python 灌数单」，与 §1 分工表一致 | 通过 | DATA `:107` |
| 5 | v2 残留 grep：`gkxlumenx_config` **零匹配**（C2 原撞名库彻底清除）；`gkxlumenx_show_config` 仅 `:29` 一处且为「v2 方案作废」否定说明；`/internal/gkx-show`、`gkx_show_service`、`两单` 均**零匹配**；`灌数单` 2 处（`:29` 作废语境、`:107`「无 Python 灌数单」否定句）均非正文断言 | 通过 | grep 全稿（2026-11-06） |
| 6 | 种子锚点未漂移：3 src（`src-1/2/3`，enabled **1/1/0**）/ 3 grp（`grp-ip/lit/org`，组色 **#165DFF/#00B42A/#F97316**）/ 9 layer（LAYER_OPTIONS 九值同序、enabled 全 1）/ 11 factor（keys 顺序与本页 §1.4 基线一致），总数 26；源文件复核仍逐值相符（layerSourceState.js `:13`–`:49` enabled true/true/false、situation.ts `:92`–`:104` 11 行） | 通过 | 本页 §1 基线 + 源仓抽查 |
| 7 | 「种子为真配置非 mock、不适用 D18」在 Java 写种子下自洽：D18 射程是**指标缺项数据的 Python mock 灌数**，四表是业务初始配置（真源、可增删改、十行级），不在其列；且 v3 下 Python 完全退出，D18 的「Python 灌」前提本身不成立；「真配置非 mock、不挂 MockBadge」语义与 ARCH §3.6 / METRIC §3 三稿一致（本页 §3 已核，v3 未动）；§1 已显式声明「业务配置表不受 D7 数据域写约束」（D7 约束数仓灌数，2026-11-06 开发核实后裁定） | 通过 | DATA `:29`/`:33`；本页 §3 |
| 8 | 库选址：取消独立 `*_config` 库，回 `lumen-svc-platform` 现有业务库实例，不进 ODS/DWD/ADS/供应方库、不用 `gapfill_` 前缀的裁定未变（本页 §5 论证继续成立） | 通过 | DATA `:29` |

### 8.2 v2 两条件在 v3 下的处置

- **C1（§6 残留旧分工）——已修**：§6 现文与 §1 分工表完全一致（均 Java 全包、「一单待建」），「两单」表述零匹配。注：v2 建议的修法方向是「归 Python 灌数单一单」，v3 以监管人开发核实裁定取代该方案（Java 建表写数），一致性目标达成，矛盾消除，本条件关闭。
- **C2（库名撞 `gkxlumenx_config`）——消解**：v3 取消独立配置库，四表回业务库实例，撞名对象在稿内零出现；v2 修订期的过渡建议名 `gkxlumenx_show_config` 亦仅存于「方案作废」说明。具体落哪个业务库 schema 由 Java 实现单定，属后续单范围，本条件关闭。

### 8.3 随单移交（非阻断）

v2 §0 的三条非阻断建议在 v3 下收件人由灌数单改指 **Java 实现单**：(1) §5 的 11 个颜色种子宜在实现单逐值落字（取值即用本页 §1.4 表）；(2) DDL 惯例（`utf8mb4` / 中文注释 / 逻辑外键不建物理 FK）宜沿（惯例文本面向数仓层，对业务库表为建议非强制）；(3) API DTO `groupId`（bigint）与表列 `group_code`（varchar）的 id→code 映射落点提示实现单注意。均不阻断签收。

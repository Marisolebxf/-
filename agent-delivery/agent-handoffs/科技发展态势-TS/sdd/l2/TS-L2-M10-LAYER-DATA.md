# TS-L2-M10-LAYER-DATA · 维护管理 · 图层与数据源 · 数据落点

- 任务：`TS-L2-M10-LAYER-DATA`
- 日期：2026-11-06
- 状态：数据分册已落盘，待架构、接口、算法、数据四角色会签。不标 done
- 监管：`human:刘剑锋` · 认领：`agent:data-agent`
- 强度：ponytail off（定义任务，不缩文档）
- 用户故事：M1 序 5–9（多对象图层管理 / 实时数据监控 / 图层分组与组织 / 数据源灵活配置 / 基础信息查看）
- 上游：`sdd/l2/TS-L2-M10-LAYER-ARCH.md` §2/§3（integration，待会签）
- 种子事实源：`repos/demo-ui-science/src/pages/tech-situation-maintain/layerSourceState.js` = `lumen-ui-science-pc/src/views/situation/maintain/maintainModel.ts`（逐字一致）；`lumen-ui-science-pc/src/mock/modules/situation.ts factorItems` / `entityColorByKey`

本叶定「图层与数据源」二级的数据落点：四张配置表的**列级定义**（粒度与必要列，不是可执行 SQL）。SRS 序号 M1 序 5–9 配置维护面。本单不建库、不建表、不灌数、不跑脚本。

## 0. 对 ARCH 稿的一处事实修正（未会签稿纠错）

ARCH §3 第 2 点与 §4.2 图写「demo 冻结种子：8 条数据源 / 9 组图层组 / 11 要素」。经核对 demo 源仓与 lumen 复刻仓（逐字一致），真种子是：

| 对象 | 真值 | 备注 |
|---|---|---|
| 数据源 | **3 条**（`src-1` 专利 API / `src-2` 论文主题库 / `src-3` 机构填报） | ARCH 的「8」疑把数据源表 8 列误记为行数 |
| 图层组 | **3 个**（`grp-ip` 知识产权 / `grp-lit` 文献 / `grp-org` 主体） | ARCH 的「9」疑把 9 图层枚举误记为组数 |
| 图层枚举 | **9 行**（`LAYER_OPTIONS`：论文/期刊/专利/专家学者/会议/组织机构/课题/项目/成果） | ARCH 未给 `cfg_tech_layer` 种子行数，本单补齐 |
| 要素显示 | **11 行**（`factorItems`：scholar/meeting/institution/enterprise/service/topic/project/paper/journal/patent/result） | 与 ARCH 一致 |

种子总数 3+3+9+11 = **26 行**。本单随稿修正 ARCH 两处数字（ARCH 未会签，属事实性纠错，不是代签）。D18 三要素（表/灌数方/读接口）不因该修正变化。

## 1. 总则

四表全落 **`gkxlumenx_show_config`**（Python 侧管理的库，建议名，会签确认——2026-11-06 监管人裁定：**写数据库全归 Python，保持原有规矩**）。不进 ODS / DWD / ADS / 供应方库 / 业务库，不用 `gapfill_` 前缀（配置真源，非 D16 缺项表）。无 ETL、无调度、无同步动作——数据源「配置」仅元数据登记（ARCH §6）。

| 角色 | 职责 |
|---|---|
| 建表（DDL）+ 种子行 | **data-agent 灌数单（Python，建表与 26 行种子一体**，值取 §2–§5 种子列） |
| 运行时写 | **Python**：`gkx_show_service` 经 `/internal/gkx-show/maintain/config/**`（display 门面校验后 Feign 转发，D15 链路，ARCH §3） |
| 运行时读 | 领域服务直读（政策 gapfill 只读先例）→ display Feign 聚合；M1 只读 layers / factor-display |

逻辑外键（`target_layer_code` / `group_code`）不建物理 FK 约束（沿数据域 MySQL 惯例）。每表公共审计列：`created_at` / `updated_at`（datetime，**由写方（Python）维护**）。**无** `metric_id` / `is_mock` / `gap_item` / `fill_method` / `gapfill_batch_id` / `generated_at` 列（METRIC 分册 §3）。

种子行语义：真实初始配置（运营继续编辑的起点），非 mock 统计，不挂 MockBadge；种子值与 demo 演示数据刻意一致（冻结清单），此「一致」即本单显式标注的占位事实——不需要进一步标注。

## 2. cfg_tech_layer（9 行，序 5）

一行=一个枚举图层。**只可改 `enabled`**，行集固定不可增删。

| 列 | 类型 | 空 | 约束 |
|---|---|---|---|
| `id` | bigint | 否 | 行键，自增 |
| `layer_code` | varchar(32) | 否 | 唯一。9 值：`paper` `journal` `patent` `scholar` `meeting` `institution` `topic` `project` `result` |
| `layer_name` | varchar(64) | 否 | 中文显示名（论文/期刊/专利/专家学者/会议/组织机构/课题/项目/成果），冻结不改 |
| `enabled` | tinyint | 否 | 默认 1。启停=可见性，单一位 |
| `sort_order` | int | 否 | 1–9，按上列顺序冻结 |
| `created_at` / `updated_at` | datetime | 否 | 审计 |

种子：9 行，`enabled` 全 1（demo 图层枚举无初始禁用态），`sort_order` 1–9。

## 3. cfg_tech_layer_group（3 行，序 7）

一行=一个图层分组。可增删改。

| 列 | 类型 | 空 | 约束 |
|---|---|---|---|
| `id` | bigint | 否 | 行键，自增 |
| `group_code` | varchar(32) | 否 | 唯一。种子 `grp-ip` / `grp-lit` / `grp-org`；新建 `grp-` + 序（Python 写侧生成） |
| `group_name` | varchar(64) | 否 | 种子：知识产权图层组 / 文献图层组 / 主体图层组 |
| `color` | varchar(9) | 否 | `#RRGGBB`。种子：`#165DFF` / `#00B42A` / `#F97316`（demo 冻结） |
| `sort_order` | int | 否 | 种子 1–3 |
| `created_at` / `updated_at` | datetime | 否 | 审计 |

删除约束：组内仍有 `cfg_tech_datasource` 引用时由 API 层拒删（`409 GROUP_IN_USE`），表上不建物理约束。

## 4. cfg_tech_datasource（3 行，序 8）

一行=一条数据源登记。可增删改。

| 列 | 类型 | 空 | 约束 |
|---|---|---|---|
| `id` | bigint | 否 | 行键，自增 |
| `source_code` | varchar(32) | 否 | 唯一。种子 `src-1` / `src-2` / `src-3`；新建 `src-` + 序（Python 写侧生成） |
| `source_name` | varchar(64) | 否 | 种子：专利 API / 论文主题库 / 机构填报 |
| `source_type` | varchar(16) | 否 | 三值枚举：`API 接口` / `数据库表` / `用户填报`（中文冻结）。种子依次三型各一 |
| `target_layer_code` | varchar(32) | 否 | 逻辑引用 `cfg_tech_layer.layer_code`。种子：`patent` / `paper` / `institution` |
| `endpoint` | varchar(512) | 否 | 语义随型：URL / 表名 / 填报模板名。种子：`https://mock.api/patents` / `dwd.paper_topic` / `填报模板-机构台账`（demo 冻结原文） |
| `enabled` | tinyint | 否 | 种子：1 / 1 / 0 |
| `group_code` | varchar(32) | 是 | 逻辑引用 `cfg_tech_layer_group.group_code`，可空。种子：`grp-ip` / `grp-lit` / `grp-org` |
| `created_at` / `updated_at` | datetime | 否 | 审计 |

**不设列**：`last_sync`（无同步动作）、`test_status`（探测不持久化，API 分册 §0/§4.1）。种子中的 `lastSync` / `testStatus` 演示值不迁移。

## 5. cfg_factor_display（11 行，序 9 配置面）

一行=一个要素的显示配置。**行集固定不可增删**，只可改显示名与颜色。

| 列 | 类型 | 空 | 约束 |
|---|---|---|---|
| `id` | bigint | 否 | 行键，自增 |
| `factor_key` | varchar(32) | 否 | 唯一。11 值：`scholar` `meeting` `institution` `enterprise` `service` `topic` `project` `paper` `journal` `patent` `result` |
| `display_name` | varchar(64) | 否 | 默认=要素中文名（专家学者/会议/组织机构/企业/服务机构/课题/项目/论文/期刊/专利/成果），可覆盖（≤32 字由 API 校验） |
| `color` | varchar(9) | 否 | `#RRGGBB`。种子=M1 `entityColorByKey` 默认色冻结 |
| `sort_order` | int | 否 | 1–11，按 `factorItems` 顺序冻结 |
| `created_at` / `updated_at` | datetime | 否 | 审计 |

**不设列**：`active`（要素图例开关是 M1 地图运行态，不属本配置表——本表只管显示名/颜色，ARCH §0 序 9 裁定）。

M1 消费：`GET /factor-display` 按 `factor_key` 对齐 `mapResult.factorItems` 覆盖图例/marker（FE-TS-10A §M1 联动语义的服务端化）。localStorage `lumen-ui-science-pc:factor-display-v1` 在接线单后降级为离线只读缓存或移除（接线单定）。

## 6. 不做

- 不建库、不执行 DDL、不灌数（**DDL+种子（26 行）一体归 data-agent 灌数单（Python），一单待建**，定义单签收后起草；2026-11-06 会签 DATA-C1 修正：原稿此句残留旧分工）
- 不写 ODS / DWD / ADS / 供应方库；不写 `gapfill_` 表；不做 ETL / 调度 / 真同步
- 不为 DB 型数据源建连通探测表（probe 不落任何表）
- 不把 `cfg_*` 表注册进数据资产目录或指标注册表（无 metric 挂接，METRIC 分册）
- 不动 demo 仓与 lumen 仓源码（种子为只读事实源）

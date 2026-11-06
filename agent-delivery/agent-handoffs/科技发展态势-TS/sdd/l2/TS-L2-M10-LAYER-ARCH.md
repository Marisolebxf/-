# TS-L2-M10-LAYER-ARCH · 维护管理 · 图层与数据源 · 后台实现架构设计

- 任务：`TS-L2-M10-LAYER-ARCH`
- 日期：2026-11-06
- 状态：架构稿已落盘，待架构、接口、算法、数据四角色会签。不标 done
- 监管：`human:刘剑锋` · 认领：`agent:arch-agent`
- 强度：ponytail off（定义任务，不缩文档）
- 图：`TS-L2-M10-LAYER-ARCH-SEQ`（调用链）· `TS-L2-M10-LAYER-ARCH-DATA`（数据流），均为本二级新图（draft）

本叶只定维护管理（M10）二级「图层与数据源」的实现架构和整体流程。需规序号 **M1 序 5–9**（`科技全域态势.md`：图层配置 5 多对象图层管理 / 6 实时数据监控 / 7 图层分组与组织 / 8 数据源灵活配置；科创要素 9 基础信息查看功能的配置面）。不写 OpenAPI 字段、DTO、枚举、错误码——那是 `TS-L2-M10-LAYER-API`（待建）。

上游只引用，不改写：`科技全域态势.md` 序 5–9、[FE-TS-10A.md](../../FE-TS-10A.md) as-built、[对照-科技发展规划与维护管理-存量任务与依赖.md](../../../../工程过程/04-系统集成/05-展示系统集成/对照-科技发展规划与维护管理-存量任务与依赖.md) A 段、[新人引导-科技发展规划与维护管理.md](../../新人引导-科技发展规划与维护管理.md) §2/§4.1、`architecture-baseline.md`（D3/D7/D12/D15/D18）。不新造 `metric_id`，不改 D4。

签收标准（D18，可实现才签）：本叶逐项写明表名、灌数方、读取接口；配置写侧不返回内存 mock，接口读表。允许用户保存的配置落 Java 业务库配置表（写侧 CRUD，见 §3 裁定），种子数据由 Python 灌数单写入（对齐 D18 形态）。

## 0. 范围裁定

| 项 | 裁定 |
|---|---|
| 序 5 多对象图层管理 | **在本二级**：图层的可见性开关、启停配置的持久化与消费。M1 地图是消费端，不在本二级重做地图 |
| 序 6 实时数据监控 | **读侧归 M1**（WBS-05-18 管线，要素分布/密度地图渲染已有）；本二级只承担"数据源启停 → 影响 M1 刷新"的配置面 |
| 序 7 图层分组与组织 | **在本二级**：分组增删改、重命名、颜色标记（配置写侧） |
| 序 8 数据源灵活配置 | **在本二级**：数据源登记（API 接口 / 数据库表 / 用户填报三型）、编辑、启停、删除；测试连通见 §3 |
| 序 9 基础信息查看功能 | **读侧归 M1**（浏览/详情/筛选/收藏，WBS-05-18）；本二级只承担 FE-TS-10A 已复刻的**要素显示配置面**（11 要素显示名/颜色，现 localStorage，正式化入配置表） |
| 序 34–40 维护技术图谱 | **不在本二级**（报价划掉，不建实现单；见对照文档 A.1） |
| 序 41–47 关键实体与关系 | **不在本二级**（归 `TS-L2-M10-ENT-*`，后续二级） |

一句话：本二级 = **M10 维护页「图层与数据源配置」分区的正式化**：把 FE-TS-10A 的页面内存 + localStorage 演示态，落成服务端配置表 + CRUD REST + M1 消费链路；地图展示本体一句不动。

## 1. 存量调查（as-built，2026-11-06 核对）

| 件 | 现状 | 与正式架构的差距 |
|---|---|---|
| `lumen-ui-science-pc` maintain 分区1 | 数据源表 8 列（新增/编辑弹窗、测试连通、启停、删除确认）+ 图层组管理 + 11 要素显示名/颜色行内编辑；状态在页面 ref，刷新即失 | 无持久化；`fetchMaintainMeta` real 分支只打 `GET /situation/v1/maintain/meta`（唯一端点，未冻结） |
| 要素显示配置 | `src/stores/factorDisplay.ts` + `localStorage lumen-ui-science-pc:factor-display-v1`；M1 全域态势图例/marker 跨页消费 | 单浏览器私有，换机/换浏览器丢失；服务端不可见 |
| M2 全景入口 | `query.section=graph` 跳入本页 graph 分区（34–40 壳） | 不变，与本二级无冲突 |
| `lumen-svc-platform` | 无 `/situation/v1/maintain/**` 实现（grep 0 命中）；有 gkxlumen-display 模块与业务库先例 | 配置表与 CRUD 均为新建 |
| `BE-TS-CONTRACT-02` | 范围 M2–M9，无 M10 契约 | 本二级 API 单从零起草，对齐 as-built URL 差异见 §5 |

## 2. 需规叶 → 实现裁定总表（D18 核查表）

本二级为**配置写侧功能，无统计数字输出**，`metric_id` 全部 **N/A**（序 6 的分布/密度统计属 M1 读侧，不在本二级，D9 不适用；由 `TS-L2-M10-LAYER-METRIC` 复核本结论）。

| 叶 | 裁定 | 表 | 灌数方/写者 | 读取接口（Java REST） |
|---|---|---|---|---|
| 序 5 图层启停/可见性 | 真读写（配置 CRUD） | `cfg_tech_layer`（业务库） | 种子行：data-agent 灌数单（Python）；用户写：`gkxlumen-display` | `/display/v1/situation/maintain/layers`（GET/PUT） |
| 序 7 图层分组与组织 | 真读写（配置 CRUD） | `cfg_tech_layer_group`（业务库） | 同上 | `/display/v1/situation/maintain/layer-groups`（GET/POST/PUT/DELETE） |
| 序 8 数据源登记（API/DB 表/用户填报） | 真读写（配置 CRUD） | `cfg_tech_datasource`（业务库） | 同上 | `/display/v1/situation/maintain/datasources`（GET/POST/PUT/DELETE） |
| 序 8 测试连通 | API 型：Java 端点探测（HTTP HEAD/GET + 超时）；DB 表型：**501**（Java 不直连业务库探测，Python 侧探测属后续增强，未排期）；用户填报型：无探测语义，前端禁用按钮 | —（不落表，探测结果不持久化） | — | `/display/v1/situation/maintain/datasources/{id}/probe`（POST） |
| 序 9 配置面（11 要素显示名/颜色） | 真读写（配置 CRUD，取代 localStorage） | `cfg_factor_display`（业务库） | 同上 | `/display/v1/situation/maintain/factor-display`（GET/PUT） |
| 序 6 实时数据监控（读侧） | **不实现**（归 M1）；本二级仅通过 datasource 启停位影响 M1 刷新 | — | — | — |

> 表名前缀 `cfg_` 对齐 ENT-OPS data-gap-catalog 的配置表命名惯例（cfg_*）。三表字段（DDL）归 `TS-L2-M10-LAYER-DATA`；路径/DTO/错误码归 `TS-L2-M10-LAYER-API`。本叶只锁表名、写者、读接口三要素。

## 3. 关键裁定：配置写侧为什么落 Java 业务库（会签重点 ①）

调用链铁律「前端 → Java REST → Python `/internal/*`」与「写数归 Python（D7）」约束的是**数据域写**（ODS/DWD/ADS/图谱的灌数与计算）。图层/数据源/要素显示配置是**运营配置元数据**，特征：行数小（十行级）、强事务、随用户操作即时读写、无算法语义。裁定：

1. 配置 CRUD 走 `gkxlumen-display` 直接读写**业务库配置表**（Java 持有配置状态；同 SCI-INT-A03 的 DN-07 先例方向——Java 业务库可持有审核/配置状态，最终由会签确认）。
2. Python 不参与配置读写；仅在**灌数单**里为三表写入种子行（对齐 demo 冻结种子：8 条数据源 / 9 组图层组 / 11 要素默认显示配置），保证 D18 三要素（表/灌数方/读接口）齐备、接口永不返回内存 mock。
3. 配置表**不进** ODS/DWD/ADS/供应方库，不用 `gapfill_` 前缀（不是 D16 缺项表，是正式配置真源——区别于政策样板的 gapfill 读侧退路）。
4. 种子行 D4 语义：配置数据本身是**真配置**（非 mock 统计），界面不需要 MockBadge；仅当种子行与 demo 演示数据刻意保持一致作为占位时，由 DATA 单标注（默认不标）。

> 若会签否决此裁定（要求配置也走 Python `/internal/*` 写），退路为：Java 仍提供 REST 门面，写转发 Python `/internal/maintain/config/*`，表挪至 Python 侧管理——成本更高、无收益，仅作记录。

## 4. 实现架构

### 4.1 调用链（图 `TS-L2-M10-LAYER-ARCH-SEQ`）

```mermaid
flowchart LR
  fe["M10 维护页 · 图层与数据源分区（FE-TS-10A 页面，接线单改造）"]
  m1["M1 全域态势地图（消费端，只读配置）"]
  gw["gkxlumen-platform-gateway"]
  bff["gkxlumen-display（Java）配置 CRUD + 只读"]
  db[(业务库 cfg_tech_layer / cfg_tech_layer_group / cfg_tech_datasource / cfg_factor_display)]
  py["data-agent 灌数单（Python，一次性种子行）"]

  fe -->|"/display/v1/situation/maintain/**（CRUD）"| gw --> bff --> db
  m1 -->|"GET layers / factor-display（只读）"| gw --> bff
  bff -->|"probe：API 型端点探测（DB 型 501）"| fe
  py -.->|"种子行写入（建表后一次）"| db
```

要点：浏览器只打 `/display/v1/situation/maintain/**`；M1 地图经同一 BFF 只读配置（替换 localStorage 消费）；无任何 demo 依赖（D12）。

### 4.2 数据流（图 `TS-L2-M10-LAYER-ARCH-DATA`）

```mermaid
flowchart LR
  seed["demo 冻结种子：8 数据源/9 图层组/11 要素显示"] --> pyw["灌数单（Python）"] --> tables["cfg_* 三+一表"]
  tables --> jread["gkxlumen-display 读"] --> fe["M10 维护页渲染"]
  fe -->|"用户保存图层/分组/数据源/要素显示"| jwrite["gkxlumen-display 写"] --> tables
  tables -->|"图层启停+要素显示配置"| m1read["gkxlumen-display 只读"] --> m1["M1 地图图例/marker/刷新"]
```

要点：单一真源 = 配置表；页面内存演示态与 localStorage 在接线单完成后**移除写路径**（factorDisplay store 改为服务端拉取 + 本地缓存回退只读）。

## 5. 与 FE-TS-10A 复刻页的接口差异（接线单输入）

| 项 | as-built（FE-TS-10A） | 正式架构（本叶） | 接线单动作 |
|---|---|---|---|
| 元数据 | `GET /situation/v1/maintain/meta` 一次取全（未冻结） | 拆为 4 组资源（layers / layer-groups / datasources / factor-display） | api 层重写拼装；`meta` 端点废弃（BE 从未实现，无兼容负担） |
| 写操作 | 页面内存（刷新即失，demo 同语义） | 4 组 CRUD REST | 分区1 全部按钮接真接口；删除仍走确认弹窗 |
| 要素显示 | localStorage + store | `GET/PUT factor-display` | store 数据源替换；localStorage 降级为离线缓存或移除（接线单定） |
| 测试连通 | 假延迟 + 假结果 | `POST probe`（API 型真探测，DB 型 501 空态文案） | 按钮 501 态文案 |
| MockBadge | 页面无 🧪 | 配置数据为真数据不挂 badge；种子行若保留演示值由 DATA 单标 | 接线单核对 |

## 6. 明确不做

- 不重做/不改 FE-TS-10A 页面结构（锁定期内不动 maintain 目录；接线单只改 api 拼装层）
- 不做地图渲染、要素浏览/详情/收藏（M1 读侧，WBS-05-18）
- 不做 DB 表型数据源的真连通探测（501，后续增强）
- 不碰序 34–40（报价划掉）与序 41–47（ENT 二级）
- 不新造指标、不写字段表、不重开 GDF；不做 ETL/调度（数据源"配置"仅元数据登记）

## 7. 会签关注点

1. §3 配置写侧落 Java 业务库的裁定（或退路）
2. `cfg_*` 表放业务库（gkxlumen-display 库）的位置是否接受
3. probe 的 API 型探测发起方（Java 出网）是否允许
4. 接口差异表 §5 的 `meta` 端点废弃
5. METRIC 复核 §2 的"全 N/A"结论

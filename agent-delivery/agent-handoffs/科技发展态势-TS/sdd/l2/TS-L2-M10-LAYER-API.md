# TS-L2-M10-LAYER-API · 维护管理 · 图层与数据源 · 后台接口设计

- 任务：`TS-L2-M10-LAYER-API`
- 日期：2026-11-06
- 状态：接口分册已落盘，待架构、接口、算法、数据四角色会签。不标 done
- 监管：`human:刘剑锋` · 认领：`agent:api-agent`
- 强度：ponytail off（定义任务，不缩文档）
- 用户故事：M1 序 5–9（多对象图层管理 / 实时数据监控 / 图层分组与组织 / 数据源灵活配置 / 基础信息查看）
- 上游：`sdd/l2/TS-L2-M10-LAYER-ARCH.md`（integration，待会签。本分册以该稿为准，不改它）
- 种子事实源：`repos/demo-ui-science/src/pages/tech-situation-maintain/layerSourceState.js` 与 `lumen-ui-science-pc/src/views/situation/maintain/maintainModel.ts`（逐字一致：3 数据源 / 3 图层组 / 9 图层枚举）、`lumen-ui-science-pc/src/mock/modules/situation.ts factorItems`（11 要素）

本分册只定维护管理二级「图层与数据源」的后台接口。需规序号 M1 序 5–9 的**配置维护面**（读侧归 M1 的部分见 ARCH §0）。`BE-TS-CONTRACT-02` 范围是 M2–M9，不含 M10，**不回填**；本分册是 M10 维护面的唯一契约源，后续 Java 实现单以本分册定 DTO、枚举与错误码。不写实现代码。

签收口径：全部资源同步读写业务库配置表（表结构归 `TS-L2-M10-LAYER-DATA`）。接口读表，不返回内存 mock。无行返回空数组，不返回 501。唯一 501 是数据库表型数据源的连通探测（ARCH §2 裁定）。

## 0. 与 as-built 的差异（接线单输入，细化 ARCH §5）

| 项 | as-built（FE-TS-10A） | 本分册契约 | 接线单动作 |
|---|---|---|---|
| 元数据 | `GET /situation/v1/maintain/meta` 一次取全（real 分支唯一端点，BE 从未实现） | 废弃。拆 4 组资源（本分册 §2–§5） | api 层重写拼装 |
| 图层标识 | `targetLayer` 存中文字面量（`'专利'`） | `targetLayerCode` 存英文 code（`patent`），显示名经 layers 资源带出 | 对照 LAYER_OPTIONS 索引取 code |
| 最后同步列 | 行上 `lastSync` 展示值 | **不设**。数据源是元数据登记，无同步动作（ARCH §6 不做 ETL） | 「最后同步」列移除或恒显 `-` |
| 测试连通 | `testStatus` 存行上（'通过'/'待测'/'未测'） | 探测结果不持久化（ARCH §2），每次 probe 实时返回 | 行上无该字段，按钮态即时呈现 |
| 删除图层组 | demo 无约束直接删 | 组下仍有数据源引用时 `409 GROUP_IN_USE`，先改挂再删 | 前端接 409 文案 |
| 至少保留一组 | demo 有「至少保留一个图层组」约束（`layerSourceState.js` 删组逻辑） | **正式契约不保留**该约束（运营配置，删空组集合属合法态，UI 侧不强制） | 2026-11-06 会签 API 备注补行：显式声明放弃，接线单不再移植该拦截 |

## 1. 总则

前缀 `/display/v1/situation/maintain/`。浏览器只打此前缀，经网关 `gkxlumen-platform-gateway`（只转 `/display/**`）到 `gkxlumen-display`。全部同步，无 Job、无任务记录、不建 SSE、不进 `gkxlumen-topic-async-service`。不调任何 `demo-*` 服务。

**内部委托（2026-11-06 开发核实后终版 v3，ARCH §3）**：配置表归 Java 业务库，Python 不参与。`gkxlumen-display` 是门面（鉴权、枚举/参数校验、聚合），**不直连 Python/DB（D15）**：

- 读：display 经 Feign → 领域服务 → 直读业务库 `cfg_*` 四表，M1 消费同链路
- 写：display 门面校验（本分册 §7 枚举与格式校验在门面完成，400 类错误不出网关层）→ Feign → 领域服务直写业务库。写侧错误（404/409）由领域服务写结果回传映射，错误码语义与本分册 §6 一致
- 对外 URL、方法、DTO、错误码不受内部链路影响——本分册全部契约不变

行数量级：图层 9、要素 11、数据源与分组十行级。**全量返回，不分页**。

写操作均全量小对象提交；并发冲突用行级最后写胜（运营配置，单管理员场景，不设乐观锁版本号）。

鉴权沿 `/display` 网关登录态；M10 页面无权限是页面降级非白屏（WBS-05-24 行），接口不做细粒度角色。traceId 沿既有展示链，本分册不新设计观测点。

## 2. layers（序 5 图层启停/可见性）

图层是**固定枚举集**（9 个，demo `LAYER_OPTIONS` 冻结），不可增删——增删的是数据源与分组，不是图层。每图层仅一个 `enabled` 位：开=参与 M1 渲染，关=隐藏。可见性与启停合并为这一个位，不拆两位。

| 方法路径 | 语义 | 请求 | 响应 |
|---|---|---|---|
| `GET /layers` | 全量图层（M1 与 M10 都消费） | — | `200 { items: Layer[] }` |
| `PUT /layers` | 批量改启停 | `{ items: [{ layerCode, enabled }] }` | `200` 更新后全量 `Layer[]` |

Layer：`layerCode`（英文 code，见 §7）、`layerName`（中文显示名）、`enabled`（boolean）、`sortOrder`（int）。

- 只接受 `layerCode` + `enabled`；`layerName` / `sortOrder` 不可经本接口改（枚举冻结）。带其他字段忽略，不报错
- `layerCode` 不在 9 枚举内 → `400 PARAM_INVALID`
- M1 地图初始化时 `GET /layers` 取开关集；本接口不提供图层内点位/样式数据（那是 M1 读侧管线）

## 3. layer-groups（序 7 图层分组与组织）

| 方法路径 | 语义 | 请求 | 响应 |
|---|---|---|---|
| `GET /layer-groups` | 全量分组 | — | `200 { items: LayerGroup[] }` |
| `POST /layer-groups` | 新建 | `{ groupName, color, sortOrder? }` | `201` 新建 `LayerGroup` |
| `PUT /layer-groups/{id}` | 改名/颜色/排序 | `{ groupName?, color?, sortOrder? }` | `200` 更新后 `LayerGroup` |
| `DELETE /layer-groups/{id}` | 删除 | — | `200`；组内仍有数据源 → `409 GROUP_IN_USE` |

LayerGroup：`id`（服务端生成 bigint）、`groupCode`（种子冻结 `grp-ip` / `grp-lit` / `grp-org`，新建由服务端按 `grp-` + 序生成）、`groupName`（≤64 字）、`color`（`#RRGGBB`）、`sortOrder`。

- `groupName` 不强制唯一（demo 同语义，避免过度设计）；`groupCode` 唯一
- `color` 不合 `#RRGGBB` 格式 → `400`
- 删除分组前须先把组内数据源改挂他组或置空（PUT datasource 的 `groupId` 传 `null`）

## 4. datasources（序 8 数据源灵活配置）

| 方法路径 | 语义 | 请求 | 响应 |
|---|---|---|---|
| `GET /datasources` | 全量数据源 | — | `200 { items: Datasource[] }` |
| `POST /datasources` | 登记 | `{ sourceName, sourceType, targetLayerCode, endpoint, groupId? }` | `201` 新建 |
| `PUT /datasources/{id}` | 编辑 / 启停 / 改挂 | 同上字段任意子集 + `enabled?` | `200` 更新后 |
| `DELETE /datasources/{id}` | 删除 | — | `200`。无级联：删源不动分组与图层 |

Datasource：`id`、`sourceCode`（种子 `src-1` / `src-2` / `src-3`，新建 `src-` + 序）、`sourceName`（≤64 字）、`sourceType`（§7 三值）、`targetLayerCode`（9 枚举）、`endpoint`（≤512 字，语义随 `sourceType`：URL / 表名 / 填报模板名）、`enabled`、`groupId`（可空）。

- `sourceType` / `targetLayerCode` 出枚举 → `400`
- `groupId` 传值须存在 → `404 NOT_FOUND`
- **无 `lastSync`、无 `testStatus` 字段**（§0 差异）：数据源无同步动作，探测不持久化

### 4.1 probe（序 8 测试连通）

| 方法路径 | 语义 | 响应 |
|---|---|---|
| `POST /datasources/{id}/probe` | 按型分派实时探测 | 见下 |

| sourceType | 行为 | 响应 |
|---|---|---|
| `API 接口` | 领域服务发起 `HEAD`（失败回退 `GET`）探测 `endpoint`，超时 5s，重定向跟随 ≤3，**不读响应体**（display 不出网，D15） | `200 { result: '通过'\|'失败', latencyMs, message? }` |
| `数据库表` | 未排期（ARCH §2） | `501 { code: 'NOT_IMPLEMENTED', message: '数据库表型数据源连通探测未排期' }` |
| `用户填报` | 无探测语义 | `400 { code: 'PARAM_INVALID', message: '用户填报型数据源无连通探测语义' }`（2026-11-06 会签 API-C1 统一：原稿此格 `INVALID_SOURCE_TYPE` 与 §6 双轨，收进四码封闭） |

- API 型探测结果**只随本次响应返回，不落库、不留存、不写审计**
- **SSRF 防护（2026-11-06 会签 ARCH-C4 补进契约）**：探测目标须过私网黑名单——拒绝环回（127.0.0.0/8、::1）、私网（10/8、172.16/12、192.168/16、169.254/16）、云元数据（100.64/10 及各云 metadata 端点）地址段与内网主机名解析命中；命中即返回 `400 PARAM_INVALID`，不发起请求。DNS 重绑定防护：解析后按 IP 复核再连接（实现单 DoD 落地）
- 出网位置归领域服务（display 不出网）已获会签通过（ARCH §7 ⑤）；若部署环境最终否决出网，整条 probe 降级为全型 `501`，URL 不变（退路保留）
- 前端对填报型禁用按钮、对 DB 型按钮呈现 501 空态文案（接线单）

## 5. factor-display（序 9 配置面：11 要素显示名/颜色）

取代 `localStorage lumen-ui-science-pc:factor-display-v1`。要素集固定 11 个（M1 `factorItems` 冻结），不可增删，只可改显示名与颜色。

| 方法路径 | 语义 | 请求 | 响应 |
|---|---|---|---|
| `GET /factor-display` | 全量 11 行（M1 与 M10 都消费） | — | `200 { items: FactorDisplay[] }` |
| `PUT /factor-display` | 批量覆盖显示名/颜色 | `{ items: [{ factorKey, factorName?, color? }] }` | `200` 更新后全量 |

FactorDisplay：`factorKey`（英文 key，§7 11 枚举）、`factorName`（≤32 字，默认=要素中文名）、`color`（`#RRGGBB`）、`sortOrder`。

- 只接受 `factorKey` + `factorName` + `color`；`sortOrder` 不可改（枚举序冻结）
- `factorKey` 不在 11 枚举 → `400`；M1 消费方按 `factorKey` 对齐 `mapResult.factorItems` 覆盖图例/marker（对齐 FE-TS-10A §M1 联动语义）

## 6. 错误码汇总

| 码 | 场景 |
|---|---|
| `400 PARAM_INVALID` | 枚举外值、缺必填、颜色格式、名称超长、填报型 probe |
| `404 NOT_FOUND` | 路径 `id` / 请求 `groupId` 不存在 |
| `409 GROUP_IN_USE` | 删除仍有数据源引用的分组 |
| `501 NOT_IMPLEMENTED` | 仅 DB 型 probe |

无行=空数组 + `200`，不是 501、不是 404。无鉴权场景新码（沿网关登录态 401/403 既有语义，本分册不重定义）。

## 7. 枚举（demo 冻结，本分册冻结为唯一契约值）

**SourceType**（3 值，中文冻结）：`API 接口` / `数据库表` / `用户填报`

**LayerCode**（9 值，英文 code；`layerName` 括注）：

| code | layerName |
|---|---|
| `paper` | 论文 |
| `journal` | 期刊 |
| `patent` | 专利 |
| `scholar` | 专家学者 |
| `meeting` | 会议 |
| `institution` | 组织机构 |
| `topic` | 课题 |
| `project` | 项目 |
| `result` | 成果 |

**FactorKey**（11 值）：`scholar` `meeting` `institution` `enterprise` `service` `topic` `project` `paper` `journal` `patent` `result`（专家学者/会议/组织机构/企业/服务机构/课题/项目/论文/期刊/专利/成果）

LayerCode ⊂ FactorKey：`enterprise`、`service` 是要素但不是地图图层枚举。两枚举独立冻结，不互推导。

## 8. 不做

- 不写 Java 实现代码，不落控制器（实现单 `TS-L2-M10-BE-IMPL` 待建）
- 不改 `BE-TS-CONTRACT-02`（范围 M2–M9），不并入 `BE-TS-IMPL-01` / `BE-TS-DATA-01`
- 不定义 M1 读侧管线、要素浏览/详情/收藏（WBS-05-18）
- 不定义 ENT 分区（41–47）、图谱分区（34–40 不实现）接口
- 不设分页、乐观锁、字段级审计接口；不新建 Job/SSE/异步任务
- 不新造 `metric_id`（全 N/A，见 METRIC 分册）

## 增量 2026-11-11（TS-L2-M10-DEMO-FULL-L01，以实现为准）

真源：`agent-handoffs/科技发展态势-TS/TS-L2-M10-DEMO-FULL-L01-方案.md` §2.2。要点：

- 写方法以实现为准：`POST …/save`、`POST …/delete`（网关只放行 GET / POST）；新增返回 200。
- `cfg_tech_layer.group_code`：`GET /layers` 每行带 `groupId`；`POST /layers/save` 的 `items[]` 支持 `{layerCode, enabled?, groupId?}`，`groupId:null` 表示取消挂组。删组时组下仍有图层或数据源返回 409 `GROUP_IN_USE`，并给出计数。
- 探测落库：`cfg_tech_datasource` 新增 6 列；`GET /datasources` 返回 `probeStatus / probeAt / probeLatencyMs / probeMessage / dataUpdatedAt / rowCount`。
- probe：
  - API 型网络失败一律 200 + `result=失败`。
  - 数据库表型实做：正则校验 + schema 别名白名单（dwd / ads / ods → `demo_gkxlumenx_*`）+ information_schema + COUNT / MAX(时间列)，参数化只读。
  - 用户填报型 400；SSRF 黑名单 400。
- 写接口（全部 POST，含 probe）要求登录，401 / 40101；读接口匿名（2026-10-31 裁定）。
- 迁移：`lumen-svc-platform/db/9x_gkxlumenx_cms_tech_maintain_config_v2.sql`，可重复执行，含测试残留清理与图层挂组种子。

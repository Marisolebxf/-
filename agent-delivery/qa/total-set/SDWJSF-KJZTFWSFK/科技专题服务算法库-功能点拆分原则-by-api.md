# 科技专题服务算法库 · 功能点拆分原则（by-api）

- **版本**：**0.2.1**（2026-10-16 呈现层对齐友商可读性；0.2 #1–#12 仍有效）
- **方法名**：`by-api`（目录 / 文件名 / 任务号均带此词，**不是** 需规口径 v3）
- **适用任务（拟）**：`QA-KJZTFWALGO-FP-BY-API-L01`（登记表待 PM 补建）
- **工作单元**：**一条六级 = 一个子 agent**（L01–L60）。过程稿：`fp-split-by-api-run/`
- **金样（11b）**：**L01** 产业链基础指标（`chain.basic`）→ 人确认 → **L13** 产业全要素图谱 API（含 4A 封闭清单）→ 人确认 → 其余 **58 路可并行**
- **旧稿归档**：`fp-split-by-api-run-v0-202609/`（837 条接口级、L31 金样、无合表 Excel）**只读对照，不得回填主表**

---

## 决策摘要（#1–#12）

| # | 决策 |
|---|------|
| 1 | **B**：by-api 合表为算法库 **对外唯一** 功能点拆分交付；需规 v2 合表 **不再作为算法库总集正式稿**（可内部对照） |
| 2 | **2b**：最小粒度 = `endpoint.id` + 一条可独立验收（catalog 命名入参或顶层 `responseFields`；空态/失败等哨兵行） |
| 3 | **3c**：行级去重键 = `endpoint.id` + `field_key`（param/response 名或哨兵）；**全库不重复** |
| 4 | **4A**：图谱类 catalog `endpoint.id`（含 `*.graph`、`chain.panorama` 等；L13 金样时列 **封闭清单**）**主挂 L13**；**L05–L12** 仅需规行，METHOD/path/endpoint_id **空**，review 写「契约见 L13」 |
| 5 | **5b**：catalog 有、需规无 → **不进主表**；过程登记 `catalog-orphan-registry.yaml`，**不交付甲方** |
| 6 | **6a**：需规有、catalog 无 → **仍占 FUNC 序号**，接口列空，`catalog_status` = `req_only` |
| 7 | **7b**：`catalog_status` 归一化：`live` / `unavailable` / `mock` / `req_only` |
| 8 | **8a**：拆行只认 catalog `params` + `responseFields`；不用 sample/viz；`metricIds` **不单独拆行**；契约不全先补 catalog |
| 9 | **9a**：单 endpoint **不设行数硬顶** |
| 10 | **10a**：旧 `fp-split-by-api-run/` 已归档为 `fp-split-by-api-run-v0-202609/`；本目录为 v0.2 新跑 |
| 11 | **11b**：金样 L01 → L13 双确认后并行 58；合表前全库校验绿 |
| 12 | **12a**：合表在总集主列右侧加 **GKX 扩展列**（见下文） |

---

## 与需规口径怎么分开

| | 需规口径（内部对照） | 本套 by-api v0.2 |
|---|---|---|
| 目录 | `fp-split-run/` | `fp-split-by-api-run/` |
| 原则 | `科技专题服务算法库-最细颗粒度功能点拆分原则-v1.md` | **本文件** |
| 合表 | `…功能点拆分_v2.xlsx` 等 | `…功能点拆分-by-api_v1.xlsx`（**对外交付**） |
| 真源 | 60 六级需规 | 60 六级需规 **+** 联调台 catalog |
| 粒度 | 动作+对象+规则（模型级） | **endpoint.id + 契约字段/哨兵**（字段级，8a） |
| 实现仓 | 禁止 | 禁止读 Python/Java **实现**；**允许读** `lumen-ui-algo-apiview` catalog JSON |

**禁止**覆盖旧 v1/v2 xlsx，禁止改 `fp-split-run/work/`。

友商/深度挖掘那份约 2400 行 Excel（技术/人才/机构六级）**只学列语义**，不对标 60 条条数。

---

## 一、真源

| 角色 | 路径 |
|---|---|
| **业务真源** | 功能清单 v1.2 · sheet「深度挖掘算法」· **60** 条六级 + 需规全文（`fp-split-run/work/Lxx.md` 摘录块可引用） |
| **接口真源** | `${GKX_ROOT}/repos/lumen-ui-algo-apiview/src/catalog/*.json` |
| **冻结快照** | `fp-split-by-api-run/_catalog-snapshot.md`（SHA 以文件头为准；变更须重跑 `agent-delivery/scripts/_dump_algo_apiview_catalog.py`） |
| **挂接对照** | `fp-split-by-api-run/_l6-to-catalog-map.yaml`（4A：图谱 endpoint **主挂 L13**） |
| **孤儿登记** | `fp-split-by-api-run/catalog-orphan-registry.yaml`（5b，不交付） |

拆点逻辑：需规定能力边界；catalog 定可验收契约字段。`status=unavailable` / `local_mock` **仍拆**，`catalog_status` 如实填。

---

## 二、范围

| 项 | 约定 |
|---|---|
| 纳入六级 | **60** 条，不扩 |
| catalog 多页无六级 | `innov.*` 等 → 对照表 `catalog_skip` 或 orphan；**不另开六级** |
| `/v1` 与 `/internal` 同 handler | 计 **1** 个 endpoint（以 catalog `endpoint.id` 为准） |
| 去重 | **3c**：全库 `endpoint.id` + `field_key` 唯一；**不再**按 METHOD+path 合并吞字段 |

页面列：catalog 页 `title`。L05–L12 图谱段：页面列可填需规语义页名；接口扩展列按 4A 留空。

---

## 三、一条功能点（字段级，2b + 8a）

一条 = **`endpoint.id`（或 req_only 无接口）** + **`field_key`** + 一条可独立验收规则。

| 类型 | `field_key` | 说明 |
|---|---|---|
| 入参 | catalog `params[].name` | 接收/校验该命名入参 |
| 出参 | catalog `responseFields[]` 顶层名 | 输出/展示该字段（**不**拆 JSON 嵌套子键，除非 catalog 已列名） |
| 哨兵 | `_empty` / `_fail` / `_async` 等约定键 | 空态、失败、异步等与字段验收不同则分行 |

`metricIds` 仅作 review/血缘备注，**不**为每个 metric_id 单独占 FUNC 行。

规则来源：catalog 字段名 = 原文直接；需规有 catalog 无 = 原文直接 + `req_only`；unavailable/mock = 验收须写明契约态。

### 3.1 呈现层（友商表可读性，人拍板 2026-10-16）

主表列名 **保持招标习惯**：列仍叫 **「功能点」**（不叫「字段功能」）。用 **「算法环节」** 替代原「拆分维度」列语义（按处理链路命名，不是 HTTP 动词）。

| 主列 | 说明 |
|------|------|
| 子功能项 | 六级名 |
| **功能点** | 短标题，建议 `算法输入-{field_key}{中文简称}` / `算法输出-…` / 需规能力短语；可读即可 |
| **算法环节** | 封闭枚举（见下）；**每个 catalog 入参一行、一个环节**（不拆「处理+传递」两行） |
| **具体描述** | 1～3 句可验收正文：字段类型/必填、本环节做什么、失败或空态如何识别；可写「传入本接口」 |
| 规则来源 | 短引用（catalog / 需规章节）；细节放具体描述 |
| **接口/模型名称** | catalog 该 endpoint 的 `title` 或需规指标名（合表主列或紧挨功能点左侧，与友商 xlsx 对齐） |

**算法环节**（允许值；勿发明友商有、我方无的环节）：

| 环节 | 适用 |
|------|------|
| 查询条件处理 | catalog **入参** `params[]`：**一行/参数**，含清理、校验、标准化、作为查询条件传入本 endpoint（合并原「校验与传递」） |
| 指标计算 | 出参中 **数值/汇总/比率/趋势** 类 `responseFields` |
| 结果组装 | 出参中 **维度回显、列表结构、标识类** 字段；或契约要求的响应体组装 |
| 分析结果生成 | 空态 `_empty`、无业务数据可区分展示 |
| 异常处理 | 失败 `_fail`、入参非法、上游错误可识别（可与空态分行） |
| 结果同步 | 需规明确写「同步/消息队列/更新时间」且 **无** catalog 字段可挂时，`req_only` 行 |
| 模型计算 | 需规「数据处理/环比/阈值判定」等 **无** 对应 catalog 字段的算法语义，`req_only` |

**禁止硬写**：

- **数据源对接**：联调台 catalog 无 `dataSources` 等配置对象；后端/融合中枢配置 **不在 by-api 表拆行**。需规里的「1）数据源对接」**不单独占功能点**（除非未来 catalog 增加可验收字段）。
- 友商式「同一入参两行环节」：**不采用**；简单入参 **合并为一行** `查询条件处理`。

嵌套 object：仅 catalog **已列名** 的顶层或已声明子键可拆；勿仿友商 2400 行技术库 schema 硬造嵌套。

`metricIds` 仍不单独拆行。

---

## 四、合表与 GKX 扩展列（12a）

在招标/总集主列（子功能项、**功能点**、**算法环节**、**具体描述**、规则来源、**接口/模型名称** 等）**右侧**追加（列名可微调，语义不得丢）：

| 列 | 说明 |
|---|---|
| `endpoint_id` | catalog `endpoint.id`；req_only 空 |
| `METHOD` | HTTP 方法 |
| `path` | 路径 |
| `field_key` | 3c 去重键之一 |
| `catalog_status` | 7b：`live` / `unavailable` / `mock` / `req_only` |
| `catalog_page_id` | 可选；页 `id` |
| `dedupe_key` | 可选；`{endpoint_id}|{field_key}`（入参仅一行/字段时与 3c 一致） |

编号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-#####`（合表版本号随交付 bump）。

条数：**不设** 3889/4000 硬指标；写不出不同验收就不拆。

---

## 五、工作方式

1. 读本原则、`fp-split-by-api-run/00-control.md`、`_l6-to-catalog-map.yaml`、本六级 `prompts/Lxx.md`。
2. **11b**：先完成 L01 work/review → 人确认 → L13（产出图谱 API **封闭清单** memo）→ 人确认 → 并行 L02–L12、L14–L60。
3. 子 agent **只读**：本原则、需规块、绑定 catalog 页/endpoint、金样 **格式**。禁止读算法实现仓、禁止抄其它六级业务点。
4. 产出 `work/Lxx.md` + `review/Lxx.md`；表行须含扩展列语义（合表前可先 Markdown 表）。
5. 60/60 + **全库 3c/7b 校验脚本绿** → 合表 `…功能点拆分-by-api_v1.xlsx`。

---

## 六、检查清单

- [ ] 未覆盖旧 v1/v2 xlsx；未改 `fp-split-run/work/`
- [ ] 未扩 60 六级；5b 孤儿未进主表
- [ ] 4A：图谱 endpoint 仅 L13 挂接口列；L05–L12 review 含「契约见 L13」
- [ ] 3c：全库 `endpoint_id`+`field_key` 无重复
- [ ] 8a：未用 sample/viz 发明字段；未对 `metricIds` 逐 id 拆行
- [ ] 3.1：主列含 **算法环节 + 具体描述**；无「数据源对接」硬造行；入参一行一环节
- [ ] 每个 work 有需规 + 接口/字段清单；review 含「是否误用实现仓」= 否

---

## 变更记录

| 版本 | 日期 | 说明 |
|---|---|---|
| 0.1 | 2026-09-04 | 接口级；L31 金样；60 路并行试跑 → 已归档 |
| 0.2 | 2026-10-16 | 字段级；对外唯一交付；4A/L13；扩展列；双金样 L01+L13 |
| **0.2.1** | **2026-10-16** | 呈现层：功能点列名保留；算法环节+具体描述；无数据源对接；入参单行环节 |

# 算法库 · 接口向测试用例编排（B 线 S1～S5）

- **系统**：`SDWJSF/KJZTFWSFK` 科技专题服务算法库（**仅此系统**适用本 playbook）  
- **总索引**：[`algo-lib-playbook-index.md`](algo-lib-playbook-index.md)  
- **A 线对照**：`total-set/SDWJSF-KJZTFWSFK/fp-split-by-api-run/work/Lxx.md`（by-api 字段级；**禁止**用例与功能点一行一对）  
- **环境**：联调台 `http://111.198.38.90:50897/`（`lumen-ui-algo-apiview`，hash 路由；catalog 见 `as-built/catalog/SDWJSF-KJZTFWSFK.yaml`）  
- **与专题 B 线差异**：被测对象是调试台下拉框里的接口，不是调试台这个系统。  
- **用例类型**：只写 API 用例（`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-#####`）。不写登录、Token、401/424。  
- **2026-10-17 已落盘的 842 条作废**：那一轮主流程覆盖不到每个接口，预期大量是 4xx。重写前不要把 `科技专题服务算法库-API测试用例.xlsx` 当验收稿。  
- 专题/展示 S1 真源：`as-built/prompts/_case.md` + [`func-test-playbook-index.md`](func-test-playbook-index.md)。

> **本文件 §编写方法论** = 算法库用例 **思路、原则、粒度** 的唯一定义；§S1 是落地流程。编号/主表列仍以 `qa-test-case-spec.md` 为准；`_case.md` **只**继承文字红线（步骤/预期分工、禁止内部引用等），**不**继承「页面区块」方法论。

---

## 编写方法论与原则（算法库 B 线真源）

### 1. 测什么、不测什么

调试台（50897 / apiview）只是 **接口文档和调试页**。每个业务页的下拉框就是本页要测的接口清单。以产业链基础指标为例，清单是这 10 个名字，用例里必须能按原名搜到：

产业链列表、A1 产业市场规模、A2 产业企业规模、A3 产业机构规模、A4 产业投融资规模、A5 全球产业区域分布、A6 全国产业分布、A7 产业动态资讯、A8 深圳产业要素、A9 深圳产业分布。

这些名字就是 catalog 里该页 `endpoints[].title`。**功能点列填 title 原文**，不要改成「主流程-市场规模」这类场景名。

| 测 | 不测 |
|----|------|
| 下拉框里的每一个接口：文档给出的请求参数、请求示例、返回体字段 | 调试台登录、Token、TENANT-ID、401/424、菜单、下拉框能不能点开 |
| 正向：合法参数组合下，返回 body 与该接口文档一致 | 把「HTTP 200 / 4xx」当成预期结果的全部内容 |
| 反向：每个参数 1 条，预期是该参数的错误说明 | 为鉴权、空列表、A 线 `_empty`/`_fail` 再单开一套用例 |

**一句话**：一条用例 = 对 **下拉框中某一个接口** 的一次请求，核对文档里的返回 body 或该参数的错误信息。

### 2. 设计单元与三层 ID

| 层 | 算法库含义 | 本步 |
|----|------------|------|
| A 功能点 | by-api 一行：`endpoint_id` + `field_key` + 语义 | **只进** `coverage-fp.md`，不是用例编号 |
| **测试用例** | `ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-#####` | 本步产出 |
| 自动化脚本 | S2 的 HTTP/集合 id | S1 不写 |

**设计单元** = **下拉框里的一个接口**（`endpoint.title`）。每个接口都要有自己的正向用例；有几个参数就有几条反向。

- 无参接口：至少 **1 条正向**。  
- 有参接口：正向覆盖该接口文档里的参数组合；反向 **每个参数 1 条**，不按参数组合去乘反向用例。  
- 一条正向用例核对这份文档返回体里的字段，不按 A 线 `field_key` 拆成多条。

### 3. 与 A 线（by-api）的关系

| 原则 | 说明 |
|------|------|
| **接口清单以调试台下拉框为准** | 条数下限 = 接口数（每接口至少 1 条正向）。旧稿全库主流程只有约 58 条，低于接口数，不合格。 |
| **禁止一对一灌表** | 不为 A 线每个 `field_key` 机械复制一行用例。 |
| **文档状态不取消接口** | `status=unavailable` 的接口仍然在下拉框里（如 A3、A5、A7）。备注可注明文档标记未交付，用例仍按该接口的请求/返回说明来写，不改成「本轮不测 / 契约占位」。 |
| **写作用例的依据** | 该接口在 catalog 中的 `title`、`method`、`path`、`params`、`sampleRequest`、`sampleResponse`、`responseFields`。A 线矩阵只做覆盖对照，不代替接口文档。 |

### 4. 入参怎么覆盖

依据是该接口的 `params` 和 `sampleRequest`，不是登录态。

1. **正向尽量覆盖参数组合**：文档有几个可取的合法取值，就写成不同的正向用例。至少包括：文档 `sampleRequest` / `example` 的那一组；每个可选参数「传 / 不传」各一条（其余参数保持合法）；多个参数同时取文档给出的另一组合法值。无参接口只有 1 条正向。  
2. **反向每个参数 1 条就够**：只动这一个参数（缺省或非法），其它参数保持文档合法值。参数有 N 个，反向就是 N 条，不再做「非法 × 缺省」的组合，也不再写鉴权反向。  
3. **步骤**写 METHOD、path，以及这一次的参数取值（可引用附录组合 id）。不写「打开页面、点发送、登录」。

### 5. 预期结果写什么

预期结果首先是 **这份接口文档里的返回内容**，不是传输层状态码。

| 用例 | 预期里写什么 | 禁止 |
|------|----------------|------|
| **正向** | 返回 body 的结构，按 `sampleResponse` 与 `responseFields` 逐字段列出：字段名、类型、在 body 中的位置。文档示例里出现的字段都要出现在预期中 | 只写「HTTP 200」「code 属于成功集合」「401 或 424」 |
| **反向** | 这个参数错了时，返回 body 里的错误说明（`message` 或 `msg` 在说哪一个参数） | 只写「HTTP 4xx」「失败态」「code 非成功集合」 |

文档示例中的具体数值可以写进正向预期，并标明来自该接口 `sampleResponse`，用来说明返回长什么样。判定点是字段和结构与文档一致。

### 6. 功能项列

1. **主流程**（P0）：该接口的一条合法请求，预期是文档返回 body。每个接口至少一条，功能点列用下拉框原名。  
2. **备选**（P0/P1）：同一接口的其它合法参数组合，预期仍是该组合下的返回 body。  
3. **异常-入参**（P1）：某个参数一条。功能项写明参数名，例如 `异常-入参-缺chainId`。

不设「异常-鉴权」「异常-契约」「契约-不可用」「异常-空结果」这类功能项。空数据如果文档返回体本身就是空数组，写在该正向用例的预期里，不单独再造一条鉴权或 4xx 用例。

### 7. 用例粒度（API 版「一测一问」）

- **一条用例 = 一次验收问题**，通常对应 **一次 HTTP 调用**（或明确写清的连续重试同一调用）。  
- **测试内容**写这个接口名 + 这一组参数在验什么，例如：「A1 产业市场规模在 chainId=INB1701、statYear=2025 时返回文档中的市场规模字段」。  
- **页面列** = 调试台页面名（产业链基础指标）。**功能点列** = 下拉框原文（A1 产业市场规模）。  
- 正向预期按返回字段展开，可以超过 3 条；一条里不要同时写成功 body 和错误信息。

### 8. 编写顺序（单 catalog 页）

```text
抄下本页下拉框全部 title（与 catalog endpoints 对齐）
  → 每个接口：按 sampleRequest/params 列正向组合，按参数各写 1 条反向
  → 正向预期抄该接口 sampleResponse / responseFields；反向预期写该参数的错误说明
  → endpoint → 用例简表
  → 功能点 → 用例矩阵（对 Lxx.md）
  → 红线自检 + 统计
```

### 9. 与专题 `_case.md` 的分工

| 专题 B 线 | 算法库 B 线 |
|-----------|-------------|
| 真源 = 50892 页面区块 | 真源 = 下拉框接口的请求/返回文档 |
| 粒度 = 可见控件 × 动作 | 粒度 = endpoint × 入参场景 |
| 主册 FUNC | 主册 **仅 API** |
| USM / 用户故事为主 | `N/A-技术项` + bid 章节可选 |

---

## 编写细则（子 agent 必须遵守）

> 句式按本节。被测清单 = 该页 catalog `endpoints[]`，与调试台下拉框标题一致。

### A. 一条接口文档里用哪些字段

| 字段 | 写到用例的哪里 |
|------|----------------|
| `title` | **功能点列原文**（如 `A1 产业市场规模`） |
| `method` + `path` | 测试步骤 |
| `params` + `sampleRequest` | 正向组合与反向（每参数 1 条）的取值 |
| `sampleResponse` + `responseFields` | **正向预期**：返回 body 的字段、类型、结构；示例值标明来自 sampleResponse |
| `status` | 只放备注。`unavailable` 不取消该接口，仍按文档请求/返回来写 |

`viz`、登录、Token 不进用例。`sampleResponse` 里比 `responseFields` 多出来的字段（如列表样例里的 `cluster_name`）也写入正向预期，因为它们出现在这份接口的返回示例里。

### B. 一册文档骨架（顺序固定）

1. 文首元信息（系统码、catalog_page_id、A 线 Lxx、50897）  
2. **§0**：本页接口清单（title 列表）。不写登录步骤，不把 Token 当成测试项。
3. **§1 用例总表**（列与模板一致；API 编号）  
4. **附录 A 入参组合表**  
5. **附录 B 本页接口清单**（title、METHOD、path、参数名；title 与下拉框一致）  
6. 同目录 `coverage-fp.md`

### C. 单元格句式（风格统一）

**测试内容**（含下拉框原名 + 这一组参数）：

- ✅ `A1 产业市场规模在 chainId=INB1701、statYear=2025 时返回文档中的市场规模字段`  
- ❌ `产业链列表在有效鉴权下返回成功信封`  
- ❌ `测试各种情况`

**前置条件**：只写业务数据是否就绪，例如 `1、chainId 使用文档示例 INB1701`。不写 Token、不写「已登录」。

**测试步骤**（每步一个请求动作，≤60 字）：

```text
1.GET /innov/v1/industry/list（无查询参数）
```

```text
1.GET /innov/v1/industry/market-stats，查询参数取组合 MKT-01
```

- 禁止步骤出现：核对、检查、点击页面、看图表。  
- 参数值不在步骤里展开成长 JSON：写 **组合 id**，定义在附录 A。

**预期结果**：

- 正向 ✅ `1、返回 body 的 data 为数组；2、元素含文档示例字段 chain_id、chain_name（string），以及 sampleResponse 中的 cluster_name、map_status、description`  
- 反向 ✅ `1、返回 body 的 message 或 msg 说明缺少 chainId；2、不返回含 total_revenue 的成功结果`  
- ❌ `HTTP 状态为 401 或 424`、`HTTP 4xx`、`code 属于成功集合`

**功能项**只用：`主流程`、`备选-参数组合`、`异常-入参-缺chainId`、`异常-入参-非法chainId`。禁止 `异常-鉴权`、`契约-不可用`。

**备注** 固定片段（空格分隔即可）：

```text
endpoint_id=chain.basic.list catalog_page_id=chain.basic 组合=— 金样
```

**功能点列** = `title` 原文。产业链基础指标这一页，10 个 title 每一个都要在功能点列出现，并且至少挂 1 条主流程。

### D. 每个接口写多少条

| 接口 | 正向 | 反向 |
|------|------|------|
| 无 `params`（如产业链列表） | 1 条主流程，预期为该接口 sampleResponse 的字段 | 0 条。不要用登录失败充数 |
| 有 `params`（如 A1：chainId、statYear） | 文档示例全参 1 条；每个可选参数「不传」再 1 条；文档若给出多组合法 example，各组 1 条 | **每个参数 1 条**（缺省或非法二选一，不要两条都写，也不要两个参数一起打坏） |
| `status=unavailable`（如 A3、A5、A7） | 与上面相同，预期仍写该接口文档中的返回字段 | 与上面相同。备注注明文档标记未交付 |

不设「全页 4～8 条」上限。接口有 10 个，主流程就至少 10 条。旧稿用鉴权、契约占位把主流程压到低于接口数，按本节视为不合格。

### E. 入参组合表（附录 A 列）

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| MKT-01 | chain.basic.market-stats | chainId=INB1701（§0 试调有效值，可替换）；statYear=2025 | 主路径全参 |
| MKT-02 | chain.basic.market-stats | 不传 chainId；statYear=2025 | 缺必填 |
| MKT-03 | chain.basic.market-stats | chainId=__invalid__；statYear=2025 | 只破坏 chainId 这一个参数 |
| MKT-04 | chain.basic.market-stats | chainId=INB1701；statYear 非法 | 只破坏 statYear 这一个参数 |

MKT-03 与 MKT-04 不要并成一条。省略可选参数属于正向备选，不要和非法值写在同一条。

### F. 预期怎么写返回 body

正向按该接口 `sampleResponse` 逐字段写，例如产业链列表：

`1、data 为数组；2、元素包含 chain_id（string）、chain_name（string）；3、文档示例还包含 cluster_name、map_status、description，返回中应有这些字段`

反向按被破坏的那一个参数写错误说明，例如 A1 缺 chainId：

`1、返回 body 的 message 或 msg 指出 chainId 缺失或非法；2、不返回带 total_revenue 的成功数据`

禁止把「HTTP 401 / 424 / 4xx」「code 属于成功集合」当作预期的主体。页面、图表、表格行数不写。

### G. 正反例（克隆风格）

**反例（禁止）**：功能点写成「主流程-列表成功」而搜不到「A1 产业市场规模」；预期是 401/4xx；用一条登录用例代替 10 个接口的主流程。

**正例（A1 正向）**：

| 列 | 内容 |
|----|------|
| 功能项 | 主流程 |
| 功能点 | A1 产业市场规模 |
| 测试内容 | A1 产业市场规模按文档示例 chainId、statYear 查询 |
| 步骤 | 1.GET /innov/v1/industry/market-stats，参数取组合 MKT-01 |
| 预期 | 1、data 为数组；2、元素含文档返回字段 total_revenue（number）及 sampleResponse 中列出的其它字段 |
| 备注 | endpoint_id=chain.basic.market-stats |

**正例（A1 反向，只动 chainId）**：

| 列 | 内容 |
|----|------|
| 功能项 | 异常-入参-缺chainId |
| 功能点 | A1 产业市场规模 |
| 测试内容 | A1 产业市场规模不传 chainId |
| 步骤 | 1.GET /innov/v1/industry/market-stats，参数取组合 MKT-02 |
| 预期 | 1、返回 body 的 message 或 msg 说明 chainId 缺失或非法；2、不返回含 total_revenue 的成功结果 |
| 备注 | endpoint_id=chain.basic.market-stats 组合=MKT-02 |

### H. 覆盖矩阵写法

- 键：`L01 | chain.basic.list | chain_id | 算法输出-chain_id产业标识`  
- 多条 field 挂 **同一** API 编号：每个 field 一行，对应用例列相同编号。  
- `规则来源` 列抄 A 线「规则来源」即可。  
- 状态只用：已覆盖 / 部分覆盖 / 未覆盖。不用「契约占位」把接口标成不测。

### I. 交卷前自检（子 agent 回复必须附计数）

| 检查 | 通过标准 |
|------|----------|
| 对象 | 本页每个 `title` 都能在功能点列搜到，且至少 1 条主流程 |
| 鉴权 | 0 条登录 / Token / 401 / 424 用例 |
| 正向 | 有参接口的文档示例组合、可选参数省略都有正向用例；预期写出 sampleResponse 字段 |
| 反向 | 每个参数恰好 1 条；预期是该参数的错误说明，不是「HTTP 4xx」 |
| 不可用 | unavailable 接口仍有按文档返回体写的主流程，不是「契约占位」 |
| 编号 | 已回写 code-registry |

---

## 角色分工

| 角色 | 做什么 | 不做什么 |
|------|--------|----------|
| **人** | 金样 catalog 页签收（建议首册 `chain.basic`）；S4 交付签字 | — |
| **父 agent** | 按 catalog 页派子 agent；验收覆盖矩阵与红线自检；维护取号与 `coverage-fp.md` 汇总 | 不代写整册 API 表；不改 A 线 `work/Lxx.md` |
| **子 agent** | 只写本 `catalog_page_id` 对应册 + 本页 `coverage-fp.md` | 不读算法实现仓；不按 A 线每个 `field_key` 各写一条用例 |

---

## 共用规范（不重复造规）

| 必读 | 用途 |
|------|------|
| [`qa-test-case-spec.md`](../qa-test-case-spec.md) | 编号、主表列、§5.4 内容红线、§5.4.1 粒度 |
| [`templates/test-case-template.md`](../templates/test-case-template.md) | 表头；算法库主册测试类型用 **API** |
| [`code-registry.yaml`](code-registry.yaml) | `SDWJSF/KJZTFWSFK` 下 **仅 API** 取号（`next_seq.API`） |
| `as-built/prompts/_case.md` | **仅**文字红线 + 交卷自检；方法论以 **本文件 §编写方法论** 为准 |
| `fp-split-by-api-run/_catalog-snapshot.md` | 与联调台 catalog 一致的 endpoint / params / responseFields 对照 |

**用户故事**：接口用例扩展列 `用户故事编号` 可填 `N/A-技术项`（见 spec §7.1）。

---

## S1 · 用例编写（API 主册）

> 思路与原则见 **§编写方法论**；本节为产物路径与操作清单。

### 成熟度与产物

| 项 | 内容 |
|----|------|
| 状态 | ✅ 可开（与 A 线 F3 并行；不必等 by-api 合表） |
| 目录 | `test-cases/SDWJSF-KJZTFWSFK/{模块层-中文}/{catalog页标题}/` |
| 主文件 | `API-{页短名}-用例.md`（一 catalog 页一册；**唯一**用例类型） |
| 覆盖 | 同目录 `coverage-fp.md`（本页）；父控可另维护系统级 `coverage/SDWJSF-KJZTFWSFK/` 汇总（待建） |

### 调试台登录（不是用例）

登录、Token、租户头是调试台自己的辅助能力，**不写入任何用例**，也不作为前置条件的验收点。执行人自己持有调用条件即可。

目录命名与专题相同：**`英文缩写-中文名称`**。

- `{模块层}` = catalog `modules[].id` + 中文（例：`chain.basic` 挂在 **`basic-基础指标`**，不是 `chain-产业链分析`）。  
- `{页目录}` = `entry_id` 去点转大写缩写 + `entries[].title`（例：`CHAINBASIC-产业链基础指标`）。  
- 系统级说明见 `test-cases/SDWJSF-KJZTFWSFK/README.md`。

### 1. 盘点（真源 = 调试台源码里的 catalog，不打开页面）

50897 页面上的下拉框和接口说明，就是这份源码渲染出来的，没有第二份清单：

- 下拉标题：`repos/lumen-ui-algo-apiview/src/views/AlgoWorkspaceView.vue` 的 `endpointOptions.label` = `endpoint.title`
- 参数表、响应字段、请求示例、响应示例：`src/components/algo/ApiInfoPanel.vue` 直接绑定 `params`、`responseFields`、`sampleRequest`、`sampleResponse`

因此编写时只读：

`repos/lumen-ui-algo-apiview/src/catalog/{chain,entan,svc,policy,innov,comp}.json`

页与模块的中文名、目录挂载用 `as-built/catalog/SDWJSF-KJZTFWSFK.yaml`。

1. 按 `catalog_page_id` 取出该页全部 `endpoints`。  
2. 每个 endpoint 抄 `title`、`method`、`path`、`params`、`sampleRequest`、`sampleResponse`、`responseFields`、`status`。  
3. **不要**开浏览器、不要用浏览器 MCP、不要为写用例去 curl 登录或打 50897。页面和现场试调都不增加文档信息。  
4. `status=unavailable` 仍按文档请求/返回写用例，备注注明未交付。  
5. 禁止读 `lumen-algo-py`、`demo-algo-*` 把实现当接口文档。

### 2. 按方法论落表

- 场景类、入参组合、出参分层、粒度：一律按 **§编写方法论 §4～§7**。  
- `路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=`、组合 id（如有）。

### 3. A 线覆盖矩阵（本页完成后）

键（复合）：`Lxx | endpoint_id | field_key | 功能点中文`（来自 `fp-split-by-api-run/work/Lxx.md`，Lxx 与六级需规对应）。

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| … | API-xxxxx | 已覆盖 / 未覆盖 / 部分覆盖 | 一条用例可挂多 field |

- A 线未完成六级：状态可先 **待 A 线合表核对**，已写 endpoint 用例仍有效。  
- B 线独有（联调台有、A 未列）：反表记 `无对应功能点`。

### 4. 金样（首册建议）

| 项 | 内容 |
|----|------|
| 页 | `chain.basic`（module **basic** · path `#/chain/basic` · A 线 L01） |
| 路径 | `test-cases/SDWJSF-KJZTFWSFK/basic-基础指标/CHAINBASIC-产业链基础指标/` |
| 册 | `API-产业链基础指标-用例.md`（骨架已建，待填用例行） |
| 重写标准 | 10 个下拉标题各至少 1 条主流程；A1 这类有参接口另有每参数 1 条反向；预期是返回 body 或该参数的错误说明 |

### 5. S1 交卷清单

1. 用例 md + `code-registry` 已回写  
2. endpoint → 用例简表  
3. 本页 **功能点 → 用例** 矩阵与计数  
4. 红线自检（同 `_case.md` §4 第 8 条，含粒度分布）  
5. 无 yaml / runs（S1 不写脚本）

---

## S2 · 脚本编写

| 项 | 内容 |
|----|------|
| 成熟度 | 🟡 待建（无专题式 Playwright 金样） |
| 方向 | HTTP 集合（`qa/tools/postman/`）或联调台驱动脚本；**不**默认 Playwright 点 UI |
| 必读（暂定） | `as-built/prompts/_script.md` 三角色纪律；`schema.md` 仅采纳 **结果落盘/禁止充绿** 等与 UI 无关条款 |
| 产物 | `as-built/scripts/SDWJSF-KJZTFWSFK/{module}/{page}/`（待首建） |
| 映射 | 用例「自动化用例ID」回填脚本 id；缺口工具 `gap-func-vs-scripts.py` 需扩展系统码后使用 |

父控开 S2 前：在总索引确认 playbook 本节已更新成熟度。

---

## S3 · 脚本执行

| 项 | 内容 |
|----|------|
| 成熟度 | 🟡 待建 |
| 环境 | `50897`；波次目录建议 `as-built/runs/{日}-50897-{wave}/`（与专题 50892 区分） |
| 编排 | 待 S2 就绪后对齐 `script-batch-run-playbook.md` 精神（串行、Excel 收口、禁止改脚本充绿） |

---

## S4 · 用例交付合并

| 项 | 内容 |
|----|------|
| 成熟度 | 🟡 待编写（`delivery/SDWJSF-KJZTFWSFK/`） |
| 必读 | [`case-delivery-playbook.md`](case-delivery-playbook.md) · `_submit.md` · `delivery/README.md` |
| A 线输入 | by-api 合表 `…功能点拆分-by-api_v1.xlsx`（或豁免前用 `work/Lxx` 矩阵） |
| 注意 | API 用例投影到总集时类型码 **API**；未覆盖功能点不投影 |

专题一键脚本 `_gen_zt_delivery_func_ab_merge.py` **不**直接适用于算法库；合表脚本待单建。

---

## S5 · 可交付测试记录

| 项 | 内容 |
|----|------|
| 成熟度 | 🟡 骨架共用 |
| 必读 | [`record-delivery-playbook.md`](record-delivery-playbook.md) |

证据：接口 JSON 片段 / 联调台截图均可；文件名仍建议 `{用例编号}-Pass|Fail-{序号}.png`。

---

## 长任务返工（2026-10-17 第二轮）

> 第一轮 89 页、`API-00001`～`00888`（含空号 `00024`～`00050`、`00212`～`00230`）整批作废。原因：测了调试台登录和 4xx，没有按接口文档写返回 body，主流程少于接口数。父控提示词只引用本节。

### 文档从哪读

只读 `lumen-ui-algo-apiview/src/catalog/*.json`（见 §S1 盘点）。禁止浏览器 MCP、Playwright、打开 `http://111.198.38.90:50897/`、为写用例登录或 curl。

### 返工动作

先停掉仍在写旧口径的会话。然后 **89 个在用 catalog 页全部重写**，覆盖原 `API-*-用例.md` 与 `coverage-fp.md`。旧行里的编号作废，不复用。

| 旧产物 | 返工 |
|--------|------|
| `API-00001`～`00888` 及两段空号 | 作废，号段冻结 |
| 各页已有用例册 | 整册覆盖为新编号 |
| `科技专题服务算法库-API测试用例.xlsx` | 旧口径，本轮不更新；册写完后再按客户模板 6 号重合 |
| `run-log.md` 批 1～22 的 89/89 | 只代表第一轮，不算本轮完成 |

- 新号从 `code-registry` 的 `next_seq.API` 起（第一轮结束后为 **889**）。不回填 `00001`～`00888`。每批结束回写 `next_seq` 与 `modules`。  
- 进度追加到 `run-log.md`，表头注明「第二轮」。不要把第一轮已完成页跳过。

### 退出（禁止无限循环）

- 同一页验收不合格：只返工 **1** 次；仍不合格 → `跳过-验收失败`，释放未用编号。  
- 同一页子任务报错、超时、无产物：只重派 **1** 次；仍失败 → `跳过-执行失败`。  
- 契约缺失或 yaml/JSON 对不上：尝试 **1** 次仍对不上 → `跳过-疑难`。  
- 连续 **2** 批（最多 8 页）全部跳过，或真源缺失 / `code-registry` 写坏 → **停机**，输出完成页与跳过页，不再派下一批。  
- 跳过页写入 `run-log.md` 后，本会话不再打开。  
- 待写页清空（完成或已跳过都算出列）→ 输出总表后停止。

## 子 agent 细则（S1 · 单 catalog 页）

1. 只写本任务 `catalog_page_id` 对应 **一个** `API-*-用例.md` + 本目录 `coverage-fp.md`。  
2. 取号类型 **仅 API**，只用父控给出的新号段（不得复用 `00001`～`00888`）。不写登录、Token、401/424。  
3. 接口文档只读 `lumen-ui-algo-apiview/src/catalog/*.json`。禁止读 `lumen-algo-py` / `demo-algo-*`，禁止按 `field_key` 一行一用例。  
4. 禁止改 A 线 `work`、禁止改业务仓、禁止改其它页。禁止浏览器、Playwright、为写用例去请求 50897。  
5. 写不下去就回报卡点并停止，不换页、不空转。

---

## 维护

- B 线阶段变更：**先改本文件**，再改 `algo-lib-playbook-index.md` §1 B 线表一行。  
- 不在 `func-test-playbook-index.md` 复制算法库长 Kickoff；该索引仅保留就绪门 + 跳转。  
- S2/S3 首版落地后更新本文件成熟度与产物路径。

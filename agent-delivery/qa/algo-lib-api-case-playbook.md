# 算法库 · 接口向测试用例编排（B 线 S1～S5）

- **系统**：`SDWJSF/KJZTFWSFK` 科技专题服务算法库（**仅此系统**适用本 playbook）  
- **总索引**：[`algo-lib-playbook-index.md`](algo-lib-playbook-index.md)  
- **A 线对照**：`total-set/SDWJSF-KJZTFWSFK/fp-split-by-api-run/work/Lxx.md`（by-api 字段级；**禁止**用例与功能点一行一对）  
- **环境**：联调台 `https://edu.itic-sci.com/dma/algovwz/`（`lumen-ui-algo-apiview`）。**带 path 前缀** `/dma/algovwz/`，末尾 `/` 必留；hash 路由完整页 = `{base_url}#/{path}`（例 `…/dma/algovwz/#/chain/basic`）。禁止写成站点根 `/#/…`、禁止丢掉 `/dma/algovwz`、禁止再写旧内网 `10.50.69.111:30897` 或 `111.198.38.90:50897`。catalog 见 `as-built/catalog/SDWJSF-KJZTFWSFK.yaml`。  
- **用例类型**：功能用例 `ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-#####`。登录只写在前置条件，不单列用例，不写 Token、401/424。  
- **2026-10-19 内部评审口径（第三轮，后续加用例和重跑都按此）**：按联调台页面操作写步骤；模块列用需规三至六级；编号改 FUNC 并从 `00001` 重排；去掉自行添加的 `A1`/`A2`；测试内容用「验证…功能，检查…」。条数仍按接口的参数组合，不合 A 线。  
- **已落盘的 API 号全部作废**：`API-00001`～`00888` 与第二轮 `API-00889`～`02210` 都不复用。工作区 Excel 与 `delivery/SDWJSF-KJZTFWSFK/` 里那份 1322 条是评审前过渡稿，第三轮册写完后再换。  
- 专题/展示 S1 真源：`as-built/prompts/_case.md` + [`func-test-playbook-index.md`](func-test-playbook-index.md)。

> **本文件 §编写方法论** = 算法库用例 **思路、原则、粒度** 的唯一定义；§S1 是落地流程。编号/主表列仍以 `qa-test-case-spec.md` 为准；`_case.md` **只**继承文字红线（**红线 3：步骤只写操作、校验全进预期**；禁止内部引用等），**不**继承「页面区块」方法论。合表无附录：参数赋值必须写在步骤/前置里（见 §4、§S4）。

---

## 编写方法论与原则（算法库 B 线真源）

### 1. 测什么、不测什么

在联调台 `https://edu.itic-sci.com/dma/algovwz/` 上按页面操作测。每个业务页的接口下拉框是本页接口清单。以产业链基础指标为例，清单用 catalog 标题，**不要自行加上 A1、A2**：

产业链列表、产业市场规模、产业企业规模、产业机构规模、产业投融资规模、全球产业区域分布、全国产业分布、产业动态资讯、深圳产业要素、深圳产业分布。

这些名字就是该页 `endpoints[].title`。若标题以 `A` 加数字再加空格开头（编写时加过、文档里没有），功能点和正文里都去掉这个前缀。文档标题里本来就有的字（如 `WAVE1`）保留。

| 测 | 不测 |
|----|------|
| 打开对应页面，在下拉框选中该接口，按一组参数点调用，在返回面板核对文档中的字段或该参数的错误说明 | 把登录、Token、401/424 写成独立用例；把「下拉框能不能点开」单独成条 |
| 正向：合法参数组合下，返回面板与该接口文档一致 | 把「HTTP 200 / 4xx」当成预期结果的全部内容 |
| 反向：每个参数 1 条，预期是该参数的错误说明 | 为鉴权、空列表、A 线 `_empty`/`_fail` 再单开一套用例 |

**一句话**：一条用例 = 在该页面上对 **下拉框中某一个接口** 做一次操作，核对返回面板里的文档字段或该参数的错误信息。

### 2. 设计单元与三层 ID

| 层 | 算法库含义 | 本步 |
|----|------------|------|
| A 功能点 | by-api 一行：`endpoint_id` + `field_key` + 语义 | **只进** `coverage-fp.md`，不是用例编号 |
| **测试用例** | `ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-#####` | 本步产出 |
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
| **文档状态不取消接口** | `status=unavailable` 的接口仍然在下拉框里（如产业机构规模、全球产业区域分布、产业动态资讯）。备注可注明文档标记未交付，用例仍按该接口的请求/返回说明来写，不改成「本轮不测 / 契约占位」。 |
| **写作用例的依据** | 该接口在 catalog 中的 `title`、`method`、`path`、`params`、`sampleRequest`、`sampleResponse`、`responseFields`。A 线矩阵只做覆盖对照，不代替接口文档。 |

### 4. 入参怎么覆盖

依据是该接口的 `params` 和 `sampleRequest`，不是登录态。

1. **正向尽量覆盖参数组合**：文档有几个可取的合法取值，就写成不同的正向用例。至少包括：文档 `sampleRequest` / `example` 的那一组；每个可选参数「传 / 不传」各一条（其余参数保持合法）；多个参数同时取文档给出的另一组合法值。无参接口只有 1 条正向。  
2. **反向每个参数 1 条就够**：只动这一个参数（缺省或非法），其它参数保持文档合法值。参数有 N 个，反向就是 N 条，不再做「非法 × 缺省」的组合，也不再写鉴权反向。  
3. **步骤写页面操作**，不写 `GET`/`POST` 加 path。顺序固定：侧栏进入本页 → 下拉选择该接口 → **在步骤里写出具体参数赋值** → 点击调用。登录放在前置条件。path 只留在附录 B 和备注，供对照文档。  
   - **合表铁律**：交付 Excel **不含附录**。步骤禁止写「按附录组合 Xxx 填写参数」；必须写成 `填写 chainId=INB1701、statYear=2025，点击调用` 这种可独立执行的句子。附录 A 只是编写时的草稿表，合进主表后测试人员不得再去翻附录。  
   - **步骤 / 预期分工**（继承 `_case.md` 红线 3）：步骤只写人对系统的操作（进入 / 切换 / 选择 / 填写 / 点击）；**禁止**在步骤里写「核对 / 确认 / 检查 / 校验 / 查看是否 / 比对」。看结果一律进预期结果。清单用例也不例外。

### 5. 预期结果写什么

预期结果首先是 **这份接口文档里的返回内容**，不是传输层状态码。

| 用例 | 预期里写什么 | 禁止 |
|------|----------------|------|
| **正向** | 返回 body 的结构，按 `sampleResponse` 与 `responseFields` 逐字段列出：字段名、类型、在 body 中的位置。文档示例里出现的字段都要出现在预期中 | 只写「HTTP 200」「code 属于成功集合」「401 或 424」 |
| **反向** | 这个参数错了时，返回 body 里的错误说明（`message` 或 `msg` 在说哪一个参数） | 只写「HTTP 4xx」「失败态」「code 非成功集合」 |

文档示例中的具体数值可以写进正向预期，并标明来自该接口 `sampleResponse`，用来说明返回长什么样。判定点是字段和结构与文档一致。

### 6. 模块列与场景类型（2026-10-19 定）

交付主表前六列按需规填，不再用联调台菜单名，也不再把「主流程 / 备选 / 异常」放进功能项。

| 列 | 填什么 |
|----|--------|
| 功能模块 | 三级，全库固定 **算法工具库** |
| 子功能模块 | 四级，全库固定 **科技专题服务算法库** |
| 功能项 | 五级。来自 `fp-split-by-api-run/01-task-list.md`，经 `_l6-to-catalog-map.yaml` 挂到本页 |
| 子功能项 | 六级。同上，用六级全名，例如「产业链基础指标模型构建」 |
| 页面 | 联调台页面标题（catalog 页 title） |
| 功能点 | 下拉接口的 `endpoints[].title`，去掉自行添加的 `A1`、`A2` |

一页只挂一个六级时，本页用例都用这一对五级/六级。一页挂多个六级时（如 `chain.panorama` 上的 L05 与 L06），按该 endpoint 在对应 `work/Lxx.md` 里的归属填写，禁止整页套同一个六级。`catalog_skip` 或 map 里没有六级的页（创新监测、工程增强等）仍要写用例，功能项和子功能项都写 **待挂需规**。

场景类型改记在备注，不占功能项：`场景=主流程`、`场景=备选-参数组合`、`场景=异常-入参-缺chainId`、`场景=异常-入参-非法chainId`、`场景=接口信息-清单`、`场景=算法测试-清单`。不设「异常-鉴权」「异常-契约」「契约-不可用」「异常-空结果」。每个接口至少一条主流程。每页另有 §6.1 的 2 条清单用例。

### 6.1 页面清单用例（每页固定 2 条）

联调台进入页面后有两个 tab：「接口信息」「算法测试」。两个 tab 共用「当前接口」下拉，选项都是该页 `endpoints[]`。页头还有「N 个接口」。接口信息 tab 的概览展示 method 和 path；算法测试 tab 的调用区同样展示 `method path`。

| 条 | 功能点 | 测什么（全部写进**预期**） | 不测什么 |
|----|--------|--------|----------|
| 接口信息-清单 | 接口信息 | 页头数量 = 下拉项数 = `endpoints.length`；下拉名称与各 `title` 一致；默认项的概览标题、method、path 对应该接口；再切换到另一项后，这三项变为后一个接口，参数表和示例区有内容刷新 | 不逐字段核对 params、responseFields、sampleResponse |
| 算法测试-清单 | 算法测试 | 下拉数量和名称与接口信息 tab、catalog 一致；切换接口后，下拉名称以及调用区的 method、path 变为所选接口，请求区正常刷新 | 不点击调用，不核对接返回字段 |

**清单步骤只写操作**，判定写预期。正例：

```text
步骤：1.侧栏进入「基础指标」→「产业链基础指标」；2.停留在「接口信息」tab；3.接口下拉切换到「产业市场规模」
预期：1、页头接口数量为 10，与下拉项数一致；2、下拉名称与 §0 / catalog title 一致；3、默认项概览 method/path 对应该接口；4、切换后概览变为产业市场规模的 GET 与对应 path，参数表与示例区已刷新
```

禁止：`2.确认页头接口数量为 10；3.查看默认选中…一致；4.…确认概览变为…`（把校验动词塞进步骤）。

只有 1 个接口时不切换，预期写明下拉仅此 1 项。名称同样去掉自行添加的 `A数字 ` 前缀。模块列仍用该页的五级/六级（无六级则「待挂需规」）。测试内容句式不变，例如：`验证产业链基础指标的接口信息功能，检查接口数量、名称和 URL 与文档一致，且切换接口后信息正常刷新`。

### 7. 用例粒度

- **一条用例 = 一次页面操作**（选中一个接口、填一组参数、点一次调用）。  
- **测试内容**必须写成完整句：「验证{功能点}功能，检查{本条要确认的事}」。  
  - 正向例：`验证产业市场规模功能，检查填写 chainId=INB1701、statYear=2025 后返回总营收等规模字段`  
  - 反向例：`验证产业市场规模功能，检查不传 chainId 时返回指出该参数的错误说明`  
- **页面列** = 联调台页面名（产业链基础指标）。**功能点列** = 下拉标题（产业市场规模），不加 `A1`。  
- 正向预期按返回字段展开，可以超过 3 条；一条里不要同时写成功 body 和错误信息。

### 8. 编写顺序（单 catalog 页）

```text
抄下本页下拉框全部 title（与 catalog endpoints 对齐，去掉自行添加的 A 序号）
  → 按 map 填五级/六级；无六级则两列写待挂需规
  → 每个接口：按 sampleRequest/params 列正向组合，按参数各写 1 条反向
  → 步骤写成联调台上的页面操作；测试内容用「验证…功能，检查…」
  → 正向预期抄该接口 sampleResponse / responseFields；反向预期写该参数的错误说明
  → endpoint → 用例简表
  → 功能点 → 用例矩阵（对 Lxx.md）
  → 红线自检 + 统计
```

### 9. 与专题 `_case.md` 的分工

| 专题 B 线 | 算法库 B 线 |
|-----------|-------------|
| 真源 = 专题业务页区块 | 真源 = 联调台页面上的下拉接口；请求/返回仍以 catalog 文档为准 |
| 粒度 = 可见控件 × 动作 | 粒度 = 页面上的一次调用（一个接口 × 一组参数） |
| 主册 FUNC | 主册 **FUNC**（2026-10-19 起；旧 API 号作废） |
| USM / 用户故事为主 | `N/A-技术项` + bid 章节可选 |

---

## 编写细则（子 agent 必须遵守）

> 句式按本节。被测清单 = 该页 catalog `endpoints[]`，与调试台下拉框标题一致。

### A. 一条接口文档里用哪些字段

| 字段 | 写到用例的哪里 |
|------|----------------|
| `title` | **功能点列**（如 `产业市场规模`）。去掉自行添加的 `A数字 ` 前缀 |
| `method` + `path` | 附录 B 与备注。测试步骤写页面操作，不写 METHOD |
| `params` + `sampleRequest` | 正向组合与反向（每参数 1 条）的取值 |
| `sampleResponse` + `responseFields` | **正向预期**：返回 body 的字段、类型、结构；示例值标明来自 sampleResponse |
| `status` | 只放备注。`unavailable` 不取消该接口，仍按文档请求/返回来写 |

`viz`、登录、Token 不进用例。`sampleResponse` 里比 `responseFields` 多出来的字段（如列表样例里的 `cluster_name`）也写入正向预期，因为它们出现在这份接口的返回示例里。

### B. 一册文档骨架（顺序固定）

1. 文首元信息（系统码、catalog_page_id、A 线 Lxx、联调台 `https://edu.itic-sci.com/dma/algovwz/`）  
2. **§0**：本页接口清单（title 列表，无自行添加的 A 序号）。登录不单列用例。
3. **§1 用例总表**（列与模板一致；FUNC 编号）  
4. **附录 A 入参组合表**  
5. **附录 B 本页接口清单**（title、METHOD、path、参数名；title 与下拉框一致）  
6. 同目录 `coverage-fp.md`

### C. 单元格句式（风格统一）

**测试内容**（必须同时有「验证」和「检查」）：

- ✅ `验证产业市场规模功能，检查填写 chainId=INB1701、statYear=2025 后返回总营收等规模字段`  
- ❌ `A1 产业市场规模按文档示例 chainId、statYear 查询`  
- ❌ `验证产业市场规模功能，检查按文档示例 chainId、statYear 查询后返回…`（「文档示例」不进测试内容 / 前置 / 步骤）  
- ❌ `产业链列表在有效鉴权下返回成功信封`  
- ❌ `测试各种情况`

**前置条件**：`1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、chainId=INB1701`。取值可来自 catalog `sampleRequest`，但正文只写赋值，**禁止**「使用文档示例 Xxx」。不写 Token，不把登录写成测试步骤。

**测试步骤**（页面操作，每步一个动作）：

```text
1.侧栏进入「基础指标」→「产业链基础指标」
2.接口下拉选择「产业链列表」
3.不填查询参数，点击调用
```

```text
1.侧栏进入「基础指标」→「产业链基础指标」
2.接口下拉选择「产业市场规模」
3.填写 chainId=INB1701、statYear=2025，点击调用
```

- 禁止步骤写 `GET`/`POST`、path、401。核对字段写在预期结果，不写在步骤里。  
- 禁止步骤写「按附录组合 … 填写参数」。参数赋值必须出现在本条步骤（或前置条件）里；附录 A 可选保留作编写对照，合表不带附录。  
- 长对象可写成 `填写 enterprise_codes=["A","B"]，点击调用`，不要只引用组合 id。

**预期结果**：

- 正向 ✅ `1、返回 body 的 data 为数组；2、元素含文档示例字段 chain_id、chain_name（string），以及 sampleResponse 中的 cluster_name、map_status、description`  
- 反向 ✅ `1、返回 body 的 message 或 msg 说明缺少 chainId；2、不返回含 total_revenue 的成功结果`  
- ❌ `HTTP 状态为 401 或 424`、`HTTP 4xx`、`code 属于成功集合`

**功能项**只写五级需规名，或「待挂需规」。场景类型放备注 `场景=`，禁止再把主流程/异常写进功能项。禁止 `异常-鉴权`、`契约-不可用`。

**备注** 固定片段（空格分隔即可）：

```text
endpoint_id=chain.basic.list catalog_page_id=chain.basic 组合=— 金样
```

**功能点列** = `title` 原文。产业链基础指标这一页，10 个 title 每一个都要在功能点列出现，并且至少挂 1 条主流程。

### D. 每个接口写多少条

| 接口 | 正向 | 反向 |
|------|------|------|
| 无 `params`（如产业链列表） | 1 条主流程，预期为该接口 sampleResponse 的字段 | 0 条。不要用登录失败充数 |
| 有 `params`（如产业市场规模：chainId、statYear） | 文档示例全参 1 条；每个可选参数「不传」再 1 条；文档若给出多组合法 example，各组 1 条 | **每个参数 1 条**（缺省或非法二选一，不要两条都写，也不要两个参数一起打坏） |
| `status=unavailable`（如产业机构规模、全球产业区域分布、产业动态资讯） | 与上面相同，预期仍写该接口文档中的返回字段 | 与上面相同。备注注明文档标记未交付 |

不设「全页 4～8 条」上限。接口有 10 个，主流程就至少 10 条。旧稿用鉴权、契约占位把主流程压到低于接口数，按本节视为不合格。

### E. 入参组合表（附录 A · 可选草稿）

附录 A 只供编写时对照号段，**不是**交付物。每一行的「参数赋值」必须同时写进该条用例的步骤（或前置）。合表 / Excel **不**附带附录。

| 组合 id | endpoint_id | 参数赋值（同步进步骤） | 意图 |
|---------|-------------|------------------------|------|
| MKT-01 | chain.basic.market-stats | chainId=INB1701；statYear=2025 | 主路径全参 |
| MKT-02 | chain.basic.market-stats | 不传 chainId；statYear=2025 | 缺必填 |
| MKT-03 | chain.basic.market-stats | chainId=__invalid__；statYear=2025 | 只破坏 chainId 这一个参数 |
| MKT-04 | chain.basic.market-stats | chainId=INB1701；statYear 非法 | 只破坏 statYear 这一个参数 |

MKT-03 与 MKT-04 不要并成一条。省略可选参数属于正向备选，不要和非法值写在同一条。

### F. 预期怎么写返回 body

正向按该接口 `sampleResponse` 逐字段写，例如产业链列表：

`1、data 为数组；2、元素包含 chain_id（string）、chain_name（string）；3、文档示例还包含 cluster_name、map_status、description，返回中应有这些字段`

反向按被破坏的那一个参数写错误说明，例如产业市场规模缺 chainId：

`1、返回 body 的 message 或 msg 指出 chainId 缺失或非法；2、不返回带 total_revenue 的成功数据`

禁止把「HTTP 401 / 424 / 4xx」「code 属于成功集合」当作预期的主体。页面、图表、表格行数不写。

### G. 正反例（克隆风格）

**反例（禁止）**：功能点写成「主流程-列表成功」或「A1 产业市场规模」；步骤是 `GET /path`；预期是 401/4xx；用一条登录用例代替各接口的主流程；功能项填菜单名而不是五级需规。

**正例（产业市场规模 · 正向）**：

| 列 | 内容 |
|----|------|
| 功能模块 | 算法工具库 |
| 子功能模块 | 科技专题服务算法库 |
| 功能项 | 基础指标分析模型 |
| 子功能项 | 产业链基础指标模型构建 |
| 页面 | 产业链基础指标 |
| 功能点 | 产业市场规模 |
| 测试内容 | 验证产业市场规模功能，检查填写 chainId=INB1701、statYear=2025 后返回总营收等规模字段 |
| 前置条件 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ |
| 步骤 | 1.侧栏进入「基础指标」→「产业链基础指标」；2.接口下拉选择「产业市场规模」；3.填写 chainId=INB1701、statYear=2025，点击调用 |
| 预期 | 1、返回面板中 data 为数组；2、元素含文档返回字段 total_revenue（number）及 sampleResponse 中列出的其它字段 |
| 备注 | endpoint_id=chain.basic.market-stats 场景=主流程 组合=MKT-01 |

**正例（产业市场规模 · 反向，只动 chainId）**：

| 列 | 内容 |
|----|------|
| 功能项 | 基础指标分析模型 |
| 子功能项 | 产业链基础指标模型构建 |
| 功能点 | 产业市场规模 |
| 测试内容 | 验证产业市场规模功能，检查不传 chainId 时返回指出该参数的错误说明 |
| 步骤 | 1.侧栏进入「基础指标」→「产业链基础指标」；2.接口下拉选择「产业市场规模」；3.不传 chainId，填写 statYear=2025，点击调用 |
| 预期 | 1、返回面板的 message 或 msg 说明 chainId 缺失或非法；2、不返回含 total_revenue 的成功结果 |
| 备注 | endpoint_id=chain.basic.market-stats 场景=异常-入参-缺chainId 组合=MKT-02 |

### H. 覆盖矩阵写法

- 键：`L01 | chain.basic.list | chain_id | 算法输出-chain_id产业标识`  
- 多条 field 挂 **同一** API 编号：每个 field 一行，对应用例列相同编号。  
- `规则来源` 列抄 A 线「规则来源」即可。  
- 状态只用：已覆盖 / 部分覆盖 / 未覆盖。不用「契约占位」把接口标成不测。

### I. 交卷前自检（子 agent 回复必须附计数）

| 检查 | 通过标准 |
|------|----------|
| 对象 | 本页每个 `title` 都能在功能点列搜到（无自行添加的 A 序号），且至少 1 条 `场景=主流程` |
| 步骤 | 每条都是联调台上的侧栏、下拉、填参、点击调用；0 条 `GET`/`POST` 步骤 |
| 模块列 | 功能模块=算法工具库；子功能模块=科技专题服务算法库；功能项/子功能项=五级/六级，或都是「待挂需规」 |
| 测试内容 | 每条都含「验证」和「检查」 |
| 鉴权 | 0 条登录 / Token / 401 / 424 用例；登录只出现在前置条件 |
| 正向 | 有参接口的文档示例组合、可选参数省略都有正向用例；预期写出 sampleResponse 字段 |
| 反向 | 每个参数恰好 1 条；预期是该参数的错误说明，不是「HTTP 4xx」 |
| 不可用 | unavailable 接口仍有按文档返回体写的主流程，不是「契约占位」 |
| 清单 | 本页恰好 2 条：`场景=接口信息-清单`、`场景=算法测试-清单`；只核对数量、名称、method、path 和切换后刷新 |
| 编号 | 只用父控给出的 FUNC 闭区间；不写 API 号 |

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
| [`templates/test-case-template.md`](../templates/test-case-template.md) | 表头；算法库主册测试类型用 **FUNC**（2026-10-19 起） |
| [`code-registry.yaml`](code-registry.yaml) | `SDWJSF/KJZTFWSFK` 第三轮用 **`next_seq.FUNC`**（当前为 1，从 `FUNC-00001` 起）。`next_seq.API=2211` 只记录已作废的 API 流水，不要再取 API 号 |
| `as-built/prompts/_case.md` | **仅**文字红线 + 交卷自检；方法论以 **本文件 §编写方法论** 为准 |
| `fp-split-by-api-run/_catalog-snapshot.md` | 与联调台 catalog 一致的 endpoint / params / responseFields 对照 |

**用户故事**：接口用例扩展列 `用户故事编号` 可填 `N/A-技术项`（见 spec §7.1）。

---

## S1 · 用例编写（FUNC 主册）

> 思路与原则见 **§编写方法论**；本节为产物路径与操作清单。

### 成熟度与产物

| 项 | 内容 |
|----|------|
| 状态 | ✅ 可开（与 A 线 F3 并行；不必等 by-api 合表） |
| 目录 | `test-cases/SDWJSF-KJZTFWSFK/{模块层-中文}/{catalog页标题}/` |
| 主文件 | `FUNC-{页短名}-用例.md`（一 catalog 页一册）。同目录旧 `API-*-用例.md` 在本页 FUNC 册写完后删除，避免两套并存 |
| 覆盖 | 同目录 `coverage-fp.md`（本页）；父控可另维护系统级 `coverage/SDWJSF-KJZTFWSFK/` 汇总（待建） |

### 调试台登录（不是用例）

登录只写在前置条件（已登录 `https://edu.itic-sci.com/dma/algovwz/`）。不单列登录用例，不写 Token、401/424。

目录命名与专题相同：**`英文缩写-中文名称`**。

- `{模块层}` = catalog `modules[].id` + 中文（例：`chain.basic` 挂在 **`basic-基础指标`**，不是 `chain-产业链分析`）。  
- `{页目录}` = `entry_id` 去点转大写缩写 + `entries[].title`（例：`CHAINBASIC-产业链基础指标`）。  
- 系统级说明见 `test-cases/SDWJSF-KJZTFWSFK/README.md`。

### 1. 盘点（真源 = 调试台源码里的 catalog，不打开页面）

`https://edu.itic-sci.com/dma/algovwz/` 上的下拉框和接口说明，就是这份源码渲染出来的，没有第二份清单：

- 下拉标题：`repos/lumen-ui-algo-apiview/src/views/AlgoWorkspaceView.vue` 的 `endpointOptions.label` = `endpoint.title`
- 参数表、响应字段、请求示例、响应示例：`src/components/algo/ApiInfoPanel.vue` 直接绑定 `params`、`responseFields`、`sampleRequest`、`sampleResponse`

因此编写时只读：

`repos/lumen-ui-algo-apiview/src/catalog/{chain,entan,svc,policy,innov,comp}.json`

页与模块的中文名、目录挂载用 `as-built/catalog/SDWJSF-KJZTFWSFK.yaml`。

1. 按 `catalog_page_id` 取出该页全部 `endpoints`。  
2. 每个 endpoint 抄 `title`、`method`、`path`、`params`、`sampleRequest`、`sampleResponse`、`responseFields`、`status`。  
3. 编写时只读 catalog JSON，不要开浏览器、不要用浏览器 MCP、不要为写用例去 curl 联调台。步骤按页面操作来写，依据是下拉标题和文档字段，不是现场试调。  
4. `status=unavailable` 仍按文档请求/返回写用例，备注注明未交付。  
5. 禁止读 `lumen-algo-py`、`demo-algo-*` 把实现当接口文档。

### 2. 按方法论落表

- 场景类、入参组合、出参分层、粒度：一律按 **§编写方法论 §4～§7**。  
- `路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=`、组合 id（如有）。

### 3. A 线覆盖矩阵（本页完成后）

键（复合）：`Lxx | endpoint_id | field_key | 功能点中文`（来自 `fp-split-by-api-run/work/Lxx.md`，Lxx 与六级需规对应）。

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| … | FUNC-xxxxx | 已覆盖 / 未覆盖 / 部分覆盖 | 一条用例可挂多 field |

- A 线未完成六级：状态可先 **待 A 线合表核对**，已写 endpoint 用例仍有效。  
- B 线独有（联调台有、A 未列）：反表记 `无对应功能点`。

### 4. 金样（首册建议）

| 项 | 内容 |
|----|------|
| 页 | `chain.basic`（module **basic** · path `#/chain/basic` · A 线 L01） |
| 路径 | `test-cases/SDWJSF-KJZTFWSFK/basic-基础指标/CHAINBASIC-产业链基础指标/` |
| 册 | `FUNC-产业链基础指标-用例.md`（第三轮覆盖；旧 API 册删除） |
| 重写标准 | 10 个下拉标题各至少 1 条主流程；产业市场规模这类有参接口另有每参数 1 条反向；步骤是页面操作；模块列是五级/六级；测试内容含「验证」和「检查」 |

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
| 成熟度 | 🟡 金样五条已写。无头试跑 3 过 2 败：FUNC-00001 缺 `cluster_name`、`map_status`；FUNC-00004 空 `chainId` 仍出数。人看截图前不铺第二页 |
| 驱动 | 联调台页面，Playwright **无头**（`run-apiview.mjs` 默认 `--headless true`） |
| 不抄 | 专题的内部评审、`30892`、`P0-xx`。文件形状和判定方式照抄，见「两套脚本」 |
| 产物 | runner 档 + 调用模板；然后才是 `as-built/scripts/SDWJSF-KJZTFWSFK/{module}/{page}/` |
| 顺序 | 1. runner 档 → 2. `chain.basic` 金样五条 → 3. 无头试跑这五条 → 4. 人看截图后再铺页 |

### 现在差什么

| 已有 | 还没有 |
|------|--------|
| 1500 条 FUNC 册，步骤里已有 `参数名=值` | 金样以外的脚本 |
| catalog `base_url` + `chain.basic` 金样五条 yaml | 第二页脚本 |
| `run-apiview.mjs`，以及 §S2「点击从源码定」 | 人看过金样截图之前的铺页 |
| 联调台控件类名稳定（见翻译表） | `gap-func-vs-scripts.py` 只有 `KJZTFWXT` 映射 |

专题入口是 `tools/run-scripts.mjs`（基址 `http://10.50.69.111:30892/`，每条脚本调用 `ensureReviewOff`）。算法库入口是 `tools/run-apiview.mjs`，不往专题文件里加分支。两边共用 `runner-core.mjs` 的读册、断言、截图和 `result.yaml`。

HTTP / Postman 不覆盖「接口信息-清单」「算法测试-清单」。S2 不走那条。

### 执行框架（run-apiview.mjs）

入口 `as-built/tools/run-apiview.mjs`。登录和四个调用动作在 `as-built/tools/apiview-session.mjs`。不改 `run-scripts.mjs` 的登录和评审开关，不改 `session-preflight.mjs`。

| 点 | 做法 |
|----|------|
| 无头 | 沿用现有 `--headless`，默认 true。正式试跑和以后的波次都无头。`--headless false` 只给人排查，不进波次命令 |
| 登录 | 浏览器上下文里做一次。`goto` 之后出现 `.login-card` 才填表：账号框、密码框、按钮「进入算法库」（`LoginView.vue`）。已看到「接口信息」就跳过。不靠地址里有没有 `/login`，路由守卫可能晚于首次判断。yaml 里不写登录步骤 |
| 口令 | 只读环境变量 `ALGO_LOGIN_USER`、`ALGO_LOGIN_PASSWORD`。缺了就停。不把口令写进 yaml、playbook 或 git |
| 评审开关 | 本入口不调用 `ensureReviewOff` |
| 路由 | `base_url` 保持 `https://edu.itic-sci.com/dma/algovwz/`（末尾 `/`）。`goto` 目标写 `#/chain/basic` 这种 catalog hash。拼接结果是 `{base_url}#/chain/basic`。`base_url` 不含 `/dma/algovwz/` 时退出码 2 |
| 会话 | 一次 `run-apiview.mjs` 共用一个浏览器上下文，多条脚本不用重复登录。单条 yaml 不写 Token |
| 截图 | 沿用现在每步一张：`runs/.../scripts/{id}/screenshots/{序号}-{步骤}.png`。`algo_run` 后再截「运行结果」卡片 |
| 调用记录 | 仅 `algo_run` 的脚本。每次执行后写 `runs/.../scripts/{id}/exchange.txt`（UTF-8 文本）。页面清单类不写 |
| 判定 | 沿用 `expect: {note, assert}`、pass/fail/blocked。禁止改断言充绿。调用类没有 `exchange.txt`，或其中的返回是空的，不得判 pass |

前端对照（写 selector 时允许读，禁止读 `lumen-algo-py` / `demo-algo-*`）：

| 要找的控件 | 文件 |
|------------|------|
| 登录 | `lumen-ui-algo-apiview/src/views/LoginView.vue` |
| 未登录跳转 | `src/router/index.ts`（无 token 去 `/login?redirect=`） |
| 两个 tab | `src/views/AlgoWorkspaceView.vue`（`role=tab`：接口信息 / 算法测试） |
| 当前接口下拉 | `src/components/algo/EndpointSelect.vue`（`.tab-endpoint-select`） |
| 入参 | `src/components/algo/ParamForm.vue`（`.param-form`，表单项 extra 文案是 `字段名 · 类型`） |
| 产业选择 | `src/components/common/ChainCascader.vue`（`.chain-cascader`）。`chainId` 一律是级联，不是文本框（`isChainCascaderField`） |
| 执行与结果 | `src/components/algo/ApiTestPanel.vue`（按钮「执行接口」，结果区「运行结果」+ `.json-viewer`） |
| 接口概览 | `src/components/algo/ApiInfoPanel.vue`（method 标签、`.endpoint-path`） |

参数名和示例值仍以 `src/catalog/*.json` 为准。Vue 只用来定怎么点。

### 两套脚本

**调用类（绝大多数）** 用下面四个 action，selector 写在 runner 里，yaml 只填业务值：

| action | 参数 | runner 做什么 |
|--------|------|----------------|
| `algo_tab` | `test` 或 `api` | 点对应 tab。调用类固定 `test` |
| `algo_pick` | 接口标题，如「产业市场规模」 | 点可见的 `.tab-endpoint-select .arco-select-view`，再在可见弹层里滚到并点 `.arco-select-option` 全文。不整页搜文字 |
| `algo_fill` | `set`：要填的字段；`omit`：要留空的字段 | 按 extra 文案找到表单项。`chainId` 走级联，见下方「点击从源码定」。整数走 `a-input-number`。`omit` 点清除。禁止改「高级 JSON」 |
| `algo_run` | 无 | 点「执行接口」，等到 `.json-viewer` 或错误 `a-alert` 出现，截运行结果，并写 `exchange.txt` |

调用类模板（复制后改标题、hash、接口名、参数和 assert）：

```yaml
id: FUNC-00002
func_id: ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00002
entry_id: chain.basic
tier: A
title: 产业市场规模主流程
steps:
  - action: goto
    target: "#/chain/basic"
  - action: algo_tab
    target: test
  - action: algo_pick
    target: 产业市场规模
  - action: algo_fill
    set: { chainId: INB1701, statYear: 2025 }
  - action: algo_run
expect:
  - note: 运行结果 data 为数组，元素含 stat_year、total_revenue、growth_rate
    assert: "await expect(page.locator('.json-viewer')).toContainText('total_revenue')"
```

缺参把字段放进 `omit`，不放进 `set`。无参接口不写 `algo_fill`。断言只要求字段名出现，不钉死 sample 里的具体数字。

`algo_run` 落盘的文本由 runner 写，不由 yaml 抄 catalog 示例。文件在该条结果目录，与 `result.yaml`、`screenshots/` 同级：

```text
runs/…/scripts/FUNC-00002/exchange.txt
```

三段固定，UTF-8：

```text
path: GET /innov/v1/industry/market-stats
request_url: <本次浏览器实际发出的完整 URL；未发出业务 HTTP 时写「无」>
params:
chainId=INB1701
statYear=2025
response:
<响应体原文；失败则写 a-alert 的错误文案>
```

- `path` 取运行结果上方展示的 method 和 path（`.test-source`），不是页面 hash。
- `params` 取提交当时表单里的值。留空的参数写 `chainId=`。无参接口这一段写「无」。
- `response` 优先用这次请求的响应体原文。页面未发业务 HTTP（前端本地示例）时，改为抄「运行结果」里实际展示的 JSON，并在 `request_url` 写「无」。禁止把 catalog 的 `sampleResponse` 填进这个文件。
- 同一次重跑覆盖本条的 `exchange.txt`，不另加序号。

**页面清单类（每页两条）** 不用 `algo_*`。步骤写成 `goto` / `click` / `assert`。`FUNC-00024` 停在「接口信息」，`FUNC-00025` 切到「算法测试」再换一个接口，两条都不点「执行接口」。换接口时：先点本 tab 的 `.tab-endpoint-select .arco-select-view`，下一步 `target` 写选项标题。runner 发现弹层已开，就只点弹层里的 `.arco-select-option`。不要把标题写成整页文字选择器。

### 金样五条（runner 落地之后才写）

| 脚本 id | 用例 | 用哪套 |
|---------|------|--------|
| FUNC-00001 | 产业链列表，无参 | 调用模板，无 `algo_fill` |
| FUNC-00002 | chainId=INB1701、statYear=2025 | 调用模板 |
| FUNC-00004 | 不传 chainId | 调用模板，`omit: [chainId]` |
| FUNC-00024 | 接口信息清单 | 页面清单 |
| FUNC-00025 | 算法测试清单 | 页面清单 |

`fixtures/testdata.yaml` 只写 `base_url`。金样 `tier: A`，禁止 `allow_skip`。

试跑命令（无头，只这五条）：

```text
cd agent-delivery/qa/as-built/tools
node run-apiview.mjs ../scripts/SDWJSF-KJZTFWSFK/basic/chain-basic \
  --only FUNC-00001,FUNC-00002,FUNC-00004,FUNC-00024,FUNC-00025 \
  --run-dir ../runs/金样-algovwz-chain-basic
```

试跑失败先看截图和 steps。selector 错了改 runner 或这条 yaml，不改用例册，不改断言把红变成绿。人看过这五条的截图之前，不派第二页。

### 可复用（只这三条）

1. 一条用例一个 `cases/{脚本id}.yaml`，禁止大包 `scripts.yaml`。
2. `expect[]` 用 `{note, assert}`。`note` 译自该条预期。`assert` 必须落到这一问，禁止空断言、禁止用 `allow_skip` 把失败记成通过。
3. 下拉先点 `.arco-select-view`，再点 `.arco-trigger-popup:visible` 里的 `.arco-select-option`。禁止整页 `getByText`，禁止点宽度为 0 的隐藏 input。

### 点击从源码定

写 selector 之前读联调台 Vue，不靠试跑去猜。对照文件见上面「前端对照」。

**接口下拉。** `EndpointSelect.vue` 是 `a-select`，选项挂在 `body` 的 `.arco-trigger-popup` 上，不在页面正文里。Arco 下拉列表 `.arco-select-dropdown-list-wrapper` 最大高度 200px，每一项行高 36px，大约只露出 5 项，再往下被裁切。点法：先打开下拉，把目标 `.arco-select-option` 滚进这块可视区，再点该项。超时 5 秒。

不要用整页 `getByText().first()`。算法测试页会挂上 `ModelFlowPanel`（`ApiTestPanel` 在 `testVisited` 之后才存在）。`modelFlowRegistry.json` 里该页 `dims` 会和部分接口标题相同，例如产业链基础指标的「产业市场规模」「产业企业规模」「产业机构规模」。整页第一个匹配会落到流程图节点上，而节点正被打开的弹层挡住，点击会空等。接口信息 tab 不挂流程图，所以停在该 tab 时整页文字有时能碰巧点中，不能当成写法。金样「产业投融资规模」不在这三项维度里，但它是下拉第 5 项，贴着 200px 底边，下一项在截图里已被裁掉。整页 click 没有滚到 `.arco-select-option`，8 秒后调用区仍停在「产业链列表」。

**chainId 级联。** `ChainCascader.vue` 是 `a-cascader`，同时开了 `path-mode`、`check-strictly`、`allow-search`。选项树在 `industryCascade.js`：很多集群名和它下面的 L0 产业同名，例如集群「新一代信息技术」下面的 `INB1701` 也叫「新一代信息技术」，而且 L0 还有子节点，不是叶子。Arco 在 `check-strictly` 下，点行文字只是展开，真正写入值的是该项上的单选框（`.arco-radio`）。`chainIdFromPath` 只认 `INB` 开头的 id，点中集群（`CL-*`）不会得到 chainId。

点法：

1. 旁边 `.arco-tag` 已经是目标 id，就不要再开面板。页面示例经常已经填好，再点一次只会空等。
2. 否则点 `.chain-cascader .arco-select-view`（级联的可点层是 SelectView，没有 `.arco-cascader-view`），用名称表里的中文名搜索（表抄 `CLUSTER_SEED` 和 `CATALOG_L1`）。在 `.arco-cascader-search-option` 里，选「最后一段等于这个名字、且路径最长」的那条。这样会点到产业节点，而不是同名集群，也不会点到更深的子产业。
3. 点这条上的 `.arco-radio`，再等 tag 变成该 id。点击超时 5 秒。名称表没有的 id 直接失败，不拿 id 原文去搜。

### 用例词和页面词

脚本按页面写，差异记在 `as_built_note`。S2 不回改用例册。

| 用例里的说法 | 脚本怎么做 |
|--------------|------------|
| 侧栏进入某页 | `goto` 完整地址 `{base_url}#/{catalog path}`。`chain.basic` 为 `https://edu.itic-sci.com/dma/algovwz/#/chain/basic`。不点侧栏去碰兄弟页 |
| 停留「接口信息」 | 进页默认即该 tab。`role=tab`，名称「接口信息」，`aria-selected=true` |
| 切换「算法测试」 | 点击 `role=tab`，名称「算法测试」 |
| 接口下拉选择「某标题」 | 先点本 tab 的 `.tab-endpoint-select .arco-select-view`，再点弹层里该标题的 `.arco-select-option`。不要整页搜标题 |
| 填写 `chainId=INB1701` | `algo_fill`。tag 已是该 id 则跳过。否则按「点击从源码定」搜索并点单选框，直到 tag 等于该 id。其它字段按表单项 extra 的字段名填。禁止只改「高级 JSON」 |
| 不传某参数 | 该输入留空，再点执行 |
| 点击调用 | 按钮文案是 **执行接口** |
| 返回面板 | 「运行结果」卡片里的 JSON。断言字段名出现，不钉死 sample 里的具体数字 |

### 落盘

```text
as-built/scripts/SDWJSF-KJZTFWSFK/basic/chain-basic/
  index.yaml                 # layout: cases-v1；gold: 上面五个 id
  cases/FUNC-00001.yaml      # 其余四条同名
  fixtures/testdata.yaml     # base_url 用 catalog 那条，带 /dma/algovwz/
  coverage.md                # 脚本 id → 用例编号 → 场景
```

`id` 与 `func_id` 尾号都是 `FUNC-00001` 这种，不用 `P0-01`。`entry_id: chain.basic`。`tier: A`。金样禁止 `allow_skip`。

断言口径：

- 主流程：运行结果 JSON 里出现用例点名的字段（如 `chain_id`、`total_revenue`）。
- 反向：结果或错误提示里出现该参数名，且不出现用例禁止的成功字段。
- 清单：页头接口个数、下拉标题、method 与 path 文案与该条预期一致。

写完只回填这五条用例的「自动化用例ID」列。其余 1495 条不动。`runs/` 只在试跑时由 runner 生成，不提交。不改专题脚本，不跑 `KJZTFWXT`。

`catalog_status=unavailable` 的接口不进金样。铺开时照样写：页面是「Java REST 未发布」且结果里没有用例要的字段，记失败。禁止改断言去迎合未发布。

### 金样之后才许铺开

人确认五条的 selector 和断言能对上页面之后，按 catalog 页派子：一页一个子 agent，每批最多 4 页。子 agent 只写本页 `cases/*.yaml` 和本页 `coverage.md`，并回填本页「自动化用例ID」。不跑批，不改用例步骤。`gap-func-vs-scripts.py` 的系统映射放到铺开时再加，金样用 `coverage.md` 看。

### 父控先做 runner（复制即用）

```text
【身份】qa-agent。只做算法库 runner 档，不写金样 yaml，不试跑。
【任务说明】agent-delivery/qa/algo-lib-api-case-playbook.md §S2「执行框架」
【改】新增 as-built/tools/run-apiview.mjs 与 apiview-session.mjs。读册和结果文件走 runner-core.mjs。
【行为】无头默认开；/login 用环境变量登录一次；不关内部评审；goto 支持 #/path；实现 algo_tab / algo_pick / algo_fill / algo_run。algo_run 之后在该条结果目录写 exchange.txt（path、params、response 三段）。
【不改】run-scripts.mjs 的登录、评审开关和 goto。不读 lumen-algo-py。不把口令写进文件。
【验收】node run-apiview.mjs --check 对一份最小 fixtures 能解析；专题目录仍用 run-scripts.mjs。
开干：按 §S2 表改 runner，改完停。
```

金样五条已由 `QA-KJZTFWSFK-SCRIPT-GOLD-L01` 落盘。无头试跑已由 `QA-KJZTFWSFK-SCRIPT-TRIAL-L01` 做完：3 过 2 败，不要和编写单混在一起，也不要为了变绿改断言。上面这段 runner 父控包已在 2026-10-22 做完（`QA-KJZTFWSFK-RUNNER-APIVIEW-L01`），不要再派一遍。

---

## S3 · 脚本执行

| 项 | 内容 |
|----|------|
| 成熟度 | 🔴 全库未开。金样五条已无头试跑（3 过 2 败）。全库波次仍走 `script-batch-run-playbook.md`（串行、禁止改脚本充绿）。人看截图前不铺页 |
| 环境 | `https://edu.itic-sci.com/dma/algovwz/`；波次目录建议 `as-built/runs/{日}-algovwz-{wave}/` |
| 编排 | 试跑通过后再按专题波次手册串行铺开。一条波次同时只跑一个 runner |

---

## S4 · 用例交付合并

| 项 | 内容 |
|----|------|
| 成熟度 | 🟡 待编写（`delivery/SDWJSF-KJZTFWSFK/`） |
| 必读 | [`case-delivery-playbook.md`](case-delivery-playbook.md) · `_submit.md` · `delivery/README.md` |
| A 线输入 | by-api 合表 `…功能点拆分-by-api_v1.xlsx`（或豁免前用 `work/Lxx` 矩阵） |
| 注意 | 投影类型码 **FUNC**。2026-10-19 已导出的 1322 条 API 交付表是评审前过渡稿，第三轮册完成后再换。未覆盖功能点不投影。不合 A 线，除非另下指令 |

专题一键脚本 `_gen_zt_delivery_func_ab_merge.py` **不**直接适用于算法库；合表脚本待单建。

### 合表前硬闸门（Excel 无附录）

合进客户 17 列功能表之前，对全部 `FUNC-*-用例.md` 主表行扫描（正文四列：测试内容 / 前置条件 / 测试步骤 / 预期结果）：

| 闸门 | 命中则不合格 |
|------|----------------|
| 附录引用 | 步骤或前置出现「按附录」「附录组合」「见附录」 |
| 文档示例话术 | 出现「使用文档示例」「按文档示例」；应改为直接赋值如 `chainId=INB1701` |
| 步骤含校验动词 | 步骤出现「核对 / 确认 / 检查 / 校验 / 查看是否 / 比对 / 验证」（功能点标题里的「比对」字样除外） |
| 调用类无具体入参 | 有参接口的主流程 / 备选步骤既没有 `参数名=` 赋值，也没有「不传 xxx」 |

不合格先改册再合表，禁止把「附录 id」原样打进交付 Excel。

---

## S5 · 可交付测试记录

| 项 | 内容 |
|----|------|
| 成熟度 | 🟡 骨架共用 |
| 必读 | [`record-delivery-playbook.md`](record-delivery-playbook.md) |

证据：接口 JSON 片段 / 联调台截图均可；文件名仍建议 `{用例编号}-Pass|Fail-{序号}.png`。

---

## 长任务返工（2026-10-19 第三轮 · 现行）

> 父控提示词只引用本节。第一轮 `API-00001`～`00888`、第二轮 `API-00889`～`02210`（含工作区 Excel 与交付目录那份 1322 条）全部作废，不复用。`run-log` 里已有批次只代表旧轮，不算本轮完成。

### 本轮必须遵守的规则

1. 环境 `https://edu.itic-sci.com/dma/algovwz/`。步骤是侧栏进页、下拉选接口、按组合填参、点击调用。不写 `GET`/`POST`。  
2. 功能模块=算法工具库，子功能模块=科技专题服务算法库，功能项=五级，子功能项=六级。无六级的页两列都写「待挂需规」。一页多六级时按 endpoint 归属拆开。  
3. 编号 `ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-#####`，从 `FUNC-00001` 重排。父控按现有各册行数预分配闭区间，子 agent 不自己抢号。  
4. 功能点用 catalog `title`，去掉自行添加的 `A1`、`A2`。  
5. 测试内容写成「验证{功能点}功能，检查{本条要确认的事}」。  
6. 每个接口至少 1 条主流程；正向覆盖合法参数组合；反向每个参数 1 条。场景写在备注 `场景=`。不合 A 线。  
7. 登录只放前置条件。调用类用例的预期仍写返回面板里的文档字段或该参数的错误说明。前置与步骤里的取值写成 `chainId=INB1701`，禁止「使用文档示例」。  
8. **每页另加 2 条页面清单用例**（不占接口参数组合的条数）：一条「接口信息」，一条「算法测试」。数量 / 名称 / method / path 的判定写在**预期**；步骤只写进入、停留 tab、切换下拉。写法见 §6.1。  
9. 步骤必须自含参数赋值（`填写 a=1、b=2，点击调用`），禁止「按附录组合填写」。附录 A 可选，合表不带。  
10. 89 页册全部完成后，父控按 §S4 合表硬闸门扫一遍，再重出两份 Excel（工作区合表 + `delivery/SDWJSF-KJZTFWSFK/6.国际科技信息中心项目_科技专题服务算法库_测试用例.xlsx`），按客户模板 17 列，仍不合 A 线。子 agent 不写 Excel。

### 文档从哪读

只读 `lumen-ui-algo-apiview/src/catalog/*.json`，五级/六级读 `01-task-list.md` 与 `_l6-to-catalog-map.yaml`。禁止浏览器 MCP、Playwright、为写用例去请求联调台或旧的 50897/30897。

### 返工动作

**89 个在用 catalog 页全部重写**。新册为 `FUNC-{页}-用例.md`，覆盖 `coverage-fp.md`，然后删除同目录 `API-*-用例.md`。

| 旧产物 | 返工 |
|--------|------|
| `API-00001`～`02210` | 作废，号段冻结 |
| 各页 `API-*-用例.md` | 本页 FUNC 册写完后删除 |
| 工作区与 delivery 下的算法库用例 xlsx | 旧 API 表作废。89 页 FUNC 册完成后由父控按客户模板重出，仍不合 A 线 |
| `run-log.md` 已有行 | 只代表旧轮 |

- 取号用 `next_seq.FUNC`（当前为 1）。不要改 `next_seq.API`。每批结束回写 `next_seq.FUNC` 与 `modules`。  
- 进度追加到 `run-log.md`，表头注明「第三轮」。不要把旧轮已完成页跳过。

### 退出（禁止无限循环）

- 同一页验收不合格：只返工 **1** 次；仍不合格 → `跳过-验收失败`，释放未用编号。  
- 同一页子任务报错、超时、无产物：只重派 **1** 次；仍失败 → `跳过-执行失败`。  
- 契约缺失或 yaml/JSON 对不上：尝试 **1** 次仍对不上 → `跳过-疑难`。  
- 连续 **2** 批（最多 8 页）全部跳过，或真源缺失 / `code-registry` 写坏 → **停机**，输出完成页与跳过页，不再派下一批。  
- 跳过页写入 `run-log.md` 后，本会话不再打开。  
- 待写页清空（完成或已跳过都算出列）→ 输出总表后停止。

## 子 agent 细则（S1 · 单 catalog 页）

1. 只写本任务 `catalog_page_id` 对应 **一个** `FUNC-*-用例.md` + 本目录 `coverage-fp.md`。写完后删除同目录 `API-*-用例.md`。  
2. 只用父控给出的 FUNC 闭区间。禁止复用任何 `API-` 号。不写登录用例、Token、401/424。  
3. 接口文档只读 `lumen-ui-algo-apiview/src/catalog/*.json`。五级/六级只读任务队列和 map。禁止读 `lumen-algo-py` / `demo-algo-*`，禁止按 `field_key` 一行一用例。  
4. 禁止改 A 线 `work`、禁止改业务仓、禁止改其它页。禁止浏览器、Playwright、为写用例去请求联调台或旧的 50897/30897。  
5. 写不下去就回报卡点并停止，不换页、不空转。

---

## 维护

- B 线阶段变更：**先改本文件**，再改 `algo-lib-playbook-index.md` §1 B 线表一行。  
- 不在 `func-test-playbook-index.md` 复制算法库长 Kickoff；该索引仅保留就绪门 + 跳转。  
- 2026-10-22：算法库入口是 `run-apiview.mjs`，专题入口仍是 `run-scripts.mjs`。共用 `runner-core.mjs`。金样五条已写。同日无头试跑 3 过 2 败；下拉只点弹层选项，`chainId` 点级联单选框。见 §S2「点击从源码定」。

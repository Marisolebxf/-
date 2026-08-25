# CHAIN-ENG-PAGE-MATRIX-L01 · 产业链 demo 8 功能页工程闭环与原型差矩阵

> 日期：2026-08-24  
> parent：`CHAIN-HZW-THREE-TRACK-L01`  
> 结论状态：**首轮静态审计 + 构建检查完成；浏览器逐页实测待补**  
> 本叶不评价算法是 Mock 还是真实实现，只评价功能流转、工程链和原型一致性。

## 任务认领

| 字段 | 值 |
|---|---|
| claimed_by | `human:李伟` |
| supervised_by | `human:李伟` |
| claim_type | `pull` |
| 状态 | `in_progress` |

## Ponytail

| 字段 | 值 |
|---|---|
| ponytail | `lite` |
| 说明 | 本叶是只读矩阵/探针，不写业务代码；未跳过 D8/D9/D10、调用链或 handoff。 |

## 范围和判定标准

工程链目标：

```text
demo-ui-topic 页面
  → demo Java REST
  → demo_ 库
```

每页检查：

1. 页面和主操作能否正常流转；
2. 前端是否只调 Java；
3. Java 是否有对应门面，并有 demo 库/表证据；
4. `USE_MOCK=false` 是否仍由 fixture/localStorage 填数；
5. 对照已评审原型：区块、状态、条件栏、应同行内容是否折行、标签/控件/按钮是否错行；
6. 分析工作区是否满足 I2-12：切条件不自动 create、同条件单飞、当天成功复用、完成后不自动跳结果。

## 总结论

**当前不达到“8 页功能完整、工程链完整、可交付”标准。**

- 前端没有越层直连 Python；Vite 只代理 `/topic` 和 `/ops` 到 Java 网关。
- demo Java 已有产业链分析门面，但前端 8 页基本未消费 `/topic/v1/industry/**`。
- 真实闭环仅见维护页的产业集群目录/映射：前端 → Java → `demo_gkxlumenx_dim`。
- 查询、总览、分析任务、结果、报告主要来自前端 fixture / localStorage。
- 全仓无统一 `USE_MOCK` 开关；集群接口失败时也会自动回落 `CLUSTER_SEED`。
- 全景条件栏已有截图证据：标签/下拉/按钮未保持一行基线，长产业名导致折行或错位；第 1 条不能放行。

## 8 页矩阵

| 页面 | 路由与主流程 | 前端 → Java | Java → demo 库 | Mock 关闭诚实性 | 原型内容/样式 | I2-12 | 总判 |
|---|---|---|---|---|---|---|---|
| 产业查询 | 路由和推荐/检索/筛选/入篮/全景深链结构齐 | **FAIL**：检索仅本地 `INDUSTRY_SEARCH_RECORDS` | 无 | **FAIL**：固定 fixture | 待浏览器补 V1–V7；高级筛选同行风险 | N/A | **FAIL** |
| 产业链总览 | 路由、集群→L0、全景/资讯/概况三 Tab 齐；与 USM 五 Tab 有差 | **FAIL**：图谱/资讯/KPI 本地数据 | 无 | **FAIL**：KPI/企业等写死 | 顶栏 Select/Tag/Button 存在折行风险，待四档宽度实测 | N/A | **FAIL** |
| 全景图谱 | 改条件→开始分析→过程→结果结构齐 | **PARTIAL**：仅 `resolve-scope` 调 Java；图谱/KPI fixture | `resolve-scope` 读 dim 映射；分析结果无 | **FAIL** | **FAIL（截图）**：分析对象、所属产业、数据截至和按钮基线不齐，长文案折行 | 静态 PASS | **FAIL** |
| 运行诊断 | 周期/关键环节/瓶颈/记录，过程/结果/报告结构齐 | **PARTIAL**：仅 `resolve-scope`；task 用 localStorage | 仅 dim 映射；分析无 | **FAIL** | scope 行/底栏待浏览器；存在旧 `TaskConfigPanel` 双轨死代码 | 静态 PASS | **FAIL** |
| 区域评价 | 指数/竞争力/记录，配置→过程→结果齐 | **PARTIAL**：仅 `resolve-scope` | 仅 dim 映射 | **FAIL**：区域和结果 fixture | 多选、权重表和 CTA 折行风险，待浏览器 | 静态 PASS | **FAIL** |
| 深圳决策 | 对比→发展链、负例拦截结构齐 | **PARTIAL**：仅 `resolve-scope` | 仅 dim 映射 | **FAIL**：比较结果 fixture | Cascader/来源/目标混排待浏览器 | 静态 PASS | **FAIL** |
| 维护管理 | 16 项菜单；集群映射可编辑 | **PARTIAL PASS**：集群 GET/PUT 已接；其余多为本地/占位 | **PASS（映射子路径）**：`demo_gkxlumenx_dim.industry_cluster(_map)` | **FAIL/PARTIAL** | 导航/表单待浏览器；约 13/16 能力为占位 | N/A | **FAIL** |
| 结果/报告 | 新工作区内联结果/报告 + 遗留 `/results`、`/reports` 双轨 | **FAIL**：无 HTTP；localStorage + 固定结果 | 无 | **FAIL** | 遗留壳与新版主链脱节，待浏览器核对直达 | 静态 PASS（新版内联） | **FAIL** |

## 工程链证据

### 前端只调 Java（合规）

- `demo-ui-topic/vite.config.ts`：仅将 `/topic`、`/ops` 代理到网关，并明确“不直连 Python/DB”。
- `src/app/lib/industryCluster/api.ts` 当前只有：
  - `GET /topic/v1/meta/industry-clusters`
  - `POST /topic/v1/meta/industry-clusters/resolve-scope`
  - `PUT /ops/v1/industry-cluster-maps/{clusterId}`
- 产业查询/总览/诊断/区域/深圳未调用 `/topic/v1/industry/**`。

### Java 门面存在但前端未接

`demo-svc-platform/gkx-innov` 已有 `ChainController` / `ChainService` / `ChainAlgoClient`，覆盖 panorama、cycle、key-nodes、bottlenecks、region-index、competitiveness、shenzhen 等路径；Java 经 Feign 调 Python。当前 demo 前端未消费这些门面。

### demo 库证据

产业集群 meta / 映射由 Java 读取：

- `demo_gkxlumenx_dim.industry_cluster`
- `demo_gkxlumenx_dim.industry_cluster_map`

其余页面“有数”主要来自前端 fixture，不能作为 demo 库接通证据。

## 原型差（P0）

用户提供的两张全景条件栏截图已证明：

1. 应处于同一条件栏的标签、下拉框、按钮没有保持统一水平/垂直基线；
2. 长产业名把控件挤压或折到下一行；
3. 标签和输入框出现错行；
4. 当前共享 CSS `.policy-analysis-filter-row { flex-wrap: wrap }`，字段又是 `flex-direction: column`，与本轮“标签和框同行、不折行”的验收口径存在直接冲突。

后续浏览器实测必须覆盖 1680 / 1440 / 1280 / 1100 宽度，逐页截图条件栏/工具条。

## I2-12 静态结论

全景、诊断、区域、深圳的静态实现满足：

- 切对象/Tab/条件不自动创建任务；
- 只有点击“开始分析”才 submit；
- 同指纹查在跑任务；
- 当天成功结果可复用；
- 完成后需要显式“查看结果”，不自动跳。

缺口：任务存储仍为浏览器 localStorage，不是 Java task API，因此只能判交互门控 PASS，不能判工程链 PASS。

## 运行检查

| 命令 | 结果 |
|---|---|
| `npm run build` | **PASS**；Vite 生产构建成功。存在单包 >500k 警告，不挡本叶。 |
| `npm run design:check` | **FAIL**；`theme.css must include padding: 18px 16px 20px`。该检查是全仓设计契约，需前端修单判断是否与本次条件栏同源。 |
| `industry-chain-permission-contract` | **PASS 6/6**。 |
| `industry-center-clean-rebuild` | **FAIL（测试基线失效）**；引用的 `UX-SPEC-CHAIN.md` 已不存在。 |
| `industry-search-five-pack` | **FAIL 1/5**；Node 直接 import `.ts` 报 `ERR_UNKNOWN_FILE_EXTENSION`。 |
| `industry-panorama-five-pack` | **FAIL（测试文件编码损坏）**；乱码正则导致 SyntaxError。 |
| `industry-diagnosis-five-pack` | **FAIL 4/20**；16 过、4 处源码契约匹配失败。 |
| `industry-regional-five-pack` | **FAIL 1/12**；11 过、1 处源码契约匹配失败。 |
| `industry-shenzhen-five-pack` | **PASS 11/11**。 |
| demo 静态站 `192.168.88.63/gkx_topic_demo` | **不可达（HTTP 000）**；当前网络 15 秒超时。 |
| demo Java `30889/api/topic/v1/industry/list`、meta clusters | **不可达（HTTP 000）**；当前网络 15 秒超时。 |
| 浏览器 8 页 × 4 宽度 | **待补**；本会话无浏览器自动化结果，不能把静态检查冒充视觉验收。 |
| demo Java / DB 在线探测 | **待补**；需实际环境 URL/账号或已部署 demo 地址。 |

## 缺口分流建议

### `CHAIN-ENG-FE-GAP-FIX-L01`

- 接入已有 demo Java 产业查询/分析门面；
- 建统一 Mock 开关，关闭时禁止 fixture/localStorage 填数；
- 修全景及同族条件栏折行、标签/框/按钮错行；
- 清理结果/报告旧双轨；
- 维护页占位能力按范围拆分，不以菜单存在冒充完成。

### `CHAIN-ENG-JAVA-DEMO-L01`

- 逐页核对前端所需接口与 `ChainController` 实包；
- 补分析 task / result / report Java 契约及持久化；
- 明确 Java 读 ADS 与 Java→Python 的边界；
- 提供 demo 库、表、样例响应证据。

## 当前开放项

1. 浏览器逐页视觉/交互实测未完成；
2. 已找到 demo 地址（静态站 `192.168.88.63/gkx_topic_demo`、Java 经 `30889/api`），但当前网络均 HTTP 000；
3. `design:check` 已红；
4. 产业链静态契约测试存在基线路径失效、测试文件乱码和 Node 不能直接 import TS 等问题；
5. 当前结论足以判定工程链 **不完整**，但不足以给出每个视觉像素缺陷的最终清单。

## 涉及文件

- `repos/demo-ui-topic/src/app/pages/industry-center/**`
- `repos/demo-ui-topic/src/app/lib/industryCluster/api.ts`
- `repos/demo-ui-topic/src/app/system-tasks/systemTaskStore.ts`
- `repos/demo-ui-topic/src/app/routes.tsx`
- `repos/demo-ui-topic/src/app/components/filter/filterControls.css`
- `repos/demo-svc-platform/gkx-innov/**/ChainController.java`
- `repos/demo-svc-platform/gkx-innov/**/IndustryClusterService.java`

## 架构合规自检

- ✅ 前端未直连 Python/DB；
- ✅ Java→Python 边界存在；
- ✅ demo 集群映射使用 demo schema；
- ❌ 8 页主路径未形成前端→Java→demo 数据闭环；
- ❌ Mock 关闭零 fixture 尚未实现；
- ⚠️ 图谱算法/指标口径不在本叶评价范围；
- ⚠️ 可观测 traceId 需在线实测补证。


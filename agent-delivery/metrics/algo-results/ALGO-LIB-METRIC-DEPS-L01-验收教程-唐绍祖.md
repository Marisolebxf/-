# ALGO-LIB-METRIC-DEPS-L01 人工验收教程（给唐绍祖）

> 用途：正式 push 并通知淮政玮之前，由你（唐绍祖）人工核对、验收 A1 的产出。
> 本任务类型：`spike`（合同盘点）。8/25 的对外主交付是「三方 ODS 不满足清单」，不是代码、不是 seed。
> 一句话边界：你签「怎么算、算不算模型、算法库 97 叶是否全覆盖、ODS 判定是否诚实」；口径/适用性归淮政玮，ODS Mapping 落地归辜少彬，A2 差集归淮政玮签。

---

## 0. 验收前先建立的三条心智

1. **这是一张「盘点表」，不是一张「实现表」。** 允许大量 `pending_ods`（未核验），但不允许把「未核验」写成「已确认缺口」，也不允许凭 DWD 反推 ODS 已满足。
2. **A1 不改 seed、不写业务代码。** 只要 `cfg_metric-*.yaml` / 就绪度矩阵 / registry 被动了，直接打回，不用继续看内容。
3. **两个合同分开。** 算法库合同 L 看「库里有没有这 97 叶、联调台能不能演示」；功能合同 F 看「页面上数字对不对」。本任务只验收 L 侧盘点，不验收页面。

---

## 1. 你签什么、不签什么

| 范围                                         | 归属                          | 你的动作                      |
| -------------------------------------------- | ----------------------------- | ----------------------------- |
| 公式 /`algorithm.type` / MODEL·GRAPH 步骤 | **唐绍祖**              | 逐条抽检 + 会签               |
| 算法库 97 叶是否全覆盖（表1）                | **唐绍祖**              | 核对叶数、无漏维              |
| ODS 满足度判定是否诚实（表2/表3）            | 唐绍祖审 + 辜少彬落地 Mapping | 抽检判定是否诚实、未标假 full |
| 口径 / 8 件套 / 适用性                       | 淮政玮                        | 不签                          |
| A2 差集（专题 7 + 展示 70）                  | 淮政玮                        | 不签，已并行交付              |
| 三方 ODS 实际 Mapping / 入站                 | 辜少彬 / GDF                  | 不签，8/25 后开               |

---

## 2. 验收前准备

### 2.1 交付文件（8 个，都在 `agent-delivery/metrics/algo-results/`）

| 文件                                            | 角色                                        |
| ----------------------------------------------- | ------------------------------------------- |
| `ALGO-LIB-METRIC-DEPS-L01-requirements.yaml`  | 表1：97 叶需规逐条对应                      |
| `ALGO-LIB-METRIC-DEPS-L01-metrics.yaml`       | 表2：指标·算法·公式·输入依赖（机器真源） |
| `ALGO-LIB-METRIC-DEPS-L01-ods-gaps.yaml`      | 表3：从表2 投影的缺口（机器）               |
| `ALGO-LIB-METRIC-DEPS-L01-ods-gaps.md`        | 给人读的缺口清单                            |
| `ALGO-LIB-METRIC-DEPS-L01-ods-status.xlsx`    | 8/25 给人主表（四 sheet）                   |
| `ALGO-LIB-METRIC-DEPS-L01-summary.md`         | 八维计数                                    |
| `ALGO-LIB-METRIC-DEPS-L01.md`                 | handoff（`review` 状态）                  |
| `ALGO-LIB-METRIC-DEPS-L01-验收教程-唐绍祖.md` | 本验收教程（给唐绍祖）                      |

### 2.2 真源与对照（只读）

- Schema：`agent-delivery/metrics/algo-results/ALGO-LIB-METRIC-DEPS-L01-schema.md`
- xlsx 栏目与 DoD：`agent-delivery/agent-handoffs/算法库联调-ALGO-LIB/给人说明-指标与算法工作类型与流程梳理.md` §9
- 97 叶真源：`agent-delivery/bid-reference/srs/05-深度挖掘算法/科技专题服务算法库/README.md` + 八维各层 md
- 只读样板（非验收对象）：`metrics/calc-logic/ENT/`、`metrics/registry/cfg_metric-ENT-seed.yaml`、`metrics/indicator-inventory/2026-08-20/`

### 2.3 工具

- xlsx：Excel 或 WPS 直接打开。
- yaml：任意文本编辑器；想快速核对计数可跑本教程 §11 的 Python 片段。

**重要分工**：本教程中第一步至第五步、第七步的机械数量/重复项/缺项/命名异常核对，Agent 已代唐绍祖完成并复核两遍，结论见 §8.12；唐绍祖只需重点完成 §8 的 10 条内容判断和会签，不需要逐条重新数数。若只做可信度抽查，可任选 2~3 条对照 §10 关键数字即可。

---

## 3. 第一步：核对表1（97 叶需规覆盖）

**看什么**：`ALGO-LIB-METRIC-DEPS-L01-requirements.yaml`

**怎么核**：

1. 打开文件，找到 `srs_leaf_count_expected` 与 `srs_leaf_count_actual`，两者必须都是 `97`。
2. 数 `requirements` 列表长度，必须 `97` 条；`requirement_id` 不得重复。
3. 对照八维 README，逐维确认叶数：

| 维度           | 叶数         |
| -------------- | ------------ |
| 企业           | 11           |
| 政策           | 9            |
| 产业链         | 16           |
| 产业服务       | 13           |
| 综合           | 11           |
| 技术链         | 14           |
| 科研机构       | 10           |
| 人才           | 13           |
| **合计** | **97** |

4. 每条需规必须有 `coverage_status`（`full | partial | missing | third_party`）与 `metrics[]`（0～N）。

**合格线**：

- 叶数 = 97，八维无漏、无重复 ID。
- 每条都有 `coverage_status` + `metrics[]`。
- 覆盖四档合计 97：`full` + `third_party` 应等于 97（本批结果：`full=60`、`third_party=37`、`partial=0`、`missing=0`）。
- 技术链 / 科研机构 / 人才三维必须全部是 `third_party`，不能伪展开成 `full`。

**不合格要打回**：叶子漏维、`requirement_id` 重复、有需规既无指标也无 `third_party` 说明、把第三方维标成 `full`。

---

## 4. 第二步：核对表2（指标·算法·公式·依赖）

**看什么**：`ALGO-LIB-METRIC-DEPS-L01-metrics.yaml`

**怎么核**：

1. 数 `metrics` 列表，应为 `101` 条，`metric_id` 无重复。
2. 每条指标必须有：
   - `definition`（非空）
   - `algorithm.type`（`STAT | COMPUTE | MODEL | GRAPH | API | MIXED | UNKNOWN`）
   - `formula` 或 `steps`（至少其一）
   - `inputs[]`（重要计算依赖，逐输入单独评 ODS）
3. **MODEL / GRAPH / MIXED 必须 `steps` 非空**，禁止只写「模型计算」一句话。
4. **第三方维（技术链/科研机构/人才）**：`formula` 可写「不展开」，但 `inputs[]` 与每条输入的 `ods_mapping_status` 仍必须存在。
5. 每条输入必须有 `ods_mapping_status`（`full | partial | none | pending_ods | n/a`）+ `evidence`。
6. 指标级 `dependency_rollup` 必须符合 schema 汇总规则：

| 输入情况                        | 指标 rollup 结论                        |
| ------------------------------- | --------------------------------------- |
| 全部必需输入 full               | `full`                                |
| 至少一项可用且存在 partial/none | `partial`                             |
| 全部必需输入 none               | `none`                                |
| 任一必需输入未核三方 ODS        | `pending_ods`（禁止凭 DWD 反推 full） |
| 纯派生                          | `n/a`，inputs 指向上游 metric_id      |

**合格线（本批快照，供对照）**：

- 指标数 = 101，无重复 ID。
- `algorithm.type` 分布：`API=38`、`GRAPH=8`、`MIXED=10`、`MODEL=37`、`STAT=8`。
- `dependency_rollup` 分布：`full=1`、`partial=2`、`none=1`、`pending_ods=91`、`n/a=6`。
- 所有 MODEL/GRAPH/MIXED 都有 steps；所有指标都有 definition 与 formula/steps。

**不合格要打回**：MODEL/GRAPH 缺 steps、某个 `algorithm.type=UNKNOWN` 却已经开工、第三方维被伪展开成自研公式、输入缺 `ods_mapping_status` 或 `evidence`。

---

## 5. 第三步：核对表3 + xlsx 四 sheet

**看什么**：`ALGO-LIB-METRIC-DEPS-L01-ods-gaps.yaml`、`ALGO-LIB-METRIC-DEPS-L01-ods-status.xlsx`、`ALGO-LIB-METRIC-DEPS-L01-ods-gaps.md`

**怎么核**：

1. `ods-gaps.yaml` 是从表2 `inputs[]` 投影出来的，禁止手填一套对不上的平行表。
   - `confirmed_unmet` 只含 `none` + `partial`（本批 = 40 条：none=37 + partial=3）。
   - `pending_verify` 只含 `pending_ods`（本批 = 334 条）。
2. 打开 xlsx，确认四张 sheet 都在，且行数正确：

| Sheet      | 内容              | 数据行数（本批） |
| ---------- | ----------------- | ---------------- |
| 全量满足度 | 表2 全部 inputs   | 469              |
| 不满足     | 仅 none + partial | 40               |
| 待核验     | 仅 pending_ods    | 334              |
| 八维汇总   | 8 维 + 合计       | 9（合计叶数=97） |

3. 核对列名与 §9.3 完全一致（尤其中文列名）：
   - Sheet1 列：`维度, requirement_id, 需规标题, metric_id, 指标中文名, input_name, required_grain, required_field, source_system, ods_table, ods_field, ods_mapping_status, evidence, gap, impact, 指标级 rollup`。
   - Sheet2 在 Sheet1 基础上首列加 `gap_id`（`ODS-GAP-001` 起）。
   - Sheet3 首列加 `判断说明`，且每行都必须写「未核验 ≠ 已确认缺口」。
   - Sheet4 列：`维度, SRS 叶数, 表1 已登, 指标数, full, partial, none, pending_ods, n/a, 不满足条数, 待核验条数`。
4. `ods-gaps.md` 文首应写清：已确认不满足 40、待核验 334、全量五档计数。

**合格线**：

- Sheet1 行数 = 表2 全部 inputs 行数（469，全量，不是只出缺口）。
- Sheet2 只含 `none`/`partial`；Sheet3 只含 `pending_ods`；`pending_ods` 一条都不许进 Sheet2。
- 每条不满足写清：缺什么字段/粒度、影响哪条需规/指标、对公式的影响。

**不合格要打回**：只交 yaml 不交 xlsx、Sheet1 不是全量、`pending_ods` 混进 Sheet2、不满足条目没写 `impact`。

---

## 6. 第四步：合规红线（逐条过，有一条违规则打回）

逐项确认，全部必须「未发生」：

- [ ] 未改 `metrics/registry/cfg_metric-*-seed.yaml`
- [ ] 未改 `metrics/registry/metric-readiness-matrix-*.yaml`
- [ ] 未改 `metrics/registry/*-seed.yaml`（其他维度 seed）
- [ ] 未改 `agent-delivery/task-registry.yaml`（本叶不碰任务注册）
- [ ] 未写 Python / Java / 前端业务代码
- [ ] 未交混用的 `*-deps.yaml`
- [ ] 未凭项目 DWD 反推 ODS `full`
- [ ] 未把 `pending_ods` 写入「不满足」清单
- [ ] 未伪展开第三方公式（第三方 `formula` 只能是「不展开」）
- [ ] 未把 A2 `missing`（专题 7 + 展示 70）混进 ODS 表
- [ ] 未为缺口编造正式 `M_*` 写入 seed（无正式 ID 一律 `TEMP_ALGO_*`）

快速自查方式：`git status --short` 应只看到本叶 `algo-results/` 下的交付文件；如果出现 `metrics/registry/` 或 `cfg_metric-*.yaml` 的改动，立即停。

---

## 7. 第五步：summary / handoff 一致性

1. `summary.md` 的八维计数必须与 xlsx Sheet4 完全一致（叶数 97、指标 101、ODS 五档、不满足 40、待核验 334）。
2. `summary.md` 必须含：八维覆盖率四档、指标级 `dependency_rollup` 五档、`algorithm.type` 分布、confirmed/pending 计数。
3. `handoff`（`ALGO-LIB-METRIC-DEPS-L01.md`）必须指向上述全部路径、状态为 `review`、写清开放项。

---

## 8. 抽检（必做 10 条，人肉看内容）

不要只信计数。下面 10 条覆盖 `STAT / GRAPH / MODEL / MIXED / API / third_party`，也覆盖企业、政策、产业链、产业服务、综合、技术链、人才七类维度；请按顺序逐条打开文件、定位 `metric_id`、核对内容，并记录「通过 / 打回」。

抽检字段都在该条 metric 的 `algorithm:` 节点内：`algorithm.type`、`algorithm.formula`、`algorithm.steps`；`inputs[]` 与 `dependency_rollup` 是与 `algorithm` 平级的兄弟节点。下面列出的 `formula`、`steps`、`type` 均是 `algorithm` 节点下的简写。

### 8.1 企业 STAT：`M_ENT_KEY_TOTAL`（重点企业总数）

- **打开文件**：`agent-delivery/metrics/algo-results/ALGO-LIB-METRIC-DEPS-L01-metrics.yaml`。
- **定位方式**：搜索 `- metric_id: M_ENT_KEY_TOTAL`，看同一 YAML 块到下一个 `- metric_id:` 前为止。
- **检查内容**：`algorithm.type=STAT`；`formula=COUNT(DISTINCT enterprise_id) WHERE 双阈值命中`；`inputs[]` 为「专利数据、技术交易额」两项。
- **字段期望**：专利数据 `ods_mapping_status=partial`，证据应写 `dwd_patent=0 行 / dwd_patent_legal=0 行`；技术交易额 `pending_ods`；指标级 `dependency_rollup=pending_ods`。
- **怎么判断合理**：STAT 只能做去重计数，不应出现「模型评分」「特征标准化」；双阈值必须能落成两个明确条件，如果 `双阈值命中` 没有写阈值值域，应记「骨架合理、口径待淮政玮补阈值」，不算算法错误。
- **我的分析**：这个指标本质是「满足 A 且满足 B 的企业去重数」，常见于高新技术企业/科技型中小企业认定的组合条件筛选。当前用「专利数 + 技术交易额」是业务可解释的，但没有给出具体数量/金额阈值，不能冒充生产级已定口径；故 `partial + pending_ods` 的诚实判定是正确的。

### 8.2 企业 GRAPH：`TEMP_ALGO_ALGO-ENT-GRAPH-108_1`（企业实体识别构建）

- **打开文件**：同 `metrics.yaml`，搜索 `- metric_id: TEMP_ALGO_ALGO-ENT-GRAPH-108_1`。
- **检查内容**：`algorithm.type=GRAPH`；`formula=GRAPH(实体识别 + 关系抽取 + 图谱构建)`；`steps` 必须非空且至少三步。
- **字段期望**：`steps` 应为「抽取目标实体及属性… / 识别实体间关系… / 写入 Nebula 图库…」；输入为 `pending_ods`；rollup 为 `pending_ods`。
- **怎么判断合理**：GRAPH 的关键判断点是步骤是否写清「实体、关系、存储、输出」，且存储必须是 Nebula，不能是 Neo4j。步骤只写「实体识别 + 关系抽取」一句话要打回。
- **我的分析**：这里三步是图谱构建的标准流水线，符合知识图谱工程惯例；但它不是可执行算法公式，本叶属于 spike 盘点，允许流程级步骤，不能当作生产模型交付。输入仍全为 `pending_ods`，状态诚实。

### 8.3 企业 MODEL：`M_ENT_TECH_POWER_SCORE`（企业技术力评估模型）

- **打开文件**：同 `metrics.yaml`，搜索 `- metric_id: M_ENT_TECH_POWER_SCORE`。
- **检查内容**：`algorithm.type=MODEL`；`steps` 非空；`inputs[]` 中「企业专利数据库数据、科技项目库数据、研发投入数据、企业人才结构档案、技术合作关系数据」应逐条有 `pending_ods`，另有「指标体系与权重参数」为 `n/a`。
- **字段期望**：`steps` 为「定义评价指标体系并归一化 / 按权重聚合 / 输出评分与解释」；指标级 rollup 为 `pending_ods`。
- **怎么判断合理**：MODEL 不能只有 `MODEL(模型计算)` 一句话；必须能看到输入特征、归一化、聚合、输出四段。这里虽然步骤完整，但公式仍是通用骨架，没有具体权重与特征口径，所以只能签「盘点通过、生产未实现」，不能签「可投产」。
- **我的分析**：企业技术力评价通常可从专利数量/质量、研发投入、研发人才、技术合作四类切入，方向合理；但没有给出权重和归一化公式，仍属于定义卡而非算法。权威机构做技术力评价也多为指标体系+专家权重，不是单一权威公式，因此本叶用 `pending_business_definition` 是合适的。

### 8.4 政策 MODEL：`TEMP_ALGO_ALGO-POLICY-DEEP-168_1`（政策效果评估模型）

- **打开文件**：同 `metrics.yaml`，搜索 `- metric_id: TEMP_ALGO_ALGO-POLICY-DEEP-168_1`。
- **检查内容**：`algorithm.type=MODEL`；`steps` 非空；输入应为「政策原文及相关实施文件、政策执行过程数据、宏观经济数据、社会发展指标、环境影响数据」。
- **字段期望**：数据类输入 `pending_ods`，权重/参数类 `n/a`；rollup 为 `pending_ods`；`weights_status=pending_business_definition`。
- **怎么判断合理**：政策效果评估必须同时有「政策文本/执行过程」和「结果性经济社会环境指标」，否则只是政策分类不是效果评估。这里输入维度覆盖了这些方向，但权重和因果口径仍未定义，应标记待业务定义。
- **我的分析**：政策效果评估通常分投入、过程、产出、影响四层；本叶输入已经粗粒度覆盖政策原文、执行、宏观、环境影响，方向合理。国际上常用 OECD 政策评估框架，但对单条政策仍需要因果识别和权重，故不能把通用模型步骤当成已定公式。

### 8.5 产业链 MODEL：`TEMP_ALGO_ALGO-CHAIN-DEEP-117_1`（产业链全景模型构建）

- **打开文件**：同 `metrics.yaml`，搜索 `- metric_id: TEMP_ALGO_ALGO-CHAIN-DEEP-117_1`。
- **检查内容**：`algorithm.type=MODEL`；`steps` 非空；输入应覆盖产业知识图谱、企业、技术、人才、科研机构、服务机构、供应链、市场、行业九个方向。
- **字段期望**：所有数据输入 `pending_ods`；rollup 为 `pending_ods`；无 `full` 假标。
- **怎么判断合理**：产业链全景模型需要多源数据，若输入全是 `pending_ods`，结论必须仍是「待核验」；不能因为模型名字叫「全景」就把 rollup 标 `full`。
- **我的分析**：产业链图谱/全景分析通常会包含主体节点（企业、机构、服务机构）和关系/交易/供应链数据，本叶的输入设计合理。当前这些三方来源都未核验，保持 `pending_ods` 是唯一正确选择。

### 8.6 产业服务 MODEL：`TEMP_ALGO_ALGO-SVC-DEEP-176_1`（人力资源服务机构技术力评价模型）

- **打开文件**：同 `metrics.yaml`，搜索 `- metric_id: TEMP_ALGO_ALGO-SVC-DEEP-176_1`。
- **检查内容**：`algorithm.type=MODEL`；`steps` 非空；输入应至少覆盖「人才资源相关数据」和「客户反馈数据」。
- **字段期望**：人才资源数据 `pending_ods`，客户反馈数据 `none` 且 `gap/impact` 写明缺表；rollup 为 `pending_ods`。
- **怎么判断合理**：对服务机构评价，除了自身专业/人才数据，还应纳入服务对象反馈，若客户反馈数据缺失，评价模型就缺少闭环；不能把仅依赖机构侧数据的模型标成完整。
- **我的分析**：人力资源服务机构技术力评价通常包含专业能力、人才资源、服务结果/满意度。本叶输入覆盖了人才资源，但客户反馈表缺失，所以模型无法完整计算，当前状态诚实。

### 8.7 综合 MIXED：`TEMP_ALGO_ALGO-SYNTH-SYNTH-182_1`（区域科技创新成果综合评价模型）

- **打开文件**：同 `metrics.yaml`，搜索 `- metric_id: TEMP_ALGO_ALGO-SYNTH-SYNTH-182_1`。
- **检查内容**：`algorithm.type=MIXED`；`steps` 非空；输入应覆盖区域基础科学成果、应用科技成果等。
- **字段期望**：`steps` 为「标准化与去重统计 / 按区域、类型、层次、领域聚合 / 综合评价」；rollup 为 `pending_ods`。
- **怎么判断合理**：MIXED 必须能拆成 `STAT + COMPUTE/MODEL` 子项，不能只写一句混合。当前步骤可读，但输入名存在括号内逗号被切碎的问题（例如 `区域基础科学成果数据（论文`、`学术奖项`、`重大科学突破）` 被拆成三条），属于必须修正的命名异常。
- **我的分析**：区域科技创新综合评价本质是「创新要素去重统计 + 标准化加权 + 综合评分」，MIXED 分类正确。当前输入名的括号/逗号被 YAML 列表解析错位，是我发现的开放项，不应由你人工逐条数，但需要你确认是否需要先修名再放行。

### 8.8 综合 API/GRAPHAPI：`TEMP_ALGO_ALGO-SYNTH-GRAPHAPI-116_1`（产业全要素图谱 API 服务开发）

- **打开文件**：同 `metrics.yaml`，搜索 `- metric_id: TEMP_ALGO_ALGO-SYNTH-GRAPHAPI-116_1`。
- **检查内容**：`algorithm.type=API`；`formula=API(graph_query)`；`steps` 非空。
- **字段期望**：`steps` 为「解析图谱查询参数 / 执行子图·路径·中心性查询 / 返回标准化结果」；输入 `pending_ods`；rollup 为 `pending_ods`。
- **怎么判断合理**：API 类型通常是封装外部服务，不展开内部公式；但这里是对内 Nebula 图谱查询 API，步骤写查询解析、路由、结果封装是合规的，不属于把第三方模型伪展开。
- **我的分析**：图谱查询 API 的标准能力就是参数解析 + 图遍历/中心性 + 结果标准化，方向无问题。仍需注意，当前唯一输入 `pending_ods`，接口可以建设，但底层图谱数据未核验前不能称生产可用。

### 8.9 技术链 third_party：`TEMP_ALGO_ALGO-TECH-DEEP-132_1`（技术发展历程模型）

- **打开文件**：`agent-delivery/metrics/algo-results/ALGO-LIB-METRIC-DEPS-L01-requirements.yaml`，搜索 `- requirement_id: ALGO-TECH-DEEP-132`，确认 `coverage_status=third_party`；再回到 `metrics.yaml` 搜索 `- metric_id: TEMP_ALGO_ALGO-TECH-DEEP-132_1`。
- **检查内容**：`algorithm.type=API`；`formula=不展开`；`steps=[]`；输入仍必须存在并逐条有 ODS 判定。
- **字段期望**：技术新闻数据/媒体报道量等 `none` 且写清缺表；专利、科研论文、行业资讯、政策文件发布频率等 `pending_ods`；rollup 为 `pending_ods`。
- **怎么判断合理**：third_party 的唯一红线是「不伪展开自研公式」；只要 `formula=不展开` 且 `steps=[]`，即使有大量 `none`，也不能被擅自改成自研模型。技术发展历程模型若变成我方内部模型，需要新建/扩口径流程，不能在本叶里替代。
- **我的分析**：技术生命周期/发展历程常见分析方式包括专利趋势、论文趋势、政策与技术标准、媒体热度；本叶输入覆盖这些方向，但第三方交付形态未定，故用 API + 不展开 + 多 `pending_ods` 是合规的。

### 8.10 人才 third_party：`TEMP_ALGO_ALGO-TALENT-DEEP-157_1`（人才流动追踪模型）

- **打开文件**：先查 `requirements.yaml` 的 `ALGO-TALENT-DEEP-157`，确认 `coverage_status=third_party`；再查 `metrics.yaml` 的 `TEMP_ALGO_ALGO-TALENT-DEEP-157_1`。
- **检查内容**：`algorithm.type=API`；`formula=不展开`；`steps=[]`；输入应包含社交网络、招聘网站、简历库、人才关联关系链、职业轨迹、招聘信息特征、行业与企业标签。
- **字段期望**：社交网络/招聘网站/简历库/招聘特征为 `none` 且写清缺表；人才关联关系链/职业轨迹/行业标签为 `pending_ods`；rollup 为 `pending_ods`。
- **怎么判断合理**：人才流动追踪属于第三方人才数据能力，我方只做 API 封装与数据缺口评估，不伪展开算法。若后续要自建模型，需再走 F−L/T0-X 扩库流程。
- **我的分析**：人才流动分析通常依赖招聘平台、社交网络、简历库、职业轨迹等敏感三方数据；本叶把外部可爬取源标 `none`、三方库标 `pending_ods`，区分是合理的，不能把这些外部源误标为 `full`。

### 8.11 唐绍祖需要人工衡量、判断的重点（对应工作说明 §2.1）

这 10 条抽检最终要回答四个「人判」问题，机器只能检查结构，不能替你判断：

1. **`algorithm.type` 是否与公式形态匹配**。见下表；若公式写了「评分/预测/聚类」却标 `STAT`，打回；若 third_party 写了自研公式，打回。
2. **公式是否可执行、确定、可复现**。公式中的每个算子、窗口、粒度、过滤条件都要能落到 SQL/Python，不允许「模型计算」「综合评价」这种不可执行词单独充当完整公式。
3. **业务口径是否成立**。输入是否覆盖指标定义声称的维度，是否遗漏关键结果性数据，权重/阈值是否仍待业务定义。
4. **是否诚实声明成熟度**。`pending_ods` 不得被写成 `full`；定义卡骨架不得被写成生产模型；`n/a` 的业务参数/模型超参不得被当成三方源映射。

| `algorithm.type`         | 唐绍祖人判标准                                           | 本批常见风险                  |
| -------------------------- | -------------------------------------------------------- | ----------------------------- |
| `STAT`                   | 只做计数/占比/排名/简单聚合，公式应能 SQL 直译           | 把复杂评分误标 STAT           |
| `COMPUTE`                | 固定公式（加权/标准化/阈值），无训练模型                 | 权重未定却写成可计算          |
| `MODEL`                  | 评分/预测/聚类；`steps` 必须写输入、归一化、聚合、输出 | 只有通用三步，无具体特征/权重 |
| `GRAPH`                  | 实体/关系/子图/路径；必须写 Nebula 存储与输出            | 一句话「图谱构建」            |
| `API`/`third_party`    | 封装调用；`formula=不展开`，不伪展开内部公式           | 第三方被写成本地模型          |
| `MIXED`                  | 必须可拆为 STAT + COMPUTE/MODEL 子项                     | 一句「综合评估」不拆分        |
| `LITERATURE`/`UNKNOWN` | 尚未判定，禁止开工实现                                   | 本批不出现                    |

判断公式合理性时可对照的外部/行业框架（不是要求完全等同，而是判断「是否走了同类通用路径」）：

- `STAT`：优先对统计年鉴、普查/行政登记等官方计数口径；合理性看是否只做筛选、去重、计数/占比/排名，且每个过滤条件可落到一个明确字段/值域。
- `COMPUTE`：可参考 `z-score`、`min-max`、熵权法、层次分析法（AHP）等标准化/加权方法；若权重未定却写成可计算，应视为「公式骨架成立、权重待业务定义」。
- `MODEL`：评分/预测类可对照 OECD 政策评估框架、世界知识产权组织（WIPO）及全球创新指数（GII）等指标体系思路；关键是输入、归一化、聚合、输出四段闭环，而不是“模型计算”四个字。
- `GRAPH`：可对照图论中的中心性、路径、子图等通用方法（本项目落地必须用 Nebula，禁止 Neo4j）；合理性看是否写清实体、关系、存储、输出。
- `API`/`third_party`：参照主流人才/企业/专利数据服务商的交付形态；合理性看是否封装接口、列清输入和数据缺口，不伪展开内部算法。
- `MIXED`：可参照国家统计局综合评价、GII 等多层复合指数；合理性看是否能拆成 STAT + COMPUTE/MODEL 子项，而不是一句“综合评估”。

### 8.12 机器代验收与两遍复核结果（唐绍祖无需人工重复）

以下数量、重复项、缺项、命名异常已由我代唐绍祖机器核验并复核两遍，你只需在报告上确认，不需要再逐条数：

- 两遍结果一致：表1 需规 `97` 条，`requirement_id` 无重复；八维叶数 `11/9/16/13/11/14/10/13`。
- 表1 覆盖：`full=60`、`third_party=37`、`partial=0`、`missing=0`。
- 表2 指标：`101` 条，`metric_id` 无重复。
- `algorithm.type`：`API=38`、`GRAPH=8`、`MIXED=10`、`MODEL=37`、`STAT=8`。
- `MODEL/GRAPH/MIXED` 缺 `steps`：`0` 条。
- 输入级 ODS 五档：`full=1`、`partial=3`、`none=37`、`pending_ods=334`、`n/a=94`，合计 `469`。
- 指标级 `dependency_rollup`：`full=1`、`partial=2`、`none=1`、`pending_ods=91`、`n/a=6`。
- 表3：`confirmed_unmet=40`、`pending_verify=334`；`gap_id` 无重复。
- xlsx 四 sheet 数据行：`469 / 40 / 334 / 9`。
- 六条基础叶（政策/产业链/产业服务/技术/机构/人才 base）已将「业务参数/模型超参输入」的 rollup 从错误的 `full` 修正为 `n/a`，修正后所有 `inputs[]` 全 `n/a` 的指标均 rollup `n/a`，无规则违背。
- 合规红线（机器复核两遍）：未改 `metrics/registry/cfg_metric-*-seed.yaml`、未改 `metrics/registry/metric-readiness-matrix-*.yaml`、未改 `agent-delivery/task-registry.yaml`；未写业务代码；`pending_ods` 未混入「不满足」；A2 missing 未混入 ODS 表。工作树中已存在的 `UU` / 未跟踪文件不属于本叶交付，验收时不动、不暂存、不 push。

机器发现、但不属于「验收打回」的命名异常开放项（供淮政玮/后续语义层决定，不要求唐绍祖人工核数）：

- 101 条 `definition` 句末均带中文句号，属于中文标点可读性风格，暂不改。
- 75 条 `input_name` 与 75 条 `required_field` 尾部残留中文句号，例如「指标体系与权重参数。」「环境影响数据。」「行业。」，疑似整型时遗留；建议后续清理，但当前不改变状态判定。
- `n/a` 输入共 94 条，多为「权重/阈值/超参/指标体系」，`source_system` 写成「业务参数/模型超参」；其中六条基础叶按本教程 schema 处理为指标级 rollup `n/a`。这些输入是语义参数而非 ODS 源，应在后续语义层明确是否指向上游 `metric_id` 或统一为 `parameters`，本叶暂不冒充生产级公式。
- `TEMP_ALGO_ALGO-SYNTH-SYNTH-182_1` 等输入名中的括号内逗号被切碎，属于命名/结构化待办，不在数量核验范围内。

**抽检不合格要打回**：STAT 出现 Python 模型逻辑、MODEL/GRAPH/MIXED 缺 steps、third_party 被伪展开成自研公式、第三方维没列 inputs、把 `pending_ods` 写成 `full`、输入名含括号逗号切碎而不登记开放项。

---

## 9. 验收结论与放行

### 通过

满足上面五步 + 抽检十条后：

1. 在 `ALGO-LIB-METRIC-DEPS-L01.md` 上会签（确认 `review`）。
2. push `gkx-orchestration`（只推 `algo-results/` 下本叶交付文件；工作树里与本叶无关的 `UU` 冲突文件不要动、不要 revert、不要 stash）。
3. 通知淮政玮，附 `ALGO-LIB-METRIC-DEPS-L01-ods-status.xlsx` + `ALGO-LIB-METRIC-DEPS-L01-ods-gaps.md`，并明确：`pending_ods` 是「待核验」，不是「已确认缺口」。

### 打回

任一条不合格，列出「文件 / 行或 metric_id / 问题 / 期望值」四项即可，不必口头泛泛说「有问题」。

---

## 10. 关键数字快照（核对时逐项对照）

- SRS 叶数：97（八维：11/9/16/13/11/14/10/13）
- 指标数：101，无重复 `metric_id`
- ODS 输入总数：469
- ODS 五档：`full=1`、`partial=3`、`none=37`、`pending_ods=334`、`n/a=94`
- 不满足（none+partial）：40
- 待核验（pending_ods）：334
- `dependency_rollup`：`full=1`、`partial=2`、`none=1`、`pending_ods=91`、`n/a=6`
- `algorithm.type`：`API=38`、`GRAPH=8`、`MIXED=10`、`MODEL=37`、`STAT=8`
- xlsx 四 sheet 数据行：469 / 40 / 334 / 9（合计叶数=97）

---

## 11. 快速机器核对（可选，一条命令）

在 `gkx-orchestration` 仓库根目录执行（需 Python + PyYAML + openpyxl）：

```python
import yaml, collections, openpyxl
base = 'agent-delivery/metrics/algo-results/'

req = yaml.safe_load(open(base+'ALGO-LIB-METRIC-DEPS-L01-requirements.yaml', encoding='utf-8'))
met = yaml.safe_load(open(base+'ALGO-LIB-METRIC-DEPS-L01-metrics.yaml', encoding='utf-8'))
gap = yaml.safe_load(open(base+'ALGO-LIB-METRIC-DEPS-L01-ods-gaps.yaml', encoding='utf-8'))

def lst(o):
    if isinstance(o, list): return o
    for v in o.values():
        if isinstance(v, list): return v
    return []

rl, ml, gl = lst(req), lst(met), lst(gap)
print('SRS', len(rl), 'metrics', len(ml), 'gaps', len(gl))
print('req dup', [k for k,c in collections.Counter(r['requirement_id'] for r in rl).items() if c>1])
print('metric dup', [k for k,c in collections.Counter(m['metric_id'] for m in ml).items() if c>1])

ods = collections.Counter()
for m in ml:
    for i in m.get('inputs', []):
        ods[i.get('ods_mapping_status')] += 1
print('ods', dict(ods))
print('rollup', dict(collections.Counter(m.get('dependency_rollup', {}).get('ods_mapping_status') for m in ml)))
print('type', dict(collections.Counter((m.get('algorithm') or {}).get('type') for m in ml)))
print('bad_steps', [m['metric_id'] for m in ml if (m.get('algorithm') or {}).get('type') in ('MODEL','GRAPH','MIXED') and not (m.get('algorithm') or {}).get('steps')])
print('rollup_suspicious', [m['metric_id'] for m in ml if set(i.get('ods_mapping_status') for i in m.get('inputs', [])) == {'n/a'} and (m.get('dependency_rollup') or {}).get('ods_mapping_status') != 'n/a'])

wb = openpyxl.load_workbook(base+'ALGO-LIB-METRIC-DEPS-L01-ods-status.xlsx', data_only=True)
for ws in wb.worksheets:
    print(ws.title, ws.max_row-1, 'cols', ws.max_column)
```

期望输出应与 §10 快照完全一致；`bad_steps` 必须为空、两个 dup 列表必须为空、`rollup_suspicious` 必须为空。

---

## 附：本教程对应真源

- DoD 清单：`agent-delivery/agent-handoffs/算法库联调-ALGO-LIB/给人说明-指标与算法工作类型与流程梳理.md` §9.4 / §9.5
- 字段与枚举：`agent-delivery/metrics/algo-results/ALGO-LIB-METRIC-DEPS-L01-schema.md`
- 派单说明：`agent-delivery/agent-handoffs/算法库联调-ALGO-LIB/给人说明-ALGO-LIB-METRIC-DEPS-L01-2026-08-21.md`

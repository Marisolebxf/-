# 政策效果推演（M_POLICY_SIMULATE）

> **归属与维护**
> - **维护者**：唐绍祖
> - **适用系统**：科技信息展示系统（单系统件；抬头治理批次 20261027）
> **指标画像**
> - **类型**：SIM（省级基线 × 情景参数 × 弹性系数）｜ **域**：政策（POLICY）｜ **UI 挂载**：政策分析页「效果推演」情景面板（设计位）、推演结果曲线图（设计位）
> - **数据支持度**：**完全不支持**｜ **公式定义人**：`gkx-orchestration/agent-delivery/metrics/calc-logic/POLICY/M_POLICY_SIMULATE.md`（基线 + 弹性推演两步）；王惠正本 `gkx-orchestration/agent-delivery/metrics/calc-logic/POLICY/M_POLICY_SIMULATE.md（王惠正本已演化并入）`（V1.0-20260904）
> - **同域边界**：与 `M_POLICY_INTENSITY_SCORE` / `M_POLICY_INTENSITY_INDEX` 是上下游——那两件出「力度」，本件拿力度当基线 `B` 做外推。两件都判完全不支持，因此本件连基线都拿不到；这不是「上游质量差」，是「上游不存在」。
> - **一句话结论**：推演公式 $\Delta Y=e\cdot(X_{sim}-X_{base})/X_{base}$、$Y_{sim}=B(1+\Delta Y)$ 需要四样东西——基线 `B`、情景 `X`、弹性 `e`、校验 `Y`。gkx 280 表里对应的 5 张表**一张都没有**；live 侧其中 4 张 0 行、唯一有行的 `policy_intensity` 631 行属造数面且关键列全 NULL；另有 `policy_simulate` 36 行亦为造数面。四段输入皆空，判**完全不支持**。
> **复现与产物**
> - **复现脚本**：`metrics/repro/M_POLICY_SIMULATE.py`（否定性证据探针）｜ **产物**：`metrics/repro/out/M_POLICY_SIMULATE_out.json`｜ **共用底数**：`code/_snapshots21/policy_dims_20261023.json`、`policy_struct_20261023.json`、`policy_fields_a23_20261021.json`
> **版本与分级**
> - **分级**：单系统（未入 D1–D5 跨系统分级清单，不涉及三系统口径分歧）｜ 全量分类见 `METRIC-SRS-GAP-L01/产物/20261027三系统兼容升级/分级清单（过程文件 _分级清单.json 随批归档）`
> - **20261027 批次**：抬头治理件（计算口径与产物数值未改动，与 20261021 基线一致）

---

> 指标最终唯一解释口径（真源）。20261027 批（三系统兼容升级版）覆盖；骨架对齐 `metrics/registry/cfg_metric-POLICY-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`M_POLICY_SIMULATE.md`；复现脚本 `metrics/repro/M_POLICY_SIMULATE.py` → `metrics/repro/out/M_POLICY_SIMULATE_out.json`。（**正本全文见本件下方「最新指标调研报告」节**；复现脚本与产物已入仓 `metrics/repro/`，见「溯源与复现」表）

> **路径说明（2026-10-24）**：本件所述 `code/…` 相对路径已实物化入仓——复现脚本 `metrics/repro/M_POLICY_SIMULATE.py`、产物 `metrics/repro/out/M_POLICY_SIMULATE_out.json`（见「溯源与复现」表）；`第三方库指标计算过程/` 正本全文已并入本件「详细计算过程」节。本地工作区目录不对外；验收以本仓为准。

---

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_POLICY_SIMULATE |
| 指标名称 | 政策效果推演 |
| 所属域 | POLICY（政策分析） |
| 一级模块 | 政策 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **完全不支持** |
| UI 挂载 | 政策分析页「效果推演」情景面板（设计位）、推演结果曲线图（设计位） |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/POLICY/M_POLICY_SIMULATE.md` |

## 口径定义

推演是**四段链**：基线、情景、弹性、校验。四段分别对应 `policy_intensity`、`policy_simulation_param`、弹性系数表、`policy_prediction_indicator`。gkx 侧四张全无；live 侧前两张有表但一张造数、一张 0 行，后两张 0 行。链断在第一段，后面三段无从谈起。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `M_POLICY_SIMULATE.md` §二（M_POLICY_SIMULATE.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_bid_`
- `dwd_policy_base`

## 待建表字段

按 20261021 判档：关键依赖维在开发库+三方库均不可构建，暂无待建清单；补数据方向见源件 §四。

## 数据支持度与缺口

- **判档**：完全不支持
- **判档理由**：推演链四段输入（基线 B、情景 X、弹性 e、校验 Y）在 gkx 与 live 两侧都拿不到可用数据：五张依赖表在 gkx 280 表中 0 张；live 侧三张同名表 0 行、另两张属造数批次且关键列不可用；政策表 33 列无金额列，「扶持力度」无量化源。没有 B 与 e，公式无法取值 → 完全不支持。
- **基期声明**：推演本应输出未来年份曲线，但基线表不存在、参数表 0 行，连基期都定不下来，故 used/missing 均为空。这不是「基期缺失」，是「推演链未建立」。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261027_指标整体开发进度调研（三系统兼容升级版，正本见文末「最新指标调研报告」） |
| 正本 MD | `M_POLICY_SIMULATE.md` |
| 复现脚本 | `metrics/repro/M_POLICY_SIMULATE.py` |
| 复现产物 | `metrics/repro/out/M_POLICY_SIMULATE_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

---

---

# 最新指标调研报告

> 本节为 20261027 批正本全文（三系统兼容升级版；替换 20261021 调研正本 · 2026-10-24 并入版）。口径与数值以本节为准；`metrics/repro/` 内脚本与产物已同步本批。

## 〇、数据支持度与四判定口径（本文件沿用，勿忘）

> 口径源自《总览说明-20261019》「表字段口径」；**完全转换支持**以用户澄清为准：**结构 + 当前数据量都已足够，现在就能通过转换/加工得到该指标**；数据量不够则不得归入此类。

### 0.1 数据支持度四档

| 档位 | 定义 |
|---|---|
| **完全直接支持** | **开发库+三方库（gkx）**中直接就有该指标（或 100% 语义一致指标/结果面）可用，且数据量完全支持直查/直算 |
| **完全转换支持** | 两库均无现成结果面，但依赖侧的表结构与当前数据量均已足够，现在即可通过转换与加工生成该指标；数据量不足不得入本档 |
| **部分支持** | 无论如何构建，始终有部分依赖维度无法从**开发库+三方库（gkx）**得到足够数据 |
| **完全不支持** | 该指标及其关键依赖维度，在**开发库与三方库（gkx）**均无法构建（结构与数据均不具备可算闭环） |

> **数据源口径**：本件支持度按「开发库 + 三方库（gkx，183.240.141.251:3318 只读）」评估，仅排除 `demo_*`；本机开发库事实面为空壳（`gkxlumenx_dwd/ods/ads` 逐表实测非空 0 张），实际取数面为 gkx。

### 0.2 四判定（拆分证据）

| 判定项 | 定义 |
|---|---|
| **表结构直接支持（开发库+三方库）** | 表结构直接有该指标对应字段，或 100% 语义一致字段。 |
| **表数据直接支持（开发库+三方库）** | 不但有结构，字段当日还有**足够数据**支撑直算（非空壳）。 |
| **依赖表结构支持（开发库/三方库）** | 间接依赖源表的结构：有 / 仅三方库有（需转换）/ 均无。 |
| **依赖表数据支持（开发库/三方库）** | 依赖源表当日数据：是（量足）/ 部分（行数受限或字段缺失）/ 需先入湖但源侧量足 / 否。 |

### 0.3 本指标套用（一句话）

推演是**四段链**：基线、情景、弹性、校验。四段分别对应 `policy_intensity`、`policy_simulation_param`、弹性系数表、`policy_prediction_indicator`。gkx 侧四张全无；live 侧前两张有表但一张造数、一张 0 行，后两张 0 行。链断在第一段，后面三段无从谈起。

---

## 摘要

「政策效果推演」是政策评估族里最像「模型」的一件：它不算现状，它算「如果政策力度提高 20%，效果会提高多少」。正本给了两步公式——先取省级政策力度指数当基线 $B$，再用弹性系数 $e$ 把情景参数的变化率映射成效果变化率，最后 $Y_{sim}=B\times(1+\Delta Y)$。

这个公式本身没问题，问题是它的四段输入在库里全都拿不到。

第一段是基线 $B$。正本要求 `policy_intensity` 表里 `scope_type='province'` 的 `intensity_index`。gkx 280 表里**没有** `policy_intensity`——含 policy 的四张表全是 `dwd_policy_base` 及其备份。live 侧有 `gkxlumenx_ads.policy_intensity`（631 行），但注册表登记为 `Mock @ batch=mock_20260623`、`is_mock: true`，`MOCK_TABLE_REGISTRY.md` 记录的指纹是 `intensity_index` 全 NULL、`scope_type` 恒为 `province`。一张「力度指数全空」的表，连基线都取不出来。

第二段是情景 $X$。正本要求 `policy_simulation_param` 承载 `support_intensity`（扶持力度）、`coverage_scope`（覆盖面）等。gkx 无此表；live 有 `gkxlumenx_dwd.policy_simulation_param`，**0 行**。参数表空，等于没有情景可设。

第三段是弹性 $e$。这是最容易被忽略的一段——很多人以为 $e$ 是个可以「先取 1」的常数。取 1 意味着「扶持力度提高 10%，效果就提高 10%」，这是一个极强的假设，而且没有任何依据。要标定 $e$，至少需要「政策参数变化」与「效果变化」的配对观测；库内既无参数记录（0 行），也无效果时间序列（`policy_metric_timeseries` 只存在于 live 造数面、93 行）。没有配对序列，回归无从谈起；正本也写明 $e$ 待 QPOL-02 签认，而 QPOL-02 未签。

第四段是校验 $Y$。正本要用 `policy_prediction_indicator` 的 `predicted_upper` / `predicted_lower` 给预测区间。gkx 无此表；live 同名表 **0 行**。没有校验数据，推演结果无法回测——一个不能回测的模型，输出的是意见不是结论。

还有一层更根本的问题：**扶持力度无法量化**。`dwd_policy_base` 33 列里金额类列 **0 个**（全库 123 个金额类列全部落在 `dwd_bid_*` 招标表）。「扶持力度」这个情景参数，本来最自然的度量是金额，库内没有；退到「政策条数」又不成立——条数是供给规模，对「力度提高 10%」这种参数化情景不产生响应。

本件因此也做了一个「退一步」的演示：如果把省级政策条数当基线，会得到什么。31 个省级单位共 17,476 条政策，北京最多（1,932 条）。但条数无法对情景参数求导，$\Delta Y$ 对条数没有意义，所以这个替代口径只是把一个不能算的东西换成一个不该算的东西。

一句话收口：这不是「模型不准」，是「模型没有输入」。四段链断在第一段，任何推演值都是编的。

| 口径要点 | 取值 |
|---|---|
| 推演链段数 | 4（B / X / e / Y） |
| gkx 依赖表 | 0 / 5 |
| live 可行表 | 0 / 5 |
| `policy_intensity`（live） | 631 行，造数面，`intensity_index` 全 NULL |
| `policy_simulation_param` | 0 行 |
| `policy_prediction_indicator` | 0 行 |
| `policy_simulation_result` | 0 行 |
| `policy_intensity_eval` | 0 行 |
| gkx 总表数 / live 总表数 | 280 / 267 |
| 政策表列数 / 金额列 | 33 / 0 |
| 全库金额列（招标表） | 123 |
| 省级政策条数 | 17,476（31 省） |
| 政策文件类条数 | 7,525（37.625%） |
| 判档 | 完全不支持 |

---

## 一、需求定义概述

### 1.1 所属功能模块（要开发什么）

功能模块是**政策分析 → 政策效果推演**。设计上应有一个情景面板：用户拖动「扶持力度」「覆盖面」两个滑块，页面实时给出推演效果值、相对基线的变化率与预测区间曲线。本件判定该面板**无法渲染**——滑块没有参数表可写，曲线没有基线可起。

### 1.2 为什么需要这个指标

第一，政策制定是事前行为，决策者最想知道的不是「过去怎么样」，而是「如果这么做会怎么样」。推演是唯一能回答这个问题的形态。

第二，它是政策评估族的终点。前面几件做的是「现状测量」（数量、结构、力度、关联），推演做的是「反事实推断」。没有推演，整个族只能描述不能预测。

第三，它是最容易被「公式能写、参数随便给」骗过去的一件。$\Delta Y=e\cdot\Delta X/X$ 三行代码就能算，$e$ 取 1、$X$ 取条数，立刻出一条曲线。这条曲线看起来专业，实际是把两个没有关系的量做了个除法。本件要把这条路堵死。

### 1.3 需求文档是否给出定义方法

**给了完整的两步公式与四段输入，并明确标注弹性系数待签。** 正本写得很清楚：基线取 `policy_intensity` 的 `intensity_index`，情景由 `policy_simulation_param` 承载，弹性 $e$ 待 QPOL-02，输出写 `ads.policy_simulate(baseline_value, simulated_value, delta_rate, curve)`。

正本还有一句关键的兜底：「若无省级，按 `rank_no` 取全局力度指数分位。」这句话说明作者预见到省级基线可能缺，给了降级路径。但降级路径的前提是「全局力度指数存在」，而 `policy_intensity` 整表在 gkx 不存在、在 live 是造数面——兜底也落空。

### 1.4 类似指标权威机构构建方法可行性分析概要

| 方法族 | 代表机构/文献 | 口径要点 | 与本指标的差 | 贴合度 |
|---|---|---|---|---|
| A 政策弹性模型 | 政策评估计量经济学 | 用历史数据估政策变量对产出的弹性 | 需配对时间序列，库内无 | 中（方法对、数据无） |
| B CGE 可计算一般均衡 | 国务院发展研究中心等 | 多部门均衡模型，参数靠标定 | 需投入产出表，库内无 | 低 |
| C 情景分析（Scenario） | 战略研究常用 | 定性情景 + 专家打分 | 可做，但产出不是数值曲线 | 中（形态） |
| D 政策力度指数外推 | 正本采用 | 基线 × 弹性 × 参数变化率 | 需基线、参数、弹性三样 | 零（三样全无） |
| E 机器学习预测 | 时间序列/回归 | 用历史政策与效果训练 | 无效果标签 | 零（无标签） |

**三句结论**：① A 族是方法论正解，但它要求的历史配对序列在库内不存在；② C 族能给方向性判断，但产出是文字不是曲线，与需求形态不符；③ D 族是正本选择，它在有力度指数的库里成立，在本库不成立——连基线表都没有。

### 1.5 引用来源（可核验）

| # | 来源 | 位置 | 用途 |
|---|---|---|---|
| 1 | `gkx.information_schema.tables` | 183.240.141.251:3318 | 证明 280 表无 5 张依赖表 |
| 2 | `gkx.dwd_policy_base` | 同上 | 33 列，无金额列 |
| 3 | `_work_gkx21/GKX_INVENTORY.json` | 本任务目录 | gkx 逐表 COUNT(*) |
| 4 | `_work_gkx21/LIVE_INVENTORY.json` | 本任务目录 | live 267 表逐表行数 |
| 5 | `_work_gkx21/DATA_FACTS_gkx21.md` §3.62 | 本任务目录 | 123 个金额列全在招标表 |
| 6 | `_work_gkx21/MOCK_TABLE_REGISTRY.md` | 本任务目录 | 造数表指纹 |

### 1.6 本报告的口径与边界（须与甲方会签）

**推测定义**：设省级单位 $p$ 的基线力度为 $B_p$，情景参数为 $X_{sim}$、基线参数为 $X_{base}$，弹性为 $e$，则

$$\Delta Y_p=e\cdot\frac{X_{sim}-X_{base}}{X_{base}},\qquad Y_{sim,p}=B_p\times(1+\Delta Y_p)$$

预测区间取 $[Y_{sim}\cdot(1-\delta),\,Y_{sim}\cdot(1+\delta)]$，$\delta$ 由 `policy_prediction_indicator` 给出。

**边界**：① 本件 $B_p$ 不可得，故整链不可算，产物写 `null`；② 不把弹性 $e$ 预设为 1 或任何常数——那是未经验证的假设；③ 不用政策条数当基线（见 §4.3）；④ 不用 live 造数表；⑤ 不输出任何「示意曲线」。

---

## 二、计算过程（从缺：为什么不出推演值）

按派单书 F4，「完全不支持」档不写长计算过程，只留判定链条。本件的链条四段，逐段核。

第一段（基线 $B$）：查 gkx 280 表，`policy_intensity` 不存在；查 live，同名表 631 行但 `intensity_index` 全 NULL、`scope_type` 恒 `province`。

第二段（情景 $X$）：查 gkx，`policy_simulation_param` 不存在；查 live，同名表 0 行。参数无从设定。

第三段（弹性 $e$）：查两库，无系数表；查效果序列，`policy_metric_timeseries` 只在 live 造数面（93 行），与参数表 0 行无法配对，回归与标定均不成立；QPOL-02 未签。

第四段（校验 $Y$）：查 gkx，`policy_prediction_indicator` 不存在；查 live，同名表 0 行。无预测区间可校验。

四段全断，公式无法取值。产物的 `tables` 段逐表记录 `in_gkx` / `live_rows` / `usable`，`elasticity_probe` 段记录为什么 $e$ 不能取常数，`alternative_baseline_demo` 段记录「退到条数」为什么也不成立。

---

## 三、数据支撑情况

### 3.1 四判定落表

| 判定项 | 结论 | 证据 |
|---|---|---|
| 表结构直接支持（开发库+三方库） | **否** | 两库均无 `policy_intensity` / `policy_simulation_param` 等结果面 |
| 表数据直接支持（开发库+三方库） | **否** | live 侧 4 张 0 行、1 张造数面（631 行） |
| 依赖表结构支持（开发库/三方库） | **否** | 5 张依赖表在 gkx 全无 |
| 依赖表数据支持（开发库/三方库） | **否** | 无基线、无参数、无弹性、无校验 |

### 3.2 五张依赖表逐表核对

| 表 | 角色 | gkx | live 行数 | 可用性 |
|---|---|---|---|---|
| `policy_intensity` | 基线 $B$ | 不存在 | 631 | 造数面，`intensity_index` 全 NULL |
| `policy_intensity_eval` | 力度明细（三维分） | 不存在 | 0 | 空表 |
| `policy_simulation_param` | 情景 $X$ | 不存在 | 0 | 空表 |
| `policy_prediction_indicator` | 校验 $Y$ | 不存在 | 0 | 空表 |
| `policy_simulation_result` | 推演结果 | 不存在 | 0 | 空表 |

5 张表里 4 张在 live 是 0 行，唯一的 631 行是造数面。gkx 侧一张都没有。这张表可以直接回答「为什么判完全不支持」——不是「数据少」，是「表都没有」。

### 3.3 弹性系数的标定条件

| 条件 | 要求 | 实测 | 结论 |
|---|---|---|---|
| 参数记录 | `policy_simulation_param` 有历史情景 | 0 行 | 不满足 |
| 效果序列 | 政策效果的时间序列 | 仅 live 造数面 93 行 | 不满足 |
| 配对观测 | 同一对象、同一时点的参数与效果 | 无 | 不满足 |
| 签认 | QPOL-02 | 未签 | 不满足 |
| 先验区间 | 专家给定的 $e$ 范围 | 无 | 不满足 |

四项数据条件全不满足，第五项（专家先验）也没有。这种情况下 $e$ 只能拍一个数，而拍出来的数会决定整条曲线——$e=0.5$ 与 $e=2$ 给出的推演值差 4 倍。一个由拍脑袋参数决定的模型，不能作为决策依据。

### 3.4 扶持力度的量化源

| 候选量化源 | 是否存在 | 说明 |
|---|---|---|
| 政策表金额列 | **否** | 33 列内金额类列 0 个 |
| 政策—扶持金额表 | **否** | 两库均无 |
| 招标金额（`dwd_bid_*`） | 是（123 个金额列） | 语义是采购，不是扶持，不得混用 |
| 政策条数 | 是 | 供给规模，对情景参数无响应 |
| 政策文件类条数 | 是（7,525） | 同上，只是筛掉了事务通知 |

前两行是正解但不存在，第三行是常见误用——招标金额是「政府买东西花了多少钱」，扶持金额是「政府给企业多少钱」，两者方向相反，混用会得出「采购越多扶持越强」的荒谬结论。第四、五行是最省事的替代，但它们不随情景参数变化，$\Delta X/X$ 恒为 0 或无穷。

### 3.5 省级条数基线演示

| 省 | 政策条数 | 省 | 政策条数 |
|---|---|---|---|
| 北京市 | 1,932 | 上海市 | 1,842 |
| 广东省 | 1,612 | 山东省 | 1,284 |
| 浙江省 | 1,214 | 陕西省 | 861 |
| 江苏省 | 852 | 河南省 | 748 |
| 天津市 | 666 | 安徽省 | 630 |
| 福建省 | 612 | 其余 20 省 | 合计 5,223 |

31 个省级单位合计 17,476 条，另有 2,524 条无省级归属（其中 2,174 条是国家级）。这张表看起来可以当基线——但它测的是「发文多少」，不是「力度多强」。北京 1,932 条不等于北京力度指数最高；事实上发得越多往往说明单条越细，力度可能更分散。

### 3.6 与开发库 live 的差异

| 能力 | gkx | live | 结论 |
|---|---|---|---|
| 政策主表 | 20,000 行 | 0 行 | gkx 有源 |
| 力度基线 | 无表 | 631 行造数 | 两侧均不可用 |
| 情景参数 | 无表 | 0 行 | 两侧均不可用 |
| 推演结果 | 无表 | 36 行造数 | 两侧均不可用 |
| 预测校验 | 无表 | 0 行 | 两侧均不可用 |

两侧的缺口形态不同：gkx 有源无果，live 有果但假。本件需要的是「果」，所以两侧都不能用。这也是为什么不能只看一侧就下结论——只看 gkx 会漏掉 live 的 36 行，只看 live 会误以为有推演结果。

---

## 四、数据缺失情况

### 4.1 缺口的后果归因

后果一：**情景面板无法上线**。滑块没有参数表可写，拖动后无处保存。

后果二：**曲线图无法渲染**。没有基线 $B$，$Y_{sim}$ 的起点不存在。

后果三：**下游依赖推演的件连带失效**。`M_POLICY_DS_11_POLICY_EVAL_015` 的临时读面写的是 `policy_simulate.curve` 与 `explanation`，本件判完全不支持后，那件只能退到正文环节词代理，不能读推演曲线。

### 4.2 数据陷阱（本批实测，须写入下游复用说明）

1. **`policy_intensity` 在 gkx 不存在**：王惠正本的 SQL 直接写 `FROM gkx.policy_intensity`，在 gkx 上会报「表不存在」。
2. **live 的 631 行是造数面**：`intensity_index` 全 NULL、`scope_type` 恒 `province`、`delta_rate` 只有三个取值。
3. **政策表 33 列无金额列**：不要把 `dwd_bid_*` 的招标金额当扶持金额。
4. **`policy_support` 全 JSON null**：扶持对象取不出，`support` 边与扶持力度都无从生成。
5. **`implementation_date` 全零日期**：实施时间参数也没有真值可用。
6. **`policy_prediction_indicator` 0 行**：预测区间无法校验，模型不可回测。

### 4.3 为什么不用政策条数当基线

条数是最容易拿到的数：17,476 条省级政策，按省分组就有 31 个「基线值」。本件**明确拒绝**，理由有四：第一，条数是供给规模，力度是效果强度，北京条数最多不代表力度最强；第二，条数对情景参数（扶持力度、覆盖面）不产生响应，$\Delta X$ 无定义；第三，条数已经由 `M_POLICY_TOTAL_COUNT`、`M_POLICY_NATIONAL_DIST` 等件发布，再用它顶替推演基线等于同一组数贴两个标签；第四，一旦这么做，推演曲线会变成「假设每省多发 10% 政策，效果提高多少」——这不是政策推演，是发文计划。

### 4.4 若甲方补齐后的口径升级路径

第一步建 `policy_intensity` 并填入真实 `intensity_index`（现 live 同名表该列全 NULL）；第二步建 `policy_simulation_param` 并录入情景参数（现 0 行）；第三步 QPOL-02 签认弹性 $e$ 的口径与取值，无历史配对序列时至少给专家先验与区间；第四步建 `policy_prediction_indicator` 存预测值与上下界，才能回测；第五步补政策金额列或「政策—扶持金额」表，扶持力度才有量化源。五步做完，本件可从「完全不支持」升级为「完全转换支持」。

---

## 五、王惠方法对照（V1.0-20260904）

### 5.1 王惠原文要点

王惠正本把本件定义在「政策分析 / 政策效果推演」，更新频率日，输出 `ads.policy_simulate(baseline_value, simulated_value, delta_rate, curve)`。四步：

| 步 | 内容 | 源 |
|---|---|---|
| 第一步 | 取 `policy_intensity` 中 `scope_type='province'` 的 `intensity_index` 为基线 | `gkx.policy_intensity` |
| 第二步 | 情景参数 `support_intensity` / `coverage_scope` | `policy_simulation_param` |
| 第三步 | $\Delta Y=e\cdot(X_{sim}-X_{base})/X_{base}$，$Y_{sim}=B(1+\Delta Y)$ | 弹性 $e$ 待 QPOL-02 |
| 第四步 | 写 `ads.policy_simulate` | — |

### 5.2 与本件（calc-logic 正本）的差异

| 项 | 王惠 V1.0 | calc-logic 正本 | 差异性质 |
|---|---|---|---|
| 基线来源 | `gkx.policy_intensity`（直接写 gkx 库名） | `policy_intensity`（未指定库） | 王惠假定 gkx 有该表，实测无 |
| 降级路径 | 「若无省级，按 `rank_no` 取全局分位」 | 同 | 一致，但兜底也落空 |
| 弹性 | 待 QPOL-02 | 待 QPOL-02 | 一致 |
| 输出表 | `ads.policy_simulate` | 同 | 一致 |

两版公式完全一致，差异只在**库名假设**：王惠把 `policy_intensity` 写成 `gkx.policy_intensity`，而 gkx 280 表里没有这张表。这说明正本写作时假定了「力度表已存在」，而这个假定在本轮换源后不成立。

### 5.3 选用建议

**建议采用 calc-logic 正本的公式，但把基线来源改成「待建 `policy_intensity`」，不沿用王惠 SQL 里的 `gkx.policy_intensity` 写法。** 理由有三：第一，实测 gkx 无此表，照抄 SQL 会直接报错；第二，把库名写死会让将来换源时再次失效；第三，正本已经给了降级路径，实现时应把「基线来源」做成可配置，而不是硬编码。

另需与甲方确认：若 QPOL-02 长期未签，是否允许「不给 $e$、只给基线」的半成品？本件建议**不允许**——没有 $e$ 就没有推演，只给基线那是 `M_POLICY_INTENSITY_INDEX` 的活。

---

## 六、复现与出处

### 6.1 复现步骤（本件是探针，不是推演脚本）

```bash
cd /Users/samuel_tang/my_project/gkx-lumen/（20261021 批调研区，成果已入 metrics/ 与 METRIC-SRS-GAP-L01/产物/）
python3 code/M_POLICY_SIMULATE.py    # 产出 metrics/repro/out/M_POLICY_SIMULATE_out.json
python3 _work_gkx21/rebuild_metric.py M_POLICY_SIMULATE --check
```

脚本零 SQL，只读四份快照与两份逐表清单。产物里没有推演值，只有五张依赖表的可用性、弹性标定条件、条数基线演示与下游影响。

### 6.2 产物键位与正文数字的对应

| 正文数字 | 产物键 |
|---|---|
| 5（依赖表） | `tables_required` |
| 0（可用） | `tables_usable` |
| 631 | `tables[0].live_rows` |
| 0（四张） | `tables[1..4].live_rows` |
| 280 / 267 | `probes.gkx_total_tables` / `live_total_tables` |
| 33 / 0 / 123 | `probes.policy_table_columns` / `amount_columns_in_policy_table` / `amount_columns_gkx_total_cited` |
| 20,000 | `probes.policy_rows`、`probes.json_null_policy_support` |
| 0（实施日） | `probes.implementation_date_valid` |
| 17,476 / 31 / 1,932 | `alternative_baseline_demo.province_rows_total` / `province_count` / `top_province.rows` |
| 7,525 / 37.625% | `alternative_baseline_demo.policy_doc_rows` / `policy_doc_share_pct` |
| 36 / 93 | `live_mock_rows.policy_simulate` / `live_mock_rows.policy_metric_timeseries` |

### 6.3 出处与责任

公式来源见首部 calc-logic 与王惠正本两条路径，均可 `ls` 到。判定类型 `negative_evidence` 写在产物顶层。判档「完全不支持」与 `support_judgment` 逐字一致。

---

## 参考文献

1. 国务院. 关于全面实施预算绩效管理的意见. https://www.gov.cn/zhengce/2018-09/25/content_5325315.htm
2. 财政部. 项目支出绩效评价管理办法（财预〔2020〕10号）. https://www.gov.cn/
3. 中华人民共和国科学技术部. 关于深化科技评价改革的若干意见. https://www.most.gov.cn/ztzl/zdzx/tztg/201612/t20161222_4804.html
4. 国务院. 优化营商环境条例（国令第722号）. https://www.gov.cn/zhengce/content/2019-10/23/content_5443963.htm
5. 国务院办公厅. 关于进一步优化政务服务提升行政效能推动「高效办成一件事」的指导意见. https://www.gov.cn/
6. ISO. ISO 31000:2018 Risk management — Guidelines. https://www.iso.org/standard/65694.html
7. MySQL 8.0 Reference Manual — The DATE, DATETIME, and TIMESTAMP Types. https://dev.mysql.com/doc/refman/8.0/en/datetime.html
---

# 附件

## 附录 A　原始需求原文摘录

### A.1 口径定义（calc-logic 正本）

> 以省级政策力度指数为基线，对「扶持力度」「覆盖面」等参数化情景做弹性推演，输出基线值、模拟值、增量与变化曲线。对象=政策（区域/产业/主题粒度），基线=省级力度指数，输出=`ads.policy_simulate(baseline_value, simulated_value, delta_rate, curve)`。情景与弹性系数待 QPOL-02 确认。

### A.2 四步（王惠正本）

| 步 | 公式 / 动作 | 依赖 |
|---|---|---|
| 一 | 取 `policy_intensity.intensity_index`（`scope_type='province'`） | 力度表 |
| 二 | 设定 `support_intensity` / `coverage_scope` | 参数表 |
| 三 | $\Delta Y=e\cdot(X_{sim}-X_{base})/X_{base}$；$Y_{sim}=B(1+\Delta Y)$ | 弹性系数 |
| 四 | 写 `ads.policy_simulate` | 输出表 |

### A.3 正本的库名假设

王惠正本第三步的 SQL 写的是 `FROM gkx.policy_intensity`。实测 gkx 280 表无此表，照抄即报错。这一点写进 §5.2 与 §4.2，供实现侧避坑。

### A.4 待签事项

> 情景与弹性系数待 QPOL-02 确认。

QPOL-02 未签，$e$ 无取值，推演无法完成——这不是数据问题，是口径未定。

## 附录 B　探测证据（计数表）

| 探针 | 结果 | 判定含义 |
|---|---|---|
| gkx 总表数 | 280 | 全库核过 |
| gkx 含 policy 表 | 4（含 2 张 `_bak`） | 无力度/参数/推演表 |
| gkx `policy_intensity` | 不存在 | 基线无源 |
| live `policy_intensity` | 631 | 造数面 |
| live `policy_intensity_eval` | 0 | 空表 |
| live `policy_simulation_param` | 0 | 空表 |
| live `policy_prediction_indicator` | 0 | 空表 |
| live `policy_simulation_result` | 0 | 空表 |
| live `policy_simulate` | 36 | 造数面 |
| live 总表数 | 267 | 全库核过 |
| 政策表列数 | 33 | 无金额列 |
| 金额类列（政策表） | 0 | 扶持力度无量化源 |
| 金额类列（全库） | 123 | 全在 `dwd_bid_*` 招标表 |
| `policy_support` JSON null | 20,000 | 扶持对象取不出 |
| `implementation_date` 有效 | 0 | 实施时间无真值 |
| 省级政策条数 | 17,476 | 替代基线演示 |
| 省级单位数 | 31 | 同上 |
| 政策文件类条数 | 7,525 | 37.625% |

## 附录 C　可行性完整版

### C.1 报告目的与范围

回答：政策效果推演这套「基线 + 弹性」模型，在 gkx 与 live 两侧能不能跑；如果不能，断在哪一段、补什么能通。

### C.2 需求语义锚定

「推演」是反事实计算：给定一个未发生的情景，估算效果。它与「预测」不同——预测靠时间序列外推，推演靠参数响应。政策推演的正解是弹性模型，前提是有可标定的弹性。没有弹性，推演就退化成「假设效果与力度同比例变化」，那是把假设当结论。

### C.3 权威与学术构建方法谱系

#### C.3.1 族 A：政策弹性模型

用历史面板数据估 $e$，再做情景外推。方法成熟，但对数据要求高：需要同一对象在多个时点的政策强度与效果。

#### C.3.2 族 B：CGE

多部门均衡模型，靠投入产出表标定。政策库没有投入产出数据，不可能自建。

#### C.3.3 族 C：情景分析

定性方法，产出是几条叙事路径，不是数值曲线。与需求形态不符。

#### C.3.4 族 D：力度指数外推

正本选择，公式简单、可解释，但完全依赖基线表与弹性系数。

#### C.3.5 族 E：机器学习

需要效果标签。库内无标签，无法训练。

### C.4 数据可行性详细分析

| 依赖 | 结构 | 数据 | 结论 |
|---|---|---|---|
| 基线 `policy_intensity` | **无** | — | 不成立 |
| 参数 `policy_simulation_param` | **无**（live 0 行） | — | 不成立 |
| 弹性 $e$ | **无** | — | 不成立 |
| 校验 `policy_prediction_indicator` | **无**（live 0 行） | — | 不成立 |
| 金额列 | **无** | — | 扶持力度不可量化 |
| 政策主表 | 有 | 20,000 | 仅此一项成立 |

### C.5 推荐构建方案（工程可执行）

1. 当前不上线推演面板，页面用「参数待定」占位；
2. 先建 `policy_intensity` 并填真实 `intensity_index`（依赖 `M_POLICY_INTENSITY_SCORE` 的补数）；
3. 建 `policy_simulation_param`，把情景参数结构化；
4. QPOL-02 签认 $e$，无历史序列时给专家先验区间，并在 UI 上标注「参数为专家给定」；
5. 建 `policy_prediction_indicator` 后才能回测，回测通过才发布。

### C.6 风险与残余不确定性

最大风险是「$e$ 取 1」——它让推演退化成等比例放大，且没有任何依据。第二个风险是「用条数当基线」——推演会变成发文计划。第三个风险是「用招标金额当扶持金额」——方向相反，结论会反转。

### C.7 可行性总判（完整版结论）

四段输入全空、公式无法取值、模型无法回测。判**完全不支持**；补数并签认 $e$ 后可升级。

### C.8 对甲方四问的逐条回答

| 问 | 答 |
|---|---|
| 能不能给出推演曲线 | 不能，无基线、无参数、无弹性 |
| 能不能先取 $e=1$ 跑个示意 | 不能，那是把假设当结论 |
| 能不能用政策条数当基线 | 不能，条数对情景参数无响应 |
| 补什么能算 | 力度表 + 参数表 + $e$（QPOL-02）+ 校验表 |

## 附录 D　实测脚本与结果摘要

| 步骤 | 命令 | 输出 |
|---|---|---|
| 探针 | `python3 code/M_POLICY_SIMULATE.py` | `metrics/repro/out/M_POLICY_SIMULATE_out.json` |
| 重跑校验 | `python3 _work_gkx21/rebuild_metric.py M_POLICY_SIMULATE --check` | 内容未变 |
| 结构闸 | `python3 _work_gkx21/gate_check.py _staging21/M_POLICY_SIMULATE.md` | PASS |
| 基期闸 | `python3 _work_gkx21/check_base_years.py _staging21/M_POLICY_SIMULATE.md` | OK |

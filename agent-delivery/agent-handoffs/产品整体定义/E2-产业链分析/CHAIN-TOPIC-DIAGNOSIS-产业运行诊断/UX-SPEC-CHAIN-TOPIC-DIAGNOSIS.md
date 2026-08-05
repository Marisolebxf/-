# UX-SPEC-CHAIN-TOPIC-DIAGNOSIS｜产业运行诊断

> **文档版本**：v1.4-bottleneck-bid-vocab  
> **四件套版本**：IA/TRACE/USM/Wireframe v1.4-bottleneck-bid-vocab  
> **日期**：2026-08-05  
> **状态**：ready_for_v1  
> **体验 Owner**：human:高颖  
> **边界**：只转译已确认产品定义为可实现交互规则；不增删 Bid 叶子、不代表 PDR/Gate 通过。  
> **独立执行权威**：产业运行诊断交互只读本文件；父包 UX-SPEC 中 F-04/F-05/F-06 段落仅溯源。  
> **修订**：瓶颈补齐 `.5.1`/`.5.2` 原文词汇面；空对象配置与过程壳约定保留。

## 1. 权威输入

| 工件 | 版本 | 用途 |
| --- | --- | --- |
| IA / TRACE / USM / Wireframe | v1.4-bottleneck-bid-vocab | 边界、故事、Frame、REQ-02A/02B/03A/03B、关键/瓶颈词汇 |
| UX-UE 通用交互组件规范 | D10 | Tabs、表单、反馈、键盘 |
| Design.md | D8 | 视觉 token |
| 共享任务壳 | SYS-ANALYSIS-JOBS | 过程与显式看结果 |

## 2. 四件套同步核对

| 维度 | 数量 | 落点 |
| --- | --- | --- |
| 故事 | 7 | US-CHAIN-DIAG-01…07 |
| Frame | 5 | F-DIAG-01…05 |
| 路由 Tab | 4 | cycle / key-link / bottleneck / records |
| Bid 叶子 | 6（关键拆子叶 `.4.1`/`.4.2` 追溯） | 展示 `.2.2.2/.4/.5` + 算法 `.3.6/.8/.9` |
| review mounts | **15** | 见 Wireframe §11 |

同步结论：故事/Frame/路由一致；语义/API/readiness 为显式 Gap，不阻断 `v1_hifi_round1` 输入。

## 3. 用户旅程

### DIAG-J01｜政府周期分析闭环

故事：`US-CHAIN-DIAG-01/02/07`。  
主路径：确认产业 → `tab=cycle` 配参数 → 生成分析 → **共享过程（Bid 能力词阶段）** → 显式查看结果（回溯—诊断—预测）→ 可选记录恢复。  
异常：对象类型错误、参数越界、权限锁态、检索服务未接通（诚实降级）、检索快照缺失。

### DIAG-J02｜园区关键环节闭环

故事：`US-CHAIN-DIAG-03/04/07`。  
主路径：确认产业链 → `tab=key-link` 只读确认因子 → 生成分析 → **页内过程（`.4.1`/`.4.2` Bid 能力词）** → 显式查看全链结构化结果（高端化指数/边界衔接/关键标注等）→ 企业抽屉交接。  
异常：因子不可用、伪编辑权重被拒、证据缺失。

### DIAG-J03｜政府瓶颈诊断闭环

故事：`US-CHAIN-DIAG-05/06/07`。  
主路径：确认产业链 → `tab=bottleneck` 只读确认五维 → 生成分析 → **页内过程（`.5.1`/`.5.2` Bid 能力词）** → 显式查看多维健康与卡脖子归因建议。  
异常：维度未就绪、Mock/正式边界、无依据路径隐藏。

## 4. Frame 交互合同

### 4.1 F-DIAG-01 壳

- Tab 切换写 URL；保留兼容产业 ID；关键/瓶颈保留兼容链 ID；不携带另一 Tab 配置/结果焦点。
- **无对象**：对象条空态 +「打开对比篮」；**Tab 与各配置参数区仍完整展示**（对齐企业评估）；「生成分析」禁用。
- 禁止：无对象时隐藏配置主区；整页空白无说明。
- 键盘：Tab 可聚焦；对比篮由系统入口打开。

### 4.2 F-DIAG-02 周期

| 触发 | 结果 | 禁止 |
| --- | --- | --- |
| 无对象预览配置 | 参数卡片/版本说明可调可看；生成禁用 | 隐藏配置；无对象仍可提交 |
| 改参数 | 校验范围；提交时冻结快照 | 未校验提交 |
| 生成分析 | 最终校验 → 创建任务 → `demo_state=processing` 页内可视化过程 | 未点按钮自动创建；完成后自动进结果 |
| 过程阶段展示 | 页内 Steps 按 §4.2.1 Bid 词汇只读推进；可离开恢复 | 可操作联网控制台；运维式检索表单 |
| 过程完成 | 成功提示 + **仅**「查看分析结果」可进结果 | 自动跳转结果页 |
| V1 服务未接通 | 过程仍展示 Bid 词汇 + 降级条「固定可回放检索快照 / 待正式联网检索与模型接通」 | 「已完成实时全网检索」；删除 Bid 能力词 |
| 查看分析结果 | 用户点击后进入不可变结果；保留「回溯—诊断—预测」 | 自动跳转结果 |
| 展示检索说明 | 固定可回放快照文案 + 正式环境服务侧联网检索说明 | 「已完成实时联网」 |

#### 4.2.1 周期过程阶段文案（验收必现）

与 TRACE `domain_stage_registry.cycle` / IA §5.1 / Wireframe §4.1 同源：

1. 任务提交与参数冻结  
2. 整合产业参数与联网检索的历史与市场数据  
3. 大语言模型推理与周期阶段判断（诊断）  
4. 基于全网检索动态归纳趋势预测、关键驱动因素与潜在拐点  
5. 结果可信性校验与分析报告组装  

交互要点：

- 阶段为共享任务壳 Steps，只读进度，不是页面内「搜索引擎」。
- 用户不配置「如何联网」；联网/LLM 在服务侧兑现。
- 结果页「回溯—诊断—预测」与过程阶段语义同源，不互相替代。

### 4.3 F-DIAG-03 关键环节

| 触发 | 结果 | 禁止 |
| --- | --- | --- |
| 无对象预览配置 | 只读因子/版本仍展示；生成禁用 | 隐藏配置 |
| 打开配置 | 展示只读因子/版本（附加值率/技术壁垒/市场集中度） | 可编辑正式权重 |
| 因子不可用 | 禁用生成并说明 | 伪模板保存 |
| 生成分析 | 页内 Steps 按 §4.3.1；完成后显式看结果 | 自动跳结果 |
| 查看结果 | 结构化图谱 + 功能边界/衔接 + 高端化指数 + 关键标注 + 竞争格局/代表企业/技术趋势 | 截断为仅关键列表；隐藏边界/指数 |
| 代表企业 | 当前页共享抽屉 | 跳企业分析 |

#### 4.3.1 关键环节过程阶段文案（验收必现）

与 TRACE `domain_stage_registry.key_link` / IA §5.2 / Wireframe §5.1 同源：

1. 任务提交与产业链对象冻结  
2. 全链路环节结构化拆解（研发/设计/制造/销售/服务）  
3. 基于附加值率、技术壁垒、市场集中度计算高端化指数  
4. 关键环节智能标注与竞争格局/代表企业/技术趋势归纳  
5. 结果可信性校验与分析报告组装  

### 4.4 F-DIAG-04 瓶颈

| 触发 | 结果 | 禁止 |
| --- | --- | --- |
| 无对象预览配置 | 五维只读仍展示；生成禁用 | 隐藏配置 |
| 打开配置 | 五维只读；文案必须「资本」 | 用「资金」替代维名；拆出第六维 |
| 维度未就绪 | 禁用生成 | 前端自定阈值 |
| 生成分析 | 页内 Steps 按 §4.4.1；完成后显式看结果 | 自动跳结果 |
| 查看结果 | 四核心指标 + 各环节健康度 + 五维矩阵 + 卡脖子标记 + 成因/改进建议 + 时序说明 | 仅链级总分；隐藏卡脖子；业务模式未标注 Mock |

#### 4.4.1 瓶颈过程阶段文案（验收必现）

与 TRACE `domain_stage_registry.bottleneck` / IA §5.3 / Wireframe §6.1 同源：

1. 任务提交与产业链对象冻结  
2. 整合各环节技术/人才/资本/政策等时序数据  
3. 基于技术成熟度、人才供给量、融资事件、政策覆盖率计算环节健康度  
4. 瓶颈智能识别与卡脖子环节归因/改进建议生成  
5. 结果可信性校验与靶向方案/报告组装  

### 4.5 F-DIAG-05 记录

- 过滤后列表恢复到对应 Tab 配置草稿、过程或结果。
- `queued` 撤回遵循共享任务合同；`running` 不提供用户取消。
- 周期任务过程详情中的阶段文案须与 §4.2.1 一致。

## 5. 反馈与异常

| 场景 | 反馈 |
| --- | --- |
| permission_locked | 锁态 + 原因；隐藏敏感摘要 |
| unavailable | 与锁态区分的普通不可用 |
| config_invalid | 原位错误定位字段 |
| partial_evidence_gap | 缺口标记 + 未参与项 |
| retrieval_or_llm_not_connected（V1） | 过程仍展示 Bid 词汇 + 诚实降级说明；结果用固定可回放快照 |
| submit 失败 | 原位错误 + 可重试；配置保留 |

## 6. 组件、键盘与无障碍

- Tabs：Arco Tabs，方向键切换，选中态可见。
- 参数卡片：InputNumber `mode="button"` 可键盘操作；错误用文本不只靠颜色。
- 过程 Steps：可读当前阶段名；勿仅靠颜色区分完成态。
- 只读因子/五维：可聚焦说明「只读确认 / 正式口径待闭合」。
- 图谱/矩阵：需等价列表或可读摘要。
- 禁用控件须可读原因。

## 7. 响应式

同 Wireframe §8：1440 起卡片折行、结果可堆叠；配置控件不丢失。

## 8. 内部评审投影

| Frame | mount_id | BusinessMode |
| --- | --- | --- |
| F-01 | CHAIN-DIAG-F01-OBJECT-CONTEXT | absent |
| F-02 | CYCLE-TITLE / CYCLE-STAGE / PROCESS-STAGES / RETRIEVAL-SNAPSHOT / DECISION-BRIEF | absent |
| F-03 | KEY-TITLE / KEY-COUNT / **PROCESS-STAGES** / **HIGH-END-INDEX** / FACTOR-READONLY | absent |
| F-04 | BOTTLENECK-TITLE / BOTTLENECK-COUNT / **PROCESS-STAGES** / **LINK-HEALTH** / DIMENSION-READONLY | absent |
| F-05 | CHAIN-DIAG-F05-RECORDS | absent |

`metric_readiness_projection: []`（无专题矩阵行时不投影伪 D1–D4）。

## 9. Demo 实施交接

1. 路由与 Tab：`/industry-center/diagnosis?tab=cycle|key-link|bottleneck|records`；过程态 `demo_state=processing`；结果态 `demo_state=result`。  
2. Frame/Mount 目标 ID：`F-DIAG-*` / `CHAIN-DIAG-*`；禁止回扩 `F-CHAIN-04/05/06`。  
3. 布局对齐企业评估：无对象仍显配置；生成后页内 Steps；完成后不自动跳结果。  
4. 对象类型：周期=industry；关键/瓶颈=industry_chain；服务端再校验。  
5. 任务流：显式提交 → 可视化过程 → 显式看结果。  
6. **周期 `DIAGNOSIS_TASK_STAGES.cycle` 使用 §4.2.1；关键 `key_link` 使用 §4.3.1；瓶颈 `bottleneck` 使用 §4.4.1**（写入共享任务 `stages`）。  
7. 过程壳挂点：`CHAIN-DIAG-F02-PROCESS-STAGES`、`CHAIN-DIAG-F03-PROCESS-STAGES`、`CHAIN-DIAG-F04-PROCESS-STAGES`；结果挂点 `CHAIN-DIAG-F03-HIGH-END-INDEX`、`CHAIN-DIAG-F04-LINK-HEALTH`。  
8. 参数卡片交互可与企业评估同构，但不得复用企业字段/阶段文案。

## 10. Gap 与 V1 处理

| Gap | V1 |
| --- | --- |
| GAP-CHAIN-DIAG-METRICS | Mock/Pending + 评审挂点 |
| GAP-CHAIN-DIAG-SEMANTICS | 只读确认；可见「正式口径待闭合」 |
| GAP-CHAIN-DIAG-API | **页面仍呈现 Bid 过程词汇**；服务未接通时固定可回放 + 待接通说明；禁实时完成态假话；Gap=服务接通与诚实降级，非「不算页面需求」 |
| GAP-CHAIN-DIAG-APPROVAL | 合同沿用；范围变化补批 |

## 11. 自检

1. 7/7 故事、5/5 Frame、15/15 mounts 有交互落点。  
2. 未修改产品范围；Bid `.2.2.2` 与 `.2.2.4/.4.1/.4.2` 能力词在过程/结果可见。  
3. 与 Wireframe mounts 数字一致（15）。  
4. 不代表 PDR 通过。  

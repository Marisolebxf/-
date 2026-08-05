# UX-SPEC-CHAIN-TOPIC-DIAGNOSIS｜产业运行诊断

> 版本：1.4-bottleneck-bid-vocab  
> 状态：ready_for_v1  
> 四件套版本：1.4-bottleneck-bid-vocab  
> Track：Track-MS  
> screen_tier：medium_1440_1920  
> 体验 Owner：human:高颖  
> 独立执行权威：产业运行诊断交互只读本文件；父包 UX-SPEC 中 F-04/F-05/F-06 段落仅溯源。

## 1. 权威输入与边界

本 UX-SPEC 只深化同目录 IA、TRACE、USM、Wireframe，并遵守：

- 展示 Bid `1.1.1.2.4.2.2.2` / `.2.2.4` / `.2.2.5`（含 `.4.1`/`.4.2`/`.5.1`/`.5.2`）；算法 Bid `1.1.1.1.1.1.1.3.6` / `.3.8` / `.3.9`；
- `Design.md`、`UX-UE 通用交互组件规范.md`、`data-lineage-policy.md`；
- 共享任务壳 SYS-ANALYSIS-JOBS；报告阅读 ENT-EXPORT；
- TRACE `source_manifest` 与 Gap 处置。

边界：

- 不改变产品范围、不增删 Bid 叶子；不代表 PDR/Gate 通过。
- 三项诊断各自独立追溯；同工作空间不等于合并叶子。
- 正式权重/阈值不可前端编辑；瓶颈维名必须用「资本」。
- 无专题 readiness 矩阵行时不投影伪 D1–D4。
- 全景 / 区域 / 深圳 / 门户总览不在本包修改。

## 2. 四件套同步核对

| 核对项 | 产品结论 | UX 落点 | 结论 |
| --- | --- | --- | --- |
| 故事 | 7 | US-CHAIN-DIAG-01…07 | 一致 |
| Frame | 5 | F-DIAG-01…05 | 一致 |
| 路由 Tab | 4 | cycle / key-link / bottleneck / records | 一致 |
| Bid 叶子 | 6 + 子叶追溯 | `.2.2.2/.4/.5` + `.3.6/.8/.9` | 未合并删除 |
| 周期过程词汇 | Bid `.2.2.2` 五阶段 | §5 / F-DIAG-02 | 已定义 |
| 关键过程/结果词汇 | `.4.1`/`.4.2` | §5 / F-DIAG-03 | 已定义 |
| 瓶颈过程/结果词汇 | `.5.1`/`.5.2` +「资本」 | §5 / F-DIAG-04 | 已定义 |
| review mounts | 17 | Wireframe §11 / §9 | 一致 |
| readiness | 无专题矩阵行 | §9 `metric_readiness_projection: []` | 不投影伪 D1–D4 |

## 3. 用户旅程与任务流

### DIAG-J01｜政府周期分析闭环

故事：`US-CHAIN-DIAG-01/02/07`。  
主路径：确认产业 → `tab=cycle` 配参数 → 生成分析 → 页内过程（Bid 能力词阶段）→ 显式查看结果（回溯—诊断—预测）→ 可选记录恢复。  
异常：对象类型错误、参数越界、权限锁态、检索服务未接通（诚实降级）、检索快照缺失。

### DIAG-J02｜园区关键环节闭环

故事：`US-CHAIN-DIAG-03/04/07`。  
主路径：确认产业链 → `tab=key-link` 只读确认因子 → 生成分析 → 页内过程（`.4.1`/`.4.2`）→ 显式查看全链结构化结果 → 企业抽屉交接。  
异常：因子不可用、伪编辑权重被拒、证据缺失。

### DIAG-J03｜政府瓶颈诊断闭环

故事：`US-CHAIN-DIAG-05/06/07`。  
主路径：确认产业链 → `tab=bottleneck` 只读确认五维 → 生成分析 → 页内过程（`.5.1`/`.5.2`）→ 显式查看多维健康与卡脖子归因建议。  
异常：维度未就绪、Mock/正式边界、无依据路径隐藏。

## 4. Frame 与承载映射

| Frame | 路由 / 宿主 | 故事 | 承载 |
| --- | --- | --- | --- |
| F-DIAG-01 | `/industry-center/diagnosis` | 全部 | 对象上下文、Tab、权限锁态 |
| F-DIAG-02 | `?tab=cycle` | US-01/02 | 参数配置 / 过程 Steps / 结果 |
| F-DIAG-03 | `?tab=key-link` | US-03/04 | 因子只读 / 过程 / 全链结果 |
| F-DIAG-04 | `?tab=bottleneck` | US-05/06 | 五维只读 / 过程 / 健康与归因 |
| F-DIAG-05 | `?tab=records` | US-07 | 本工作空间历史过滤与恢复 |

## 5. 交互与状态转换

### 5.1 F-DIAG-01 壳

- Tab 切换写 URL；保留兼容产业 ID；关键/瓶颈保留兼容链 ID；不携带另一 Tab 配置/结果焦点。
- 无对象：对象条空态 +「打开对比篮」；Tab 与各配置参数区仍完整展示；「生成分析」禁用。
- 禁止：无对象时隐藏配置主区；整页空白无说明。

### 5.2 F-DIAG-02 周期

| 触发 | 结果 | 禁止 |
| --- | --- | --- |
| 无对象预览配置 | 参数可调可看；生成禁用 | 隐藏配置；无对象仍可提交 |
| 改参数 | 校验范围；提交时冻结快照 | 未校验提交 |
| 生成分析 | 创建任务 → `demo_state=processing` 页内 Steps | 未点按钮自动创建；完成后自动进结果 |
| 过程阶段展示 | Steps 按 §5.2.1 Bid 词汇只读推进 | 可操作联网控制台 |
| 过程完成 | 仅「查看分析结果」可进结果 | 自动跳转结果页 |
| V1 服务未接通 | Bid 词汇 + 降级条 | 「已完成实时全网检索」 |
| 查看分析结果 | 不可变结果；回溯—诊断—预测 | 自动跳转 |

#### 5.2.1 周期过程阶段文案（验收必现）

1. 任务提交与参数冻结  
2. 整合产业参数与联网检索的历史与市场数据  
3. 大语言模型推理与周期阶段判断（诊断）  
4. 基于全网检索动态归纳趋势预测、关键驱动因素与潜在拐点  
5. 结果可信性校验与分析报告组装  

### 5.3 F-DIAG-03 关键环节

| 触发 | 结果 | 禁止 |
| --- | --- | --- |
| 无对象预览配置 | 只读因子仍展示；生成禁用 | 隐藏配置 |
| 打开配置 | 附加值率/技术壁垒/市场集中度只读 | 可编辑正式权重 |
| 生成分析 | Steps 按 §5.3.1；完成后显式看结果 | 自动跳结果 |
| 查看结果 | 全链结构 + 功能边界/衔接 + 高端化指数 + 关键标注 + 竞争格局/代表企业/技术趋势 | 截断为仅关键列表 |
| 代表企业 | 当前页共享抽屉 | 跳企业分析 |

#### 5.3.1 关键环节过程阶段文案（验收必现）

1. 任务提交与产业链对象冻结  
2. 全链路环节结构化拆解（研发/设计/制造/销售/服务）  
3. 基于附加值率、技术壁垒、市场集中度计算高端化指数  
4. 关键环节智能标注与竞争格局/代表企业/技术趋势归纳  
5. 结果可信性校验与分析报告组装  

### 5.4 F-DIAG-04 瓶颈

| 触发 | 结果 | 禁止 |
| --- | --- | --- |
| 无对象预览配置 | 五维只读仍展示；生成禁用 | 隐藏配置 |
| 打开配置 | 五维只读；文案必须「资本」 | 用「资金」替代维名；拆出第六维 |
| 生成分析 | Steps 按 §5.4.1；完成后显式看结果 | 自动跳结果 |
| 查看结果 | 四核心指标 + 各环节健康度 + 五维矩阵 + 卡脖子 + 成因/改进建议 + 时序说明 | 仅链级总分；隐藏卡脖子 |

#### 5.4.1 瓶颈过程阶段文案（验收必现）

1. 任务提交与产业链对象冻结  
2. 整合各环节技术/人才/资本/政策等时序数据  
3. 基于技术成熟度、人才供给量、融资事件、政策覆盖率计算环节健康度  
4. 瓶颈智能识别与卡脖子环节归因/改进建议生成  
5. 结果可信性校验与靶向方案/报告组装  

### 5.5 F-DIAG-05 记录

- 过滤后列表恢复到对应 Tab 配置草稿、过程或结果。
- `queued` 撤回遵循共享任务合同；`running` 不提供用户取消。
- 过程阶段文案须与对应业务 §5.2.1 / §5.3.1 / §5.4.1 一致。

每业务 Frame 状态覆盖：`empty_object` / `loading` / `config_invalid` / `permission_locked` / `submitting` / `processing` / `succeeded_wait_view` / `result` / `partial_evidence_gap` / `error_retry`。

## 6. 反馈与异常恢复

| 场景 | 反馈 | 恢复 |
| --- | --- | --- |
| permission_locked | 锁态 + 原因；隐藏敏感摘要 | 申请权限或降级只读 |
| unavailable | 与锁态区分的普通不可用 | 更换对象或稍后重试 |
| config_invalid | 原位错误定位字段 | 修正后重试 |
| partial_evidence_gap | 缺口标记 + 未参与项 | 继续阅读已有证据 |
| retrieval_or_llm_not_connected | 过程仍展示 Bid 词汇 + 诚实降级 | 使用固定可回放快照 |
| submit 失败 | 原位错误 + 可重试 | 配置保留后重提 |

## 7. 组件、键盘与无障碍

- Tabs：Arco Tabs，方向键切换，选中态可见。
- 参数卡片：InputNumber `mode="button"` 可键盘操作；错误用文本不只靠颜色。
- 过程 Steps：可读当前阶段名；勿仅靠颜色区分完成态。
- 只读因子/五维：可聚焦说明「只读确认 / 正式口径待闭合」。
- 图谱/矩阵：需等价列表或可读摘要。
- 禁用控件须可读原因。

## 8. 响应式行为

同 Wireframe：1920/1680 参数卡片 4 列、五维可 5 列、结果图表并排；1440 起卡片折行、结果可堆叠；配置控件不丢失。宽度验收：1920 / 1680 / 1440。不声明专题小屏 `small_reflow`。

## 9. 内部评审投影

| Frame | mount_id | BusinessMode |
| --- | --- | --- |
| F-DIAG-01 | CHAIN-DIAG-F01-OBJECT-CONTEXT | absent |
| F-DIAG-02 | CYCLE-TITLE / CYCLE-STAGE / PROCESS-STAGES / RETRIEVAL-SNAPSHOT / DECISION-BRIEF | absent |
| F-DIAG-03 | KEY-TITLE / KEY-COUNT / PROCESS-STAGES / HIGH-END-INDEX / FACTOR-READONLY | absent |
| F-DIAG-04 | BOTTLENECK-TITLE / BOTTLENECK-COUNT / PROCESS-STAGES / LINK-HEALTH / DIMENSION-READONLY | absent |
| F-DIAG-05 | CHAIN-DIAG-F05-RECORDS | absent |

`metric_readiness_projection: []`（无专题矩阵行时不投影伪 D1–D4）。完整挂点清单见 §12 `review_mounts`（17）。

## 10. Demo 实施交接

1. 路由与 Tab：`/industry-center/diagnosis?tab=cycle|key-link|bottleneck|records`；过程态 `demo_state=processing`；结果态 `demo_state=result`。  
2. Frame/Mount 目标 ID：`F-DIAG-*` / `CHAIN-DIAG-*`；禁止回扩 `F-CHAIN-04/05/06`。  
3. 布局对齐企业评估：无对象仍显配置；生成后页内 Steps；完成后不自动跳结果。  
4. 对象类型：周期=industry；关键/瓶颈=industry_chain；服务端再校验。  
5. 任务流：显式提交 → 可视化过程 → 显式看结果。  
6. `DIAGNOSIS_TASK_STAGES.cycle` 用 §5.2.1；`key_link` 用 §5.3.1；`bottleneck` 用 §5.4.1。  
7. 过程壳挂点：`CHAIN-DIAG-F02/F03/F04-PROCESS-STAGES`；结果挂点 `CHAIN-DIAG-F03-HIGH-END-INDEX`、`CHAIN-DIAG-F04-LINK-HEALTH`。  
8. 参数卡片交互可与企业评估同构，但不得复用企业字段/阶段文案。

## 11. 缺口与阻断项

| Gap | blocks_v1 | blocks_stages | V1 处置 |
| --- | --- | --- | --- |
| GAP-CHAIN-DIAG-METRICS | false | pdr, v1_final, v2_lumen, production | Mock/Pending + 评审挂点 |
| GAP-CHAIN-DIAG-SEMANTICS | false | pdr, v1_final, v2_lumen, production | 只读确认；可见「正式口径待闭合」 |
| GAP-CHAIN-DIAG-API | false | pdr, v1_final, v2_lumen, production | 页面仍呈现 Bid 过程词汇；固定可回放 + 待接通说明；禁实时完成态假话 |
| GAP-CHAIN-DIAG-APPROVAL | false | pdr, v1_final, v2_lumen, production | 合同沿用；范围变化补批 |

上述缺口均有安全、确定且可见的 V1 处理，故不阻断 V1 高保真首轮。

## 12. 机器可读交付契约

```yaml
ux_spec_contract:
  module_key: CHAIN-TOPIC-DIAGNOSIS
  version: "1.4-bottleneck-bid-vocab"
  status: ready_for_v1
  source_four_pack:
    - IA-CHAIN-TOPIC-DIAGNOSIS.md
    - TRACE-CHAIN-TOPIC-DIAGNOSIS.yaml
    - USM-CHAIN-TOPIC-DIAGNOSIS.md
    - Wireframe-CHAIN-TOPIC-DIAGNOSIS.md
  screen_tier: medium_1440_1920
  delivery_stage: v1_hifi_round1
  product_scope_mutation: prohibited
  demo_code_mutation: prohibited
  source_inventory_complete: true
  original_requirement_sources:
    - 展示Bid#1.1.1.2.4.2.2.2
    - 展示Bid#1.1.1.2.4.2.2.4
    - 展示Bid#1.1.1.2.4.2.2.5
    - 算法Bid#1.1.1.1.1.1.1.3.6
    - 算法Bid#1.1.1.1.1.1.1.3.8
    - 算法Bid#1.1.1.1.1.1.1.3.9
  permission_contract:
    product_role_is_not_permission_persona: true
    mock_user_permission_inference: prohibited
    final_authorization: server_fail_closed
    unauthorized_sensitive_value: do_not_render
  journeys:
    - {journey_id: DIAG-J01-CYCLE, role: ROLE-DIAG-GOV, story_refs: [US-CHAIN-DIAG-01, US-CHAIN-DIAG-02, US-CHAIN-DIAG-07], primary_flow: [confirm_industry, configure_params, submit, process_stages, explicit_view_result], abnormal_flows: [wrong_object_type, param_out_of_range, permission_locked, retrieval_not_connected]}
    - {journey_id: DIAG-J02-KEY-LINK, role: ROLE-DIAG-PARK, story_refs: [US-CHAIN-DIAG-03, US-CHAIN-DIAG-04, US-CHAIN-DIAG-07], primary_flow: [confirm_chain, readonly_factors, submit, process_stages, explicit_view_full_chain, enterprise_drawer], abnormal_flows: [factor_unavailable, weight_edit_rejected, evidence_missing]}
    - {journey_id: DIAG-J03-BOTTLENECK, role: ROLE-DIAG-GOV, story_refs: [US-CHAIN-DIAG-05, US-CHAIN-DIAG-06, US-CHAIN-DIAG-07], primary_flow: [confirm_chain, readonly_dimensions, submit, process_stages, explicit_view_health_and_choke], abnormal_flows: [dimension_not_ready, mock_formal_boundary, solution_without_evidence]}
  frame_specs:
    - {frame_id: F-DIAG-01, route_or_host: /industry-center/diagnosis, source_refs: [US-CHAIN-DIAG-01, US-CHAIN-DIAG-03, US-CHAIN-DIAG-05, US-CHAIN-DIAG-07], states: [empty_object, object_ready, permission_locked, unavailable], interactions: [switch_tab, open_compare_basket]}
    - {frame_id: F-DIAG-02, route_or_host: "/industry-center/diagnosis?tab=cycle", source_refs: [US-CHAIN-DIAG-01, US-CHAIN-DIAG-02], states: [empty_object, config_invalid, submitting, processing, succeeded_wait_view, result, error_retry], interactions: [edit_params, submit, view_process, explicit_view_result]}
    - {frame_id: F-DIAG-03, route_or_host: "/industry-center/diagnosis?tab=key-link", source_refs: [US-CHAIN-DIAG-03, US-CHAIN-DIAG-04], states: [empty_object, config_invalid, submitting, processing, succeeded_wait_view, result, partial_evidence_gap], interactions: [confirm_factors, submit, view_process, explicit_view_result, open_enterprise_drawer]}
    - {frame_id: F-DIAG-04, route_or_host: "/industry-center/diagnosis?tab=bottleneck", source_refs: [US-CHAIN-DIAG-05, US-CHAIN-DIAG-06], states: [empty_object, config_invalid, submitting, processing, succeeded_wait_view, result, partial_evidence_gap], interactions: [confirm_dimensions, submit, view_process, explicit_view_result]}
    - {frame_id: F-DIAG-05, route_or_host: "/industry-center/diagnosis?tab=records", source_refs: [US-CHAIN-DIAG-07], states: [empty, loading, filtered, error], interactions: [filter, open_process, open_result, copy_config]}
  feedback_rules:
    - {trigger: no_object, response: show_empty_object_bar_keep_config_disable_submit, recovery: open_compare_basket}
    - {trigger: submit_validation_failed, response: inline_field_errors_keep_draft, recovery: correct_and_resubmit}
    - {trigger: retrieval_or_llm_not_connected, response: keep_bid_stage_vocab_with_degraded_banner, recovery: use_fixed_replayable_snapshot}
    - {trigger: process_succeeded, response: show_view_result_only, recovery: user_clicks_view_result}
    - {trigger: mock_in_business_mode, response: hide_or_label_non_formal_conclusion, recovery: switch_to_review_mode_or_wait_formal_data}
  responsive_widths: [1920, 1680, 1440]
  accessibility_checks: [keyboard, focus, aria, contrast, reduced_motion, alternative_structure_list]
  metric_readiness_projection: []
  metric_readiness_projection_reason: no_matrix_rows_applicable_to_CHAIN_TOPIC_DIAGNOSIS
  review_mounts:
    - {mount_id: CHAIN-DIAG-F01-OBJECT-CONTEXT, frame_id: F-DIAG-01, business_mode: absent}
    - {mount_id: CHAIN-DIAG-F02-CYCLE-TITLE, frame_id: F-DIAG-02, business_mode: absent}
    - {mount_id: CHAIN-DIAG-F02-CYCLE-STAGE, frame_id: F-DIAG-02, business_mode: absent}
    - {mount_id: CHAIN-DIAG-F02-PROCESS-STAGES, frame_id: F-DIAG-02, business_mode: absent}
    - {mount_id: CHAIN-DIAG-F02-RETRIEVAL-SNAPSHOT, frame_id: F-DIAG-02, business_mode: absent}
    - {mount_id: CHAIN-DIAG-F02-DECISION-BRIEF, frame_id: F-DIAG-02, business_mode: absent}
    - {mount_id: CHAIN-DIAG-F03-KEY-TITLE, frame_id: F-DIAG-03, business_mode: absent}
    - {mount_id: CHAIN-DIAG-F03-KEY-COUNT, frame_id: F-DIAG-03, business_mode: absent}
    - {mount_id: CHAIN-DIAG-F03-PROCESS-STAGES, frame_id: F-DIAG-03, business_mode: absent}
    - {mount_id: CHAIN-DIAG-F03-HIGH-END-INDEX, frame_id: F-DIAG-03, business_mode: absent}
    - {mount_id: CHAIN-DIAG-F03-FACTOR-READONLY, frame_id: F-DIAG-03, business_mode: absent}
    - {mount_id: CHAIN-DIAG-F04-BOTTLENECK-TITLE, frame_id: F-DIAG-04, business_mode: absent}
    - {mount_id: CHAIN-DIAG-F04-BOTTLENECK-COUNT, frame_id: F-DIAG-04, business_mode: absent}
    - {mount_id: CHAIN-DIAG-F04-PROCESS-STAGES, frame_id: F-DIAG-04, business_mode: absent}
    - {mount_id: CHAIN-DIAG-F04-LINK-HEALTH, frame_id: F-DIAG-04, business_mode: absent}
    - {mount_id: CHAIN-DIAG-F04-DIMENSION-READONLY, frame_id: F-DIAG-04, business_mode: absent}
    - {mount_id: CHAIN-DIAG-F05-RECORDS, frame_id: F-DIAG-05, business_mode: absent}
  gaps:
    - {id: GAP-CHAIN-DIAG-METRICS, summary: diagnosis_topic_metrics_and_readiness_rows_missing, blocks_v1: false, blocks_stages: [pdr, v1_final, v2_lumen, production], v1_disposition: gap_visible, v1_treatment: mock_pending_with_review_mounts, owner: "human:何老师", deadline: before_pdr, return_to: TRACE}
    - {id: GAP-CHAIN-DIAG-SEMANTICS, summary: q052_q054_formal_threshold_not_closed, blocks_v1: false, blocks_stages: [pdr, v1_final, v2_lumen, production], v1_disposition: gap_visible, v1_treatment: readonly_registered_versions_with_pending_copy, owner: "human:何老师", deadline: before_pdr, return_to: TRACE}
    - {id: GAP-CHAIN-DIAG-API, summary: retrieval_llm_and_openapi_not_connected, blocks_v1: false, blocks_stages: [pdr, v1_final, v2_lumen, production], v1_disposition: gap_visible, v1_treatment: bid_stage_vocab_plus_fixed_replayable_snapshot, owner: "human:徐滕强", deadline: before_pdr, return_to: architecture}
    - {id: GAP-CHAIN-DIAG-APPROVAL, summary: parent_diagnosis_decision_provenance_incomplete, blocks_v1: false, blocks_stages: [pdr, v1_final, v2_lumen, production], v1_disposition: gap_visible, v1_treatment: keep_written_contract_until_scope_change, owner: "human:郭万迎", deadline: before_pdr, return_to: TRACE}
```

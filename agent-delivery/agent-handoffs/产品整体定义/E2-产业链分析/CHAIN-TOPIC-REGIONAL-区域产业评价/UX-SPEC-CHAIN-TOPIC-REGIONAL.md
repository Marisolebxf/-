# UX-SPEC-CHAIN-TOPIC-REGIONAL｜区域产业评价

> 版本：1.0-package-split  
> 状态：ready_for_v1  
> 四件套版本：1.0-package-split  
> Track：Track-MS  
> screen_tier：medium_1440_1920  
> 体验 Owner：human:高颖  
> 独立执行权威：区域产业评价交互只读本文件；父包 UX-SPEC 中 F-07/F-08 段落仅溯源。

## 1. 权威输入与边界

本 UX-SPEC 只深化同目录 IA、TRACE、USM、Wireframe，并遵守：

- 展示 Bid `1.1.1.2.4.2.2.3` / `.2.2.8`（含 `.3.1`/`.3.2`/`.8.1`/`.8.2`）；算法 Bid `1.1.1.1.1.1.1.3.10`；
- `Design.md`、`UX-UE 通用交互组件规范.md`、`data-lineage-policy.md`；
- 共享任务壳 SYS-ANALYSIS-JOBS；报告阅读 ENT-EXPORT；
- TRACE `source_manifest` 与 Gap 处置。

边界：

- 不改变产品范围、不增删 Bid 叶子；不代表 PDR/Gate 通过。
- 指数与竞争力各自独立追溯；同工作空间不等于合并叶子。
- 区域不入对比篮主对象域；禁止多产业×多区域笛卡尔积。
- 自定义指标本轮显式未开放；无专题 readiness 矩阵行时不投影伪 D1–D4。
- 全景 / 诊断 / 深圳 / 门户总览不在本包修改。

## 2. 四件套同步核对

| 核对项 | 产品结论 | UX 落点 | 结论 |
| --- | --- | --- | --- |
| 故事 | 5 | US-CHAIN-REG-01…05 | 一致 |
| Frame | 4 | F-REG-01…04 | 一致 |
| 路由 Tab | 3 | index / competitiveness / records | 一致 |
| Bid 叶子 | 3 | `.2.2.3` / `.2.2.8` + `.3.10` | 未合并删除 |
| 对象组合 | 1×1 / 1×2~5 / 2~5×1 | §5 / F-REG-02/03 | 已定义 |
| 竞争力三维 | 企业能力 / 学术生态 / 配套环境 | §5 / F-REG-03 | 已定义 |
| review mounts | 9 | Wireframe §10 | 一致 |
| readiness | 无专题矩阵行 | §9 `metric_readiness_projection: []` | 不投影伪 D1–D4 |

## 3. 用户旅程与任务流

### REG-J01｜政府指数评价闭环

故事：`US-CHAIN-REG-01/02/05`。  
主路径：确认产业对象 → `tab=index` 配组合与权重 → 轻量预览 → 生成分析 → 共享过程 → 显式查看结果 → 可选记录恢复。  
异常：非法组合、权重错误、自定义指标不可用、不可比较对象、权限锁态。

### REG-J02｜园区竞争力评价闭环

故事：`US-CHAIN-REG-03/04/05`。  
主路径：确认产业对象 → `tab=competitiveness` 确认三维权重 → 生成分析 → 显式查看排名短板。  
异常：维度缺失、版本混排禁止、数据不足区域。

## 4. Frame 与承载映射

| Frame | 路由 / 宿主 | 故事 | 承载 |
| --- | --- | --- | --- |
| F-REG-01 | `/industry-center/regional` | 全部 | 对象上下文、Tab、权限锁态 |
| F-REG-02 | `?tab=index` | US-01/02 | 组合/预设指标/权重/预览/过程/结果 |
| F-REG-03 | `?tab=competitiveness` | US-03/04 | 三维一级权重/过程/排名短板 |
| F-REG-04 | `?tab=records` | US-05 | 本工作空间历史过滤与恢复 |

## 5. 交互与状态转换

### 5.1 F-REG-01 壳

- Tab 切换写 URL，保留产业对象；不携带另一 Tab 的区域/权重/预览/结果焦点。
- 无对象：对象条空态 +「打开对比篮」；配置区仍完整展示；「生成分析」禁用。
- 禁止：页内私有产业 Select；区域入篮；模块自建浮层篮；无对象时整页空白无说明。

### 5.2 F-REG-02 指数

| 触发 | 结果 | 禁止 |
| --- | --- | --- |
| 切换评价模式 | 校验组合上限；非法时禁用提交 | 自动删对象凑合法 |
| 改权重 | 实时校验合计；可一键均分 | 静默归一化后提交 |
| 轻量预览 | 显示预览值；不建 task | 写入分析记录 |
| 生成分析 | 最终校验 → 创建任务 → 过程态 | 未点按钮自动创建 |
| 查看分析结果 | 进入不可变结果 | 自动跳转结果 |
| 尝试自定义指标 | 明示本轮未开放 + Gap 挂点 | 伪装已支持入口 |

### 5.3 F-REG-03 竞争力

| 触发 | 结果 | 禁止 |
| --- | --- | --- |
| 调一级权重 | 三维固定展示；合计 100% | 增删维度、改内部算法 |
| 一键均分 | 三维各约 33.3%（演示可整百） | 静默改成两维 |
| 维度不可用 | 禁用生成并说明 | 降成两维继续算 |
| 查看结果 | 排名/三维/热力图摘要/短板/版本边界 | 跨版本混排 |

### 5.4 F-REG-04 记录

- 过滤后列表恢复到对应 Tab 配置草稿、过程或结果。
- `queued` 撤回遵循共享任务合同；`running` 不提供用户取消。

每业务 Frame 状态覆盖：`empty_object` / `loading` / `config_invalid` / `permission_locked` / `previewing` / `submitting` / `processing` / `succeeded_wait_view` / `result` / `incomparable` / `partial_metric_gap` / `error_retry`。

## 6. 反馈与异常恢复

| 场景 | 反馈 | 恢复 |
| --- | --- | --- |
| permission_locked | 锁态 + 原因；隐藏敏感摘要 | 申请权限或降级只读 |
| unavailable | 与锁态区分的普通不可用 | 更换对象或稍后重试 |
| config_invalid | 原位错误定位字段（组合/权重） | 修正后重试 |
| incomparable | 列出对象与原因，无伪排名 | 对齐模型/权重版本 |
| partial_metric_gap | 缺口标记 + 未参与计算项 | 继续阅读已有结果 |
| submit 失败 | 原位错误 + 可重试 | 配置保留后重提 |

## 7. 组件、键盘与无障碍

- Tabs：Arco Tabs，方向键切换，选中态可见。
- 权重：InputNumber `mode="button"` 可键盘操作；错误用文本不只靠颜色。
- 图表：需提供等价数据表或可读摘要（结果区）。
- 禁用控件须可读原因。

## 8. 响应式行为

同 Wireframe §7：1920/1680 配置区单列主宽、结果图表并排；1440 起结果区图表上下堆叠；权重控件保持可编辑。宽度验收：1920 / 1680 / 1440。不声明专题小屏 `small_reflow`。

## 9. 内部评审投影

| Frame | mount_id | BusinessMode |
| --- | --- | --- |
| F-REG-01 | CHAIN-REG-F01-OBJECT-CONTEXT | absent |
| F-REG-02 | INDEX-TITLE / INDEX-METRICS / CUSTOM-METRIC-GAP / PREVIEW | absent |
| F-REG-03 | COMPETITIVENESS-TITLE / COMPETITIVENESS-METRICS / VERSION-BOUNDARY | absent |
| F-REG-04 | CHAIN-REG-F04-RECORDS | absent |

`metric_readiness_projection: []`（无专题矩阵行时不投影伪 D1–D4）。完整挂点清单见 §12 `review_mounts`（9）。

## 10. Demo 实施交接

1. 路由与 Tab：`/industry-center/regional?tab=index|competitiveness|records`；过程态 `demo_state=processing`；结果态 `demo_state=result`。  
2. Frame/Mount 目标 ID：`F-REG-*` / `CHAIN-REG-*`；禁止回扩 `F-CHAIN-07/08` 与 `CHAIN-TOPIC-F07/F08`。  
3. 对象组合与权重校验必须前端拦截 + 服务端再校验；预览永不落任务库。  
4. 任务流：显式提交 → 过程 → 显式看结果；禁止完成后自动跳结果。  
5. 自定义指标：只展示「本轮未纳入」说明，不提供假创建入口。  
6. 竞争力文案用「配套环境」；语义对齐算法「配套生态」。

## 11. 缺口与阻断项

| Gap | blocks_v1 | blocks_stages | V1 处置 |
| --- | --- | --- | --- |
| GAP-CHAIN-REG-CUSTOM-METRIC | false | pdr, v1_final, v2_lumen, production | 可见差异，不伪装已支持 |
| GAP-CHAIN-REG-METRICS | false | pdr, v1_final, v2_lumen, production | Mock/Pending + 评审挂点 |
| GAP-CHAIN-REG-PERMISSIONS | false | pdr, v1_final, v2_lumen, production | fail closed |
| GAP-CHAIN-REG-APPROVAL | false | pdr, v1_final, v2_lumen, production | 合同沿用；范围变化补批 |

上述缺口均有安全、确定且可见的 V1 处理，故不阻断 V1 高保真首轮。

## 12. 机器可读交付契约

```yaml
ux_spec_contract:
  module_key: CHAIN-TOPIC-REGIONAL
  version: "1.0-package-split"
  status: ready_for_v1
  source_four_pack:
    - IA-CHAIN-TOPIC-REGIONAL.md
    - TRACE-CHAIN-TOPIC-REGIONAL.yaml
    - USM-CHAIN-TOPIC-REGIONAL.md
    - Wireframe-CHAIN-TOPIC-REGIONAL.md
  screen_tier: medium_1440_1920
  delivery_stage: v1_hifi_round1
  product_scope_mutation: prohibited
  demo_code_mutation: prohibited
  source_inventory_complete: true
  original_requirement_sources:
    - 展示Bid#1.1.1.2.4.2.2.3
    - 展示Bid#1.1.1.2.4.2.2.8
    - 算法Bid#1.1.1.1.1.1.1.3.10
  permission_contract:
    product_role_is_not_permission_persona: true
    mock_user_permission_inference: prohibited
    final_authorization: server_fail_closed
    unauthorized_sensitive_value: do_not_render
  journeys:
    - {journey_id: REG-J01-INDEX, role: ROLE-REG-GOV, story_refs: [US-CHAIN-REG-01, US-CHAIN-REG-02, US-CHAIN-REG-05], primary_flow: [confirm_industry, configure_combo_and_weights, preview, submit, process, explicit_view_result], abnormal_flows: [illegal_combo, weight_invalid, custom_metric_unavailable, incomparable, permission_locked]}
    - {journey_id: REG-J02-COMPETITIVENESS, role: ROLE-REG-PARK, story_refs: [US-CHAIN-REG-03, US-CHAIN-REG-04, US-CHAIN-REG-05], primary_flow: [confirm_industry, configure_three_dimension_weights, submit, process, explicit_view_rank_and_gap], abnormal_flows: [dimension_unavailable, version_mix_forbidden, region_data_insufficient]}
  frame_specs:
    - {frame_id: F-REG-01, route_or_host: /industry-center/regional, source_refs: [US-CHAIN-REG-01, US-CHAIN-REG-03, US-CHAIN-REG-05], states: [empty_object, object_ready, permission_locked, unavailable], interactions: [switch_tab, open_compare_basket]}
    - {frame_id: F-REG-02, route_or_host: "/industry-center/regional?tab=index", source_refs: [US-CHAIN-REG-01, US-CHAIN-REG-02], states: [empty_object, config_invalid, previewing, submitting, processing, succeeded_wait_view, result, incomparable, partial_metric_gap, error_retry], interactions: [switch_mode, edit_weights, preview, submit, explicit_view_result]}
    - {frame_id: F-REG-03, route_or_host: "/industry-center/regional?tab=competitiveness", source_refs: [US-CHAIN-REG-03, US-CHAIN-REG-04], states: [empty_object, config_invalid, submitting, processing, succeeded_wait_view, result, incomparable, partial_metric_gap, error_retry], interactions: [edit_primary_weights, equalize, submit, explicit_view_result]}
    - {frame_id: F-REG-04, route_or_host: "/industry-center/regional?tab=records", source_refs: [US-CHAIN-REG-05], states: [empty, loading, filtered, error], interactions: [filter, open_process, open_result, copy_config]}
  feedback_rules:
    - {trigger: no_object, response: show_empty_object_bar_keep_config_disable_submit, recovery: open_compare_basket}
    - {trigger: illegal_combo, response: disable_submit_with_inline_reason, recovery: adjust_to_allowed_combo}
    - {trigger: weight_not_100, response: inline_delta_and_equalize_action, recovery: adjust_or_equalize}
    - {trigger: custom_metric_attempt, response: show_gap_not_available_this_round, recovery: use_preset_metrics}
    - {trigger: process_succeeded, response: show_view_result_only, recovery: user_clicks_view_result}
    - {trigger: incomparable, response: list_objects_and_reasons_no_fake_rank, recovery: align_model_and_weight_version}
  responsive_widths: [1920, 1680, 1440]
  accessibility_checks: [keyboard, focus, aria, contrast, reduced_motion, alternative_structure_list]
  metric_readiness_projection: []
  metric_readiness_projection_reason: no_matrix_rows_applicable_to_CHAIN_TOPIC_REGIONAL
  review_mounts:
    - {mount_id: CHAIN-REG-F01-OBJECT-CONTEXT, frame_id: F-REG-01, business_mode: absent}
    - {mount_id: CHAIN-REG-F02-INDEX-TITLE, frame_id: F-REG-02, business_mode: absent}
    - {mount_id: CHAIN-REG-F02-INDEX-METRICS, frame_id: F-REG-02, business_mode: absent}
    - {mount_id: CHAIN-REG-F02-CUSTOM-METRIC-GAP, frame_id: F-REG-02, business_mode: absent}
    - {mount_id: CHAIN-REG-F02-PREVIEW, frame_id: F-REG-02, business_mode: absent}
    - {mount_id: CHAIN-REG-F03-COMPETITIVENESS-TITLE, frame_id: F-REG-03, business_mode: absent}
    - {mount_id: CHAIN-REG-F03-COMPETITIVENESS-METRICS, frame_id: F-REG-03, business_mode: absent}
    - {mount_id: CHAIN-REG-F03-VERSION-BOUNDARY, frame_id: F-REG-03, business_mode: absent}
    - {mount_id: CHAIN-REG-F04-RECORDS, frame_id: F-REG-04, business_mode: absent}
  gaps:
    - {id: GAP-CHAIN-REG-CUSTOM-METRIC, summary: custom_metric_not_open_this_round, blocks_v1: false, blocks_stages: [pdr, v1_final, v2_lumen, production], v1_disposition: gap_visible, v1_treatment: preset_only_with_explicit_gap_copy, owner: "human:淮政玮", deadline: before_pdr, return_to: compliance}
    - {id: GAP-CHAIN-REG-METRICS, summary: regional_topic_metrics_and_readiness_rows_missing, blocks_v1: false, blocks_stages: [pdr, v1_final, v2_lumen, production], v1_disposition: gap_visible, v1_treatment: mock_pending_with_review_mounts, owner: "human:何老师", deadline: before_pdr, return_to: TRACE}
    - {id: GAP-CHAIN-REG-PERMISSIONS, summary: product_role_to_L0_L4_mapping_open, blocks_v1: false, blocks_stages: [pdr, v1_final, v2_lumen, production], v1_disposition: fail_closed, v1_treatment: server_reject_first_no_mock_inference, owner: "human:郭万迎", deadline: before_pdr, return_to: USM}
    - {id: GAP-CHAIN-REG-APPROVAL, summary: parent_regional_decision_provenance_incomplete, blocks_v1: false, blocks_stages: [pdr, v1_final, v2_lumen, production], v1_disposition: gap_visible, v1_treatment: keep_written_contract_until_scope_change, owner: "human:郭万迎", deadline: before_pdr, return_to: TRACE}
```

# UX-SPEC-CHAIN-TOPIC-SHENZHEN｜深圳产业决策

> 版本：1.4-result-asbuilt-20260807  
> 状态：ready_for_v1  
> 四件套版本：1.4-result-asbuilt-20260807  
> Track：Track-MS  
> screen_tier：medium_1440_1920  
> 体验 Owner：human:高颖  
> 独立执行权威：深圳产业决策交互只读本文件；父包 UX-SPEC 中 F-09/F-10 段落仅溯源。  
> 修订：对比结果对标研判三栏 + 报告区带入发展分析；发展结果来源依据与「针对」标签；完整对比抽屉只读展开；去掉对比顶 KPI / 发展摘要 KPI；Bid 旁注 ReviewOnly。

## 1. 权威输入与边界

本 UX-SPEC 只深化同目录 IA、TRACE、USM、Wireframe，并遵守：

- 展示 Bid `1.1.1.2.4.2.2.6` / `.2.2.7`（含 `.6.1`/`.6.2`/`.7.1`）；算法 Bid `.3.2` / `.3.5` / `.3.11` / `.3.12` / `.3.13`（服务依赖）；
- `Design.md`、`UX-UE 通用交互组件规范.md`、`data-lineage-policy.md`；
- 共享任务壳 SYS-ANALYSIS-JOBS；报告阅读 ENT-EXPORT；
- TRACE `source_manifest` 与 Gap 处置。

边界：

- 不改变产品范围、不增删 Bid 叶子；不代表 PDR/Gate 通过。
- 对比与发展各自独立追溯；发展分析不得静默绕过对比结构化结果。
- 主体固定「深圳」；禁止 PDF 作发展输入；禁止项目/预算/排期执行工具 UI。
- 无专题 readiness 矩阵行时不投影伪 D1–D4。
- 全景 / 诊断 / 区域 / 门户总览不在本包修改。

## 2. 四件套同步核对

| 核对项 | 产品结论 | UX 落点 | 结论 |
| --- | --- | --- | --- |
| 故事 | 5 | US-CHAIN-SZ-01…05 | 一致 |
| Frame | 4 | F-SZ-01…04 | 一致 |
| 路由 Tab | 3 | comparison / development / records | 一致 |
| Bid 叶子 | 2 | `.2.2.6` / `.2.2.7` | 未合并删除 |
| 对比→发展链 | 显式 `source_result_id` | §5 / F-SZ-03 | 已定义 |
| review mounts | 9 | Wireframe §10 | 一致 |
| readiness | 无专题矩阵行 | §9 `metric_readiness_projection: []` | 不投影伪 D1–D4 |

## 3. 用户旅程与任务流

### SZ-J01｜对比闭环

故事：`US-CHAIN-SZ-01/02/05`。  
主路径：确认产业 → `tab=comparison` 选标杆 → 生成分析 → 显式看结果 → 可选记录恢复。  
异常：无有效标杆、权限锁态、试图更换主体。

### SZ-J02｜发展闭环

故事：`US-CHAIN-SZ-03/04/05`。  
主路径：显式选有效对比结果 → 确认政策/技术/人才目标 → 生成分析 → 显式看建议与≥2 路径。  
异常：PDF/跨产业/过期/无权来源；静默继承被拒；路径不足两条不补造。

## 4. Frame 与承载映射

| Frame | 路由 / 宿主 | 故事 | 承载 |
| --- | --- | --- | --- |
| F-SZ-01 | `/industry-center/shenzhen` | 全部 | 对象上下文、固定主体、Tab |
| F-SZ-02 | `?tab=comparison` | US-01/02 | 标杆/四维/过程/对比结果 |
| F-SZ-03 | `?tab=development` | US-03/04 | 来源结果/目标/建议路径 |
| F-SZ-04 | `?tab=records` | US-05 | 本工作空间历史过滤与恢复 |

## 5. 交互与状态转换

### 5.1 F-SZ-01 壳

- Tab 写 URL；共享产业对象；主体文案固定「深圳」不可编辑。
- 无对象：对象条空态 +「打开对比篮」；配置区仍完整展示；「生成分析」禁用。
- 禁止：页内私有产业 Select；模块私有篮；更换主体为非深圳。

### 5.2 F-SZ-02 情况对比

| 触发 | 结果 | 禁止 |
| --- | --- | --- |
| 选标杆 | 四级可搜索 Cascader（与产业总览同源）多选 1～5；**选项树自带就绪/未就绪**（未就绪灰显禁用+原因）；生成分析校验至少 1 个就绪；**不单独提供「就绪检测」按钮**；控件可编辑白底；就绪门禁说明旁注**仅评审态（ReviewOnly）** | 国内城市扁平 Select；业务态露出就绪机制旁注；可编辑标杆控件置灰 |
| 生成分析 | 校验≥1 有效标杆后建任务；`taskType=chain:shenzhen:shenzhen_comparison`（稳定，不含对象/快照）；同 Tab 已有排队/分析中任务则**恢复原过程页**（SYS-JOBS 互斥） | 无标杆仍提交；把参数拼进 taskType 绕开互斥；同 Tab 并行第二条非终态 |
| 查看结果 | 不可变结构化结论；**对标研判**（副标「独特优势 · 差距与劣势」）三栏：独特优势｜差距｜劣势；综合判断区：市场前景/技术成熟度/链条完整性/所处阶段/阶段特征；差距≠劣势；不单开「优势与劣势」；**Bid 旁注仅评审态** | 用新数据改写旧快照；差距与劣势合成一栏；再拆重复「优势与劣势」；三评估仅埋散文；业务态露出 Bid 旁注 |
| 结果页「带入发展分析」 | 与「生成/查看报告」同行收口（分析报告区）；文案「带入发展分析」；显式带 `source_result_id`；禁止结果区单独占一行 CTA | 自动跳进发展并静默带入；按钮单独占一整行 |

### 5.3 F-SZ-03 发展分析

| 触发 | 结果 | 禁止 |
| --- | --- | --- |
| 选来源结果 | 校验同产业/有效/结构兼容 | PDF、跨产业、过期、无权 |
| 生成分析 | 绑定 `source_result_id`；`taskType=chain:shenzhen:shenzhen_development`；同 Tab 非终态任务恢复原过程页 | 静默继承最近对比；同 Tab 并行第二条非终态 |
| 查看结果 | 顶部「来源依据」展示短板与优势摘要；「展开完整对比结果」以**抽屉只读**打开（URL 仍停在发展结果）；三类建议与≥2 路径挂「针对」；**不挂发展摘要 KPI** | 无来源依据直接抛建议；整页跳转对比结果致返回路径丢失；改写来源快照；装饰性 KPI 条；项目执行工具 UI；不足两条补造 |

### 5.4 F-SZ-04 记录

- 与 `F-REG-04` / `F-DIAG-05` 对齐：列含提交/完成时间与报告份数；操作=查看结果 / 复制配置 / 关联报告（无「查看任务进度」）。
- 过滤后列表恢复到对应 Tab 配置草稿或结果；关联报告进报告态。
- `queued` 撤回遵循共享任务合同；`running` 不提供用户取消。

每业务 Frame 状态覆盖：`empty_object` / `loading` / `config_invalid` / `permission_locked` / `no_benchmark` / `submitting` / `processing` / `succeeded_wait_view` / `result` / `source_invalid` / `incomplete_paths` / `stale_benchmark_note` / `error_retry`。

## 6. 反馈与异常恢复

| 场景 | 反馈 | 恢复 |
| --- | --- | --- |
| permission_locked | 锁态 + 原因；隐藏敏感摘要 | 申请权限或降级只读 |
| no_benchmark | 禁用生成；说明无有效标杆 | 调整标杆选择 |
| source_invalid | 说明拒绝原因（PDF/跨产业/过期等） | 改选有效结构化结果 |
| incomplete_paths | 明示缺口；不补造伪路径 | 等待正式服务或调整目标 |
| stale_benchmark_note | 仅标注局限不改结论 | 继续阅读旧快照 |
| submit 失败 | 原位错误 + 可重试 | 配置保留后重提 |

## 7. 组件、键盘与无障碍

- Tabs：Arco Tabs，方向键切换，选中态可见。
- 表单控件可键盘操作；禁用控件须可读原因。
- 标杆区域：Arco Cascader（可搜索、多选 1～5、`changeOnSelect`），选项树与产业总览区域分布同源；焦点/ARIA 遵循通用交互规范 Cascader 条款；**可编辑态白底 + 显式描边**（默认状态框不可丢），与只读 Input 置灰区分（`diagnosis-config-control--editable` / `sci-arco-cascader`）。
- 四维模型区：业务态仅保留标题「四维模型（只读确认）」+ 表格；维度说明旁注与「只读」角标仅评审态；不提供设置/引用类操作入口。
- 图表：需提供等价数据表或可读摘要。

## 8. 响应式行为

同 Wireframe：1920/1680 图表并排；1440 起结果区可上下堆叠。宽度验收：1920 / 1680 / 1440。不声明专题小屏 `small_reflow`。

## 9. 内部评审投影

| Frame | mount_id | BusinessMode |
| --- | --- | --- |
| F-SZ-01 | CHAIN-SZ-F01-OBJECT-CONTEXT | absent |
| F-SZ-02 | COMPARE-TITLE / COMPARE-METRICS / BENCHMARK-READY | absent |
| F-SZ-03 | DEV-TITLE / DEV-EVIDENCE / SOURCE-RESULT / CASE-GAP | absent |
| F-SZ-04 | CHAIN-SZ-F04-RECORDS | absent |

`metric_readiness_projection: []`（无专题矩阵行时不投影伪 D1–D4）。完整挂点清单见 §12 `review_mounts`（9）。

## 10. Demo 实施交接

1. 路由与 Tab：`/industry-center/shenzhen?tab=comparison|development|records`；过程态 `demo_state=processing`；结果态 `demo_state=result`。  
2. Frame/Mount 目标 ID：`F-SZ-*` / `CHAIN-SZ-*`；禁止回扩 `F-CHAIN-09/10` 与 `CHAIN-TOPIC-F09/F10`。  
3. 标杆区域复用 `REGION_CASCADER_OPTIONS`（产业总览四级地域）；支持国际；禁止私有国内城市 Select。  
4. 发展分析必须显式 `source_result_id`；PDF 输入入口不得伪装可用。  
5. 任务流：显式提交 → 过程 → 显式看结果；禁止完成后自动跳结果。  
6. 全球案例匹配：可见 Gap，不宣称已交付。

## 11. 缺口与阻断项

| Gap | blocks_v1 | blocks_stages | V1 处置 |
| --- | --- | --- | --- |
| GAP-CHAIN-SZ-METRICS | false | pdr, v1_final, v2_lumen, production | Mock/Pending + 评审挂点 |
| GAP-CHAIN-SZ-PERMISSIONS | false | pdr, v1_final, v2_lumen, production | fail closed |
| GAP-CHAIN-SZ-APPROVAL | false | pdr, v1_final, v2_lumen, production | 合同沿用；范围变化补批 |
| GAP-CHAIN-SZ-CASE-LIBRARY | false | pdr, v1_final, v2_lumen, production | 不宣称案例匹配已交付 |

上述缺口均有安全、确定且可见的 V1 处理，故不阻断 V1 高保真首轮。

## 12. 机器可读交付契约

```yaml
ux_spec_contract:
  module_key: CHAIN-TOPIC-SHENZHEN
  version: "1.4-result-asbuilt-20260807"
  status: ready_for_v1
  source_four_pack:
    - IA-CHAIN-TOPIC-SHENZHEN.md
    - TRACE-CHAIN-TOPIC-SHENZHEN.yaml
    - USM-CHAIN-TOPIC-SHENZHEN.md
    - Wireframe-CHAIN-TOPIC-SHENZHEN.md
  screen_tier: medium_1440_1920
  delivery_stage: v1_hifi_round1
  product_scope_mutation: prohibited
  demo_code_mutation: prohibited
  source_inventory_complete: true
  original_requirement_sources:
    - 展示Bid#1.1.1.2.4.2.2.6
    - 展示Bid#1.1.1.2.4.2.2.7
    - 算法Bid#1.1.1.1.1.1.1.3.2
    - 算法Bid#1.1.1.1.1.1.1.3.5
    - 算法Bid#1.1.1.1.1.1.1.3.11
    - 算法Bid#1.1.1.1.1.1.1.3.12
    - 算法Bid#1.1.1.1.1.1.1.3.13
  permission_contract:
    product_role_is_not_permission_persona: true
    mock_user_permission_inference: prohibited
    final_authorization: server_fail_closed
    unauthorized_sensitive_value: do_not_render
  journeys:
    - {journey_id: SZ-J01-COMPARISON, role: ROLE-SZ-GOV, story_refs: [US-CHAIN-SZ-01, US-CHAIN-SZ-02, US-CHAIN-SZ-05], primary_flow: [confirm_industry, select_benchmarks, submit, process, explicit_view_result], abnormal_flows: [no_valid_benchmark, permission_locked, subject_change_rejected]}
    - {journey_id: SZ-J02-DEVELOPMENT, role: ROLE-SZ-GOV, story_refs: [US-CHAIN-SZ-03, US-CHAIN-SZ-04, US-CHAIN-SZ-05], primary_flow: [explicit_select_source_result, confirm_goals, submit, process, explicit_view_advice_and_paths], abnormal_flows: [pdf_rejected, cross_industry_source, expired_source, silent_inherit_rejected, incomplete_paths]}
  frame_specs:
    - {frame_id: F-SZ-01, route_or_host: /industry-center/shenzhen, source_refs: [US-CHAIN-SZ-01, US-CHAIN-SZ-03, US-CHAIN-SZ-05], states: [empty_object, object_ready, permission_locked, unavailable], interactions: [switch_tab, open_compare_basket]}
    - {frame_id: F-SZ-02, route_or_host: "/industry-center/shenzhen?tab=comparison", source_refs: [US-CHAIN-SZ-01, US-CHAIN-SZ-02], states: [empty_object, config_invalid, no_benchmark, submitting, processing, succeeded_wait_view, result, stale_benchmark_note, error_retry], interactions: [select_benchmarks, submit, explicit_view_result, explicit_carry_to_development]}
    - {frame_id: F-SZ-03, route_or_host: "/industry-center/shenzhen?tab=development", source_refs: [US-CHAIN-SZ-03, US-CHAIN-SZ-04], states: [empty_object, config_invalid, source_invalid, submitting, processing, succeeded_wait_view, result, incomplete_paths, error_retry], interactions: [select_source_result, confirm_goals, submit, explicit_view_result]}
    - {frame_id: F-SZ-04, route_or_host: "/industry-center/shenzhen?tab=records", source_refs: [US-CHAIN-SZ-05], states: [empty, loading, filtered, error], interactions: [filter, open_result, copy_config, open_related_reports]}
  feedback_rules:
    - {trigger: no_object, response: show_empty_object_bar_keep_config_disable_submit, recovery: open_compare_basket}
    - {trigger: no_valid_benchmark, response: disable_submit_with_reason, recovery: adjust_benchmarks}
    - {trigger: pdf_or_invalid_source, response: reject_with_explicit_reason, recovery: select_valid_structured_result}
    - {trigger: process_succeeded, response: show_view_result_only, recovery: user_clicks_view_result}
    - {trigger: incomplete_paths, response: show_gap_without_fabricating_paths, recovery: wait_formal_service_or_adjust_goals}
  responsive_widths: [1920, 1680, 1440]
  accessibility_checks: [keyboard, focus, aria, contrast, reduced_motion, alternative_structure_list]
  metric_readiness_projection: []
  metric_readiness_projection_reason: no_matrix_rows_applicable_to_CHAIN_TOPIC_SHENZHEN
  review_mounts:
    - {mount_id: CHAIN-SZ-F01-OBJECT-CONTEXT, frame_id: F-SZ-01, business_mode: absent}
    - {mount_id: CHAIN-SZ-F02-COMPARE-TITLE, frame_id: F-SZ-02, business_mode: absent}
    - {mount_id: CHAIN-SZ-F02-COMPARE-METRICS, frame_id: F-SZ-02, business_mode: absent}
    - {mount_id: CHAIN-SZ-F02-BENCHMARK-READY, frame_id: F-SZ-02, business_mode: absent}
    - {mount_id: CHAIN-SZ-F03-DEV-TITLE, frame_id: F-SZ-03, business_mode: absent}
    - {mount_id: CHAIN-SZ-F03-DEV-EVIDENCE, frame_id: F-SZ-03, business_mode: absent}
    - {mount_id: CHAIN-SZ-F03-SOURCE-RESULT, frame_id: F-SZ-03, business_mode: absent}
    - {mount_id: CHAIN-SZ-F03-CASE-GAP, frame_id: F-SZ-03, business_mode: absent}
    - {mount_id: CHAIN-SZ-F04-RECORDS, frame_id: F-SZ-04, business_mode: absent}
  gaps:
    - {id: GAP-CHAIN-SZ-METRICS, summary: shenzhen_topic_metrics_and_readiness_rows_missing, blocks_v1: false, blocks_stages: [pdr, v1_final, v2_lumen, production], v1_disposition: gap_visible, v1_treatment: mock_pending_with_review_mounts, owner: "human:何老师", deadline: before_pdr, return_to: TRACE}
    - {id: GAP-CHAIN-SZ-PERMISSIONS, summary: product_role_to_L0_L4_mapping_open, blocks_v1: false, blocks_stages: [pdr, v1_final, v2_lumen, production], v1_disposition: fail_closed, v1_treatment: server_reject_first_no_mock_inference, owner: "human:郭万迎", deadline: before_pdr, return_to: USM}
    - {id: GAP-CHAIN-SZ-APPROVAL, summary: parent_shenzhen_decision_provenance_incomplete, blocks_v1: false, blocks_stages: [pdr, v1_final, v2_lumen, production], v1_disposition: gap_visible, v1_treatment: keep_written_contract_until_scope_change, owner: "human:郭万迎", deadline: before_pdr, return_to: TRACE}
    - {id: GAP-CHAIN-SZ-CASE-LIBRARY, summary: global_case_matching_not_delivered, blocks_v1: false, blocks_stages: [pdr, v1_final, v2_lumen, production], v1_disposition: gap_visible, v1_treatment: explicit_gap_no_case_claim, owner: "human:淮政玮", deadline: before_pdr, return_to: compliance}
```

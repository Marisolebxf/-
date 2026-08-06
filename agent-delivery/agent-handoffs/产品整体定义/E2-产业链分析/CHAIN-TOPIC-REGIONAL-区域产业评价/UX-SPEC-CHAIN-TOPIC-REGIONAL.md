# UX-SPEC-CHAIN-TOPIC-REGIONAL｜区域产业评价

> 版本：1.9-result-rank-leaf  
> 状态：ready_for_v1  
> 四件套版本：1.9-result-rank-leaf  
> Track：Track-MS  
> screen_tier：medium_1440_1920  
> 体验 Owner：human:高颖  
> 独立执行权威：区域产业评价交互只读本文件；父包 UX-SPEC 中 F-07/F-08 段落仅溯源。  
> 修订补充（2026-08-06）：指数配置对齐企业评估——官方模板、不铺全库、添加指标下拉、保存个人模板（`DEC-CHAIN-REG-INDEX-TEMPLATE-UX-20260806`）。  
> 修订补充（2026-08-06）：计入/未计入 vs 移除拆分（`DEC-CHAIN-REG-INDEX-INCLUDE-VS-REMOVE-20260806`）；个人模板只存已计入；取消计入不自动均分。  
> 修订补充（2026-08-06）：结果 KPI 主体化 + 四力排名表 + 已计入叶子贡献（`DEC-CHAIN-REG-INDEX-RESULT-RANK-LEAF-20260806`）。

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
- 指数 Tab **必达**自定义指标（从库添加）、权重、评价对象；交互=官方模板 + 添加下拉 + 个人模板（对齐 ENT-EVAL）。
- **禁止**默认把全库指标铺进权重表；表内仅当前工作集（可含未计入行）。
- 无专题 readiness 矩阵行时不投影伪 D1–D4；数据缺口走 `GAP-CHAIN-REG-METRICS`。
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
| review mounts | 12 | Wireframe §10 | 一致 |
| 自定义配置三件套 | 对象+权重+从库添加指标 | §5.2 / F-REG-02 | Bid 必达 |
| 模板 UX | 官方模板 / 添加指标 / 个人模板 | §5.2；参照 ENT-EVAL | `DEC-CHAIN-REG-INDEX-TEMPLATE-UX` |
| readiness | 无专题矩阵行 | §9 `metric_readiness_projection: []` | 不投影伪 D1–D4 |

## 3. 用户旅程与任务流

### REG-J01｜政府指数评价闭环

故事：`US-CHAIN-REG-01/02/05`。  
主路径：确认产业对象 → `tab=index` 配评价对象 → 加载官方模板（或选我的模板）→ 底分就绪 → 调权 / 添加指标（配置即时汇总随刷新）→（可选）保存个人模板 → 生成分析 → 共享过程 → 显式查看结果。  
异常：非法组合、权重错误、拟添加指标不可用、切换模板冲突、不可比较对象、权限锁态。

### REG-J02｜园区竞争力评价闭环

故事：`US-CHAIN-REG-03/04/05`。  
主路径：确认产业对象 → `tab=competitiveness` 确认三维权重 → 生成分析 → 显式查看排名短板。  
异常：维度缺失、版本混排禁止、数据不足区域。

## 4. Frame 与承载映射

| Frame | 路由 / 宿主 | 故事 | 承载 |
| --- | --- | --- | --- |
| F-REG-01 | `/industry-center/regional` | 全部 | 对象上下文、Tab、权限锁态 |
| F-REG-02 | `?tab=index` | US-01/02 | 组合/四力预设指标/权重/预览/过程/结果 |
| F-REG-03 | `?tab=competitiveness` | US-03/04 | 三维一级权重/过程/排名短板 |
| F-REG-04 | `?tab=records` | US-05 | 本工作空间历史过滤与恢复 |

## 5. 交互与状态转换

### 5.1 F-REG-01 壳

- Tab 切换写 URL，保留产业对象；不携带另一 Tab 的区域/权重/预览/结果焦点。
- 无对象：对象条空态 +「打开对比篮」；配置区仍完整展示；「生成分析」禁用。
- **配置首行（两 Tab 共用）**：分析对象 / 评价模式 / 对比或评价区域三字段同行（`diagnosis-config-identity--3`）；`requiredSymbol={false}` + 内联必填 `*`。
- **权重配置**：诊断同款 `Table`；指数 Tab 列为「计入 | 名称 | 分组 | 状态 | 权重 | 来源 | 说明 | 操作(移除)」；禁止卡片宫格。
- **业务 / 评审分层**：顶部配置说明、「可调」Tag、即时汇总「非正式结果」说明进 `ReviewOnly`；业务态保留：模板选择器、工作集指标表、「添加指标」、配置即时汇总、保存个人模板、一键均分。
- **结果概要标题（两 Tab）**：与产业运行诊断同序——`{分析对象} · {评价类型}结果`（例：`半导体照明产业 · 区域产业指数评价结果`）；摘要区业务态展示分析对象名称。
- 禁止：页内私有产业 Select；区域入篮；模块自建浮层篮；无对象时整页空白无说明；配置选择器竖排占多行。

### 5.2 F-REG-02 指数

| 触发 | 结果 | 禁止 |
| --- | --- | --- |
| 切换评价模式 | 校验组合上限；非法时禁用提交 | 自动删对象凑合法 |
| 选择评估模板 | 系统模板/我的模板/当次配置；默认官方模板；恢复工作集+权重且全部计入；不恢复对象 | 默认铺全库；静默覆盖未确认的当次改动 |
| 添加指标 | 按钮→下拉列出未入工作集的库内项（可按四力）；追加后默认计入，可调权 | 无源新建口径；删库项；一次勾选全库 |
| 取消计入 / 再计入 | Checkbox；取消后行保留灰显、权重冻结；不自动均分；再勾回用原权重 | 取消勾选直接删行；静默改他人权重 |
| 移除 | 操作列「移除」退出工作集；回落到添加下拉；≠删库 | 用取消勾选充当移除；删库项 |
| 保存为个人模板 | 校验已计入权重合计 100% 后，仅存名称+**已计入**指标+权重 | 写入未计入项；写入评价对象；改官方模板 |
| 改权重 | 表格内 InputNumber；一键均分仅作用已计入；未计入权重禁用 | 静默归一化；卡片宫格；四力写成 Bid 原文 |
| 调权重 / 计入 | 配置即时汇总刷新（底分×权重）；不建 task（`DEC-CHAIN-REG-INDEX-WYSIWYG-INLINE-20260806`） | 独立轻量预览按钮；无底分时展示伪正式综合指数；写入分析记录 |
| 生成分析 | 最终校验 → 创建任务（固化 template 快照）→ 过程态 | 未点按钮自动创建 |
| 查看分析结果 | 不可变结果；分层=KPI（写清主体）→ 四力排名表 → 已计入叶子贡献 → 优势短板 | 自动跳转；KPI 裸写「领先/关注」不写主体；结果只展示四力组名无叶子 |
| 拟添加指标不可用 | 禁止加入并说明数据缺口 | 以功能未开放回避 Bid |

**评价维度（原型加工词，QC11）**：四力仅为分组；结果须同时展示四力汇总与本次已计入叶子；旁注 ⚠️ 以角标挂载。不与竞争力 Tab 固定三维混用。

**模板 UX（对齐企业评估）**：见 `DEC-CHAIN-REG-INDEX-TEMPLATE-UX-20260806`；官方模板起步 + 添加指标下拉 + 保存个人模板。  
**计入 vs 移除**：见 `DEC-CHAIN-REG-INDEX-INCLUDE-VS-REMOVE-20260806`。  
**结果分层**：见 `DEC-CHAIN-REG-INDEX-RESULT-RANK-LEAF-20260806`。

**指数结果交互细则**：

| 区块 | 规则 | 禁止 |
| --- | --- | --- |
| KPI | 锚定综合指数第 1 名主体；多区域写区域名、多产业写产业名；优势/短板维取自该主体自身四力极值 | 跨主体拼装「领先商业力+关注学术力」；不写主体 |
| 四力排名对比 | 排名列 + 综合指数 + 四力；按综合指数降序 | 无序明细冒充对比 |
| 指标贡献 | 行=已计入叶子；四力作分组列；列含各对比主体得分与权重 | 只显示组名；铺全库未计入项 |
| 优势短板 | 文案含主体，可落到「四力·叶子」；QC11 角标 | 平铺长 Alert 替代角标 |

### 5.3 F-REG-03 竞争力

| 触发 | 结果 | 禁止 |
| --- | --- | --- |
| 调一级权重 | 三维固定展示；合计 100% | 增删维度、改内部算法 |
| 一键均分 | 三维各约 33.3%（演示可整百） | 静默改成两维 |
| 维度不可用 | 禁用生成并说明 | 降成两维继续算 |
| 查看结果 | 排名/三维/热力图摘要/短板/版本边界 | 跨版本混排 |

### 5.4 F-REG-04 记录

- 与 `F-DIAG-05` 对齐：列含提交/完成时间与报告份数；操作=查看结果 / 复制配置 / 关联报告（无「查看任务进度」）。
- 过滤后列表恢复到对应 Tab 配置草稿或结果；关联报告进报告态。
- `queued` 撤回遵循共享任务合同；`running` 不提供用户取消。

每业务 Frame 状态覆盖：`empty_object` / `loading` / `config_invalid` / `permission_locked` / `base_score_missing` / `submitting` / `processing` / `succeeded_wait_view` / `result` / `incomparable` / `partial_metric_gap` / `error_retry`。

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
| F-REG-02 | INDEX-TITLE / INDEX-TEMPLATE / INDEX-METRICS / CUSTOM-METRIC-ADD / PERSONAL-TEMPLATE / INDEX-DIM-FOUR-FORCE / PREVIEW | absent |
| F-REG-03 | COMPETITIVENESS-TITLE / COMPETITIVENESS-METRICS / VERSION-BOUNDARY | absent |
| F-REG-04 | CHAIN-REG-F04-RECORDS | absent |

`metric_readiness_projection: []`（无专题矩阵行时不投影伪 D1–D4）。完整挂点清单见 §12 `review_mounts`（12）。

## 10. Demo 实施交接

1. 路由与 Tab：`/industry-center/regional?tab=index|competitiveness|records`；过程态 `demo_state=processing`；结果态 `demo_state=result`。  
2. Frame/Mount 目标 ID：`F-REG-*` / `CHAIN-REG-*`；禁止回扩 `F-CHAIN-07/08` 与 `CHAIN-TOPIC-F07/F08`。  
3. 对象组合与权重校验必须前端拦截 + 服务端再校验；预览永不落任务库。  
4. 任务流：显式提交 → 过程 → 显式看结果；禁止完成后自动跳结果。  
5. **模板 UX（参照企业评估截图）**：默认官方系统模板（建议名「区域产业综合指数 V1.0」）；权重表只显示**工作集**；Checkbox=计入；「移除」退出工作集；「添加指标」下拉追加；底栏「保存为个人模板」+「生成分析」；Alert「调整仅对本次任务生效」。个人模板只固化已计入项；取消计入不自动均分。  
6. 竞争力文案用「配套环境」；语义对齐算法「配套生态」；竞争力 Tab 不抄个人模板（除非另开 DEC）。

## 11. 缺口与阻断项

| Gap | blocks_v1 | blocks_stages | V1 处置 |
| --- | --- | --- | --- |
| GAP-CHAIN-REG-CUSTOM-METRIC | — | — | **已关闭**（`DEC-CHAIN-REG-INDEX-CUSTOM-CONFIG-20260806`）；功能必达 |
| GAP-CHAIN-REG-METRICS | false | pdr, v1_final, v2_lumen, production | Mock/Pending + 评审挂点 |
| GAP-CHAIN-REG-PERMISSIONS | false | pdr, v1_final, v2_lumen, production | fail closed |
| GAP-CHAIN-REG-APPROVAL | false | pdr, v1_final, v2_lumen, production | 合同沿用；范围变化补批 |

上述缺口均有安全、确定且可见的 V1 处理，故不阻断 V1 高保真首轮。

## 12. 机器可读交付契约

```yaml
ux_spec_contract:
  module_key: CHAIN-TOPIC-REGIONAL
  version: "1.6-index-template-ux"
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
    - {journey_id: REG-J01-INDEX, role: ROLE-REG-GOV, story_refs: [US-CHAIN-REG-01, US-CHAIN-REG-02, US-CHAIN-REG-05], primary_flow: [confirm_industry, load_official_template, configure_objects, add_metrics_via_dropdown, inline_wysiwyg_refresh, optional_save_personal_template, submit, process, explicit_view_result], abnormal_flows: [illegal_combo, weight_invalid, base_score_missing, custom_metric_data_unavailable, template_switch_conflict, incomparable, permission_locked]}
    - {journey_id: REG-J02-COMPETITIVENESS, role: ROLE-REG-PARK, story_refs: [US-CHAIN-REG-03, US-CHAIN-REG-04, US-CHAIN-REG-05], primary_flow: [confirm_industry, configure_three_dimension_weights, submit, process, explicit_view_rank_and_gap], abnormal_flows: [dimension_unavailable, version_mix_forbidden, region_data_insufficient]}
  frame_specs:
    - {frame_id: F-REG-01, route_or_host: /industry-center/regional, source_refs: [US-CHAIN-REG-01, US-CHAIN-REG-03, US-CHAIN-REG-05], states: [empty_object, object_ready, permission_locked, unavailable], interactions: [switch_tab, open_compare_basket]}
    - {frame_id: F-REG-02, route_or_host: "/industry-center/regional?tab=index", source_refs: [US-CHAIN-REG-01, US-CHAIN-REG-02], states: [empty_object, config_invalid, base_score_missing, submitting, processing, succeeded_wait_view, result, incomparable, partial_metric_gap, error_retry], interactions: [switch_mode, select_template, add_metric_dropdown, save_personal_template, edit_weights, inline_wysiwyg_refresh, submit, explicit_view_result]}
    - {frame_id: F-REG-03, route_or_host: "/industry-center/regional?tab=competitiveness", source_refs: [US-CHAIN-REG-03, US-CHAIN-REG-04], states: [empty_object, config_invalid, submitting, processing, succeeded_wait_view, result, incomparable, partial_metric_gap, error_retry], interactions: [edit_primary_weights, equalize, submit, explicit_view_result]}
    - {frame_id: F-REG-04, route_or_host: "/industry-center/regional?tab=records", source_refs: [US-CHAIN-REG-05], states: [empty, loading, filtered, error], interactions: [filter, open_result, copy_config, open_related_reports]}
  feedback_rules:
    - {trigger: no_object, response: show_empty_object_bar_keep_config_disable_submit, recovery: open_compare_basket}
    - {trigger: illegal_combo, response: disable_submit_with_inline_reason, recovery: adjust_to_allowed_combo}
    - {trigger: weight_not_100, response: inline_delta_and_equalize_action, recovery: adjust_or_equalize}
    - {trigger: select_template, response: restore_indicators_and_weights_not_objects, recovery: confirm_if_dirty}
    - {trigger: add_metric_dropdown, response: append_library_metric_to_selected_rows, recovery: adjust_weights}
    - {trigger: save_personal_template, response: persist_name_indicators_weights_only, recovery: fix_weight_sum_if_needed}
    - {trigger: custom_metric_data_unavailable, response: block_add_with_metric_gap_reason, recovery: choose_available_library_metric}
    - {trigger: process_succeeded, response: show_view_result_only, recovery: user_clicks_view_result}
    - {trigger: incomparable, response: list_objects_and_reasons_no_fake_rank, recovery: align_model_and_weight_version}
  responsive_widths: [1920, 1680, 1440]
  accessibility_checks: [keyboard, focus, aria, contrast, reduced_motion, alternative_structure_list]
  metric_readiness_projection: []
  metric_readiness_projection_reason: no_matrix_rows_applicable_to_CHAIN_TOPIC_REGIONAL
  review_mounts:
    - {mount_id: CHAIN-REG-F01-OBJECT-CONTEXT, frame_id: F-REG-01, business_mode: absent}
    - {mount_id: CHAIN-REG-F02-INDEX-TITLE, frame_id: F-REG-02, business_mode: absent}
    - {mount_id: CHAIN-REG-F02-INDEX-TEMPLATE, frame_id: F-REG-02, business_mode: absent}
    - {mount_id: CHAIN-REG-F02-INDEX-METRICS, frame_id: F-REG-02, business_mode: absent}
    - {mount_id: CHAIN-REG-F02-CUSTOM-METRIC-ADD, frame_id: F-REG-02, business_mode: absent}
    - {mount_id: CHAIN-REG-F02-PERSONAL-TEMPLATE, frame_id: F-REG-02, business_mode: absent}
    - {mount_id: CHAIN-REG-F02-INDEX-DIM-FOUR-FORCE, frame_id: F-REG-02, business_mode: absent}
    - {mount_id: CHAIN-REG-F02-INLINE-WYSIWYG, frame_id: F-REG-02, business_mode: absent}
    - {mount_id: CHAIN-REG-F03-COMPETITIVENESS-TITLE, frame_id: F-REG-03, business_mode: absent}
    - {mount_id: CHAIN-REG-F03-COMPETITIVENESS-METRICS, frame_id: F-REG-03, business_mode: absent}
    - {mount_id: CHAIN-REG-F03-VERSION-BOUNDARY, frame_id: F-REG-03, business_mode: absent}
    - {mount_id: CHAIN-REG-F04-RECORDS, frame_id: F-REG-04, business_mode: absent}
  gaps:
    - {id: GAP-CHAIN-REG-CUSTOM-METRIC, summary: closed_by_DEC-CHAIN-REG-INDEX-CUSTOM-CONFIG-20260806, status: closed, v1_disposition: required_capability, v1_treatment: add_from_library_required, owner: "human:淮政玮", return_to: compliance}
    - {id: GAP-CHAIN-REG-METRICS, summary: regional_topic_metrics_and_readiness_rows_missing, blocks_v1: false, blocks_stages: [pdr, v1_final, v2_lumen, production], v1_disposition: gap_visible, v1_treatment: mock_pending_with_review_mounts, owner: "human:何老师", deadline: before_pdr, return_to: TRACE}
    - {id: GAP-CHAIN-REG-PERMISSIONS, summary: product_role_to_L0_L4_mapping_open, blocks_v1: false, blocks_stages: [pdr, v1_final, v2_lumen, production], v1_disposition: fail_closed, v1_treatment: server_reject_first_no_mock_inference, owner: "human:郭万迎", deadline: before_pdr, return_to: USM}
    - {id: GAP-CHAIN-REG-APPROVAL, summary: parent_regional_decision_provenance_incomplete, blocks_v1: false, blocks_stages: [pdr, v1_final, v2_lumen, production], v1_disposition: gap_visible, v1_treatment: keep_written_contract_until_scope_change, owner: "human:郭万迎", deadline: before_pdr, return_to: TRACE}
```

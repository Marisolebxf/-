# UX-SPEC-DS10-12｜科技政策跟踪（展示系统）

> 版本：v1.0 · 2026-08-05  
> 状态：ready_for_v1  
> 四件套版本：v1.0  
> Track：Track-MS（主）+ Track-L（大屏叙事裁剪，独立视觉规范）  
> screen_tier：medium_1440_1920  
> 体验 Owner：human:高颖 · 大屏 Owner：human:王亚东  
> task：POLICY-UX-L01

## 1. 权威输入与边界

### 1.1 权威输入

| 类型 | 文件 / 版本 | 本规格使用方式 |
| --- | --- | --- |
| IA | `IA-DS10-12-科技政策跟踪.md` v1.0 | 边界、三屏矩阵、与 E7/门户分轨 |
| TRACE | `TRACE-DS10-12-科技政策跟踪.yaml` v1.0 | 7 叶子映射、Gap、screen_tier 覆盖 |
| USM | `USM-DS10-12-科技政策跟踪.md` v1.0 | 11 故事、主/异常、验收 |
| Wireframe | `Wireframe-DS10-12-科技政策跟踪.md` v1.0 | F-DS-POL-* Frame 与字段 |
| 交互 / 视觉 | `UX-UE 通用交互组件规范.md` · `Design.md` | Track-MS 基线 |
| 数据治理 | `data-lineage-policy.md` | 指标 ⓘ / Mock / 待确认角标 |
| Track-L | 联通数智大屏规范 | 仅大屏 Frame；不套中屏密度 |

### 1.2 本轮边界

- 只转译四件套 v1.0；不改 Demo；不扩 Bid 叶子；不宣告 PDR 闭合。
- **分轨铁律**：展示 `/display/policy/*` ≠ 专题 `/policy/*` ≠ 门户 `/policy-portal/*`；页内对比不写 E7 系统对比篮；外链专题须确认条。
- 本契约 `screen_tier` 以 Track-MS 中屏三宽验收为主；小屏裁剪写在 §8；大屏 Frame 交互只读叙事，视觉归 Track-L Owner。
- `metric_readiness_projection: []`（无独立展示矩阵行时不伪填 D1–D4）；统计数字仍挂 metric_spec / Mock / ⚠️。

## 2. 四件套同步核对

### 2.1 故事与 Frame 覆盖

| Story | Frame | 结论 |
| --- | --- | --- |
| US-DS-POL-01~04 | F-DS-POL-10（+10S/10L） | 完整覆盖 |
| US-DS-POL-05 | F-DS-POL-11（+11L） | 完整覆盖 |
| US-DS-POL-06 | F-DS-POL-12 | 完整覆盖 |
| US-DS-POL-07 | F-DS-POL-PC01 | 完整覆盖 |
| US-DS-POL-08 | F-DS-POL-PC02 | 完整覆盖 |
| US-DS-POL-09 | F-DS-POL-PC03 | 完整覆盖 |
| US-DS-POL-10 | F-DS-POL-PC04 | 完整覆盖 |
| US-DS-POL-11 | 10S/10L/11L + 裁剪规则 | 完整覆盖 |

### 2.2 宿主与禁止

| 维度 | 结论 |
| --- | --- |
| 中屏路由 | `/display/policy/{panorama,evaluation,simulation,governance,parse,compare,insight-report}` |
| 大屏路由 | `/display-large/policy/{panorama,evaluation,simulation,insight-report}` |
| DS-10 vs PC-03 | 重点比对 Tab 与核增多维对比并存；可「升级对比」跳转，不互相替代 |
| 禁止 | 复用专题 storage/路由；展示页执行清洗作业；前端直连 Nebula/Python；大屏深表单 |

### 2.3 差异与缺口

`GAP-DS-PC-CATALOG`、`GAP-DS-ROUTE` 已分类；候选 route 以 IA/Wireframe 为准，catalog 回写不阻断本规格 `ready_for_v1`。

## 3. 用户旅程与任务流

### 3.1 J-DS-PANORAMA｜全景中屏

**Story**：`US-DS-POL-01~04`

主路径：进入全景 → 多维筛选 → 图+列表 → 动向/舆情/重点比对 Tab → 对比或标杆报告 → 可选升级核增对比或外链专题（确认条）。  
异常：无命中空态；加载失败重试；接待角色脱敏。

### 3.2 J-DS-EVAL｜评价中屏

**Story**：`US-DS-POL-05`

主路径：三区（分析/解读/推荐）→ 维度条驱动画布 → 方案调参模拟 → 模板导出。  
异常：口径待确认角标；计算中稳定容器无假百分比。

### 3.3 J-DS-SIM｜推演中屏

**Story**：`US-DS-POL-06`

主路径：预估表单仿真 → 多维评估 → 推演子导航（解析/影响/关联/路径/报告）。  
异常：无权限锁表单只读结果；图谱经 Java 不直连图库。

### 3.4 J-DS-PC｜核增对比研报

**Story**：`US-DS-POL-07~10`

主路径：治理看板确认底座 → 拆解结构化 → ≥2 对象多维对比 → 生成研报 → 溯源 → 导出 PDF/Word。  
异常：底座未就绪禁用对比/研报；失败明确态。

### 3.5 J-DS-TIER｜三屏差异消费

**Story**：`US-DS-POL-11`

大屏：只读热点/热力/轮播，无检索深交互与推演编辑。  
小屏：简化筛选、单列列表、关键图、报告阅读；无标杆多步向导与多图墙。

## 4. Frame 与承载映射

### 4.1 F-DS-POL-10 全景中屏

- 入口：菜单 → `/display/policy/panorama`；Tab：search / trends / sentiment / benchmark。
- 控件：筛选条、全景图、结果卡、对比勾选（演示上限 10）、标杆向导。
- 出口：详情/比对抽屉；升级 → `/display/policy/compare`；外链专题确认条。
- 禁止：写入 E7 对比篮；跳 `/policy/search`。

### 4.2 F-DS-POL-10S / 10L

- 10S：简化筛选 + KPI 一行 + 单列列表 + 底栏动向/订阅。
- 10L：深蓝叙事主视觉；讲解控制；点击仅简介浮层；无导出。

### 4.3 F-DS-POL-11 / 11L

- 11：三区 + 维度条 + 侧栏摘要/导出；推荐方案雷达与滑杆。
- 11L：效能亮点轮播；无完整调参。

### 4.4 F-DS-POL-12

- 左预估表单 / 右评估图 / 下推演子导航；仿真进结果容器；关联图走 API。

### 4.5 F-DS-POL-PC01~04

| Frame | 路由 | 关键交互 |
| --- | --- | --- |
| PC01 | `/display/policy/governance` | 四状态卡；底座未就绪禁用下游 CTA |
| PC02 | `/display/policy/parse` | 条款树/指标表/实体图；送入多维对比 |
| PC03 | `/display/policy/compare` | ≥2 对象、维度勾选、可视化、摘要、生成研报 |
| PC04 | `/display/policy/insight-report` | 目录/正文/溯源双向/PDF·Word |

## 5. 交互与状态转换

| 触发 | 结果 | 禁止 |
| --- | --- | --- |
| 全景查询 | 刷新图+列表；可写展示侧历史 | 共用专题 recent key |
| 加入对比（页内） | 重点比对或核增对比 | 写入系统对比篮 |
| 标杆一键报告 | 有对象才预览 | 空对象出空报告 |
| 评价调参 | 稳定「计算中」容器 | 假百分比 |
| 仿真提交 | 结果容器/任务态 | 前端假装算完 |
| 运行多维对比 | 表/雷达/图谱/摘要 | 单对象运行 |
| 生成研报 | 研报页可溯源 | 与专题 ENT-EXPORT 混同一下载中心文案 |
| 大屏点击 | 简介浮层 | 下钻敏感受众明细 |

## 6. 反馈与异常恢复

| 场景 | 反馈 | 下一步 |
| --- | --- | --- |
| 无命中 | 空态 + 放宽条件 CTA + MockBadge（Wave0） | 调整筛选 |
| 加载失败 | 错误条 + 重试 | 重试 / 回全景 |
| 无权限 | 锁态或只读 | 申请 / 仅浏览 |
| 底座未就绪 | 禁用对比/研报 + 治理说明 | 看 PC01 |
| 口径待确认 | ⚠️ + ⓘ MetricSpecCard | 继续演示 |
| 误入专题路由 | 分轨说明条 | 回 `/display/policy/*` |

## 7. 组件、键盘与无障碍

- Tabs / Form / Table / Drawer：Arco；方向键切 Tab；禁用可读原因。
- 图表 ECharts：提供表或摘要；地图下钻焦点回到列表首项。
- 图谱 G6：只读浏览须有键盘可选节点列表等价信息。
- 大屏：讲解控制可达；动画可用「减少动态」偏好降级为静态帧。
- 对比度：中屏 Design.md；大屏遵循 Track-L，不混中屏浅底。

## 8. 响应式行为

### 8.1 Track-MS 中屏（契约验收宽）

| 宽度 | 行为 |
| --- | --- |
| 1920 | 图列表双栏；评价多图并列 |
| 1680 | 侧栏可收；比对表横向滚动 |
| 1440 | 图上表下；推荐方案区堆叠 |

### 8.2 小屏裁剪（同路由自适应）

保留：简化筛选、列表、关键 KPI、报告阅读。  
裁剪：标杆多步向导、多图并列、推演参数编辑、雷达墙。

### 8.3 大屏（Track-L，非本契约 screen_tier）

只读叙事；无检索表单/推演编辑/敏感下钻；视觉规范独立。

## 9. 内部评审投影

| 宿主 | mount 意图 | BusinessMode |
| --- | --- | --- |
| 全景标题/分轨条 | requirement_trace + 与 E7 分轨说明 | absent |
| KPI / 分布图标题 | metric_spec（metric_id 见 Wireframe） | absent |
| 批次 | mock_badge | absent |
| QPOL 相关数字 | pending_badge ⚠️ | absent |

`metric_readiness_projection: []`。有矩阵后按 D1→DataHealthBadge(D2+D3)→D4，`max_markers: 3`，`spacing_px: 4`。

## 10. Demo 实施交接

1. 路由按 IA 候选 path 落地；catalog 回写跟进 GAP-DS-ROUTE。  
2. 全景四 Tab 能力不删叶子；页内对比与 E7 篮严格隔离。  
3. 评价/推演/核增按 Frame 分文件实现；底座门禁联动 PC01。  
4. 三屏：中屏完整；小屏裁剪；大屏独立壳与素材。  
5. 页脚或评审层固定分轨文案。  
6. 排除：专题工作台、门户扶持流程、前端直连算法图库。

**V1 Demo 激活**：本规格 `ready_for_v1` 允许中屏首轮高保真；大屏由 Track-L Owner 并行。随后用 `gkx-definition-to-demo`（中屏）+ `gkx-ui-design-standards`。

## 11. 缺口与阻断项

| Gap | blocks_v1 | blocks_stages | V1 处理 | owner | deadline | return_to |
| --- | --- | --- | --- | --- | --- | --- |
| GAP-DS-PC-CATALOG | false | pdr, production | TRACE 已按 scope-baseline 编号；catalog 补条 | human:高颖 | before_pdr | acceptance-catalog |
| GAP-DS-ROUTE | false | pdr, production | Demo 使用 IA 候选 route；门1后回写 catalog | human:高颖 | before_pdr | acceptance-catalog |
| QPOL-01/02/03 口径 | false | pdr, v1_final, production | ⚠️ + 临时默认 | human:高颖 | before_pdr | 客户决策清单跟踪表.md |

无 `blocks_v1: true`。

## 12. 机器可读交付契约

```yaml
ux_spec_contract:
  module_key: DS10-12-科技政策跟踪
  version: "1.0"
  status: ready_for_v1
  source_four_pack:
    - IA-DS10-12-科技政策跟踪.md
    - TRACE-DS10-12-科技政策跟踪.yaml
    - USM-DS10-12-科技政策跟踪.md
    - Wireframe-DS10-12-科技政策跟踪.md
  screen_tier: medium_1440_1920
  delivery_stage: v1_hifi_round1
  product_scope_mutation: prohibited
  demo_code_mutation: prohibited
  journeys:
    - journey_id: J-DS-PANORAMA
      role: 政府用户/高校科研机构和企业/智库用户
      story_refs: [US-DS-POL-01, US-DS-POL-02, US-DS-POL-03, US-DS-POL-04]
      primary_flow:
        - 进入科创政策全景中屏
        - 多维检索并切换动向舆情比对
        - 完成重点比对或升级核增对比
      abnormal_flows:
        - 无命中空态放宽条件
        - 外链专题前确认分轨
    - journey_id: J-DS-EVAL
      role: 政府用户/智库用户
      story_refs: [US-DS-POL-05]
      primary_flow:
        - 进入评价三区
        - 维度驱动可视化与方案模拟
        - 导出报告模板产物
      abnormal_flows:
        - 口径待确认角标继续演示
        - 计算中容器无假百分比
    - journey_id: J-DS-SIM
      role: 政府用户
      story_refs: [US-DS-POL-06]
      primary_flow:
        - 提交效果预估参数
        - 查看推演解析与关联结果
      abnormal_flows:
        - 无权限锁表单只读
        - 图谱经API不直连图库
    - journey_id: J-DS-PC
      role: 政府用户/智库用户
      story_refs: [US-DS-POL-07, US-DS-POL-08, US-DS-POL-09, US-DS-POL-10]
      primary_flow:
        - 确认治理底座状态
        - 拆解后多维对比并生成研报
        - 溯源并导出
      abnormal_flows:
        - 底座未就绪禁用下游
        - 少于两对象禁止运行对比
    - journey_id: J-DS-TIER
      role: 访问人员/业务用户
      story_refs: [US-DS-POL-11]
      primary_flow:
        - 大屏只读叙事浏览
        - 小屏完成裁剪后检索与阅读
      abnormal_flows:
        - 大屏拒绝深表单与敏感下钻
        - 小屏隐藏标杆多步向导
  frame_specs:
    - frame_id: F-DS-POL-10
      route_or_host: /display/policy/panorama
      source_refs: [US-DS-POL-01, US-DS-POL-02, US-DS-POL-03, US-DS-POL-04]
      states: [default, loading, empty, error, permission]
      interactions: [multi_filter_search, tab_switch, add_page_compare, benchmark_report]
    - frame_id: F-DS-POL-10S
      route_or_host: /display/policy/panorama?tier=small
      source_refs: [US-DS-POL-11]
      states: [default, loading, empty, error, permission]
      interactions: [simplified_filter, list_browse, open_kpi]
    - frame_id: F-DS-POL-10L
      route_or_host: /display-large/policy/panorama
      source_refs: [US-DS-POL-11]
      states: [default, loading, empty, error, permission]
      interactions: [narrative_play, hotspot_rotate, open_brief_overlay]
    - frame_id: F-DS-POL-11
      route_or_host: /display/policy/evaluation
      source_refs: [US-DS-POL-05]
      states: [default, loading, empty, error, permission]
      interactions: [switch_report_zone, dimension_filter, scheme_simulate, export_template]
    - frame_id: F-DS-POL-11L
      route_or_host: /display-large/policy/evaluation
      source_refs: [US-DS-POL-11]
      states: [default, loading, empty, error, permission]
      interactions: [highlight_carousel, read_only_browse]
    - frame_id: F-DS-POL-12
      route_or_host: /display/policy/simulation
      source_refs: [US-DS-POL-06]
      states: [default, loading, empty, error, permission]
      interactions: [submit_simulation, open_relation_graph, open_interpretation]
    - frame_id: F-DS-POL-PC01
      route_or_host: /display/policy/governance
      source_refs: [US-DS-POL-07]
      states: [default, loading, empty, error, permission]
      interactions: [view_pipeline_status, gate_downstream_cta]
    - frame_id: F-DS-POL-PC02
      route_or_host: /display/policy/parse
      source_refs: [US-DS-POL-08]
      states: [default, loading, empty, error, permission]
      interactions: [select_policy, view_clause_tree, send_to_compare]
    - frame_id: F-DS-POL-PC03
      route_or_host: /display/policy/compare
      source_refs: [US-DS-POL-09]
      states: [default, loading, empty, error, permission]
      interactions: [configure_objects_dims, run_compare, export_summary, generate_insight_report]
    - frame_id: F-DS-POL-PC04
      route_or_host: /display/policy/insight-report
      source_refs: [US-DS-POL-10]
      states: [default, loading, empty, error, permission]
      interactions: [read_modules, bidirectional_trace, export_pdf_word]
  feedback_rules:
    - empty_with_mock_badge
    - permission_lock_or_readonly
    - governance_gate_disables_compare_report
    - boundary_banner_vs_topic_policy
    - no_fake_percent_progress
  responsive_widths: [1920, 1680, 1440]
  accessibility_checks: [keyboard, focus, aria, contrast]
  metric_readiness_projection: []
  review_mounts:
    - DS-POL-F10-TITLE-TRACE
    - DS-POL-F10-BOUNDARY-TRACE
    - DS-POL-F10-MOCK
    - DS-POL-F10-TOTAL-METRIC
    - DS-POL-F11-EFFECT-METRIC
    - DS-POL-F12-EFFECT-METRIC
    - DS-POL-PC03-SUPPORT-METRIC
    - DS-POL-PC04-TRACE-PANEL
  gaps:
    - id: GAP-DS-PC-CATALOG
      summary: acceptance-catalog 尚未登记 DS-PC-01到04，TRACE 已按 scope-baseline 编号
      blocks_v1: false
      blocks_stages: [pdr, production]
      v1_disposition: gap_visible
      v1_treatment: deterministic_demo_contract
      owner: human:高颖
      deadline: before_pdr
      return_to: acceptance-catalog
    - id: GAP-DS-ROUTE
      summary: catalog 中 DS-10/11/12 route 为空，Demo 使用 IA 候选 route
      blocks_v1: false
      blocks_stages: [pdr, production]
      v1_disposition: gap_visible
      v1_treatment: deterministic_demo_contract
      owner: human:高颖
      deadline: before_pdr
      return_to: acceptance-catalog
    - id: GAP-DS-QPOL-CALIBER
      summary: 类型分布与力度相关口径待甲方确认，演示保留警告角标
      blocks_v1: false
      blocks_stages: [pdr, v1_final, production]
      v1_disposition: gap_visible
      v1_treatment: deterministic_demo_contract
      owner: human:高颖
      deadline: before_pdr
      return_to: 客户决策清单跟踪表.md
```

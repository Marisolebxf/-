# UX-SPEC-E7｜政策分析

> 版本：v1.0 · 2026-08-05  
> 状态：ready_for_v1  
> 四件套版本：v1.4.3  
> Track：Track-MS  
> screen_tier：medium_1440_1920  
> 体验 Owner：human:高颖  
> task：POLICY-UX-L01

## 1. 权威输入与边界

### 1.1 权威输入

| 类型 | 文件 / 版本 | 本规格使用方式 |
| --- | --- | --- |
| IA | `IA-E7-政策分析.md` v1.4.3 | 模块边界、对象流、三共享能力、空态分支、查询复用 |
| TRACE | `TRACE-E7-政策分析.yaml` v1.4.x | Bid/决策、故事验收、Gap、门户/OPS 合同 |
| USM | `USM-E7-政策分析.md` v1.4.3 | 9 故事、主/异常路径、验收场景 |
| Wireframe | `Wireframe-E7-政策分析.md` v1.4.3 | F-POL-* Frame、状态机、评审挂载 |
| 评审治理 | `产品定义评审规程.md` | Track-MS 顺序；本规格不宣告 PDR 闭合 |
| 交互规范 | `UX-UE 通用交互组件规范.md` | Arco、状态、键盘、焦点、无障碍 |
| 视觉规范 | `Design.md` | medium_1440_1920、主色与控件基线 |
| 数据治理 | `data-lineage-policy.md` | 指标呈现边界；不自填 D1–D4 |
| 共享壳 | `UX-SPEC-ENT-COMPARE` / `SYS-ANALYSIS-JOBS` / `ENT-EXPORT` | 篮/任务/报告壳层继承，本包只写政策接入 |

### 1.2 本轮边界

- 只把四件套 v1.4.3 转为可实现交互规则，不新增/删减 Bid 叶子，不改 Demo 代码，不推进 PDR/Gate。
- **唯一分析发起路径**：查询/门户入篮 → 系统对比篮政策 Tab「发起分析」→ 三项分析配置→任务→结果→报告（HTML→PDF）。
- **禁止**：查询/门户「深度分析」直达；页内第二套对比篮；篮内出分析图；跳过 HTML 直出 PDF；独立政策任务/下载中心。
- 展示系统 DS-10/11/12 与核增对比结果页不在本规格。
- `metric_readiness_projection` 为空列表：尚无 `metric-readiness-matrix-POLICY.yaml`（GAP-E7-03）；Wireframe 已声明 metric_spec / Mock / Pending 挂载，V1 按矩阵缺省时仅投影已声明挂载类型。

## 2. 四件套同步核对

### 2.1 故事与 Frame 覆盖

| Story | 交互目标 | Frame | 结论 |
| --- | --- | --- | --- |
| `US-E7-POL-01` | 查询发现并入篮 | F-POL-00 | 完整覆盖 |
| `US-E7-POL-05` | 政策 Tab 暂存与分发 | F-POL-CMP | 完整覆盖 |
| `US-E7-POL-02` | 时序分析闭环 | F-POL-01 + TASK + REPORT | 完整覆盖 |
| `US-E7-POL-03` | 区域对比闭环 | F-POL-02 + TASK + REPORT | 完整覆盖 |
| `US-E7-POL-04` | 三维评估闭环 | F-POL-03 + TASK + REPORT | 完整覆盖 |
| `US-E7-POL-06` | 任务恢复与 queued 撤回 | F-POL-TASK | 完整覆盖 |
| `US-E7-POL-07` | 报告 HTML→PDF | F-POL-REPORT | 完整覆盖 |
| `US-E7-POL-08` | 门户六页入篮 | F-POL-PORTAL | 完整覆盖（线框细则见 TRACE 门户合同） |
| `US-E7-POL-09` | 维护管理复用 ENT-OPS | F-POL-OPS | 完整覆盖（菜单 15 项对齐见 GAP-E7-08） |

### 2.2 宿主、状态与禁止行为

| 核对维度 | 同步结论 |
| --- | --- |
| 查询宿主 | `/policy/search` · `ElementSearchWorkbench`；storage `gkx-policy-search-recents:v1` |
| 对比篮 | `app-shell#system-compare-basket?active_type=policy`；容量 50；`policy_id` 去重 |
| 分析路由 | `/policy/overview` · `/policy/analysis` · `/policy/recommendation` |
| 任务 | `app-shell#system-task-layer`；与对比篮互斥展开 |
| 报告 | 统一模板 → HTML 预览 → 同源 PDF |
| 门户 | `/policy-portal/{overview,map,industry-coverage,intensity-rank,latest,shenzhen}` |
| 维护 | `/policy/maintenance`；三组菜单 |
| 状态机 | `object_empty → draft → … → succeeded → 显式查看结果 → report_handoff` |
| 禁止 | 深度分析直达；页内聚合篮按钮；虚构百分比；查询/篮内正式报告 |

### 2.3 差异与缺口

四件套 v1.4.3 相互一致。开放问题 `QPOL-01/02/03/05` 与 GAP-E7-01~08 均已 stage 分类；无 `blocks_v1: true`。实现侧须把政策 Tab 从占位切为可操作态（GAP-E7-05），属 Demo/共享篮对齐，不在本规格重拍产品决策。

## 3. 用户旅程与任务流

### 3.1 J-E7-PREP｜发现入篮（政府 / 园区 / 投资 / 研究）

**Story**：`US-E7-POL-01`、`US-E7-POL-08`

主路径：

1. 进入 `/policy/search`（默认 `mode=smart`）或门户六页之一。
2. 查询侧：模式栏 → SearchHub → 示例/热门 → 最近检索 → 推荐/结果；门户侧浏览展示卡。
3. 点击「加入对比篮」→ 按钮「已加入」；系统 Shell 角标同步；**停留原页**。
4. 不出现「深度分析」与页内聚合对比篮按钮。

异常与恢复：零命中空态；满 50 阻断；权限锁态；Drawer 未关闭时不叠加展开对比篮。

### 3.2 J-E7-DISPATCH｜对比篮唯一发起

**Story**：`US-E7-POL-05`

主路径：

1. 打开系统对比篮 → 政策 Tab（`X/50`，非「开发中」）。
2. 筛选/勾选 →「发起分析」→ 三选一任务 →「下一步：前往配置」。
3. 目标页接管 `policy_ids` + `return_context_id`；面板收起、入口保留；显示「来自对比篮」。
4. 「调整对象」仅触发系统浮层原位展开。

异常：跨 Tab 混选禁止；取消/失败保持面板；空选不分发。

### 3.3 J-E7-ANALYSIS｜三项分析 + 任务 + 报告

**Story**：`US-E7-POL-02/03/04/06/07`

主路径：

1. 有分发上下文进入对应分析页 → 配置 →「生成分析」。
2. ProcessingView：StageSteps（政策阶段文案）→ succeeded → 显式「查看结果」。
3. 有效结果「生成报告」→ report 任务 → **先** HTML 预览 → 再同源 PDF。
4. 离页后从系统任务浮层恢复；`queued` 可撤回；`running` 无取消。

异常：

| 条件 | 行为 |
| --- | --- |
| 无分发上下文 + 政策篮空 | 仅 CTA「去政策查询入篮」 |
| 无分发上下文 + 篮有对象 | CTA「去查询入篮」或「打开对比篮」 |
| 权重≠100%（三维） | 不创建任务 |
| 同类型已有进行中 | 引导恢复，不新建 |
| 过期结果 / 无报告权限 | 失败关闭；结果仍可读 |
| 报告框架未激活 | 失败关闭并说明（GAP-E7-06） |

### 3.4 J-E7-OPS｜维护管理

**Story**：`US-E7-POL-09`

主路径：进入 `/policy/maintenance` → 三组菜单切换 → 门户内容样例可维护 → 审核/发布工作流（复用 ENT-OPS）。  
异常：无权限锁态；前台页不可编辑；不在维护页跑分析任务。

## 4. Frame 与承载映射

### 4.1 F-POL-00 政策查询

| 项 | 合同 |
| --- | --- |
| 路由 | `/policy/search?mode=smart\|policy\|advanced` |
| 入口/出口 | 菜单进入；入篮后停留；高筛独立页返回保留焦点 |
| 上下文保持 | 模式、条件、结果滚动；最近检索按模式隔离 |
| 关键控件 | SearchHub、SmartChip、RecentSearchPanel、结果卡入篮、摘要 Drawer |
| 禁止 | 深度分析；页内聚合篮；Hero 内嵌高筛；与门户共用 storage |

### 4.2 F-POL-CMP 系统对比篮·政策 Tab

| 项 | 合同 |
| --- | --- |
| 宿主 | `app-shell#system-compare-basket`；壳层继承 ENT-COMPARE |
| 容量/键 | 50；`policy_id`；信封字段见 IA §3.1 |
| 分发 | 时序 / 区域 / 深圳三维 → 三路由 |
| 空态能力（目标页消费） | count=0 仅查询；count≥1 查询或开篮 |
| 禁止 | 篮内图/报告；跨 Tab 混选；页内第二套篮 |

### 4.3 F-POL-PORTAL 门户政策扶持

| 项 | 合同 |
| --- | --- |
| 路由 | 六页见 TRACE `portal_display.pages` |
| 动作 | 加入/移出/已加入；停留原页 |
| 禁止 | 分析任务、报告、私有篮、聚合开篮按钮 |

### 4.4 F-POL-01 / 02 / 03 三项分析

| Frame | 路由 | analysis_type | 配置要点 | 结果要点 |
| --- | --- | --- | --- | --- |
| F-POL-01 | `/policy/overview` | `policy_timeseries_analysis` | 粒度 year/quarter/month | 时序/强度/关键节点明细 |
| F-POL-02 | `/policy/analysis` | `policy_region_compare` | 区域多选；矩阵\|雷达\|热力 | 差异结论与条款明细 |
| F-POL-03 | `/policy/recommendation` | `policy_sz_3d_assessment` | 三维权重=100% | 仪表盘/短板/策略卡 |

共性：ContextBar + Config/Processing/Result；「调整对象」只开系统篮；无页内导出。

### 4.5 F-POL-TASK

页内 ProcessingView + 系统任务浮层恢复；生命周期与撤回规则见 Wireframe §6b；阶段文案按政策类型注册。

### 4.6 F-POL-REPORT

仅有效结果入口；统一模板；先 HTML 后 PDF；同 `report_revision` / fingerprint；V1 仅 HTML+PDF。

### 4.7 F-POL-OPS

`/policy/maintenance`；组：内容运营 / 图谱运营 / 分析配置；政策注入门户内容与主体等 tab；企业字段禁止硬套；报告模板 tab 仅维护元数据。

## 5. 交互与状态转换

| 触发 | 前置 | 结果状态 | 可逆 | 禁止 |
| --- | --- | --- | --- | --- |
| 加入对比篮 | 未满 50、有 policy_id | 已加入 + 角标+1 | 可移出 | 跳篮页 |
| 发起分析 | 政策 Tab 已选≥1 | 分发 Modal | 取消回列表 | 混选 |
| 下一步前往配置 | 任务已选 | 目标 draft + 收起面板 | 调整对象重开 | 清空篮当返回 |
| 生成分析 | 配置合法 | created→…→running | queued 可撤回 | 假百分比 |
| 查看结果 | succeeded | result_available | 否（结果只读） | 自动跳转 |
| 生成报告 | 有效结果 | report 任务→HTML | 同 fingerprint 复用 | 跳过 HTML |
| 下载 PDF | HTML 同源修订 | PDF 下载 | PDF 缺失可重生成 | HTML/PDF 不同修订 |
| 三维改权重 | 配置态 | 校验合计 | 可均分 | 非法仍提交 |
| 菜单进分析无上下文 | — | object_empty | — | 伪造分发上下文 |

## 6. 反馈与异常恢复

| 场景 | 反馈 | 恢复 |
| --- | --- | --- |
| loading | 骨架 / StageSteps | 等待 |
| empty 查询零命中 | 模式空态 | 调整条件 |
| object_empty（篮空） | 仅去查询入篮 | 入篮后再分发 |
| object_empty（篮有对象） | 查询或打开对比篮 | 开篮发起 |
| error | 错误条 + 重试 | 配置保留 |
| permission | 锁态；隐藏敏感摘要 | 申请权限 |
| expired 结果 | 不可新开正式报告 | 复制配置重跑 |
| full basket | 第 51 份阻断 | 移除后加入 |
| concurrent same type | 引导恢复原任务 | 任务浮层进入 |

## 7. 组件、键盘与无障碍

| 区域 | 组件选型 | 键盘 / 焦点 / ARIA |
| --- | --- | --- |
| 查询模式 | Arco Tabs / Radio.Group | 方向键切换；`aria-selected` |
| 搜索 | Arco Input.Search + SmartChip Tag | Chip 可聚焦删除；Esc 不误清最近检索 |
| 结果入篮 | Button 状态切换 | 禁用时说明满额原因 |
| 对比篮 | 继承 ENT-COMPARE：Tabs、Checkbox、Modal | 拖动区不含业务控件 |
| 分析配置 | Select / InputNumber / Checkbox | 错误用文本，不只靠颜色 |
| 图表 | ECharts | 提供等价表或可读摘要 |
| 任务 Steps | Steps + Alert | 焦点落在当前阶段说明 |
| 报告预览 | 共享阅读器 | 目录可键盘跳转章节 |
| 维护 | ENT-OPS 菜单 + Table/Form | 锁态可读原因 |

对比度遵循 Design.md；禁用与 loading 不得吞焦点。

## 8. 响应式行为

`screen_tier=medium_1440_1920`；验收宽：1920 / 1680 / 1440。

| 宽度 | 行为 |
| --- | --- |
| 1920 | 查询结果与分析双栏完整；图表并列 |
| 1680 | 分析侧栏可收；矩阵横向滚动优先于挤压标签 |
| 1440 | 图表可上下堆叠；ContextBar 动作折行但不丢「调整对象」「生成分析」 |

无 small / 大屏轨。固定：系统篮/任务入口位置继承 Shell；分析页 Config 主操作常显。

## 9. 内部评审投影

业务模式一律 `absent`。评审模式由全局开关控制。

| mount_id | frame_id | marker_type |
| --- | --- | --- |
| E7-POL-F00-PAGE-TITLE-TRACE | F-POL-00 | requirement_trace |
| E7-POL-F00-MOCK | F-POL-00 | mock_badge |
| E7-POL-FCMP-POLICY-TAB-TRACE | F-POL-CMP | requirement_trace |
| E7-POL-F01-PAGE-TITLE-TRACE | F-POL-01 | requirement_trace |
| E7-POL-F01-COUNT-METRIC | F-POL-01 | metric_spec |
| E7-POL-F01-INTENSITY-METRIC | F-POL-01 | metric_spec |
| E7-POL-F01-MOCK | F-POL-01 | mock_badge |
| E7-POL-F02-PAGE-TITLE-TRACE | F-POL-02 | requirement_trace |
| E7-POL-F02-MATRIX-METRIC | F-POL-02 | metric_spec |
| E7-POL-F02-MOCK | F-POL-02 | mock_badge |
| E7-POL-F02-PENDING-QPOL | F-POL-02 | pending_badge |
| E7-POL-F03-PAGE-TITLE-TRACE | F-POL-03 | requirement_trace |
| E7-POL-F03-DIM-METRIC | F-POL-03 | metric_spec |
| E7-POL-F03-SHORTBOARD-METRIC | F-POL-03 | metric_spec |
| E7-POL-F03-MOCK | F-POL-03 | mock_badge |
| E7-POL-F03-PENDING-WEIGHT | F-POL-03 | pending_badge |

入口标记顺序（有矩阵后）：`数字 → [ⓘ] → [DataHealthBadge] → [🧪/⟳]`；`max_markers: 3`；`spacing_px: 4`。当前无矩阵行时不投影伪 D1–D4。

禁止：图表区叠标签；PDF 正文强制评审挂载；Pending 做成阻断模态。

## 10. Demo 实施交接

1. 挂载 `ElementSearchWorkbench`；政策标签/schema/卡片/入篮动作注入；禁深度分析。
2. ENT-COMPARE：政策 Tab 可操作 + 角标计入 + 三分发任务 + 空态按 count 分支。
3. 三项分析页：分发上下文门禁；注册 `analysis_type` / 政策 StageSteps；显式看结果。
4. 报告：`report_template_id` + 章节 payload；先 HTML 后 PDF。
5. 门户六页入篮；维护页 ENT-OPS 菜单形态（门户内容样例优先）。
6. 排除：展示系统页；私有任务/下载中心；页内导出替代系统报告。

**V1 Demo 激活条件**：本规格 `ready_for_v1` 且共享篮政策 Tab 可操作（实现对齐 GAP-E7-05）。激活后用 `gkx-definition-to-demo` + `gkx-ui-design-standards`。

## 11. 缺口与阻断项

| Gap | blocks_v1 | blocks_stages | V1 处理 | owner | deadline | return_to |
| --- | --- | --- | --- | --- | --- | --- |
| GAP-E7-01 密度指数代理 | false | pdr, v1_final, production | 可见代理口径 + 评审标注 | human:何老师 | before_pdr | TRACE |
| GAP-E7-02 三维/权重待确认 | false | pdr, v1_final, production | 临时默认 + ⚠️ | human:高颖 | before_pdr | 客户决策清单跟踪表.md |
| GAP-E7-03 无 POLICY 矩阵 | false | pdr, v1_final | 挂载声明不自填 D1–D4 | human:何老师 | before_v1_final | metrics |
| GAP-E7-04 落地实效无 ODS | false | v2_lumen, production | Mock + Pending | human:辜少彬 | before_production | architecture |
| GAP-E7-05 政策 Tab 实现占位 | false | pdr, v1_final | Demo 必须切可操作态 | human:高颖 | before_v1_hifi | ENT-COMPARE |
| GAP-E7-06 报告框架未激活 | false | v1_final, production | 入口可验；正式 PDF 失败关闭 | human:高颖 | before_v1_final | shared_report |
| GAP-E7-07 门户入篮挂载 | false | pdr, v1_final | Demo 补挂载入篮控件 | human:高颖 | before_v1_hifi | portal_display |
| GAP-E7-08 OPS 15 项落地 | false | pdr, v1_final | 组/项不可删；非样例可占位 | human:高颖 | before_v1_hifi | maintenance_ops |

无 `blocks_v1: true` 项。

## 12. 机器可读交付契约

```yaml
ux_spec_contract:
  module_key: E7-政策分析
  version: "1.0"
  status: ready_for_v1
  source_four_pack:
    - IA-E7-政策分析.md
    - TRACE-E7-政策分析.yaml
    - USM-E7-政策分析.md
    - Wireframe-E7-政策分析.md
  screen_tier: medium_1440_1920
  delivery_stage: v1_hifi_round1
  product_scope_mutation: prohibited
  demo_code_mutation: prohibited
  journeys:
    - journey_id: J-E7-PREP
      role: 政府科技主管部门/产业园区/投资机构/研究团队
      story_refs: [US-E7-POL-01, US-E7-POL-08]
      primary_flow:
        - 进入政策查询或门户展示
        - 加入系统对比篮政策 Tab
        - 停留原页且角标同步
      abnormal_flows:
        - 零命中空态调整条件
        - 满50阻断后移除再加入
    - journey_id: J-E7-DISPATCH
      role: 业务用户
      story_refs: [US-E7-POL-05]
      primary_flow:
        - 打开系统对比篮政策 Tab
        - 勾选对象并发起分析任务
        - 分发至目标分析页并收起面板
      abnormal_flows:
        - 跨Tab混选被禁止
        - 取消分发保持面板展开
    - journey_id: J-E7-ANALYSIS
      role: 政府科技主管部门/研究团队
      story_refs: [US-E7-POL-02, US-E7-POL-03, US-E7-POL-04, US-E7-POL-06, US-E7-POL-07]
      primary_flow:
        - 配置并提交analysis任务
        - 显式查看不可变结果
        - 生成报告先HTML后同源PDF
      abnormal_flows:
        - 无分发上下文按篮count分支空态
        - queued撤回与running无取消
        - 权重非法或过期结果失败关闭
    - journey_id: J-E7-OPS
      role: 内容运营/数据治理
      story_refs: [US-E7-POL-09]
      primary_flow:
        - 进入政策维护管理
        - 在ENT-OPS三组菜单中维护门户内容样例
      abnormal_flows:
        - 无权限锁态
        - 前台页禁止编辑发布
  frame_specs:
    - frame_id: F-POL-00
      route_or_host: /policy/search
      source_refs: [US-E7-POL-01]
      states: [default, loading, empty, error, permission]
      interactions: [mode_switch, smart_chip_remove, advanced_filter, add_to_basket]
    - frame_id: F-POL-CMP
      route_or_host: app-shell#system-compare-basket?active_type=policy
      source_refs: [US-E7-POL-05]
      states: [default, loading, empty, error, permission]
      interactions: [filter_select, launch_analysis, dispatch_next, restore_panel]
    - frame_id: F-POL-PORTAL
      route_or_host: /policy-portal/*
      source_refs: [US-E7-POL-08]
      states: [default, loading, empty, error, permission]
      interactions: [browse_display, add_to_basket, remove_from_basket]
    - frame_id: F-POL-01
      route_or_host: /policy/overview
      source_refs: [US-E7-POL-02]
      states: [object_empty, draft, loading, empty, error, permission, result_readonly]
      interactions: [configure_granularity, submit_analysis, view_result, open_compare_basket]
    - frame_id: F-POL-02
      route_or_host: /policy/analysis
      source_refs: [US-E7-POL-03]
      states: [object_empty, draft, loading, empty, error, permission, result_readonly]
      interactions: [configure_regions, switch_view, submit_analysis, view_result]
    - frame_id: F-POL-03
      route_or_host: /policy/recommendation
      source_refs: [US-E7-POL-04]
      states: [object_empty, draft, loading, empty, error, permission, result_readonly]
      interactions: [configure_weights, submit_analysis, view_result, drill_shortboard]
    - frame_id: F-POL-TASK
      route_or_host: app-shell#system-task-layer
      source_refs: [US-E7-POL-06]
      states: [queued, running, succeeded, failed, withdrawn]
      interactions: [resume_task, withdraw_queued, view_result_explicit]
    - frame_id: F-POL-REPORT
      route_or_host: shared-report-reader
      source_refs: [US-E7-POL-07]
      states: [default, loading, error, permission, expired]
      interactions: [generate_report, preview_html, download_pdf]
    - frame_id: F-POL-OPS
      route_or_host: /policy/maintenance
      source_refs: [US-E7-POL-09]
      states: [default, loading, empty, error, permission]
      interactions: [switch_ops_group, edit_portal_content, lock_unauthorized]
  feedback_rules:
    - object_empty_by_basket_count
    - full_basket_block
    - concurrent_analysis_resume
    - report_html_before_pdf
    - permission_fail_closed
  responsive_widths: [1920, 1680, 1440]
  accessibility_checks: [keyboard, focus, aria, contrast]
  metric_readiness_projection: []
  review_mounts:
    - E7-POL-F00-PAGE-TITLE-TRACE
    - E7-POL-F00-MOCK
    - E7-POL-FCMP-POLICY-TAB-TRACE
    - E7-POL-F01-PAGE-TITLE-TRACE
    - E7-POL-F01-COUNT-METRIC
    - E7-POL-F01-INTENSITY-METRIC
    - E7-POL-F01-MOCK
    - E7-POL-F02-PAGE-TITLE-TRACE
    - E7-POL-F02-MATRIX-METRIC
    - E7-POL-F02-MOCK
    - E7-POL-F02-PENDING-QPOL
    - E7-POL-F03-PAGE-TITLE-TRACE
    - E7-POL-F03-DIM-METRIC
    - E7-POL-F03-SHORTBOARD-METRIC
    - E7-POL-F03-MOCK
    - E7-POL-F03-PENDING-WEIGHT
  gaps:
    - id: GAP-E7-01
      summary: 政策密度指数以 M_POLICY_TOTAL_COUNT 代理并在评审标注
      blocks_v1: false
      blocks_stages: [pdr, v1_final, production]
      v1_disposition: gap_visible
      v1_treatment: deterministic_demo_contract
      owner: human:何老师
      deadline: before_pdr
      return_to: TRACE-E7-政策分析.yaml
    - id: GAP-E7-02
      summary: 三维框架与力度权重待甲方确认，演示用临时默认并标警告角标
      blocks_v1: false
      blocks_stages: [pdr, v1_final, production]
      v1_disposition: gap_visible
      v1_treatment: deterministic_demo_contract
      owner: human:高颖
      deadline: before_pdr
      return_to: 客户决策清单跟踪表.md
    - id: GAP-E7-03
      summary: 尚无 metric-readiness-matrix-POLICY.yaml，不自填 D1-D4
      blocks_v1: false
      blocks_stages: [pdr, v1_final]
      v1_disposition: gap_visible
      v1_treatment: deterministic_demo_contract
      owner: human:何老师
      deadline: before_v1_final
      return_to: metrics
    - id: GAP-E7-04
      summary: 落地实效性监测无 ODS，Wave0 Mock
      blocks_v1: false
      blocks_stages: [v2_lumen, production]
      v1_disposition: gap_visible
      v1_treatment: deterministic_demo_contract
      owner: human:辜少彬
      deadline: before_production
      return_to: architecture
    - id: GAP-E7-05
      summary: 实现须将政策 Tab 从占位切换为可操作态并计入角标
      blocks_v1: false
      blocks_stages: [pdr, v1_final]
      v1_disposition: gap_visible
      v1_treatment: deterministic_demo_contract
      owner: human:高颖
      deadline: before_v1_hifi
      return_to: ENT-COMPARE
    - id: GAP-E7-06
      summary: 共享报告框架未激活时正式 PDF 失败关闭并保留结果阅读
      blocks_v1: false
      blocks_stages: [v1_final, production]
      v1_disposition: gap_visible
      v1_treatment: deterministic_demo_contract
      owner: human:高颖
      deadline: before_v1_final
      return_to: shared_report
    - id: GAP-E7-07
      summary: 门户六页入篮控件需与政策 Tab 可操作态同步挂载
      blocks_v1: false
      blocks_stages: [pdr, v1_final]
      v1_disposition: gap_visible
      v1_treatment: deterministic_demo_contract
      owner: human:高颖
      deadline: before_v1_hifi
      return_to: portal_display
    - id: GAP-E7-08
      summary: 维护管理按 ENT-OPS 十五项对齐，非样例可占位但不可删组删项
      blocks_v1: false
      blocks_stages: [pdr, v1_final]
      v1_disposition: gap_visible
      v1_treatment: deterministic_demo_contract
      owner: human:高颖
      deadline: before_v1_hifi
      return_to: maintenance_ops
```

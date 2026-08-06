# Wireframe-CHAIN-TOPIC-REGIONAL｜区域产业评价

> **版本**：v1.7-comp-result-viz  
> **状态**：核心产品包 Wireframe；`ready_for_v1: true`  
> **体验 Owner**：高颖  
> **screen_tier**：`medium_1440_1920`  
> **边界**：本文件为区域产业评价唯一结构基线；父包 `F-CHAIN-07/08` 仅溯源。  
> **修订（2026-08-06）**：指数配置对齐企业评估——官方模板、不铺全库、添加指标下拉、保存个人模板（`DEC-CHAIN-REG-INDEX-TEMPLATE-UX-20260806`）。  
> **修订（2026-08-06）**：竞争力结果可视化——柱状+矩阵热力+条件 GIS（`DEC-CHAIN-REG-COMP-RESULT-VIZ-20260806`）。

## 1. Frame 清单

| Frame | 路由 / 宿主 | 目标 | 故事 |
| --- | --- | --- | --- |
| `F-REG-01` | `/industry-center/regional` | 工作区壳、对象上下文、Tab | 全部 |
| `F-REG-02` | `?tab=index` | 指数配置 / 结果 | `US-CHAIN-REG-01/02` |
| `F-REG-03` | `?tab=competitiveness` | 竞争力配置 / 结果 | `US-CHAIN-REG-03/04` |
| `F-REG-04` | `?tab=records` | 分析记录 | `US-CHAIN-REG-05` |

## 2. 统一骨架与状态机

- 壳层：页标题「区域产业评价」+ 对象上下文条 + 一级 Tab（指数 / 竞争力 / 分析记录）。
- 工作态：`no_object` → `config` → `task_created` / `processing`（共享壳）→ `result`；记录态独立。
- 两业务 Tab 共享兼容产业对象；区域、指标、权重、即时汇总、结果焦点隔离。
- 点击「生成分析」才创建任务；结果须显式「查看分析结果」；禁止自动跳转。

## 3. F-REG-01 工作区壳与对象上下文

```text
┌─ 区域产业评价 ───────────────────────────────────────────────────┐
│ 分析对象：{产业摘要} | [打开对比篮]                                 │
│ Tabs: 区域产业指数评价 | 区域产业竞争力评价 | 分析记录              │
└────────────────────────────────────────────────────────────────────┘
```

| 字段 | 规则 |
| --- | --- |
| 产业对象摘要 | 来自共享篮兼容产业；无效时空态文案引导打开对比篮 |
| Tab | `index` / `competitiveness` / `records`；写入 URL |

状态：`no_object` / `object_ready` / `permission_locked` / `unavailable`。  
禁止：页内私有产业 Select；区域入篮；模块自建浮层篮。

评审挂点：`CHAIN-REG-F01-OBJECT-CONTEXT`（requirement_trace；BusinessMode absent）。

## 4. F-REG-02 区域产业指数配置与结果

```text
┌─ 区域产业评价 / 指数评价 ─────────────────────────────────────────┐
│ 分析对象 | 评价模式 | 区域选择（三字段同行）                          │
│ ② 评估模板  [系统模板 / 我的模板 / 当次配置 ▾]  默认：官方综合指数 V1 │
│    Alert：当前使用官方模板，用户调整仅对本次任务生效（未保存个人模板时）│
│ ③ 指标与权重（仅当前已选；分组=四力 ⚠️QC11）                         │
│    [添加指标 ▾]  [一键均分]  合计=100%                               │
│    表：选择 | 名称 | 分组 | 数据状态 | 权重 | 来源 | 说明             │
│ 配置即时汇总（综合指数随权重刷新 · 非正式结果）                         │
│ [保存为个人模板]                              [生成分析]               │
├─ 结果 ─────────────────────────────────────────────────────────────┤
│ KPI：综合第1·{主体} | 优势维 | 短板维 | 与第2名分差（写清主体）     │
│ 四力排名对比：排名 | 区域/产业 | 综合 | 四力汇总（降序）             │
│ 指标贡献：四力分组 | 叶子指标 | 权重 | 各主体得分（已计入，非全库） │
│ 优势短板（文案含主体，可落到 四力·叶子）| [查看配置] [生成报告]       │
└────────────────────────────────────────────────────────────────────┘
```

| 字段 / 区块 | 规则 | metric / gap |
| --- | --- | --- |
| `industry_ids` / `region_codes` | 评价对象可配；仅 1×1、1×2~5、2~5×1 | — |
| 评估模板 | 分组：系统模板（官方，≥1）/ 我的模板 / 当次自定义；切换恢复指标+权重，不恢复对象 | 对齐 ENT-EVAL；`decision_ref: DEC-CHAIN-REG-INDEX-TEMPLATE-UX-20260806` |
| 已选指标与权重 | **只渲染当前模板/当次已选行**；禁止默认铺全库；分组=四力；合计 100% | `metric_gap_ref: GAP-CHAIN-REG-METRICS`；`QC11` |
| 添加指标 | 按钮→下拉/选择器列出未入本次配置的库内指标（可按四力筛）；选中后追加行 | Bid `.3.1`；不可用项禁加或禁提交 |
| 保存为个人模板 | 存名称+指标+权重；不存对象/任务名；写入「我的模板」 | 同 ENT-EVAL 个人模板语义 |
| 四力归属（临时） | 商业力/技术力/学术力/支撑力映射见 DEC 四力；**结果层组名不可替代叶子** | 后台可映射国标 |
| 即时汇总 | **配置即时汇总**=Bid「所见即所得」（底分×已计入权重）；不建任务 | `CHAIN-REG-F02-INLINE-WYSIWYG` |
| 正式结果分层 | KPI 主体化 → 四力排名表 → 已计入叶子贡献 → 优势短板；绑定任务快照 | `decision_ref: DEC-CHAIN-REG-INDEX-RESULT-RANK-LEAF-20260806`；`GAP-CHAIN-REG-METRICS` |

禁止：默认一次勾选全库；静默归一化；独立轻量预览按钮；即时汇总冒充正式结果；区域入篮；运营改官方模板/建库/无源造指标；把个人模板名当任务名；竞争力 Tab 误用本模板能力。

评审挂点：
- `CHAIN-REG-F02-INDEX-TITLE`（requirement_trace）
- `CHAIN-REG-F02-INDEX-TEMPLATE`（requirement_trace · 官方/个人模板）
- `CHAIN-REG-F02-INDEX-METRICS`（missing_metric_entry）
- `CHAIN-REG-F02-INDEX-DIM-FOUR-FORCE`（pending_decision · QC11）
- `CHAIN-REG-F02-CUSTOM-METRIC-ADD`（requirement_trace · Bid `.3.1`）
- `CHAIN-REG-F02-PERSONAL-TEMPLATE`（requirement_trace）
- `CHAIN-REG-F02-INLINE-WYSIWYG`（requirement_trace · Bid「所见即所得」内联汇总；`DEC-CHAIN-REG-INDEX-WYSIWYG-INLINE-20260806`）

## 5. F-REG-03 区域竞争力配置与结果

```text
┌─ 区域产业评价 / 竞争力 ───────────────────────────────────────────┐
│ 分析对象 | 评价模式 | 区域选择（同指数合同，三字段同行）              │
│ 三大一级维度权重表（对齐诊断）| 合计=100% | [一键均分] [生成分析]   │
├─ 结果 ─────────────────────────────────────────────────────────────┤
│ KPI（写清主体）                                                     │
│ [柱状：综合指数排名] [矩阵热力：主体×三维+综合]  ← 宽屏并排         │
│ GIS 区域热力（仅 multi-region 且区域≥2；Demo-B）                    │
│ 排名明细表（与图同源可联动）| 优势短板 | 版本边界 | [生成报告]     │
└────────────────────────────────────────────────────────────────────┘
```

| 字段 / 区块 | 规则 | metric / gap |
| --- | --- | --- |
| 柱状 / 矩阵热力 | Bid `.8.2` 必达；ECharts；与表同源；点击联动高亮主体 | `decision_ref: DEC-CHAIN-REG-COMP-RESULT-VIZ-20260806` |
| GIS 热力 | 条件块；multi-industry 隐藏；Demo-A 可未上、Demo-B 补 | 同上；`CHAIN-REG-F03-COMP-HEATMAP-GIS` |
| 生成报告 | 共享报告交接，非页内 PDF 引擎 | `CHAIN-REG-F03-COMP-REPORT` |
| 对象组合 | 同 F-REG-02；配置首行同行 | — |
| 三大一级维度和权重 | 维度固定；诊断同款表格只调一级权重 | `metric_gap_ref: GAP-CHAIN-REG-METRICS` |
| 综合指数 / 排名 / 热力图 | 同模型与权重版本才可比较 | `metric_gap_ref: GAP-CHAIN-REG-METRICS` |

禁止：新增/删除一级维度；降成两维；人工覆盖排名；跨版本混排。

评审挂点：
- `CHAIN-REG-F03-COMPETITIVENESS-TITLE`（requirement_trace）
- `CHAIN-REG-F03-COMPETITIVENESS-METRICS`（missing_metric_entry）
- `CHAIN-REG-F03-VERSION-BOUNDARY`（requirement_trace）

## 6. F-REG-04 分析记录

```text
┌─ 分析记录 ────────────────────────────────────────────────────────┐
│ 过滤：类型(指数|竞争力) / 状态                                      │
│ 列表：任务摘要 | 完成时间 | 报告(N 份)                              │
│       → [查看结果] [复制配置] [关联报告]                            │
└────────────────────────────────────────────────────────────────────┘
```

| 列/动作 | 说明 |
| --- | --- |
| 报告 | 按结果快照 `snapshot:{result_id}` 统计系统报告任务；对齐诊断记录 / 企业评估历史表 |
| 查看结果 | 打开不可变结果；过程仍可从任务壳进入 |
| 复制配置 | 回到配置草稿；不复制任务中心内部阶段实现 |
| 关联报告 | 有报告时可打开；0 份时禁用；**列表不挂「查看任务进度」**（与 `F-DIAG-05` 一致） |

禁止：复制共享任务中心内部阶段实现；跨模块历史混排而不标注类型。

评审挂点：`CHAIN-REG-F04-RECORDS`（requirement_trace；挂在 Tab，列表区不重复标题）。

## 7. 响应式

- 1920 / 1680：配置区单列主宽；结果图表并排。  
- 1440：结果区图表上下堆叠；权重控件保持可编辑。  
- 不声明专题小屏 `small_reflow`。

## 8. 状态覆盖（每业务 Frame）

`empty_object` / `loading` / `config_invalid` / `permission_locked` / `previewing` / `submitting` / `processing` / `succeeded_wait_view` / `result` / `incomparable` / `partial_metric_gap` / `error_retry`。

## 9. 模块排除

全景图谱、诊断三项、深圳两项、门户总览、技术链、区域入篮、指标库后台维护、模型训练、页内 PDF 引擎。

## 10. review_trace_contract

| mount_id | frame_id | marker_type | BusinessMode |
| --- | --- | --- | --- |
| CHAIN-REG-F01-OBJECT-CONTEXT | F-REG-01 | requirement_trace | absent |
| CHAIN-REG-F02-INDEX-TITLE | F-REG-02 | requirement_trace | absent |
| CHAIN-REG-F02-INDEX-TEMPLATE | F-REG-02 | requirement_trace | absent |
| CHAIN-REG-F02-INDEX-METRICS | F-REG-02 | missing_metric_entry | absent |
| CHAIN-REG-F02-CUSTOM-METRIC-ADD | F-REG-02 | requirement_trace | absent |
| CHAIN-REG-F02-PERSONAL-TEMPLATE | F-REG-02 | requirement_trace | absent |
| CHAIN-REG-F02-INDEX-DIM-FOUR-FORCE | F-REG-02 | pending_decision | absent |
| CHAIN-REG-F02-INLINE-WYSIWYG | F-REG-02 | requirement_trace（Bid 所见即所得） | absent |
| CHAIN-REG-F03-COMPETITIVENESS-TITLE | F-REG-03 | requirement_trace | absent |
| CHAIN-REG-F03-COMPETITIVENESS-METRICS | F-REG-03 | missing_metric_entry | absent |
| CHAIN-REG-F03-COMP-BAR | F-REG-03 | requirement_trace | absent |
| CHAIN-REG-F03-COMP-HEATMAP-MATRIX | F-REG-03 | requirement_trace | absent |
| CHAIN-REG-F03-COMP-HEATMAP-GIS | F-REG-03 | mock_badge | absent |
| CHAIN-REG-F03-COMP-REPORT | F-REG-03 | requirement_trace | absent |
| CHAIN-REG-F03-VERSION-BOUNDARY | F-REG-03 | requirement_trace | absent |
| CHAIN-REG-F04-RECORDS | F-REG-04 | requirement_trace | absent |

共 **16** 个唯一宿主。

## 11. 自检

1. 每 Frame 有路由、故事、字段、状态、禁止行为。  
2. 统计值均有 `metric_gap_ref` 或后续正式 metric_id，无伪口径。  
3. 官方模板默认加载；表内仅已选指标；「添加指标」下拉 +「保存为个人模板」可走通。  
4. BusinessMode 全 absent。  
5. 排除项明确。  

# UX-SPEC-CHAIN-TOPIC-SHENZHEN｜深圳产业决策

> **文档版本**：v1.0-package-split  
> **四件套版本**：v1.0-package-split  
> **日期**：2026-08-05  
> **状态**：ready_for_v1  
> **体验 Owner**：human:高颖  
> **独立执行权威**：深圳产业决策交互只读本文件；父包 F-09/F-10 段落仅溯源。

## 1. 权威输入

IA / TRACE / USM / Wireframe（本目录）· D10 通用交互 · D8 Design · SYS-ANALYSIS-JOBS 任务壳。

## 2. 四件套同步核对

| 维度 | 数量 |
| --- | --- |
| 故事 | 5（US-CHAIN-SZ-01…05） |
| Frame | 4（F-SZ-01…04） |
| Bid 叶子 | 2（`.2.2.6` / `.2.2.7`） |
| review mounts | **9** |

结论：对比→发展结构化输入链闭合；PDF 输入禁止；案例库为显式 Gap。

## 3. 用户旅程

### SZ-J01｜对比闭环

`US-CHAIN-SZ-01/02/05`：确认产业 → `tab=comparison` 选标杆 → 生成分析 → 显式看结果 → 可选记录恢复。

### SZ-J02｜发展闭环

`US-CHAIN-SZ-03/04/05`：显式选对比结果 → 确认目标 → 生成分析 → 显式看建议与路径。  
禁止：无来源自动跑；从对比结果页自动跳进发展并静默带入（允许「带入来源」显式动作）。

## 4. Frame 交互

### F-SZ-01

Tab 写 URL；共享产业对象；主体文案固定「深圳」不可编辑。

### F-SZ-02

| 触发 | 结果 | 禁止 |
| --- | --- | --- |
| 选标杆 | 更新就绪矩阵 | 自动填默认城市 |
| 生成分析 | 校验≥1 有效标杆后建任务 | 无标杆仍提交 |
| 查看结果 | 不可变结构化结论 | 用新数据改写旧快照 |

### F-SZ-03

| 触发 | 结果 | 禁止 |
| --- | --- | --- |
| 选来源结果 | 校验同产业/有效/结构兼容 | PDF、跨产业、过期、无权 |
| 生成分析 | 绑定 `source_result_id` | 静默继承最近对比 |
| 查看结果 | 三类建议+≥2 路径 | 项目执行工具 UI |

### F-SZ-04

过滤恢复；`queued` 可撤回，`running` 不提供用户取消。

## 5. 反馈

`permission_locked` 与 `unavailable` 分离；`source_invalid` 说明拒绝原因；`incomplete_paths` 明示缺口；`stale_benchmark_note` 仅标注局限不改结论。

## 6. 键盘与无障碍

Tabs/表单可键盘操作；禁用控件可读原因；图表提供可读摘要或数据表。

## 7. 响应式

同 Wireframe：1440 起结果区可堆叠。

## 8. 评审投影

Wireframe §10 的 9 个 mount；BusinessMode absent；`metric_readiness_projection: []`。

## 9. Demo 交接

1. 路由 `/industry-center/shenzhen?tab=comparison|development|records`。  
2. 目标 ID：`F-SZ-*` / `CHAIN-SZ-*`；旧 `F-CHAIN-09/10` 迁移前勿再扩展。  
3. 发展分析必须显式 `source_result_id`。  
4. 任务流：显式提交 + 显式看结果。

## 10. Gap

| Gap | V1 |
| --- | --- |
| GAP-CHAIN-SZ-METRICS | Mock/Pending |
| GAP-CHAIN-SZ-PERMISSIONS | fail closed |
| GAP-CHAIN-SZ-APPROVAL | 合同沿用 |
| GAP-CHAIN-SZ-CASE-LIBRARY | 不宣称案例匹配已交付 |

## 11. 自检

5/5 故事、4/4 Frame、9/9 mounts；未扩范围；不代表 PDR 通过。  

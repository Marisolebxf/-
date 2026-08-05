# UX-SPEC-CHAIN-TOPIC-REGIONAL｜区域产业评价

> **文档版本**：v1.0-package-split  
> **四件套版本**：IA/TRACE/USM/Wireframe v1.0-package-split  
> **日期**：2026-08-05  
> **状态**：ready_for_v1  
> **体验 Owner**：human:高颖  
> **边界**：只转译已确认产品定义为可实现交互规则；不修改 Demo、不增删 Bid 叶子、不代表 PDR/Gate 通过。  
> **独立执行权威**：区域产业评价交互只读本文件；父包 UX-SPEC 中 F-07/F-08 段落仅溯源。

## 1. 权威输入

| 工件 | 版本 | 用途 |
| --- | --- | --- |
| IA / TRACE / USM / Wireframe | v1.0-package-split | 边界、故事、Frame、Gap |
| UX-UE 通用交互组件规范 | D10 | Tabs、表单、反馈、键盘 |
| Design.md | D8 | 视觉 token |
| 共享任务壳 | SYS-ANALYSIS-JOBS | 过程与显式看结果 |

## 2. 四件套同步核对

| 维度 | 数量 | 落点 |
| --- | --- | --- |
| 故事 | 5 | US-CHAIN-REG-01…05 |
| Frame | 4 | F-REG-01…04 |
| 路由 Tab | 3 | index / competitiveness / records |
| Bid 叶子 | 3 | 展示 `.2.2.3` `.2.2.8` + 算法 `.3.10` |
| review mounts | **9** | 见 Wireframe §10 |

同步结论：故事/Frame/路由一致；自定义指标与指标 readiness 为显式 Gap，不阻断 `v1_hifi_round1` 输入。

## 3. 用户旅程

### REG-J01｜政府指数评价闭环

故事：`US-CHAIN-REG-01/02/05`。  
主路径：确认产业对象 → `tab=index` 配组合与权重 → 预览 → 生成分析 → 共享过程 → 显式查看结果 → 可选记录恢复。  
异常：非法组合、权重错误、自定义指标不可用、不可比较对象、权限锁态。

### REG-J02｜园区竞争力评价闭环

故事：`US-CHAIN-REG-03/04/05`。  
主路径：确认产业对象 → `tab=competitiveness` 确认三维权重 → 生成分析 → 显式查看排名短板。  
异常：维度缺失、版本混排禁止、数据不足区域。

## 4. Frame 交互合同

### 4.1 F-REG-01 壳

- Tab 切换写 URL，保留产业对象；不携带另一 Tab 的区域/权重/预览。
- 无对象：主区空态 +「打开对比篮」；禁止整页空白无说明。
- 键盘：Tab 可聚焦；对比篮由系统入口打开。

### 4.2 F-REG-02 指数

| 触发 | 结果 | 禁止 |
| --- | --- | --- |
| 切换评价模式 | 校验组合上限；非法时禁用提交 | 自动删对象凑合法 |
| 改权重 | 实时校验合计；可一键均分 | 静默归一化后提交 |
| 轻量预览 | 显示预览值；不建 task | 写入分析记录 |
| 生成分析 | 最终校验 → 创建任务 → `task_created` | 未点按钮自动创建 |
| 查看分析结果 | 进入不可变结果 | 自动跳转结果 |

### 4.3 F-REG-03 竞争力

| 触发 | 结果 | 禁止 |
| --- | --- | --- |
| 调一级权重 | 三维固定展示；合计 100% | 增删维度、改内部算法 |
| 维度不可用 | 禁用生成并说明 | 降成两维 |
| 查看结果 | 排名/三维/热力图/短板 | 跨版本混排 |

### 4.4 F-REG-04 记录

- 过滤后列表恢复到对应 Tab 配置草稿、过程或结果。
- `queued` 撤回遵循共享任务合同；`running` 不提供用户取消。

## 5. 反馈与异常

| 场景 | 反馈 |
| --- | --- |
| permission_locked | 锁态 + 原因；隐藏敏感摘要 |
| unavailable | 与锁态区分的普通不可用 |
| incomparable | 列出对象与原因，无伪排名 |
| partial_metric_gap | 缺口标记 + 未参与计算项 |
| submit 失败 | 原位错误 + 可重试；配置保留 |

## 6. 组件、键盘与无障碍

- Tabs：Arco Tabs，方向键切换，选中态可见。
- 权重：InputNumber / Slider（若用）须可键盘操作；错误用文本不只靠颜色。
- 图表：需提供等价数据表或可读摘要（结果区）。
- 禁用控件须可读原因。

## 7. 响应式

同 Wireframe §7：1440 起图表可堆叠；配置控件不丢失。

## 8. 内部评审投影

| Frame | mount_id | BusinessMode |
| --- | --- | --- |
| F-01 | CHAIN-REG-F01-OBJECT-CONTEXT | absent |
| F-02 | CHAIN-REG-F02-INDEX-TITLE / INDEX-METRICS / CUSTOM-METRIC-GAP / PREVIEW | absent |
| F-03 | CHAIN-REG-F03-COMPETITIVENESS-TITLE / COMPETITIVENESS-METRICS / VERSION-BOUNDARY | absent |
| F-04 | CHAIN-REG-F04-RECORDS | absent |

`metric_readiness_projection: []`（无专题矩阵行时不投影伪 D1–D4）。

## 9. Demo 实施交接

1. 路由与 Tab：`/industry-center/regional?tab=index|competitiveness|records`。  
2. Frame/Mount 目标 ID：`F-REG-*` / `CHAIN-REG-*`；若代码仍为 `F-CHAIN-07/08`，迁移前不得再扩旧 ID。  
3. 对象组合与权重校验必须前端拦截 + 服务端再校验。  
4. 任务流：显式提交、显式看结果；预览永不落任务库。  
5. 自定义指标：只展示未纳入说明，不提供假入口。

## 10. Gap 与 V1 处理

| Gap | V1 |
| --- | --- |
| GAP-CHAIN-REG-CUSTOM-METRIC | 可见差异，不阻断首轮 |
| GAP-CHAIN-REG-METRICS | Mock/Pending + 评审挂点 |
| GAP-CHAIN-REG-PERMISSIONS | fail closed |
| GAP-CHAIN-REG-APPROVAL | 合同沿用；范围变化补批 |

## 11. 自检

1. 5/5 故事、4/4 Frame、9/9 mounts 有交互落点。  
2. 未修改产品范围。  
3. 与 Wireframe mounts 数字一致（9）。  
4. 不代表 PDR 通过。  

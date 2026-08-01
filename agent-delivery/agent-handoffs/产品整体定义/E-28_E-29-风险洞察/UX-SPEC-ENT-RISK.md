# UX-SPEC-ENT-RISK｜风险洞察对象上下文

> 状态：ready_for_v1（仅本次系统对比篮联动增量；模块整体状态继承 TRACE）
> 日期：2026-07-31
> delivery_stage：v1_hifi_round1
> screen_tier：medium_1440_1920

## 1. 输入与边界

- 对应 `IA / TRACE / USM / Wireframe-ENT-RISK` 当前版本；原始业务能力仍来自 E-28、E-29。
- 本增量只调整共享分析对象区与系统对比篮联动，不改变供应链图谱、痛难点模型、任务或报告。
- 供应链仍为 1–2 家，痛难点仍按当前集合上限；对象超限保留对象并阻断提交。

## 2. 状态与交互

| 状态 | 可见内容 | 操作与反馈 |
| --- | --- | --- |
| 配置态无对象 | Tab 上方“分析对象”；约 64px 紧凑状态行；“暂未选择分析对象 / 请在系统对比篮中选择企业” | “打开对比篮”原位展开系统浮层，不跳转 |
| 配置态有对象 | 来源、对象标签、不可用提示、管理全部对象 | “打开对比篮调整对象”原位展开；当次移除同步两个风险 Tab，但不回写篮 |
| 再次分发 | 目标风险类型、对象与来源数量一起更新 | `source=compare-basket` 时有效 `analysis_type` 优先于残留 `tab`；`enterprise_codes[]` 覆盖配置草稿 |
| 任务过程 / 结果 / 报告 | 使用任务对象快照 | 外部对象参数不覆盖任务快照 |
| 超限 / 无效 | 保留有效对象并显示 Alert | 禁用“开始分析”；打开篮调整，不静默截断 |

## 3. 状态机

```text
configuration.empty --打开对比篮--> configuration.empty + basket.expanded
configuration.populated --打开对比篮调整对象--> configuration.populated + basket.expanded
basket.dispatch --URL同步--> configuration.populated(analysis_type + enterprise_codes[])
configuration --开始分析--> processing(task snapshot) --> result --> report
```

## 4. 参数合同

1. `source=compare-basket` 时只接受 `supply-chain / pain-points` 两个有效 `analysis_type`，并使其优先于残留 `tab`。
2. 配置态监听有序 `enterprise_codes[]`，按企业 ID 去重；不可解析项计入 `unresolvedCount`。
3. 任务处理、结果和报告由 `task_id` 对应快照恢复对象、关系范围和诊断维度。
4. `open_compare_basket=1` 由系统浮层消费后删除，其他参数与两个 Tab 的配置草稿保持。

## 5. 可达性与验收

- 空态不用大尺寸 `Empty`；1440 / 1680 / 1920 均保持紧凑主结构。
- 点击“打开对比篮”后 pathname 保持 `/enterprise-center/risk`，对比篮具名区域可操作。
- 同一已挂载配置页再次收到对象参数后立即显示有效对象；切换风险类型不清空共享对象。
- 供应链超过 2 家继续显示全部已解析对象和明确原因，不截断、不误启用提交。

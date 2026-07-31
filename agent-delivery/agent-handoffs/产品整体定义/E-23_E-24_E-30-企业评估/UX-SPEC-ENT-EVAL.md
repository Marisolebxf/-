# UX-SPEC-ENT-EVAL｜企业评估对象上下文

> 状态：ready_for_v1（仅本次系统对比篮联动增量；模块整体状态继承 TRACE）
> 日期：2026-07-31
> delivery_stage：v1_hifi_round1
> screen_tier：medium_1440_1920

## 1. 输入与边界

- 对应 `IA / TRACE / USM / Wireframe-ENT-EVAL` 当前版本；原始业务能力仍来自 E-23、E-24、E-30。
- 本增量只调整对象上下文与系统对比篮联动，不改变评估模型、指标、任务、结果或报告。
- 对比篮是新增企业对象的唯一入口；页面内移除只影响本次配置草稿，不回写篮。

## 2. 状态与交互

| 状态 | 可见内容 | 操作与反馈 |
| --- | --- | --- |
| 配置态无对象 | 标题“评估对象”；约 64px 紧凑状态行；“暂未选择评估对象 / 请在系统对比篮中选择企业” | 右侧主按钮“打开对比篮”；设置 `open_compare_basket=1`，当前页面不跳转 |
| 配置态有对象 | “来自对比篮 · X 家”、对象标签、不可用对象提示、渐进披露 | 标题操作“打开对比篮调整对象”；原位展开系统浮层；当次移除不回写篮 |
| 再次分发 | 新模式、新对象与来源数量一起更新 | `source=compare-basket` 时有效 `analysis_type` 优先于残留 `mode`；`enterprise_codes[]` 覆盖配置草稿 |
| 任务过程 / 结果 / 报告 | 展示任务对象快照 | 外部路由对象参数不覆盖任务快照 |
| 全部对象无效 | 紧凑无对象状态 + 不可用数量 Alert | 可打开对比篮重新选择；不预填演示企业 |

## 3. 状态机

```text
configuration.empty --打开对比篮--> configuration.empty + basket.expanded
configuration.populated --打开对比篮调整对象--> configuration.populated + basket.expanded
basket.dispatch --URL同步--> configuration.populated(mode + enterprise_codes[])
configuration --生成评估--> processing(task snapshot) --> result --> report
```

## 4. 参数合同

1. `source=compare-basket` 且 `analysis_type` 有效：采用 `analysis_type`。
2. 其他入口：采用有效 `mode`，再兼容 `analysis_type`、`capabilityType` 与旧 Tab。
3. 配置态监听有序 `enterprise_codes[]`，按企业 ID 去重并解析；不可解析项计入 `unresolvedCount`。
4. `open_compare_basket=1` 由系统浮层消费并从 URL 删除，其他配置参数保持。

## 5. 可达性与验收

- 两个按钮均为 Arco `Button`，具有可见焦点；系统浮层使用具名 `region`。
- 空态不使用大尺寸 `Empty`，1440 / 1680 / 1920 均保持单行主结构。
- 点击入口后 URL pathname 不变且“对比篮”区域可操作。
- 冲突参数 `source=compare-basket&analysis_type=business&mode=competitiveness` 必须选择商业力评估。
- 同一已挂载页面从空对象再次收到 3 个有效编码后，显示 3 家企业，不要求刷新。

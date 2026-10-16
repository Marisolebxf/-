# 产业周期分析 脚本→用例 覆盖表（2026-10-14 BATCH32 · chain-cycle）

蓝本 = `qa/test-cases/KJZTFWXT/industry-center-产业链分析/CYCLE-产业周期分析/FUNC-产业周期分析-用例.md` v2.0（00546~00561，16 条）。
脚本 **16 条**（金样 4 + 其余 12，includes 展开），与用例 **1:1**，无未脚本化。

金样锁定（用例册元信息）：P0-01=00546 · P0-02=00549 · P0-03=00551 · P0-04=00553（烟测=跑全部金样；条数不强制 5）。

## 主表（脚本 → 用例）

| 脚本 id | 用例编号 | 页面区块/状态 | P | 可见动作 |
|---------|----------|---------------|---|----------|
| P0-01 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00546 | 入口·路由与双 Tab | P0 | goto cycle 核对路由/标题/Tab |
| P0-02 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00549 | 配置·四参数默认 | P0 | 默认态核对 4 spin + 查看 |
| P0-03 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00551 | 异步·开始分析 | P0 | 点开始分析；改时间不自动起 |
| P0-04 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00553 | 结果·阶段与报告 | P0 | 诊断记录→查看结果 |
| P0-05 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00547 | 配置·对象两级联动 | P0 | 切产业「生物产业」 |
| P0-06 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00548 | 配置·时间范围 | P0 | Select 近3年/近5年 |
| P0-07 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00550 | 配置·参数编辑 | P0 | 键入/调节/清空 |
| P0-08 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00552 | 过程·能力词产物词 | P0 | 开始分析后读文案 |
| P0-09 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00554 | 结果·预测与重跑 | P0 | 查看结果→新建分析 |
| P1-01 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00555 | 备选·查看与重置 | P1 | 查看 + 重置参数 |
| P1-02 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00556 | 备选·双 Tab 草稿 | P1 | Tab 往返 |
| P1-03 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00557 | 备选·版本只读 | P1 | 读三项 version input |
| P1-04 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00558 | 备选·诊断记录列表 | P1 | 切诊断记录 |
| P1-05 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00559 | 备选·恢复任务 | P1 | 查看结果复用 task_id |
| P1-06 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00560 | 备选·评审零泄漏 | P1 | 开/关内部评审模式 |
| P1-07 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00561 | 异常·未选对象拦截 | P1 | 清空集群后点开始分析 |

## 覆盖说明

- **16/16 全脚本化**：无未脚本化声明。
- **allow_skip**：P0-04 / P0-09 / P1-05（依赖诊断记录已完成任务；环境无完成态时 Pass-N/A）。
- **同路由兄弟**：关键环节 / 瓶颈堵点 **不写正向**（仅本 entry `workspace=cycle`）。
- **对比篮**：系统浮层 observed，专项归 COMPARE。

## as_built 偏差（写入脚本 as_built_note，不升发明断言）

1. 用例「周期参数默认启用」→ 现场数据状态列 **「可用」**（P0-02）。
2. 时间范围：用例写快捷项 → 现场为 **Select**（近3年/近5年），默认近5年（P0-06）。
3. 分析对象 aria-label：**集群 / 产业**（对应用例产业 / 产业链）（P0-05）。
4. 未选对象：按钮 **仍 enabled**，点击提示「尚未选择分析对象」拦截（P1-07）。
5. 结果态诚实降级常见（驱动因素/拐点未返回）；禁「已完成实时全网检索」（P0-09）。
6. 版本三项为 **readonly input value**（非可见文本节点）（P1-03）。

# 深圳产业情况分析对比 脚本→用例 覆盖表（2026-10-14 BATCH32 · chain-sz-compare）

蓝本 = `qa/test-cases/KJZTFWXT/industry-center-产业链分析/SZCMP-深圳产业情况分析对比/FUNC-深圳产业情况分析对比-用例.md` v2.0（00732~00753，22 条）。
脚本 **22 条**（金样 5 + 其余 17，includes 展开），与用例 **1:1**，无未脚本化。

金样锁定（用例册元信息）：P0-01=00732 · P0-02=00734 · P0-03=00737 · P0-04=00738 · P0-05=00742（烟测=跑全部金样）。

## 主表（脚本 → 用例）

| 脚本 id | 用例编号 | 页面区块/状态 | P | 可见动作 |
|---------|----------|---------------|---|----------|
| P0-01 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00732 | 入口·路由与标题 | P0 | goto comparison 核对路由/标题 |
| P0-02 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00734 | 配置·产业占位与选项 | P0 | 产业占位 + 展开集群清单 |
| P0-03 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00737 | 配置·主体深圳锁定 | P0 | 读/改写/清空主体 |
| P0-04 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00738 | 配置·标杆诚实空态 | P0 | 读 Q016 占位；禁预置城市 |
| P0-05 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00742 | 异步·显式开始分析 | P0 | 点开始（可 skip）；切条件不自动起 |
| P0-06 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00733 | 入口·双 Tab 构成 | P0 | 默认态核对 Tab |
| P0-07 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00735 | 配置·集群切换回显 | P0 | 生物产业↔新一代信息技术 |
| P0-08 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00736 | 配置·切换后保持 | P0 | 切集群后读主体/维度 |
| P0-09 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00739 | 配置·四维只读 | P1 | 读 4 spin；尝试改值 |
| P0-10 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00740 | 配置·只读启用形态 | P1 | 读查看×4 / 无增删维 |
| P0-11 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00741 | 操作·门控状态机 | P0 | 未选禁用；选产业后 observed |
| P0-12 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00753 | 异常·禁用态触发 | P0 | force click + Enter |
| P1-01 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00743 | 备选·重置回默认 | P1 | 选产业→重置参数 |
| P1-02 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00744 | 备选·重置后保持 | P1 | 重置后读主体/标杆/门控 |
| P1-03 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00745 | 备选·同条件单飞 | P1 | 双点开始分析 |
| P1-04 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00746 | 备选·当天结果复用 | P1 | 分析记录→查看结果 |
| P1-05 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00747 | 备选·重新分析 | P1 | 结果态「按此配置新建分析」 |
| P1-06 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00748 | 备选·Tab 互切保持 | P1 | 记录↔对比 Tab |
| P1-07 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00749 | 备选·记录构成过滤 | P1 | 切分析记录浏览 |
| P1-08 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00750 | 备选·development 隔离 | P1 | 切 development 再切回 |
| P1-09 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00751 | 备选·评审增量可见 | P1 | 开评审→追溯/角标 |
| P1-10 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00752 | 备选·关闭零泄漏 | P1 | 关评审→刷新两 Tab |

> 金样 = P0-01~05（id 锁定禁改）；脚本 id 前缀与用例优先级列独立（主表 P 列写用例优先级）。

## 覆盖说明

- **22/22 全脚本化**：用例册 00732~00753 每行恰一脚本；无未脚本化声明。
- **expect 点数**：全部译自用例「预期结果」列；双层 `{note, assert}`（X9）。
- **allow_skip**：P0-05（开始分析因 Q016 禁用时创建任务点）/ P1-03 / P1-04 / P1-05。
- **同路由兄弟**：`workspace=development`（chain-sz-dev）**不写正向**（仅 P1-08 隔离）。
- **对比篮**：系统浮层 observed，专项归 COMPARE。

## as_built 偏差（写入脚本 as_built_note，不升发明断言）

| 脚本 | 用例 | 偏差 |
|------|------|------|
| P0-02 | 00734 | 分析对象为**双级** Select（集群 + 产业）；占位「请选择产业」在产业级；15 集群在集群级 |
| P0-05 / P0-11 | 00742 / 00741 | 选产业后「开始分析」仍 **disabled**（标杆 Q016 空）；00741 第二点按用例备注 observed；00742 创建任务点 allow_skip |
| P1-01 | 00743 | **重置参数不清**集群/产业选中（实勘仍留脏值）；机检按用例期望回占位（预期红）+ as_built_note |
| P1-05 | 00747 | 现场入口文案为「按此配置新建分析」，非「重新分析」 |
| P1-07 | 00749 | 时间列名「创建时间」；报告操作为「查看报告/下载报告」 |

## 未脚本化

无。

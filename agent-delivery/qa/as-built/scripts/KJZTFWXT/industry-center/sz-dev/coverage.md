# 深圳产业发展分析 脚本→用例 覆盖表（2026-10-14 BATCH32 · chain-sz-dev）

蓝本 = `qa/test-cases/KJZTFWXT/industry-center-产业链分析/SZDEV-深圳产业发展分析/FUNC-深圳产业发展分析-用例.md` v2.0（00754~00778，25 条）。
脚本 **25 条**（金样 6 + 其余 19，includes 展开），与用例 **1:1**，无未脚本化。

金样锁定（用例册元信息）：P0-01=00754 · P0-02=00756 · P0-03=00758 · P0-04=00759 · P0-05=00761 · P0-06=00762（烟测=跑全部金样；条数按可测主路径为 6，不强制 5）。

## 主表（脚本 → 用例）

| 脚本 id | 用例编号 | 页面区块/状态 | P | 可见动作 |
|---------|----------|---------------|---|----------|
| P0-01 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00754 | 入口·路由与标题 | P0 | goto development 核对路由/标题 |
| P0-02 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00756 | 配置·产业占位与选项 | P0 | 产业占位 + 展开 15 选项 |
| P0-03 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00758 | 配置·主体深圳锁定 | P0 | 读/改写/清空主体 |
| P0-04 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00759 | 配置·绑定占位与只读 | P0 | 读 placeholder；禁键入 |
| P0-05 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00761 | 操作·门控状态机 | P0 | 初始禁用→仅产业仍禁→绑有效后可用 |
| P0-06 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00762 | 异步·显式开始分析 | P0 | 点开始（可 skip）；切条件不自动起 |
| P0-07 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00755 | 入口·双 Tab 构成 | P0 | 默认态核对 Tab |
| P0-08 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00757 | 配置·产业切换回显 | P0 | 生物↔新一代信息技术 + 主体保持 |
| P0-09 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00760 | 配置·无效绑定过滤 | P0 | 展开绑定；点无效项 |
| P0-10 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00763 | 结果·来源依据快照 | P0 | 查看结果（allow_skip） |
| P0-11 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00764 | 结果·完整对比抽屉 | P0 | 抽屉只读（allow_skip） |
| P0-12 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00765 | 结果·三类建议 | P0 | 政策/技术/人才（allow_skip） |
| P0-13 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00766 | 结果·多套路径 | P0 | 路径/诚实标注（allow_skip） |
| P0-14 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00778 | 异常·禁用态触发 | P0 | force click + Enter |
| P1-01 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00767 | 备选·发展目标勾选 | P1 | 三勾状态机 |
| P1-02 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00768 | 备选·重置回门控 | P1 | 脏配置→重置参数 |
| P1-03 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00769 | 备选·同条件单飞 | P1 | 双点开始分析 |
| P1-04 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00770 | 备选·当天结果复用 | P1 | 分析记录→查看结果 |
| P1-05 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00771 | 备选·重新分析 | P1 | 结果态重跑入口 |
| P1-06 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00772 | 备选·Tab 互切保持 | P1 | 记录↔发展 Tab |
| P1-07 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00773 | 备选·记录构成过滤 | P1 | 切分析记录浏览 |
| P1-08 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00774 | 备选·comparison 隔离 | P1 | 切 comparison 再切回 |
| P1-09 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00775 | 备选·评审增量可见 | P1 | 开评审→追溯/角标 |
| P1-10 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00776 | 备选·关闭零泄漏 | P1 | 关评审→刷新两 Tab |
| P1-11 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00777 | 异常·刷新不继承 | P1 | reload 后绑定仍占位 |

> 金样 = P0-01~06（id 锁定禁改）；脚本 id 前缀与用例优先级列独立（主表 P 列写用例优先级）。

## 覆盖说明

- **25/25 全脚本化**：用例册 00754~00778 每行恰一脚本；无未脚本化声明。
- **expect 点数**：全部译自用例「预期结果」列；双层 `{note, assert}`（X9）。
- **allow_skip**：P0-05（无有效绑定时第三点）/ P0-06（创建任务点）/ P0-09（无无效并存）/ P0-10~P0-13 / P1-03~P1-05 / P1-07（空记录）。
- **同路由兄弟**：`workspace=comparison`（chain-sz-compare）**不写正向**（仅 P1-08 隔离）。
- **对比篮**：系统浮层 observed，专项归 COMPARE。

## as_built 偏差（写入脚本 as_built_note，不升发明断言）

| 脚本 | 用例 | 偏差 |
|------|------|------|
| P0-02 | 00756 | 分析对象为**单级** Select（15 产业集群项）；对比册为双级集群+产业——勿混 locator |
| P0-05 / P0-06 | 00761 / 00762 | 门控依赖有效对比结果绑定；无绑定时创建任务 allow_skip |
| P1-02 | 00768 | **重置清绑定+门控禁用**；产业选中可能残留；目标保持默认三勾（非全空） |
| P1-07 | 00773 | 时间列名「创建时间」；报告操作为「查看报告/下载报告」；空态「暂无数据」可 skip |
| P0-10~13 / P1-04/05 | 00763~66 / 00770/71 | 勘察无成功结果；失败态「查看结果」disabled |

## 未脚本化

无。

# 培育企业推荐分析 脚本→用例 覆盖表（2026-10-14 BATCH32）

蓝本 = `qa/test-cases/KJZTFWXT/enterprise-企业分析/CULTIVATE-培育企业推荐分析/FUNC-培育企业推荐分析-用例.md` v2.0（01004~01031，28 条）。
脚本 **28** 条（金样 5 + 其余 23，includes 展开），与用例 **1:1**。
金样锁定：P0-01=01004 · P0-02=01010 · P0-03=01013 · P0-04=01014 · P0-05=01020。

## 主表（脚本 → 用例）

| 脚本 id | 用例编号 | 页面区块/状态 | P | 可见动作 |
|---------|----------|---------------|---|----------|
| P0-01 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01004 | 入口·路由与默认 Tab | P0 | 深链 goto |
| P0-02 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01010 | 门控·无条件置灰 | P0 | 默认态核对 |
| P0-03 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01013 | 异步·发起到成功 | P0 | 选条件+开始分析（成功 allow_skip） |
| P0-04 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01014 | 名单·列构成 | P0 | 浏览成功名单（allow_skip） |
| P0-05 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01020 | 候选·加入培育 | P0 | 对比篮加入培育候选 |
| P0-06 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01005 | 隔离·workspace | P0 | cultivation↔attraction |
| P0-07 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01006 | 条件·三选择器占位 | P0 | 浏览 |
| P0-08 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01007 | 条件·8 产业链项 | P0 | 产业类别下拉 |
| P0-09 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01008 | 条件·选择回显 | P0 | 选产业+规模 |
| P0-10 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01009 | 条件·政策导向 | P0 | 下拉开关两次 |
| P0-11 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01011 | 门控·恢复可用 | P0 | 选规模 |
| P0-12 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01012 | 图例·8 态 | P0 | 展开状态 select |
| P0-13 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01015 | 名单·所需支持 | P0 | 浏览（allow_skip） |
| P0-14 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01016 | 详情·一企一策链路 | P0 | 点行（allow_skip） |
| P0-15 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01017 | 指标·ⓘ 弹卡 | P0 | 点指标说明 |
| P0-16 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01018 | 角标·阈值待定 | P0 | 点 Q015 角标 |
| P0-17 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01019 | 候选工作台·构成 | P0 | 切 Tab |
| P0-18 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01021 | 最近分析·构成 | P0 | 切 Tab |
| P1-01 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01022 | Tab·往返保留 | P1 | 三 Tab 往返 |
| P1-02 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01023 | 详情·行业分布 | P1 | allow_skip |
| P1-03 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01024 | 异步·防重提交 | P1 | 分析中再点 |
| P1-04 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01025 | 空结果态 | P1 | allow_skip |
| P1-05 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01026 | 字段缺失降级 | P1 | allow_skip |
| P1-06 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01027 | 条件变更重分析 | P1 | 提示可测；成功 allow_skip |
| P1-07 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01028 | 对比篮·落点隔离 | P1 | 两按钮 |
| P1-08 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01029 | 历史·不覆盖条件 | P1 | allow_skip（常空） |
| P1-09 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01030 | 同条件复用 | P1 | allow_skip |
| P1-10 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01031 | 评审·三枚追溯零泄漏 | P1 | 开/关评审 |

## 未脚本化

无（28/28 均有脚本 id；其中依赖成功态/空结果/历史任务的条目以 `allow_skip` 声明构造不足时 Pass-N/A，不判未脚本化）。

## 覆盖说明

- **expect**：全部双层 `{note, assert}`；译自用例预期列，未发明额外断言。
- **allow_skip 预置**：P0-03（成功点）/ P0-04 / P0-13 / P0-14 / P1-02 / P1-04 / P1-05 / P1-06（第三点）/ P1-08 / P1-09 —— 根因：2026-10-14 实勘发起分析常落「推荐分析失败」，最近分析常「暂无数据」。
- **as-built 偏差**（见各条 `as_built_note`）：
  1. 用例「8 快捷标签」→ 现场无独立 chip，8 项在「产业类别」下拉（同 sz-status）。
  2. 用例「政策导向空选项」→ 现场已返回四项（科技创新/产业升级/绿色发展/市场拓展）。
  3. 对比篮关闭钮可能不可见——可见再点。
  4. 同路由招引视图条件区不写入本套（P0-06 仅验隔离）。
- **禁止越界**：不写招引推荐条件详验、不写报告 Reader、不写对比篮 L2/L3 深层。

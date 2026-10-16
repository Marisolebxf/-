# 企业供应链关系分析 脚本→用例 覆盖表（2026-10-14）

蓝本 = `qa/test-cases/KJZTFWXT/enterprise-企业分析/SUPPLY-企业供应链关系分析/FUNC-企业供应链关系分析-用例.md` v2.0（01032~01055，24 条）。
脚本 24 条（金样 5 + 其余 19，includes 展开），与用例 **1:1**。

金样（用例册元信息锁定）：P0-01=01032 · P0-02=01039 · P0-03=01041 · P0-04=01044 · P0-05=01046。

locator 基准 = `fixtures/scout/`（先 `/login` 再深链；`_probe.mjs` / `_probe-deep.mjs` / `_probe-result2.mjs`）。

## 主表（脚本 → 用例）

| 脚本 id | 用例编号 | 页面区块/状态 | P | 可见动作 |
|---------|----------|---------------|---|----------|
| P0-01 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01032 | 入口·路由与双 Tab | P0 | 深链 supply-chain |
| P0-02 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01039 | 门控·开始分析禁用 | P0 | 空态+浮层勾 3 家 |
| P0-03 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01041 | 结果·供应链图谱 | P0 | 最近分析→恢复结果 |
| P0-04 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01044 | 结果·关键节点清单 | P0 | 关键节点 Tab（allow_skip 空） |
| P0-05 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01046 | 结果·断链风险标注 | P0 | 断链风险 Tab |
| P0-06 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01033 | 隔离·workspace | P0 | 切痛点再切回 |
| P0-07 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01034 | 配置·对象空态 | P0 | 浏览空态引导 |
| P0-08 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01035 | 配置·关系范围三选 | P0 | 浏览三复选 |
| P0-09 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01036 | 配置·对象带入 | P0 | 前往对比篮→确定 |
| P0-10 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01037 | 配置·对象上限 | P0 | 浮层勾 3 家 |
| P0-11 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01038 | 配置·预检区块 | P0 | 空态+回填预检 |
| P0-12 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01040 | 过程·开始分析发起 | P0 | 点开始分析 |
| P0-13 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01042 | 图谱·逐层下钻 | P0 | 默认 1 级（下钻 allow_skip） |
| P0-14 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01043 | 图谱·末级提示 | P0 | allow_skip |
| P0-15 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01045 | 清单·双向定位 | P0 | allow_skip（关键节点空） |
| P0-16 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01047 | 风险·联动定位 | P0 | 断链风险项（入口 allow_skip） |
| P0-17 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01048 | 历史·恢复结果 | P0 | 恢复结果 |
| P0-18 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01049 | 历史·列表字段 | P0 | 最近分析 Tab |
| P1-01 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01050 | 配置·关系范围组合 | P1 | 勾选组合/全不选 |
| P1-02 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01051 | Tab·往返保留 | P1 | 当前↔最近 |
| P1-03 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01052 | 风险·备份方案提示 | P1 | 断链风险项文案 |
| P1-04 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01053 | 对象·移除不回写 | P1 | 移除 1 家 |
| P1-05 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01054 | 对象·清空回空态 | P1 | 移除全部 |
| P1-06 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01055 | 评审·追溯显隐 | P1 | 内部评审模式开关 |

> 金样 = P0-01/02/03/04/05（id 锁定禁改）。

## 覆盖说明

- **24/24 已脚本化**：无「未脚本化」空洞；图谱下钻/末级/关键节点定位等标 `allow_skip`（无稳定 locator 或样例数据空）。
- **未脚本化清单**：无。
- **expect**：全部双层 `{note, assert}`；译自用例预期列。
- **同路由隔离**：本套 `entry_id=ent-supply` only；痛点视图仅 P0-06 隔离反向，不写痛点正向。
- **as-built 偏差（2026-10-14 headless）**：
  1. 对象带入 = 页内「前往对比篮选择企业」→「选择分析企业」浮层「确定」回填（不发起）；非系统篮「发起分析」+六类型弹窗（P0-09）。
  2. 超限前移：浮层勾选第 3 家后「确定」禁用且显示「已选 3 家」，无法回填 3 家到配置页预检（P0-02/P0-10）。
  3. 空态引导文案：「请先在对比篮选择企业，再进入风险洞察配置。」
  4. 关系范围默认三选全勾；预检回填后四行：对象有效/数据覆盖/模型状态/权限范围。
  5. 新发起任务可快速「分析失败」；结果态金样靠「最近分析→恢复结果」（如 RISK-20260910-001）。
  6. 「核心供应商清单」现场落在「关键节点」Tab；样例任务关键节点 0 项、断链风险 2 项（节点异常/路径脆弱）+「建议提前制定备份方案」。
  7. 评审追溯 aria-label：`风险洞察需求追溯` / `关系范围需求追溯`。
  8. 对比篮关闭钮可能不可见——脚本内可见再点。

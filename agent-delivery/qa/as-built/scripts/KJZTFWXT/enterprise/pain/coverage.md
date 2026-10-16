# 企业发展痛难点分析 脚本→用例 覆盖表（2026-10-14 BATCH32 · ent-pain）

蓝本 = `qa/test-cases/KJZTFWXT/enterprise-企业分析/PAIN-企业发展痛难点分析/FUNC-企业发展痛难点分析-用例.md` v2.0（01070~01099，30 条）。
脚本 30 条（金样 5 + 其余 25，includes 展开），与用例 **1:1**。

金样（用例册元信息锁定）：P0-01=01070 · P0-02=01075 · P0-03=01079 · P0-04=01080 · P0-05=01085。

locator 基准 = `fixtures/scout/`（2026-10-14 headless；survey-page + `_probe*.mjs`）。

## 主表（脚本 → 用例）

| 脚本 id | 用例编号 | 页面区块/状态 | P | 可见动作 |
|---------|----------|---------------|---|----------|
| P0-01 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01070 | 入口·路由/页头/双 Tab | P0 | 深链 pain-points |
| P0-02 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01075 | 对象·确定回填 | P0 | CTA→勾选→确定 |
| P0-03 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01079 | 过程·开始分析 | P0 | 开始分析→processing |
| P0-04 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01080 | 结果·诊断构成 | P0 | 最近分析→恢复结果（A·零 allow_skip） |
| P0-05 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01085 | 报告·四段/入口 | P0 | 创建报告（allow_skip） |
| P0-06 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01071 | 隔离·workspace | P0 | 切 supply 再回 pain |
| P0-07 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01072 | 空态·门控 | P0 | 空态核开始分析禁用 |
| P0-08 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01073 | 对比篮·发起门控 | P0 | 系统篮勾选→发起分析 |
| P0-09 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01074 | 弹窗·六类型 | P0 | 发起分析→类型清单 |
| P0-10 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01076 | 诊断范围·四维 | P0 | 勾选组合 |
| P0-11 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01077 | 预检·呈现边界 | P0 | 浏览预检区（A 档·零 allow_skip） |
| P0-12 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01078 | 开始分析·唯一入口 | P0 | 条件满足后可用 |
| P0-13 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01081 | 结果·维度标记 | P0 | 恢复结果浏览 |
| P0-14 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01082 | 结果·五层链路 | P0 | 命中依据…解决方向 |
| P0-15 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01083 | 结果·匹配依据 | P0 | 命中依据区 |
| P0-16 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01084 | 结果·集合共性 | P0 | Top5 + 四维诊断 |
| P1-01 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01086 | Tab·往返保留 | P1 | 最近↔当前 |
| P1-02 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01087 | 对象·1–50 集合 | P1 | 勾选 6 家回填 |
| P1-03 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01088 | 对象·摘要收纳 | P1 | 管理全部对象入口 |
| P1-04 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01089 | 抽屉·搜索移除 | P1 | 打开抽屉 |
| P1-05 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01090 | 维度·全不选拦截 | P1 | 取消四维 |
| P1-06 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01091 | 预检·刷新 | P1 | 空态→回填 |
| P1-07 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01092 | 过程·无结果入口 | P1 | processing 无创建报告 |
| P1-08 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01093 | 结果·维度跟随 | P1 | B·allow_skip ticket=ENV-PAIN-PARTIAL-DIM（全维历史不可核部分维跟随） |
| P1-09 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01094 | 结果·数据不足 | P1 | 暂不判断 |
| P1-10 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01095 | 集合·典型企业 | P1 | 典型企业文案 |
| P1-11 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01096 | 空结果门控 | P1 | **allow_skip**（难构造） |
| P1-12 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01097 | 报告·入口三态 | P1 | 创建/生成中 |
| P1-13 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01098 | 最近分析·恢复 | P1 | 列表+恢复同 task_id |
| P1-14 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-01099 | 评审·追溯显隐 | P1 | 内部评审模式开关 |

> 金样 = P0-01/02/03/04/05（id 锁定禁改）。脚本 id 前缀与用例优先级列独立。

## 覆盖说明

- **30/30 全脚本化**：无空洞；P1-11（01096 无问题空结果）与部分结果链预置 `allow_skip`。
- **未脚本化清单**：无（01096 已挂脚本但声明构造难 → allow_skip，不算未脚本化空洞）。
- **expect**：全部双层 `{note, assert}`。
- **as-built 偏差（2026-10-14 headless）**：
  1. 页内 CTA 走「选择分析企业」**确定回填**；六类型走系统 dock「发起分析」→「选择分析任务」（类型名「企业发展痛点分析」非「痛难点」）。
  2. 对比篮「关闭对比篮」常 **not-visible**——脚本仅可见时点击。
  3. 新发起任务常快速「分析失败」仍停 `view=processing`；结果态优先「最近分析→恢复结果」。
  4. 报告区标题「发展痛难点分析建议报告」；创建后可能长时间「生成中」；问题卡层文案为命中依据/成因/行业最佳实践/解决方向。
  5. ≥6 家摘要：前三家 +「管理全部对象（N 家）」。
  6. 过程页任务摘要可出现「进度 0%」（observed）；预检区无接入进度百分比。
  7. **同路由隔离**：本套 `entry_id=ent-pain` only；供应链仅 P0-06 隔离反向，不写兄弟正向。

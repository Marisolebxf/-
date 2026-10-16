# 重点企业领域分析 脚本→用例 覆盖表（2026-10-14）

蓝本 = `qa/test-cases/KJZTFWXT/enterprise-企业分析/KEYDOM-重点企业领域分析/FUNC-重点企业领域分析-用例.md` v2.0（00511~00530，20 条）。
脚本 20 条（金样 5 + 其余 15，includes 展开），与用例 **1:1**。
金样锁定（用例册元信息）：P0-01=00511 · P0-02=00512 · P0-03=00515 · P0-04=00516 · P0-05=00518。

## 主表（脚本 → 用例）

| 脚本 id | 用例编号 | 页面区块/状态 | P | 可见动作 |
|---------|----------|---------------|---|----------|
| P0-01 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00511 | 入口·侧栏进入 | P0 | 进入领域页核路由/标题 |
| P0-02 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00512 | 空态·待选择 | P0 | 浏览空态引导 |
| P0-03 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00515 | 结果·四大区块 | P0 | 回填对象后核区块顺序 |
| P0-04 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00516 | 概览·KPI | P0 | 浏览概览四卡 |
| P0-05 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00518 | 概览·指标说明 | P0 | 评审态点 ⓘ |
| P0-06 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00513 | 对比篮·六类型弹窗 | P0 | dock 勾选→发起→选领域→下一步 |
| P0-07 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00514 | 页头·对象徽记 | P0 | 浏览来自对比篮徽记 |
| P0-08 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00517 | 概览·对象联动 | P0 | 调整对象后看指标 |
| P0-09 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00520 | 区块·企业领域覆盖 | P0 | 浏览矩阵 |
| P0-10 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00521 | 区块·跨领域布局 | P0 | 浏览关系图 |
| P0-11 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00522 | 区块·重点领域分布 | P0 | 浏览表+调整刷新 |
| P0-12 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00523 | 报告·打开返回 | P0 | 查看 HTML 报告→返回 |
| P1-01 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00519 | 口径·多源说明 | P1 | 评审态打开说明卡 |
| P1-02 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00524 | 报告·领域结论 | P1 | 报告目录/返回对象 |
| P1-03 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00525 | URL·上下文 | P1 | 系统发起核参+返回 |
| P1-04 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00526 | 对象·同名去重 | P1 | 人工造数（manual/allow_skip） |
| P1-05 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00527 | 报告·入口时序 | P1 | 空态/结果态看报告按钮 |
| P1-06 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00528 | 隔离·同壳参数 | P1 | type→domain 往返 |
| P1-07 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00529 | 异常·刷新恢复 | P1 | reload 结果态 |
| P1-08 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00530 | 评审·零泄漏 | P1 | 评审开/关 |

## 覆盖说明

- **20/20 已脚本化**：无「未脚本化」空洞；P1-04 为 manual + allow_skip（数据前提）。
- **未全机检**：P1-04（同名异主体样本不足）→ `manual: true` + `allow_skip`。
- **expect**：全部双层 `{note, assert}`；P1-04 第二条仅 note+manual。
- **as-built 现场偏差**（写入各脚本 as_built_note / fixtures）：
  1. 空态无「四入口」长引导，仅「尚未选择企业」+ 对比篮 CTA。
  2. 概览 KPI 业务态文案为「已覆盖领域/涉及企业/跨领域企业/识别依据」四卡；用例三项名对齐评审态指标说明 aria。
  3. 「查看 HTML 报告」空态页头亦可见（与 00527 用例「空态无入口」相反）——P1-05 以实勘断言可见。
  4. 结果对象有两条路径：页内「选择分析企业」确定回填；系统 dock「发起分析」→六类型（含 return_context_id）。
  5. 同壳无页内 Tab，侧栏两个二级入口。

## 自检

- [x] 每条用例 ≥1 脚本；func_id 尾号与用例一致
- [x] 金样 5 条 = 00511/00512/00515/00516/00518
- [x] 未写 view=type 类型看板内容（隔离仅 P1-06）
- [x] 业务态断言路径含关评审（P0-05/P1-01/P1-08）

# 产业关键环节识别 脚本→用例 覆盖表（2026-10-14 BATCH32 · chain-key-link）

蓝本 = `qa/test-cases/KJZTFWXT/industry-center-产业链分析/KEYLINK-产业关键环节识别/FUNC-产业关键环节识别-用例.md` v2.0（00578~00600，23 条）。
脚本 23 条（金样 5 + 其余 18，includes 展开），与用例 **1:1**。

金样（用例册元信息锁定）：P0-01=00578 · P0-02=00579 · P0-03=00581 · P0-04=00583 · P0-05=00585。

locator 基准 = `fixtures/scout/`（2026-10-14 headless；survey-page + scout-deep / scout-result / scout-start）。

## 主表（脚本 → 用例）

| 脚本 id | 用例编号 | 页面区块/状态 | P | 可见动作 |
|---------|----------|---------------|---|----------|
| P0-01 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00578 | 入口·路由/页头/双 Tab | P0 | 深链 key_link |
| P0-02 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00579 | 配置·三级默认 | P0 | 读集群/产业/细分 |
| P0-03 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00581 | 配置·三权重只读 | P0 | spinbutton 34/33/33 |
| P0-04 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00583 | 操作·开始分析闸门 | P0 | 开始分析；切对象不自动起 |
| P0-05 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00585 | 结果·全链路五环节 | P0 | 诊断记录→查看结果 |
| P0-06 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00580 | 配置·三级联动 | P0 | 切生物产业→重置 |
| P0-07 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00582 | 配置·版本四项只读 | P0 | 读 disabled input |
| P0-08 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00584 | 过程·阶段能力词 | P0 | 开始分析（allow_skip） |
| P0-09 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00586 | 结果·边界/衔接 | P0 | 查看结果 |
| P0-10 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00587 | 结果·高端化指数 | P0 | 查看结果 |
| P0-11 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00588 | 结果·关键/皇冠图例 | P0 | 查看结果 |
| P1-01 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00589 | 结果·排序切换 | P1 | **allow_skip**（无控件） |
| P1-02 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00590 | 操作·重置参数 | P1 | 脏配置→重置 |
| P1-03 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00591 | 上下文·共享 | P1 | 切 bottleneck 再回（仅共享） |
| P1-04 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00592 | 诊断记录·列表 | P1 | 切诊断记录 Tab |
| P1-05 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00593 | 评审·零泄漏 | P1 | 开/关内部评审模式 |
| P1-06 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00594 | 诊断记录·恢复 | P1 | 查看结果 |
| P1-07 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00595 | 隔离·兄弟 workspace | P1 | cycle/bottleneck 往返（仅隔离） |
| P1-08 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00596 | 版本·快照只读往返 | P1 | Tab 往返 |
| P1-09 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00597 | 结果·格局/企业/趋势 | P1 | 查看结果（allow_skip） |
| P1-10 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00598 | 结果·强制重跑 | P1 | 按此配置新建分析 |
| P1-11 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00599 | 异常·对象空/不齐 | P1 | 切集群门控 |
| P1-12 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00600 | 异常·数据不足诚实 | P1 | 查看结果空态 |

> 金样 = P0-01/02/03/04/05（id 锁定禁改）。脚本 id 前缀与用例优先级列独立。

## 覆盖说明

- **23/23 全脚本化**：无空洞；P0-08 / P1-01 / P1-09 等预置 `allow_skip`（过程 UI / 排序控件 / 趋势区块现场不稳定）。
- **未脚本化清单**：无。
- **expect**：全部双层 `{note, assert}`。
- **as-built 偏差（2026-10-14 headless）**：
  1. 可见指标名已对齐 USM「附加值率 / 技术壁垒 / 市场集中度」；用例册预期列仍写旧演示名「高价值环节占比 / 战略重要性评分 / 关键环节数」——脚本按可见表名断言；评审态「指标说明」aria-label 仍为旧名。
  2. 对象三级 aria-label 为「集群 / 产业」+ 细分可见文案（对应用例「产业 / 产业链 / 细分产业」）。
  3. 「注册项只读启用」落在 `aria-label`，正文区另有「只读确认：已注册项与演示权重」说明。
  4. 对象不全时「开始分析」disabled；切条件不自动起任务。
  5. 结果优先「诊断记录→查看结果」；现场诚实降级（高端化 —、关键环节数 0、暂无代表企业）。
  6. 用例「重新分析」现场 CTA=「按此配置新建分析」；升序/降序控件未见。
  7. 同路由隔离：本套 `entry_id=chain-key-link` only；cycle/bottleneck 仅隔离反向，不写兄弟正向。

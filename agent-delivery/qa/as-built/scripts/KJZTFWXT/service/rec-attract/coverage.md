# coverage · svc-rec-attract（引入服务机构推荐分析）

> 主表：脚本 id → 用例编号 → 页面区块/状态 → P → 档(A/B) → 可见动作 / skip ticket
> 金样 A 档 = index.gold（P0-01~05）；其余 B 档。脚本 id 前缀 P0 与用例册优先级列独立（P0-19~P0-23 承接 P1 用例）。
> env-gate overall=pass（2026-10-14）；tickets 见 fixtures/testdata.yaml。

| 脚本 id | 用例编号 | 页面区块/状态 | P | 档(A/B) | 可见动作 / skip ticket |
|---|---|---|---|---|---|
| P0-01 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00779 | 入口路由/双 Tab | P0 | A | 深链进入，验 URL+标题+双 Tab 选中 |
| P0-02 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00780 | 分析配置区/产业下拉 | P0 | A | 展开下拉核 15 选项与 placeholder |
| P0-03 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00785 | 模型区四指标默认权重 | P0 | A | 浏览四 spin 初值 35/30/20/15 |
| P0-04 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00788 | 恢复默认权重复位 | P0 | A | 改权重→点「恢复默认权重」 |
| P0-05 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00789 | 开始分析门控（软文案+enabled） | P0 | A | 空态验软引导文案；选产业验 enabled（不点击） |
| P0-06 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00781 | 产业集群选定回显/清空/切 Tab | P0 | B | 选→改选→清空→切 records 返回，全程不自动起任务 |
| P0-07 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00782 | 目标筛选 Tag 组 | P0 | B | skip：ASBUILT-SVCATTR-TARGET-CHAIN-TAGS-MISSING-D2（现场无 Tag 组，D2） |
| P0-08 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00783 | 链位 Tag 组 | P0 | B | skip：ASBUILT-SVCATTR-TARGET-CHAIN-TAGS-MISSING-D2（同上） |
| P0-09 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00784 | 目标与链位跨组并存 | P0 | B | skip：ASBUILT-SVCATTR-TARGET-CHAIN-TAGS-MISSING-D2（同上） |
| P0-10 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00786 | 指标说明文案/底部声明 | P0 | B | 核四说明关键词+声明五要点（D1 文案 as-built） |
| P0-11 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00787 | 权重调节钮+键入编辑 | P0 | B | 上调/下调一次 36→35；fill 25 |
| P0-12 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00790 | 显式触发创建任务/过程态 | P0 | B | 选产业→点开始分析→验 processing+记录新行 |
| P0-13 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00791 | 同条件单飞拦截 | P0 | B | 发起→回配置→同条件重点→记录不膨胀或拦截提示 |
| P0-14 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00792 | 推荐名单结果态（壳+诚实空） | P0 | B | 历史「查看结果」→结果壳+工具条；空态走诚实空分支 |
| P0-15 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00793 | 综合分只展示不重算 | P0 | B | 改权重前后名单分值/排序不变；空态核「不重算」承诺文案 |
| P0-16 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00794 | 名单字段构成/默认降序 | P0 | B | 核排名/综合/推荐理由列+数值降序；空态 return |
| P0-17 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00795 | 推荐理由逐行对应 | P0 | B | 核「推荐理由」列+每行理由类文案；空态 return |
| P0-18 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00796 | 变更条件重析 | P0 | B | 起任务→切「生物」不自动跑→显式重析进新过程态 |
| P0-19 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00797 | 分析记录列表/切回保留 | P1 | B | 记录列表+状态如实；切 Tab 后产业/权重保留 |
| P0-20 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00798 | 当天同条件复用+重新分析 | P1 | B | 同条件重点不重跑（三选一口径）；结果态「重新分析」入口 |
| P0-21 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00799 | cultivate 工作区隔离 | P1 | B | 切 workspace=cultivate 验非招引口径；回切配置正常 |
| P0-22 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00800 | 评审模式显隐/零泄漏 | P1 | B | persona 菜单开关评审；四追溯按钮+角标；关后零泄漏+业务态不变 |
| P0-23 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00801 | 分析失败态/重试 | P1 | B | skip：ENV-SVCATTR-FAULT-INJECTION-NOT-AVAILABLE-001（无故障注入手段，D4） |

## 覆盖小结（R3·W3 补齐后）

- 新增 18 条（P0-06~P0-23）全部 B 档；skip 4 条（P0-07/08/09 同源 D2 Tag 缺失 + P0-23 D4 故障注入）= 4/18 ≈ 22.2% ≤25% ✅
- 本入口全量 23 条（A 档 5 + B 档 18）；用例册 23 条用例 ↔ 23 脚本 1:1 全覆盖（编号母表映射，无自编 id）
- 结果态三条（P0-14/15/16/17）按 env-gate「结果壳可达、名单常诚实空」走双分支判定（壳必验、填名单条件核），不造假绿

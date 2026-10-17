# 服务机构技术力评估分析 脚本→用例 覆盖表（R3）

蓝本 = `qa/test-cases/KJZTFWXT/service-产业服务链分析/SVCCAP-服务机构技术力评估分析/FUNC-服务机构技术力评估分析-用例.md`
env-gate **overall=fail**（对比篮服务机构 <2，`ENV-SVCCAP-BASKET-ORG-LT2-001`）。

## 主表

| 脚本 id | 用例编号 | 页面区块/状态 | P | 档 | 可见动作 / skip ticket |
|---------|----------|---------------|---|----|------------------------|
| P0-01 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00671 | 入口·路由双 Tab | P0 | A | capability 深链 |
| P0-02 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00672 | 配置·五维模型 | P0 | A | 权重合计 100% |
| P0-03 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00676 | 门控·空态 disabled | P0 | A | **仅**断言「开始评估」disabled；不测放行 |
| P0-04 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00681 | 评审零泄漏 | P0 | A | 关评审无泄漏 |
| P0-05 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00673 | 配置·权重编辑与维度启停 | P0 | A | 调节钮/直改 30/停用/启用（不发起评估） |
| P0-06 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00674 | 诚实性·无本地重算 | P0 | A | 改 40 界面等值无重算；已完成结果只认后端签发、缺分不发明 |
| P0-07 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00675 | 对比篮三入口与带入 | P0 | B | 三入口文案（D2 分支互斥 as-built）+ 带入回显 + 重复幂等 + 移除仅作用本次；ticket=ASBUILT-SVCCAP-TRI-ENTRY-D2 |
| P0-08 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00677 | 结果呈现·同源开关与诚实空态 | P0 | A | chart-switch ranking 选中 + 雷达分支数据驱动 + 空态不伪造（canvas=0）+ 第二条任务交叉验证；ⓘ 评审开启态 aria-label 硬断；数据态同源证据（两视图同显/雷达维度轴）补测归 ENV-SVCCAP-NO-SCORE-RESULT |
| P0-09 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00678 | 过程态·门控壳+过程只读；发起/单飞/复用 manual | P1 | B | allow_skip+ticket=`ENV-SVCCAP-BASKET-ORG-LT2-001`；机检=空选 disabled+「查看过程」壳（无伪造%）；预期①②③发起链 manual（禁假绿） |
| P0-10 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00679 | 分析记录·列表/空态+打开结果+Tab 配置保留 | P1 | B | 零 allow_skip；机检=列表↔空态双分支 + 历史「查看结果」只读 + Tab 往返权重/对比对象保留（不发起）；D1 回切主 Tab 须 regex name |
| P0-11 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00680 | 评审开启·两追溯+指标说明角标+长提示 | P1 | B | 零 allow_skip；机检=开评审两枚追溯可点弹层 + ⓘ「指标说明：服务机构技术力维度分」+ pending 长提示（权重阈值待确认/只展示后端分）；不发起 |
| P0-12 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00682 | 配置·权重边界（非负/小数超界/和≠100） | P1 | B | 零 allow_skip；机检=−5→0、10.5→取整、101→100 + 35/25/20/20/10 合计偏离提示且不静默归一；不发起 |
| P0-13 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00683 | 配置·无可用维度（仅剩1/全停用） | P1 | B | 零 allow_skip；机检=仅剩1维/全停用 tip「至少启用 2 个评价维度」+start disabled + 恢复默认权重/对齐；不发起 |
| P0-14 | ZNFWJQ-KJZTFWXT-v1.0-FUNC-00684 | 异常·评估失败局部错误与重试 | P1 | B | allow_skip+ticket=`ENV-SVCCAP-BASKET-ORG-LT2-001`；机检=配置壳+五维默认权重+双 Tab；预期①②失败提示/重试 manual（禁假绿） |

过程/结果主路径 → B + `ENV-SVCCAP-BASKET-ORG-LT2-001`（待篮内 ≥2 升 A）。三入口 D2 已落 P0-07（2026-10-15：两入口仅空篮警示分支渲染 as-built，tier B 待父裁；ticket=ASBUILT-SVCCAP-TRI-ENTRY-D2）。
P0-08 结果呈现（2026-10-15）：只读已完成任务结果可机检（A）——同源=chart-switch 单选互斥（雷达 radio 数据驱动渲染，无分时缺位 + canvas=0 诚实空态，两条任务探针交叉验证）；数据态证据（排名/雷达同显、雷达维度轴=启用维度、分数旁 ⓘ 贴合）补测归 `ENV-SVCCAP-NO-SCORE-RESULT`。
P0-09 异步任务（2026-10-15 GAP）：B 档 allow_skip+`ENV-SVCCAP-BASKET-ORG-LT2-001`；机检仅门控+过程只读壳；发起/单飞/当天复用三条 manual（env-gate fail 禁假绿）；D1「计算中」→「进行中」。
P0-10 分析记录与配置保留（2026-10-15 GAP）：B 档零 allow_skip；不点「开始评估」；列表/「暂无分析记录」双分支 + 历史打开结果 + Tab 往返保留 cap_w/spin/对比对象；D1 回切主 Tab `exact:true` 失效改 regex。
P0-11 评审开启态（2026-10-15 GAP）：B 档零 allow_skip；不点「开始评估」；两追溯+ⓘ+pending 长提示机检；D1 长提示全文挂 `.perm-pending-badge`（ⓘ 弹卡为 MetricSpecCard 8 件套互证）。
P0-12 权重边界（2026-10-15 GAP）：B 档零 allow_skip；配置态钳制+合计提示机检；D1 用例「点开始评估」验发起拦截 → 篮<2 改以合计提示承预期③。
P0-13 无可用维度（2026-10-15 GAP）：B 档零 allow_skip；配置态 tip+disabled 机检；D1 文案「至少启用 2 个」/预期③ start 可用改 tip 消失+默认对齐（篮门控仍 disabled）。
P0-14 评估失败（2026-10-15 GAP）：B 档 allow_skip+`ENV-SVCCAP-BASKET-ORG-LT2-001`；机检仅配置壳；失败提示/重试两条 manual（开放项 2，禁假绿）；D4 环境债；D1 重试文案预注姊妹仓；篮≥2 后仿 sz P0-20 route.abort 升实跑。

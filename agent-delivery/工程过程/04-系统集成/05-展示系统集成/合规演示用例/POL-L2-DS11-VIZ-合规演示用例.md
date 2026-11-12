# POL-L2-DS11-VIZ · 政策分析报告可视化呈现 · 合规演示用例

- 规程：`agent-delivery/产品实现规程.md` §6.4
- 系统：科技信息展示系统 · 科技政策跟踪 · 政策分析评价
- 需规序号：219–222
- 需规全文：`agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/科技政策跟踪-系统详细设计说明书.md` §2
- 日期：2026-11-07
- 增补：2026-11-12 `POL-L2-DS11-VIZ-GAPFILL-L02-CASE`（`agent:qa-agent`）追加 Tab1 七可视化块行
- 调度核对：见文末

期望摘自 `测试用例/POL-L2-DS11-VIZ-TEST-L01.md`，不改那份实测。221 设计不设资源。七可视化块（DS11-VIZ，demo 复刻保留块，无 SRS 序号）期望摘自 `sdd/l2/POL-L2-DS11-VIZ-GAPFILL-L02.md` 灌数行与 `POL-L2-DS11-VIZ-GAPFILL-L02-DATA.md` §4，数字以灌数行为准。

历史集成测试记录保持原文件。这里只写基于现有数据选定的一组输入。

## 覆盖表

| 需规位置 | 界面 | 输入或选择 | 触发 | 接口地址 | 按界面值填好的请求 | 期望输出 | 数据情况 |
|---|---|---|---|---|---|---|---|
| 219 多维指标趋势图 | 政策分析评价 · 可视化 | 切换维「时间」，指标「科技政策连续出台数」 | 进入趋势图即请求，一次只带一种类 | POST /display/v1/policy/evaluation/jobs | {"kind":"趋势","switch":["时间"],"metric":["科技政策连续出台数"]} | 该指标 2021–2026 六点：48、62、75、83、79（波动）、91（重点）。对不上则空，不造曲线，不返回 501 | 可演 |
| 220 分区/群体对比分析图 | 政策分析评价 · 可视化 | 对象「行业」。不把「行业」当作 219 的切换维 | 另一次请求 | POST /display/v1/policy/evaluation/jobs | {"kind":"分区","subject":"行业"} | records 10 行（行业组）。再加投向「财政资金」为 5 行。对象用「时间」或投向对不上则空，不返回 501 | 可演 |
| 221 多维结构关联图 | 政策分析评价 · 可视化 | 不填。本叶不发政策接口 | 无 | 不设 /display/v1/policy 资源 | 不请求 | 只消费第 7 项已有子图。挂接空则弦线图、关系网、路径都空。不新开查图资源 | 设计无资源 |
| 222 报告模板定制与批量导出 | 政策分析评价 · 可视化 | 模板「区域政策效果季度对比」 | 打开该模板即 GET | GET /display/v1/policy/evaluation/shells | kind=模板选用&template=区域政策效果季度对比 | records 2 行：季度/地区/柱状，季度/地区/热力。不造 PDF/Excel，不返回 501。测试用例 TC-03a 已判红：shells 对「模板选用」落空列表（GAP-01），库内有行。循环不把这次空列表改写成通过 | 可演 |
| DS11-VIZ 评估指标体系卡 | 政策分析评价 · 可视化 | 不填筛选项。七块无用户选择条件，直读 | 打开 Tab1 即 GET | GET /display/v1/policy/evaluation/viz | block=metric | R.ok({records:[…]}) 5 行：覆盖广度 85（权重 20）、深度力度 78（25）、协同程度 72（20）、实施效果 68（25）、创新引领 82（10）。五维权重合计 100；行挂 pending_ref=QPOL-02（权重待甲方确认，QPOL-02 未关闭）→ 页面 ⓘ/⚠️ 待核验在位；不灌总分行（总分归页头 sim_score 卡）。列表进度条与五维雷达读同一批行。无行或接口失败则诚实空态，不补默认维度，不返回 501 | 可演（gapfill_policy_eval_viz_metric 5 行，is_mock=1） |
| DS11-VIZ 三联画像 | 政策分析评价 · 可视化 | 卡面任一类（政策/企业/人才）点「查看详情」开抽屉 | 打开 Tab1 即 GET；抽屉为前端开合 | GET /display/v1/policy/evaluation/viz | block=portrait | R.ok({records:[…]}) 3 行：政策卡「综合力度指数 86 分」、企业卡「匹配满意度 82 分」、人才卡「留用意愿指数 78 分」；portrait_type 闭集恰为 政策/企业/人才。抽屉详情读同一行：概述 + 指标组（政策行含「发布密度：128 项/季」等 4 组）+ 要点若干条，与表内原文一致。无行则三卡与抽屉全空，不编画像，不返回 501 | 可演（gapfill_policy_eval_viz_portrait 3 行，is_mock=1） |
| DS11-VIZ 地理分布图 | 政策分析评价 · 可视化 | 不填。城市气泡由行上经纬度落点 | 打开 Tab1 即 GET | GET /display/v1/policy/evaluation/viz | block=geo | R.ok({records:[…]}) 10 行（北京市 386 / 上海市 352 / 深圳市 325 / 广州市 298 / 杭州市 275 / 南京市 258 / 武汉市 228 / 成都市 242 / 西安市 195 / 苏州市 210），中国地图 + 城市气泡按行上 lng/lat 落点，气泡大小随 policy_count；tooltip 首行为地区名，附代表政策名（如北京市「AI产业规划、中关村创新政策」）。不灌「全国」兜底行、不灌 flows 连线。无行则保留「暂无地理分布数据」空态，不返回 501 | 可演（gapfill_policy_eval_viz_geo 10 行，is_mock=1） |
| DS11-VIZ 分地区落实率 | 政策分析评价 · 可视化 | 不填。表格按前端行为排序 | 打开 Tab1 即 GET | GET /display/v1/policy/evaluation/viz | block=region_impl | R.ok({records:[…]}) 8 行：深圳市 91/94/96/4、北京市 88/92/95/6、上海市 85/90/93/8、杭州市 84/87/91/9、广州市 82/86/90/10、成都市 81/84/89/11、南京市 79/82/88/12、武汉市 76/80/85/14（落实率/资金到位/申报完成/延期项数）。落实率进度条带色阶；延期项 >10 红标（南京市 12、武汉市 14）为前端行为。无行则空表，不补默认地区，不返回 501 | 可演（gapfill_policy_eval_viz_region_impl 8 行，is_mock=1） |
| DS11-VIZ 话题热力图 | 政策分析评价 · 可视化 | 不填。行集组装满矩阵 | 打开 Tab1 即 GET | GET /display/v1/policy/evaluation/viz | block=topic_heat | R.ok({records:[…]}) 96 行：8 话题（人工智能/生物医药/新能源/半导体/量子科技/先进材料/航空航天/海洋科技）× 12 个月（2025-06 至 2026-05）满矩阵，如人工智能 2025-11=98、2026-04=92；热力格 visualMap 色阶随行值域动态。缺格不补 0（本批为满矩阵 8×12）。无行则空态，不返回 501 | 可演（gapfill_policy_eval_viz_topic_heat 96 行，is_mock=1） |
| DS11-VIZ 情感分布 | 政策分析评价 · 可视化 | 不填。环形读总体行，堆叠柱读分话题行 | 打开 Tab1 即 GET | GET /display/v1/policy/evaluation/viz | block=topic_sentiment | R.ok({records:[…]}) 6 行：总体 1 行（正面 58 / 中性 27 / 负面 15，合计 100；sample_size=12840 为占比口径留证）+ 分话题 5 行（人工智能 72/18/10、生物医药 61/28/11、新能源 55/30/15、半导体 48/32/20、量子科技 64/26/10，三列合计均 100）。环形图读总体行，堆叠柱读 5 条分话题行；三分类闭集外的行丢弃（前端行为）。无行则两图空态，不返回 501 | 可演（gapfill_policy_eval_viz_topic_sentiment 6 行，is_mock=1） |
| DS11-VIZ 产业影响力气泡图 | 政策分析评价 · 可视化 | 不填。图例=行上 category 去重 | 打开 Tab1 即 GET | GET /display/v1/policy/evaluation/viz | block=bubble | R.ok({records:[…]}) 8 行：AI产业 95/92/500/35、生物医药 88/85/420/28、半导体 90/88/450/22、新能源 82/80/380/25、量子科技 75/70/280/45、先进材料 72/68/250/18、航空航天 78/75/320/20、海洋科技 68/65/200/30（影响力 x 轴/关注度 y 轴/资金亿元=气泡大小/增长率%）。图例恰为 科技/产业/前沿 三类去重。无行则不画图，不返回 501 | 可演（gapfill_policy_eval_viz_bubble 8 行，is_mock=1） |

## 一条主路径

按下面顺序走可演的行。条件不另做排列组合。

1. 序号 219：切换维「时间」、指标「科技政策连续出台数」。请求 `{"kind":"趋势","switch":["时间"],"metric":["科技政策连续出台数"]}`。应看到 2021–2026 六点 48、62、75、83、79（波动）、91（重点）。
2. 序号 220：对象「行业」。请求 `{"kind":"分区","subject":"行业"}`。应看到 10 行。
3. 序号 222：模板「区域政策效果季度对比」。请求 `GET .../shells?kind=模板选用&template=区域政策效果季度对比`。应看到 2 行。GAP-01 未修好时空列表仍判不通过。
4. DS11-VIZ 七可视化块（Tab1 分析报告可视化，进入页面即各自请求 `GET /display/v1/policy/evaluation/viz`，block 分别为 metric / portrait / geo / region_impl / topic_heat / topic_sentiment / bubble，七次请求互不混读）：
   - metric：进度条列表 + 五维雷达，5 行（覆盖广度 85/权重 20、深度力度 78/25、协同程度 72/20、实施效果 68/25、创新引领 82/10），权重合计 100，ⓘ/⚠️ QPOL-02 待核验在位。
   - portrait：三卡 + 抽屉详情，政策（综合力度指数 86 分）/企业（匹配满意度 82 分）/人才（留用意愿指数 78 分）各一行，抽屉读同一行原文。
   - geo：中国地图 + 城市气泡 10 个（北京市 386 为最大），tooltip 附代表政策名。
   - region_impl：四率表 8 行，深圳市 91/94/96/4 最高，南京市 12、武汉市 14 延期项红标。
   - topic_heat：热力格满矩阵 8 话题 × 12 月（2025-06 至 2026-05）= 96 行，人工智能 2025-11 峰值 98。
   - topic_sentiment：环形 1 行（58/27/15，样本量 12840）+ 堆叠柱 5 行（人工智能 72/18/10 等）。
   - bubble：八气泡四元组（AI产业 95/92/500/35 影响力、关注度、资金三轴最高；增长率最高为量子科技 45），图例 科技/产业/前沿。
   - 七块每块统计数字/图表旁 🧪 MockBadge 与 ⓘ 在位（is_mock=1，D4 仍是 mock）；任一块无行或接口失败只置本块空态，不清其它块已渲染内容。

## 调度核对

需规每一条都有一行。`可演` 的行可以进入循环。`设计无资源` 的行不派数据单，也不新开接口。

- 七可视化块不在需规 219–222 十三叶原文（demo 复刻保留块，走查档 A），每块各占一行、均 `可演`，不受「需规每一条都有一行」的空行退回约束；数据已由 `POL-L2-DS11-VIZ-GAPFILL-L02` 灌入（2026-11-12 --apply 成功，七表 136 行），期望句与库内行逐字对得上，循环可只读核对。
- 循环打点：只打 `GET /display/v1/policy/evaluation/viz?block=<key>` 七键 + 库内只读 SELECT（库 `gkxlumenx_gapfill`，先例同 TEST-L01 DP 章：密码经环境变量注入，不打印不落文）。循环不写库、不重新灌数。
- 环境口径沿用既有 `POL-L2-DS11-VIZ-LOOP计划.md`：探测域名 `https://edu.itic-sci.com/tid/api/display/**`，token 文件 `%USERPROFILE%\.gkx\display-loop-token`，请求头 `Authorization: Bearer` + `systemCode: display`；七块样本即覆盖表七行 GET（block=metric/portrait/geo/region_impl/topic_heat/topic_sentiment/bubble）。
- 验收单：沿用既有 `POL-L2-DS11-VIZ-DEMO-ACCEPT-LOOP`（`ready`，报告 `agent-handoffs/科技政策跟踪-POL/POL-L2-DS11-VIZ-DEMO-ACCEPT-LOOP.md`），七块可演行并入该循环行集，不另建验收单。
- 灌数幂等：脚本 `--apply` 不整表删除、可重复执行，重跑行数不变（5/3/10/8/96/6/8，合计 136）；演示环境若清批次（DELETE `gapfill_batch_id='POL-L2-DS11-VIZ-GAPFILL-L02'` 或 TRUNCATE 七表），七块回到 FIX-03 诚实空态，属空态验收分支（见下），重灌后自动恢复可演。
- 依赖提示：`/display/v1/policy/evaluation/viz` 端点由 `POL-L2-DS11-VIZ-GAPFILL-L02-BE`（element `@Inner /evaluation/viz` + display `block` 分发）与 `-FE`（七块真轨接线）落地；未上线时接口不可达，七块行不参与已演示计数，判「未演」不判「通过」。

### 七块空态验收分支（数据不在场时的诚实空态）

演示环境 DB 可清批次的场景。前置：七表无行（或端点未上线/接口失败）。步骤：打开 Tab1，逐块观察。预期（逐块）：

| 块 | 空态预期 |
|---|---|
| metric | 列表与雷达均空态提示，不补默认五维、不造权重 |
| portrait | 三卡区域空态，抽屉不可开或开即空，不编画像 |
| geo | 保留「暂无地理分布数据」二段空态，无气泡落点、不造「全国」兜底 |
| region_impl | 空表（表头在、无数据行），不补默认地区 |
| topic_heat | 空态提示，无热力格、不造满矩阵 |
| topic_sentiment | 环形与堆叠柱均空态，不造占比 |
| bubble | 不画图（行 <2 不画为前端行为，0 行必空态），不造气泡 |

通用断言：全部 HTTP 200、`records` 空列表——不返回 501、不返回写死 mock、不把空态渲染成假数据；任一块失败不清空其它块已渲染内容；Network 无 `@/mock` 或 demo fixture 填数（`USE_MOCK=false` 真轨）。重灌批次后七块恢复上表可演期望。

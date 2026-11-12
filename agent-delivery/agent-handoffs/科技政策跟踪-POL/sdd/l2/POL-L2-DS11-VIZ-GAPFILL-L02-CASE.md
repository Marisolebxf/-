# POL-L2-DS11-VIZ-GAPFILL-L02-CASE · Tab1 七可视化块合规演示用例补行

- 任务：`POL-L2-DS11-VIZ-GAPFILL-L02-CASE`
- 日期：2026-11-12
- 执行：`agent:qa-agent`（子会话）· 监管：`human:淮政玮`
- ponytail: full
- 状态：产物停本地工作区，不 commit / 不 push；registry 状态推进与提交由主会话收口（本会话不碰 task-registry MCP）
- 用例真源（本次修订对象）：`agent-delivery/工程过程/04-系统集成/05-展示系统集成/合规演示用例/POL-L2-DS11-VIZ-合规演示用例.md`
- 数据事实：`sdd/l2/POL-L2-DS11-VIZ-GAPFILL-L02.md`（灌数 handoff，--apply 已成功）+ `sdd/l2/POL-L2-DS11-VIZ-GAPFILL-L02-DATA.md` §4（列清单）+ `repos/lumen-algo-py/scripts/mysql/gapfill_policy_eval_viz2.sql`（as-built 行内容，逐行核对用）
- 契约真源：`sdd/2026-11-12-BE-viz读面侦察笔记.md` §3（`GET /display/v1/policy/evaluation/viz?block=<key>`，R.ok + records，恒 200 空态惯例）+ `sdd/2026-11-12-FE-viz接线说明书.md`（七块组件与空态行为）

## 1. 范围与实现

只改一份文档：`POL-L2-DS11-VIZ-合规演示用例.md`。四处改动：

| # | 位置 | 改动 |
|---|---|---|
| 1 | 头部 | 加「增补：2026-11-12 `POL-L2-DS11-VIZ-GAPFILL-L02-CASE`」行 + 一句七块期望出处说明（灌数 handoff + DATA §4，数字以灌数行为准） |
| 2 | 覆盖表 | 追加 7 行（每块一行），列结构与既有 4 行完全一致（需规位置/界面/输入或选择/触发/接口地址/按界面值填好的请求/期望输出/数据情况） |
| 3 | 一条主路径 | 追加第 4 步「DS11-VIZ 七可视化块」+ 7 个子条目（每块一句图表形态 + 关键行事实）+ 角标/失败隔离断言 |
| 4 | 调度核对 | 追加 4 条核对项（七块定位与可演性、循环打点、环境与验收单口径沿用既有 LOOP 计划、灌数幂等与依赖提示）+ 新增小节「七块空态验收分支」（逐块空态预期表 + 通用断言） |

既有 219/220/221/222 四行与其余章节未动。用例行格式（含「不返回 501 / 不造曲线 / 空态诚实」句式、数据情况列「可演（表名 N 行，is_mock=1）」写法）与既有文档完全一致。

## 2. 覆盖表新增 7 行摘要

| 块 | block 键 | 期望核心 | 数据情况 |
|---|---|---|---|
| DS11-VIZ 评估指标体系卡 | metric | records 5 行；五维分值/权重逐行列出；权重合计 100；pending_ref=QPOL-02 → ⓘ/⚠️ 待核验；不灌总分行（归页头 sim_score 卡） | 可演（gapfill_policy_eval_viz_metric 5 行，is_mock=1） |
| DS11-VIZ 三联画像 | portrait | records 3 行；三类 KPI（综合力度指数 86 / 匹配满意度 82 / 留用意愿指数 78 分）；抽屉与卡读同一行原文 | 可演（…_portrait 3 行，is_mock=1） |
| DS11-VIZ 地理分布图 | geo | records 10 行（北京市 386 … 苏州市 210 全名单）；经纬度落点、气泡大小随 policy_count；不灌「全国」兜底与 flows | 可演（…_geo 10 行，is_mock=1） |
| DS11-VIZ 分地区落实率 | region_impl | records 8 行（四率一延期逐城列出）；>10 红标（南京 12、武汉 14）为前端行为 | 可演（…_region_impl 8 行，is_mock=1） |
| DS11-VIZ 话题热力图 | topic_heat | records 96 行 = 8 话题 × 12 月（2025-06 至 2026-05）满矩阵；缺格不补 0 | 可演（…_topic_heat 96 行，is_mock=1） |
| DS11-VIZ 情感分布 | topic_sentiment | records 6 行 = 总体 1（58/27/15，sample_size=12840）+ 分话题 5（三列合计均 100） | 可演（…_topic_sentiment 6 行，is_mock=1） |
| DS11-VIZ 产业影响力气泡图 | bubble | records 8 行四元组 + 图例 科技/产业/前沿 三类去重 | 可演（…_bubble 8 行，is_mock=1） |

合计 7 行新增，全 `可演`。

## 3. 期望句与灌数行一致性核对表

期望句里每个数字均对照 `gapfill_policy_eval_viz2.sql` as-built INSERT 逐字核对（非凭 DATA/种子转抄）：

| 期望句事实 | 灌数行（SQL as-built） | 一致 |
|---|---|---|
| metric 5 行：覆盖广度 85/20、深度力度 78/25、协同程度 72/20、实施效果 68/25、创新引领 82/10 | 5 条 INSERT (dim_label, score_value, weight_pct) 与之逐字同；权重 20+25+20+25+10=100 ✅ | ✅ |
| metric 全行 pending_ref='QPOL-02' | 5/5 行 pending_ref='QPOL-02' | ✅ |
| metric 不灌总分行 | 表无总分行（灌数 handoff §2「不灌总分行」+ SQL 仅 5 条维度行） | ✅ |
| portrait 3 行 KPI：政策 86 / 企业 82 / 人才 78（单位「分」） | 政策行 kpi=「综合力度指数」86 分、企业行「匹配满意度」82 分、人才行「留用意愿指数」78 分 | ✅ |
| portrait_type 闭集恰为 政策/企业/人才 | 3 行分别为 政策/企业/人才，UNIQUE(portrait_type) | ✅ |
| 政策抽屉含「发布密度：128 项/季」等 4 组 | detail_metrics_text=「发布密度：128 项/季；平均资助强度：3200 万元；跨部门协同率：68%；免申即享占比：24%」恰 4 组 | ✅ |
| geo 10 行名单与 policy_count：北京 386/上海 352/深圳 325/广州 298/杭州 275/南京 258/武汉 228/成都 242/西安 195/苏州 210 | 10 条 INSERT 逐一同 | ✅ |
| 北京市 tooltip 代表政策「AI产业规划、中关村创新政策」 | sample_policies_text=「AI产业规划、中关村创新政策」 | ✅ |
| region_impl 8 行四率：深圳 91/94/96/4、北京 88/92/95/6、上海 85/90/93/8、杭州 84/87/91/9、广州 82/86/90/10、成都 81/84/89/11、南京 79/82/88/12、武汉 76/80/85/14 | 8 条 INSERT 逐一同；>10 红标：南京 12、武汉 14 恰两行（广州 10 不标） | ✅ |
| topic_heat 96 行 = 8 话题 × 12 月满矩阵，月份 2025-06 至 2026-05 | 8 话题（人工智能/生物医药/新能源/半导体/量子科技/先进材料/航空航天/海洋科技）× 12 月各 12 条 = 96 条 INSERT；8×12=96 ✅ | ✅ |
| 人工智能 2025-11=98、2026-04=92（热力峰值示例） | (人工智能,2025-11,98)、(人工智能,2026-04,92) | ✅ |
| sentiment 总体 1 行 58/27/15、sample_size=12840 | 总体行 (58,27,15,12840)；58+27+15=100 ✅ | ✅ |
| sentiment 分话题 5 行：人工智能 72/18/10、生物医药 61/28/11、新能源 55/30/15、半导体 48/32/20、量子科技 64/26/10 | 5 条 INSERT 逐一同；各行三列合计均 100 ✅；分话题 sample_size 均 NULL（FE 未消费，期望句未引用） | ✅ |
| bubble 8 行四元组：AI产业 95/92/500/35、生物医药 88/85/420/28、半导体 90/88/450/22、新能源 82/80/380/25、量子科技 75/70/280/45、先进材料 72/68/250/18、航空航天 78/75/320/20、海洋科技 68/65/200/30 | 8 条 INSERT 逐一同 | ✅ |
| 图例恰为 科技/产业/前沿 | category 去重恰 {科技,产业,前沿}（科技×3、产业×3、前沿×2），与 FE 色板三键对齐 | ✅ |
| 七表行数 5/3/10/8/96/6/8、合计 136、is_mock=1、metric_id NULL、批次 POL-L2-DS11-VIZ-GAPFILL-L02 | 灌数 handoff §4 --apply JSON + 独立 SELECT 复核一致 | ✅ |

核对结论：**16/16 全对上，零编造数字**。空态分支期望句（「暂无地理分布数据」二段空态、行 <2 不画等）引用 FE 接线说明书 §2 既有前端行为，不涉灌数行。

## 4. 调度 / 环境口径对齐（与既有文档核对）

| 项 | 既有口径（真源） | 用例文档写法 | 一致 |
|---|---|---|---|
| 用例落盘位置 | 规程 §6.4 + 测试用例 README：`工程过程/04-系统集成/05-展示系统集成/合规演示用例/{模块}-合规演示用例.md` | 即本次修订文件 | ✅ |
| 探测域名 / token | `编排计划/POL-L2-DS11-VIZ-LOOP计划.md` §3：`https://edu.itic-sci.com/tid/api/display/**`、token 文件 `%USERPROFILE%\.gkx\display-loop-token`、头 `Authorization: Bearer` + `systemCode: display` | 调度核对第 3 条照抄同口径，并注明七块样本 = 七行 GET | ✅ |
| 验收单 | 同计划 §2：`POL-L2-DS11-VIZ-DEMO-ACCEPT-LOOP`（`tech_task`/`qa-agent`，不签 done） | 沿用该验收单，七块可演行并入，不另建 | ✅ |
| 灌数幂等 | 灌数 handoff §4：`--apply` 不整表删除、可重复执行 | 调度核对第 4 条：重跑行数不变（5/3/10/8/96/6/8=136）；清批次场景转空态分支，重灌自动恢复 | ✅ |
| 空态契约 | BE 侦察笔记 §3：恒 `R.ok(records:[])`，不抛 501/404；TEST-L01 §0：期望未发生必红 | 七行期望输出与空态分支通用断言同句式 | ✅ |
| 依赖 | `-BE`/`-FE` 未上线则端点不可达 | 调度核对第 5 条：判「未演」不判「通过」 | ✅ |

## 5. 文件清单

| 文件 | 改动 |
|---|---|
| `agent-delivery/工程过程/04-系统集成/05-展示系统集成/合规演示用例/POL-L2-DS11-VIZ-合规演示用例.md` | 头部增补 + 覆盖表 +7 行 + 主路径第 4 步（7 子条）+ 调度核对 5 条 + 空态验收分支小节（逐块表 + 通用断言） |
| `agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/l2/POL-L2-DS11-VIZ-GAPFILL-L02-CASE.md` | 本 handoff（新增） |

只读引用（未改）：`sdd/l2/POL-L2-DS11-VIZ-GAPFILL-L02.md`、`sdd/l2/POL-L2-DS11-VIZ-GAPFILL-L02-DATA.md`、`repos/lumen-algo-py/scripts/mysql/gapfill_policy_eval_viz2.sql`、`sdd/2026-11-12-BE-viz读面侦察笔记.md`、`sdd/2026-11-12-FE-viz接线说明书.md`、`编排计划/POL-L2-DS11-VIZ-LOOP计划.md`。

## 6. 架构合规自检

| 铁律 | 结果 |
|---|---|
| D9 诚实性：不伪闭合 | ✅ 期望句全部来自灌数行事实；QPOL-02 待核验、is_mock=1、D4 仍 mock 均如实标注；端点未上线判「未演」不判「通过」 |
| D16/D18：gapfill 行经接口读、接口不返写死 mock | ✅ 用例断言「不返回写死 mock / 不造曲线 / 空态诚实」 |
| 用例与实测分离（测试用例 README §「另见」） | ✅ 未改 `测试用例/POL-L2-DS11-VIZ-TEST-L01.md`，未把 GAP-01 空列表改写为通过 |
| 不碰 task-registry MCP、不 commit/push | ✅ 产物停本地，主会话收口 |

## 7. 遗留与提示（给主会话/循环执行人）

1. `/viz` 端点由 `POL-L2-DS11-VIZ-GAPFILL-L02-BE`（element `@Inner /evaluation/viz` + display `block` 七键分发）与 `-FE`（七块真轨接线）落地后才可实跑；未上线期间七块行不参与已演示计数。
2. BE 交付时需把 viz 端点补进 `sdd/l2/POL-L2-DS11-VIZ-API.md`（FE 接线说明书 §4.1 已登记该缺口）；用例文档不预写 API 分册内容。
3. 循环执行时若七表被清批次，按用例文档「七块空态验收分支」验收；重灌 `POL-L2-DS11-VIZ-GAPFILL-L02` 批次后恢复可演。

## 8. cost（占位）

完工总控回填。

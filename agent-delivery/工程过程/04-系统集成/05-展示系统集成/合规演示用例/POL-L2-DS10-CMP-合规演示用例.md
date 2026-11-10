# POL-L2-DS10-CMP · 政策重点比对 · 合规演示用例

- 规程：`agent-delivery/产品实现规程.md` §6.4
- 系统：科技信息展示系统 · 科技政策跟踪 · 科创政策全景
- 需规序号：213–218
- 需规全文：`agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/科技政策跟踪-系统详细设计说明书.md` §2
- 日期：2026-11-08（2026-11-10 期望重冻结：215 部门行/头条、216 时点、217 报告文案；见 `POL-L2-DS10-CMP-DEMO-FIX-R20261110-DATA`）
- 调度核对：见文末

查库时间：2026-11-10 16:0x（读面时间，取自展示接口只读对照；首轮冻结 2026-11-07 16:01:36，2026-11-10 并行灌数批次 `BTN-panorama`、`mock_20260623` 合法覆盖后重冻结）。主机 `10.50.11.76`，用户 `gkxlumenx`（取自 `lumen-algo-py/scripts/seed/seed_synth_elem.py`）。口令未写入本文件。

**对标双方（216 / 217 / 218 固定）**：`北京市` ↔ `广东省`。本用例只认这一对；范围固定「国内先进地区」。不要用广东/山东或其他省组合当主路径——`gapfill_policy_benchmark_report` 可演样本按北京/广东灌，换对象会对不上行或只出单侧。报告表「对标对象」列是**该行视角主体**；另一侧是对照方（文案里的「两地 / 对方」即指这一对里的另一方）。

展示读面（代码）：`gkxlumen-display` 的全景 `stats` / `version-diff` / `benchmark-report` / `{id}/detail` 委托 `gkxlumen-element`；`stats` 的头条再委托专题指标。element 缺项库 `gkxlumenx_gapfill`，ADS 库 `demo_gkxlumenx_ads`，正文库 `demo_gkxlumenx_dwd`。本次只读这些库。

| 库.表 | 用途 |
|---|---|
| `gkxlumenx_gapfill.gapfill_policy_version_diff` | 213 |
| `gkxlumenx_gapfill.gapfill_policy_detail_compare` | 214 申报条件、申报材料 |
| `demo_gkxlumenx_dwd.policy_base_info` | 213/214 正文：标题、发布时间、发布机构、政策类型 |
| `demo_gkxlumenx_ads.policy_intensity` | 214/218 力度；216 省级对标对象 |
| `gkxlumenx_gapfill.gapfill_policy_impl_dept` | 215 实施部门 |
| `demo_gkxlumenx_ads.policy_level_dist` | 215 头条 `M_POLICY_TOTAL_COUNT` |
| `demo_gkxlumenx_ads.policy_metric_timeseries` | 216 `M_POLICY_SUPPORT_STRENGTH` |
| `gkxlumenx_gapfill.gapfill_policy_benchmark_report` | 217 |

缺项四表 `is_mock=1`。D4 仍是 mock。有行即写可演。217 只读全景 `benchmark-report`。研报 `POST /display/v1/policy/report/jobs` 不在本叶。

历史集成测试记录保持原文件。这里只写基于现有数据选定的一组输入。

## 覆盖表

| 需规位置 | 界面 | 输入或选择 | 触发 | 接口地址 | 按界面值填好的请求 | 期望输出 | 数据情况 |
|---|---|---|---|---|---|---|---|
| 213 政策新旧对比 | 科创政策全景 · 政策新旧对比 | 政策 `18363390`（标题「广东省科学技术厅关于印发《贯彻落实〈科技部办公厅关于营造更好环境支持科技型中小企业研发的通知〉的工作方案》的通知」）；旧时点 `2022-04-06`；新时点 `2022-06-15` | 两个时点都选定后点「查询对比」 | `GET /display/v1/policy/panorama/version-diff` | `policy_id=18363390&publish_date_a=2022-04-06&publish_date_b=2022-06-15` | records 3 行，日期对为 `2022-04-06` / `2022-06-15`。新增：「相对另一发布日，增补了研发环境支持的说明。缺项演示。」修改：「相对另一发布日，支持对象的表述有修改。缺项演示。」删除：「相对另一发布日，删去了一处过渡安排。缺项演示。」出处 `gapfill_policy_version_diff.summary_text`。对不上则 records 空 | 可演 |
| 214 政策详情对比 | 科创政策全景 · 政策详情对比 | 政策 `18363390` 与 `18407696`（标题「深圳市科技创新委员会（深圳市外国专家局）关于发布2022年度深圳市外国人来华工作许可工资收入计算标准的通知」）；维度含申报条件、申报材料 | 至少两项后点「开始对比」 | `GET /display/v1/policy/panorama/{id}/detail` | `GET /display/v1/policy/panorama/18363390/detail?dimensions=申报条件,申报材料`；`GET /display/v1/policy/panorama/18407696/detail?dimensions=申报条件,申报材料` | `18363390`：申报时间 `2022-04-06`，受理部门「广东省科学技术厅」，申报条件「注册地在广东省，且属于科技型中小企业。缺项演示，不是正式申报口径。」申报材料「营业执照、研发投入说明。缺项演示，不是正式材料清单。」`18407696`：申报时间 `2022-06-15`，受理部门「深圳市科技创新委员会」，申报条件「用人单位在深圳市，且为外国人来华工作许可申请单位。缺项演示，不是正式申报口径。」申报材料「单位证明、收入计算说明。缺项演示，不是正式材料清单。」两策 `policy_type` 为 NULL，产业类别空。力度分不在这次 GET：`policy_intensity.intensity_score` 当前均为 `20.0000000000`。点「计算支持力度」会先 `intensity.run()` 再读，本用例未提交该请求 | 可演 |
| 215 部门政策对比 | 科创政策全景 · 部门政策对比 | 读取后选「北京市科学技术委员会」（北京市）与「广东省科学技术厅」（广东省），跨区域 | 点「读取部门数据（stats 同步读）」 | `GET /display/v1/policy/panorama/stats` | `kind=all` | `impl_depts.records` **14 行**（2026-11-10 重冻结；BTN-panorama 批次扩充）。北京市科学技术委员会：项目类别件数 2，清单两行「三城一区科技创新成果科普传播」「科技监督检查」；技术类别件数 1，清单「三城一区科技创新成果科普传播」。广东省科学技术厅：项目类别件数 2，清单两行「科技型中小企业研发环境支持」「外国人来华工作许可收入标准」；技术类别件数 1，清单「科技型中小企业研发环境支持」。另有上海市科学技术委员会项目类别件数 1（清单「科技型中小企业研发环境支持」）；深圳市科技创新委员会技术类别件数 1（清单「外国人来华工作许可收入标准」）；北京市人民政府项目/技术各 1（清单「北京市人民政府关于印发《北京市关于加快新型储能产业高质量发展的若干措施》的通知」）；深圳市福田区人民政府、深圳市南山区人民政府（广东省）各项目/技术 1（清单分别为《福田区支持网络与通信产业科创平台建设实施细则》《南山区促进合成生物科技成果转化应用指南》印发通知）；苏州市人民政府（江苏省）项目/技术各 1（清单《苏州市新材料产业知识产权强基行动方案》印发通知）。出处 `gapfill_policy_impl_dept` 的 `region_name`、`impl_dept`、`aspect`、`item_count`、`list_title`。头条 `M_POLICY_TOTAL_COUNT` 为 **20184**（2026-11-10 重冻结），出处 `demo_gkxlumenx_ads.policy_level_dist.policy_count`。部门件数用 `item_count`，不用 20184 | 可演 |
| 216 标杆比对功能 | 科创政策全景 · 标杆比对 | **对标双方「北京市」↔「广东省」**；范围「国内先进地区」；字段「支持力度」 | 按这三项填好后请求 stats。页面按钮「读取对标数据」当前只发 `kind=all` | `GET /display/v1/policy/panorama/stats` | `kind=all&benchmark_scope=国内先进地区&benchmark_object=北京市&benchmark_object=广东省&compare_field=支持力度` | `benchmark_objects` 含北京市 `scope_code=110000`、广东省 `scope_code=440000`（省级共 31 行）。`support_strength`：`region_code` `110000` 与 `440000`，`stat_date` **`2026-11-10`**（2026-11-10 重冻结；mock_20260623 批次重跑，值不变），`metric_value` 均为 `58.0000000000`，`dim_key`「支持力度」。出处 `policy_intensity.scope_name` / `scope_code`，`policy_metric_timeseries.metric_value`（`metric_id=M_POLICY_SUPPORT_STRENGTH`）。范围「全球科创领先城市」对象为空，本路径不选。只发 `kind=all` 时力度块为空 | 可演 |
| 217 对标报告生成与导出 | 科创政策全景 · 对标报告 | **对标双方「北京市」↔「广东省」**（谁对谁：北京对广东；报告两行各以一方为视角）；字段「支持力度」 | 点「生成报告」；有行后再点「导出（当次行）」 | `GET /display/v1/policy/panorama/benchmark-report` | `benchmark_object=北京市&benchmark_object=广东省&compare_field=支持力度` | records **2 行**（北京一行 + 广东一行，缺任一侧则本行失败）。2026-11-10 重冻结（BTN-panorama 批次重写文案，行结构/对象/字段不变）。北京市视角：差异「北京市与对照地区的支持力度不一样。」优劣「北京市的支持力度一边更集中，一边覆盖更稳。」建议「可借鉴对照地区把支持力度写清楚的做法。」正文「北京市《北京市人民政府关于印发《北京市关于加快新型储能产业高质量发展的若干措施》的通知》在支持力度上与对照地区不同，可借鉴对方把同类措施写清楚的做法。」。广东省视角：差异「广东省与对照地区的支持力度不一样。」优劣「广东省的支持力度一边更集中，一边覆盖更稳。」建议「可借鉴对照地区把支持力度写清楚的做法。」正文「广东省《深圳市福田区人民政府关于印发《福田区支持网络与通信产业科创平台建设实施细则》的通知》在支持力度上与对照地区不同，可借鉴对方把同类措施写清楚的做法。」。出处 `gapfill_policy_benchmark_report` 的 `difference_text`、`pros_cons_text`、`suggestion_text`、`report_body`。导出串接当次行原文，不产 PDF/Word 字节 | 可演 |
| 218 对标结果可视化展示 | 科创政策全景 · 对标结果可视化 | **对标双方「北京市」↔「广东省」**；地区视角；图种雷达、柱状或热力任选其一 | 点「生成可视化」 | `POST /display/v1/policy/panorama/jobs` | `{"sub_type":"policy_intensity","params":{"scope_type":"province","policy_ids":["北京市","广东省"]}}`（`analysis_fp` 由前端按对象集现算，本用例不冻结哈希） | 省级行：北京市 `intensity_index` `864.1800000000`，`industry_coverage` `27.8800000000`，`rank_no` 2；广东省 `intensity_index` `741.5100000000`，`industry_coverage` `35.7700000000`，`rank_no` 3。两行 `intensity_score` 为空。`metric_id` 为 `M_POLICY_INTENSITY_INDEX/M_POLICY_INDUSTRY_COVERAGE`。出处 `demo_gkxlumenx_ads.policy_intensity`。该 POST 会先 `intensity.run()` 再读。本用例填写时未提交，期望是 2026-11-07 16:01:36 的表内现数 | 可演 |

## 一条主路径

按下面顺序走可演的行。条件不另做排列组合。214 的「计算支持力度」和 218 的「生成可视化」都会先写表再读。本路径把表内现数写进期望，填写时没有提交这两次写请求。

1. 序号 215：打开「部门政策对比」，点「读取部门数据（stats 同步读）」。请求 `GET /display/v1/policy/panorama/stats?kind=all`。应看到 **14 行**实施部门（2026-11-10 重冻结），其中北京市科学技术委员会与广东省科学技术厅的件数和清单与覆盖表一致。头条政策总数 **20184**。
2. 序号 216：打开标杆比对，范围选「国内先进地区」，**对标双方只选「北京市」「广东省」**（不要选山东等其它省），字段勾「支持力度」。请求带上 `benchmark_scope`、两个 `benchmark_object` 和 `compare_field=支持力度`。应看到省级对象码 `110000`、`440000`，支持力度 `58.0000000000`（`2026-11-10`）。
3. 序号 217：仍用北京↔广东 + 支持力度，点「生成报告」。请求 `GET /display/v1/policy/panorama/benchmark-report`。应看到 **北京市、广东省各一行**（共 2 行）；「对照地区 / 对方」分别指这一对里的另一侧。四句原文与覆盖表一致（2026-11-10 重冻结文案）。再点「导出（当次行）」，文件内容来自这两行。
4. 序号 218：仍用北京↔广东，视角保持「地区」。表内现数为北京市力度指数 `864.1800000000`、产业覆盖 `27.8800000000`、排名 2，广东省力度指数 `741.5100000000`、产业覆盖 `35.7700000000`、排名 3。点「生成可视化」才会提交 `policy_intensity`；填写本用例时未点。
5. 序号 213：打开政策 `18363390` 的新旧对比，时点 `2022-04-06` 与 `2022-06-15`，点「查询对比」。应看到新增、修改、删除三句摘要。
6. 序号 214：详情对比选择 `18363390` 与 `18407696`，点「开始对比」。应看到两个申报时间、两个受理部门、两段申报条件和两段申报材料。产业类别为空。不点「计算支持力度」。

## 调度核对

需规 213–218 各有一行。可演 6 行，覆盖不到 0 行。主路径只串这 6 行。不建本二级的演示样本循环，不派数据单，不派算法单。

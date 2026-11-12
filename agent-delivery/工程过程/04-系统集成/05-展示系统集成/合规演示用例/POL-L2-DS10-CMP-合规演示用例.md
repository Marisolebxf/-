# POL-L2-DS10-CMP · 政策重点比对 · 合规演示用例

- 规程：`agent-delivery/产品实现规程.md` §6.4
- 系统：科技信息展示系统 · 科技政策跟踪 · 科创政策全景
- 需规序号：213–218
- 需规全文：`agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/科技政策跟踪-系统详细设计说明书.md` §2
- 日期：2026-11-08（2026-11-10 期望重冻结：215 部门行/头条、216 时点、217 报告文案；见 `POL-L2-DS10-CMP-DEMO-FIX-R20261110-DATA`。2026-11-11 增补 214 支持强度构成四维冻结，出处 `gapfill_policy_support_factors`，见 `POL-FACTOR-GAPFILL-L01`。2026-11-11 增补 216 政策类型块冻结：QPOL-01 文种临时默认 🟡，出处 `demo_gkxlumenx_dwd.policy_base_info.policy_type` 按省聚合，见 `POL-L2-DS10-CMP-PTYPE-QA-L01`。**2026-11-12 COVER-FDE**：补 213 变化统计 Tag、214 差异柱图+优缺点、217 真 Word/PDF、218 三图种形态期望）
- 调度核对：见文末

查库时间：2026-11-10 16:0x（读面时间，取自展示接口只读对照；首轮冻结 2026-11-07 16:01:36，2026-11-10 并行灌数批次 `BTN-panorama`、`mock_20260623` 合法覆盖后重冻结）。主机 `10.50.11.76`，用户 `gkxlumenx`（取自 `lumen-algo-py/scripts/seed/seed_synth_elem.py`）。口令未写入本文件。

**对标双方（216 / 217 / 218 固定）**：`北京市` ↔ `广东省`。本用例只认这一对；范围固定「国内先进地区」。不要用广东/山东或其他省组合当主路径——`gapfill_policy_benchmark_report` 可演样本按北京/广东灌，换对象会对不上行或只出单侧。报告表「对标对象」列是**该行视角主体**；另一侧是对照方（文案里的「两地 / 对方」即指这一对里的另一方）。

展示读面（代码）：`gkxlumen-display` 的全景 `stats` / `version-diff` / `benchmark-report` / `{id}/detail` 委托 `gkxlumen-element`；`stats` 的头条再委托专题指标。element 缺项库 `gkxlumenx_gapfill`，ADS 库 `demo_gkxlumenx_ads`，正文库 `demo_gkxlumenx_dwd`。本次只读这些库。

| 库.表 | 用途 |
|---|---|
| `gkxlumenx_gapfill.gapfill_policy_version_diff` | 213 |
| `gkxlumenx_gapfill.gapfill_policy_detail_compare` | 214 申报条件、申报材料（优缺点改走实时 LLM Job，不读本表） |
| `gkxlumenx_gapfill.gapfill_policy_support_factors` | 214 支持强度构成四维（资金/税收/土地/人才） |
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
| 213 政策新旧对比 | 科创政策全景 · 政策新旧对比 | 政策 `18363390`（标题「广东省科学技术厅关于印发《贯彻落实〈科技部办公厅关于营造更好环境支持科技型中小企业研发的通知〉的工作方案》的通知」）；旧时点 `2022-04-06`；新时点 `2022-06-15` | 两个时点都选定后点「查询对比」 | `GET /display/v1/policy/panorama/version-diff` | `policy_id=18363390&publish_date_a=2022-04-06&publish_date_b=2022-06-15` | records 3 行，日期对为 `2022-04-06` / `2022-06-15`。新增：「相对另一发布日，增补了研发环境支持的说明。缺项演示。」修改：「相对另一发布日，支持对象的表述有修改。缺项演示。」删除：「相对另一发布日，删去了一处过渡安排。缺项演示。」出处 `gapfill_policy_version_diff.summary_text`。顶层 `analysis_text`：「政策由 2022-04-06 版本演进至 2022-06-15 版本，整体呈支持力度加强、适用范围拓展趋势。」出处 `gapfill_policy_version_analysis.analysis_text`。**形态期望（COVER-FDE + 213-ANALYSIS）**：同屏见「变化统计与分析」块——Tag「新增 1 项 / 修改 1 项 / 删除 1 项」+ 上述非空演变趋势说明。对不上则 records 空 | 可演 |
| 214 政策详情对比 | 科创政策全景 · 政策详情对比 | 政策 `18363390`（标题「广东省科学技术厅关于印发《贯彻落实〈科技部办公厅关于营造更好环境支持科技型中小企业研发的通知〉的工作方案》的通知」）与 `18407696`（标题「深圳市科技创新委员会（深圳市外国专家局）关于发布2022年度深圳市外国人来华工作许可工资收入计算标准的通知」）；维度含申报条件、申报材料 | 至少两项后点「开始对比」 | `GET /display/v1/policy/panorama/{id}/detail`；另必 `POST /display/v1/policy/panorama/jobs`（`sub_type=policy_detail_pros_cons`） | `GET .../18363390/detail`；`GET .../18407696/detail`；`POST .../jobs` body 含 `sub_type=policy_detail_pros_cons` 与两 id（指纹 `policy-detail-pros-cons-live:`） | 申报时间/部门/条件/材料与既有冻结一致（条件材料仍读 gapfill 附带列）。优缺点来自 Job `result_payload.items[]` 的 `pros_text`/`cons_text`（DWD 正文实时 LLM；**不读不写** gapfill 优缺点列；无密钥则空态「暂无优缺点说明」）。两策产业类别空。支持强度构成四维（既有冻结）仍有效。**形态期望（COVER-FDE + PROS-LLM）**：同屏见差异柱图 + 每策优缺点块（或诚实空态）；列头/图例为政策名称，**禁止**「政策 #id」。力度分另点「计算支持力度」 | 可演 |
| 215 部门政策对比 | 科创政策全景 · 部门政策对比 | 读取后选「北京市科学技术委员会」（北京市）与「广东省科学技术厅」（广东省），跨区域 | 点「读取部门数据（stats 同步读）」 | `GET /display/v1/policy/panorama/stats` | `kind=all` | `impl_depts.records` **14 行**（2026-11-10 重冻结；BTN-panorama 批次扩充）。北京市科学技术委员会：项目类别件数 2，清单两行「三城一区科技创新成果科普传播」「科技监督检查」；技术类别件数 1，清单「三城一区科技创新成果科普传播」。广东省科学技术厅：项目类别件数 2，清单两行「科技型中小企业研发环境支持」「外国人来华工作许可收入标准」；技术类别件数 1，清单「科技型中小企业研发环境支持」。另有上海市科学技术委员会项目类别件数 1（清单「科技型中小企业研发环境支持」）；深圳市科技创新委员会技术类别件数 1（清单「外国人来华工作许可收入标准」）；北京市人民政府项目/技术各 1（清单「北京市人民政府关于印发《北京市关于加快新型储能产业高质量发展的若干措施》的通知」）；深圳市福田区人民政府、深圳市南山区人民政府（广东省）各项目/技术 1（清单分别为《福田区支持网络与通信产业科创平台建设实施细则》《南山区促进合成生物科技成果转化应用指南》印发通知）；苏州市人民政府（江苏省）项目/技术各 1（清单《苏州市新材料产业知识产权强基行动方案》印发通知）。出处 `gapfill_policy_impl_dept` 的 `region_name`、`impl_dept`、`aspect`、`item_count`、`list_title`。头条 `M_POLICY_TOTAL_COUNT` 为 **20184**（2026-11-10 重冻结），出处 `demo_gkxlumenx_ads.policy_level_dist.policy_count`。部门件数用 `item_count`，不用 20184 | 可演 |
| 216 标杆比对功能 | 科创政策全景 · 标杆比对 | **对标双方「北京市」↔「广东省」**；范围「国内先进地区」；字段「支持力度」+「政策类型」（QPOL-01 文种临时默认 🟡） | 按这三项填好后请求 stats。页面按钮「读取对标数据」当前只发 `kind=all` | `GET /display/v1/policy/panorama/stats` | `kind=all&benchmark_scope=国内先进地区&benchmark_object=北京市&benchmark_object=广东省&compare_field=支持力度&compare_field=政策类型` | `benchmark_objects` 含北京市 `scope_code=110000`、广东省 `scope_code=440000`（省级共 31 行）。`support_strength`：`region_code` `110000` 与 `440000`，`stat_date` **`2026-11-10`**（2026-11-10 重冻结；mock_20260623 批次重跑，值不变），`metric_value` 均为 `58.0000000000`，`dim_key`「支持力度」。**政策类型块（2026-11-11 冻结，QPOL-01 文种临时默认 🟡，待甲方确认不去角标）**：`policy_types.records` 2 行（只含勾选对象）；北京市 `top_type=实施细则`、`top_count=3`、`items` 含该省多文种（`policy_type`/`policy_count`）；广东省 `top_type=目录`、`top_count=14`；行键 snake/camel 双形（`scope_name`/`scopeName`），前端 `compareLive.ts` 按 `policyTypeCellText` 渲「Top 文种+件数」，界面列头带 🟡 QPOL-01 角标「类型一级分类口径待甲方确认；本列临时默认 DWD 文种按省聚合（Top 文种+件数）」；无文种省份显示 `—` 不造 0。出处 `demo_gkxlumenx_dwd.policy_base_info.policy_type`（`is_deleted=0`、`source_plane IN ('domestic','global')`）按省 `COUNT(DISTINCT policy_id)` 聚合，Java 端计件下推库端（`PolicyGapfillController`）。218 可视化图中该列不进雷达/柱状/热力轴（文本值不进数值轴）。范围「全球科创领先城市」对象为空，本路径不选。只发 `kind=all` 时力度块为空、政策类型块为空（`compare_field` 未勾选不返回） | 可演 |
| 217 对标报告生成与导出 | 科创政策全景 · 对标报告 | **对标双方「北京市」↔「广东省」**（谁对谁：北京对广东；报告两行各以一方为视角）；字段「支持力度」 | 点「生成报告」；有行后再点「导出 Word」或「导出 PDF」 | `GET /display/v1/policy/panorama/benchmark-report` | `benchmark_object=北京市&benchmark_object=广东省&compare_field=支持力度` | records **2 行**（北京一行 + 广东一行，缺任一侧则本行失败）。2026-11-10 重冻结（BTN-panorama 批次重写文案，行结构/对象/字段不变）。北京市视角：差异「北京市与对照地区的支持力度不一样。」优劣「北京市的支持力度一边更集中，一边覆盖更稳。」建议「可借鉴对照地区把支持力度写清楚的做法。」正文「北京市《北京市人民政府关于印发《北京市关于加快新型储能产业高质量发展的若干措施》的通知》在支持力度上与对照地区不同，可借鉴对方把同类措施写清楚的做法。」。广东省视角：差异「广东省与对照地区的支持力度不一样。」优劣「广东省的支持力度一边更集中，一边覆盖更稳。」建议「可借鉴对照地区把支持力度写清楚的做法。」正文「广东省《深圳市福田区人民政府关于印发《福田区支持网络与通信产业科创平台建设实施细则》的通知》在支持力度上与对照地区不同，可借鉴对方把同类措施写清楚的做法。」。出处 `gapfill_policy_benchmark_report` 的 `difference_text`、`pros_cons_text`、`suggestion_text`、`report_body`。**形态期望（COVER-FDE，2026-11-12 纠偏）**：导出走 `POST /display/v1/situation/report/generate`（`reportType=policy-panorama-benchmark`）→ OpenHTMLtoPDF；PDF=真 `.pdf` 字节；Word=同源 `format=html` 存 `.doc`；内容来自当次行；禁止 text/plain、禁止打印另存冒充 PDF；无行不产文件 | 可演 |
| 218 对标结果可视化展示 | 科创政策全景 · 对标结果可视化 | **对标双方「北京市」↔「广东省」**；地区视角；图种雷达、柱状或热力任选其一 | 点「生成可视化」 | `POST /display/v1/policy/panorama/jobs` | `{"sub_type":"policy_intensity","params":{"scope_type":"province","policy_ids":["北京市","广东省"]}}`（`analysis_fp` 由前端按对象集现算，本用例不冻结哈希） | 省级行：北京市 `intensity_index` `864.1800000000`，`industry_coverage` `27.8800000000`，`rank_no` 2；广东省 `intensity_index` `741.5100000000`，`industry_coverage` `35.7700000000`，`rank_no` 3。两行 `intensity_score` 为空。`metric_id` 为 `M_POLICY_INTENSITY_INDEX/M_POLICY_INDUSTRY_COVERAGE`。出处 `demo_gkxlumenx_ads.policy_intensity`。该 POST 会先 `intensity.run()` 再读。本用例填写时未提交，期望是 2026-11-07 16:01:36 的表内现数。**形态期望（COVER-FDE）**：界面可选雷达 / 柱状 / 热力三图种；无行则图空，不返回演示序列 | 可演 |

## 一条主路径

按下面顺序走可演的行。条件不另做排列组合。214 的「计算支持力度」和 218 的「生成可视化」都会先写表再读。本路径把表内现数写进期望，填写时没有提交这两次写请求。

1. 序号 215：打开「部门政策对比」，点「读取部门数据（stats 同步读）」。请求 `GET /display/v1/policy/panorama/stats?kind=all`。应看到 **14 行**实施部门（2026-11-10 重冻结），其中北京市科学技术委员会与广东省科学技术厅的件数和清单与覆盖表一致。头条政策总数 **20184**。
2. 序号 216：打开标杆比对，范围选「国内先进地区」，**对标双方只选「北京市」「广东省」**（不要选山东等其它省），字段勾「支持力度」与「政策类型」。请求带上 `benchmark_scope`、两个 `benchmark_object` 和 `compare_field=支持力度&compare_field=政策类型`。应看到省级对象码 `110000`、`440000`，支持力度 `58.0000000000`（`2026-11-10`）；政策类型列北京「实施细则 3」、广东「目录 14」（QPOL-01 文种临时默认 🟡，列头带角标），无文种省份显示 `—`；可视化图表中该列不进数值轴。
3. 序号 217：仍用北京↔广东 + 支持力度，点「生成报告」。请求 `GET /display/v1/policy/panorama/benchmark-report`。应看到 **北京市、广东省各一行**（共 2 行）；「对照地区 / 对方」分别指这一对里的另一侧。四句原文与覆盖表一致（2026-11-10 重冻结文案）。再点「导出 Word」或「导出 PDF」：应再打 `POST /display/v1/situation/report/generate`，PDF 下载真 `.pdf`，Word 为同源 HTML 的 `.doc`；内容来自这两行，不得是打印另存或 text/plain。
4. 序号 218：仍用北京↔广东，视角保持「地区」，图种在雷达/柱状/热力中任选。表内现数为北京市力度指数 `864.1800000000`、产业覆盖 `27.8800000000`、排名 2，广东省力度指数 `741.5100000000`、产业覆盖 `35.7700000000`、排名 3。点「生成可视化」才会提交 `policy_intensity`；填写本用例时未点。
5. 序号 213：打开政策 `18363390` 的新旧对比，时点 `2022-04-06` 与 `2022-06-15`，点「查询对比」。应看到新增、修改、删除三句摘要，「变化统计与分析」块 Tag「新增 1 项 / 修改 1 项 / 删除 1 项」，以及一句含两日期的演变趋势说明。
6. 序号 214：详情对比选择 `18363390` 与 `18407696`，点「开始对比」。应看到两个申报时间、两个受理部门、两段申报条件和两段申报材料、差异柱图、每策优缺点块（实时 LLM 结果板；无密钥则诚实空态）；列头与图例为两策政策名称（不得出现「政策 #18363390」/「政策 #18407696」）。同次对比必打 `policy_detail_pros_cons` Job，优缺点不读 gapfill。产业类别为空。支持强度构成：`18363390` 资金 40 / 税收 100 / 土地 40 / 人才 100；`18407696` 资金、税收、土地显示 —，人才 100。不点「计算支持力度」。

## 调度核对

需规 213–218 各有一行。可演 6 行，覆盖不到 0 行。主路径只串这 6 行。不建本二级的演示样本循环，不派数据单，不派算法单。

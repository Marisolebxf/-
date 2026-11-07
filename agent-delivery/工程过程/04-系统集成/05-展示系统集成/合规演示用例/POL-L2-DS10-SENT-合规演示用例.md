# POL-L2-DS10-SENT · 政策舆情评估 · 合规演示用例

- 规程：`agent-delivery/产品实现规程.md` §6.4
- 系统：科技信息展示系统 · 科技政策跟踪 · 科创政策全景
- 需规序号：207–212
- 需规全文：`agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/科技政策跟踪-系统详细设计说明书.md` §2
- 日期：2026-11-07
- 调度核对：见文末

历史记录 `测试用例/POL-L2-DS10-SENT-QA-L01.md` 不改写成期望。208 不设资源。

历史集成测试记录保持原文件。这里只写基于现有数据选定的一组输入。

## 查库

- 时间：2026-11-07 15:56:52
- 主机 `10.50.11.76`，用户 `gkxlumenx`（`lumen-algo-py/scripts/seed/seed_synth_elem.py` 缺省）。只读 SELECT，未执行 `--apply`。
- 207 检索读 `demo_gkxlumenx_dwd.policy_base_info`。展示 `PolicyPanoramaService.search` 委托 Python `polan.search.search_policies`；平面头未传时 `apply_plane` 用 demo 库。
- 209 读 `demo_gkxlumenx_ads.policy_effect`（`scope_type=region_effect`）和 `demo_gkxlumenx_ads.policy_metric_timeseries`（`metric_id=M_POLICY_IMPLEMENTATION_EFFECT`）。出处：`polan/job.py` `_policy_effect_rows`。
- 210 读 `gkxlumenx_gapfill.gapfill_policy_audience_feedback`。出处：`PolicyGapfillController` `FEEDBACK_SQL`。
- 211 读 `gkxlumenx_gapfill.gapfill_policy_assessment_report`。出处：同控制器 `REPORT_SQL`。
- 212 读 `demo_gkxlumenx_ads.policy_match`。出处：`polan/job.py` `_policy_match_rows`。
- 对照：`gkxlumenx_ads.policy_effect` 的 `region_effect` 为 0 行，不拿来填。`gkxlumenx_dwd.policy_base_info` 同一关键词也是 73 条，展示默认平面不读这张。
- 这些行里效果 `ext` 带 `is_mock: true`。D4 仍可以是 mock。库内有可展示行，本用例记可演。

## 覆盖表

| 需规位置 | 界面 | 输入或选择 | 触发 | 接口地址 | 按界面值填好的请求 | 期望输出 | 数据情况 |
|---|---|---|---|---|---|---|---|
| 207 政策查询与对比 | 科创政策全景 · 舆情 | 关键词「人工智能」 | 点「进入多维检索查询」进入检索页，在关键词框输入后点搜索。对比弹窗用同一关键词搜候选 | `GET /display/v1/policy/panorama/search` | `keyword=人工智能&q=人工智能` | 条件与 `polan.search` 一致：`is_deleted=0`，标题、关键词或摘要含「人工智能」，`ORDER BY publish_date DESC, policy_id`。`COUNT(*)` 为 73。首条 `policy_id` 18323509，标题「关于组织开展人工智能医疗器械创新任务揭榜申报工作的通知」，发布机关「苏州市工业和信息化局」，发布时间 2021-11-24，省份「江苏省」，城市「苏州市」。下一条 18363833，标题「关于组织推荐人工智能医疗器械创新任务揭榜工作的通知」，发布机关「河北省工业和信息化厅」，发布时间 2021-11-16。无命中则列表空，不返回 501 | 可演 |
| 208 区域政策差异性分析 | 科创政策全景 · 舆情 | 不填。本叶不发政策接口 | 无 | 不设资源 | 不请求 | 只读第 7 项已有子图。不新开查图资源 | 设计无资源 |
| 209 政策实施效果跟踪 | 科创政策全景 · 舆情 | 不填区域。全区域一次提交 | 打开舆情页签时无条件板自动提交；也可点「开始分析」 | `POST /display/v1/policy/panorama/jobs` | `{"sub_type":"policy_effect"}` | `policy_effect` 中 `scope_type=region_effect` 共 31 行。广东省 `scope_code` 440000：`effect_score` 存 `15.0000000000`，`ext.explanation` 原文「广东省效果评分15.0（v2 确定性口径：有效率×50%+力度均值×50%；社会/环境维待采购不合成）」。时序同一 `region_code`：`stat_date` 2026-11-07，`metric_value` `0.0000000000`，`dim_key`「落地实效性」，`metric_id` `M_POLICY_IMPLEMENTATION_EFFECT`。无 `region_effect` 行则空，不另造一行 | 可演 |
| 210 政策受众反馈收集 | 科创政策全景 · 舆情 | 渠道「问卷调查」（库内 `channel` 为「问卷」） | 打开舆情页签即 GET；再点该渠道 | `GET /display/v1/policy/panorama/feedback` | 无查询参数 | `ORDER BY feedback_at DESC, id DESC` 共 6 行，问卷、在线评价、意见征集各 2 行。问卷内按该序：广州某高校科研人员，「缺项演示。这条意见的来源类别是问卷。成果转化收益分配规则希望写得更明确。」，评分空；深圳某科技企业研发负责人，「缺项演示。这条意见的来源类别是问卷，不是一份真实问卷。希望研发费用补助的申报材料能合并成一次提交。」，评分 `4.50`，`policy_id` `GF-POL-SENT-210-01`。在线评价可见北京某集成电路企业，「缺项演示。这条意见的来源类别是在线评价。设备更新补贴的兑现周期偏长。」，评分 `3.00`。意见征集可见成都某新型研发机构，「缺项演示。这条意见的来源类别是意见征集。建议把中试平台的共用设备清单公开。」，评分 `5.00`。无行则空列表 | 可演 |
| 211 政策效果评估报告 | 科创政策全景 · 舆情 | 不填。点列表首条「查看报告」 | 打开舆情页签即 GET | `GET /display/v1/policy/panorama/assessment-report` | 无查询参数 | `ORDER BY generated_at DESC, id DESC` 的首条 `id` 2。`scope_text`「深圳市高层次人才安居与青年科研岗位条款，2024年至2025年。这是报告里的评估范围，不是区域代码。」达成度「缺项演示。安居资格按年度公布后，符合条件的青年科研人员申请路径更清楚。这段达成度只写在本行，不是新指标。」社会影响「缺项演示。稳定的安居窗口使青年科研人员在本地连续工作的安排更明确。」问题「缺项演示。认定材料和安居申请仍要分别提交，办理进度互不可见。」建议「缺项演示。把认定与安居合成一次申请，并在同一页面显示办理进度。」正文「缺项演示。正文只写在本行，不生成文件。本报告评估深圳市高层次人才安居与青年科研岗位条款：达成度是申请路径更清楚；社会影响是连续工作的安排更明确；问题是两套材料分开办理；建议是合成一次申请并显示进度。」同表还有 `id` 1，`scope_text` 以「广东省科技企业研发支持条款，2024年至2025年。这是报告里的评估范围，不是区域代码。」开头。无行则空 | 可演 |
| 212 政策匹配与推送 | 科创政策全景 · 舆情 | 主体「华芯生物有限公司（E0001）」。推送方式保持「系统通知（收件箱）」 | 选中该主体后点「开始匹配」。切换主体不自动请求 | `POST /display/v1/policy/panorama/jobs` | `{"sub_type":"policy_match","params":{"subject_id":"E0001"}}` | 该主体 5 行，`subject_name`「华芯生物有限公司」。`rank_no` 1：`policy_title`「国务院办公厅关于印发新能源汽车产业发展规划（2021—2035年）的通知」，`match_score` `25.0000000000`，`match_reasons` 原文 `["国家级普适"]`，`metric_id` `M_POLICY_MATCH`。该主体其余行分数与理由相同。无行则空，不造演示分。点「推送匹配政策」不读表，本次没有可核对的投递原文，不编已发送 | 可演 |

## 一条主路径

按下面顺序走可演的行。208 不进入。条件不另做排列组合。

1. 打开科创政策全景 · 政策舆情评估。210 与 211 随挂载 GET；209 无条件，随挂载 POST `{"sub_type":"policy_effect"}`。应看到反馈 6 行、报告 2 行，以及广东省效果口径说明「广东省效果评分15.0（v2 确定性口径：有效率×50%+力度均值×50%；社会/环境维待采购不合成）」。
2. 点「问卷调查」。应看到广州某高校科研人员与深圳某科技企业研发负责人两句意见，原文与覆盖表 210 相同。
3. 点评估报告列表首条「查看报告」。应看到深圳市高层次人才安居与青年科研岗位条款的达成度、社会影响、问题、建议和正文，原文与覆盖表 211 相同。
4. 点「进入多维检索查询」，关键词填「人工智能」后点搜索。请求 `keyword=人工智能&q=人工智能`。应看到首条「关于组织开展人工智能医疗器械创新任务揭榜申报工作的通知」（18323509，苏州市工业和信息化局，2021-11-24）。对比候选用同一关键词，下一条为 18363833。
5. 回到舆情，主体选「华芯生物有限公司（E0001）」，点「开始匹配」。请求 `{"sub_type":"policy_match","params":{"subject_id":"E0001"}}`。应看到排名 1「国务院办公厅关于印发新能源汽车产业发展规划（2021—2035年）的通知」，理由原文 `["国家级普适"]`。

## 调度核对

需规 207–212 各有一行。可演 5 行（207、209、210、211、212）。覆盖不到 0 行。设计无资源 1 行（208），不派数据单，不新开查图资源。主路径只串可演行。

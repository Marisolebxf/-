# POL-L2-DS10-QRY · 多维检索查询 · 合规演示用例

- 规程：`agent-delivery/产品实现规程.md` §6.4
- 系统：科技信息展示系统 · 科技政策跟踪 · 科创政策全景
- 需规序号：197–202
- 需规全文：`agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/科技政策跟踪-系统详细设计说明书.md` §2
- 日期：2026-11-07
- 调度核对：见文末

历史验收记录 `测试用例/POL-L2-DS10-QRY-FE-DISP-L01-验收用例.md` 不改写成期望。其中的 404 仍留在原文件。契约 `BE-POL-CONTRACT-01` 仍是 backlog。

历史集成测试记录保持原文件。这里只写基于现有数据选定的一组输入。

## 查库

- 时间：2026-11-07 16:09:26
- 主机 `10.50.11.76`，用户 `gkxlumenx`（`lumen-algo-py/scripts/seed/seed_synth_elem.py` 缺省）。只读 SELECT，未执行 `--apply`。
- 检索与详情读 `demo_gkxlumenx_dwd.policy_base_info`。`PolicyPanoramaService.search` / `detail` 委托专题，再进 Python。平面头未传时 `apply_plane` 用 demo 库。该表 `COUNT(*)` 为 20008，且 `COALESCE(is_deleted,0)=0` 仍是 20008，目录开关不回退 `gkxlumenx_gapfill.gapfill_policy_qry_doc`。
- 统计读 `demo_gkxlumenx_ads` 的 `policy_level_dist`、`policy_type_dist`、`policy_timeseries`、`policy_national_dist`、`policy_sz_dist`（行数 6、14、46、31、5，都不为 0，不回退 `gapfill_policy_qry_stat`）。197–202 的界面动作是检索、排序、收藏和分享，期望不引用这些统计卡数字。
- 智能排序只读 `gkxlumenx_gapfill.gapfill_policy_qry_rank`（`rank_dim` 为 relevance、timeliness、importance 各 6 行）。
- 历史与收藏读 `gkxlumenx_topic_policy.policy_search_history`（62 行）、`policy_favorite`（3 行）。
- `gkxlumenx_topic_policy.policy_share_export` 不存在。分享接口不回读导出记录。
- 对照：`gkxlumenx_dwd.policy_base_info` 有 40000 行。展示默认平面不读这张，不拿来填期望。
- 排序行在缺项表，D4 仍可以是 mock。库内有展示会读的行，对应序号记可演。

## 覆盖表

| 需规位置 | 界面 | 输入或选择 | 触发 | 接口地址 | 按界面值填好的请求 | 期望输出 | 数据情况 |
|---|---|---|---|---|---|---|---|
| 197 多维度检索条件设置 | 科创政策全景 · 检索 · 关键词搜索 | 关键词框填「人工智能」。地区选「深圳市」（选项 key `shenzhen`，页面收成 `region=深圳`）。不选「海外参考」，不选「科创政策」 | 点搜索。地区变化后约 80ms 会再发一次 | `GET /display/v1/policy/panorama/search` | `keyword=人工智能&q=人工智能&region=深圳` | `is_deleted=0`，标题、关键词或摘要含「人工智能」，且省、市、区、国家、地域或 `region` 含「深圳」。`ORDER BY publish_date DESC, policy_id`。`COUNT(*)` 为 8，默认 `limit` 20 会全部返回。首条 `policy_id` 18358631，标题「市工业和信息化局关于组织推荐首届全国人工智能创新应用大赛参赛团队的通知」，发布机关「深圳市工业和信息化局」，发布时间 2021-09-02，省份「广东省」，城市「深圳市」。其后依次：18323060「市工业和信息化局关于征集人工智能创新应用示范项目（第二批）的通知」；18378985「陈如桂市长率队调研参观市工业展览馆」；18320515「市工业和信息化局关于组织申报广东省首批智能制造生态合作伙伴的通知」；18369119「市工业和信息化局关于征集人工智能创新应用示范项目的通知」；18398039「关于甄选“第十八届中国人才交流大会—2020年中国IT产业校企合作大会”参展企业的通知」；18340257「深圳国际创新谷创新型产业用房租赁通告（第四期）」；18341932「高交会组委办关于邀请高新技术企业参观高交会的通知」。无命中则列表空，不返回 501 | 可演 |
| 198 高级检索功能 | 科创政策全景 · 检索 · 高级检索 | 关键词框留空。政策关键词填「固态电池」；发布部门选「科技部」；发布时间 2023 至 2023。不选政策状态「有效」 | 点「应用检索」 | `GET /display/v1/policy/panorama/search` | `keyword=固态电池&q=固态电池&ministry=科技部&publish_year_from=2023&publish_year_to=2023` | 三个条件同时成立：`publish_organization` 含「科技部」，标题、关键词或摘要含「固态电池」，`publish_year` 为 2023。`COUNT(*)` 为 1。`policy_id` cn-gov-5737584，标题「工业和信息化部等六部门关于推动能源电子产业发展的指导意见」，发布机关「工业和信息化部 教育部 科技部 人民银行 银保监会 能源局」，发布时间 2023-01-17，`policy_type`「意见」，`rank`「国家级」。状态列全空，选「有效」会得到 0 条，本行不选。页面不把 NOT 送进查询。无命中则列表空，不返回 501 | 可演 |
| 199 检索结果智能排序 | 科创政策全景 · 检索 · 结果卡 | 排序选「相关性」（选项 value `relevance`） | 点「检索结果智能排序」里的「相关性」 | `GET /display/v1/policy/panorama/rank` | `factor=relevance` | 只读名次表，`rank_dim=relevance`，`ORDER BY rank_no, policy_id`，共 6 条。顺序：GF-POL-QRY-004（`rank_no` 1）、GF-POL-QRY-001（2）、GF-POL-QRY-003（3）、GF-POL-QRY-005（4）、GF-POL-QRY-002（5）、GF-POL-QRY-006（6）。每条 `gap_item`「无排序模型；只存名次，无分数」。`metric_id` 为空。响应不含 `smartScore`。页面若还带上当次检索参数，排序仍只认 `factor`。无行则 `items` 空 | 可演 |
| 200 检索结果筛选与分类 | 科创政策全景 · 检索 · 结果卡 | 效力级别先选「国家级」。结果出来后，在「检索结果筛选与分类」的政策类型选「意见」。不选地域 | 类型下拉变更后约 80ms 再发 search | `GET /display/v1/policy/panorama/search` | `level=国家级&policy_type=意见` | `rank` 等于「国家级」（不是 `["国家级"]` 这种 JSON），且 `policy_type` 含「意见」。`ORDER BY publish_date DESC, policy_id`。`COUNT(*)` 为 2。首条 `policy_id` cn-gov-7041785，标题「国家能源局等部门关于推进能源装备高质量发展的指导意见」，发布时间 2025-09-23，`policy_type`「意见」。下一条 `policy_id` cn-gov-5737584，标题「工业和信息化部等六部门关于推动能源电子产业发展的指导意见」，发布时间 2023-01-17，`policy_type`「意见」。两条按该字段分成一组「意见」。这 5 条国家级明文的 `region` 为空，二次筛地域没有可选项。无命中则列表空，不返回 501 | 可演 |
| 201 检索历史与收藏 | 科创政策全景 · 检索 | 已登录，用户标识 184。请求不传 `user_id` | 打开检索页即 GET 历史与收藏。再打开收藏 cn-gov-7067354 | `GET /display/v1/policy/panorama/favorites` | 无查询参数 | 历史按 `id` 降序。用户 184 最新一条 `id` 42，`query_json` 原文 `{"keyword":["电池"],"q":["电池"]}`。收藏按 `policy_id` 排序：cn-gov-6999382、cn-gov-7067354。再 `GET /display/v1/policy/panorama/favorites/cn-gov-7067354`，正文标题「鼓励外商投资产业目录（2025年版）」，正文开头含「（经国家发展改革委委务会议审议通过和商务部审签并经国务院同意2025年12月15日国家发展改革委、商务部令第37号公布」。匿名时列表空，不把空列表写成这条的期望 | 可演 |
| 202 检索结果导出与分享 | 科创政策全景 · 检索 · 结果卡 | 在 197 的结果上点「导出 Excel」 | 点导出 | `GET /display/v1/policy/panorama/share` | `keyword=人工智能&q=人工智能&region=深圳&format=excel&channel=link` | 不编 Excel、PDF 或邮件。`policy_share_export` 不存在，本次 SELECT 没有导出原文。不把 197 的目录标题写成已下载文件 | 覆盖不到：缺 Excel/PDF 导出记录和邮件记录。`gkxlumenx_topic_policy.policy_share_export` 不存在，分享接口不回读导出记录 |

## 一条主路径

按下面顺序走可演的行。202 不进入。条件不另做排列组合。

1. 序号 197：关键词框填「人工智能」，地区选「深圳市」，点搜索。请求 `keyword=人工智能&q=人工智能&region=深圳`。应看到 8 条，首条「市工业和信息化局关于组织推荐首届全国人工智能创新应用大赛参赛团队的通知」（18358631，深圳市工业和信息化局，2021-09-02）。
2. 序号 198：关键词框留空。高级检索填政策关键词「固态电池」、发布部门「科技部」、发布时间 2023 至 2023，点「应用检索」。请求 `keyword=固态电池&q=固态电池&ministry=科技部&publish_year_from=2023&publish_year_to=2023`。应看到唯一一条「工业和信息化部等六部门关于推动能源电子产业发展的指导意见」（cn-gov-5737584）。
3. 序号 200：效力级别选「国家级」，再在结果卡政策类型选「意见」。请求 `level=国家级&policy_type=意见`。应看到 2 条，首条「国家能源局等部门关于推进能源装备高质量发展的指导意见」（cn-gov-7041785，2025-09-23），下一条为 cn-gov-5737584。两条 `policy_type` 都是「意见」。
4. 序号 199：排序选「相关性」。请求 `factor=relevance`。应看到 6 条名次，第一条 `policy_id` GF-POL-QRY-004、`rank_no` 1，`gap_item`「无排序模型；只存名次，无分数」。响应不含 `smartScore`。
5. 序号 201：以用户 184 登录后打开检索页。历史最新一条 `id` 42，条件为关键词「电池」。收藏为 cn-gov-6999382、cn-gov-7067354。打开后者，标题为「鼓励外商投资产业目录（2025年版）」。

## 调度核对

需规 197–202 各有一行。可演 5 行（197、198、199、200、201）。覆盖不到 1 行（202，缺导出文件与邮件记录）。设计无资源 0 行。主路径只串可演行。本文不建演示样本循环，不派数据单，不派算法单。

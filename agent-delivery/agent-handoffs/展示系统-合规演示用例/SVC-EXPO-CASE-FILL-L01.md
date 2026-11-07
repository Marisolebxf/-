ponytail: full

# SVC-EXPO-CASE-FILL-L01 handoff（EXPO 合规演示用例回填）

- 任务：SVC-EXPO-CASE-FILL-L01；对象：`agent-delivery/工程过程/04-系统集成/05-展示系统集成/合规演示用例/SVC-L2-EXPO-合规演示用例.md`
- 完成：2026-11-07；27 行（SRS 575–601）数据情况列零缺格；输入或选择列已升级为可选项全集；状态行改「M2/M3 已填·2026-11-07」；新增证据口径块（主路径一句话后）与备注 8/9/10
- 未动：需规序号、其他列、索引文件、task-registry、对齐表、其他用例；未 commit/push

## 探测环境

- 网关 `http://10.50.69.111:30895`，StripPrefix=1，无 token 即 200；工具 curl.exe `--max-time 40`，全部只读 GET；无探测受阻（所有探测一次成功）

## 条件全集枚举结果

### exchange（来源：GET /display/v1/exchange/dictionaries 实测）
- activityType（必填，全集）：exchange 科技交流(22) / reasoning 科技思辨(135) / live 科技直播(32) / course 课程(63，字典名「科技竞赛课程」）
- status：upcoming 未开始 / ongoing 进行中 / ended 已结束（实测 exchange: 0/0/22；reasoning upcoming 26；course ongoing 13；live ended 32）
- timeRange：thisWeek / thisMonth / thisQuarter（exchange 0/0/4；reasoning 本月 5）
- categoryId：1 学术交流(12) / 2 专题研讨 / 3 技术讲座 / 4 专业论坛 / 5 合作项目 / 6 行业资讯
- liveType（仅 live）：seminar(13) / review / lecture / training / open_class / other
- subjectAreaId 1–13：exchange/live 生效（9→1、live 2→11）；⚠️ reasoning 不生效（任意值恒 135）
- sortType：LATEST / HOTTEST；difficulty 1/2/3；expertRole expert/host
- overview：stats 252/2282/77/105；yearly 2026(225/2276/77/105)、2025(6/3/0/0)、2024(6/1/0/0)；deepShiReachable=true；⚠️ activityCountByType={} 空对象
- sync 需 activityType（漏参 400），exchange 水位 total=25、nextUpdatedSince=2026-10-28T14:49:21+08:00

### competition（全量 pageSize=100 聚合 + 逐参数实测）
- competitionLevel：1 国家级(21) / 2 省级(4) / 3 市级(3) / 5 行业级(5) / 6 学校级(2)；⚠️ 各档合计 39 > total 37（疑对端多标签）
- stage：registering(4) / processing(3) / reviewing(2) / coming(0) / completed(28)，合计 37
- registrationDeadline：thisWeek(1) / thisMonth(1)；competitionTypeName：常规赛 35 / 认证赛 2（前端本地过滤）
- keyword=科技 → 7；theme=人工智能 → 0；stats 37/79/17；publishUrl=https://szc.test.dp.tech/tics/competitions/create
- ranking 有榜竞赛（探测 14 场 completed）：11048(3 条，榜首「我要发发发」清华大学 97 分） / 107(2) / 66(1) / 11026(1) / 11045(1)
- discussion 有数据：11048(5 帖，partitionId=4 成果交流区） / 11060(8 帖，partitionId=1 报名交流区）
- resource 有数据集：11048 / 11060 / 11055 / 11008（含预签名 downloadUrl）；107 为空

### communication（全量 pageSize=100 聚合 + 逐参数实测）
- contentType 实测 7 类：1 顶级期刊(22) / 2 学术会议(10) / 3 前沿成果(3) / 4 活动资讯(3) / 5 技术课程(2) / 6 成果转化(4) / 7 需求发布(3)；⚠️ 与 SRS 10 类口径完全不同
- subjectCategoryId：1 细胞与基因(13)/2 合成生物（9)/3 智能机器人（8)/4 前沿新材料（4)/5 光载信息（9)/6 深地深海（3)/8 量子信息（1)
- subjectAreaIds（传播口径）：1 哲学（11)/2 经济学（13)/3 法学（3)/4 教育学（5)/5 文学（5)/6 历史学（2)/7 理学（5)/8 工学（1)/13 艺术学（2)
- institutionTypeIds：1 学校（16)/2 机构（9)/3 媒体（1)/4 企业（5)（另 16 条无机构类型）
- sortType LATEST/HOTTEST 生效；keyword=科技 → 7；日期窗 2026-10-01~11-07 → 5；publishTimeOrder 仅 ASC 生效
- stats：totalContentCount=47；⚠️ monthlyViewCount/activeUserCount/newContentCount 均为 0
- detail contentId=17 → 28 字段齐全；sync total=57

## 逐行判定

- 可演 22 行：575–584、587、589、590、592、593–600（其中 578/581/587/593/595/597/599 带 ⚠️ 诚实口径注记）
- 覆盖不到 4 行：585（discussion 接口通页面未渲染）、586/591（resource 接口通页面未消费）、588（发布组织口径冲突）
- 部分可演 1 行：601（PC 可演，移动端待定）；待开发完成 0 行

## 遗留问题（最需人工确认）

1. 口径冲突（备注 1）：跳转 vs BFF 页面内嵌，588 验收口径待定
2. reasoning 学科筛选不生效、contentTypes 多值=0、publishTimeOrder=DESC 空壳、非法日期 200 空壳不报错——四处对端行为是否报修深势侧
3. 传播 stats 三卡全 0、overview activityCountByType={}——演示口径与前端取值路径确认
4. iframe 详情依赖对端 X-Frame-Options 放行，现场须预演

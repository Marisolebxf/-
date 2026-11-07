# POL-L2-DS11-READ · 结果解读报告多维展示 · 合规演示用例

- 规程：`agent-delivery/产品实现规程.md` §6.4
- 系统：科技信息展示系统 · 科技政策跟踪 · 政策分析评价
- 需规序号：223–226
- 需规全文：`agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/科技政策跟踪-系统详细设计说明书.md` §2
- 日期：2026-11-07
- 调度核对：见文末

期望摘自 `测试用例/POL-L2-DS11-READ-TEST-L01.md`。D4 仍是 mock。焦点与摘要走 jobs，短板条数走 counts。

历史集成测试记录保持原文件。这里只写基于现有数据选定的一组输入。

## 覆盖表

| 需规位置 | 界面 | 输入或选择 | 触发 | 接口地址 | 按界面值填好的请求 | 期望输出 | 数据情况 |
|---|---|---|---|---|---|---|---|
| 223 热点问题分析看板 | 政策分析评价 · 结果解读 | 不填筛选项，看短板条数 | 打开看板即 GET counts | GET /display/v1/policy/evaluation/counts | 无查询参数 | 有 `region_gap` 行时 `records` 至少 1 行，含 scopeCode、scopeName、shortboardCnt，shortboardCnt 为正整数，与表内一致，响应不含机遇字段。无行则空，不得返回 0，不返回 501。焦点指数 `POST jobs` body `{"sub_type":"policy_focus_ads"}` 会先跑 focus.run 并改写 `policy_id` 非空行，测试用例未给出具体分数，循环不重放 | 可演 |
| 224 分主题分指标互动解读 | 政策分析评价 · 结果解读 | 不另填。与 225 同一次 GET | 打开解读即 GET shells | GET /display/v1/policy/evaluation/shells | 无查询参数 | 解读 4 条：研发费用加计扣除、科技型中小企业培育、高新技术企业认定、科技创新成果科普传播。各有一句结论和一句应用建议。测试用例 BUG-01：shells 因旧列名恒空。循环不把这次空列表改写成通过 | 可演 |
| 225 多媒体辅助解读 | 政策分析评价 · 结果解读 | 不另填。与 224 同一次 GET | 同一次 shells | GET /display/v1/policy/evaluation/shells | 无查询参数 | 多媒体 3 条：研发费用加计扣除政策图解、科技型中小企业政策宣讲实录、高新技术企业认定要点速览。与 224 同一条 BUG-01 | 可演 |
| 226 智能摘要与结论推送 | 政策分析评价 · 结果解读 | sub_type 固定 policy_text_parse | 开始分析后取已有摘要，请求内不调用 parse.run | POST /display/v1/policy/evaluation/jobs | {"sub_type":"policy_text_parse"} | 结果只含 `ads.policy_text_parse.summary`。跑前后表行数不变。测试用例未冻结某一句摘要，循环不另编句子。无摘要则空，不返回写死段落 | 可演 |

## 一条主路径

按下面顺序走可演的行。条件不另做排列组合。

1. 序号 223：`GET /display/v1/policy/evaluation/counts`。有 region_gap 行时至少 1 行且 shortboardCnt 为正整数。不重放会改表的焦点 jobs。
2. 序号 224 与 225：同一次 `GET /display/v1/policy/evaluation/shells`。应看到解读 4 条、多媒体 3 条。BUG-01 未修好时空列表仍判不通过。
3. 序号 226：`POST .../evaluation/jobs`，body `{"sub_type":"policy_text_parse"}`。结果只含已有 summary，跑前后行数不变。不另编摘要句子。

## 调度核对

需规每一条都有一行。`可演` 的行可以进入循环。`设计无资源` 的行不派数据单，也不新开接口。

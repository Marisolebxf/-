# 重判明细 · TNIE（1 条）

| # | metric_id | 分组 | 中文名 | 现type | definition | formula | 新判type | 理由 |
|---|---|---|---|---|---|---|---|---|
| 1 | `M_TNIE_EVENT_COUNT` | T3 | 抽取事件条数 | MODEL | 单次科技新闻四要素抽取响应中 events 数组的长度；统计窗口为单次请求； 对象为启发式/LLM 抽取得到的事件对象；不去重（同文多次抽取可重复计数）； Wave0 默认 MODE=mock，口径待甲方确认后是否纳入正式看板。 | len(response.events) |  |  |

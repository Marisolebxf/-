# 数据说明卡 · M_TNIE_EVENT_COUNT（Wave0）

> 与 UI `MetricSpecHint` / `MetricSpecCard` 对齐；种子真源：`metrics/registry/cfg_metric-TNIE-seed.yaml`

### 抽取事件条数（M_TNIE_EVENT_COUNT）

| 字段 | 内容 |
|------|------|
| **业务名** | 抽取事件条数 |
| **metric_id** | `M_TNIE_EVENT_COUNT`（UI 别名 `TNIE.event_count`） |
| **业务口径定义** | 单次科技新闻四要素抽取响应中 `events` 数组长度；窗口=单次请求；不去重；Wave0 mock/llm 均可 |
| **计算公式** | `len(response.events)` |
| **数据源表** | `ads_tech_news_extraction` / `ads_tech_news_event`（DDL 已备）；Wave0 亦可 SQLite 沙箱落库 |
| **数据来源系统** | demo-algo-science → Java `gkxlumen-innov` 透传 → 网关 `/innov/**` |
| **更新频率** | on_request |
| **版本** | 0.1.0 |
| **是否 Mock** | 是（🧪）；⚠️ 待甲方确认是否纳入正式 KPI |
| **UI 出现位置** | lumen-ui-science-pc → 科技新闻四要素复核页头 |
| **acceptance** | E-TECH-NEWS-IE-M1-L03 |

# SITUATION-ENT-M1-REAL-DATA-20261105 · M1 科技全域态势真实数据收口 + 收藏服务端闭环

> **2026-11-05** · `agent:backend-agent` · 监管人 `human:李伟`
> **WBS 落点**：WBS-05-18 · DS-01 科技全域态势（M1 页面）
> **上游批次**：`METRIC-AUTH-DATA-1105-L01`（算法侧新增 9 源 / 31 表 / 约 32.4 万行，落 `demo_gkxlumenx_ai`）
> **运行形态**：本地部署测试（display 7099 + show-py 8082 + 前端 3000）

## 1. 任务摘要

按用户裁定把 M1「科技全域态势」从「企业 + 五要素真实、其余 mock」推进到「除会议外全部真实或带明确缺口记录」，并修复收藏列表两个服务端化缺口。

### 1.1 用户裁定（决策留痕）

| # | 决策 | 裁定原话 / 依据 | 落地结果 |
|---|---|---|---|
| D1 | **企业影响力直接用「综合企业评分」** | 2026-11-05「综合企业评分 就用它当企业影响力」 | 影响力卡改读 `enterprise_score.score_total`（0–100），去掉「占位」字样；实测 188,775 家 / 均分 37.8 |
| D2 | **期刊显示全量名录** | 2026-11-05「期刊显示全量」 | 主页要素卡 / 地图 / 对比口径统一为 `dwd_zh_journal(2796) + dwd_en_journal(605)` = **3,401**，不再用质量榜 1514 或 mock 7200 |
| D3 | **会议保持 mock** | 2026-11-05「会议还是 mock」 | overview / map 会议 1,280 保留 `mock=true`；依据 `M_INNOV_CONFERENCE_INFLUENCE` 完全不支持 |
| D4 | **其余能接都接** | 2026-11-05「其余能接都接」 | 影响力机构 7,842 / 专家 21,316 / 期刊 1,514 / 论文（学科 TOP10_X）改读 `demo_gkxlumenx_ai` |
| D5 | **企业影响力只走我方库，不读 demo** | 2026-11-05「企业影响力 这个是我方库的，先读 demo 库」 | 企业卡仍走 element（我方 `enterprise_score`），demo 库只用于机构 / 专家 / 期刊 / 论文 |
| D6 | **收藏两个缺口补链** | 2026-11-05「打通这个两个接口」 | `removeFollow` 同步服务端 `remove`；打开收藏面板时 `refreshFromServer` |

## 2. 数据源与口径

### 2.1 外部权威库 `demo_gkxlumenx_ai`（只读）

| 榜单 | 表 | 行数 | 取数口径 |
|---|---|---|---|
| 机构影响力 | `ads_org_innovation_rank` | 7,842 | 创新指数榜，按分数降序 |
| 专家影响力 | `innov_scholar_influence` | 21,316 | scholar influence score |
| 期刊影响力 | `ads_journal_quality_list` | 1,514 | quality_score（0–100；源表多数集中在 0–0.1，仅 317 本 >1，均分 0.92 对头部不敏感，已在 countNote 披露） |
| 论文影响力 | `ads_paper_field_top` | 36,785 | ASJC 学科维 `TOP10_X`（top10% 高被引论文占比），发文量 ≥1000、`CHAR_LENGTH(asjc)=4` 去重父子学科 |
| 期刊全量 | `demo_gkxlumenx_ods.dwd_zh_journal` + `dwd_en_journal` | 2,796 + 605 | 全量名录 = **3,401**；质量榜子集 1,514 另返 `quality_count` |

### 2.2 我方库

| 要素 | 源 | 行数 / 值 |
|---|---|---|
| 企业影响力 | `ADS enterprise_score.score_total`（经 element） | 188,775 家 / 均分 37.8 |
| 服务机构统计 | `ADS svc_metric_fact`（与专题同源） | 43,296 |
| 企业 / 论文 / 专利 / 人才 / 项目 / 机构 | element + 久新 | 187,643 / 858,620 / 71,043 / 159,546 / 392,032 / 48,444 |

### 2.3 指标库核对结论（`指标入库详情.xlsx`）

- **科技专题系统（304 条）**：7 条影响力指标（期刊 / 机构 / 论文 / 事件 / 孵化载体 / 生态评分 / 服务机构），**不含企业影响力**。
- **科技专题算法库（459 条）**：`M_INNOV_ENTERPRISE_INFLUENCE`「企业影响力」存在，**部分支持、是否归了久新=否**，源表 `dwd_org_annual_financial_info` / `dwd_org_base_info` / `dwd_org_subsidiary_info` / `dwd_patent` / `dwd_patent_transfer` / `dwd_zh_author` / `dwd_zh_paper`。
- 由此确认：企业影响力在算法侧只有定义、无全库产物，故 D1 采用并列可用的 `score_total` 口径。

## 3. 代码改动

### 3.1 `lumen-topic-py`（show-py 只读门面）

| 文件 | 类型 | 说明 |
|---|---|---|
| `gkx_show_service/adsdb.py` | 新增 | 复用 ADS 只读连接，`connect/query` 增加 `database` 参数；线程连接改为按库缓存字典 |
| `gkx_show_service/demoai.py` | 新增 | `demo_gkxlumenx_ai` 只读薄封装 |
| `gkx_show_service/views/demo_indicator.py` | 新增 | `POST /internal/gkx-show/demo/journal-total`、`POST /internal/gkx-show/demo/influence` |
| `gkx_show_service/views/svc_factor.py` | 新增 | 服务机构要素 KPI 包（与专题 `svc_*` 同源） |
| `gkx_show_service/main.py` | 修改 | 注册 `svc_factor`、`demo_indicator` 路由 |
| `k8s/dev-show-py.yaml` | 修改 | 显式 `GKX_ADSDB_DATABASE=demo_gkxlumenx_ads`（服务机构与专题同源） |

### 3.2 `lumen-svc-platform`（display BFF）

| 文件 | 说明 |
|---|---|
| `controller/SituationController.java` | 期刊卡 / 地图改全量 3,401；新增 `demoJournalTotalOf()`、`demoInfluenceOf()`、`journalSubFactorFromDemo()`、`paperSubFactorFromDemo()`、`buildScholarInfluenceCardFromDemo()`、`buildInstitutionInfluenceCardFromDemo()`；企业卡口径改为 `score_total` 并删除「占位」表述；技术产出卡级统计只合计非 mock 子类（`countNote` 说明）；论文子类 `source` 由 `ISCORR_X` 修正为 `TOP10_X` |
| `feign/RemoteShowPythonClient.java` | 新增 `demoJournalTotal` / `demoInfluence`（`@NoToken`） |

### 3.3 `lumen-ui-science-pc`（前端）

| 文件 | 说明 |
|---|---|
| `src/components/export/useFollow.ts` | `removeFollow` 本地删除后同步调用 `removeRelation`（失败 toast「仅本地生效」），避免刷新后被服务端反显回来 |
| `src/views/situation/overview/index.vue` | 新增 `onToggleFollowPanel()`，打开「我的收藏」时调用 `refreshFromServer()` 重新反显 |

## 4. 验证证据（2026-11-05 本地实跑）

### 4.1 overview `/v1/situation/overview`

| 要素 | 值 | 来源 | mock |
|---|---|---|---|
| 期刊 | **3,401** | 久新中英文期刊名录 | 否 |
| 会议 | 1,280 | 代码层 mock | **是** |
| 企业 | 187,643 | element | 否 |
| 论文 / 专利 / 人才 | 858,620 / 71,043 / 159,546 | 久新 | 否 |
| 项目 / 机构 / 服务机构 | 392,032 / 48,444 / 43,296 | 久新 / 我方 ADS | 否 |

### 4.2 influence `/v1/situation/influence`

| 卡 | count | averageScore | mock |
|---|---|---|---|
| 企业影响力 | 188,775 | 37.8 | 否（`score_total` 口径） |
| 机构影响力 | 7,842 | — | 否（demo） |
| 专家影响力 | 21,316 | — | 否（demo） |
| 技术产出·期刊子类 | 1,514 | 0.92 | 否（demo） |
| 技术产出·论文子类 | —（学科维） | — | 否（demo TOP10_X） |
| 技术产出·专利子类 | 1,820,000 | 96.1 | **是** |
| 服务机构影响力 | 6,200 | 82.8 | **是** |

技术产出卡级 `count=1,514`、`averageScore≈0.9`，已排除 mock 子类并附 `countNote`。

### 4.3 工程校验

- `mvn -pl gkxlumen-display -am -DskipTests package -o`：**BUILD OK**（JDK17）
- `vue-tsc --noEmit`（`node_modules/.bin/vue-tsc.cmd`）：**exit 0**
- display 重启 7099 后两个端点均 200，无 5xx；`/v1/situation/factors/search` 因 search-py 未启动返回 `degraded:true`（预期降级）

## 5. 剩余缺口

| # | 缺口 | 现状 | 结论 |
|---|---|---|---|
| 1 | 会议 | 1,280 mock | 数仓无源；算法库 `M_INNOV_CONFERENCE_INFLUENCE` 完全不支持 |
| 2 | 技术产出·专利 | mock 1,820,000 / 96.1 | 算法库仅样本级（覆盖率 0.012%），不能全库排名 |
| 3 | 服务机构影响力 | mock 6,200 / 82.8 | 无 `M_SVC_ORG_TECH_SCORE` 全库产物（统计类服务机构已真实） |
| 4 | 论文影响力 | 真实但仅 ASJC 学科维 | 无单篇论文对象级榜（`M_INNOV_PAPER_INFLUENCE` 部分支持） |
| 5 | 集群分析 | 200 条真实散点，note「模型输出待核验」 | 口径未评审，非数据缺 |
| 6 | 收藏落库 / 反显 | 代码闭环；本地 401，`sys_user_relation` 0 行 | upms 未启动 / 无登录，端到端未验证 |
| 7 | 要素搜索 | `degraded:true` | search-py 8080 未启动（环境问题） |

## 6. 后续建议

1. 起 `search-py`（8080）让要素检索走真实检索。
2. 起 upms + 配置 `feign.upms.url` + 登录 token，端到端验证收藏写入与反显。
3. 专利影响力去 mock 需算法侧产出全库影响力分数（当前仅样本级）。
4. 会议如必须真实，需新增会议名录数据源（DOAJ / arXiv 均不含会议）。

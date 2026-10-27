# PORTAL-ENT-DEV-SRS-API-L01 · 门户企业发展四页签 · 需规对齐读接口与字段扩展（#58–#76）

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:api-agent` |
| supervised_by | `human:徐滕强` |
| claim_type | `pull` |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 查询侧最小 diff（IN 查询/字段透出/DTO 补字段），未新增依赖、未造抽象；D8/D9/可观测/架构铁律未跳过 |

## 任务背景与目标

对齐 `agent-handoffs/系统集成-SYSINT/PORTAL-ENT-DEV-API-REQUIREMENTS.md`（需规 75–78，#58–#76）：前端反馈 #62–#76 数据缺失/契约缺口；用户裁定生产/dev 读 demo 库现成数据、汇总表灌数方案（否决在线聚合，理由：上线后由算法 ETL 定时刷新，在线聚合届时还得改回）。

## 执行路径偏离说明

- registry 原记「在线聚合」方案 → **实际按用户 2026-10-26/27 两次裁定改为「汇总表灌数」**：`INSERT…SELECT` 从底表聚合喂给 bootstrap 已建的汇总表，接口侧保持 0 改动；上线后灌数程序由数据侧接管为正式 ETL。
- star 企业口径缺失（ES 无 `star_enterprise` 标签、DWD 无 `enterprise_star` 表）：**用户裁定等上线后灌 `enterprise_star` 表**，本叶仅按 unicorn∪gazelle 近似灌了 DWD 统计行，ES 侧 #72 列表=0 属数据缺口非代码缺口。

## 修改内容

### 数据侧（demo_gkxlumenx_dwd，database-mcp 执行；脚本 `lumen-svc-platform/db/9y_portal_ent_dev_seed.sql`，commit 375e581）

| 表 | 行数 | 内容 |
|---|---|---|
| enterprise_distribution | 43 | national 25 省 / global CHN / regional 粤 6 市 / city 深圳 11 区 |
| enterprise_industry_summary | 525 | 13 链 ×（历年 + 汇总）+ ALL |
| enterprise_year_stat | 556 | national / shenzhen / chain:* 历年新增+累计 |
| enterprise_chain_kpi | 13 | 每链 KPI |
| enterprise_qualification_matrix | 6 | 高企/上市/专精特新 × national/city |
| enterprise_stat_summary | 57 | key/star 节点·区·链 + qualification_count |
| enterprise_type_scale_stats | 25 | 类型×规模×深圳 |
| shenzhen_enterprise_summary | 85 | enterprise_total / key_enterprise_total / yearly_growth / industry_distribution |
| enterprise_base.region_id | 18.9 万 | 城市级国标码回填（深圳 95,600=440300） |

### Python（lumen-topic-py，branch dev）

| commit | 内容 |
|---|---|
| 746ca12 | E-32 多链：`OverviewRepository.industry_trend_multi`（IN 查询按链分组保序去重）；视图 `chain_codes` 多链路径 + `chain_code` 单链兼容 |
| 5436eed | 多链响应结构修正：`items=[]` + `multi_items=groups`（对齐 Java DTO，避免 items 字段撞车反序列化为 null） |
| a72c618 | DoD-3 卡片技术指标：#72/#76 `_source` 加 `statistics`，extract 透出 `patent_count`（=statistics.patent_valid_count）/`rd_ratio`（=statistics.rd_ratio），**不再依赖 #1 检索** |

### Java（lumen-svc-platform，branch dev，模块 gkxlumen-topic-enterprise）

| commit | 内容 |
|---|---|
| cd0880e | #69 计数修复：`KeyChainSubjectItem` 显式 `@JsonProperty("key_enterprise_count")`（Python 字段名与蛇形策略不一致致全 null） |
| 9272fa6 | E-32：`EnterpriseChainCodeRequest` 加 `chain_codes`；`IndustryTrendResponse` 加 `multi_items`（`ChainTrendGroupItem`） |
| ee4028e | DoD-3：`FeaturedEnterpriseItem` 补 `patent_count`/`rd_ratio` |

## 测试结果（线上 dev 网关 10.50.69.111:30892 实测）

| 接口 | 结果 |
|---|---|
| #62 industry-kpi | ✅ enterprise_total=189,115 / research_staff=14,530,656 / 13 链 / 高企 27,936 |
| #63 industry-comparison | ✅ 13 链全部有数 |
| #64 industry-trend 单链 | ✅ INB1309 68 年（1900–2026）有序 |
| #64 industry-trend 多链（E-32） | ✅ `chain_codes:[INB1309,INB170201]` → multi_items 2 组（68 年/41 年，total 186,610/5,267） |
| #65 distribution | ✅ national/global/regional/city 四维（广东 188,775=99.83%；global CHN 189,114） |
| #66 key-enterprise/kpi | ✅ 28,132 / 27,936 / 22 节点 / 1 区 |
| #67 chain-list INB1309 | ✅ 上中下游 groups（上游 3,876） |
| #68 industries | ✅ 国标行业树 |
| #69 chain-subject-stats | ✅ 计数恢复（INB1309=27,705） |
| qualification-summary | ✅ 6 类资质（科技中小 99,114 / 高企 62,583 / 专精特新 39,566…） |
| #70 type-scale-stats city | ✅ 类型×规模 25 行 |
| #71 star kpi | ✅ 覆盖 14 环节 / 1 区（总数 0 待 star 灌数） |
| #72 star list | ⚠️ total=0：ES 无 `star_enterprise` 标签（用户裁定等上线后灌 enterprise_star 表） |
| #73 sz kpi | ✅ 95,600 / 15,806 |
| #74 sz growth-trend | ✅ 2015–2026 累计 |
| #75 sz industry-distribution | ✅ 9 链 |
| #76 sz key-list | ✅ 3 家返回且新字段 patent_count/rd_ratio 已透出（此 3 家 ES 无专利数据故为 0/null）；列表偏少因 ES 索引 region_id 未回灌（DWD 已回填，等 ETL 重灌 ES，用户裁定与代码无关） |

自检：Python `py_compile` + AST 规则自检通过；Java javac DTO 编译 0 error（本机 mvn 因 nexus.mo.com 不可达无法 -am 全量，由 CI backend:build 兜底）。

## CI/CD

- 分支：双仓 `origin/dev`
- commit：svc-platform `cd0880e`/`9272fa6`/`ee4028e`；topic-py `746ca12`/`5436eed`/`a72c618`；seed `375e581`
- pipeline：svc-platform #3061/#3073、topic-py #3060/#3066/#3068（`py:smoke` 绿、镜像构建绿）
- 部署：ns=zhipu-tts；`deploy:topic-enterprise`×2 + `deploy:search-py`×2 手动触发全部 success（health: mock_enabled=false, es_available=true）
- dev 测试 URL：`http://10.50.69.111:30892/api/enterprise/topic/v1/**`（见上表）

## 架构合规自检（铁律逐条）

| 铁律 | 结论 |
|---|---|
| 1 算法只在 Python | ✅ 聚合 SQL 与查询改造全在 topic-py，Java 仅 DTO/透传 |
| 2 调用链 前端→Java→Python /internal | ✅ 未越层；#69/#64/#72/#76 均 Java 门面 → Python Feign |
| 5 CI/CD push→绿→rollout | ✅ 双仓 pipeline 绿 + 手动 deploy success + rollout 完成 |
| 7 共享聚合核心 | ✅ 前端只调 Java；Java 不写算法不连 nGQL |
| 8 数据策略 汇总表先行 | ✅ 灌数脚本落 `db/9y_portal_ent_dev_seed.sql` 可追溯、可重跑（幂等 DELETE+INSERT） |
| 9 D9 指标血缘 | ✅ 指标口径沿用注册表现值；灌数为 D4 侧填数，未改口径 |
| 12 demo/lumen 隔离 | ✅ 全部改动在 lumen-* 仓 dev 分支，未碰 demo-* |

## 遗留风险 / 移交事项

1. **star 口径**（用户已裁定）：等上线后灌 `enterprise_star` 表 + ES 打 `star_enterprise` 标签；此前 #72 列表为 0 属预期。
2. **ES 重灌**：DWD `enterprise_base.region_id` 已回填，需触发 ETL 重灌 ES 索引后 #76 列表数量才恢复（用户裁定与代码无关）。
3. **正式 ETL 归属**：seed 脚本为 demo 阶段一次性填数，上线后由数据侧接管为定时 ETL。
4. **前端联调**（DoD-4）：后端四 Tab 数据就绪，待 `SYSINT-04-04-L01` 前端按本 handoff 接口契约联调（USE_MOCK=false）。

## 涉及文件

- `repos/lumen-svc-platform/db/9y_portal_ent_dev_seed.sql`
- `repos/lumen-svc-platform/gkxlumen-topic-enterprise/gkxlumen-topic-enterprise-api/.../dto/EnterpriseChainCodeRequest.java`
- `repos/lumen-svc-platform/gkxlumen-topic-enterprise/gkxlumen-topic-enterprise-api/.../dto/EnterpriseExtendedDTOs.java`
- `repos/lumen-topic-py/gkx_common/repositories/overview.py`
- `repos/lumen-topic-py/gkx_search_service/views/enterprise_overview.py`
- `repos/lumen-topic-py/gkx_search_service/views/enterprise_star_enterprise.py`
- `repos/lumen-topic-py/gkx_search_service/views/enterprise_shenzhen.py`

## Cost（按 budget-estimate.md 四字段）

| 字段 | 值 |
|---|---|
| actual_tokens | ≈380000（含跨日联调与两轮部署验证） |
| model_used | glm-5.3-Flash |
| actual_cost | ≈$0.9 |
| cost_warn | green（< $10 阈值） |

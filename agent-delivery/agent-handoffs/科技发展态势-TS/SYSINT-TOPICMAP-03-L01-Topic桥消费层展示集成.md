# SYSINT-TOPICMAP-03-L01 · Topic 桥消费层（展示系统集成）

> **2026-11-05** · `agent:backend-agent` · 监管人 `human:李伟`
> **父任务**：SYSINT-TOPICMAP-02-L01（算法中台 Topic↔产业节点映射灌数，`agent:algorithm-agent` 淮政玮）
> **WBS 落点**：WBS-05-18 · DS-01 科技全域态势

## 1. 任务摘要

把产业领域筛选从「v3 产业码 → subfield（89/252 子学科有缺口）」升级为 **Topic 桥**：「集群码 CL-* → 久新官方 `ads_sz_gkx_industry_cluster_topic` → topic_ids → 各要素 `*_topic` 明细表」。本次落地消费层（展示 BFF + Python 门面），**不等待算法中台灌数**——久新官方映射表已实查 3098 行、15 集群全覆盖、全部 approved，可直接用作真源。

### 关键提升

| 项 | v3 现状 | Topic 桥后 |
|---|---|---|
| 专利学科过滤 | ❌ `ads_patent_profile` 无学科维度 → 诚实地返 null + note | ✅ `ads_patent_analysis_topic ⋈ ads_patent_profile`，36.5 万行 / run_id 取最新（2026-10-28），1990-2025 全量年度 |
| 6 集群 pending_vendor | ❌ 新能源/新材料/高端装备/绿色环保/海洋/未来能源选完不生效 | ✅ 全部 15 集群在 `ads_sz_gkx_industry_cluster_topic` 有映射 |
| 人才/机构 | `ads_geo_yearly_discipline_metrics(subfield_id)` 粗聚合 | topic_ids → topic→subfield 反推，聚合表仍可用；未来可改查明细 `*_topic` 表 |

## 2. 实查验证（2026-11-05 直连久新 Doris 只读库）

### 2.1 映射真源 `ads_sz_gkx_industry_cluster_topic`

| 指标 | 值 |
|---|---|
| 总行数 | **3,098** |
| 去重 topic | 1,491 |
| 去重 subfield | 67 |
| 去重 cluster_code | **15**（全覆盖） |
| review_status | 全部 `approved` |
| mapping_method | 全部 `SUBFIELD_INHERITANCE_AUTO_APPROVED` |
| industry_chain_stage | 有（UPSTREAM/MIDSTREAM/DOWNSTREAM，默认 MIDSTREAM） |

集群覆盖详表：

| cluster_code | cluster_name_zh | topic 数 |
|---|---|---|
| CL-FUT-01 未来制造 | 254 | CL-FUT-02 未来信息 317 |
| CL-FUT-03 未来能源 | 28 | CL-FUT-04 未来空间 82 |
| CL-FUT-05 未来健康 | 327 | CL-SEI-01 新一代信息技术 420 |
| CL-SEI-02 生物产业 | 289 | CL-SEI-03 新能源 **113** ← 之前 pending_vendor |
| CL-SEI-04 新材料 **204** ← pending_vendor | CL-SEI-05 高端装备 **271** ← pending_vendor |
| CL-SEI-06 智能网联新能源汽车 | 339 | CL-SEI-07 绿色环保 **157** ← pending_vendor |
| CL-SEI-08 低空经济与空天 | 134 | CL-SEI-09 传统与创意产业 100 |
| CL-SEI-10 海洋产业 **63** ← pending_vendor | — | — |

### 2.2 各要素 `*_topic` 明细表

| 要素 | 表 | 行数 | topic 字段 | 可 topic 过滤 |
|---|---|---|---|---|
| 人才 | `ads_talent_topic_profile` | 6,846,951 | `topic_id` | ✅ |
| 机构 | `ads_institution_topic_entry` | 3,358,401 | `topic_id` | ✅ |
| 论文 | `ads_paper_profile` | ~400 万 | `primary_topic_id` + `topic_ids[]` | ✅ primary_topic_id（**避开**数组字段 ARRAY_CONTAINS，慢 2x+） |
| 专利 | `ads_patent_analysis_topic` | **365,610** | `topic_id` + `run_id` | ✅ run_id 取最新 `e4dcc585`（2026-10-28），5 个版本数据全同 |
| 项目 | `ads_project_topic` | 11,374,389 | `topic_id` + `is_primary` | ✅ |
| 课题 | `ads_research_problem_discipline` | — | `topic_id` | ✅ |

### 2.3 查询性能（久新 Doris 256MB 内存限制）

| 查询 | 耗时 | 备注 |
|---|---|---|
| 人才 topic_id IN(3) | **553 ms** | 有索引，OK |
| 机构 topic_id IN(3) | **1,083 ms** | OK |
| 论文 primary_topic_id IN(3) | **1,856 ms** | 单列 IN |
| 论文 ARRAY_CONTAINS(topic_ids, 'x') | ~3,500 ms | ⚠️ 慢 2x+，**避开**用 primary_topic_id |
| 专利（36 万小表） | 预计 < 200 ms | ✅ |

### 2.4 专利 run_id 版本口径（阻塞项已确认）

5 个 run_id 数据**完全相同**（`metrics_as_of_date` 都 = 2026-09-18，3484 topic，73122 行 / 版本），只是不同时间戳的重复写入。**取最新 `e4dcc585` 即可**。

### 2.5 Topic↔Subfield 从属关系

`ads_discipline_topic.subfield_id` 是 NOT NULL 外键，**topic→subfield 1:N 从属关系已由久新官方保证**。展示层只需一次 `SELECT DISTINCT subfield_id FROM ads_discipline_topic WHERE topic_id IN (...)` 即可反推聚合表（只有 subfield 列）需要的 subfield_ids。

## 3. 改动清单（5 文件，两仓）

### Python `gkx_show_service`（repo: `lumen-topic-py`）

| 文件 | 改动 |
|---|---|
| `gkx_show_service/views/meta.py` | 新增 `POST /internal/gkx-show/topic/from-cluster`：`cluster_codes CL-*` → 久新 `ads_sz_gkx_industry_cluster_topic` 反查 `topic_ids[]` + `subfield_ids[]`；含白名单校验（CL- 前缀、上限 15）、JiuxinUnavailable 降级 |
| `gkx_show_service/views/geo_indicator.py` | `factor_metrics` 增 `topic_ids` 白名单解析 + topic→subfield 反推 |
| `gkx_show_service/views/monitor_indicator.py` | `yearly_trend` + `overview_kpi` 同上（replace_all 两函数）；**专利段升级** topic_ids 有值时改查 `ads_patent_analysis_topic ⋈ ads_patent_profile`（JOIN patent_id），`WHERE run_id = 最新 AND topic_id IN (...) AND YEAR(publication_date) = %s` |

### BFF `gkxlumen-display`（repo: `lumen-svc-platform`）

| 文件 | 改动 |
|---|---|
| `feign/RemoteShowPythonClient.java` | 新增 `topicFromCluster()` Feign 方法，`@NoToken @PostMapping("/internal/gkx-show/topic/from-cluster")` |
| `controller/SituationController.java` | ① `TopicResolution` record（topicIds + subfieldIds + note）<br>② `resolveTopicIdsFromCluster(Scope)`：调 show-py 新端点<br>③ `kpiBodyOf` / `regionFactorsOf` / `yearlyTrendBodyOf` 三方法增 topicIds 参数<br>④ `map` + `overview` 两端点接入 TopicResolution，topic 桥 subfield 覆盖旧 subfieldIds<br>⑤ **保留旧 `resolveSubfieldIds`（v3 innov subfield 路径）** 作降级——久新 Doris 不可用时回落到 innov subfield_topic_map |

## 4. 数据流变更前后

```
变更前（v3 subfield 核心）：
  前端 CL-* / INB* → BFF resolveSubfieldIds(innov) → subfield_ids → Python → discipline_metrics 聚合表
  专利：ads_patent_profile 无学科维度 → 诚实返 null + note

变更后（topic 核心）：
  前端 CL-* → BFF resolveTopicIdsFromCluster(show-py) → topic_ids + subfield_ids（topic 反推）
    → Python topic_ids 优先 → *_topic 明细表（人才/机构/专利/项目/课题/论文 primary_topic_id）
    → Python subfield_ids（降级）→ discipline_metrics 聚合表
```

## 5. 自检

| 项 | 结果 |
|---|---|
| `mvn compile -pl gkxlumen-display -am`（JDK 17） | ✅ exit 0 |
| VS Code Java 诊断（2 文件） | ✅ 零错误 |
| `python -m py_compile`（3 文件） | ✅ 零错误 |

## 6. 遗留事项

| 项 | 状态 | 说明 |
|---|---|---|
| Python 服务（:8082）重启 | ⏸️ 待执行 | 本地改完未重启，徐滕强接管 |
| BFF（:7099）重打包重启 | ⏸️ 待执行 | Maven compile OK → package 后替换 jar |
| 联调验证 | ⏸️ 待执行 | 选 CL-SEI-01 → overview 看专利是否真实联动 |
| 前端 subfield 死代码清理 | 📋 后续 | 等联调绿后统一清理 |
| 算法中台 `dwd_topic_industry_map` 同步消费 | 📋 后续 | 消费层可同时支持两种映射源（降级用），当前直连久新官方表 |
| `ads_paper_profile.topic_ids[]` 多 topic 场景 | ⚠️ 暂用 primary_topic_id | 多 topic 归属需 ARRAY_CONTAINS，慢 2x+，降精度处理 |
| adsdb.py / svc_factor.py | ℹ️ 本次未改 | 与 Topic 桥无关 |

## 7. 改动文件清单

```
lumen-svc-platform/gkxlumen-display/src/main/java/...
  controller/SituationController.java
  feign/RemoteShowPythonClient.java

lumen-topic-py/gkx_show_service/views/
  meta.py
  geo_indicator.py
  monitor_indicator.py
```

其他遗留改动（SituationMockProvider / ShenzhenInnovationController 等）为 **之前 session 遗留**，本次不纳入 commit 范围。

## 8. 证据

- 久新实查 SQL + 结果（本次会话直接 mysql -h 47.93.119.170 -P 29030 取得）
- [Topic桥可行性判定.md](../../工程过程/04-系统集成/02-对接三要素/调研/Topic桥可行性判定.md)
- [SYSINT-TOPICMAP-02-L01.md](../../系统集成-SYSINT/SYSINT-TOPICMAP-02-L01.md)（父任务，算法中台灌数）

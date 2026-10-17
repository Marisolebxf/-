# 派单包：FIX-TOPIC-SEARCH-PY-DWD-PREFIX-L01（bugfix · v1.0）

- **派单方**：coordinator（architect-agent 起草）
- **执行 Agent**：`data-agent`
- **监管人**：human:徐滕强（dispatch-rules.yaml#agent_supervisors；2026-08-03 起 data-agent 默认监管）
- **仓**：`demo-svc-topic-py`（`${GKX_ROOT}/repos/demo-svc-topic-py`，子项目 `gkx_search_service/`）
- **服务**：`gkx-search-service`（镜像 `harbor.htmisoft.net/gkx/gkx-search-service:ec1ff14d`；K8s `demo-platform-search-py`，ns `dev`）
- **Epic**：`E-PLATFORM`
- **状态**：`backlog`（待 PM/监管人 confirm 后 `ready` 认领）
- **任务类型**：`bugfix` · P0
- **依赖**：无（独立 bugfix；`DEVOPS-TOPIC-PY-CICD-L01` 已 done，CI/CD 通道可用）
- **架构真源**：`agent-delivery/observability.md` §9（trace 查询入口）

---

## 0. 故障现场（Trace 证据）

| 项 | 值 |
|---|---|
| Trace 1 | `6ede6064ae21cef8709de017d5eb7c55`（2026-08-03 13:08 · 企业画像专利明细） |
| Trace 2 | `1d54b14aa8ef76d13b253352a6efc9c2`（2026-08-03 13:09 · 企业画像风险全量） |
| 前端入口 | `POST /enterprise/topic/v1/profile/patent`、`POST /enterprise/topic/v1/profile/risk/all` |
| 结果 | 前端 500 |

**调用链**（两笔一致，Tempo 已核）：
```text
FE → gkxlumen-gateway
   → gkxlumen-topic-enterprise-biz (Java, Feign)
   → demo-platform-search-py (gkx-search-service, Python)   ← 故障源
   → MySQL 192.168.88.43:3306 / gkxlumenx_dwd
```

**错误链**：
- Java span 异常事件：`FeignException$ServiceUnavailable: [503] POST http://topic-enterprise-python/internal/gkx-search/profile/patent`
- Python span 异常消息：`MySQL 查询专利明细失败：(1146, "Table 'gkxlumenx_dwd.dwd_enterprise_patent_detail' doesn't exist")`
- Trace 2 同理：`dwd_risk_judicial_case doesn't exist`
- Java 将 Python 503 包装为 500 返回前端

---

## 1. 根因（已逐层验证）

**Python `gkx_search_service` SQL 硬编码了 PG 时代 `dwd_` 前缀表名；迁移到 MySQL 后表名不带前缀，二者不匹配。**

- 迁移依据：`agent-delivery/agent-handoffs/algo-pg-to-mysql-migration.md` §14（PG schema `dwd` → MySQL database `gkxlumenx_dwd`，**表名本身无 `dwd_` 前缀**）
- 实测 `gkxlumenx_dwd` 共 101 张表，**仅 `dwd_sz_city_benchmark` 一张带前缀**
- 代码硬编码（12 张 + 风险 18 类）：`dwd_enterprise_patent_detail` / `dwd_enterprise_invest` / `dwd_enterprise_patent_history` / `dwd_enterprise_stat_summary` / `dwd_enterprise_type_scale_stats` / `dwd_enterprise_region_summary` / `dwd_enterprise_industry_distribution` / `dwd_enterprise_industry_summary` / `dwd_enterprise_growth_trend` / `dwd_enterprise_distribution` / `dwd_enterprise_risk_summary` / `dwd_shenzhen_enterprise_summary` / 18 类 `dwd_risk_*`
- MySQL 实际表名：`enterprise_patent_detail` / `enterprise_invest` / `enterprise_patent_history` / … / `risk_judicial_case` / `risk_*`（无前缀）
- **表结构字段对得上**（均含 `org_id`），纯表名不匹配
- 服务当前 `GKX_MOCK_ENABLED=0`（真实连 MySQL），故直接抛 1146

### ⚠️ 附带问题：专利明细列名也需核对

`enterprise_profile.py` 专利明细 SQL 用了 PG 时代列名（`publication_number` / `title_zh` / `title_en` / `abstract_zh` / `grant_number` / `ipc_main` / `cpc_main` / `inventor` / `applicant_name` / `assignee_name` / `citation_count` / `cited_by_count`），而 MySQL `enterprise_patent_detail` 实际列是 `patent_id` / `patent_name` / `patent_type` / `filing_date` / `publish_date` / `legal_status` / `ipc_code` 等。**表名改对后若列名仍不匹配，接口依然报错**——修复时须一并对齐列名（以 `agent-delivery/data/data-design/企业/DWD表结构设计-企业模块.md` 为真源）。

---

## 2. 修复范围

| # | 文件（`gkx_search_service/views/`） | 改动 |
|---|---|---|
| 1 | `enterprise_profile.py` | 专利明细：`dwd_enterprise_patent_detail` → `enterprise_patent_detail`；**列名对齐 MySQL**（`publication_number`→`patent_id` 等，按 DWD 表结构设计） |
| 2 | `enterprise_risk.py` | 18 类风险配置表 `dwd_risk_*` → `risk_*`（含 `has_party` JOIN 的 `dwd_risk_*_party` → `risk_*_party`） |
| 3 | `enterprise_detail_patent.py` | `dwd_enterprise_patent_history` → `enterprise_patent_history` |
| 4 | `enterprise_detail_supply.py` | `dwd_enterprise_invest` → `enterprise_invest` |
| 5 | `enterprise_distribution.py` | `dwd_enterprise_distribution` → `enterprise_industry_distribution`（**注意：确认代码意图**，可能对应 `enterprise_industry_distribution` 或 `enterprise_industry_summary`，以 DWD 设计为准） |
| 6 | `enterprise_key_enterprise.py` | `dwd_enterprise_stat_summary` → `enterprise_stat_summary`；`dwd_enterprise_type_scale_stats` → `enterprise_type_scale_stats` |
| 7 | `enterprise_overview.py` | `dwd_enterprise_region_summary`→`enterprise_region_summary`；`dwd_enterprise_industry_distribution`→`enterprise_industry_distribution`；`dwd_enterprise_growth_trend`→`enterprise_growth_trend`；`dwd_enterprise_industry_summary`→`enterprise_industry_summary` |
| 8 | `enterprise_detail_basic.py` | 仅注释提及 `dwd_tag_dict`，核对是否实际查询；若查 `tag_dict` 无需加前缀 |
| 9 | 全仓 grep | `dwd_enterprise_` / `dwd_risk_` 归零（注释可保留说明，但运行时 SQL 必须对齐） |

> `dwd_sz_city_benchmark`、`tag_dict`、`chain` 等已用 `gkxlumenx_dwd.` 前缀（可通），**不动**。

---

## 3. 禁止

- 修改 `demo-algo-science` / `demo-algo-ent-analysis`（算法灌数据仓，与本次检索修复无关）
- 修改 Java `lumen-svc-platform`（Java 侧无需改动，Feign 链路正常，只是 Python 返 503）
- 修改 MySQL 表名/建库（业务表结构归 data 侧，本次只对齐代码引用）
- 改 `GKX_MOCK_ENABLED` 掩盖问题（可临时 Mock 缓解，但修复目标是真实出数）
- 引入 ORM 或重写查询逻辑（最小 diff，仅表名/列名对齐）

---

## 4. DoD（已登记 registry）

1. `gkx_search_service` 全部 SQL 表名去掉 `dwd_` 前缀，与 `gkxlumenx_dwd` 库实际表名对齐（含 18 类 `dwd_risk_*`）
2. 专利明细接口字段列名对齐 MySQL 实际列，pymysql 查询出数
3. 风险全量接口 18 类风险明细表名逐一对齐，出数
4. 全仓 grep `dwd_enterprise_` / `dwd_risk_` 归零；`py_compile` / import 全绿
5. dev 环境 `gkx-search-service` 重新部署后：Tempo 链路可见，`/profile/patent` 与 `/profile/risk/all` 返回 200，无 1146 错误
6. handoff（`agent-delivery/agent-handoffs/FIX-TOPIC-SEARCH-PY-DWD-PREFIX-L01.md`）含范围/偏离/证据/架构合规/cost 四字段回填

---

## 5. 验收路径（监管人/QA 可执行）

1. 本地仓 `py_compile` / import 通过；全仓 grep 归零
2. 构建推镜像（CI 见 `DEVOPS-TOPIC-PY-CICD-L01`，harbor `gkx/gkx-search-service`）
3. K8s `demo-platform-search-py` 滚动更新
4. 通过前端页面触发专利明细 / 风险全量，或直接 curl Java 网关：
   - 响应 200；Network 响应头含 `traceparent` / `X-Trace-Id`
5. Grafana `http://192.168.88.34:3000（**旧环境已废弃**；现网 Grafana：$newGf）` → Tempo → 粘贴新 traceId，确认 gateway → topic-enterprise-biz → search-py 三段均 ok（见 `observability.md` §9）

---

## 6. 架构合规自检（预期）

| 铁律 | 说明 |
|---|---|
| D2 调用链 FE→Java→Python | ✅ 未改链路 |
| D4 可观测性 | ✅ 修复后 Tempo 链路绿即为验收项 |
| D5 CI/CD | ✅ 走既有 pipeline |
| D8 Design.md | N/A（Python 检索服务） |
| D9 数据血缘 | ✅ 表名对齐不改变血缘；字段口径以 DWD 设计为真源 |

---

## 7. Cost（预估）

| 字段 | 值 |
|---|---|
| `model_used` | cursor-grok-4.5（待执行 agent 回填） |
| `estimated_tokens` | ~40k |
| `difficulty` | M |
| `effort_points` | 3 |

---

## 8. 下一任务

- 修复后若有其他模块同源问题（`dwd_shenzhen_enterprise_summary` ↔ `shenzhen_policy_*` 对应关系待执行时确认），在 handoff 中记录，另开 follow-up 单。

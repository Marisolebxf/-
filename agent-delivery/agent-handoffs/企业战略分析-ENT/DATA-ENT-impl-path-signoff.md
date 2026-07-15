# Data handoff：DATA-ENT-IMPL-PATH

- 时间：2026-07-15
- 作者：data-agent（资深数据工程师 + Python 微服务开发）
- 支撑基线：`企业维度-Python微服务架构预设计.md` v1.3、`企业搜索-ES索引设计.md` v3.4、`docs/API-接口文档.md` v14.0
- commit 标记：`[agent:data-agent] feat(ent-search): 企业检索+详情 Python 微服务初版实现`
- 仓库：`gkx-lumen/demo-svc-topic-py`
- 分支：`dev`
- commit SHA：`0657816`
- CI/CD：GitLab 仓已创建；Pipeline/CI 配置待后续补充（pipeline_waiver active 期间跳过）

## 产物清单

| 产物 | 路径（相对 `demo-svc-topic-py/`） | 说明 |
|------|-----------------------------------|------|
| FastAPI 入口 | `gkx_search_service/main.py` | 应用入口，注册全部 15 个 router，76 个端点列表 |
| 公共库（6 模块） | `gkx_common/` | config / db / es / mock / nebula / observability / response |
| 企业搜索 view | `gkx_search_service/views/enterprise_search.py` | 关键词搜索/智能搜索/高级筛选/联想/聚合/批量查/推荐 |
| 企业详情 view | `gkx_search_service/views/enterprise_profile.py` | 全景画像/card 弹框/新闻/招投标/供应链/股东/投资 |
| 企业图谱 view | `gkx_search_service/views/enterprise_graph.py` | subgraph + expand（NebulaGraph + Mock 兜底） |
| 企业风险 view | `gkx_search_service/views/enterprise_risk.py` | 18 类风险明细（summary/all/逐类分页） |
| 企业专利 view | `gkx_search_service/views/enterprise_detail_patent.py` | 专利明细/统计 |
| 企业财务 view | `gkx_search_service/views/enterprise_detail_finance.py` | 财务快照/趋势 |
| 企业融资 view | `gkx_search_service/views/enterprise_detail_financing.py` | 融资事件/统计 |
| 企业分布 view | `gkx_search_service/views/enterprise_distribution.py` | 四维度地图热力（全球/全国/地区/深圳） |
| 企业总览 view | `gkx_search_service/views/enterprise_overview.py` | KPI/产业分布/增长趋势/区域热力 |
| 重点企业 view | `gkx_search_service/views/enterprise_key_enterprise.py` | 重点企业总数/产业链主体/资质摘要/交叉统计 |
| 明星企业 view | `gkx_search_service/views/enterprise_star_enterprise.py` | 明星企业/KPI |
| 深圳企业 view | `gkx_search_service/views/enterprise_shenzhen.py` | 深圳企业统计/趋势/分布/重点企业 |
| 高级筛选 meta | `gkx_search_service/views/meta.py` | regions/company-types/scales/tags/filters 码表 |
| 配置 | `conf/settings.yaml` | Mock/ES/PG/Nebula 连接配置 |
| API 文档 | `docs/API-接口文档.md` | 76 端点完整文档（含 Feign Client 示例） |
| Dockerfile | `docker/Dockerfile.search` | 检索服务容器化 |
| 测试 | `tests/test_enterprise_search.py` | 231 个 pytest 测试 |
| DWD 表设计 DDL | 主仓 `agent-delivery/data/data-design/dwd_enterprise_ddl.sql` | 企业模块 DWD 表 DDL |

## 范围与实现

### 架构概览

```
前端 (lumen-ui-topic) → 网关 → Java (gkxlumen-topic)
                              ↓ POST /api/gkx-search/**
                        Python (demo-svc-topic-py gkx_search_service)
                              ↓
                    ┌─────────┼─────────┐
                    ES        PG        NebulaGraph
               (gkx_enterprise) (DWD)   (entan space)
               检索/聚合/统计     详情明细     关系图谱
```

### 已实现功能模块（76 端点）

| 模块 | 端点数 | 数据源 | 说明 |
|------|--------|--------|------|
| 企业搜索 | 7 | ES | keyword/smart/advanced/suggest/aggregations/by-codes/hot |
| 企业对比 | 1 | ES | 最多 10 家企业对比 |
| 企业详情画像 | 12 | ES+PG | 全景/弹框/基础/新闻/招投标/供应链/股东/投资/专利/财务/融资 |
| 风险模块 | 20 | PG DWD | summary/all + 18 类风险各独立分页 |
| 企业图谱 | 2 | NebulaGraph+Mock | subgraph/expand |
| 企业发展概况 | 4 | DWD 预聚合 | KPI/产业分布/增长趋势/区域热力 |
| 重点企业 | 5 | ES+DWD | 总数/产业链分组/主体统计/资质/交叉统计 |
| 明星企业 | 3 | ES+DWD | KPI/明星企业/覆盖 |
| 深圳企业 | 4 | ES+DWD | 统计/趋势/分布/重点企业 |
| 企业分布 | 1 | DWD 预聚合 | 4 维度地图（全球/全国/地区/深圳） |
| 高级筛选 meta | 5 | DWD+Fixed | 地区码表/企业类型/规模/标签/枚举 |
| NebulaGraph 公共库 | - | - | gkx_common/nebula.py + nebula_graph.py |

### Mock 策略

- 默认开启（`conf/settings.yaml` → `mock.enabled: true`）
- Mock 数据生成 20 家企业，覆盖全部 ES 字段
- 无需 ES/PG/Nebula 即可独立运行和调试
- 图谱接口返回 `source: mock`，真实 Nebula 连接后自动切换为 `source: nebula`
- 司法风险返回 `source: mock` 标注

### 删除的废弃接口（v14.0）

- `POST /profile/judicial` → 已由 `/profile/risk/all` + 18 类风险接口替代
- `POST /profile/relation-graph` → 已由 `/profile/graph/subgraph` + `/profile/graph/expand`（NebulaGraph）替代

### 关键设计决策

| 决策 | 选择 | 理由 |
|------|------|------|
| URL 标准 | `/api/{project}/{module}/{action}` | 统一前缀便于负载均衡配置；POST 全 JSON Body，无路径参数 |
| 高级筛选 | 前端构造 JSON 查询树 | 支持任意 AND/OR 组合 + 8 种运算符 + 18 过滤字段 |
| 企业总数去重 | 预聚合表存 `chain_code='ALL'` 特殊行 | 一家企业可属多个产业，不可简单相加 |
| 企业分布 | DWD 预聚合表 | 百万级企业实时 ES 聚合性能不可控；~274 行表毫秒级查询 |
| 关系图谱 | NebulaGraph 为主存 + Mock 兜底 | D3 铁律规定；PG 镜像暂不实现 |
| 司法风险 | 18 张独立表 + 映射表 + 汇总表 | 2 亿行级数据避免单表过大；支持多企业关联同一案件 |

## 架构合规自检

| 铁律 | 合规 | 说明 |
|------|------|------|
| D1: 算法只在 Python | ✅ | Java 无算法代码 |
| D2: 调用链不可越层 | ✅ | 前端 → Java → Python，Python 不对外暴露 |
| D3: 图谱用 NebulaGraph | ✅ | NebulaGraph Space `entan`；禁止 Neo4j |
| D4: 可观测性 | ✅ | `observability.py` 含 OTel 集成（`gkx_common/observability.py`） |
| D5: CI/CD | ⚠️ | GitHub 仓已创建；CI/CD Pipeline 配置待补充（已登记 waive） |
| D6: demo2 只读 merge 铁律 | ✅ | 本仓为新建独立仓 |
| D7: 共享聚合核心 | ✅ | Python 只调 ES/PG，不写算法逻辑 |
| D8: 前端规范 | ✅ | 本仓为 Python 后端服务，不涉及前端 |
| D9: 数据血缘 | ✅ | API 文档每个接口标注数据源；Mock 数据含 🧪 Badge |
| D10: 交互规范 | ✅ | 不涉及前端交互 |

## 偏离说明

| 偏离项 | 说明 | 原因 |
|--------|------|------|
| 未注册到 `repo-registry.yaml` | `demo-svc-topic-py` 是新仓，未在 repo-registry 中登记 | 新仓，待后续 RFC 或 PM 决议后补登 |
| CI/CD Pipeline | 未配置 `.gitlab-ci.yml` | pipeline_waiver active 期间跳过（`gkx-orchestration` task-registry §40-49） |
| 图谱 PG 镜像 | 未实现 PG fallback | 用户明确要求"现阶段不用 PG 兜底" |
| 股东数据 | 仅返回 Mock + `note: "DWD 无此表"` | 上游未提供股东数据源 |

## 验收证据

- **本地测试**：231 pytest 全部通过
- **服务启动**：`uvicorn gkx_search_service.main:app --port 8090`，Mock 模式正常返回
- **Swagger UI**：`http://localhost:8090/docs` 76 端点完整
- **GitLab 仓库**：`https://gitlab.htmisoft.net/gkx-lumen/demo-svc-topic-py`
- **本地 commit**：`0657816`（分支 `dev`）

## 待办事项

| 优先级 | 事项 | 负责人 |
|--------|------|--------|
| P0 | 推送代码到 GitLab：`cd ~/Desktop/xtq/projects/gdf/projects/repos/demo-svc-topic-py && git push -u origin dev` | 开发者 |
| P1 | 补充 `.gitlab-ci.yml` Pipeline 配置 | DevOps |
| P1 | 登记 `demo-svc-topic-py` 到 `repo-registry.yaml` | coordinator |
| P2 | ES 索引创建 + 数据灌入后关闭 Mock 模式 | data-agent |
| P2 | NebulaGraph 正式连接后验证图谱查询 | data-agent |
| P3 | 股东数据上游接入后补充 DWD 表 + 实现 | data-agent |

---

**Handoff 编写**：data-agent（2026-07-15）
**评审建议**：请 PM/architect 确认后签收

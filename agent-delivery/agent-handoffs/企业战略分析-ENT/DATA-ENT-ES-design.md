# Data handoff：DATA-ENT-ES-design

- 时间：2026-07-02
- 作者：data-agent（资深数据工程师 + 数据架构师）
- 支撑基线：`企业维度-Python微服务架构预设计.md` v1.3、`企业搜索-ES索引设计.md` v2.2、`企业搜索-ES更新机制.md` v1.0
- commit 标记建议：`[agent:data-agent] 企业搜索 ES 索引设计/更新机制/样例数据 + 企业模块详细设计`

## 产物清单

| 产物 | 路径（相对主仓根） | 说明 |
|------|-------------------|------|
| ES 索引设计 | `agent-delivery/data/data-design/企业搜索-ES索引设计.md` | v2.2，含 mapping/settings/分析器/字段分层策略/字段含义表/样例查询 |
| ES 更新机制 | `agent-delivery/data/data-design/企业搜索-ES更新机制.md` | v1.0，按源表独立模块并行同步 + Painless script 局部更新 |
| ES 样例文档 | `agent-delivery/data/data-design/sample-enterprise-doc.json` | 软通动力样例（部分真实 + 部分 Mock） |
| 企业模块详细设计 | `agent-delivery/data/data-design/企业模块-详细设计.docx` | 9 子模块功能点/接口/表/SQL/数据缺口/算法需求 |
| Python 微服务架构预设计 | `agent-delivery/企业维度-Python微服务架构预设计.md` | v1.3，4 Python 服务 + 1 Java 业务服务（gkxlumen-topic 全包） |

## 范围与实现

### ES 索引设计（gkx_enterprise 索引）

- **索引名**：`gkx_enterprise`（别名机制，零停机重建）
- **`_id`**：`org_id`（32 位 MD5，保证全量企业唯一性和存在性）
- **文档量**：~1500 万（全国在营企业）
- **核心结构**：
  - 顶层字段：基础信息/上市/行业/经营状态/风险等级等（用于排序和过滤）
  - nested 字段：tags / executives / financials（全部年份）/ financings / bids / patents / innovation_carriers / industry_chains / news / supply_chain_relations
  - statistics（nested, dynamic:false）：各维度预计算汇总（patent_total / bid_total / latest_revenue 等）
  - flat 数组：industry_chains_flat / industry_node_codes_flat 等（用于聚合）
- **字段分层策略（§2.4）**：
  - ES 存：搜索/过滤/聚合/排序需要的字段（含 bids/patents 大 nested）
  - PG 存：仅详情页展示的高体积数据（司法明细 12 张表，只灌计数到 ES）
- **性能配置**：`nested_objects.limit` 调高至 100000；列表页查询用 `_source.excludes` 排除大 nested

### ES 更新机制（v1.0 重构）

- **核心方案**：17 个独立同步模块，每个源表一个模块，各自扫描昨日增量，各自只更新自己的 ES 字段
- **更新方式**：全部用 Painless script 局部更新（`ctx._source.xxx = params.xxx`），不用全文档 PUT，避免并发覆盖
- **大 nested（bids/patents）**：script 按 id 去重追加，无需 GET 全文档
- **并发安全**：ES 文档级锁排队执行 + `retry_on_conflict=5` 自动重试
- **refresh_interval**：保持 30s 不变（减少 segment 生成频率，对批量写入友好）
- **调度**：凌晨 02:00 触发，17 模块并行（最多 5 并发），单模块失败不影响其他
- **全量重建**：每周日凌晨，别名零停机切换，Bulk index 全文档写入新索引

### Python 微服务架构（v1.3）

- **Python 层 4 服务**：gkx-search-service / gkx-graph-service / gkx-analytics-service / gkx-ai-service
- **Java 层 1 业务服务**：gkxlumen-topic（全包：专题 7 要素 + 展示域 + 指标注册查询）
- **铁律**：所有数据含指标元数据均经 Python `/internal/*`，Java 不直读任何数据库表

### 企业模块详细设计

- 9 子模块：企业概览 / 重点企业类型分析 / 重点企业领域分布分析 / 企业能力评估 / 深圳企业现状分析 / 供应链协同分析 / 企业发展支持 / 企业引育决策 / 企业竞争力分析
- 每个子模块含：功能点、接口设计、PG 源表、SQL 查询口径、数据缺口分类（结构缺口/数据缺口/待甲方确认）

## 偏离说明

| 偏离 | 理由 | as-built |
|------|------|----------|
| `_id` 用 `org_id` 而非 `social_credit_code` | 部分企业（外资）无统一信用代码 | org_id 全量唯一存在 |
| 司法明细走 PG 不灌 ES | 拼多多等企业司法数据量导致单文档十几兆 | ES 只存计数 + 风险等级，明细按需查 PG |
| ES 更新从"全文档重写"改为"按源表独立模块并行 script 局部更新" | 旧方案一个字段变更导致全文档重写，浪费严重 | 17 模块并行，各写各的字段 |

## 验收证据

- [x] ES 索引设计文档完成（v2.2，含字段分层策略）
- [x] ES 更新机制文档完成（v1.0，含 Painless script 示例 + 17 模块清单）
- [x] 样例 ES 文档生成（软通动力，含 financials/financings/bids/patents/statistics）
- [x] 企业模块详细设计完成（9 子模块，含 SQL 口径 + 数据缺口分类）
- [x] Python 微服务架构设计完成（v1.3，图文一致性校验通过）
- [ ] CI 绿（设计类文档，cicd: skip）
- [ ] K8s dev URL（设计阶段无部署）

## 架构合规自检（公约 §2 十条逐条）

1. ✅ 算法只在 Python（ES ETL 同步脚本归属 Python search-service）
2. ✅ 调用链不越层（前端 → Java → Python → ES/PG，Python `/internal/*` 不对外）
3. ✅ 图谱用 NebulaGraph（ES 更新机制不涉及图谱，但架构设计里 graph-service 用 Nebula）
4. ✅ 可观测性（ES 同步模块有健康检查接口 + OTel tracing）
5. ✅ CI/CD（设计类文档 cicd: skip，后续 ETL 脚本 push → Pipeline → K8s）
6. ✅ demo2 只读 merge 铁律（不涉及）
7. ✅ 共享聚合核心方案 A（Java gkxlumen-topic 全包，两前端共享）
8. ✅ 数据策略（标准表 ADS 先行 + Mock 填充）
9. ✅ 前端规范唯一来源 D8（ES 设计为后端数据层，不涉及前端 UI 规范）
10. ⚠️ 数据血缘铁律 D9（ES 索引 statistics 字段的统计指标尚未标注 metric_id，列为 P1 待补）

## 影响下游

- **api-agent / frontend-agent**：ES 索引结构 = 搜索接口的返回字段契约；`_source` 过滤策略影响列表页性能
- **algorithm-agent**：`competitiveness_score` 由 ai-service 计算，ES 只存结果
- **architect-agent**：ES 更新机制从全文档重写改为 script 局部更新，需架构评审确认
- **devops**：ES 集群需配置 `nested_objects.limit=100000`、堆内存 ≥32GB

## P1 待补项（不影响本次交付）

- [ ] ES 索引 statistics 字段标注 metric_id（D9 数据血缘铁律）
- [ ] sample-enterprise-doc.json 标注 Mock 字段（🧪 MockBadge）
- [ ] `企业模块-详细设计.docx` 注册到 formal-docs-registry.yaml
- [ ] ES 集群配置细化（分片/副本/内存/磁盘）
- [ ] IK + 拼音插件安装文档

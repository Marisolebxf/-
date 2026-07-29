# 派单：重点企业分析 + 深圳企业现状分析（Python / Java / 前端）

> **派单人**：[agent:architect] supervised_by human:徐滕强  
> **日期**：2026-07-29  
> **Epic**：E-ENT-SCRUM-PDR  
> **设计文档**（v2.3 / v1.3，已补齐全部接口 JSON spec）：  
> - `agent-delivery/data/data-design/企业/重点企业分析-功能设计.md`（v2.3）  
> - `agent-delivery/data/data-design/企业/深圳企业现状分析-功能设计.md`（v1.3）  

---

## 一、设计文档核验结论（架构师已签）

| 维度 | 重点企业分析 | 深圳企业现状分析 |
|------|------------|----------------|
| 字段覆盖 | ✅ Tab A 全覆盖；Tab B ES `core_tech_tags_flat` + 5 张 DWD 表 | ✅ Tab A 全覆盖；Tab B v1 `ent_sz_status` ADS 表 |
| 性能 | ✅ 重点企业子集 ≤10 万，ES terms/filter 50-200ms | ✅ 深圳子集 ≤1 万，ES 80-200ms；Tab B 读 ADS <50ms |
| 需新建表 | 0 张 | `dwd_code_city_area`（可选，demo Mock）；`ads.ent_sz_status` 从 v1 迁移 |
| 需客户决策 | 0 项 | 0 项（Q016 对标城市集合待确认，不阻塞 demo） |
| 接口 JSON spec | ✅ 10 个接口全部补齐 | ✅ 5 个接口全部补齐 |

---

## 二、Python 侧派单（demo-svc-topic-py）

### 任务 1：重点企业分析 — 10 个接口

**文件**：`gkx_search_service/views/enterprise_key_analysis.py`（新建）

**接口清单**：

| # | 路由 | 数据源 | 说明 |
|---|------|--------|------|
| 1 | `POST /internal/gkx-search/key-analysis/overview-kpi` | ES | TabA 3 张 KPI 卡 |
| 2 | `POST /internal/gkx-search/key-analysis/map-distribution` | ES | 地图区域分桶 + 采样 |
| 3 | `POST /internal/gkx-search/key-analysis/region-insight` | ES | 区域洞察（类型结构+同级 TOP） |
| 4 | `POST /internal/gkx-search/key-analysis/enterprise-list` | ES | 企业清单 Drawer |
| 5 | `POST /internal/gkx-search/key-analysis/brief-card` | ES | 企业点位轻量卡 |
| 6 | `POST /internal/gkx-search/key-analysis/domain-overview` | ES | 领域布局概览 KPI |
| 7 | `POST /internal/gkx-search/key-analysis/domain-matrix` | ES | 企业×领域覆盖矩阵 |
| 8 | `POST /internal/gkx-search/key-analysis/domain-graph` | ES | 跨领域关系图 |
| 9 | `POST /internal/gkx-search/key-analysis/domain-list` | ES | 重点领域分布表 |
| 10 | `POST /internal/gkx-search/key-analysis/domain-evidence` | DWD（PG） | 识别依据弹框 |

**关键实现要求**：
- Tab A 接口（1~5）：ES 查询，公共筛选参数含 `base_tag=key_enterprise` 先缩集
- 产业筛选**必须用 `industry_chains_flat`**（keyword 数组），**禁止走 `industry_chains` nested query**
- 企业类型下拉排除 `key_enterprise` 自身，只含 7 个资质类 tag
- 时间筛选用 `incorporation_year`（企业成立时间）
- 接口 6~9（domain-overview/matrix/graph/list）：ES mget + `core_tech_tags_flat` 内存聚合，已选企业 ≤50
- 接口 10（domain-evidence）：PG 查 5 张 DWD 表拼装 3 类证据：
  - `enterprise_extra.business_scope` → 业务范围
  - `enterprise_industry_product`（WHERE org_id AND chain_name LIKE）→ 产品线
  - `enterprise_chain_patent`（WHERE org_id AND chain_name LIKE LIMIT 5）→ 专利
  - `enterprise_fund_project`（WHERE org_id AND domain_code）→ 科研项目
  - `enterprise_patent_history`（WHERE org_id ORDER BY data_year DESC LIMIT 1）→ 有效专利数
- Mock 数据：`gkx_common/mock.py` 中补充重点企业 mock 文档（含 `tags_flat` 含 `key_enterprise` + 资质标签、`core_tech_tags_flat`、`addr_lng/lat`）

### 任务 2：深圳企业现状分析 — 5 个接口

**文件**：`gkx_search_service/views/enterprise_sz_status.py`（新建）

**接口清单**：

| # | 路由 | 数据源 | 说明 |
|---|------|--------|------|
| 1 | `POST /internal/gkx-search/sz-status/chain-kpi` | ES | TabA 4 张 KPI 卡 |
| 2 | `POST /internal/gkx-search/sz-status/chain-stage-stats` | ES | 环节分布 + 角色分布 |
| 3 | `POST /internal/gkx-search/sz-status/enterprise-list` | ES | 深圳企业清单 |
| 4 | `POST /internal/gkx-search/sz-status/city-benchmark` | ADS/Mock | 多城市对标表 + 雷达 |
| 5 | `POST /internal/gkx-search/sz-status/city-insight` | ADS/Mock | 相对优势/短板 |

**关键实现要求**：
- 接口 1~3：ES 查询，`region_id` 前缀 `4403*` 固定深圳，`industry_chains_flat` 过滤产业链
- 链中角色 = 上游/中游/下游/暂未标注，按 `industry_chains.node_stage`（1/2/3/空）映射，**不含智库标注**
- 重点环节企业：临时用 `node_type=2` 或 `node_imp_level>=2` 定义（需联查 DWD `dwd_industry_chain_info`），demo 可 Mock
- 产业链完整度：分子 = ES 聚合 `node_id` 去重数；分母 = DWD `dwd_industry_chain_info` 中该 chain 的 `node_type=2` 总数
- 接口 4~5（city-benchmark/city-insight）：demo 阶段 Mock；正式读 `ads.ent_sz_status`
- Mock 数据：`gkx_common/mock.py` 中补充深圳企业 + 产业链关联 mock

### 通用要求
- 在 `main.py` 注册两个新 router
- 每个接口写 pytest 测试（参考已有 `test_enterprise_search.py` 模式）
- 更新 `docs/API-接口文档.md` 补充 15 个新接口
- commit message 标注 `[agent:python-agent]`

---

## 三、Java 侧派单（lumen-svc-platform / gkxlumen-topic-enterprise）

### 任务 3：Feign Client + 对比篮适配

**文件**：`gkxlumen-topic-enterprise/gkxlumen-topic-enterprise-biz/src/main/java/.../feign/`

**工作内容**：
1. 新建 `GkxSearchKeyAnalysisFeignClient`：封装 10 个 `/key-analysis/*` 接口的 Feign 调用
2. 新建 `GkxSearchSzStatusFeignClient`：封装 5 个 `/sz-status/*` 接口的 Feign 调用
3. 新建对应 DTO 类（Request/Response），字段与设计文档 JSON spec 完全对齐
4. 对比篮适配：`CompareBasketController` 已有 add/remove/dispatch/get，确认前端「加入对比篮」调用路径无需新增接口
5. 领域分布 Tab 的分析对象从对比篮获取：复用 `GET /topic/v1/compare-basket/list` 返回 org_ids

**关键注意**：
- Feign 调用 Python `/internal/gkx-search/*` 前缀
- domain-evidence 接口的 Python 响应 `items[]` 是动态的（0~3 条），DTO 用 `List<EvidenceItem>` 接收
- commit message 标注 `[agent:java-agent]`

---

## 四、前端派单（lumen-ui-science-pc 或 demo-ui-science）

### 任务 4：重点企业分析页面

**路由**：`/enterprise-center/key-enterprise-analysis`

**页面结构**（双 Tab）：
- Tab A「类型与区域分析」：顶部筛选（区域 Cascader + 时间窗口 + 产业多选 + 企业类型多选）+ 3 KPI 卡 + Leaflet 地图 + 区域洞察面板 + 企业清单 Drawer
- Tab B「领域分布分析」：分析企业多选下拉（对比篮）+ 领域 KPI + 企业×领域矩阵 + 跨领域关系图（AntV G6）+ 领域分布表 + 识别依据弹框

**关键交互**：
- 地图气泡点击 → 下钻/刷新区域洞察 + 清单计数
- 企业清单 Drawer → 查看画像（跳转统一画像路由）/ 加入对比篮（调 Java compare-basket）
- 矩阵单元格「N 条依据」→ 弹识别依据弹框
- 弹框底部三按钮 → 跳转已有模块（企业画像/企业评估/风险洞察），带 `org_id`

### 任务 5：深圳企业现状分析页面

**路由**：`/enterprise-center/shenzhen-enterprise-status-analysis`

**页面结构**（双 Tab）：
- 全局输入：产业链必选 Select + 区域固定深圳
- Tab A「产业链定位」：4 KPI 卡 + 环节分布图 + 角色分布图 + 企业清单（含加入对比篮）
- Tab B「多城市横向对标」：对标城市多选 + 双雷达（ECharts）+ 相对优势/短板 + 城市×指标对比表

**关键交互**：
- 未选产业链 → 双 Tab 空态
- 企业清单 → 查看详情（跳转画像）/ 加入对比篮
- commit message 标注 `[agent:frontend-agent]`

---

## 五、依赖关系

```
任务1（Python key-analysis） ─┐
任务2（Python sz-status）    ─┼── 任务3（Java Feign）── 任务4/5（前端）
                              │
                              └── 前端可先用 Mock 并行开发
```

- Python 接口完成后 Java Feign 才能联调
- 前端可先用 Mock 数据并行开发，Python 接口 ready 后切换

---

## 六、DoD

- [ ] Python：15 个接口全部实现 + pytest 全绿 + API 文档更新
- [ ] Java：2 个 Feign Client + DTO 类 + 对比篮适配验证
- [ ] 前端：2 个页面可访问 + 双 Tab 切换 + 地图/图表/Drawer/弹框交互完整
- [ ] 三侧 handoff md 提交到 `agent-delivery/agent-handoffs/`
- [ ] commit message 标注 `[agent:<role>]`

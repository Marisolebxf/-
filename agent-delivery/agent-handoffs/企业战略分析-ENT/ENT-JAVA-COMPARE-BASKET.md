# Handoff：ENT-JAVA-COMPARE-BASKET

- **时间**：2026-07-21
- **执行**：agent:api-agent（监管：human:侯佳伟）
- **仓库 / 分支**：`lumen-svc-platform` / `dev`
- **派单包**：`ENT-JAVA-COMPARE-BASKET-派单包.md`
- **状态建议**：`review`（待 coordinator 验收；**勿自行改 done**）
- **接口总文档**：[`API-ENT-full-catalog.md`](./API-ENT-full-catalog.md)（**101** 端点；本单 **#91–101**）

## 1. 范围与实现

对比篮 Java 业务层（**不做评估计算**；摘要 Feign `enterprises/compare`）：

| # | 方法 | 服务内路径 |
|---|---|---|
| 91 | GET | `/topic/v1/compare-basket` |
| 92 | POST | `/topic/v1/compare-basket/items` |
| 93 | DELETE | `/topic/v1/compare-basket/items/{enterprise_code}` |
| 94 | DELETE | `/topic/v1/compare-basket/items/batch` |
| 95 | GET | `/topic/v1/compare-basket/search` |
| 96 | POST | `/topic/v1/compare-basket/dispatch` |
| 97 | GET | `/topic/v1/compare-basket/return-context/{context_id}` |
| 98–99 | GET/POST | `/topic/v1/compare-basket/recruit-candidates` |
| 100–101 | GET/POST | `/topic/v1/compare-basket/cultivate-candidates` |

表：`ent_compare_basket` / `ent_compare_basket_item` / `ent_recruit_candidate` / `ent_cultivate_candidate` / `ent_compare_return_context`（TTL 表，as-built 增补）

## 2. 偏离说明（as-built）

| 项 | 派单 | As-built | 理由 |
|---|---|---|---|
| 库 | PG / lumen 业务库 | MySQL `gkxlumenx_topic_enterprise` | 对齐 SEARCH-BIZ/FILTER |
| return_context 存储 | 未单列表 | 独立表 `ent_compare_return_context` | 会话 TTL 30min 需要 |
| Entity 位置 | 派单写 biz/entity | `*-api/.../api/entity` | 对齐 upms / SEARCH-BIZ |
| HTTP | REST | REST（与 SEARCH-BIZ 全 POST 不同，按本派单） | 派单契约 |
| `user_id` | 未明示 | 前端传递（query/body） | 专题服务无登录态 |

## 3. 产物清单

| 产物 | 路径 |
|---|---|
| DDL | `db/9x_gkxlumenx_topic_enterprise.sql` |
| Entity/DTO | `EntCompare*`、`EnterpriseCompareBasketDTOs` |
| Mapper/Service/Controller | `EntCompare*Mapper`、`CompareBasketService(+Impl)`、`CompareBasketController` |
| 总目录 | `API-ENT-full-catalog.md`（90→101） |
| 本 handoff | `ENT-JAVA-COMPARE-BASKET.md` |

## 4. 验收证据

| 项 | 结果 |
|---|---|
| Maven + JDK17 编译 | ✅ SUCCESS |
| 独立 Controller 未改 OpenApi/Feign | ✅ |
| 上限 50 / 去重 / 默认互斥候选 | ✅ |
| Feign compare 补全 + 失败降级 | ✅ |
| DDL 执行 | ⏳ 目标库执行建表 |
| 接口冒烟 | ⏳ CI/dev 部署后 |

## 5. 架构合规自检（7 条）

| # | 铁律 | 结果 |
|---|---|---|
| 1 | 算法只在 Python | ✅ 本单无评估算法 |
| 2 | 调用链 | ✅ 摘要经 Feign → Python `/internal/*`；篮状态 Java 自管 |
| 3 | 图谱 | N/A |
| 4 | 可观测性 | ✅ 沿用 OTel Agent |
| 5 | CI/CD | ✅ push 后 Pipeline |
| 6 | demo2 不 merge lumen | ✅ |
| 7 | 独立文件 Convoy | ✅ |

## 6. cost 四字段（估计）

| 字段 | 值 |
|---|---|
| `actual_tokens` | ~180000 |
| `model_used` | cursor-grok-4.5 |
| `actual_cost` | ~8 |
| `cost_warn` | false |

## 7. 开放项

1. 目标 MySQL 执行 DDL
2. coordinator 验收 → done
3. 前端联调另开任务

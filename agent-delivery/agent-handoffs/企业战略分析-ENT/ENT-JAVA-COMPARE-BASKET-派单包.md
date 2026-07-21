# 派单包：ENT-JAVA-COMPARE-BASKET

- **派单方**：coordinator（architect-agent 起草）
- **时间**：2026-07-21
- **执行 Agent**：`api-agent`
- **监管人**：human:侯佳伟
- **Sprint**：2026-W30
- **Epic**：E-ENT-SCRUM-PDR
- **仓**：`lumen-svc-platform`（gkxlumen-topic-enterprise 模块）
- **上游依赖**：无（纯 Java 业务层，不依赖 Python 评估接口；对比篮的企业摘要数据已有 `/internal/gkx-search/enterprises/compare`）
- **架构分析真源**：`agent-handoffs/企业战略分析-ENT/ENT-ARCH-COMPARE-EVAL-分析.md`

---

## 0. 铁律前置

1. **纯 Java 业务层**。不调 Python 评估接口（评估归 ENT-PY-EVAL-TASK / ENT-JAVA-EVAL，后续派）
2. **对比篮是派生暂存/分发容器**（Decision 088）。不展示分析结果、不拥有统计 metric、不做评估计算
3. **企业摘要数据复用已有 Feign**。`/internal/gkx-search/enterprises/compare`（Java 侧 `RemoteEnterprisePythonClient` 已有 `enterprises/compare`）—— 篮卡片字段直接用，不新增 Python 接口
4. **篮级状态全部 Java 自管**。持久化 / return_context / 候选名单 / 篮内搜索 / 勾选，全部 Java PG 表
5. **分文件隔离**。新建独立 Controller / Service / Mapper / Entity，不与现有 `EnterpriseOpenApiController` 混改（Convoy 风险）

---

## 1. 目标

在 `gkxlumen-topic-enterprise` 实现对比篮的完整 Java 业务层：篮持久化、篮内管理、发起分析分发、候选名单管理，支撑 Wireframe-ENT-COMPARE v1.5 的 F-CMP-01~05 全流程。

---

## 2. 必读

| 优先级 | 文件 | 用途 |
|---|---|---|
| P0 | `agent-handoffs/企业战略分析-ENT/ENT-ARCH-COMPARE-EVAL-分析.md` | 架构分析（对比篮字段矩阵/结论） |
| P0 | `agent-handoffs/产品整体定义/ENT-COMPARE/Wireframe-ENT-COMPARE.md` | **UI 契约真源**（F-CMP-01~05 字段表/交互/状态矩阵） |
| P0 | `agent-handoffs/产品整体定义/ENT-COMPARE/IA-ENT-COMPARE.md` | IA/路由 |
| P1 | `repos/lumen-svc-platform/gkxlumen-topic-enterprise/.../feign/RemoteEnterprisePythonClient.java` | 现有 Feign（已有 enterprises/compare） |
| P1 | `agent-handoffs/企业战略分析-ENT/ENT-JAVA-SEARCH-BIZ-派单包.md` | 同类 Java 业务层任务参考（表设计/三层规范） |

---

## 3. 范围

### 3.1 新建文件（分文件隔离，Convoy 安全）

```
gkxlumen-topic-enterprise-biz/src/main/java/com/topcomm/gkxlumen/topic/enterprise/
├── controller/CompareBasketController.java        # 对外 /topic/v1/compare-basket/*
├── service/CompareBasketService.java              # 接口
├── service/impl/CompareBasketServiceImpl.java     # 实现
├── mapper/CompareBasketMapper.java                # MyBatis
├── entity/CompareBasketEntity.java                # 篮主表
├── entity/CompareBasketItemEntity.java            # 篮内企业项
├── entity/RecruitCandidateEntity.java             # 招引候选名单
├── entity/CultivateCandidateEntity.java           # 培育候选名单
└── (mapper XML) resources/mapper/CompareBasketMapper.xml
```

### 3.2 数据库表（lumen 业务库 migration）

| 表 | 用途 | 关键字段 |
|---|---|---|
| `ent_compare_basket` | 单用户单篮 | user_id, basket_count, created_at, updated_at |
| `ent_compare_basket_item` | 篮内企业项 | id, user_id, enterprise_code, enterprise_name, source_route, source_summary, operated_at, sort_order |
| `ent_recruit_candidate` | 招引候选名单 | id, user_id, enterprise_code, enterprise_name, added_at, source |
| `ent_cultivate_candidate` | 培育候选名单 | id, user_id, enterprise_code, enterprise_name, added_at, source |

> 单用户单篮：`ent_compare_basket` 按 user_id 唯一；上限 50（Decision 088，GAP-IMPL-01 闭合）。

### 3.3 API 端点（对外 `/topic/v1/compare-basket/*`）

| # | 端点 | 方法 | 功能 | 对应 Wireframe |
|---|---|---|---|---|
| 1 | `/topic/v1/compare-basket` | GET | 获取当前用户篮（含企业列表，企业摘要调 Feign enterprises/compare 补全） | F-CMP-02 |
| 2 | `/topic/v1/compare-basket/items` | POST | 加入企业（校验上限 50、去重；记录 source_route） | F-CMP-02 加入 |
| 3 | `/topic/v1/compare-basket/items/{enterprise_code}` | DELETE | 移除单个企业 | F-CMP-02 移除 |
| 4 | `/topic/v1/compare-basket/items/batch` | DELETE | 批量移除 / 清空（二次确认前端做） | F-CMP-02 清空 |
| 5 | `/topic/v1/compare-basket/search` | GET | 篮内搜索（仅按企业名称过滤当前篮，不分页全量） | F-CMP-02 搜索 |
| 6 | `/topic/v1/compare-basket/dispatch` | POST | 发起分析分发（enterprise_codes[] + analysis_type → 生成 return_context_id，返回目标路由） | F-CMP-03 发起分析 |
| 7 | `/topic/v1/compare-basket/return-context/{context_id}` | GET | 恢复工作现场（筛选/勾选/滚动位置；会话级 TTL） | F-CMP-05 返回 |
| 8 | `/topic/v1/compare-basket/recruit-candidates` | GET | 招引候选名单列表 | F-CMP-03 查看引育名单 |
| 9 | `/topic/v1/compare-basket/recruit-candidates` | POST | 加入招引候选（批量，返回新增/重复数） | F-CMP-03 加入招引候选 |
| 10 | `/topic/v1/compare-basket/cultivate-candidates` | GET | 培育候选名单列表 | F-CMP-03 查看引育名单 |
| 11 | `/topic/v1/compare-basket/cultivate-candidates` | POST | 加入培育候选（批量，返回新增/重复数） | F-CMP-03 加入培育候选 |

### 3.4 发起分析分发逻辑（端点 6）

输入：`{enterprise_codes[], analysis_type}`
analysis_type 枚举（Wireframe F-CMP-03）：
- `technology` → `/enterprise-center/evaluation?mode=technology`
- `business` → `/enterprise-center/evaluation?mode=business`
- `competitiveness` → `/enterprise-center/evaluation?mode=competitiveness`
- `supply-chain` → `/enterprise-center/risk?tab=supply-chain`
- `pain-points` → `/enterprise-center/risk?tab=pain-points`

输出：
```json
{
  "return_context_id": "ctx-xxx",
  "target_route": "/enterprise-center/evaluation?mode=technology&source=compare-basket",
  "enterprise_codes": ["91440300...", "..."],
  "enterprise_count": 3
}
```

> return_context 存 `ent_compare_basket_item` 的当前筛选/勾选/滚动快照（JSON），会话级 TTL（如 30min）；新会话/失效只恢复篮内容（Wireframe F-CMP-05 状态矩阵）。

### 3.5 企业摘要补全

篮卡片需要的企业摘要（名称/地区/产业/类型/风险等级/引育标签）：
- Java 调 Feign `RemoteEnterprisePythonClient.enterprisesCompare(org_ids)`（**已存在**）
- 返回的 `_COMPARE_SOURCE` 字段已覆盖全部卡片需求
- 最近操作时间 / source_route 从 `ent_compare_basket_item` 取（Java 自管）

---

## 4. 禁止

- 在对比篮内做评估计算 / 生成评分 / 雷达 / 排名（Decision 088）
- 全库搜索企业（篮内搜索仅过滤当前篮）
- 按统一社会信用代码搜索（Wireframe §3.3）
- 弹二次确认移除（Wireframe §3.3：单个移除不弹二次确认；清空才弹）
- 修改 `EnterpriseOpenApiController.java` / `RemoteEnterprisePythonClient.java`（Convoy 隔离）
- 替甲方拍板 GAP-IMPL-02 正式持久化方案（本任务实现 PG 持久化即闭合，标 🟢）

---

## 5. Definition of Done

1. 4 张表 DDL（lumen 业务库 migration）
2. 11 个接口三层齐全（Controller→Service→Mapper），**独立文件**不混改现有 Controller
3. 单用户单篮逻辑（user_id 唯一约束 + 上限 50 校验）
4. 加入去重（enterprise_code 唯一）、移除不弹二次确认
5. 发起分析分发：5 种 analysis_type 路由映射 + return_context_id 生成
6. return_context 恢复：筛选/勾选/滚动快照 + TTL 失效降级
7. 候选名单：批量加入返回新增/重复数
8. 企业摘要经 Feign 调 `enterprises/compare`（复用现有，不新增 Python 接口）
9. 本地 Maven+JDK17 编译通过
10. handoff + 架构合规自检 7 条 + cost 四字段

---

## 6. Convoy 风险

| 风险 | 缓解 |
|---|---|
| 与其他 api-agent 任务同改 Java 模块 | **全新建文件**（CompareBasket* 系列），不碰 EnterpriseOpenApiController / RemoteEnterprisePythonClient |
| 与 ENT-JAVA-EVAL（后续派）同属 enterprise 模块 | 评估任务也将独立文件（EvalController），互不冲突 |

---

## 7. 认领话术

```text
/goal ENT-JAVA-COMPARE-BASKET
监管：human:侯佳伟
api-agent：gkxlumen-topic-enterprise 新建对比篮业务层 11 接口（/topic/v1/compare-basket/*），4 张表，纯 Java 业务层。
先读：ENT-ARCH-COMPARE-EVAL-分析.md、Wireframe-ENT-COMPARE.md、ENT-JAVA-SEARCH-BIZ-派单包.md（同类参考）。
铁律：纯 Java 业务层；对比篮不做评估计算；企业摘要复用现有 Feign enterprises/compare；全新建文件 Convoy 隔离。
```

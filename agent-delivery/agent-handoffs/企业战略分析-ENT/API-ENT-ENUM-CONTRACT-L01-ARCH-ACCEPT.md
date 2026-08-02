# 架构验收：API-ENT-ENUM-CONTRACT-L01

- **时间**：2026-08-02
- **评审角色**：architect-agent（监管人会话：`human:徐滕强`）
- **评审范围**：`API-ENT-ENUM-CONTRACT-L01` @ `demo-svc-topic-py` `ec1ff14` + handoff
- **对照**：公约 §2 铁律、本单 DoD、`architecture-baseline` 方案 A 调用链

---

## 决议

**条件通过（架构合规 PASS / 关单 CONDITIONAL）**

- 契约与运行时守卫达到本单目标，**无架构铁律违规**，可放行下游 `ENT-JAVA-ENUM-CONTRACT-L02` 按 §25 开工。
- **registry 转 `done`** 建议由 coordinator 在下列条件满足后执行（见 §关单条件）。

---

## 七条+铁律检查

| # | 检查项 | 结果 |
|---|--------|------|
| 1 | 算法只在 Python | ✅ meta/schema 只读；无 Java 算法 |
| 2 | 调用链 FE→Java→Python `/internal/*` | ✅ 仅扩 Python `/internal/gkx-search/meta/*`；Java 另开 L02 |
| 3 | 图谱 NebulaGraph | ✅ 不涉及 |
| 4 | 可观测性 | ✅ 既有服务；本单未改 instrument（可接受） |
| 5 | CI/CD | ✅ `py:smoke` + `py:image:search` 绿；⏳ `deploy:search-py` 待手动 |
| 6 | demo 不污染 lumen | ✅ 改 `demo-svc-topic-py` |
| 7 | 方案 A / Java 不写算法 | ✅；动态码表走 meta 透传策略已写入 §25.5 |
| 8 | 数据策略 | ✅ 固定枚举 + 既有 DIM/DWD meta；无 ODS 乱接 |
| 9–11 | D8/D9/D10 | ✅ 无前端/无新统计指标 |

---

## Findings（缺陷优先）

### [P2] handoff 证据未与 push 状态对齐 — `API-ENT-ENUM-CONTRACT-L01.md` §0/§2

§0 / §2 仍标「⏳ 待 push / ⏳ commit」，与 §7 已写 `ec1ff14` 已 push 矛盾。验收人易误判交付未完成。  
**要求**：关单前把 N1–N6 / DoD 表状态改成已 push，并回填 pipeline 链接。

### [P2] catalog↔strategy 漂移防护未覆盖 ops — `meta.py` + `test_meta_query_tree_schema_matches_field_strategy`

单测只断言 `field` / `es_field` / `strategy` 一致，**不校验** catalog 声明的 `ops` 是否与 `_build_leaf_condition` 实际支持一致。双份真源仍是中期风险（handoff 已登记 follow-up）。  
**不挡本单通过**；建议 L02 前或 follow-up 补 ops 一致性断言 / 单源化。

### [P2] `cicd: required` 的 K8s 热未完成 — Pipeline [#4621](https://gitlab.htmisoft.net/gkx-lumen/demo-svc-topic-py/-/pipelines/4621)

| Job | 状态 |
|-----|------|
| `py:smoke` | success |
| `py:image:search` | success |
| `deploy:search-py` | **manual**（未点） |

契约验收可基于本地 263 passed + smoke 绿；**完整 DoD 热部署**需人手 play `deploy:search-py`，或登记 deploy waiver。

### [P3] 排序白名单未收入 `enum_guards.py` — `enterprise_search.py`

铁律入口模块与 sort 归一化分居两处，后续新人易漏接。行为正确（三检索已覆盖），建议 follow-up 迁入或 re-export。

### [P3] 非法枚举「静默回退」与部分接口 `Rerr` 并存

`sort_field` / `region_type` 等回退默认；`aggregations.field` / `dimension` / `region_level` 直接报错。本单对 sort 的回退是明确产品要求，可接受；建议 §25.7 注明「标识符类：回退或拒绝均可，但禁止透传」。

---

## 无问题项（确认通过）

- Q058/Q059 listing/scale/`is_above_scale` 与 `meta.py` 常量一致  
- `POST /meta/query-tree-schema` + filters 三项扩展已落地；`main.py` endpoints 已登记  
- Format B `contains`、industry_class `free_text` 纠偏有单测  
- 排序 / enum_guards 白名单禁止非法值进 ES/SQL 标识符位  
- 范围隔离：未并入 `ENT-ES-ETL-L01`；Java 未混进本单  
- 下游 `ENT-JAVA-ENUM-CONTRACT-L02` 派单包与 §25 交接清晰  

---

## 关单条件（给 coordinator）

1. 修正 handoff §0/§2 过期 ⏳（可随小文档 commit）  
2. 回填 §7：Pipeline `4621`；`py:smoke`/`py:image:search` 绿；deploy 已 play **或** 书面 waiver  
3. 人签：`supervised_by human:徐滕强` 接受本架构意见后 → registry `done`  

**L02**：可读 §25 开工；**勿在 L01 `done` 前关闭 L02**。

---

## 签字

- architect-agent：条件通过（2026-08-02）  
- 架构师 lead（人）：待 `human:徐滕强` 确认  

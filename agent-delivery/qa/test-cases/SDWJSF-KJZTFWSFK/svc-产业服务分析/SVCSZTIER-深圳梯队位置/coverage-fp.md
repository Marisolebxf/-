# 深圳梯队位置 · 功能点覆盖（svc.sz-tier）

> catalog `svc.sz-tier` · 50897 · path `/industry-service/sz-tier`  
> 用例 `API-深圳梯队位置-用例.md`  
> A 线范围：**不扩六级**（`fp-split-by-api-run/_l6-to-catalog-map.yaml`）；矩阵键以 catalog `svc.sz-tier.main` 入参/出参及契约哨兵为准  
> 功能点键：`svc.sz-tier | endpoint_id | field_key | 功能点中文`  
> 编排：`algo-lib-api-case-playbook.md` §S1  

---

## 1. endpoint → 用例

| endpoint_id | METHOD | path | 对应用例 | 备注 |
|-------------|--------|------|----------|------|
| svc.sz-tier.main | GET | /entan/v1/svc/sz-tier | API-00644～API-00648 | catalog `status=unavailable`；§0 **未试调** |

---

## 2. 功能点 → 用例（主矩阵）

| 功能点键 | 规则来源 | 对应用例 | 状态 | 说明 |
|----------|----------|----------|------|------|
| svc.sz-tier \| svc.sz-tier.main \| industry \| 算法输入-industry目标产业 | catalog industry | API-00644、API-00646、API-00647 | 部分覆盖 | SVCSZTIER-01 合法产业；非法/空产业见 02/03；不传 industry（SVCSZTIER-04）本轮无独立用例 |
| svc.sz-tier \| svc.sz-tier.main \| dims \| 算法输出-dims三维度梯队位置 | catalog dims | API-00644、API-00648 | 契约占位 | unavailable，禁止 sample 内 tier 档位作通过条件 |
| svc.sz-tier \| svc.sz-tier.main \| _empty \| 深圳梯队无数据空态 | 契约空结果 | — | 未覆盖 | endpoint unavailable 且无稳定「合法入参必空」试调证据 |
| svc.sz-tier \| svc.sz-tier.main \| _fail \| 深圳梯队查询失败 | 契约错误态 | API-00644、API-00645、API-00646、API-00647 | 已覆盖 | 含 catalog 不可用、鉴权失败与 industry 入参失败语义 |
| svc.sz-tier \| \| tier_dim_org_count \| 机构数量维度梯队划分 | 需规（M_SVC_SZ_TIER 口径） | — | 未覆盖 | req_only；catalog 未拆 dim 级独立字段 |
| svc.sz-tier \| \| tier_dim_tech_score \| 技术力维度梯队划分 | 需规（M_SVC_SZ_TIER 口径） | — | 未覆盖 | req_only |
| svc.sz-tier \| \| tier_dim_chain_coverage \| 服务链完整度维度梯队划分 | 需规（M_SVC_SZ_TIER 口径） | — | 未覆盖 | req_only |
| svc.sz-tier \| \| compare_city_scope \| 对比城市名单与分档规则 | 需规 Q-SVCCHAIN-04 | — | 未覆盖 | req_only；业务口径待甲方确认 |

---

## 3. 统计

| 状态 | 条数 |
|------|------|
| 已覆盖 | 1（`_fail`） |
| 部分覆盖 | 1（`industry`） |
| 契约占位 | 1（`dims`） |
| 未覆盖 | 5（含 `_empty` 1 + req_only 4） |

---

## 4. B 线交卷摘要

| 项 | 值 |
|----|-----|
| API 用例条数 | 5 |
| 编号 | API-00644～API-00648 |
| `_empty` 未覆盖 | 1 |
| 试调 | **未试调**（§0 未 curl） |
| FUNC | 0 |

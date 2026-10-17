# 匹配推送 · 功能点覆盖（policy.match）

> catalog `policy.match` · 50897 · path `/policy/match`  
> 用例 `API-政策匹配推送-用例.md`  
> A 线范围：**不扩六级**（`fp-split-by-api-run/_l6-to-catalog-map.yaml`）；矩阵键以 catalog `policy.match.main` 入参/出参及契约哨兵为准  
> 功能点键：`policy.match | endpoint_id | field_key | 功能点中文`  
> 编排：`algo-lib-api-case-playbook.md` §S1  

---

## 1. endpoint → 用例

| endpoint_id | METHOD | path | 对应用例 | 备注 |
|-------------|--------|------|----------|------|
| policy.match.main | GET | /policy/v1/policy/match | API-000504～API-000508 | catalog `status=unavailable`；§0 **未试调** |

---

## 2. 功能点 → 用例（主矩阵）

| 功能点键 | 规则来源 | 对应用例 | 状态 | 说明 |
|----------|----------|----------|------|------|
| policy.match \| policy.match.main \| subject_id \| 算法输入-subject_id主体标识 | catalog subject_id | — | 部分覆盖 | MATCH-01 不传 subject_id；MATCH-04 无独立用例 |
| policy.match \| policy.match.main \| subject_type \| 算法输入-subject_type主体类型 | catalog subject_type | API-000504、API-000506 | 已覆盖 | 主路径 enterprise + 枚举外失败 |
| policy.match \| policy.match.main \| limit \| 算法输入-limit结果条数上限 | catalog limit | API-000504、API-000507 | 已覆盖 | 主路径 limit=20 + 非正整数失败 |
| policy.match \| policy.match.main \| match_score \| 算法输出-match_score匹配分 | catalog match_score | API-000504、API-000508 | 契约占位 | unavailable，禁止 sample 分值作通过条件 |
| policy.match \| policy.match.main \| _empty \| 匹配推送无数据空态 | 契约空结果 | — | 未覆盖 | endpoint unavailable 且无稳定「合法入参必空」试调证据 |
| policy.match \| policy.match.main \| _fail \| 匹配推送查询失败 | 契约错误态 | API-000504、API-000505、API-000506、API-000507 | 已覆盖 | 含 catalog 不可用、鉴权失败与入参失败语义 |
| policy.match \| \| subject_profile_topn \| 主体画像Top-N政策匹配推送 | 需规（bid §1.1.1.1.1.1.1.2.6） | — | 未覆盖 | req_only；四维加权与 QPOL-03 待甲方确认 |
| policy.match \| \| match_reasons_explain \| 可解释匹配理由输出 | 需规可解释推送 | — | 未覆盖 | req_only；catalog 8a 未声明 match_reasons 字段 |
| policy.match \| \| multi_channel_push \| 多通道推送与订阅 | 需规推送通道 | — | 未覆盖 | req_only；本 endpoint 为查询 API，不含推送通道契约 |

---

## 3. 统计

| 状态 | 条数 |
|------|------|
| 已覆盖 | 3（`subject_type`、`limit`、`_fail`） |
| 部分覆盖 | 1（`subject_id`） |
| 契约占位 | 1（`match_score`） |
| 未覆盖 | 4（含 `_empty` 1 + req_only 3） |

---

## 4. B 线交卷摘要

| 项 | 值 |
|----|-----|
| API 用例条数 | 5 |
| 编号 | API-000504～API-000508 |
| `_empty` 未覆盖 | 1 |
| 试调 | **未试调**（§0 未 curl） |
| FUNC | 0 |

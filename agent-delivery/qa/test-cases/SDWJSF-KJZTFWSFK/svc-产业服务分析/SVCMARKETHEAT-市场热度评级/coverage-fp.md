# 市场热度评级 · 功能点覆盖（svc.market-heat）

> catalog `svc.market-heat` · 50897 · path `/industry-service/market-heat`  
> 用例 `API-市场热度评级-用例.md`  
> A 线范围：**不扩六级**（`fp-split-by-api-run/_l6-to-catalog-map.yaml`）；矩阵键以 catalog `svc.market-heat.main` 入参/出参及契约哨兵为准  
> 功能点键：`svc.market-heat | endpoint_id | field_key | 功能点中文`  
> 编排：`algo-lib-api-case-playbook.md` §S1  

---

## 1. endpoint → 用例

| endpoint_id | METHOD | path | 对应用例 | 备注 |
|-------------|--------|------|----------|------|
| svc.market-heat.main | GET | /entan/v1/svc/market-heat | API-000639～API-000643 | catalog `status=unavailable`；§0 **未试调** |

---

## 2. 功能点 → 用例（主矩阵）

| 功能点键 | 规则来源 | 对应用例 | 状态 | 说明 |
|----------|----------|----------|------|------|
| svc.market-heat \| svc.market-heat.main \| industry \| 算法输入-industry产业技术领域 | catalog industry | API-000639、API-000641 | 部分覆盖 | MH-01 合法 industry=人工智能；非法 industry（MH-02）见 API-000641；不传 industry（MH-04）本轮无独立用例 |
| svc.market-heat \| svc.market-heat.main \| market_heat_level \| 算法输出-market_heat_level市场热度等级 | catalog market_heat_level | API-000639、API-000643 | 契约占位 | unavailable，禁止 sample「高」等文案作通过条件 |
| svc.market-heat \| svc.market-heat.main \| series \| 算法输出-series新增机构时间序列 | catalog series | API-000639、API-000643 | 契约占位 | unavailable，禁止 sample 内 new_org_count 数值作通过条件 |
| svc.market-heat \| svc.market-heat.main \| _empty \| 市场热度无数据空态 | 契约空结果 | — | 未覆盖 | endpoint unavailable 且无稳定「合法入参必空」试调证据 |
| svc.market-heat \| svc.market-heat.main \| _fail \| 市场热度查询失败 | 契约错误态 | API-000639、API-000640、API-000641、API-000642 | 已覆盖 | 含 catalog 不可用、鉴权失败、非法 industry 与错误 path |

---

## 3. 统计

| 状态 | 条数 |
|------|------|
| 已覆盖 | 1（`_fail`） |
| 部分覆盖 | 1（`industry`） |
| 契约占位 | 2（`market_heat_level`、`series`） |
| 未覆盖 | 1（`_empty`） |

---

## 4. B 线交卷摘要

| 项 | 值 |
|----|-----|
| API 用例条数 | 5 |
| 编号 | API-000639～API-000643 |
| `_empty` 未覆盖 | 1 |
| 试调 | **未试调**（§0 未 curl） |
| FUNC | 0 |
| code-registry | **未回写**（父控；本子任务禁改 registry / run-log） |

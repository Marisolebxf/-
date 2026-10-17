# 趋势预测 · 功能点覆盖（innov.forecast）

> catalog `innov.forecast` · 50897 · path `/innov/forecast`  
> 用例册：`API-趋势预测-用例.md`（API-00784～00798）  
> A 线真源：`fp-split-by-api-run/work/` **未收录** `innov.forecast`（`_l6-to-catalog-map.yaml`：创新监测不在本轮 60 六级）；矩阵键按 catalog `params` / `responseFields` + 契约 `_empty` / `_fail`  
> 编排：`algo-lib-api-case-playbook.md` §S1  

---

## 1. endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | 备注 |
|-------------|--------|------|----------|------|
| innov.forecast.domain | GET | /innov/v1/forecast/domain/{domainId} | API-00784～00788 | catalog `status=running`；§0 **未试调** |
| innov.forecast.contributions | GET | /innov/v1/forecast/contributions | API-00789～00793 | catalog `status=running` |
| innov.forecast.bursts | GET | /innov/v1/forecast/bursts | API-00794～00798 | catalog `status=running`；domainId 可选 |

---

## 2. 功能点 → 用例矩阵（catalog 契约 field）

| 功能点键 | 规则来源 | 对应用例编号 | 状态 | 说明 |
|----------|----------|--------------|------|------|
| innov.forecast \| innov.forecast.domain \| domainId \| 算法输入-domainId领域 ID | catalog domainId（path） | API-00784、00786、00787 | 已覆盖 | 合法 D-AI + 非法 + 空 path 段 |
| innov.forecast \| innov.forecast.domain \| history \| 算法输出-history历史年度 | catalog history | API-00784、00788 | 已覆盖 | array 形态；禁止 sample 年度数值 |
| innov.forecast \| innov.forecast.domain \| predictions \| 算法输出-predictions预测点 | catalog predictions | API-00784、00788 | 已覆盖 | array 形态；禁止 predictValue/ci 数值 |
| innov.forecast \| innov.forecast.domain \| _empty \| 领域趋势无数据空态 | 契约空结果 | — | 未覆盖 | 未试调，无稳定「合法 domainId 必空 history/predictions」证据 |
| innov.forecast \| innov.forecast.domain \| _fail \| 领域趋势查询失败 | 契约错误态 | API-00784、00785、00786、00787 | 已覆盖 | 含鉴权与 domainId 单缺陷 |
| innov.forecast \| innov.forecast.contributions \| domainId \| 算法输入-domainId领域 ID | catalog domainId（query，必填） | API-00789、00791 | 已覆盖 | 主路径 + 缺必填 |
| innov.forecast \| innov.forecast.contributions \| pageNum \| 算法输入-pageNum页码 | catalog pageNum | API-00789 | 部分覆盖 | CONTRIB-01 含 pageNum=1；省略分页见 CONTRIB-04 待试调 |
| innov.forecast \| innov.forecast.contributions \| pageSize \| 算法输入-pageSize页大小 | catalog pageSize | API-00789、00792 | 已覆盖 | 主路径 + 非正整数失败 |
| innov.forecast \| innov.forecast.contributions \| list \| 算法输出-list贡献度排行 | catalog list | API-00789、00793 | 已覆盖 | array 形态；禁止 sample contribution 数值 |
| innov.forecast \| innov.forecast.contributions \| _empty \| 贡献度无数据空态 | 契约空结果 | — | 未覆盖 | 未试调，无稳定空 list 构造 |
| innov.forecast \| innov.forecast.contributions \| _fail \| 贡献度查询失败 | 契约错误态 | API-00789、00790、00791、00792 | 已覆盖 | 含鉴权与入参失败 |
| innov.forecast \| innov.forecast.bursts \| domainId \| 算法输入-domainId领域 ID（可空） | catalog domainId（query，可选） | API-00794、00796、00797 | 已覆盖 | 带筛选 + 非法 + 省略 |
| innov.forecast \| innov.forecast.bursts \| topicName \| 算法输出-topicName主题 | catalog topicName | API-00794、00798 | 已覆盖 | 元素 string 形态 |
| innov.forecast \| innov.forecast.bursts \| burstScore \| 算法输出-burstScore强度 | catalog burstScore | API-00794、00798 | 已覆盖 | 元素 number 形态；禁止 sample 强度值 |
| innov.forecast \| innov.forecast.bursts \| _empty \| 主题突变无数据空态 | 契约空结果 | — | 未覆盖 | 未试调，无稳定必空突变列表证据 |
| innov.forecast \| innov.forecast.bursts \| _fail \| 主题突变查询失败 | 契约错误态 | API-00794、00795、00796 | 已覆盖 | 含鉴权与非法 domainId |

---

## 3. A 线 / snapshot 说明

| 项 | 结果 |
|----|------|
| `work/*.md` 检索 `innov.forecast` | **0 命中** |
| snapshot | `fp-split-by-api-run/_catalog-snapshot.md` 登记 **3** endpoint、`running`×3 |

---

## 4. B 线交卷摘要

| 项 | 值 |
|----|-----|
| API 用例条数 | **15**（3 endpoint × 5） |
| 编号闭区间 | **API-00784**～**API-00798** |
| 金样 | **API-00784**（完整信封） |
| 鉴权代表 | **API-00785**（全页引用） |
| `_empty` 未覆盖 | **3**（每 endpoint 1） |
| 试调 | **未试调**（§0 未 curl） |
| FUNC | **0** |
| code-registry / run-log | **未改**（父控回写） |

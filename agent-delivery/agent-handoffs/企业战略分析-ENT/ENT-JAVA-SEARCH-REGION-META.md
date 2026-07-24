# ENT-JAVA-SEARCH-REGION-META · 企业所属地区全国树契约

> 状态：已按监管人确认提交，待 coordinator 验收

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:api-agent` |
| supervised_by | `human:徐滕强` |
| claim_type | `pull` |
| claimed_at | `2026-07-24T18:30:00+08:00` |
| lock_until | `2026-07-24T22:30:00+08:00` |

## 范围与实现

1. `/search/meta/regions` 语义：注册区县 → 企业所属地区全国树
2. 请求新增 `mode` / `keyword`；响应新增 `has_children` / `children`
3. 高级筛选叶子字段新增 `enterprise_region`（`region_id` 前缀匹配）
4. 同步 Python docs + API-ENT-full-catalog / contract-draft

## 产物

- `demo-svc-topic-py/gkx_search_service/views/meta.py`
- `demo-svc-topic-py/gkx_common/mock.py`
- `demo-svc-topic-py/gkx_search_service/views/enterprise_search.py`
- `lumen-svc-platform/.../EnterpriseRegionRequest.java`
- `lumen-svc-platform/.../EnterpriseResponseDTOs.java`
- `lumen-svc-platform/.../EnterpriseOpenApiController.java`

## 提交与验证

- Python：`20d657a feat(search): support enterprise region tree [agent:api]`
- Java：`e791f8c feat(search): expose enterprise region tree [agent:api]`
- Python 地区接口测试：`2 passed`
- Java：`git diff --check` 通过；本机仅有 Java 8，Maven 编译要求 Java 17，未能完成编译
- `gkx_ai_service/**` 未纳入提交，仍保留原工作区改动

## 架构合规自检

- ✅ 算法仍在 Python；Java 仅做 REST 契约与转发
- ✅ 调用链保持前端 → Java → Python `/internal/*`
- ✅ 未引入 Neo4j、未改变图谱方案
- ✅ 未修改可观测性、CI/CD、部署配置
- ✅ 未向 lumen 正式仓 main 提交
- ✅ 未改变共享聚合核心与 ADS 数据策略
- ✅ 地区接口契约、Mock 和接口文档同步
- ✅ 未引入未确认业务口径

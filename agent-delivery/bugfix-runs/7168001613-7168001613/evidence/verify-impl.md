# 实现验证证据（2026-11-14 12:2x）

## lumen-topic-py
- 新增测试 tests/test_overview_chain_scope.py：4/4 通过
  - view 层：industry-kpi 链码下推（数组/单码/ALL 归一）、industry-comparison 链码下推、distribution 链维走现聚 SQL（断言 JOIN enterprise_industry_chain + eb.city='深圳市' + 参数绑定）、无链码走原预聚合表（回归）
  - repository 层：industry_kpi_all/industry_comparison 的链码进 SQL 绑定参数（compile().params 断言）；无链码时无 IN 过滤（回归）
- 命令：`.venv\Scripts\python.exe tests\test_overview_chain_scope.py` → `all 4 tests passed`；pytest -q → `4 passed in 0.50s`
- 回归：test_one_map_search_query / test_svc_rec_chain_filter 全过；test_meta_dimension_endpoints 有 2 个基线既有失败（stash 对照验证与本次改动无关，git stash push -u → 仍 2 failed → pop 还原）
- 既有文件 gkx_svc_service/repo.py、views/search.py 的未提交改动属于并行 run 7168034647，本 run 未触碰（stash round-trip 后内容不变）

## lumen-svc-platform
- DTO 加字段（EnterpriseMetaRequest.chainCode/chainCodes；EnterpriseDistributionRequest.chainCode），ServiceImpl 为 @RequestBody 整体转发无需改动
- 编译：mvn -pl gkxlumen-topic-enterprise-api -am compile -o（JAVA_HOME=.tools\jdk17）exit 0；biz 模块 -am compile exit 0

## lumen-ui-topic
- DevelopmentOverviewPanel.vue：scopeChainCode（L0 码直取/集群首 L0，对齐 KeyEnterprisesPanel 既有规约）；KPI/对比/分布请求带 chain_code；pickRank 按码精确匹配、失败清空不兜底
- portalFormat.ts：删除无消费者的 matchChainCode（名称模糊匹配，本次缺陷根因之一）
- types/search.ts：EntMetaRequest 加 chain_code/chain_codes
- 自检：npm run type-check → exit 0（15.8s）；npm run build-only → ✓ built in 23.38s
- 工作区其他 ServicePortal* 文件为并行会话产物，未触碰

# CMS-JX-SMART-COUNTRY-L01 handoff

- **任务**: 智能搜索地区筛选——cms_country_map 映射 + 四接口 country_location_ids 过滤
- **执行**: agent:api-agent · 监管 human:徐滕强 · ponytail full
- **仓**: lumen-svc-platform（4536a47 / 6c510ee）· lumen-topic-py（55a4857）· 均 push origin/dev
- **依赖**: CMS-JX-SMART-SEARCH-L01（pending_test）；本任务与 INDUSTRY-L01 并行

## 范围与实现

1. **映射表** `gkxlumenx_cms.cms_country_map`（DDL `db/9x_gkxlumenx_cms_country_map.sql` + 灌数脚本 `db/load_country_map.py`）
   - 久新 xlsx 232 国 × 自有 code_country 19 国，**汉字精确匹配 19/19 全中、无重名**；213 国置 `NOMATCH`
   - dev 库已建表灌数并校验（232=19+213，CHN 唯一）
2. **四接口新增可选筛选项 `country_location_ids`**（数组；不传=行为与旧版完全一致）
   - 企业：loc_ 码翻译 → **/search/query + query_tree（country_code in）**真过滤；含 NOMATCH → 必空
   - 产业：参数收下忽略（无地区概念，不报错）
   - 政策/服务链：仅国内数据 → 仅中国（CHN）放行，其余快速空返回
3. **下游白名单**（lumen-topic-py 55a4857，用户裁定"加功能支持"）：
   - `enterprise_search._FIELD_STRATEGY` + `meta._QUERY_TREE_FIELD_CATALOG` 各加 1 行 `country_code`（term）
   - 自检 `tests/test_country_code_strategy.py` 3/3 绿

## 关键排查与决策记录

- 首版把 `country_codes` 传给下游 `/smart` → 冒烟发现被静默忽略（USA/CHN 同 10000，假通过）；ES 聚合证实 `gkx_enterprise` v1/v2 各 208394 条全 CHN
- 用户指出 **ES 别名下是国内（v1）+ 海外（gkx_enterprise_global_v1）双索引**，不能因现网全 CHN 而降级 → 改走 query_tree 真过滤（下游白名单 1 行 + CMS 切换），改后 USA 真实过滤为 0
- 兼容铁律落实：无 country 筛选时企业仍走 /smart 原链路，旧调用方零影响

## 验收证据（2026-11-03 集群冒烟，镜像 cms:6c510ee2 + search-py:55a4857，走久新同款网关）

| # | 场景 | 结果 |
|---|---|---|
| 1 | 企业无筛选（基线 /smart） | code=0 total=66 |
| 2 | 企业 CHN | code=0 total=11 |
| 3 | 企业 USA | code=0 **total=0**（真过滤生效） |
| 4 | 企业 NOMATCH（喀麦隆） | code=0 total=0 |
| 5 | 企业 CHN+USA | code=0 total=11（并集） |
| 6 | 政策 CHN=1020 / USA=0 | ✅ 仅中国放行 |
| 7 | 服务 CHN=95 / USA=0 | ✅ |
| 8 | 产业带 country 参数 | code=0 total=9（忽略不报错） |
| 9 | 兼容回归（四接口不传 country） | 全部与旧版一致 |

单测：CMS SmartSearchServiceTest 14/14 + CountryMapServiceTest 4/4（并入）+ topic-py 3/3。

## 架构合规

- D1：久新 → CMS → Java 门面 → Python/ES ✅；loc_ 原码不出 CMS（DoD 铁律）✅
- D12：仅调 gkxlumen-* ✅；下游白名单改动为 1 行 + 注释 + 自检（最小增量，用户裁定）✅

## 评审与修复（2026-11-03 bugbot 轮，回归安全视角）

- 裁定：无筛选向后兼容 **SAFE**（企业走原 /smart、政策/服务精确回退原实现、新增字段纯增量不覆盖）；下游 Python country_code 白名单 **SAFE**（3/3 新测试）
- **C-1（Critical，已修 e298d0e）**：IndustryClusterService 码表首查询无兜底——dim 库无权限时会异常穿透且 map 恒空导致每次重试风暴（波及所有企业搜索含旧调用）。修复：try-catch + 5 分钟失败负缓存
- I：政策/服务多产业时 industryIds 迭代取首个（HashSet 任意序）——文档声明限制，产品后续如需多产业语义再升级
- I：跨库前缀 gkxlumenx_dim/dwd 为部署级假设——需确认 demo/prod CMS 库账号均有跨库 SELECT 权（当前 dev 实测通过）
- Minor：@Operation「keyword 必填」过期文案已随 e298d0e 更新；232 国覆盖率（19 命中）需向久新声明
- 部署后回归（e298d0eb）：旧调用 66 / 产业 3547+上浮 / country USA=0 / 政策 1020 / 服务 95 / 产业 9 全过

ponytail: full。

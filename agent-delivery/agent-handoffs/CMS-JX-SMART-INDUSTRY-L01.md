# CMS-JX-SMART-INDUSTRY-L01 handoff

- **任务**: 智能搜索产业筛选与返回——领域展开/前缀匹配/就近上浮
- **执行**: agent:api-agent · 监管 human:徐滕强 · ponytail full
- **仓**: lumen-svc-platform（92fabf9 / 51e2292 / d3d749b）· push origin/dev
- **依赖**: CMS-JX-SMART-SEARCH-L01（pending_test）；与 COUNTRY-L01 并行完成

## 范围与实现

1. **筛选**：四接口新增可选 `industry_ids`（数组；产业码 INB* 或领域码 CL-*；不传=行为与旧版一致）
   - 企业 ES：领域码经 `industry_cluster_map` 展开 → `/search/query` query_tree `industry_chain_code in`（`industry_chains_flat` **prefix** 策略，子链自动覆盖）——Python 零改动（字段已在白名单）
   - 政策：下游既有 `industry_code` 参数透传（Python 零改动）
   - 服务链：下游既有 `industry` 参数透传（Python 零改动）
   - 产业：接口自身即码本，后置 records 过滤（id/stableId 前缀）
2. **返回**：四接口 records 每条纯新增 `industry_id` + `industry_name`（就近上浮：数据链码/名称 → 归属产业 → 汉字；用户拍板 11-03「都挂产业」）
   - 双路径：`industry_chains_flat` 码（/smart 链路）→ 链名称反查（/search/query _source 无码字段，`industry_chain_names_flat` L0 名=产业名）
3. **keyword 口径**（用户拍板）：keyword 与 industry_ids 至少一个；纯产业筛选 keyword 缺省为空串

## 关键修复记录（冒烟驱动）

| 轮 | 问题 | 修复 |
|---|---|---|
| R1 | `industry_cluster_map` 未加 dim 库前缀 → 50001 bad SQL | 全限定 \`gkxlumenx_dim\`.\`industry_cluster_map\`（51e2292） |
| R2 | 空 keyword 被必填校验挡住 | keyword 与 industry_ids 至少一个（51e2292） |
| R3 | /search/query `_source` 白名单无 `industry_chains_flat` 码字段 → 上浮 None | 降级路径：`industry_chain_names_flat` 链名反查产业码（d3d749b） |

## 验收证据（2026-11-03 集群冒烟，镜像 cms:d3d749be）

| # | 场景 | 结果 |
|---|---|---|
| 1 | 企业 industry_ids=INB1303（纯筛选，无 keyword） | code=0 total=3547；records 每条 `industry_id=INB1303, industry_name=集成电路` ✅ |
| 2 | 企业 领域 CL-SEI-01（展开 5 产业） | code=0 total=10000；上浮各自正确（INB1306 软件与信息服务 / INB1333 智能终端 / INB1236 低空经济）✅ |
| 3 | 企业 产业+country 组合 | code=0 total=1764 ✅ |
| 4 | 政策 industry_ids=INB1303 | code=0 total=9（下游 industry_code 真过滤）✅ |
| 5 | 服务 industry_ids=INB1303 | code=0（下游过滤，结果 0 为真实现状）✅ |
| 6 | 产业接口 industry_ids=INB1303 | total=7（集成电路 L0+6 子链精准）✅ |
| 7 | 兼容回归：无筛选旧调用 | total=66 与旧版一致；新增字段不上浮时为 null（纯新增）✅ |

单测：IndustryClusterServiceTest 5/5（展开/就近/前缀/汉字）+ 全套 19/19 绿。

## 架构合规

- D1：久新 → CMS → Java 门面 → Python/ES ✅；Python **零改动**（industry_chain_code 既有白名单）✅
- 兼容：请求只增 industry_ids、响应只增 industry_id/industry_name ✅；其他前端不传新参数行为不变 ✅
- D12：仅调 gkxlumen-* ✅

## 评审与修复（2026-11-03 bugbot 轮，回归安全视角）

- 裁定：无筛选向后兼容 **SAFE**（企业走原 /smart、政策/服务精确回退原实现、新增字段纯增量不覆盖）；下游 Python country_code 白名单 **SAFE**（3/3 新测试）
- **C-1（Critical，已修 e298d0e）**：IndustryClusterService 码表首查询无兜底——dim 库无权限时会异常穿透且 map 恒空导致每次重试风暴（波及所有企业搜索含旧调用）。修复：try-catch + 5 分钟失败负缓存
- I：政策/服务多产业时 industryIds 迭代取首个（HashSet 任意序）——文档声明限制，产品后续如需多产业语义再升级
- I：跨库前缀 gkxlumenx_dim/dwd 为部署级假设——需确认 demo/prod CMS 库账号均有跨库 SELECT 权（当前 dev 实测通过）
- Minor：@Operation「keyword 必填」过期文案已随 e298d0e 更新；232 国覆盖率（19 命中）需向久新声明
- 部署后回归（e298d0eb）：旧调用 66 / 产业 3547+上浮 / country USA=0 / 政策 1020 / 服务 95 / 产业 9 全过

ponytail: full；cost 随后回填 registry。

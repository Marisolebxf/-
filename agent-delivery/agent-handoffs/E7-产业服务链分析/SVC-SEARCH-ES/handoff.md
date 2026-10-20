# LUMEN-SVC-SEARCH-ES-L01 · 服务机构检索 ES 化 — gkx_svc_org 独立轻量索引 + ETL + 查询双引擎

> 收尾 handoff（S0–S4 全段）。配套：[方案文档.md](方案文档.md) · [接口文档.md](接口文档.md) · [S4-验证报告.md](S4-验证报告.md) · `lumen-etl-es-py/docs/PLAYBOOK-svc-org-index-recreate.md`

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:api-agent` |
| supervised_by | `human:淮政玮`（registry）；S3 前端段口头监管 `human:xutengqiang` |
| claim_type | `pull` |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 未用 YAGNI 跳过任何铁律：D9 metric ⓘ 沿用页面既有角标体系（检索列表非统计数字点位）；可观测 Python instrument 已由仓内既有链路覆盖，前端 `observability.ts` 引擎灰度埋点记遗留（见下）；D12 隔离保持（未引 demo-* 服务）。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip`（本机未挂载） |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | `SVC-STORAGE-FLOW`（方案文档 §2 存储-查询流图） |
| 图 diff | 新增边：ADS svc_org_card 五表 JOIN → ETL service_org → gkx_svc_org_v1（别名 gkx_svc_org）→ topic-py 双引擎；查询链虚线为降级路径（mysql 回退），无禁止事项变化 |
| 会签态 | `draft`（随本 handoff 待架构师核） |

## 问题清单

- **[已决] 索引选型**：不并入企业索引加 tag（方案 §1.3 对比），独立轻量索引 `gkx_svc_org`，_id=org_id，卡面详情走企业 ES 二次查询
- **[已决] org_kind 线上实证全为「企业」43,296**（高校/院所暂无真源）——高筛「高校」诚实返 0，不造数；待 svc 源侧扩池
- **[已决] 深分页窗口**：`max_result_window` 默认 10000 档在 43k 池 p834 起截断，已在线调 50000；重建索引须重调（已写入 PLAYBOOK §2）
- **[已决] 城市形态**：ES 真值带「市」后缀（深圳市 14033 / 广州市 19600 实证），前端直译送双形态，ES 实测 0 → 14,033 命中

## 修改内容

### S1 · lumen-etl-es-py（commit `a17a2a4`）
- `conf/es/gkx_svc_org_mappings.json`：23 字段 mapping（ik_max_word/pinyin/edge_ngram，复用 settings 生成器）
- `etl/service_org.py`：五表 JOIN 灌数（svc_org_card ⋈ circle ⋈ tech_power ⋈ industry_tags ⋈ patent_history），物化 org_kind/stage_codes/fields_flat，43,296 文档，doc_as_upsert 幂等
- `docs/PLAYBOOK-svc-org-index-recreate.md`：重建/灌数/回退手册（本次收尾补深分页窗口备注）
- `app/es.py`：`ensure_svc_org_index`（幂等创建 + 别名绑定，禁删重建）

### S2 · lumen-topic-py（commit `db68cf7`）
- `gkx_svc_service/search_es.py`：ES 引擎（filters DSL 翻译器 13 字段×9 op、keyword wildcard 转义、`_recommended_top6`、`_sort_clause`）
- `gkx_svc_service/repo.py`：`SVC_SEARCH_ENGINE=es|mysql` 双引擎调度；**P1 闸门**——MySQL 路径遇 ES-only 参数（filters/org_kind/stage_code/tech_score_gte/非默认 sort）诚实拒绝 `unsupported_under_mysql`，禁止静默丢弃
- `gkx_svc_service/views/search.py`：sort/org_kind/stage_code/tech_score_gte/filters 入参透传
- `tests/test_gkx_svc_search_es.py`：24 项单测（调度/降级/拒绝/转义），全绿

### S3 · lumen-ui-topic（commit `46cda9f` + bugbot 修复待提交）
- `src/views/service/serviceOrgSearchModel.ts`：`dslToSearchBody` 切 filters 直译协议
- `src/views/service/serviceOrgSearchProtocol.ts`（bugbot 修复新增）：映射 + `leafToFilters` 真源——空值守卫、range 拆 gte+lte、containsAll 拆多条 in、city 双形态归一
- `src/mock/service/searchOrgsMock.ts`：matchesFilter 求值（城市去后缀归一）、行工厂补 stage_codes/fields_flat/patent_valid_count
- `src/api/service/types.ts`：SvcSearchFilter 等类型扩展
- selfcheck：`serviceOrgSearchDsl.selfcheck.mjs` import 真源断言（6 用例）+ `serviceOrgSearch.selfcheck.mjs` 锚点更新

### S4 · 活体 A/B 验证
- 三 tab 示例词双引擎对照 5/6 完全一致；行业 LIKE 子串 1 处差异属 ES 精确语义更优（接口文档 §6）
- 全池一致性：filters 组合 × 双引擎 total 全等（43,296 基准）
- 深分页 P95 224ms（p100-110 size20 实测）

### bugbot 审查（S3 提交 `46cda9f`，5 项全真全修，代码待提交）
1. **high** 空值叶子直译发送致 ES 零命中 → `isEmptyValue` 守卫整叶跳过
2. **med** range 错译 `eq` 数组值违反契约 → 拆 gte+lte 两条
3. **med** 城市形态错位（生产必现：ES 值带「市」） → 双形态 `["深圳","深圳市"]`，实测 0→14,033
4. **med** containsAll 弱化为任一命中 → 拆多条 in（AND 语义）
5. **low** selfcheck 复刻副本漂移 → 改 import 真源断言

## 测试结果

- `lumen-topic-py`：`pytest tests/test_gkx_svc_search_es.py` 24/24 ✅；`python -m gkx_svc_service.search_es` 自检 ✅
- `lumen-ui-topic`：`node src/views/service/serviceOrgSearchDsl.selfcheck.mjs` 6/6 ✅；`node src/views/service/serviceOrgSearch.selfcheck.mjs` ✅；`pnpm type-check` ✅；`pnpm build` ✅
- 活体：S4 A/B 对照矩阵（见 S4-验证报告.md）；bugbot 修复后 ES 实测命中恢复（city 14,033 / range 3,201 / containsAll 41）

## 遗留风险

- **前端 bugbot 修复代码已提交推送**（2026-10-20 用户批准）：`lumen-ui-topic` `5f583db`（origin/dev），rebase 后 selfcheck 6/6 + type-check 复验绿
- `observability.ts` 引擎灰度埋点（`engine` 字段）未接：待 `SVC_SEARCH_ENGINE=es` 生产灰度时一并加
- `SVC_SEARCH_ENGINE` 当前 dev 默认 `mysql`；ES 灰度切换需运维窗口 + S4 基线复测
- 城市后缀归一是前端双形态方案；若后端未来做 `_normalize_city` 需同步回收前端展开（避免双重处理）

## CI/CD（必填）

- 分支：三仓均 `dev`
- commit：lumen-etl-es-py `a17a2a4` · lumen-topic-py `db68cf7` · lumen-ui-topic `5f583db`（`46cda9f` S3 主体 + bugbot 修复 `711cb29` rebase 后终态；2026-10-20 用户批准推送）
- pipeline：三仓 push 后 GitLab CI 绿（etl / topic-py / ui-topic 均已推 dev 验证）
- 部署 namespace / 镜像 tag：dev 环境 K8s 常规 rollout（pipeline 产物，无特殊 tag）
- K8s rollout：etl / topic-py 成功；ui-topic 待推后随 CI
- dev 测试 URL / 命令与结果：`POST /svc/topic/v1/service/search/orgs`（经 gateway）双引擎 A/B 见 S4 报告；前端 `/service-center/search` 三 tab 联调通过

## 可观测性（建议）

- OTEL_SERVICE_NAME：`gkx-topic-py`（svc 检索链路沿用仓内 instrument）
- traceId（dev 抽样）：随 S4 活体请求已产生（未单列留档，Loki/Tempo 可查）
- Tempo / Loki：有

## 涉及文件

- 编排：`agent-delivery/agent-handoffs/E7-产业服务链分析/SVC-SEARCH-ES/{方案文档,接口文档,S4-验证报告,handoff}.md`
- etl：`conf/es/gkx_svc_org_mappings.json`、`etl/service_org.py`、`app/es.py`、`docs/PLAYBOOK-svc-org-index-recreate.md`
- topic-py：`gkx_svc_service/{search_es.py,repo.py,views/search.py}`、`tests/test_gkx_svc_search_es.py`
- ui-topic：`src/views/service/{serviceOrgSearchModel.ts,serviceOrgSearchProtocol.ts,serviceOrgSearchDsl.selfcheck.mjs,serviceOrgSearch.selfcheck.mjs}`、`src/mock/service/searchOrgsMock.ts`、`src/api/service/types.ts`

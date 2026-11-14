# LUMEN-SVC-PT-CHAIN-SLICE-L01 — 服务机构门户 5 接口产业切片

- 任务：LUMEN-SVC-PT-CHAIN-SLICE-L01（缺陷 7168034647）
- 监管：human:孔东 · 执行：agent:api-agent
- 仓：`repos/lumen-topic-py` · commit `3b140d9` + merge `5b18afe`（origin/dev 已推）

## 范围与实现

缺陷：服务机构门户 5 页（概况/产业分布/区域分布/技术能力/深圳介绍）切换产业时，前端已传
`industry`/`chainId`，Java 门面透传，但 Python `gkx_svc_service` 视图层**丢弃参数**
（`_ = body` / `filtered: False` 硬编码），repo 层只查全局 ADS 指标——KPI 与图表不随产业变化。

实现（挂链表现算切片，非灌数）：

1. **视图层** `gkx_svc_service/views/search.py`：
   - 新增 `_portal_slice_codes(body)`：`chain_codes` 列表（ranking 既有契约）优先；
     兼容 `industry`/`industryId`/`chain`/`chainId` 单码（INB 链码 / `CL-*` 集群码 / 点分路径
     `CL-SEI-01.INB1303`——取 INB 段优先，对齐前端 `chainCodesForIndustryPath` 语义）。
   - 五个门户路由 + `/portal/ranking` 全部接入；无产业参数 → `None` → 全量（向后兼容）。
2. **repo 层** `gkx_svc_service/repo.py`：
   - `_portal_chain_slice()`：公共切片入口（去重≤20、dwd/dim 库校验、CL-* 经
     `dim.industry_cluster_map`（`map_status='mapped'`）展开链码并集、INB17/18xx 旧码经
     `_resolve_chain_codes` 收敛；垃圾码/无映射集群 → `empty:chain_unmatched` 诚实空）。
   - `portal_overview(chain_codes)`：切片态在 `svc_org_card` 上按挂链交集现算 KPI（机构数=
     卡表行数、深圳=city 口径，同 svcseed `M_SVC_ORG_CNT`/`M_SVC_SZ_SCALE`）、六类布局
     （`service_type_candidate`，同 `M_SVC_INDUSTRY_LAYOUT`）、机构类型（名称启发式，同口径）、
     四档规模（`employees_number`，同 `_scale_bin`）、省级分布；`new_org_series`/`invest_series`
     依赖成立年与融资事件（无链切片灌数）→ 诚实省略并在 note 说明。
   - `portal_section(section, chain_codes)`：industry_distribution（六类现算；`svc_chain_gap`
     无链维度 → stages 诚实省略）、region_map（省级现算；country 无灌数 → 省略）、
     capability_rank / key_orgs（`_tech_rank` 加挂链过滤）、shenzhen（sz_total+区县现算；
     trend 诚实省略）。
   - `_tech_rank(limit, chain_codes)`：新增可选挂链 `IN` 过滤（子查询参数化，参数序=码序+limit）。
   - **兄弟缺陷一并修**：`ranking_list` TECH 分支原在切片代码前短路返回，技术力榜（门户技术
     能力页 `/portal/ranking` + `list_type=TECH`）一直忽略产业参数——现与 ATTRACT/CULTIVATE
     同口径切片。
   - `_query` 增加 `dim=` 库名参数（`{dim}` 占位符）；新增 `dim_db()`（`demo_*_dim` 校验，
     环境变量 `GKX_MYSQL_DIM_DB` 可覆盖）。
   - 所有非切片响应补 `filtered: False`（前端 `ServicePortalOverviewPage` hint 文案依赖
     `filtered === false`；切片态 `filtered: true` + `chain_codes` 回显）。
3. **测试** `tests/test_svc_portal_chain_slice.py`（mock 真路径范式，对齐
   `test_svc_rec_chain_filter.py`）：view 参数解析（单码/点分/列表/空参）、INB 切片 SQL 与
   参数序、CL-* dim 展开并集、垃圾码/无映射集群诚实空（不打 SQL）、TECH 榜切片回归、
   切片现算聚合正确性（六类/类型/规模/深圳区县）、非切片 `filtered: False`。

## 影响面排查（用户要求的前置确认）

| 关联点 | 结论 |
|---|---|
| 展示系统 `gkx_show_service/svc_factor.py`（同 svc_* 表） | 独立实现不 import gkx_svc_service，不受影响 |
| Java V-S 聚合 `ServiceVizServiceImpl` 复用 `portal/region-map` | body 透传；不传产业时行为不变；传产业时同向受益（注释本就写「同产业同链条同口径」） |
| Java 门面 + 单测（`ServiceFacadeServiceImpl*`） | 纯透传 + 诚实空断言，响应结构只增不改，无需 Java 侧改动 |
| 门户 5 页前端（`lumen-ui-topic`） | 已传 `industry`/`chainId`，无需改动即可生效 |
| 移动端 `lumen-ui-topic-mobile` | 门户路径无组件映射（NotAdapted），不受影响 |
| 既有 pytest | 不传产业路径行为不变，17 项相关测试全绿 |

## 自检证据

- `pytest tests/test_gkx_svc_search.py tests/test_gkx_svc_mounted_on_search.py tests/test_svc_portal_chain_slice.py tests/test_svc_rec_chain_filter.py tests/test_factor_search.py` → **22 passed**（merge 远端 factor-search 后复跑）
- 全量 `pytest tests`（忽略需真库密码的 `test_one_map_indfilter.py`）→ 406 passed, 9 failed,
  2 skipped；**9 个失败经 stash 对照确认为存量问题**（需连 dev MySQL/环境变量，与本改动无关）

## 已知边界

- 切片态 `new_org_series` / `invest_series` / `trend` / `stages` / `global` 诚实省略（数据源
  无链维度），note 说明；前端已有对应空态展示。
- 省级分布切片用 `city` 兜底（卡表 province 列无投影数据），已加 ponytail 注释标记升级路径。
- CL-* 展开依赖 dim `industry_cluster_map` 的 `map_status='mapped'` 行（6 集群 mock 映射已由
  `scripts/seed_cluster_map_mock.py` 补齐）。

## 架构合规自检

- ✅ 调用链未变（前端→Java→Python `/internal/*`）
- ✅ 诚实空约束：非法码/无映射/查询零行均 `empty:chain_unmatched`，不回退全量、不造数
- ✅ 参数化 SQL（挂链 IN 占位符），无拼接注入面
- ✅ D19：等值/IN 两侧同库表 utf8mb4（同库实例）

## cost

- actual_tokens: ~180k · model_used: glm-5.3 · actual_cost: ~$1.4 · cost_warn: false

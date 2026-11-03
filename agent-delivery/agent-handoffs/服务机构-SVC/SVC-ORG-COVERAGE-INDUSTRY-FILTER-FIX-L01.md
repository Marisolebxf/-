# Handoff — SVC org_coverage 产业过滤修复（伞任务 LUMEN-SVC-FE-WALK-OPT-L01 走查项）

- **日期**：2026-11-02
- **执行**：agent:frontend（全栈链路修复，跨 lumen-topic-py / lumen-algo-py / lumen-ui-topic）
- **监管人**：human:孔东（走查提出人）
- **task-registry**：挂伞任务 `LUMEN-SVC-FE-WALK-OPT-L01`（in_progress，E7-产业服务链分析）；本 handoff 为走查缺陷修复记录，不单开任务
- **强度**：ponytail full

## 1. 问题与根因

用户走查 `/service/institution-judgment?workspace=field`（服务机构产业领域分析，叶 `org_coverage`）：选「生物产业 → 生物医药与生命健康」+ 两个机构（新能源 / 生物医药），分析结果仍显示「人工智能与应用」无关矩阵。

根因（三处叠加，链路全断在 industry）：

1. **topic-py 白名单漏叶**：`gkx_svc_service/views/task.py::_call_svcan` 只对 `tech_power/graph/shortboard/attract/cultivate/shenzhen` 追加 `?industry=`，`org_coverage` 被漏 → 前端传了产业但没下发到算法。
2. **algo 矩阵不消费产业**：`svcan/assembly/leaves.py::leaf_org_coverage` 调 `matrix_asm.build()` 不传 industry；`matrix.py::_chain_rows` 拉全部链行 → 矩阵列按覆盖机构数降序，「人工智能与应用」（18.7 万行）永远排第一列。
3. **前端写死产业码**：`servicePortalIndustryScope.ts` 写死 `DEFAULT_PORTAL_INDUSTRY_PATH = ['CL-SEI-01', 'INB170102']` 与 `FIELD_LABEL_BY_L0` 字典 → 默认值/兜底绑死在已会变的码上。**用户裁定 2026-11-02：码表走数据库，前端禁止写死产业码。**

## 2. 修复内容（严格按需规 05.7.1 §7「按所选产业过滤矩阵行列」）

### 2.1 lumen-topic-py（`gkx_svc_service/views/task.py`）

- `_call_svcan` industry 白名单加入 `org_coverage`；任务 params 里 `industry`（前端已传 `CL-SEI-02.INB170201` 形态）透传到算法 URL query。

### 2.2 lumen-algo-py（`svcan/assembly/`）

- `leaves.py::leaf_org_coverage`：`matrix_asm.build(..., industry=params.get("industry"))`。
- `matrix.py::build()`：新增 `industry` 参数；函数内导入 engine 现成码名桥 `_industry_key` / `_industry_name_candidates`（`dim.industry_cluster_map` 码→名翻译，与 engine 读面同源，无环依赖）。
- `matrix.py::_chain_rows`：SQL 改为 `org_id IN (...) AND (chain_code = %s [OR dim 桥名前缀互匹配])`——码直等命中新码行；码名对不上时经 dim 表翻译候选名前缀互匹配兜住（同 `engine._chain_org_ids` 语义）。
- 空态区分：产业筛后无行 → `reason=industry_filter_no_match`（诚实空态，区别于无数据 `no_chain_rows`）。

### 2.3 lumen-ui-topic（前端去写死码）

- `servicePortalIndustryScope.ts`：
  - `DEFAULT_PORTAL_INDUSTRY_PATH` 改为空数组；新增 `defaultPortalIndustryPathFrom(clusters)` 从动态目录（`GET /topic/v1/meta/industry-clusters`，真源 `dim.industry_cluster_map` 50 行新码）取「第一个集群的第一个 L0」。
  - `FIELD_LABEL_BY_L0` / `CLUSTER_FIELD_LABEL` 降级为 API 未加载时的兜底文案，注释明确禁止作为真源维护。
  - `normalizePortalIndustryPath` / `serializePortalIndustryPath` 不再回填写死默认。
- 消费点改造（等目录 loaded 后动态回填）：
  - `ServicePortalShell.vue`：onMounted 无 industry 参数时 load clusters 后 `defaultPortalIndustryPathFrom` 回填。
  - `ServicePortalIndustryCascader.vue`：cascaderValue / watch(loaded) / 清空回调三处改动态默认。
  - `ServiceOrgAnalysisWorkspace.vue`：`ensurePortalIndustryQuery` 改动态；fingerprint 去掉写死 `INB2503` 兜底。
  - `enterpriseDevelopmentIndustry.ts`：`defaultEnterpriseDevIndustryPath` 去 `CL-SEI-01` 写死，改「clusters 第一个集群」。
- `orgTrendResultMock.ts`：mock 序列键 INB2503/INB1309/INB1306 → INB170201/INB170102/INB170106 新码（mock 层，不涉业务逻辑）。
- 需规 §1 ⚠️ 角标：结果页产业选择器旁加 `IconExclamationCircle` tooltip「产业过滤口径待甲方确认（跟踪表 Q-SVCCHAIN-09）」。

### 2.4 编排仓

- 《客户决策清单跟踪表》新增 **Q-SVCCHAIN-09**（产业过滤粒度 + 默认产业，🟡）——需规 §7 声称已登记但实际缺行，本次补上。
- 需规 `05.7.1` §1/§7 同步修正：删除过时的「演示默认 INB1309」（INB1309 已废弃旧码），改为动态码表 + Q-SVCCHAIN-09 引用。

## 3. 数据事实（修复时实查）

- 生产 `dim.industry_cluster_map` = 50 行新码（`INB1701~INB1710` L0 + `INB170101...` L1 + `INB18xx` 未来产业），Java `IndustryClusterService` 直读该表 → 前端级联选项本就是动态的，写死的只有默认值/兜底。
- `dwd.enterprise_industry_chain` 关联表新旧码双轨（`INB170102` 18.7 万行 vs `INB1309` 18.7 万行同现），新码直等可命中；码名不一致场景由 dim 桥兜住。
- demo 库 `industry_chain_20261029`（49 行）/`industry_cluster_map_20261029`（50 行）为新码表快照，结构与生产一致。

## 4. 验证证据

| 项 | 结果 |
|---|---|
| lumen-algo-py `pytest tests/test_svcan_assembly.py` | **21 passed**（新增 `test_org_coverage_industry_filters_matrix_fields`：断言 SQL 带 `AND (chain_code=...)`、dim 桥 LIKE 分支、`industry_filter_no_match` 空态、无产业参数回归） |
| lumen-algo-py `pytest tests/` 全量 | **668 passed, 6 skipped** |
| lumen-topic-py `pytest tests/test_gkx_svc_task.py` | **21 passed**（`test_org_coverage_pushes_org_ids_to_algo` 断言更新为带 `&industry=...`） |
| lumen-ui-topic `pnpm type-check` | 绿（vue-tsc 无错） |
| lumen-ui-topic 自检 ×22（全量 service/*.selfcheck.mjs） | 全绿 |
| lumen-ui-topic `pnpm build` | 绿（29.2s） |

> 注：lumen-topic-py 全量收集有 9 个本地环境旧版 sqlalchemy 的 ImportError（`URL`/`DeclarativeBase`），与本次改动无关；相关 28 个测试全绿。

### 4.1 代码评审（subagent review，2026-11-02）

- 结论：**Ready to proceed**，无 Critical；Important-1（field 指纹缺产业）已随评审修复，其余登记遗留。
- **[已修] field 工作区当天复用闸门不含产业**：`svcFingerprint` 原只对 capability 拼产业段，field 缺 → 同机构集切产业后 `decideAnalysisTaskGate` 按指纹命中旧产业的当天成功任务，原症状可经复用路径复发。修法：field 与 capability 同款把 industry 拼进指纹（v2 4 段 `svc|field|{industry}|{ids}`；trend 不消费产业维持 3 段），`idsFromFingerprintParts` / mock `svcOrgIdsFromTask` / 两个 selfcheck 同步。旧 3 段任务回落第 3 段取 ids，历史任务机构集还原不受影响（仅当天复用闸门失效，属预期新分析）。
- **[已修] Minor**：删除死导出 `DEFAULT_PORTAL_INDUSTRY_PATH`；`ServicePortalShell.vue` 头注释旧码示例换新码。
- [登记遗留] 集群级选择（只选集群不选 L0）时矩阵诚实空 `industry_filter_no_match`，与 tech_power 等叶既有语义一致非回归；后续可做集群级 Union L0 或空态文案明示「请选择到细分产业」。
- [登记遗留] `selected_industry` 测试断言过松（envelope 未回显所选产业）；空态 reason 在「机构集无效+带产业」边缘场景会误标 `industry_filter_no_match`。均为极边缘，不阻塞。

### 4.2 线上复测发现 P0 回归并已修复（2026-11-02 17:35 hotfix `84be2cb`）

用户 16:57 部署后跑两条任务（SVC-20261102-002/003）全部筛空 `industry_filter_no_match`。跳板 kubectl 进 pod 实测定位：

- **根因（本单 P0 回归）**：`matrix._chain_rows` 拼了产业条件占位符（`chain_code=%s OR LIKE×2`），但执行参数 `tuple(params)` **漏并 `ind_params`** → 占位符 5 个 vs 参数 1 个，pymysql 执行异常被 `_q` fail-soft 吞掉返回 `[]` → 诚实空态。单测 spy 只断言 SQL 文本不断言执行参数，subagent 评审亦未覆盖参数侧——双层都漏。
- **修法**：`params = params + ind_params`（占位符顺序 = org_ids → key → 每名两参）；测试补「参数数 == 占位符数 + 首参 org + 产业码/名在参数中」三重断言防复活。
- **pod 内验证**（镜像 `84be2cb`，pipeline 3464 全绿 + deploy:api 完成）：`build(db, [三叶草 org], industry="CL-SEI-02.INB2503")` → `status=ads_ready`，fields=[生物医药与生命健康, 生物医药]，orgs=[三叶草生物降解新材料科技（深圳）有限公司]，格值 depth=100。跳板 kubeconfig 副本已删。
- **教训**：涉及 SQL 参数拼接的改动，测试必须断言**执行参数**而非仅 SQL 文本；fail-soft `_q` 会把占位符失配变成静默空态，评审需专门核对占位符/参数数量一致性。

- **[线上复测确认] 前端仍在发旧码**：SVC-20261102-002 前端传 `CL-SEI-02.INB2503`（INB2503 是 dim 老码域，cluster_id 也是旧 CL-SEI-02），说明线上前端级联/默认仍走旧目录——本次前端动态目录改动（b167fec）虽已部署 pipeline 3458，但页面缓存或级联默认回填可能未生效，**需人工强刷页面后复测**；且 demo 库 `dim.industry_cluster_map` 只有 15 行老码（50 行新码在 `industry_cluster_map_20261029` 快照表，未切换真源表），新码 INB170201 依赖此表翻译的桥接在 demo 面暂不生效（INB2503 直等命中不受影响）。

## 5. 架构合规自检

| 铁律 | 自检 |
|---|---|
| 调用链（前端→Java→topic-py→algo） | ✅ 只打通既有链路的参数透传，无越层 |
| 算法只在 Python | ✅ 过滤逻辑在 algo 侧 SQL；Java/前端不写算法 |
| 数据真源 | ✅ 码表一律走 DB（`dim.industry_cluster_map`）；前端零写死码 |
| 诚实空态 | ✅ 筛后无命中 `industry_filter_no_match`，不回退全量矩阵（不再「选生物医药出人工智能」） |
| D9 指标 | ✅ 矩阵数字仍来自 `chain_score` 代理（Q-SVCCHAIN-02 🟡 不变），ⓘ/🧪 挂点未动 |
| 待甲方确认项 | ✅ Q-SVCCHAIN-09 已登记 + UI ⚠️ 角标（公约 §3.8） |
| Git | ✅ 评审修复后按用户 2026-11-02 指令「审核通过即推线上验证」推 `origin/dev`（lumen 人工验收闸门的 `/goal` 授权例外） |

## 6. 偏离说明

- 无。需规 §7「按所选产业过滤矩阵行列」即本次实现的语义；「演示默认 INB1309」为需规自身过时表述（INB1309 是已废弃旧码），已随本修复修正需规并补登记 Q-SVCCHAIN-09。

## 7. 遗留

- 甲方确认 Q-SVCCHAIN-09（过滤粒度：集群/L0/细分码；默认产业取值）后：去 ⚠️ 角标；若需细分码级过滤另扩 cascader 第三层。
- 旧码 `INB1309` 等在 `enterprise_industry_chain` 双轨并存属数据侧清理范畴（供方问题清单口径），不在本修复。

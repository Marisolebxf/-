# /goal 派单包 — ENT-Q068-CATALOG-SWEEP（主单 L01 + 拆叶 A02）

> 生成：2026-10-26 15:17 · coordinator-agent · 监管人 `human:徐滕强`
> 两单已 MCP 认领（`claimed`，lock 24h）。将下述话术分别粘贴到对应 agent 会话即可开工。
> **验收闸门（2026-10-20 用户裁定）**：改完停本地工作区，**禁止自动 commit/push**，等监管人走查通过后再推。

---

## 单 1 · 主单 → frontend-agent

```markdown
/goal frontend-agent
身份：你是经验丰富、遵循最佳实践的资深前端工程师，精通 Vue 3 + TypeScript + Arco Design Vue + Pinia；
只经网关调 Java，不直连 Python/DB；沿用 observability 埋点规范。
强度：ponytail full（默认）。禁止用 YAGNI 跳过 D8/D9/D10、可观测与架构铁律。

任务 ID：ENT-Q068-CATALOG-SWEEP-L01（registry 已认领，勿改状态字段）
仓库：${GKX_ROOT}/repos/lumen-ui-topic（主）+ ${GKX_ROOT}/repos/lumen-topic-py（过滤链）
监管人：human:徐滕强

背景：
产业下拉当前用老字典 ent.chains(scope=future)，数据源 DWD chain 表为空后走硬编码兜底
（老 20+8 枚举），缺"未来空间"等 Q068 新集群。全站统一目录 = Q068 深圳 3.0「15 集群」
（真源 demo_gkxlumenx_dim.industry_cluster；前端统一组件 IndustryClusterSelect /
useIndustryClusters；接口 GET /topic/v1/meta/industry-clusters?include_l0=true 已验证
返回 15 集群 + L0）。本单把老产业字典全链路清掉。

改动范围（lumen-ui-topic，5 处）：
1. src/components/enterprise/keyAnalysis/TypeRegionPanel.vue
   「重点企业类型分析」产业下拉：ent.chains → IndustryClusterSelect（或 useIndustryClusters
   组装 options）。提交值从 chain_codes(老码) 改为 industryIds(Q068 L0 INB 码，多选)。
2. src/views/enterprise/EnterpriseSzStatus.vue「深圳现状」产业链下拉：同上切 Q068。
3. src/components/enterprise/recruit/RecruitFilterPanel.vue
   引育推荐两模式（attraction 行业领域 / cultivation 产业类别）：ent.chains → Q068 全量。
4. src/components/enterprise/recruit/RecruitHistoryTable.vue
   历史记录 code→汉字翻译改走 useIndustryClusters（旧快照老码解析不到 → 诚实显示原码）。
5. 删除硬编码：src/utils/keyAnalysisParams.ts 的 KEY_ANALYSIS_CHAIN_OPTIONS /
   SZ_STATUS_CHAIN_OPTIONS、src/stores/entMetaChains.ts 的 FALLBACK_OPTIONS 回退逻辑
   （若 store 无其他消费方可整体下线）。useKeyEnterpriseAnalysis.ts 的
   metaChainsStore.ensureLoaded({scope:'future'}) 改为 useIndustryClusters().load()。

改动范围（lumen-topic-py，过滤链对齐，独立 commit 标 [agent:frontend-agent]）：
6. gkx_search_service/views/key_analysis.py：_build_common_filter 的 chain_codes 过滤
   改为 terms industry_chains_flat + 兼容 Q068 industry_id（INB L0 码，prefix 语义由
   前端传整码决定）；删除对老码的别名展开（若有）。
7. gkx_ai_service/views/recommend.py：industryDomains/industryCategories 直接接收
   INB 新码透传算法侧（A02 单负责归一映射，本单不重复实现）。
8. meta.py 的 _CHAIN_FALLBACK/_FUTURE_CHAINS：本单不删（深圳现状页若仍引用则一并切走后
   在 handoff 标注 deprecated，待 A02/后续单收口删除）。

硬性约束：
- ES industry_chains_flat 当前为空 → 按产业筛选命中 0 属预期，UI 诚实空态，禁止 fixture 填数。
- Q068 仍 🟡：下拉区挂 PendingBadge/角标「产业目录待甲方确认（Q068）」。
- 禁止把互斥 display 叠同一节点；复用已有组件，不新造轮子。
- 全部改动停本地工作区，禁止 commit/push（监管人走查后统一提交）。

必读：
- agent-delivery/客户决策清单跟踪表.md Q068 行
- ${GKX_ROOT}/repos/lumen-ui-topic/src/components/form/IndustryClusterSelect.vue（复用组件契约）
- src/composables/useIndustryClusters.ts

DoD：
- 三页下拉（重点企业分析 / 深圳现状 / 引育两模式）均为 15 集群树，含未来空间等 5 个 fut 集群；
- KEY_ANALYSIS_CHAIN_OPTIONS 等老硬编码全删，grep 无残留引用；
- pnpm type-check 绿；重点企业分析页手工走查截图（下拉展开图）贴 handoff；
- handoff：agent-delivery/agent-handoffs/企业战略分析-ENT/ENT-Q068-CATALOG-SWEEP-L01.md，
  含「使用点×处理方式」全局扫描清单、ponytail/cost 四字段、lumen-topic-py 独立 commit 记录；
- 完成后 registry 状态推进由 coordinator 执行（你只写 handoff，不改状态）。
```

---

## 单 2 · 拆叶 → python-agent

```markdown
/goal python-agent
身份：你是经验丰富、遵循最佳实践的资深 Python 工程师，精通 FastAPI / 数据码表归一 / pytest；
算法与候选解析逻辑严谨，杜绝静默丢匹配。
强度：ponytail full（默认）。禁止用 YAGNI 跳过输入校验与可观测。

任务 ID：ENT-Q068-CATALOG-SWEEP-A02（registry 已认领，勿改状态字段）
仓库：${GKX_ROOT}/repos/lumen-algo-py
监管人：human:徐滕强

背景：
lumen_common/algorithms/science/__init__.py 的 _FUTURE_CHAIN_CODE_TO_NAMES（约 L392）
是老「八大未来产业」小表（IC001/AI001/NEW_ENERGY/LOW_ALTITUDE/QUANTUM/OCEAN/ROBOT →
中文名），用于招引/培育推荐 industryDomains/industryCategories 候选解析。主单 L01 已把
前端切 Q068 15 集群全量树，用户可能传入任意集群的 INB 码（含未来空间 INB180401 等），
只留 8 项会静默丢匹配。用户已拍板：老码彻底废弃，不做兼容层。

改动：
1. 将 _FUTURE_CHAIN_CODE_TO_NAMES 重构为全量 INB 码表归一
   _INDUSTRY_CODE_TO_NAMES：
   - 真源 = demo_gkxlumenx_dim.industry_cluster_map（15 集群 / 50 行 INB 映射；
     industry_id → industry_name，同码异名取 DIM 名）；
   - 键 = 全部 INB* 码（L0 4位 + L1 6位都在表内），值 = 规范中文名（可附 L0 父名提高
     _text_hit 命中面，与现结构 (name,) 元组兼容）；
   - 值 fallback：未登记码 → (原码,) 直传，不猜名（诚实 miss）；
   - 删除全部老码键（IC001/AI001/NEW_ENERGY/LOW_ALTITUDE/QUANTUM/OCEAN/ROBOT 及
     ROB01/BIO01/COM01/INB1309/INB1204 等别名残留）；
   - ponytail 注释更新：码表已统一 INB，此映射仅做「码→展示名」翻译。
2. 更新/新增最小自检 tests/test_resolve_filter_candidates_fallback.py（或新增一个小
   test 文件，无框架 fixture）：
   - 新码命中：INB170101→集成电路匹配、INB180401→深海矿产（非八大集群，防回归）；
   - 未登记码 fallback：直传原码不抛错；
   - 老码 IC001：不再有特殊映射（按 fallback 原码走，命中 0 属预期）。
3. 同步更新模块 docstring 中「八大规范码」表述为「Q068 全量 INB 码表」。

硬性约束：
- 不动 resolve_filter_candidates 的匹配语义（OR / _text_hit 逻辑保持）；
- 不引入新依赖；改动停本地工作区，禁止 commit/push；
- 现有 tests 全量回归通过。

DoD：
- 全量 INB 归一生效，未来空间等 7 个非"八大"集群码可命中；
- 老码映射零残留（grep IC001/AI001 等无 hit）；
- 自检含新码+fallback+老码失效三断言且通过；
- handoff：agent-delivery/agent-handoffs/企业战略分析-ENT/ENT-Q068-CATALOG-SWEEP-A02.md
  （ponytail/cost 行 + 回填主单 evidence 引用），完成后由 coordinator 推状态。
```

---

## 收口约定（coordinator 用）

- 两叶 handoff 齐 → coordinator 汇总走查 → 监管人徐滕强确认后统一 commit/push；
- L01 转 `integration`（note 含「联调确认」关键词触发 AV-1）；A02 按 tech/feature 同轨；
- 联调冒烟：重点企业分析页下拉 15 集群可见 + 选未来空间 → 后端请求携带 INB 码（ES 空 → 空态诚实）；
- 数据侧缺口（ES industry_chains_flat 全空 / DWD chain 表空）另立数据单，不在本包内。

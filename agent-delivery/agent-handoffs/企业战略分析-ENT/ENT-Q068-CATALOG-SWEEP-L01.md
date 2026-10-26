# ENT-Q068-CATALOG-SWEEP-L01 — 产业目录老字典全链路清扫（Q068 切换）

- **任务**：ENT-Q068-CATALOG-SWEEP-L01（registry 已认领；状态推进由 coordinator 执行，本 handoff 不改状态）
- **执行**：agent:frontend-agent（GLM · Cursor 会话）
- **监管人**：human:徐滕强
- **日期**：2026-10-26
- **ponytail**：full（默认；未用 YAGNI 跳过 D8/D9/D10、可观测与架构铁律）

## 1. 背景与目标

产业下拉老字典 = `ent.chains`（`scope=future`，DWD chain 表空后走硬编码兜底 20+8 枚举），缺「未来空间」等 Q068 新集群。本单把 lumen-ui-topic 三页下拉（重点企业类型分析 / 深圳现状 / 引育两模式）+ 历史翻译 + 过滤链全量切到 **Q068 深圳 3.0「15 集群」统一目录**（真源 `demo_gkxlumenx_dim.industry_cluster`；前端复用 `IndustryClusterSelect` / `useIndustryClusters`；接口 `GET /topic/v1/meta/industry-clusters?include_l0=true` 已验证返回 15 集群 + L0）。

## 2. 范围与实现（对照派单 5+3 处）

### lumen-ui-topic（5 处，16 文件，全部停本地工作区）

| # | 文件 | 处理 |
|---|------|------|
| 1 | `src/components/enterprise/keyAnalysis/TypeRegionPanel.vue` | 产业下拉 `DictSelect dict="ent.chains" scope="future"` → `IndustryClusterSelect`（多选，`maxTagCount=2`）；提交值 `selectedIndustries` 从老 chain_code 改为 **Q068 L0 INB 码**（`@update:industry-ids`）。组件自带 Q068 PendingBadge ⚠ 角标 |
| 2 | `src/views/enterprise/EnterpriseSzStatus.vue` | 产业链下拉同上切 `IndustryClusterSelect`（单选 `industry-id`）；删除无消费方的 `onChainChange`；移除 `DictSelect` import |
| 3 | `src/components/enterprise/recruit/RecruitFilterPanel.vue` | 招引「行业领域」/ 培育「产业类别」（`source==='chains'`）分支改 `IndustryClusterSelect`；`dictKeyFor` 删 chains 分支（`ent.tags`/`ent.scales` 仍走 DictSelect） |
| 4 | `src/components/enterprise/recruit/RecruitHistoryTable.vue` | 历史 code→汉字翻译：`useEntMetaChainsStore.resolveName`（带老码 fallback）→ `useIndustryClusters().findIndustry(name ?? 原码)`；旧快照老码（IC001 等）解析不到时**诚实显示原码**（组件 `?? key` 兜底，不伪造） |
| 5a | `src/utils/keyAnalysisParams.ts` | 删除 `KEY_ANALYSIS_CHAIN_OPTIONS`（8 项硬编码）与 `SZ_STATUS_CHAIN_OPTIONS`（deprecated 别名）；`buildKeyAnalysisCommonRequest.chainCodes` 注释更新为「Q068 L0 产业码（INB*）经 chain_codes 字段透传」 |
| 5b | `src/stores/entMetaChains.ts` | **整体下线（文件删除）**。消费方全查清：TypeRegionPanel / EnterpriseSzStatus / RecruitHistoryTable / useDict('ent.chains') / useKeyEnterpriseAnalysis，全部在本单一并切走，无其他消费方 |
| 5c | `src/composables/useKeyEnterpriseAnalysis.ts` | `metaChainsStore.ensureLoaded({scope:'future'})` → `useIndustryClusters().load()`（catalog 由 TypeRegionPanel 的 IndustryClusterSelect 自加载；composable 侧保留 load 防竞态） |
| 连带 | `src/composables/dict/useDict.ts` | 删 `ent.chains` 分支 + `scope` 参数 + `MetaChainScope` 类型引用 |
| 连带 | `src/composables/dict/dictKeys.ts` | `FLAT_DICT_KEYS` 删 `'ent.chains'`；`assertFlatDictKey` 加显式报错 `"useDict('ent.chains') 已下线：请用 IndustryClusterSelect（Q068）"` 防旧调用悄悄漏过 |
| 连带 | `src/components/form/DictSelect.vue` | 删 `scope` prop（类型门报错驱动；现无消费方） |
| 连带 | `src/api/enterprise/index.ts` / `search.ts` / `paths.ts` | 删 `entSearchMetaChains` 导出/定义/路径（#138）；类型 `EntMetaChainsRequest/Item/Response` 保留（#G5 policy-orientations 仍用），删 `scope` 字段、注释更新 |
| 连带 | `src/mock/register.ts` / `src/mock/enterprise/topicApi.ts` | 删 `entSearchMetaChains` mock 注册与 `mockEntSearchMetaChains`（含 IC001/ROB01 老码）；产业目录 mock 真源 = `mock/industry/industryClusters.ts`（15 集群，不动） |

### lumen-topic-py（4 处，全部停本地工作区）

| # | 文件 | 处理 |
|---|------|------|
| 6 | `gkx_search_service/views/key_analysis.py` | `_build_common_filter`：`chain_codes` 现承载 Q068 L0 INB 码（整码 terms 精确命中 `industry_chains_flat`，prefix 语义由前端传整码决定）；**兼容 `industry_ids` 字段名**；确认无老码别名展开（原文无该逻辑，无需删）；docstring 注明 ES 字段当前为空 → 按产业筛选命中 0 属预期 |
| 7 | `gkx_ai_service/views/recommend.py` | `industryDomains` / `industryCategories` 直接接收 INB 新码透传算法侧；`_FILTER_KEYS` 上方加注释注明「归一映射（INB→算法口径）由 A02 单负责，本层不重复实现」 |
| 8 | `gkx_search_service/views/meta.py` | `_CHAIN_FALLBACK` / `_FUTURE_CHAINS` / `/chains` 端点**本单不删**，按派单标 **DEPRECATED**（高筛字段库 `value_source=meta_chains` 与链上脚本仍引用；待 A02 / 后续单收口后整体删除）；`meta_chains` docstring 消费方列表更新（重点分析/深圳现状/引育已划掉） |
| 8b | `gkx_search_service/views/sz_status.py` | `_build_sz_chain_filter` docstring 补 Q068 语境说明：term 码值无关、整码精确命中，前端深圳现状提交值已切 INB L0 码，过滤器无需代码改动（Bugbot 审查轮补记） |

### Java（lumen-svc-platform）：零改动

核实 `KeyAnalysisCommonRequest.chainCodes` 为纯透传 DTO（`@JsonNaming(SnakeCaseStrategy)`），前端继续以 `chain_codes` 键承载 INB L0 码，Java → Python 无损。

## 3. 「使用点 × 处理方式」全局扫描清单

扫描 pattern：`entMetaChains | entSearchMetaChains | KEY_ANALYSIS_CHAIN_OPTIONS | SZ_STATUS_CHAIN_OPTIONS | FALLBACK_OPTIONS | dict="ent.chains" | 'ent.chains'`（lumen-ui-topic 全仓含 tests/e2e）：

| 使用点 | 处理 | 结果 |
|--------|------|------|
| `TypeRegionPanel.vue` `dict="ent.chains"` | 切 IndustryClusterSelect | ✅ 0 残留 |
| `EnterpriseSzStatus.vue` `dict="ent.chains"` | 切 IndustryClusterSelect | ✅ 0 残留 |
| `RecruitFilterPanel.vue` `dictKeyFor→'ent.chains'` | 分支删除，chains 走 IndustryClusterSelect | ✅ 0 残留 |
| `RecruitHistoryTable.vue` `useEntMetaChainsStore` | 切 useIndustryClusters | ✅ 0 残留 |
| `useKeyEnterpriseAnalysis.ts` `ensureLoaded({scope:'future'})` | 切 `useIndustryClusters().load()` | ✅ 0 残留 |
| `useDict.ts` ent.chains 分支 / `dictKeys.ts` | 分支删除 + 防御报错 | ✅ 仅剩防御报错字符串（预期） |
| `stores/entMetaChains.ts` FALLBACK_OPTIONS | 文件整体删除 | ✅ |
| `api/enterprise` 三文件 + mock 两文件 | API/mock 全下线 | ✅ 0 残留 |
| `EntMetaChainsRequest.scope` 类型字段 | 删除（policy-orientations 不用 scope） | ✅ |
| lumen-topic-py `meta.py` 老兜底 | **保留 + DEPRECATED 标注**（派单第 8 条明确） | 🟡 待 A02 收口 |

Python 侧 `key_analysis.py` 老码别名展开：核查原文**不存在**该逻辑，无可删项（派单第 6 条「若有」条件不成立）。

## 4. 硬性约束对照

- **ES `industry_chains_flat` 当前为空 → 按产业筛选命中 0 属预期**：后端不做回退不造数（docstring 明示）；前端下拉数据源是 DIM 集群目录（非 ES），不涉 fixture 填数 ✅
- **Q068 🟡 PendingBadge**：`IndustryClusterSelect` 组件尾部自带（`pending-ref="Q068"`，hint「产业集群映射口径待甲方确认（Q068）」），三页复用即自动挂载，评审模式门控 ✅
- **互斥 display 不叠加 / 复用组件不新造轮子**：全程复用既有 `IndustryClusterSelect`，未新建组件；集群/产业两级独立 select ✅
- **全部改动停本地，禁止 commit/push**：两仓 `git status` 确认全部 M/D 停工作区，无 commit ✅（见 §8 commit 计划）

## 5. 验收证据

- **type-check**：`pnpm type-check`（vue-tsc --build）三轮全绿（DictSelect scope 清理、Bugbot 修复轮后各一轮）✅
- **Python 语法**：`py_compile` 四文件通过（key_analysis / meta / recommend / sz_status）✅
- **Bugbot 审查轮（主会话 in-place，2026-10-26）**：3 低危（无高/中危），已全部处置：
  1. `TypeRegionPanel.vue` 误删 `DictSelect` 显式 import（企业类型字段仍用，靠 unplugin 自动注册兜底）→ **已恢复显式 import**
  2. `sz_status.py` 过滤链码值疑点 → 核实 term 码值无关，**补 docstring 注释**（8b 行）
  3. `UseDictParams` 死类型 → **已删除**（useDict.ts + index.ts 导出链，`autoLoad` 亦无调用方，改回无条件 onMounted）
- **走查截图**（Playwright + 系统 Chrome，dev server Mock 模式 `VITE_APP_USE_MOCK=true`，走 `mockIndustryClusters` 15 集群），存于 `assets-ENT-Q068-CATALOG-SWEEP-L01/`：
  - `1-keyanalysis-page.png` 重点企业类型分析页全貌
  - `2-keyanalysis-cluster-open.png` 产业集群下拉展开（15 项全量）
  - `3-keyanalysis-industry-open.png` 集群→产业 L0 下拉（新一代信息技术 → 集成电路/传感器/人工智能/智能终端/软件与信息服务；含跨集群复用 L1 标记）
  - `4-szstatus-page.png` / `5-szstatus-cluster-open.png` 深圳现状页 + 产业链下拉展开（15 集群）
  - `6-recruit-attraction-page.png` / `7-recruit-cluster-open.png` 引育推荐（招引）页 + 行业领域下拉展开（15 集群）
- **选项抓取**（脚本输出）：三页集群下拉均为 15 项 = 10 SEI + 5 FUT（未来制造（智能机器人）/ 未来信息（光载信息、AI 底层生态）/ 未来能源 / 未来空间 / 未来健康（合成生物、细胞基因、脑机工程））✅ 含未来空间等 5 个 fut 集群
- **DoD 对照**：三页下拉 15 集群树 ✅｜老硬编码 grep 无残留 ✅｜type-check 绿 ✅｜截图贴 handoff ✅｜扫描清单/ponytail/cost/py commit 记录 ✅（本文件）

## 6. 架构合规自检

| 铁律 | 状态 |
|------|------|
| 调用链 前端→Java REST→Python `/internal/*` | ✅ 未越层（industry-clusters 走既有 Java topic 网关路由；未直连 Python/DB） |
| D8 Design/Arco 优先 | ✅ 复用 Arco select 封装组件 `IndustryClusterSelect`，未新造轮子 |
| D9 数据血缘 | ✅ 下拉数据只读消费 `/topic/v1/meta/industry-clusters`；不手写就绪度；Q068 🟡 PendingBadge 随组件挂载 |
| D10 交互规范 | ✅ 组件键盘可达/allow-search/aria-label 均为既有组件能力，未削弱 |
| D12 demo/lumen 隔离 | ✅ 仅动 lumen-ui-topic / lumen-topic-py，未引 demo 依赖 |
| 可观测 | ✅ 走既有 `defineApi`/request 埋点链路，无新增裸 fetch |
| Q068 客户决策 | ✅ 仍 🟡（决策清单 L321 行未动）；UI ⚠ 角标在位；不替甲方拍板 |

## 7. 偏离说明

1. **lumen-topic-py 未做独立 commit**：派单改动范围节写「独立 commit 标 [agent:frontend-agent]」，但硬性约束节明确「全部改动停本地工作区，禁止 commit/push（监管人走查后统一提交）」+ 仓级 AGENTS.md 人工验收闸门（2026-10-20 用户裁定）。按更强约束执行：**停本地待走查**。走查通过后建议 commit message 见 §8。
2. **`IndustryClusterSelect` 的 `placeholder` 属性被移除**：该组件 `inheritAttrs: false` 且未透传 attrs，此前传入的 `placeholder="全部产业"` 等本就不生效（死属性）；产业下拉占位文案由组件内 `industryPlaceholder` 计算（「请先选择集群」→「请选择产业」），删除死属性不改变行为。
3. **`meta.py` 高筛仍引用 `/chains`**：派单第 8 条允许保留；已标 DEPRECATED 并注明收口条件（A02 / 高筛码值切换后续单）。

## 8. lumen-topic-py 独立 commit 记录（待监管人走查后执行）

```
git add gkx_search_service/views/key_analysis.py gkx_ai_service/views/recommend.py gkx_search_service/views/meta.py gkx_search_service/views/sz_status.py
git commit -m "[agent:frontend-agent] Q068: key_analysis 过滤链兼容 INB L0 码/industry_ids；recommend INB 透传；meta/chains 标 DEPRECATED；sz_status 过滤注释对齐 (ENT-Q068-CATALOG-SWEEP-L01)"
```

（lumen-ui-topic 侧 commit 由监管人统一安排，建议同任务 ID 单独一笔：`[agent:frontend-agent] Q068: 三页产业下拉切 15 集群目录，下线 ent.chains 老字典 (ENT-Q068-CATALOG-SWEEP-L01)`）

## 9. cost 四字段

| 字段 | 值 |
|------|-----|
| actual_tokens | ≈ 690,000（含子任务/工具轮次累计，估算） |
| model_used | GLM-4.x（Cursor agent 会话，glm-5.3 署名） |
| actual_cost | ≈ $3.5 |
| cost_warn | false（< $10 阈值） |

## 10. 后续待办（非本单）

- A02：算法侧 INB → 模型口径归一映射（recommend 链）
- 高筛字段库 `industry_chain_code` 码值切 Q068 + `meta.py` `/chains` 端点删除（收口单）
- ES `industry_chains_flat` 灌数后复测「按产业筛选命中 > 0」
- Java 侧 `chainCodes` 字段语义正名（可选，纯注释级；透传无损已核实）

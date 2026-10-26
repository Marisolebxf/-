# ENT-Q068-CATALOG-SWEEP-A02 · lumen-algo-py 老码归一（招引/培育推荐 industryDomains/industryCategories）

> 主单：ENT-Q068-CATALOG-SWEEP-L01（前端下拉切 Q068 15 集群全量树）。
> 派单包：`agent-delivery/agent-handoffs/企业战略分析-ENT/ENT-Q068-CATALOG-SWEEP-派单包.md`

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:python-agent` |
| supervised_by | `human:徐滕强` |
| claim_type | `pull`（coordinator 派单包，MCP 认领） |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 与派单 `/goal` 强度行一致；码表为 DIM 真源 50 行的静态快照（单一 dict，无新增抽象/依赖）；未用 YAGNI 跳过输入校验（未登记码诚实 fallback）与码表不变量自检 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip`（本机未挂载） |

## 修改内容

`lumen_common/algorithms/science/__init__.py`（+79/−29 行）：

1. **删除**函数内局部老「八大未来产业」小表 `_FUTURE_CHAIN_CODE_TO_NAMES`（IC001/BIO01/AI001/NEW_ENERGY/LOW_ALTITUDE/QUANTUM/OCEAN/ROBOT 共 8 键）。
2. **新增**模块级全量 INB 码表 `_INDUSTRY_CODE_TO_NAMES`（`_tag_hit` 之后）：
   - 真源：`demo_gkxlumenx_dim.industry_cluster_map`（2026-10-26 快照，50 行映射 → 42 唯一码 = 14 个 L0 4 位 + 28 个 L1 6 位）；
   - 值 = 规范中文名元组，L1 附 L0 父名（提高 `_text_hit` 命中面）；同码异名取 DIM 名（仅 INB1801 同码双集群 CL-FUT-01「未来制造」/CL-FUT-05「未来健康」，两 DIM 名并列）；
   - 与 L0 同名的 L1（INB170301/INB180301「新能源/未来能源」）去重不重复列；
   - 未登记码 fallback：`(原码,)` 直传不猜名（诚实 miss）；
   - ponytail 注释更新为「码表已统一 INB，此映射仅做码→展示名翻译」。
3. **两处调用点换表**（匹配语义 OR / `_text_hit` 完全不动）：
   - attraction `industryDomains` 归一（原 L392 附近）；
   - cultivation `industryCategories` 归一（原 L466 附近，注释同步改「Q068 全量 INB 码表」）。
4. 老码键与「八大规范码」表述零残留（含别名 ROB01/BIO01/COM01/INB1309/INB1204）。

测试（2 文件）：

- `tests/test_resolve_filter_candidates_fallback.py`（15 项自检，含新增 4 项）：
  - `test_inb_full_catalog_hits_future_space`：未来空间 INB180401（深海矿产，非老八大集群）经链归属命中；防回归；
  - `test_unregistered_code_falls_back_to_raw`：未登记码直传原码不抛错（文本含码才命中、不沾边 0 候选）；
  - `test_legacy_chain_codes_no_special_mapping`：7 老码 + 5 别名不在码表（断言零残留），老码 fallback 原码 0 命中属预期；
  - `test_industry_code_catalog_invariants`：42 码 / 码格式 / L1 父码必在表（INB180501 例外，L0 未登记）等码表不变量，防 DIM 快照漂移；
  - 原 IC001 用例改 INB170101（语义不变：归一名命中链归属「集成电路」短链名）。

**走查修正（2026-10-26 16:30，Bugbot medium 真阳）**：`test_industry_code_catalog_invariants` 的 L1 父码分支原为死代码（`len(code) == 6` 永假——整码实为 7/9 字符，切片 `code[:4]` 亦错），父码一致性断言从未执行、测试空转通过；且原 `table[parent][0] in names` 严格断言与双名父码（INB1801=未来制造/未来健康，L1 按集群挂其一）矛盾。修复：`len(code) == 9` + `parent = code[:7]`，断言改「父码任一名 ∈ L1 名单」。已反证验证三场景（L1 丢父名 / 幽灵父码 / 数量漂移）坏表均被正确拦截，防线真实生效。
- `tests/test_e2e_failure_combos_selfcheck.py`：5 组线上失败组合的产业码 IC001/AI001 → INB170101/INB170102（业务语义不变），mock 链码 INB1309 → INB170102。

## 测试结果

- 定向：`python3 tests/test_resolve_filter_candidates_fallback.py` → **15 项自检全部通过 ✓**；`python3 tests/test_e2e_failure_combos_selfcheck.py` → 5 组合全部可解析 ✓（Bugbot 修正后复跑同绿）
- 不变量反证（走查修正新增）：三场景坏码表（L1 丢父名 / 幽灵父码 / 数量漂移）均被正确拦截，L1↔L0 父码防线真实生效
- 全量：`python3 -m pytest tests/ -q` → **545 passed, 6 skipped, 0 failed**（171.83s；6 skip 为既有环境相关跳过，非本次引入）；Bugbot 修正后全量复跑 **545 passed, 6 skipped, 0 failed**（170.24s，2026-10-26 16:36）
- 老码残留扫描：`rg "IC001|AI001|BIO01|NEW_ENERGY|LOW_ALTITUDE|QUANTUM|OCEAN\b|ROBOT|ROB01|COM01|INB1309|INB1204|_FUTURE_CHAIN_CODE_TO_NAMES" lumen_common/ tests/ gkx_ai_service/` → `lumen_common/` 与 `gkx_ai_service/` **零命中**；`tests/` 仅两类预期命中：① fallback 测试自身的负向断言（老码失效验证，任务要求）；② 其他模块既有 mock fixture（chain_shenzhen/policy/svcan 等，非本单范围）

## 遗留风险

1. **数据缺口（ DIM 侧）**：L0 `INB1805` 未在 `industry_cluster_map` 登记（L1 `INB180501` 脑科学与脑机工程在表）；若前端下发 INB1805，归一按未登记码 fallback 原码直传（诚实 miss）。已在码表注释与不变量测试标注；建议数据侧补登。
2. **码表快照同步**：DIM 增删 L0/L1 时需同步本静态快照；`test_industry_code_catalog_invariants` 断言 42 码不变量可拦截漏同步（数量变化时测试红，提醒人工核对 DIM）。
3. **生产命中面依赖链归属**：纯 DIM 全名（如「半导体与集成电路」）对 GB/T 长行业文本（「集成电路设计」）不做双向子串命中（改名前亦如此，非本次引入）；INB 码命中主要走 `enterprise_industry_chain.chain_name` 真源面。ES `industry_chains_flat` 全空为已知数据侧缺口（主单收口约定：另立数据单）。
4. 老码任务快照重放（历史 recommend 快照存 IC001 等）将 0 命中——用户已拍板废弃不兼容，属预期行为。

## CI/CD（必填）

- 分支：`dev`（工作区，**未 commit/push**，按验收闸门等监管人走查）
- commit：无（人工验收后统一提交）
- pipeline：无
- 部署：无
- dev 测试 URL / 命令与结果：本地 `python3 -m pytest tests/ -q` → 545 passed, 6 skipped

## 可观测性（建议）

- OTEL_SERVICE_NAME：不适用（静态码表重构，无新增链路；调用链埋点不变）
- traceId：无
- Tempo / Loki：无新增

## 涉及文件

- `lumen-algo-py/lumen_common/algorithms/science/__init__.py`
- `lumen-algo-py/tests/test_resolve_filter_candidates_fallback.py`
- `lumen-algo-py/tests/test_e2e_failure_combos_selfcheck.py`

## 架构合规自检

- ✅ 铁律 1：算法只在 Python（码表归一在算法层，未动 Java/前端）
- ✅ 铁律 2：调用链不变（前端 → Java REST → Python `/internal/*`；recommend filters 透传路径未动）
- ✅ D9：不涉及界面指标展示，无 8 件套变更
- ✅ D12：无 demo/lumen 越层调用
- ✅ 验收闸门（2026-10-20 用户裁定）：改动全部停本地工作区，未 commit/push

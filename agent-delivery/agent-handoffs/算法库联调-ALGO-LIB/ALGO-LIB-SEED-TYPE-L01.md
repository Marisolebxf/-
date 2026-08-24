# ALGO-LIB-SEED-TYPE-L01 · A1 会签后回填 seed — algorithm_type（522 条）

> 定义任务。把库里**待签 522 条**指标的 `algorithm_type` 回填进 seed（11 个 `cfg_metric-*-seed.yaml`）。`formula` 一律保留 seed 现有（监管人决策 type_only，延续 keep_detail）。**未**改 definition/源表/源系统/更新频率，**未**改 A2 missing，**未**写业务代码。
> 范围依据：淮政玮 2026-08-24「现在库里的指标都全了，SEED-TYPE-L01 需要重新跑」+「全部 522 条都要做」。
>
> **后补 §2.1 重判**：按《给人说明-指标与算法工作类型与流程梳理.md》§2.1「轴 A · algorithm.type」枚举表，对 522 条中 T2+T3（431 条）逐条重判（loop 工程，11 域分域）；T1（11）+ TTEMP（90）= 101 条 A1 表2 已签**一律不动**。共修正 **94 条**（MODEL 误判为主），已回填 seed。详见 `_work/ALGO-LIB-SEED-TYPE-L01-rejudge-修正清单.md`。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:唐绍祖` |
| claim_type | `pull` |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `off` |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本叶回填 seed YAML，未走 Headroom。 |

## 范围与实现

- **目标**：库里 `in_seed` 待签 522 条（`UNKNOWN` 371 + 缺字段 151）全部补 `algorithm_type`。
- **分级**：T2 赋号卡 156 + T-TEMP A1 已签 90 + T3 机器初判 276 = 522。
- **type 来源**：
  - T2：`id-assign/*.yaml` 的 `algorithm_type_suggested`。
  - T-TEMP：A1 表2 `TEMP_ALGO_*` 已签 `type` → 正式号（`API`→`third_party`）。
  - T3：按 formula/中文名规则初判。
- **写入方式**：`metric-registry-lib.mjs` 子集语法；371 条替换 `algorithm_type: UNKNOWN`，151 条在 `formula:` 后插 `algorithm_type:` 行；**保留各文件 CRLF/LF + BOM**（ENT 为 BOM+CRLF，其余 LF），避免整文件行尾改写。

## DoD 对照

| 项 | 结果 |
|----|------|
| 仅回填已签 algorithm_type；未签不写 | ✅ 522 条 type（T2 建议 + T-TEMP 已签 + T3 初判，监管人统签采纳） |
| 不把 suggested 当已签 | ⚠️ T2 赋号卡建议经监管人「全部采纳」统签后回填；见偏离说明 |
| MODEL/GRAPH/MIXED steps 留定义卡/表2，不冒充 8 件套 | ✅ 只写 type，不写 steps |
| D1 仅 9 项齐才 aligned；否则 draft；禁 UNKNOWN 派实现单 | ✅ 全部 D1 仍 draft，未动 |
| 不改存量口径 definition/源表 | ✅ 仅 algorithm_type 行 |
| data-agent 协作校验；handoff 含回填清单 | ✅ 库解析 532 全 non-UNKNOWN；清单见 `_work/` |
| 不写业务代码；不把 A2 missing 改 mapped | ✅ 定义叶，无代码 |

## 偏离说明

1. **范围 11 → 522**：派单包/说明仍写「11 条 `M_ENT_*`」，淮政玮口头修正「库里指标都全了、SEED-TYPE-L01 重新跑」+「全部 522 都要做」，监管人确认后按 522 执行。
2. **T-TEMP 90 条纳入**：`new-ids.md` 原写「禁止把 A1 表2 type / 赋号建议当已签」，被淮政玮「全部 522 都要做」覆盖；90 条 type 取自 A1 表2 已签，作为「建议 type」签收采纳（非绕过签收）。
3. **formula type_only**：只补 `algorithm_type`，formula 一律不动（延续 keep_detail 精神）。
4. **`M_ENT_KEY_TOTAL` 不再跳过**：`acc16b1` 补库后已在 seed，本次回填 `STAT`。
5. **§2.1 重判 94 条**：初判（loop 前）对 T3 过度依赖「名字含指数/评分 → MODEL」，与 §2.1 枚举表冲突。按 §2.1 逐条重判后修正 94 条（`MODEL→STAT` 49、`MODEL→COMPUTE` 30、`MODEL→GRAPH` 3、`MODEL→MIXED` 2、`STAT→COMPUTE` 3、`GRAPH→STAT` 3、`GRAPH→COMPUTE` 2、`GRAPH→MIXED` 1、`COMPUTE→STAT` 1）。核心边界见下「COMPUTE 边界」。

## 产物清单

- `metrics/registry/cfg_metric-*-seed.yaml`（11 文件，+522 行 `algorithm_type`）
- `metrics/request/_work/ALGO-LIB-SEED-TYPE-L01-签收草表.md`（522 条分级签收表）
- `metrics/request/_work/ALGO-LIB-SEED-TYPE-L01-T3高风险清单.md`（209 条占位符初判，供抽查）
- `metrics/request/_work/ALGO-LIB-SEED-TYPE-L01-backfill.md`（回填清单）
- `metrics/request/_work/ALGO-LIB-SEED-TYPE-L01-rejudge-修正清单.md`（§2.1 重判 94 条逐条清单 + 边界说明）
- `metrics/request/_work/rejudge/{DOMAIN}.md` + `{DOMAIN}.changes.json`（11 域 loop 明细与变更记录）

## 验收证据

- `metric-registry-lib.mjs` 解析：532 条 `in_seed` 全部 `algorithm_type ≠ UNKNOWN`、0 缺失；YAML 无损坏。
- 类型分布（重判后）：`STAT=164, MODEL=198, GRAPH=53, COMPUTE=37, MIXED=33, third_party=47`（重判前：`STAT=114, MODEL=282, GRAPH=56, COMPUTE=3, MIXED=30, third_party=47`）。
- `git diff --stat`：`11 files changed, 522 insertions(+), 371 deletions(-)`；全量 diff 审计：删除行 371 全部为 `algorithm_type: UNKNOWN`、新增行 522 全部为合法 type，**0 误改其他字段**，无 CRLF/BOM 污染。
- §2.1 重判：`_seed_rejudge_apply.mjs` dry-run `replace=94 mismatch=0 未找到=0` 后 `--apply` 落盘；抽样校验关键指标（`M_ENT_REVENUE_LATEST`→STAT、`M_CHAIN_ACADEMIC_POWER`→COMPUTE、`M_INNOV_DS_02_PATH_002`→GRAPH 等）全部正确。

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 1 算法只在 Python | ✅ 不写算法实现 |
| 2 调用链 | ✅ 不越层 |
| 3 NebulaGraph | ✅ 不引入 Neo4j |
| 4 可观测性 | N/A |
| 5 CI/CD | ✅ skip |
| 6 demo2 merge | ✅ 不 merge lumen |
| 7 共享聚合 | ✅ 只改编排仓 seed YAML |
| 8 数据策略 | ✅ 不伪 full |
| 9 D8 | N/A |
| 10 D9 | ✅ draft + type，不标 aligned |
| 11 D10 | N/A |
| 12 D12 | ✅ 不调 demo 服务 |

## Cost 回填

| 字段 | 值 |
|------|-----|
| actual_tokens | 待回填（本会话未统计，由监管人补） |
| model_used | 待回填 |
| actual_cost | 待回填 |
| cost_warn | green |

## 会签

| 角色 | 结论 |
|------|------|
| 状态 | `done`（2026-08-25 `human:淮政玮` 终签；522 条全部纳入） |
| 公式 / 类型 `human:唐绍祖` | 本叶执行：522 条按「全部采纳建议 type」统签并回填；formula 保留 seed 现有（type_only）。后按 §2.1 重判 T2+T3 共 431 条，修正 94 条（详见 rejudge 修正清单） |
| 身份 Owner / 签收 `human:淮政玮` | 已终签。差 1 条=`M_ENT_KEY_TOTAL`（T3 草表∩T1 冻结，非漏填）。COMPUTE 新口径：子指标含评价模型的加权合成→MODEL；30 条 MODEL→COMPUTE 已回退为 MODEL。根目录 `_seed_*.mjs` 暂不整理。 |

## 遗留风险

- T3 的 276 条为机器初判，其中 **209 条 formula 是 `pending_*` 占位符**（初判靠中文名），已入 `T3高风险清单.md` 供抽查；抽查后如需更正，单条改 seed 即可。
- 全部 MODEL（终签回退后 228 条）formula 仍为骨架/占位，`D1` 仍 `draft`，未达 `aligned`；后续 OPEN 贴源叶 + T0-X 复会逐条正式化类型/公式。
- **COMPUTE 边界已按淮政玮终签口径回退**：加权合成若子指标含评价模型（密度/评分/壁垒等）归 MODEL。30 条 `MODEL→COMPUTE` 已改回 MODEL。仍留 COMPUTE=7（HHI/熵类固定公式、GRAPH→COMPUTE 的招引/培育 demo 分、及重判前存量）。A1 已签 `M_ENT_TECH_POWER_SCORE` 等未动。
- `agent-delivery/metrics/cfg_metric-SVC-seed.yaml` 存在一个**异常位置的 untracked 文件**（应在 `registry/` 下），非本叶产物，建议淮政玮核查清理。

## CI/CD（必填）

- 分支：`dev`（编排仓，本会话未要求 push）
- commit：待你确认后提交
- pipeline URL / ID：N/A
- 部署 namespace / 镜像 tag：N/A
- K8s rollout：N/A
- dev 测试命令与结果：`metric-registry-lib.mjs` 解析 532 全 non-UNKNOWN + `git diff` 全量审计通过

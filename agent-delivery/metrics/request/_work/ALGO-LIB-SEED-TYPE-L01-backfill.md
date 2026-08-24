# ALGO-LIB-SEED-TYPE-L01 · 回填清单（522 条）

> 定义任务。回填 `algorithm_type` 进 seed（覆盖 11 个 `cfg_metric-*-seed.yaml`）。**只补 `algorithm_type`，formula 一律不动**（监管人决策 type_only，延续 keep_detail）。
> 范围依据：淮政玮 2026-08-24 确认「现在库里的指标都全了，SEED-TYPE-L01 需要重新跑」→「全部 522 条都要做」。
> 后补：按 §2.1 枚举表对 T2+T3（431 条）loop 重判，修正 94 条，见本文件 §八 与 `ALGO-LIB-SEED-TYPE-L01-rejudge-修正清单.md`。

## 一、总览

| 项 | 值 |
|---|---|
| 待签总数 | **522** 条 |
| 处理方式 | `algorithm_type` 回填；formula 保留 seed 现有 |
| 替换（`UNKNOWN` → type） | 371 条 |
| 插入（缺字段 → 新增行） | 151 条 |
| 覆盖 seed 文件 | 11 个 |

## 二、分级依据（522 = 156 + 90 + 276）

| 分组 | 条数 | type 来源 |
|---|---|---|
| T2 · 赋号卡建议 | 156 | `id-assign/*.yaml` 的 `algorithm_type_suggested`（unsigned，签收采纳） |
| T-TEMP · A1 已签沿用 | 90 | A1 表2 `TEMP_ALGO_*` 已签 `type` → 正式 `M_*` 号（`API`→`third_party` 38 条） |
| T3 · 机器初判 | 276 | 按 formula/中文名规则初判（209 占位符 + 67 真实公式） |

## 三、类型分布（回填 522 条）

| algorithm_type | 条数 |
|---|---|
| STAT | 111 |
| MODEL | 275 |
| GRAPH | 56 |
| MIXED | 30 |
| third_party | 47 |
| COMPUTE | 3 |

> 全库 532 条（含此前已回填 T1 10 条）最终（重判前）：`STAT=114, MODEL=282, GRAPH=56, MIXED=30, third_party=47, COMPUTE=3`，0 条 `UNKNOWN`、0 条缺失。
> §2.1 重判后（修正 94 条）：`STAT=164, MODEL=198, GRAPH=53, COMPUTE=37, MIXED=33, third_party=47`。

## 四、各域回填数

| domain | 文件 | 替换 | 插入 | 小计 |
|---|---|---|---|---|
| CHAIN | cfg_metric-CHAIN-seed.yaml | 39 | 60 | 99 |
| COMMON | cfg_metric-COMMON-seed.yaml | 1 | 0 | 1 |
| ENT | cfg_metric-ENT-seed.yaml | 19 | 50 | 69 |
| INNOV | cfg_metric-INNOV-seed.yaml | 138 | 0 | 138 |
| ORG | cfg_metric-ORG-seed.yaml | 22 | 0 | 22 |
| POLICY | cfg_metric-POLICY-seed.yaml | 13 | 19 | 32 |
| SVC | cfg_metric-SVC-seed.yaml | 43 | 0 | 43 |
| SYNTH | cfg_metric-SYNTH-seed.yaml | 25 | 21 | 46 |
| TALENT | cfg_metric-TALENT-seed.yaml | 32 | 0 | 32 |
| TECH | cfg_metric-TECH-seed.yaml | 39 | 0 | 39 |
| TNIE | cfg_metric-TNIE-seed.yaml | 0 | 1 | 1 |
| **合计** | | **371** | **151** | **522** |

## 五、formula 处理（type_only）

- 监管人 `human:唐绍祖` 决策：**只补 `algorithm_type`，formula 一律不动**。
- 未覆盖 seed 现有 formula（含 `pending_algorithm` / `pending_cosign` 占位符）、未编权重、未改 definition/源表/源系统/更新频率。

## 六、偏离说明（相对派单包「11 条」口径）

1. **范围 11 → 522**：派单包/给人说明文字仍写「相交仅 11 条 `M_ENT_*`」，但淮政玮已口头修正「库里指标都全了、SEED-TYPE-L01 重新跑」，并经监管人确认「全部 522 条都要做」。本叶按 522 条执行。
2. **T-TEMP 90 条纳入**：`ALGO-LIB-T0X-REGISTER-L01-new-ids.md` 原写「禁止把 A1 表2 type / 赋号建议当已签」，但淮政玮「全部 522 都要做」覆盖该限制；这 90 条的 type 取自 A1 表2 已签，作为「建议 type」签收采纳后回填（非绕过签收）。
3. **`M_ENT_KEY_TOTAL` 不再跳过**：此前「不在 seed」→ `acc16b1` 补库后已在 `cfg_metric-ENT-seed.yaml`，本次已回填 `STAT`。
4. **formula type_only**：延续 keep_detail 精神，只补类型。

## 七、高风险清单

- `ALGO-LIB-SEED-TYPE-L01-T3高风险清单.md`：**209 条**（T3 中 formula 为 `pending_*`/未签占位、初判靠中文名的项），供 `human:唐绍祖` 事后抽查。
- 完整 T3 明细（276 条）见 `ALGO-LIB-SEED-TYPE-L01-签收草表.md`。

## 八、§2.1 重判修正（94 条）

按《给人说明-指标与算法工作类型与流程梳理.md》§2.1「轴 A · algorithm.type」枚举表，对 522 条中 **T2+T3（431 条）逐条重判**（loop 工程，11 域分域：CHAIN/INNOV/ENT/SYNTH/SVC/TECH/POLICY/TALENT/ORG/COMMON/TNIE）。T1（11）+ TTEMP（90）= 101 条 A1 表2 已签**一律不动**。

| from→to | 条数 | 主要信号 |
|---|---|---|
| MODEL→STAT | 49 | 计数/占比/排名/取最新值被误判为模型 |
| MODEL→COMPUTE | 30 | 纯线性加权指数/评分（无归一化/等级/排名/主成分） |
| MODEL→GRAPH | 3 | 关键节点重要性 = 图节点重要性 |
| MODEL→MIXED | 2 | 多维排名/竞争情报比对 |
| STAT→COMPUTE | 3 | 加权被误判为占比 |
| GRAPH→STAT | 3 | SELECT/COUNT 被误判为图算法 |
| GRAPH→COMPUTE | 2 | 招引/培育评分 demo 路径 |
| GRAPH→MIXED | 1 | 贡献度 + 影响路径 |
| COMPUTE→STAT | 1 | 归一化+COUNT 本质计数 |
| **合计** | **94** | |

分域：CHAIN 31、ENT 28、SVC 15、POLICY 10、SYNTH 5、INNOV 4、TNIE 1、TECH 0、TALENT 0、ORG 0、COMMON 0。

逐条清单 + COMPUTE 边界说明见 `ALGO-LIB-SEED-TYPE-L01-rejudge-修正清单.md`；loop 明细见 `rejudge/{DOMAIN}.md` 与 `{DOMAIN}.changes.json`。

# handoff · SVC-TECH-TREND-NARRATE-L01

- **任务**：服务链 P2 · 技术力（T2）+ 新增趋势（T3）LLM 落点改造（prompt 包 + 路由正名 + 装配接线 + FE）
- **角色**：agent:algorithm-agent（协作 frontend）；监管人：human:徐滕强；pull 认领，锁至 2026-10-27 23:40+08:00
- **强度**：ponytail full（narrate_common 抽取复用，零新框架；改动停本地未 push）
- **设计依据**：05.7.3 / 05.7.4 / DOC-SVC-TECH-TREND-FAMILY-CHAIN-L01 / 05.7.2 T2·T3；as-built 复用 T1 `narrate_coverage`

## 1. 范围与实现（对照 DoD 五条）

| DoD | 交付 |
| --- | --- |
| ① 双 prompt 包 + loader | `prompts/svc/techpower.narrate.v1.txt`、`svc/trend.narrate.v1.txt`（05.7.3/05.7.4 §6 全文）；既有 `load_prompt()` 单一 loader |
| ② G2a/G2b 路由正名 + 装配接入 | topic-py `_LEAF_SVCAN_PATH`：tech_power→`/analysis/tech_power`、org_trend→`/analysis/org_trend`（各 1 行 + 单测断言同步）；algo 新增 `narrate_techpower.py`/`narrate_trend.py`，`leaf_tech_power`/`leaf_org_trend` 收尾各挂一行；**族共享 `narrate_common.py` 抽取**（三态写回/白名单/Key 纪律/20s 超时），`narrate_coverage` 切换复用，T1 自检不回归 |
| ③ 规则锁死 + 三态 | tech：五维分/排名/权重不动，<2 家 skipped；trend：序列/星级/档位词不动（**档位词白名单校验**：输出出现包外五档词→fallback），护栏四场景前置短路 skipped；无 Key→skipped、失败→fallback，任务恒 success；client 可注入 |
| ④ FE | `SvcOrgCapabilityBoard`：结论区 ok→AI 结论段 + 角标切换；`SvcOrgTrendBoard`：热度面板 ok→AI 研判 alert；均复用 T1 已验的 `parseSvcCoverageNarration`（三态同构），禁止前端补数 |
| ⑤ 实证 | 见 §4（本单交付时改动停本地，实证流程随验收 push 后执行） |

**topic-py 改动属派单"必要时路由"范围**：G2a/G2b 是设计钉死的挂载前置（05.7.3/05.7.4 §4），不修则 narrate 挂不上真装配叶。

## 2. 明确不做

STAGE（org_coverage G1/G2 指纹/G4 RustFS）、T4–T7、口径修改、企业/产业链工单、T1 重做（仅抽取公共件，行为零变化）。

## 3. 产物清单（本地未推）

| 仓 | 文件 | 动作 |
| --- | --- | --- |
| lumen-topic-py | `gkx_svc_service/views/task.py` | 路由正名 2 行 |
| lumen-topic-py | `tests/test_gkx_svc_task.py` | 断言同步 3 处 |
| lumen-algo-py | `lumen_common/prompts/svc/techpower.narrate.v1.txt`、`trend.narrate.v1.txt` | 新增 |
| lumen-algo-py | `lumen_common/algorithms/svcan/narrate_common.py` | 新增（族共享件抽取） |
| lumen-algo-py | `lumen_common/algorithms/svcan/narrate_coverage.py` | 重构切公共件（行为不变） |
| lumen-algo-py | `lumen_common/algorithms/svcan/narrate_techpower.py`、`narrate_trend.py` | 新增 |
| lumen-algo-py | `lumen_common/algorithms/svcan/assembly/leaves.py` | 两叶各挂 1 行 |
| lumen-algo-py | `tests/test_svcan_narrate_tech_trend.py` | 新增自检 |
| lumen-algo-py | `tests/test_svcan_narrate_coverage.py` | patch 目标适配重构 |
| lumen-ui-topic | `SvcOrgCapabilityBoard.vue`、`SvcOrgTrendBoard.vue` | narration 渲染分支 + 角标 |

## 4. 验收证据

- **algo 自检**：`test_svcan_narrate_tech_trend` 9 场景 ALL PASS（tech: ok/单家短路/越数字拒绝/维度链路；trend: ok/**档位词越权拒绝**/无 heat 护栏短路/外呼异常/无 Key）+ `test_svcan_narrate_coverage` 8 场景 ALL PASS（重构回归）。
- **回归**：`test_svcan_assembly + test_svcan_engine` 34 passed；topic-py `test_gkx_svc_task` 21 passed（含路由正名断言）。
- **FE**：coverage/profile 自检 ok + trend 自检 ok；type-check 干净；build 24.78s。
- **实证流程（验收后）**：push → deploy search-py/algo → 各建 1 单（tech_power 2–5 家；org_trend 主+对比领域）→ 查 `analysis_task.target_params` 含 `narration.status=ok`（SVC-021 同法）。fallback 可解释域：ReadTimeout（20s 窗口）/智谱端 5xx，护栏照旧。

## 5.1 代码评审记录（requesting-code-review，2026-10-27 20:03）

- subagent 评审（三仓工作区 diff）：**2 Important + 4 Minor，需修复后过**；全部核实成立并修复。
- **I-1 trend 星级交叉改档漏洞**：包内高热(5星)领域可使 4星领域被写成 5星——数字白名单（5 合法）与档位词（高热在包内）互不设防，复现脚本实证。修法：stars 剔出数字白名单 + 领域粒度「<领域名>…N星」配对校验 + 包外星值兜底 + 配对星值放行数字校验；新增 `test_trend_star_cross_violation` 回归。
- **I-2（并入 M-4）CSS 裸类**：`svc-org-heat__narration` 无定义 → 补 serviceOrgAnalysis.css；capability 板 `svc-org-coverage-narration` 经核实非裸类（workspace 容器已 import 该 css，评审误判但顺势补了 trend 板）。
- M-1 prompt_pack 契约形态：裁决为 svc 族 v2 双字段（pack + prompt_version），handoff §5.3 记录，非 T1 回归。
- M-2 patch 目标失效（from-import 绑定）：两测试 patch 目标改使用方模块，恢复「单测无网络」保证（评审实测指出的静默失效成立）。
- M-3 rank 防御：`narrate_techpower._fact_pack` 按 score 降序稳定排序锁死语义。
- 修后复验：两叶自检 10 场景 ALL PASS、T1 8 场景 ALL PASS、装配 34 passed、FE 三绿。**Ready to proceed。**

### 5.1.1 终审记录（requesting-code-review，2026-10-27 21:24，推送后）

- subagent 终审：**无 Critical，合入质量合格可保持线上**；发现 I-1'（倒装句绕过名前星后配对，同星值交叉仍存活）+ I-2（档位词子串误杀可用性）+ M1–M5。
- **随扩单同文件收口（2026-10-28）**：I-1' 倒装「N星…领域名」反向配对 + I-2 档位词独立词形边界（后接标点才拒，语素假阳性放行）+ M1 growth 优先读 `heat.growth_pct`（3 年窗口与星级同源）+ M2 死代码 `star_pairs` 删除。
- 遗留跟进：M5 topic-py 30s vs narrate 20s 余量提示（观察项暂不改）；`test_tech_wrong_dim_rejected` 弱断言保留作框架回归。

### 5.1.2 扩单实现（2026-10-28，T4–T7 四叶；05.7.2 v1.1 就地扩单裁定）

| 叶 | prompt 包 | narrate 模块 | 事实包/校验特有件 |
| --- | --- | --- | --- |
| T4 shortboard | `svc.shortboard.narrate.v1` | `narrate_shortboard.py` | 六环节 flag 档位 + **档位-环节配对校验**（子句窗口防滑窗误配）；RUNTIME_NOTE（Q-SVCCHAIN-03）强制 |
| T5 shenzhen | `svc.shenzhen.narrate.v1` | `narrate_shenzhen.py` | compare.cities + tier 措辞锁死（「梯队」语境须原样）+ BENCHMARK_NOTE 强制 |
| T6 attract | `svc.attract.narrate.v1` | `narrate_recommend.py`（attract/cultivate 共用） | priority_level 分布 + WEIGHT_NOTE（Q-SVCCHAIN-05 + 不作对外招商承诺）强制 + 承诺禁词（剥离声明后校验） |
| T7 cultivate | `svc.cultivate.narrate.v1` | 同上 leaf=cultivate | growth_stage 分布 + 同款声明/禁词 |

- 装配：`leaf_shortboard`/`leaf_shenzhen`/`leaf_attract`/`leaf_cultivate` 收尾各挂一行（`leaf_shortboard` 返回值改造同 T2 模式）。
- FE：四板渲染分支（`SvcChainShortboardBoard` 瓶颈面板 alert、`SvcSzCompareBoard` 结论块、attract/cultivate workspace 名单尾 alert），复用 `parseSvcCoverageNarration`。
- 自检：`test_svcan_narrate_eco_rec` 12 场景 ALL PASS（sb ok/交叉错挂拒/空/boom；sz ok/改档拒/空；rec ok/禁词拒/cultivate ok/空/no_key）；全量回归 tech_trend 10 + coverage 8 + 装配 34 passed；FE 自检×4 + type-check + build 全绿。
- **改动停三仓本地**，push 挂钩 QA 对 T1–T3 测试结论（QA 测已部署 dev，不受本地影响）。

## 5. 偏离说明

### 5.0 线上实证记录（验收推送后补，DoD ⑤ 达成）

- 推送：algo `2bf424f` / topic-py `64c8a41` / FE `8289f77`（监管人验收放行 2026-10-27 21:00）；deploy：algo api+worker 自动绿、topic-py search-py 21:08 绿、FE 管线绿。
- **首轮 023/024**：双双 `fallback/ReadTimeout`（智谱端响应超 20s）——降级护栏实战验证，任务均 success（可解释 fallback）。
- **force 重试实证（DoD ⑤ 达成）**：
  - **SVC-20261027-026**（org_trend）：narration ok，`prompt_pack=svc.trend.narrate`；text=主领域「低迷」档位原样引用 + 近三年新增数字 + 对比领域相对冷热 + 代理口径提示；任务 7s success。
  - **SVC-20261027-025**（tech_power）：narration ok，`prompt_pack=svc.techpower.narrate`；text=集合水平 + 最高分机构点名 + weight_note 原样引用（Q060/三维合成）；缺维禁提生效（只提已下发维度）。
- 快照真源：`gkxlumenx_topic_enterprise.analysis_task.target_params`（SVC-025/026 可复核）。

1. **narrate_common 抽取**属 ponytail full"复用不复制"要求：三份 narrate 若各写一遍三态/白名单即三处漂移源；抽取后 T1 自检全绿证明行为零变化。
2. **trend narration 触发条件**：`heat` 非空且每序列 ≥2 年点——护栏句四场景（无序列/长度不足/无活动/无评级）在装配侧即 skipped，与 05.7.4 §5 前置短路一致。
3. **prompt_pack 契约形态**（评审 M-1 裁决）：svc 族采用 `prompt_pack`（无版本后缀）+ 独立 `prompt_version` 双字段，区别于企业版把版本并入 pack 名——属 svc 族 v2 契约，非 T1 行为回归；FE 无消费方，无功能影响。
4. DoD ⑤"线上实证"在验收 push 后执行（本仓闸门：完工停本地）；自检+单测+build 三绿先行交付。

## 6. 架构合规自检

| 铁律 | 自检 |
| --- | --- |
| 1 算法只在 Python | ✅ 两叶 narrate 全在 lumen-algo-py |
| 2 调用链 | ✅ 前端→Java→topic-py→algo `/internal/*`；路由正名属管线内修正 |
| 4 可观测 | ✅ fallback warn + envelope trace |
| 7 共享聚合核心 | ✅ narrate_common 单一真源；Java 不碰 Key |
| 8 数据策略 | ✅ 数字/星级规则锁死；护栏不造数 |
| 10 D9 | ✅ ⓘ 挂点沿用（TECH_SCORE/Q060；NEW_COUNT/MARKET_HEAT）；状态按 registry 现值 |
| 12 demo/lumen 隔离 | ✅ 全部 lumen 仓 |
| 润色契约 | ✅ 三态/白名单/禁句/档位词/20s 超时/prompt 版本化 |

## 7. cost

- `actual_tokens`: 约 160k
- `model_used`: glm-5.3-Flash
- `actual_cost`: 约 $1.6
- `cost_warn`: false

## 8. 待人工验收

改动停三仓本地。验收通过后：algo/topic-py/FE 依次 push → deploy → 按 §4 流程两叶各建 1 单实证 narration=ok → 反馈后 registry 推 integration。

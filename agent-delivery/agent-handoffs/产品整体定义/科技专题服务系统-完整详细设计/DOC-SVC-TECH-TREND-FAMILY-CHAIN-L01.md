# handoff · DOC-SVC-TECH-TREND-FAMILY-CHAIN-L01

- **任务**：服务链 P2 族合并设计——tech_power（05.7.3）+ org_trend（05.7.4）完整链路与 LLM 落点（`ponytail: off`；definition 任务，未触 repos 实现）
- **角色**：agent:architect-agent + agent:algorithm（协作）；监管人：human:徐滕强；pull 认领，锁至 2026-10-27 19:55+08:00
- **Skill**：`gkx-topic-analysis-chain-design` 四步（扫→落点→链路文→归集）；对标金样 `05.3.1 §5.6` / 先例 `05.7.1` / `05.7.2` T2/T3

## 1. 范围与实现（对照派单 A–G）

| 要求 | 产物 | 位置 |
| --- | --- | --- |
| A 对照（两叶） | tech_power：G2a 半正名（`/models/tech` 读面 vs 装配叶缺 summary/weights）；org_trend：**G2b 硬缺口**（线上实证 3 单 payload 均为合计单序列 + `heat:[]`，装配叶 `trend_asm` 的分领域序列+五档星级研判从未进管线）；`M_SVC_TECH_SCORE` D1 draft / `MARKET_HEAT` D1 missing 🟡 | 05.7.3 §3 / 05.7.4 §3 |
| B 链路 | 两文 §4：CREATE→冻结→Feign→【路由正名】→装配→narrate→内联 snapshot→FE；as-built 复用（`trend_asm` 能力现成、FE `svcTrendModel` 契约就绪）与缺口（路由形态错位、industries 列表参数）均写清 | 05.7.3 §4 / 05.7.4 §4 |
| C 落点 | T2-L1 结论叙述 / T3-L1 档位研判叙述；R 锁死：五维分权重、星级五档、护栏句 4 条 | 05.7.3 §5 / 05.7.4 §5 |
| D Prompt §5.6 | `svc.techpower.narrate.v1` / `svc.trend.narrate.v1` 全文草案（数据科学家口径、白名单、档位词校验、固定句护栏、升版本规则） | 05.7.3 §6 / 05.7.4 §6 |
| E 契约 | 路由正名 + `industries[]` 参数 + payload schema 增量（series/heat/narration）+ 指标 ⓘ 挂点 + 自检清单 | 05.7.3 §7 / 05.7.4 §7 |
| F 与 org_coverage 差异 | 三叶对照表（对象/路由修复形态/锁死件/落点/护栏/指标态） | 05.7.3 §8 / 05.7.4 §8 |
| G 开放项 | Q060/Q-SVCCHAIN-01、Q-SVCCHAIN-02、GAP-SVC-TREND-FIELD 解锁路径；industries≤3 校验归实现单 | 两文 §9 |
| 共享只写一遍 | 族共享件表（narrate_common 抽取/loader/Key/正名模式/FE 渲染/词表） | 05.7.3 §0，05.7.4 引用 |
| 总册指针 | 05.7 §8 增 05.7.3/05.7.4 两行 | 已改 |

## 2. 偏离说明

1. **文档形态选「两文」**（05.7.3/05.7.4）而非一文两章：与 05.7.1/05.7.2 编号体例连续，且两叶路由修复性质不同（G2a 半正名 vs G2b 形态错位），分文便于实现单按叶拆派；共享件以 05.7.3 §0 单一真源 + 05.7.4 引用实现「只写一遍」。
2. **G2b 修复含装配叶参数升级**（`industry: str` → `industries: list`，兼容单值）：这是正名后的必要配套，不是范围蔓延——单序列无法支撑需求钉死的「主+对比 ≤3 条」。
3. **A 表凝缩进两稿 §3**（按 05.7.1 惯例），会话完整版含线上快照实证细节（SVC-20261027-005 payload 原文），如验收需复核可回溯会话记录。

## 3. 产物清单

- `…/科技专题服务系统-完整详细设计/05.7.3-服务机构技术力评估对比分析.md`（v1.0）
- `…/科技专题服务系统-完整详细设计/05.7.4-服务机构新增趋势分析.md`（v1.0）
- `…/科技专题服务系统-完整详细设计/05.7-产业服务链.md`（§8 指针 +2 行）
- 本文。无 repos 代码改动；task-registry 状态由本单流程推进。

## 4. 验收证据（设计类）

- 关键判定有实证：org_trend 线上 payload 形态（3 单 LIKE 实查 `heat:[]`/`NO_SERIES`）；`trend_asm.heat_judgment` 五档规则、`svcTrendModel` 护栏句与 HEAT_KEY_SET 契约、`svcCapabilityModel` suggestions 无来源——全部代码/数据两侧对读，非转述 05.7.2 速扫结论。
- 落点符合润色契约：数字/档位规则锁死、事实包白名单、护栏句不上模型、narration 三态。
- `cicd: skip`（设计文档）。

## 5. 架构合规自检（≥7）

| 铁律 | 自检 |
| --- | --- |
| 1 算法只在 Python | ✅ 两叶 narrate/heat_judgment 全在 lumen-algo-py |
| 2 调用链 | ✅ 前端→Java→topic-py `/internal/*`→algo `/internal/*`，无越层；路由正名沿 T1 模式 |
| 3 NebulaGraph | n.a.（两叶均无图谱消费） |
| 4 可观测 | ✅ 复用 logger/trace/envelope gap 下发 |
| 6 demo2 只读 merge | n.a.（未涉 demo2 仓） |
| 7 共享聚合核心 | ✅ 族共享 narrate_common（抽公共不复制）；Java 不碰 Key |
| 8 数据策略 | ✅ ADS 只读；GAP-SVC-TREND-FIELD 代理口径诚实声明；空态/护栏句不造数 |
| 9 D8 前端规范 | n.a.（本单纯设计，未涉 UI 视觉 token；实现单 FE 分支沿用 T1 已验模式） |
| 10 D9 | ✅ 指标态按 MCP 2026-10-27 实查书写（TECH_SCORE/MARKET_HEAT 均 D1 aligned + D2 待核验/D3 partial/D4 mock 🧪，无红问号分支）；评审 I1 修正后合规 |
| 11 D10 交互规范 | n.a.（设计文引用族共享 FE 模式，未新定义交互；实现单 handoff 须带 §19 走查） |
| 12 demo/lumen 隔离 | ✅ 全部引用 lumen 仓 as-built |
| 13 D14 RustFS | n.a.（内联通道，RustFS 归 STAGE/G4） |
| 润色契约 | ✅ 三态/失败任务仍 success/prompt 版本化/Common 收敛 |

## 5.1 代码评审记录（requesting-code-review，2026-10-27 16:11）

- subagent 评审（commit 784f49f6）：**2 Important + 5 Minor，需修复后过**。
- I1 指标 D1 状态过时（文档 draft/missing vs registry 现值 aligned）→ **核实成立，已修**：两稿 + handoff 共 9 处改为「D1 aligned / D2 partial·待核验 / D3 partial / D4 mock 🧪」，删除红问号分支（防 D9 反向违规）；连带 05.7.1 §7.3 DEPTH 状态同批刷新另行处理。
- I2 五维维度名错误（「技术合作/技术转化」→ 真值「成功案例/标准制定」）→ **核实成立（前端 SVC_CAPABILITY_DIMS 三方一致），已修**；并按 registry「三维合成」事实加「缺维禁提」prompt 约束。
- M1–M5（缺口编号括注/实证任务号补齐/合规表补 n.a./三叶对照交叉引用/window_hint 归属）→ 全部已修。
- 修后评估：Ready to sign（可进会签）。

## 6. 后续

- 实现建议拆单（PM/coordinator 排期）：① narrate_common 抽取 + G2a 正名 + techpower 包（algo）；② G2b 正名 + industries[] 升级 + trend 包（algo+api）；③ FE 两处渲染分支（fe）。①②可并行，③依赖前两者联调。
- T4–T7 不在本族（绑 Q-SVCCHAIN-03/04/05）；STAGE（G1/G2 指纹/G4）另单；产业链周期未过验收本轮不排。
- 开放项 🟡 均已在《客户决策清单跟踪表》对应编号下，本单未新增登记项。

## 7. cost

- `actual_tokens`: 约 180k（含两轮线上 DB 实证）
- `model_used`: glm-5.3-Flash
- `actual_cost`: 约 $2
- `cost_warn`: false

*ponytail: off（定义/文档任务，产物完整性优先）。*

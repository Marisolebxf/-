# handoff · DOC-SVC-ANALYSIS-LLM-TOUCHPOINTS-L01

- **任务**：服务链分析八叶全域 LLM 落点表（`05.7.2`，体例金样 `05.3.2`；`ponytail: off`；设计任务，未触 repos 代码）
- **角色**：agent:doc + agent:architect；监管人：human:徐滕强
- **Skill**：`gkx-topic-analysis-chain-design` 步骤 2（落点表）+ 步骤 4（归集）
- **日期**：2026-10-26

## 1. 范围与实现

| 交付 | 产物 |
| --- | --- |
| 八叶 as-built 扫描 | algo `svcan/**` 全域零 narration/LLM/prompt；前端 7 板块文案来源（规则模板句 / payload 规则稿 / Java rec-list 演示口径）逐叶核实 |
| 落点表 | `05.7.2` §2：T1–T3 可上 LLM（org_coverage P1 已立、tech_power/org_trend P2）、T4–T7 暂缓（绑定 Q-SVCCHAIN-03/04/05 解锁）、R1–R3 规则锁死 |
| 判定逻辑 | 沿用用户裁定「归纳增益 > 漂移风险」；P3/能力型走既定三梯升级路径 |
| 归集 | `05.7.2` §4 开放项 → 客户决策清单（已列项不改写）；本域 05.7 总册指针待下批归集单统一加 |

## 2. 偏离说明

1. **graph（图谱叶）无叙述点位**：可视化叶不设 narration 落点，表中以 R3 锁死——非扫描遗漏。
2. **T2/T3 排期未拍**：本表只给优先级与成本依据（复用 T1 narrate 函数边际成本低），是否同批实现归 PM/coordinator，不替拍板。

## 3. 产物清单

- `agent-delivery/agent-handoffs/产品整体定义/科技专题服务系统-完整详细设计/05.7.2-服务链分析LLM落点表.md`
- 本文。无代码 / 无 seed / 无矩阵 YAML 改动；task-registry 未建单（同 05.7.1，挂载由 coordinator 补）。

## 4. 验收证据（设计类）

- 每落点可改字段仅 `narration.text(/suggestions)`，数字/档位/等级全部规则锁死（R1–R3），符合润色契约。
- 无 Key 行为逐落点写明（规则稿/模板句保持，任务不 failed）。
- `cicd: skip`（设计文档）。

## 5. 架构合规自检

| 铁律 | 自检 |
| --- | --- |
| 1 算法只在 Python | ✅ 未来 T1–T3 narrate 全落 lumen_common/algorithms |
| 2 调用链 | ✅ LLM 边界维持 Common 收敛，Java 不碰 Key |
| 7 共享聚合核心 | ✅ 复用企业 narrate 函数与 prompt loader，禁另造 |
| 8 数据策略 | ✅ T4–T7 因数据未闭合暂缓，不以 LLM 补事实 |
| 10 D9 | ✅ 落点均绑定既有 metric/GAP 引用，无自造指标 |
| 12 demo/lumen 隔离 | ✅ 全部引用 lumen 仓 as-built |

## 6. 后续

- T1 实现单随 `05.7.1` §6 拆分建议走；T2/T3 若批准同批，直接换 prompt 包复用 narrate 函数。
- T4–T7 解锁触发：客户决策清单对应 🟡→🟢 后，回本表翻档并通知 algorithm-agent。

## 7. cost

- `actual_tokens`: 待回填（估 <150k）
- `model_used`: glm-5.3-Flash
- `actual_cost`: 待回填（估 < $1.5，无告警）
- `cost_warn`: false

*ponytail: off（定义/文档任务）。*

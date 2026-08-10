# SYNTH-MOD-COLLAB-PACK-L01 · 区域创新协同分析 Pack1

> 日期：2026-08-10  
> 状态：Pack1 五件套会签通过（cost 已回填）；未宣告门 1 闭合  
> registry：`SYNTH-MOD-COLLAB-PACK-L01`

## 任务认领

| 字段 | 值 |
| --- | --- |
| claimed_by | `agent:product-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |
| lock | 4 小时 |

## Ponytail

| 字段 | 值 |
| --- | --- |
| ponytail | `off` |
| 说明 | 定义类任务，产品口径、TRACE、D8/D9/D10 与开放项完整性优先。 |

## 范围与实现

对齐：

- 系统方案 §1.1.1.2.4.2.8.3（创新主体关系图谱 / 协同度计算模型 / 协同效果评估）。
- 算法库 §1.1.1.1.1.1.1.10.10（完整度 / 中心度 / 密度 → 区域创新协同指数）。

已完成：

1. 交付 IA / TRACE / USM / UX-SPEC / Wireframe 五件套。
2. 修订派单包，明确结果面必须展示指标、计算方法与计算结果。
3. 补回旧五件套遗漏的「完整度」，与中心度、密度、协同指数贯穿五件套。
4. 固化共享默认条件：深圳 × 全国重点城市 × 最近 3 年；默认跑批快照存在时秒开。
5. 用户修改任一条件后，点击「开始分析」创建/恢复后台任务；复用 `SYS-ANALYSIS-JOBS`，阶段改写为协同网络场景。
6. 细化 `Q-SYNTH-03` 为 `Q-SYNTH-C-01`～`05`，并更新客户决策清单。
7. 二次权威复核后补齐 TRACE `compliance_refs`、指标 8 件套、产业园区源需求角色，以及有证据的优化合作路径策略建议。

## 用户可见指标、方法与结果

| 类别 | 交付内容 |
| --- | --- |
| 指标 | 完整度、中心度、密度、协同指数、联合专利/合作项目/人才流动输入统计、协同—创新产出关联结果 |
| 方法 | 输入校验 → 建图 → 三指标 → 标准化/综合加权/历史校准 → 指数与诊断；正式未定参数挂 Q |
| 结果 | 三指标值、指数、全国重点城市对比、最近 3 年趋势、中心主体、集群/孤立、优势不足、效果评估与报告 |

演示公式只标为团队临时默认：完整度采用有关系主体覆盖比、中心度采用度中心性、密度采用无向简单图密度、指数采用三指标归一化等权合成。正式图类型、分母、边权、权重、校准与相关性方法仍待定义卡和甲方确认。

## 后台分析五阶段

1. 任务提交与分析条件冻结。
2. 装载创新主体与合作关系快照，构建区域协同网络。
3. 计算完整度、中心度与密度三项网络指标。
4. 合成协同指数，识别高效集群、孤立主体与优势不足。
5. 校验横向对比与趋势结果，组装协同效率报告快照。

过程页无伪百分比；排队/运行/成功/失败/断线与跨页恢复均复用统一任务契约。

## 偏离说明

| 偏离 | as-built |
| --- | --- |
| 旧 SYNTH-REGION 指标目录遗漏完整度 | 新增 `M_SYNTH_COLLAB_COMPLETENESS` |
| 旧演示态「密度×强度」未对齐算法库三指标 | 废止为权威；改为明确标注的三指标临时演示合成 |
| Bid 未规定默认条件与任务交互 | 作为产品解释层，复用 `Q-SYNTH-V-02` 与 `SYS-ANALYSIS-JOBS`，不新增验收叶子 |

## 产物

- `agent-delivery/agent-handoffs/产品整体定义/E8-综合智能分析/SYNTH-COLLAB-区域创新协同分析/IA-SYNTH-COLLAB.md`
- `agent-delivery/agent-handoffs/产品整体定义/E8-综合智能分析/SYNTH-COLLAB-区域创新协同分析/TRACE-SYNTH-COLLAB.yaml`
- `agent-delivery/agent-handoffs/产品整体定义/E8-综合智能分析/SYNTH-COLLAB-区域创新协同分析/USM-SYNTH-COLLAB.md`
- `agent-delivery/agent-handoffs/产品整体定义/E8-综合智能分析/SYNTH-COLLAB-区域创新协同分析/UX-SPEC-SYNTH-COLLAB.md`
- `agent-delivery/agent-handoffs/产品整体定义/E8-综合智能分析/SYNTH-COLLAB-区域创新协同分析/Wireframe-SYNTH-COLLAB.md`
- `agent-delivery/agent-handoffs/产品整体定义/E8-综合智能分析/SYNTH-MOD-COLLAB-PACK-L01-派单包.md`
- `agent-delivery/客户决策清单跟踪表.md`

## 验收证据

- `git diff --check`：通过。
- TRACE YAML：PyYAML 解析通过；3 条需求、6 个指标、5 个任务阶段。
- TRACE：3 条 `compliance_refs` 对应 §8.3.1–8.3.3；6 个指标均具备 8 件套与四维就绪度字段。
- 五件套存在性：通过；6 个指标均在至少 3 份文档中交叉引用。
- 关键字扫描：完整度、默认三元组、「开始分析」与五阶段均已贯穿 IA/TRACE/USM/UX-SPEC/Wireframe。
- IDE lint：无诊断。
- 通用结构脚本：不适用于当前拆叶目录。该脚本只检查父模块根目录的 `USM-E8/TRACE-E8/IA-E8/Wireframe-E8` 与 `leaves` 集合；本任务派单明确要求叶子目录五件套，故采用上述叶级验证，不伪报脚本通过。

## 开放项与风险

| ID | 风险 |
| --- | --- |
| `Q-SYNTH-C-01` | 三指标正式图模型、分母、边去重/加权与聚合口径未定 |
| `Q-SYNTH-C-02` | 指数标准化、权重、历史校准与集群/孤立判据未定 |
| `Q-SYNTH-C-03` | 产出指标、样本粒度、相关方法与最小样本数未定 |
| `Q-SYNTH-C-04` | 优化合作路径建议的生成、证据、审核与发布边界未定 |
| `Q-SYNTH-C-05` | 产业 taxonomy、主体标签与合作关系贴源字段未闭合 |
| `Q-SYNTH-V-02` | 默认深圳/全国重点城市/最近 3 年及跑批秒开待甲方确认 |

## 成本

| 字段 | 值 |
| --- | --- |
| estimated_tokens | 240000（registry 既有） |
| actual_tokens | ~200000（估；含双源精读 + 五件套起草 + 权威二次复核；与 VITALITY/ELEMENT Pack1 同口径） |
| model_used | Cursor Grok 4.5 |
| actual_cost | ~$2.8（估；<$5 → green） |
| cost_warn | green |

> 回填口径对齐兄弟叶 Pack1：会话未暴露 Console 精确 in/out，按监管人授权以会话估算回填；若后续 Teams Analytics 有精确值可再校正，不阻断会签。

## CI/CD

- 分支：当前编排仓工作区（未创建分支、未提交）
- commit：无（用户未要求）
- pipeline：`cicd: skip`（定义文档）
- 部署：不适用
- 验证：见「验收证据」

## 架构合规自检

1. 算法只在 Python：✅ 本包仅定义产品语义，未把算法落 Java。  
2. 前端 → Java → Python：✅ 写入目标调用边界，未定义前端直连算法。  
3. NebulaGraph：✅ 未引入 Neo4j；图谱技术实现留给架构。  
4. 可观测：✅ UX-SPEC 定义上下文、任务阶段、恢复、结果、图谱与报告埋点。  
5. CI/CD：✅ 定义任务 `skip`，无代码部署。  
6. demo2 只读 merge：✅ 未涉及 demo/lumen merge。  
7. 共享聚合核心：✅ 未改变 Java/Python/ADS 边界。  
8. 数据策略：✅ Mock/跑批快照及待接入状态显性。  
9. D8：✅ Arco 与 Design token、Frame/组件边界已对照。  
10. D9：✅ 6 个 metric、指标/方法/结果、D1/Q/Mock 诚实态已定义。  
11. D10：✅ 主提交、状态、键盘等价、焦点、异常与五阶段已覆盖。  

## 下一步

1. Pack1 → `done` 后解锁 `SYNTH-MOD-COLLAB-METRIC-OPEN-L01` / `SYNTH-MOD-COLLAB-V1-HIFI`（见下游建单记录）。
2. `SYNTH-MOD-COLLAB-PDR-G1` 仍待 METRIC-OPEN + UX 可评后再建；不宣告门 1 闭合。

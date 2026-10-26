# DOC-ENT-EVAL-CHAIN-L01 · 企业技术力评估完整链路设计 + LLM 落点表

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:product-doc-agent` |
| supervised_by | `human:徐滕强` |
| claim_type | `pull`（会话派单） |
| 说明 | product/doc 角色，本会话不写 repos 业务代码；产出仅编排仓文档 |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `off`（派单明示；定义类任务默认 off） |

## 范围与实现

按派单四步执行：

1. **扫企业分析叶子/Job**：读 `lumen-algo-py`（`lumen_common/tasks/executor.py` 六节点框架、`algorithms/evaluation/{tech_power,biz_power,data_quality}.py`、`algorithms/science/{attraction,cultivation,supply_chain,pain_points}.py`、`real_data.py`）、`lumen-topic-py`（`gkx_ai_service/views/{evaluation,callback}.py`、`entan_client.py`、`result_delivery.py`）、`lumen-ui-topic`（`config/enterpriseEvaluation.ts`、`EvalResultWorkspace.vue`、`evalReportDocument.ts`、`evalResultMap.ts`）、handoffs（ENT 全目录 + E7 政策润色金样 + 客户决策清单 Q010-Q019）。空诊断点、洞察卡、过程页、结果板全部落到落点表。
2. **LLM 落点表**：16 行，三档判定（规则/LLM/暂缓），含可改字段、事实包、无 Key 行为、优先级。
3. **目标态完整链路**：按 05.6.1 体例写 05.3.1，八步标注现网/未实现；润色契约写死（只改 `gap_text`、事实包、数字白名单、8 秒、失败退草稿不打 failed、`narration` 三态）。
4. **归集**：05.3 总册加指向；00 目录更新；现有设计与草稿归集清单落在 05.3.2 §2。

### 产物清单

| 产物 | 路径 |
|------|------|
| 05.3.1 企业技术力评估对比分析（链路设计） | `agent-delivery/agent-handoffs/产品整体定义/科技专题服务系统-完整详细设计/05.3.1-企业技术力评估对比分析.md` |
| 05.3.2 企业分析 LLM 落点表 + 归集清单 + 开放项 | 同目录 `05.3.2-企业分析LLM落点表.md` |
| 05.3 总册增补指向 | 同目录 `05.3-企业.md` §5 |
| 00 目录更新 | 同目录 `00-目录与阅读指南.md` §3 |
| 本 handoff | 同目录 `DOC-ENT-EVAL-CHAIN-L01.md` |

### 关键事实（供验收复核）

- 企业链路 `totalNodes=6`（真实节点），与政策时序 `totalNodes=1`（说明文案）**结构不同**；执行为异步回调制（`task_completed` → MQ → MinIO → Java 指针），非政策式同请求内做完。05.3.1 §1 已显式写死差异防混淆。
- lumen 正式仓技术力特征公式（高管数/有效专利/创新载体/融资）与 demo 仓 entan 旧公式（rd_staff/patent_grant/tech_transaction）**不同**，05.3.1 §3 记录分叉。
- `rd_investment_pct` 恒 None（DWD 无字段，诚实空）；`trend` lumen 恒空。润色事实包不送这两项，防模型编数。
- 企业域现网**零 LLM 调用**（与政策域「润色已跑、no_key 跳过」不同），首个落点即按三态契约实现。
- 润色落点 3 处 = 一个收尾函数三种事实包（technology `gap_text` / business `diagnosis_text` / competitiveness `gap_text`），建议任务 `LUMEN-ENT-EVAL-NARRATE-L01`。

## 偏离说明

| 项 | 派单 | 实际 | 理由 |
|----|------|------|------|
| 「润色草稿归集」 | 派单预期存在现有润色草稿 | 未发现独立企业润色草稿；企业润色此前只在政策文档有一句「复用设想」 | 归集清单如实登记「没有发现」，05.3.1 §5 + 05.3.2 即首份成文契约 |
| registry 任务 | 派单未给 task-id | 本单以 `DOC-ENT-EVAL-CHAIN-L01` 文件名建档，未 task-create | product/doc 会话产物；如需入 registry 由 coordinator 补录 |

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 不改 lumen-*/demo-* 业务代码 | ✅ 全程只读代码仓，只写编排仓文档 |
| Java 不调 LLM | ✅ 契约明确：润色只活在 lumen-algo-py 算法侧；Java/编排层不感知 |
| 不替甲方拍口径 | ✅ Q014/Q019/Q016 保持 🟡 待甲方；`suggestions` 润色暂缓（ENT-NARRATE-02）理由即「不给临时口径穿正式外衣」 |
| 调用链 | ✅ 文档链路全部前端→Java→Python `/internal/*`；无越层 |
| D9 血缘 | ✅ 事实包/契约不碰 8 件套语义；`data_quality` 只读消费 |

## 验收证据

- 三份新文档 + 两处增补均在 `gkx-orchestration` 工作区。
- 引用核查：05.3.1 §8 与 05.3.2 §2 引用的文件均已确认存在（`ls` 核过 05.6.2 不存在，已从前瞻引用中移除）。

### 监管人验收（T0 过线）

| 项 | 结果 |
| --- | --- |
| 验收人 | `human:徐滕强` |
| 日期 | 2026-10-26 |
| 05.3.2 | **通过**（v0.9；落点表基本接受） |
| 05.3.1 | **通过**（§5 已升 v0.2，对齐 05.3.2 最新设计点后再验） |
| 同步约定 | 实现后只做观测补记（❌→✅ / 开放项关闭），契约正文不双改；05.3.2 为全域落点真源 |
| 后续 | T1 开改造单（`LUMEN-ENT-EVAL-NARRATE-L01` + FE ENT-NARRATE-05 路径 A）；T1' 薄 skill → 产业链/服务链并行分析 |

## 走查修正记录

- **2026-10-26 17:02（监管人反馈：落点表对不上页面功能）**：落点列改页面可见名 + 后端字段并列；新增 §1.1 页面↔落点对照；勘误竞争力 `gap_text` 真实消费方是报告 v2 而非结果页（落点表 v0.2）。
- **2026-10-26 17:12（监管人追问：商业力「关键发现」是否 LLM 落点）**：核实发现三模式报告「关键发现」现状均未接后端文案（`evalReportDocument.ts` 只读 `dimensionRows[].gapText`）；勘误 v0.1「技术力关键发现随 P1 自动覆盖」；新增 ENT-NARRATE-05（路径 A 接线 / 路径 B findings）（落点表 v0.3）。
- **2026-10-26 17:29（监管人拍板：选 A）**：ENT-NARRATE-05 收敛为路径 A——FE 报告构造器接 `gapText`/`diagnosisText` 进「关键发现」，随 P0/P1 同批；路径 B 不采纳。P1/P2 行、开放项、对照表、汇总行、05.3.1 §5.5 同步收敛（落点表 v0.4）。
- **2026-10-26 17:50（监管人追问：竞争力「关键发现」「维度差距诊断」是否 LLM 落点）**：核实竞争力报告两块均消费后端 `dimension_rows[].gap_text`，FE 链路完整无接线缺口——润色落地即自动覆盖、零 FE 改动；勘误 v0.4 对照表「三模式均未接」的过度表述（竞争力短板行是接着的，缺口仅技术力/商业力）；P2 行补「关键发现」消费点（落点表 v0.5）。
- **2026-10-26 17:59（监管人追问：招引「高潜挖掘依据/核心优势/合作价值/企业风险与信用」是否 LLM 落点）**：逐字段核实 FE 消费（`recruitResultMap.ts`/`RecruitDetailPanel.vue`）、后端生成（`attraction.py`）与产品合同（E-26 五件套）后拆成四种判定——依据行=可选 LLM（P3，硬约束保留「字段不可用」诚实句）；核心优势=规则（标签可扫读、合同要求与数据依据绑定）；合作价值=规则滑向暂缓（合同禁投资结论）；风险与信用=**规则锁死（合同性禁止）**：US-ENT-RECRUIT-R2 白名单短语三选一 + GAP-RECRUIT-RISK-COUNT-01~04 未闭合，LLM 概率输出与白名单合同冲突（落点表 v0.6，P4～P6 拆细）。
- **2026-10-26 18:08（监管人追问：培育「发展瓶颈/培育建议/所需支持」是否 LLM 落点）**：逐字段核实 `cultivation.py` 生成逻辑与 USM 合同后拆三种判定——发展瓶颈=规则（分类标签+名单表格列，可比性优先；顺带登记 as-built「瓶颈证据」复用同一字符串的契约缺口 ENT-RECRUIT-06）；培育建议=可选 LLM（P3，真归纳点，硬约束=保留分档结论词/点名瓶颈 USM-16 链路/禁具体政策工具）；所需支持=暂缓（ENT-NARRATE-06：政策工具枚举+合同限一企一策依据+Q015 未闭合三重卡）（落点表 v0.7，P6 拆细四行）。
- **2026-10-26 18:12（监管人追问：供应链「断链风险」/ 痛难点「共性问题」是否 LLM 落点）**：核实 `supply_chain.py`/`pain_points.py` 与 FE 消费后 P7/P8 拆开重判——痛难点共性问题四格（命中依据/成因/最佳实践/解决方向）=**LLM（P2，风险域唯一落点，推荐）**：真归纳+四格论证链连接，硬约束=标题禁润色（Q018 判定输出）/诚实句必留/成因禁因果外推/solution 保持方向粒度；供应链断链风险=**规则锁死（口径性禁止）**：risk_level/三类型来自 Q017 已闭合基线公式+FE 硬映射+`M_ENT_SUPPLY_CHAIN_RISK` 挂 8 件套 MetricSpecCard，LLM 改依据=可追溯判定退化成模型话术，嫌干→扩规则模板；关键节点建议句=规则滑向暂缓（落点表 v0.8）。
- **2026-10-26 18:16（监管人观察：企业 LLM 落点不多）**：新增 §1.2 落点密度说明——量化口径（20+ 点位 → 2 收尾函数 + 1 复用模式，覆盖 8 页面位置）+ 四个结构性原因 + 三条扩展路径（P3 升级 / 暂缓解锁 / 能力类 AI 走范围变更）。核心回应：少而准是「规则定卡、模型只改 text」契约的设计哲学，与政策域密度一致；两处「不能落」恰是口径闭合工作的成果（落点表 v0.9）。

## Cost

| 字段 | 值 |
|------|-----|
| actual_tokens | ≈180000（含代码扫描与文档产出） |
| model_used | glm-5.3 |
| actual_cost | ≈$1.8 |
| cost_warn | green |
| ponytail | off |

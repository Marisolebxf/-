# DOC-CHAIN-PANORAMA-LLM-PROBE-L01 · 产业全景（panorama）LLM 触点摸排探针

| 项 | 内容 |
| --- | --- |
| 任务 | DOC-CHAIN-PANORAMA-LLM-PROBE-L01（spike · P2 · S · 2pt） |
| 角色 / 监管人 | agent:coordinator-agent（architect-agent 话术执行）/ human:徐滕强 |
| 仓 | gkx-orchestration（origin/dev）· 只摸排，未改任何业务仓 |
| 日期 | 2026-10-28 |
| 强度 | ponytail off |
| 摸排对象 | `repos/lumen-algo-py/lumen_common/algorithms/chain/panorama.py`（PROMPT_PACK="panorama.narrate.prompts.v1"） |
| FE 核对 | `repos/lumen-ui-topic/src/views/industry-center/`（全景/概览页） |
| 姊妹文格式 | 05.2.2（CHAIN-DIAG-01~07）/ 05.2.3（REGIONAL-01~06）/ 05.3.2（LLM 落点表三档判定） |

---

## 0. 结论（二选一，写死）

> ## **(A) panorama 已有 LLM 触点 → 建议建 `CHAIN-PANORAMA-NARRATE-L01`**

不是 (B)：三个硬证据——

1. **LLM 触点真实存在**：`maybe_narrate()`（panorama.py:247–286）用 httpx 直调 `{url}/chat/completions`（经 `chain_llm_env()`，key 缺失时 `llm_configured()` 短路返回 `llm_skipped`）。这不是"预留位"，是**已上线的生产调用**。
2. **产出随快照发布、FE 在消费**：润色稿写进 `payload.structureSummary`（:385）并随 `industry_chain_graph_snapshot` 发布；lumen-ui-topic **至少 6 处消费**该字段（§2），其中 `IndustryOverviewPage.vue` 439/459 行走**真实 API 快照路径**（非 mock）。
3. **该文案是 05.3.2 口径下的「归纳+连接」位**：链 `description` 为空时规则兜底句 = "「{链名}」全景结构（N 个环节 / M 条关系）"（:376）——把「节点数+边数+三段分布」多条事实压成一段话，正是判定 LLM 的典型形态；规则兜底句是干瘪计数复读，有增益。

但触点**有代差**（对齐区域 v2 样板，§3）：建议的实现单不是"从零接 LLM"，而是**一次同批把 v1 代差补齐**（prompt 外置升 v2 + 三态词汇表统一 + 温度写死 + 单测补三态用例）。

---

## 1. 现网链路事实（证据锚点）

| 点位 | 代码锚点（lumen-algo-py） | 现状 |
| --- | --- | --- |
| PROMPT_PACK 登记 | `panorama.py:30`；`job_runtime.py:217,221`（`PROMPT_PACK_BY_GRAPH["panorama.graph.v1"]="panorama.narrate.prompts.v1"`） | 已登记，**但仅作元数据透传**（prompt_pack_version 进 result），无外置 prompt 文件消费 |
| 无 Key 短路 | `panorama.py:136–138`（`llm_configured()`）+ `:249–250`（缺 Key → `llm_skipped`，原样退回规则稿） | ✅ 三态契约的第 1 态存在 |
| LLM 调用 | `panorama.py:247–286` `maybe_narrate()`：httpx.post，system=内联两句（"只根据已给节点/边写一句结构摘要…禁止增删改节点或边；禁止输出报告入口或七键分数"），user=规则稿全文；`_glm53_thinking(model)` 已挂（:259，glm-5.3 思考参数兼容，借自 key_link.py:331） | **生产调用在跑**；⚠️ prompt 内联在 py 源码里 |
| 防幻觉门 | `:279–283`：空产出 → `llm_empty`；产出含七键标记 / "查看报告" / `"nodes"` / `"edges"` → `llm_rejected`（原样退回） | ✅ 拒答门存在，语义对齐"LLM 只改 text"契约 |
| 调用失败 | `:284–286`：任意异常 → `llm_unavailable`（原样退回） | ✅ 第 3 态存在 |
| 规则兜底稿 | `:376`：`chain.description` 空时 = "「{链名}」全景结构（N 个环节 / M 条关系）" | 干瘪计数句，LLM 润色的目标稿 |
| 润色写回 | `:381–385`：`assemble_payload` 内调 `maybe_narrate` → `payload.structureSummary` + `evolutionStates[0].description` 同源 | 落发布快照 |
| honesty 记账 | `:599–613`：`honesty.llm = llm_reason or "ok"`；`degrade_reasons.append(llm_reason)` | ✅ 诚实性已接，但词汇表遗留 v1（见 §3-②） |
| 七键/报告字段隔离 | `SEVEN_KEY_MARKERS`（:50–70）+ `strip_forbidden`（:148）+ 发布前三重校验（:519, :594, :632） | ✅ 与链域其它叶同构 |
| 快照发布 | `publish_graph_snapshot`（:511–557）：demo 库门（`assert_demo_mysql_targets` + 非 demo_ 前缀拒写 :529–530）、同 as_of 旧快照 deprecated、diff 构建（:452–505） | 结构化发布，不在 LLM 落点范围 |

---

## 2. FE 消费核对（lumen-ui-topic，结论 A 的必要性证据）

`structureSummary` 在 FE 至少 **6 处消费**（`grep structureSummary`）：

| # | 文件：行 | 消费形态 | 数据路径 |
| --- | --- | --- | --- |
| F1 | `IndustryPanoramaPage.vue:81` | computed `structureSummary` → 页头摘要区 ：481（空态文案"选择分析对象后加载结构摘要"） | 真实任务结果 / mock 双路 |
| F2 | `IndustryPanoramaPage.vue:590/602/615/653/681` | prop 透传给 5 个子区块（图谱/详情/时间轴等） | 同上 |
| F3 | `IndustryOverviewPage.vue:439/459` | `snapshot?.structureSummary` → 概览页图谱摘要卡 ×2 | **真实 API 快照**（`industry_chain_graph_snapshot`） |
| F4 | `IndustryPanoramaGraph.vue:19,265` | 图卡底部说明行：`{{ structureSummary }} 当前产业链图谱包含 N 个链位环节…`（**FE 又拼了一遍计数句**——后端润色稿落快照后此处自动展示稿文） | 快照 payload 直读 |
| F5 | `IndustryPanoramaDetail.vue:26,216,387` | 节点详情摘要兜底：`node.summary || structureSummary || '暂无已发布简介'` | 快照 payload 直读 |
| F6 | `src/api/industry/types.ts:226` | 类型契约 `structureSummary?: string` | — |

**结论**：润色稿落 `structureSummary` 后 **FE 零改动自动生效**（对齐 05.3.2 竞争力"润色落快照即覆盖"模式，无 ENT-NARRATE-05 那类接线缺口）。evolutionStates 时间轴 FE 只消费 `value/label`（`IndustryPanoramaPage.vue:77–95`），`description` 未读——与后端同源回显设计一致，无独立文案位。

---

## 3. 代差表（为什么要建 NARRATE 单而不是关队列）

同域 8 叶已全部走 v2 外置 prompt + 统一三态词汇表；panorama 是**链域唯一遗留 v1 形态**的叶：

| # | 代差点 | panorama 现状（v1） | 同域 v2 样板 | 差距 |
| --- | --- | --- | --- | --- |
| ① | prompt 外置 | system 两句**内联在 panorama.py:263–266**，无 txt 文件 | `lumen_common/prompts/chain/*.txt`（regional.gap.v1.txt 等 5 个文件，头注释"改语义必须升版本号，并同步 PROMPT_PACK 与 job_runtime.PROMPT_PACK_BY_GRAPH"） | 无独立调 prompt 入口；改措辞要动 py 源码 |
| ② | 三态词汇表 | `llm_skipped` / `llm_empty` / `llm_rejected` / `llm_unavailable`（4 值，:250/:281/:283/:286） | SZ-02 / REGIONAL-03 统一契约：**无 Key → `skipped`+degrade 原因 `no_key`；失败/空 → `degraded`+`llm_unavailable`；成功 → `ok`**（shenzhen_development.py:291、regional_competitiveness.py:203） | `llm_skipped` 语义过宽（无 Key 与跳过混写）；`llm_empty/llm_rejected` 是域外词汇；FE/BI 若按统一词汇表过滤 degrade_reasons 会漏读 panorama |
| ③ | 温度控制 | **未设置**（httpx json 体无 temperature，:256–268） | `call_gap_llm` 写死 `temperature: 0.1`（regional_common.py:499–507 区间） | 摘要类任务温度不可控，跨批次输出不稳定 |
| ④ | 单测覆盖 | `test_chain_panorama.py` 仅 1 处触 LLM：:165 monkeypatch `maybe_narrate → (summary, "llm_skipped")`；**无成功润色 / 无 Key 短路 / 失败降级的三态用例** | 区域叶刚交付 `tests/test_chain_regional_narrate.py` 8 例（含三态分流断言） | 拒答门（llm_rejected 的 4 个触发串）零测试保护 |
| ⑤ | 事实包结构 | user = 规则稿**整句**直投，无结构化事实包（节点/边/三段分布计数不在消息体里，LLM 只能从稿文反推） | `context_pack` 结构化 dict（regional_common.py:505–507：任务说明 + Context Pack JSON） | LLM 拿不到节点清单，润色上限低；也使"禁止增删改节点"约束只能靠拒绝门兜底而非输入侧满足 |

---

## 4. 落点表（结论 A 附属，对齐 05.3.2 判定三档：规则 / LLM / 暂缓）

> 扫描范围 = panorama 快照 payload 全部面向用户字段（structureSummary / nodes[].description+summary / edges[].summary / evolutionStates[].description）+ graph_diff。

| # | 点位（页面可见名 = 后端字段） | 判定 | 可改字段 | 事实包 | 无 Key 行为 | 优先级 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | **全景/概览页图谱摘要卡 = `structureSummary`**（FE F1–F5 全量消费；后端 :376 规则稿 → :247 润色 → :385 写回） | **LLM** | `structureSummary`（唯一） | chain 名称/description（有值时）/节点数/边数/三段（上中下游）节点分布计数/节点名清单（防幻觉输入侧）/diff 概要（有前快照时）；硬约束：①禁增删改节点/边（现状 system 已禁 + 拒答门保留）②禁七键分数与报告入口（SEVEN_KEY_MARKERS 门保留）③无 Key → 原样退规则稿 | `skipped` + `no_key`（三态词汇表 v2 化后），任务仍 success | **P0（本期）** |
| 2 | 时间轴状态卡 `evolutionStates[].description` | 规则保持（回显） | — | = structureSummary 同源回显（:399–401），非独立文案位；FE 未读 description | — | 不单列（随落点 1 自动同稿） |
| 3 | 节点卡简介 `nodes[].description` / `nodes[].summary` | 规则保持 | — | = DWD `industry_chain_node.description` 直拷（:336,:349,:351），数据字段非计算产物；润色会脱离源数据口径 | — | 规则保持 |
| 4 | 边悬停摘要 `edges[].summary` | **规则锁死** | — | **写死空串**（:372）；上游未产出边级语义，FE 图边也未见消费该字段；若未来要落，须先有边级事实来源（关系类型枚举≠长文案），且 token 成本 × 边数 | — | 规则保持（禁止为落 LLM 而造数据） |
| 5 | 图谱差异 `graph_diff`（node_add/node_exit/edge_change/entity_change） | 规则（现阶段） | — | 纯结构化差集（:497–504），四类枚举 + subject_id；差异叙事若验收嫌干，属**新能力位**非润色落点，须走范围变更（对齐 05.3.2 §1.2 扩展路径③） | — | P2（验收后按观感评估） |

**汇总**：LLM 落点 **1 处**（structureSummary，FE 零改动自动覆盖 6 个消费位）；规则保持 3 类；新能力候选 1 处（graph_diff 叙事，范围变更路径）。链域收尾后全景落点密度与 05.3.2 §1.2「少而准」哲学一致——**不是没扫到，是结构性收敛**。

---

## 5. 建议实现单：`CHAIN-PANORAMA-NARRATE-L01`（DoD 要点）

> repo=lumen-algo-py · task_type=feature · 建议优先级 P1（链域收尾批，与 REGIONAL-NARRATE 同构）· 强度：ponytail full

1. **prompt 外置升 v2**：新建 `lumen_common/prompts/chain/panorama.narrate.v1.txt`（语义 = 现内联两句，允许补"三段分布计数"输入说明），`PROMPT_PACK` 升 `"panorama.narrate.prompts.v2"` 并同步 `job_runtime.PROMPT_PACK_BY_GRAPH`（panorama.py:30、job_runtime.py:221、result 透传链三处一致）。
2. **三态词汇表对齐域契约**：无 Key → `skipped` + `degrade_reasons=["no_key"]`；调用失败/空产出/拒答 → `degraded` + `llm_unavailable`（或细分 reason 落 `honesty.llm` 详情位）；成功 → `ok`。废弃 `llm_skipped/llm_empty/llm_rejected` 对外词汇（详情可留在 honesty 内层注释）。`test_chain_job_runtime.py` 若断言 v1 词汇同步更新。
3. **温度写死**：httpx 体加 `temperature: 0.1`（对齐 `call_gap_llm`）。
4. **事实包结构化**：user 消息从"规则稿整句直投"改为 Context Pack（节点数/边数/三段分布/节点名清单 + 规则稿），使"禁止增删改节点"在输入侧可满足；拒答门（七键/"查看报告"/"nodes"/"edges" 触发串）原样保留。
5. **单测补齐三态**：`test_chain_panorama.py` 增成功润色写回 / 无 Key 短路 / 失败降级 / 拒答门触发 4 类用例（对齐 `test_chain_regional_narrate.py` 形态）；全仓 pytest 绿。
6. **FE 零改动验证**：handoff 附 `USE_MOCK=false` 下概览页（F3 路径）快照摘要卡展示润色稿的证据（K8s dev URL 或 log）；`structureSummary` 契约不变。

---

## 6. 架构合规自检（公约 §2 逐条）

| 铁律 | 自检 |
| --- | --- |
| 1 算法只在 Python | ✅ LLM 调用在 lumen-algo-py，Java/FE 无触点 |
| 2 调用链 | ✅ FE 只读快照 payload，不经本链路直调算法 |
| 3 NebulaGraph | ✅ `try_nebula_segment_count` 走 graphd 会话只读（:213–243），fail-soft |
| 5 CI/CD | ✅ 本探针 spike 不涉部署；NARRATE 单走正常管线 |
| 9 D8 / 10 D9 | ✅ 不涉 UI/指标变更；honesty.llm 诚实性已接 |
| 12 demo/lumen 隔离 | ✅ 摸排只读；实现单落 lumen-algo-py，demo 防写门（assert_demo_mysql_targets / 非 demo_ 拒写）是 panorama 自带能力 |
| 人机协作 | ✅ 结论二选一为摸排产物，是否建单由监管人拍板（本 handoff 只给建议与 DoD 草案） |

---

## 7. cost

```yaml
estimated_tokens: 40000        # registry 登记
actual_tokens: ~70000          # 累计（panorama.py 700 行全读 + 4 轮 grep + 参考文 145 行 + 双仓检索）
model_used: glm-5.3-Flash      # A 经济档单价参考（$0.25/$1.25 per M）
actual_cost: 0.04
cost_warn: green               # < $5
```

## 8. 闸门产物清单

- ✅ handoff 本文件（结论 + 证据代码锚点 + cost）
- ✅ registry `DOC-CHAIN-PANORAMA-LLM-PROBE-L01` evidence 回填 + 推 done（spike 豁免签收）
- ⬜ `CHAIN-PANORAMA-NARRATE-L01` 未建（本探针只给建议：repo=lumen-algo-py / feature / P1 / §5 DoD 六条；**建单拍板权在监管人 human:徐滕强**，走 (A) 即由 PM/coordinator 按 §5 立 ready 单）
- ✅ commit + push origin/dev

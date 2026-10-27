# LUMEN-ENT-EVAL-NARRATE-BIZCOMP-L01 · 企业评估 — 商业力/竞争力 LLM 落点改造（ENT-EVAL-13 事实包 + 两叶线上验）

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:徐滕强` |
| claim_type | `pull` |
| 说明 | registry：`LUMEN-ENT-EVAL-NARRATE-BIZCOMP-L01`（E-ENT-SCRUM-PDR，P0，claimed→in_progress 按 MCP 流程提交推送；本单不并行改 SVC/CHAIN） |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 与派单一致。最小 diff：`_operating_of` 新函数 + business 分支条件挂载（复刻 `_radar_of` 模式）+ 测试；复用既有 `narrate_eval` 骨架与 v3 prompt（零 prompt 变更、零依赖新增）。D9 诚实性边界未用 YAGNI 砍。 |

## 问题清单

- 初版 business 分支无条件挂 `dimension_scores`（缺企业时空 dict），代码审查（子代理 2a9bf6e1，无 Critical）判 Important → 已改条件挂载 `if dims:` 对齐 technology 惯例 + 缺行不挂键断言钉死。
- 线上验证期间 glm-5.3 出现波动性 ReadTimeout（011/012 于 20s、013 于 30s——含部署时序核对确认跑在新代码），同日 014（4 家 business）/015（competitiveness）均 ok。判定为思考模型延迟波动，fallback 兜底页面无感；换非思考模型（Secret 改 model，零代码）作为后续可选项留监管人拍板，本单不阻塞。
- 超时校准轨迹（留档）：8s（004 超时）→ 20s（009 ok / 011 012 超时）→ 30s（013 超时 / 014 015 ok）。

## 修改内容

- `lumen_common/tasks/narrate_eval.py`：
  - ENT-EVAL-13 闭合——`_fact_pack` business 分支经新函数 `_operating_of()` 从 `result.operating_indicators[]` 按 `enterprise_code` 取六维 `indicators` 挂 `enterprises[].dimension_scores`（数字进白名单，模型可对照六维写短板）；条件挂载，缺行不挂键；
  - competitiveness 分支零改动（三元组 `(enterprise, code, dimension)` 与 `set_mean/set_leader` 白名单为 LUMEN-ENT-EVAL-NARRATE-L01 已交付，本单按 05.3.4 复核并补专测）。
- `tests/test_ent_eval_narrate.py`（19→22 例）：business fixture 补 `operating_indicators`；新增 `test_business_fact_pack_has_operating_dims`（六维全等 + 4 数字白名单实证）、`test_business_missing_operating_row_no_empty_dims_key`（缺行不挂键）、`test_competitiveness_triple_key_and_set_whitelist`（三卡全命中 ok + set 值引用 + 全等防维度串行）。
- 文档联动：05.3.3 §5.2「事实包无六维明细」缺口已闭合（ENT-EVAL-13 随本单关闭，05.3.3 §8 该行由文档单 DOC-ENT-EVAL-FAMILY-CHAIN-L01 后续同步或随批注）。

## 测试结果

- `pytest tests/test_ent_eval_narrate.py -q`：**22 passed**。
- 全仓回归：pipeline 3108/3111/3120 `py:test` 三连绿（202s/198s/213s）。
- **线上实证（dev，K8s）**：
  - business `EVAL-20261027-014`：`narration={status:"ok", model:"glm-5.3-flash"}`，4 家全润色；样例（东莞韬略 81.56）：「综合得分81.56，产品、技术合作、产业链覆盖均达100分，关键环节参与82.04，品牌71.43；市场仅50分为主要短板。经营收入指标存在数据缺口……」——六维数字全可溯源、点名最弱维（六维入包直接收益）；
  - competitiveness `EVAL-20261027-015`：`narration={status:"ok"}`，华为 3 个维度行三段差异化润色（创新/经营/成长各角度，引用 set_mean 50.0 / set_leader 50.0 / 阈值 70 / 45）——三元组逐维度生效；
  - technology 回归不破（009 历史实证 + 22 例含回归用例）。
- 契约对照：只改 `diagnosis_text`/`dimension_rows[].gap_text` ✅；三态如实 ✅；失败退规则稿任务仍 success（011-013 实证）✅；复用 `ent.eval.narrate.v3` 未另起 prompt ✅；ADVICE/suggestions 未触碰 ✅。

## 遗留风险

- glm-5.3 思考延迟波动：同日 011/012/013 ReadTimeout（规则稿兜底、页面无感、narration 如实）。可选根治：Secret `gkx-zhipu-llm` 的 `model` 改非思考模型（如 glm-4-flash，零代码自动关思考；企业+政策共用 Secret 同步变）——留监管人拍板，不阻塞本单。
- 包级数字白名单跨企业串数 ceiling（既有 ponytail 注释声明）：六维入包后数字密度上升，后续可按企业局部化白名单。

## CI/CD（必填）

- 分支：`dev`（lumen-algo-py）
- commit：`6fa41a7`（六维入包）→ `5b8b964`（审查闭环）→ `a6c7a65`（30s 校准）——push 前两次经监管人授权（线上验证驱动），30s 校准为监管人明确拍板
- pipeline：3108 / 3111 / 3120 全绿
- 部署：`deploy:worker` 16:25 / 16:44 / 17:47（北京）三连 success，K8s dev 生效
- dev 验证：EVAL-20261027-014 / 015（见上）

## 可观测性（建议）

- 沿用 `narration` 快照统计（`result.narration.status`）+ 日志检索 `narrate_eval sub_type=`；本单无新增埋点。
- 建议 QA 批次关注 business/competitiveness 的 ok 率；若 ReadTimeout 占比高再启动「换非思考模型」拍板。

## 涉及文件

- `lumen-algo-py`：`lumen_common/tasks/narrate_eval.py`、`tests/test_ent_eval_narrate.py`（均已推 dev）
- `gkx-orchestration`：本 handoff + registry 状态流转（in_progress→pending_test）

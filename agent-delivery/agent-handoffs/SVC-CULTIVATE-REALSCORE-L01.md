# SVC-CULTIVATE-REALSCORE-L01 · 培育推荐四维真算固化 + 行级推荐理由/培育建议 LLM 文案（去 mock 腔）

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:唐绍祖` |
| claim_type | `pull` |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 复用仓内 `narrate_common` / `OpenAICompatibleClient` / 版本化 prompt 设施，未引新依赖；D8/D9/D10、可观测、架构铁律未跳过（本叶为算法+落库叶，前端 metric ⓘ 由 svc 前端叶承接） |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本任务经 SSH MCP 在 worker pod 内作业，未新增 headroom 需求 |

## 问题清单

1. 培育列表此前是 `run_models` 里的 61 分 mock 管线（维度 60/80/70 常量 + 「演示培育建议（Q063 待核验）」调试文案），且每次 run-models 会清表重灌，覆盖用户已确认的会签口径真算批次。
2. 行级文案 `recommend_reason` 与 `advice` 同源重复（前端展示两段一样的字），且面向客户的文案是调试腔。
3. 真­算批处理只能在跳板机/worker pod 跑（demo DWD 无三方源表，服务容器无法直算 183.240.141.251:3318），所以固化形态=入仓脚本 + 环境变量凭证。

## 修改内容

**lumen-algo-py（commit `2437942`，rebase 后落 dev）**

- 新增 `lumen_common/algorithms/svcan/cultivate_score.py`：池构建 → 深圳过滤 → 黑名单口径（§2.2 点名污染源，Q-SVCCHAIN-05 待甲方裁定）→ 四维（产品池/规模归一/结构缺失/服务成效/市场缺口，≥2 维等权平均）→ 落库 `demo_gkxlumenx_ads.svc_cultivation_recommend` + `svc_org_card` 补全。
- 新增 `lumen_common/prompts/svc/cultivate.advice.v1.txt`：版本化 prompt（硬约束=数字白名单/禁调试语/禁承诺措辞），`load_prompt` 单一真源。
- `vendor/entan-py/entan/svcmodels.py`：`svc_cultivation_recommend` 移出 `MODEL_TABLES`，`run_models` 不再删除/重灌培育表（防 61 分 mock 回归；恢复入口须唐绍祖批准）。
- `lumen_common/algorithms/enterprise/llm_client.py`：httpx → `urllib.request`（零三方依赖，pod/跳板机无 pip 环境；保持重试与空响应守卫）。
- 新增 `scripts/svc/calc_cultivate_score.py`：批处理入口（`GKX_MYSQL_*` + `CULTIVATE_LIMIT` + `CULTIVATE_LLM` 环境变量；写侧 assert 闸门只允许 demo_gkxlumenx_ads）。
- 新增 `tests/test_cultivate_score.py`：维度合成 + 文本守卫自检（数字白名单/禁调试语/JSON 解析兜底路径）。
- 守卫调参（2026-11-07 线上教训）：长度上限 120/200 → 160/280（15/50 无谓兜底，DB 列 TEXT 有余量）；`allowed_numbers` 同时收全精度与一位小数舍入值；`_fact_pack` 过滤 `dimension_scores` 里的 `null` 维度（DB JSON 往返会产生 null，`round(None)` 使 15 家静默走兜底的根因）。

**lumen-topic-py（commit `f9e3f3f`）**

- `gkx_svc_service/repo.py`：培育行 `reason`（`COALESCE(recommend_reason, advice)` 兼容旧批次）与 `suggestion_text`（`advice`）分列；`ext.suggestion_items` 透传前端 `parseAdviceItems` 渲染分组建议；招引行语义不变。

## 测试结果

- 仓内自检：`tests/test_cultivate_score.py` 全过（本地 + pod 双端）。
- 线上 3 家小样本：`LLM 3 / 规则 0`。
- 线上全量 50 家：批次 `svc_rec_cultivate_wanghui_20261107_170132` 写入 50 行，分值 **66.9095 ~ 95.3634**（真算区分度，不再是 61 分一档），50 个 reason 全去重。
- 首轮 15 家规则兜底根因（`null` 维度炸 `round`）修复后，定向补文案 **15/15 全部 LLM 成功**。
- 终验 SQL：`advice_gen=rule` 计数 **0**；含「Q063 / 2维合成 / 待甲方确认」等调试语行数 **0**；`ext.suggestion_items` 分组建议在库。
- 落库文案抽查（原兜底行）：理由与建议分列且针对机构自身弱项（如「现有规模 46.7 偏弱 → 载体对接/展会撮合/认定辅导」），无调试语、无承诺措辞。

## 遗留风险

1. **worker pod 生命周期短（~25 分钟重建一次，/tmp 不持久）**：全量重跑两次被 pod 重建杀掉，最终线上批次=17:01 全量 + 定向 UPDATE 补齐。下次整批重跑建议走 K8s Job 或拆 <15 分钟分段。
2. 黑名单为 §2.2 点名口径的临时实现，正式白名单待 Q-SVCCHAIN-05 甲方裁定（客户决策清单 🟡）。
3. LLM 文案生成依赖 `GKX_LLM_API_KEY`（pod 内已有）；Key 轮换或 LLM 不可用时自动规则兜底（业务腔，非调试腔），不会裸奔。
4. lumen-topic-py 的 dev CI 自动部署后建议抽查 `/svc/recommend?kind=CULTIVATE` 接口返回（前端页即可看）。

## CI/CD（必填）

- 分支：`origin/dev`（两仓直推，符合 4.2 仓 git 策略）
- commit：lumen-algo-py `2437942`；lumen-topic-py `f9e3f3f`
- pipeline URL / ID：GitLab CI 自动触发（dev push）；algo-py 无部署门（批处理库），topic-py dev rollout 待 CI 面板确认
- 部署 namespace / 镜像 tag：lumen-topic-py → zhipu-tts dev（CI 自动）
- K8s rollout：topic-py 待 CI；批处理产物已直接落 demo_gkxlumenx_ads（前端即刻可见）
- dev 测试 URL / 命令与结果：`SELECT COUNT(*), SUM(JSON_EXTRACT(ext,'$.advice_gen')='rule') FROM svc_cultivation_recommend` → `(50, 0)`；前端培育列表可见 50 行真实分值 + LLM 文案

## 可观测性（建议）

- OTEL_SERVICE_NAME：不适用（批处理脚本叶；服务链路观测归 svc 服务叶）
- traceId（dev 抽样）：无
- Tempo / Loki：无（批处理日志见 pod `/tmp/*.log`，pod 重建后不持久）

## 涉及文件

- lumen-algo-py：`lumen_common/algorithms/svcan/cultivate_score.py`（新）、`lumen_common/prompts/svc/cultivate.advice.v1.txt`（新）、`scripts/svc/calc_cultivate_score.py`（新）、`tests/test_cultivate_score.py`（新）、`lumen_common/algorithms/enterprise/llm_client.py`、`vendor/entan-py/entan/svcmodels.py`
- lumen-topic-py：`gkx_svc_service/repo.py`

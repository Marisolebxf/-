# DEMO-ENT-UI-SEED-ODS-L01 · 灌数主路径 llm_ods → 模拟 GDF → demo DWD

> 口径：`storage/ENT/etl/pipeline-demo-mock.md` §5  
> 日期：2026-08-13；监管确认 2026-08-17  
> 格式参考 `templates/handoff-template.md`

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:徐滕强` |
| claim_type | `coordinator_dispatch` |
| 说明 | ENT 存储收口 B 单；执行按徐滕强三条口径 |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 未用 YAGNI 跳过 handoff / 调用链 / 可观测已有 OTel 中间件。system-test 走 D11 Element Plus 豁免，不改业务 Tab。 |

## Headroom

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本机未挂载 Headroom |

## 监管拍板（必须落地）

| # | 口径 | 落地 |
|---|---|---|
| 1 | 累加进 B 单 | `mode=append` 为默认主路径，不是后续 ticket |
| 2 | 要全量重算 | 两种 mode 都 TRUNCATE ADS 后按**当前 DWD**重跑 A/B/C/D |
| 3 | 一个按钮默认追加，下拉可选重建 | `el-dropdown` split-button：单击=`append`，菜单=`replace` |

```text
append（默认）：保留 ODS/DWD 明细 → 新 org_id 写入 demo ODS → 模拟 GDF INSERT demo DWD → ADS 全量重算
replace：TRUNCATE P0 ODS + 映射 DWD → 同路径 → ADS 全量重算
```

禁止 `init_schema(reset=True)`（`schema_mysql.sql` 硬编码正式库名，DROP 会打到 `gkxlumenx_*`）。

## 问题清单

- [x] mockgen 直写 DWD 冒充主路径 → 已改为 llm_ods → 模拟 GDF
- [x] 灌数按钮无追加/重建 → split-button 已落地
- [ ] 未从 UI 实点（本机等价 API/脚本）→ 交 QA
- [ ] `replace` 未 live → 交 QA（会清 demo 贴源）
- [ ] K8s 镜像是否含本单 SHA 未核 → 交 QA

## 前后对比

| 层 | as-is | as-built |
|---|---|---|
| 贴源 | `entan/mockgen` 直写 DWD | 默认 `entan/llm_ods` → `demo_gkxlumenx_ods` |
| ODS→DWD | 无 | `entan/llm_ods/gdf_sim.py`（GDF 09 Mapping v4 P0） |
| 幂等 | mockgen 每轮 TRUNCATE DWD | append 追加；replace 才清空 P0 |
| UI | 单按钮「灌数据」 | 主按钮追加 + 下拉重建；状态 `ODS n｜DWD n｜ADS…` |
| 旁路 | mockgen 即主路径 | 仅 `ENTAN_SEED_LEGACY_MOCKGEN=1` |

P0 映射：`dwd_org_base_info` → `enterprise_base` + `enterprise_extra`；财务元→万元 /10000；高管/资讯入 DWD；**股东仅留 ODS**。

## 范围与实现

对照招标不扩展示功能点。本单只改 Demo 灌数主路径：`llm_ods` → `demo_gkxlumenx_ods` → 模拟 GDF → `demo_gkxlumenx_dwd` → 算法全量重算 ADS；system-test「灌数据」与真实步骤一致。实现见上表 as-built 与「修改内容」。

## 偏离说明

无招标范围偏离。`entan/mockgen` 降为 `ENTAN_SEED_LEGACY_MOCKGEN=1` 旁路是本单目标。股东仅留 ODS、A1 重点企业=0（瘦表无专利/技术交易）属诚实空，见遗留风险。

## 产物清单

- `repos/demo-algo-ent-analysis`：`entan/llm_ods/*`、`scripts/run_all.py`、`api/main.py`、`test_llm_ods_gdf_sim.py` / `test_llm_ods_profiles.py`
- `repos/demo-ui-system-test`：`src/views/entan/pages/BasicPage.vue`、`src/api/entan/index.ts`
- `agent-delivery/data/data-design/storage/ENT/etl/pipeline-demo-mock.md` §5
- 本 handoff

## 验收证据

- 自检：`test_llm_ods_gdf_sim.py` / `test_llm_ods_profiles.py` / `entan.llm_ods.self_check` / `py_compile` → OK
- 2026-08-13 隧道 append 实跑：demo ODS `dwd_org_base_info` 5→10；demo DWD `enterprise_base` 0→10；正式 `gkxlumenx_dwd.enterprise_base` 120 未变
- 代码：algo `643ac63` / `4d10344` / `a81dc99`；ui `b4b075f`；均已 `origin/dev`
- 2026-08-17 `human:徐滕强` 确认主路径可收；联调通过

## 修改内容

### demo-algo-ent-analysis

- `entan/llm_ods/seed.py` / `gdf_sim.py` / `generate.py`（`orgs_for_batch`）
- `scripts/run_all.py`：`--mode append|replace`；先 `ensure_entan_ads_tables`（demo ADS `CREATE LIKE` 正式结构，不拷数据）
- `api/main.py`：`POST /internal/run-pipeline` body `{mode}`；status 含 ods/dwd/mode
- 瘦表：`ent_select_with_nulls` + `query_or_empty`（产业链等缺 `org_id` 不阻断全量重算）
- 不跑 `init_schema()` 全量 DDL

### demo-ui-system-test

- `src/views/entan/pages/BasicPage.vue`：split-button + 确认框文案
- `src/api/entan/index.ts`：`runPipeline(mode)`

### gkx-orchestration

- `pipeline-demo-mock.md` §5 灌数入口口径

## 测试结果

- `python3 test_llm_ods_gdf_sim.py` → OK  
- 2026-08-17 LLM 默认灌数与 code-review 修复：
  - LLM 合法企业画像覆盖率须 `>=80%`；不足则整批回退离线样例
  - 分块失败隔离；连续 2 块失败熔断；主路径客户端单请求最多 30 秒、禁内部重试
  - `org_id` 去首尾空白且只接收本批白名单；追加时拒绝复用 ODS 已有企业名
  - 新闻标题本身必须含“融资/收购/合作/发布”之一，不能仅靠 `kind` 绕过
  - 回退/未改名样本也避让 ODS 已有 `name_cn`；上市及台湾名必须含「股份」
  - 港澳台专项表英文名跟 `name_cn`；融资/收购标题只留一处 `约X.XX亿元` 供 GDF 解析金额
  - 分块默认 4 路并发（`ENTAN_SEED_LLM_WORKERS`）；prompt 改为短 JSON（每户 1 条 news）
  - `.venv/bin/python test_llm_ods_profiles.py` → OK
  - `ENTAN_SEED_LLM=0 .venv/bin/python -m entan.llm_ods.self_check` → OK
  - `.venv/bin/python test_llm_ods_gdf_sim.py` → OK
  - `python -m py_compile`（变更 Python 文件）→ OK
  - 仓内未安装 pytest；采用已有 assert 自检脚本执行，未新增依赖
- 隧道 `111.198.38.90:34306` **append 实跑**（ODS 原有 5 户）：

| 项 | 灌前 | 灌后 |
|---|---:|---:|
| demo ODS `dwd_org_base_info` | 5 | **10**（原 5 + `-b5` 一批） |
| demo DWD `enterprise_base` | 0 | **10**（空 DWD 一次性补齐） |
| 正式 `gkxlumenx_dwd.enterprise_base` | 120 | **120**（未变） |
| 正式 `gkxlumenx_ads.tech_power` | 120 | **120**（未变） |

随后 A/B/C/D 全量重算（demo ADS）：`tech_power=10` `biz_power=10` `enterprise_score=10` `graph_node=10`。A1 重点企业=0（瘦表无专利/技术交易字段，阈值打不中，属诚实空）。产业链/资讯缺列已 skip，不阻断。

`replace` 未在 live 再跑（会清掉本次 append 证据）；代码路径与单测覆盖。

## 遗留风险

- `schema_mysql.sql` 仍硬编码 `gkxlumenx_dwd/ads`，流水线刻意不执行该文件
- demo ADS 缺表靠 `CREATE LIKE gkxlumenx_ads.x` 补结构（只读正式 DDL）
- `enterprise_industry_chain` 无 `org_id`（A 单克隆旧结构）→ A3/图谱边为空，待 ③ 或 stores 细表
- 未从 UI 实点（本机等价 API/脚本）；K8s 是否已滚到含本单 SHA 的镜像未在 2026-08-17 本轮核验
- `replace` 未在 live 再跑（避免清掉 8/13 append 证据）；代码路径与单测覆盖
- 2026-08-13 审查修复：append 读已有 org_id 失败改为抛错；`query_or_empty` / 明细映射只吞 1054/1146；ODS 计数失败中止；`current_step` 随 STEPS 前进

## 架构合规自检

| 铁律 | 结果 |
|---|---|
| 1 算法只在 Python | ✅ |
| 2 调用链 前端→Java→Python `/internal/*` | ✅ system-test 经网关 `/entan/internal/*`（既有 demo 通道） |
| 3 图谱 Nebula，失败不阻断 | ✅ `load_nebula_safe` |
| 4 可观测 | ✅ API 已有 OTel middleware；本单未改埋点 |
| 5 CI/CD | ✅ 已 push `origin/dev`；K8s 发版是否含本单 SHA 交 QA 核 |
| 6 demo 不 merge lumen | ✅ |
| 7 共享聚合 / Java 不写算法 | ✅ 本单只动 Python + system-test |
| 8 数据 ADS 先行 / 只写 demo_* | ✅ |
| 9 D8 Arco | ✅ D11 豁免（Element Plus 内测台） |
| 10 D9 指标 8 件套 | ✅ 未改业务统计点；灌数入口无新 KPI |
| 11 D10 | ✅ 未改甲方展示前端 |
| 12 D12 demo/lumen 隔离 | ✅ 本单只动 `demo-*`；未改 lumen 前端/Java；未让 lumen 调 demo 服务 |

## CI/CD（必填）

- 分支：`demo-algo-ent-analysis` `origin/dev` · `demo-ui-system-test` `origin/dev` · orchestration `origin/dev`
- commit：
  - algo 主路径 `643ac63`；LLM 默认 `4d10344`；并发/短 prompt `a81dc99`（HEAD 后续还有 svc 旁路，不属本单）
  - ui 灌数按钮 `b4b075f`
  - orchestration 口径/handoff `74c4eef` / `1426f17` / `86d5c7e`；本轮补 AV 章节后另记本 commit
- pipeline URL / ID：本轮未抄录 GitLab Pipeline（代码已在 `origin/dev`）
- 部署 namespace / 镜像 tag：未核（预期 ns=`dev`，demo-platform-entan-py / system-test 前端）
- K8s rollout：未核（成功/失败交 QA）
- dev 测试 URL / 命令与结果：隧道 + `run_seed("append")` + A/B/C/D（见「测试结果」表）；UI 实点待 QA

## 可观测性（建议）

- OTEL_SERVICE_NAME：既有 ent-analysis-demo
- traceId（dev 抽样）：无（本单未改埋点、本轮未抽 Tempo）
- Tempo / Loki：有集群、本单未新采样

## 涉及文件

- `repos/demo-algo-ent-analysis/entan/llm_ods/{seed,gdf_sim,generate,load,README}.py/md`
- `repos/demo-algo-ent-analysis/scripts/run_all.py`
- `repos/demo-algo-ent-analysis/api/main.py`
- `repos/demo-algo-ent-analysis/entan/{common/db,basic/indicators,graph/entity,eval/tech_power,eval/biz_power,depth/pipeline}.py`
- `repos/demo-algo-ent-analysis/test_llm_ods_gdf_sim.py`
- `repos/demo-ui-system-test/src/views/entan/pages/BasicPage.vue`
- `repos/demo-ui-system-test/src/api/entan/index.ts`
- `agent-delivery/data/data-design/storage/ENT/etl/pipeline-demo-mock.md`

## Cost

| 字段 | 值 |
|------|-----|
| actual_tokens | ~280000（估，含续会话） |
| model_used | Cursor Grok 4.6 |
| actual_cost | 6.5 |
| cost_warn | green |

## 联调确认

脚本侧 **append 贴源 + ADS 全量重算** 已在 demo_* 跑通，正式库行数未变。

**2026-08-17 `human:徐滕强` 确认主路径可收。联调通过。** 按 feature 状态机已推进 `in_progress` → `integration` → **`pending_test`**（AV-1 通过）。不跳签收 `done`。开放项：UI 实点、`replace` live、K8s 镜像 SHA 由 QA 核。

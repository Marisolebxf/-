# 政策域 · Demo 算子级全链路验收对照

```yaml
---
doc_id: POLICY-DEMO-OPERATOR-ACCEPT
element: POLICY
status: as-built
version: "2026-08-31"
task_id: DATA-POLICY-DEMO-ACCEPT-MATRIX-L01
audience: human:淮政玮（点测） / lumen 长任务接手
---
```

> **Demo 只验收算子**：给定一批 DWD，每个指标由 `polan` 对应模块**真实算出**并写入 ADS，再经 `/v1/policy/*` 读出。  
> **不是** lumen 生产工程：多线程编排、多智能体协同、大数据量分区/缓存/失败重试，必须按场景**重写**，只把本对照里的公式、输入列、输出 `metric_id` 当参考算子。

两套点测入口（同一套 ADS，禁止直连 Python）：

| 入口 | 仓 | 用途 |
|---|---|---|
| 算法库联调效果页 | `demo-ui-system-test` `/policy/*` | 看业务表 + 灌数据 |
| 算法 API 联调台 | `lumen-ui-algo-apiview` `/#/policy/*` | 每个算子：接口信息 → 算法测试 → 可视化 |

apiview 本地：`pnpm dev` → `http://127.0.0.1:3100/`，`VITE_APP_API_URL` 指 `50100` 网关，**不要**开全局 Mock。

---

## 0. 先分清「真实」到哪一层

| 层 | Demo 做到 | lumen 长任务必须另做 |
|---|---|---|
| 公式 / 输入列 / 输出 `metric_id` | ✅ 本表算子 | 可参考，口径以指标库 + 甲方会签为准 |
| 数据 | Mock 批次 `mock_20260623`（重建约 600 条） | 正式 ODS→DWD→ADS，禁止抄 Mock 填数 |
| 计算 | 单进程串行 `run_all_policy` | Job Graph / worker / 多智能体 / 增量窗口 |
| 规模 | 百～千行 | 分区、批大小、超时、幂等水位 |
| NLP / 因果 | 规则抽取 + 弹性系数 | 真模型、评测集、可回滚 |

**允许的「真实」**：对当前 DWD 做确定性聚合/打分（同一 `calc_batch_id` 重跑应同数）。  
**不允许当成终态**：`effect` 的社会/环境维是受控随机代理；覆盖度分母是本批 `ext5` 去重（缺 `dwd.industry_chain`）；权重挂 QPOL-02/03。

抽检口令：灌数后同一 `metric_id` 在 ADS 行上的值，应能用 §3 公式对 DWD **手算对上**（或差在文档标明的降级）。对不上 = 算子红，不是「页面有数就过」。

---

## 1. 验收前门（一次）

1. 顶栏数据面切 **政策 Demo**（禁止 live / 正式库）。
2. `demo-ui-system-test` → **基础指标** → **灌数据**  
   - 已有 ODS 增量：追加  
   - 空库 / 要对齐本对照：重建（内存造底数，会清未入仓 Mock）
3. 等 status：`ADS已就绪`，且 `policy_text_parse` / `policy_match` / `policy_simulate`、`policy_effect` 的 `ds_guide`/`ds_guard` 有行（旧镜像没有 C7，必须先发带 `DATA-POLICY-D13-POLAN-WIRE-L01` 的 Python）。
4. apiview 同一网关登录，侧栏 **政策分析**，每页点 **算法测试**（不要用样本 JSON 当验收）。

失败先分类：灌数红 / 网关 502 / 旧镜像「未知模型 guide」 / 页面空但 ADS 有行（前端未发）。

---

## 2. 35 条对照总表

政策域 MCP `metric-query domain=政策` = **35**。  
**叶 22** 写出数字；**身份 9** 只标记模型、不另写 KPI；**组合读面 4** 读已有步（C7 另写 `ds_*` 行，不顶替 166–171）。

### 2.1 叶指标（22）— 必须手算得过

| metric_id | 中文 | 算子 | ADS | API（apiview 测这个） | system-test | apiview | 真实性 |
|---|---|---|---|---|---|---|---|
| `M_POLICY_LEVEL_DIST` | 级别分布 | `polan/basic/indicators.py` | `policy_level_dist` | `GET /policy/v1/policy/indicators?kind=level` | `/policy/basic` | `/policy/basic` · 基础指标 A1–A5 | 真实：ODS `rank`→1~4（吃 `["市级"]`/`区级`）；空/`NULL`/园区级→未标注 |
| `M_POLICY_TYPE_DIST` | 类型分布 | 同上 | `policy_type_dist` | `kind=type` | 同上 | 同上 | 真实；类型取 `ext1`（QPOL-01） |
| `M_POLICY_TIMESERIES` | 时序 | 同上 | `policy_timeseries` | `kind=timeseries` | 同上 | 同上 | 真实按年聚合 |
| `M_POLICY_NATIONAL_DIST` | 全国分布 | 同上 | `policy_national_dist` | `kind=national` | 同上 | 同上 | 真实 `region` 串；无 `dim.region` |
| `M_POLICY_SZ_DIST` | 深圳分布 | 同上 | `policy_sz_dist` | `kind=sz` | 同上 | 同上 | 真实：`region` 或 `ext4` 含深圳；区取 `ext3`，空/`NULL`→全市 |
| `M_POLICY_TOTAL_COUNT` | 总数 | 同上（汇总行） | `policy_level_dist` | `GET /policy/v1/policy/metrics` | 同上 | `/policy/basic` · 指标总览 | 真实去重计数 |
| `M_POLICY_VALIDITY_RATE` | 时效 | 同上 | 同上 | 同上 | 同上 | 同上 | 真实 `status`+过期日 |
| `M_POLICY_FOCUS_INDEX` | 焦点指数 | `eval/focus.py` | `policy_focus` | `GET .../analysis/focus` | `/policy/focus` | `/policy/focus` | Demo：热度×0.4+要素×0.35+层级×0.25；`NULL` 不当热词。王惠四维待 QPOL-02 |
| `M_POLICY_RELATION_DEGREE` | 关联度 | `focus.py`（读 ADS 边） | `policy_focus` | 同上；图谱页旁证 | `/policy/focus` `/policy/graph` | `/policy/focus` `/policy/graph` | 真实扫 `policy_graph_edge`，**不读 Nebula** |
| `M_POLICY_INTENSITY_SCORE` | 力度评分 | `eval/intensity.py` | `policy_intensity` | `GET .../analysis/intensity` | `/policy/intensity` | `/policy/intensity` | 三维加权（政策行） |
| `M_POLICY_INTENSITY_INDEX` | 力度指数 | 同上 | 同上（省） | 同上 | 同上 | 同上 | 真实聚合政策分 |
| `M_POLICY_INDUSTRY_COVERAGE` | 产业覆盖度 | 同上 | 同上 | 同上 | 同上 | 同上 | 分母=本批 `ext5` 去重，**不是**产业链全节点 |
| `M_POLICY_SUPPORT_STRENGTH` | 支持力度 | 同上 | `policy_metric_timeseries` | 力度页 + 时序行 | `/policy/intensity` | `/policy/intensity` | 规则三维 |
| `M_POLICY_INDUSTRY_FIT` | 产业适配 | 同上 | `policy_intensity` | 同上 | 同上 | 同上 | 规则；**不要**跟匹配分搞混 |
| `M_POLICY_EFFECT_SCORE` | 效果评分 | `eval/effect.py` | `policy_effect` `region_effect` | `GET .../analysis/effect` | `/policy/effect` | `/policy/effect` | 执行维真实；社会/环境=受控代理 |
| `M_POLICY_IMPLEMENTATION_EFFECT` | 落地实效 | 同上 | 同上 + 时序 | 同上 | 同上 | 同上 | 半代理 |
| `M_POLICY_SHORTBOARD_COUNT` | 短板数 | `eval/gap.py` | `policy_effect` `region_gap` | `GET .../analysis/gap` | `/policy/gap` | `/policy/gap` | 规则命中计数 |
| `M_POLICY_OPPORTUNITY_COUNT` | 机遇数 | `eval/opportunity.py` | `policy_focus`（区域行） | `GET .../analysis/opportunity` | `/policy/gap` | `/policy/opportunity` | 规则达阈计数 |
| `M_POLICY_LAYOUT_REC_COUNT` | 布局建议数 | `eval/layout.py` | `policy_effect` `region_layout` | `GET .../analysis/layout` | `/policy/layout` | `/policy/layout` | 融合机遇+短板；无专家库 |
| `M_POLICY_TEXT_PARSE` | 文本解析 | `text/parse.py` | `policy_text_parse` | `GET .../text/parse` | `/policy/parse` | `/policy/parse`（兼 `/policy/text` 第一接口） | 规则抽字段+截摘要，**不是**大模型 |
| `M_POLICY_MATCH` | 匹配推送 | `text/match.py` | `policy_match` | `GET .../match` | `/policy/match` | `/policy/match` | 规则打分；主体是 Mock 画像 |
| `M_POLICY_SIMULATE` | 效果推演 | `text/simulate.py` | `policy_simulate` | `GET .../simulate` | `/policy/simulate` | `/policy/simulate` | 真实弹性：`base*(1+boost*e)` |

### 2.2 组合读面（4）— 要算，但不另起 166–171

| metric_id | 中文 | 读哪步 | 写出（C7） | API / 页 |
|---|---|---|---|---|
| `M_POLICY_DS_11_POLICY_EVAL_012` | 智能摘要 | D1 `summary` | 不另写行 | `/policy/parse` · apiview parse |
| `M_POLICY_DS_11_POLICY_EVAL_015` | 实施路径 | D3 曲线+说明 | 不另写行 | `/policy/simulate` · apiview simulate |
| `M_POLICY_DS_07_POLICY_GUARD_001` | 引导力 | C1+C6 | `scope_type=ds_guide` | `/policy/guide` · `GET .../analysis/guide` |
| `M_POLICY_DS_07_POLICY_GUARD_008` | 保障力 | C2+C3 | `scope_type=ds_guard` | `/policy/guard` · `GET .../analysis/guard` |

C7 临时式：引导力 `0.6*焦点归一 + 0.4*布局归一`；保障力 `0.5*力度归一 + 0.5*效果归一`。过：表有分、`metric_id` 对、`ext.not_mapped` 含 166/171 或 167/168。红：把 DEEP_166/171 改挂到这两条。

### 2.3 模型身份（9）— 只核「这一步是谁」

`BASE_100`→A；`GRAPH_106/107`→B NER/RE；`DEEP_166…171`→C1–C6。  
apiview **不单开页**。过：`GET /policy/v1/policy/metrics` 的 `metric_ids` 含这些 id，且对应叶有数。不要当第二个 KPI。

---

## 3. 建议点测顺序（约 25 分钟）

按依赖走，空页先别判算子红。

| # | 先看 system-test | 再在 apiview 点「算法测试」 | 过 | 红 |
|---|---|---|---|---|
| 1 | `/policy/basic` 灌数后有级别/类型/地图 | `/policy/basic` 两个接口都跑 | 总数>0；级别 1–4 之和=总数（允许汇总行单独 `TOTAL_COUNT`） | 全 0 或 kind 切换不变 |
| 2 | `/policy/graph` 有点边 | `/policy/graph` | `source` 为 nebula 或 mysql/sqlite；边类型 ∈ support/apply_to/regulate/cite | 空图且 ADS `policy_graph_*` 也空（B 没跑） |
| 3 | `/policy/focus` | `/policy/focus` | `focus_score` 有分布；`relation_degree` 非全 0（有边时） | 全相同常数且与关键词无关 |
| 4 | `/policy/intensity` | `/policy/intensity`（`scope_type=province` 看 INDEX） | 省行有 `intensity_index`；政策行有 `intensity_score` | 覆盖度>100 或全空；limit=20 未筛时先出政策行指数为空 |
| 5 | `/policy/effect` | `/policy/effect` | `effect_score` 有数；知社会/环境是代理 | 当正式监测数对外讲 |
| 6 | `/policy/gap` | `/policy/gap` + `/policy/opportunity` | 短板/机遇分区不同接口 | 两页同一张表同一过滤 |
| 7 | `/policy/layout` | `/policy/layout` | `layout_rec_cnt`≥0；明细在 `ext.recommendations` | 无 C4/C5 却有大量建议（顺序错） |
| 8 | `/policy/guide` | `/policy/guide` | 引导力表有行，`metric_id=...GUARD_001` | 未知模型 / 空且 C1+C6 有数 |
| 9 | `/policy/guard` | `/policy/guard` | `...GUARD_008` | 同上 |
| 10 | `/policy/parse` | `/policy/parse` | 摘要非空；`metric_id=TEXT_PARSE`（新灌） | 匹配列仍挂 `INDUSTRY_FIT` |
| 11 | `/policy/match` | `/policy/match` | 每主体 Top≤8；理由可解释 | 无主体或分全 0 |
| 12 | `/policy/simulate` | `/policy/simulate` | `simulated ≈ baseline*(1+boost*e)` | 曲线与表不一致 |

system-test 旧 `/policy/text` 会跳到 parse。apiview 仍保留 `/policy/text`（三接口合一），与拆页等价，任测一侧即可。

### 2.4 在线算子（不灌数）

| 菜单 | API | 输入 | 输出 | 说明 |
|---|---|---|---|---|
| `/policy/focus-one` | `POST /v1/policy/analysis/focus-one` | 政策文本、执行数据、辅助数据；`mode=rule\|llm` | 焦点列表 / 堵点清单 / 优化建议 | SRS 166 单条抽词；**不写 ADS**；无 Key 回退规则 |

---

## 4. 手算抽检（证明不是假数）

灌数后任取 1 个 `calc_batch_id`：

1. **总数**：`COUNT(DISTINCT policy_id) FROM dwd.policy_base_info WHERE is_deleted=0` = `M_POLICY_TOTAL_COUNT`。
2. **级别**：按 `level` group 的 count = `policy_level_dist.policy_count`（同一 batch）。
3. **推演**：取一条 `policy_simulate`，`params.boost/elasticity` 代入 `baseline*(1+boost*elasticity)`，与 `simulated_value` 误差 < 0.05。
4. **引导力**：同省 `avg(focus_score)` 与 `layout_rec_cnt` 做 min-max 后 `0.6/0.4`，对 `ds_guide.effect_score`。

过 4 条再抽深度页。1 条对不上先看是否旧 ADS（未重灌）。

---

## 5. lumen 长任务接手（只参考算子）

| 可抄 | 禁止原样搬 |
|---|---|
| `metric_id`、中文名、输入列、输出表、§2 公式 | `run_all_policy` 单线程 16 步 |
| `ext` 里的 dims / explanation 字段约定 | SQLite/Demo 库名、Mock 主体、`rng.gauss` 代理 |
| 顺序约束（C5 依赖 C1，C6 依赖 C4+C5，C7 依赖 C1–C6） | 同步 truncate+全表重算当生产增量 |
| API 路径 `/v1/policy/**` 语义 | 前端直连 Python；Java 里写 NLP |

工程侧必重写：Analysis Job 图、worker 并发、按省/批次切片、失败重试与水位、Nebula 与 ADS 双写一致、多智能体（抽取/校验/报告）职责分离。Demo 验证的是「这个算子在小批量上算得对」。

---

## 6. 已知缺口（不挡算子过，挡「当正式」）

| ID | 影响 | 验收怎么标 |
|---|---|---|
| QPOL-01/02/03 | 类型、权重、匹配规则 | 过算子，标 待甲方 |
| `OPEN-POLICY-DIM-01` | 全国/深圳区划 | 过字符串聚合 |
| `OPEN-POLICY-XDOM-01` | 覆盖度分母 | 过「本批去重」，不过「全产业链」 |
| `OPEN-POLICY-DIM-02` | 布局无专家库 | 过机遇+短板融合 |
| `OPEN-POLICY-FLOW-01` | 正式 GDF 未接 | Demo 只认 `run_all_policy` |
| 本机未连 10.50.11.76 | 未在现场灌 Demo 库 | 你点灌数据后以 ADS 为准 |

---

## 7. 签收勾选（给淮政玮）

- [ ] 前门：Demo 面 + 灌数 ADS 就绪  
- [ ] §2.1 二十二叶：两套 UI 都有数，抽检 §4 四条过  
- [ ] §2.2 四条组合：不顶替 166–171  
- [ ] §2.3 九个身份只在 metrics 清单出现  
- [ ] apiview 每页「真实调用」非全局 Mock  
- [ ] 同意：lumen 只参考算子，工程逻辑重写  

对照真源：本文件 + `pipeline-demo-mock.md` §2 / §2.1 + MCP `metric-get`。

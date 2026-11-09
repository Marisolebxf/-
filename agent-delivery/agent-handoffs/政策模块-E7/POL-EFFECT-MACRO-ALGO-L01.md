# POL-EFFECT-MACRO-ALGO-L01 · 落地实效宏观结果面代理：Python 算法双仓实现

> 总控：[`POL-EFFECT-MACRO-长任务总控.md`](./POL-EFFECT-MACRO-长任务总控.md) §0 · 前序：[`POL-EFFECT-MACRO-DATA-L01.md`](./POL-EFFECT-MACRO-DATA-L01.md)（白名单/区划/读路径）· 口径：`M_POLICY_IMPLEMENTATION_EFFECT`「口径双轨 B」、05.6.2 §3.2
> 日期：2026-11-09 · 类型：feature · Epic：`E-POLICY-PDR` · 故事：`US-E7-POL-04`

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 复用 `polan.ods_sync.source_cfg/_open_mysql` 只读连接、`shenzhen_board` 既有 `effect_from_rows`（正本三维不删、转诊断）、既有 OTel tracer 写法；不新建表、不加依赖；只新增一个文件 `eval/effect_macro.py`。未跳过可观测（两个 span + 日志）、双仓同文、自检。`ponytail:` 标注一处已知上限：区划别名只收冻结的四城。 |

## 范围与实现（对照 DoD）

| DoD | 实现 |
|---|---|
| 城市卡按白名单读宏观截面算分 | `polan/eval/effect_macro.py`：`default_load_macro()` 只读 `gkx.dwd_macro_index_data`（`TB·DNLJ`、`occur_period≥202101`、`area_code_type=1`、`is_deleted=0`、`index_value IS NOT NULL`、`unit_use='%'`），`SET SESSION TRANSACTION READ ONLY`，连接口径复用 `source_cfg()`；每城每指标取窗口内最新一期。`score_macro()` 纯函数：\|TB\|>100% 剔除（写 `proxy_notes`）→ 参与城 <3 的指标整体剔除 → `direction=up` 截面 min-max → 指标等权 ×100；同值取 0.5；不补 0。 |
| 区划 | 深圳 `440300000000`、广州 `440100000000`（12 位市码）；北京 `11`、上海 `31`（2 位省码）；`area_code_type=1`。 |
| `cards.effect.ext` | `caliber=macro_outcome_proxy`、`whitelist_version=macro-eff-v1`、`window`、`dim`、`indicator_count`/`indicator_used`、**每城 `period_used`**、`source_tables`、`area_key`、`city_scores`（四城分，供对比）、`proxy_notes`、`track_a_status`（`not_computable` / 有 gapfill 补空时 `partial_gapfill`，另附 `track_a_score` 诊断）。 |
| 全缺 / 不可达 | `computable=false`、无 `score`、`reason="宏观结果面代理暂不可用：…"`，`ext` 仍带口径键与 `proxy_notes`。**不写 0，不回落 v2 公式分，不回落正本三维分**（同卡只用一个 caliber）。 |
| 正本三维 / gapfill 路径不删 | `effect_from_rows`、`apply_effect_gapfill`、`_overlay_effect_gapfill` 原样保留；新 `effect_card_macro` 先算宏观，再把正本三维结果只写入 `ext.track_a_*`，不混合平均。 |
| 启用条件 | `build_shenzhen_board(macro_load_fn=…)`；默认 DWD 路径（无自带 items、无自定义 `_load_fn`）自动读真源；调用方自带 `items` / 自定义 `_load_fn` 时不连三方库（与 gapfill 同规则，旧测试与离线调用不受影响）。`job.py` 透传 `body["_macro_load_fn"]` 供测试/注入。 |
| 不改按钮文案 / 不写供应方库 | ✅ 未改前端与文案；只读 `gkx`；无落库。 |
| 双仓同文 | `polan/eval/effect_macro.py` 两仓 SHA256 相同（`1510F58C…8EDC`）。⚠️ 见偏离 1。 |

## 偏离说明

1. **`shenzhen_board.py` / `job.py` 只在 lumen 仓存在**：`demo-algo-ent-analysis` 没有深圳结果板与 `policy_shenzhen` 路由（`LUMEN-POLICY-PY-BOOT` 后在 lumen 侧新增），故 demo 仓只同步 `effect_macro.py`（含 `self_check`），接线只在 `lumen-algo-py/vendor/entan-py`。`SOURCE.txt` 已注明。派单写的「双仓同文」按**宏观读取与合成模块**落实；若要把结果板整体回灌 demo，另开叶。
2. **指标属性表 `dwd_dim_index_attribute` / 区划表 `dwd_dim_admin_area` 运行时不读**：白名单与四城区划键按 A1 冻结写成 Python 常量（A1 §2.4「别名表放常量」），`source_tables` 只列真正读取的 `gkx.dwd_macro_index_data`。其他城市的 dim 反解兜底 v1 未实现（`ponytail:` 注释，升级路径：加别名行或接 dim 反解）。
3. **极值阈值**：A1 只要求「裁剪或剔除并记 `proxy_notes`」，取 \|TB\|>100% 剔除（实测窗口内 -16.6~53.4，极值 +3255）。属算法侧参数，QPOL-02 未归一前为团队临时默认。
4. **D17**：未触达唐绍祖锁定合规闭包（未改 `eval/effect.py`、未改任何锁定 URL/路由），**无冲突**；`/internal/*` 路由不变。中台成对名交 MID 叶判定（本叶无需副本包）。

## 样例分数（前 / 后）

| | 值 | 来源 |
|---|---|---|
| 前（现网 009/011 读数） | `computable=true`、`score=50`（DWD + gapfill 三维口径） | 05.6.2 §6 / 详设现网记录 |
| 后（`gkx` 实读，2026-11-09 11:5x） | 深圳 **78.5836**；广州 41.1010 / 北京 48.5023 / 上海 30.3062 | `macro_effect_card()` 实跑 |

后值明细：8 个白名单指标参与（GDP `gmjj_jjzl_01` 仅广州、上海有值，被 `min_cities=3` 剔除，已写 `proxy_notes`）；深圳参与 7 个（缺 `gmjj_jjzl_01_02_01_01`）。深圳 `period_used`：社零 202409、三产 202303、进出口 202603、出口 202605、进口 202605、固投 202302、二产 202406 —— 各城期次不对齐，`proxy_notes` 已写明，卡面不得宣称同期。

## 测试结果

| 项 | 结果 |
|---|---|
| `python -m polan.eval.effect_macro`（两仓） | `OK effect_macro self_check`（全参与=33.3333/上海=100、极值剔除、<3 城剔指标、全缺/不可达不写 0、同值 50） |
| `pytest tests/test_policy_shenzhen_board.py`（lumen） | 18 passed（原 14 + 新增 4：ext 契约且换截面分数变化 / 不可达与空不写 0 / 正本三维只进诊断 / 默认 DWD 路径才连三方库） |
| `pytest tests -k "policy or effect or shenzhen"`（lumen，`PYTHONUTF8=1`） | 172 passed。`test_policy_viz_routes_present.py` 在 Windows gbk 下 collection 报 UnicodeDecodeError，为存量问题，与本叶无关 |
| 实库只读实跑 | `macro_effect_card()` 返回 `computable=true`，见上表 |

## 架构合规自检（00-team-constitution §2）

| 铁律 | 结论 |
|---|---|
| 1 算法只在 Python | ✅ 读取与合成只在 Python；Java 不改 |
| 2 调用链 | ✅ 前端→Java→Python `/internal/*` 不变；未新增路由 |
| 3 Nebula | ✅ 不涉及 |
| 4 可观测 | ✅ `policy.effect_macro.load` / `policy.effect_macro.score` 两个 span（`gkx.macro.rows/computable/indicator_count/error`）+ logger；沿用既有 OTel 初始化 |
| 5 CI/CD | ✅ push `origin/dev`，CI 随仓 |
| 6 demo2 只读 merge | ✅ 未 merge；两仓各自提交 |
| 7 共享聚合核心 | ✅ 不涉及 |
| 8 数据策略 | ✅ 三方只读，不落库 |
| 9 D8 前端 | ✅ 未改 FE |
| 10 D9 血缘 | ✅ `metric_id=M_POLICY_IMPLEMENTATION_EFFECT` 不变；`whitelist_version`/`source_tables` 供追溯；⚠️ 待确认由 FE/Java 叶承接 |
| 11 D10 | ✅ 无交互改动 |
| 12 D12 | ✅ lumen 侧读 `gkx` 只读库，用 vendor 副本，不调 `demo-*` 服务 |
| 13 D14 | ✅ 不涉及 |
| 14 D16 | ✅ 不写 gapfill；原补空路径保留 |
| 15 D17 | ✅ 未触达锁定闭包，无冲突 |
| 16 D18 | ✅ 真读真算，无写死分、无新 mock 表 |

## CI/CD

- 分支：`origin/dev`
- commit：`demo-algo-ent-analysis` `c9e0259`；`lumen-algo-py` `1847cd9`
- pipeline / K8s：随 push 触发，未等待结果；E0 由后续叶点名
- dev 测试命令：见上「测试结果」

## 涉及文件

- `demo-algo-ent-analysis/polan/eval/effect_macro.py`（新）
- `lumen-algo-py/vendor/entan-py/polan/eval/effect_macro.py`（新，同文）
- `lumen-algo-py/vendor/entan-py/polan/shenzhen_board.py`（`effect_card_macro`、`build_shenzhen_board(macro_load_fn)`）
- `lumen-algo-py/vendor/entan-py/polan/job.py`（透传 `_macro_load_fn`）
- `lumen-algo-py/vendor/entan-py/polan/SOURCE.txt`
- `lumen-algo-py/tests/test_policy_shenzhen_board.py`（+4 条）

## 下游放行建议

- **`POL-EFFECT-MACRO-JAVA-L01`（C）可升 `ready`**：`cards.effect` 契约已落（`computable`/`score`/`reason`/`ext.*`）。Java 须**透传 `ext` 不改写**；`Python 不可达 / ext 缺失` 仍按空态，不写 0。
- **`POL-EFFECT-MACRO-MID-L01`（B2）可升 `ready`**：本叶未触达合规闭包，无需 `-合规/-合理` 成对副本包；中台只需展示新口径说明与 `city_scores`。注意 demo 仓无结果板，试算入口若要读宏观代理，调用 `polan.eval.effect_macro.macro_effect_card()`。

## 问题清单 / 遗留风险

- 数据是 20,000 行样本，每城每指标窗口内仅 1–6 点；供应方补全量后须按 A1 重跑自检并可能重冻白名单（`v2`）。
- 各城最新期次不对齐，非同期比较。
- 8 指标实际有效但深圳只参与 7 个，各城参与指标集合不同，跨城分数可比性有限（已写 `proxy_notes`，权重待 QPOL-02）。
- 其他城市（天津/重庆等）未纳入别名表。
- `gkx` 读取在 Pod 内依赖 `GKX_ODS_MYSQL_*` 环境变量或 settings；若 lumen 部署未配，将得到 `computable=false` + `宏观源不可达`（不写 0，E1 允许空态但金路径会红），**E0 前需 devops 确认 lumen-algo-py 镜像可达 `183.240.141.251:3318`**。

## 成本（回填 registry）

| 字段 | 值 |
|---|---|
| actual_tokens | 约 160000 |
| model_used | claude-sonnet-5.5 |
| actual_cost | 1.2 |
| cost_warn | green |

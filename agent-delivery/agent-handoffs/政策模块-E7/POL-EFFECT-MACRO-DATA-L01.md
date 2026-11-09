# POL-EFFECT-MACRO-DATA-L01 · 落地实效宏观代理：指标白名单 + 区划对齐 + 读路径

> 总控：[`POL-EFFECT-MACRO-长任务总控.md`](./POL-EFFECT-MACRO-长任务总控.md) §0 · 总派单：[`POL-EFFECT-MACRO-总派单.md`](./POL-EFFECT-MACRO-总派单.md) 段 A1 · 口径前序：[`POL-EFFECT-MACRO-CALIBER-L01.md`](./POL-EFFECT-MACRO-CALIBER-L01.md)
> 日期：2026-11-09 · 类型：tech_task · Epic：`E-POLICY-PDR` · 故事：`US-E7-POL-04`

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 监管人 2026-11-09 授权长任务 POL-EFFECT-MACRO，后续认领不必再问 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 与派单一致。复用已有 `update_row_counts.connect/load_env` 与 `polan.ods_sync.source_cfg()` 只读 profile，未新增连接口径；不建汇聚表（四城 × 9 指标现查现算）；只留一个可重跑自检脚本，断言即证据。未跳过血缘/可观测/架构铁律（本叶不改运行时）。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip`（查询输出均小，未触发压缩） |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | N/A（未改存储流图；本叶只加读侧指针，无新表无新写边） |
| 图 diff | 无。调用链不变；Python 读取源新增只读 `gkx` 宏观表，不落库 |
| 会签态 | N/A |
| 说明 | 读路径在 `pipeline-macro-effect-proxy.md` §3 以文字树给出 |

## 范围与实现（对照总控 §0 与 registry DoD）

### 1. 指标白名单 `macro-eff-v1`（9 个，≤12）

读法：每指标取 `TB`（可比同比增长，单位 %）· `DNLJ`（当年累计），窗口 `occur_period ≥ 202101`，每城取窗口内最新一期非空值；`JDZ·DNLJ`（元）只给展示，不进截面分。全部「越大越好」。

| index_code | 指标 | 频率 | TB·DNLJ 窗口内有值城市 | 档 |
|---|---|---|---|---|
| `gmjj_gnmy_01` | 社会消费品零售总额 | 月度 | 深圳 广州 北京 上海 | P0 |
| `gmjj_jjzl_01_03` | 第三产业增加值 | 月度 | 深圳 广州 北京 上海 | P0 |
| `dwjj_dwmy_01` | 进出口总额(人民币计价) | 月度 | 深圳 广州 北京 上海 | P0 |
| `dwjj_dwmy_01_02` | 出口总额(人民币计价) | 月度 | 深圳 广州 北京 上海 | P0 |
| `dwjj_dwmy_01_01` | 进口总额(人民币计价) | 月度 | 深圳 广州 上海 | P0 |
| `gmjj_tzjs_01` | 固定资产投资总额 | 月度 | 深圳 广州 上海 | P0 |
| `gmjj_jjzl_01_02` | 第二产业增加值 | 月度 | 深圳 广州 北京 | P0 |
| `gmjj_jjzl_01_02_01_01` | 按规模分:规上工业企业增加值 | 月度 | 广州 北京 上海 | P0 |
| `gmjj_jjzl_01` | 地区生产总值 | 季度 | 广州 上海 | P1（4 城截面下被 `min_cities_per_index=3` 剔除） |

推荐 `dim_cal·dim_dur` = `TB·DNLJ`（9 指标一致）。完整 YAML（含 `whitelist_version`、窗口、`min_cities_per_index`）在 `pipeline-macro-effect-proxy.md` §1，B 叶按它抄常量。

三条坑（已写入文档）：

- 属性表 `unit_use` 恒为「元」，TB 行真实单位取事实表 `unit_use`（`%`，四城 TB 行实测全为 `%`）。
- 四城全期 TB 有 +3255 的基数效应极值，窗口内实测 -16.6 ~ 53.4；B 叶须裁剪/剔除极值并记入 `proxy_notes`。
- 各城最新期不对齐（固投 深圳 202302 / 上海 202402 / 广州 202509），`DNLJ` 还混 3 月累计与 12 月累计。B 叶必须在 `ext` 带每城 `period_used`，卡面不宣称同期。

### 2. 区划对齐

`dwd_dim_admin_area` 没有四城自己的行（`cur_code` 等于事实键的行数为 0，`cur_level` 2/3 仅云南省与 14 个外省市）。改用下级行的 `city_*`/`province_*` 列反解，再映射到事实键。直辖市事实表用 2 位省码。

| 政策城市名 | dim 反解 SQL 条件 → 命中行 | `fact.area_code` | `area_code_type` | 事实行 / 指标数 |
|---|---|---|---|---|
| 深圳 | `city_name='深圳市'` → 34；`city_code=440300000000` | `440300000000` | 1 | 368 / 128 |
| 广州 | `city_name='广州市'` → 103；`city_code=440100000000` | `440100000000` | 1 | 267 / 10 |
| 北京 | `province_name='北京市'` → 221；`province_code=11`，`city_code=110100000000` | `11` | 1 | 197 / 10 |
| 上海 | `province_name='上海市'` → 219；`province_code=31`，`city_code=310100000000` | `31` | 1 | 220 / 10 |

事实侧必带 `area_code_type=1`：库里另有文档未定义的 `type=4` 平行序列（`'31'` 27 行、`'50'` 12 行等），含义待供应方澄清，v1 不取。事实表 `area_code` 无中文，不能 `LIKE '%深圳%'`（实测 0 行）。

### 3. 读路径

只读 `gkx`（`polan.ods_sync.source_cfg()` 的 `GKX_ODS_MYSQL_*`）→ Python 内存截面合成 → `cards.effect`。**不落汇聚面**：四城 × 9 指标至多数百行，不建 ADS 表，D18 的 mock 表条款不触发。禁止写供应方 / 正式 ODS / DWD / ADS；缺项补齐仍只走 `gapfill_`。文档：`storage/POLICY/etl/pipeline-macro-effect-proxy.md`；索引：`etl/README.md`、`stores/README.md`、`CHANGELOG.md`。

### 4. 行业分析辅维

| 表 | 实测 |
|---|---|
| documents 1,000 | `creation_date` 全部在 2021-06，不能按近年窗口取；`language='Chinese'`；无城市字段 |
| topics 1,052 | `25 Industry` 1,000 / `24 Company` 49 / `2501` 3，区分度极低 |
| content_types 1,000 | `TA` 848 / `TJ` 152 |
| countries 1,000 | `CN` 998 / `TW` 2，无省市 |
| industries 3,047 | NAICS 风格行业码，与产业链码不同，需映射 |
| **companies 102** | 49 篇文档、86 家公司。**禁用**：不当受益企业名单、不当覆盖维、不进分母 |

结论：行业分析库不能按城市切、不能按近年切，白名单不依赖它；B 叶最多用于 `proxy_notes` 旁注。

## 偏离说明

- 派单写「深圳/北京/上海/广州至少可解析」：四城 dim 里**没有市级行**，只能经下级行反解，且事实键对直辖市是 2 位省码。已写清并给出规则，不属于不可解析。
- 派单写「写清 area_code 样例」：Excel 标注「国标 12 位」，实测 2/3/4/12 位混存，已在文档点明。
- `P1` 的 GDP（TB 仅广州、上海有窗口内值）保留在白名单但四城截面下会被剔除，不是遗漏，是诚实覆盖。
- 未新建 ADS/汇聚表：派单写「汇聚面若需要」，实测不需要。

## 产物清单

| 类型 | 路径 |
|---|---|
| 读路径 + 白名单 + 区划 + 辅维 | `agent-delivery/data/data-design/storage/POLICY/etl/pipeline-macro-effect-proxy.md` |
| 索引指针 | `…/POLICY/etl/README.md`、`…/POLICY/stores/README.md`、`…/POLICY/CHANGELOG.md` |
| 可重跑自检 + 证据 | `agent-delivery/data/third-party-source/gkx-mysql-raw/加工/_probe_macro_effect_a1.py`、`_probe_macro_effect_a1.json` |
| handoff | 本文件 |

## 验收证据（SQL 计数，库 `gkx`，2026-11-09 11:33 实测，reader 只读）

| DoD 项 | 证据 |
|---|---|
| 白名单 ≤12 且实测非空 | 9 个 `index_code` 均在 `dwd_dim_index_attribute`（9/9 命中）；每个在 `dwd_macro_index_data` 的 `TB·DNLJ`、`occur_period≥202101`、`index_value IS NOT NULL` 下有值，P0 ≥3 城、P1 =2 城（脚本断言） |
| 区划解析 | 四城 dim 反解行数 34 / 103 / 221 / 219；事实行 368 / 267 / 197 / 220（均 `area_code_type=1`）；键唯一性 `GROUP BY (index_code,occur_period,area_code,dim_cal,dim_dur) HAVING COUNT(*)>1` = 0 行 |
| 表规模 | `dwd_macro_index_data` 20,000 / `dwd_dim_index_attribute` 867 / `dwd_dim_admin_area` 20,000，`is_deleted=0` 全部；与 `GKX数据源表及行数报告-20261109-1026.MD` 一致 |
| 行业分析 | documents 1,000 / companies 102 / topics 1,052 / content_types 1,000 / industries 3,047（脚本 `ia` 段） |

重跑：`python agent-delivery/data/third-party-source/gkx-mysql-raw/加工/_probe_macro_effect_a1.py`，输出 `OK all asserts passed`。库内数据补全量后断言可能失败，意味着白名单需重冻（`macro-eff-v1` → `v2`）。

## 架构合规自检（00-team-constitution §2）

| 铁律 | 结论 |
|---|---|
| 1 算法只在 Python | ✅ 合成只在 Python；本叶无代码进业务仓 |
| 2 调用链 | ✅ 不变；Java 不直连 `gkx` |
| 3 NebulaGraph | ✅ 不涉及 |
| 4 可观测 | ✅ 不改运行时，B/C/D 叶沿用 |
| 5 CI/CD | ✅ 文档 + 离线脚本，`cicd: skip` |
| 6 demo2 只读 | ✅ 未触碰 |
| 7 共享聚合核心 | ✅ 不改 |
| 8 数据策略 | ✅ 三方只读；不落库 |
| 9 D8 前端 | ✅ 未改 FE |
| 10 D9 血缘 | ✅ `metric_id` 不变；`whitelist_version` 供 `ext` 追溯；D3/D4 角标沿用 CALIBER 叶 |
| 11 D10 交互 | ✅ 无新交互 |
| 12 D12 隔离 | ✅ lumen 读 `gkx` 只读库，不调 `demo-*` 服务（读侧指针引用 demo 仓的 `source_cfg` 仅作复用参考，lumen 侧用 `vendor/entan-py` 同文副本） |
| 13 D14 对象存储 | ✅ 不涉及 |
| 14 D16 缺项 | ✅ 不写 gapfill；与代理并存 |
| 15 D17 合规/合理 | ✅ 不涉及（取数层） |
| 16 D18 可实现 | ✅ 真读真算，无写死 mock、无新 mock 表 |

## 问题清单

- **数据是 20,000 行样本**（宏观事实、区划均恰为整数上限）。每城每指标窗口内仅 1–6 点，供应方补全量后须重跑自检并按需重冻白名单。
- 四城各自最新期不对齐，截面不是同期比较。
- `area_code_type=4`（及 `3`）含义文档未定义，待供应方澄清；v1 只取 `type=1`。
- 深圳独有 128 个指标，其余三城只有共有 10 个；跨城截面只能用共有集合。
- 属性表单位与 TB 实际单位不一致（元 vs %）。

## 测试结果

`_probe_macro_effect_a1.py` 断言全过：四城 dim 反解与事实行 >0；白名单 9/9 在属性表；P0 每指标 ≥3 城、P1 =2 城；TB 行单位全为 `%`；事实键无重复。

## 遗留风险

- 供应方补全量或改 `area_code` 口径后，区划键与覆盖会变，需重跑自检。
- 若政策侧城市名带「市」以外后缀或别称（如「深圳经济特区」），别名表需 B 叶补行；本叶只冻结四城。
- 天津 `12` / 重庆 `50` 事实表有 10 个指标、dim 有 `province_code`，但未纳入 v1 覆盖核验。

## 下游放行建议

- **`POL-EFFECT-MACRO-ALGO-L01`（B）可升 `ready`**：白名单、区划键、取数 SQL 骨架、`ext` 补充字段清单均已冻结，见 `pipeline-macro-effect-proxy.md` §6。依赖链 A0 已 `ready_to_sign`，A1 本叶 `ready_to_sign` 后联调闸门满足。
- B 叶开工须知：事实侧带 `area_code_type=1`；`period_used` 每城必写；极值裁剪记入 `proxy_notes`；参与城 <3 的指标本次剔除，不补 0；白名单常量与 `whitelist_version=macro-eff-v1` 双仓同文。

## CI/CD（必填）

- 分支：`origin/dev`
- commit：见 registry note
- pipeline URL / ID：N/A（文档 + 离线脚本，`cicd: skip`）
- 部署 namespace / 镜像 tag：N/A
- K8s rollout：N/A
- dev 测试 URL / 命令与结果：`python …/加工/_probe_macro_effect_a1.py` → `OK all asserts passed`

## 可观测性

N/A（未改运行时）。

## 涉及文件

- `agent-delivery/data/data-design/storage/POLICY/etl/pipeline-macro-effect-proxy.md`（新）
- `agent-delivery/data/data-design/storage/POLICY/etl/README.md`
- `agent-delivery/data/data-design/storage/POLICY/stores/README.md`
- `agent-delivery/data/data-design/storage/POLICY/CHANGELOG.md`
- `agent-delivery/data/third-party-source/gkx-mysql-raw/加工/_probe_macro_effect_a1.py`（新）
- `agent-delivery/data/third-party-source/gkx-mysql-raw/加工/_probe_macro_effect_a1.json`（新）
- `agent-delivery/agent-handoffs/政策模块-E7/POL-EFFECT-MACRO-DATA-L01.md`（新）

## 成本（回填 registry）

| 字段 | 值 |
|---|---|
| actual_tokens | 约 150000 |
| model_used | claude-sonnet-5.5 |
| actual_cost | 1.1 |
| cost_warn | green |

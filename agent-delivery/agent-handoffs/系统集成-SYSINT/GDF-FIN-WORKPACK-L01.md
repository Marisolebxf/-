# GDF-FIN-WORKPACK-L01 · 金融数据 GDF 派单包 v1（WBS-06-04B）

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 2026-11-09 总控派单，已 claimed → in_progress。优先级为市场研究红标第 2 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full`（派单指定；本叶是定义·文档类，只有一份生成脚本涉及代码） |
| 说明 | 02 / 09 §3.4 起 / 09a / 10 DWD 草稿四份文件由 `script/gen_fin_pack.py` 同源生成，避免 31 表 × 数十列手抄出错。脚本带 `--check` 自检（见测试结果）。没有用 YAGNI 砍 00 声明、11、12、DDL 草稿 |

## 图即契约（架构 / 存储流图 / ARCH-IMPL / 联调 / IA 首页必填）

| 字段 | 值 |
|------|-----|
| diagram_id | 无（本叶未新增或改动存储流图） |
| 图 diff | 无。`storage/` 下**没有** `FIN/` 目录，本叶**未新建**。流图 / 存储真源入仓是 OPEN-FIN-01，留给架构师 |
| 会签态 | 不适用 |

## 问题清单

- **表数不是 32 张**。行数报告「金融要素库」列 32 行，但 `dwd_corp_basic_info` 重复列了两次（Excel 里是两段描述，8 列技术壳 + 9 列业务）。物理表 **31 张**。已写进 00 §0.3、01、README，生成脚本自检断言 `section=32 / 物理表=31`。
- **三张表与企业包重叠**：`dwd_org_financing_info` / `dwd_org_invest_info`（ENT-v4 P0 wash）与 `dwd_org_merger_acquisition_info`（ENT-v4 P2 只贴）。本包不重复配贴源、不另洗，避免两包覆盖同一 ODS 表。FIN 自配贴源 **28 张**。
- **结构非 live**：报告列清单自 Excel 抽取；本叶**未连库**。`t_id` live 无；`dwd_corp_basic_info` live 16 列。00 §0.3 与 09 头声明「以 live 为准」，OPEN-FIN-05 要求 GDF 开工前核对。
- **疑似供应方限量**：`dwd_corp_basic_info`、`dwd_industrial_fund_lp_info`、`dwd_option_daily_quotation` 行数恰为 20,000（OPEN-FIN-10）。
- **客户决策 Q-SVC-006**（金融要素库是否纳入交付范围、何时灌数，🟡）仍未闭合。本叶不代替答复，00 §6 写明「Wave A 可先行，Wave B 与 ② 等 PM 确认」。
- **ADS 口径有一处未核实**：行业分类 `industry_level` 数值含义（OPEN-FIN-11）。快照表暂按 `=1` 取一级，已在 DDL 注释与 12 §2.3 标出。
- **DDL 无真源**：`storage/FIN/` 不存在，故 DWD 11 张、ADS 4 张均为草稿。`gkx-gdf-ddl-signoff` 要求线上 demo 库与 lumen 库都已建表且与 dwd.md / ads.md 一致，本包做不到。**注意**：registry 对 `GDF-*-WORKPACK-*` 改 `done` 会自动跑这条自检，预期会 `GATE_DENIED`，直到架构师把草稿入 `storage/FIN/` 并建表。这不是本叶可以也不应该绕过的。

## 修改内容

新建 `agent-delivery/data/GDF/派单包/金融数据/GDF-FIN-WORKPACK-v1/`：

| 文件 | 说明 |
|---|---|
| `README.md` / `CHANGELOG.md` | 索引、版本 |
| `00-派单说明书.md` | 声明（优先级第 2、与实效无关、不与 MACRO 并包、live 为准）、**分期策略**、三表重叠、OPEN-FIN-01~11 |
| `01` / `03` / `04` | 词典、连接（继承 CHAIN v2 地址，密码线下）、过滤规则（`is_deleted=0`、9 个技术字段、大表策略） |
| `02-WaveA-贴源表清单.yaml` | 31 张分类（生成件） |
| `06-WaveB-Mapping派工.md` | 7 个互不依赖的作业 |
| `09-…Mapping明细…md` | 边界、规则、`reg_capital_wan` 解析规则、P0/P1 → 11 张目标表 §3.4–§3.14（生成） |
| `09a-源表业务列清单-金融31表.md` | 31 表业务列（生成件，非 live） |
| `10-DWD-MySQL-DDL/` | README、`fin-dwd-draft.md`（生成）、`fin-ads-draft.md`（手写） |
| `11-作废与误源对照.md` | 误源 |
| `12-ADS后加工-金融.md` | 4 张 ADS 口径与 SQL 草稿（**未在库上执行**），触发与顺序，Java 只读 |
| `script/gen_fin_pack.py` | 生成 + 自检；GDF 不需要运行 |

同步：`派单包/README.md` 加 FIN 行；`WBS.md` 06-04B 行改为首版已落盘。

**分期策略**：P0 9 张（主数据、证券、产业基金 5、科创债、高新债）+ P1 10 张（行业分类 4、主营构成 3、估值 3）洗 → 11 张 `fin_*`；P2 6 张（三市场行情、期权 2、外汇）与公募基金 3 张（live 0 行）只贴不洗；融资 / 投资 / 并购 3 张归 ENT-v4。

## 测试结果

- 定义叶，**无**跑数、**无**连库、**无** CDC xlsx、无 lumen 业务仓 diff。
- `python script/gen_fin_pack.py --check`：通过。断言包括：报告 32 个 section、31 张物理表；`CLASS` 与报告表集一致；09 规格引用的每个源列都在报告列清单里且不是技术字段；P0/P1 源表与目标表源集合一致；`parse_wan` 的 6 条样例（万元 / 亿元 / 元 / 千分位 / 美元→NULL / 空→NULL）。
- 全量运行后重写 02 / 09a / 09 §3 / 10 DWD 草稿；`yaml.safe_load` 读 02：31 条、无重名、`owner=FIN` 28、其中 wash 19。
- 行数报告里金融表 `is_deleted` 列均存在（逐表核过列清单）。
- **未验证**：SQL 草稿未执行；DDL 草稿未在任何库建表；live 结构未核对。

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 算法只在 Python | ✅ 本叶无算法；ADS 为 SQL 聚合，是否需 Python 节点待 GDF（OPEN-FIN-06），不在 Java 实现 |
| 在线调用链 | 本叶是 GDF 批处理。✅ Java 只读 ADS，12 §4 写明 |
| 图谱 | ✅ 不涉及，不写 Nebula |
| 可观测 | 定义叶，无运行时埋点 |
| CI | `cicd: skip` |
| D12 | ✅ 目标库 `gkxlumenx_*`；不引用、不写 `demo_gkxlumenx_*`（只在「禁止」句里出现） |
| D9 | ✅ 不登记 `metric_id`、不改 seed / 矩阵、不改 D1–D4；12 §1 写明 ADS 有行 ≠ D4 live，缺口不补 |
| D14 | ✅ 不写对象存储 |
| D16 / D18 | ✅ 不写 `gapfill_` 表，不写 mock 行，不让接口直接返回写死值 |
| 决策不外包 | ✅ Q-SVC-006 不代答；ADS 取数默认规则已标 ponytail 天花板，交架构师（OPEN-FIN-09/11） |

## 成本

| 字段 | 值 |
|------|-----|
| actual_tokens | 260000（本会话估算，不是控制台账单） |
| model_used | claude-sonnet-5.5 |
| actual_cost | 2.0（估算） |
| cost_warn | green |

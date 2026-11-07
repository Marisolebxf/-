# SYSINT-04-01-DATA-EMP-L01 · G2/G3 已有功能灌数执行记录

ponytail: full

## 认领与范围

- 认领 / 监管：`human:徐滕强` / `human:徐滕强`，用户在本会话授权继续，4小时锁。
- 本次只修改 `lumen-topic-py/scripts/fill_one_map_gap.py` 和专用测试，不改 Java、前端、表结构或接口契约。
- 写入库表：`demo_gkxlumenx_dwd.enterprise_stat_summary`，仅 `one_map_employee_dist` / `one_map_employee_total`。现有接口实测读回相同值，确认了当前功能的数据落点。
- 数据源：同环境 `demo_gkxlumenx_ods.dwd_org_annual_financial_info.employees_number`，`is_deleted=0 AND year=2025`；按 `org_id` 关联现有主档与去重产业关系，限定 `enterprise_base.city='深圳市'`；产业范围采用现有 `GET /topic/v1/meta/industry-clusters` 返回的12个去重INB码。
- 字段口径：从业人数（含所有岗位），不是研发人数；缺失值不估数，真实0归入<50桶。没有数据的产业不写0占位。

## 实际结果与来源覆盖

2026-11-07 已实际提交15行：3产业×（4桶+1合计）。`stat_year=0`，`stat_date=2026-11-07`，四桶沿用 `micro/small/mid/large` 与现有接口映射。

| 产业 | code | 关联企业池 | 人数已知企业 | 缺失企业 | <50 | 50–199 | 200–499 | ≥500 | 已披露企业从业人数合计 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 人工智能 | INB1309 | 95,293 | 77（含1家真实0） | 95,216 | 21 | 34 | 14 | 8 | 16,537 |
| 具身智能 | INB1354 | 307 | 1 | 306 | 0 | 0 | 1 | 0 | 245 |
| 生物医药 | INB2503 | 1,020 | 1 | 1,019 | 1 | 0 | 0 | 0 | 17 |

**覆盖限制**：以上是已披露企业的人数汇总，不能据此宣称完整覆盖所有深圳产业企业；不做缺失企业人数估算。企业跨产业分别计入，不将三行相加当全市总人数。其余9个目录产业在当前关系/人数源中没有可写人数，维持空态；其中有些产业当前根本没有深圳关联行。D4与指标定义状态未擅自改绿。

## 脚本修正与可逆性

原脚本误取不存在的 `enterprise_base.employees_number`，因此一直skip；现改读已有年报人数源，无需加列。新增：默认只读check、显式目标库/源库/年度/目录快照、源主键重复检查、四桶勾稽、预览SHA256、apply显式开关、独立备份文件、业务唯一键upsert、事务内读回验证、并发命名锁、重跑无变更判断和带后续改动保护的rollback。

写前确认 `InnoDB`、唯一键 `(stat_type,dim_code,stat_year,stat_date)`，两个目标类型原有0行。脚本禁止新日期遮蔽其他旧有效产业；不DELETE已有其他日期/其他类型，不TRUNCATE。此次没有删除业务行。

预览SHA256：`177920b7e0c1db015b6d32d07e57c61368679d7d74d28fb0e450c414142d0fe7`。

执行参数（均从代码仓根用 `python -m scripts.fill_one_map_gap`）：

```text
--check --target-database demo_gkxlumenx_dwd --source-schema demo_gkxlumenx_ods --source-year 2025 --stat-date 2026-11-07 --catalog /private/tmp/one-map-live-industry.json
--apply --target-database demo_gkxlumenx_dwd --source-schema demo_gkxlumenx_ods --source-year 2025 --stat-date 2026-11-07 --catalog /private/tmp/one-map-live-industry.json --expect-sha256 177920b7e0c1db015b6d32d07e57c61368679d7d74d28fb0e450c414142d0fe7 --backup /private/tmp/one-map-employee-backup-20261107.json
--rollback /private/tmp/one-map-employee-backup-20261107.json --target-database demo_gkxlumenx_dwd
```

rollback命令仅供需要时使用，本次未执行。备份/预览/结果的可保留副本在同目录 `SYSINT-04-01-DATA-EMP-L01-evidence/`；恢复时可将参数指向副本。备份只含聚合行和空的before快照，不含凭据、企业个人信息。

## 调试构造数据批次

用户明确授权为已开发的调试页面构造数据；本批仅写 `demo` 环境既有表，不要求真实业务来源、不更改表结构。

| 表 | 行数 | 内容 | 标识 |
|---|---:|---|---|
| `demo_gkxlumenx_dwd.enterprise_stat_summary` | 141 | 12产业的G1规模趋势/最新值、G2人数桶、G3人数和、G4九区指数 | 指标行名带 `【调试构造】` |
| `demo_gkxlumenx_dwd.enterprise_industry_summary` | 72 | 12产业×2021–2025企业数量趋势 | 产业名带 `【调试构造】` |
| `demo_gkxlumenx_dwd.enterprise_region_summary` | 9 | 九区企业地图/区卡值 | 使用页面精确区名 |
| `demo_gkxlumenx_dwd.policy_base_info` | 540 | 12产业×9区×5年政策样例 | `source_plane=debug`，ID前缀 `DEBUG-ONEMAP-` |
| `demo_gkxlumenx_ads.policy_industry_rel` | 540 | 政策样例与产业关联 | `chain:INB...` |

共1302行。覆盖前目标行已备份在执行机 `/private/tmp/one-map-debug-backup-20261107.json`，备份SHA256=`e54886bdffb8deaa743365af558457f73b15bb041df6402c7798a0e2529bdee0`。完整计划和备份仅留本机；仓库只发布聚合摘要 `debug-batch-summary.json`，不提交明细快照。

12产业的API-1/2、九区API-4的发展与企业卡，以及API-6 development/enterprise地图均有值。政策样例在API-3总量/区分布可见，但API-3趋势 value、API-4 policy_count、API-6 policy map仍为空；API-5调试关键词无ES命中。该数据任务未修改应用代码，因此这些区块尚未完成页面全项联调。

## 验证与部署

- `python3 -m pytest -q tests/test_one_map_gap_fill.py`：5项通过，覆盖空源/摘要变化拒绝、保留已有维度、桶数勾稽、幂等复跑及后续改动时拒绝回滚。
- 线上 `POST http://10.50.69.111:30895/topic/v1/portal/one-map/enterprise-stats`：INB1309/INB1354/INB2503均HTTP200、code0，employee_count与四桶逐值一致；INB2505仍为null四桶，未伪补0。随后全目录12个INB逐一复核：3个有源产业读回灌入值、9个无源产业保持空态，12/12通过。
- 相同计划再次apply：`changed=false, rows=15`，无新增/改写。
- `lumen-topic-py`提交：`08265876452365da12e9506431de96de838be61f`，已推 `origin/dev`。
- [Pipeline 4180](https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/lumen-topic-py/-/pipelines/4180)：success，py:smoke、镜像及deploy:search-py等已有流水线job成功。此次未手动触发额外部署。数据灌入与现有已部署接口对账完成，不依赖修改接口代码。
- 手工核验未保留traceId，因此不虚构链路证据；API结果已存JSON。

## 其余数据项与四单纠偏

- DATA-EMP：保留，已实际执行有源部分；旧DATA-OPEN整组定义冻结不再是本次用户授权灌数的业务前置。部分覆盖仍需验收，未将整单标done。
- DATA-SCALE：保留为原清单G1数据灌入。已查当前ADS候选值，其批次为 `mock_20261103_reload` 且region=ALL，不是可直接作为深圳真实规模的来源，因此本次不冒充真实G1灌入；不依赖重新定义所有功能。
- INDEX-DEF：本轮误扩成重新定义/模型会签的工作，撤回本轮派发并保留记录；原清单G4若已有九区结果可直接灌，当前只找到城市级mock结果，不能把城市值填区。
- API-GAP：本轮误扩为接口改造，撤回本轮派发并保留记录；现有读链已能读回15行，不需要先改接口才能灌数。
- G5/G6无需新灌，本次接口读到既有四桶和占比；未为这两项改表或重做口径。

## 架构与交接

无DDL ✅；Python脚本写原表 ✅；Java/前端不写库 ✅；无mock或估数冒充来源 ✅；保留未知空态 ✅；备份和回滚可用 ✅；没有改他人工作区文件 ✅。

本次使用独立代码工作树避免与SYSINT-DICT-02-L01全仓声明及主工作区未提交repo.py冲突。实际代码仅脚本和专用测试；工作树 `/private/tmp/one-map-py`，分支 `codex/one-map-employee-fill`。

实际模型token/费用未有可靠计量，未伪造cost数字；交接只陈述实际执行证据，不自行签收done。

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

## 用户授权调试构造批次

用户明确授权为已开发的调试页面构造数据；本批仅写 `demo` 环境既有表，不要求真实业务来源、不更改表结构。

| 表 | 行数 | 内容 | 标识 |
|---|---:|---|---|
| `demo_gkxlumenx_dwd.enterprise_stat_summary` | 141 | 12产业的G1规模趋势/最新值、G2人数桶、G3人数和、G4九区指数 | 指标行名带 `【调试构造】` |
| `demo_gkxlumenx_dwd.enterprise_industry_summary` | 72 | 12产业×2021–2025企业数量趋势 | 使用标准产业名；`stat_date=2026-11-07` |
| `demo_gkxlumenx_dwd.enterprise_region_summary` | 9 | 九区企业地图/区卡值 | 使用页面精确区名 |
| `demo_gkxlumenx_dwd.policy_base_info` | 540 | 12产业×9区×5年政策样例 | `source_plane=debug`，ID前缀 `DEBUG-ONEMAP-` |
| `demo_gkxlumenx_ads.policy_industry_rel` | 540 | 政策样例与产业关联 | `chain:INB...` |

共1302行。覆盖前目标行已备份在执行机 `/private/tmp/one-map-debug-backup-20261107.json`，备份SHA256=`e54886bdffb8deaa743365af558457f73b15bb041df6402c7798a0e2529bdee0`。完整计划和备份仅留本机；仓库只发布聚合摘要 `debug-batch-summary.json`，不提交明细快照。自动审查拒绝的是完整行计划/备份文件的Git发布，不影响已经提交的demo数据库事务。

## 调试构造数据批次

用户明确授权为已开发的调试页面构造数据；本批仅写 `demo` 环境既有表，不要求真实业务来源、不更改表结构。

| 表 | 行数 | 内容 | 标识 |
|---|---:|---|---|
| `demo_gkxlumenx_dwd.enterprise_stat_summary` | 141 | 12产业的G1规模趋势/最新值、G2人数桶、G3人数和、G4九区指数 | 指标行名带 `【调试构造】` |
| `demo_gkxlumenx_dwd.enterprise_industry_summary` | 72 | 12产业×2021–2025企业数量趋势 | 使用标准产业名；`stat_date=2026-11-07` |
| `demo_gkxlumenx_dwd.enterprise_region_summary` | 9 | 九区企业地图/区卡值 | 使用页面精确区名 |
| `demo_gkxlumenx_dwd.policy_base_info` | 540 | 12产业×9区×5年政策样例 | `source_plane=debug`，ID前缀 `DEBUG-ONEMAP-` |
| `demo_gkxlumenx_ads.policy_industry_rel` | 540 | 政策样例与产业关联 | `chain:INB...` |

共1302行。覆盖前目标行已备份在执行机 `/private/tmp/one-map-debug-backup-20261107.json`，备份SHA256=`e54886bdffb8deaa743365af558457f73b15bb041df6402c7798a0e2529bdee0`。完整计划和备份仅留本机；仓库只发布聚合摘要 `debug-batch-summary.json`，不提交明细快照。

详细备份包含被替换的原人数样本及调试目标行，只保存在执行机；完整行计划同样未提交仓库。自动审查拦截的是将大体量调试快照推入Git，不是数据库灌数事务。数据库中的调试数据已提交且验证通过。

首轮写入时，12产业的API-1/2、九区API-4的发展与企业卡以及API-6 development/enterprise 地图已有值；当时政策趋势、区政策数和政策地图仍为空，API-5 搜索无命中。后续已定位并修复应用适配缺陷，最终六类接口全部回归通过，证据见文末“最终回归”。

## 验证与部署

- `python3 -m pytest -q tests/test_one_map_gap_fill.py`：5项通过，覆盖空源/摘要变化拒绝、保留已有维度、桶数勾稽、幂等复跑及后续改动时拒绝回滚。
- 线上 `POST http://10.50.69.111:30895/topic/v1/portal/one-map/enterprise-stats`：INB1309/INB1354/INB2503均HTTP200、code0，employee_count与四桶逐值一致；INB2505仍为null四桶，未伪补0。随后全目录12个INB逐一复核：3个有源产业读回灌入值、9个无源产业保持空态，12/12通过。
- 相同计划再次apply：`changed=false, rows=15`，无新增/改写。
- `lumen-topic-py`提交：`08265876452365da12e9506431de96de838be61f`，已推 `origin/dev`。
- [Pipeline 4180](https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/lumen-topic-py/-/pipelines/4180)：success，py:smoke、镜像及deploy:search-py等已有流水线job成功。此次未手动触发额外部署。数据灌入与现有已部署接口对账完成，不依赖修改接口代码。
- 手工核验未保留traceId，因此不虚构链路证据；API结果已存JSON。
- 首轮政策应用残余已由后续适配修复解决：API-3 改读 `publish_count`，API-4/6 改读 `kind=all` 的 `data.sz`，API-5 补兼容路由。最终结果见“最终回归”。

## 其余数据项与四单纠偏

- DATA-EMP：用户授权后补入构造批次；integration状态只表示数据/接口结果进入集成检查，不等于整个调试页六个接口全部绿，更不自行标done。
- DATA-SCALE：G1数据已经随调试构造批次写入并由API-1验证；原独立真实来源工单属重复拆单，保留记录、不再派发。
- INDEX-DEF：G4九区构造指数已随调试批次写入并由区卡/发展地图验证；原重新定义工单属范围扩大，保留记录、不再派发。
- API-GAP：经线上复测确认存在三个真实适配缺陷，不再是误扩范围；已完成政策字段映射和 API-5 搜索路由修复，代码与部署证据见同名 API-GAP handoff。
- G5/G6无需新灌，本次接口读到既有四桶和占比；未为这两项改表或重做口径。

## 架构与交接

无DDL ✅；Python脚本写原表 ✅；Java/前端不写库 ✅；无mock或估数冒充来源 ✅；保留未知空态 ✅；备份和回滚可用 ✅；没有改他人工作区文件 ✅。

本次使用独立代码工作树避免与SYSINT-DICT-02-L01全仓声明及主工作区未提交repo.py冲突。G2/G3脚本修复已单独推送；调试样例通过一次性数据库事务写入既有表，无应用代码改动。调试摘要 `debug-batch-summary.json` 仅含批次/计数/接口残余，不含行级数据。

实际模型token/费用未有可靠计量，未伪造cost数字；交接只陈述实际执行证据，不自行签收done。

## API适配修复交接

`lumen-svc-platform` `7a37b73` 已推送 `dev`：API-3政策趋势改用Python返回的 `publish_count`；API-4与API-6政策读取改用 `kind=all` 响应中的 `data.sz` 后按区筛选。对应 `OneMapFacadeServiceTest` 已用临时 Maven 3.9.9 实际执行，10 项通过、0 失败。该修复不建表、不改表、不写库。


## 最终回归（2026-11-07）

- 修复提交：Java `7a37b73`；Python 兼容路由 `67c7bd0`、过滤操作符修正 `6ae85c8`。
- Java Pipeline `4219` 的 `deploy:topic` Job `29687` 成功；早期 `deploy:topic-svc` 不是 `/topic/**` 的正确服务，已纠正。
- Python Pipeline `4223` 成功；Harbor 首次推送超时后重试 Job `29769` 成功，`deploy:search-py` Job `29747` 成功。
- 数据库最终核对仍为 1302 行：统计 141、产业趋势 72、区县 9、政策 540、产业关联 540；没有 DDL。
- 政策关联统一为 `chain:INB*`；产业名和区名使用页面标准值，避免精确匹配与地图显示失效。
- 线上全量回归：12/12 产业 API-1/2/3 有值；9/9 行政区 API-4 有值；API-6 三类地图分别 9/9、9/9、10/10 非空；API-5“腾讯 + INB1309”返回 7 条。
- 回归摘要保存在执行机 `/private/tmp/one-map-final-regression.json`，未提交行级明细。

### 调试页与 QA

- 前端提交 `03661ffe82470ea06c18de6e73572b049292b8a2`，Pipeline `4227` 全绿；`/one-map-debug` 已免 SSO 打开。
- 页面内 API-1～API-6 逐项执行均 HTTP 200、`code=0`。
- 新入口 `/open/topic` 已由 Nacos 重灌恢复，HTTP 200、`code=0`。
- 最终 Helm 验证 Pipeline `4233`：`backend:build` `29832`、`helm:lint` `29833`、`helm:chart` `29844` 全成功。
- QA 结果与截图见 `SYSINT-04-01-DATA-EMP-L01-evidence/qa-regression.json`、`one-map-ui-qa.jpg`。


## 偏离

- 本批按用户授权使用调试构造数据，未追求真实业务来源，属于原始真实灌数口径的明确偏离；不参与正式指标就绪度签收。

## 产物清单

- 1302行既有表调试数据、数量/接口证据、UI QA截图及本 handoff。

## 架构合规自检

- ✅ 无 DDL：所有调试数据写入既有表，未新增/修改字段或索引。
- ✅ 范围隔离：只覆盖 demo 环境明确调试批次，不写生产库。
- ✅ 可逆：写入前备份、事务提交、行数和唯一键验收，失败可回滚。
- ✅ 数据绑定：政策产业关联使用既有 `chain:INB*` 契约。
- ✅ 显示一致：产业名和九区名使用页面标准名称。
- ✅ 接口只读：Java/Python 查询不触发写库。
- ✅ 可追溯：批次、统计日期、接口结果和截图均有证据。

## Cost 回填

| 字段 | 值 |
|---|---|
| actual_tokens | `not_measured` |
| model_used | `codex` |
| actual_cost | `not_measured` |
| cost_warn | `green` |

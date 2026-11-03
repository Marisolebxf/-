# DR-RES-MOCK-LOAD-L01 · 科技数据资源 mock 灌数

| 字段 | 值 |
|---|---|
| claimed_by | `human:淮政玮` |
| supervised_by | `human:淮政玮` |
| claim_type | 已认领，开工时已是 `in_progress` |
| 状态 | 仍是 `in_progress`。本叶不改登记表，不标 `done` |

ponytail: full

## 库与结果

| 项 | 值 |
|---|---|
| 目标库 | `demo_gkxlumenx_ads` |
| 实例 | `10.50.11.76:3306`（MySQL `@@hostname` = `node03`）。账号取自 `lumen-svc-platform` 的 `gkxlumen-element` `application-local.yml`，用户名 `gkxlumenx`。密码未写入脚本、未写入本文 |
| 执行机器 | 本机 `DESKTOP-4QHU2S8` 直连。没有走 SSH |
| 批次 | mock 行 `mock_dr_res_load_l01`；久新快照 `snap_dr_res_load_l01`。两批都以规定前缀开头 |
| fill_method | `manual` |
| 可重复 | 同一脚本连续执行两次。第二次先按这两个 `calc_batch_id` 删除再插入，只读 `COUNT(*)` 与第一次相同 |
| 是否已灌入 | **是**。mock 行在库里。snap 两张表也已写入 |

未写入正式库 `gkxlumenx_ads`、ODS、DWD、久新、库 `gkxlumenx_gapfill`。久新只做了 `SELECT` 和 `SHOW FULL COLUMNS`。

## 只读行数

`SELECT DATABASE()` = `demo_gkxlumenx_ads`。逐表 `SELECT COUNT(*)`：

| 表 | 行数 | 批次 |
|---|---:|---|
| `gapfill_dr_type_slice` | 11 | mock。structure 4 + theme 7 |
| `gapfill_dr_source_channel` | 60 | mock。来源五类 × 6 个月 + 机构活跃度五类 × 6 个月 |
| `gapfill_dr_catalog_item` | 30 | mock。overview_source 10 + access_source 12 + access_detail 8 |
| `gapfill_dr_ingest_task` | 20 | mock。done 12、running 4、pending 4 |
| `gapfill_dr_collection_fact` | 116 | mock。年度 2025 与 2026，另有月 / 周 / 日、渠道归集、历史明细 |
| `gapfill_dr_theme_library` | 8 | mock。每个主题库都有字段行 |
| `gapfill_dr_theme_column` | 25 | mock |
| `gapfill_dr_quality_issue` | 30 | mock |
| `gapfill_dr_usage_subject` | 15 | mock。六类主体都有行 |
| `gapfill_dr_usage_series` | 120 | mock。调用、使用详情、主题、供应方、需求方、业务、累计，按月有点 |
| `gapfill_dr_call_event` | 40 | mock。app_log 10、supplier_detail 10、column_usage 12、user_track 8 |
| `gapfill_dr_api_probe` | 8 | mock |
| `gapfill_dr_graph_node` | 25 | mock。overview_kg 10、theme_relation 15 |
| `gapfill_dr_resource_link` | 27 | mock。overview_kg 11、theme_relation 16 |
| `gapfill_dr_block_json` | 4 | mock。四个 `block_code` 各 1 行 |
| `gapfill_dr_entity_year` | 175 | snap |
| `gapfill_dr_column_catalog` | 131 | snap |

`block_code`：`overview_classify`、`semantic_theme`、`partition`、`big_data_center` 各 1。

## 四个对齐

脚本在提交前断言，库内只读复核也成立。

| 对齐 | 取值 |
|---|---|
| structure 切片 `value` 之和 = 年度接入最后一年的 total | **30398 = 30398** |
| 主题库行数 = 主题库数量 | **8** |
| 问题行数 = 问题资源数 | **30** |
| `status=pending` 的任务数 = 待处理任务 | **4** |

年度 total 的取法：`gapfill_dr_collection_fact` 里 `grain=year`、`metric=volume`，且 `channel_name`、`table_name`、`biz_type` 都为空，按 `period_label` 取最后一年的 `row_count`。库里是 2025 年 26720、2026 年 30398。30398 来自四条 structure 切片相加，写在类型切片和 2026 年 `volume` 上。

`gapfill_dr_entity_year` 没有 `mock_` 行。目录总量 30398 没有写入实体存量。

## snap

已写入。

| 项 | 值 |
|---|---|
| 实例 | 久新 Doris `47.93.119.170:29030`，库 `gkx_technology_analysis_dev`，账号 `test2` |
| 口令 | 本机环境变量 `JX_ADS_PASSWORD` 未设置。脚本读到本机已有配置后连接。口令未写入脚本、未写入本文 |
| 语句 | 只读。`SHOW FULL COLUMNS` 三张表；四个年份列 `GROUP BY` 后 `COUNT(*)`。年份列名用 A0：`ads_paper_profile.publication_year`、`ads_patent_profile.application_year`、`ads_patent_profile.publication_year`、`ads_project_profile.start_year`。列名先与 `SHOW FULL COLUMNS` 核对，缺列则整批 snap 失败 |
| 实体年 | `paper.publication_year` 12 年、合计 4000000；`patent.application_year` 51 年、合计 1768955；`patent.publication_year` 37 年、合计 1768955；`project.start_year` 75 年、合计 74144。空年份未写入（`stat_year` 不可空） |
| 列目录 | `ads_paper_profile` 38、`ads_patent_profile` 45、`ads_project_profile` 48，合计 131。序号按现网 `SHOW` 顺序，没有手填列名或条数 |

## 偏离

年度接入的 total 落在 `metric=volume` 的 `row_count` 上。表上没有名为 total 的列。

`big_data_center` 的 `overview` 仍是种子里的介绍数字。方案第 5 节要求 Java 用主题库行汇总覆盖这四个数。本叶没有改方案，也没有在 JSON 里改成主题库汇总数。

没有改方案第 5 节，没有改契约，没有改 `DR-RES-MOCK-DDL-L01.sql`，没有改 `DR-RES-A0-L01.md`。没有在接口代码里写死 mock。

## 架构合规

| 铁律 | 结果 |
|---|---|
| 只写验收库 `demo_gkxlumenx_ads`，表名 `gapfill_dr_` | 已灌入上表 |
| 不写正式 `gkxlumenx_ads`、ODS、DWD、久新、`gkxlumenx_gapfill` | 未写。久新只读 |
| D18 | mock 行在表里。接口未返回写死 mock |
| 实体存量不进资源总量 | `entity_year` 只有 `snap_` 查询结果 |
| 算法 / 调用链 / 可观测 | 本叶无接口代码 |

## CI/CD

- 分支：`dev`（工作区）
- commit：无。未 commit，未 push
- pipeline / K8s：无

## 产物

- `agent-delivery/agent-handoffs/科技数据资源-DR/DR-RES-MOCK-LOAD-L01.py`
- `agent-delivery/agent-handoffs/科技数据资源-DR/DR-RES-MOCK-LOAD-L01.md`

再跑：在本机执行该 Python。MySQL 口令仍从 `application-local.yml` 读取。久新口令仍从环境变量 `JX_ADS_PASSWORD`、`JX_ADS_PASSWORD_FILE`、用户目录 `.gkx/jx_ads_password`，或本机已有的久新只读配置读取。连不上久新时，脚本删掉自己的 `snap_` 行，两张快照表保持空，mock 行仍提交。

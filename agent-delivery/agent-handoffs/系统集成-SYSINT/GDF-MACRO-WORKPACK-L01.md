# GDF-MACRO-WORKPACK-L01 · 宏观行业 GDF 派单包 v1（WBS-06-05B）

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:data-agent`（协作 `agent:architect-agent`） |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 2026-11-09 总控派单，已 claimed → in_progress。优先级为市场研究红标第 1（P0） |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full`（派单指定；本叶是定义·文档类，仅一份只读自检 SQL 涉及可执行语句） |
| 说明 | 只留一份可重跑的只读自检 `sql/check_area_resolve.sql`，断言写在 `04` §3.5。没有用 YAGNI 跳过 00 声明、02、09、10、11、12。未新增脚本框架、未加依赖 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip`（查询输出均小，未触发压缩） |

## 图即契约（架构 / 存储流图 / ARCH-IMPL / 联调 / IA 首页必填）

| 字段 | 值 |
|------|-----|
| diagram_id | 无（本叶未新增或改动存储流图） |
| 图 diff | 无。包内 `00` §3、`12` §0 有文字 / mermaid 流程；`storage/` 下**没有** MACRO 目录，本叶**未新建**，入仓是 OPEN-MACRO-05，留给架构师 |
| 会签态 | 不适用 |

## 问题清单

- **区划键不是直接 join**：四个政策城市在 `dwd_dim_admin_area` 里没有自己的 `cur_code` 行，事实表 `area_code` 长度 2 / 3 / 4 / 12 混存。反解规则落 `04` §3.2 与 `09` §3.1.1。
- **`area_code_type` 有未定义值**：实测 1 = 19,819、3 = 49、4 = 132（Excel 只定义 1 / 2 / 3）。v1 只取 1 进 ADS（OPEN-MACRO-01）。
- **区县行 / 国家行不是城市**：type=1 下 `district_by_area_code` 3,058 行、`unresolved` 5,332 行（含国家级 `0086`）。不向上聚合、不进 ADS（OPEN-MACRO-03 / 04）。
- **20,000 行是样本上限**（事实表、区划表都恰为 20,000）。验收不写固定值（OPEN-MACRO-02）。
- **Excel 与 live 结构差**：Excel 多出 `t_id`；live 业务键无物理唯一索引，物理主键是 `dwd_id`。Wave B 在 DWD 另设业务 UK 并计冲突数。
- **单位坑**：属性表 `unit_use` 恒为「元」；TB 行真实单位取事实表（`%`）。已写进 04 §5、09 §3.3、DDL COMMENT。
- **DDL 无 storage 真源、现网未核**：本叶无产线库权限，`gkxlumenx_ods` / `_dwd` / `_ads` 现网是否已有这些表没查（OPEN-MACRO-05 / 06）。`10` 与 `12` §2 的 DDL 未执行。
- **registry 签收闸门预期**：`GDF-*-WORKPACK-*` 改 `done` 时服务端会跑 `gkx-gdf-ddl-signoff`，要求线上 demo 库与 lumen 库已建表且与 storage 一致。本包 DDL 只是草稿，**预期 `GATE_DENIED`**，直到架构师把草稿入 storage 并建表。这不是本叶该绕过的。
- **②b 只是附录**：落地实效改读 ADS 要三条前置（`12` §5.3）：②a 灌数验收、算法侧另开叶、QPOL-02 会签。本叶不动算法，不动正本三维。
- **指标 8 件套未登记**：`12` §4 给 `macro_city_section` 的血缘卡是占位，本叶未查、未写 metric-registry。

## 修改内容

新建 `agent-delivery/data/GDF/派单包/宏观行业/GDF-MACRO-WORKPACK-v1/`：

| 文件 | 说明 |
|---|---|
| `README.md` / `CHANGELOG.md` | 索引、版本；顶部写优先级 |
| `00-派单说明书.md` | **§0 优先级声明**（市场研究红标第 1 / P0）、作废清单、分层、OPEN-MACRO-01~07 |
| `01-命名与分层词典.md` | 六表名对照（ODS `dwd_*` → DWD `macro_*`）、易混名、UK |
| `02-WaveA-贴源表清单.yaml` | 六张 P0 wash |
| `03-连接与网络.md` | 与政策 / 产业链包同一套地址，密码线下 |
| `04-技术字段与过滤规则.md` | 取数无行过滤；**区划反解 §3**；`area_code_type`；基线与断言；单位 |
| `05-WaveA-验收检查表.md` | 小维度表精确相等；抽检 SQL |
| `06-WaveB-Mapping派工.md` | B1 五维度、B2 事实表 |
| `09-宏观行业域-ETL-Mapping明细-源表到DWD.md` | 逐表逐字段；§3.1.1 反解 SQL |
| `10-DWD-MySQL-DDL/README.md` + `macro-dwd.md` | 六张 DWD 建表草稿 |
| `11-作废与误源对照.md` | 误源 |
| `12-DWD后加工-城市截面ADS与实效代理附录.md` | ②a ADS 建表草稿 + 灌数 SQL + 血缘占位；②b 附录 |
| `sql/check_area_resolve.sql` | 只读自检 |

同步：`派单包/README.md` 加 MACRO 行；`WBS.md` 06-05B 行改为首版已落盘。

## 测试结果

2026-11-09 12:35 前后，用本机已有只读凭据连三方 `gkx`（**只 SELECT，未写任何库**）：

- 六表行数：20,000 / 867 / 20,000 / 3 / 7 / 4，与 `GKX数据源表及行数报告-20261109-1026.MD` 一致。
- `sql/check_area_resolve.sql` 实跑：区划反解分布与 `04` §3.5 基线一致（type=1：`city_by_city_code` 10,599、`district_by_area_code` 3,058、`municipality_by_province_code` 830、`unresolved` 5,332；type=3 城市 49；type=4 城市 93 + 直辖市 39）；事实表业务键（含 `area_code_type`）无重复；`index_code` / `dim_cal` / `dim_dur` / `source_code` 无孤儿。
- `09` §3.1.1 反解 SQL 在 live 表上试跑，分布与上相同，语法通过。
- `12` §3 灌数 SELECT 在 live 表上试算：2,201 序列、103 个城市、128 个指标；`(fact_area_code, area_code_type, index_code, dim_cal, dim_dur)` 无冲突；维度名称无缺失。四城对 9 个白名单指标 `TB·DNLJ` 的覆盖城市集合与 `pipeline-macro-effect-proxy.md` §1 一致。
- 以上是**从供应方源表模拟**，不是 GDF 回传。`10` 与 `12` §2 的 DDL 未执行。**不宣称已建表、已灌数或已跑通。**

## 遗留风险

- 现网结构未核（OPEN-MACRO-06）；DDL 草稿未签收（OPEN-MACRO-05）。
- 区县聚合口径、type=3/4 含义、补数后白名单重冻（OPEN-MACRO-01~04）。
- ②b 会签（OPEN-MACRO-07）。
- 通用 `parse_workpack.py` 对本包字段矩阵的识别未验证，预填前须补规则或按 09 人工配置。
- `done` 前置闸门（见问题清单）。

## CI/CD（必填）

- 分支：`dev`（编排仓直推 `origin/dev`）
- commit：见下方回填
- pipeline URL / ID：无（编排仓无业务 CI）
- 部署 namespace / 镜像 tag：无
- K8s rollout：不适用（设计类 `cicd: skip`）
- dev 测试 URL / 命令与结果：不适用

## 可观测性（建议）

- OTEL_SERVICE_NAME：不适用
- traceId（dev 抽样）：不适用
- Tempo / Loki：无

## 涉及文件

- `agent-delivery/data/GDF/派单包/宏观行业/GDF-MACRO-WORKPACK-v1/**`
- `agent-delivery/data/GDF/派单包/README.md`
- `agent-delivery/工程过程/04-系统集成/06-GDF数据治理集成/WBS.md`
- 本 handoff

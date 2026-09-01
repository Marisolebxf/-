# DATA-POLICY-STORAGE-ETL-FILL-L01 · 政策 etl 层补齐

## 任务认领

| 字段 | 值 |
|---|---|
| task_id | `DATA-POLICY-STORAGE-ETL-FILL-L01` |
| claimed_by | `agent:data-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| repo / branch | `gkx-orchestration` / `origin/dev` |
| depends_on | `DATA-POLICY-STORAGE-EDGE-SEMANTIC-L01`（≥ ready_to_sign） |

## Ponytail

- ponytail: `full`
- 两份不存在的管线（ES / Mock→ADS）**没有照 CHAIN 模板编设计**，而是写成 `not-built` 占位说明——凑齐文件数不是目标，诚实标注才是。
- `pipeline-ods-to-dwd.md` 不复制 `ods-to-dwd-mapping.md` 已有的列矩阵，只写路径与调度，一句指针互链。
- 未新建 `etl/scripts/`、未造 DDL 快照目录（CHAIN 有，POLICY 本波无对应产物）。

## 图即契约

| 字段 | 值 |
|---|---|
| diagram_id | `POLICY-STORAGE-FLOW` |
| 图 diff | **无**。补 ETL 侧文字，拓扑未动，不翻签。 |
| 会签态 | `approved`（`human:淮政玮` · 2026-08-21）维持 |

## 前置核查（决定每份怎么写）

补文档前先核实每条管线真实状态，不按文件名想当然：

| 管线 | 核查结论 | 依据 |
|---|---|---|
| ODS→DWD | **as-built** | `polan/mockgen/generate.py` 写 ODS `dwd_policy_base` 再映射 DWD；`incr.py` 读 ODS−DWD 差集 |
| DWD→ADS | **as-built** | `run_all_policy.py` `build_steps()` 第 4–15 步；12 个模块各写 ADS |
| DWD→ES | **not-built** | `rg -i elasticsearch polan` 零命中；`stores/elasticsearch.md` 亦声明不施工 |
| Mock→ADS | **not-built** | Mock 只写 ODS/DWD，ADS 一律从 DWD 重算；`metrics.py` 的 mock 是查询期降级、不回写 |

## 修改内容

新增 5 份：

- `etl/README.md` — 管道索引表，引入 `as-built` / `draft` / `not-built` 三态标注；主链一句话图；全域铁律。
- `etl/pipeline-ods-to-dwd.md`（as-built）— ODS/DWD 库表对应、`replace` 与 `append` 两模式语义差异、`run_all_policy` 调度、`assert_demo_mysql_targets` 库名门禁、`OPEN-POLICY-FLOW-01`。
- `etl/pipeline-dwd-to-ads.md`（as-built）— 12 步模块→ADS 表写入图；**顺序约束**（C6 layout 必须在 C5/C4 之后，`policy_focus` / `policy_effect` 多模块共写）；幂等策略分模块；ADS 全量重算不做增量；查询期降级不回写。
- `etl/pipeline-dwd-to-es.md`（not-built）— 结论 + 不建理由 + 三条触发再评估条件。
- `etl/pipeline-mock-to-ads.md`（not-built）— 说明政策 Mock 是贴源 Mock（写 ODS/DWD）；辨析「贴源 Mock」与「查询期降级」两个 mock。

改 2 份：`storage/POLICY/README.md` 读序第 4 条改指 `etl/README.md`；`CHANGELOG.md` 追加。

**未改**业务仓代码、**未** APPLY DDL、**未**灌数、**未**改 `stores/`。

## 发现的缺口（不静默修）

`stores/mysql/ads.md` 只登记九张指标表 + 两张图镜像，但代码实际还写入 **四张未登记表**：`policy_entity`（NER 结果）、`policy_text_parse`（D1）、`policy_match`（D2）、`policy_simulate`（D3）。

处理：在 `pipeline-dwd-to-ads.md` 写入图中列出并加 ⚠️ 标注，补登走 `OPEN-POLICY-GRAPH-03` 同批升级 `human:淮政玮`。S3 已 `ready_to_sign`，细表登记变更不由文档叶自行拍板。

## 验收证据

逐条回源：

| 结论 | 来源 |
|---|---|
| 15 步编排与步名 | `scripts/run_all_policy.py` `build_steps()` L50–67 |
| replace/append 语义 | 同上 L51 `seed_label` + `mockgen/incr.py` 模块头 |
| 各模块→ADS 表映射 | 全仓 `rg "ads\}\.[a-z_]+" polan` 输出逐条归类 |
| C6 依赖 C5/C4 | `polan/eval/layout.py` L7 显式声明 |
| 各模型幂等策略 | `polan/eval/__init__.py` 模块头「写前删除自己拥有的 rowset」；`entity.py` L48 `conn.truncate` |
| 库名门禁 | `run_all_policy.py` L81 `assert_demo_mysql_targets()` |
| 零 ES | `rg -i elasticsearch polan scripts/run_all_policy.py` exit=1 |
| 查询期降级不回写 | `polan/metrics/metrics.py` 模块头 |

无 CI（定义叶）。相对链接已按目录层级核对。

## 遗留风险

- `OPEN-POLICY-GRAPH-03` 现累积两项待裁决：四类边 DDL 列、ADS 四张未登记表。
- `pipeline-to-minio.md` 仍是 draft 指针（前缀 `policy/{task_id}/`），对应导出能力 `OPEN-POLICY-DISP-09` 未落地。
- `pipeline-demo-mock.md` 与新增 `pipeline-ods-to-dwd.md` 存在少量叙述重叠（前者是全景分解，后者是路径与调度），已用互链区隔；若后续 SEED 单改写 Mock 策略需同步两份。

## CI/CD

- 分支：`gkx-orchestration` `origin/dev`
- commit：待提交（`[agent:data-agent]`）
- pipeline / K8s：N/A（编排仓文档叶）

## 涉及文件

- `agent-delivery/data/data-design/storage/POLICY/etl/README.md`（新增）
- `agent-delivery/data/data-design/storage/POLICY/etl/pipeline-ods-to-dwd.md`（新增）
- `agent-delivery/data/data-design/storage/POLICY/etl/pipeline-dwd-to-ads.md`（新增）
- `agent-delivery/data/data-design/storage/POLICY/etl/pipeline-dwd-to-es.md`（新增）
- `agent-delivery/data/data-design/storage/POLICY/etl/pipeline-mock-to-ads.md`（新增）
- `agent-delivery/data/data-design/storage/POLICY/README.md`
- `agent-delivery/data/data-design/storage/POLICY/CHANGELOG.md`

## 架构合规自检

| 铁律 | 结果 |
|---|---|
| 算法只在 Python | ✅ 零代码改动；文档记录算法链仍全在 `polan` |
| 调用链 / D12 | ✅ 文档重申 Java 只读 ADS、不直连 nGQL；未涉 lumen |
| 图谱 Nebula 一张 G | ✅ 仅 `demo_gkx_chain`；禁 Neo4j |
| 无闸门不写正式库 | ✅ 三份文档均写明零写入 `gkxlumenx_*` / `gkx`，并记录 `assert_demo_mysql_targets` 门禁 |
| D9 血缘 | ✅ ODS→DWD→ADS→前端全链可追；缺表项指向 `OPEN-POLICY-DISP-*` |
| 诚实性 | ✅ 两条不存在的管线标 `not-built`，未编造设计 |

## cost

| 字段 | 值 |
|---|---|
| actual_tokens | 58000 |
| model_used | claude-opus-4.6 |
| actual_cost | 0.74 |
| cost_warn | green |

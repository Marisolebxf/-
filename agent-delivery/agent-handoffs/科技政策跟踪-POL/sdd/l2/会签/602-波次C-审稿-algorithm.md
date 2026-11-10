# 602 · 波次 C · algorithm-agent 审稿

- 身份：`agent:algorithm-agent`
- 日期：2026-11-10
- 被审：`POL-L2-PC1-CLEAN-ARCH.md`、`POL-L2-PC1-CLEAN-API.md`、`POL-L2-PC1-CLEAN-DATA.md`，以及 Storage 里准确性演示那一节、`CHANGELOG.md`、`01-data-flow.md` 那一句、`stores/README.md` 的 ADS 索引行
- 不审：`POL-L2-PC1-CLEAN-METRIC.md`（本身份本波已写）
- 口径：说明书「#### 602」、读法方案文末裁定清单、`.cursor/skills/gkx-fde-design-change/审稿硬清单.md` algorithm-agent 三节
- 本稿只记账。不改 ARCH、API、指标、数据、说明书、线框、Storage、代码

已知且不作为新缺陷：候选和执行不复用 `governance/results`；六条正式事实表不建；准确性表名 `policy_accuracy_demo` 是本波草稿名。

## 硬清单

1. 本叶有统计数字。页眉「库内政策数」在指标任务和 `指标与501.md` 治理节仍是 `M_POLICY_TOTAL_COUNT`（STAT，注册表 D4=`mock`，2026-11-10 `metric-get`）。勾选条数和五条命中条数没有 `metric_id`。准确性演示数没有 `metric_id`。三份稿没有把页眉的 `metric_id` 写出来，数据稿又给演示数写了 D4。见 ALG-1、ALG-2。
2. 三份稿都没有新造 `metric_id` 字符串。ARCH 第 15、156 行写了不新造、不改 D4。没有把注册表 D4 改成 live。数据稿把「D4 仍是 mock」写到没有指标号的演示数上，见 ALG-2。页眉若把现查 COUNT 当成已接入，见 ALG-1。
3. 两条新读口的响应里没有 `M_POLICY_VALIDITY_RATE`，也没有把九张指标表写进 602 的判定。现行 `governance/results` 的清洗 KPI 仍挂着这条有效率，三份稿没有写切断，见 ALG-3。流图和索引见 ALG-4。

## 核过

- 五条命中和批次头条数：API 第 73–75 行只写命中条数、勾选条数，没有 `metric_id`；没点不出现、不造 0（API 第 67、75 行）。与指标任务「不新造清洗 `metric_id`」一致。
- 准确性不进六条现算：ARCH 第 5 节、API 第 77 行、DATA 第 5 节都把它单独成表，界面标明演示，不得写成已经按原文核过。表名草稿与 CHANGELOG、`ads.md`「准确性演示」节一致，且写明不计入 as-built 16 张。
- `ads.md` 展示窗口里的 `M_POLICY_*` 仍落在原来九张指标表，本波没有改列，也没有把 `policy_accuracy_demo` 写进那九张。

## 异议

[algorithm-agent] ALG-1 · 页眉库级计数没有写出 `metric_id`，现读的数也不是这条指标的源表 · ARCH 第 145–147 行、API 第 116 行、DATA 第 92 行只写「原资源、D4 不改、不重写读法」。指标任务和 `指标与501.md` 治理节（约第 176 行）写明页眉附卡是 `M_POLICY_TOTAL_COUNT`，D4=`mock`，`srs_refs` 在全景序号 215 与专题序号 100，不替代 602。`metric-get`：源表 `dwd_policy_base`，`d4_ingestion_status=mock`。element `PolicyGovernanceController` 第 59 行的 `totalPolicyCount` 是 `{dwd}.policy_base_info` 的 `COUNT(*)`。三处不是同一张表。硬清单第 1、2 条 · 三份稿补一句：页眉这个数的 `metric_id` 仍是 `M_POLICY_TOTAL_COUNT`，D4 保持 mock，不随这一次勾选改变。`results` 里的 COUNT 不得写成 D4 已接入，也不得拿来替代本批条数。

[algorithm-agent] ALG-2 · 准确性演示数没有指标号，数据稿却写了 D4，响应里的「数」也没有数值列 · DATA 第 73 行「标明演示。D4 仍是 mock」。第 75–83 行只有来源、贴源 id、演示命中说明、写入批次标记。ARCH 第 78、131 行和 API 第 77 行把读到的内容叫「演示数 / 数」放进同一次响应。裁定清单第 3 条只要求标明演示，不得写成已经按原文核过。指标任务写明这条演示数不是指标、不注册、不写公式。D4 只属于已注册指标。硬清单第 1、2 条 · DATA 删掉这句 D4。演示说明保持文字。若界面必须有一个看得出是演示的数，写明它不是注册指标、不占 D4、不写成质量分，并给出列名；读失败仍是「读取失败」，不用 0 顶上。

[algorithm-agent] ALG-3 · 清洗页上的有效率没有从本叶拿掉 · 指标任务和 `指标与501.md` 第 169 行写明 602 不挂 `M_POLICY_VALIDITY_RATE`（该指标挂点在检索序号 198）。ARCH 第 145–147 行、API 第 31、116 行只说 `results` 继续给 603 和页眉、本叶不改这条资源。element 同一响应第 41–42、60 行仍带 `qualityAgg`（`script_state` 按 job、status 计数）。展示 `lumen-ui-science-pc` `src/api/policy.ts` 第 114–122 行把 `qualityAgg` 的条数标成清洗 KPI，`metricId` 为 `M_POLICY_VALIDITY_RATE`。硬清单第 3 条 · ARCH 与 API 写明：清洗页从 `results` 只取页眉库内政策数。`qualityAgg` 不进入 602 的批次明细，也不再挂 `M_POLICY_VALIDITY_RATE`。本批命中条数只来自 `clean-execute`，不注册成指标。

[algorithm-agent] ALG-4 · 准确性草稿表在流图和索引上会和九张指标表混读 · `01-data-flow.md` 第 75 行写 602 点执行时 Java 只读 `policy_accuracy_demo`，下一张图（第 77–84 行）仍是「Java 只读 ADS → `policy_*`」，第 88 行的消费方是全景/评价/推演 KPI。`policy_*` 含 `ads.md` 里挂着 `M_POLICY_TOTAL_COUNT`、`M_POLICY_VALIDITY_RATE` 的九张指标表。`stores/README.md` 第 21 行 ADS 索引仍只写 16 张，没有指向「准确性演示」草稿节。CHANGELOG 与 `ads.md` 第 97–103 行已经写明这张表不计入 16 张。硬清单第 3 条 · 602 那一句与全景读图分开，并写「不读九张指标表」。索引行加一句：另有草稿表 `policy_accuracy_demo`，不计入 16，不是指标表。

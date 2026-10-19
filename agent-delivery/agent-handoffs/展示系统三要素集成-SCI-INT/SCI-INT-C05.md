# SCI-INT-C05 标准层结构清单（ADS / ES / 维表 / 回流快照）· handoff

- 角色：agent:data-agent · 监管：human:淮政玮 · claim_type=coordinator_dispatch
- ponytail: N/A（分析叶）
- 产物：`产物/SCI-INT-C05.yaml`（生成 `产物/_work/C05-build.py`，采集 `产物/_work/C05-collect.py`，自检 `产物/_work/C05-check.py`）
- 对端：北京久新（旧写「九新」，引用旧路径时保留原路径）；久新相关内容全部「待确认」

## 1. 范围与实现

范围：展示系统三要素（人才 / 技术 / 机构）集成需要的标准层结构，即 ADS 表、ES 索引（lumen-etl-es-py）、地理维表与领域维表、久新模型结果回流的落库位置和快照版本。本叶是 D03/D04 的前置。招标依据：bid-reference `srs/02-科技信息展示系统`（科技全域态势 / 技术图谱 / 成果 / 科技人才态势各节），各卡 `merged_from` 指回原卡的 srs 行。

实现：

1. **采集**：`C05-collect.py` 扫描 B01、C01–C04、A01–A05 的产物，找出所有 `structure_escalation: true` 的卡片和顶层块，共 **80 条原始提法**（卡片 72 条，顶层块 8 条：B01 根 / IP-08 / IP-11，C04 space_plan / write_back_conflicts 4 项）。
2. **归并**：`C05-build.py` 把每条原始提法映射到一张规范卡（主映射 `to` 加附带映射 `also`），得到 **49 张规范卡**，int_id 范围 `INT-C-{TAL|TECH|ORG|X}-400`～`499`。每张卡都有：规范名、物理位置（统一用 `gkxlumenx_*`）、字段草案、主键（对齐 scholar_id / technology_id / org_uid）、刷新频率、写入方、读取方、来源源卡 `source_cards`、消费方 `consumer_cards`、`merged_from` / `merged_also`。页面、指标、久新行、消费方都由脚本从源产物计算得到，没有手抄。
3. **顶层块**：`dedup_map`（80 条，差集为 0）、`geo_dim_plan`、`domain_dim_plan`、`jiuxin_result_backflow`（分 SQL / Python / API 三种形态）、`conflicts`（19 条）、`risks`（5 条）、`open_items`（11 条）。
4. **人才态势 DS-13～16 预判**：依据 DS-13/14 的 page yaml 与 SRS「科技人才态势」，补了 3 张低置信度卡（`confidence: low`）：TAL-405 地区×领域×年度聚合粒度、TAL-406 流动 OD 聚合、TAL-407 荣誉 / 出访 / 动态扩展档案。另外在 TAL-400/402/404、X-466、X-474/475 上挂了 DS-13/14 消费方。DS-15/16 只看了判定分布，没有逐叶核对，已列入 OI-C05-09。

规范卡分布：

| 类别 | 数量 | 卡 |
|---|---|---|
| ADS | 15 | TAL-402/404/405/406/407、TECH-424/425/427/431/432、ORG-443、X-460/464/466/472 |
| 快照 | 4 | TECH-428 图版本、TECH-429 图节点指标、TECH-430 图路径、X-480 模型结果统一快照 |
| ES | 2 | X-463 `sci_factor`（人才 / 机构 / 技术点检索）、X-465 `sci_achievement` |
| 维表 | 5 | TECH-421 `tech_domain`、X-474 `code_region` 扩展、X-475 `region_scope` 扩展、X-476 `code_country`（复用）、X-478 `industry_cluster`（复用） |
| 主数据 | 3 | TAL-400 talent_master、TECH-420 technology_master、ORG-440 research_org |
| 映射 / 桥表 | 7 | TAL-401、TECH-422/423、ORG-441/442、X-461、X-477 |
| 人工层 | 3 | TAL-403、TECH-426、X-462 |
| 配置 / 用户自有 / ODS / 缓存 / Nebula | 3+4+1+1+1 | TECH-433（复用 `lumen_analysis_task`）、X-468、X-482；TECH-434、X-469/470/471；X-467；X-481；X-490 |

结论：

- **地理维表**：不新建地理主维。复用 `gkxlumenx_dim.code_region / region_scope / code_country / city`，需要扩展的有：街道级（level=4）、港澳台码、大鹏新区码、园区成员；另新增一张地名 / 区划归一映射表 `map_region_alias`。境外省 / 州（admin1）是否引入待定。行政区划精度属于业务口径，需登记客户决策。
- **领域维表**：技术领域只有一个真源 `gkxlumenx_dim.tech_domain`（domain_code），人才、机构、技术点共用；外部分类通过锚点桥表 `map_tech_domain_anchor` 挂接；产业维沿用 `industry_cluster`，不与技术领域混用。
- **久新回流**：
  - SQL 由我方 GDF/ETL 执行，结果写入各基础指标 ADS，版本 = batch_id + as_of + sql_version；
  - Python 并入 lumen-algo-py，结果写入 `sci_result_snapshot` 和图快照，版本 = run_id + model_version + snapshot_version；
  - API 经 Python 适配层，先进 Redis 缓存；只有甲方同意落库（DN-09）后才写快照。
  - 三种形态的版本都登记到 `sci_snapshot_version`，Java 只读 published 版本。保留策略为建议值，待确认。

## 2. 偏离

- 指令写「每张 ADS/ES/维表一张卡」。Nebula 图结构已由 C04 建了 9 张卡，C05 没有为它们逐张重建，而是收成 1 张 `INT-C-X-490`（「Nebula 增量 schema」）。C04 卡和 C01/C02 里的 Nebula 提法都主映射到这张卡，同时用 `also` 关联到对应的 ADS 真源卡，ADS 卡是唯一真源。
- C05 新增了 7 张卡，原始提法里没有对应来源（`merged_from` 为空）：TAL-406、TAL-407、TECH-422、X-474～X-478。来源分别是地理 / 领域规划和人才态势预判，卡内 gaps 已注明。
- 卡片的 `algorithm_type` 填「n/a（结构卡）」：结构卡没有单一算法类型，具体指标的算法类型看原卡或 MCP。
- A06 / A07 / A08 / A10 的产物在本叶执行期间已经出现，但按派单范围没有纳入归并。check 输出了它们的提法数（A06 9、A07 7、A08 9、A10 7），记在 OI-C05-01，待 Z01 补归并。

## 3. 产物清单

| 文件 | 说明 |
|---|---|
| `产物/SCI-INT-C05.yaml` | 49 卡 + dedup_map / geo_dim_plan / domain_dim_plan / jiuxin_result_backflow / conflicts / risks / open_items |
| `产物/_work/C05-collect.py` | 原始提法采集（`--dump` 可导出明细） |
| `产物/_work/C05-build.py` | 归并映射与生成 |
| `产物/_work/C05-check.py` | 自检 |
| `SCI-INT-C05.md` | 本 handoff |

未改业务仓、seed / 矩阵、其他叶产物；未连库；未 git commit / push。

## 4. 验收证据

- 原始提法 80 条，归并为规范卡 49 张：ADS 15 / 快照 4 / ES 2 / 维表 5，另有主数据 3、映射 / 桥表 7、人工层 3、配置 3、用户自有 4、ODS 1、缓存 1、Nebula 1。
- dedup 差集为 0：漏映射 0、多映射 0，`merged_from` 与 `dedup_map` 互为反向，一致。
- `structure_escalation` = 47 张卡，全部指向 `human:李伟`；X-476 和 X-478 是存量复用、不改结构，所以不升级。geo / domain / backflow 三个顶层块同样标了升级。
- 冲突 19 条，其中命名 / ID 类 7 条（CF-01 VID、05 tech_domain、06 节点指标、07 ads_ 前缀、09 technology_id、11 图版本、15 metric_id 重复）；涉及 D12 的 3 条（CF-02/03/04）。

`python 产物/_work/C05-check.py` 实际输出：

```
OK yaml.safe_load; cards=49 (INT-C-*-400..499 唯一)
OK raw mentions=80 -> canonical=49; dedup missing=0 extra=0
OK by_kind={'dwd_master': 3, 'map_bridge': 7, 'ads': 15, 'override': 3, 'dim': 5, 'snapshot': 4, 'cfg': 3, 'user_own': 4, 'es': 2, 'ods': 1, 'cache': 1, 'nebula_schema': 1}
OK structure_escalation=47 conflicts=19 risks=5 open_items=11 low_conf=3
INFO 待 Z01 补归并（范围外已出现产物）: {'SCI-INT-A06': 9, 'SCI-INT-A07': 7, 'SCI-INT-A08': 9, 'SCI-INT-A10': 7}
```

最大 3 个开放项：

1. OI-C05-02（P0）：三要素主数据（scholar_id / technology_id / org_uid）由谁持有未定，所有主键草案都依赖它。
2. OI-C05-03（P0）：lumen 链路落 demo_* 的风险，包括图 space 写 demo_gkx_chain、lumen-algo-py 的 K8s 配置写 demo_gkxlumenx_*、innov 读 demo 库。
3. OI-C05-06（P1）：甲方是否允许缓存 / 落库久新 API 结果（DN-09）。

## 5. 架构合规自检

| 铁律 | 结论 |
|---|---|
| 算法只在 Python | ✅ 所有写 ADS / 快照 / 人工层的写入方都是 lumen-algo-py 或 GDF/ETL；Java 只读 |
| 调用链 前端→Java→Python /internal/* | ✅ 人工层、变更集由 Java 经 `/internal/*` 提交，再由 Python 落表（R-C05-05） |
| 图谱只用 NebulaGraph TRSGraph | ✅ X-490 只在 TRSGraph 中追加；未新建 space，未用 Neo4j |
| Java 只读 ADS、不直连 nGQL | ✅ 每张卡的读取方是 Java 只读；用户态表（收藏 / 分组 / 订阅 / 模板 / 填报）需要 Java 写，放在 cfg/ods 而不是 ADS，已作为 CF-C05-16 提给李伟确认 |
| 可观测 | N/A（分析叶，不改代码）；变更日志卡带 trace_id |
| D9 数据血缘 | ✅ 快照主键都含 metric_id；没有发明 metric_id，重复登记问题见 CF-C05-15 |
| **D12 demo/lumen 隔离** | ✅ 规范卡的物理位置一律是 `gkxlumenx_*`（check 断言），demo 只出现在 X-490 的现状描述里。⚠️ 发现 3 处违规方案或存量问题，只写进 conflicts / risks，没有采纳：C04 方案写 demo_gkx_chain；lumen-algo-py 的 K8s 配置写 demo_gkxlumenx_*；gkxlumen-innov 读 demo_gkxlumenx_* |
| 业务口径不替甲方拍板 | ✅ 行政区划精度、分类体系、久新落库合规都列为决策项，没有裁决 |
| 结构升级 | ✅ 所有新表 / 新索引都标 `structure_escalation: true`，指向 human:李伟 |

## 6. cost

| 字段 | 值 |
|---|---|
| actual_tokens | ≈ 900k（估算，含两轮上下文压缩） |
| model_used | claude-opus（Cursor agent） |
| actual_cost | ≈ $9.0（估算） |
| cost_warn | yellow（>$5 且 <$10） |

## 8. 补归并（2026-10-19，恢复后复核）

晚到提法 82 条（A06–A15、B02–B09）已并入本文件：58 条挂到原有卡，新卡 8 张（INT-C-X-491、INT-C-TECH-492、INT-C-X-493、INT-C-TECH-494、INT-C-ORG-495、INT-C-ORG-496、INT-C-X-497、INT-C-X-498）。scope_count=162，card_count=57，差集 0。人才流动边、人才主档、湾区/深圳地理扩展、共享快照、A14 图谱标签按「并入已有卡、不另造表」处理。

恢复后复跑 `产物/_work/C05-check.py`，退出码 0：原始提法 162 全部落在 dedup_map，号段 400–499 唯一。上文 §2 里「A06/A07/A08/A10 待 Z01 补归并」已被这次归并覆盖。本叶仍是待签收，没有新开任务，也没有 commit。

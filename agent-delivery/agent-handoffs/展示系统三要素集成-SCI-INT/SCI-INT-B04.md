# SCI-INT-B04 handoff：人才引进评估 DS-16（6）+ 结构统计（1）

| 项 | 值 |
|---|---|
| task_id | SCI-INT-B04（spike） |
| 执行 | agent:algorithm-agent |
| 监管人 | human:淮政玮 |
| 对端 | 无（DS-16 不进久新包；结构统计自建） |
| ponytail | N/A（spike 分析，无代码） |
| 日期 | 2026-10-19 |

## 1. 范围与实现

- **范围**：总派单 B04 的 7 条。6 条 DS-16 人才引进评估 + 1 条查询结果人才结构。每条一卡，`layer=metric`，号段 `INT-B-TAL-300` … `INT-B-TAL-306`。
- **产出**：`产物/SCI-INT-B04.yaml`。模式与 `algorithm_type` 保持包内 `b01`，未改挂、未发明 `M_*`。
- **DS-16 六条**（005 / 006 / 007 / 010 / 013 / 025）：`IP-10`，`counterpart: none`，`delivery_form: none`，`jiuxin_row_id: null`。Java 门面只回空态，不经 Python，不向久新要接口。
- **结构统计** `M_TALENT_STRUCT_QUERY`：`STAT`、`IP-01`。GDF 聚合进 ADS，Java 只读；Python 不参与。
- **主档**：七张卡的下游都只引用已升级的 `SE-B03-01`（`dwd_talent_master`），本叶不另起表名，`structure_escalation` 全部为 false。
- **成本模型**（013）：采集来源未定（DN-A15-COST）。不出费用，不建费用表。

### 1.1 久新依赖

本叶不新增久新行号，也不消费已有行。六条库缺型叶禁止伪造 API 行；结构统计是自建 SQL 聚合，没有对端行。

| 久新行 | 角色 | 消费卡 |
|---|---|---|
| （无） | DS-16 不进久新包 | INT-B-TAL-300 … 305 |
| （无） | 结构查询自建 | INT-B-TAL-306 |

### 1.2 六条 owner 建议

建议只登记，不拍板。三选一仍留在各卡 `decision_needed`，不写成久新已提供。倾向都是「范围调整」：无注册源，且包内写明不进久新包。若产品保留该能力，再改为「我方自研」，仍不得新开久新行、不得改挂 164 / 501 / 111 / 157 / 160 / 165。

| 卡 | 指标 | 约束 | 建议 |
|---|---|---|---|
| INT-B-TAL-300 | 沟通障碍智能检测（005） | 原文要模型，不是尽调字段；禁止改挂 164/501；不发明指标 | 范围调整 |
| INT-B-TAL-301 | 文化融合风险评估（006） | 原文要模型；禁止改挂 164 | 范围调整 |
| INT-B-TAL-302 | 国际流动壁垒分析（007） | 禁止按号挂 111；157 不顶替 | 范围调整 |
| INT-B-TAL-303 | 引进阻力量化评分（010） | 禁止改挂 164 招引推荐指数；501 不等于本指标覆盖；智库标法不冲掉 A | 范围调整 |
| INT-B-TAL-304 | 高精度成本模型构建（013） | 禁止改挂 164；来源未定（DN-A15-COST）；不建费用表 | 范围调整 |
| INT-B-TAL-305 | 团队组合与协同分析（025） | 对不上 164/165；禁止 160 顶替；禁止按号挂 165 | 范围调整 |

## 2. 偏离说明

- 卡片数 = 指标数 = 7，差集空。未按页面再拆卡。
- 骨架曾带预填 note，核对后已删除。卡内容未推倒重写。
- C 层草稿把学者表对端写成 `gkx_mysql_raw` 且模式为占位。本叶结构统计按包内 `IP-01` 写，不把 C 层占位抄进来。
- DS-16 页面引用只保留包内 `DS-16-TALENT-RECRUIT`。结构统计包内 `srs_refs_02` 为空，`page_ref` 保持空。

## 3. 产物清单

- `agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/产物/SCI-INT-B04.yaml`（7 张卡）
- `agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/产物/_work/B04-check.py`
- 本 handoff
- 没有 commit，没有 push，没有改业务仓、seed 或矩阵。

## 4. 验收证据

执行 `python "agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/产物/_work/B04-check.py"`，退出码 0：

```
cards=7 expect=7 gap=[]
int_ids=300-306 unique=7
jiuxin_rows: []
structure_escalation_refs: ['SE-B03-01']
OK
```

脚本核对：包内 7 个 metric_id 全覆盖且顺序一致、差集为空、卡号在 300–399、无占位符 TBD、模式与 `algorithm_type` 与久新行均等于包内 `b01`。另核对：六条 DS-16 为 IP-10 且 `counterpart: none`、owner 三选一留在 `decision_needed`、结构统计为 STAT / IP-01、013 写明不建费用表、全文结构升级 id 只有 `SE-B03-01`、无 `SRS-` 行号。

**结论：7 张卡，差集 0。**

### 4.1 结构升级

| id | 负责人 | 表 | 范围 |
|---|---|---|---|
| SE-B03-01（引用，不新开） | human:李伟 | `dwd_talent_master` | 七张卡的主档都只引用此项。本叶无新 id |

### 4.2 最大 3 个开放项

1. **DS-16 六项无来源**（DN-04）：owner 三选一未拍板。本叶倾向范围调整，不代产品或甲方关闭。
2. **013 成本采集来源**（DN-A15-COST）：未定。确认前不出费用、不建费用表。
3. **结构统计主档表名**：只引用 `SE-B03-01`。ADS 落表名仍由 B03 升李伟，本叶不另起。

## 5. 架构合规自检

| 铁律 | 结论 |
|---|---|
| 1 算法只在 Python | ✅ DS-16 不实现算法；结构统计的聚合在 GDF SQL，Java 只读 ADS |
| 2 调用链：前端 → Java → Python /internal | ✅ DS-16 不经 Python、不直连久新；IP-01 由 Java 读 ADS |
| 3 只用 NebulaGraph | ✅ 本叶不写图、不写 nGQL；未采用 Neo4j |
| 4 可观测 | N/A（spike 分析，无代码） |
| 5 CI/CD | N/A（spike，cicd skip） |
| 6 demo 不 merge 进 lumen | ✅ 未改任何业务仓 |
| 7 共享聚合核心 | ✅ 结构统计读 ADS；主档只引用 SE-B03-01，不另造一份人才主档 |
| 8 ADS 先行 + Mock | ✅ D1=草案、D4=Mock 只记包内现状；无源即空态，USE_MOCK=false 不填假数 |
| 9 D8 | N/A |
| 10 D9 | ✅ 每卡绑定包内 metric_id，未把状态改绿，未读 metrics/registry |
| 11 D10 | N/A |
| 12 D12 | ✅ 未指向 demo-* 服务；未改 lumen 调用链 |
| 业务口径不替甲方拍板 | ✅ owner 三选一留在 decision_needed；建议只写在本 handoff |
| 只读 | ✅ 未连库，未 commit，未读 task-registry.yaml |

## 6. cost

价表无 grok 行。按 algorithm 默认比例 75/25，用旗舰档 Opus 4.7 单价（输入 $15/M、输出 $75/M）作上界。`source: estimate`。

`actual_cost = 120000×0.75×15/1e6 + 120000×0.25×75/1e6 = 3.60`

| 字段 | 值 |
|---|---|
| actual_tokens | 120000 |
| model_used | grok-4.7 |
| actual_cost | 3.60 |
| cost_warn | green |

未超过 $10，不暂停。

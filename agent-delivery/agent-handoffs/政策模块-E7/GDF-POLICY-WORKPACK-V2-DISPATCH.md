# 派单包：政策维 GDF 工作包 v2（对标企业包 + 产业抽取 + 条款结构化）

> **状态**：2026-10-26 已按 §0.2 的目录、同表、不补 07/08/14 落盘。第 4 项随后按用户要求改掉：GDF 配包内 Python，不配内部 HTTP。见包内 `12` / `15`（v2.0.2）。  
> **已认领**：`agent:data-agent`，监管人 `human:淮政玮`。正文在 `GDF-POLICY-WORKPACK-v2/`。  
> **过程**：WBS-06-03B。见 `工程过程/04-系统集成/06-GDF数据治理集成/WBS.md` 与同目录 `技术方案.md`。不代替 WBS-06-03，不并进 WBS-06-17 / 06-18。

- **派发角色**：coordinator-agent
- **承接 / Owner**：`human:淮政玮`（执行 `data-agent`；监管人必须是淮政玮，不用 data-agent 默认监管徐滕强）
- **协作**：GDF 导入核对 = `human:辜少彬` / CDC 预填 = `human:胡森泉`（本叶只出包，不代替他们导入或预填）
- **仓**：`gkx-orchestration`（`agent-delivery/data/GDF/派单包/政策/`）
- **Epic**：`E-PLATFORM-P1`
- **Sprint**：`2026-W44`
- **task-id**：`GDF-POLICY-WORKPACK-V2-L01`
- **强度**：definition，**禁止** ponytail 行
- **图**：`POLICY-STORAGE-FLOW`。本叶不改拓扑。发现新写库边先停，改流图会签后再写进包。

---

## 0. 沿用（v1 已冻结，本叶不重开）

| # | 决策 | 值 |
|---|------|-----|
| 1 | 源 | 三方 `gkx.dwd_policy_base`（国内）+ `gkx.dwd_global_policy_base`（国际），只读 |
| 2 | 目标 ODS | `gkxlumenx_ods` 同名表。Demo `demo_gkxlumenx_*` 只作对照，禁止当产线目标 |
| 3 | 目标 DWD 主表 | **一张** `gkxlumenx_dwd.policy_base_info`。`policy_id`←ODS `id`。UK 永远 `(source_plane, policy_id)`（MAP-01 方案 A，2026-09-01 淮政玮）。禁止 `gbl:` 改键，禁止第二张政策主表 |
| 4 | Mapping | 施工真源仍是 v1 的 `09` 明细。v2 **原样继承**，禁止改字段矩阵、禁止重开 MAP-01 |
| 5 | 作废 | `dwd_zck_*`、旧稿 37 列宽表、PG、Demo `polan/ods_sync.py` 当产线 DAG |

## 0.1 本叶加工（写进 v2，不进 CDC）

派单口语里的「条件结构化」= **条款结构化**。

| 作业 | 读 | 写 | 禁止 |
|------|----|----|------|
| POLICY-C1 抽取产业 | `policy_base_info` 的 `title` / `abstract` / `keywords` / `keypoints` / `content` / `policy_support`。不用 `theme` 当查询词 | 只写 `policy_industry_rel`：DWD 按槽位插入/复活/逻辑删除，同一事务同步 ADS 同名表 | 改主表任何列；回写 `related_entities.industry`；物理删除；检索失败写假链码 |
| POLICY-C2 条款结构化 | 同一主表的 `title` / `abstract` / `content`，以及已洗入的 `policy_support` | 只合并 `gkxlumenx_ads.policy_text_parse`：`structured_elements.clauses` + `clause_meta` | `TRUNCATE`；写 ES；回写 DWD；模型失败写假条款 |

两作业都在 Wave B 当日 `success` 之后。互不依赖。B 失败或只完成贴源时不触发。C 失败不回滚已成功的 B。

交付物是 **Python 脚本**，在现行包 `scripts/`。GDF 复制到自己的 Python 节点后执行。禁止在 CDC、SeaTunnel 里另写切条或对码。不要把内部 HTTP 配成这两项作业。日批 `limit`≤100，不要堵在 Mapping 作业的进程里。流程图在包内 `12`。

## 0.2 待精修（起草时未请人拍板）

1. **目录策略**：现案是新建 `GDF-POLICY-WORKPACK-v2/`，v1 降历史、不改 v1 正文。若改为在 v1 上加文件升 v1.1，改本节和 §1。
2. **国内/国外是否仍进同一张主表**：v1 已拍板同表。WBS-06-17（`SYSINT-06-17-L01`）写明国内政策另有一叶、不并进 `policy_base_info` 包，且该叶尚无派单包。本叶默认继承 v1 同表，不兼做 06-17。若要拆包，先改本说明再改任务。
3. **企业包里有、本叶 DoD 未列的文件**：`07-启动会材料`、`08` 导读、`14` 图谱卷。政策侧图谱不在本叶。需要就补进 §1。
4. **15 的调度方式**：已按用户要求改掉。现行是 GDF 复制 `scripts/` 两份 Python，两张平面 B 都成功后在自己的节点上跑。不配内部 HTTP，也不把飞书值班当当前投递。

---

## 1. 产物落点

新建目录（对标 **企业 v4** 的开工件，缺文件不许用「目录在」冒充完成）。Wave A/B 正文从 v1.0.3 **复制继承**，只加版本指针和「现行包改为 v2」；不重写 09 矩阵。

`agent-delivery/data/GDF/派单包/政策/GDF-POLICY-WORKPACK-v2/`

| 文件 | 必须写清 |
|------|----------|
| `README.md` + `00-派单说明书.md` | 现行可投递或剩余开放项；作废清单；Wave A → B → C 顺序；C 不进 Mapping CDC |
| `01-命名与分层词典.md` | `gkx.dwd_*` = 本项目 ODS，不是项目 DWD |
| `02-WaveA-贴源表清单.yaml` | 两张 P0 + `is_deleted=0` / 非历史（继承 v1） |
| `03` / `04` | 连接（口令线下）+ 技术字段与过滤 |
| `05-WaveA-验收检查表.md` | 对标企业 `05`：表数对齐 `02`，供 GDF 回签 |
| `06-WaveB-Mapping派工.md` | 洗入一张 `policy_base_info`；点名 C 不进本派工字段配置 |
| `09-政策域-ETL-Mapping明细-源表到DWD.md` | **施工真源**。继承 v1，不改列规则 |
| `10-DWD-MySQL-DDL/` | `policy_base_info` 快照 + `policy_industry_rel` DDL。条款落在 ADS `policy_text_parse`，不另造 DWD 条款表 |
| `11-作废与误源对照.md` | 继承 v1 作废项，并写上：CDC/SeaTunnel 另写抽取或切条、C 改主表、条款 TRUNCATE / 写 ES |
| `12-DWD后加工-抽取产业与条款结构化.md` | C1/C2 的读、写、增量跳过、失败不写假结果、中台函数名。对标企业 `12`/`14` 的「作业边界」厚度，不是企业那两卷的 ES/图谱内容 |
| `13-现网DDL差集-GDF开工必读.md` | 对标企业 `13`：只核 `gkxlumenx_ods` / `gkxlumenx_dwd`；缺列只 ADD；禁止 DROP、禁止改已有列类型；GDF 不连 demo |
| `15-GDF触发调度与回执.md` | 对标企业 `15`：B success 后才触发 C1/C2；GDF 只触发和收终态；目标契约与现网缺口分开写；现网未接通不得画成今日 DAG |
| `CHANGELOG.md` | v2.0 相对 v1.0.3 的差异 |

回写：

- `data/GDF/派单包/README.md`：现行政策包改为 v2，v1 标历史
- v1 `README.md` 顶部加一行「已被 v2 替代，禁止当现行施工包」（这一处是指针，不改 v1 的 09/00 正文）

**本叶不要求** CDC 预填 xlsx（胡森泉下一叶）。包不齐则禁止喊「可以预填」。通用 `parse_workpack.py` 仍不认 `policy_base_info` 字段行，预填叶须先补解析规则或按 09 人工配置；本叶在 README 写明这一缺口即可。

---

## 2. 必读

| 序 | 路径 | 用途 |
|---:|------|------|
| 1 | `data/GDF/GDF协作指南.md` | 谁配作业、谁出包 |
| 2 | `data/GDF/派单包/企业/GDF-ENT-WORKPACK-v4/` | **目录样板**（05 / 13 / 15 的写法）。不要把企业 ES、图谱表名抄进政策包 |
| 3 | `data/GDF/派单包/政策/GDF-POLICY-WORKPACK-v1/` | Wave A/B 继承真源，含 `09` 与 `10` |
| 4 | `data/GDF/派单包/政策/GDF-POLICY-WORKPACK-v1/12-DWD后加工-抽取产业与条款结构化.md` | C1/C2 现口径，v2 加深而不是另起一套规则 |
| 5 | `data/data-design/storage/POLICY/01-data-flow.md` | `POLICY-STORAGE-FLOW`；产业关联与条款落点 |
| 6 | `data/data-design/storage/POLICY/stores/mysql/dwd.md` | `policy_industry_rel` 与 `related_entities.industry` 弃用 |
| 7 | `data/data-design/storage/POLICY/etl/industry-match-optimize.md` | 对码文本与 `12` 是否一致，冲突先停 |
| 8 | `agent-handoffs/产品整体定义/跨系统-向量库/POL-CLAUSE-BATCH-L01.md` | 条款跑批已有口径（规则先切，模型只兜底） |
| 9 | 本文件 | 精修后的派单说明，优先于聊天口述 |

---

## 3. `/goal`

定义叶。禁止 ponytail 强度行。身份行按手册 §9.6。

```
/goal data-agent
身份：你是经验丰富、遵循最佳实践的资深数据架构/数据工程师，精通数仓分层(ODS/DWD/DWM/ADS)、数据建模、数据质量与血缘；践行数据契约先行。
强度：N/A（定义/文档）。本单不出 SQL/ETL 脚本。
上下文：定义包，禁止用 headroom 压缩代替精读 09 与 12。
任务 ID：GDF-POLICY-WORKPACK-V2-L01
监管人：human:淮政玮
仓：gkx-orchestration
性质：设计类（cicd: skip）
图：必含 POLICY-STORAGE-FLOW。本叶不改拓扑；图文冲突以图为准。必读 agent-delivery/diagram-as-contract.md。发现新写库边先停。
范围：新建 派单包/政策/GDF-POLICY-WORKPACK-v2。Wave A/B 原样继承 v1.0.3（两源贴源，洗入一张 policy_base_info，UK=(source_plane, policy_id)）。加工卷写清 POLICY-C1 产业抽取与 POLICY-C2 条款结构化：C1 只写 policy_industry_rel（DWD 同步 ADS），C2 只合并 ADS policy_text_parse.clauses。目录对标企业 v4 的 05/13/15，外加政策 12。v1 降为历史。
禁止：重开 MAP-01 或改 09 字段矩阵；CDC/SeaTunnel 另写切条或对码；C 改主表或回写 related_entities.industry；条款 TRUNCATE 或写 ES；GDF 直连 Python/模型/向量库；Java 门面未落地写成产线已接通；写 Nebula；改 lumen 业务仓；把 demo_gkxlumenx_* 当产线目标；密钥进 Git；本叶出 CDC 预填 xlsx。
DoD：见 task-registry GDF-POLICY-WORKPACK-V2-L01。
Handoff：agent-handoffs/政策模块-E7/GDF-POLICY-WORKPACK-V2-L01.md
```

---

## 4. 验收对照（摘 registry DoD）

- 存在 `GDF-POLICY-WORKPACK-v2/`，含 00/01/02/03/04/05/06/09/10/11/12/13/15/CHANGELOG/README
- 09 与 v1.0.3 字段矩阵一致；UK 仍是 `(source_plane, policy_id)`
- 12 写明 C1、C2 的读写表、增量跳过、失败不写假结果、中台函数名
- 15 把「目标契约」和「现网尚未接通」分开；B 未 success 不触发 C
- `派单包/README.md` 现行政策包 = v2，v1 标历史
- 无 CDC 预填、无业务仓 diff、无 `POLICY-STORAGE-FLOW` diff
- handoff：`agent-handoffs/政策模块-E7/GDF-POLICY-WORKPACK-V2-L01.md`

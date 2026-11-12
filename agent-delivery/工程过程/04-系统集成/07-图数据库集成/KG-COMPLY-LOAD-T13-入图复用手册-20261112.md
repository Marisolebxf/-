# KG-COMPLY-LOAD-T13 · 入图过程复用手册（执行器参数化）

| 项 | 内容 |
|---|---|
| 执行人 | `human:白鑫凤`（认领 2026-11-12 15:41） |
| 日期 | 2026-11-12 |
| 交付位置 | 本目录（07-图数据库集成） |
| 输入 | T02（`887db942` 前序交付及 `scripts/t02_m02*.py`）、T03（`scripts/kg-comply-t03*.py`、`对接文档/燕大/T03/`）、T04（`KG-COMPLY-LOAD-T04-交付-20261112/t04_loader.py` 及对账单）三单已签收 done 的执行器经验 |
| 依据 | SDD §5 T13、[KG-COMPLY-VID-L01](./KG-COMPLY-VID-L01-VID前缀实测与裁定.md)、[KG-COMPLY-STRUCT-L01](./KG-COMPLY-STRUCT-L01-结构与空间选定.md)、[KG-COMPLY-T11-正式线结构覆盖对照清单](./KG-COMPLY-T11-正式线结构覆盖对照清单.md) |
| DoD | ①参数表（space/props.batch/VID/源表映射/建点跳过策略）+ ②复跑步骤 + ③对账模板；写明换 space 名复跑路径 |
| 不做什么 | 不实际在 `gkx_chain` 复跑；不写成正式加工派单；本手册不触发任何写库 |

> **一分钟说明**：本手册把 T02–T04 三单手工跑通的入图做法参数化。目标读着（SDD 原文）：*任何人按手册、不靠口头，能在另一空间复跑同一套结构*。所有具体数字均为 2026-11-12 签收时的实测终值，复跑时以自己的对账单为准。

---

## 1. 流程总览

```
久新 ADS（Doris 47.93.119.170:29030 / gkx_technology_analysis_dev）
        │ 只读 SQL（count 预检 → JOIN 带名取数）
        ▼
入图执行器（Python：Doris 读 + Nebula 写）
        │ ①probe 预检 → ②dry-run 演练 → ③pilot 小批 → ④full 全量
        │ 每批：端点先探后建 → 批量 INSERT（rank=0 幂等）→ 回读计数 → 跳过留档 CSV
        ▼
图库（TRSGraph 10.50.75.136:9669，space = demo_gkx_chain，参数可换）
        │
        ▼
对账（应灌 vs 实灌 vs 批号回读；存量边按边数对源行；只读核验查询）
```

三单分工与批号一览（本期实灌终值，均已签收）：

| 单 | 范围 | 批号 | 实灌终值 |
|---|---|---|---|
| T02 | M02 cooperate research↔research | `comply-20261111-t02` | 3,442,271（原有 7,617 条核验跳过不重写） |
| T03 | person/research 主数据 + M01 + M04 | `comply-2026-11-11-t03` | M01 2,525,789；M04 72,099；点已存在新增 0 |
| T04 | person/research 覆盖写 + M08 + M09 + 随边建点 | `comply-20261112-t04-{1,2,3,4,p1,p2}`（1=试点批被 full 幂等覆盖；2=M09+patent；3/4=M08+project；p1/p2=person/research 主数据） | M08 17,426；M09 85,069；patent 70,496 / project 17,402 随边建 |

---

## 2. 参数表（DoD ①）

### 2.1 连接与目标空间

| 参数 | 本期值 | 复跑时 |
|---|---|---|
| `NEBULA_ADDR` | `10.50.75.136:9669` | 按目标环境 |
| `SPACE` | `demo_gkx_chain` | **必改**（见 §5；正式线空间名待定，勿预设 `gkx_chain`） |
| `DORIS_ADDR` | `47.93.119.170:29030` | 按源环境（正式线应指向我方加工链 ADS） |
| `DORIS_DB` | `gkx_technology_analysis_dev` | 按源环境 |
| 凭据 | 一律环境变量（`NEBULA_USER/PASS`、`DORIS_USER/PASS`），**不落盘、不进 git** | 铁律不变 |

客户端：Python + `pymysql`（Doris，MySQL 协议）+ `nebula3-python`（老版客户端，`Config` 非 `Configs`）。

### 2.2 批号规则 `props.batch`

- 格式：`comply-<日期>-<任务号>[-序号]`，如 `comply-20261112-t04-2`。
- **只有本期新写入的点和边才带批号**；执行器回读对账按 `props CONTAINS "<batch>"` 计数。
- 试点批（pilot）会被同任务 full 批幂等覆盖，终态以 full 批号为准。
- ⚠️ **不给存量边补批号**（改既有数据禁止，见 §6）；存量边改用「边数 vs 源行数」对账。
- 复跑（正式线）时应换前缀体系（如 `prod-<日期>-<批次>`），与合规线 `comply-*` 区分，具体以正式派单为准。

### 2.3 VID 规则（两套并存，裁定 [KG-COMPLY-VID-L01](./KG-COMPLY-VID-L01-VID前缀实测与裁定.md) 五条）

**编号一律「从数据读字段拼出来」，不按文档硬算。**

| 点类别 | 本期现场规则（demo 存量在用） | 正式库目标规则 | 编号来源字段 |
|---|---|---|---|
| 企业 enterprise | `ent:<org_id>`（32 位码） | `ent:<统一社会信用代码>` | 属性 `org_id`（信用代码列实测 0/208,394 有值，本期无料） |
| 产业链环节 segment | `segment:<segment_key>` | `seg:` + 环节码（码内嵌链号，如 `seg:INB1204…`；裁定原文口径） | 属性 `segment_key` |
| 服务机构 institution | `institution:<org_id>` | `svc:<org_id>` | 机构 `org_id` |
| 政策 policy | `pol:<政策主键>` | `policy:<政策主键>` | 政策源表主键 |
| 技术点层 5 类 | `tech_point:` 等（本期不动） | 同左 | — |
| **科研机构 research（新）** | `inst:<institution_id>`（=规范规则） | 同左 | `institution_id` |
| **人才 person（新）** | `person:<talent_id>` | 同左 | `talent_id` |
| **论文 paper（新）** | `paper:<doi>`，无 DOI 退回 `paper:<src_id>` | 同左 | DOI / 源主键 |
| **专利 patent（新）** | `patent:<patent_id>` | `patent:<patent_no>` | 本期画像表无 `patent_no` 列，按 SDD 退路用主键 |
| **项目 project（新）** | `proj:<project_id>` | `proj:<project_no>` | 同上，主键造号退路 |

> 落地即两套配置：「现场规则」本期用；「规范规则」留给正式库。⚠️ T11 实测提示的坑：`inst:`（research）与 `institution:`（institution）两个前缀极易串，代码里必须按 Tag 严格区分。

### 2.4 源表映射（久新 ADS → Tag/Edge）

**点（Tag）：**

| Tag | 源表 | 本期数 | 建点方式 |
|---|---|---:|---|
| person | `ads_talent_profile` | 100,000 | T04 主数据全量覆盖写（`props.source=T04主数据全量`） |
| research | `ads_institution_profile` | 83,745 | 同上（`institution_type_id` 原值入 props） |
| patent | `ads_patent_profile` | 70,496 | M09 随边建，带画像 title |
| project | `ads_project_profile` | 17,402 | M08 随边建，带画像 name |
| paper | （无可用源） | 0 | 结构在、本期 0 点 |

**边（Edge，四档：实灌 / 存量不重灌 / 裁定不建 / 空态）：**

| M | 边型/方向 | 源表/口径 | 本期终值 | 档 |
|---|---|---|---:|---|
| M01 | cooperate person↔person | `ads_talent_collaborator` 5,051,578 行，无向取 ID 小侧一条 | 2,525,789 | 实灌（T03） |
| M02 | cooperate research↔research | `ads_institution_collaboration_yearly` 跨年合并（ID 小侧），排除 company 端点 | 3,442,271 | 实灌（T02） |
| M04 | belong person→research | `ads_talent_experience`（`experience_type=2` 工作经历），排除 company、同机构多段合并成唯一对 | 72,099 | 实灌（T03） |
| M08 | participate research→project | `ads_project_institution` 且 `institution_role_code` 非空（源表方向项目→机构，SELECT 已对调） | 17,426 | 实灌（T04） |
| M09 | author_of person→patent | `ads_talent_patent` | 85,069 | 实灌（T04） |
| M15 | depends_on segment→segment | 存量 | 1,073 | **存量只回读，不重灌** |
| M17 | participates enterprise→segment | 存量 | 178,731 | 同上 |
| M22 | cooperate enterprise↔enterprise | 存量 | 94,824 | 同上 |
| M07 | —（不建） | `ads_talent_project` 770 万行 100% `funded_output_author`，资助署名≠参与 | 0 | 裁定不建 |
| M06/M03/M19/M20 | — | M06 无源；M03 端点全 company（8,784 机构无一合格）；M19 与 **M02** 同源（research_coop）；M20 与 **M01** 同源（talent_coop） | 0 | 裁定记 0 或停建 |
| M05/M10–M14/M16/M18/M21/M23/M24 | 11 条 M：10 条挂 8 种边型全 0（M12–M14 同挂 `policy_apply_to`；M16 挂存量 `cite`）；M18 挂存量 `participates` 按口径 0——该边 213,500 条属 M17 与历史混装，勿按边名总数误判非空 | 0 | 空态（T05 核验） |

> ⚠️ **边型拼写陷阱**：`participate`（无 s，M07/M08，2026-11-11 T01 补建）与 `participates`（有 s，M17/M18，历史存量边）是**两个不同的边型**——查询、对账、建边时差一个字母就是在操作另一条边，写脚本前先核对清楚（T05 报告已提示的手滑点）。同理 `cite` 一个边型装两条 M——M06 paper→paper、**M16 政策→政策**（以 L03 M 表为准，唐绍祖 2026-11-12 勘误定案：原「M16 论文→专利」写法有误）——本期均 0，将来若只建其一必须按端点拆开核。

边属性通用形：`(weight, props)`，业务字段进 `props` JSON（如 M08 的 `relation_type`/`institution_role_code`、M01 的 `match_method=coauthor`、M04 的 `match_method=employment_history_aggregated`）。weight 口径按单：M02=Σ`co_paper_count`；M01=`collaboration_score`（空补 0）；M04=0；M08/M09=1.0 恒定。

**历史结构边与 T06 裁定**（不映射 M01–M24，如实登记）：

- `belongs_to` 覆盖 359 / 1,414 个环节，未挂链 **1,055 个环节数**（⚠️ 是环节数，**不是**「可补 1,055 条边」）；属结构归属，按 T06 裁定**本期不补边、不推断、不计入任何 M 关系的缺失率**——补建前须核源端 `chain_id`、目标链存在性与业务归属，本期只记录缺口。
- `support` / `apply_to` 端点 100% 重合，权重分别恒为常数 0.8 / 0.6（全图一个值，**不是强度**）：**停读 `support`、单读 `apply_to`**，权重不作强度用。
- institution→institution 34,769（在 `participates` 上）：本期不改名（`service_relate` 仅为正式线备选名），**不得映射** M02/M19/M17/M18。

### 2.5 建点与跳过策略

1. **先探后建（防空壳，最重要的一条）**：写边前对全部端点 VID 批量 `FETCH PROP ON <tag>` 探测，缺的才建；否则 Nebula 会**静默建空壳点且不报错**。
2. **主数据点 = 全量覆盖写**（源表真值为准，幂等覆盖随边/他人所建的兜底名点，终态全带真名）；**随边建点 = 只在端点缺失时补**，props 标 `source` 与批号。
3. **已存在点的两种处理，按来源定**：T03 用条件插入跳过（保他人属性）；T04 主数据用覆盖写。⚠️ `INSERT VERTEX` 是**整标签覆盖**——两任务都要写同一 Tag 时必须先对齐属性列集，否则后写会清掉先写的属性（T04 对账单 §4 已提示此交接风险）。
4. **存量边（M15/M17/M22）只回读核对，不重灌、不补批号**；否则边数翻倍、对账永对不上。
5. 跳过必须留档 CSV（`src_vid,dst_vid,reason`），异常行零跳过也要有空档证明。

---

## 3. 复跑步骤（DoD ②）

以 T04 执行器用法为模板（其余单同构）：

```bash
# 0) 前置：写入授权链成立（本期=徐滕强 2026-11-11 授权记录；复跑=正式派单+回签）；
#    环境变量就绪；确认目标 SPACE 不是 gkx_chain（本期）
export NEBULA_ADDR=10.50.75.136:9669 NEBULA_USER=… NEBULA_PASS=…
export DORIS_ADDR=47.93.119.170:29030 DORIS_USER=… DORIS_PASS=…

# 1) 结构核验（T01 流程）：schema 与目标空间逐 Tag/Edge 对照，缺口走 DDL 补建并复验
python3 t01_verify.py            # 只读

# 2) 预检 probe：源表 count vs 应灌数、关键列命中
python3 t04_loader.py --rel m08 --probe

# 3) dry-run：出样例 nGQL 语句，不写库
python3 t04_loader.py --rel m08 --dry-run 100

# 4) pilot 小批：真写 N 条带批号，全链路（探测/建点/回读）演练
python3 t04_loader.py --rel m08 --pilot 1000 --batch comply-<日期>-t04-1

# 5) full 全量：幂等（rank=0、(src,dst) 去重、断点续跑 journal），整批失败自动逐条重试定位坏行
python3 t04_loader.py --rel m08 --full --batch comply-<日期>-t04-4

# 6) 回读对账：执行器自动按批号 CONTAINS 计数；TRS 方言——点属性必须带 Tag 前缀
#    MATCH (v:person) WHERE v.`person`.props CONTAINS "<batch>" RETURN count(v)

# 7) 总账：按 §4 模板出对账单，交只读核验（模板见 t04_t10_verify.py / t05_empty_state.py）
```

工程参数（三单实测收敛值）：批大小 200 点/批、200 边/批；Doris 取数**一次性拉全量**（`LIMIT/OFFSET` 深翻页在 MPP 下又慢又可能漏/重行）；画像名 JOIN 行内带出优先、IN 批查（1000/批）兜底；长任务用分片+checkpoint+排他锁（T02：545 互斥分片、SQLite 断点）；nGQL 字符串必须整体转义（源表内容含裸换行会断裂语句）。图库侧读**一律按端点 Tag 锚定**——实例已触发内存高水位（0.8）：无锚定全表扫基本失效、大聚合会被拒（实测 `sum(e.weight)` 518 秒后被拒）；拉明细时另加 `LIMIT` 分批。

---

## 4. 对账单模板（DoD ③）

**边表**（每条实灌关系一行）：

| 关系 | 边型/方向 | 应灌 | 实灌 | 批号 | 核验 |
|---|---|---:|---:|---|---|
| M08 机构→项目 | participate: research→project | 17,426 | 17,426 | -t04-4 | ✅ MATCH count 一致；lead 17,393 + investigator 33；role/relation_type 入 props |
| M07 人才→项目 | 不建（无源） | 0 | 0 | — | 770 万行 100% funded_output_author，不得以资助署名冒充参与 |

**点表**：| Tag | 应灌 | 实灌 | 批号 | 说明 |（patent/project 注明「随边建」；paper 注明 0 点理由）

**存量不动区表**：灌数前后各跑一次，数字必须逐一相等。⚠️ 多端点边型必须**按端点拆分**核对，勿拿边名裸总数对账（本期基线：cooperate 的 ent↔ent = 94,824，须用 `MATCH (:enterprise)-[e:cooperate]->(:enterprise)` 拆——裸总数已是 6,062,884 = M01 2,525,789 + M02 3,442,271 + M22 94,824（T04 复核时实测即此数，见 T04T10-核验-实测.md）；participates 213,500（= M17 178,731 + 混装 34,769，本期无新写，裸总数即基线）；depends_on 1,073）。

**禁区表**：任务卡声明不碰的 M 系（如 T04 的 M10–M14/M16），复测必须全 0。

**只读核验查询集**（对账单的每个数字都要能被这些查询复现）：

```ngql
-- ⚠️ 图库已触发内存高水位（0.8）：查询一律按端点 Tag 锚定，禁无锚定全表扫；
--    大聚合会被拒（实测 sum(e.weight) 518s 被拒）；拉明细另加 LIMIT 分批
-- 总数（带锚定，兼做方向抽验防反转）
MATCH (:person)-[e:author_of]->(:patent) RETURN count(e);
-- 批号抽验（同样带锚定）
MATCH (:person)-[e:author_of]->(:patent) WITH e LIMIT 1 RETURN e.props AS p;
-- 多端点边型必须拆端点（cooperate 本期实存三路：person↔person / research↔research / ent↔ent；
-- M03 的 person→research 口径本期 0；T11 提示该边型共装 4 条 M，拆完才算对齐）
-- 存量与禁区同法；点属性条件必须带 Tag 前缀（TRS 方言）
```

**边界**：社群检测（T10 的 435/437 榜）为离线 JSON 结果、**不写回图**，不属本手册对账范围（社群口径见 T10 交付骨架记录）。

---

## 5. 换空间复跑说明（正式线路径）

**「换 space 名即可复跑」成立的前提是把下面这排开关一起切**，只改空间名是不够的：

| 开关 | 合规线（本期） | 正式线复跑时 |
|---|---|---|
| space | `demo_gkx_chain` | **待定**——T11 实测正式库尚不存在（`SHOW SPACES` 仅 demo 一个），且与 architecture-baseline v2.2.15「不建正式名 gkx_chain」有冲突，空间名待 WBS-07-00G/00H 责任人确认（勿预设） |
| VID 规则 | 现场规则（§2.3 左列） | 规范规则（§2.3 中列）；前提：正式加工链真能供出信用代码等字段 |
| 数据源 | 久新 ADS 现成 `ads_*` | 我方加工链 ADS（供应商库→ods→dwd→ads，GDF 调度） |
| 灌数口径 | 应灌子集（本期各裁定） | 不自动继承，按正式派单重新定 |
| 批号前缀 | `comply-*` | 正式批次体系，按派单 |
| 执行方式 | 人工脚本（本手册） | GDF 调度转发 → 引擎内部作业（见 `GDF-GRAPH-SCHED-CONTRACT-L01`） |
| 授权 | 徐滕强 2026-11-11 授权记录 | 正式派单发出 + 回签，未回签前一步不写 |

**正式线注意项**（T11/T04 签收时实测沉淀，建库前必须定性）：

1. `inst:`（research）与 `institution:`（institution）前缀易串；project 的 Tag 名与前缀不同形（`proj:`）。
2. `participates` 是唯一没有 weight 的边型（用 chain_role/participation_depth/chain_score），且 `first_year` 在 props JSON 内而非独立列——SDD §3.2 字面与实际不符，建契约时二选一。
3. M08/M09 本期 weight 恒 1.0 无强弱信息：不得把 Σweight 当业务量、前端不得按 weight 渲染粗细；M09 props 未记发明人排序；patent/project 随边建点属性薄（仅 source+batch），按年份/领域筛选需先补属性。
4. belongs_to/apply_to/support 三条历史边混装（共 22,273 条）、`participates` 上 institution→institution 34,769 条混装——正式线新建时按 M 定义拆开，别复刻混装。

---

## 6. 红线（复跑时同样生效）

1. **绝不写正式空间**（本期指 `gkx_chain`；正式线指一切未授权空间）——执行器进空间前应自检断言。
2. 不灌 mock、不从正式空间拷数。
3. 不给存量边/存量点补 props.batch（改既有数据禁止）。
4. cooperate（存量 ent↔ent）、participates（存量）、depends_on 不重建。
5. 凭据只走环境变量；批号之外的写入留痕（skip CSV、journal、对账单）缺一不可。
6. 本手册是操作说明，**不是正式加工派单**；正式线开工以派单+回签为准。

---

## 附：输入材料索引

| 材料 | 位置 |
|---|---|
| T04 执行器 + 对账单 | `KG-COMPLY-LOAD-T04-交付-20261112/`（t04_loader.py / t04_precheck.py / T04-对账单-交T07.md） |
| T02 执行器与全量证据 | `scripts/t02_m02*.py`；`T02-M02-全量入图-20261111.md` 及同目录 JSON |
| T03 执行器与验收 | `scripts/kg-comply-t03*.py`；`对接文档/燕大/T03/`（verification.json 等） |
| 只读核验模板 | `t04_t10_verify.py`、`t05_empty_state.py`、`T04T10-核验-实测.md`、`T05-空态核验报告.md` |
| 结构与裁定 | `KG-COMPLY-STRUCT-L01-结构与空间选定.md`、`KG-7ELEM-SCHEMA-DDL-L01`、`KG-COMPLY-VID-L01`、`KG-COMPLY-T11-正式线结构覆盖对照清单.md` |

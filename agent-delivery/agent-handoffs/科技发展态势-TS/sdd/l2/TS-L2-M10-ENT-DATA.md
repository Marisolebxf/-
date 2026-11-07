# TS-L2-M10-ENT-DATA · 维护管理 · 关键实体与关系 · 数据落点

- 任务：`TS-L2-M10-ENT-DATA`
- 日期：2026-11-07
- 状态：四角色会签完成（DATA 3+API 跨册 3+ARCH-A4 全回填），**待监管人签收**。不标 done
- 监管：`human:刘剑锋` · 认领：`agent:data-agent`
- 强度：ponytail off（定义任务，不缩文档）
- 用户故事：全景序 41–47
- 上游：`sdd/l2/TS-L2-M10-ENT-ARCH.md`（done）· A03 write_back_design_draft（已加消费注记）· 会签输入：`会签/TS-L2-M10-ENT-SIGNOFF-DATA.md`（8 决策项/建表基线 10 张/VID 四交叉点）

本叶定 M10-ENT 的数据落点：**MySQL 变更链 5 表 + 技术点主表 + ADS 投影 + Nebula 投影边界**（列级定义非可执行 SQL）。**不建 cfg_ 配置表**（与 LAYER 模式区隔）。本单不建库不建表不灌数。

## 0. 决策项裁定（DATA 会签 7.1 八项，本叶落笔方案）

| # | 决策项 | 本叶方案（会签/监管人可否） |
|---|---|---|
| D1 库名 | 变更链+主表落库 | **`gkxlumenx_dwd`**（Python 写侧现有库；已对照 algo-mysql-connection-info 查重——gkxlumenx_dwd 在五业务库清单内无撞名；**非** Java 平台库）。**写者=Python 单写者先行**（OI-A03-05 推荐档；DN-07 若推翻按退路迁移，沿 LAYER 演变先例记档） |
| D2 主表分层 | DWD 持有+ADS 镜像 vs 单层 | **两层**（C02 INT-C-TECH-180 建议）：主表 `dwd.technology_master`（真源）+ ADS 镜像（Java 只读面） |
| D3 ADS 投影 | 复用 graph_node/edge vs 新建 | **新建同构** `gkxlumenx_ads.graph_entity_node` / `graph_entity_edge`（前缀 entity 区分技术–技术图投影；复用需核 as-built 承载，新建边界干净）——会签可否 |
| D4 Demo 落点 | Demo 投影 | `demo_gkx_chain` + demo ADS 实例（结构同正式；storage README §5.1） |
| D5 快照 N | 每 N 版全量快照 | **默认 N=50** 报监管人确认（A03 无归属人，本叶拟默认）；change_set_ids[] 用**关联表** graph_version_change_set（可索引、回滚可追溯） |
| D6 合并/redirect | 首版做否 | **首版不做**（API 册同裁：查重命中只提示「仍新建」）；redirect 语义留 A03 id_stability 在册 |
| D7 status 值域 | change_set 状态机 | `draft/approved/published/rejected`（approve 可选 DN-A03-02；approved 非必经） |
| D8 保留期 | 版本/审计保留 | 沿 DN-A03-06 待拍板（在册），表设计不预设 |

## 1. MySQL 变更链（gkxlumenx_dwd，写者=Python）

建表基线 **10 张**（会签清单；列级要点，DDL 归实现单）：

| 表 | 粒度/要点 |
|---|---|
| `technology_master` | 一行一技术点：technology_id BIGINT PK（自建主表先行档）、name_cn/name_en、category（引用 dim_tech_domain 维表，C02-181）、description、importance_level、external_ids JSON（**外部 ID 对齐字段——OI-A03-01 返工护栏**，ARCH 会签）、status、created/updated |
| `graph_change_set` | 一行一变更集：id、base_version、ops JSON（7 op 封闭枚举）、status（D7 值域）、operator、trace_id、created |
| `graph_change_log` | 一行一对象变更：change_id、version_id、object_type/object_id、op、before/after JSON、operator、trace_id、at（审计双轨之一，请求级归 Java @SysLog） |
| `graph_version` | 一行一版本：version_id、parent_version_id、label、operator、created、stats JSON |
| `graph_version_change_set` | 版本↔变更集多对多关联（D5） |
| `graph_tombstone` | 一行一抑制对象：object_type/object_id、reason、operator、at（auto 复活抑制；**会签 DATA-C1 补漏表**） |
| `graph_conflict_queue` | 一行一冲突：auto 新值 vs manual 覆盖字段、状态（DN-A03-03；**会签 DATA-C1 补漏表**；reserved 首版空实现但表建） |
| `graph_snapshot` | 每 N=50 版全量快照（D5；体积随版本数/N） |
| `dim_tech_domain` | 技术领域维表（C02-181；本页只读选用） |
| `graph_entity_overlay` | 三方实体覆盖层（update_entity_overlay 存储面——三分册会签 API 跨册补）：entity_type+entity_id 唯一、patch 字段、version_id |
| `graph_version` 列补 | **projection_status**（三分册会签 API 跨册补：R2 暴露依赖此列） |
| ADS：`graph_entity_node` / `graph_entity_edge` | 见 §2 |

版本 diff 不独立物化（change_log before/after 可聚合推导，会签 §5 同裁）。

## 2. ADS 投影（gkxlumenx_ads，Python 发布时写，Java 只读）

- `graph_entity_node`：technology_id、name_cn、category、importance_level、overlay 套用后展示字段、version_id
- `graph_entity_edge`：edge_key(src,dst,rel_type,rank)、**strength_auto / strength_manual / source 三列**（ALGO 保护条款落列——读面指标只取 auto）、time_range(年粒度)、version_id
- R2 全景现状读经 display→topic Java 读此投影（含 projection_status）

## 3. Nebula 投影边界（gkx_chain，写者=Python 发布事务）

- 首版增量投影：本页写回产生的 UPSERT/DELETE VERTEX/EDGE；**VID=`tech:{technology_id}`**
- **存量 `tech:{名称}` 不迁移**（OI-A03-02 留 C04）；读侧 union 经主表 technology_id 解析（ARCH-C2 口径）
- **存量 seed 前置（三分册会签 DATA-A1 补）**：实现单须含一步「存量技术点映射 seed」——扫描 Nebula 存量 technology 顶点（名称 VID），在 `technology_master` 建 seed 行（technology_id 生成+name_cn=存量名+external_ids 记 `legacy_vid`），使主表先行档真正可解析；seed 幂等（ON DUPLICATE）
- VID 四交叉点（DATA 会签）：① 读合并按主表 ② impact 双 VID 口径=经主表 union 后计数 ③ 新建查重扫主表不扫存量图（图内重复点主源=主表）④ auto 层 Job 撞存量名称 VID：写前经**主表名称/external_ids(legacy_vid) 映射**解析（非 redirect——D6 首版不做 redirect，三分册会签 DATA-A2 更正），撞不上则新点（后续 Job 单详化）
- Demo：demo_gkx_chain 同构（注：本节「D6」指 VID 交叉点序号，非决策项 D6——三分册会签 N2 澄清；Nebula space 名经配置项注入可切正式/demo，实现单落）

## 4. 事务与补偿（沿 ARCH §1，存储侧含义）

发布序列（三分册会签 ARCH-A4 锁定）：**MySQL（主表+version+change_log）先提交 → Nebula 投影 → ADS 投影最后**（原稿 ADS 随 MySQL 先提交系与 ARCH 矛盾，已对齐 ARCH 版：ADS/Nebula 同段失败同补偿，R2 恒读上一已发布版，无 pending 版过滤问题）；Nebula/ADS 失败 → version.projection_status=pending + 补偿重放。不做跨库分布式事务。

## 5. 不做

- 不建 cfg_* 表；不写 ODS/供应方库；不灌数不跑脚本（DDL 归实现单，写者 Python）
- 不做 redirect/合并后端（D6）；不做 conflicts 业务逻辑（表建逻辑空）
- 不做挂接状态表（三分册会签 DATA-A3 裁：hang 状态由边存在性+change_log 表达，不另建表——entan graph_membership 先例不采）；不动存量 Nebula VID；不替 DN-07/DN-A03-02/03/06 拍板
- Java 零写以上任何表（只读 §2 投影）

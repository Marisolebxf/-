# 派单包：宏观行业要素库 live 调研

- **状态**：2026-09-02 `human:淮政玮` 口头「把这个作为调研任务，指派给王惠」已收
- **派发角色**：coordinator-agent
- **承接 / Owner**：`human:王惠`（口径 / 指标可用性；人自己调研）
- **协作咨询**：公式 / 算法怎么用 → `human:唐绍祖`（本叶不改算法仓）
- **仓**：`gkx-orchestration`
- **Epic**：`E-PLATFORM-P1`
- **Sprint**：`2026-W36`
- **task-id**：`DATA-MACRO-LIVE-VERIFY-L01`
- **强度**：definition / spike，**禁止** ponytail 行

---

## 0. 已拍板（勿再议）

| # | 决策 | 值 |
|---|------|-----|
| 1 | 本叶性质 | **调研**：看六张表里装了什么、能否挂政策/产业指标。不是建 GDF 包，不是 COPY DWD 落库 |
| 2 | 结构策略（后续叶） | 项目 DWD **建议完全 copy** 入站现表；本叶只出对照结论，**不对** `gkxlumenx_dwd` `CREATE/ALTER` |
| 3 | 入站表名 | 以 2026-09-02 重抽 Excel 为准，英表已带 `dwd_` |
| 4 | 工作面 | 三方 MySQL `gkx` @ `183.240.141.251:3318` 只读；取数默认 `is_deleted=0` |
| 5 | 禁止 | 改 `cfg_metric-*-seed.yaml` / 就绪度矩阵；编造 GDF Mapping；把 `ods_*` 当正式输入 |

## 1. 六表（Excel = live 现表名）

| # | 中文 | live 表 | 2026-09-02 12:49 抽检（全表=业务行） | 建表时间 |
|---|---|---|---:|---|
| 1 | 数据表 | `dwd_macro_index_data` | 20,000 | 2026-09-01 15:41 |
| 2 | 指标属性表 | `dwd_dim_index_attribute` | 867 | 2026-09-01 15:37 |
| 3 | 区划表 | `dwd_dim_admin_area` | 20,000 | 2026-09-01 15:37 |
| 4 | 计算维度表 | `dwd_dim_index_cal` | 3 | 2026-09-01 15:37 |
| 5 | 时间维度表 | `dwd_dim_index_dur` | 7 | 2026-09-01 15:37 |
| 6 | 数据来源表 | `dwd_dim_source_code` | 4 | 2026-09-01 15:37 |

Excel 业务列 live **齐**；每表另多 9 个供应方技术字段（`dwd_id` + 六技术字段 + `operator_remarks` / `insert_remark`）。物理主键 live = `dwd_id`，不是 Excel 标的联合主键。

预备抽检 JSON：`data/third-party-source/gkx-mysql-raw/加工/_probe_macro_live.json`（可复跑 `_probe_macro_live.py`）。

## 2. 预备抽检（给王惠起手，须复核）

事实表像 **2 万行样例封顶**（区划表同），不是全量国统库。字典 867 条更像完整目录。

**事实里高频指标（行数）**：社零 2316、固投 1953、出口 1936、规上工业增加值 1893、进出口 1801、GDP 1136、二产/一产/三产增加值。期界 `194912`–`202606`，431 个数据期；287 个 `index_code` 出现在事实里（字典 867，多数指标本批无事实行）。

**维表枚举**

- 计算：`JDZ` 绝对值、`TB` 可比同比%、`HB` 环比%（事实只用了 JDZ 12494 + TB 7506，无 HB）
- 时间：`DNLJ` 当年累计为主，另有期末/当月/当季
- 来源：事实以 `LBS` 本地统计局 14528 为主，其次世界银行 / 国家统计局 / 海关

**字典里和产业相关的名字**（样例）：新一代电子信息 / 数字与时尚 / 生物医药 / 半导体与集成电路 / 智能网联汽车 / 人工智能 / 低空经济与空天 **产业增加值**。`index_name` 含「产业」38、「专利」42、「GDP」16；**「政策」「科创」「研发」「深圳」= 0**。

**质量（必须写进调研笔记，勿当口误滑过）**

| 现象 | 抽检 |
|---|---|
| 事实 `area_code` 与区划 `cur_code` 对不上 | 20000 行里 18986 行 JOIN 失败 |
| 事实 `area_code` 样例 | `0086` / `440300000000`（深圳码）/ `EU` / `840` 混在一起；LIKE 中文「深圳」= 0 行 |
| `dim_cal`/`dim_dur`/`source_code` | 事实存 **代码**（JDZ/DNLJ/LBS），Excel 样例写的是中文名 |
| `area_code_type` | 文档值域 1/2/3；live 出现 **4**（132 行） |
| 区划层级 | 社区 18407 / 街道 1447 / 区县 120…像街道社区样例切片；广东 889 行，深圳只见到街道级 |

## 3. 调研要回答的问题

1. 这 867 个 `index_code` 里，哪些能直接当政策效果「实施前后关键指标」、哪些能当区域产业指数/周期的官方分母？
2. 产业链码 / 申万 / 国统 / 这套 `a71xxx` 产业增加值，对得上我们对哪几条链？对不上的登记决策清单，**不替甲方拍板**。
3. 区划用 `cur_code` 12 位还是事实里的杂糅 `area_code`？政策 `city` 文本怎么对齐深圳？
4. 2 万封顶是否够试点？不够 → 向供应方要全量（另开三方问题，本叶只登记）。

建议先圈的 metric（可增不可散扫 560 条）：

- 政策：`M_POLICY_DEEP_168_1`、`M_POLICY_EFFECT_SCORE`、`M_POLICY_IMPLEMENTATION_EFFECT`、`M_POLICY_INDUSTRY_FIT`、`M_POLICY_INDUSTRY_COVERAGE`
- 产业：`M_CHAIN_COMPETITIVENESS_INDEX`、`M_CHAIN_REGION_INDEX`、`M_CHAIN_CYCLE_STAGE`
- 综合：`M_SYNTH_185_1`

## 4. 必读

| 序 | 路径 |
|---:|---|
| 1 | `data/third-party-source/doc/md-extract/市场研究（金融、宏观行业、行业分析、产业链）数据汇总表.md` §宏观行业要素库 |
| 2 | `data/third-party-source/gkx-mysql-raw/CONNECTION.md` + `加工/SUPPLIER-WORK-CONSTRAINTS.md` |
| 3 | `data/third-party-source/gkx-mysql-raw/加工/_probe_macro_live.json` |
| 4 | 并列切片（不要糊）：`data/data-design/storage/CHAIN/sources/inventory-industry-analysis.md`（行业分析是研报六表，不是本库） |
| 5 | `data-lineage-policy.md` |
| 6 | `客户决策清单跟踪表.md` |

连库：`gkx-mysql-raw/.env.local`（只读）。**禁止打印密码。**

## 5. `/goal`（王惠本机；人主导，agent 仅助查）

```
/goal DATA-MACRO-LIVE-VERIFY-L01
监管人：human:王惠
仓：gkx-orchestration
范围：调研 gkx live 宏观行业 6 表内容与政策/产业指标可挂性；写调研笔记 + 对照表 + 决策清单开放项。
禁止：改 seed/matrix；建 GDF 包；对正式 DWD APPLY；把行业分析 documents 六表并进本叶。
DoD：见 registry。
```

定义类，**不要**写 ponytail 强度行。

## 6. 验收对照

- 六表「装了什么」有人话结论，不是只贴 COUNT
- 对照表至少覆盖 §3 点名的 metric
- 质量五条有登记；该进决策清单的已进
- handoff 含认领字段、ponytail=N/A、架构合规、cost 四字段

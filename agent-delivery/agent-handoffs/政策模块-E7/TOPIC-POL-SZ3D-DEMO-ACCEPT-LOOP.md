# TOPIC-POL-SZ3D-DEMO-ACCEPT-LOOP · 深圳政策现状演示实例反复验收

## 任务认领

| 字段 | 值 |
|---|---|
| claimed_by | `agent:qa-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |
| 说明 | 2026-11-07 第一轮探测后，监管人裁定档位和落地实效没有结果不算通过。验收单仍留在 `ready`，不签完成。 |

## Ponytail

| 字段 | 值 |
|---|---|
| ponytail | `N/A` |
| 说明 | 本轮只读接口和库，没有改业务代码。 |

## 图

本轮不改调用链，没有图。

## 运行 2026-11-07

- 用例真源：`agent-delivery/agent-handoffs/政策模块-E7/LUMEN-POLICY-SZ3D-DATA-DEMO-L01.md`
- 锚点：`industry_vid=chain:INB1303`
- 库：只读 `demo_gkxlumenx_dwd.policy_base_info`。未删除行 20008；`city='深圳市'` 879；这 879 行的 `rank` 都有值；无城市名 9713
- 样本满足：否（2026-11-07 监管人裁定：扶持档位、落地实效没有结果，不能算通过。下面「运行 2026-11-07 第二轮」是按这个裁定补上的）
- 停止：继续
- 探测：`GET http://10.50.69.111:30892/api/topicAsync/topic/v1/analysis/tasks/POLICY-20261107-004/result`。不带 `user_id` 时 HTTP 200、`code=1`、`msg=未获取到当前用户`。按结果接口的实际参数加上 `user_id=guest` 后 HTTP 200、`code=0`，任务状态 `success`。没有新签发任务
- 结果：支持力度可算；条数 879；分数 33.5585；名次 5；层级均值 0.4653；档位原因「无金额列」，分值空。第 4 章不可算，原因「实施日、支持对象、反馈全缺」。第 5 章有供给结构，条数与分数同上。`honesty.source=dwd`，`fabricated=false`
- 第 3 章仍是「未提供链名」。留在缺陷包 `LUMEN-POLICY-SZ3D-E1-DEFECT-C1.md`，本轮不建查询单
- 子任务：见第二轮。本段只记录探测结果，裁定后改为不通过

### 缺口

| 缺口键 | 类 | 现况 | 预期 | 建议 | 挂到任务 |
|---|---|---|---|---|---|
| `policy_base_info.support.tier` | DATA | 档位值为空，原因「无金额列」 | 有结果，且不是把空写成 0 | 先核对政策表有没有非空金额或档位；没有则不能造 | `TOPIC-POL-SZ3D-DEMO-FIX-R20261107-DATA` |
| `policy_base_info.effect` | DATA | 第 4 章不可算，原因「实施日、支持对象、反馈全缺」 | 可算并有结果，且不是 0 分充数 | 先核对实施日、支持对象、反馈有没有非空源；三维都空则分数无定义 | `TOPIC-POL-SZ3D-DEMO-FIX-R20261107-DATA` |
| `shenzhen_board.tier_effect` | ALGO | 结果板不读金额、不取落地实效，原因写死 | 源列已有非空值时要按列算；源列全空时仍不可算，不得出 0 | 本轮源列没有非空值，不改公式出假分 | `TOPIC-POL-SZ3D-DEMO-FIX-R20261107-ALGO` |

## 运行 2026-11-07 第二轮

- 用例：`agent-delivery/工程过程/04-系统集成/03-专题系统集成/编排计划/深圳政策现状分析-LOOP计划.md` 第 1 节（裁定后的通过线）
- 库：本轮没有再连上 `10.50.11.76`（连接超时）。现况以已签发结果和口径说明为准：`metrics/calc-logic/POLICY/M_POLICY_SUPPORT_STRENGTH.md`、`metrics/calc-logic/POLICY/M_POLICY_IMPLEMENTATION_EFFECT.md`
- 样本满足：否
- 停止：重复缺口
- 子任务已建。数据单做了源核对，没有改库。算法单核对了结果板，没有改代码。没有把空写成 0
- 口径说明：政策表没有金额列，`policy_support` 全空；实施日是零日期，支持对象取不到，两库没有反馈表。三维都空时分数无定义。强行出 0 会把缺数写成政策事实
- 数据单 `TOPIC-POL-SZ3D-DEMO-FIX-R20261107-DATA` 因此停在阻塞：没有可回填的非空源。算法单 `TOPIC-POL-SZ3D-DEMO-FIX-R20261107-ALGO` 停在待签收：源列全空时改公式也出不了数
- 不重读 `POLICY-20261107-004`。库和代码都没变，结果不会变
- 同一缺口键还在。本轮不再新建第三张单。要在演示里出现数字，只能另建带 mock 标签的缺项表并让结果板去读，不能写进 `policy_base_info`。这一步等 `human:淮政玮` 点头

### 缺口

| 缺口键 | 类 | 现况 | 预期 | 建议 | 挂到任务 |
|---|---|---|---|---|---|
| `policy_base_info.support.tier` | DATA | 仍无金额源 | 有结果，不写 0 | 等监管人决定是否另开有标签的演示缺项表。不写进 `policy_base_info` | 已挂数据单，不新建 |
| `policy_base_info.effect` | DATA | 实施日、支持对象、反馈仍全缺 | 可算并有结果，不写 0 | 同上 | 已挂数据单，不新建 |

## 运行 2026-11-07 第三轮

- 用例：`agent-delivery/工程过程/04-系统集成/03-专题系统集成/合规演示用例/深圳政策现状分析-合规演示用例.md`
- 库：本轮没有再写库。金额、施行日、适用对象沿用此前写入 demo 的结果
- 样本满足：否
- 停止：继续。缺的是报告第 4 章，不是再补一版金额或实效
- 探测：`POLICY-20261107-004` 仍是旧结果。支持力度 879 / 33.5585 / 名次 5 / 层级均值 0.4653。档位原因「无金额列」。落地实效不可算
- 重算：当天同一指纹会复用 004，所以另签发 `POLICY-20261107-009`（`force=true`，`reused=false`，状态 success）。验收 GET 本身没有带 force。此后验收改读 009
- 009 结果卡：支持力度四个数不变。档位 `4`，原因「截面金额均值临时分位，QPOL-02」。落地实效 `computable=true`，`score=50`。不是 0。产业适配性仍是「未提供链名」，不建单
- 009 报告：第 2 章有档位 4。第 5 章有供给结构，数字同上。第 4 章仍只写「不可算」
- 原因：`PolicyShenzhenSnapshot.effectLines` 不看可算状态，固定印「不可算」。结果卡已经有分。本地已改成可算且分数不是 0 时印「分数 …」。本机 Maven 3.6.0 跑不了该模块测试，改动未推，线上第 4 章还不会变
- 不新建数据单，不新建算法单。不签完成

### 缺口

| 缺口键 | 类 | 现况 | 预期 | 建议 | 挂到任务 |
|---|---|---|---|---|---|
| `report_chapters.effect` | ALGO | 009 的落地实效卡是 50，报告第 4 章仍是「不可算」 | 第 4 章写出分数 50，不写「不可算」，也不写 0 | 等报告抽取改动发布后再读新任务。009 本身不会变 | 本地改动，未建新单 |

## 运行 2026-11-07 第四轮

- 用例：`agent-delivery/工程过程/04-系统集成/03-专题系统集成/合规演示用例/深圳政策现状分析-合规演示用例.md`
- 库：本轮没有写库
- 样本满足：否。接口已有结果，页面还没显示
- 停止：继续。不新建数据单，不新建算法单。不是同一条空源缺口再出现
- 探测：`POLICY-20261107-011`，`user_id=guest`，HTTP 200，`code=0`，状态 success。对象是技术领域「人工智能」
- 011 结果卡：支持力度 879 / 33.5585 / 名次 5 / 层级均值 0.4653。档位 `4`，原因「截面金额均值临时分位，QPOL-02」。落地实效 `computable=true`，`score=50`。适配性分数 9.245，命中 43，锚点「智能网联汽车、人工智能」
- 页面：结果板不读档位值和实效分数，两处都印「不可算」。空原因时还套上「实施日、支持对象、反馈全缺」
- 改动：`lumen-ui-topic` 的结果板、报告块和解析。可算且分数不是 0 时印分数；档位有值时印档位。0 和空分仍印不可算。自检 `policyShenzhen.selfcheck.mjs` 通过。改动停在本地，未推
- 不签完成

## 运行 2026-11-08 凌晨（第 009/011 口令更新后探测的下一轮）

- 口令：本轮从本机文件读取，为用户当次新给的值。两笔 GET 200，`code=0`，状态 success，头 `systemCode: topic`、参数 `user_id=guest`。没带 force，没 POST，没新签发
- 009：支持力度 879 / 33.5585 / 名次 5 / 层级均值 0.4653；档位 `4`（QPOL-02）；落地实效 `computable=true, score=50`；适配性「未提供链名」（结果卡 `anchor_name` 空），strategies 只有供给结构。结果时间是 16:01
- 011：同上四项；适配性 9.245 / 命中 43 / 锚点「智能网联汽车、人工智能」；strategies 有供给结构和产业适配。结果时间是 16:44
- 结果载荷位置变化：`data.resultData` 现在是空，业务载荷整体搬进了 `data.targetParams.result_payload`（结果资产 `res-POLICY-…` 指针）。前端 `readAnalysisResultPayload` 本来就走 `targetParams.result_payload` 兜底，页面不受影响；本轮探测脚本同步改读了这里
- 库核对红：`demo_gkxlumenx_dwd.policy_base_info` 里 `city='深圳市'` 现在 1458 行（预期 879），按 `_LEVEL_W` 均值 0.3873（预期 0.4653）。构成：原生 879（rank 分布未动）+ 一张图 debug 540（`debug_one_map_20261107_v1`，区县级，SYSINT-04-01 灌）+ 图2 合成 49（`SYNTH-*`，D16 例外已批，检索统计计入）。另有约 9667 行原生行被别的会话做了城市回填（无城市名 9713→46），下次重算 score 33.5585 / 名次 5 也会漂
- 结果仍绿是因为 009/011 是 16:01 / 16:44 的旧基线快照；下次任何重算都会红
- 处置：数据侧不可修——删 debug 540 破坏一张图演示，删 SYNTH 49 破坏图2 演示并违背已批 D16 例外，隔离/改 city 同样破坏读取。按第 4 节建 `TOPIC-POL-SZ3D-DEMO-FIX-R20261108-DATA`（`agent-agent` 调查后 `blocked`），等 `human:淮政玮` 拍板读取口径：方案 A = 结果板 SQL 加原生过滤（转 ALGO 单 + LOOP §1 口径修订）；方案 B = 放宽通过线为动态基线
- 已上线确认（本轮顺带核对 origin/dev）：Java 报告第 4 章改动 `3a2c3c7`（16:08）已推；前端指标勾选 `6acb245`→`40c09b3/7973080/6321146`、去 Mock 角标 `cf304e0`（23:23）已推；报告仪表盘（需规 116）和三维柱状图已在前端 `6321146`。前端任务 `LUMEN-POLICY-SZ3D-FE-SRS-R20261107` 仍 `in_progress`（工单 note 说明已推 6acb245）
- 样本满足：否（库核对红）
- 停止：新缺口已建单并 blocked 等人拍板，不是连续两轮同键（上一轮同键是「档位/实效无结果」，已闭合；本轮是「共表演示数据混入截面」，新键）

### 缺口

| 缺口键 | 类 | 现况 | 预期 | 建议 | 挂到任务 |
|---|---|---|---|---|---|
| `policy_base_info.city_section.scope` | DATA→口径 | 深圳市行 1458、均值 0.3873；一张图 debug 540 + 图2 SYNTH 49 混入；~9667 行被城市回填 | 879 / 0.4653 稳定复现，且不破坏一张图、图2 演示 | 方案 A：board SQL 加原生过滤（`source_plane='domestic' AND etl_batch_id IS NULL`），同步修订 LOOP §1 库核对口径；方案 B：通过线改动态基线。等 `human:淮政玮` 拍板 | `TOPIC-POL-SZ3D-DEMO-FIX-R20261108-DATA`（blocked） |

## 运行 2026-11-08 02:44（方案 A 上线后重签轮）

- 用例：`agent-delivery/工程过程/04-系统集成/03-专题系统集成/合规演示用例/深圳政策现状分析-合规演示用例.md`
- 库：本轮没有写库。DB 直查受限（10.50.75.136 跳板机无 mysql 客户端，3306 端口通；按 SSH 熔断规则停止找客户端），截面读数以算法 `diagnostics` 实读为证
- 样本满足：是（接口全绿；本轮起验收入口改读新号）
- 停止：继续。本轮无新缺口，无新建单
- 部署：`lumen-algo-py` `4df6ab5`（`CITY_SECTION_SQL` 原生过滤：`COALESCE(source_plane,'')='domestic' AND etl_batch_id IS NULL`）CI 流水线 4280 全绿，`deploy:entan-api` success，新算法已上线
- 重签：旧 `targetParams` 冻结体只剩展示件（frozen_cards/report_chapters），锚点键被覆写，原样重放会撞 `VALIDATION_OBJECT_XOR`；按总控「接口事实必须保留」重建创建体，沿用原指纹 + `force=true`，`reused=false`
  - `POLICY-20261108-009`（产业：`industry_id=INB1303` + `industry_vid=chain:INB1303`，指纹 86977506…1b714）
  - `POLICY-20261108-010`（技术领域组合：`scope_kind=industry` + `industry_codes=[INB1209,INB1309]` + `industry_name=智能网联汽车、人工智能`，指纹 a64bc063…f4417）
- 探测（两条 `success`，`honesty.source=dwd, degraded=false, fabricated=false`）：
  - 支持力度：879 / 33.5585 / 名次 5 / 层级均值 0.4653 / spearman 0.9467 —— 原生过滤生效（count 是 879 不是 1458），`city_rows=10295`、`city_null_rows=9712` 与基线一致，城市回填未漂移截面
  - 档位：`value=4`，原因「截面金额均值临时分位，QPOL-02」
  - 落地实效：`computable=true`，`score=72.7658` —— `EFFECT-READ` 公式已接通 gapfill 缺项行实算（此前占位基线 50 退役；计划 §1 同步改口径）
  - 009 适配性：「未提供链名」（anchor_name 空），不建单
  - 010 适配性：9.245 / 43 / 锚点「智能网联汽车、人工智能」
  - 报告：第 4 章印「分数 72.7658」不再是「不可算」；第 5 章 009 有供给结构、010 有供给结构+锚点适配
- 计划修订：`深圳政策现状分析-LOOP计划.md` 状态行、§1 通过线（探测号/落地实效 72.7658/第 4 章）、§3 调用表、§4「旧章节」条款已改读新号
- 验收单：保持 `ready`，不签完成

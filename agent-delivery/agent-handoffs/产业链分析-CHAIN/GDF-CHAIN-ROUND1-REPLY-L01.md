# GDF-CHAIN-ROUND1-REPLY-L01 · 产业链包 v2 round1 核对签收与 20 题答复

> 交付日期：2026-11-02 · 监管：`human:徐滕强`

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:徐滕强` |
| claim_type | `pull`（GDF round1 落盘后徐滕强指示处理，参照政策 round1 回复模式） |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `off`（派单文档修订与答复类任务，参照 GDF-POLICY-ROUND1-REPLY-L01 同口径） |

## 1. 范围与实现

**触发**：GDF round1 核对（落盘提交 `2972be90`，01 核对报告判定不能开工 + 02 提问清单 20 题）。

### 逐题答复落点（对照 02-提问清单编号）

| 组 | 题 | 结论（均经徐滕强拍板） | 落点 |
|---|---|---|---|
| 链树分层 | 1~3 | 12 根链 8 层确认；链表=L0+L1（53 行）、节点表=L2~L7（1,220 行）；`chain_tier` 8 级 | `09`§3.1/3.2 重写 |
| 主键父级 | 4~6 | 主键改 `industry_code`；父级=直接父级码（`industry_link_code`），不跳级；名称=`industry_name`；`level` 列禁用；`parent_name`（层级 0..7）作判定源 | `09`§3.1/3.2 重写 |
| 企业挂接 | 7 | 口径待 ODS 补灌后命中率重测（双方 round1 数字均不采信）；不阻塞 A/B1 | `09`§3.4 + `23`§2 问 7 |
| 后加工接口 | 8~13 | 五项（上图/rebuild 契约、点数稳定、图空间名）打包架构师确认，round2 补 `12`；跳过写 `skip` 已定 | `12` v2.2 修订 |
| DDL 真源 | 14 | `10/dwd-chain.md` 复制件为唯一真源（库名全局改正式库）；v5 作废；旧 `链树四表.md` 删除 | `10/` 重构 |
| 抽取方式 | 15 | 四张链表全量+清空重灌（先例：本轮已执行）；季度比对兜底；行数+码集对账 | `23`§2 问 15 |
| `sort_no` | 16 | 同链按 `industry_code` 升序序号 | `09`§3.2 |
| `future_industry_flag` | 17 | 按簇表 `industry_cluster_map` fut 组派生（6 条根链），弃 INB13 前缀 | `09`§3.1 |
| `stage_code` | 18 | 采用三等分（余数归 upstream），不置 NULL | `09`§3.2 |
| 脏值 | 19 | 单引号列表字面量解析；`[]` 与中文路径/异常信用码行进治理清单 | `09`§3.4 |
| 分析六表 1,000 行 | 20 | ODS 同步作业 LIMIT 缺陷非抽样；补灌后重贴 | `23`§2 问 20 |

### 附带完成

- **码表一次性修数同步（架构师新规下唯一例外通道，徐滕强拍板）**：`industry_cluster`(15) / `industry_cluster_map`(15，INB13 码系替换旧 50 行 INB17/18 死码) / `industry_chain`(53) / `industry_chain_node`(1,220) / `subfield_topic_map`(390)，demo→lumen 单向，已终验；`gapfill_chain_market_size` 不同步（造数）。
- **正式库链树两表清空重灌**：修复口径错误（链表曾混入 L2~L7 共 1,273 行）。
- **环境红线写入包**（`23`§1 + README）：GDF 只读真源 `gkx` + `gkxlumenx_*`，禁读 demo；数据旧以真源为准施工、业务问题咨询我方。
- **collation 注意项**（`23`§4）：`gkxlumenx_dwd`(0900_ai_ci) × `gkxlumenx_dim`(general_ci) 跨库 JOIN 需显式 CONVERT。

## 2. 偏离说明

- 政策 round1 模式中「逐函数对照签收」不适用本轮（GDF 交的是核对报告不是脚本），改为「五环节判定逐条复核签收 + 20 题有问必答」。
- 问 7/8~13 未闭环：前者等数据（ODS 补灌），后者等人（架构师）——按规约未由人拍板项不代答，标注待定与去向。

## 3. 产物清单

| 产物 | 位置 |
|---|---|
| 23-核对签收与答复.md（新增） | `data/GDF/派单包/产业链/GDF-CHAIN-WORKPACK-v2/` |
| 09 v2.2（§3.1~3.4 重写 + 开放项更新） | 同上 |
| 10/dwd-chain.md（新增复制件）+ README 重写（删链树四表.md） | 同上 |
| 12 v2.2 修订 | 同上 |
| CHANGELOG v2.2 / README v2.2 | 同上 |
| 数据库变更 | `gkxlumenx_dim` 3 表同步；`gkxlumenx_dwd` 链树两表重灌（均有 rollback 快照） |
| git commit | 本单随验随推 `origin/dev` |

## 4. 验收证据

- 真源列语义实测：1,273 行 `level` 全 0；`industry_code` 唯一；码长×层级交叉零例外（8 组全单调）
- 同步终验：5 表 demo vs lumen 行数一致（15/15/53/1,220/390）；链表 L≥2 = 0 行、节点表 L<2 = 0 行；簇挂接 JOIN 66 次命中（含政策一簇多挂）
- demo 复制件 `dwd-chain.md`：`demo` 残留仅 2 处叙述性文字，`demo_gkxlumenx_dwd` 零残留
- 09 新旧对照：`level∈{0,1}` 分表写法零残留（grep 验证）

## 5. 架构合规自检

| 铁律 | 状态 |
|---|---|
| D12 demo/lumen 隔离 | ✅ 本轮主线正是落实新规：禁 GDF 读 demo；码表同步为我方一次性修数通道；`12` 占位图空间标注禁施工 |
| 调用链 | ✅ 未变更；12 的「GDF 不执行建库写入」重申 |
| 数据流单向 | ✅ 真源→ODS→DWD；demo→lumen 仅码表例外且记录在案 |
| D9/指标 | ✅ 不涉及页面指标；链表为数据底座 |

## 6. 遗留与移交

| 项 | 去向 |
|---|---|
| tags 全量贴源与命中率重测 → 问 7 口径 | GDF Wave A 开工即完成（贴源=灌数，约 228 万行）；命中率随对账回执产出（2026-11-02 徐滕强纠正：灌 ODS 是 GDF 的活，我方不代灌） |
| 图空间名 / 上图与 rebuild 契约 / 点数稳定 → `12` round2 补 | 架构师（已打包提交 2026-11-02） |
| 簇表 8 个 INB 一簇多挂 | 客户决策清单 🟡（不影响 flag 派生） |
| collation 统一与否 | 架构师另行拍板；暂按 `23`§4 写法施工 |
| 工单 `GDF-CHAIN-ROUND1-REPLY-L01` 建单 | task-registry MCP `task-create` 服务端 `effort_points` 校验异常，请 coordinator 代建（参数见本 handoff §1 与 git commit） |

## cost

| 字段 | 值 |
|---|---|
| ponytail | `off` |
| model_used | `glm-5.3-Flash` |
| actual_tokens | 80000 |
| actual_cost | 5 |
| cost_warn | `green` |

---

## 8. round2 契约补全追加（2026-11-02 晚，任务 GDF-CHAIN-ROUND2-CONTRACT-L01）

徐滕强三项拍板/确认落地：

| 项 | 结论 | 落点 |
|---|---|---|
| 图空间名 | `gkx_chain`（demo 名去前缀） | `12` 全文替换（占位名零残留）；`23` 问 13 已答复 |
| 上图/rebuild 契约 | 从 `lumen-algo-py` 源码考古获得：上图 `POST /internal/v1/chain/graph/project`（回执 status/vertex_counts/edges_written/industry_index/...）；rebuild `POST /internal/industry/embed/rebuild`（code/data.indexed/index_version）；`index_version`=yyyyMMddHHmmss | `12` 新增 §5.1~5.2 |
| 点数稳定判定 | 四连判（读表无错/点数>0/写入≥锚点/词表非空）经现网推演合理（1273=53+1220 贴合）；两条边界写入（只防丢点不防多点；entity_rel 0 行为预期态） | `12`§5.3 |

- 正式图谱由 GDF 专门代码读写；我方代码 demo 闸门（assert_demo_nebula_space / FORMAL_SPACE 常量）**不进 GDF 契约**，其正式化改造属 algo 域另派。
- `23` 问 8~13 改「已答复」；开工判定 `12` 后加工 → **可起草**；09 OPEN-CHAIN-FLOW-02 关闭；CHANGELOG v2.2.1。
- 20 题至此全部闭环（问 7 随 GDF Wave A 贴满 tags 表后按真实命中率定口径；我方无代灌待办——2026-11-02 徐滕强澄清：灌正式 ODS 是 GDF 的活，demo 贴源单 CHAIN-ODS-SYNC-L01 保持原用途不动）。
- 淮政玮确认五项已定、lumen 空间 `gkx_chain`。12 文首、第 1 节警告和 23 遗留表残留句已改齐。

---

## 9. round2 全问闭环追加（2026-11-03，任务 GDF-CHAIN-ROUND2-REPLY-L02）

> 流程更正：round2 收口时曾两处违规（11 问只拍 2 题即代答其余；未建单先动文档），徐滕强指出后本单补建并逐题补拍。前一笔 051ba72a 含未拍板内容已按最终拍板全面修正覆盖。

| 问 | 拍板（均徐滕强） | 落点 |
|---|---|---|
| 1~3 链树 | chain_id=所属 L1 链 + parent_node_id 直接父级 + 真父子边 1,055 条（先前已确认） | 09 v2.3 |
| 4 stage_code | **维持三等分派生**（1-4/5-8/9+）；排序含义 🟡 登记待供应方确认，不符则重算刷新 | 09§3.0 + OPEN-CHAIN-MAP-01 + 23§8 |
| 5~8 原子接口 | **转架构师确认**（数据侧不代答引擎能力）；幂等基线语义先行承诺；definition_id 催燕大进包 | 23§8 |
| 9~10 参数化 | **路线 A**：脚本环境变量全量化 + 依赖内联，交付即运行；**徐滕强本人改脚本**（不另派 algo；误建单已撤销） | 23§8 |
| 11 _SPACE_OK | 口径澄清（demo 域实现不进 GDF DAG） | 23§8 |
| 附注三处不一致 | 02 tags 解析写法 / CHANGELOG v2.2 flag 表述 / 12§5.1 JSON 定位——均已修 | 各文件 |

**round2 提问清单 11 问全部闭环。** CHANGELOG v2.3.1。

## cost

| 字段 | 值 |
|---|---|
| ponytail | `off`（派单文档修订类） |
| model_used | `glm-5.3-Flash` |
| actual_tokens | 60000 |
| actual_cost | 4 |
| cost_warn | `green` |

---

## 10. 问 7 口径拍板追加（2026-11-03 16:20，徐滕强）

**拍板：链上企业挂接业务口径 = 全量全国，不存在「只做广东」选项。** 不得以样例匹配率定业务范围——PoC 阶段样例匹配不上属正常现象，非业务范围证据。

落点：`23`§8 问 7 / `09`§3.4 / OPEN-CHAIN-MAP-07 三处已改。执行规则不变（命中才写 org_id、对不上不伪造），未命中行进治理清单待企业主档扩展后**二次挂接**——丢弃≠放弃，不缩小业务范围。round1 各方命中率数字（85%/15%/2%）均记为样例期参考值。

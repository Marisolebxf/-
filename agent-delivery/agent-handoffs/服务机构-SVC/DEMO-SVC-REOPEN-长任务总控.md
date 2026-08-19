# 服务机构施工 · 阶段 F（底座）长任务总控（已授权）

> **日期**：2026-08-19  
> **拍板**：`human:淮政玮`（微信 · 2026-08-19）  
> **授权 / 本管线监管**：`human:侯佳伟`（后续认领 **不必再问**）  
> **签收**：`ready_to_sign → done` 仍是 `human:淮政玮`（chore 豁免）  
> **范围**：**只阶段 F（底座）**。禁止写「F 绿自动续 P」。50892 产品段另开总控、另授权。  
> **前置**：范围 3 停机已完成（`DEMO-SVC-ABORT-L01` = done）  
> **升格自**：[`DEMO-SVC-REOPEN-开工方案.md`](./DEMO-SVC-REOPEN-开工方案.md) v0.2（该文件现为指针）  
> **转交**：[`DEMO-SVC-停机转交-侯佳伟.md`](./DEMO-SVC-停机转交-侯佳伟.md)  
> **规约**：[`长任务执行规约.md`](../../长任务执行规约.md) v1.13 · **禁止 force**  
> **锁**：`lock_hours=24` · `claim_type=coordinator_dispatch` · `supervised_by=human:侯佳伟`

---

## 0. 授权句（本机落盘 · 2026-08-19）

> 授权：`human:侯佳伟`。`human:淮政玮` 2026-08-19 同意按开工方案 §9 先开阶段 F（底座）。  
> 按本总控重建 `storage/SVC` S1–S4；再在 50100 产业服务算法库恢复灌数并接到 `demo_gkxlumenx_*`；图谱与十模型按契约表出数回写；算法未定稿则移植 30999 产业服务链分析（`service-center`）示例算法，禁止用产业链 `industry-center`。  
> **总控范围写死阶段 F。** 底座退出门绿之前不开 50892 产品段；**禁止**本总控写「F 绿自动续 P」。阶段 F 内 **不要碰** `lumen-topic-py` / `lumen-algo-py` / `lumen-svc-platform` / `lumen-ui-topic`。  
> 短板阈值（Demo）用已评审原型（0 家空白 / ≤1 薄弱 / 均深&lt;55 瓶颈），挂 **Q-SVCCHAIN-03**；Q061 只作对照列 + `pending_client`，F-ALGO 运行时不要切过去。  
> 全部新 ID。后续认领不必再问聊天。禁止 force。签收仍 `human:淮政玮`。

S1 会签前 **禁止** 建 F-SEED / 十模型叶。本总控 push 之前曾禁止建叶（已满足）。

---

## 0.1 一句话

先把 **50100 Demo 底座**做齐：契约流图会签 → 灌数 → 基础指标 / 图谱 / 十模型从设计表出数回写。  
**不是**复活旧 A，**不是** 50892 产品长任务，**不是** 50100 继续吃前端 Mock。CHAIN 不动。

---

## 0.2 三站不要混

| 站 | URL | 本总控 |
|----|-----|--------|
| **50100 产业服务算法库** | http://111.198.38.90:50100/ | **主战场**（灌数 + 出数） |
| **50892 专题** | http://111.198.38.90:50892/ | **本总控禁止施工** |
| **30999 原型** | https://skxdemo.unicomcn.tech:30999/ | 只读；代理算法只搬 **`/service-center/*`** |

`/industry-center/overview` = 产业链（CHAIN），禁止当 SVC 算法来源。

---

## 1. 已拍板（不回问）

| # | 项 | 决定 |
|---|-----|------|
| 1 | 库 | 只写 `demo_gkxlumenx_*`；禁正式 `gkxlumenx_*` |
| 2 | ODS | 共用现有 `demo_gkxlumenx_ods`，不新建 ODS 实例；禁 DROP 33 张约定表 |
| 3 | 抽取 | 主路径 = ODS → SVC DWD（`entan.svcseed` 升主）；禁 `SELECT enterprise_*`；禁复制 `dwd_org_base_info` 全列 |
| 4 | 圈定 | Demo 临时规则 `svc_rule_demo_kw_v1`（`name_cn` + `industry_l*_name`） |
| 5 | 主体 | 机构权威在 ENT；禁止 SVC 平行 `svc_org_base`；hang `org_id` |
| 6 | fixture | 24 家 `seed_svc_demo_mock.py` **旁路**，不得当底座退出门 |
| 7 | 🟡 | Q-SVC-010 / Q060 / Q062 / Q063 / Q-SVCCHAIN-03：不伪闭合 live；UI「待核验」 |
| 8 | 调用链（F） | 50100 沿 ENT 算法台惯例直连 `demo-algo-ent-analysis` `/entan/internal/svc/*`，只读写 Demo 库。产品站调用链留给 **P 总控** |
| 9 | 共用仓 | 只动 SVC 路径；`storage/CHAIN` / `gkxlumen-topic-chain` / `views/chain.py` / 产业链页 **不动** |
| 10 | git | `origin/dev` 直推；禁止 force；commit `[agent:<role>]` 或 `[human:侯佳伟]` |
| 11 | 看板 | 旧施工叶留 ID 审计；新 DAG **必须新 ID** |
| 12 | 文档 | 废作 handoff **不删** |
| 13 | 灌数真源 | **只认 50100「基础指标」灌数据按钮**（`append`/`replace`）。CLI/`svcseed` 是同一引擎，允许 CI/过夜，不得另做一套 50100 读不到的路径 |
| 14 | 出数铁律 | 图谱及十模型每次运行：**读 S 契约表 → 算法 → 回写 Demo ADS/图**。禁止 `svcModelCatalog` / GraphView 内置节点充数 |
| 15 | 代理算法 | 未定稿则移植 `demo-ui-topic` **`service-center`** 纯函数到 **Python**（`demo-algo-ent-analysis`）。禁只留前端。禁 `industry-center` |
| 16 | **阶段边界** | **本总控 = 阶段 F only。** F 内 **禁止** 改 `lumen-topic-py` / `lumen-algo-py` / `lumen-svc-platform` / `lumen-ui-topic`。公式冻结清单是 F-GATE 产物，**留给下一份 P 总控移植**（换引擎不换表）。**禁止**「F 公式冻结后并行移植 svcan」。**禁止**「F 绿自动续 P」 |
| 17 | 一张图 | SVC hang 进 Demo `demo_gkx_chain`（决策 #7），不新建平行 `gkx_service` space |
| 18 | **短板阈值（Demo）** | **运行时只用**已评审原型：0 家=空白 / ≤1=薄弱 / 均深&lt;55=瓶颈；挂 **Q-SVCCHAIN-03**。**Q061**（&lt;45 / ≥70）只作对照列 + `pending_client`，F-ALGO **不要切过去**。上线前仍须甲方确认 |

结构歧义升级 `human:李伟`。环境卡点微信 `human:淮政玮`。

---

## 2. DAG（仅阶段 F）

```text
S   storage/SVC 重建（编排仓）
    S1 流图会签（ARCH-SVC-STORAGE-S1-L02）
       → 不是建表、不是灌数
       → 画死：怎么流 / 谁写谁读 / 禁止什么
       → human:淮政玮 会签后才允许 S2/S3 写细表、才允许 50100 灌数
         （结构歧义仍升级 human:李伟，不是本单会签人）
    S2 源/ETL 指针
    S3 DWD+ADS 细表（含图谱 hang、模型回写表）
    S4 入口 / README 加回 SVC
    无会签流图不得把细表标 approved，也不得开 F-SEED

F-SEED  恢复 50100 灌数（demo-algo-ent-analysis + demo-ui-system-test）
F-ALGO  图谱 + 十模型：读表 → 算 → 回写 Demo ADS/图
F-GATE  底座退出门（现场 50100，不是 50892）
        · 只认契约命中行，不认 fixture 24 家
        · 基础指标 A1–A6 / 图谱 / 十模型能出数或诚实空态
        · 公式冻结清单入库（供下一份 P 总控，本总控不移植）
```

联调闸门：前序 handoff + ≥ `integration`/`pending_test` 即可开下一叶，不等签收 `done`。  
同仓一次一张 coding。S 在编排仓。

**本总控无段 B/C/D/E，无金路径表。** 段 E / 50892 金路径写在下一份 P 总控。

卡住只允许：真环境不通、正式库误写风险、结构升级 `human:李伟`、cost 硬闸。

---

## 3. 50100 菜单覆盖（F-GATE 必齐）

| 菜单 | 路径 | 是什么 | 阶段 |
|------|------|--------|------|
| 基础指标 | `/industry-service/basic` | 招标 §4.1.7 A1–A6（**不是**十模型）+ **灌数据** | F-SEED |
| 产业服务图谱 | `/industry-service/graph` | hang `demo_gkx_chain`（**不是**十模型） | F-ALGO |
| 短板 / 关系 / 六类技术力 / 引入 / 培育 | `/gap` … `/cultivate` | 招标 §9 **十模型** | F-ALGO |

十模型 ID：`SVC_SERVICE_CHAIN_GAP`、`SVC_SERVICE_RELATION_CHAIN`、`SVC_*_TECH_POWER`×6、`SVC_ATTRACTION_RECOMMEND`、`SVC_CULTIVATION_RECOMMEND`。

---

## 4. 代理算法白名单

真源（只读，禁止 merge 进 lumen）：

`${GKX_ROOT}/repos/demo-ui-topic/src/app/pages/service-center/`

| 模型 | 原型 | Demo 运行时口径 |
|------|------|-----------------|
| 短板 | `computeStageStats` / `service_eco_chain` | **Q-SVCCHAIN-03**（0 / ≤1 / 均深&lt;55）。Q061 对照列，不切换 |
| 图谱 / 关系链 | `buildEcoGraph` + 密度/中心性 | Q062；挂 `demo_gkx_chain` |
| 六类技术力 | capability 等权雷达 | Q060 五维等权 |
| 招引 / 培育 | `computeAttractList` / `computeCultivateList` 默认权重 | Q063 |

移植到 `demo-algo-ent-analysis` Python。配置 yaml 标 `pending_client` + `proxy_from: demo-ui-topic@<commit>`。正式实现到位后：**换引擎、不换表**（由 P 总控执行）。

---

## 5. 段 S 细叶（S1 会签后再建后续）

同构 `storage/ENT` / `storage/CHAIN`。写作顺序：

`00-context` → **`01-data-flow`（会签）** → `sources` → `etl` → `stores` → `seeds` → `storage/README.md` 加回 SVC。

| 叶 | 角色 | 何时建 | DoD 要点 |
|----|------|--------|----------|
| `ARCH-SVC-STORAGE-S1-L02` | architect | **本总控 push 后立刻** | 流图会签；**不建表、不灌数** |
| `DATA-SVC-STORAGE-S2-L02` | data | S1 会签后 | sources + ETL；细表 draft |
| `DATA-SVC-STORAGE-S3-L02` | data | S2 联调闸门 | DWD+ADS（含十模型结果表） |
| `DATA-SVC-STORAGE-S4-L02` | data | S3 联调闸门 | README 入口 |

S1 会签 Owner：`human:淮政玮`（他在等这份流图）。监管：`human:侯佳伟`。结构歧义：`human:李伟`。看板 `ready_to_sign → done` 签收仍 `human:淮政玮`。

F-SEED / F-ALGO / F-GATE 建议 ID（**S1 会签前禁止建**）：

| 建议 ID | 仓 |
|---------|-----|
| `DEMO-SVC-LAB-SEED-L01` | `demo-algo-ent-analysis` |
| `DEMO-SVC-LAB-UI-SEED-L01` | `demo-ui-system-test` |
| `DEMO-SVC-LAB-GRAPH-L01` | 同上两仓 |
| `DEMO-SVC-LAB-MODELS-L01` | `demo-algo-ent-analysis` |
| `DEMO-SVC-LAB-UI-MODELS-L01` | `demo-ui-system-test` |
| `DEMO-SVC-LAB-GATE-L01` | data + 现场 |

强度：coding `ponytail full`；S1 definition `ponytail off`。

---

## 6. 阶段 P（**不在本总控**）

50892 产品长任务：**底座 F-GATE 绿后由淮政玮单独授权**，另写 `…-P-长任务总控.md`。

本文件 **禁止**：

- 写「F 绿自动续 P」
- 预建 lumen B/C/D/E 叶
- 在 F 内移植 `lumen-algo-py svcan` / 恢复 `gkxlumen-topic-svc` / 改 `lumen-ui-topic`

P 总控才做：换引擎不换表（消费 F-GATE 公式冻结清单）。

---

## 7. 废作（不要派、不要当 `depends_on`）

现行只认：本总控、开工方案指针、停机转交、停机总控、`DEMO-SVC-ABORT-L01`、以及本轮 **新 ID** 叶。

旧 `DEMO-SVC-*` / `LUMEN-SVC-*` 施工叶、旧 S1–S4（含 `ARCH-SVC-STORAGE-FLOW-SIGNOFF-L01`）、旧 ABCD/FULL 总控 = **废作留档，不删、不派**。

不废：`SVC-DATA-ANALYSIS-L01*`、产品五件套、`TOPIC-SVCCHAIN-R*`、`SVC-ALGO-DESIGN-L01`。

---

## 8. 开工顺序（本总控范围内）

1. 本总控已 push `origin/dev`。  
2. MCP 建并认领 `ARCH-SVC-STORAGE-S1-L02`（24h · `coordinator_dispatch` · `supervised_by=human:侯佳伟`）。  
3. **等 S1 会签**（`01-data-flow` `signoff_status=approved` · `human:淮政玮`）。别着急灌数。  
  
4. 再会签后建 S2 → S3 → S4 → F-SEED → F-ALGO → F-GATE。  
5. F-GATE 绿 → **停本总控主链**；P 段等单独授权。

---

## 9. 不做

- 不派旧 C/D、不复活 Gate-0 / 旧 E `ready_to_sign` 当本轮完成  
- 不删废作 handoff  
- 不碰 CHAIN / `industry-center`  
- S1 会签前不建表、不灌数、不建 F-SEED  
- 阶段 F 不碰四份 lumen 仓  
- 不写「F 绿自动续 P」  
- 不写正式 `gkxlumenx_*`、不 DROP ODS 33 表、不平行主体表/平行图空间  

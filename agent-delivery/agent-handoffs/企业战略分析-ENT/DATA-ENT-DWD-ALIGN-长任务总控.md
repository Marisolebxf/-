# 企业 DWD 库/稿/代码对齐 · 长任务总控

> **日期**：2026-09-03  
> **授权人 / 监管人**：`human:徐滕强`  
> **授权句**：**后续认领不必再问。**（2026-09-03 `human:徐滕强` 聊天授权；可一次提交 `origin/dev`。）  
> **升级人**：结构歧义（新表 / 改主键 / 新 ES / 正式 Nebula space）→ `human:李伟`。同段不依赖该点的叶继续。  
> **锁**：`lock_hours=24`。lease 过期同一监管人续领，不改设计。  
> **目标**：工商 DWD 正式库、设计稿 v3.1、派单包文档、`lumen-etl-es-py` 读列一致；曾用名写入现有 ES mapping；图谱按 `14` 已拍板 op 接正式 DWD。demo 只对照。  
> **不含**：GDF Wave A/B **洗数执行**（辜少彬）；Java REST/Feign **结构**；改 ES 文档字段名 / 别名；未点名写正式 `gkx_chain`。  
> **demo DWD**：与正式库 **同一套** ADD / 不 DROP（2026-09-03 改口）。灌数仓 `demo-algo-science`（及 ENT 重灌脚本）**要核列名**，只改对上正式库列的映射，不另起一套。  
> **切法**：**不套**规约前端 A–E。按仓切 `gkx-orchestration` / `lumen-etl-es-py` / `lumen-algo-py`。无 Java 段、无前端段、无段 E 金路径。下表「文档/ETL/图谱/DDL/曾用名」只是作业名。  
> **模式**：长任务。规约：[`长任务执行规约.md`](../../长任务执行规约.md) · **同仓同时只派一张 coding 单**；跨仓可并行。  
> **厚包**：派单包 [`GDF-ENT-WORKPACK-v3/`](../../data/GDF/派单包/企业/GDF-ENT-WORKPACK-v3/)（`09`/`10`/`12`/`13`/`14`/`15`）。薄条 = 各叶 registry DoD + 本文件 §3；coordinator `/goal` 必抄本总控路径。  
> **不并入**：`GDF-ENT-WORKPACK-V3-L01`（保持 `ready_to_sign`，不打回）  
> **废作叶**：`DATA-ENT-DWD-ALIGN-APPLY-L01`（已拆成 ETL + DDL，**勿派**）  
> **下游解锁**：registry `depends_on` **禁止等签收 `done`**。前序 handoff 齐且 ≥ `integration` / `pending_test` 即按 §6.2 升 ready。  
> **监管人清单（防忘）**：§5。跑完只认 §5.3，不靠聊天。

| 作业 | 仓 | 分支 | 任务 | 并行组 | 状态门 |
|------|-----|------|------|--------|--------|
| 文档回写 | `gkx-orchestration` | `origin/dev` | `DATA-ENT-DWD-ALIGN-DOC-L01` | **P0** | 授权句补齐后 ready |
| ETL 改读列 | `lumen-etl-es-py` | `origin/dev` | `DATA-ENT-DWD-ALIGN-ETL-L01` | **P0**（与文档不同仓） | 授权句后 ready；**不** depends DOC |
| 图谱 op | `lumen-algo-py` | `origin/dev` | `DATA-ENT-GRAPH-OPS-L01` | **P0**：2026-09-03 继续做。`/internal` + 正式 DWD 预览；**不写**未点名 `gkx_chain` | Java REST 零改 |
| 正式库 ALTER | `gkx-orchestration` | `origin/dev` | `DATA-ENT-DWD-ALIGN-DDL-L01` | P1 | DOC **联调闸门**（同仓串行）；无拟 ALTER 清单禁止派 |
| 曾用名 ES | `lumen-etl-es-py` | `origin/dev` | `DATA-ENT-ES-FORMER-L01` | P1 | ETL 联调闸门（同仓串行） |

无前端段 E。闭环抽检：正式库 `information_schema` vs v3.1 vs ETL `SELECT`；ES params 键名不变；Java 企业 API 零 diff。

---

## 1. 已拍板（禁止回问）

1. **demo 不当真源**，只对照 8-12。禁止按 `demo_gkxlumenx_dwd` **覆盖**正式库。2026-09-03：**demo DWD 与正式库同一套 ADD**（DDL 叶两库都做）。灌数项目要核是否改读正式列名。  
2. **总真源不整表二选一**。按 Q-WP3-29 四类处理：  
   - (1) 改名（`bid_title`↔`announcement_title` 等）→ **跟正式库列名**，设计稿/ETL 改回去。  
   - (2) 设计有、正式库从未有 → 专利按 v3.1 **可 ADD**（Q-WP3-23/28 2026-09-03 改口）；extra 七列仍 Q-WP3-24。现网同义列 **不 DROP**。  
   - (3) 正式库有、设计稿 8-12 写丢 → **补回设计稿**（7-29 ETL 已证明的 base 宽列等）。  
   - (4) 正式库后加列 → **保留并回写设计稿**，禁止按稿删。  
3. 三方 live `gkx` **只读**，不改供应方表。  
4. 调用链不变：前端 → Java → Python `/internal/*`。GDF 不直写 ES / 不写 nGQL。  
5. **Java API 兼容（硬）**：不改 `lumen-svc-platform` 企业 REST / Feign 路径、请求体、响应 JSON。`lumen-etl-es-py` 只改 DWD `SELECT` / `row.get`；**ES 文档字段名、nested 结构、别名 `gkx_enterprise` 不动**（例如仍写 ES `announcement_title`，只是改从 `bid_title` 取值）。禁止为对齐去改 Java 检索契约。  
6. 废作：按设计稿整库覆盖正式库；自动「三方同步」脚本；再写一份 as-built 却从 demo `SHOW CREATE`；GDF 直写 ES/nGQL；改 Java 检索/图谱 REST；派已拆的 `APPLY-L01`。  
7. git：只推 `origin/dev`；commit `[agent:<该叶角色>]`（文档/ETL/DDL/FORMER=`data-agent`，GRAPH=`algorithm-agent`）；禁止 force。未获「可以一次提交」前不 push。  
8. 强度：ponytail full（文档叶不以缩代码为目标）。  
9. ETL 另含：`finance` 改读正式库 `net_profit` 写入现有 ES `pure_profit`（停 `total_profit` 双写）。不改 ES 键名。

未拍板（A 叶分类表里标出，只审这类）：7-29 SELECT 没写到、又不能证明是 8-12 之后才加的列。禁止猜测口径。

---

## 2. 依赖

```text
P0 并行（跨仓）
  DOC-L01 ─────────────┐
  ETL-L01 ──────────┐  │
  GRAPH-OPS-L01     │  │
                    │  │
P1 同仓串行          │  │
  ETL-L01 ──闸门──► ES-FORMER-L01
  DOC-L01 ──闸门──► DDL-L01
```

废作：不要派「按 v3.1 无分类直接 ALTER」；不要派 `APPLY-L01`。  
Mapping 文档回写在 **DOC**（`09/10/13`）。GDF Wave A/B **洗数**仍不在本管线。

---

## 3. 开工顺序

1. 人补授权句 → coordinator 把 **DOC + ETL** 升 ready；GRAPH 仅当 §3 第 4 步条件满足才升。  
2. DOC：四类表 + 回写 v3.1 / 派单包 `10/09/13`。不 ALTER。  
3. ETL（可与 DOC 同时）：六模块改读正式库列名；ES params 键名不动。  
4. GRAPH：接 `/internal/entan/graph*` + 正式 DWD 四 op；space 未点名只预览、不写 `gkx_chain`（升级人仍李伟）。  
5. DOC 闸门后派 DDL；ETL 闸门后派 FORMER。  
6. 抽检；handoff + cost。签收可积压，不挡主链。

卡住只允许：真环境不通、正式库误写风险、拟 ALTER 与已拍板冲突、第 4 类残留待你审、正式图谱 space 未点名、单叶 cost >$10。

---

## 4. 验收（无前端金路径）

| # | 期望（未发生=红） |
|---|-------------------|
| 1 | v3.1 工商表 CREATE TABLE 列集 ⊇ 正式库该表列（第 4 类已回写） |
| 2 | 正式库已按清单 ADD 专利宽列 / extra 七列 / 财务缺列；旧同义列仍在 |
| 3 | `reg_info`/`finance`/`news`/`bid`/`invest`/`executive` 的 SQL 列在正式库都存在；写入 ES 的 **params 键名与 mapping 与改前一致** |
| 4 | demo 未当施工真源；live `gkx` 无 DDL；`lumen-svc-platform` 企业 API **零 diff** |
| 5 | `former_names` 写入现有 mapping 字段；未改 Java 检索约定 |
| 6 | 图谱只接 `14` 本期 op；内部 `/internal` 与现网 Feign 一致；未点名不写正式 `gkx_chain` |

允许空态：第 4 类里标「待核、本叶不写」的列，须在 DOC handoff 点名。

---

## 5. 监管人清单（`human:徐滕强` · 防忘）

本管线 **不替代** V3 签收、GDF 洗数、Java `/ent/v1`。下面三张表才是你要做的；agent 不得代签、不得代通知 GDF。

### 5.1 现在（长任务还没开跑）

| # | 你做 | 不做 / 说明 |
|---|------|-------------|
| 1 | 在本文件页眉把授权句改成 **「后续认领不必再问」** | 不写这句，coordinator 不准升 ready |
| 2 | 说 **「可以一次提交」** 才允许把总控/包修订推进 `origin/dev` | 未说之前只落盘本地 |
| 3 | 正式图谱 space **先不点名**（已授权） | GRAPH 已接 `/internal` 预览，仍零写入 `gkx_chain` |
| 4 | **demo DWD 跟正式库同一套 ADD**（已授权） | DDL 两库一起做；灌数仓要核列名 |
| 5 | 看 DOC 分类表里标「待核」的第 4 类残留列 | 只审这类；已拍板项 agent 不准回来问 |

### 5.2 跑的时候（授权后）

| # | 你做 | 不做 |
|---|------|------|
| 1 | 结构项（正式库 ADD 与清单冲突、要新 ES 字段、要写 `gkx_chain`）来找你或李伟 | 不要每叶再点头 |
| 2 | 签收可积压 | 不要用「淮政玮还没点 done」卡住 DDL/FORMER |
| 3 | 单叶 >$10 停该叶复盘 | 授权句不能突破 cost 硬闸 |

### 5.3 五叶都到 `ready_to_sign` 之后（你要收口）

按顺序做，做完在本表勾。

| # | 你做 | 真源 / 给谁 |
|---|------|-------------|
| 1 | **抽检四条**：正式库列 ⊇ 清单 ADD；旧同义列还在；六模块 SQL 列都在；`lumen-svc-platform` 企业 API **git diff 为空** | 总控 §4 |
| 2 | **通知辜少彬**：派单包列契约已修订（建议 CHANGELOG 升 v3.1）；洗数只认新 `09`/`10`/`13`，禁止再按 v3.0 设计稿列名洗 | 飞书；GDF 已开工必须发 |
| 3 | **V3-L01 不打回**。handoff 末加一行：「列契约以 `DATA-ENT-DWD-ALIGN-DOC-L01` 为准」。保持 `ready_to_sign` | 淮政玮仍只签 V3 定义叶 |
| 4 | 请 **淮政玮** 签 `GDF-ENT-WORKPACK-V3-L01`（若他卡「包又改了」：说明是对齐修订，DoD 未破） | 只有他能 `ready_to_sign→done` |
| 5 | 本管线五叶签收可积压；你若代收只审 handoff/抽检，**done 仍是淮政玮**（`chore` 除外） | 宪章 |
| 6 | **APPLY-L01** 确认无人误派；需要的话让 coordinator 标死/改标题「废作」 | 勿再施工 |
| 7 | demo DWD **已拍板跟 ADD**；收口时确认两库 information_schema 一致 | DDL 叶 |
| 8 | GRAPH `/internal` 已接；space **仍未点名**，禁止宣称图已灌绿 | 升级人李伟 |
| 9 | **GDF 洗数**：把修订后的包交给辜少彬开 Wave A/B（本管线不洗） | 阻塞表仍：`forg_subsidiary` / `chain_dtl` / `pat_dtl` |
| 10 | 日批先继续 **`15` §6.1**（飞书值班 + 本侧转发 + 轮询）。不要让 GDF 配 `/ent/v1` | 目标契约未上线 |
| 11 | **另开（不进本 DAG，除非你改口）**：`15` 转发脚本叶；`OPEN-ENT-ETL-JOBID`；Java `/ent/v1`+callback（`OPEN-ENT-GDF-TRIGGER`/`CALLBACK`）；CDC 预填（胡森泉）；`DATA-ENT-STORAGE-OPS-OPEN-L01` | 你说了才建/才并 |
| 12 | 本管线 **不**做：创新载体/合作/科研/供应链/链专利/招聘上 ES/专利 nested/股东上图上 ES | Q-WP3 已锁 |

### 5.4 本管线跑完 ≠ 整条企业数据链完成

```text
本管线绿
  → 稿/库/ETL 读列一致，GDF 有一份不骗他的 09/13
  → 辜少彬 Wave A/B 洗数（另线）
  → §6.1 日批触发 ES（另线或后开叶）
  → Java /ent/v1 + callback（你点头才动 Java）
  → 正式图谱 space（李伟/你点名）
```

禁止把本管线 `ready_to_sign` 说成「ES 已灌绿 / 图谱已灌绿 / GDF 已导入」。

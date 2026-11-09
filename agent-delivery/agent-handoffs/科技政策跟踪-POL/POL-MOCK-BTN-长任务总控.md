# POL-MOCK-BTN · 政策 Mock 按页按钮化 · 长任务总控（无人值守）

> **日期**：2026-11-09  
> **授权**：`human:淮政玮`（本管线监管人；后续认领 **不必再问**）  
> **目标**：算法中台「政策 Mock」页按展示系统七页各放一个按钮，一键重灌该页全部缺项表；点完出回执，按需规序号写明表、行数、一条样例、哪页读；展示系统经 Java 读得到、读得懂。  
> **模式**：长任务。规约：[`长任务执行规约.md`](../../长任务执行规约.md)  
> **执行 agent 按本文件已拍板项继续**，禁止把「等用户」当默认阻塞。  
> **派单状态**：2026-11-09 只建单、写总控，**未派单**。由授权人另行下令后 coordinator 才开始认领。

| 段 | 仓 | 分支 | 任务 | 状态门 |
|----|-----|------|------|--------|
| A | `demo-algo-ent-analysis` | `origin/dev` | `POL-MOCK-BTN-A01` | 无前置 |
| B | `demo-algo-ent-analysis`（同步 `lumen-algo-py/vendor/entan-py`） | `origin/dev` | `POL-MOCK-BTN-B01` → `B02` → … → `B07` | 同仓串行；前序满足联调闸门即可，不等签收 |
| C | `lumen-svc-platform` | `origin/dev` | `POL-MOCK-BTN-C01` → `C02` → `C03` | A01 满足闸门后可与 B 并行；同仓串行 |
| D | `demo-ui-system-test` | `origin/dev` | `POL-MOCK-BTN-D01` | B01 回执接口满足闸门后 |
| E | qa-agent | 已发布 demo 算法中台 + lumen dev 展示接口 | `POL-MOCK-BTN-E01` | B07、C03、D01 均满足闸门后 |

厚包：本文件 §5 · 金路径：本文件 §4 · 缺陷包：`templates/long-task-e-defect-pack.md`  
设计依据：`sdd/科技政策跟踪-系统详细设计说明书.md` 第 5 节（现状）、第 6 节（路径）、第 11 节（缺项表）

---

## 1. 无人值守规则（违反才停）

1. **监管已授权**：`supervised_by=human:淮政玮`，`claim_type=coordinator_dispatch`。升 ready 后直接认领开工。  
2. **已拍板不回问**：见 §5。  
3. **甲方 🟡**：诚实降级，不停工等纪要。  
4. **结构歧义**：`blocked` + 升级 `human:李伟`；同段其它叶继续。  
5. **缺数据**：禁止写 ODS、正式 DWD、ADS 和供应方库；缺项只进 `gkxlumenx_gapfill` 的 `gapfill_` 表（209、212 例外：写已有 `ads.policy_effect`、`ads.policy_match`，走已有 `run()`）。读空则空态。  
6. git：只推 `origin/dev`；禁止 force；commit `[agent:<role>]`。  
7. **推送**：后端 `demo-algo-ent-analysis`、`lumen-algo-py`、`lumen-svc-platform` **完工即推**（自检绿后 commit + push）。前端 `demo-ui-system-test` **不适用完工即推**，停在本地待 `human:淮政玮` 确认。  
8. 每叶 handoff + `ponytail:` + cost 四字段。`ready_to_sign→done` 可积压。  
9. **段 E**：禁止逐叶 QA；E01 一张；QA 不改代码；**期望未发生必红**；红了先按规约 §11.4 分类，C1 由 coordinator 派修。  
10. **Nacos / 密钥**：不重发 Nacos。给演示算法服务配大模型密钥属线上变更，单独找授权人批准，**不挡主链**（见 §5.3）。

锁：`lock_hours=24`。lease 过期则同一监管人续领，不改设计。

---

## 2. 依赖（联调闸门，见规约 §6）

```text
A01 ──► B01 ──► B02 ──► B03 ──► B04 ──► B05 ──► B06 ──► B07 ──┐
  │       └──────► D01（回执接口定型后） ────────────────────────┤
  └──► C01 ──► C02 ──► C03 ───────────────────────────────────┴──► E01
```

废作（不要派、不要当依赖，已在 registry 置 blocked 并写明取代关系）：

| 旧单 | 取代 |
|---|---|
| `POL-L2-DS10-SENT-GAPFILL-L01` | `POL-MOCK-BTN-B02` |
| `POL-L2-PC2-SEM-GAPFILL-L01` | `POL-MOCK-BTN-B05` |
| `POL-L2-PC3-XCMP-GAPFILL-L01`、`POL-L2-PC3-VIZ-GAPFILL-L01`、`POL-L2-PC3-OUT-GAPFILL-L01` | `POL-MOCK-BTN-B06` |
| `POL-L2-PC4-DEEP-GAPFILL-L01`、`POL-L2-PC4-INSIGHT-GAPFILL-L01`、`POL-L2-PC4-WRITE-GAPFILL-L01`、`POL-L2-PC4-TRACE-GAPFILL-L01` | `POL-MOCK-BTN-B07` |

---

## 3. 开工顺序

1. A01 出缺项表总表与可读标准，补建缺的表。  
2. B01 搭按钮框架与回执接口；随后 B02–B07 逐页收编或新写灌数逻辑。  
3. A01 满足闸门后并行 C01–C03（新增拆解、对比、研报三条读口）。  
4. B01 满足闸门后 D01 接 7 个按钮与回执表格（本地待确认推送，不挡 E）。  
5. B07、C03 满足闸门、D01 有 handoff → E01。

卡住只允许：真环境不通、正式库误写风险、结构升级项、E 超 3 轮 / cost 硬闸。

---

## 4. 金路径（段 E1 · 总控必填）

> **期望未发生必红**。空态只有写进本行才算过。D01 未推送时，E01 直接调算法中台按钮接口（与按钮同一入口），不算绕过。

| # | 按钮 | 入口 | 期望（未发生=红） | 允许的空态 |
|---|------|------|-------------------|-----------|
| 1 | 全景 | 按钮接口 → 回执 → 展示 `panorama/*`、`assessment-report`、`benchmark-report` | 回执含 199、205、209–218 各序号行数 >0、样例为中文自然句；展示接口对应区块非空 | 201、202、204、212 匹配（用户数据，无记录返回空） |
| 2 | 评价 | 同上 → `evaluation/*` | 219–231 各序号行数 >0；展示读到 | 无 |
| 3 | 推演 | 同上 → `simulation/jobs` | 232–242（240 除外）行数 >0；`DS12-EST` 用例 232–236 请求仍读到 | 240 读图 |
| 4 | 治理 | 同上 → `governance/lineage-index`、`indicator-library` | 604、605 行数 >0 | 602、603 读第 6 项 |
| 5 | 拆解 | 同上 → `parse/jobs` | 606 行数 >0；展示读到 | 607–609 |
| 6 | 对比 | 同上 → `compare/jobs` | 610、611、613 行数 >0；展示读到 | 612 用户配置 |
| 7 | 研报 | 同上 → `report/jobs` | 614–617 行数 >0；618 读到正文 | 618 无文件 |
| 8 | 重复点击 | 任一按钮连点两次 | 行数不翻倍（幂等）；回执两次一致或说明差异 | 无 |
| 9 | 正式库 | 顶栏切到正式库后点按钮 | 拒绝并提示，库内无变化 | 无 |

P1 不挡闭环：大模型密钥未配时回执标「模板句」即算过。

---

## 5. 已拍板（2026-11-09 `human:淮政玮`）

### 5.1 按钮与落点

- **按页分 7 个按钮**：全景 / 评价 / 推演 / 治理 / 拆解 / 对比 / 研报。与现有「Mock 10 条数据」「真实政策补外围」并列，职责分开：那两个造政策与外围，新按钮按当前演示库政策重灌缺项表。
- 按钮后端在 `demo-algo-ent-analysis` 的 `polan/mockgen`，与 `synth.py` 同一套单飞与轮询（`GET /policy/mock/synth` 同款状态）。每次改动同步字节一致副本到 `lumen-algo-py/vendor/entan-py/polan/mockgen/`。
- 库落点沿用 `POL-L2-DS12-EST-DEMO-FIX-R20261109-DATA` 已验证的 `gkxlumenx_gapfill`，写前过 `assert_demo_mysql_targets`；顶栏切正式库时拒绝。
- `lumen-algo-py/scripts/seed_gapfill_policy_*.py` 15 个脚本收编：脚本改为调用按钮同一函数，**不再整表清空**（DS12 用例行曾被 `--apply` 清掉）。按钮是唯一人工复现入口。
- 写法幂等（按业务键 upsert），只删本按钮批次号的旧行；不动其它批次与真实政策行。

| 按钮 | 序号 | 表 |
|---|---|---|
| 全景 | 199；205；209–212；213–218 | `gapfill_policy_qry_*`、`gapfill_policy_trend_*`、`gapfill_policy_theme_dist`、`gapfill_policy_audience_feedback`、`gapfill_policy_assessment_report`、`ads.policy_effect` / `ads.policy_match`（已有 `run()`）、`gapfill_policy_version_diff`、`gapfill_policy_detail_compare`、`gapfill_policy_benchmark_report`、`gapfill_policy_impl_dept` |
| 评价 | 219–231 | `gapfill_policy_eval_*` |
| 推演 | 232–242 | `gapfill_policy_sim_forecast`、`gapfill_policy_sim_result`、`gapfill_policy_sim_stakeholder` |
| 治理 | 604、605 | `gapfill_policy_lineage_index`、`gapfill_policy_indicator_lib` |
| 拆解 | 606 | `gapfill_policy_semantic`（新建） |
| 对比 | 610、611、613 | `gapfill_policy_xcmp`、`gapfill_policy_xcmp_viz`、`gapfill_policy_xcmp_summary`（新建） |
| 研报 | 614–618 | `gapfill_policy_report_analysis`、`_insight`、`_body`、`_trace`（新建） |

表名以说明书第 11 节为准；A01 盘点发现与现网实际表名不一致时，以现网为准并回写总表。

### 5.2 回执与可读标准

- 回执按需规序号逐行：序号、需规叶名、表、本次写入行数、表内总行数、一条样例（≤60 字）、读取页面与接口、生成方式（大模型 / 模板句）。
- 内容一律中文自然句；不出现占位符、空字段名、`null`、英文枚举码。
- 每行带真实存在于演示库的 `policy_id`（或明确的地区 / 主题键）。
- `is_mock=1`，D4 仍 mock；不新造 `metric_id`，沿用说明书 §5.2 已写的三类。

### 5.3 大模型

有密钥用大模型；无密钥自动退回「真实政策字段 + 模板句」，回执注明。配密钥走 skill `gkx-gitlab-ci-var`，须授权人当次批准，不挡主链。

### 5.4 Java 读口（C 段）

- 照 `PolicySimulationController` 的 `simulation/jobs` 写法：display 经 `RemoteElementClient` 调 `gkxlumen-element` GET，element 读缺项表；display 不写 mock、不连 Python。
- 一个对外路径一叶：`POST /display/v1/policy/parse/jobs`、`compare/jobs`、`report/jobs`（说明书第 6 节）。无行返回空，不造 0。
- 不改 Nacos，不动网关路由以外的共享配置；如需网关路由，按 `gkx-nacos-shared-config` 单 dataId 发布，并先找授权人批准。

### 5.5 范围外

lumen 展示前端拆解、对比、研报三页接这三条读口；说明书 §5.3 前端页头写死问题。均另开单，不在本管线。

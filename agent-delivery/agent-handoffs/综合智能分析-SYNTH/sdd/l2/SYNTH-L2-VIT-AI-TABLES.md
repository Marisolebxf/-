# SYNTH L2 · 活力补册 — ADS 结果表与读装包（ARCH/DATA/API/METRIC 合并册）

- 日期：2026-11-05（v1.0.5：会签退回。五张结果改落 ADS；权重缺行禁常量；快照可按 snapshotId 读旧批）
- 状态：**DRAFT，第一轮退回后改稿，待复审**
- 定位：**补册**。活力叶已由 VIT 五单覆盖任务接口、Java 白名单、FE 接线、gapfill 输入缺项。本册只补结果落表、灌行与读装包：五张 `synth_vit_*` 新建在 `demo_gkxlumenx_ads` / `gkxlumenx_ads`。不新建 registry 单。
- 上游：总册 §2.1/§11（v1.0.5-draft）；指纹与总纲冲突时以**本册 §3** 为准

## 1. ARCH（流程与落点）

```text
实算/预填（Python, vendor/entan-py，seed_synth_vit_*.py）
  读：gkxlumenx_gapfill 三张既有输入（new_product_sales_ratio / rd_employee / policy_effect），不是结果表
  写：demo_gkxlumenx_ads / gkxlumenx_ads 的 synth_vit_*（5 张；预填 is_mock=1；整批写）
  读：只读上述 ADS 表 → 装包 VitalityResult
    → GET /topic/v1/synth/vitality/batch-snapshot
    → GET /internal/v1/synth/vitality/batch-snapshot
    → POST /internal/v1/synth/jobs/execute
```

- 指数入口同核：`M_SYNTH_VIT_INDEX` ≡ `M_SYNTH_186_1`，只算一处。
- 上游维分：`M_SYNTH_182_1`(科技)/`M_SYNTH_184_1`(人才)/`M_SYNTH_185_1`(政策) 已有 SPEC；`M_SYNTH_183_1` 产业维未换源 → 维分产业行缺，不补 0。
- 权重三方案存表，不在装包里写死：`WEIGHT_MAIN`=0.30/0.35/0.20/0.15（`M_SYNTH_VIT_WEIGHT`）；`INDEX_MAIN`=0.30/0.30/0.20/0.20（`weight_provenance_metric_id='M_SYNTH_VIT_INDEX'`）；`EQUAL`=0.25×4。三档由 seed 写入 `synth_vit_weight`，`is_mock=1`。指数与权重同 `weight_profile_code` 配对读表。
- **缺行**：只读 `synth_vit_weight` 已灌行。没有该 profile 行就 `null`+`reason`+`confidence`。装包不得填入 `0.30/0.35/0.20/0.15`、`0.30/0.30/0.20/0.20` 或 `0.25×4`。

## 2. DATA（表 · 每表四项：粒度/唯一键/写入/读批）

库：`demo_gkxlumenx_ads` / `gkxlumenx_ads`。灌数方 entan-py `seed_synth_vit_*.py`。读取：`GET /topic/v1/synth/vitality/batch-snapshot` 与 `GET /internal/v1/synth/vitality/batch-snapshot`，装包只读这五张 ADS 表。公共列见总册 §11.2。

| 表 | 业务粒度（一行=） | 唯一键（`uk_`） | 写入方式 | 读取批次规则 |
|---|---|---|---|---|
| `synth_vit_index` | 区域×对比范围×窗×**权重方案** 的指数 | `(region_code, compare_scope, window_label, weight_profile_code, calc_batch_id)` | 实算/预填整批写 | succeeded 最新批单行（**profile 选择规则见 §3**） |
| `synth_vit_dim_score` | 同上 × 权重方案 × 维度（科技/产业/人才/政策） | `+ (weight_profile_code, dim_code)` | 同上 | 同批 ≤**12** 行（3 方案×4 维；产业维可缺） |
| `synth_vit_weight` | 同上 × 权重方案 × 维度（行主 `metric_id=M_SYNTH_VIT_WEIGHT`；**`INDEX_MAIN` 方案行的 `weight_provenance_metric_id='M_SYNTH_VIT_INDEX'`**，标记该组权重服务于指数件口径，不冒充权重指标自有口径） | `+ (weight_profile_code, dim_code)` | 预填必须 `is_mock=1` | 同批 ≤**12** 行（3 方案×4 维） |
| `synth_vit_indicator` | 同上 × 分项指标 | `+ (indicator_code)` | 同上 | 同批 N 行 |
| `synth_vit_rank` | 对比范围内每城市×**权重方案**（排名按方案分别出） | `(region_code, compare_scope, window_label, weight_profile_code, rank_city_code, calc_batch_id)` | 同上 | 同批全城市行（同 profile 内） |

- 预填范围：默认三元组（深圳 × 全国重点城市 × 最近 3 年，Q-SYNTH-V-02 🟡）。
- 批次「最新」按 `calc_batch_created_at` 排序（总册 §11.2 v0.5），禁字符串比较。
- 血缘：活力五指标源=兄弟指标产物+gapfill 输入（`gapfill_synth_new_product_sales_ratio` / `gapfill_synth_rd_employee` / `gapfill_synth_policy_effect`），写表 COMMENT。
- DDL：列宽/索引/授权会签后 data-agent 出（demo+正式结构一致）。

## 3. API（参数/异常/空态）

**权重方案选择（固定规则）**

| 规则 | 说明 |
|---|---|
| 参数 | 快照/任务均支持可选 `weight_profile`；枚举 **`INDEX_MAIN` \| `WEIGHT_MAIN` \| `EQUAL`**（大小写敏感） |
| 默认 | **未传 = `INDEX_MAIN`**（与 `M_SYNTH_VIT_INDEX` 件口径 0.30/0.30/0.20/0.20 一致） |
| 非法值 | 非枚举 → **400** + reason，不默改、不静默回落 |
| 同请求一致 | 同一快照/任务装包内：`synth_vit_index` / `dim_score` / `weight` / `rank` **必须同 `weight_profile_code`**；报告页消费该快照时沿用快照内 profile（响应体回显 `weight_profile`），禁止报告另选档 |

**任务去重指纹 / 冻结 / 缓存（活力叶强制，覆盖旧总纲三段式）**

| 项 | 规则 |
|---|---|
| 归一 | `weight_profile_norm` = 请求值；缺省或空 → `INDEX_MAIN`（归一后再拼指纹，禁止把「空」与「INDEX_MAIN」当成两档） |
| `analysis_fp`（活力） | `region\|compare\|window\|weight_profile_norm`（四段；窗仍先归一中文再入指纹） |
| params 冻结 | create/`targetParams`/`freezeIntelTargetParams` 必须写入 `weight_profile`（归一后）；`object_summary` 建议带 profile 短码 |
| 当天复用 / running 单飞 | 同 `analysisType` + **四段** `analysis_fp` 才复用；仅三段相同但 profile 不同 → **新任务**；**`legacy_unknown` 任务永不参与自动复用** |
| **查询缓存键**（可变、可覆盖） | 稳定键 `cache_key = region\|compare\|window\|weight_profile_norm`：仅用于「当前条件最新成功快照」索引；同键再跑成功可指向新 `snapshotId` |
| **不可变 `snapshotId`** | 每成功批唯一：`snap:{calc_batch_id}` 或等价 UUID/自增快照记录 ID（**必须含批次或记录唯一性**）；禁止仅用条件(+profile) 当 ID。同条件重跑 → **新** `snapshotId`，旧 ID 仍指向旧批 |
| 报告 / 恢复匹配 | 任务复用按四段 fp；打开历史结果/图谱按 **不可变 `snapshotId`**；query `analysis_fp` 与冻结 fp 不一致 → 不复用 |

**旧三段任务识别（仅活力；禁止一律当成 INDEX_MAIN）**

历史实现混用等权 0.25、`TEMP_WEIGHTS` 0.30/0.30/0.25/0.15、以及未来 `INDEX_MAIN`，**不得**把「仅三段 fp」直接映射为 `INDEX_MAIN`。

| 存量形态 | 处理 |
|---|---|
| 冻结 params / result 含可识别权重向量或 `weight_profile` / 明确 `methodVersion` 映射表 | 按识别结果归入 `EQUAL` / `WEIGHT_MAIN` / `INDEX_MAIN` / 其它登记档；仅当向量与档位**精确匹配**才可参与该档自动复用 |
| 仅有三段 `analysis_fp`，且**无法**从冻结权重、`dimScores.weight`、`methodVersion` 确认档位 | 标 **`legacy_unknown`**；可展示历史结果，**禁止**自动复用 / 当天单飞命中；新请求（含默认 `INDEX_MAIN`）**必须重新分析** |
| 用户请求 `INDEX_MAIN`（含缺省归一） | 不得命中 `legacy_unknown` 或权重向量≠INDEX_MAIN 的旧任务 |
| 要素/协同叶 | 仍三段 `region\|compare\|window`（本册不改） |

权重档对照（识别用，容差 0）：`EQUAL`=0.25×4；`INDEX_MAIN`=0.30/0.30/0.20/0.20；`WEIGHT_MAIN`=0.30/0.35/0.20/0.15。现网 mock `TEMP_WEIGHTS`（0.30/0.30/0.25/0.15）**不落任一一档** → 一律 `legacy_unknown`。

- 快照 `GET /topic/v1/synth/vitality/batch-snapshot?region=&compare=&window=&weight_profile=&snapshotId=`：
  - 200：`{snapshotId, cache_key?, computedAt, methodVersion, weight_profile, calc_batch_id, result: VitalityResult}`
  - 传入 `snapshotId`：只读该批，不改走最新批
  - 未传 `snapshotId`：用 `cache_key` 取最新成功 `snapshotId`，再按该 ID 读 ADS 批；重跑成功后索引改指新 ID，旧 `snapshotId` 仍可读旧批
  - 404：非默认三元组无预计算 → 前端 no_batch 引导「开始分析」
  - 500：仅基础设施故障；缺数据一律 200+null/reason，不 500
- 任务 create params：`{ region, compare, window, weight_profile? }`；下游 execute 同构；`analysis_fp` 四段；失败 → `failed`+`reason`。
- 缺行统一策略：总册 §11.4。

## 4. METRIC（挂接/就绪度/血缘）

| metric_id | D1 | D4 | 落表 | 缺行表现 |
|---|---|---|---|---|
| `M_SYNTH_VIT_INDEX` | aligned | mock | `synth_vit_index` | null+reason |
| `M_SYNTH_VIT_DIM_SCORE` | aligned | mock | `synth_vit_dim_score` | 产业维 null（`M_SYNTH_183_1` 未换源） |
| `M_SYNTH_VIT_WEIGHT` | aligned | mock | `synth_vit_weight` | 无行 → null+reason+confidence；禁止常量回填 |
| `M_SYNTH_VIT_INDICATOR` | aligned | mock | `synth_vit_indicator` | 缺项行 null（gapfill 灌后收敛） |
| `M_SYNTH_VIT_RANK` | aligned | mock | `synth_vit_rank` | ranks 空数组 |

`deltaVsCompare`/`yoy`/`trend`/`strengths`/`weaknesses` 无独立 id：装包推导，推不出空。D4 改 live 条件：ADS 实算成功 + 缺项闭合（总册 §11.5）。开放项 `Q-SYNTH-01 / V-01 / V-02` 🟡 不拍板。

## 5. 观测与可追溯

- 埋点：沿用 FE `synth_vit_*`；服务侧每次装包记 `trace` 日志（region/compare/window/batch_id/耗时/缺行数）。
- 血缘：每表 COMMENT 登记源（兄弟指标 / gapfill 表 / Nebula 导出），data-agent DDL 落地时写入。
- 批次追溯：响应同时给不可变 `snapshotId` 与 `calc_batch_id`；页面 ⓘ 可回查批次。

## 6. 验收条件

1. 默认三元组快照 200 且字段与 MOCK-INV §1 同构；非默认 404。
2. 任一缺行：null+reason+confidence。权重表无行时不得填入三档向量。无 0 填充、无随机数。
3. 只读 `succeeded` 批：构造一条 `running`/`failed` 批数据不被读取（自检脚本断言）；三权重方案（`WEIGHT_MAIN`/`INDEX_MAIN`/`EQUAL`）行并存互不覆盖，`synth_vit_index` 与 `synth_vit_weight` 同 profile 配对读取（断言 index 用的权重与 weight 表该 profile 行一致）。
4. **profile 规则**：未传 `weight_profile` → 响应/装包为 `INDEX_MAIN`；传 `EQUAL`/`WEIGHT_MAIN` 时 index/dim/weight/rank **四表同码**；非法枚举 400；报告字段与快照 `weight_profile` 一致。
5. **指纹**：同条件先跑 `EQUAL` 再选 `INDEX_MAIN` → **不得**复用等权任务；四段 fp 断言。
6. **旧任务**：无权重/方法信息的三段任务标 `legacy_unknown`；新 `INDEX_MAIN`（含缺省）请求 **必须重新分析**，不得复用该旧任务。
7. **snapshotId**：批 A 发布后同条件再跑批 B → B 的 `snapshotId` ≠ A；用 A 的 `snapshotId` 仍读 A 批（`calc_batch_id` 不变）；`cache_key` 可改指 B。
8. 重跑生成新批次，旧批可回溯；`is_mock=1` 行页面 🧪。
9. 五阶段文案与 MOCK-INV §2 逐字一致。

## 7. 实现单/文件边界（并行分配）

| 动作 | 仓/文件 | 归属 |
|---|---|---|
| 5 张 ADS DDL + 预填脚本 | `lumen-algo-py/scripts/mysql/synth_vit.sql` + `seed_synth_vit_*.py`（库 `demo_gkxlumenx_ads` / `gkxlumenx_ads`） | data/算法并行线 1 |
| 装包读表改造 | `vendor/entan-py` synth 装包函数 | 算法线 1 |
| 快照/任务接口 | 已有 VIT-PY/BE 单范围（本册不重复） | 既有五单 |
| gapfill 输入 | 既有 GAPFILL 两单 + DBA 单 | 既有五单 |

## 8. 会签

| 角色 | 状态 |
|---|---|
| 架构 | 已签-架构（2026-11-05）：**可签**。五张 ADS 表 D18 三要素齐（表名/灌数方/读取接口）；`snapshotId` 不可变 ≠ `cache_key`、`legacy_unknown` 禁复用、权重缺行禁常量均合规。保留意见 AR-6（五表同批写入的跨表原子性：册内只定义单表批次状态机，建议 seed 以同 `calc_batch_id`+同批次时间戳写五表、校验失败整批同置 `failed`，写进实现单验收）与待确认 TC-2 见 `agent-delivery/agent-handoffs/LUMEN-INTEL-SDD-SIGNOFF-L01.md`，不挡签 |
| 算法 | 未签 |
| 数据 | 未签 |
| 产品 | 未签 |

## 9. 修订

| 版本 | 日期 | 说明 |
|---|---|---|
| v0.1 | 2026-11-04 | 首版骨架 |
| v0.2 | 2026-11-04 | 评审修复：每表四项（粒度/唯一键/写入/读批）、异常空态枚举、血缘/观测/验收五条、文件边界表、权重缺行策略对齐总册 §11.4 |
| v0.3 | 2026-11-04 | 第二轮审核对齐：批次排序 `calc_batch_created_at`（禁字符串比较）；权重 `weight_source='calc_logic_placeholder'` 口径 |
| v0.5 | 2026-11-04 | 第四轮审核收敛：权重标识统一 `calc_logic_placeholder`；双权重方案并存（`placeholder_equal` 等权 / `calc_main` 主口径 0.30/0.30/0.20/0.20），index/dim_score/weight 唯一键加 `weight_profile_code` |
| v0.6 | 2026-11-04 | 第五轮审核收敛：index/rank 唯一键补 `weight_profile_code`（dim_score/weight 已有）；权重三方案对齐 calc-logic 实核（WEIGHT_MAIN 0.30/0.35/0.20/0.15、INDEX_MAIN 0.30/0.30/0.20/0.20、EQUAL 等权），index 与 weight 同 profile 配对 |
| v0.7 | 2026-11-04 | 第六轮收敛：dim_score/weight 行数改 ≤12（3 方案×4 维）；验收补三方案并存与配对读取断言 |
| v0.8 | 2026-11-04 | 第七轮收敛：`synth_vit_weight` 补 `weight_provenance_metric_id`（INDEX_MAIN 行归属指数件口径），避免口径误归 |
| v1.0 | 2026-11-05 | 头部对齐总册 v1.0-draft（正文口径已在 v0.8，本版只统一版本引用） |
| v1.0.2 | 2026-11-05 | P2：补 `weight_profile` 参数枚举、默认 `INDEX_MAIN`、同请求四表+报告同 profile；验收加断言 |
| v1.0.3 | 2026-11-05 | 活力 `analysis_fp` 升级四段含归一 `weight_profile`；冻结/复用/缓存/报告匹配同步；旧三段≡INDEX_MAIN 兼容 |
| v1.0.4 | 2026-11-05 | 废止旧三段≡INDEX_MAIN；按权重/methodVersion 识别，否则 `legacy_unknown` 禁复用；`snapshotId` 不可变含批次，与 `cache_key` 分离 |
| v1.0.5 | 2026-11-05 | 会签退回：五张改落 ADS；权重缺行禁常量；快照增加可选 snapshotId |


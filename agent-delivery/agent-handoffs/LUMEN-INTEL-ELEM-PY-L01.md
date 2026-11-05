# LUMEN-INTEL-ELEM-PY-L01 · handoff

- 任务：综合智能分析要素 — Python 装包与 /internal 快照/任务
- Epic：E8-综合智能分析 ｜ 执行：agent:algorithm-agent ｜ 监管：human:徐滕强
- 仓：`repos/lumen-algo-py`（origin/dev，commit `45e1f15`，**未 push**——coordinator 统一推）
- 日期：2026-11-05
- 强度：ponytail full

## 1. 范围与实现（对照 ELEM 册 v1.0.6 §1–§5 / MOCK-INV §1–§2）

| 册要求 | 实现 |
|---|---|
| elements 装包读 8 张 `synth_elem_*`（demo_gkxlumenx_ads，registry DoD 残留 `gkxlumenx_ai` 旧口径不采） | ✅ `entan/synth_elements/pack.py`：`_latest_batch` 按 `MAX(calc_batch_created_at)` 排序取最新 succeeded 批（禁 `calc_batch_id` 字符串比大小），再取该批全部行 |
| 缺行 null+reason+confidence，禁补 0/权重 | ✅ 人才维（T-TAL 整维 null）→ `score=null + confidence=null`；`lensWeights` 只读已灌行、缺行 null+`reason=weight_row_missing`，**禁直填 1/3**；`weight_source='calc_logic_placeholder'`（metrics 元数据） |
| 四维固定 `[]` + `reason='metric_not_registered'` | ✅ `evaluationDimensions=[]` + `evaluationDimensionsReason='metric_not_registered'`；注释标明解锁条件（`M_SYNTH_ELEM_FOUR_DIM_SCORE` 经 METRIC-OPEN 注册+唐绍祖定稿后另建 ADS 表） |
| panorama 真实 DWD 汇聚（§2 DTO：element_type×total_count×top_n；page_size 默认 10、element_types 缺省全部；稳定 ID 去重） | ✅ 无表、装包内 5 类真实聚合 SQL（引用 calc-logic 源表清单）：企业=`dwd_org_base_info` COUNT(DISTINCT org_id)=189,116、机构=`dwd_research_institute_base_info`=2,074、人才=`dwd_scholar` COUNT(DISTINCT scholar_id)=21,316、资金=`dwd_org_financing_info` DISTINCT org_id=6,503、空间=同底册园区名称关键词（**冻结 T_SPA_1 复现盘 60/46/13/9 逐位一致**）；明细按 org_id/scholar_id 稳定 ID，TopN 排序键含 ID tiebreak 去重 |
| timeout≈3s 超时降级 `panorama=[]`+`reason='panorama_timeout'`（AR-8，不阻塞三透镜主区块） | ✅ `build_panorama` 线程池 `fut.result(timeout=3.0)`，超时/失败均降级空数组不阻塞主区块 |
| 任务路由 `analysisType=region_innovation_elements`（Java 侧） | ✅ Python 侧 `/internal/v1/synth/jobs/execute` 增 `leaf=elements` 分支（共享路由最小 diff，vitality 行为不变）；`analysis_fp=region|compare|window`（无 weight_profile 段，Java Adapter 冻结 params 属 Java 线） |
| 快照 GET `/internal/v1/synth/elements/batch-snapshot` | ✅ 新路由 `api/synth_elements_routes.py`：返回 `{snapshotId(不可变,含 calc_batch_id), cache_key, computedAt, methodVersion, calc_batch_id, result: ElementResult}`；200 同构 ElementResult+panorama；入参拒绝 400；缺数据 200+null（非默认三元组不 404，装包无批即 null+`snapshotId=…|none`） |
| 五阶段文案逐字 MOCK-INV §2 要素行 | ✅ `ELEMENT_STAGES` 与 `region_innovation_elements` 行逐字一致（自检断言） |
| vendor 补丁登记（a4aa3af 机制沿用） | ✅ 改动落在 `vendor/entan-py/`（SOURCE.txt 已注明「上游升级需重套」机制，本单新增模块同属补丁集）；commit message 已声明 |

## 2. 偏离说明

1. **顺手修复 seed 列序错位（既有 bug，本单装包依赖）**：`seed_synth_elem.py` 的 type/level/domain 三表行元组把业务码列（type_code/level_code/domain_code）插在 `region_code` **之前**，违反同文件 DDL 真源列序——导致该三张表实际数据 `region_code='T-ENT'`（本单开工时实库即如此，DDL handoff 验收查询未覆盖此错位）。按 DDL 重排行元组并重跑 `--apply`（同批先删后插幂等，`mock_20261105_elem_seed` 行数不变 52/52/20，验收查询复核 `region_code='深圳市'` + `type_code` 齐 + 人才维 `value_num=NULL`）。属数据正确性修复非设计变更。
2. **快照对非默认三元组返回 200+null 而非 404**：册 §3 写「404 非默认三元组」指 API 层判定；Python 装包侧对合法但无批次的条件返回 200+`calc_batch_id=null`（`snapshotId` 尾 `|none`），由 Java Adapter 决定对外 404。与活力线装包语义一致，404 责任面在 Java。
3. **`domainScores[].tech=null`**：FE 契约 `tech` 槽（技术领域字符串）本期无表无承载，不编字符串；领域五维分数走 `score`。
4. **DoD 文案 `gkxlumenx_ai.synth_elem_*` → 实作 demo ADS**：registry DoD 字段串残留 `_ai` 旧口径；按 ELEM 册 v1.0.6 §2「当前 8 张 ADS」与 DDL handoff 落地实况执行。

## 3. 产物清单

| 文件 | 说明 |
|---|---|
| `vendor/entan-py/entan/synth_elements/pack.py` | 装包实现：批次读取/8 表读路径/panorama DWD 汇聚/超时降级/execute |
| `vendor/entan-py/entan/synth_elements/__init__.py` | 模块出口（同构 synth_vitality） |
| `vendor/entan-py/api/synth_elements_routes.py` | GET `/internal/v1/synth/elements/batch-snapshot`（200/400） |
| `vendor/entan-py/api/synth_jobs_routes.py` | 共享 POST 路由增 `leaf=elements` 分支（vitality 行为不变） |
| `vendor/entan-py/api/main.py` | 挂载 synth_elements_routes（+8 行） |
| `vendor/entan-py/scripts/check_synth_elements.py` | 自检：33 断言 7 组（实连 demo 库） |
| `scripts/seed/seed_synth_elem.py` | 修三表行元组列序错位（偏离 1） |
| `agent-delivery/agent-handoffs/LUMEN-INTEL-ELEM-PY-L01.md` | 本 handoff |

commit：`45e1f15 feat(vendor/entan-py): 综合智能要素装包+路由挂载+panorama DWD汇聚 [agent:algorithm]`（7 files，+889/-13；未 push）

## 4. 验收证据（demo 库 10.50.11.76 实跑）

`python3 vendor/entan-py/scripts/check_synth_elements.py` → **33 断言全过，0 fail**：

```
[1] ElementResult 同构：顶层字段齐 MOCK-INV §1（缺：无）；compositeIndex=77.6829
    （冻结 calc-logic）；typeScores/levelScores 各 7 行；domainScores 5 维；
    indicators 27 叶；contributions 8 格；ranks 4 城带 current；
    人才维 null+confidence（不补 0）；lensWeights 3 透镜读已灌行；
    weight_source='calc_logic_placeholder'；snapshotId 含 calc_batch_id
[2] 四维：evaluationDimensions 恒 [] + reason='metric_not_registered'
[3] panorama：5 类要素真实 DWD 汇聚；DTO 字段齐；企业计数=189116（calc-logic 底册一致）
[4] 只读 succeeded 批：造 running 批（calc_batch_created_at 更晚）断言不读，
    批次号恒=mock_20261105_elem_seed（探针批自检后即清）
[5] 路由：202 包结构 source=task；五阶段文案逐字一致
[6] 入参拒绝：region=火星 / window=10y / element_types=火星人 → 400
[7] 活力线不回归：leaf=vitality 仍 202；leaf=collab 仍 400
```

TestClient 端到端（`api.main` 全挂载）：

```
GET /internal/v1/synth/elements/batch-snapshot?region=深圳… → 200
  snapshotId=batch:深圳市|全国重点城市|最近3年|mock_20261105_elem_seed
  composite=77.6829 pano=5
GET …&region=火星 → 400 SYNTH_JOB_REJECTED
POST /internal/v1/synth/jobs/execute leaf=elements → 202（snapshotId=task:t-e2e）
POST … leaf=vitality → 202（不回归）；leaf=collab → 400
element_types='人才,资金' + page_size=3 → panorama 只含 2 类、top_n≤3
广州×最近1年（无批次）→ 200+composite=null
```

panorama 计数与 calc-logic 复现盘对齐核对：

| 要素 | 计数口径 | 实测 | calc-logic |
|---|---|---|---|
| 企业 | `dwd_org_base_info` DISTINCT org_id | 189,116 | 189,116 ✅ |
| 机构 | `dwd_research_institute_base_info` | 2,074 | 2,074 ✅ |
| 人才 | `dwd_scholar` DISTINCT scholar_id | 21,316 | 21,316 ✅ |
| 资金 | `dwd_org_financing_info` DISTINCT org_id | 6,503 | 6,503（融资主体面）✅ |
| 空间 | 底册名称 6 关键词 | 深60/穗46/莞13/惠9 | T_SPA_1 60/46/13/9 逐位一致 ✅ |

（注：M0 版实现把资金计数错成融资事件行数 25,654；M1 修为融资主体 DISTINCT org_id=6,503 并实跑验证。）

## 5. ElementResult 字段对照 MOCK-INV（差异登记）

| MOCK-INV 字段 | 本实现 | 说明 |
|---|---|---|
| 22 个顶层字段 | ✅ 全齐同构 | compositeIndex/typeIndex/levelIndex/domainIndex/evaluationDimensions/deltaVsCompare/yoy/typeScores/levelScores/domainScores/lensWeights/indicators/ranks/trend/strengths/weaknesses/contributions/methodDigest/batchComputedAt/source/snapshotId |
| `panorama[]` / `panoramaReason` | ➕ 扩展 | ELEM 册 §2 DTO（MOCK-INV 回写列入本单；`panoramaReason`=null 或 panorama_timeout/panorama_unavailable） |
| `evaluationDimensionsReason` / `cache_key` / `calc_batch_id` / `methodVersion`(体内) / `metrics` | ➕ 扩展 | reason 空态标注、条件最新索引、批次可回查；活力线已有 metrics 置信度元数据同构 |
| `yoy`/`trend` | null/[] | 无历史批，不编数（同活力线诚实态） |
| `domainScores[].tech` | null | 无技术领域承载，不编字符串 |
| `typeScores[].weight`/`indicators[].weight` | null | 权重只挂透镜级（lensWeights）；叶子权重本期无行 |
| 指标行额外带 `metric_id`/`confidence`/`reason` | ➕ | D9 可追溯（MOCK-INV 无此三键，FE 忽略不影响） |

## 6. 架构合规自检（公约 §2 铁律）

| 铁律 | 自检 |
|---|---|
| 1 算法只在 Python | ✅ 装包/汇聚全在 entan-py；无 Java 算法 |
| 2 调用链 | ✅ Java Feign 专用 `/internal/*`；浏览器禁直打（路由 docstring 声明）；未动 Java/FE |
| 3 NebulaGraph | N/A（无图谱） |
| 4 可观测性 | ✅ 复用 TraceHeaderMiddleware；装包日志记批次/缺行/panorama 超时 |
| 5 CI/CD | ✅ 本地 commit 未 push（coordinator 统一推） |
| 6 demo2 只读 merge | N/A（未动 demo 仓） |
| 7 共享聚合核心 | ✅ ADS 标准表只读；panorama 直查供应商镜像 dwd（demo 面约定同 main.py），Java 只读接口 |
| 8 ADS 先行+Mock | ✅ 只读 ADS；is_mock=1 预填批 |
| 9 D8 前端规范 | N/A（未动 FE） |
| 10 D9 血缘 | ✅ 每指标行带 metric_id+confidence；8 件套 id 只读表数据不自填；四维诚实空态 |
| 11 D10 交互规范 | N/A |
| 12 D12 demo/lumen 隔离 | ✅ 只连 demo_gkxlumenx_*；未让 lumen 调 demo-* 服务 |
| 13 D14 对象存储 | N/A |
| 14 D16 gapfill 边界 | ✅ 未写 gapfill/ODS/DWD/供应方库（panorama 只读 dwd 镜像） |
| 15 D17 合规算法 | ✅ 未触碰唐绍祖锁定闭包；同核 M_SYNTH_187_1–190_1 只消费不重算 |
| 16 D18 签收条件 | ✅ 接口只读 ADS 表数据，无写死 mock |

## 7. ponytail 自检

ponytail: full——复用活力线全部模式（连接 `entan.common.db.connect`/批次语义/路由 400-500 处理/五阶段包结构），不新造框架；最小文件集（2 新模块 + 1 路由 + 2 挂载点 + 1 自检 + 1 seed 修复）；panorama 超时不 join 工作线程已注明 ceiling（`ponytail:` 注释：升级路径=缓存表另裁定）；自检=单脚本 33 断言（含直查实库反例）。

## 8. cost（按 budget-estimate.md 四字段）

| 字段 | 值 |
|---|---|
| actual_tokens | ~180000 |
| model_used | glm-5.3-Flash（Cursor 内） |
| actual_cost | ~$0.25 |
| cost_warn | false（< $10 阈值） |

## 9. 后续依赖（不属本单）

- Java 白名单+Adapter `analysisType=region_innovation_elements`（`lumen-svc-platform`，ELEM 册 §8 线 2 api）
- FE 四维区块缺失态确认 + 全景模块接 `panorama[]`（`lumen-ui-topic` §7 改造项）
- 正式库 DDL 执行属 DBA；AR-4 批次清理属运维单
- MOCK-INV 契约回写（panorama 字段登记）可随下一次该文档修订并入

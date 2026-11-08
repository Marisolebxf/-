# TA-L2-DS13 全球领域人才态势 · 演示样本循环（LOOP）计划（阻塞型）

> 依据：`产品实现规程.md` §6.5（含 §6.5.7）。用例真源：`../合规演示用例/TA-L2-DS13-合规演示用例.md`（23 行，R1 已判 15 可演 / 8 部分可演）。
> 验收单：`TA-DS13-DEMO-ACCEPT-LOOP`。监管人：human:李伟。
> 现状：**R1 完成 · 可申请签收** —— 缓存止血方案已发布并实测生效（global 3.3s / profile 1.5s / recommend 1.9s，均 `code=0` 无 `emptyReason`）；8 条部分可演均为供数缺口，页面走空态不伪闭合。

## 状态行（每轮回写）

| 轮次 | 日期 | 探测 | 对得上 | 缺口 | 子任务 | 结论 |
|---|---|---|---|---|---|---|
| R0 | 2026-11-09 | `POST .../situation/talent/global/dataset` → 200 但 `DOWNSTREAM_UNREACHABLE`，耗时 **60.1s** | 0 / 23 | BLOCKED-DS13-01 下游断链；BLOCKED-DS13-02 超时 | 待久新 | **blocked，不进 LOOP** |
| R0b | 2026-11-09 | 路径更正后 `GET {网关}/display/v1/talent/global/dataset` → 200 / **61.1s** / 110B，`emptyReason=DOWNSTREAM_UNREACHABLE` | 0 / 23 | 根因修正：非「无数据/无实现」——本地/开发 2026-11-07 同一聚合 **29.8s 成功（regions=24 / flows=600）**；生产耗时越过 Feign 读超时即降级空态。`build_global_dataset` 每次请求实时全表聚合、**无缓存/无预计算** | 待久新 + 预计算落地 | **blocked 维持**；待生产 show-py 日志确认是超时还是 Doris 连接错误 |
| R1 | 2026-11-09 | `GET {网关}/display/v1/talent/global/dataset` → 200 / **3.3s** / 454.9KB，`code=0` 无 `emptyReason`（profile 1.5s / recommend 1.9s 同绿） | **15 / 23**（8 部分可演） | 供数缺口 G-DS13-01~06：engineer 恒 0（探针确认 taxonomy 无工程节点）、动态仅 `media` 单型且无「近一周/近一月」时间窗控件、机构核心成果/关联专家空、画像项目级别/经费分项与合作表空（专利经探针排除）、学术力分项恒 0 | 无阻塞子任务 | **R1 完成·转需规核对 → 待监管人签收** |

## 1. 探测（每轮第一笔，只读）

- `GET {网关}/display/v1/talent/global/dataset`（无查询参数）；头同其它页。
  ⚠️ **2026-11-09 路径更正**：原记 `POST .../situation/talent/global/dataset` 实测 **404**；正确为 `GET /v1/talent/global/dataset`（`TalentController` L44–47），`POST` 同路径返回 405。
- **必须记耗时**：单次调用 > 30s 即记性能缺口（与断链分开记，两条独立缺口）。
- **熔断**：`DOWNSTREAM_UNREACHABLE` → 记 blocked，连续三轮仍断 → 上报监管人升级（§6.5.7 步 9）。

## 2. 阻塞解除前置（三条全满足才转常规 LOOP）

| 前置 | 验收口径 | 责任方 | 状态 |
|---|---|---|---|
| P1 下游通道恢复 | `talent/global/dataset` 返回真实业务体（非 `DOWNSTREAM_UNREACHABLE`） | 久新 | ✅ 2026-11-09 达成（444.2→454.9KB 真数据） |
| P2 超时治理 | 单次响应 ≤ 5s，或改为异步任务 + 轮询；60s 同步调用不可演示 | 后端 + 久新 | ✅ 3.3s（整页 TTL 缓存 + 预热；目标态仍推预计算快照） |
| P3 用例 23 行零未填 | M2/M3 判定补齐 | 用例侧 | ✅ R1 已逐行判定（15 / 8 / 0） |

## 3. 解除后的判定与退出

转常规 LOOP（同 DS-03 计划 §3）：全过 → 状态行回写 → 需规核对（23 行）→ 等监管人签收；有缺口 → 分类建子任务；只读不签发；同页同条件单飞。

**本页额外强制**：P2 未达成前即使通道恢复也不得进演示（一次 60s 等待足以毁掉整场演示）。

## 4. 已知记录

- **200 不等于可用**：本页是「状态码 200 + 业务断链」的典型，判定必须看响应体 `DOWNSTREAM_UNREACHABLE`。
- **2026-11-08 复测仍断**：非瞬时抖动，不要靠「再试一次」掩盖。
- 本页当前不计入演示脚本。
- **2026-11-09 根因分析（R0b）**：
  - 实现是完整的：`gkxlumen-display/TalentController#globalDataset` → Feign → `gkx_show_service` `/internal/gkx-show/talent/global-dataset` → `talent_datasets.build_global_dataset()`；开发环境 2026-11-07 日志有多次成功（`regions=24 flows=600`，预热耗时 **29.8s**）。
  - 生产返回的 `emptyReason` 是 Java 侧**统一降级文案**（`TalentController#emptyDataset`），既覆盖下游超时，也覆盖下游报错 → **不能据此断定「久新通道彻底断」**。
  - 生产 61.1s 属「等满读超时再降级」，与本地 29.8s 成功相冲突，指向 **聚合过慢 + 无缓存**（`build_global_dataset` 每次请求实时扫 `ads_talent_profile` 等多张全量表，约 500 行聚合逻辑，无 TTL 缓存/无预计算）。
  - 待确认项：生产 show-py 是否有该请求的错误栈（超时 / Doris 连接失败 / OOM），需运维或 k8s 日志取证后二选一收敛。
- **可执行修复路径（按优先级）**：① 预计算落快照表（ETL 每日刷，接口只读快照，目标 ≤5s）— 与本项目 DS-14/16 的 precompute 同型；② 加进程内 TTL 缓存 + 启动预热（止血，1 天内可验证）；③ 拆 Tab 懒加载（按子页分块聚合）；④ 单纯调大 Feign 超时**只能消除空态、不能达到可演示标准**（P2 要求 ≤5s）。
- **B 已实现（2026-11-09，`lumen-topic-py` 本地未发布）**：
  - 新增 `gkx_show_service/dataset_cache.py`（`TtlCache`：命中直返 / 过期 stale-while-revalidate / 冷启动单飞 / 失败不写缓存）；`views/talent_dataset.py` 四页接入各自缓存并导出 `WARMERS`；`main.py` 启动后台线程按 `global→region→profile→recommend` 预热并每 300s 续期（TTL 由 `GKX_SHOW_TALENT_CACHE_TTL` 控制，默认 1800s）。
  - 自检：`TtlCache` 四组用例全过（冷启动单飞、并发只算一次、过期返旧值+后台刷新、失败透传不缓存）；`py_compile` + 导入校验通过（`WARMERS=['global','region','profile','recommend']`）。
  - **待验证（发布后端到端）**：show-py 发布 → 预热日志出现 `[cache] talent/global refreshed in ~30s` → 生产复测 `GET /v1/talent/global/dataset` 应 <1s 返回真数据（非 `DOWNSTREAM_UNREACHABLE`）；届时按 §2 前置三条转常规 LOOP R1。
- **R1 实测（2026-11-09，B 方案发布后）**：
  - 三端点均绿：global **3.3s / 454.9KB**、profile 1.5s / 380.4KB、recommend 1.9s / 508.9KB，`code=0` 且无 `emptyReason`；`regions=24`、`migrationFlows=600`、`heatData=600`、`activityFeed=30`、`topInstitutions=20`、`regionTree` 全球→12 国→64 城。
  - 23 行判定：**15 可演 / 8 部分可演 / 0 待开发完成**（明细见用例文末「LOOP 对照汇总（R1）」）。
  - 8 条部分可演全部是供数缺口（G-DS13-01~06），非接口/实现缺陷；页面按期望走空态或降级，不补 0、不编造。
  - 遗留建议：预热线程目前无条件执行，若后续有按模块灰度需求再加 readiness 门控；`TtlCache.get` 等待刷新无超时保护（当前实测无影响）。
- **R1.5 本地修复（2026-11-09，代码未发版）**：P0 六项服务侧修复落地并本地复验 —— W1-2S 学历归一化（24 城 doctor 401→7,537 / master 179→680 / bachelor 233→341）、W2-1 关联专家（20/20 家、60 人）、W2-2 机构成果（20/20 家、每家 2 条事实统计）、W4-3/W4-4（hot 0.28–0.96、align 43.5–83.2）、W5-1 国际合作（15/15 人、90 行）；本地四端点 200（global 55s 冷建 / profile 19s / region / recommend）。**待发版后复跑 R2，再按生产实测值更新 23 行数据情况**。未做：W2-3（前端无 `education` 字段）、W3-1（前端枚举为 `paper/job/project/award/event`，与后端原稿不符且无月粒度）、W3-2（前端无来源列）。新记缺口 G-DS13-07：机构专利表每机构 ≤20 条采样。

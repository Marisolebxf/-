# CHAIN-ODS-SYNC-L01 · 产业链数据同步（三方 gkx → Demo ODS，replace 全量）

- 任务：`CHAIN-ODS-SYNC-L01`（feature，P1，L/8 点）
- 执行：`agent:algorithm-agent`｜监管：`human:徐滕强`（2026-10-29 人确认改派：claimed_by 与 supervised_by 均为徐滕强；建单初稿口径为 human:淮政玮，已作废）
- 仓库：`demo-algo-science`（主实现）+ `demo-ui-system-test`（产业链基础指标页按钮）
- 分支：两仓 `origin/dev` 直推（禁 main、禁 force）
- 强度：ponytail full（可观测/幂等/进度回传/写门禁均按铁律交付，未用 YAGNI 裁剪）
- 口径：**2026-10-29 人确认，mode=replace**（TRUNCATE 后全量；UI 只暴露「清空后全量同步」一档；覆盖建单初稿 upsert 差集）

## 1. 范围与实现（对照建单交付清单）

| 清单项 | 产物 | 状态 |
|---|---|---|
| `chainan/llm_ods/ods_sync.py` | 新增（replace 同步核心：keyset 分批 + 日期清洗 + 写门禁 + on_progress） | ✅ |
| `POST /internal/industry/sync-ods` | `api/main.py` 新增（body `{mode:"replace"}`，后台线程，`_sync_state` 互斥） | ✅ |
| status 扩展 | `GET /internal/status` 并入 `sync_running/last_sync/last_sync_error/last_sync_cost_s/last_sync_mode/last_sync_tables`（table/written/todo/skipped/truncated） | ✅ |
| UI「数据同步」按钮 + 四步说明弹卡 | `src/views/chain/pages/BasicPage.vue`（复用 SeedHelpBadge）+ `src/api/chain/index.ts` `runChainOdsSync()` | ✅ |
| 离线自检 | `tests/test_chain_ods_sync_dates.py`（日期转换 7 例 + 批清洗 1 例 + keyset 分页漂移 1 例 + 门禁/口径 3 例 = 12 例全绿） | ✅ |
| handoff + cost 回填 | 本文件 + MCP `task-update-fields` | ✅ |

### 调用链（架构铁律 2/12 合规）

```
UI(数据同步按钮) → 网关 /chain/internal/** (StripPrefix=1, 直连 innov-py, 网关注释明示「灌数/状态仍走此路由」)
→ Python POST /internal/industry/sync-ods（后台线程）
→ 三方 gkx 183.240.141.251:3318（只读）→ demo_gkxlumenx_ods 四表
Java 零改动（demo-svc-platform 与 lumen-svc-platform 均未触碰；lumen 前端调用链不涉本功能，D12 合规）
```

### 关键行为

- **replace 语义**：逐表 `TRUNCATE demo_gkxlumenx_ods.<t>` → 全量重灌；接口对非 replace mode 直接 400 语义拒绝（`只支持 replace`）。
- **列交集复制 + 跳 `_demo_id`**（`intersect_columns`，探针实测四表交集率 100%）。
- **大表流式**：主键游标（keyset `WHERE pk > last ORDER BY pk LIMIT n`，offset 漂移免疫）分批，批大小 `CHAIN_ODS_SYNC_BATCH`（默认 1000）；无主键表回退 SSCursor `fetchmany` 流式。禁一次性 `SELECT *` 入内存。
- **日期脏值**（源实探后定口径）：零日期/非法字符串 → 可空列 NULL（`publish_date`）、NOT NULL 列兜底 epoch(1970-01-01)（`created_time/updated_time` 目标列 NOT NULL、default=CURRENT_TIMESTAMP）；无法兜底行整行计 skipped 不中断。
- **互斥**：sync ↔ 灌数双向互斥（Python `_lock` 闸 + UI 按钮互禁 + 后端双向前置校验）。
- **live plane 禁用**：`is_live("chain")` 直接拒绝；写门禁 `assert_write_gate` 禁 gkx/DWD/ADS/非白名单，lumen ODS 需 `CHAIN_ODS_SYNC_ALLOW_LUMEN=1` 显式放行（默认禁用）。

## 2. 开工探针（handoff 硬要求）

源库 `gkx`（183.240.141.251:3318 只读）行数 + 目标列交集：

| 表 | 源行数 | 源列 | 目标列 | 交集 | 主键 | 脏日期 |
|---|---|---|---|---|---|---|
| dwd_industry_chain_info | 1,273 | 17 | 17 | 17 | pk_id | created_time **全列 1,273 行 0000-00-00** |
| dwd_org_industry_tags | **2,283,762** | 15 | 15 | 15 | dwd_id | 无 |
| dwd_org_industry_product_tags | 80,258 | 18 | 18 | 18 | dwd_id | created/updated_time 共 1,611 行 0000-00-00 |
| dwd_industry_chain_news_info | 108,052 | 16 | 16 | 16 | pk_id | 无（publish_date 可空、干净） |

目标 `demo_gkxlumenx_ods` 现存行：157 / 104 / 169 / 90（demo 假数据，将被 replace 覆盖——本同步即用于以真实贴源替换 mock）。

## 3. 真机全量验证（本机直连，等价服务端路径）

- 过程进度回包样例（`on_progress` → status 同构）：`[{chain_info written=1273 todo=1273 truncated=true}, {org_industry_tags written=2032000 todo=2283762 ...}]`
- **FINAL `{"ok": true, "cost_s": 1945.7}`**，四表明细：

| 表 | TRUNCATE | written | todo | skipped | 单表耗时 |
|---|---|---|---|---|---|
| dwd_industry_chain_info | ✅ | 1,273 | 1,273 | 0 | ~2s |
| dwd_org_industry_tags | ✅ | **2,283,762** | 2,283,762 | 0 | ~26min |
| dwd_org_industry_product_tags | ✅ | 80,258 | 80,258 | 0 | ~1min |
| dwd_industry_chain_news_info | ✅ | 108,052 | 108,052 | 0 | ~1.5min |

- **目标库行数复核**（同步后直查 demo_gkxlumenx_ods）：四表 dest 行数 = 源行数逐表相等（1273 / 2283762 / 80258 / 108052，全 OK）。
- **脏日期兜底复核**：`chain_info.created_time` epoch 兜底 1,273 行（=探针脏值数）；`product_tags.created_time` 兜底 1,611 行（=探针脏值数）。精确对账，无一行 skipped（全部可兜底）。
- 实测吞吐 ≈1,500~2,000 行/批窗口（跨公网 RTT 主导，单批 SELECT 0.15s + INSERT/commit）；总耗时 32.4 分钟。

## 4. 批大小选型理由

- 1000 行/批：228 万行 = 2,284 批，单批窗口 ~1MB 级（15 列×均值行宽），不动用 LONGTEXT 全表扫；跨公网 RTT 下单批 <1s，失败重试粒度小；对比 500 批次减半但单批内存翻倍、对比 2000 吞吐增益有限（RTT 主导）——默认 1000 居中，可用 `CHAIN_ODS_SYNC_BATCH` 调。
- 每批独立 commit：中断后已入库行保留（幂等恢复靠 replace 重跑，demo 口径可接受）。

## 5. 偏离说明

1. **监管人改派（人确认）**：建单初稿 `human:淮政玮`，2026-10-29 人确认改派为 `human:徐滕强`（claimed_by/supervised_by 同步更新）。按改派后口径执行，无实质影响。
2. **demo-algo-science 落后 origin/dev 20 提交**：`git pull --no-rebase`（merge）前本地 `conf/settings.yaml` 有未提交 host 迁移改动，与上游 `92faa5a`（同值替换）撞车——按多会话保护规约用 `git stash push`（未 drop，可恢复）后 pull。配置值与上游一致，仅差一行注释，不影响运行。
3. **UI 同步按钮三文件改动**（BasicPage.vue / api/chain/index.ts 新增封装）：`touched_files` 计划中的 `BasicIndicators` 无需改动（进度挂在既有 dataStatus 标签）。

## 6. 架构合规自检

| 铁律 | 结论 |
|---|---|
| 1 算法只在 Python | ✅ 同步逻辑全在 Python；Java 零改动 |
| 2 调用链 | ✅ UI → 网关 `/chain/internal/**` → innov-py `/internal/*`；未越层 |
| 3 NebulaGraph | ✅ 本功能不涉图谱 |
| 4 可观测 | ✅ 进度 status 轮询（written/todo/skipped/truncated）；关键路径 logger.info/warning；路由层 exception 落 last_sync_error |
| 5 CI/CD | ✅ push origin/dev 触发流水线 |
| 7 共享聚合核心 | ✅ 只写 demo_gkxlumenx_ods；不写 DWD/ADS、不直连 nGQL |
| 8 标准表先行 | ✅ 贴源进 ODS，替代 mock 假数据 |
| 12 demo/lumen 隔离 | ✅ lumen 仓零触碰；目标库写门禁白名单 |
| D9 指标 8 件套 | ✅ 本叶只贴源不入指标面（口径明确「到此为止」），无统计数字 UI 改动 |

## 7. 产物清单

- `demo-algo-science`：
  - `chainan/llm_ods/ods_sync.py`（新增）
  - `api/main.py`（+`/internal/industry/sync-ods`、status 并入 `_sync_state`、灌数入口加同步互斥闸）
  - `tests/test_chain_ods_sync_dates.py`（新增，12 例）
- `demo-ui-system-test`：
  - `src/api/chain/index.ts`（+`runChainOdsSync`）
  - `src/views/chain/pages/BasicPage.vue`（+同步按钮/四步弹卡/进度/互斥）

## 8. 验收证据

- 离线自检：`python3 -m pytest tests/test_chain_ods_sync_dates.py -q` → **12 passed**
- 路由冒烟：FastAPI 路由表含 `/internal/industry/sync-ods`（本机 import 断言通过）
- dry_run：四表 todo = 1273 / 2283762 / 80258 / 108052
- 真机全量：FINAL ok=true，cost_s=1945.7；四表 written=todo、skipped=0；目标行数逐表复核 OK；脏日期兜底数与探针精确对账（1273/1611）
- UI 构建：`pnpm build` ✓ built in 14.05s（本仓无 type-check 脚本）
- CI / K8s dev：
  - `demo-algo-science` pipeline **[3244](https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/demo-algo-science/-/pipelines/3244)**：py:smoke / py:image / **deploy:innov-py**（job 19877，跑在 3962041e）/ diag:k8s 全 success；`py:base-image` 为上游既有手动档（此前多次运行均未跑过、非本任务产物），本任务镜像直接复用缓存未触发。
  - `demo-ui-system-test` pipeline **[3245](https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/demo-ui-system-test/-/pipelines/3245)**：frontend:build / frontend:image / trivy / **deploy:k8s** / sync:feishu 全 success。
- 提交：algo `3962041`、UI `636cc68` + merge `8e71816`（pull --no-rebase，无冲突）。

## 9. cost（四字段）

- actual_tokens: 296000
- model_used: glm-5.3-Flash
- actual_cost: 1.2
- cost_warn: green

## 10. 代码评审（requesting-code-review，2026-10-29）

评审员子代理结论：**0 Critical / 3 Important / 5 Minor → Needs fixes（轻度，~15 行）**。Spec 轴 8 项零缺口；SQL 注入面/SSCursor 并发/每批 commit 幂等/UI 回包匹配等 8 项顾虑核查排除。同日修复并推送：

| 级别 | 问题 | 修复 | 提交 |
|---|---|---|---|
| I1 | 复合主键 keyset 只按首列推进会静默漏行 | `pick_pk()` 只认单列 PRI，复合/无主键降级 SSCursor 流式（宁慢勿漏）+ 新增测试 | algo `da0775d` |
| I2 | `_start_chain_pipeline` 锁外查 sync 后锁内不复查 → 竞态窗口 | `_start_chain_pipeline` 锁内补查 `_sync_state["sync_running"]` | algo `da0775d` |
| I4 | UI 轮询 600×3s=30min < 实测 32.4min | 预算 1200 次（≈60min） | UI `d445a3f` |
| m1 | written 计原始批大小（含被清洗丢弃行） | 两分支改 `written += len(clean_rows)`，written+skipped=todo | algo `da0775d` |
| m4 | keyset 测试写死 `rows[-1][0]`，测不出 pk 列错位 | 测试改用 `cols.index(pk)` 与实现同式 | algo `da0775d` |

修复后验证：自检 **13 passed**（+复合主键降级用例）、路由注册与 I2 守卫断言通过、UI `pnpm build` ✓ 12.39s。
未修（留档）：m2 既有灌数 UX 瑕疵（非本 PR 引入）、m3 门禁后缀式风格（白名单兜底仍闭合）、m5 无主键分支闲置（四表全有主键）。

ponytail: full——可观测（status 进度/错误回传）、幂等语义（replace 明示 TRUNCATE）、写门禁、互斥、大表分批均为铁律交付项，未裁剪；未新增任何第三方依赖（pymysql/pyyaml/fastapi 均为仓内已有）。

# SITUATION-ENT-D3-L01 · 执行任务清单

> 规格：同目录 `spec.md`。批准后按序执行；每项完成即回填证据。
> 纪律：不 commit / 不 push；改动停本地等人工验收。

## T1 后端 mock Provider
- [x] 新建 `repos/lumen-svc-platform/gkxlumen-display/src/main/java/com/topcomm/gkxlumen/display/support/SituationMockProvider.java`
  - `@Component`，常量 `SOURCE=mock` / `MOCK_REASON` / `MOCK_VERSION=d3-v1`
  - `supports` / `countOf`（journal 7200、meeting 1280）/ `unitOf`（种、场）/ `metadata` / `inScope`
- 验证：文件存在，无随机数、无 DB 访问。✅ 102 行，`Map.of` 冻结常量，无 Random / DB / Feign

## T2 `SituationController` 接线
- [x] 注入 `SituationMockProvider`
- [x] `buildFactorItems` 覆盖 journal/meeting：`active=true`、count、`source="mock"`、`mock/mockReason/mockVersion`
- [x] `buildStats` / `buildFactorCards` 追加 journal/meeting 两项（unit 种/场，带 mock 元数据，置后）
- [x] `buildRegions`：`layerOrder` 追加范围内 mock key；`layers` 含 mock key、`metrics` 不含；`heatKey` 只取有数值图层
- [x] 类头注释同步（期刊/会议 = 代码层 mock）
- 验证：`mvn -o -q -DskipTests compile` 通过。✅ `-pl gkxlumen-display -am compile` exit 0（258s，JDK17）；`active` 跟随勾选范围、`metrics` 零写入、`heatKey` 为 null 时沿用原分档

## T3 端点自检
- [x] 停掉 :7099 现有 java 进程 → 重新 `package` → 启动（注入 `GKX_JIUXIN_*` 的用户环境变量）✅ `mvn -o -DskipTests -pl gkxlumen-display -am package` BUILD SUCCESS（7m34s）；新 jar 于 17:15 产出并重启
- [x] POST `http://localhost:7099/v1/situation/map`（`{"enabledFactorKeys":["journal","meeting"]}`）✅
  - journal=7200、meeting=1280、`source="mock"`、`mock=true`、mockReason/mockVersion 齐
  - `regions[].layerKeys` 含 journal/meeting，`regions[].metrics` 无这两个键（深圳 metrics 空）
- [x] POST `.../overview`：stats/factorCards 含期刊 7,200 种、会议 1,280 场 ✅（顺序在 institution 之后）
- [x] 真实要素（paper/patent/scholar/project/institution/topic/result）`source` 不变、无 mock 字段 ✅（mock 字段计数=0）
- 备注：本地直连路径为 `/v1/situation/**`（服务 context path=`/`，无 `/display` 前缀）；前端经 `/api/display/**` 代理剥前缀，:3000 实走 code=0

## T4 前端类型与 MockBadge
- [x] `src/types/situation.ts`：`FactorItem` / `OverviewStat` / `OverviewFactorCard` 加可选 `mock/mockReason/mockVersion`
- [x] 新建 `src/review/MockBadge.vue`（`v-if="isReviewFeatureEnabled()"`，Arco Tooltip + `IconExperiment`，class `mock-badge`）
- [x] `src/review/index.ts` 导出 `MockBadge`
- [x] `src/review/README.md` 补包含项与清理清单（`MockBadge` / `.mock-badge`）

## T5 总览卡挂角标
- [x] `OverviewTab.vue` 卡值处加 `<MockBadge v-if="item.mock" ... />`
- [x] 不改其他布局/样式；`views/situation/**` 与 `styles/*.css` 其余 diff 为零
- 验证：`pnpm type-check`、`pnpm build` 通过。✅ 本机 `pnpm` shim 损坏（corepack 缓存），改用等价 `npm run type-check`（0 error）/ `npm run build`（✓ built 1m9s）；本次仅 `types/situation.ts` + `OverviewTab.vue` 两处业务 diff

## T6 页面实跑
- [x] :3000 打开科技全域态势 → 期刊/会议卡出现且数值正确；评审角标仅在 mock 数字旁；无业务 mock 字样 ✅（browser 实测：期刊 7,200 种 / 会议 1,280 场可见，紫色 IconExperiment 仅挂这两个数字旁）
- [x] 临时 `REVIEW_FEATURE.enabled=false` → 页面无 `.mock-badge` / mock 字样 → 恢复 `true` ✅（卡片数值仍在、flask 图标全消失、body.innerText 无 mock/示例/演示数据；验证后已恢复 true，`git diff feature.ts` 为空）

## T7 台账与 handoff
- [x] 新建 `agent-handoffs/科技发展态势-TS/mock-ledger.md`（跨页表头：数据块/要素 key/mock 文件与方法/生成规则/mock_version/真实源接替条件/清理条件/任务 ID；首条登记 D3）✅ 4 行登记（chips/卡/图层/角标）+ 检索方式
- [x] 新建 `SITUATION-ENT-D3-L01.md`（含变更清单、验证证据、ponytail + cost 四字段、去 mock 接真数路径）✅
- [x] `task-registry.yaml`：D3 / MOCK-LEDGER 状态与 repo/update_time 回写；`WBS.md` 175/176 行回写 ✅（两单 status=integration、evidence/cost/touched_files 齐）
- [x] YAML 校验（tasks 总数、ID 无重复）✅ tasks_total=1259、dup_ids=[]、两单 integration

## T8 收尾
- [x] 汇总 diff 清单；确认未 commit / 未 push；停本地等 `human:李伟` 走查 ✅（见下方 §收尾）

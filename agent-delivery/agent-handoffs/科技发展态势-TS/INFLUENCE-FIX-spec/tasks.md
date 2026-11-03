# INFLUENCE-FIX-L01 任务清单

> 审批人：`human:李伟`｜执行者：agent｜铁律：跑完停本地，**不 commit / 不 push**

## T1 后端：要素范围判定抽公共方法
- [x] `SituationController` 新增 `factorInScope(Map params, String factorKey)`（复用 `enterpriseInScope` 的 `enabledFactorKeys` 解析）
- [x] `enterpriseInScope` 改为委托 `factorInScope(params,"enterprise")`（行为不变）
- 验收：`enabledFactorKeys=["paper"]` 时企业卡不出现 ✅（实测仅出 1 张技术产出卡）

## T2 后端：机构卡纳入筛选 + 归一化
- [x] `buildInstitutionInfluenceCard(carriers, total, keyword)`：地域由调用侧传 `city`/`cities`；关键词结果侧 `name.contains`
- [x] `influence` 调用侧：按 `factorInScope("institution")` 守门；单选城市传 `city`（`GBA_SHOW_CITIES` 归一），全域传 `cities=GBA_SHOW_CITIES`；`sort_by=paper_count`
- [x] 新增 `institutionScore`：`100·(log1p(v)-min)/log1p 范围内 min-max`，全组相同取 50
- [x] `items[].score` = 0–100 归一化分；`items[].rawValue` = paper_count
- [x] `card.averageScore` = 归一化分均值；`metricLabel="相对影响力分"`；`count=null`；`countNote`/`caliberNote` 写入
- 验收：`items[0].score == 100`；`averageScore ∈ (0,100]`；`count == null` ✅（100.0 / 32.5 / null）

## T3 后端：补 3 类 mock 卡（5 类齐）
- [x] `SituationMockProvider` 新增 `technologyOutputCard`（含 paper/journal/patent 子类）、`influenceCard(key, scopeKey)`（scholar/service）、`scaledSeed`
- [x] 种子冻结 demo `influenceFactorCards`；`MOCK_VERSION=influence-v1`；`MOCK_REASON` 引用 xlsx 指标ID + 算法服务未上线
- [x] `influence` 装配顺序 technologyOutput → enterprise → institution → scholar → service
- [x] 卡片携带 `mock/mockReason/mockVersion`；`metricLabel` / `caliberNote`
- 验收：5 卡齐 ✅（端点全域 5 卡）；同参幂等 ✅；换 timeRange 值变化 ✅
- 备注：页面默认只出 4 类（服务项目卡不可达）——服务机构要素 `factorItems.active=false`（久新无服务项目计数、CMS `v_cms_svc` 未接线），已登记台账与 handoff §五

## T4 后端：契约字段修正 + 编译
- [x] `defaultFactorType` = `cards.get(0).factorType`（去掉硬编码 enterprise）
- [x] `totalCount` 跳过 null；`totalDefinition` 含 mock 口径说明
- [x] `mvn -o -q -DskipTests -pl gkxlumen-display -am compile` ✅ exit 0
- [x] Stop-Process 停 :7099 → package → 重启 → 轮询 LISTENING ✅（pid 73352）

## T5 前端：InfluenceTab 口径修正
- [x] 卡头 `metricLabel`；子类表头 `metricLabel`
- [x] `count` null → `—` + `countNote`
- [x] 公式注释改 `caliberNote + source`（删虚假复合公式）
- [x] scope strip `totalCount` null → `—`
- [x] 卡/详情挂 `MockBadge`（复用 `@/review/MockBadge.vue`）

## T6 前端：类型 + 三绿
- [x] `types/situation.ts` `InfluenceItem` 补 `metricLabel/countNote/caliberNote/rawValue/mock/mockReason/mockVersion`
- [x] `npm run type-check` ✅、`npm run build` ✅
- [x] `:3000` 实跑验收 ✅（4 类卡、机构「对象数量 —」+ 口径说明、无虚假公式改「口径注释」、切深圳市企业 51,379→23,834）
- [x] 评审关闭零泄漏回归 ✅（`.mock-badge` DOM 计数 0、无「代码层 mock」文案；验后恢复 `feature.ts` 且 `git diff` 0 行）

## T7 文档回写
- [x] `mock-ledger.md` 追加 3 行影响力 mock
- [x] `INFLUENCE-FIX-L01.md` handoff（mock 点 + 归一化待真实口径）
- [x] `task-registry.yaml` / `WBS.md` 登记（WBS-05-18-12，`status: integration`）

## T8 汇总
- [x] `git status` / `git diff --stat` 汇总改动
- [x] 确认未 commit / 未 push，等人工验收

# 任务依赖
- T2 / T3 依赖 T1
- T4 依赖 T2 / T3
- T6 依赖 T5 与 T4（需新 jar 提供契约字段）

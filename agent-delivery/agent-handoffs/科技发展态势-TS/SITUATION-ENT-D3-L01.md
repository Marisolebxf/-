# SITUATION-ENT-D3-L01 · 期刊 / 会议两要素代码层 mock

> **任务**：科技全域态势·D3——期刊 / 会议（数仓真无源，`ADS_SCHEMA.md` §24.10 明列缺失）以**代码层 mock** 落地：集中单一 Provider、非评审模式正常展示、评审模式 🧪 MockBadge
> **角色**：`agent:api-agent` · 监管人：`human:李伟`
> **状态**：`backlog → in_progress → integration`（改动停本地，**未 commit / 未 push**，待人工验收）
> **上位**：[SITUATION-ENT-D-维度打通任务单草案](./SITUATION-ENT-D-维度打通任务单草案.md) §3-D3 / §5 D-B；规格 [D3-spec/spec.md](./D3-spec/spec.md)（已批准）
> **挂接**：WBS §4.3（WBS-05-18-10） · 台账 [mock-ledger.md](./mock-ledger.md)（WBS-05-18-11，首条已登记） · 2026-11-01

---

## 一、交付内容（git 改动面 = 2 仓 7 文件）

| 仓 | 文件 | 改动 | 说明 |
|---|---|---|---|
| `lumen-svc-platform` | `gkxlumen-display/.../display/support/SituationMockProvider.java`（**新增**） | 唯一 mock 出口 | `@Component`；`SOURCE="mock"` / `MOCK_REASON` / `MOCK_VERSION="d3-v1"`；`supports` / `countOf`（journal 7200、meeting 1280）/ `unitOf`（种、场）/ `metadata` / `inScope`；无随机、无 DB、无外部调用 |
| `lumen-svc-platform` | `gkxlumen-display/.../display/controller/SituationController.java`（修改） | 4 处接线 + 注释 | `buildFactorItems`（覆盖 journal/meeting 为 active+count+mock 三元组）；`buildStats` / `buildFactorCards`（institution 后追加两卡，`mockStat`/`mockCard` 私有装配）；`buildRegions`（mock key 只进 `layerKeys`、**不进 `metrics`**；`heatKey` 只取有真实数值图层）；类头注释同步 |
| `lumen-ui-science-pc` | `src/types/situation.ts`（修改） | 3 个接口加可选字段 | `FactorItem` / `OverviewStat` / `OverviewFactorCard` 各加 `mock?` / `mockReason?` / `mockVersion?` |
| `lumen-ui-science-pc` | `src/review/MockBadge.vue`（**新增**） | 评审角标 | 根部 `v-if="isReviewFeatureEnabled()"`（DOM 零泄漏）；Arco `Tooltip` + `IconExperiment` `#7C3AED`；样式 scoped 自含；无「示例/演示/模拟」业务字样 |
| `lumen-ui-science-pc` | `src/review/index.ts`（修改） | 追加导出 | `export { default as MockBadge } from './MockBadge.vue'` |
| `lumen-ui-science-pc` | `src/review/README.md`（修改） | 清理清单 | 包含项加 `MockBadge`；清理清单加检索项 `MockBadge` / `.mock-badge` |
| `lumen-ui-science-pc` | `src/views/situation/overview/components/OverviewTab.vue`（修改） | 挂角标 | 卡值 `span` 后紧邻 `<MockBadge v-if="item.mock" :reason="item.mockReason" :version="item.mockVersion" />` + 一行 import；其余零 diff |

**`lumen-topic-py` 零改动**：py 层已把 journal/meeting 诚实声明为 `no_source`（`geo_indicator.py#UNSUPPORTED_FACTORS`），且设计约束禁止 mock 回填——mock 只落页面契约装配层（display）。

## 二、关键决策（spec §2 已批准）

1. **落仓 = display 层 Provider**，不改 py：py 是数据源层（缺数不造），display 是页面契约装配层；接真数时 Provider 换 Feign 调用即可，py 无需回滚。
2. **mock 值冻结自 demo 种子**：期刊 `7200 种`、会议 `1280 场`（`demo-ui-science/src/data.js` factorItems，2026-11-01 快照）；确定性、无随机。
3. **城市级零编造**：`regions[].layerKeys` 追加 mock key（保证可参与筛选、不触发「暂无数据」提示），但 `metrics` 绝不写 journal/meeting；`heatKey` 只取有真实数值的图层（企业开启时仍为 enterprise，否则取首个有值图层，全无则沿用原默认分档，不除零）。
4. **不接**：`/compare` 年度曲线、`/influence` 排名、导出、CMS 服务机构、专利；不改造既有卡顺序。
5. **D-B 裁定落地**：非评审模式正常展示（无 mock 字样、视觉与真实要素一致）；评审模式数字旁挂 🧪 MockBadge；`REVIEW_FEATURE.enabled=false` 时 DOM 零泄漏（根部 v-if，非 CSS 隐藏）。

## 三、验证证据（V1–V8）

| # | 验证 | 结果 |
|---|---|---|
| V1 | display 编译 | ✅ `mvn -o -q -DskipTests -pl gkxlumen-display -am compile` exit 0（258s，JDK17） |
| V2 | `/v1/situation/map` `{"enabledFactorKeys":["journal","meeting"]}` | ✅ journal=7200 / meeting=1280、`active=true`、`source="mock"`、`mock=true`、mockReason/mockVersion 齐；`regions[].layerKeys` 含两 key（深圳 `journal,meeting`）、`metrics` 无这两键 |
| V3 | `/v1/situation/overview` | ✅ stats/factorCards 含 `期刊 7,200 种`、`会议 1,280 场`，带 `mock=true`；顺序在 institution 之后（enterprise→paper→patent→talent→project→institution→journal→meeting） |
| V4 | 真实要素未受影响 | ✅ stats+factorCards 中非 mock 项带 `mock` 字段计数 = 0 |
| V5 | 前端类型门 | ✅ `npm run type-check`（vue-tsc）exit 0 / 0 error（本机 `pnpm` shim 损坏，等价走 npm，见 §五-3） |
| V6 | 前端构建 | ✅ `npm run build` exit 0（`✓ built in 1m9s`；仅 unocss/esbuild 既有告警） |
| V7 | 页面实跑 :3000 | ✅ browser 实测：期刊 / 会议卡可见、数值正确、紫色烧瓶角标仅挂这两个数字旁；经 :3000 代理 `/api/display/v1/situation/overview` code=0 |
| V8 | 评审关闭零泄漏 | ✅ 临时 `enabled=false`（HMR）：卡片数值仍在、flask 图标全消失、`body.innerText` 无 `mock` / `示例` / `演示数据`；验后恢复 `true`，`git diff feature.ts` 为空 |
| V9 | 台账 / handoff | ✅ `mock-ledger.md` 首条 4 行登记（chips / 卡 / 图层 / 角标）；本 handoff 含 ponytail + cost 四字段 |

## 四、契约变化（新增可选字段，向后兼容）

`/v1/situation/map` 的 `factorItems[]`、`/v1/situation/overview` 的 `stats[]` / `factorCards[]` 中，mock 项新增：

| 字段 | 值 | 说明 |
|---|---|---|
| `source` | `"mock"` | 真源标记（真实要素不带该值） |
| `mock` | `true` | 前端角标触发位 |
| `mockReason` | `数仓文档 §24.10 列为缺失：顶级会议/期刊名单未接入` | Tooltip 文案 |
| `mockVersion` | `d3-v1` | 种子 / 规则变更时递增 |

真实要素（paper/patent/scholar/project/institution/topic/result/service）**不带**这些字段（不伪标）。

## 五、排障与备注

1. **打包排障（复用 D2 经验）**：`package` 前必须先 `Stop-Process` 停掉 :7099 旧进程，否则 repackage 报「Unable to rename」。本次顺利：停旧 → `mvn -o -DskipTests -pl gkxlumen-display -am package` BUILD SUCCESS（7m34s）→ `java -jar --spring.profiles.active=local` 重启。
2. **本地直连路径无 `/display` 前缀**：服务 context path=`/`，curl 直连用 `http://localhost:7099/v1/situation/**`（`application-local.yml` 已把 `/v1/situation/**` 加进 `ignore-urls`，免 token）；带 `/display` 前缀会 401。前端走 `/api/display/**` 代理剥前缀，与生产网关行为对齐。
3. **本机 pnpm shim 损坏**（corepack 缓存缺 `pnpm.cjs`，既有环境问题）：T5 验证改用等价 `npm run type-check` / `npm run build`，与 `pnpm` 同脚本；`package.json` 曾被 corepack 误写 `packageManager` 字段，已还原（diff 为空）。
4. **中途 500 事故**：重打包窗口期（旧进程已停、新 jar 未启动）页面请求全部 500——用户现场发现并报告；重启后经 :3000 代理复测 code=0，恢复正常。

## 六、去 mock 接真数路径（接替条件）

1. 数仓接入「顶级会议 / 期刊名单」（`ads_venue_profile` 等表落地，`ADS_SCHEMA.md` §24.10 缺口关闭）。
2. `SituationMockProvider` 的 `countOf` / `unitOf` 换成 Feign 真实调用（调用点不变）；契约里 `mock` / `mockReason` / `mockVersion` 删除。
3. 按 [mock-ledger.md](./mock-ledger.md) 清理清单逐项核销；前端 `MockBadge` 因 `item.mock` 消失自然不再渲染，组件本体随评审层上线清理解除（见 `src/review/README.md`）。

## 七、Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | mock 集中单一 Provider（不散落）；`source/mock/mockReason/mockVersion` 契约完整；不给城市编造数值、不参与排名/计分/导出；评审关闭 DOM 零泄漏实测通过；台账同步登记；未用 YAGNI 裁剪诚实性字段 |

## 八、Cost（成本四字段）

| 字段 | 值 |
|------|-----|
| estimated_tokens | 90000 |
| actual_tokens | ~185000（规格探底 + 双仓实现 + 编译/打包/端点/浏览器五路验证，in+out 估算） |
| model_used | kimi-k3 |
| actual_cost | ~$1.8（估算） |
| cost_warn | green（< $5） |

## 九、改动停本地（人工验收闸门）

- 两仓全部改动**未 commit / 未 push**，停本地等 `human:李伟` 走查。
- 服务状态：display :7099 已用新 jar 重启（含 mock）；py :8082 未动；前端 :3000 dev 运行中。

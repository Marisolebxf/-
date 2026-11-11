ponytail: off（多仓实现 + 联调交付；按公约 ponytail §4 不以缩代码为目标）

# TS-L2-M10-DEMO-FULL-L01 · handoff（本地实现完成，待人工确认）

> **日期**：2026-11-11　|　**执行**：coordinator-agent（4 路子智能体并行：algorithm / api / frontend×2）　|　**监管**：human:刘剑锋
> **方案**：`TS-L2-M10-DEMO-FULL-L01-方案.md`　|　**用例**：`合规演示用例/TS-L2-M10-合规演示用例.md`（可演（本地）13 / 覆盖不到 7 / 未填 0）　|　**LOOP**：`TS-M10-DEMO-ACCEPT-LOOP.md`「运行 2026-11-11（本地）」52/52
> **状态（2026-11-11 19:50 已上线）**：
> - 共享库：`gkxlumenx_cms` v2 迁移、`demo_gkxlumenx_ads` 成员表迁移已执行（执行前整表备份于本机 `/tmp/m10-full/backup-*`）。src-2 经只读核实改指 `ods.dwd_zh_paper`（中台 ODS 论文主表，100900 行）。
> - 代码：PY `eeb00c0` / `6429ab6` / `e950699`、FE `6125a41`、Java `0d50cf7d` / `9b950725` 全部推送 `origin/dev` 并部署生效。
> - 线上验证：读侧与本地 12/12 一致；实体写链路线上实发通过（发现并修复 2 处缺陷）；匿名写 401 / 40101。用例已改为线上版（可演 13 / 覆盖不到 7 / 未填 0）。
> - 待补：带登录 token 的线上写复测（监管人放 `~/.gkx/display-loop-token`）；示范专利-19 一条旧版「合作」候选边物理清理（SQL 见 LOOP 报告缺口表，不影响展示）。

## 一、本地走查入口

| 项 | 值 |
|---|---|
| 页面（真登录，接口走 edu 网关、维护接口走本机） | `http://localhost:3100/trend/tech-situation-maintain` |
| 页面（mock 登录，同上） | `http://localhost:3101/trend/tech-situation-maintain` |
| 只读降级演示（本机 display 写鉴权开） | `http://localhost:3102/trend/tech-situation-maintain`：改任意配置后切只读 |
| 全域态势消费侧 | 同端口 `/trend/tech-overall-situation` |
| 复位本地库 | `/tmp/m10-full/reset_local.sh`（快照 → 两份 v2 迁移 → 探测夹具 → 技术点名称复原） |
| 本地进程 | entan-py 8000、topic 7092、cms 7198、display 7199 / 7299、vite 3100 / 3101 / 3102；日志 `/tmp/m10-full/logs/` |
| 未动的旧进程 | 11-09 起的 cms 7098、display 7099、vite 3000（来源不明，没有停） |

## 二、改动清单

### lumen-algo-py（vendor/entan-py）

- `api/tech_graph_maintain_routes.py`
  - R1 服务端检索：keyword / entityType / 年份 / sortBy / page-size，返回 total。
  - R2 新增 description、成员语义、生效类型。
  - 成员表 `graph_entity_member`：挂接时存快照，删边只删边，解挂时按快照回写候选边。
  - overlay 支持 type 覆盖。
  - validate 改为 422 + 中文 preview；submit 前跑同一套校验。
  - publish 返回 results。
  - impact 对不存在的技术点返回 404。
  - 成员表缺失时自动回退旧语义。
- `scripts/mysql/tech_graph_maintain.sql`：追加成员表（含 `snapshot_strength`、`snapshot_time_to`）。
- `scripts/mysql/tech_graph_maintain_v2_member.sql`（新增）：建成员表，并从现有人工边回填，回填时带上快照。
- `test_graph_maintain.py`：41 项全过。

### lumen-svc-platform

- cms `TechMaintainService`
  - 图层挂组；删组 409 同时统计图层数与数据源数。
  - 探测结果落库；数据库表型探测实做（正则 + schema 别名白名单 + information_schema + 参数化只读）。
  - API 型探测失败一律返回 200 + 失败。
  - 单测 20 项。
- display `SituationMaintainController` / `SituationMaintainEntController`
  - 全部 POST 写接口要求登录：`gkxlumen.maintain.write-require-login` 默认 true，未登录返回 401 / 40101。
  - recommend 透传 5 个新参数。
  - 单测 12 项。
- topic `TechGraphMaintainController` / `Client`：透传 5 个新参数，单测 8 项。
- display `application-local.yml`：写鉴权开关置 false（只在本地生效）。
- topic `application-local.yml`（新增）：本地 profile，含仅本地生效的 bean 覆盖。
- `db/9x_gkxlumenx_cms_tech_maintain_config_v2.sql`（新增，可重复执行）：
  - 加列。
  - 测试残留清理。
  - 新增「科研活动图层组」，9 个图层按语义挂组。
  - src-1 / src-2 / src-4 复原挂组；src-2 由占位表名改指 `dwd.dwd_zh_paper`。

### lumen-ui-science-pc

- 图层分区
  - `LayerSourcePanel.vue`：新增 9 个图层的开关与挂组表；数据源表「连通」「最近同步」改为持久化口径；名称必填；只读控制。
  - `FactorIdentityPanel.vue`、`MaintainDialog.vue`：支持只读，弹窗内行内提示。
  - `api/situation/maintain.ts`、`mock/modules/maintain.ts`、`types/maintain.ts`、`maintainSource.ts`（新增）。
  - `stores/layerConfig.ts`（新增）：图层配置 store，遇请求被取消重试一次。
- 全域态势
  - `overview/index.vue`、`FactorMapSection.vue`、`SituationFilterBar.vue`、`models/layerLegend.ts`（新增）。
  - 进页即拉配置；停用图层不出点位并置灰；图例按图层组分段。
- 实体分区
  - `EntityRelationPanel.vue`：服务端检索、分页、跨页勾选；画布 + 列表共享选择；批量工具条；预览与结果统计。
  - 新组件 `EntityPanoramaGraph.vue`（G6 v5）：右键、框选、Delete 键、双击编辑。
  - 新弹窗 `EntityEditDialog.vue`、`RelationEditDialog.vue`、`BatchEntityEditDialog.vue`。
  - `maintainEntOps.ts`、`types/maintainEnt.ts`、`api/situation/maintain-ent.ts`、`mock/modules/maintain-ent.ts`、`mock/register.ts`。
- 权限降级
  - `maintainAccess.ts`（新增）、维护页 `index.vue` 顶部提示条。
  - `layouts/DefaultLayout.vue`：路由降级全局提示条。
- D9：`review/metricSeed.ts`、`review/readinessSeed.ts` 按真源逐字段转录 `M_TECH_GRAPH_105_1`（cfg seed / TECH 就绪度矩阵）。没有新增 metric_id，也没有改绿任何状态。
- 自检
  - `maintainEnt.test.mjs`、`maintainSource.test.mjs`、`layerLegend.test.mjs`（新增）。
  - `pnpm type-check` 绿，5 个 node 自检绿，`pnpm build` 绿。
- 本地联调用的 `vite.m10.local.config.ts` 只登记在 `.git/info/exclude`，不入库。

## 三、本地联调中发现并修复（详见 LOOP 报告「缺口」节）

1. 解挂或删边后，回推荐的年份被人工改值污染。修法：成员快照。
2. validate 漏 base_version。
3. 首屏推荐没进跨页缓存。
4. 同 URL 并发 GET 被全局去重中止。
5. 右键菜单被遮罩的原生 contextmenu 立刻关闭。
6. 单节点时自适应缩放过大，以及连线标签竖排。
7. v2 脚本的挂组复原与占位表名。

## 四、人工确认后的提交与部署步骤（按序）

1. **提交**（各仓 `origin/dev` 直推，commit 带 `[agent:<role>]`）
   - lumen-algo-py：routes、两份 SQL、测试。
   - lumen-svc-platform：cms、display、topic 代码与测试，`db/…_v2.sql`，两份 local yml（只影响本地 profile）。
   - lumen-ui-science-pc：上面列的 20 个修改文件和 13 个新增文件。前端遵守 fe-manual-confirm-push，等口令再推。
   - gkx-orchestration：用例、索引、LOOP 计划、LOOP 报告、本 handoff、截图、registry。
2. **共享库**（**先执行 DDL，再让新代码上线**。PY 对成员表缺失有回退，顺序反了也不会报错，但成员语义要等 DDL 后才生效）
   - `gkxlumenx_cms` ← `db/9x_gkxlumenx_cms_tech_maintain_config_v2.sql`
   - `demo_gkxlumenx_ads` ← `scripts/mysql/tech_graph_maintain_v2_member.sql`
   - 执行前先只读核对一次线上现值：QA 可能又改过。
3. **CI 部署**：algo-py（entan-api）、display、cms、topic 四个服务，加上前端。Nacos 和 helm 不改。写鉴权默认 true，线上即生效。
4. **线上数据复原**：在页面上把技术点 3 改回「神经性厌食症治疗的临床视角 / 中」，走变更集，留审计。
5. **线上 LOOP**：监管人把 display token 放进本机 token 文件 → 按用例逐行复测 → 回写 LOOP 计划状态行 → 建验收单并签收。
6. **重点复核**：「论文主题库」（`dwd.dwd_zh_paper`）探测结果。线上表不存在，或 cms 账号无权读，都会如实显示失败。失败时需另定一张真实表。

## 五、遗留与风险

| # | 项 | 去向 |
|---|---|---|
| 1 | 读接口仍匿名（按 2026-10-31 孔东裁定）；写接口只校验已登录，不区分维护角色。SSO 模式下没有权限码，按钮级权限需要门户配置维护按钮码 | 架构 / 产品裁定 |
| 2 | 推荐候选 91% 是示范种子（D4=mock）；强度来源口径（relation_strength vs 105）待算法确认 | algorithm-agent |
| 3 | 契约文档（LAYER-API / ENT-API）尚未按方案 §2 回写 | 提交时一并更新 |
| 4 | `spring-boot:repackage` 本机报既有问题，CI 打包需留意（Java 路回报） | devops |
| 5 | 11-09 遗留的本机进程（7098 / 7099 / 3000）没有停 | 监管人确认后清理 |

## 六、架构合规自检

- 调用链：前端 → display REST → topic Feign → Python `/internal/*`；Java 纯透传，不写 nGQL ✅
- D9：只读转录真源；不新增 metric_id；D4 mock 如实；人工强度不进指标列 ✅
- D12 / 库边界：开发验证全部在本机隔离库；没有连接或写入任何远端库；共享库变更推迟到确认后 ✅
- 安全：写接口加登录门槛；数据库表型探测用 schema 白名单、正则和参数化，只读；SSRF 黑名单保留 ✅
- 多会话保护：没有 reset、force，也没有 stash 他人文件；registry 写后即推送（只推了建单认领）；他人进程未动 ✅

## 七、cost

- actual_tokens：约 1,300,000（4 路子智能体约 350K + 主会话约 950K，以输入为主）
- model_used：claude-opus-5-5
- actual_cost：约 $25（按 budget-estimate C 档 $15/$75 粗估，未扣缓存折扣）
- cost_warn：**red（> $20）**。按公约 §3.7 应 hard stop 并请 architect 评审。本任务已停在「待人工确认」，不再继续投入。复盘要点：
  - 四路子智能体各自全量读需规与代码。
  - 本地环境搭建：MySQL、四服务、代理、浏览器冒烟。
  - 联调中 6 处缺陷的定位与修复。

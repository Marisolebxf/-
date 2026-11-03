# Frontend handoff：LUMEN-UI-ALGO-APIVIEW-BIZNAV-L01

- 时间：2026-11-03
- 仓库：`repos/lumen-ui-algo-apiview`（分支 `dev`，改动**停本地未推**，待监管人 human:徐滕强 人工验收）
- 任务：算法联调台侧栏按专题/展示业务树重组 + `/home` 总览 D1–D4/缺口汇总
- 强度：ponytail full（护栏项全部交付；本叶非视觉复刻，复刻行见下）
- 监管人/认领人：human:徐滕强

## 范围与实现（对照 DoD）

| DoD | 实现 | 证据 |
|---|---|---|
| 侧栏默认按「专题系统 / 展示系统」业务树 | `src/catalog/businessNav.json`（映射真源）+ `src/catalog/businessNav.ts`（解析层）+ `AlgoShell.vue` 三层树渲染 | 截图 ①②③；专题 8 组 / 展示 7 组 |
| 查询类指标页双挂（同一 catalog 页=同一实现） | 双挂锚 = 同一 `pageRoutePath`，tooltip「双挂锚 · 主挂：… · 同一实现 · 同一入口」 | 展示/企业展示组 11 锚 + 政策跟踪 8 锚；截图 ③ |
| 同名异实现拆页并对照 | 本仓无同名异实现对（techchain.panorama 与展示 DS-02 为**同名同实现**，锚点处理）；如后续出现按映射表 §3 对照需规/指标设计拆页 | 映射表 v2 §四 |
| 不做「按功能」视图切换 | 无切换控件；侧栏仅业务树一种视图 | 截图 ①–⑤ |
| 旧深链仍可达 | 路由/`pageRoutePath`/`/jx`/`/ext`/redirect 零改动；`#/chain/basic` Playwright 实测渲染正常 | 走查输出 `legacyChainBasic:true` |
| 挂不上 → 「未挂/工程」 | 15 页：6 前置统计 + chain.wave1 + 3 工程增强 + comp.basic + tech.basic + MI-SI 核增 5 页（Q2 裁定） | 截图 ①底部组 |
| 图谱构建单入口 | 15 页独立组（未挂/工程之上）；双系统 13 页角标「双系统」紫 + tooltip「展示+专题双系统消费 · 同一实现 · 同一入库（不重复计入指标 D1–D4）」；单消费 2 页角标「专题」；**禁止双挂**（展示树内仅「→ 图谱构建（单入口）」导航锚，点击展开图谱组不跳路由） | 截图 ④；DOM 探针 `riskHTML` 同款验证 |
| 图谱不计入 D1–D4 | `BizNavSummary.vue` 汇总基数=39 readiness 镜像指标（不含图谱）；卡片脚注注明 | 截图 ⑥ |
| handoff 含全量映射表（allCatalog） | 131 页零遗漏：`docs/BIZNAV-L01-页面业务树映射表.md`（v2 已确认）+ `scripts/business-nav.test.mjs` 门禁（每页恰好一个主挂；引用 id 100% 存在；图谱禁双挂） | `pnpm test` 121/121 绿 |
| endpoints 内容无 diff | `git diff -- src/catalog/ src/api/ src/router/` = 0 行 | 本 handoff §变更面 |
| /home 与/或 /dev 汇总 | `/home` 新增 `BizNavSummary.vue` 三卡：按系统计数（含双挂锚数）+ D1–D4 四维（39 指标 readiness 镜像分档）+ 实测健康度五态（237 条 health 镜像）+ 缺口清单（gapNotes 只读展示） | 截图 ⑥ |
| 业务有联调无页缺口清单 | gapNotes 真源=差集 L02/pages YAML 审计：DS-02/DS-03 零落点、DS-28 零落点、DS-30 五页零落点、DS-13~16 13 个 mapped 指标 catalog 未挂接、chain.wave1 有消费无菜单 | `/home` 卡3；侧栏组尾 ⚠ 注记 |
| type-check / catalog 自检 / build 绿 | `pnpm type-check` 绿；`pnpm test` 121/121（含新 business-nav 门禁）；`pnpm build-only` 绿（chunk>500kB 警告为既有现象） | 本 handoff §工程验证 |
| push origin/dev | **按人工验收闸门（2026-10-20 裁定）停本地**，验收后由监管人确认再推 | `git status` 7 文件未提交 |
| cost 四字段 + 架构合规自检 | 见 §成本与 §合规自检；registry 已回填 | registry `task-update-fields` |

## 映射表结论（要点，全文见映射表 v2）

- **专题系统 93 页**：产业链 15 / 企业 13（entan 11 + innov.risk + innov.recommend 带「异步演示」角标，Q3 定案）/ 政策 14 / 服务 12 / 技术链 10·久新 / 科研 8·久新 / 人才 11·久新 / 综合 10。
- **展示系统 独占 6 + 双挂锚 24**：态势 6 独占（innov 五聚合页 + tech-planning）+3 双挂（policy.guide/guard/deep←DS-07 实证）；政策跟踪 8 锚；人才态势 1 锚（talent.basic）；知识图谱→图谱构建锚；成果展示 2 独占（innov.topic-strategy / innov.service-org，C1 修正）；服务全景 0；企业展示 11 锚（C2 修正：entan 全部业务页）。
- **图谱构建 15 页**：单入口，双系统 13 + 专题 2（institute-ner/relation）。
- **未挂/工程 15 页**；其中 entan.basic / policy.basic 本体在未挂但双挂展示锚。
- **v2 关键修正（人已追认）**：C1 成果展示组 0→2 页；C2 企业展示 3→11 锚、market-heat/sz-tier 退出展示；C3 态势组取消 DS-02/DS-03 假锚改缺口注记。

## 产物清单

- `src/catalog/businessNav.json`（业务树真源，含 meta 裁定记录）
- `src/catalog/businessNav.ts`（解析层：TOPIC/DISPLAY/GRAPH/UNASSIGNED + renderGroup + businessKeyOfPage）
- `src/layout/AlgoShell.vue`（三层树侧栏；图谱单入口；未挂/工程；precompute 逻辑原样保留）
- `src/views/BizNavSummary.vue`（新增，/home 汇总三卡）
- `src/views/HomeLegacyView.vue`（+4 行：挂 BizNavSummary）
- `scripts/business-nav.test.mjs`（新增，业务树门禁）
- `docs/BIZNAV-L01-页面业务树映射表.md`（v2，已确认）
- 截图：`/tmp/biznav-home.png`（/home 汇总+侧栏树）、`/tmp/biznav-topic.png`（专题树）、`/tmp/biznav-display.png`（展示树）、`/tmp/biznav-graph.png`（图谱构建组）、`/tmp/biznav-disp-ent.png`（企业展示双挂锚）、`/tmp/biznav-ent2.png`（企业分析含异步演示角标）

## 验收证据

- 工程三绿：type-check ✅ / test 121✅ / build ✅（本机 dev 分支实测）
- Playwright 走查（静态预览 `dist`，token 预置）：汇总区/专题/展示/图谱/未挂/缺口/D1/D4 全命中；旧深链 `#/chain/basic` 渲染正常；零 pageerror；DOM 探针 `风险洞察（异步）异步演示`、`引育推荐（异步）异步演示` 实证角标渲染
- endpoints 零 diff：`git diff -- src/catalog/ src/api/ src/router/ | wc -l` = 0

## 偏离说明

1. 侧栏二/三级沿用 Arco `a-sub-menu`/`a-menu-item` + 既有 nav-owner-badge 样式，未引入新组件文件（ponytail：第二处出现才封装）。
2. 「未挂/工程」组名带空格（UNASSIGNED_GROUP.title = '未挂 / 工程'），与派单话术「未挂/工程」语义一致。
3. `/dev` 未加汇总卡（派单为「/home 与/或 /dev」，选 /home 单点；/dev 保持开发者视图原样）——如需 /dev 同款可在验收后追加。
4. 展示树「科技知识图谱」组用导航锚（点击展开图谱组）而非路由跳转——图谱组是侧栏组不是路由页。
5. 侧栏滚动修复：`nav` 容器加 `max-height + overflow-y`（scoped，不动 main.css）。

## 架构合规自检（公约 §2）

1. 算法只在 Python ✅（未触及）
2. 调用链 前端→Java→Python/internal ✅（未改 api 层）
3. NebulaGraph 协议 ✅（未触及）
4. 可观测性 ✅（observability.ts 未动；AlgoWorkspaceView 埋点链路未改）
5. CI/CD ✅（未推，验收后走 Pipeline；本任务 `cicd` 由派单指定 frontend:build+deploy）
6. demo2 只读 merge 铁律 ✅（未触 demo-*）
7. 共享聚合核心方案 A ✅（纯前端导航重组，不改契约）
8. 数据策略 ADS 先行 ✅（未触数据层）
9. D8 前端规范 ✅（Arco 组件 + token 色板沿用仓内既有变量；新增色值仅角标 #0aa5a8/#722ed1 与 Arco 色板同族，徽标类小组件）
10. D9 数据血缘 ✅（汇总只读消费 readiness/health 生成镜像；无手填、无改绿；图谱组明确不计入；缺口文案读真源不硬编码新口径）
11. D10 交互规范 ✅（键盘可达：菜单为 Arco 原生交互；tooltip 有文字替代；aria-label 保留）
12. D12 demo/lumen 隔离 ✅（仅改 lumen-ui-algo-apiview；无 demo 服务调用）
13. D14 对象存储 ✅（未触及）
14. D16 缺项 ✅（缺口只展示不加工）
15. D17 合规/合理 ✅（未触合规算法闭包）
16. 人工验收闸门 ✅（停本地待验收）

## 成本

- actual_tokens：~210000（估算，含两次映射审计脚本与三轮浏览器走查）
- model_used：glm-5.3-Flash
- actual_cost：<$10
- cost_warn：green

## 复刻行

跳过：导航重组非视觉复刻。

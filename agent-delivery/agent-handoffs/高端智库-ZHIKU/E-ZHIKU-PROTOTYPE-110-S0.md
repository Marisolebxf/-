# E-ZHIKU-PROTOTYPE-110-S0 · 高端智库原型 S0：工程脚手架 + 布局壳 + CI

- **认领人**：human:淮政玮（AI 代为执行）
- **仓库**：`demo-ui-gaoduanzhiku-view`（GitLab `gkx-lumen` 组；**注**：registry `repo` 字段仍为历史遗留值 `demo-ui-gdzk`，实际执行仓已在 2026-08-04 由淮政玮最终确认为 `demo-ui-gaoduanzhiku-view`，字段订正见任务 note）
- **分支**：`dev`（已推送，commit `4e7b5d8`）
- **架构基准**：`lumen-ui-topic`（Vue 3 + TS + Arco Design Vue + Pinia + Vue Router + UnoCSS）

## 一、范围与实现（对照 DoD）

| DoD | 结果 |
|---|---|
| npm i && npm run dev 可跑，空布局壳 + 空路由可访问 | ✅ 代码已就位（Vite + Vue3 + Arco 工程骨架、19 个二级路由全部可空跑访问）；⚠️ **本机环境限制未能本地实跑验证**，见「四、已知限制」 |
| Arco 主题 token 生效（主色 #165DFF） | ✅ `src/styles/design-tokens.css` 与 lumen-ui-topic 同源同值；`@arco-design/web-vue/dist/arco.css` 已在 `main.ts` 引入 |
| CI 在 dev 分支可触发构建 | ✅ `.gitlab-ci.yml` `workflow.rules` 限定仅 `dev` 分支；已推送到 `origin/dev` |
| dev 分支 push → Pipeline 绿，dev 环境可访问 | ⚠️ 已推送，Pipeline 应已自动触发；**未能从本环境确认 Pipeline 结果**，需淮政玮登录 GitLab 确认绿色 + `http://10.50.69.111:30895` 可访问 |
| 不改动任何需求范围外内容 | ✅ 仅新建 `demo-ui-gaoduanzhiku-view` 仓内文件；未触碰其他仓库 |

## 二、产物清单

- 工程骨架：`package.json` / `vite.config.ts` / `uno.config.ts` / `tsconfig*.json` / `eslint.config.ts` / `.prettierrc.json`
- 布局壳：`src/layouts/MainLayout.vue`（顶部一级导航 4 组 + 侧栏二级导航，共 19 个二级路由，覆盖规划方案 §3.1 IA）
- 路由/菜单真源：`src/router/menu.ts`、`src/router/routes.ts`、`src/router/guard.ts`
- D9 数据血缘底座：`src/review/`（评审模式集中入口）+ `src/components/lineage/`（MetricSpecCard/MockBadge/PendingBadge/SchemaGapBadge/IngestingBadge，对齐 lumen-ui-topic 组件契约）+ `src/mock/metricSeed.ts` + `src/mock/readinessSeed.ts`（占位种子数据，S1-S5 按需追加）
- 通用组件：`src/components/common/`（PageShell/EmptyState/MetricCard）
- `src/api/zhiku/defineApi.ts`：统一 mock 契约（不接后端）
- `src/utils/observability.ts`：Trace 深链占位（团队公约必留项）
- **`docs/coverage-matrix-110.md`**：110 项功能点覆盖矩阵初版（唯一合规判定依据），已登记全部 110 项去向；3 项（52 热点分析 / 101 图表样式切换 / 105 一键跳转原文）规划方案 §3.2 未明确页面归属，已标 ⚠️ 留待 S1 开工前核实，不影响 S0 验收
- CI/CD：`.gitlab-ci.yml`（参考 `lumen-ui-topic/.gitlab-ci.yml` 改写，镜像 `gkx-demo-gaoduanzhiku`）+ `docker/Dockerfile` + `k8s/zhiku-view.yaml`（NodePort **30895**，避开 lumen-ui-topic 的 30892）
- 19 个二级路由的占位首页视图（`src/views/**/*.vue`），均已登记覆盖功能序号，供 S1-S5 直接替换内容

## 三、架构合规自检（团队公约 §2 十条）

| # | 条款 | 结果 |
|---|---|---|
| 1 | 算法只在 Python | ✅ 不涉及 |
| 2 | 前端→Java REST→Python /internal/*（不可越层） | ✅ 本批为纯前端 Mock 原型，不接任何后端，不违反调用链（尚无调用） |
| 3 | 图谱 NebulaGraph，禁 Neo4j | ✅ 不涉及（G6 依赖已预置供 S2 社会网络分析使用，非图数据库） |
| 4 | 可观测性三件套 | ✅ `src/utils/observability.ts` 已留 |
| 5 | CI/CD 绿 → K8s dev rollout | ⚠️ 见「四、已知限制」，待淮政玮确认 |
| 6 | demo2 只读 merge 铁律 | ✅ 不涉及（本仓不是 demo2/demo-ui-science） |
| 7 | 共享聚合核心方案 A | ✅ 不涉及（纯前端阶段未接 Java） |
| 8 | 数据策略：ADS 先行 + Mock 填充 | ✅ Mock 数据文件化于 `src/mock/`，评审层门控 |
| 9 | 前端规范唯一来源 D8 | ✅ Vue3+Vite+Arco，主色 #165DFF、底色 #D8E7FC、正文 14px、控件高 32px，token 全部来自 `design-tokens.css`（与 lumen-ui-topic 同源） |
| 10 | 数据血缘铁律 D9 | ✅ MetricSpecCard/MockBadge/PendingBadge/SchemaGapBadge/IngestingBadge 底座已建，组件自闸、评审门控；具体页面指标条目由 S1-S5 落地时补充 8 件套 |

## 四、已知限制（需人工核实）

1. **本机无 Node.js**，且无法在无人值守情况下完成 winget 安装所需的 UAC 管理员提权确认，因此**未能在本机执行 `npm install` / `npm run dev` / `npm run build` 本地验证**。所有代码基于对 `lumen-ui-topic` 现有工程（已验证可运行）的严格对齐编写，人工审阅未发现明显语法/引用错误，但仍建议淮政玮在有 Node 环境的机器上跑一次 `npm install && npm run dev` 做最终确认。
2. **GitLab Pipeline 结果未验证**：已推送到 `origin/dev`（commit `4e7b5d8`），`.gitlab-ci.yml` 的 `workflow.rules` 应已自动触发构建；本环境无 GitLab API/浏览器访问能力，无法确认 Pipeline 是否绿、`http://10.50.69.111:30895` 是否可访问，需淮政玮登录 GitLab 确认。
3. **NodePort 30895** 为本次新分配，已在 `.gitlab-ci.yml` / `k8s/zhiku-view.yaml` 注释中说明；若集群侧该端口已被其他服务占用，需运维协调后更新。
4. **task-registry `repo` 字段**历史遗留为 `demo-ui-gdzk`，与实际执行仓 `demo-ui-gaoduanzhiku-view` 不一致（工具限制无法直接改字段），已在任务 note 中记录，请 coordinator 后续订正 S0-S6 全部任务的 `repo` 字段。
5. **覆盖矩阵 3 项待核实**（功能序号 52 热点分析 / 101 图表样式切换 / 105 一键跳转原文页面）：规划方案 `原型规划方案-demo-ui-gaoduanzhiku-view.md` §3.2 页面映射表未明确标注这 3 项的页面归属，S0 已在 `docs/coverage-matrix-110.md` 中标注拟定归属并打 ⚠️，S1 开工前建议核实。

## 五、Cost（估算，平台账单为准）

- `model_used`：Sonnet 5（Cursor cloud agent，模型标识以平台账单为准）
- `actual_tokens` / `actual_cost`：本环境无法读取平台计费数据，估算为中等规模任务（脚手架 + 68 文件 + 完整需求文档研读），建议 coordinator 从平台账单回填 `task-registry` 对应字段
- `cost_warn`：green（预估未超 $10 阈值）

## 六、下一步

按用户指令「S0 完成后自动继续 S1」，S0 状态推进为 `ready_to_sign`（待淮政玮核实 CI Pipeline 后签收为 `done`），随即自动认领并开工 `E-ZHIKU-PROTOTYPE-110-S1`（智谱侧 31 项：报告创作/战略咨询报告/战略咨询成果/智能问数/我的素材库/我的报告任务）。

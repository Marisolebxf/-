# FE-DISPLAY-TECHINDEX-NEW-L01 · 科技指数New — 全域指标体系展示页（九域 + 8 件套 + 算法口径）

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch`（2026-08-09 项目负责人会话直接指示：按 Q-TINDEX-01~04 临时默认派单） |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 未用 YAGNI 跳过 D9/可观测性惯例：ⓘ 8 件套 + 🧪 MockBadge + 红问号诚实态全交付，全部走 `ReviewOnly` 评审门控（关则 DOM 零泄漏）。镜像**生成器**替代手写 140 条指标（手写即漂移）；未加任何 npm 依赖（yaml 解析按团队 `task-registry-lib.mjs` 惯例定向实现）；复用 `policy-tracking/components/MockBadge.jsx` 与「科技创新评估new」挂载先例。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | user-headroom MCP 已挂载；本单多次大文件读取改用定向 grep/分段读取规避，未调用压缩。 |

## 范围与实现（对照 bid-reference）

| 锚点 | 落点 |
| --- | --- |
| 展示系统 §1.1.1.1.4.1.8.1 指标展示（指标项/概述/计算方法/意义/权重） | 「科技指数New」页九域指标卡 + ⓘ 8 件套弹卡（口径/公式/源表/源系统/频率/版本） |
| 算法库 §基础指标分析模型 七域（产业链/技术/企业/人才/科研机构/政策/服务机构） | 七域 Tab + bid 维度 chips；TECH/TALENT/ORG/SVC 按 bid 维度列演示指标（红问号） |
| 王惠产出：`metrics/registry/cfg_metric-{ENT,POLICY,CHAIN,TNIE}-seed.yaml` | `metricCatalogMirror.js`（60/19/60/1 条，生成器产物，禁手改） |
| 唐绍祖产出：`算法设计说明.md` 公共约定 + COMP 10 模型 + SVC 模型族 + M10 | 页面顶部公共算法约定卡 + 每域算法口径卡（含 pending Q 引用） |
| 综合分析域 | COMP Tab：10 模型清单 + 4 演示指数（红问号） |

**边界**：按 Q-TINDEX-01 临时默认只做展示侧；同行评议专家智库管理机制不进本期。bid §4.1.8.2 可视化/§4.1.8.3 排行榜未在新页重做（老「科技指数」页保留，切换策略见 Q-TINDEX-04）。

## 产物清单

| 文件 | 说明 |
| --- | --- |
| `repos/demo-ui-science/src/pages/tech-index-new/index.jsx` | 页面（Tabs 九域 + 声明条 + 公共约定 + 指标卡网格） |
| `…/catalogConfig.js` | 域配置（bid 维度 + 算法口径 + Q 引用 + 演示指标；手写仅限展示定义） |
| `…/metricCatalogMirror.js` | **生成物**：四域 8 件套镜像（60/19/60/1） |
| `repos/demo-ui-science/scripts/build-techindex-metric-mirror.mjs` | 镜像生成器（定向 YAML 解析，跨仓读 orchestration seed） |
| `…/metricCatalogConsistency.test.mjs` | 自检：镜像==seed 重解析比对 + 九域配置 + 挂载接线 |
| `…/style.css` | 页面样式 |
| `src/data.js` / `src/App.jsx` | 菜单 `科技指数New`（不去后缀，按用户要求显示原名）+ 挂载 |

## DoD 对照

- [x] 新菜单「科技指数New」挂载（沿用 科技创新评估new 先例；**偏离**：用户要求菜单显示原名，未加 topicDisplayNames 去后缀映射）
- [x] 九域覆盖：ENT/POLICY/CHAIN/TNIE seed 域 + TECH/TALENT/ORG/SVC/COMP bid 维度域
- [x] 王惠产出：四域指标卡 8 件套来自镜像（生成器同步，非手写）；未注册指标红问号不显伪 8 件套
- [x] 唐绍祖产出：公共约定（ln(1+x)+min-max / AHP×熵权 / T½=2 年衰减 / 权重落配置）+ M10/COMP/SVC 模型标注，权重待确认项标 ⚠️ Q-TINDEX-03
- [x] 统计数字带 ⓘ/红问号 + 🧪 MockBadge（ReviewOnly 门控）；页面常驻 Q-TINDEX-01~04 声明
- [x] 自检 `node src/pages/tech-index-new/metricCatalogConsistency.test.mjs` 通过；开发中曾捕获 COMP 维度配置错误（破坏即失败成立）
- [x] `npm run build` 通过；push origin/main 完成；本 handoff + cost 四字段回填

## 验收证据

- 自检输出：`tech-index-new consistency OK：镜像=seed 真源 / 九域配置 / 菜单挂载 全部一致`；旧页 `mockDataConsistency.test.mjs` 回归仍过
- 生成器校验：镜像条数与 seed `total_metrics` 对齐（ENT 60 修复列 0 注释早停缺陷后达标）
- 构建：vite build ✓（9846 模块，仅存量 chunk 告警）
- commit：`09326e6`（dev → dev，并快进 `dev:main`）；30999 约 2–3 min 生效，菜单「科技发展态势 → 科技指数New」
- 后续修复 `8a46d7d`：补齐版心 `margin-left: 240px`（折叠 80px）+ 视口高度锁定，修复页面内容溢出左侧菜单（监管人截图反馈）；自检新增版心布局断言防回退

## 遗留风险 / 开放项

- Q-TINDEX-01~04 均 🟡：甲方确认后需按决策回写（口径/权重/菜单切换），相关返工走新任务
- TECH/TALENT/ORG/SVC/COMP 五域 metric_id 注册依赖王惠口径正式化（Q-TINDEX-02）；正式化后跑生成器扩展 `MIRROR_DOMAINS` 即可
- 页面数值为 metric_id 哈希派生 Mock（🧪 标注），接 ADS 后由 Java REST 替换（调用链铁律）
- 评审模式关闭时 ⓘ/🧪/⚠️ 全不渲染（与政策页同规约）；业务态只留数值与名称

## CI/CD（必填）

- 分支：本地 `dev` commit `09326e6` → push `origin/dev` + `git push origin dev:main`（5edaf9c..09326e6，非 force）
- pipeline：demo 仓静态站点，无独立 pipeline；push main 后 2–3 min 自动部署
- dev 测试 URL / 命令与结果：`node src/pages/tech-index-new/metricCatalogConsistency.test.mjs` ✅；`npm run build` ✅；https://skxrules.unicomcn.tech:30999/ 待人工抽查

## 可观测性（建议）

- 纯前端静态页，无请求链路；未新增埋点（demo 页先例如此）。正式化时随 lumen 仓补 `observability.ts`。

## 架构合规自检（§2）

| # | 铁律 | 结果 |
|---|---|---|
| 1 | 算法只在 Python | ✅ 前端仅展示算法口径文案，未实现算法 |
| 2 | 调用链 | ✅ Wave0 Mock 镜像，无直连 Python/DB |
| 3 | 图谱 Nebula | N/A |
| 4 | 可观测性 | N/A（demo 静态页，见上） |
| 5 | CI/CD | ✅ push main → 30999 |
| 6 | demo 只读 merge | ✅ 仅 demo-ui-science |
| 7 | 共享聚合 | N/A（demo） |
| 8 | ADS/Mock | ✅ Mock + 🧪 全标注 |
| 9 | D8 Design | ✅ 复用既有 New 页模式与 AntD 组件，主色 #165DFF |
| 10 | D9 血缘 | ✅ 8 件套镜像真源化 + 红问号诚实态 + ReviewOnly 零泄漏 |
| 11 | D10 交互 | ✅ AntD Tabs/Popover/Tooltip 标准交互 |

## 成本回填

| 字段 | 值 |
| --- | --- |
| actual_tokens | 260000（估，含真源通读与生成器调试） |
| model_used | kimi-k3 |
| actual_cost | 2.6 USD（估） |
| cost_warn | green |

## 建议下一状态

feature：handoff 已交 + evidence 已回填 → AV-0 目标 `integration`；本单无后端联调面，建议 coordinator 评估直接推 `pending_test`，由 QA/监管人抽查 30999「科技指数New」。

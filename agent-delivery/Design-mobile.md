# GKX 手机端（小屏 H5）设计与工程约束

> **状态**：v1.1.1 · 2026-08-26 · `human:孔东` 确认 C1–C7（C1 改为 Arco+Vant 分层共存）· 供 `E-FE-SMALL-SCREEN` / LT-6-NORM  
> **不替代** `Design.md`（PC + token 真源）  
> **会签**：前端 Lead `human:孔东`（已确认）· 体验 `human:高颖`（轻量，可补签）  
> **工程门**：`repos/lumen-ui-science-mobile/docs/小屏断点与裁剪规则.md`  
> **出效果提示词（非 P0）**：`repos/lumen-ui-science-mobile/docs/小屏AI出效果备忘.md`  
> **仓内副本**：`repos/lumen-ui-science-mobile/docs/Design-mobile.md`（与本文应对齐；冲突以**本文**为准）  
> **会签原文**：`agent-delivery/agent-handoffs/LT-6-NORM-小屏规约会签.md`

---

## 已确认决议（C1–C7）

> 2026-08-26 `human:孔东` 拍板。正文各节按编号展开，不以丽影 DRAFT v0.1 的「整仓换 Vant / Tabbar 做一级 IA / 同仓 mobile」为准。C1 同日改为分层共存。

| 编号 | 决议 | 落点 |
|------|------|------|
| **C1** | **分层共存**：壳导航 + Icon + D9 弹层用 `@arco-design/web-vue`；页内表单/反馈用 **Vant 4**。一个文件只认一个库 | 本文 §1 |
| **C2** | App 级 = 滑入侧栏（L1/L2 白名单）。**Vant Tabbar 只做页内分块**，禁止当一级菜单。同菜单页分块较多时酌情用 Tabbar（`PageTabs`），少时用 `van-tabs` / 分段按钮，二者按需不叠 | 本文 §3 |
| **C3** | 专题独立仓 `lumen-ui-topic-mobile`，**禁止**写进 `lumen-ui-topic`。时机：人工把 science-mobile **全量复制**到 topic-mobile，再按仓删减 | 本文 §0.2 · 断点规则 §4 |
| **C4** | 工程产品门只认 `PHONE_MAX_PX = 767`；`<360` / `360–430` / `431–767` 只做页内疏密，不新开壳 | 本文 §2 · 断点规则 §1 |
| **C5** | **不下发**红线用本文 §10；**观感上限**用 `小屏AI出效果备忘.md`（2 列 KPI、ECharts、地图工具条、底 Tab） | 本文 §10 · AI 备忘 |
| **C6** | 两仓统一 Vue Router **`createWebHistory`**（history）；nginx `try_files` 回 `index.html`。禁止一仓 hash、一仓 history | 本文 §1、§7 |
| **C7** | 专题小屏只做内部裁剪演示；**对外验收仍 PC**。Q030 未绿前不改权限清单屏幕列 | 本文 §0.2 · `Design.md` §11 |

---

## 0. 给 AI 的执行指令

从 PC 页生成手机端时，本文件是强约束。

### 0.1 与 PC 规范的关系

| 层级 | 真源 | 手机端怎么用 |
|------|------|----------------|
| 视觉 token / 主色 / 气质 | `Design.md` §4–§6 | **原样继承** |
| PC 骨架 / 24 栅格 / 三栏工作台 | `Design.md` §3、§8、§11 | **禁止压缩复刻**；换成 §3 手机骨架 |
| 交互行为语义 | D10 | 保留状态机；触控替代 hover 见 §8 |
| 指标血缘 | D9 | 数字旁 ⓘ / 角标不删；热区见 §9 |
| 调用链 | 架构铁律 + D12 | 前端 → Java Gateway；禁 Python / demo-* |

### 0.2 仓与范围（2026-08-26 确认）

| 系统 | 小屏仓 | 本期 |
|------|--------|------|
| 科技信息展示系统 | **`lumen-ui-science-mobile`** | 中屏核心路径裁剪 |
| 科技专题服务系统 | **`lumen-ui-topic-mobile`**（独立仓） | 内部裁剪演示；**禁止**写进 `lumen-ui-topic` |
| Track-L 大屏 | — | **不做** |

拆仓（C3）已执行：science-mobile 只留展示；topic-mobile 只留专题。步骤见断点规则 §4。

对外验收：专题仍以 PC 工作台为准。Q030 未绿前专题小屏不进对外验收、不改权限清单屏幕列。

小屏 = 中屏核心裁剪，不是新 App，也不是把 PC 三栏压扁。

### 0.3 禁止做成

- 深色数据大屏 / 玻璃拟态 / 营销官网 / 自由渐变科技风
- 把 PC `app-sidebar + 三段工作区` 缩到 375 宽
- 堆完整高级筛选树、多图联动、重图谱编辑
- 另起与 `#165DFF` / `#D8E7FC` 无关的品牌色
- 在 `lumen-ui-topic` 内用 media query 假装手机 App
- 互斥 `display` 叠在同一节点

---

## 1. 技术栈（C1：Arco + Vant 分层共存）

| 项 | 选择 |
|----|------|
| 框架 | Vue 3 + `<script setup>` + TypeScript + Vite + Pinia |
| 壳 / Icon / D9 | **`@arco-design/web-vue`**：`Menu` / `Popover` / `Tooltip` + `@arco-design/web-vue/es/icon`。Arco **按需 CSS**，禁止整包 `arco.css` |
| 页内控件 | **Vant 4**：Field / Button / Picker / Popup / Switch / Tag / Empty / Form / NoticeBar / Toast / **Tabbar（仅页内）** / Tabs。按钮高 **32px**、min-width **44px** |
| 图标 | 统一 Arco Icon（含导航与 D9）。禁止用 Vant Icon 顶 D9 契约 |
| 图表 | ECharts（`vue-echarts`）；**禁止 G6** |
| 地图 | Leaflet + 天地图（`UnifiedLeafletMap` / `MapChrome`） |
| 路由 | Vue Router **`createWebHistory`**（C6）；两仓统一。nginx 须 `try_files` 回 `index.html` |

**不选**：antd-mobile / NutUI / RN / uni-app / 小程序。**禁止** Vant `Tabbar` 做 App 一级 IA（C2）；同菜单页内容分块多时可用 Tabbar 做页内导航，与 `van-tabs` 按需选用。

分层规矩：一个 `.vue` 文件只写一套前缀（壳文件用 `a-menu`，页/筛选/登录用 `van-*`）。禁止同一模板混用。

优先复用：`MobileShell` / `StatCard` / `ListCard` / `QuickFilter` / `ProfileDrawer` / `PageTabs` / `BackToTop` / `SectionTitle` / `VChart` / `UnifiedLeafletMap` / `MapChrome`。

### 1.1 Token

```css
:root {
  --sci-bg-page: #d8e7fc;
  --sci-surface-solid: #ffffff;
  --sci-surface-soft: #f7f8fa;
  --sci-border: #e5e6eb;
  --sci-text-1: #1d2129;
  --sci-text-2: #4e5969;
  --sci-text-3: #86909c;
  --sci-primary: #165dff;
  --sci-primary-hover: #4080ff;
  --sci-primary-soft: #e8f3ff;
}
```

页底 `#D8E7FC`；主色 `#165DFF`。Arco `primary-6` 与 Vant `--van-primary-color` 都桥到 `--sci-primary`。

---

## 2. 视口与断点（C4）

| 项 | 值 |
|----|-----|
| 设计稿基准宽 | **375px** |
| 最大内容宽 | **430px** 居中 |
| 安全区 | `env(safe-area-inset-*)` |
| 触控 | 按钮高 **32px**、宽 ≥**44px**；图标热区（顶栏菜单 / D9 ⓘ）仍 **44×44** |

**产品门（工程只认）**：`PHONE_MAX_PX = 767`。`≥768` 提示用 PC / 中屏。常量：`src/config/breakpoints.ts`。

页内密度（不新增壳）：`<360` 单列更紧；`360–430` 默认；`431–767` 可双列卡，禁止恢复 PC 侧栏。

---

## 3. 骨架（C2：双层导航）

禁止 PC 三栏同屏。

**App 级**：顶栏（菜单 ≥44 / 标题 / 次要动作）+ **滑入侧栏**（L1/L2 白名单，非常驻）。**禁止** Tabbar / `van-tabbar` 做一级菜单。

**页内**：同菜单页内容分块用底部导航。分块较多时**酌情**用 **Vant Tabbar**（`PageTabs` 封装，不改路由；例：SPIKE 四块）；分块少用 `van-tabs` 或分段按钮。二者按需，不叠两套。

**详情**：`ProfileDrawer` 半屏 / 全屏。筛选：`QuickFilter`；复杂条件进全屏抽屉，扁平 ≤8 项。

拆仓后展示仓去掉「展示/专题」切换；专题仓只留专题白名单。

地图页：顶筛选摘要 + 中地图（≥55% 高）+ 底抽屉或页内 Tab。禁止左图层/右分析常驻。

---

## 4. 密度

正文 14px；辅助 ≥12px；页标题 17–18px。按钮高 **32px**（与 PC 控件同），min-width **44px**。控件圆角 4px，卡片 8px。页边 12–16px。升红降绿。

---

## 5. PC → 手机映射

| PC | 手机 |
|----|------|
| 侧栏 Menu | 滑入侧栏（白名单） |
| Tabs | 页内：分块多酌情 `PageTabs`（Vant Tabbar），少块 `van-tabs` / 分段按钮。禁止当一级菜单 |
| Table | `ListCard`，关键列 ≤3 |
| FilterPanel 整树 | 扁平 ≤8 +「高级」 |
| 右栏 Drawer | `ProfileDrawer` |
| 多图 / G6 | 一主图或列表；图谱编辑留 PC |
| Metric ⓘ | 44px 热区，抽屉展示 8 件套 |

---

## 6. 生成流程

定角色 → 抽 ≤5 步核心路径 → 换 §3 骨架 → 按 §5 映射 → 观感跟备忘、红线跟 §10 → Mock 开关 → D9 → §12 自检。

### 6.1 目录

```
lumen-ui-science-mobile/   # 仅展示
lumen-ui-topic-mobile/     # 仅专题（全量复制后删减）
```

两仓都保留：`breakpoints.ts`、`src/review/`、`observability.ts`、`--sci-*`。

可复用 API 类型 / catalog / 壳组件。禁止搬 PC 布局、FilterPanel 整树、G6。

---

## 7. 铁律

前端只打 Java gateway；D12 禁 demo；可观测保留；commit 带 `[agent:frontend-agent]` / `[human:姓名]`，推 `origin/dev`；排版 lite 不得跳过 D9/本骨架；**路由 history**。

---

## 8–9. 交互增量与 D9

无 hover 依赖；抽屉锁滚回焦；空/载/错态齐全。角标热区 ≥44px；禁止因屏小删除追溯；评审关后零泄漏。

---

## 10. 能力红线（C5）

观感上限以 `小屏AI出效果备忘.md` 为准（2 列 KPI、底 Tab、ECharts、地图工具条）。本表只定**不下发**：

权重 / 推演 / 布尔全树 / 图谱建模 / 大报表 / 对比篮 / 导出 → 仅 PC。

Q030 🟢 后按页替换。

---

## 11. 任务 × 文件关联

| 任务 | 仓 | 必读 |
|------|-----|------|
| `FE-SMALL-SHELL-L01` | `lumen-ui-science-mobile` | 本文 + 断点规则 + `src/shell/` |
| `FE-SMALL-AI-SPIKE-L01` | `lumen-ui-science-mobile` | 本文 + AI 备忘 |
| `FE-DISPLAY-SMALL-BATCH-A` / `B` | `lumen-ui-science-mobile` | 本文 + 断点规则 + 备忘 · `src/views/{模块}/**` |
| `FE-TOPIC-SMALL-ENT-L01` | **`lumen-ui-topic-mobile`** | 本文 + 断点规则 §4 + 备忘；先全量复制再删减 |
| `FE-TOPIC-SMALL-CHAIN-POL-L01` | `lumen-ui-topic-mobile` | 同上 |
| `FE-TOPIC-SMALL-SVC-COMP-L01` | `lumen-ui-topic-mobile` | 同上 |
| `FE-LARGE-PENDING-L01` | — | 本文不适用 |

编排同步：`Design.md` §11 · `architecture-baseline.md` D4 · `repo-registry.yaml` · `paths.yaml` · `系统-06-多端小屏.md`。

---

## 12. AI 自检

1. Vue3；壳/D9 用 Arco，页内用 Vant；Tabbar 只在页内、不进侧栏；主色/页底正确  
2. 无 PC 三栏；App 导航是滑入侧栏  
3. 按钮高 32 / 宽 ≥44；图标热区 44×44；产品门 ≤767  
4. 筛选已降维；D9 追溯仍在  
5. 只经 gateway；路由 **history**  
6. 专题页不进 `lumen-ui-topic`  
7. handoff 写明裁自哪页、砍了什么、目标仓、Mock 开关  

---

## 13. 修订

| 版本 | 说明 |
|------|------|
| DRAFT v0.1 | 2026-08-25 丽影稿 |
| **v1.0** | 2026-08-26 孔东确认：C1 当时为单库 Arco · C2 双层导航 · C3 全量复制后删减 · C4 767 门 · C5 红线/备忘分层 · C6 history · C7 专题小屏内部演示、对外仍 PC |
| **v1.1** | 2026-08-26 孔东：C1 改为 Arco（壳/Icon/D9）+ Vant 4（页内控件）分层共存；C2 明确 Tabbar 可做页内分块、禁止一级菜单 |
| **v1.1.1** | 2026-08-26 孔东：按钮高统一 32px，触控只保宽度 ≥44；图标热区仍 44×44 |

---

## 14. 参考

- `agent-delivery/Design.md` §0、§4、§5、§11
- `agent-delivery/architecture-baseline.md` D4
- `agent-delivery/工程过程/02-策划与监控/02-智树工作计划/02-进度/系统-06-多端小屏.md`

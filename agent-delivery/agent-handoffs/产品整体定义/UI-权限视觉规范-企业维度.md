# UI 权限视觉规范 · 企业维度切片（E-PERM-L02）

> **任务**：E-PERM-L02（Epic `E-PERM-M1`）—— **企业维度视觉切片**（级别切换器 / 身份徽标 / 降级态 / 权重只读 / D9 角标 / 菜单锁态 / 概览去重布局）
> **角色**：ui-agent（资深 UI 设计师，严格遵循 `Design.md` D8 + `data-lineage-policy.md` D9）
> **时间**：2026-06-22
> **范围**：**仅 `demo-ui-topic` 专题系统 · 仅 PC 中屏 MEDIUM 单形态**；只产出权限/血缘相关视觉态，不重新设计企业业务页本身。
> **上游输入**：`UX-权限交互规范-企业维度.md`（§7.2 给 ui-agent 接力建议表为本任务直接依据；§2.2 切换器 / §3.3 降级态 / §4 角标 / §1.5 概览布局）
> **权威依据**：`Design.md`（§4 色彩 / §5 字体 / §6 圆角描边阴影 / §7 通用组件 / §8 工作区 / §13 实现映射 / §14 检查清单）、`data-lineage-policy.md §5`（MetricSpecCard / DataLineageDrawer / MockBadge）、`ARCH-权限体系-评审.md §9`（守 #165DFF/32px、禁 antd、专题不得误用大屏酷炫态）
> **下游接力**：frontend-agent（E-PERM-L03）落 `demo-ui-topic` 代码

---

## 0. 头部元信息与隔离声明

| 项 | 内容 |
|---|---|
| 工作根 | `GKX_ROOT = E:/gkx-lumen`（已读 `gkx-orchestration/.env` 确认） |
| 唯一可写文件 | 本文件 `agent-delivery/agent-handoffs/产品整体定义/UI-权限视觉规范-企业维度.md`（新建） |
| **隔离声明** | 本任务**不动任何现有文件**（不改 `src/`、不改路由、不改业务口径、不改其它编排 md/yaml）；除本文件外全部只读。仓内其它 modified 文件（task-registry / dispatch-queue / level-perms-matrix 等）属其它任务/coordinator，**不提交**。 |
| 不做 | 不写业务逻辑；不改路由；不重设计企业业务页；不替甲方拍板业务口径（沿用 UX ⚠️ 角标）；不扩范围 |
| 组件库铁律 | **Arco Design**（`@arco-design/web-react` + `@arco-design/web-react/icon`）；**禁 antd**（D8 §13 硬铁律 + ARCH §9） |
| 屏幕维度 | 专题恒 MEDIUM（PC）；本文**不出现**大屏酷炫态 / 深色大屏 / 小屏裁剪态（D8 §0 禁止项 + ARCH §6.1.3） |
| 视觉气质基线 | 浅蓝白轻科技工作台；主色 `#165DFF`、底色 `#D8E7FC`、正文 14px、控件高 32px（D8 §0/§2/§14） |

### 0.1 术语对齐（沿用 UX §0.1）

| 级别 | 代号 | 企业语境用户 | 默认视图 |
|---|---|---|---|
| L0 | GUEST 公众访客 | 未登录浏览企业概况 | 只读概览 |
| L1 | REGISTERED 注册用户 | 注册企业/公众（入门级） | 工作台（入门，E-20 仅结论条） |
| L2 | PRO 专业用户 | 实名认证企业/科研/智库（分析级） | 工作台（完整驾驶舱） |
| L3 | INTERNAL 内部业务用户 | 政府/管委会经办 | GOV=驾驶舱 / INNO=工作台 |
| L4 | ADMIN 管理/运营 | 后台维护（企业页非本切片） | 后台 |

> 身份（persona）只决定默认视图 + 数据范围，不增减权限：`GOV=驾驶舱`、`INNO·THINK=工作台`、`VISIT=只读`。

### 0.2 Persona 优先的顶部演示视角控件

视觉设计必须遵守 `UX-权限交互规范-企业维度.md §0.2 / §2.2` 的主从关系：

- 顶部只暴露一个“当前用户视角”胶囊，不再把 `Persona` 与 `Level` 做成两个平级控件。
- 胶囊主文案显示 Persona，例如 `GOV · 驾驶舱`、`INNO · 工作台`。
- Level 是下拉面板里的“高级演示调节”，默认由 Persona 自动带出推荐值。
- 手动调出非推荐组合时，必须出现弱提示：`该组合仅用于权限边界演示，非真实业务角色`。

视觉上，Persona 区域要比 Level 区域更强；Level 区域必须弱化，避免业务用户误解为可随意拼装的真实角色体系。

实现验收备注：

- 顶部权限/视角控件以 `PersonaLevelSwitcher` 为唯一验收对象。
- 旧 `app-user-switch`、`app-user-pill`、`app-user-role-menu`、`app-user-role-option` 视觉契约废弃。
- `design:check` 应检查 `persona-switch`、`persona-switch__level`、`persona-menu`、`persona-menu__row`、`persona-menu__advanced`、`persona-menu__warning`，并检查非推荐组合提示文案。

---

## 1. 全局 Token 表（从 Design.md 取，本规范专用变量建议）

### 1.1 基础 token（D8 §4.1 / §6，直接复用，不新发明）

| 语义 | 变量名（建议） | 色值 / 规格 | 出处 |
|---|---|---|---|
| 页面底色 | `--sci-bg-page` | `#D8E7FC` | D8 §4.1 |
| 主面板白（半透明） | `--sci-surface-main` | `rgba(255,255,255,0.8)` | D8 §4.1 |
| 纯白 | `--sci-surface-solid` | `#FFFFFF` | D8 §4.1 |
| 填充浅灰 | `--sci-surface-soft` | `#F7F8FA` | D8 §4.1 |
| 填充灰（hover/禁用底） | `--sci-surface-hover` | `#F2F3F5` | D8 §4.1 |
| 边框浅灰 | `--sci-border` | `#E5E6EB` | D8 §4.1 |
| 边框中灰（禁用边框） | `--sci-border-strong` | `#C9CDD4` | D8 §4.1 |
| 主文字 | `--sci-text-1` | `#1D2129` | D8 §4.1 |
| 次文字 | `--sci-text-2` | `#4E5969` | D8 §4.1 |
| 弱文字（占位/禁用） | `--sci-text-3` | `#86909C` | D8 §4.1 |
| 品牌主蓝 | `--sci-primary` | `#165DFF` | D8 §4.1 |
| 品牌中蓝（hover/序列） | `--sci-primary-hover` | `#4080FF` | D8 §4.1 |
| 品牌浅蓝（选中底/focus） | `--sci-primary-soft` | `#E8F3FF` | D8 §4.1 |
| 成功 | `--sci-success` / 浅底 | `#00B42A` / `#E8FFEA` | D8 §4.2 |
| 警示 | `--sci-warning` / 浅底 | `#FF7D00` / `#FFF7E8` | D8 §4.2 |
| 错误 | `--sci-danger` / 浅底 | `#F53F3F` / `#FFECE8` | D8 §4.2 |
| 控件高度 | `--sci-control-h` | `32px` | D8 §0/§7 |
| 小控件高度 | `--sci-control-h-sm` | `24px` | D8 §7.1 |
| 圆角·按钮/输入 | `--sci-radius-ctrl` | `3px`（2–4px 区间） | D8 §6.1 |
| 圆角·卡片/面板 | `--sci-radius-card` | `8px` | D8 §6.1 |
| 圆角·主外壳 | `--sci-radius-shell` | `10–12px` | D8 §6.1 |
| 圆角·胶囊 | `--sci-radius-pill` | `999px` | D8 §6.1 |
| 阴影·浮层 | `--sci-shadow-popover` | `0 4px 10px rgba(0,0,0,0.10)` | D8 §6.3 |
| 阴影·柔和面板 | `--sci-shadow-soft` | `0 8px 18px rgba(107,143,235,0.08)` | D8 §6.3 |
| 正文字号/行高 | `--sci-font-body` | `14px / 22px` | D8 §5.2 |
| 辅助字号 | `--sci-font-aux` | `12px / 16–20px` | D8 §5.2 |
| 关键数值 | `--sci-font-metric` | `24–34px / 35–44px` 600 | D8 §5.2 |

### 1.2 权限态专用语义 token（基于基础色派生，本规范新增建议）

> 原则：**不新发明颜色**，全部由 §1.1 基础色派生组合。仅为权限/锁态/角标提供语义别名，方便 FE 统一引用。

| 语义 | 变量名（建议） | 取值（派生自基础色） | 用途 |
|---|---|---|---|
| 级别 L0 中性 | `--perm-level-l0` | `#86909C`（弱文字灰） | L0 访客段配色 |
| 级别 L1 主色阶浅 | `--perm-level-l1` | `#4080FF`（品牌中蓝） | L1 注册段 |
| 级别 L2 主色 | `--perm-level-l2` | `#165DFF`（品牌主蓝） | L2 专业段（分析级核心） |
| 级别 L3 强调 | `--perm-level-l3` | `#0E42B3`（主蓝加深 ≈ primary×0.8） | L3 内部段强调 |
| 级别 L4 管理色 | `--perm-level-l4` | `#FF7D00`（警示橙，复用状态色） | L4 管理段（区别业务蓝） |
| 锁态前景 | `--perm-lock-fg` | `#86909C`（弱文字） | 🔒 图标/锁态文字 |
| 锁态底 | `--perm-lock-bg` | `#F7F8FA`（填充浅灰） | 禁用/锁态背景 |
| 锁态描边 | `--perm-lock-border` | `#E5E6EB` | 锁态边框 |
| 升级引导主色 | `--perm-upgrade` | `#165DFF` | 升级/登录/申请按钮主色 |
| 待确认角标 | `--perm-pending` | `#FF7D00` / 底 `#FFF7E8` | ⚠️ 待甲方确认角标 |
| Mock 角标 | `--perm-mock` | `#FF7D00` / 底 `#FFF7E8`（与待确认共用警示色系，靠图标区分） | 🧪 MockBadge |
| 血缘卡底 | `--lineage-card-bg` | `#F7F8FA`（浅蓝灰，叠 1px `#E5E6EB`） | MetricSpecCard 背景 |
| 信息角标 | `--lineage-info-fg` | `#4E5969`（次文字，hover→`#165DFF`） | ⓘ 图标 |

> ⚠️ **L4 管理色用警示橙 `#FF7D00`**：刻意区别于业务蓝系，避免 L3/L4 视觉混淆；橙色取自 D8 §4.2 状态色，非新发明。L4 在企业前台页不渲染（仅切换器列项可见），故橙色出现面积极小。

---

## 2. 级别切换器 L0–L4（对照 UX §2.2，D8 §7 / §13 Segmented）

### 2.1 控件选型与规格

- **组件**：Arco `Segmented`（分段单选；D8 §13「操作」类推荐 `Segmented`），Wave0 演示态置于 `app-header` 右区。
- **高度**：`32px`（`--sci-control-h`，严守 D8 §0/§7）；圆角 `3px`（`--sci-radius-ctrl`），外层容器圆角可用 `999px` 胶囊（D8 §6.1 分段/胶囊）。
- **字号**：`14px`（`--sci-font-body`）；选中项 500 字重（D8 §5.2 正文强调）。
- **Wave1**：接 SSO 后切换器**隐藏/只读**（级别由 token 决定），仅保留只读级别标识 Tag。

### 2.2 五级配色阶（常态/悬停/选中）

| 级别 | 配色语义 | 常态（未选中） | 悬停 hover | 选中 active/selected |
|---|---|---|---|---|
| L0 访客 | 中性灰 `--perm-level-l0` | 文字 `#86909C`，透明底 | 底 `#F2F3F5`，文字 `#4E5969` | 底 `#FFFFFF` 浮块 + 文字 `#86909C` + 下边 2px `#86909C` |
| L1 注册 | 主色阶浅 `--perm-level-l1` | 文字 `#4E5969`，透明底 | 底 `#E8F3FF`，文字 `#4080FF` | 底 `#FFFFFF` 浮块 + 文字 `#4080FF` + 下边 2px `#4080FF` |
| L2 专业 | 主色 `--perm-level-l2` | 文字 `#4E5969`，透明底 | 底 `#E8F3FF`，文字 `#165DFF` | 底 `#FFFFFF` 浮块 + 文字 `#165DFF`（500）+ 下边 2px `#165DFF` |
| L3 内部 | 强调 `--perm-level-l3` | 文字 `#4E5969`，透明底 | 底 `#E8F3FF`，文字 `#0E42B3` | 底 `#FFFFFF` 浮块 + 文字 `#0E42B3`（500）+ 下边 2px `#0E42B3` |
| L4 管理 | 管理橙 `--perm-level-l4` | 文字 `#4E5969`，透明底 | 底 `#FFF7E8`，文字 `#FF7D00` | 底 `#FFFFFF` 浮块 + 文字 `#FF7D00`（500）+ 下边 2px `#FF7D00` |

> 选中态遵循 Arco `Segmented` 的「白色浮块 thumb」语义（不是整段蓝底），与 D8 §10「选中=蓝色文字/蓝色底」一致；配色阶通过**文字色 + 下划强调线**体现级别差异，底色统一克制（白浮块），不做满段高饱和。

### 2.3 控件态示意（ASCII）

```
app-header 右区（高 32px）
┌──────────────────────────────────────────────────────────┐
│  级别：[ L0 访客 ][ L1 注册 ][▌L2 专业▐][ L3 内部 ][ L4 管理 ]  │  ← 整体胶囊容器底 #F2F3F5
└──────────────────────────────────────────────────────────┘
                          ▲
                  选中项=白浮块+#165DFF文字+底部2px蓝线

常态项：透明底 / #4E5969 文字
hover ：#E8F3FF 浅蓝底 / 对应级别强调色文字
选中  ：#FFFFFF 浮块 + 对应级别色文字(500) + 2px 下强调线
切换旁：若涉及 Q026 升级路径未定 → 右挂 ⚠️(见 §5.3)
```

### 2.4 最小 CSS 片段（仅样式，不接逻辑）

```css
.perm-level-seg.arco-segmented {
  height: 32px;
  border-radius: 999px;
  background: var(--sci-surface-hover, #f2f3f5);
  font-size: 14px;
}
.perm-level-seg .arco-segmented-item {
  color: var(--sci-text-2, #4e5969);
  border-radius: 999px;
}
.perm-level-seg .arco-segmented-item:hover {
  background: var(--sci-primary-soft, #e8f3ff);
}
/* 选中浮块（Arco thumb）统一白底，级别差异靠文字色 + 下强调线 */
.perm-level-seg .arco-segmented-item-selected {
  background: #fff;
  font-weight: 500;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);
}
.perm-level-seg .arco-segmented-item-selected[data-level='L2'] { color: #165dff; box-shadow: inset 0 -2px 0 #165dff; }
.perm-level-seg .arco-segmented-item-selected[data-level='L3'] { color: #0e42b3; box-shadow: inset 0 -2px 0 #0e42b3; }
.perm-level-seg .arco-segmented-item-selected[data-level='L4'] { color: #ff7d00; box-shadow: inset 0 -2px 0 #ff7d00; }
```

### 2.5 与 Design.md 对照

| 维度 | 取值 | D8 章节 |
|---|---|---|
| 控件高 32px | ✅ | §0 / §7 |
| 主色 #165DFF（L2 选中） | ✅ | §4.1 / §10 |
| 圆角 3px/999px | ✅ | §6.1 |
| 字号 14px | ✅ | §5.2 |
| 选中=蓝字 + 浅蓝底语义 | ✅ | §10 / §7.3 |
| 组件 Segmented | ✅ | §13 操作类 |

---

## 3. 身份标识徽标（GOV / INNO·THINK / VISIT，D8 §7.4 Tag / §13 Badge）

### 3.1 选型与规格

- **组件**：顶部使用自定义胶囊按钮（保留 Arco Button/Dropdown/Menu 语义）；面板内列表项可用 Arco `Dropdown` / `Menu` 语义组合。视觉遵循 D8 `Tag` 胶囊和浅色面板规则。
- **顶部高度**：`32px` 主胶囊；左侧圆形身份标识 `40px` 左右可突出当前 Persona；圆角 `999px`。
- **位置**：`app-header` 右区。它替代原来平级摆放的级别切换器 + 身份徽标。
- **交互**：点击胶囊展开二级面板；选择 Persona 自动带出推荐 Level；Level 调节在面板内弱化呈现。
- **图标**：用 Arco Icon 线性图标，**禁 emoji**（D8 §12.3）。

### 3.2 三徽标视觉

| 身份 | 文案 | 图标（Arco Icon 建议） | 浅底 | 文字 | 边框 |
|---|---|---|---|---|---|
| GOV 驾驶舱 | `GOV · 驾驶舱` | `IconDashboard` | `#E8F3FF`（品牌浅蓝） | `#165DFF` | `#ADC6FF`（蓝系浅边，派生） |
| INNO·THINK 工作台 | `INNO · 工作台` | `IconCommon`/`IconApps` | `#E8FFEA`（成功浅底） | `#00B42A` | `#AFF0B5`（绿系浅边，派生） |
| VISIT 只读 | `VISIT · 只读` | `IconEye` | `#F7F8FA`（填充浅灰） | `#86909C` | `#E5E6EB` |

> 配色逻辑：GOV=驾驶舱→主蓝系（决策结论优先）；INNO=工作台→成功绿系（创新/明细，复用 D8 §4.2 状态色，非新发明）；VISIT=只读→中性灰（弱化）。三者底色均淡，不抢业务图表色。

### 3.3 顶部胶囊 + 二级面板结构（推荐）

```
app-header 右区：
┌───────────────────────────────┐
│  普   GOV · 驾驶舱        ▾   │
└───────────────────────────────┘
  左圆标：当前 Level 简称（访/注/专/内/管 或 普/专/内/管，按 UI 最终口径）
  主文案：当前 Persona
  右图标：下拉箭头

点击展开：
┌────────────────────────────────────────────────────┐
│ GOV · 驾驶舱                         >   L3 内部   │ ← 推荐组合，当前行浅蓝底
│ INNO · 工作台                        >   L2 专业   │
│ THINK · 工作台                       >   L2 专业   │
│ VISIT · 只读                         >   L0 访客   │
│ OPS · 后台                           >   L4 管理   │
│ SYS · 后台                           >   L4 管理   │
│────────────────────────────────────────────────────│
│ 高级演示调节： L0 访客 / L1 注册 / L2 专业 / L3 内部 / L4 管理 │
│ 演示模式：切换视角会影响默认视图与可见数据范围                │
└────────────────────────────────────────────────────┘
```

面板规则：

- Persona 列为主列表，字号和选中态强于 Level 区。
- 推荐 Level 显示在每行右侧，作为自动带出结果，不做成与 Persona 平级的主入口。
- “高级演示调节”用 12px 次级标题 + 紧凑分段控件或按钮组，整体视觉弱化。
- 非推荐组合时，在高级调节区下方追加 `Alert` / 轻提示：`该组合仅用于权限边界演示，非真实业务角色`，使用警示浅底，不打断操作。

### 3.4 最小 CSS 片段

```css
.persona-switch {
  height: 32px;
  border-radius: 999px;
  padding: 0 12px 0 4px;
  font-size: 14px;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  border: 1px solid rgba(22, 93, 255, 0.18);
  background: rgba(232, 243, 255, 0.72);
  color: var(--sci-text-1);
}
.persona-switch__level {
  width: 40px;
  height: 40px;
  border-radius: 999px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: var(--sci-surface-solid);
  color: var(--sci-primary);
  font-weight: 600;
  box-shadow: 0 0 0 4px rgba(255, 255, 255, 0.48);
}
.persona-menu {
  min-width: 560px;
  border-radius: var(--sci-radius-card);
  background: var(--sci-surface-solid);
  border: 1px solid var(--sci-border);
  box-shadow: var(--sci-shadow-popover);
}
.persona-menu__row {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 24px 160px;
  align-items: center;
  min-height: 44px;
  padding: 0 24px 0 20px;
}
.persona-menu__row.is-active {
  background: var(--sci-primary-soft);
  color: var(--sci-primary);
}
.persona-menu__advanced {
  border-top: 1px solid var(--sci-border);
  padding: 12px 20px 16px;
  color: var(--sci-text-2);
  font-size: 12px;
}
.persona-menu__warning {
  margin-top: 8px;
  border-radius: var(--sci-radius-ctrl);
  background: #fff7e8;
  color: #ff7d00;
  padding: 6px 8px;
}
```

### 3.5 与 Design.md 对照

| 维度 | 取值 | D8 章节 |
|---|---|---|
| 顶部胶囊 32px / 浅底深字 | ✅ | §7.4 / §7.1 |
| 圆角胶囊 999px | ✅ | §6.1 |
| 状态色复用（绿/蓝/灰） | ✅ | §4.2 |
| 线性图标、禁 emoji | ✅ | §12.3 |

---

## 4. 降级态视觉（🔒 / 灰显 / Tooltip / 升级入口，对照 UX §3.3，D8 §7.1 Button / §10）

> 降级**非阻断**：无权不整页 403，关键转化入口保留可见。统一表现 = `disabled 灰显 + 🔒 锁标 + Tooltip + 转化入口`。

### 4.1 四种降级形态视觉

| 形态 | 适用对象 | 视觉规格 |
|---|---|---|
| **A. 灰显锁定按钮** | `interact`/`deep`/`personal` 类无权按钮（下钻/对比/视图切换/高级筛选/导出等） | 次级按钮外形 + 文字色 `#86909C`（`--sci-text-3`）+ 底 `#F7F8FA` + 边 `#E5E6EB` + 前置 🔒（Arco `IconLock` 12–14px，色 `--perm-lock-fg`）；`cursor:not-allowed`；保留可点（触发 Tooltip + 转化），不真正 disabled 屏蔽点击 |
| **B. Tooltip 提示** | 上述按钮 hover | Arco `Tooltip`，白底深字 12px，文案如「登录后下钻」「升级专业用户解锁」「内部权限可用」；底部带转化入口（见 D） |
| **C. 打码占位** | `view-sensitive` 敏感字段（联系方式/法人/财务） | 字段值替换为 `••••••` 占位（`--sci-text-3` 色），旁挂「申请查看」文字按钮（L2 起可申请）；非前端假脱敏，仅占位演示态（Wave0🧪） |
| **D. 转化入口按钮** | 登录/升级/申请 | **主按钮**（D8 §7.1）：底 `#165DFF`、白字、高 32px（行内场景可用 24px 小按钮）、圆角 3px；文案「登录」「升级专业用户」「申请权限」 |

### 4.2 降级态示意（ASCII）

```
正常按钮（有权）：
  [ 下钻分析 ]   主/次按钮，#165DFF 或白底蓝边，32px

降级按钮（无权，形态 A+B+D）：
  [🔒 下钻分析 ]   灰字 #86909C / 底 #F7F8FA / 边 #E5E6EB
        │ hover
        ▼
  ┌────────────────────────────┐
  │ 登录后可下钻分析             │ ← Tooltip 12px
  │           [ 登录 ]          │ ← 转化主按钮 #165DFF
  └────────────────────────────┘

敏感字段（形态 C）：
  联系电话： ••••••••  [申请查看]   ← 占位灰 + 文字按钮(L2起)
```

### 4.3 升级/登录/申请按钮体系（D8 §7.1）

| 按钮 | 类型 | 底色 | 文字 | 高 | 圆角 | hover |
|---|---|---|---|---|---|---|
| 登录（L0 常驻 header） | 主按钮 | `#165DFF` | `#FFFFFF` | 32px | 3px | `#4080FF` |
| 升级专业用户 | 主按钮 | `#165DFF` | `#FFFFFF` | 32px/24px | 3px | `#4080FF` |
| 申请权限/申请敏感 | 次级按钮 | `#FFFFFF` | `#165DFF` | 32px/24px | 3px | 底 `#E8F3FF` |
| 注册（L0 常驻） | 次级按钮 | `#FFFFFF` | `#1D2129` | 32px | 3px | 蓝描边/浅蓝底 |

### 4.4 最小 CSS 片段

```css
/* 降级灰显锁按钮 */
.btn-locked {
  height: 32px;
  border-radius: 3px;
  font-size: 14px;
  color: var(--sci-text-3, #86909c);
  background: var(--sci-surface-soft, #f7f8fa);
  border: 1px solid var(--sci-border, #e5e6eb);
  cursor: not-allowed;
  display: inline-flex;
  align-items: center;
  gap: 4px;
}
.btn-locked .icon-lock { color: var(--perm-lock-fg, #86909c); font-size: 14px; }
/* 敏感打码占位 */
.sensitive-masked { color: var(--sci-text-3, #86909c); letter-spacing: 2px; }
/* 转化主按钮沿用 Design.md §7.1 Arco 覆盖 */
.btn-upgrade.arco-btn-primary { height: 32px; border-radius: 3px; background: #165dff; border-color: #165dff; }
.btn-upgrade.arco-btn-primary:hover { background: #4080ff; border-color: #4080ff; }
```

### 4.5 与 Design.md 对照

| 维度 | 取值 | D8 章节 |
|---|---|---|
| 主按钮 #165DFF/32px/3px | ✅ | §7.1 |
| disabled 文字 #86909C / 底 #F7F8FA / 边 #E5E6EB | ✅ | §10 |
| Tooltip 白底深字 | ✅ | §10 error/提示 + §13 |
| 锁标用 Arco Icon 非 emoji | ✅ | §12.3 |
| 非阻断（不整页 403） | ✅ | §10 empty/error |

> ⚠️ **关于 🔒/🧪/⚠️/ⓘ 符号**：UX 文档与 D9 规约以 emoji 命名这些角标（🔒/🧪/⚠️/ⓘ）。落地时 D8 §12.3「禁用 emoji 表达状态/菜单」优先——**一律用 Arco Icon 线性图标实现**（`IconLock` / `IconExperiment` / `IconExclamationCircle` / `IconInfoCircleFill`），本文沿用 emoji 仅作**语义标记/阅读锚点**，FE 实现必须替换为矢量图标。

---

## 5. D9 角标视觉（ⓘ / 🧪 / ⚠️ + MetricSpecCard + DataLineageDrawer，对照 UX §4 + data-lineage-policy §5.1）

### 5.1 三角标视觉规格

| 角标 | Arco Icon 实现 | 尺寸 | 常态色 | hover/激活 | 浅底（可选胶囊） |
|---|---|---|---|---|---|
| ⓘ MetricSpecCard 触发 | `IconInfoCircle` | 14px | `#4E5969`（次文字） | `#165DFF` | 无（紧贴数字右侧） |
| 🧪 MockBadge | `IconExperiment` | 14px | `#FF7D00`（警示橙） | tooltip | 底 `#FFF7E8` 胶囊（可选） |
| ⚠️ 待确认 | `IconExclamationCircle` | 14px | `#FF7D00`（警示橙） | tooltip | 底 `#FFF7E8` 胶囊（可选） |

> 🧪 与 ⚠️ 共用警示橙色系（D8 §4.2，非新发明），靠**图标形状**区分（试管 vs 感叹号），避免引入新色。

### 5.2 共存优先级与放置（UX §4.2）

```
数字右侧顺序：  数字 → ⓘ → 🧪 → ⚠️
示例（E-20 KPI「创新型企业数」含 pending Q011）：
   412  ⓘ 🧪 ⚠️
    │    │  │  └ hover：口径待甲方确认(Q011)，现按临时默认展示
    │    │  └ hover：当前为 Mock 数据，预计 {mock_until} 切真实源 {source_systems}
    │    └ hover/点击：弹 MetricSpecCard（见 §5.4）
    └ 关键数值 24–34px 600（--sci-font-metric）
```

- ⓘ **始终在**（每个统计数字必有，D9 §7.5 铁律：禁删 ⓘ）；🧪/⚠️ 条件出现。
- 角标只读、不参与权限降级（与密级脱敏正交）。
- 角标间距 `4px`；与数字间距 `4px`。

### 5.3 MetricSpecCard 卡片视觉（data-lineage-policy §5.1.1）

- **触发**：ⓘ hover/点击弹出（Arco `Popover` 或 `Card` 浮层）。
- **样式**：浅色蓝灰底 `--lineage-card-bg`（`#F7F8FA`）+ **8px 圆角**（`--sci-radius-card`）+ 1px `#E5E6EB` 描边 + `--sci-shadow-popover` 轻阴影；**不深色霓虹**。
- **内容**：8 件套前 7 项（`metric_id` / 中文名 / 口径定义 / 公式 / 源表 / 源系统 / 更新频率；version 收副信息）。用 Arco `Descriptions`（D8 §13 展示类）。
- **底部**：「查看完整加工链路」文字按钮 → `DataLineageDrawer`（Wave1）。
- **降级**：catalog 失败显示「数据说明加载中」（不阻塞）。

```
┌─ MetricSpecCard ──────────────────────────────┐  底 #F7F8FA / 8px 圆角
│ M_ENT_INNOVATIVE_COUNT          [version v1.0] │  标题 14px 600 + 副信息 12px 弱
│ ────────────────────────────────────────────── │
│ 中文名   创新型企业数                            │  Arco Descriptions
│ 口径定义 统计窗口内...去重逻辑...（≥50字）       │  正文 14px / 行高 22px
│ 公式     COUNT(DISTINCT ...) WHERE is_innov...  │  等宽/12px
│ 源表     dwd.enterprise ← ods:dwd_org_tag_info  │
│ 源系统   Mock @ batch=mock_2026... (🧪)         │
│ 更新频率 daily                                  │
│ ────────────────────────────────────────────── │
│              [ 查看完整加工链路 → ]              │  文字按钮 #165DFF
└────────────────────────────────────────────────┘
```

### 5.4 DataLineageDrawer 抽屉视觉（data-lineage-policy §5.1.2 + D8 §7.8）

- **触发**：MetricSpecCard 底部按钮。
- **方向/宽度**：右侧滑出，宽 `480–720px`（D8 §7.8），本场景建议 `600px`。
- **内容**：`ODS → DWD → DWS → ADS` 4 段血缘 + 算法节点（G6/mermaid 渲染，业务自定义容器遵 D8）。
- **样式**：白底、标题/关闭/底部操作区完整、边框阴影克制（D8 §7.8）；血缘节点用要素色克制点缀，连线浅灰蓝 `#DCE9FF`。
- **Wave0 占位**：Wave1 才上线，Wave0 点击显示「血缘图建设中（Wave1）」空态（保留外壳，D8 §10 empty）。

```
                         ┌─ DataLineageDrawer (右滑 600px) ──┐
                         │ 数据血缘 · M_ENT_INNOVATIVE_COUNT  ✕│
                         │ ───────────────────────────────── │
                         │  ODS ──→ DWD ──→ DWS ──→ ADS        │  4 段，连线 #DCE9FF
                         │  ┌──┐   ┌──┐   ┌──┐   ┌──┐         │
                         │  │  │   │ ⚙ │   │  │   │  │         │  ⚙=算法节点
                         │  └──┘   └──┘   └──┘   └──┘         │
                         │  Wave0：血缘图建设中（Wave1）空态    │
                         │ ───────────────────────────────── │
                         │                       [ 关闭 ]      │
                         └─────────────────────────────────────┘
```

### 5.5 最小 CSS 片段

```css
.metric-info-icon { color: var(--lineage-info-fg, #4e5969); font-size: 14px; cursor: pointer; margin-left: 4px; }
.metric-info-icon:hover { color: #165dff; }
.metric-badge { font-size: 14px; color: #ff7d00; margin-left: 4px; }
.metric-badge--soft { background: #fff7e8; border-radius: 999px; padding: 0 4px; }
.metric-spec-card {
  background: var(--lineage-card-bg, #f7f8fa);
  border: 1px solid var(--sci-border, #e5e6eb);
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  padding: 12px 16px;
  min-width: 320px;
}
.lineage-drawer .arco-drawer-content { background: #fff; }
.lineage-node-line { stroke: #dce9ff; }
```

### 5.6 与 Design.md / D9 对照

| 维度 | 取值 | 出处 |
|---|---|---|
| MetricSpecCard 浅蓝灰 + 8px 圆角 | ✅ | D9 §5.1.1 |
| Drawer 右滑 480–720px | ✅ | D8 §7.8 |
| ⓘ 始终在、不删 | ✅ | D9 §7.5 |
| Wave0 全显 🧪 | ✅ | D9 §5.1.3 |
| 角标用 Arco Icon 非 emoji | ✅ | D8 §12.3 |
| 血缘连线浅蓝 #DCE9FF | ✅ | D8 §6.2 |

---

## 6. 菜单锁态（app-sidebar 菜单项 🔒 升级态，对照 UX §3.3.5，D8 §3.3 / §13 Menu）

### 6.1 选型与规格

- **组件**：Arco `Menu`（D8 §13 导航类）。展开宽 200px（D8 §3.1）。
- **正常菜单项**：行高 ≈40px（菜单项），文字 14px `#1D2129`；选中=浅蓝底 `#E8F3FF` + 蓝字 `#165DFF`（D8 §3.3）。
- **锁态菜单项**：可见但锁定（**非阻断、不隐藏**，保留做转化，UX §3.3.5）。

### 6.2 菜单锁态视觉

| 态 | 文字色 | 图标 | 行底 | 交互 |
|---|---|---|---|---|
| 正常（有权） | `#1D2129` | 业务线性图标 | 透明 / hover `#F2F3F5` | 点击进路由 |
| 选中 | `#165DFF`（500） | 同上 | `#E8F3FF` | — |
| **锁态（无权 L1 看 L2 菜单）** | `#86909C`（弱文字） | 业务图标变灰 + **行尾 🔒**（`IconLock` 14px，`--perm-lock-fg`） | 透明 | hover→Tooltip「升级专业用户解锁企业分析」；点击不进路由，弹升级引导（不整页跳转） |

### 6.3 菜单锁态示意（ASCII）

```
app-sidebar (200px)  企业分析菜单组（L1 用户视角）
┌────────────────────────────┐
│ 📊 企业分析概览·驾驶舱        │ ← 正常(可进，L1 进入仅结论条)
│ ▌企业分析概览·驾驶舱▐  选中  │ ← #E8F3FF 底 + #165DFF 字
│ ─ 重点企业类型分析    🔒     │ ← 锁态：灰字 #86909C + 行尾 IconLock
│ ─ 领域分布分析        🔒     │
│ ─ 能力评估(技术/商业) 🔒     │
│ ─ 深圳现状/多城市对标 🔒     │
│ ...                          │
└────────────────────────────┘
        hover 锁项 ▼
   ┌──────────────────────────────┐
   │ 升级专业用户解锁企业分析       │ Tooltip
   │           [ 升级 ]            │ 转化主按钮 #165DFF
   └──────────────────────────────┘
```

### 6.4 最小 CSS 片段

```css
.arco-menu-item.is-locked {
  color: var(--sci-text-3, #86909c);
}
.arco-menu-item.is-locked .menu-lock {
  margin-left: auto;
  color: var(--perm-lock-fg, #86909c);
  font-size: 14px;
}
/* 选中态守 Design.md §3.3 */
.arco-menu-item.arco-menu-selected {
  background: var(--sci-primary-soft, #e8f3ff);
  color: var(--sci-primary, #165dff);
  font-weight: 500;
}
```

### 6.5 与 Design.md 对照

| 维度 | 取值 | D8 章节 |
|---|---|---|
| sidebar 展开 200px | ✅ | §3.1 |
| 选中浅蓝底 #E8F3FF + 蓝字 | ✅ | §3.3 |
| 锁态弱文字 #86909C | ✅ | §10 disabled |
| 非阻断（不隐藏菜单） | ✅ | UX §3.3.5 + D8 §10 |
| 🔒 用 Arco IconLock | ✅ | §12.3 |

---

## 7. 权重只读态（weight L3 以下只读展示，对照 UX §3.2/§3.3.2，D8 §7 / §10）

> `btn:common:weight`（权重/口径配置）需 L3；L1/L2 降级为**只读展示当前权重**（不可编辑），出现在 E-23/E-24 能力评估、E-30 综合竞争力。

### 7.1 可编辑态 vs 只读态视觉区分

| 维度 | 可编辑态（L3+） | 只读展示态（L3 以下） |
|---|---|---|
| 控件 | Arco `InputNumber`/`Slider`（32px，白底，蓝 focus） | 纯文本 + 进度条静态展示（无输入框边框） |
| 数值色 | `#1D2129` 主文字 | `#4E5969` 次文字 |
| 进度条 | `#165DFF` 实心可拖 | `#4080FF` 静态填充（无拖拽手柄） |
| 操作区 | `[保存] [重置]` 主/次按钮 | 隐藏；改为「内部权限可调」灰提示 + `[申请权限]` 次级按钮 |
| 标识 | — | 只读 `IconLock` 或「只读」`Tag`（弱灰）+ 可附 ⓘ 看口径 |

### 7.2 权重只读态示意（ASCII）

```
可编辑态（L3+）：
  专利权重   [  25 ] %  ━━━━━●━━━━━  [保存] [重置]
             InputNumber 32px        蓝实心可拖

只读展示态（L1/L2）：
  专利权重   25%  ⓘ        ━━━━━━━━░░░░  (只读)
  技术权重   60%  ⓘ        ━━━━━━━━━━░░  (只读)   ← #4080FF 静态填充
  ──────────────────────────────────────────
  权重口径调整需内部权限   [ 申请权限 ]   ← 次级按钮 #165DFF 字/白底
```

### 7.3 最小 CSS 片段

```css
.weight-readonly .weight-value { color: var(--sci-text-2, #4e5969); font-weight: 500; }
.weight-readonly .weight-bar {
  height: 6px;
  border-radius: 999px;
  background: var(--sci-surface-hover, #f2f3f5);
}
.weight-readonly .weight-bar > i {
  display: block;
  height: 100%;
  border-radius: 999px;
  background: #4080ff; /* 静态填充，区别可编辑的 #165dff 可拖 */
}
.weight-readonly .weight-tip { color: var(--sci-text-3, #86909c); font-size: 12px; }
```

### 7.4 与 Design.md 对照

| 维度 | 取值 | D8 章节 |
|---|---|---|
| InputNumber/Slider 32px | ✅ | §7.2 / §13 |
| 只读=次文字 #4E5969 | ✅ | §5.2 / §10 |
| 进度条蓝系（无新色） | ✅ | §4.1 |
| 申请按钮次级样式 | ✅ | §7.1 |

---

## 8. 概览去重后布局（E-20 移除"结构洞察"tab 后单视图驾驶舱，对照 UX §1.5，D8 §3）

> E-20 概览去 tab 后 = **单视图驾驶舱**，专题 MEDIUM 标准浅色工作台，**禁大屏酷炫态**（D8 §0/§12.3 + ARCH §6.1.3）。

### 8.1 布局骨架（D8 §3.1 六容器 + §3.2 工作区）

```
app-shell (底 #D8E7FC)
└─ app-frame  grid: 200px | 1fr ; rows: 64px | 1fr
   ├─ app-header(64px)   [Logo「科技专题服务·企业」] ... [级别切换器 §2][身份徽标 §3][用户菜单]
   ├─ app-sidebar(200px) [企业分析菜单组：dash 选中 / type·domain·... 🔒 §6]
   └─ content-shell(margin 16px, 白半透明, 圆角 10px, 白描边)
      ├─ filter-row(88–104px)   产业范围 | 区域 | 年份 | 关键字   [查询主按钮]
      ├─ JudgmentStrip 结论条    本期企业总数 1,286 ⓘ🧪 / 创新型 32% ⓘ🧪⚠️ …
      ├─ MetricCard ×5（核心指标）每卡：关键数值24–34px + ⓘ🧪(+⚠️) + 标题
      ├─ workspace-grid（概览用双列分析区，非强制三段）
      │   ├─ analysis-panel-左：历年新增企业趋势（ECharts 折线，业务蓝系）
      │   └─ analysis-panel-右：全国分布（点击省→下钻 E-21，带 region）
      ├─ 重点企业 TopN 列表（[加入对比篮][打开画像 Drawer]）
      └─ 决策链下钻入口 Button 组：
            [→ 类型分析 P1/E-21] [→ 领域分布 P2/E-22] [→ 深圳现状 P5/E-25]
            [→ 引育推荐 P6] [→ 综合竞争力 P10/E-30(L3 强调)]
      ✗ 已移除：原"结构洞察"二级 Tabs（企业全景/类型概览/领域概览）整组
```

### 8.2 L1 / L2 分级视觉差异（同一页两态，UX §1.5.4 + §2.3）

| 区块 | L1（入门级，仅结论条） | L2（分析级，完整） |
|---|---|---|
| JudgmentStrip 结论条 | ✅ 完整显示 | ✅ 完整显示 |
| MetricCard ×5 | 降级：仅显示数值，下钻/视图切换锁 🔒（或整组弱化） | ✅ 完整 + 可下钻 |
| 趋势/全国分布 | 降级灰显或收起（按 Q031 临时默认） | ✅ 完整可交互 |
| TopN + 多维对比 | 单维可见，多维对比 🔒「升级专业」 | ✅ 多维 |
| 决策链下钻入口 | 各按钮按目标页 minLevel 显示锁态（type/domain→🔒） | ✅ 解锁 |
| 视图切换/布局/高级筛选 | 🔒「升级专业用户」 | ✅ |

> ⚠️ E-20 L1「仅结论条」精确范围（哪些 KPI/图表对 L1 隐藏 vs 显示）= Q031 待甲方确认，视觉上对降级块统一加 ⚠️「待甲方确认」角标（§5.1），FE 按临时默认实现。

### 8.3 单视图驾驶舱视觉守则（禁大屏酷炫）

| 守则 | 取值 | D8 章节 |
|---|---|---|
| 底色浅蓝 #D8E7FC，非深色大屏 | ✅ | §0/§14 |
| content-shell 白半透明 + 圆角 10px + 白描边 | ✅ | §3.1 |
| 关键数值 24–34px（服务分析，非海报巨字） | ✅ | §5.2 |
| 普通卡片无强阴影（仅浮层轻阴影） | ✅ | §6.3 |
| 禁霓虹/紫蓝发光/赛博网格/玻璃拟态炫光 | ✅ | §0/§12.3 |
| 图表用要素色/图表序列，连续量同色系渐变 | ✅ | §4.3/§9 |
| 保留右侧分析收口（双列分析区即承载） | ✅ | §3.2/§8.3 |

---

## 9. Design.md §14 检查清单逐条对照

### 9.1 §14 检查项 8 条

| # | 检查项 | 本规范结论 | 说明 |
|---|---|---|---|
| 1 | 仍是浅蓝白科技工作台，非深色大屏？ | ✅ | 全程底色 #D8E7FC、浅色工作台；§8 明确禁大屏酷炫 |
| 2 | 保留 Header/左导航/主容器/中央主视图/右侧分析？ | ✅ | §8.1 六容器骨架 + 双列分析收口 |
| 3 | 选中态统一 #165DFF / #E8F3FF？ | ✅ | §2 切换器、§6 菜单选中、§3 GOV 徽标均守 |
| 4 | 表单/按钮/分页/标签接近 Arco 节奏？ | ✅ | Segmented/Tag/Button/Menu/Descriptions 全用 Arco（§2/§3/§4/§6） |
| 5 | 地图工具栏/图例/筛选项尺寸克制？ | ✅ | 控件 32px、角标 14px、Tag 24px |
| 6 | 有 loading/empty/disabled/error 状态？ | ✅ | 降级 disabled（§4）、MetricSpecCard catalog 失败 loading、Drawer Wave0 empty、菜单锁态 disabled |
| 7 | 图表颜色遵循要素色/图表序列（§4.3）？ | ✅ | §8.3 明确趋势/分布用业务蓝系 + 图表序列 |
| 8 | 避免霓虹/紫蓝发光/营销 hero/emoji/无意义占位？ | ✅ | §4.5 注明角标 emoji 仅语义锚点、FE 用 Arco Icon；禁发光 |

### 9.2 §14 验收 6 条

| # | 验收项 | 本规范结论 | 说明 |
|---|---|---|---|
| 1 | 首屏像地图/图谱分析工作台，非卡片仪表盘 | ✅ | §8.1 工作台骨架 + 双列分析区 |
| 2 | Header 高度接近 64px | ✅ | §8.1 app-header 64px |
| 3 | 左导航接近 200px | ✅ | §6.1 / §8.1 sidebar 200px |
| 4 | 表单/按钮/分页/工具栏高度接近 32px | ✅ | §1.1 `--sci-control-h:32px` 全引用 |
| 5 | 主色取样接近 #165DFF | ✅ | §1.2 L2/升级/选中均 #165DFF |
| 6 | 无 antd / vendor-antd / .ant- class | ✅ | §0 组件库铁律 Arco；所有 className 用 `.sci-*/.perm-*/.arco-*` 覆盖 |

> 综合：§14 共 14 条 **全过（✅14 / N/A 0 / ❌0）**。本规范为视觉文档（无运行代码），验收 1–5 由 FE（E-PERM-L03）落地后截图取样最终核验；本文已逐条给出 token/规格保证可达成。

---

## 10. handoff：DoD 对照 + FE 接力 + 成本回填

### 10.1 DoD 对照（任务 7 类视觉全覆盖）

| # | 任务要求（7 类） | 本文章节 | 覆盖 |
|---|---|---|---|
| 1 | 级别切换器 L0–L4（配色阶 + 三态 + Segmented 32px） | §2 | ✅ |
| 2 | 身份标识徽标（GOV/INNO·THINK/VISIT） | §3 | ✅ |
| 3 | 降级态（🔒/灰显/Tooltip/升级登录申请按钮） | §4 | ✅ |
| 4 | 权重只读态（区别可编辑态） | §7 | ✅ |
| 5 | D9 角标（ⓘ/🧪/⚠️/MetricSpecCard/DataLineageDrawer） | §5 | ✅ |
| 6 | 菜单锁态（app-sidebar 🔒 升级态） | §6 | ✅ |
| 7 | 概览去重后布局（E-20 单视图驾驶舱） | §8 | ✅ |
| — | 全局 token 表 | §1 | ✅ |
| — | Design.md §14 对照 | §9 | ✅（14/14 过） |

补充范围自检（团队公约）：未写业务逻辑 ✅ / 未改路由 ✅ / 未改业务口径 ✅ / 仅 commit 不 push ✅ / 专题仅 PC 无大屏小屏态 ✅ / 禁 antd 用 Arco ✅ / 未替甲方拍板（沿用 ⚠️ 角标）✅ / 未重设计业务页 ✅。

### 10.2 给 frontend-agent（E-PERM-L03）实现接力

| UI 态 | 建议组件名 | className 建议 | token 变量 | Arco 基座 |
|---|---|---|---|---|
| 级别切换器 | `<PermLevelSwitcher>` | `.perm-level-seg` | `--perm-level-l0..l4` | `Segmented` |
| 身份徽标 | `<PersonaTag>` | `.persona-tag--gov/inno/visit` | `--sci-primary-soft` 等 | `Tag` + `Dropdown` |
| 降级锁按钮 | `<PermGate>` 包 `<LockedButton>` | `.btn-locked` / `.btn-upgrade` | `--perm-lock-fg/-bg/-border` | `Button` + `Tooltip` |
| 敏感打码 | `<MaskedField>` | `.sensitive-masked` | `--sci-text-3` | 文本 + `Button`(text) |
| 权重只读 | `<WeightReadonly>` | `.weight-readonly` | `--sci-primary-hover` | `Progress`/静态 |
| ⓘ 角标 | `<MetricInfoIcon>` | `.metric-info-icon` | `--lineage-info-fg` | `IconInfoCircle`+`Popover` |
| 🧪 MockBadge | `<MockBadge>` | `.metric-badge--soft` | `--perm-mock` | `IconExperiment`+`Tooltip` |
| ⚠️ 待确认 | `<PendingBadge>` | `.metric-badge` | `--perm-pending` | `IconExclamationCircle`+`Tooltip` |
| 数据说明卡 | `<MetricSpecCard>` | `.metric-spec-card` | `--lineage-card-bg` | `Card`/`Popover`+`Descriptions` |
| 血缘抽屉 | `<DataLineageDrawer>` | `.lineage-drawer` | `--sci-map-border` | `Drawer` + G6/mermaid |
| 菜单锁态 | `<SidebarMenu>` item `is-locked` | `.arco-menu-item.is-locked .menu-lock` | `--perm-lock-fg` | `Menu` + `IconLock` |
| 概览驾驶舱 | `<EnterpriseOverviewDash>` | 六容器 `.app-*/.content-shell/.workspace-grid` | 全局 §1.1 | `Layout`/`Grid` |

实现要点：
1. **角标 emoji 必须替换为 Arco Icon**（D8 §12.3，详 §4.5）；本文 emoji 仅阅读锚点。
2. **颜色全部走 CSS 变量**（§1），禁页面内硬编码主色（ui.mdc 约束）。
3. **降级非阻断**：`<PermGate>` 越权渲染 `LockedButton`（disabled 视觉 + Tooltip + 转化入口），不整页 403。
4. **专题恒 MEDIUM**：不引入大屏 `showcase` 态；`screens:[MEDIUM]`。
5. **L4 管理橙**仅切换器列项出现，企业前台页不渲染 L4 态。
6. demo→lumen 走 PR 非直搬；`demo-ui-topic` 改动 push 前确认 PM（公约 §4.2 + ARCH §6.2）。

### 10.3 成本回填（cost_tracking_policy）

| 字段 | 值 |
|---|---|
| estimated_tokens | 110,000 |
| actual_tokens | ~95,000 |
| model_used | claude-opus-4.8 |
| actual_cost | ~$1.9 |
| cost_warn | green |

---

**本文档为 UI 视觉规范（无运行代码）；角标 emoji 命名仅作语义锚点，FE 落地一律用 Arco Icon。Q010~Q032 业务口径经甲方确认升 🟢 后，UI/FE 移除对应 ⚠️ 角标。E-20 去重单视图驾驶舱沿用 UX 方案 B（独立页权威），由 FE（E-PERM-L03）落地。**

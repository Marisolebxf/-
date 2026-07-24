# UI-HIFI-ENT-OPS 会签单 · 维护管理全量 15 项菜单

> **版本**：`HIFI-ENT-OPS-medium-v0.2`  
> **任务**：`ENT-MOD-OPS-V1-HIFI`  
> **仓**：`demo-ui-topic`  
> **日期**：2026-07-24  
> **执行**：`agent:ui-agent` · **监管**：`human:淮政玮`  
> **会签决策人（登记）**：`human:高颖` + `human:孔东`  
> **真源**：`ENT-OPS-维护管理/企业维护管理-能力全清单.md` v0.2

## 1. 预览入口

| 分组 | 路径 |
| --- | --- |
| 门户内容（默认） | `/enterprise-center/maintenance?tab=portal` |
| 企业主体 | `/enterprise-center/maintenance?tab=entity` |
| 企业动态与区域 | `/enterprise-center/maintenance?tab=entity_dynamics` |
| 企业实体生命周期 | `/enterprise-center/maintenance?tab=lifecycle` |
| 其余 11 项占位 | `/enterprise-center/maintenance?tab=<id>`（非法 tab 回退 `portal`） |

本地：`cd repos/demo-ui-topic && npm run dev` → `http://localhost:5173/`  
菜单权限：`L4` / `MENU_ENT_MAINTENANCE`（`super_admin` / `sys_admin` / `data_maint` / `graph_maint` / `content_ops`）。

### 1.1 全量 15 项 tab id

| 分组 | tab id |
| --- | --- |
| 内容运营（5） | `portal` · `entity` · `entity_dynamics` · `expert_knowledge` · `visualization` |
| 图谱运营（4） | `lifecycle` · `relation_lifecycle` · `entity_attrs` · `graph_draw` |
| 分析配置（6） | `fields_metrics` · `model_rules` · `data_batch` · `report_templates` · `perm_mask` · `audit` |

## 2. H-01～H-08 自评

| # | 检查项 | 自评 | 说明 |
|---|--------|------|------|
| H-01 | 与 wireframe / 全清单结构一致；字段 metric_id / 待核对项关联 | ✅ | 左侧分组导航 15 项齐全（CMS5+图谱4+分析配置6）；可演示 portal/entity/entity_dynamics/lifecycle；本页无统计 KPI，metric_id=N/A；Q-OPS-02 用 PendingBadge |
| H-02 | Design.md §4–§7 色彩/字体/圆角/控件高 | ✅ | 复用现有 Arco + `--sci-*`；主色 `#165DFF`、页底 `#D8E7FC`；未引入新 UI 库 |
| H-03 | 主路径与异常态（空/加载/无权限） | ✅ | 门户/主体/动态 Empty；生命周期无时间线 Empty；非法 tab 回退默认 portal；菜单 L4/`MENU_ENT_MAINTENANCE` 锁态未改 |
| H-04 | 中屏/小屏差异说明 | 🟡 | 沿用现网 flex-wrap / table scroll；专题系统 PC 工作台范围（Design.md §14）；未单独出小屏裁剪稿 |
| H-05 | 首轮基线版本号 + 反馈可追溯 | ✅ | 冻结本版 `HIFI-ENT-OPS-medium-v0.2`；对照能力全清单 v0.2 |
| H-06 | 不涉及大屏蓝色风格 | ✅ | Track-MS 中屏运营工作台 |
| H-07 | Mock/待核对标注位 | ✅ | 可演示区 MockBadge（🧪）；占位页带「占位」Tag + 能力名 + 招标锚点；Q-OPS-02 PendingBadge |
| H-08 | 高颖+孔东首轮基本完成确认 | 🟡 | 自评可演示；正式会签结论待 `human:高颖` + `human:孔东` 登记 |

**首轮结论（执行侧）**：⚠️ 带非阻断反馈可演示（H-04 / H-08 为 🟡）；无阻断 ❌。

## 3. Design.md §14 / D10 对照（摘要）

- 主色 / 页面底 / 控件高沿用项目 sci token 与既有 maintenance 页。
- 左侧分组导航（内容运营 / 图谱运营 / 分析配置）+ 门户内二级职责 Tab 保留。
- 业务态不泄漏 Q 号文案（Q-OPS-02 在 PendingBadge/`ReviewOnly` 内）。
- 分析配置 6 项与图谱运营非 lifecycle 叶子为占位，**未删菜单**；未做 ODS 工商字段可编辑。

## 4. 范围边界

| 做 | 不做 |
| --- | --- |
| 全量 15 项一级菜单 + `?tab=` 同步 | 删减菜单项 / merge 进 lumen |
| portal 可演示 + entity / entity_dynamics / lifecycle 骨架 | 占位项深度交互与联调 |
| 占位页：能力名 + 招标锚点 +「占位」标识 | 覆盖工商主数据编辑 |
| MockBadge / PendingBadge | 接真实后端 |

## 5. 待会签动作

1. `human:高颖` / `human:孔东` 走查 portal / entity / entity_dynamics / lifecycle + 抽查占位项并回填 H-08。  
2. H-04 若需单独小屏说明，由 UX 在门 1 前闭合（专题系统默认 PC）。  
3. Q-OPS-02 继续挂客户决策清单，上线前升 🟢 才可去角标。

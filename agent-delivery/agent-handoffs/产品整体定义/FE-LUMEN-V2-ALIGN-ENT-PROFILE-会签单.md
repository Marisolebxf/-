# FE-LUMEN-V2-ALIGN-ENT-PROFILE 会签单

> 任务：`ENT-MOD-PROFILE-V2-DEMO` · 企业详情（画像）整页 · 监管 `human:曹丽影`  
> 决策依据：`DECIDE-FE-V2-LUMEN-DIRECT` · 派单包 §5.5

## 1. 范围对照

| 项 | 约定 | 实现 |
|---|---|---|
| 页面 | `views/enterprise/EnterpriseDetail.vue` | ✅ |
| 壳 | 复用 S2A `ElementProfile` `mode=page` | ✅ |
| 面包屑 | `ProfileBreadcrumb` + `source` / `sourceSearch` | ✅ |
| Tab | demo `enterpriseProfileTabs` 对齐（含关系图谱 ECharts） | ✅ |
| API | `getEnterpriseDetail` / `getEnterpriseProfile` | ✅ Mock |
| 第二套画像壳 | 禁止 | ✅ 未另起 |

## 2. 入口与上下文

| 入口 | query | 验收 |
|---|---|---|
| S2A Lab「查看详情」 | `source=search&sourceSearch=/enterprise/search-s2a-lab` | ☐ |
| 对比篮点企业名 | `source=compare&sourceSearch=/enterprise/enterprise-compare` | ☐ |
| 直达 `/enterprise/:code` | `source=direct` | ☐ |

## 3. Tab 清单

| Tab | 状态 |
|---|---|
| 工商概况 / 主要团队 / 资质荣誉 / 知识产权 | Mock 可展示 |
| 经营财务（营收趋势折线） | Mock + ECharts |
| 供应链关系 | Mock 表 |
| **关系图谱** | Mock + ECharts force graph |
| 舆情动态 | Mock 列表 |
| 风险信息 | Mock + ⚠️ PendingBadge（Q020） |
| 招投标 | pending 空态 |

## 4. 构建与提交

| 项 | 值 |
|---|---|
| 分支 | `feature/ent-profile-v2` |
| worktree | `worktrees/lumen-ui-topic--ENT-MOD-PROFILE-V2-DEMO` |
| commit SHA | _（合并前回填）_ |
| `npm run type-check` | ✅ 通过（2026-07-16） |
| `npm run build-only` | ✅ 通过（2026-07-16） |

## 5. 会签栏（内部评审）

| 角色 | 签字 | 日期 |
|---|---|---|
| 前端执行 · 曹丽影 | ☐ | |
| 前端 Lead / 孔东 | ☐ | |
| 产品 / UX（对照 demo） | ☐ | |

## 6. 开放项

- S4 正式「企业查询」页替换 Lab 回跳路径 `search-s2a-lab` → `enterprise-search`
- 风险 / 招投标三方源接入后移除 Pending
- 深度分析跳转（demo `buildEnterpriseDeepAnalysisUrl`）待评估页就绪

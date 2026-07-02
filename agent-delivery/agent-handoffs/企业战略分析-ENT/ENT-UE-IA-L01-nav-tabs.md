# ENT-UE-IA-L01 企业中心导航与页面内 Tab 重组 Handoff

## 修改文件清单

- `repos/demo-ui-topic/src/app/components/Layout.tsx`
  - 左侧企业相关导航收敛为一个「企业中心」一级组。
  - 仅暴露四个二级菜单：企业总览、企业全景、企业洞察、企业决策。
- `repos/demo-ui-topic/src/app/routes.tsx`
  - 新增 `/enterprise-center/overview`、`/enterprise-center/panorama`、`/enterprise-center/insight`、`/enterprise-center/decision`。
  - 默认首页重定向到 `/enterprise-center/overview`。
  - 保留旧 `/enterprise/*` 与 `/development/*` 路由。
- `repos/demo-ui-topic/src/app/pages/enterprise/EnterpriseCenterPage.tsx`
  - 新增企业中心聚合页，提供四个模块的页面内一级 Tab 框架。
  - Tab 内容复用既有企业发展与企业分析页面，不做深层业务页重写。
- `repos/demo-ui-topic/scripts/check-enterprise-ia.mjs`
  - 新增静态 IA 契约检查脚本。
- `gkx-orchestration/agent-delivery/agent-handoffs/产品整体定义/UX-UE 通用交互组件规范.md`
  - 补充面包屑通用显示规则：1-2 级路径不显示面包屑，超过 2 级才显示；首节点从业务域根节点开始，不默认使用“首页”。

## 新左侧菜单结构

```text
企业中心
├─ 企业总览      /enterprise-center/overview
├─ 企业全景      /enterprise-center/panorama
├─ 企业洞察      /enterprise-center/insight
└─ 企业决策      /enterprise-center/decision
```

左侧菜单不再暴露：

- 门户-企业发展
- 企业分析
- 企业画像
- 企业检索
- 内容管理
- 旧企业发展/企业分析子页面菜单项

## 页面内一级 Tab 结构

| 左侧菜单 | 页面内一级 Tab | 当前承载 |
|---|---|---|
| 企业总览 | 总览看板 / 结构分布 / 重点名单 / 更新动态 | 复用 `EnterpriseOverview`、`DevelopmentOverview`、`KeyEnterprisesPanorama`；更新动态为前台消费后台维护结果的提示视角 |
| 企业全景 | 企业地图 / 重点企业 / 明星企业 / 深圳企业 / 名单视图 | 复用重点企业、明星企业、深圳企业和检索结果页；企业地图为 L02/L 后续细化预留 |
| 企业洞察 | 类型分布 / 领域分布 / 深圳现状 / 供应链 / 痛难点 | 复用现有五个企业分析页 |
| 企业决策 | 能力评估 / 招引培育 / 竞争力 / 决策建议 | 复用能力评估、引育决策、竞争力页；决策建议为后续汇总视角预留 |

Tab 切换使用页面内 `global-workbench-tabs`，不进入左侧三级菜单；ContextBar 保持显性，Tab 切换不静默清空全局筛选。

面包屑遵循《UX-UE 通用交互组件规范.md》通用规则：企业中心四个二级页面不显示面包屑；进入企业检索等超过 2 级的兼容/深层入口时显示，例如 `企业中心 / 企业全景 / 企业检索`。

## 旧路由保留情况

已保留旧路由，包括但不限于：

- `/development/overview`
- `/development/search`
- `/development/enterprise/:enterpriseCode`
- `/development/key-enterprises`
- `/development/star-enterprises`
- `/development/shenzhen`
- `/enterprise/overview`
- `/enterprise/type-distribution`
- `/enterprise/domain-distribution`
- `/enterprise/status-analysis`
- `/enterprise/supply-chain`
- `/enterprise/pain-points`
- `/enterprise/capability`
- `/enterprise/competitiveness`
- `/enterprise/recommendation`

这些旧路由不再作为左侧菜单项暴露，可继续作为直达、分享、验收材料引用和后续 active 映射对象。

## L02 预留点

- `EnterpriseCenterPage` 中每个 Tab 已记录对应 `legacyRoute`，可作为 L02 旧路由到新菜单 + Tab 的映射表来源。
- 当前旧路由直接访问时仍渲染原页面；完整高亮新菜单和选中对应 Tab 的逻辑留给 `ENT-UE-IA-L02`。
- 企业地图、更新动态、决策建议为框架预留视角，未做业务深层重写。

## 验证命令与结果

```bash
node scripts/check-enterprise-ia.mjs
```

结果：通过，输出 `enterprise IA contract passed`。

```bash
npm run build
```

结果：通过。Vite 构建成功，存在 chunk size 大于 500 kB 的既有打包体积警告。

```bash
npm run design:check
```

结果：旧 `app-user-switch` / `app-user-role-menu` 断言已废弃，已改为检查 `PersonaLevelSwitcher`、`persona-switch`、`persona-menu`、`persona-menu__advanced`、`persona-menu__warning`，以匹配“Persona 主选择 + Level 高级演示调节”的新产品规则。

当前全量 `design:check` 仍未通过，但失败点已变为既有产业链页面契约：`src/app/pages/industry/ChainProfilePage.tsx must use standard tab classes instead of Arco Tabs`。该失败与本次企业中心 IA / 顶部权限视角控件无关，需单独处理产业链页面 Tab 标准化。

```bash
npm install
```

结果：成功安装依赖；`npm audit` 提示 2 个 high severity 漏洞，未在本任务内执行 `npm audit fix --force`。

## 风险与后续建议

- 聚合页当前采用“外层企业中心 Tab + 内层复用旧业务页”的方式，避免重写深层业务，但旧业务页内部仍可能显示旧标题或旧面包屑。L02 可继续做旧路由 active 映射与页面标题口径收敛。
- 顶部权限/视角控件已从旧 `PermLevelSwitcher + PersonaTag` 平级组合收敛为 `PersonaLevelSwitcher`，检查脚本已同步新契约；后续不要恢复旧 `app-user-switch` 结构。
- 企业检索已从左侧菜单移除，但仍通过名单视图/兼容路由承载；完整检索收敛仍归 `ENT-UE-IA-L07`。

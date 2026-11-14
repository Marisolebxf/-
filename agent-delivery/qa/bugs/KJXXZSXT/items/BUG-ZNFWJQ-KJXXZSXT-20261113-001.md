# BUG-ZNFWJQ-KJXXZSXT-20261113-001 · 产业级联多选未按标准 Arco 父子联动

| 项 | 值 |
|----|----|
| 编号 | BUG-ZNFWJQ-KJXXZSXT-20261113-001 |
| 系统 | KJXXZSXT（科技信息展示系统） |
| 模块 | 全局公共组件 / 产业领域级联多选（IndustrySelect） |
| 结论 | 产品缺陷 |
| 登记 | 人工 |
| 状态 | fixed |
| 入口 | 各模块顶部筛选「产业领域」等；典型入口：科技全域态势 `/situation/overview` |
| 环境 | 未说明 |
| 发现日期 | 2026-11-13 |
| 关联用例 | 无 |
| 关联脚本 | 无 |
| 登记人 | 未具名 |

### 预期

产业领域等场景使用标准 Arco Design 级联多选：勾选父级（产业集群）自动勾选其全部子级；勾选部分子级时父级显示半选，子级全部勾选时父级显示全选；子级可正常点击勾选。

### 实际

封装组件 `IndustrySelect` 开启 `check-strictly`，父子选中态解耦：选择一级后下级不会自动勾选，勾选下级后上级不显示已选/半选态，交互与标准 Arco 级联多选不一致。

### 证据

- 试跑目录：无
- 截图：无
- 登记表备注：飞书项目缺陷 work_item_id=7167305998（标题「全局处理： 前端级联多选控件优化」）。修复仓 `lumen-ui-science-pc`：`src/views/situation/global-innovation/components/IndustrySelect.vue` 去掉 `check-strictly`，按标准多选 value 进出；`resolve.selfcheck.mjs` 锚点同步。本地自检：`resolve.selfcheck.mjs`、`pnpm type-check`、`situationFilterBar.test.mjs`、`pnpm build` 绿（改动待孔东本机 commit）。

### 范围

BUG-ZNFWJQ-KJXXZSXT-20261113-001。影响复用 `IndustrySelect` 的展示系统各页（态势、人才、政策等约 20 处）。

### 处理

已改标准 Arco 级联多选（父子联动）。待展示系统前端合入 dev 并部署后飞书缺陷 7167305998 复验关闭。

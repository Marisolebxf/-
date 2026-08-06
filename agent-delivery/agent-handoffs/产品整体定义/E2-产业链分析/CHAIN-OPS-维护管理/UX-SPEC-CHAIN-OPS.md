# UX-SPEC-CHAIN-OPS

> **模块**：CHAIN-OPS · 产业链维护管理  
> **版本**：v0.1 · 2026-08-06  
> **status**：`ready_for_v1`  
> **source_four_pack**：同目录 IA / TRACE / USM / Wireframe v0.1  
> **体验 Owner**：human:高颖  
> **轨道**：Track-MS

## 1. 目标与范围

支撑 L4 运营在 `/industry-center/maintenance` 完成产业全景内容写侧与 15 项菜单可达；V1 高保真以 **A1 门户内容工作流** 为完整样例，其余项菜单+占位。

## 2. 主路径

1. 有权限用户从「产业链分析 → 维护管理」进入，默认 `tab=portal`。  
2. 选择产业与 `block_key`，新建/编辑草稿 → 保存 → 提交审核。  
3. 审核通过 → 待发布 → 发布；门户总览只读 published。  
4. 切换左栏其他 14 项：到达占位页，可返回 portal。

## 3. 状态与反馈

| 状态 | 反馈 |
| --- | --- |
| 无权限 | 全页锁态 + 说明需 L4 维护角色；不露写控件 |
| 保存成功 | Message.success；列表刷新 |
| 审核退回 | 状态 `returned`，编辑区可见退回原因（Demo 可用固定文案） |
| 发布成功 | 状态 `published`；提示前台只读消费 |
| 占位项 | Tag「占位」+ Alert，不假装已联调 |

## 4. 键盘与无障碍

- 左栏导航按钮 `role="tab"` / `aria-selected`。  
- 表格与主按钮可键盘聚焦；弹层 Esc 关闭。  
- 锁态区域 `aria-disabled` / 说明文本可读。

## 5. 组件边界（Arco）

Button / Table / Tabs（或自绘左栏 tablist）/ Form / Input / Select / Tag / Alert / Empty / Message / Modal。视觉 token 遵循 `Design.md`。禁止引入企业维护业务组件 import。

## 6. 评审挂载

| mount_id | kind | refs |
| --- | --- | --- |
| CHAIN-OPS-F00-SHELL | requirement_trace | IC-43 |
| CHAIN-OPS-F01-PORTAL | requirement_trace | IC-43, SPEC-CMS |
| CHAIN-OPS-GAP-ROLE | pending_badge | GAP-CHAIN-OPS-ROLE |

## 7. 验收用例（节选）

1. L4 content_ops 可见菜单并进入 portal 工作台。  
2. L0–L3 进入 maintenance 见锁态或菜单不可见（按 Layout 权限过滤）。  
3. 五块 `block_key` 均可出现在类型筛选。  
4. 草稿→待审→待发→已发布路径可点通（本地 Demo 状态）。  
5. 左栏 15 项齐全且不可因占位而隐藏。

## 8. §19 走查

- [x] 主路径与异常（锁态）  
- [x] 状态反馈  
- [x] 键盘可达（导航+主按钮）  
- [x] Arco 选型边界  
- [x] 与 Design.md 分层（本文件不改视觉 token）  

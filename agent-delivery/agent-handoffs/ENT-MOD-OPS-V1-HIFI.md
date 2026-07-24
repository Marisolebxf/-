# ENT-MOD-OPS-V1-HIFI · 维护管理 V1 高保真全量 15 项菜单

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:ui-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |
| 说明 | 监管人已授权连续执行重跑；本轮不要求 git commit/push；不改 task-registry / USM / TRACE / IA / Wireframe / UX-SPEC |

## 修改内容

- 对齐真源 `企业维护管理-能力全清单.md` v0.2：左侧分组导航 **15 项齐全**（内容运营 5 / 图谱运营 4 / 分析配置 6）。
- `?tab=<id>` 与选中态同步；非法 tab 回退默认 `portal`。
- **可演示深度**：
  - `portal`：编辑 / 审核 / 发布 / 版本工作流（含明星 / 深圳内容类型）
  - `entity`：主体搜索列表 + 运营档案 / ODS 只读 + 主数据纠错 Modal
  - `entity_dynamics`：动态列表（新闻 / 财报 / 诉讼 / 舆情）+ 风险等级 + 深圳专项骨架
  - `lifecycle`：阶段字典 + 企业状态时间线（与成长轨迹内容分离）
- **占位项**（不得删菜单）：`expert_knowledge` / `visualization` / `relation_lifecycle` / `entity_attrs` / `graph_draw` / `fields_metrics` / `model_rules` / `data_batch` / `report_templates` / `perm_mask` / `audit` — 均带能力名 + 招标锚点 +「占位」标识。
- Mock 数据区加 `MockBadge`（🧪）；不接真实后端。
- `enterpriseCenterRouteMap`：维护管理中心壳始终 `maintenance`，15 项 tab 由 MaintenancePage 自管。

## 测试结果

- `npm run build`（demo-ui-topic）✅ exit 0（vite build ~39s）
- 本地预览：`http://localhost:5173/enterprise-center/maintenance?tab=portal`（dev 已在跑）
- 菜单权限：`L4` / `MENU_ENT_MAINTENANCE`

## 产物

- 会签单：`agent-handoffs/产品整体定义/UI-HIFI-ENT-OPS-会签单.md`（`HIFI-ENT-OPS-medium-v0.2`；H-01~H-08）
- 本 handoff

## 遗留风险

- H-04 小屏裁剪规则未单独出稿（🟡；专题系统 PC 工作台默认）
- H-08 正式双签待高颖+孔东
- Q-OPS-02 写侧归属仍待甲方
- 11 项占位页深度交互待后续 PACK/UX

## CI/CD

- 分支：本地工作区（本任务不要求 commit/push）
- commit：N/A
- pipeline / K8s：N/A
- 本地验证：`cd E:/gkx-lumen/repos/demo-ui-topic && npm run build`；开发启动 `npm run dev`

## 涉及文件

- `repos/demo-ui-topic/src/app/pages/enterprise/EnterpriseMaintenancePage.tsx`
- `repos/demo-ui-topic/src/app/pages/enterprise/enterpriseMaintenanceDefinition.ts`
- `repos/demo-ui-topic/src/app/pages/enterprise/enterpriseCenterRouteMap.ts`
- `agent-delivery/agent-handoffs/产品整体定义/UI-HIFI-ENT-OPS-会签单.md`
- `agent-delivery/agent-handoffs/ENT-MOD-OPS-V1-HIFI.md`

## Cost 回填（估算）

| 字段 | 值 |
|------|-----|
| actual_tokens | ~95_000 |
| model_used | cursor-grok-4.5 |
| actual_cost | ~$2.80 |
| cost_warn | green |

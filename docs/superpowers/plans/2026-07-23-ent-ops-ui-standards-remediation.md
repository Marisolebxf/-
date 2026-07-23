# ENT-OPS UI Standards Remediation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将维护管理 Demo 整改为符合 GKX 规范的 Arco 搜索/列表工作台和页面级业务 Frame，并移除真实人员姓名。

**Architecture:** 将静态业务定义与页面渲染拆开：`enterpriseMaintenanceDefinition.ts` 负责类型、元数据、演示行和筛选规则；`EnterpriseMaintenancePage.tsx` 负责受控路由态、Arco 工作台、页面级详情 Frame 和标准反馈。F-OPS-02～06 不再由超宽 Drawer 承载，而是在当前 Shell 内容区切换，并统一通过 `return_context` 返回工作台。

**Tech Stack:** React 18、TypeScript、React Router、Arco Design React、现有 `--sci-*` Token、现有 `TraceInfoIcon`。

---

## File map

- Create: `repos/demo-ui-topic/src/app/pages/enterprise/enterpriseMaintenanceDefinition.ts`
  - ENT-OPS 类型、元数据、演示行、虚构维护人、筛选和状态转换纯函数。
- Modify: `repos/demo-ui-topic/src/app/pages/enterprise/EnterpriseMaintenancePage.tsx`
  - Arco 搜索/列表工作台、页面级 F-OPS-02～06、Form 和评审挂载。
- Preserve: `repos/demo-ui-topic/src/app/pages/enterprise/EnterpriseCenterPage.tsx`
  - 入口已经接到 `EnterpriseMaintenancePage`，除非导出名称变化，否则不再修改。
- Modify: `gkx-orchestration/agent-delivery/agent-handoffs/交付覆盖/ENT-OPS/implementation-coverage.yaml`
  - 记录规范整改后的 `implemented/manual_review` 状态。
- Modify: `gkx-orchestration/agent-delivery/agent-handoffs/交付覆盖/ENT-OPS/validation-report.md`
  - 记录静态审计结果和仍未执行的项目验证。
- Modify: `gkx-orchestration/agent-delivery/agent-handoffs/交付覆盖/ENT-OPS/handoff.md`
  - 更新交接边界。

### Task 1: 拆分 ENT-OPS 业务定义

**Files:**
- Create: `repos/demo-ui-topic/src/app/pages/enterprise/enterpriseMaintenanceDefinition.ts`
- Modify: `repos/demo-ui-topic/src/app/pages/enterprise/EnterpriseMaintenancePage.tsx`

- [ ] **Step 1: 创建集中定义文件**

定义并导出：

```ts
export type WorkspaceView =
  | 'editor_workbench'
  | 'all_content'
  | 'review_center'
  | 'publish_center'
  | 'versions_center';

export type DetailFrame =
  | 'workbench'
  | 'editor'
  | 'review'
  | 'publish'
  | 'versions'
  | 'conflict';

export type ContentRow = {
  id: string;
  title: string;
  enterprise: string;
  enterpriseRef: string;
  type: ContentType;
  status: WorkflowStatus;
  updatedAt: string;
  editor: string;
  version: number;
};
```

同时迁移 `TYPE_META`、`STATUS_META`、`VIEW_META`、`INITIAL_ROWS` 与 `statusMatchesView`。所有 `editor` 值只允许 `内容编辑 A/B/C`，不得包含真实姓名。

- [ ] **Step 2: 提供纯筛选函数**

```ts
export function filterMaintenanceRows(
  rows: ContentRow[],
  filters: {
    view: WorkspaceView;
    type?: ContentType;
    status?: WorkflowStatus;
    keyword: string;
  },
) {
  const normalizedKeyword = filters.keyword.trim().toLowerCase();
  return rows.filter((row) => (
    statusMatchesView(row, filters.view)
    && (!filters.type || row.type === filters.type)
    && (!filters.status || row.status === filters.status)
    && (!normalizedKeyword
      || `${row.title}${row.enterprise}${row.id}`.toLowerCase().includes(normalizedKeyword))
  ));
}
```

- [ ] **Step 3: 页面改用集中定义**

从 `EnterpriseMaintenancePage.tsx` 删除重复类型、常量和筛选函数，改为命名导入。页面本地只保留状态、列描述、Frame 组件和事件处理。

- [ ] **Step 4: 执行源文件整洁检查**

Run:

```bash
git -C repos/demo-ui-topic diff --check -- \
  src/app/pages/enterprise/enterpriseMaintenanceDefinition.ts \
  src/app/pages/enterprise/EnterpriseMaintenancePage.tsx
```

Expected: 无输出，退出码 0。

### Task 2: 将 F-OPS-01 改为 Arco 搜索/列表工作台

**Files:**
- Modify: `repos/demo-ui-topic/src/app/pages/enterprise/EnterpriseMaintenancePage.tsx`

- [ ] **Step 1: 替换工作台导航和搜索**

导入 Arco：

```ts
import {
  Alert,
  Button,
  Descriptions,
  Empty,
  Form,
  Input,
  Message,
  Modal,
  Select,
  Table,
  Tabs,
  Tag,
} from '@arco-design/web-react';
```

使用受控 `Tabs` 表达五个列表 variant：

```tsx
<Tabs
  activeTab={view}
  onChange={(key) => setView(key as WorkspaceView)}
  items={VIEW_META.map((item) => ({
    key: item.id,
    title: item.label,
  }))}
/>
```

关键词控件改为 `Input.Search`，并保留 `Select` 内容类型、流程状态与重置按钮。筛选区使用现有 `sci-arco-select`、`sci-arco-search` 或等价项目类，不新增页面私有控件。

- [ ] **Step 2: 定义 Arco Table columns**

```ts
const columns: TableColumnProps<ContentRow>[] = [
  {
    title: '内容标题',
    dataIndex: 'title',
    width: 300,
    render: (_, row) => (
      <div className="min-w-0">
        <div className="truncate font-medium" title={row.title}>{row.title}</div>
        <div className="mt-1 text-[12px] text-[var(--sci-text-3)]">
          {row.id} · v{row.version}
        </div>
      </div>
    ),
  },
  {
    title: '企业',
    dataIndex: 'enterprise',
    width: 260,
    render: (_, row) => (
      <div className="min-w-0">
        <div className="truncate" title={row.enterprise}>{row.enterprise}</div>
        <div className="mt-1 text-[12px] text-[var(--sci-text-3)]">
          {row.enterpriseRef}
        </div>
      </div>
    ),
  },
  {
    title: '内容类型',
    dataIndex: 'type',
    width: 160,
    render: (_, row) => (
      <Tag color={TYPE_META[row.type].color}>{TYPE_META[row.type].label}</Tag>
    ),
  },
  {
    title: '流程状态',
    dataIndex: 'status',
    width: 120,
    render: (_, row) => (
      <Tag color={STATUS_META[row.status].color}>{STATUS_META[row.status].label}</Tag>
    ),
  },
  { title: '维护人', dataIndex: 'editor', width: 120 },
  { title: '更新时间', dataIndex: 'updatedAt', width: 180 },
  {
    title: '操作',
    width: 120,
    fixed: 'right',
    render: (_, row) => availableAction(row),
  },
];
```

操作列继续使用 Arco `Button` 与 Arco Icon；不创建原生按钮。

- [ ] **Step 3: 渲染 Arco Table 和分页**

```tsx
<Table<ContentRow>
  rowKey="id"
  columns={columns}
  data={filteredRows}
  borderCell={false}
  pagination={{
    pageSize: 10,
    showTotal: true,
    sizeCanChange: true,
    sizeOptions: [10, 20, 50],
  }}
  noDataElement={<Empty description="当前角色与筛选条件下暂无内容" />}
  scroll={{ x: 1120 }}
/>
```

删除全部原生 `<table>`、`<thead>`、`<tbody>`、`<tr>`、`<th>`、`<td>` 和独立 `Pagination`。

- [ ] **Step 4: 静态确认不存在自定义表格**

Run:

```bash
if rg -n '<table|<thead|<tbody|<tr|<th|<td' \
  repos/demo-ui-topic/src/app/pages/enterprise/EnterpriseMaintenancePage.tsx; then
  exit 1
fi
```

Expected: 无输出，退出码 0。

### Task 3: 将 F-OPS-02/F-OPS-06 改为页面级详情 Frame

**Files:**
- Modify: `repos/demo-ui-topic/src/app/pages/enterprise/EnterpriseMaintenancePage.tsx`

- [ ] **Step 1: 建立统一页面态和返回上下文**

```ts
const [frame, setFrame] = useState<DetailFrame>('workbench');
const [returnContext, setReturnContext] = useState({
  routeVariantId: 'editor_workbench' as WorkspaceView,
  type: undefined as ContentType | undefined,
  status: undefined as WorkflowStatus | undefined,
  page: 1,
});

function enterFrame(nextFrame: Exclude<DetailFrame, 'workbench'>, row: ContentRow) {
  setReturnContext({
    routeVariantId: view,
    type: typeFilter,
    status: statusFilter,
    page: 1,
  });
  setActive(row);
  setFrame(nextFrame);
}

function returnToWorkbench() {
  setView(returnContext.routeVariantId);
  setTypeFilter(returnContext.type);
  setStatusFilter(returnContext.status);
  setFrame('workbench');
}
```

- [ ] **Step 2: 将编辑器改为当前内容区页面**

当 `frame === 'editor'` 时，返回一个带 `返回内容工作台` Arco Button 的页面级 Frame。三栏必须保持：

```tsx
<div className="grid grid-cols-24 gap-4">
  <section className="col-span-4 min-w-[184px]">企业主数据</section>
  <section className="col-span-12 min-w-[560px]">门户内容分型表单</section>
  <section className="col-span-8 min-w-[320px]">门户预览</section>
</div>
```

标题宿主继续使用 `ENT-OPS-F02-EDITOR-TITLE`；主数据宿主继续使用 `ENT-OPS-F02-MASTER-DATA-BOUNDARY`。

- [ ] **Step 3: 使用 Arco Form.Item**

```tsx
<Form layout="vertical">
  <Form.Item label="内容标题" required>
    <Input value={draftTitle} onChange={setDraftTitle} />
  </Form.Item>
  <Form.Item label="内容摘要" required>
    <Input.TextArea
      value={draftSummary}
      onChange={setDraftSummary}
      autoSize={{ minRows: 5, maxRows: 8 }}
    />
  </Form.Item>
  <Form.Item label="业务材料引用">
    <Select options={materialOptions} />
  </Form.Item>
</Form>
```

纠错 Modal 内同样使用 `Form.Item`；不得保留任何原生 `<label>`。

- [ ] **Step 4: 保留冲突失败输入**

`frame === 'conflict'` 时渲染当前内容区冲突 Frame，挂载 `ENT-OPS-F06-CONFLICT-TITLE`。服务端版本和本地草稿并排展示；返回编辑态时不得重置 `draftTitle`、`draftSummary` 或 `active`。

### Task 4: 将 F-OPS-03～05 改为页面级治理 Frame

**Files:**
- Modify: `repos/demo-ui-topic/src/app/pages/enterprise/EnterpriseMaintenancePage.tsx`

- [ ] **Step 1: 审核 Frame**

`frame === 'review'` 渲染只读变更摘要、来源材料和门户预览，标题挂载 `ENT-OPS-F03-REVIEW-TITLE`。审核通过更新为 `pending_publish`；退回更新为 `returned`，完成后调用 `returnToWorkbench()`。

- [ ] **Step 2: 发布 Frame**

`frame === 'publish'` 渲染发布范围、当前状态和发布方式。挂载 `ENT-OPS-F04-PUBLISH-RISK`。发布方式使用：

```tsx
<Form.Item label="发布方式">
  <Select
    value={publishMode}
    onChange={(value) => setPublishMode(value as 'now' | 'scheduled')}
    options={[
      { value: 'now', label: '立即发布' },
      { value: 'scheduled', label: '定时发布：2026-07-23 09:00' },
    ]}
  />
</Form.Item>
```

退回草稿继续表达并执行演示原子语义：定时计划存在时同时清空计划并回到 `draft`；失败路径不得单独取消计划。

- [ ] **Step 3: 版本与审计 Frame**

`frame === 'versions'` 渲染不可变版本列表和审计说明，挂载 `ENT-OPS-F05-VERSION-AUDIT-TITLE`。从历史版创建草稿切换到 `editor`，并保留 `source_version_id` 说明；不得覆盖历史版本。

- [ ] **Step 4: 控制页面高度和内容滚动**

详情 Frame 使用当前内容区滚动，不创建 `92vw` Drawer。删除 `Drawer` 导入和所有 `<Drawer>` 节点。标准确认仍可使用宽度受控的 Arco `Modal`。

### Task 5: 规范审计与交付状态回写

**Files:**
- Modify: `gkx-orchestration/agent-delivery/agent-handoffs/交付覆盖/ENT-OPS/implementation-coverage.yaml`
- Modify: `gkx-orchestration/agent-delivery/agent-handoffs/交付覆盖/ENT-OPS/validation-report.md`
- Modify: `gkx-orchestration/agent-delivery/agent-handoffs/交付覆盖/ENT-OPS/handoff.md`

- [ ] **Step 1: 运行复合标签审计**

Run:

```bash
node /Users/ying/.codex/skills/gkx-ui-design-standards/scripts/check-composite-labels.mjs \
  repos/demo-ui-topic/src/app/pages/enterprise/EnterpriseMaintenancePage.tsx
```

Expected: `PASS` 或等价零问题结果，退出码 0。

- [ ] **Step 2: 核对七个 mount**

Run:

```bash
rg -o 'ENT-OPS-F0[1-6]-[A-Z0-9-]+' \
  repos/demo-ui-topic/src/app/pages/enterprise/EnterpriseMaintenancePage.tsx \
  | sort -u
```

Expected: 精确输出设计说明列出的七个 mount id。

- [ ] **Step 3: 核对禁用模式**

Run:

```bash
if rg -n '<table|<label|高颖|王宁|李敏|<Drawer|width="92vw"' \
  repos/demo-ui-topic/src/app/pages/enterprise/EnterpriseMaintenancePage.tsx \
  repos/demo-ui-topic/src/app/pages/enterprise/enterpriseMaintenanceDefinition.ts; then
  exit 1
fi
```

Expected: 无输出，退出码 0。

- [ ] **Step 4: 执行 diff 检查**

Run:

```bash
git -C repos/demo-ui-topic diff --check -- \
  src/app/pages/enterprise/EnterpriseMaintenancePage.tsx \
  src/app/pages/enterprise/enterpriseMaintenanceDefinition.ts \
  src/app/pages/enterprise/EnterpriseCenterPage.tsx
```

Expected: 无输出，退出码 0。

- [ ] **Step 5: 回写交付覆盖**

将三项 coverage 保持为 `implemented/manual_review`，补充：

```yaml
ui_standards_remediation:
  arco_table: implemented
  arco_tabs_and_search: implemented
  page_level_frames: implemented
  composite_label_audit: passed
  real_person_names_in_demo: absent
```

`validation-report.md` 必须明确：本轮按用户既有要求未运行项目测试、生产构建、双模式 DOM、真实指针或截图验证，因此不得登记为 `verified`。

- [ ] **Step 6: 提交范围**

实施完成后仅暂存本计划列出的 ENT-OPS 文件；不得暂存工作区中企业分析或其他模块的既有修改。是否提交和推送等待用户明确指令。

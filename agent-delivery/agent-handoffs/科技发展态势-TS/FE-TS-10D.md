# FE-TS-10D · handoff

- 任务：`FE-TS-10D`（维护技术图谱 · 真画布 + 草稿栈 + 版本/回滚）
- 日期：2026-11-13 · 监管：`human:刘剑锋` · 认领：`agent:frontend-agent`
- 状态：代码完成，三绿通过；**未 commit、未 push**（按要求等所有仓一起看 diff）
- 仓：`repos/lumen-ui-science-pc`（`dev`）

## 一、改动文件

| 文件 | 改动 |
|---|---|
| `src/types/maintainEnt.ts` | `/current` 节点 `layout`、`tech_edges[]`、`GraphNodeImpact` 五字段、三个新 op、`PublishResult`、版本/详情/回滚/预览类型；`results` 可空 |
| `src/api/situation/maintain-ent.ts` | 新增 `loadGraphVersions` / `loadGraphVersionDetail` / `previewGraphRollback` / `rollbackGraphVersion` / `loadGraphNodeImpact`；`submitChangeSet` 支持 `client_batch_id`；`publishChangeSet({changeSetId,label})`；删除 50301；50303 提示；409 拆「取锁超时」与「基线过期」；失败数 `results?.failed ?? 0` |
| `src/mock/modules/maintain-ent.ts` | 有状态 mock 工作集（节点/技术点边/版本/快照/变更日志）；`/current` 动态回读；版本列表/详情/回滚预览/回滚可走通；publish 返回 `node_id_map` 与分组 stats |
| `src/mock/register.ts` | 注册 5 个图谱版本/预检 mock |
| `src/views/situation/maintain/graphMaintainModel.ts`（新增） | 草稿净差 `buildGraphOps`、临时号替换 `applyNodeIdMap`、撤销/重做、本地草稿读写、多标签锁、409 重放、四种历史 stats 兼容、版本/回滚/关系/对象中文映射 |
| `src/views/situation/maintain/components/GraphMaintainEditor.vue` | 重写为 G6 真画布；全部交互、草稿、保存、409、版本面板、回滚、删除确认、只读/多标签/离页确认 |
| `src/views/situation/maintain/index.vue` | 移除写死 4 节点 seed；接入新编辑器；分区切换/路由离开未保存确认 |
| `src/views/situation/maintain/components/MaintainDialog.vue` | `allow-create`（分类为空降级文本）、`allow-clear`（重要性选填） |
| `src/views/situation/maintain/maintainModel.ts` | 移除 real 轨写死 4 节点 seed（mock 轨保留演示） |
| `src/views/situation/maintain/graphMaintain.test.mjs`（新增） | 草稿净差/级联删除/临时号/409 重放/撤销重做/localStorage/多标签锁/四种 stats/版本回滚/时间范围/本地校验/固定坐标断言 |
| `src/types/panorama.ts` | 关系 `origin` / `strengthManual`；结果 `overlay`；实体行关系来源字段 |
| `src/lib/graph/liveGraph.ts` | `coerceLiveGraph` 透传 `overlay`；人工强度优先于 `weight`；存量关系码中文化 |
| `src/views/situation/panorama/index.vue` | overlay 不可用非阻塞提示；学科筛选灰字；实体详情显示关系来源/人工强度 |
| `src/views/situation/panorama/components/KnowledgeGraphCanvas.vue` | 关系悬浮提示：人工/存量、人工强度、存量关系码中文字典；连线标签中文化 |

## 二、功能点映射（ARCH §6）

### 34 增加节点

| 功能点 | 落地 |
|---|---|
| 34-1 右键空白创建 | 画布空白右键「添加节点」，落点为右键世界坐标 |
| 34-2 工具栏按钮 | 工具栏「添加节点」，落点为视口中心 |
| 34-3 弹窗字段 | 名称必填、技术分类必填（下拉取现有分类，空时可手填）、描述、重要性（高/中/低，可清空）；按钮「确定」 |
| 34-4 指定位置 | `layout{x,y}` 入草稿并随 `add_node` 提交；有 layout 的节点渲染时固定 `x/y + fx/fy`，刷新/重渲染坐标不变；无坐标节点走确定性自动布局 |
| 34-5 唯一标识符 | 草稿/详情显示「待保存」，保存后 `node_id_map` 替换并回读显示正式编号 |

### 35 删除节点

| 功能点 | 落地 |
|---|---|
| 35-1 单击/框选 | G6 单击多选、Shift 追加、框选模式；选中态高亮 |
| 35-2 右键/Delete | 右键「删除节点」+ Delete/Backspace；输入框/弹窗内不拦截 |
| 35-3 确认框提示关系 | 删除前调 impact，显示技术点关系/实体关系/实体挂接/全景隐藏存量关系四项；null 显示「无法统计」；草稿节点不调服务端并说明 |
| 35-4 节点与关系移除 | 草稿即时移除，级联移除两端技术点边；提交 `delete_node{cascade:true}` |

### 36 增加关系

| 功能点 | 落地 |
|---|---|
| 36-1 Ctrl 选两点 | Ctrl/Shift 点选两个节点 |
| 36-2 右键「添加关系」 | 恰好两点（含右键点）时菜单出现；先选为起点、后选为终点 |
| 36-3 类型/强度/时间 | 类型固定「包含/依赖/促进」；强度 0–10；起止年可空；不取全景 relationTypeOptions |
| 36-4 显示连线 | 草稿即时画有向箭头 + 类型/强度/人工标签；重复同型由后端 422 返回 |

### 37 删除关系

| 功能点 | 落地 |
|---|---|
| 37-1 点击高亮 | 连线点击选中高亮 |
| 37-2 右键/Delete | 右键「删除关系」+ Delete/Backspace |
| 37-3 确认后移除 | 确认框「删除该关系？两端节点保留」；确认后连线消失、两端保留 |

### 38 编辑节点

| 功能点 | 落地 |
|---|---|
| 38-1 双击/右键 | 双击节点 + 右键「编辑属性」 |
| 38-2 四字段 | 名称/分类/描述/重要性，与 34-3 共用弹窗 |
| 38-3 点保存更新 | 「确定」后画布即时回显，提示「已加入待保存改动」；不出现「已保存」 |

### 39 草稿与撤销

| 功能点 | 落地 |
|---|---|
| 39-1 自动记录修改 | 工具栏常驻「未保存改动 N 项（本批上限 50）」；N 为净差 op 条数；点击计数弹出逐条中文摘要（新增/删除/修改技术点、新增/删除关系），不做单条撤销 |
| 39-2 撤销/重做按钮 | 两按钮带禁用态；只动本地草稿栈 |
| 39-3 Ctrl+Z / Ctrl+Y | 画布获焦时生效；弹窗、输入框、可编辑元素内不拦截；兼容 Cmd |
| 39-4 可追溯 | 按用户+基线版本存 localStorage；重进提示恢复；离页 beforeunload + 路由/分区切换确认；保存后清空草稿 |

### 40 保存与版本

| 功能点 | 落地 |
|---|---|
| 40-1 保存 | 「保存图谱」→ `/current` 预检 → `changes` → `publish` → `node_id_map` 替换 → 清草稿 → 回读 current + versions；失败保留草稿 |
| 40-2 创建新版本 | 保存弹窗版本说明；成功后版本列表新增一行 |
| 40-3 回滚 | 预览确认框：目标说明/时间/操作人；「移除/恢复/还原」三项计数 + 分组明细 + 「生成新版本可再回滚」；快照超限显示不可再回滚；确认后重新回读 |
| 40-4 修改记录与操作人 | 版本表（说明/类型/操作人/时间/统计/可回滚）；详情抽屉逐条中文 before/after；兼容四种历史 stats |

### 横切

| 功能点 | 落地 |
|---|---|
| real 轨不显示写死种子 | `maintainModel.ts` 移除 4 节点 seed；real 轨只读 `/current`，空态；mock 轨保留演示 |
| 未登录只读 | 沿用整页 `maintainReadonly`，编辑器只读 + 顶部提示 |

## 三、全景页（补充要求）

1. `overlay.status === 'unavailable'`：图谱区上方非阻塞提示「人工维护的改动暂未显示，请稍后刷新」，其余照常显示。
2. 选择学科筛选（`selectedFieldValues.length > 0`）时显示灰字「维护中新建的技术点不参与学科筛选」。
3. 人工关系（`origin === 'manual'`）：连线悬浮提示和实体详情标「人工」；有 `strengthManual` 时显示人工强度，不回落 `weight`。
4. 存量关系码只读中文字典：`KNOWLEDGE_DEPENDENCY`→知识依赖、`PATENT_CONVERGENCE`→专利趋同、`CO_EVOLUTION`→协同演进、`WEAK_DEPENDENCY`→弱依赖，未知大写码→其他关系；悬浮提示标「存量」。
5. `coerceLiveGraph` 保留 `overlay`，避免真实轨重建对象时丢字段；未改原有字段用法。

## 四、三绿

- `pnpm type-check`：通过
- maintain 单测：`maintain.test.mjs` / `maintainEnt.test.mjs` / `maintainSource.test.mjs` / `graphMaintain.test.mjs` 全部 ok
- `pnpm build`：通过（1m13s；仅既有 chunk 体积/unocss 警告）

## 五、未落地 / 折扣项

1. **关系属性编辑**按 ARCH §1-1 明确不做，未保留入口。
2. **节点拖拽**按 ARCH §1-1 禁用，未注册 `drag-node`；仅新建节点记录落点。
3. 未做浏览器端真实网关联调：real 轨依赖 GRAPH 后端发布/版本端点上线；本次以类型、单测、mock 有状态模型和 build 验证。

## 六、契约问题 / 收口

1. 50301 已按 GRAPH-API §7 退役删除；新增 50303（下游不可达），文案「服务暂不可用，请稍后重试」。
2. 409 已区分：取锁超时/死锁「他人正在保存，请稍后重试」；基线过期才提示新版本并进入重放弹窗。
3. `publish.results` 历史可能为 `null`，失败数统一 `results?.failed ?? 0`；成功提示对 null 显示「该版本未记录逐条结果」。
4. 历史四种 `stats` 形状均兼容，不假设固定嵌套。
5. `client_batch_id` 按 A7 可选：编辑器不强制携带；409 重放不依赖它。
6. 需规简报称“26 个功能点 + 2 条横切”，ARCH 文档标题处写“27 个功能点”，存在 1 项计数口径差异，实现以 §6 表逐行为准。
7. `overlay` 目前按 `{status}` 增量消费，未知字段透传；若后续读图契约扩展 `overlay` 子字段，前端无需改类型。
8. `strengthManual` 与 `weight` 量纲可能不同（人工 0–10、存量 0–1）；展示层已分开，未做跨量纲归一。

## 七、cost

- actual_tokens：跨两次会话累计，粗估 ~160k
- model_used：Claude Code agent（frontend-agent）
- actual_cost：无法从本地精确读取
- cost_warn：green

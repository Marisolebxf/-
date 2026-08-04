# Wireframe-ZHIKU-TECH-SYSTEM｜技术体系分析 · 线框与字段表

> **版本**：v1.0-rework-r4（与 USM/IA/UX-SPEC/TRACE 同步）

## F-TS-01 技术体系管理（tab=system 上半区）

```
┌ 工具条：搜索框 | [新建体系] | 统计卡 ⓘZHIKU-TS-SYSTEM-TOTAL 🧪 ┐
│ 体系卡片×N：名称 / 更新时间 / 节点数 / [在线编辑] [删除]      │
└ 新建弹窗：名称(必填) + 模板(空白/三层示例)                     ┘
```

| 区块 | 字段 | 控件 | 数据源 | 交互 | 序号 |
| --- | --- | --- | --- | --- | --- |
| 工具条 | keyword | a-input-search | store.filters | 实时过滤，持久化 | 8 |
| 工具条 | 新建体系 | a-button + a-modal | store.createSystem | 校验空/重名；入库置顶持久化 | 8 |
| 卡片 | 在线编辑/删除 | a-button / a-popconfirm | store | 编辑 → F-TS-02（?system=）；删除确认含专家意见提示 | 8 |

## F-TS-02 在线编辑器（tab=system 下半区，?system=）

```
┌ 体系选择器 | 更新时间 ─────────────────────────────┐
│ 左：a-tree（展开态持久化，选中节点高亮）           │
│ 右：属性面板 名称 / TRL(1-9) / 重要性(1-5)         │
│     [添加子节点] [删除节点(级联确认)]              │
└────────────────────────────────────────────────────┘
```

| 区块 | 字段 | 控件 | 数据源 | 交互 | 序号 |
| --- | --- | --- | --- | --- | --- |
| 树 | tree/expandedKeys | a-tree | system.tree | 展开/选中持久化；URL ?system= 同步 | 9 |
| 属性 | title/maturity/importance | a-input + a-slider ×2 | node | 即时保存；更新时间回写 | 9 |
| 操作 | 增/删节点 | a-button + Modal.confirm | store | 删除提示级联子节点数 | 9 |

## F-TS-03 专家交互（tab=expert）

```
┌ 体系选择 | 分支筛选 | 待确认计数 Badge ┐
│ 意见卡×N：专家/分支Tag/内容/时间/状态  │
│   讨论串（回复列表）+ 回复框 + [确认]  │
└ Empty：该体系暂无专家意见              ┘
```

| 区块 | 字段 | 控件 | 数据源 | 交互 | 序号 |
| --- | --- | --- | --- | --- | --- |
| 筛选 | systemId/branch | a-select ×2 | opinions | 双维过滤 | 10 |
| 意见卡 | replies/confirmed | a-comment + a-button | store | 回复追加持久化；确认幂等 | 10 |

## F-TS-04 论文分析（tab=paper）

```
┌ 统计卡 ⓘZHIKU-TS-PAPER-TOTAL 🧪 ┐
│ 总览：词云 | 热度排行 | 增长趋势折线                     │
│ 交叉：领域×地区矩阵（高/中/低 颜色编码）→ 单元格样本弹层 │
│ 任务：表格(状态/进度) [新建] [合并(勾选≥2)] [重新解析]   │
└──────────────────────────────────────────────────────────┘
```

| 区块 | 字段 | 控件 | 数据源 | 交互 | 序号 |
| --- | --- | --- | --- | --- | --- |
| 总览 | wordcloud/rank/trend | VChart + a-table | PAPER_* | — | 11 |
| 交叉 | cells | CrossHeat 矩阵 | PAPER_CROSS_* | 单元格点击 → 样本明细弹层 🧪 | 12 |
| 任务 | tasks | a-table + a-progress | store | 新建/合并/重新解析；进度模拟推进持久化 | 13、14 |

## F-TS-05 专利分析（tab=patent）

```
┌ 总览：词云 | 热点排行 | 国别布局条形 | IPC 饼图 ┐
│ 任务：表格 [暂停/恢复] [删除]                   │
│ 案例库：案例卡×3 → 详情抽屉                     │
│ 深度分析：维度切换 | 矩阵 | [导出CSV] [生成专利分析报告] │
└ 算法层能力说明卡 🧪（序号 19/20 目标态描述）    ┘
```

| 区块 | 字段 | 控件 | 数据源 | 交互 | 序号 |
| --- | --- | --- | --- | --- | --- |
| 总览 | 四视图 | VChart ×3 + a-table | PATENT_* | — | 15 |
| 任务 | status | a-table + a-switch | store | 启停/删除持久化 | 16 |
| 案例 | case | a-card + a-drawer | PATENT_CASES | 详情抽屉 | 17 |
| 深度 | 矩阵/导出/报告 | CrossHeat + a-button | PATENT_CROSS_* | CSV 真实下载；报告 → CT-TS-01 | 18 |
| 说明 | 能力卡 | a-alert | 静态 | 🧪 目标态标注 | 19、20 |

## F-TS-06 科研项目分析（tab=project）

```
┌ 统计卡 ⓘZHIKU-TS-PROJECT-TOTAL 🧪 | 检索条(关键词/领域/年份/状态) ┐
│ 项目表格 | 仪表盘：经费柱图 + 活跃度折线 + 地域分布                │
│ 任务：表格(状态/进度/优先级) [新建] [合并]                        │
└───────────────────────────────────────────────────────────────────┘
```

| 区块 | 字段 | 控件 | 数据源 | 交互 | 序号 |
| --- | --- | --- | --- | --- | --- |
| 检索 | keyword/field/year/status | 组合控件 | store.filters | 持久化；Empty→清空 | 21 |
| 仪表盘 | 三视图 | VChart | PROJECT_* | 随领域筛选联动 | 22 |
| 任务 | tasks | a-table | store | 新建/合并持久化 | 23 |

## F-TS-07 社会网络分析（tab=network）

```
┌ 统计卡 ⓘZHIKU-TS-NETWORK-NODE-TOTAL 🧪 ┐
│ 网络图（节点点击选中）↔ 结果分析（指标卡/关键节点表/社区列表） │
│ 任务表格 | 数据上传：模板选择(4类) + 上传区 → [生成分析任务]    │
│ 维护表格：增/删/改 | [重新分析] [导出CSV]                       │
└─────────────────────────────────────────────────────────────────┘
```

| 区块 | 字段 | 控件 | 数据源 | 交互 | 序号 |
| --- | --- | --- | --- | --- | --- |
| 可视化 | graph | NetworkGraph 组件 | nodes/edges | 图↔列表双向选中，选中持久化 | 24 |
| 结果 | stats/keyNodes | MetricCard + a-table | 派生重算 | 随维护变更重算 | 25 |
| 任务 | tasks | a-table | store | 上传生成任务推进 | 26 |
| 上传 | template/upload | a-select + a-upload | UPLOAD_TEMPLATES | 未选模板禁用生成 🧪 | 27 |
| 维护 | nodes CRUD | a-table + Modal | store | 增删改联动图/统计；导出 CSV | 28 |

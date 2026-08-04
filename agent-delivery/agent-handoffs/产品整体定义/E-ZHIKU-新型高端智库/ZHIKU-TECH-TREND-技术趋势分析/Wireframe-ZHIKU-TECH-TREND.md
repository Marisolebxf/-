# Wireframe-ZHIKU-TECH-TREND｜技术趋势分析 · 线框与字段表

> **版本**：v1.0-rework-r4（与 USM/IA/UX-SPEC/TRACE 同步）

## F-TT-01 聚类分析（tab=cluster）

```
┌ 任务区：表格(名称/算法/状态) [新建任务] [重跑失败] [删除] ┐
│ 统计卡 ⓘZHIKU-TT-CLUSTER-TOTAL 🧪                          │
│ 结果区：散点图(按簇着色) ↔ 簇卡×4（选中联动）              │
│ 三级筛选：初级/中级/终级 滑杆 + 权重和校验 + [重新计算]    │
│ 清单定制：主题项(可重命名) [导出CSV] [重新计算恢复默认]    │
└────────────────────────────────────────────────────────────┘
```

| 区块 | 字段 | 控件 | 数据源 | 交互 | 序号 |
| --- | --- | --- | --- | --- | --- |
| 任务 | tasks | a-table + a-modal | store | 新建入列模拟推进；重跑/删除持久化 | 29 |
| 结果 | points/summaries | VChart scatter + a-card | CLUSTER_* | 簇卡↔散点双向选中，选中持久化 | 30 |
| 筛选 | weights ×3 | a-slider | store.weights | 和=100 才可重算；重算刷新簇排序 🧪 | 31 |
| 清单 | customList | a-list 可编辑 | store | 重命名/导出/恢复持久化 | 32 |

## F-TT-02 共性网络（tab=network）

```
┌ 任务区：表格 [新建分析任务] ┐
│ 关系矩阵：术语×术语 → 单元格明细弹层(共现/相似度/强度)  │
│ 聚类规则：规则卡(启停开关/阈值滑杆) [新建规则]           │
│ 语义网络：主题卡×N(置信度/中心性/文献量/关键词/作者)     │
│ 高产作者：作者卡×4 → [学术档案] 跳人才库（CT-TT-01）     │
└──────────────────────────────────────────────────────────┘
```

| 区块 | 字段 | 控件 | 数据源 | 交互 | 序号 |
| --- | --- | --- | --- | --- | --- |
| 任务 | tasks | a-table + a-modal | store | 新建入列推进持久化 | 33 |
| 矩阵 | cells | CrossHeat | RELATION_MATRIX_* | 单元格三值明细弹层 🧪 | 34 |
| 规则 | rules | a-switch + a-slider + modal | store.rules | 启停联动语义区过滤；新建校验 0-100 | 35 |
| 语义 | topics | a-card | SEMANTIC_* + 规则过滤 | 全停用 Empty 提示 | 36 |
| 作者 | authors | a-card + a-button | PROLIFIC_AUTHORS | 跳 `/talent/profile`；未收录提示 | 37 |

## F-TT-03 热点与关联（tab=hotspot）

```
┌ 统计卡 ⓘZHIKU-TT-HOTSPOT-TOTAL 🧪 | 搜索框 ┐
│ 热点区：词云 + 排名表(频次/增长率) → 详情抽屉(走势+相关实体) │
│ 交叉区：关联矩阵 ↔ 网络图（选中联动）单元格明细(强度/增长/论文) │
│ 合作区：合作网络图 ↔ 详情列表(强度/领域/时长/评分)              │
│ 趋势区：多技术勾选折线（实线历史+虚线预测⚠）+ 对比表格          │
│         预测统计位：红问号 ZHIKU-TT-TREND-FORECAST（D1 missing） │
└──────────────────────────────────────────────────────────────────┘
```

| 区块 | 字段 | 控件 | 数据源 | 交互 | 序号 |
| --- | --- | --- | --- | --- | --- |
| 热点 | words/rank | VChart wordcloud + a-table | HOTSPOT_* | 搜索持久化；行点击详情抽屉 | 38 |
| 交叉 | cells/graph | CrossHeat + NetworkGraph | CROSS_RELATION_* | 单元格↔图联动，三值明细 | 39 |
| 合作 | graph/list | NetworkGraph + a-table | COOPERATION_* | 图↔列表双向定位 | 40 |
| 趋势 | series 勾选 | a-checkbox-group + VChart | DEVELOPMENT_TREND | 勾选持久化；预测 D1 红问号 + ⚠ 行内标注 | 41 |

## F-TT-04 动态预警（tab=alert）

```
┌ 统计卡 ⓘZHIKU-TT-ALERT-PENDING 🧪 ┐
│ 预警列表(级别着色) → 详情抽屉(影响评估+关联技术+[生成预警研判报告]) │
│   [标记已处理] → 已处理分组(折叠)                                    │
│ 跟踪双栏：左 技术动态(跟踪对象切换) | 右 专家动态                    │
│ 订阅规则：规则卡(关键词/频率/渠道/启停) [新建][编辑][删除] + 命中预览 │
│ 趋势检测：目标+周期选择 [运行检测] → 结果卡(趋势序列+三类建议)        │
└──────────────────────────────────────────────────────────────────────┘
```

| 区块 | 字段 | 控件 | 数据源 | 交互 | 序号 |
| --- | --- | --- | --- | --- | --- |
| 预警 | alerts | a-table/a-list + a-drawer | store.alerts | 处理态持久化联动统计卡；抽屉含报告出口（CT-TT-02） | 42 |
| 跟踪 | trackObjects/events | a-radio + a-timeline ×2 | TRACK_* | 对象切换刷新事件流，选择持久化 | 43 |
| 订阅 | rules | a-card + a-switch + modal | store.subscriptions | CRUD+启停+重复拦截+命中预览 🧪 | 44 |
| 检测 | tasks/results | a-select + a-button + VChart | store.detections | 未选目标禁用；结果三类建议分组 🧪 | 45 |

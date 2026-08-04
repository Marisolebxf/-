# Wireframe-ZHIKU-RESEARCH-NEED｜研究需求分析 · 线框与字段表

> **版本**：v1.0-rework-r4（与 USM/IA/UX-SPEC/TRACE 同步）

## F-RN-01 科技实体清单（tab=entity）

```
┌ 筛选条：搜索框 | 领域多选 | 地区多选 | 类型多选 | 卡片/列表切换 | [批量导入] [清空筛选] ┐
│ 统计卡：筛选命中实体数 ⓘZHIKU-RN-ENTITY-TOTAL 🧪                                     │
│ 卡片流（或表格）：名称 / 领域Tag / 类型Tag / 地区 / 热度 / [导入🧪标记]              │
│ Empty：无匹配 → "清空筛选"                                                          │
└ 导入弹窗：上传区（演示）+ 确认 → 校验摘要（成功 N / 跳过重复 M）                     ┘
```

| 区块 | 字段 | 控件 | 数据源 | 交互 | 序号 |
| --- | --- | --- | --- | --- | --- |
| 筛选条 | keyword | a-input-search | store.filters | 模糊匹配名称，实时过滤，持久化 | 1、3 |
| 筛选条 | field/region/type | a-select multiple ×3 | 常量表 | 叠加过滤，持久化 | 1、3 |
| 筛选条 | viewMode | a-radio-group | store.ui | 卡片/列表切换，持久化 | 1 |
| 筛选条 | 批量导入 | a-button + a-modal | 候选池 | 🧪 校验摘要；新实体置顶入库持久化 | 1、3 |
| 统计卡 | 命中实体数 | MetricCard | filteredEntities.length | ⓘ 8 件套 + 就绪度 | 1 |
| 卡片流 | 实体卡 | a-card / a-table | filteredEntities | 点击 → F-RN-02 抽屉（?entity=） | 2 |

## F-RN-02 实体画像抽屉（?entity=）

```
┌ 抽屉：实体名 + 领域/类型/地区 Tag ─────────────┐
│ 基础信息描述列表（热度/类型/地区）             │
│ 近 6 期热度趋势折线（VChart）                  │
│ 相似实体推荐 🧪（同领域规则）→ 点击切换详情    │
└ 关闭 → URL 清参                                ┘
```

| 区块 | 字段 | 控件 | 数据源 | 交互 | 序号 |
| --- | --- | --- | --- | --- | --- |
| 头部 | name/tags | a-descriptions | entityById | URL `?entity=` 可分享恢复；非法 id 提示回落 | 2 |
| 趋势 | heatTrend | VChart line | 派生序列 | — | 3 |
| 推荐 | similar[] | a-list | 同领域过滤 | 点击切换详情；🧪 标注 | 3 |

## F-RN-03 颠覆性技术 / 前沿技术（tab=frontier）

```
┌ 颠覆性技术识别（卡片×3）：名称/核心指标/TRL/热度/参与方/场景 + [前沿详情] ┐
│ 前沿技术清单：搜索框 | 重点关注区（星标集合）                             │
│ 清单行：名称/描述/★关注 → 详情抽屉（热度趋势图）                          │
└ Empty：筛选无结果 → "清空筛选"；关注区空 → 引导文案                        ┘
```

| 区块 | 字段 | 控件 | 数据源 | 交互 | 序号 |
| --- | --- | --- | --- | --- | --- |
| 颠覆卡 | 六要素 | a-card | DISRUPTIVE_TECHS | [前沿详情] → 打开对应前沿抽屉 | 4 |
| 前沿清单 | keyword/follow | a-input-search + 星标 | FRONTIER_TECHS + follows | 关注集持久化；🧪 自动挖掘标注 | 5 |
| 前沿详情 | heatTrend | 抽屉 + VChart | frontier.heatTrend | 可视化分析图表 | 5 |

## F-RN-04 技术趋势卡片（tab=trend）

```
┌ 统计卡：趋势技术总数 ⓘZHIKU-RN-TREND-TECH-TOTAL 🧪 | 标签云（可点选过滤） ┐
│ 趋势卡片流：技术名 / 标签 Tag / 摘要                                       │
└ 卡片点击 → 摘要抽屉（含 [去技术趋势分析深挖] 跨叶子链接）                  ┘
```

| 区块 | 字段 | 控件 | 数据源 | 交互 | 序号 |
| --- | --- | --- | --- | --- | --- |
| 标签过滤 | activeTag | a-tag checkable | TREND_CARDS tags | 点选过滤持久化；Empty→清空标签 | 6 |
| 卡片流 | techName/tags/summary | a-card | TREND_CARDS | 点击 → 摘要抽屉 | 6 |
| 抽屉 | 深挖入口 | a-link | — | 跳 `/strategy/tech-trend?tab=hotspot`（CT-RN-02） | 6 |

## F-RN-05 媒体聚焦（tab=media）

```
┌ 统计卡：待处理预警数 ⓘZHIKU-RN-MEDIA-WARNING-PENDING 🧪 | 层次分布条形图 ┐
│ 层次过滤：国际/国家/省市/城市/机构/学科（radio）                          │
│ 舆情列表：标题/层次Tag/情感/关联实体(链接)/预警标记 + [标记已处理]        │
│ 已处理分组（折叠）                                                        │
└ [生成舆情研判报告] → 确认 → 写作预填任务（CT-RN-01）                      ┘
```

| 区块 | 字段 | 控件 | 数据源 | 交互 | 序号 |
| --- | --- | --- | --- | --- | --- |
| 层次过滤 | level | a-radio-group | store.ui | 过滤+分布图联动；Empty→查看全部 | 7 |
| 分布图 | 层次计数 | VChart bar | 派生 | 与过滤联动高亮 | 7 |
| 列表 | 预警处理 | a-button | handledIds | 处理态持久化，统计卡联动 | 7 |
| 列表 | 关联实体 | a-link | entity 回链 | 打开 F-RN-02 抽屉；未收录提示 | 7 |
| 底部 | 生成报告 | a-button primary | writing.createTask | 预填大纲+跳转（CT-RN-01）；🧪 图谱联动标注 | 7 |

# IA-ZHIKU-TALENT-POOL｜科技人才库 信息架构

> **版本**：v1.0-rework-r3（与 USM/Wireframe/UX-SPEC/TRACE 同步）
> **真源**：需求拆解 §三 序号 59-74、80-81；USM-ZHIKU-TALENT-POOL.md

## 1. 模块目标与边界

- **目标**：分类/检索定位 → 四维画像研判 → 收藏与专属池沉淀 → 动态资讯与推送跟踪的人才服务闭环。
- **包含**：人才画像（59-62）、领域分类（63-66）、TOP100 与专属池（67-70）、列表筛选与清单（71-74）、动态资讯（80）、信息推送（81）。
- **不包含**：地图分布/人才指数/驾驶舱/人才库订阅（75-79，归 ZHIKU-TALENT-MAP）；报告写作本体（归 ZHIKU-WRITING，仅提供跨叶子出口）；后台数据管理。

## 2. 对象与稳定标识

| 对象 | 标识 | 生命周期 | 说明 |
| --- | --- | --- | --- |
| 学者 Scholar | `sch-*` | 静态种子，只读 | 画像四维数据的挂载主体 |
| TOP100 条目 | `top-*` | 静态种子，只读 | 榜单行，可勾选入池 |
| 列表人才条目 | `list-*` | 静态种子，只读 | 列表筛选结果行 |
| 专属人才池 Pool | `pool-*` | 用户创建/维护，持久化 | 名称 + 成员 id 集合 + 创建时间 |
| 收藏条目 Favorite | scholar/top/list id 复用 | 用户维护，持久化 | 跨页统一集合（含来源类型） |
| 资讯 News | `news-*` | 静态种子，只读 | 可关联 scholar |
| 推送 Push | `push-*`（种子）/ `push-gen-*`（偏好生成） | 种子只读 + 用户偏好追加，持久化 | 已读状态持久化 |
| 偏好 Preference | 学者名/方向/关键词字符串 | 用户维护，持久化 | 驱动专属推送生成 |
| 推荐条目 Recommendation | `rec-*` | 静态种子 + 已阅状态持久化 | 新兴方向/潜力人才 🧪 |

## 3. IA 结构（导航与页面）

```
人才服务（左侧手风琴一级：talent）
├── 人才画像 /talent/profile          F-TP-01（URL: ?scholar=&tab=basic|relation|behavior|psych）
├── 人才库   /talent/pool             （URL: ?tab=domain|top100|list）
│   ├── 领域分类 Tab                  F-TP-02
│   ├── TOP100 榜单 Tab               F-TP-03
│   └── 列表筛选 Tab                  F-TP-04
│   └── 头部「我的收藏」抽屉          F-TP-06 支撑区（跨 Frame）
└── 人才动态 /talent/news             （URL: ?tab=news|push）
    ├── 人才动态 Tab                  F-TP-05
    └── 人才信息推送 Tab              F-TP-06
```

## 4. Frame 职责

| Frame | 页面/区域 | 职责 | 序号 |
| --- | --- | --- | --- |
| F-TP-01 | 人才画像页 | 四维画像（基础/关联/行为/心理）、学者搜索切换、收藏、URL 上下文 | 59-62 |
| F-TP-02 | 人才库·领域分类 | 九大类树 + 分布联动 + 知识图谱 + 智能推荐 🧪 + 导出 | 63-66 |
| F-TP-03 | 人才库·TOP100 | 条件筛选 + 勾选保存池 + 池管理（重命名/更新/共享/导出/删除）+ 报告出口 | 67-70 |
| F-TP-04 | 人才库·列表筛选 | 组合检索 + 列表/卡片双视图 + 统计可视化 + 清单导出 | 71-74 |
| F-TP-05 | 人才动态·资讯 | 类别/关键词过滤 + 学者回链 + 关键词订阅入口 | 80 |
| F-TP-06 | 人才动态·推送（含收藏抽屉） | 偏好管理 + 双组推送流 + 已读管理；收藏抽屉为跨页支撑 | 81 |

## 5. 数据与服务边界

- 全部数据来自 `src/mock/` 领域 store（Pinia），静态种子 + 用户态持久化（localStorage `zhiku-tp-` 前缀）。
- 目标态映射：前端 → Java REST（gkxlumen-topic 聚合层）→ ADS 人才主题表；画像/图谱/推荐算法归 Python `/internal/*`（正式版）。demo 不连任何后端。
- 跨叶子消费：`useWritingTaskStore.createTask`（ZHIKU-WRITING，池分析报告预填）；`useTalentMapStore` 订阅规则新增时经 `useTalentNewsStore` 追加推送条目（TM-05 → TP-08 联动，契约见 TRACE）。

## 6. 指标登记（8 件套均在 metricSeed，就绪度在 readinessSeed）

| metric_id | 挂载点 | 就绪度要点 |
| --- | --- | --- |
| `ZHIKU-TP-INFLUENCE-SCORE` | F-TP-01 关联信息·贡献度卡 | D1 draft（演示态公式声明）/ D4 mock |
| `ZHIKU-TP-GROWTH-INDEX` | F-TP-01 行为信息·成长指数卡 | D1 draft / D4 mock |
| `ZHIKU-TP-DOMAIN-NODE-TOTAL` | F-TP-02 节点总数卡 | D1 draft / D4 mock |
| `ZHIKU-TP-TOP100-TOTAL` | F-TP-03 收录数卡 | D1 draft / D4 mock（修复 S4 未登记错挂） |
| `ZHIKU-TP-POOL-TOTAL` | F-TP-03 我的人才池数卡 | 新增，D1 draft / D4 mock |
| `ZHIKU-TP-LIST-TOTAL` | F-TP-04 命中总数卡 | 新增，D1 draft / D4 mock |
| `ZHIKU-TP-PUSH-UNREAD` | F-TP-06 未读推送卡 | D1 draft / D4 mock（修复 S4 未登记错挂） |

## 7. 跨模块契约

| 契约 | 方向 | 载体 |
| --- | --- | --- |
| 人才池分析报告 | TP → WRITING | `createTask({type:'research', outline 预填池摘要})` + 路由 `/writing/create?step=outline&task=` |
| 订阅规则推送联动 | TM → TP | `useTalentNewsStore.appendGeneratedPush(rule)`（TM-05 新增规则时调用） |
| 画像回链 | TM-03 / TP-02/03/04/05 → TP-01 | 路由 `/talent/profile?scholar=<id>` |

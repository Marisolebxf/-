# UX-SPEC-ZHIKU-TALENT-MAP｜科技人才地图 交互规范

> **版本**：v1.0-rework-r3；交互底座依《UX-UE 通用交互组件规范》（D10），视觉 token 依 Design.md（地图工作区 §8）。

## 1. 用户旅程与任务流

| 旅程 | 入口 | 主任务流 | 出口 |
| --- | --- | --- | --- |
| 分布研判 | 人才地图 Tab | 类别/热力筛选 → 点位↔列表联动 → 流动趋势 | 生成分析报告（→WRITING） |
| 指数对比 | 人才指数 Tab | 权重定制 → 区域对比 → 明细核对 | 研判结论（演示态声明约束） |
| 精准检索 | 人才检索 Tab | 模式选择 → 检索/复搜 → 推荐扩展 | 画像下钻（→POOL） |
| 全景研判 | 驾驶舱 Tab | 卡片定制 → 产业联动 → 预测查看 | 会议呈现 |
| 资源订阅 | 订阅 Tab | 规则新增 → 预览命中 → 推送消费 | 推送流（→POOL TP-08） |

## 2. 状态机

### 2.1 地图选中

```
(无选中) --点位点击/列表行点击--> selected(pointId)（持久化）
selected --类别筛选滤除该点--> (无选中，自动清除)
selected --再次点击同点--> (取消选中)
```

### 2.2 订阅规则

```
(表单) --校验通过+非重复--> 活跃规则（持久化）--删除(二次确认)--> 移除
活跃规则 创建时 --> 触发 appendGeneratedPush（POOL 推送流 unread 条目）
```

### 2.3 驾驶舱定制

```
默认全显 --抽屉勾选--> 自定义显隐（持久化，≥1 张校验）--恢复默认--> 全显
```

## 3. 交互与状态覆盖细则

- **URL 契约**：`/talent/map?tab=map|index|search|cockpit|subscription`；tab 为上下文真源，刷新/分享恢复。
- **持久化键**（localStorage，前缀 `zhiku-tm-`）：`categories` / `heat` / `selected-point` / `index-weights` / `index-region` / `index-chart` / `search-mode` / `search-history` / `cockpit-cards` / `cockpit-industry` / `rules`。
- **双向联动协议**：地图与列表共享 `selectedId`；任一侧变更即同步另一侧（TalentMapView 已具备 selectedId prop + select 事件，R2 增量）。
- **诚实性交互**：`ZHIKU-TM-INDEX-SCORE` 与 `ZHIKU-TM-COCKPIT-ALERT` 用红问号（IconQuestionCircle #F53F3F），点开仅显 GAP 治理引用；权重和为 0 时得分显示"—"，禁止 NaN/伪值。
- **反馈**：规则新增成功 Message 双提示（"已订阅"+"已生成推送提醒"）；删除类动作 Modal 二次确认。
- **键盘可达**：滑杆左右键步进；检索回车提交；抽屉/Modal Esc 关闭。
- **无障碍**：地图点位提供列表等价操作路径（列表行=点位的可达替代）；⚠️ 声明 role=alert。

## 4. ReviewMode 集成

- MetricCard ⓘ/？/🧪/就绪度角标经评审层门控，组件自闸，关闭评审模式 DOM 零泄漏。
- 指数/预测的"演示态计算"业务声明（面向甲方诚实性）不随评审模式隐藏。

## 5. 机器可读交付契约

```yaml
frames:
  - { id: F-TM-01, route: /talent/map, query: [tab=map] }
  - { id: F-TM-02, route: /talent/map, query: [tab=index] }
  - { id: F-TM-03, route: /talent/map, query: [tab=search] }
  - { id: F-TM-04, route: /talent/map, query: [tab=cockpit] }
  - { id: F-TM-05, route: /talent/map, query: [tab=subscription] }
stores:
  - useTalentMapStore   # 全部 TM 用户态（zhiku-tm-）
persistence:
  prefix: zhiku-tm-
  keys: [categories, heat, selected-point, index-weights, index-region, index-chart, search-mode, search-history, cockpit-cards, cockpit-industry, rules]
cross_leaf:
  - { to: ZHIKU-WRITING, api: useWritingTaskStore.createTask, trigger: F-TM-01 生成人才地图分析报告 }
  - { to: ZHIKU-TALENT-POOL, api: useTalentNewsStore.appendGeneratedPush, trigger: F-TM-05 新增订阅规则 }
  - { to: ZHIKU-TALENT-POOL, route: /talent/profile?scholar=, trigger: F-TM-03 画像下钻 }
acceptance_source: USM-ZHIKU-TALENT-MAP.md AC-US-ZHIKU-TM-01..06
```

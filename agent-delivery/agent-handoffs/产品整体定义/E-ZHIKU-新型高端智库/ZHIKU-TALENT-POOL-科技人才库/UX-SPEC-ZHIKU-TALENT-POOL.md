# UX-SPEC-ZHIKU-TALENT-POOL｜科技人才库 交互规范

> **版本**：v1.0-rework-r3；交互底座依《UX-UE 通用交互组件规范》（D10），视觉 token 依 Design.md。

## 1. 用户旅程与任务流

| 旅程 | 入口 | 主任务流 | 出口 |
| --- | --- | --- | --- |
| 画像研判 | 左侧菜单/其他页回链 | 搜索或切换学者 → 四页签浏览 → 收藏 | 收藏夹 / 相似学者跳转 |
| 池沉淀 | 人才库·TOP100 | 筛选 → 勾选 → 保存池 → 维护池 | 池导出 / 写作模块（报告出口） |
| 清单检索 | 人才库·列表筛选 | 组合筛选 → 视图切换 → 统计研判 → 导出 | CSV 清单 |
| 动态跟踪 | 人才动态 | 资讯过滤 → 回链画像 / 订阅关键词 → 推送消费 | 推送已读 |

## 2. 状态机

### 2.1 专属人才池

```
(无) --保存(名称+成员≥1)--> 活跃池 --重命名/更新成员--> 活跃池
活跃池 --删除(二次确认)--> (移除，5s 撤销提示)
```

### 2.2 推送条目

```
unread --标记已读/全部已读--> read（持久化，不可回退）
偏好新增 --生成--> unread（push-gen-*，🧪）
```

### 2.3 推荐条目（领域分类）

```
fresh --标记已阅--> read（移入已阅分组，持久化）
```

## 3. 交互与状态覆盖细则

- **URL 契约**：`/talent/profile?scholar=&tab=`；`/talent/pool?tab=`；`/talent/news?tab=`。路由 query 为上下文真源，store 与 URL 双向同步（进入时 URL 优先）。
- **持久化键**（localStorage，前缀 `zhiku-tp-`）：`favorites` / `pools` / `top100-filters` / `list-filters` / `list-view` / `domain-selected` / `rec-read` / `news-filters` / `push-feed` / `push-read` / `preferences` / `profile-last`。
- **反馈**：所有落库动作 Message 成功提示；破坏性动作（删池）Modal 二次确认；导出成功提示文件名。
- **空态**：局部 Empty（不整页替换），带引导动作（清空筛选/去订阅/去收藏）。
- **加载**：智能识别类模拟动作用按钮 loading ≥600ms；页签切换不加骨架（本地数据）。
- **失败恢复**：localStorage 写失败静默降级（不阻断交互）；URL 非法参数回退默认值并 Message 提示。
- **键盘可达**：筛选输入回车提交；表格行勾选空格切换（Arco 默认）；抽屉/Modal Esc 关闭。
- **无障碍**：收藏星标带 aria-label（收藏/取消收藏 XXX）；⚠️ 声明条 role=alert。

## 4. ReviewMode 集成

- 所有 MetricCard ⓘ/🧪/就绪度角标经评审层门控（reviewMode），组件自闸；关闭评审模式 DOM 零泄漏（无 metric_id/GAP-*/Q0xx 字样）。
- 心理信息 ⚠️ Q-ZHIKU-05 声明为业务态文案（非评审层），关闭评审模式仍保留（面向甲方的边界诚实性）。

## 5. 机器可读交付契约

```yaml
frames:
  - id: F-TP-01
    route: /talent/profile
    query: [scholar, tab]
    tabs: [basic, relation, behavior, psych]
  - id: F-TP-02
    route: /talent/pool
    query: [tab=domain]
  - id: F-TP-03
    route: /talent/pool
    query: [tab=top100]
  - id: F-TP-04
    route: /talent/pool
    query: [tab=list]
  - id: F-TP-05
    route: /talent/news
    query: [tab=news]
  - id: F-TP-06
    route: /talent/news
    query: [tab=push]
stores:
  - useTalentProfileStore   # 画像上下文 + 搜索
  - useTalentPoolStore      # 分类/TOP100/列表/池/收藏（zhiku-tp-）
  - useTalentNewsStore      # 资讯/偏好/推送（zhiku-tp-）
persistence:
  prefix: zhiku-tp-
  keys: [favorites, pools, top100-filters, list-filters, list-view, domain-selected, rec-read, news-filters, push-feed, push-read, preferences, profile-last]
cross_leaf:
  - to: ZHIKU-WRITING
    api: useWritingTaskStore.createTask
    trigger: F-TP-03 池"生成人才池分析报告"
  - from: ZHIKU-TALENT-MAP
    api: useTalentNewsStore.appendGeneratedPush
    trigger: TM-05 新增订阅规则
acceptance_source: USM-ZHIKU-TALENT-POOL.md AC-US-ZHIKU-TP-01..08
```

# UX-SPEC-SVCCHAIN-RECOMMEND｜机构招引培育 交互规格

> **版本**：v1.0-r3（移除 US-05 / F-SVC-REC-04 收藏，对齐 bid-reference）
> 通用交互底座：`UX-UE 通用交互组件规范.md`（D10）；本文件只写模块特有契约。

## 1. 用户旅程（主线）

设定产业方向 → 招引页签调权重 → 生成名单 → 导出 → 培育页签设筛选与权重 → 生成培育名单 → 展开建议/下钻画像 → 加入对比篮。

## 2. 状态机

### 2.1 页面壳

| 状态 | 进入条件 | 表现 |
| --- | --- | --- |
| tab=attract/cultivate | URL 或点击 | 各页签状态互不清除 |
| industry 非法 | URL 参数不在字典 | 回落默认 + Message |
| tab=watchlist（遗留 URL） | 旧书签/分享链 | Message 提示已下线，回落 attract |

### 2.2 名单生成（招引/培育同构）

| 状态 | 条件 | 表现 |
| --- | --- | --- |
| idle | 未生成 | 引导空态 |
| invalid | 权重合计≠100 或（培育）筛选全空 | 生成按钮禁用 + 红字原因 |
| generated | 生成成功 | 排名表 + 表尾计数 |
| stale | 生成后配置/产业变更 | 黄条"配置已变更，请重新生成"，旧表可读 |
| empty | 候选集为空/匹配全 0 | 语义空态文案，不渲染空表 |

生成为同步纯函数计算（确定性）；同配置重复生成结果一致。

### 2.3 对比篮

- "+篮"走系统篮 `service_org`；满篮时 Message 拒绝且按钮态不变；已在篮显示"已加入"可反向移除（R2B 契约，详见 R1 UX-SPEC 修订版 §对比篮）。

## 3. 反馈与错误恢复

| 场景 | 反馈 |
| --- | --- |
| 归一化成功 | 权重值就地更新，无 Message 打扰 |
| 导出成功 | Message"已导出 N 条"；文件含演示口径声明行 |
| `org` 参数非法 | Message + 清 URL 参数，页面不崩 |
| localStorage 损坏 | 回落默认配置 + 一次性 Message |

## 4. 键盘与无障碍

- 权重输入框支持 ↑/↓ 步进 5；Tab 顺序 = 视觉顺序。
- 排名表行展开（培育建议）支持 Enter/Space；抽屉 Esc 关闭焦点还原（D10 通用规则）。
- 徽章均有 aria-label（复用 `SvcMetricBadges` 既有实现）。

## 5. 响应式

≥1440 配置区与结果区上下排；1024-1439 表格横向滚动；<1024 不承诺（PC 工作台）。

## 6. 持久化契约

`localStorage key = topic-svc-recommend`（version 字段 + 损坏回落；v2 起移除收藏字段）：

| 字段 | 内容 |
| --- | --- |
| `industry` | 产业方向 |
| `attract.weights` / `cultivate.weights` | 两模型权重 |
| `cultivate.orgTypes` / `cultivate.stages` | 培育筛选 |
| `activeTab` | 页签（attract \| cultivate） |

对比篮内容不在本 key（系统篮统一持久化，R2B）。

## 7. 与企业检索模式的差异登记（R2B 要求）

| 点 | 企业模式 | 本叶子 | 理由 |
| --- | --- | --- | --- |
| 招引名单入篮 | 企业结果行可入篮 | 外部机构**不可**入篮 | 外部机构不在库、无画像/技术力数据，入篮后对比分析无数据支撑；诚实态优先 |
| 培育名单入篮 | — | 本土机构可入篮 | org_id 与 R1 在库机构对齐 |

## 8. ReviewMode 联动

⚠️（Q-SVCCHAIN-05）与 metric_id 文案仅评审模式渲染；业务模式保留 ⓘ、🧪 与"演示模型口径"可读声明；关闭评审模式 DOM 无 `Q0xx/GAP-*` 泄漏。

## 9. 机器可读交付契约

| 项 | 值 |
| --- | --- |
| 路由 | `/service-center/recommend` |
| URL 参数 | `tab` / `industry` / `org` |
| store | `serviceRecommendStore.ts`（reducer + localStorage） |
| 数据 | `serviceRecommendData.ts`（确定性 mock）+ `serviceRecommendModel.ts`（纯函数） |
| D9 | `serviceReadinessSeed.ts` 增补 3 个 metric；`serviceReviewData.ts` 增补 8 件套与 TRACE 行 |

# UX-SPEC-ZHIKU-TECH-TREND｜技术趋势分析 · 交互规格

> **版本**：v1.0-rework-r4；交互基线遵循《UX-UE 通用交互组件规范》（D10）与 Design.md（D8）

## 1. 任务流与 Frame 映射

| 旅程 | 步骤 | Frame |
| --- | --- | --- |
| 主题发现 | 聚类任务 → 结果 → 权重定制 → 清单导出 | F-TT-01 |
| 关系挖掘 | 网络任务 → 矩阵下钻 → 规则调整 → 主题/作者 | F-TT-02（作者 → CT-TT-01） |
| 四维研判 | 热点 → 交叉 → 合作 → 趋势 | F-TT-03 |
| 信号处置 | 预警处理 → 跟踪 → 订阅 → 检测 → 报告 | F-TT-04（报告 → CT-TT-02） |

## 2. 状态与转移

- **Tab 态**：`?tab=cluster|network|hotspot|alert`，非法回落 cluster。
- **任务状态机**：聚类 `created → running(模拟≥1.2s) → done | failed`，failed 可重跑；共性网络同构；检测任务运行即出结果（历史累积）。
- **权重校验**：三滑杆和 ≠100 → 重算禁用 + 差值提示；=100 → 可重算，重算后簇按加权得分重排。
- **规则联动**：规则 `enabled=false` → 语义主题区过滤对应主题并显示"受规则影响"提示；全部停用 → Empty。
- **预警**：`pending → handled`（单向，分组转移）；订阅规则重复关键词幂等拦截。
- **趋势勾选**：至少保留一项才渲染图表，全取消显示 Empty。

## 3. 反馈与错误恢复

| 场景 | 反馈 |
| --- | --- |
| 权重和 ≠100 | 按钮 disabled + "当前合计 X，需为 100" |
| 任务名/订阅关键词/规则阈值非法 | 表单 error，不关弹窗 |
| 删除任务/规则 | a-popconfirm 确认 |
| 矩阵空单元格 | 不可点击（cursor 默认） |
| 检测未选目标 | 运行按钮 disabled |
| 各区无结果 | 局部 EmptyState + 一键恢复（清空搜索/启用规则/勾选技术） |
| 恢复演示数据 | Modal.confirm 后重置 `zhiku-tt-` 全部 key |

## 4. 组件与可达性

- Arco 组件：a-tabs/a-slider/a-switch/a-checkbox-group/a-timeline/a-drawer/a-popconfirm/a-table/a-card/a-modal。
- 键盘：抽屉/弹窗 Esc；滑杆方向键微调（Arco 原生）；开关 Space 切换。
- D9 角标：`ZHIKU-TT-CLUSTER-TOTAL`/`ZHIKU-TT-HOTSPOT-TOTAL`/`ZHIKU-TT-ALERT-PENDING` 三卡 ⓘ+🧪；`ZHIKU-TT-TREND-FORECAST` 红问号（IconQuestionCircle `#F53F3F`）只显 GAP 引用；聚类/语义/检测/订阅命中行内 🧪。

## 5. 机器可读交付契约

```yaml
frames:
  - { id: F-TT-01, route: /strategy/tech-trend, query: { tab: cluster } }
  - { id: F-TT-02, route: /strategy/tech-trend, query: { tab: network } }
  - { id: F-TT-03, route: /strategy/tech-trend, query: { tab: hotspot } }
  - { id: F-TT-04, route: /strategy/tech-trend, query: { tab: alert } }
stores:
  - { id: useClusterAnalysisStore, file: src/mock/clusterAnalysis.ts, persistence_prefix: zhiku-tt-, keys: [cluster-tasks, weights, custom-list, cluster-ui] }
  - { id: useCommonNetworkStore, file: src/mock/commonNetwork.ts, persistence_prefix: zhiku-tt-, keys: [cn-tasks, rules] }
  - { id: useTechHotspotStore, file: src/mock/techHotspot.ts, persistence_prefix: zhiku-tt-, keys: [hotspot-ui] }
  - { id: useTechAlertStore, file: src/mock/techAlert.ts, persistence_prefix: zhiku-tt-, keys: [alerts, subscriptions, detections, alert-ui] }
cross_leaf:
  - { id: CT-TT-01, target: route, route: /talent/profile }
  - { id: CT-TT-02, target: useWritingTaskStore.createTask, route: /writing/create }
acceptance_source: USM-ZHIKU-TECH-TREND.md#4
```

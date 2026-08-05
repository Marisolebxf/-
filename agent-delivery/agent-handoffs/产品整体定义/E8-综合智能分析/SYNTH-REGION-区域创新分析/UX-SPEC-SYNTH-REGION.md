# UX-SPEC-SYNTH-REGION｜交互规范

> 版本 v1.0-r3。视觉 token 以 `Design.md` + 本仓既有 Tailwind/Arco 混合基线为准；交互行为以 `UX-UE 通用交互组件规范.md`（D10）为准。本文只定本叶子特有契约。

## 1. 组件选型（Arco 边界）

| 场景 | 组件 | 约束 |
| --- | --- | --- |
| 上下文条选择器 | Arco `Select` | 三页同构；切换即生效，无"确认"二段提交 |
| 指标体系分层 | 自绘维度卡 + 展开行 | 展开动画 ≤200ms；键盘 Enter/Space 可展开 |
| 排名榜区域卡 | 自绘卡片（button 语义） | 点击/Enter 切换目标区域；当前卡 `aria-current` |
| 要素/主体抽屉 | Arco `Drawer` | 关闭后焦点回触发元素；ESC 可关 |
| 关系图谱 | `ForceGraph`（ECharts 力导向） | roam + drag；节点 click 下钻分流 |
| 雷达/曲线/条形 | ECharts（复用仓内封装）或自绘条形 | 图表失败局部错误 + 重试 |
| 提示 | Arco `Message` | 参数非法 / 恢复默认 / 伪跳转拦截 |

## 2. 状态机

### 2.1 区域上下文（三页共享）

```
初始化: URL(region,window) 合法 → 用 URL；否则 localStorage(v 匹配) → 用持久化；否则默认(深圳市/全国重点城市/近5年)
切换: dispatch → 全页重算 → URL replace 同步 → localStorage 写入
非法参数: Message + 清参 + 回落
```

### 2.2 下钻链路

```
F-SYN-01 排名卡 click → region 切换（同页）
F-SYN-01 [下钻要素分析] → /intelligence/elements?region=&window=
F-SYN-02 [促协同分析] → /intelligence/collaboration?region=&window=
F-SYN-02 要素卡 click → Drawer(element=) → 关闭清参
F-SYN-03 节点 click → enterprise: navigate(CT-SYN-01)
                    → svcOrg: navigate(CT-SYN-02)
                    → talent/institution: Drawer(F-SYN-05)
浏览器返回：navigate 均为 push，返回可回上一状态
```

### 2.3 图谱选中

```
node click(人才/高校) → selectedNode + Drawer
中心性列表 click → selectedNode 高亮（再次点击取消）
集群卡 click → selectedCluster → highlightNodes/links（再次点击取消）
筛选变更 → 选中态若被过滤则清除
```

## 3. 持久化契约

- Key：`topic-synth-workbench`；shape `{ v: 1, state: SynthState }`；版本不符 / 解析失败 → 回默认 + Message。
- 持久化字段：region / compareScope / window / expandedDims / graphFilters（industry + nodeKinds）。
- 不持久化：抽屉开合（走 URL）、选中节点/集群（`node` 参数可选恢复）。
- URL 优先级 > localStorage > 默认。

## 4. 异常与空态总表

| 场景 | 表现 | 恢复 |
| --- | --- | --- |
| 非法 region/element/node 参数 | Message + 清参 + 回落 | 重新选择 |
| 区级口径无对比/排名 | 对应区局部空态文案，其余区正常 | 切市级 |
| 指标/要素无数据 | "暂无数据"置灰，不 0 填充、不参与结论 | 换口径 |
| 图谱筛选无节点 | 图谱容器空态 + 统计归零 | 放宽筛选 |
| 跨模块目标不存在 | 拦截跳转 + Message"目标画像暂不可用" | 留在当前页 |
| 图表渲染失败 | 局部错误卡 + 重试按钮，壳与上下文保留 | 重试 |
| 相关性样本不足 | 文案"样本不足"，不画伪相关线 | 扩大时间窗 |

## 5. 键盘与无障碍

- 排名卡 / 维度卡 / 要素条 / 集群卡 / 中心性项均为 `button` 语义，Tab 可达，Enter/Space 触发。
- Drawer 打开焦点入内、关闭回触发元素；`aria-label` 完整。
- 图谱为鼠标主导交互，键盘用户经中心性列表 / 集群卡 / 孤立主体列表等价到达节点详情（等价路径原则）。
- 角标按钮 `aria-label="{mountId} 内部评审说明"`。

## 6. D9 评审层

- 评审层集中在 `intelligence/` 域内单套文件（`IntelReviewMount` + `IntelMetricBadges` + `intelReviewData` + `intelReadinessSeed`），组织方式对齐 service-center。
- 门控：`useCurrentUser().reviewMode`；组件自闸；关闭评审模式 DOM 零泄漏（无 metric_id / Q-SYNTH-* / GAP-* 字样）。
- 排列顺序：数字 → [ⓘ/❓] → [结构] → [⚠️] → [🧪]；同点位 ≤3 枚、间距 4px；全部 Arco Icon。
- D1 missing 指标（活力指数 / 要素评价 / 要素贡献度 / 协同指数 / 相关系数）：红问号只显治理引用，不显伪 8 件套；诚实性约束按 policy v1.3 §2.3。

## 7. 观测埋点

沿用仓内 `observability` 惯例：region 切换、排名卡切换、顺链下钻、要素抽屉、图谱节点下钻（分流类型）、集群高亮、报告触发。

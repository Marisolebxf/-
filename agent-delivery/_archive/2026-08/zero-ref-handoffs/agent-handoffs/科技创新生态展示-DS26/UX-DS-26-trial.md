# UX-DS-26-trial · ux-agent 试点 · DS-26 科技创新生态展示 IA/wireframe

## 执行时间

2026-06-22（ux-agent · 科技成果展示模块第三次 UX 试点）

## 评审状态

| 项 | 状态 |
|---|---|
| UI/UE 评审 | ✅ **通过**（2026-06-22，用户确认） |
| push origin/main | ❌ **被拒**（main 为 protected branch；需 PM/有权限账号 push 或走 feature 分支 + MR） |
| 本地 commit | ✅ `d2d814c`（rebase 后仍在 main，working tree clean） |
| 下一步 | 派 **ui-agent** 实现 `/sandbox/innovation-ecosystem/*` |

## 任务

- 覆盖功能点：**DS-26 科技创新生态展示**（acceptance-catalog tier=INTEG，行 310–321）
- 范围真源：`bid-reference/科技信息展示系统和科技专题服务系统.md` §1.1.1.1.4.6.2（行 3403–3475，3 个三级子功能 + 12 项四级）
- 设计规范：`agent-delivery/Design.md` §0–§3、§7–§8、§13
- 数据血缘：`agent-delivery/data-lineage-policy.md`（metric_id 前缀 `M_IC_*`）
- 工作仓：`E:/gkx-lumen/repos/demo-ui-science`（仅 docs，不写代码）

## 完成清单（对照 ux.mdc 自检 11 条）

| # | 检查项 | 状态 | 证据 |
|---|--------|------|------|
| 1 | bid-reference 章节 100% 覆盖 | ✅ | IA §4 映射表 12/12 四级 |
| 2 | 路由命名 | ✅ | `/sandbox/innovation-ecosystem/*` |
| 3 | 异常路径 ≥3 | ✅ | userflow §3 共 5 条 |
| 4 | 埋点 ≥5 | ✅ | userflow §4 共 8 个 |
| 5 | 开放项标注 | ✅ | wireframe W-O1~10 + 本 handoff K-O1~7 |
| 6 | 隔离声明 | ✅ | README |
| 7 | Design.md 骨架命名 | ✅ | 无 PageShell/GlobalWorkbenchTabs |
| 8 | 信息架构骨架 §4 | ✅ | P-01~04 均有 5 段优先级 |
| 9 | 字段表 6 列 | ✅ | wireframe 四页 |
| 10 | metric_id 占位 | ✅ | 唯一 metric 21 个（见 §metric 汇总） |
| 11 | 业务口径未定登记 | ✅ | Q020–Q026 待 PM 同步客户决策清单 §2.2 |

## 产物绝对路径

1. `E:/gkx-lumen/repos/demo-ui-science/docs/ia/sandbox/innovation-ecosystem-2026-06-22/README.md`
2. `E:/gkx-lumen/repos/demo-ui-science/docs/ia/sandbox/innovation-ecosystem-2026-06-22/DS-26-IA.md`
3. `E:/gkx-lumen/repos/demo-ui-science/docs/ia/sandbox/innovation-ecosystem-2026-06-22/DS-26-userflow.md`
4. `E:/gkx-lumen/repos/demo-ui-science/docs/ia/sandbox/innovation-ecosystem-2026-06-22/DS-26-wireframe.md`
5. 本文件

## 体量统计

| 文件 | 说明 |
|------|------|
| README.md | 试点元信息 + 隔离声明 |
| DS-26-IA.md | IA + 路由 + 映射 |
| DS-26-userflow.md | Mermaid 主/异常路径 + 埋点 |
| DS-26-wireframe.md | 4 页 ASCII + 字段表 + metric 清单 |

## 范围与实现

| 项 | 内容 |
|---|---|
| scope_ref | bid §1.1.1.1.4.6.2.1 ~ §1.1.1.1.4.6.2.3 |
| implementation_as_built | **4 页**：P-01 总览驾驶舱 + P-02 载体地图 + P-03 人才态势 + P-04 协作网络 |
| data_gaps | 无 `DS-26-data-availability-matrix.md`；`dwd_innovation_carrier` ✅ 可直接映射；人才高端分类 / 宏观 KPI / 服务状态 ❌ 或 🧪 Mock |
| variance_note | 未扩至 DS-27 时空演进；P-01 宏观 KPI 按 bid 概述段保留但标 Mock |

## 页面数与覆盖功能点

- **页面数**：4
- **覆盖功能点**：DS-26（§2.1 载体地图 ×4 + §2.2 人才态势 ×4 + §2.3 协作关系 ×4 = 12 四级叶子）

## metric_id 汇总（21 个唯一 ID）

`M_IC_CARRIER_TOTAL`, `M_IC_CARRIER_NEW_COUNT_Y`, `M_IC_CARRIER_YOY_GROWTH`, `M_IC_CARRIER_NEW_COUNT_Q`, `M_IC_CARRIER_QOQ_GROWTH`, `M_IC_CARRIER_DENSITY_BY_REGION`, `M_IC_CARRIER_BY_TYPE`, `M_IC_TALENT_TOTAL`, `M_IC_TALENT_NEW_COUNT_Y`, `M_IC_TALENT_DENSITY_BY_REGION`, `M_IC_TALENT_BY_CATEGORY`, `M_IC_TALENT_CARRIER_MATCH`, `M_IC_COLLAB_PROJECT_COUNT`, `M_IC_COLLAB_EDGE_WEIGHT`, `M_IC_COLLAB_PATENT_COUNT`, `M_IC_COLLAB_NETWORK_DENSITY`, `M_IC_COLLAB_INFLUENCE_SCORE`, `M_IC_HITECH_ENT_TOTAL` (Mock), `M_IC_SK_INNOV_HK_ENT_TOTAL` (Mock), `M_IC_HITECH_GDP_RATIO` (Mock)

## 开放项（待 UI/UE 评审，7 条 K-O）

| # | 决策项 | 团队临时默认 | 影响 | 客户决策清单 ID |
|---|--------|-------------|------|----------------|
| K-O1 | 载体/运营/入驻三元关系展示 | carrier + org_name | P-02 Drawer | **Q020** |
| K-O2 | 院士/千人/孔雀 ODS 映射 | dwd_scholar + 标签 Mock | P-03 | **Q021** |
| K-O3 | 区划下钻精度 | 市级 | 地图 | **Q022** |
| K-O4 | 载体服务状态/预约 | 静态 Mock | P-02 | **Q023** |
| K-O5 | 深港/GDP 宏观 KPI | P-01 MockBadge | P-01 | **Q024/Q025** |
| K-O6 | G6 聚合阈值 | >300 节点 | P-04 | — |
| K-O7 | 热力密度算法 | COUNT/网格 | P-02 | **Q026** |

> **PM 动作**：请将 Q020–Q026 同步至 `agent-delivery/客户决策清单跟踪表.md` §2.2。

## 给 ui-agent 的 Arco 控件映射建议

| 场景 | Arco / 业务组件 |
|------|----------------|
| 页面骨架 | `Layout`, `Grid`, `Space` → class `app-shell` / `app-frame` / `content-shell` / `workspace-grid` |
| 顶栏筛选 | `Form`, `Cascader`, `DatePicker.RangePicker`, `Select`, `Input`, `Button` |
| 左侧图层 | `Checkbox.Group`, `Switch` → `layer-panel` |
| 地图 | Leaflet + `Button`(`IconZoomIn/Out/Fullscreen/Refresh`) |
| 协作网络 | AntV G6（`@antv/g6`）→ `graph-stage` |
| 右侧分析 | `Tabs`（§7.3 轻量蓝字）+ `Table` + `Pagination` + `Statistic` |
| KPI ⓘ | `MetricSpecCard`（Card + Drawer + Descriptions） |
| Mock | `MockBadge`（Tag orange）+ `Alert` |
| 待确认 | `Tag` ⚠️ + `Tooltip` |
| 下钻 | `Drawer` width=480 |
| 图表 | ECharts（折线/饼/条形） |
| 空/错/加载 | `Empty`, `Alert`, `Skeleton`, `Spin` |

**路由实现建议**：

```
/sandbox/innovation-ecosystem/overview   → P-01
/sandbox/innovation-ecosystem/carriers   → P-02
/sandbox/innovation-ecosystem/talents    → P-03
/sandbox/innovation-ecosystem/collaboration → P-04
```

**禁止**：同页 import `antd`；删除 `analysis-panel`；使用 GlobalWorkbenchTabs / PageShell 等废止名。

## git 状态

```
bf929e8 [sandbox] ux-agent 试点：DS-26 科技创新生态展示 IA/wireframe [agent:ux-agent]
```

- **改动**：4 files changed, 653 insertions(+)（rebase 于 remote `037e1f0 迁移` 之上）
- **push**：❌ main 受保护，本地 ahead 1 commit；待 PM 有权限 push 或 MR

## 阻塞项

| 阻塞 | 说明 | 建议 |
|------|------|------|
| 无 DS-26 数据映射表 | data-agent 未建 matrix | PM 排 data-agent 建 `DS-26-data-availability-matrix.md`；ui-agent 可先用 wireframe mock |
| Q021 人才分类 | ODS 无院士/千人/孔雀字段 | Wave 0 Mock + ⚠️，不阻塞 ui 沙箱 |
| Q024/Q025 宏观 KPI | 无 ODS | P-01 MockBadge，不阻塞 |

## 下一步

1. **UI/UE 评审**本 handoff + 4 份 md
2. 评审通过后 **ui-agent** 在 `demo-ui-science` 实现沙箱页
3. PM 同步 Q020–Q026 至客户决策清单
4. data-agent 补 `DS-26-data-availability-matrix.md`

---

**ux-agent 停止于此，等待评审通过后派 ui-agent。**

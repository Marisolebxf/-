# UX-DS-28-trial · ux-agent 试点 · DS-28 大型科学仪器共享 IA/wireframe

## 执行时间

2026-07-17（ux-agent · 科技成果展示 · 仪器共享首日上手试点）

## 评审状态

| 项 | 状态 |
|---|---|
| UI/UE / mentor 评审 | ⏳ **待评审** |
| 登记 task-registry | ❌ **本任务不登记**（留给 mentor 决定） |
| 本地 commit | ✅ demo `4e0f4ed` + orchestration `6b7e638` |
| push | ❌ **不 push**（按任务要求） |
| 下一步 | mentor 评审 → 可选登记 registry → 派 **ui-agent** |

## 任务

- 覆盖功能点：**DS-28 大型科学仪器共享**（acceptance-catalog tier=INTEG）
- catalog 口径：**对接仪器共享平台可视化展示**；不单独承担完整预约与运营闭环
- 范围真源：`bid-reference/科技信息展示系统和科技专题服务系统.md` §1.1.1.1.4.6.4（行 3561–3645）
- 设计规范：`Design.md` §0/§3/§7/§8/§14
- 数据血缘：`data-lineage-policy.md`（metric_id 前缀 `M_INSTR_*`）
- 工作仓：`${GKX_ROOT}/repos/demo-ui-science`（仅 docs，不写代码）
- 质量标杆：DS-26（结构可参考 DS-15，但不抄口语区块名 / 5 列字段表）

## 完成清单（对照 ux.mdc 自检 11 条）

| # | 检查项 | 状态 | 证据 |
|---|--------|------|------|
| 1 | bid-reference 章节 100% 覆盖 | ✅ | IA §4：§4.6.4.1/3 完整；§4.6.4.2 → stub 映射 |
| 2 | 路由命名 | ✅ | `/sandbox/instrument-share-2026-07-17/*` |
| 3 | 异常路径 ≥3 | ✅ | userflow §3 共 5 条 |
| 4 | 埋点 ≥5 | ✅ | userflow §4 共 9 个 |
| 5 | 开放项标注 | ✅ | wireframe W-O1~7 + 本 handoff K-O1~7 |
| 6 | 隔离声明 | ✅ | README |
| 7 | Design.md 骨架命名 | ✅ | 无 PageShell / GlobalWorkbenchTabs |
| 8 | 信息架构骨架 §4 | ✅ | P-01~04 均有 5 段优先级 |
| 9 | 字段表 6 列 | ✅ | wireframe 四页 |
| 10 | metric_id 占位 | ✅ | 唯一 15 个 `M_INSTR_*` |
| 11 | 业务口径未定登记 | ✅ | Q051–Q057 待 PM 同步客户决策清单 |

## 产物绝对路径

1. `${GKX_ROOT}/repos/demo-ui-science/docs/ia/sandbox/instrument-share-2026-07-17/README.md`
2. `…/DS-28-IA.md`
3. `…/DS-28-userflow.md`
4. `…/DS-28-wireframe.md`
5. 本文件：`agent-delivery/agent-handoffs/大型科学仪器共享-DS28/UX-DS-28-trial.md`

## 体量统计

| 文件 | 说明 |
|------|------|
| README.md | 试点元信息 + 隔离 + 与 DS-15/26 差异 + ui 接力 |
| DS-28-IA.md | IA + 路由 + bid 映射 + 超范围说明 |
| DS-28-userflow.md | Mermaid 主/异常 + 埋点 |
| DS-28-wireframe.md | 4 页 ASCII + 6 列字段表 + metric 清单 |

## 范围与实现

| 项 | 内容 |
|---|---|
| scope_ref | bid §1.1.1.1.4.6.4.1 ~ §1.1.1.1.4.6.4.3 |
| implementation_as_built | **4 页**：P-01 藏宝图 + P-02 详情 + P-03 机构 + P-04 预约对接 stub |
| data_gaps | 无 `DS-28-data-availability-matrix.md`；字段一律 🧪 Mock |
| variance_note | §4.6.4.2 按 catalog 裁为对接展示；**未**设计站内下单/排期/订单闭环 |

## 页面数与覆盖功能点

- **页面数**：4（≤4）
- **覆盖**：§4.6.4.1 五级叶子 → P-01/P-02；§4.6.4.3 四级叶子 → P-03；§4.6.4.2 → P-04 stub + 只读服务字段

## metric_id 汇总

`M_INSTR_TOTAL`, `M_INSTR_OPEN_COUNT`, `M_INSTR_SHARE_RATE`, `M_INSTR_ORIGINAL_VALUE_SUM`, `M_INSTR_ORG_TOTAL`, `M_INSTR_BY_CATEGORY`, `M_INSTR_BY_STATUS`, `M_INSTR_DENSITY_BY_REGION`, `M_INSTR_RATING_AVG`, `M_INSTR_USE_FREQ_90D`, `M_INSTR_ORG_RATING_AVG`, `M_INSTR_ORG_SHARE_SCORE`, `M_INSTR_ORG_OPEN_RATE`, `M_INSTR_ORG_ACTIVE`, `M_INSTR_ORG_INSTR_COUNT`

## 开放项（≥5，待 mentor/PM）

| # | 决策项 | 团队临时默认 | 影响 | 客户决策清单 ID |
|---|--------|-------------|------|----------------|
| K-O1 | 仪器主键与共享平台 ID 映射 | Mock `INS-*` | 全链路 | **Q051** |
| K-O2 | 外链 URL / SSO / ticket | URL+query；未配置禁用 CTA | P-04 | **Q052** |
| K-O3 | 服务状态枚举对齐 | 空闲/排期协调/忙碌 | P-01 图例 | **Q053** |
| K-O4 | 原值/价格脱敏 | 默认脱敏 | P-02 | **Q054** |
| K-O5 | 区划精度与密度算法 | 区级；COUNT/面积 Mock | P-01 | **Q055** |
| K-O6 | 创新载体字段来源 | 文本 Mock，不硬链 DS-26 | P-02 | **Q056** |
| K-O7 | 机构共享能力评分公式 | 0–100 Mock | P-03 | **Q057** |

> **PM 动作**：请将 Q051–Q057 同步至 `agent-delivery/客户决策清单跟踪表.md` §2.2（本试点**未改**该表，避免越权）。

## 给 ui-agent 的 Arco 控件映射建议

| 场景 | Arco / 业务组件 |
|------|----------------|
| 页面骨架 | `Layout`/`Grid`/`Space` → `app-shell` / `app-frame` / `content-shell` / `workspace-grid` |
| 顶栏筛选 | `Form`, `Cascader`, `Select`, `Input`, `Button` |
| 左侧图层 | `Checkbox.Group`, `Switch` → `layer-panel` |
| 地图 | Leaflet + 缩放/全屏/刷新图标按钮 |
| 右侧分析 | `Tabs`（§7.3）+ `Table` + `Pagination` + `Statistic` |
| KPI ⓘ | `MetricSpecCard` |
| Mock | `MockBadge` + `Alert` |
| 待确认 | `Tag` ⚠️ + `Tooltip` |
| 下钻 | `Drawer` width=480 |
| 详情 | `Descriptions` + `Tabs` + `Breadcrumb` |
| stub | `Alert` + `Card` + 外链 `Button` |
| 空/错/加载 | `Empty`, `Alert`, `Skeleton`, `Spin`, `Result` |

**路由实现建议**：

```
/sandbox/instrument-share-2026-07-17/instruments              → P-01
/sandbox/instrument-share-2026-07-17/instruments/:instrumentId → P-02
/sandbox/instrument-share-2026-07-17/orgs                      → P-03
/sandbox/instrument-share-2026-07-17/booking-bridge            → P-04
```

**mock 建议目录**：

```
mocks/instrument-share/
├── overview-kpi.json
├── instruments.json          # 含 status/category/geo，空值率 ≥15%
├── instruments/INS-….json
├── orgs.json
├── orgs/ORG-….json
└── bridge-config.json        # baseUrl / enabled
```

**禁止**：站内预约表单/订单表；同页 `antd`；删除 `analysis-panel`；废止骨架名。

## 阻塞项

| 阻塞 | 说明 | 建议 |
|------|------|------|
| demo-ui-science ACL | 仓 `docs/` 对 Everyone 仅 RX，需提权写入 | 已用提升权限落盘；若失败见 mentor |
| 无 DS-28 data matrix | 字段全 Mock | PM 排 data-agent |
| Q052 外链未定 | P-04 CTA 可能长期禁用 | 不阻塞其余三页 UI |

## 下一步（通知 mentor）

1. **请 mentor 评审**本 handoff + 沙箱 4 份 md  
2. 评审通过后决定是否 **登记 task-registry** 并派 **ui-agent**  
3. PM 同步 Q051–Q057 至客户决策清单  
4. data-agent 补 `DS-28-data-availability-matrix.md`

---

**ux-agent 停止于此：本地 commit（不 push），等待 mentor 评审。**

# Epic E-INNOV-M1 · demo2 与 innov 模块映射

> **策略**：demo2 独立演进；lumen 全新 fork；首 Epic 走创新监测快路径。
> **demo2 真源**：[https://skxrules.unicomcn.tech:30999/](https://skxrules.unicomcn.tech:30999/) · `gkx1/demo-ui-science.git`
> **实现基线**：`demo-ui-system-test` 已有 `/innov` 五 Tab（M1–M5），API 客户端已对齐 03 契约。

---

## 1. demo2「全球创新监测」→ API 模块

| demo2 Tab（中屏） | 对应 innov 模块 | 03 契约 API | lumen 首 Epic 范围 |
|------------------|----------------|-------------|---------------------|
| 全球创新实时数据 | M1 科创事件 | `/events`, `/events/heatmap`, `/events/stats` | **本 Epic 核心** |
| 创新载体排行榜 | M3 创新载体排行 | `/carriers/rank`, `/carriers/{id}` | Epic 2 |
| 城市创新能力分析 | M4 城市创新能力 | `/cities/rank`, `/cities/compare` | Epic 2 |
| 创新成果展示 | M2 落图赋分（部分） | `/graph/subgraph`, `/graph/influence/rank` | Epic 2 |

---

## 2. demo2 交互 vs demo-ui-system-test EventMap

| 能力 | demo2 全球创新实时数据 | demo-ui-system-test EventMap | M1 Epic 动作 |
|-----|----------------------|---------------------|-------------|
| 地域筛选 | 地域范围 combobox | 暂无（可后补 adminCode） | backlog |
| 时间 | 开始/结束年份 | daterange | 保持 daterange，后续对齐年粒度 |
| 类型 | 专利/论文/资讯/机构/企业 | 事件类型多选 | **已对齐**（eventTypes） |
| 领域 | 领域 combobox | 暂无 | backlog |
| 地图 | 显示模式/全屏 | Leaflet 点位+热力 | **已对齐** |
| 列表 | 创新价值排序、卡片 | 表格+分页 | Epic 内保持表格，UI 美化放 Epic 2 |
| 订阅/推送 | 订阅区域、推送记录 | 暂无 | M3 用户态，Epic 3 |
| 对比分析 | 对比分析按钮 | 暂无 | backlog |

---

## 3. 三仓文件锚点（demo → lumen 复制参考）

| 层 | demo 路径 | 说明 |
|----|----------|------|
| 前端 API | `demo-ui-system-test/src/api/innov/index.ts` | 已覆盖 M1–M5 + dict |
| 前端页面 | `demo-ui-system-test/src/views/innov/components/EventMap.vue` | M1 地图页 |
| Java | `demo-svc-platform/gkx-innov/.../EventController.java` | 事件 REST |
| Java DAO | `demo-svc-platform/gkx-innov/.../InnovDao.java` | ADS 只读 |
| 网关 | `demo-svc-platform/helm/.../gkx-gateway-dev.yml` | `/innov/**` |
| Python | `demo-algo-science/scripts/run_all.py` | 全流水线 |
| Helm | `demo-svc-platform/helm/gkx-platform/values.yaml` | innov + innovPy |

---

## 4. Epic 2 预告（M1 完成后）

按 demo2 四 Tab 顺序扩展（**格式/范围**可对照 V6 §3.2.4.x；**实现说明**按 lumen 实写）：

1. M3 载体排行 Tab → `CarrierRank.vue` · V6 §3.2.4.4 · §5.1.19
2. M4 城市对标 Tab → `CityIndex.vue` · V6 §3.2.4.6 · §5.1.21
3. M2 创新成果 → `GraphInfluence.vue` · V6 §3.2.4.1–2
4. M5 预测 → `ForecastView.vue` · V6 §3.2.4.3.5
5. demo2 全球创新监测 **整页 UI 换肤**（参考 demo2 布局，仍不接 demo2 git）

---

## 5. 正式文件 ↔ innov 对照（范围参考 · 内容实写）

| demo2 Tab | V6 范围（格式/章节） | innov API（技术口径） |
|-----------|---------------------|----------------------|
| 创新成果展示 | §3.2.4.1–2 | M2 部分 |
| 全球创新实时数据 | §3.2.4.3 | M1 /events |
| 创新载体排行榜 | §3.2.4.4 | M3 /carriers |
| 城市创新能力分析 | §3.2.4.6 | M4 /cities |

officecli 查章节是否存在（不必导出正文）：

```powershell
& $OC query $DOC 'paragraph:contains("3.2.4.3")'
```

---

## 6. 与报价表对应

| 报价表条目 | Epic |
|-----------|------|
| 全球创新监测-整体前后端设计和开发（中/大/小屏） | E-INNOV-M1（中屏 API 联调）→ 后续大屏/小屏适配 Epic |
| 湾区/深圳创新监测 | 共用 M1 API + 区域参数，独立 Epic |
| 创新监测-开发承接包 S2 里程碑 M1 | **本 Epic 验收口径** |

# Evidence · F-DS-POL-11/12 + 核增骨架

> task: DS10-12-V1-HIFI-L01 · 2026-08-05  
> packages: PKG-DS-POL-11-12 · PKG-DS-PC-SKELETON  
> checkpoint: **content_review_passed** + **nav_smoke_passed**（人工确认「通过」）

## 政策分析评价（F-DS-POL-11）

| 项 | 实现 |
|----|------|
| 决策 | `DEC-DS11-BID-ALIGN-20260808`：3 Tab · ECharts geo · chord · 画像摘要抽屉 · mock 队列+日志 |
| Tab | 仅「分析报告可视化 / 结果解读 / 推荐方案」 |
| 维度条 | `analysis/DimensionBar.jsx` → 驱动 `TrendMetricsChart` |
| 父段能力 | 地理分布 / 话题热力+网民态度 / 气泡 / 画像三卡抽屉 / 各地落实 / 弦线 chord+关系网+传导路径 |
| 叶子 | `.1.1` 趋势 · `.1.2` 分区群体对比 · `.1.3` 结构关联 · `.1.4` 模板批量队列+操作日志 |
| KPI D9 | `M_POLICY_FOCUS_INDEX` / `EFFECT_SCORE` / `SHORTBOARD_COUNT` / `LAYOUT_REC_COUNT` / `OPPORTUNITY_COUNT` + ⓘ / 🧪 |
| 文件 | `PolicyAnalysis.jsx` + `analysis/*` + `policyData.js`（DS-11 mock 段） |
| 方案 | `PLAN-DS11-政策分析评价-Bid对齐修订方案.md`（approved） |

入口：菜单「政策分析评价」→ `policy-analysis`

### 走查摘要（2026-08-08 · build 绿）

- [x] A1 仅 3 Tab + 维度条  
- [x] A3 地理 / 热力态度 / 气泡 / 画像 / 落实  
- [x] A4 弦线 chord（非 sankey）+ 关系网 + 传导路径  
- [x] A5 地区/行业/群体 · 柱+热力  
- [x] A6 批量队列 + 操作日志（🧪）

### 结果解读（DEC-DS11-INTERPRET · 2026-08-08）

- [x] B1 四区：热点诊断 / 互动 / 多媒体 / 摘要推送  
- [x] B2 诊断图 + 高频/异常/重点打标 + 案例抽屉  
- [x] B3 专题切换 → 结论高亮 + 应用建议  
- [x] B4 视频占位播放 + 数据动画 + 侧栏文字评议  
- [x] B5 推送管理层 → 站内队列（未外发）  
- [x] B6 摘要可编辑 · 🧪 NLP 演示  


## 政策效果推演（F-DS-POL-12）

| 项 | 实现 |
|----|------|
| 分轨条 | 权限/图谱经平台 API；禁止浏览器直连 Nebula/Python |
| KPI D9 | 效果分 / 实施效果 / 支持力度 / 布局建议数 + ⓘ / 🧪 |
| IA | 2 主 Tab：效果预估 / 科技政策推演（`DEC-DS12`） |
| 文件 | `PolicySimulation.jsx` + `simulation/estimate/*` + `simulation/interpret/*` |

入口：菜单「政策效果推演」→ `policy-simulation`

### 科技政策推演六叶（§1.1.1.1.4.2.3.2.1～.2.6 · 2026-08-08）

| coverage id | Bid 叶子 | 走查要点 | 状态 |
|-------------|---------|----------|------|
| `DS-POL-12-INTERPRET-01` | 政策文本智能解析 | 关键词 + **核心内容** + 战略意图 + 对象/条件/力度 | ✅ |
| `DS-POL-12-INTERPRET-02` | 政策重点可视化展示 | 导图含目标·领域·路径·资金；**点击节点**右侧详情 | ✅ |
| `DS-POL-12-INTERPRET-03` | 政策影响范围分析 | 受益对象；**区域地图叠柱**；行业；时间变化 | ✅ |
| `DS-POL-12-INTERPRET-04` | 政策关联分析 | 关联网络图 + 协同/体系位置说明；非 Nebula Banner | ✅ |
| `DS-POL-12-INTERPRET-05` | 政策实施路径预测 | Timeline 节点含日期与**责任主体** | ✅ |
| `DS-POL-12-INTERPRET-06` | 政策解读报告生成 | 四章预览；章节勾选；**Markdown/纯文本**下载；≠ PC-04 | ✅ |

- [x] C8～C12（PLAN-DS12 §验收）推演区六叶主路径可走查  
- [x] 诚实 Mock：无伪 NLP / 无 Nebula 直连 / 报告 ≠ PC-04

## 核增四页骨架（DS-PC-01~04）

| 菜单 | pageKey | leaf |
|------|---------|------|
| 政策数据治理 | policy-governance | DS-PC-01 |
| 智能政策拆解 | policy-parse | DS-PC-02 |
| 多维政策对比 | policy-compare-upgrade | DS-PC-03 |
| 智能研报生成 | policy-insight-report | DS-PC-04 |

- 实现：`PolicyPcPages.jsx` + `data.js` / `pageRouting.js` / `App.jsx`
- V1 处置：`feature_disabled_with_reason`（深度交互下一迭代；骨架可导航 + Steps 串联）
- 全景重点比对可 CTA 跳转至 DS-PC-03

## 人工确认

- [x] content_review / nav_smoke 通过（会话确认「通过」，2026-08-05）

## 返工修复（2026-08-05 晚）

- 问题：核增骨架黄条把内部处置码 `feature_disabled_with_reason` 直接展示给业务用户
- 修复：`PolicyPcPages.jsx` 改为「部分能力暂未开放（演示骨架）」+ 页级中文说明；蓝条标题按四页分轨；卡片文案改为「演示数据区 · Wave0 Mock」
- 处置码仅保留在 coverage yaml（`v1_treatment`），不再上屏

- 问题：核增页无内容壳，主内容从 left:0 叠到透明侧栏上（表现为「侵入菜单 / 侧栏背景消失」）
- 修复：新增 `PolicyPcPages.css`，根节点 `policy-pc-page` 对齐评价/推演壳（`margin-left: 268px` + 白底圆角卡片）

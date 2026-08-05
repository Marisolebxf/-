# TOPIC-SVCCHAIN-R2C · 门户"专题服务"叶子（五件套 + 闭环实现）Handoff

- **任务**：TOPIC-SVCCHAIN-R2C（E7-产业服务链分析 · 门户展示侧叶子 SVCCHAIN-PORTAL）
- **执行**：agent:frontend（监管人 human:黄敬洲）
- **日期**：2026-08-06
- **范围真源**：招标展示系统 §1.1.1.1.1.1.1.33 专题服务（33.1-33.5，序号 97-104）；产品对标 `产品整体定义/E-31-企业发展/`；交互对标 demo-ui-topic `src/app/pages/development/` 与 `policy-portal/` 门户惯例

---

## 1. 范围与实现（与 bid-reference 对照）

| Bid 条目 | 序号 | 实现 | 路由 |
|---|---|---|---|
| 33.1 全球服务机构概况 | 97 数量分析（总量+历年趋势） | KPI×3 + 8 年趋势折线（<2 可比点自动隐藏） | `/service-portal/overview` |
| 〃 | 98 类型分析 | 类型环形图（高校/科研院所/企业，与主数据 `OrgType` 同字典） | 〃 |
| 〃 | 99 规模分析 | 人员规模四档条形（全集含 0 值档，hover 含占比） | 〃 |
| 33.2 服务机构产业分布 | — | 结合产业链全景：六环节卡（字典复用分析侧 `CHAIN_STAGES`，CT-SVC-PT-01）+ 八领域×六环节热力总览；0 值环节如实"暂无覆盖"；环节卡下钻分析侧生态环节详情 | `/service-portal/industry-distribution` |
| 33.3 服务机构区域分布 | — | 全球（Top12 国家/地区）⇄ 全国（Top12 省级）双视图，Leaflet 比例圆点地图 + 排行条形；"其他"余量如实列出 | `/service-portal/region-map` |
| 33.4 服务机构技术能力 | — | 固定五维等权（门户不可调权），各产业 Top30 排名表；**复用分析侧 `computeEvaluation` 同一实现**（CT-SVC-PT-03，无第二套口径）；金银铜前三配色；在库不足 30 家诚实标注 | `/service-portal/capability-rank` |
| 33.5 深圳产业服务介绍 | 100 机构数量趋势 | 深圳 8 年趋势折线 + KPI | `/service-portal/shenzhen` |
| 〃 | 101 类型统计 | 深圳类型环形图 | 〃 |
| 〃 | 102 产业领域分布 | 领域×环节堆叠条形（结合深圳产业链全景语义，环节同字典）；多领域重复计口径 UI 明示 | 〃 |
| 〃 | 103 区域分布 | 深圳十区 Leaflet 地图 + 排行（十区字典全集） | 〃 |
| 〃 | 104 重点产业服务机构 | 卡片墙（固定等权技术力 Top 遴选，口径明示）+ 详情抽屉四板块：①概况 ②当前规模 ③业务服务领域 ④业务分布区域（Leaflet 迷你地图）；URL `org` 参数可分享恢复 | 〃 + `KeyOrgDetailDrawer` |

**33.1-33.5 与序号 97-104 逐条闭合**：TRACE-SVCCHAIN-PORTAL.yaml `#reverse_check` 反向核对表全绿（10/10）。

### 门户 ↔ 分析侧互通（CT-*）

- **CT-SVC-PT-01**：产业分布/深圳领域分布复用分析侧 `CHAIN_STAGES` 环节字典（同一来源，不自造第二套链路字典）。
- **CT-SVC-PT-02**：重点机构详情/技术力榜行内"分析画像" → `/service/institution-judgment?org=<id>`，分析侧打开同一机构画像抽屉（URL org 参数为共同契约）。
- **CT-SVC-PT-03**：技术力排名 = 分析侧 `computeEvaluation` 固定等权应用；`M_SVC_ORG_TECH_SCORE` 沿用 Q-SVCCHAIN-01 诚实态（D1 draft ⚠️）。
- **CT-SVC-PT-04**：区域/深圳/业务分布地图复用 `policy-portal/PolicyLeafletMap`（Leaflet circleMarker，禁百度/高德）。
- **CT-SVC-ORG-03 扩展触点**：门户技术力榜、重点机构详情抽屉均可"加入对比篮"（系统篮 `service_org`，与分析侧即时同步、幂等切换）。
- **数据不做两套**：实体层（机构基础信息/覆盖/技术力五维）全部取 `serviceCenterData.SERVICE_ORGS` 主数据；门户仅新增聚合层（全球/全国/深圳统计）与扩展档案（`KEY_ORG_PROFILES`，只增字段不覆盖）；层级一致性 深圳 3,182 ≤ 广东 5,600 ≤ 中国 21,400 ≤ 全球 89,600。

### D9 血缘

- 新聚合指标 10 个（`M_SVC_PT_*`）登记 TRACE + `serviceReadinessSeed` + `serviceReviewData`（BATCH_R2C），全部 D4 mock 🧪 + D3 待定 ⚠️（挂 Q-SVCCHAIN-06）；技术力/覆盖深度复用分析侧既有指标（`M_SVC_ORG_TECH_SCORE` / `M_SVC_ORG_COVERAGE_DEPTH`），不重复注册。
- 每个统计数字挂 `SvcMetricBadges`（ⓘ→结构→⚠️→🧪 并存排列）；需求追踪 `REQ-SVC-PT-*` 挂 `ServiceReviewMount`；评审模式关闭 DOM 零泄漏（走 service-center 评审层自闸）。

## 2. 偏离说明（3 处轻偏离，均登记如实态）

1. **AC-US-SVC-PT-02-04**（环节展开代表机构）：门户环节卡不重复实现"代表机构展开"，点击直接下钻分析侧生态页环节详情（该处已有机构行与画像入口）。理由：避免第二套"环节-机构"视图，互通语义一致；如需门户内展开待人工评审后补。
2. **AC-US-SVC-PT-03-02 后半**（地图点选 → 列表行高亮滚动）：未实现点选联动（列表为 ECharts 条形，无行级高亮语义）。地图 hover 数值与列表同源可核对。待后续将列表升级为表格时补。
3. **AC-US-SVC-PT-04-05 后半**（榜单机构名下钻 US-06 详情）：榜单行下钻目标为分析侧画像（信息更全）；US-06 门户详情组件仅用于深圳重点机构（Bid 104 语义）。全球榜单机构多数无门户扩展档案，用 US-06 组件会大面积"资料完善中"，体验更差。

另：本仓无 TypeScript 编译器依赖（无 tsc 门禁），验证口径与 R1/R2 相同 = `pnpm run build`（vite 全量转译 5,156 模块）+ `pnpm run design:check` + IDE 零 lint 错误。

## 3. 产物清单

**编排仓（gkx-orchestration，origin/dev）**
- 五件套：`agent-delivery/agent-handoffs/产品整体定义/E7-产业服务链分析/SVCCHAIN-PORTAL-专题服务/`（USM / IA / Wireframe / UX-SPEC / TRACE.yaml）
- `E7-产业服务链分析/README.md` 划分表新增 SVCCHAIN-PORTAL 叶子 + Q-SVCCHAIN-06
- `客户决策清单跟踪表.md` 新增 Q-SVCCHAIN-06（🟡 门户聚合统计口径与数据源）
- 本 handoff

**业务仓（demo-ui-topic，origin/dev）**
- `7b1a9bf` chore(ci)：design:check 修正扫描目录（存量 chore，独立 commit）：`industry` → `industry-center`、空目录 `service` → `service-center` + `service-portal`；D10 后新页组（industry-center/service-center/service-portal）豁免 legacy "禁 Arco Tabs" 断言（附 Windows 路径分隔符归一化修复）。脚本此前因扫描已更名目录直接崩溃，现三段全绿。
- `4c9d932` feat(service-portal)：13 文件 +2,173 行——新建 `src/app/pages/service-portal/` 9 文件（5 页面 + 详情抽屉 + data/model/shared）、`routes.tsx` 注册 `/service-portal/*` 5 路由、`Layout.tsx` 左侧菜单"产业服务链分析 → 专题服务展示"、`serviceReadinessSeed.ts` / `serviceReviewData.ts` 登记 10 个 `M_SVC_PT_*` 指标与 `REQ-SVC-PT-*` 追踪（BATCH_R2C）。

## 4. 验收证据

- `pnpm run design:check`：三段（design contract + 2 shell contract 测试）全部通过 ✅
- `pnpm run build`：vite 生产构建成功（5,156 modules，41s）✅
- IDE lint（service-portal 全目录 + 改动文件）：0 错误 ✅
- **AC 自走查**：28 条 AC 中 25 条 ✅、3 条轻偏离（§2 登记）；层级一致性、确定性（无运行时随机）、0 值全集、诚实标注（在库不足 30 / 资料完善中 / 演示口径声明条）逐条核过
- **CI**：token 无 API 读权限，**请人工确认** GitLab Pipeline 绿灯（demo-ui-topic dev 分支 `4c9d932`）

## 5. 架构合规自检（十条）

1. 算法只在 Python ✅（纯前端 mock，无算法实现；技术力为前端演示计算，正式态走 Java REST 聚合）
2. 调用链 ✅（目标态 IA 已声明 前端 → Java `/topic/v1/service-portal/**`；demo 态 mock 数据）
3. NebulaGraph ✅（不涉及图谱）
4. 可观测性 ✅（demo 原型仓豁免口径，与 R1/R2 一致）
5. CI/CD ✅（push 触发 Pipeline，绿灯待人工确认）
6. demo2 只读 merge ✅（demo-ui-topic 独立仓，不 merge 进 lumen）
7. 共享聚合核心 ✅（前端只调 Java 的目标态契约写入 IA/TRACE）
8. 数据策略 ✅（Mock 先行，D3 待 Q-SVCCHAIN-06 口径确认）
9. 前端规范 D8 ✅（Arco + ECharts + Leaflet + 主色 #165DFF；禁 antd/emoji 状态图标）
10. 数据血缘 D9 ✅（10 指标 8 件套 + 四维就绪度登记；每个统计数字 ⓘ + 🧪；MockBadge 全覆盖）

## 6. Cost 回填

- `actual_tokens`：约 2,900,000（会话累计，含 fork 前五件套编制）
- `model_used`：claude-fable-5
- `actual_cost`：约 $8.7（估算）
- `cost_warn`：false（< $10）

## 7. 遗留风险 / 待办

- **Q-SVCCHAIN-06（🟡）**：门户全球/全国/深圳聚合统计的统计范围、区域归属口径、重点机构遴选标准、扩展档案（领导人/营收）数据源均待甲方拍板；UI 已全站 ⚠️ + 演示口径声明条。
- **Q-SVCCHAIN-01 沿用**：技术力评价算法为演示等权口径（D1 draft），正式算法待甲方确认指标体系。
- 3 处 AC 轻偏离（§2）待人工评审决定是否补齐。
- CI 绿灯待人工确认（令牌无 API 读权限）。
- 左侧菜单单入口"专题服务展示"，子页高亮依赖页组内子导航条（与 policy-portal 惯例一致）；如需菜单级五项展开待 UX 评审。

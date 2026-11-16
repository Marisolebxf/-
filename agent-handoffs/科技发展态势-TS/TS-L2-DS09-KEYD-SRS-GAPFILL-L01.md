# 重点领域规划 · 五处需规缺失内容补齐（飞书 bug 7168838360 / 7169235515 / 7168756217 / 7169251013 / 7169246517）

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:zcode`（本机并行窗口之一，代 human:徐滕强） |
| supervised_by | 待用户确认（口头派单：修复我名下 bug，多窗口自动分工不重复） |
| claim_type | `pull`（无 registry 任务号；飞书 bug 五连，claim_id=claim-20261116-KEYD-zcode，5 个 bug 均已发 [agent-claim] 评论） |
| 分工边界 | 本窗口=重点领域规划 Tab（seq 185–190 五 bug）；另一窗口=综合发展规划模块（7168907585 已认领并建 fix/7168907585-push-field-options 分支，7168946128 样式 bug 与其同文件同模块留归该窗口） |

## 范围与实现（对照需规 seq 185–190）

全部为 **FE 确定性派生**，数据源 = `GET /display/v1/situation/planning/key-areas` 现有块（clusters / carriers / carrier_types / district_baselines / land_use / plans），**不动 Java / ADS / DDL**，不新增接口不写库不造数（G-B4 / D18）。

| bug | 需规 seq | 缺失内容 | 实现 |
|-----|---------|---------|------|
| 7168838360 | 185 | 空间密度分析和集聚度评估 | 空间布局分析卡（地图下方）新增双列面板：①空间密度分析——区县载体规模条（district_baselines.total_carriers 派生：相对密度指数 18-100 + 占比%）；②集聚度评估——首位集聚区/TOP1 集中度/CR2/区载体总量 + 集聚等级 tag（CR2≥50 高度集聚 / ≥40 中度集聚 / 其余 相对均衡，确定性规则），面板带演示口径注记 |
| 7169235515 | 187 | 查看土地利用类型、创新产出效益｜提供利用效率评估和优化建议 | 土地效益卡新增：①土地利用类型汇总 chip（land_use.land_type 聚合：块数/面积/占比/平均效率）；②保留效益柱状图（创新产出效益承载）；③利用效率评估（good/medium/poor 状态分布，中文映射按 DDL 注释归 FE）；④优化建议（按效率状态的规则文案，标注「按效率状态规则生成，非规划文本」） |
| 7168756217 | 188 | 提供载体详细信息和创新活动分析 | ①载体详情 Modal：列表行与地图点位点击同开（handleCarrierRowClick 复用），字段=类型/区域/能级/所属集群（cluster_id 派生，7 行未挂集群显「—」诚实空）/服务能力/资源重点；②创新活动能级分析面板：能级构成 + 类型构成 + 领军载体（国家级）名单，carriers 表行按当前筛选现算 |
| 7169251013 | 189 | 产业大门类、科技领域细分｜技术规模、技术发展状态、领军主题 | ①集群导航升级两级：industry_category 大门类分组标签 × 集群按钮（副行显「领域细分：technologyField」）；②联动画像面板：技术规模（载体数/覆盖区县）/技术发展状态（能级构成表征）/领军主题（领域 + 国家级载体名单，用 DDL 注明的 189 承载列 technology_field / carriers.level） |
| 7169246517 | 190 | 资源投入建议、空间布局优化方案 | 「查看建议」弹窗新增两节：①资源投入建议（行动清单 = plans.actions 表行 + 资源缺口口径注记）；②空间布局优化方案（clusters × carriers 空间分布派生行：集群/领域/载体数/覆盖区县 + 方案主题以 plans 表行为准） |

## 偏离说明

- 「技术发展状态」「创新活动分析」无专列数据源（185/187/188 判定 other_system、189 n/a_ops）：以载体能级/类型构成**表征**并在面板标注演示口径，未挂任何 metric_id、未造数；正式态由 GIS/ADS 图层读数替换（与 U8-2 land_benefit 诚实空同思路）。
- 187 优化建议为按 status 的**规则文案**（非表行、非模型输出），已注明；不改挂 seq 190（遵守需规对照文档禁令）。
- 189 需规「地图呈现技术在城市内空间分布」已有承载（集群选中即过滤地图点位，filterCarrierLocations 存量逻辑），本次未改。

## 产物清单

| 仓 | 分支 | commit | 文件 |
|----|------|--------|------|
| lumen-ui-science-pc | `fix/7168838360-keyareas-srs-gapfill`（worktree `D:/gkx-lumen/wt/keyareas-srs-gapfill`，基于 origin/dev 64556f9） | `5f80f23` | models/techDevelopmentPlanModel.ts（+222 派生构造器）、tabs/KeyAreaTab.vue（+241/-17）、styles/demo-tech-development-plan.css（+262）、techDevelopmentPlan.test.mjs（+41 断言） |

未 push：按工作区铁律（任何 push 前须用户确认），本地验证完成后停在待授权状态。

## 验收证据

- `node --experimental-strip-types src/views/situation/tech-development-plan/techDevelopmentPlan.test.mjs` ✅（含新增「重点领域需规缺失补齐」断言组）
- `npm run type-check`（vue-tsc --build）✅ 零错误
- `npm run build`（type-check + vite build）✅ 1m49s built（chunk 体积告警为存量）
- `npx eslint`（本改动 4 文件）✅ 零错误（顺手移除 dev 存量未使用导入 buildCarrierPopupHtml；lint --fix 误触的 knowledge-graph 两文件已还原）
- 线上目测路径：科技发展态势 → 科技发展规划 → 重点领域规划页签（待 push + CI rollout 后按《接口说明与需规对照》§五验收）

## 架构合规自检（宪法 §2 逐条）

- D7/D12 调用链：✅ 仅 FE 渲染层，未调任何 demo-* / 未越层
- D8 前端栈：✅ Arco 组件（a-tag/a-modal/a-card/a-select）+ 既有 tzp-* 样式体系扩展
- D9 数据血缘：✅ 未新增统计指标；派生量均标注演示口径、不挂 metric_id（other_system/n_a_ops 叶无统计核，DDL 注释明示 NULL）
- D16/D18/G-B4：✅ 不建 gapfill 表、接口不动、无写死 mock 注入；派生公式确定性可复算
- §3 人机协作：✅ commit 带 [agent:zcode]；push 待用户授权；本 handoff 即 DoD 交付

## 后续

1. 用户授权后 push 分支（或按需拆 per-bug 分支），CI 绿后 K8s dev rollout；
2. 飞书 5 个 bug 回复验证路径与 commit 号，转验收（验收口径=bug 标题所列需规缺失项逐条可见）；
3. 若验收要求 187 建议文案表行化（模板行方案，同 195/196 先例），再立数据侧小单（Java 加列 + 灌数），本 FE 结构无需变动（LAND_STATUS_ADVICE 单点替换）。

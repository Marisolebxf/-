# TOPIC-STRAT-R4 · 专题战略分析重跑总收口（E7 产业服务链 + E8 综合智能分析）

- **任务**：TOPIC-STRAT-R4（crosscut / tech_task），Epic E7-产业服务链分析
- **执行**：agent:frontend（监管/认领 human:淮政玮），2026-08-06
- **性质**：集成验证与总收口，无新叶子开发；本批仅修订 1 份 USM 措辞 + 产出覆盖矩阵与本 handoff

## 1. 批次总览（R1~R4）

| 批次 | registry 任务 | 范围 | 业务仓 commit | AC 自走查 |
|---|---|---|---|---|
| R1 打样 | TOPIC-SVCCHAIN-R1 | 服务机构分析域（7.1-7.3，6 项） | `9825411` | 32/32 ✅（用户确认打样达标） |
| R2 | TOPIC-SVCCHAIN-R2 | 服务链生态（7.4/7.5/7.8）+ 招引培育（7.6/7.7），10 项 | `284b681`（+`acf7f42` pnpm v11 迁移） | 28/28 + 21/21 ✅ |
| R2B | TOPIC-SVCCHAIN-R2B | 检索对齐企业模式 + 对比篮（用户追加口径一） | 同 `284b681` | 13/13 ✅（其中 AC-08-01 经 R4 复核加修订注，见 §3.4） |
| R2C | TOPIC-SVCCHAIN-R2C | 门户专题服务（33.1-33.5 / 序号 97-104，用户追加口径二） | `7b1a9bf` + `4c9d932` | 25/28 ✅ + 3 轻偏离（§3.1-3.3） |
| R3 | TOPIC-SYNTH-R3 | 综合智能分析（8.1-8.3，9 项） | `905da04` | 34/34 ✅ |
| R4 | TOPIC-STRAT-R4 | E2E 走查 + 覆盖矩阵 + 开放项核对 + 总收口 | 无代码改动 | — |

**AC 总计 156 条：152 ✅ + 4 条轻偏离登记**（R2C 3 条 + R4 复核新增 1 条，全部有维持理由与文档对齐，见 §3）。

## 2. R4 全链路 E2E 走查结论（静态代码核对）

**通过项**：
- 路由：13 条业务路由全部挂真实组件（service-center/search、service/* 3 页、service-portal/* 5 页、intelligence/* 3 页），8 条旧路径均为重定向；左侧菜单两组入口齐全（产业服务链分析 5 项、综合智能分析 3 项）。
- 旧组件残留：`ServiceChainAnalysis` / `ServiceInstitutionJudgment` / `ServiceInstitutionDecision` 全仓零引用。
- 对比篮：`ServiceOrgBasketButton` 直接触点 7 处（检索行、画像抽屉、图谱环节详情、培育名单行 ×2、门户榜单行、门户详情抽屉）；`service_org` 类型已注册 `SystemCompareBasketLayer`；分发经 `serviceAnalysisRegistry` 到 R1 评估页（`source=compare-basket`）+ `ServiceOrgCompareBasketPanel` 回跳，**全仓无第二套对比入口**。
- 13 条 CT-* 契约逐条代码核实：CT-SVC-ORG-01~04、CT-SVC-ECO-01/02、CT-SVC-PT-01~04、CT-SVC-ORG-03-EXT、CT-SYN-01~03。关键点：门户/协同图谱下钻 `/service/institution-judgment?org=` 参数契约一致；协同图谱企业节点 → `/enterprise-center/profile/:enterpriseCode`（路由存在）；门户 Top30 复用 `computeEvaluation`、环节字典单源 `CHAIN_STAGES`、地图容器复用 `PolicyLeafletMap`；协同报告走系统报告面。
- 主数据单源：`SERVICE_ORGS` 被 service-center / service-portal / intelligence 三域共用（含协同图谱机构节点），门户只加聚合层；数量层级一致（深圳 3,182 ≤ 广东 5,600 ≤ 全球 89,600；领域合计 5,030 ≥ 机构数口径已在 UI 明示）。
- 共享文件连续修改（routes.tsx / Layout 菜单 / 系统篮 / seeds）经 R2→R2C→R3 无覆盖断链。
- D9：`serviceReadinessSeed`（34 处注册）+ `intelReadinessSeed`（19 处）+ 两域 ReviewMount 挂载在位；`M_SVC_ORG_* / M_SVC_PT_* / M_SYNTH_*` 页面消费与种子一致。
- localStorage 前缀：`topic-svc-workbench` / `topic-svc-eco` / `topic-svc-recommend` / `topic-svc-portal-*` / `topic-synth-workbench` + 系统篮统一存储，域间独立。

**发现并处理**：仅 1 处（§3.4，文档措辞与实现不一致，已修订 USM，不动代码）。

## 3. 轻偏离复核结论（4 条，全部维持）

1. **R2C-1 环节代表机构改下钻分析侧**：维持。避免门户复制机构列表造成两处维护，符合主数据单源原则。
2. **R2C-2 地图点选联动未做**：维持。`PolicyLeafletMap` 为跨模块通用容器（政策门户共用），加点选回调的回归风险大于收益；如确需可另开独立小单。
3. **R2C-3 榜单下钻指向分析侧画像**：维持。此即 CT-SVC-PT-02 契约行为，非缺陷。
4. **R4 新增：R1 集合/覆盖视图无行内入篮按钮**：入篮经"行头开画像抽屉→抽屉内入篮"一跳承接，路径可达、状态跨页一致。维持实现，已修订 `USM-SVCCHAIN-ORG-ANALYSIS.md`（主路径触点清单 + AC-08-01 修订注）对齐。

## 4. 覆盖矩阵结论

见《产品整体定义/coverage-matrix-E7E8-专题战略分析重跑.md》：**36 行（§2.4.2.7 十六项 + §2.4.2.8 九项 + 门户 §33 十一行）全闭合，无遗漏、无双重归属**，与六份 TRACE 反向一致。状态分布：closed 9 / 演示态 🧪 18 / 口径待定 ❓ 9。

## 5. 开放项九项表（与《客户决策清单跟踪表》253-261 行核对一致，无漏项）

| 编号 | 主题 | 临时默认 | 影响面 | 闸门 |
|---|---|---|---|---|
| Q-SVCCHAIN-01 | 技术力评价模型定义卡 | 最大值归一×用户权重（🧪） | R1 评估 + 门户 Top30 | **上线闸门** |
| Q-SVCCHAIN-02 | 深度得分/热度评级口径 | 强度归一 + 演示分档 | R1 覆盖/趋势 | **上线闸门** |
| Q-SVCCHAIN-03 | 瓶颈识别/生态影响力 | 机构数+深度阈值演示规则 | R2 短板/图谱 | **上线闸门** |
| Q-SVCCHAIN-04 | 深圳统一评价框架+城市基准数据源 | 三指标演示框架 | R2 深圳现状 | **上线闸门**（数据源需甲方指定） |
| Q-SVCCHAIN-05 | 招引/培育模型口径 | 加权求和+建议标签 | R2 推荐名单 | **上线闸门**（名单不作对外承诺） |
| Q-SVCCHAIN-06 | 门户统计口径与全球/全国数据源 | 确定性聚合数据集 | R2C 门户五页 | **上线闸门**（落地切 Java REST） |
| Q-SYNTH-01 | 活力指数模型 | 四维等权演示合成 | R3 活力页 | **上线闸门** |
| Q-SYNTH-02 | 要素评价与影响关联 | 四维等权+占比推导 | R3 要素页 | **上线闸门** |
| Q-SYNTH-03 | 协同度与效果评估 | 密度×强度演示合成 | R3 协同页 | **上线闸门** |

全部 🟡，责任人：算法定义卡族=唐绍祖 + 甲方确认；数据源族=数据 Lead + 甲方指定。

## 6. CI 状态

- 本地佐证：R4 全量 `pnpm run build` 绿（5,165 模块，exit 0，仅 chunk 体积历史告警）；`design:check` 于 R2C/R3 批全绿且本批无代码改动。
- 远端：令牌无 GitLab API 读权限，**R1~R3 各批 dev pipeline（commit `9825411` / `284b681` / `7b1a9bf` / `4c9d932` / `905da04`）+ 本批编排仓推送后的绿灯请人工在 GitLab 页面确认**；`git ls-remote` 已确认业务仓远端 HEAD 与本地一致（见 §8 验证记录）。

## 7. 架构合规十条自检

1 算法只在 Python：✅ 纯前端 demo，演示算法均 🧪 标注且登记 Q-*；2 调用链：✅ 无越层（mock 层预留 Java REST 切换：Q-SVCCHAIN-06 备注）；3 图谱：✅ 未引入 Neo4j（EChart graph/ForceGraph 前端渲染）；4 可观测：✅ demo 仓沿用现状；5 CI/CD：✅ push 触发 pipeline；6 demo2 只读 merge：✅ 不涉及；7 共享聚合核心：✅ 前端只造 mock 不造后端；8 数据策略：✅ mock 先行 + 单源主数据；9 前端规范：✅ Arco + ECharts + Leaflet，design:check 门禁；10 数据血缘：✅ 全部统计数字 ⓘ+metric_id+就绪度角标，D1 missing 红问号诚实态。

## 8. 演示准备指引

- 干净环境：清除 localStorage 前缀 `topic-svc-`（workbench/eco/recommend/portal-*）、`topic-synth-workbench`、系统对比篮存储（含 `service_org` 类型）；企业/政策篮如需一并清理按系统篮统一 key。
- 推荐演示动线：门户专题服务（`/service-portal/overview` 五页）→ 重点机构详情 → 进入分析侧画像 → 服务机构查询/入篮 → 技术力对比（对比篮分发）→ 服务链生态（短板/图谱）→ 招引培育名单 → 综合智能分析（活力 → 要素下钻 → 协同图谱 → 机构/企业节点跨模块下钻）。
- 验证记录：R4 `git ls-remote` 业务仓 origin/dev == 本地 `905da04`；两仓 status 干净后收口提交。

## 9. registry 终态

TOPIC-SVCCHAIN-R1 / R2 / R2B / R2C / TOPIC-SYNTH-R3 = `integration`（evidence/cost 齐备）；TOPIC-STRAT-R4 = 本批收口后推 `integration`。后续人工节点：QA 领测（pending_test→testing）→ 淮政玮 `ready_to_sign → done` 签收。

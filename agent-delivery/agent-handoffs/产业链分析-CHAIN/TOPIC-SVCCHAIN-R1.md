# TOPIC-SVCCHAIN-R1 · 产业服务链 R1 打样 — 服务机构分析域（五件套 + 闭环重实现）Handoff

> **任务**：TOPIC-SVCCHAIN-R1（E7-产业服务链分析 · P1 打样批）
> **执行**：agent:frontend ｜ **监管**：human:淮政玮
> **日期**：2026-08-05
> **状态**：integration（等待用户确认打样质量后放行 R2）

---

## 1. 范围与实现（对照 bid-reference）

范围真源：`agent-delivery/bid-reference/科技信息展示系统和科技专题服务系统.md` §1.1.1.2.4.2.7.1–7.3，共 **6 个三级项**，逐条闭合：

| # | 招标三级项 | 落点 | 结论 |
| --- | --- | --- | --- |
| 7.1.1 | 服务机构产业领域覆盖分析 | US-01（机构集合确认）+ US-02（广度=覆盖领域数 / 深度=服务深度得分） | ✅ |
| 7.1.2 | 领域分析结果呈现（矩阵图/热力图） | US-02：热力图（机构×领域，五档色阶）↔ 矩阵图（X=广度整数刻度，Y=平均深度，四象限标注）双图型切换持久化 | ✅ |
| 7.2.1 | 新增趋势可视化呈现 | US-04：主领域+最多 2 对比领域折线，时间窗近 3/5/8 年持久化，明细表可下钻 | ✅ |
| 7.2.2 | 市场热度判断 | US-05：斜率/波动特征 → 热度星级+依据行（引用图上真实数值）；算法未定 → D1 missing 诚实态 | ✅（演示口径，Q-SVCCHAIN-02） |
| 7.3.1 | 多维度评价模型 | US-06：内置五维（专利/研发投入/核心专家/成功案例/标准制定，与招标列举一致）+ 自定义维度，启停/调权/归一 | ✅（演示口径，Q-SVCCHAIN-01） |
| 7.3.2 | 自定义对比分析 | US-06：2~5 家机构横向对比，排名列表 ↔ 每机构雷达图，配置持久化、结果确定性可复现 | ✅ |

范围外（README 已注明模块划分）：7.4/7.5/7.8（链路生态域）与 7.6/7.7（招引培育域）归 R2 两叶子。

## 2. 产物清单

### 2.1 五件套（编排仓 `agent-delivery/agent-handoffs/产品整体定义/E7-产业服务链分析/`）

| 文件 | 说明 |
| --- | --- |
| `README.md` | E7 模块划分（7.1-7.3 本叶子 / 7.4-7.8 R2 两叶子）、开放项索引 |
| `SVCCHAIN-ORG-ANALYSIS-服务机构分析/USM-SVCCHAIN-ORG-ANALYSIS.md` | 6 故事（US-01~06），主路径/异常表/AC 共 32 条，粒度对齐 E2 CHAIN-TOPIC-PANORAMA |
| `.../IA-SVCCHAIN-ORG-ANALYSIS.md` | 稳定 ID、IA 结构、URL 契约（`field`/`tab`/`org`）、Frame 职责、复用契约 |
| `.../Wireframe-SVCCHAIN-ORG-ANALYSIS.md` | F-SVC-01~05 骨架：上下文条/选择器/覆盖/趋势/评估/画像抽屉 |
| `.../UX-SPEC-SVCCHAIN-ORG-ANALYSIS.md` | 旅程、状态机、错误恢复、键盘可达、持久化契约（`topic-svc-`）、ReviewMode 集成 |
| `.../TRACE-SVCCHAIN-ORG-ANALYSIS.yaml` | 6 项需求→故事→Frame→实现正反向核对、指标注册、Q-SVCCHAIN-01/02、跨模块契约 |

### 2.2 实现（业务仓 `demo-ui-topic`，commit `9825411`，origin/dev）

17 文件变更（+3025 / −1814），新增 `src/app/pages/service-center/` 域：

| 文件 | 职责 |
| --- | --- |
| `serviceCenterData.ts` | 领域字典/机构库/维度定义/趋势序列确定性 mock + 广度深度计算 |
| `serviceCenterStore.ts` | reducer + localStorage（前缀 `topic-svc-`，版本化，损坏回落默认+提示） |
| `serviceCenterModel.ts` | 评估计算（归一×权重）、热度判读（斜率/波动分档）、覆盖结论生成（🧪 演示态） |
| `serviceReviewData.ts` / `serviceReadinessSeed.ts` | D9 指标 8 件套镜像 + 四维就绪度种子 |
| `ServiceReviewMount.tsx` / `SvcMetricBadges.tsx` | 评审层门控（reviewMode 自闸，业务态零泄漏） |
| `OrgPickerModal.tsx` | 机构选择器：类型分组/关键词/单类与全量全选/清空/取消不半提交 |
| `OrgProfileDrawer.tsx` | 机构画像抽屉：基本信息/覆盖细分/技术力五维/近三年记录/加入集合 |
| `CoverageView.tsx` | 覆盖分析：热力↔矩阵切换、行头与气泡下钻、无覆盖机构诚实空态 |
| `TrendView.tsx` | 趋势：≤3 曲线、时间窗、最后一条曲线不可关、明细表下钻 |
| `CapabilityView.tsx` | 评估：五维+自定义维度、权重校验/一键归一、2~5 家、排名↔雷达 |
| `ServiceOrgAnalysisPage.tsx` | 页面壳：URL 同步（`field`/`tab`/`org`）、指标条、空态引导 |
| `routes.tsx` / `Layout.tsx` | 路由替换旧 `ServiceInstitutionJudgment` → 新页，导航更名"服务机构分析" |
| `service/ServiceInstitutionJudgment.tsx` | **删除**（旧粗糙实现） |

### 2.3 决策登记

`客户决策清单跟踪表.md` 新增 **Q-SVCCHAIN-01**（技术力模型算法定义卡缺失）、**Q-SVCCHAIN-02**（深度得分/热度评级口径未定），均 🟡 待算法 Lead + 甲方。

## 3. AC-US 自走查（32/32 通过）

| 故事 | AC | 结果 | 走查要点 |
| --- | --- | --- | --- |
| US-01 | 01-01 | ✅ | 选择器分组/搜索/单类全选/全选所有/清空，Tag 与勾选一致（`OrgPickerModal.tsx`） |
| | 01-02 | ✅ | 集合/领域/页签 localStorage 持久化，刷新保留（`serviceCenterStore.ts` persist） |
| | 01-03 | ✅ | URL `field`+`tab` 直达恢复，不回落默认（`ServiceOrgAnalysisPage` URL 初始化优先级） |
| | 01-04 | ✅ | 空集合三视图 Empty+“去选择机构”引导，不渲染空坐标轴 |
| | 01-05 | ✅ | 取消保留确认前集合；确认为唯一提交点（pending 态隔离） |
| US-02 | 02-01 | ✅ | 热力行=已选、列=字典全集、五档 piecewise 色阶=图例，hover 一致 |
| | 02-02 | ✅ | 矩阵 X 整数刻度/Y 0-100，四象限 graphic 标注，气泡可点 |
| | 02-03 | ✅ | 图型切换持久化，集合与领域不丢 |
| | 02-04 | ✅ | 深度 ⓘ `M_SVC_ORG_COVERAGE_DEPTH`（draft ⚠️）+🧪；广度挂 `M_SVC_ORG_COVERAGE_BREADTH` |
| | 02-05 | ✅ | 结论区 🧪，数值来自当前 covered 计算结果 |
| | 02-06 | ✅ | 无覆盖机构走 Alert 名单，不参与 TOP 排名 |
| US-03 | 03-01 | ✅ | 三视图（热力行头/矩阵气泡/趋势明细/评估排名+雷达）下钻同一 `OrgProfileDrawer` |
| | 03-02 | ✅ | `org` 参数分享恢复；关闭移除参数 |
| | 03-03 | ✅ | Drawer 不重载主体，页签/筛选/集合不变 |
| | 03-04 | ✅ | “加入集合”仅集合外显示，加入即重算+持久化 |
| | 03-05 | ✅ | 五维数字 ⓘ（TECH_SCORE draft ⚠️）+🧪 |
| US-04 | 04-01 | ✅ | ≤3 曲线，超限 placeholder 提示"最多 3 个领域"且选择器禁用 |
| | 04-02 | ✅ | 时间窗 3/5/8 年切换同步 X 轴，持久化 |
| | 04-03 | ✅ | 新增数量挂 `M_SVC_ORG_NEW_COUNT` ⓘ+🧪 |
| | 04-04 | ✅ | 图例开关仅可见性；最后一条禁关（title 提示"至少保留一条曲线"） |
| | 04-05 | ✅ | 明细表机构名下钻抽屉 |
| US-05 | 05-01 | ✅ | 热度评级 `M_SVC_ORG_MARKET_HEAT` D1 missing 红问号，评审模式只显 GAP/Q-SVCCHAIN-02 引用 |
| | 05-02 | ✅ | 每条研判带"依据"行，数值取自当前序列 |
| | 05-03 | ✅ | <3 年数据 / 全 0 → 诚实空态文案，不输出伪评级 |
| | 05-04 | ✅ | 领域/时间窗切换研判同步重算（useMemo 依赖） |
| | 05-05 | ✅ | 业务态无 metric_id/Q 编号泄漏，保留"演示口径"用户可读声明 |
| US-06 | 06-01 | ✅ | 内置五维与招标 7.3.1 列举一致，可启停/调权 |
| | 06-02 | ✅ | 三类前置禁用+解释；提供"按比例归一到 100%" |
| | 06-03 | ✅ | 综合得分 ⓘ（TECH_SCORE draft ⚠️ Q-SVCCHAIN-01）+🧪；排名与雷达同一次计算 |
| | 06-04 | ✅ | 雷达轴=启用维度动态一致 |
| | 06-05 | ✅ | 配置全持久化；确定性 mock 保证复现（evaluated fingerprint 一致校验） |
| | 06-06 | ✅ | 结论区 🧪，机构名/得分与本次评估一致 |

## 4. 架构合规自检（十条）

1. 算法只在 Python：✅ 纯前端 mock 演示，无算法实现；评估/热度均标演示态并登记 Q。
2. 调用链：✅ 无后端调用；正式接入按 IA §数据边界走 Java REST。
3. 图谱：✅ 不涉及。
4. 可观测性：✅ 沿用本仓既有接入，无变更。
5. CI/CD：✅ push origin/dev 触发流水线（本地 vite build 绿；远端状态见 §5）。
6. demo2 只读 merge：✅ 未触碰 lumen 仓。
7. 共享聚合核心：✅ 不涉及 Java 变更。
8. 数据策略：✅ 全 mock 确定性数据 + 🧪 标识。
9. 前端规范（D8）：✅ Arco React + ECharts，主色 `#165DFF`，Arco Icon 表状态、无 emoji 状态位。
10. 数据血缘（D9）：✅ 8 指标注册（`M_SVC_ORG_*`），ⓘ+metric_id+四维就绪度角标走本仓评审层；TECH_SCORE/COVERAGE_DEPTH D1 draft ⚠️、MARKET_HEAT D1 missing 红问号，禁止伪闭合。

## 5. 验收证据

- 业务仓 commit：`9825411`（`2847e82..9825411`，origin/dev），17 文件 +3025/−1814，`[agent:frontend]`。
- 本地验证：`vite build` 通过（exit 0，两次复验）；改动文件 lint 0 错。本仓 `package.json` 无独立 tsc/type-check 脚本，类型门禁以 build + lint 为准。
- 远端 CI：push 已触发；当前会话令牌无 GitLab API 读权限，流水线绿灯待人工/后续确认（历史该仓 dev push 流水线均绿）。
- 决策登记：`客户决策清单跟踪表.md` Q-SVCCHAIN-01/02。

## 6. 遗留风险与开放项

| 项 | 说明 | 去向 |
| --- | --- | --- |
| Q-SVCCHAIN-01 | 技术力评价模型无算法定义卡（维度口径/归一化/默认权重），现为"对比集合内最大值归一×用户权重"演示规则 | 待算法 Lead（唐绍祖）定义卡 + 甲方确认；落地前禁止对外决策展示 |
| Q-SVCCHAIN-02 | 服务深度得分与热度评级判读口径未定 | 同上；MARKET_HEAT 保持 D1 missing |
| CI 绿灯确认 | 令牌无 API 权限，远端流水线状态未即时核验 | 监管人 GitLab 页面确认或下批次补验 |
| 机构↔企业库实体互认 | 无稳定主数据映射，画像抽屉未做跨库跳转（USM"不包含"已声明） | R2 链路生态域评估是否需要 |

## 7. Cost（已回填 registry）

| 字段 | 值 |
| --- | --- |
| actual_tokens | ~2,600,000 |
| model_used | claude-fable-5 |
| actual_cost | ~$7.8 |
| cost_warn | false |

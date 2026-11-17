# FE-TOPIC-SMALL-ENT-L01 · 专题小屏企业维 — 深耕批 E：企业分析 PC↔Mobile 差距整改（2026-11-17）

> 认领：human:孔东（延续 FE-TOPIC-SMALL-ENT-L01 认领，批 A–D 已入库）
> 范围来源：2026-11-17 会话对照清单（lumen-ui-topic vs lumen-ui-topic-mobile 企业分析大模块：评估/风险/招引/详情/类型/领域/深圳现状）
> 用户裁定（2026-11-17）：D9 角标铺满不做；CMS 未适配汇总到「专题内容管理」大模块需求；PDF 直下与 G6 图谱记为进阶版优化
> ponytail: full

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `human:孔东` |
| supervised_by | `human:孔东` |
| claim_type | `pull` |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | N/A（前端视图/接线批，无存储流/调用链图改动） |
| 图 diff | 无 |
| 会签态 | N/A |

## 问题清单

对照 PC 仓 `lumen-ui-topic` 企业分析大模块，小屏存在两类缺口：

**正确性缺陷（P0）**
1. `useMobileAsyncAnalysis.ts` 轮询定长 30 次 × 400ms ≈ 12s：真实 LLM 任务（30–120s）在 `USE_MOCK=false` 下必假超时「分析超时」
2. 三异步分析视图（评估/风险/招引）运行中不可取消；无历史任务入口（`analysisTaskList`/`analysisTaskCancel`/`analysisTaskDelete` API 已有但 UI 未接）

**功能缺口（P1）**
3. 评估指标写死本地 `EVALUATION_MODES`，PC 侧 `entEvalIndicators`（#114 指标树动态目录）未接
4. 详情页仅 4 Tab，PC `EnterpriseProfileTabPanel` 有资讯/风险（`risk/all`）/招投标/供应链 4 类明细
5. 类型分析缺区域维度筛选与区域洞察联动
6. 领域分析缺参与深度矩阵（#128 `domain-matrix`，Q013 口径）
7. 深圳现状多城对标仅平铺列表，无雷达图
8. 风险痛难点结果平铺 ListCard，PC 侧按四维分组卡 + severity 强调 + readablePainText 文案治理

## 修改内容

### 批次 1（P0 正确性）
- **P0-1 轮询重构** `composables/useMobileAsyncAnalysis.ts`：删定长循环 → 指数退避（1s 起 ×1.4 封顶 5s）+ 5 分钟预算 + `pollToken` 令牌中止（取消/切页/销毁静默退出）；超时文案引导「最近分析」；`resolveTaskResultData` 支持大结果资产（`resultData` 空走 `fetchAnalysisAssetJson`）
- **P0-2 最近分析** 新组件 `components/AnalysisHistorySheet.vue`：底部弹层，按 `analysisType+subType` 过滤，成功任务回放（`restoreTask`）/删除（`analysisTaskDelete` 软删）/新建；三视图 header 挂入口
- **P0-3 运行态取消** 三视图 running 阶段「取消分析」按钮 → `analysisTaskCancel`（失败不阻断复位）

### 批次 2（P1 功能缺口）
- **P1-4 指标目录动态化**：`evaluation.ts` 补 `entEvalIndicators`（POST `/topicAsync/topic/v1/evaluation/indicators`，对齐 PC）；`config/enterpriseEvaluation.ts` 补 `flattenEvalIndicators`/`mergeCatalogIntoModeIndicators`（语义对齐 PC helpers：sub_types 选树、权重归一 100、known-key 过滤、available/data_status 解析）；视图 `loadCatalog` 失败回退本地权威定义；mock 由本地定义生成目录
- **P1-5 详情页 4→7 Tab**：新增资讯（分页 van-list）/风险（`entProfileRiskAll` 分组计数 + 最新事项拍平）/招投标（分页）Tab；供应链独立（`entProfileSupplyChain` 端点优先，panorama 兜底）；`PageTabs.vue` 改横滚适配 >4 Tab；mock 补 risk-all/supply-chain
- **P1-6 痛难点维度分组**：新 `utils/riskPainMap.ts`（对齐 PC `parsePainIssues`+`readablePainText`：PAIN_DIM 映射、蛇形字段改中文/不展示、DWD token 剥离）；风险视图按四维分组卡 + severity 左边条（高红/中橙/低蓝）+ 证据/成因/最佳实践/改进方向四格；无结构化数据回退平铺
- **P1-7 类型分析区域维度**：`keyAnalysisParams.ts` 补 `SZ_DISTRICT_OPTIONS`（6 区码表对齐 fixtures）+ `buildKeyAnalysisCommonRequest` 支持 regionId（区级 region_level）；composable 加 `regionCode` 状态联动 KPI/洞察/清单；视图区选择 chip + 选中区洞察卡（企业数 + 类型 tag）；mock `resolveKeyAnalysisRecords` 支持区级过滤、`regionInsight` 回显请求 region
- **P1-8 领域深度矩阵**：`keyAnalysis.ts` 补 `entKeyAnalysisDomainMatrix`；视图 CSS grid（首列 sticky 横滚），格值 = 参与深度 0–100、透明度映射（`rgba(22,93,255,α)`），Q013 口径注释保留；mock 按 buildDomainList 证据数归一
- **P1-9 深圳多城雷达**：`cityRadarOption`（技术力/企业密度/完整度三轴，含全国基准行），列表保留作明细；280px 高度适配底部 legend

## 明确不做（用户裁定 2026-11-17）

| 项 | 依据 |
|---|---|
| D9 角标铺满 | 用户裁定「不补角标」 |
| CMS 未适配 | 汇总到「专题内容管理」大模块需求统一处理 |
| PDF 直下 / G6 图谱 | 用户裁定记为进阶版优化（后续批次） |

## 测试结果

- `npm run type-check` exit 0（修 4 处类型错：矩阵类型导入、`:key` null 收窄、peer_regions 可空）
- `npm test` **72/72 pass**（含新增 `scripts/enterprise-gap-remediation.test.mjs` 10 项防漏断言：轮询不回归定长、三视图历史+取消、指标目录接线、7 Tab、维度分组、区域/矩阵/雷达接线、Sheet 回放/删除）
- `npm run build` exit 0（12.39s；chunk >500kB 警告为存量提示）

## 遗留风险

- 风险/招引视图的「最近分析」恢复回放按 `analysisType+subType` 过滤，`analysisTaskList` 后端须支持 subType 过滤参数（类型中已声明，联调时确认）
- 痛难点分组渲染依赖后端 issues[] 带 dimension/priority 字段；缺失时回退平铺（不阻塞）
- `domain-matrix` 真源端点 Q013 口径 participation_depth 0–1，雷达/矩阵归一阈值以联调实测为准
- PDF 直下 / G6 图谱未做（裁定进阶版）；风险多级图谱仍引导 PC 端

## 架构合规自检

- ✅ 调用链：新端点全经 `gkxlumen-platform-gateway`（`/api → topicAsync/topic/v1` 与 `enterprise/topic/v1`），无越层、无直连 demo-*
- ✅ D12：未 merge demo 代码，PC 仓只读对照后按 Vant/Vue3 重写
- ✅ Mock 开关：新端点全走 defineApi + registerApiMock；USE_MOCK=false 零 fixture 渲染（防漏断言覆盖）
- ✅ 无新增依赖（Vant/ECharts/现有工具复用）
- ✅ 多会话保护：commit 前逐文件核对，28 文件均为本会话产物（`components.d.ts` 为 unplugin 自动生成）

## CI/CD（必填）

- 分支：`dev`
- commit：见 git log（`[agent:frontend-agent]` 标注）
- pipeline URL / ID：push 后 GitLab CI 自动触发（lumen-ui-topic-mobile → K8s dev）
- 部署 namespace / 镜像 tag：CI 产出
- K8s rollout：待 CI（dev 自动）
- dev 测试 URL / 命令与结果：待 CI 部署后走 `e2e:chain-gold` 复测（段 E）

## 涉及文件

**新增（3）**
- `src/components/AnalysisHistorySheet.vue`
- `src/utils/riskPainMap.ts`
- `scripts/enterprise-gap-remediation.test.mjs`

**修改（25）**
- API 层：`api/enterprise/{paths,evaluation,keyAnalysis,profileDetail}.ts`、`types/{evaluation,keyAnalysis,profile}.ts`
- mock 层：`mocks/{evaluationTemplates,keyAnalysisSzStatus,profileDetail}.ts`
- 组合层：`composables/{useMobileAsyncAnalysis,useMobileKeyTypeAnalysis,useMobileKeyDomainAnalysis}.ts`
- 配置/工具：`config/enterpriseEvaluation.ts`、`utils/keyAnalysisParams.ts`、`fixtures/enterpriseKeyAnalysis.ts`
- 视图层：`views/enterprise/{EnterpriseEvaluationView,EnterpriseRiskView,EnterpriseRecruitView,EnterpriseDetailView,EnterpriseKeyTypeView,EnterpriseKeyDomainView,EnterpriseSzStatusView}.vue`、`components/PageTabs.vue`
- 生成：`components.d.ts`（unplugin 自动）

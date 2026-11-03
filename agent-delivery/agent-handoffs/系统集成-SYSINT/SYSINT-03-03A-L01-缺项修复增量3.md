# Handoff · SYSINT-03-03A-L01 产业服务内容管理 · 5 子功能补齐（第 3 轮 · D-2 拍板）

> **任务**：`SYSINT-03-03A-L01`（feature / P1 / M / 5分）· 执行 `agent:frontend-agent` · 监管 `human:孔东`
> **本轮范围**：D-2 拍板（2026-11-03）A-2 五个子功能按需规补齐 UI（331(1)/331(2)/332(1)/332(2)/333(1)/(2)），mock 数据，页面布局入口参照企业发展内容管理页
> **代码基线**：`lumen-ui-topic` dev @ `05d7178` 之上，**改动停在本地工作区未 commit**（人工验收闸门：走查通过后再推）
> **对照真源**：需规 seq 331–333（`agent-delivery/bid-reference/srs/04-科技专题服务系统/科技专题内容运营中心/门户内容管理.md`）；缺口台账 v1.2
> **建档**：2026-11-03 · 强度 ponytail full

---

## 需规 → 实现对照

| 需规 | 子功能 | 实现（schema / 组件） |
|---|---|---|
| 331(1) | 全球服务机构概况：基础档案（名称/成立时间/服务类型）+ 专家综合服务能力评估 | `svc_org_profile`（showBody：正文存专家评估意见；服务类型=孵化器/检测平台/咨询公司/其他）→ 机构编辑 Tab「全球概况」`ServiceOrgSectionForm` |
| 331(2) | 服务机构产业与区域分布：覆盖产业领域、地理区域（国家/省市/园区）、与产业对应关系描述 | `svc_org_distribution`（rows：industry_name + region（复用 RegionSelect 四级级联，C-3/B-5 同款）+ relation_desc）→ 机构编辑 Tab「产业区域分布」 |
| 332(1) | 技术力评估维度维护（如技术方案先进性、实施能力、客户反馈） | `svc_rank_dimension`（维度名称/说明/权重%）→ 榜单屏维度区（`ServiceCmsRankTab`） |
| 332(2) | 服务机构技术力 Top30 榜单：上榜机构、评估理由、专家评述、服务案例 | `svc_tech_rank`（rank_no/org_id/rank_basis/expert_comment/service_case）→ 榜单屏（Top30 上限、名次查重、同榜机构查重、满员拦截，校验口径复用 `EnterpriseCmsRankTab`） |
| 333(1) | 深圳服务产业档案：代表性机构、服务类型、覆盖行业 | `sz_svc_profile`（domain_label + rows：org_name/service_type/industry_coverage）→ 深圳屏档案区（`ServiceCmsShenzhenTab`） |
| 333(2) | 深圳服务产业竞争力分析：优势、短板、发展潜力 | `sz_svc_competitiveness`（strength/bottleneck/potential_summary）→ 深圳屏竞争力区 |

## 工作台结构（参照 EnterpriseCmsWorkspace 四屏模式）

`ServiceCmsWorkspace.vue` 升级为四屏：

1. **机构列表**：原筛选/表格保留；新增「全球概况」「产业区域分布」状态列（未维护/草稿/已发布）；列表操作条新增两个入口按钮
2. **机构编辑**（3 Tab）：业务领域介绍（原 Tab 原样保留，含 X-6 DoD 校验）+ 全球概况 + 产业区域分布
3. **技术力榜单**：Top30 榜单 + 评估维度双区
4. **深圳服务产业**：档案 + 竞争力分析双区

## 产物清单

| 文件 | 类型 | 说明 |
|---|---|---|
| `src/components/cms/cmsTypeSchema.ts` | 改 | +`SVC_TYPE_OPTIONS` 字典；+5 个 service schema |
| `src/components/cms/cmsMockSeeds.ts` | 改 | +6 类种子（概况 1/分布 1/维度 2/榜单 2/档案 1/竞争力 1） |
| `src/views/cms/service/ServiceCmsWorkspace.vue` | 重写 | 单屏 → 四屏工作台 |
| `src/views/cms/service/ServiceCmsRankTab.vue` | 新 | 榜单 + 维度维护 |
| `src/views/cms/service/ServiceCmsShenzhenTab.vue` | 新 | 档案 + 竞争力维护 |
| `src/views/cms/service/ServiceOrgSectionForm.vue` | 新 | 机构维度单记录表单（参照 EnterpriseSectionForm，绑 org_id） |
| `src/views/cms/service/serviceCmsGapFix2.selfcheck.mjs` | 新 | 5 子功能自检（26 断言） |

## 复用与决策（ponytail）

- 表单/抽屉/行编辑全部复用现有组件（`CmsEditDrawer`/`CmsScalarField`(region)/`CmsRepeatRows`/`useCmsMockStore`/`persistRecord`）；榜单校验逻辑照抄 `EnterpriseCmsRankTab`（名次正整数 1–30、名次查重、同榜机构查重、满员拦截）
- **覆盖产业/行业字段用 text 而非 cascader**：`IndustryThreeLevelCascader` 是 `string[]` 多选模型 + 走接口目录（Q068），适配筛选不适合单值表单；企业 CMS 同类字段（`classify_value`）先例也是 text。mock 阶段自由文本最贴合需规「与产业对应关系描述」
- 机构维度概况/分布是「一机构一记录」块（同 `EnterpriseSectionForm` 模式），不走抽屉——与既有业务领域 Tab 的抽屉并存是原页面结构，保留
- D-7：专家评价保持自由文本（不做结构化署名）
- 机构主数据：mock `CMS_MOCK_ORGS` 2 家占位；「新增机构」等 Java 主数据（不在本轮）

## 测试结果

- `node src/views/cms/service/serviceCmsGapFix2.selfcheck.mjs` ✅（需规字段完整性 + 组件接线 + 工作台结构 + X-6 不回归）
- `node src/views/cms/service/serviceCmsGapFix.selfcheck.mjs` ✅（上轮 X-6/R-1/R-3 不回归）
- `npm run type-check`：**本次文件 0 错误**；存量 3 处（`vite.config.ts` 1 处、`CmsScalarField.vue` stage-multiselect 2 处）已 stash 验证为并行会话改动基线，非本轮引入
- `npx eslint`（6 个改动文件）✅ 0/0
- **未做浏览器走查**（停本地待孔东验收）

## 验收建议（走查路径）

1. 服务 CMS → 机构列表：新增「全球概况/产业区域分布」状态列；操作条「技术力 Top30 榜单」「深圳服务产业」入口
2. 机构编辑 → 「全球概况」Tab：成立时间/服务类型/正文（专家评估）→ 发布 → 状态列变已发布
3. 「产业区域分布」Tab：添加行 → 覆盖产业领域 + 地理区域（四级级联）+ 对应关系描述 → 发布
4. 榜单屏：新增上榜机构（名次自动=当前+1）→ 同名次/同机构重复应被拦截；榜单满 30 拦新增；「评估维度」区新增/编辑/删除
5. 深圳屏：「服务领域档案」行内含代表性机构/服务类型/覆盖行业；竞争力分析含优势/短板/发展潜力
6. 回归：业务领域 Tab 的 X-6 DoD 校验仍生效（正文粘贴「评估 92.5 分」发布应被拦）

## 架构合规自检

- 调用链：纯前端 mock ✅；可观测：mock 阶段无请求 ✅
- D8/D9/D10：CMS 管理页无统计数字 ✅
- D12：未触碰 demo-* ✅
- 未新增依赖、未改配置 ✅
- ponytail: full（榜单校验/复用组件优先，无新抽象层）

## cost

- actual_tokens: ~55000
- model_used: glm-5.3
- actual_cost: ~$0.5
- cost_warn: green

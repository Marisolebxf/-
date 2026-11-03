# Handoff · SYSINT-03-02A-L01 产业全景运营正文 · 缺项修复增量

> **任务**：`SYSINT-03-02A-L01`（feature / P1 / L / 5分）· 执行 `agent:frontend-agent` · 监管 `human:孔东`
> **本轮范围**：2026-11-03 note「缺项优化补充」中不依赖拍板的 4 项；只动前端代码，数据走 mock（用户指令 2026-11-03 12:18）
> **对照真源**：`agent-handoffs/专题对齐-TOPIC/门户内容管理-四页前端实现对照.md` v1.1
> **代码基线**：`lumen-ui-topic` dev @ `11bab82` 之上，commit `220db19` **停在本地未 push**（人工验收闸门 + 用户指令"先 commit 不 push"）
> **建档**：2026-11-03 · 强度 ponytail full

---

## 修改内容（4 项）

| 缺项 | 文件 | 改动 |
|---|---|---|
| **319(1)** 产业概况只有标题+正文 | `cmsTypeSchema.ts` + `cmsMockSeeds.ts` + `PanoramaSectionForm.vue` | `pano_industry_intro` 补 5 个 formFields：发展阶段（四态 select）/产业定位/核心优势摘要/创新亮点摘要/主要挑战摘要；SectionForm 增 formFields 网格渲染（复用 `CmsScalarField` + `fieldGridSpan`，同企业 SectionForm 模式）；IC 种子补演示值 |
| **319(2)** 历程无专家观点 | `cmsTypeSchema.ts` + `cmsMockSeeds.ts` | `pano_dev_history` columns 增 `expert_opinion`（textarea，非必填）；种子行补键（值留空，演示不伪造专家观点） |
| **A-3** 本地产业数据无入口（需规 7805 / 320(1)） | 三文件同上 | 新 content_type `pano_sz_metrics`（5 列：指标名称/数值/单位/数据年份/备注）；BLOCKS 增「本地数据」块 + 列表列 + Tab；IC 种子 2 行演示 |
| **C-2** 列表无状态筛选 | `PanoramaCmsWorkspace.vue` | 查询区加状态下拉（全部/未维护/草稿/已发布）；**宽口径**：一行 = 一个产业六维总览，任一维度命中该状态即显示（与服务页单块口径不同，已在代码注释说明） |

## ⚠️ 契约偏差声明（重要）

`pano_*` 5 类契约（PORTAL-CMS-专题全景.md，草案）**没有**本轮新增的字段（intro 5 字段、history expert_opinion、新 content_type pano_sz_metrics）。任务 DoD 写明「契约草案确认前不改字段」，本轮按用户 2026-11-03 12:18 开工指令执行，**该偏差需在下次契约确认会同步**，Java 叶 `SYSINT-03-02A-JAVA-L01` 对应端点需扩字段/增类型。Java 侧现状：5 个 pano_* 写接口已在 integration。

## 不在本轮（有依赖）

- **A-1 / R-5**（318 图谱维护整叶 + 待确认占位列）→ D-1 拍板（做：复用 G6 + IndustryPanoramaPage；不做：登记 REMOVED 删列）
- **C-3** 产业字典不可维护 → 走 Java 主数据（CMS-JX-IND-TREE integration 中）
- **B-1 多语言**（319(1) 需规明写）→ D-3；**B-2 专家署名结构化** → D-7（本轮 expert_opinion 是纯文本列，署名四件套等 D-7 统一组件）
- X-2 revision 机制 → 全模块共性，随架构统一改

## 测试结果

- `node --experimental-strip-types src/views/cms/panorama/panoramaCmsGapFix.selfcheck.mjs` ✅（逐项 assert 四个缺项落点）
- `npm run type-check`：CMS 相关 0 错误（vite.config.ts 存量错误非本轮引入）
- `npx eslint src/views/cms/panorama/ src/components/cms/cmsTypeSchema.ts cmsMockSeeds.ts` ✅ 0/0
- **未做浏览器走查**（停本地待孔东验收）

## 验收建议（走查路径）

1. 产业全景列表 → 状态筛「草稿」→ 只见人工智能行（intro 草稿）；重置还原（C-2）
2. 编辑集成电路 → 产业介绍 Tab → 见 发展阶段/定位/核心优势/创新亮点/主要挑战 五字段，IC 有演示值（319(1)）
3. 发展历程 Tab → 条目行多出「专家观点」多行文本列（319(2)）
4. 本地数据 Tab → 两条演示指标（2300 亿元 / 420 家）；可增删行、发布（A-3）
5. 列表「本地数据」列显示已发布标签（A-3）

## 架构合规自检

- 调用链：纯前端 mock，无新接口 ✅
- 可观测：mock 阶段无请求 ✅（接 Java 后 @/utils/request 自动继承）
- D8/D9/D10：CMS 管理页无统计数字 ✅
- 未新增依赖、未改配置 ✅
- 契约偏差已声明（见上节）⚠️

## cost

- actual_tokens: ~60000
- model_used: glm-5.3
- actual_cost: ~$0.5
- cost_warn: green

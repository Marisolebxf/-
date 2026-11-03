# Handoff · SYSINT-03-01A-L01 企业发展运营正文 · 缺项修复增量（第 2 轮）

> **任务**：`SYSINT-03-01A-L01`（feature / P1 / L / 8分）· 执行 `agent:frontend-agent` · 监管 `human:孔东`
> **本轮范围**：2026-11-03 note「缺项优化补充」中可纯前端 + mock 闭环的 6 项；只动前端代码，数据走 mock（用户指令 2026-11-03 12:18）
> **对照真源**：`agent-handoffs/专题对齐-TOPIC/门户内容管理-四页前端实现对照.md` v1.1（基线 `09ad60a`）
> **代码基线**：`lumen-ui-topic` dev @ `c6c4f7f` 之上，改动**停在本地工作区**（人工验收闸门，AGENTS.md ⚠️）
> **建档**：2026-11-03 · 强度 ponytail full

---

## 修改内容（6 项，5 文件 + 1 删 + 1 selfcheck）

| 缺项 | 文件 | 改动 |
|---|---|---|
| **C-1** 单记录块无删除 | `EnterpriseSectionForm.vue` | 已入库记录显示「删除」按钮（a-popconfirm 确认 → `store.remove(contentId)` → 重置为新建态）；多条记录（产品）仍由外层列表管理 |
| **C-2** 列表无状态筛选 | `EnterpriseCmsWorkspace.vue` | 查询区加「档案状态」下拉（全部/未维护/草稿/已发布），与编辑页基础档案状态同口径；查询/重置联动 |
| **B-3** 排序无入口 | `EnterpriseCmsKeySetTab.vue` + `EnterpriseCmsWorkspace.vue` | 深圳重点名单加上移/下移（重编号 sort_order）；产品 Tab 加上移/下移（换 store 相邻记录位，数组序即展示序） |
| **X-1** 链位整块覆盖写 | `EnterpriseChainSlotsDrawer.vue` | `mergeRows` 保存前从 store **重读最新父记录**再合并他人行（旧快照整条覆盖的根因修复）；带 ponytail 注释：仍非并发安全，接 Java 后由服务端按记录版本收口 |
| **X-5** standard_ref 换设备失效 | `EnterpriseSectionForm.vue` | 选项 value 改「产业:标准名」稳定键；旧 contentId 引用并入选项保证回显 label 不显示裸码 |
| **R-2** 死代码 | 删 `EnterpriseCmsListTab.vue`（12 KB，git rm，零业务引用） |
| **资质荣誉拆 Tab**（孔东 2026-11-03 12:29 走查指令） | `cmsTypeSchema.ts` + `cmsMockSeeds.ts` + `EnterpriseCmsWorkspace.vue` | 新 content_type `ent_honor_list` 承接荣誉 4 列（名称/级别/年份/备注），`ent_basic_profile` 去掉 rows 只留档案字段+正文；工作台加「资质荣誉」Tab 与基础档案并列；种子两条荣誉原样搬家，演示数据无缝。注意：契约侧若已有 ent_basic_profile 荣誉字段，接 Java 时需同步该拆分（新增 8 类外的 content_type 需 Java 叶确认） |

## 不在本轮（有依赖，防弃件）

- **B-2 专家署名** → 挂 D-7（统一结构化小组件方案）待拍板
- **C-3 企业字典不可维护** → 走 Java 主数据（`CMS-JX-ENT-LIST-L01` integration 中），不前端自建
- **D-4**（基础档案/榜单三处能力去留）、**D-6**（链位唯一入口）→ 孔东拍板后执行
- B-1 多语言 / X-2 / X-8 / X-9 全模块共性项 → 另议

## 测试结果

- `node --experimental-strip-types src/views/cms/enterprise/enterpriseCmsGapFix.selfcheck.mjs` ✅（逐项 assert 六个缺项 + 荣誉拆分的落点）
- `npm run type-check`：CMS 相关 0 错误（`vite.config.ts` 1 个 dual-package 存量错误非本轮引入，过滤确认）
- `npx eslint src/views/cms/enterprise/ src/components/cms/cmsTypeSchema.ts src/components/cms/cmsMockSeeds.ts` ✅ 0 error 0 warning
- **未做浏览器走查**（改动停本地，待监管人验收时走查）

## 验收建议（走查路径）

1. 列表「档案状态」筛 未维护 → 只见无基础档案行；重置还原（C-2）
2. 任一企业「明星名单」Tab 已有记录 → 见红色「删除」→ 确认后回新建态、列表标签变未维护（C-1）
3. 「重点企业全景图」→ 深圳重点圈定 → 勾 3 家 → 上移/下移 → 排序列 1/2/3 重编（B-3）
4. 企业编辑「产品」Tab 建两条 → 上移互换位置（B-3）
5. 两个浏览器窗口分别开 企业编辑「链位」与 重点企业全景图，各加一行保存 → 互不吞行（X-1）
6. 明星名单「入选标准」下拉 → 选后刷新（F5）→ 回显标准名而非裸码（X-5）
7. 企业编辑「资质荣誉」Tab 与「基础档案」并列 → 荣誉两条（小巨人/科技进步奖）在独立 Tab；基础档案不再显示条目区（荣誉拆分）

## 架构合规自检

- 调用链：纯前端 mock，无新接口 ✅
- 可观测：沿用 03-03A 确认口径（mock 阶段无请求；接 Java 后 `@/utils/request` 自动继承）✅
- D8/D9/D10：CMS 管理页无统计数字，指标角标不涉及 ✅
- 未新增依赖、未改配置文件 ✅

## cost

- actual_tokens: ~110000（含前轮会话检索）
- model_used: glm-5.3
- actual_cost: ~$0.9
- cost_warn: green

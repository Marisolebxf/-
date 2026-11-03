# SYSINT-03-04A-L01 政策新闻运营正文 · 缺项修复增量（B-4/B-5）

> **任务**：SYSINT-03-04A-L01（监管 human:孔东）
> **日期**：2026-11-03 · agent:frontend-agent · 强度 ponytail full
> **前置拍板**：D-5 保留（human:孔东 2026-11-03）；D-7 不做（专家署名范围外）
> **代码基线**：`lumen-ui-topic` dev @ `6a3b8bf`（停本地，**未 push**，待监管人验收；含两轮：`a7adf8f` B-4 + 静态级联首版，`6a3b8bf` 按孔东拍板改 RegionSelect + 联想接口）

## 本轮修复（对照文档 v1.2 §3.4/§4.2）

| 缺项 | 需规出处 | 修复 | 落点 |
|---|---|---|---|
| **B-4** 榜单无「名次」字段 | 336(2)（行 7997–7999）Top10 排序语义不成立 | 表单加 `rank_no`（必填、半宽、首位），placeholder 与关键词筛选同步含「名次」 | `cmsTypeSchema.ts` `policy_intensity_rank.formFields` |
| **B-5** 地理分布无层级 | 335(2)（行 7991–7993）要求国家/省/市/区四级 | **改用企业查询页同款 `RegionSelect`**（孔东 2026-11-03 拍板：复用现成组件+接口）。数据源 `entRegionScopesStore`（region-scopes 接口，30min 缓存，失败回退本地树）；值存「/」label 路径（如 `全国/广东省/深圳市`），label↔code 互转工具 `regionLabelsToCodes` | `types.ts`（kind=region）+ `CmsScalarField.vue` + `regionOptions.ts` |
| **C-3** 企业选择不可检索 | §4.3 | **改用查企业联想接口**（孔东 2026-11-03 拍板）。`enterpriseSelect` 字段与关系对象企业列换 `ent-select`：输入关键词调 `entSearchSuggest`（同查企业页），value=org_id；历史/种子值不在联想结果时并入选项兜底回显 | `types.ts`（kind=ent-select）+ `CmsScalarField.vue` + `cmsTypeSchema.ts` |

## 设计说明

- **RegionSelect 复用**：企业查询页在用的 region-scopes 级联（全球/全国→省→市→区，全国支线下四级）；CMS 值存人可读 label 路径而非 scope_code，`regionLabelsToCodes` 做 label→code 回显互转；未命中段原样返回兜底显示。
- **ent-select 联想**：`entSearchSuggest({prefix, size:20})` 返回 `org_id + name_cn`；mock 态该接口已注册（`mockEntSearchSuggest`），联调后零改动接真。列表筛选/KeySetTab 弹窗等其余 `CMS_MOCK_ENTERPRISES` 消费点属 01A 增量（后续同样替换）。
- **D-4 登记**（孔东拍板）：`ent_basic_profile`/`ent_rank_dimension`/`ent_competitive_rank` 前端按现状保留，Java 侧后续按需求补接口。

## 不在本轮（有依赖）

- **Java 写接口叶**：政策 4 类 content_type 无对应 JAVA 叶（企业/全景/服务均有），保留后需拆——已在 registry note 登记，等 coordinator 排。
- **USE_MOCK=false 接线**：等 Java 叶 + 契约确认。

## 测试结果

- `node --experimental-strip-types src/views/policy/policyCmsGapFix.selfcheck.mjs` ✅（B-4 字段/必填/种子 + B-5 RegionSelect/region-scopes 四级/label-code 互转/未命中兜底 + C-3 联想接口 逐项 assert）
- `npm run type-check`：本轮文件 0 错误（余 `vite.config.ts` 存量 1 个；`PolicyNewsCmsPage.vue:96` 1 个为并行会话 WorkbenchTabs 改动引入，非本轮）
- `npx eslint`（6 个改动文件）✅ 0 error 0 warning
- **未做浏览器走查**（改动停本地，待监管人验收时走查）

## 验收建议（走查路径）

1. 政策新闻 CMS → 力度评估 → 政策力度榜单 → 新建 → 首字段为「名次」（必填，不填发布被拦）
2. 统计与区域 → 编辑 → 地理区域列为企业查询页同款级联（全国→广东省→深圳市→南山区 四级），选到哪级存哪级；接口不可达时回退本地树仍可选
3. 种子数据 `pol-stats-1` 两条区域行显示「全国/广东省/深圳市」「全国/广东省」路径
4. 种子 `pol-rank-1` 编辑回显名次 = 1
5. 企业 CMS 任一「企业」字段（如基础档案）→ 输入「深芯」→ 联想出企业列表（同查企业页）；历史值 ENT-DEMO-001 仍回显不空白

## 架构合规自检

- 调用链：entSearchSuggest / region-scopes 均为仓内既有前端→Java REST 接口，未越层 ✅
- D8 Design：复用企业查询页 RegionSelect 与 Arco a-select，无新依赖 ✅
- D9 指标血缘：CMS 内容管理非统计指标点位，不涉及 ⓘ/MockBadge（政策正文页面另有处理）✅
- 多会话保护：本轮只提交 6 个自持文件；并行会话的 WorkbenchTabs/routes/viz 等改动未触碰 ✅

**ponytail**: full —— 删除自造静态树改复用现成组件（-85 行自造数据）；region/ent-select 做成通用 CmsColumnKind，D-2 服务 CMS 区域分布与机构选择可复用。

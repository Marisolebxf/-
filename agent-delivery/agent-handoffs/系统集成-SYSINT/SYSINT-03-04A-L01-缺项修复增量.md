# SYSINT-03-04A-L01 政策新闻运营正文 · 缺项修复增量（B-4/B-5）

> **任务**：SYSINT-03-04A-L01（监管 human:孔东）
> **日期**：2026-11-03 · agent:frontend-agent · 强度 ponytail full
> **前置拍板**：D-5 保留（human:孔东 2026-11-03）；D-7 不做（专家署名范围外）
> **代码基线**：`lumen-ui-topic` dev @ `a7adf8f`（停本地，**未 push**，待监管人验收）

## 本轮修复（对照文档 v1.2 §3.4/§4.2）

| 缺项 | 需规出处 | 修复 | 落点 |
|---|---|---|---|
| **B-4** 榜单无「名次」字段 | 336(2)（行 7997–7999）Top10 排序语义不成立 | 表单加 `rank_no`（必填、半宽、首位），placeholder 与关键词筛选同步含「名次」 | `cmsTypeSchema.ts` `policy_intensity_rank.formFields` |
| **B-5** 地理分布无层级 | 335(2)（行 7991–7993）要求国家/省/市/区四级 | `CmsColumnKind` 新增 `cascader`；`region` 列换四级级联（国家/省/市/区，mock 静态树：中国北京/广东/上海 + 美国加州样例），值存「/」路径（如 `中国/广东省/深圳市`）；列表回显即路径文本 | `types.ts` + `CmsScalarField.vue`（a-cascader 渲染）+ `cmsTypeSchema.ts` |

## 设计说明

- **cascader 值形态**：`/` 拼接路径而非行政码——与 rows 自由文本展示一致、mock 阶段无字典依赖；接 Java 时如换地区字典接口，改 `cascaderOptions` 来源即可，值形态在契约确认会定（⚠️ 契约草案无对应字段，同 pano_* 偏差处理）。
- **树为静态 mock**：覆盖需规四级语义的最小样例（中国 3 省→市→区，深圳 4 区齐）；接主数据后替换。
- **B-2 专家署名**：按 D-7 拍板不做结构化，`expert_comment` 维持自由文本。

## 不在本轮（有依赖）

- **Java 写接口叶**：政策 4 类 content_type 无对应 JAVA 叶（企业/全景/服务均有），保留后需拆——已在 registry note 登记，等 coordinator 排。
- **USE_MOCK=false 接线**：等 Java 叶 + 契约确认。

## 测试结果

- `node --experimental-strip-types src/views/policy/policyCmsGapFix.selfcheck.mjs` ✅（B-4 字段/必填/种子 + B-5 cascader/四级深度/路径值/渲染 逐项 assert）
- `npm run type-check`：仅 `vite.config.ts` 1 个存量 dual-package 错误（非本轮引入）
- `npx eslint`（5 个改动文件）✅ 0 error 0 warning
- **未做浏览器走查**（改动停本地，待监管人验收时走查）

## 验收建议（走查路径）

1. 政策新闻 CMS → 力度评估 → 政策力度榜单 → 新建 → 首字段为「名次」（必填，不填发布被拦）
2. 统计与区域 → 编辑 → 地理区域列为四级级联（中国/广东省/深圳市/南山区），选到哪级存哪级
3. 种子数据 `pol-stats-1` 两条区域行显示「中国/广东省/深圳市」「中国/广东省」路径
4. 种子 `pol-rank-1` 编辑回显名次 = 1

## 架构合规自检

- 调用链：前端本地 mock 存储，未越层 ✅
- D8 Design：Arco `a-cascader` + 仓内 token，无新依赖 ✅
- D9 指标血缘：CMS 内容管理非统计指标点位，不涉及 ⓘ/MockBadge（政策正文页面另有处理）✅
- 多会话保护：改动仅本仓 5 文件，主仓另见拍板落档 commit ✅

**ponytail**: full —— 最小 diff（5 文件 +130/-8），cascader 做成通用 CmsColumnKind 而非政策私有控件（后续 D-2 服务 CMS 区域分布可复用）。

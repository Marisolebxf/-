# SYSINT-03-15-L01 · 专题内容管理 CMS 公共控件与通用表单框架

> **任务**：SYSINT-03-15-L01（`task_type=feature`，E-PM-DELIVERY，WBS-03-15）
> **执行**：`human:孔东` 开 Agent 会话 · **监管**：`human:孔东`
> **仓库**：`lumen-ui-topic`（改动停在本地工作区，未 commit、未 push）
> **日期**：2026-10-24 · **强度**：ponytail full
> **ponytail:** full。未跳过 D8 token。本叶是运营编辑框架，无统计数字，不挂指标 ⓘ。

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `human:孔东` |
| supervised_by | `human:孔东` |
| claim_type | `pull` |
| 说明 | 2026-10-24 孔东认领并开工。2026-10-24 孔东确认可以验收。 |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 公共组件单独目录，复用仓内 Arco Vue。富文本按孔东放行引入与后台同版 WangEditor，并在保存时做契约白名单过滤。 |

## 问题清单

- 企业、产业全景、专题服务三套正文页不在本叶，仍由 `SYSINT-03-01A-L01`、`SYSINT-03-02A-L01`、`SYSINT-03-03A-L01` 套用本框架。
- 政策扶持不出 CMS 表单。
- 不接 Java 写接口。企业发展写接口在 `SYSINT-03-01A-JAVA-L01`。

## 修改内容

公共组件在 `lumen-ui-topic/src/components/cms/`。

| 组件 | 作用 |
|------|------|
| `CmsContentFrame` | 列表、新建、编辑；保存草稿、发布、归档 |
| `CmsRichText` | WangEditor。工具条仅标题、加粗、列表、引用、链接、网络图片、撤销、重做。不上二进制、不上视频 |
| `CmsRepeatRows` | 可配置行。名单与时间线共用 |
| `CmsScalarField` | 单行文本、多行文本、日期、单选、复选 |
| `CmsIndustrySwitch` | 产业切换。选项由调用方传入，宽 240px，不超过 400px |

预览路由 `/cms-framework-preview`：不进侧栏，不进统一用户中心，假数据。HTML 保存前按企业发展契约白名单过滤（段落、标题、列表、引用、加粗、链接、图片 URL）。

**偏离**：`package.json` 增加 `@wangeditor-next/editor@5.6.43`、`@wangeditor-next/editor-for-vue@5.1.14`，与 `lumen-ui-admin` 同版。DoD「不另引组件库」的放行人是 `human:孔东`（2026-10-24 开工前确认）。

## 测试结果

- `node src/components/cms/htmlWhitelist.selfcheck.mjs` 通过。
- `npx vue-tsc --noEmit -p tsconfig.app.json` 通过。
- 浏览器走查 `https://localhost:3000/cms-framework-preview`：未选产业不能保存；新建草稿后列表可见；再发布后状态为已发布；产业筛到生物医药后只剩对应行；侧栏无该路由。
- 编辑页可见单选、复选、多行文本。产业下拉宽度 240px。

## 遗留风险

- 全景、专题服务契约仍是草案。字段由调用方传入，本叶不写死 12 个 `content_type`。
- 公共信封没有审核态。预览只有草稿、发布、归档。
- 未接写接口，不能算与 Java 联调通过。
- 未 commit、未 push，无 CI、无 K8s rollout。

## CI/CD

- 分支：本地 `dev` 工作区，未 commit
- commit：无
- pipeline URL / ID：无
- 部署 namespace / 镜像 tag：无
- K8s rollout：未部署
- dev 测试 URL：`https://localhost:3000/cms-framework-preview`

## 可观测性

- 本叶预览不调 Java，无新 trace。正式业务页接线时再带 `observability.ts`。

## 架构合规

| 铁律 | 结果 |
|------|------|
| 前端只准备调 Java，本叶不直连 Python | 符合。预览无请求 |
| D8 控件高 32px、正文 14px、主色沿用仓内 token，单控件不超过 400px | 符合 |
| D12 不调用 demo 服务 | 符合 |
| 不进菜单、不编造统一用户中心路径 | 符合。菜单注册仍是 `SYSINT-03-18-L01` |
| 政策扶持不做 CMS 表单 | 符合 |

## 涉及文件

- `repos/lumen-ui-topic/src/components/cms/`
- `repos/lumen-ui-topic/src/views/cms/CmsFrameworkPreview.vue`
- `repos/lumen-ui-topic/src/router/routes.ts`
- `repos/lumen-ui-topic/package.json`
- `repos/lumen-ui-topic/package-lock.json`
- `repos/lumen-ui-topic/pnpm-lock.yaml`

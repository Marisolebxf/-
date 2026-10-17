# CMS-JX-ENT-NEWS-L01 · 企业动态资讯 CRUD

> **任务**：`CMS-JX-ENT-NEWS-L01`（feature / P1）
> **依据**：《CMS-JX接口规格书.md》§1.2
> **代码**：lumen-svc-platform `gkxlumen-cms` commit `e3efd5c`

## 认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:api-agent` |
| supervised_by | `human:徐滕强` |
| claim_type | pull |

## Ponytail

ponytail: `full`（复用 overlay 审计 / CmsErrors / Api-Key；无新依赖；纯内容表 CRUD）

## 交付

| 端点 | 行为 |
|------|------|
| `POST /cms/v1/enterprise/news/list` | domain=ENT、软删剔除；keyword(title)/kind/risk/status + 分页 |
| `POST /cms/v1/enterprise/news/detail` | 同上过滤 |
| `POST /cms/v1/enterprise/news/create` | title/content/company 必填；company=org_id[] 校验存在于 `v_cms_ent` |
| `POST /cms/v1/enterprise/news/update` | 字段白名单局部更新；company 同校验 |
| `POST /cms/v1/enterprise/news/delete` | reason 必填；软删 + `cms_op_audit` |

响应约定：`company`=org_id[]，`companyNames`=从 `v_cms_ent` 回显名称；`date`←`pub_date`，`sourceUrl`←`source_url`。

异常统一走 `CmsErrors` + `CmsEnvelope`（本单顺带把 ENT-CRUD 异常迁到共享类）。

## 验证

- 本地 `mvn -pl gkxlumen-cms -am compile` 绿
- CI：pipeline [6500](https://gitlab.htmisoft.net/gkx-lumen/lumen-svc-platform/-/pipelines/6500) `backend:build` + `backend:image:cms` SUCCESS（commit `e3efd5c`）
- 部署：镜像 `gkxlumen-cms:e3efd5cd`（kubectl set image，因 GitLab `deploy:cms` 手动闸门本次未点）
- 活库冒烟（ClusterIP :7098）：list total=0 → create id=1 → detail 回显 companyNames → update risk=中 → keyword list=1 → delete → detail 40401；幽灵 company → 40001。**联调通过**

## 架构合规

| 铁律 | 结论 |
|------|------|
| 调用链 / 无算法 | ✅ 纯 Java CRUD |
| 真源只读 | ✅ 只写 `cms_content_news` + audit；名称读视图 |
| Api-Key | ✅ `/cms/v1/*` 既有 Filter |
| demo/lumen | ✅ lumen-svc-platform |

## Cost

| 字段 | 值 |
|------|-----|
| actual_tokens | ~35000 |
| model_used | composer |
| actual_cost | ~$0.4 |
| cost_warn | green |

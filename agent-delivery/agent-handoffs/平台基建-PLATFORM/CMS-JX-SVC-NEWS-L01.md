# CMS-JX-SVC-NEWS-L01 · 服务机构动态资讯 CRUD

> **任务**：`CMS-JX-SVC-NEWS-L01`（feature / P1）
> **依据**：《CMS-JX接口规格书.md》§3.2
> **代码**：lumen-svc-platform `gkxlumen-cms` commit `0495b5f`

## 认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:api-agent` |
| supervised_by | `human:徐滕强` |
| claim_type | pull |

## Ponytail

ponytail: `full`（复用 cms_content_news 表 + ENT-NEWS 已审骨架；无新依赖）

## 交付

| 端点 | 行为 |
|------|------|
| `POST /cms/v1/service-org/news/list` | domain=SVC、软删剔除；keyword(title)/kind + 分页钳制 |
| `POST /cms/v1/service-org/news/detail` | org=org_id[]，orgNames 从 `v_cms_svc` 回显 |
| `POST /cms/v1/service-org/news/create` | title/org 必填；org 校验存在于 `v_cms_svc`；kind 枚举 服务案例/客户反馈/培训活动/路演对接会 |
| `POST /cms/v1/service-org/news/update` | 白名单局部更新（org_ids CAST JSON）；行数 0 → 404 |
| `POST /cms/v1/service-org/news/delete` | reason 必填；`is_deleted=0` 守卫 + 行数兜底 404（防并发双删双审计） |

与 ENT 资讯同表不同域（domain 列隔离），live 已验证互不串扰。

## 验证

- CI：pipeline 6557（0495b5f）`backend:build`+`image:cms` 绿
- 部署：Pod `gkxlumen-cms:0495b5f7`
- 冒烟：list→create→detail（orgNames 回显）→update kind→kind 筛选→**ENT 列表隔离 total=0**→ghost org 40001→无 reason 40001→软删后 404
- bugbot：no bugs（与已审 ENT-NEWS 骨架对照，无漂移）

## 架构合规

✅ 纯 Java CRUD / 真源只读 / Api-Key / lumen 正式仓

## Cost

| 字段 | 值 |
|------|-----|
| actual_tokens | ~30000 |
| model_used | composer |
| actual_cost | ~$0.35 |
| cost_warn | green |

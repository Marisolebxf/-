# CMS-JX-POL-CRUD-L01 · 政策条目写侧 + 删除操作审计

> **任务**：`CMS-JX-POL-CRUD-L01`（feature / P1）
> **依据**：《CMS-JX接口规格书.md》§2.1
> **代码**：lumen-svc-platform `gkxlumen-cms` commits `18f032d` + `ddbd569`（bugbot 修复）

## 认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:api-agent` |
| supervised_by | `human:徐滕强` |
| claim_type | pull |

## Ponytail

ponytail: `full`（复用 OverlayDao/视图/CmsErrors；无新依赖；审计接口直译规格）

## 交付

| 端点 | 行为 |
|------|------|
| `POST /cms/v1/policy/list` | join 视角 `v_cms_pol`；`activeOnly` 默认 true（status≠失效，NULL 视为有效）；keyword(title)/reviewStatus/industryTag/regionTag/status 筛选 |
| `POST /cms/v1/policy/detail` | 视图详情（含只读 status/level/source） |
| `POST /cms/v1/policy/create` | 虚拟政策 `cms:POL-{uuid8}`，title 必填；不写真源 |
| `POST /cms/v1/policy/update` | 10 字段白名单 `JSON_MERGE_PATCH`；首覆盖前 `requireVisible`；软删行 404 |
| `POST /cms/v1/policy/delete` | reason 必填 → 专家知识引用检查（policy 四域 `$.entityId`）40901 → 软删 + 审计 |
| `POST /cms/v1/policy/audit-logs/list` | `cms_op_audit`（POL 全部写操作）；列 time/operator/action(新增/编辑/删除)/title/reason；标题回退链 视图→overlay→真源 |

**bugbot 修复（medium）**：审计标题回退链补 `LEFT JOIN demo_gkxlumenx_dwd.policy_base_info`——"无覆盖直删真源政策"场景视图已剔除、overlay `$.title` 为 NULL，靠真源表补全标题。

## 验证

- CI：pipelines 6524（18f032d）+ 6530（ddbd569）`backend:build`+`image:cms` 绿
- 部署：Pod `gkxlumen-cms:ddbd569a`
- 冒烟：list(total=20000, activeOnly 生效)→create 虚拟→detail→update(虚拟+真源 docNo)→ghost 404→audit-logs keyword 命中→delete 无 reason 40001→软删后 404→审计三动作齐；**标题回退专项**：无覆盖直删真源政策后审计行 title=真源标题（TITLE_FALLBACK_OK）
- bugbot 复审：唯一 finding 被 validator 剔除（误报），修复确认干净

## 架构合规

✅ 纯 Java CRUD / 真源只读（审计回退链也只 LEFT JOIN）/ Api-Key / lumen 正式仓

## Cost

| 字段 | 值 |
|------|-----|
| actual_tokens | ~40000 |
| model_used | composer |
| actual_cost | ~$0.45 |
| cost_warn | green |

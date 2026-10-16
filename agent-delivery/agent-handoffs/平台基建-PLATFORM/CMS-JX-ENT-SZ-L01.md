# CMS-JX-ENT-SZ-L01 · 深圳本地企业专项 CRUD

> **任务**：`CMS-JX-ENT-SZ-L01`（feature / P1）
> **依据**：《CMS-JX接口规格书.md》§1.3
> **代码**：lumen-svc-platform `gkxlumen-cms` commits `41113a1` + `069d4b6`（bugbot 修复）

## 认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:api-agent` |
| supervised_by | `human:徐滕强` |
| claim_type | pull |

## Ponytail

ponytail: `full`（复用 CmsErrors / Api-Key / 审计；无新依赖）

## 交付

| 端点 | 行为 |
|------|------|
| `POST /cms/v1/enterprise/sz/list` | keyword（企业名 join）/district 筛选 + 分页（page/size 钳制） |
| `POST /cms/v1/enterprise/sz/detail` | name=org_id，nameDisplay 回显 |
| `POST /cms/v1/enterprise/sz/create` | name=org_id（须存在于 v_cms_ent）、industry 必填；同企业唯一有效行由 DB 唯一键保证 |
| `POST /cms/v1/enterprise/sz/update` | 白名单局部更新；换绑企业预检 + DuplicateKey 兜底 |
| `POST /cms/v1/enterprise/sz/delete` | reason 必填；软删 + 审计；并发双删 → 404 |

**bugbot 修复（medium）**：check-then-insert 并发双插 → `cms_content_sz` 加软删感知唯一键 `uk_sz_active(domain, active_org)`，`active_org = IF(is_deleted=0, org_id, NULL)` STORED 生成列；活行唯一、软删行退出约束（可重复软删同企业）。live 库已 ALTER，DDL 文件同步。

## 验证

- CI：pipeline 6515（41113a1）+ 6518（069d4b6）`backend:build` + `image:cms` 绿
- 部署：Pod `gkxlumen-cms:069d4b67`
- 冒烟：list→create→detail（nameDisplay 回显）→dup 40001→update→district 筛选→delete→404；ghost org 40001；news page=0 钳制回归 ok
- bugbot 复审：no bugs

## 架构合规

✅ 纯 Java CRUD / 真源只读 / Api-Key / lumen 正式仓

## Cost

| 字段 | 值 |
|------|-----|
| actual_tokens | ~30000 |
| model_used | composer |
| actual_cost | ~$0.35 |
| cost_warn | green |

# CMS-JX 只读接口收口（徐滕强名下 6 单）

> **覆盖单**：CMS-JX-ENT-LIST-L01（suggest 收口）/ CMS-JX-SVC-LIST-L01（suggest 收口）/ CMS-JX-IND-TREE-L01 / CMS-JX-IND-LINK-L01 / CMS-JX-ENT-PRODUCT-L01 / CMS-JX-BULK-L01
> **契约真源**：老设计单 CMS-JX-INT-DESIGN-L01 §5.2（A5 改写全 POST 版）
> **代码**：lumen-svc-platform `ReadonlyFacadeService/Controller`，commits `c2f9417` → 冒烟修复 `fdd3376` → bugbot 修复 `1204621`/`e4de6b1`
> **认领**：api-agent / supervised_by human:徐滕强 / pull（批量授权）

## 交付端点

| 端点 | 说明 |
|------|------|
| `POST /cms/v1/enterprise/suggest` | 企业下拉：v_cms_ent（含虚拟/软删剔除），keyword LIKE + limit≤50，**滤 name IS NULL**（bugbot low） |
| `POST /cms/v1/service-org/suggest` | 机构下拉：v_cms_svc 同口径 |
| `POST /cms/v1/enterprise/products` | 按企业 id 查产品：**读 v_cms_prod join 视角**（bugbot med：直查真源会绕过运营改挂/软删），LEFT JOIN 真源补链/环节编码 |
| `POST /cms/v1/industry/tree` | 标准产业分类树（仅真源；自定义/合并视角走既有 /industry/tree-merged） |
| `POST /cms/v1/industry/chain-links` | 标准链环节（仅真源；同上） |
| `POST /cms/v1/bulk/entities` | 四类实体批量（图谱初始化）：entity_type 枚举 40001、limit≤500 钳制、返回 id/name/type/region/industry（bugbot med 补齐契约字段）、**incremental:false 显式声明** updated_after 暂不过滤（视图无稳定 update_time，正式化对列后启用） |

## 修复链

1. `fdd3376` 冒烟：真源表无 `is_deleted` 列；视图子查询缺别名
2. `1204621` bugbot：products 改读视图（绕过 overlay 矛盾）/ suggest 滤 NULL 名 / bulk 补 type/region/industry + incremental 标志
3. `e4de6b1` 冒烟：v_cms_svc 类型列名为 `type` 非 `org_type`

## 验证

- CI：pipelines 6598/6600/6603/6605 build+image:cms 全绿
- 部署：Pod `gkxlumen-cms:e4de6b1f`
- 冒烟：11/11 全绿（suggest×2 / products / tree / chain-links / bulk×4类 / 非法类型 40001 / limit 9999→500 钳制）
- bugbot：3 项（2 med + 1 low）全修后复验绿

## 偏差记录

- bulk 的 `updated_after` 增量语义延后（视图无稳定更新时间列，正式化对列时启用；响应已带 `incremental:false` 防调用方误解）
- tree/chain-links 标准目录与 tree-merged/chain-links-merged 合并视图并存：契约路径给标准数据，合并视图给 CMS 运营面板

## 架构合规

✅ 只读零写零审计 / 双数据源 @Qualifier 各归其位 / Api-Key 全覆盖 / ClusterIP 不出集群

## Cost

| actual_tokens | model_used | actual_cost | cost_warn |
|---|---|---|---|
| ~25000 | composer | ~$0.3 | green |

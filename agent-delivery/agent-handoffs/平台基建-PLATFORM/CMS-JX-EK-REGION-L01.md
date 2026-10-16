# CMS-JX-EK-REGION-L01 · 专家知识·综合区域

> **任务**：`CMS-JX-EK-REGION-L01`（feature / P1）｜**规格**：《CMS-JX接口规格书.md》§6.5
> **实现**：/cms/v1/expert/region/*
> lumen-svc-platform 625e81f（批量）+ 0218b83/6ce9588+0ec56ec/8910c6f/6e8685b/c3ebb64f（冒烟+review 修复链）
> **CI**：pipelines 6569/6575/6583/6587/6589/6592 build+image:cms 全绿｜**部署**：Pod gkxlumen-cms:c3ebb64f

## 交付
同五域统一实现；2 section；entity={entityType:'region',name} 自由文本

## 验证
- 冒烟：58 项全量冒烟 + 8 项 review 修复专项验证全绿
- 统一 review：三组并行 bugbot（A/B/C）：3 high + 2 medium + 4 low 全修，复验通过（PROD 回读 ROUNDTRIP_OK / rel.update OK / stage 筛选收窄 flt=1<all=189115 / 改码引用 40001 / 防撞标准码 40001 / 空串 date OK / 防环验证生效）

## Ponytail
ponytail: `full`（复用 CmsErrors/OverlayDao/Api-Key/模板骨架；无新依赖）

## 架构合规
✅ 纯 Java CRUD / 真源只读 / Api-Key / 不碰 Nebula / lumen 正式仓

## Cost
| actual_tokens | model_used | actual_cost | cost_warn |
|---|---|---|---|
| ~15000（批量摊销） | composer | ~$0.15 | green |

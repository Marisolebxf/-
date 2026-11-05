# 企业评估维度与双Top30接口

交付标识：20261105-enterprise-cms-rank-api。ponytail: full；增量后端实现，前端文件未修改。

依据：需规324。新增后端模块，前端可并行接入；已有内容类型及接口保持兼容。

网关前缀：`/cms/cms-ops/v1/enterprise/content`。继续使用用户态Bearer及`systemcode: topic`。

## 内容类型与字段

| content_type | 必填字段 | 可选字段 |
| --- | --- | --- |
| `ent_rank_dimension` | `future_industry_code`、`rank_type`、`dimension_name`、`dimension_meaning` | `weight_percent`（0–100，可不填）、`sort_order`、`locale` |
| `ent_competitive_rank` | `future_industry_code`、`rank_type`、`enterprise_code`、`rank_no`、`rank_basis` | `expert_comment`、`sort_order`、`locale` |

- `rank_type`：`tech`技术力、`business`商业力；独立人工维护，不自动计算评分。
- `rank_no`：整数1–30。同产业同榜单内名次唯一、企业唯一，草稿和已发布共同占位。
- 不同产业/榜单可重复使用同一名次与企业。软删除释放占位，下架仍占位。
- `enterprise_code`使用既有企业标识（与CMS企业摘要一致），不存在或已剔除的企业不允许上榜。
- 可选权重仅为运营维度记录，不默认推导权重、不强制总和100、不进入算法。
- `page_key`为`rank`。`content_id`为字符串；`publish_status/version/publish_time`由发布动作控制，前端不直接写。

## 路径

| 方法 | 路径 | 行为 |
| --- | --- | --- |
| GET | `/{content_type}` | 列表，支持`future_industry_code`、`rank_type`、`enterprise_code`、`publish_status`、`page`、`size` |
| GET | `/{content_type}/{id}` | 详情 |
| POST | `/{content_type}` | 新建草稿 |
| POST | `/{content_type}/{id}/update` | 部分编辑，合并原字段后校验 |
| POST | `/{content_type}/{id}/publish` | 发布，版本递增，重新校验 |
| POST | `/{content_type}/{id}/unpublish` | 下架为草稿，版本保留 |
| POST | `/{content_type}/{id}/delete` | 软删除 |

信封沿用`{code:0,msg:"ok",data:...}`；列表为`{total,page,size,records}`。
榜单列表按`rank_type,rank_no,id`升序；维度按`sort_order,id`升序。

名次/企业重复及参数错误返回40001；并发争用由数据库唯一索引兜底，返回40901冲突，提示刷新。

新建维度示例：

```json
{
  "future_industry_code": "INB1303",
  "rank_type": "tech",
  "dimension_name": "技术积累",
  "dimension_meaning": "人工维护评估维度说明"
}
```

新建榜单条目示例（非正式评估结果）：

```json
{
  "future_industry_code": "INB1303",
  "rank_type": "tech",
  "enterprise_code": "5e1e6b71d726b16d339f5c2b5aba87ff",
  "rank_no": 1,
  "rank_basis": "模拟评估依据，仅供接口联调",
  "expert_comment": "模拟评述，非真实专家意见"
}
```

## 存储与接线

DDL：`db/9zz_gkxlumenx_cms_ops_enterprise_rank.sql`。仅CMS新增两张独立表，保留原有审计与发布事务。
不写DWD/ES，不占用服务机构榜单表。

前端已有同名schema，可继续使用原`cmsOps`适配器。前端同学完成接入时移除两类型的`CMS_OPS_UNSUPPORTED`标记，保留加载/错误/空态；本次后端提交不修改前端文件。

## 交付验证

- 后端提交`2cdc4bb`，已推送`origin/dev`；本地61项回归通过（既有服务38、类型元数据18、新企业榜单5）。
- 两张表已在CMS业务库按幂等DDL创建；事务验证Top30名次范围、名次及企业唯一、双榜单隔离、重复软删除后释放名次通过，测试数据全部回滚。
- 保留原CMS用户鉴权、事务与审计，不写DWD/ES；没有改前端页面、开关或旧类型字段。
- 既有`list`服务签名保留，新增带可选rank_type的重载。只有两个新类型支持rank页面键；旧列表排序保持原样。
- CI旧版Mockito API兼容修复`1c0a3ee`已推送；流水线3924 backend:build、helm:lint、backend:image:cms全部成功，CI实际61项相关回归无失败。
- 自动deploy:cms排队时，使用项目SSH跳板将同一CI镜像`gkxlumen-cms:1c0a3ee1`滚动dev，rollout成功。
- `scripts/verify_enterprise_rank_api.py`从真实网关入口验证：两个rank_type维度及榜单CRUD、部分编辑、发布/下架、已发布过滤、名次排序、整数1–30边界、重复名次、重复企业、不存在企业、并发抢位仅一个成功，以及软删除后重用均通过。
- dev留下`INB1303`的2条模拟维度、4条模拟上榜草稿（2企业×技术力/商业力）；标记`MOCK_ENT_RANK_20261105`，非正式评估或真实专家意见。关联企业沿用已有乐科、君正时代的真实标识；临时INB1306并发样本已软删除，不修改主数据。
- 旧内容类型的结构/排序/CRUD签名保持兼容；前端源码及开关没有修改，前端负责人可按本文件契约移除新类型的unsupported标记并完成页面接入。
- 暂无task-registry MCP，不伪造任务登记与成本；本次后端交付已可联调，不宣称前端页面验收完成。

# 缺口清单

只写方法和表名。本包不建表，不灌数，不写 ODS，不写供应方库，不写久新分析库。库名若要用，只允许 `gkxlumenx_gapfill`，表名以 `gapfill_` 开头。

第一批的 `industry_chain_node` 不走缺口表。`node_id` 为空的行跳过，不用环节名称生成 VID。

## 先加工，再考虑缺口表

| 缺什么 | 落在哪一层 | 缺口表（仅当没有第二来源） | 本版 |
|---|---|---|---|
| `depends_on` 要上下游，正式行是 `parent_child` | 在 DWD `industry_chain_node_rel` 用已有 `node_id` 写成白名单里的 `relation_type`。`parent_child` 保持原样，不改名 | `gapfill_segment_depends_on`，列是两个环节 `node_id` 和方向 | 不建表，不触发这条边 |
| 企业到环节，`node_id` 对不上已有 `segment:` | 先确认环节 ID 就是 `industry_chain_node.node_id`。企业点归企业包，本包不补企业 | 仍对不上时才用 `gapfill_enterprise_segment_rel`，列是企业 `org_id` 和环节 `node_id`。与企业包里的同名表是一张，不另起 | 本版不灌 |
| 服务机构到环节没有正式行 | 在 `industry_chain_entity_rel` 增加 `entity_type=service_institution` 且关系类型在白名单内的行。机构主数据不在本包 | `gapfill_service_segment_rel`，列是机构稳定 ID 和环节 `node_id` | 本版不建表 |

从环节介绍正文里猜上下游：本侧没有写图入口。工程过程里的 `upstream_from_text.py` 只是未实现示例，不能配成现在的步骤。

分批和燕大的小版本对齐：v0.1 只调通环节点。上表里标成「本版不建表」的，留到写明下一版再开。

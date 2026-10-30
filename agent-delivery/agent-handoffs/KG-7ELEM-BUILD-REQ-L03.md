# KG-7ELEM-BUILD-REQ-L03 · 七要素建图·必须三元组与关系总图

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 已认领，本次不重新 task-claim。状态保持 integration。输入只认重写后的 L02（查询 46、算法 36） |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `N/A` |
| 说明 | 定义/文档。未用强度行删三元组 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | L02 读的是原文 |

## 图即契约（架构 / 存储流图 / ARCH-IMPL / 联调 / IA 首页必填）

| 字段 | 值 |
|------|-----|
| diagram_id | `KG-7ELEM-MUST-EDGES` |
| 图 diff | 按新 L02 重裁。实线 24 条。删掉服务机构 participates 服务机构。新增政策 cite 政策。可选 0，不画 |
| 会签态 | `draft`（源文件 frontmatter，无人签） |
| 说明 | 不是 L0 `ARCH-TOPO-LUMEN`，不复制存储流图。实线只表示必须建，不授权改图空间 |

## 问题清单

- 必须三元组 24（M01–M24），可选 0。
- 七类两两 28 对：必须建 15，不建 13。不建里无消费 6、待确认 7、已有边覆盖 0。
- 相对上一版边名：删除「服务机构 participates 服务机构」；新增「政策 cite 政策」。科研合作来源改为 A29，人才合作来源改为 A30。企业 cooperate / supply / parent_sub 只取方向已写死的 A32、A33、A34。
- 燕大 EDGE 全部写新建。L04 未签收，不写成复用放行。

## 修改内容

- 覆盖 `工程过程/04-系统集成/07-图数据库集成/KG-7ELEM-BUILD-REQ-L03-必须三元组与关系.md`。
- 未改 L02、L04、L05。未改 storage、代码、图空间。

## 测试结果

- 图上 24 条实线与必须表 24 行一一对应。可选边没有，也不在图上。
- 关系名、终点或方向标了待确认的行没有升成必须边。
- 技术 cite 与政策 cite 拆开。两两 15+13=28，含 7 对自身。

## 遗留风险

- A26「同 A25」若以后被确认也包括机构混装，M18 要退出必须。
- A35 的 institution 没有归入单一七要素，产业链环节—科研机构仍是待确认。
- `industry` 若以后归入产业链环节，A28 要重开。
- 基数 L02 未写，表中全部待确认。

## CI/CD（必填）

- 分支：`gkx-orchestration` `dev`
- commit：未提交。厚包要求停在本地
- pipeline URL / ID：无。`cicd: skip`
- 部署 namespace / 镜像 tag：无
- K8s rollout：无
- dev 测试 URL / 命令与结果：无

## 可观测性（建议）

- 无服务改动

## 涉及文件

- `agent-delivery/工程过程/04-系统集成/07-图数据库集成/KG-7ELEM-BUILD-REQ-L03-必须三元组与关系.md`
- `agent-delivery/agent-handoffs/KG-7ELEM-BUILD-REQ-L03.md`

## 架构合规

| 铁律 | 结果 |
|---|---|
| 只写文档 | ✅ |
| 不改 Nebula 空间、不选燕大空间当生产 | ✅ |
| 待确认端点、关系名、方向不进必须 | ✅ |
| L04 未签收不写成已放行复用 | ✅ |
| 技术点不并进技术 | ✅ |

## 成本

| 字段 | 值 |
|------|-----|
| model_used | grok-4.7 |
| actual_tokens | 未回填注册表 |
| actual_cost | 未回填注册表 |
| cost_warn | 未回填注册表 |

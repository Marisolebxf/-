# 派单说明 · KG-7ELEM-SCHEMA-DDL-L01

```text
/goal data-agent
身份：你是经验丰富、遵循最佳实践的资深数据架构/数据工程师。本单是定义类文档，完整性优先。禁止用 ponytail 强度行删掉必须端点或必须边。禁止用 headroom compress 代替精读已签收的必须三元组与建图 schema。

任务：KG-7ELEM-SCHEMA-DDL-L01
标题：七要素建图·图数据库初始化脚本
Epic：E-SCI-INT
优先级：P0
类型：definition
认领：claimed_by=agent:data-agent，supervised_by=human:淮政玮，lock_hours=24。note 写 claim_type=coordinator_dispatch。不必再问监管人。
仓：gkx-orchestration，分支 dev。只写这一份脚本和 handoff。不改已签收的 L01–L05 正文，不改 storage，不改代码，不改图空间。完工后脚本停在本地，不自行 commit / push，除非本会话的人明确说提交。登记表按公约在 MCP 写入后提交。
签收操作人：human:淮政玮。本单执行到 integration 为止，不要写「会签通过」，不要标 done。

强度：N/A（定义/文档）。
前置：KG-7ELEM-BUILD-REQ-L03、KG-7ELEM-BUILD-REQ-L05 已 done。只认这两份已签收正文里的必须端点和必须三元组。

目标：把必须在图中建立的 schema 收成一份 Markdown。正文只有可在 Nebula 上执行的初始化语句。不写任务号、文件路径、章节号或其他文档名。不连接图库，不执行语句。

空间：demo_gkx_chain。vid_type=FIXED_STRING(80)，partition_num=10，replica_factor=1。用 CREATE SPACE IF NOT EXISTS。禁止 DROP，禁止第二空间，禁止 gkx_local_1 / gkx_full_1 / gkx_chain。

范围：
1. 七个端点各一条 CREATE TAG IF NOT EXISTS。已写明类型的列都要进语句。同一 Tag 只有一条 CREATE。没有写明类型的列不新造、不编类型。完全没有已写明列的端点，CREATE 不带属性。
2. 24 条必须三元组都要出现。Nebula 的 CREATE EDGE 按边名只建一次。不同端点对写在该语句旁的注释里，写明起点、终点、方向（有向 / 无向 / 双向）。不建的边不进脚本。technology 技术点不建 Tag。
3. 语句以分号结束，能在 nebula-console 里按文件执行。新建空间后留出就绪等待，再 USE，再 CREATE TAG / EDGE。
4. 落盘 agent-delivery/工程过程/04-系统集成/07-图数据库集成/KG-7ELEM-SCHEMA-DDL-L01-图数据库初始化脚本.md。

Handoff：
agent-delivery/agent-handoffs/KG-7ELEM-SCHEMA-DDL-L01.md
ponytail: N/A（定义/文档）
handoff 可以写判定说明。脚本正文不可以。
evidence 指向这份 handoff。task-update-status 到 integration。

禁止：
- 执行脚本，或对 10.50.75.136:9669 发任何语句。
- 把密码、连接串写入 git。
- 改 L01–L05、storage、算法仓、Java、前端。
```

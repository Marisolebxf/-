# 派单说明 · KG-GRAPH-COVER-01（包 A · 燕大 · 技术点层覆盖补齐）

> 2026-11-13。淮政玮派。P0，第一批。这是本次计划的地基：**A 不完成，B/D/H 全部空转**。
> 一句话：技术点层有三条边没灌满、一个字段全空，把它们补齐，且补完要能说清补了多少、跳过多少、为什么跳。

```text
/goal data-agent
身份：你是资深图数据工程师，负责把源表数据按现有 schema 灌进 NebulaGraph，并出可复算的对账。本单是数据补齐，不是结构变更。禁止用 ponytail 删减检查项，禁止用 headroom compress 代替精读缺口表。

任务：KG-GRAPH-COVER-01
标题：技术点层覆盖补齐（tech_has_institution / tech_rel / tech_path_step / community_id）
Epic：E-SCI-INT
优先级：P0
类型：data_task
负责人：human:白鑫凤（监管 human:淮政玮）。认领 claimed_by=human:白鑫凤 或 agent:data-agent，supervised_by=human:淮政玮。
状态：ready。依赖 KG-GRAPH-PLAT-09（图库扩容/调水位）必须先有结论；扩容未到位时先跑第 0 步小批量试写。
仓：gkx-orchestration，分支 dev。脚本与对账文档落本仓；不改 schema，不改 Java/前端，不动 MySQL 任何既有库。
图空间：demo_gkx_chain（10.50.75.136:9669）。凭据走环境变量，口令不进 git。
完成日期要求：2026-11-17（P0 窗口）。

强度：medium。允许写批量脚本，但必须可断点续、可 dry-run。

前置事实（已实测，直接采信，不重新调研）：
- 源表 ads_technology_institution 2,528,802 行，图中 tech_has_institution 现 51,000 条 → 缺 2,477,802（98%）。
- 源表 ads_technology_graph_edge 587,252 行，图中 tech_rel 现 541,428 条 → 缺 45,824。
- 源表 ads_technology_evolution_path_step 47,909 行，图中 tech_path_step 现 35,018 条 → 缺 12,891。注意 47,909-35,018 恰等于路径条数 12,891，疑似每条路径少记 1 步（末端节点），必须先判定是取数规则还是数据缺陷。
- 源表 ads_technology_community_member 19,430 行（每技术点一行），图中 tech_point.community_id 19,430 点全部为空串（不是 NULL）。
- 图库内存已到 80% high watermark，无 Tag 锚定的全表扫与大聚合会被拒（sum(weight) 518 秒后拒）。所有查询必须带 Tag 锚定。

目标：四项缺口补齐到可验收水位，并出对账。技术点层是 428/432/435/437 与专题技术链 104/105 的共同底座，补不齐则这两块都只能降档交付。

第 0 步 · 扩容闸门（必做，先于一切写入）
1. 向 human:淮政玮 确认 KG-GRAPH-PLAT-09 结论（已扩容 / 已调 high_watermark / 未处理）。
2. 未处理时：只做 dry-run + 1 万条小批量试写，把「写入被拒」的原始报错留证，不硬灌。
3. 已处理时：跑一次 `MATCH (v:tech_point) RETURN count(v)` 与一次 `MATCH ()-[e:tech_has_institution]->() RETURN count(e)`，全表计数能过才继续。

第 1 步 · tech_has_institution（最大项，2,477,802 条）
1. 读源表时按技术点分批（每批 20 万行），每批固定 batch 值：kg100-cover-01-ins-01 … -ins-13。
2. 写入前先 FETCH 两端点：源端 tech_point:<tcn>、目标 tech_institution:<id> 必须都已存在；不存在则跳过并计数（skip_missing_endpoint）。
3. 写入用 INSERT EDGE tech_has_institution(weight, props) VALUES；props 至少含 {"batch":"<批号>","source":"ads_technology_institution"}。
4. 每批写完立刻回读该批 CONTAINS 计数，与写入声明条数比对，不一致即停并留证。
5. 全部完成后总量目标 ≥ 2,402,362（95%）；低于 95% 必须写清原因。

第 2 步 · tech_rel（45,824 条）
1. 以源表 587,252 行为全集，减去图中已有 541,428，得到差集再灌；禁止整表重灌（会破坏已有 props.batch）。
2. batch = kg100-cover-01-rel；同样先 FETCH 两端点。
3. 目标：tech_rel 总量 = 587,252（100%），允许因源端点缺失产生的 skip，skip 必须逐条留证。

第 3 步 · tech_path_step（12,891 条，先判定再动手）
1. 先出《路径步规则确认单》：抽 10 条路径，对比源表 47,909 行与图中 35,018 条，判定缺口是①每条路径少 1 步（末端节点）②源表含无效步③取数口径不同。
2. 属①或③：按确认后的规则补，batch = kg100-cover-01-step，目标 47,909（或按确认规则的实际应有数）。
3. 属②或无法判定：**不灌**，把结论写进交付文档，本项按 B 档（空态）交，不许猜着补。

第 4 步 · community_id 回填（19,430 点）
1. 从 ads_technology_community_member 读 (technology_node_id, community_id)，生成 UPDATE VERTEX 语句，按 2 万条一批。
2. 回填后校验：`MATCH (v:tech_point) WHERE v.tech_point.community_id != '' RETURN count(v)` 应为 19,430。
3. 注意字段现在是空串不是 NULL，校验语句不能用 IS NOT NULL。

对账（本单核心交付之一）：
| 项 | 源表应有 | 图中补后 | 跳过 | 跳过原因 |
|---|---:|---:|---:|---|
| tech_has_institution | 2,528,802 | 实填 | 实填 | 端点缺失/其他 |
| tech_rel | 587,252 | 实填 | 实填 | 同上 |
| tech_path_step | 47,909 或按规则 | 实填 | 实填 | 规则判定 |
| community_id | 19,430 | 实填 | 实填 | — |

主文路径（新建）：
agent-delivery/工程过程/04-系统集成/07-图数据库集成/派单-20261113-图谱100/KG-GRAPH-COVER-01-覆盖补齐对账.md
同目录放：脚本（可复跑）、路径步规则确认单、每批回读记录。

Handoff：
agent-delivery/agent-handoffs/KG-GRAPH-COVER-01.md
写清：四项目标/实际/跳过数、环境是否扩容、批次清单、未完成项与原因。
evidence 指向对账文档。task-update-status 到 integration，不写 done。

禁止：
- DROP SPACE、清空重建、删除任何现有边或点。
- 建第二个图空间（gkx_chain / gkx_local_1 等）。
- 无 Tag 锚定的全表扫、大聚合。
- 整表重灌 tech_rel（会冲掉已有批号）。
- 猜着补路径步；规则未确认就灌。
- 把口令、连接串写进 git。
- 改 schema、改 Java、改前端、动 MySQL 既有库。
```

---

## 附：为什么这一单最重要

技术点层是「科学技术全景 17–33」「科技知识图谱 423–437」「专题技术链 104/105」三处的共同数据底。机构边只有 2%，全景页的「按机构筛」等于没有数据；关系边缺 4.5 万，428 的整榜就要重算两遍。**先灌满、再重算、再出接口**，顺序不能倒。

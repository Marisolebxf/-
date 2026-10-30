# 派单说明 · KG-7ELEM-LOAD-PATH-L06

> 2026-10-30 先给人看。还没有授权领取，也没有授权开跑。开工仍以 [`KG-7ELEM-LOAD-长任务总控`](../../../agent-handoffs/七要素建图-KG-7ELEM/KG-7ELEM-LOAD-长任务总控.md) 和厚包为准。本文件只写科研机构、人才、技术这一叶，并补上久新材料。

```text
/goal data-agent
身份：你是经验丰富、遵循最佳实践的资深数据架构/数据工程师。本单是定义类文档，完整性优先。禁止用 ponytail 强度行删掉三问里的任一类。禁止用 headroom compress 代替精读已签收必须边、我方代码、燕大代码和久新已落盘材料。

任务：KG-7ELEM-LOAD-PATH-L06
标题：七要素上图路径·科研机构、人才、技术
Epic：E-SCI-INT
优先级：P0
类型：definition
认领：本说明写出时任务仍是 ready。只有本会话明确说领取之后，才 task-claim：claimed_by=agent:data-agent，supervised_by=human:淮政玮，lock_hours=24。note 写 claim_type=coordinator_dispatch。
仓：gkx-orchestration，分支 dev。只写本叶产物、本叶目录里的示例脚本和 handoff。
签收操作人：human:淮政玮。执行到 integration 为止。不要写「会签通过」。不要标 done。
强度：N/A（定义/文档）。
协作：algorithm-agent。只在代码入口对不上时核对。不改算法仓。

前置：KG-7ELEM-BUILD-REQ-L03、KG-7ELEM-BUILD-REQ-L05 已 done。必须边只认 L03 已签收正文。schema 只认 L05 已签收正文。

本叶必须边（不新增、不删除）：
- M01 人才 cooperate 人才，无向
- M02 科研机构 cooperate 科研机构，无向
- M03 人才 cooperate 科研机构，无向
- M04 人才 belong 科研机构，有向
- M05 科研机构 belong 科研机构，有向
- M06 技术 cite 技术，有向
- M07 人才 participate 技术，有向
- M08 科研机构 participate 技术，有向
- M09 人才 author_of 技术，有向
- M10 科研机构 publish 政策，有向。本叶只写科研机构这一端，政策一端注明归 L04
- M19 科研机构 research_coop 科研机构，双向。不并进 M02
- M20 人才 talent_coop 人才，双向。不并进 M01
M13、M14（政策 policy_apply_to 人才 / 科研机构）若来源在久新的人才或科研机构表，本叶写这一端的表和字段，并注明整条边归 L04。不在本叶重裁必须或不必须。
企业—科研机构、企业—技术、企业—人才不建。产业链环节到这三类不建。服务机构互相 participates 不补。technology 技术点不计入七要素「技术」。

共同输入（只读，总派单已列）：
- 已签收 L03 必须三元组、L05 建图 schema
- 我方写图代码：lumen-algo-py，以及对接文档里已经点名的入口。这三类没有独立 pipeline-to-nebula，没有就写没有，不另造存储域
- 燕大已实现代码：yanda/tech-kg-api。只作已实现对照，不选燕大 space 作生产

久新材料（本叶额外必读）：
久新原文只认对端目录里 2026-10-22 已落盘的两份快照，schema 5.11.0：
- agent-delivery/工程过程/04-系统集成/02-对接三要素/对接文档/对端/2026-10-22-ADS_SCHEMA-5.11.0.md
- agent-delivery/工程过程/04-系统集成/02-对接三要素/对接文档/对端/2026-10-22-ADS_SCHEMA_RELEASE_NOTES.md
我方从久新只读库整理的索引可以用来定位表和字段，引用时标明是我方整理，不是久新原文：
- 同夹 调研/调研记录.md、调研/表清单.csv、调研/字段清单.csv、调研/指标支持.csv
130 表溯源、93 指标缺口是我方二次分析。可以对照，不能代替上面的快照和字段清单，也不能写成久新已经确认的上图口径。
SYSINT-SCHEME-02 仍是处理中。久新材料不是已放行的上图契约。
快照日期是 2026-10-22。快照和现库不一致时，两套都写，并写明探查日期。不要只沿用 10-22 的行数。

数据探查（允许，只读）：
账号、密码、库名只从 agent-delivery/工程过程/04-系统集成/02-对接三要素/对接文档/对端/数据库链接信息.md 读取。主机和端口用同目录 README 里已写的连接示例。这两处都不抄进产物、handoff 或示例脚本。
只对本叶相关表做探查：ads_talent_*、ads_institution_*、ads_paper_*、ads_patent_*、ads_project_*。用 SHOW、COUNT、DISTINCT、空值比例、键能否对上。可以 LIMIT 少量行核对键和类型，不导出整表。
人才画像里的电话、邮箱、出生年等列只记字段名，不把值写进产物。
只读。禁止 INSERT、UPDATE、DELETE、DDL，禁止改久新库。
探查结果写进三问：现库有行、字段能对上必须边，才可以写进第 1 问的「久新库有数」；我方没有写图代码时，仍不能写成我方已经能上。

读久新材料时先按前缀找，再读字段，再决定能不能对上必须边：
- 人才：ads_talent_*
- 科研机构：ads_institution_*。久新把企业收在 institution 里，稳定代码 institution_type_id=company。企业不是科研机构。用机构表时必须写明如何滤掉 company。滤不掉就不要写成科研机构能直接上
- 七要素「技术」只看论文、专利、项目：ads_paper_*、ads_patent_*、ads_project_*
- ads_technology_*、ads_discipline_*、ads_emerging_topic_*、ads_research_problem_* 不是七要素「技术」。技术点、学科、主题、研究问题不建 Tag，不拿来填 M06、M07、M08、M09
表名出现不等于这条边能上。字段对不上、行数为 0、文档写预留或证据未到，都写进第 2 问或第 3 问，不要写进第 1 问。清单里没有的表不要编造，写「清单未列」。

三问（只覆盖上面列出的必须边；我方、燕大、久新分成三列）：
1. 关系库现在就能上的：源表、字段、Tag 或 Edge、代码入口、上图步骤。入口要能在仓库里打开。久新表能对上字段时，写明是久新库里的表，不是我方 ADS。没有我方写图代码就不要写成我方已经能上。
2. 因关系数据缺项不能直接上、要先加工的：缺哪张表或哪一列。建议加工落在哪一层。不写 ODS，不写供应方库，不写久新库。建议可以是 DWD/ADS 映射或 gapfill_ 前缀，只写方法，不建表、不灌数。
3. 不能靠源表、要先用其他技术的：技术名称、现有代码有没有、建议落在 Python 哪一类入口。Java 不做 NLP、向量或模型推理。没有代码的写成「未实现」。可以在本叶目录附 Python 示例脚本，只说明核心逻辑。脚本不接真实库，不执行，不加新依赖，不放进业务仓。示例不能把未实现写成已实现。

落盘：
agent-delivery/工程过程/04-系统集成/07-图数据库集成/KG-7ELEM-LOAD-PATH-L06-科研人才技术.md
示例脚本若有，同目录，文件名写明对应哪条边。

Handoff：
agent-delivery/agent-handoffs/KG-7ELEM-LOAD-PATH-L06.md
ponytail: N/A（定义/文档）
写清：三问各几条；待确认几条；燕大有代码但我方没有的几条；久新现库能对上字段、但我方没有写图代码的几条；探查日期。不写密码、主机、端口、账号、连接串。
evidence 指向这份 handoff。task-update-status 到 integration。

禁止：
- 改 L02–L05 的产物，改已签收建图正文，改初始化脚本，改 storage，改业务仓。
- 执行 nGQL，连接图库。久新 Doris 只按上面的只读探查来用，不写入。
- 把密码、主机、端口、账号、连接串写入产物或 git 里的新文件。数据库链接信息.md 已有，不要再复制一份。
- 把久新 ads_* 写成我方 ADS，把 company 并进科研机构，把技术点并进七要素「技术」。
- 把设想、示例脚本或未签收方案写成已实现。
```

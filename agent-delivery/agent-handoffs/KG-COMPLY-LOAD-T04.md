# KG-COMPLY-LOAD-T04 · 已归档交付的验收索引

日期：2026-11-12。整理已有证据，不代替最终签收。

## 任务认领与执行记录

- 交付执行人：韩梦蕊（SDD 建议执行人）；交付提交 887db942（2026-11-12），口径定案随 a6cf1823 / 9c371a83 / ca4bd2a8。
- 登记册原为 backlog，2026-11-12 回填 review；历史无认领字段，不倒填 claimed_by 或认领时间。

## 范围与实现

按唐绍祖 11-11 答复定案：M07 不建（770 万行 100% funded_output_author，资助署名≠参与）；M08 只建真隶属 participate research→project 17,426（lead 17,393 + investigator 33）；M09 author_of person→patent 85,069；M06 论文→论文无源不建；paper 本期 0 点。批号体系 comply-20261112-t04-*。

VID：person:<talent_id>、inst:<institution_id> 按定案字段；画像表无 patent_no/project_no 列，按 SDD 退路规则主键造号（patent:<patent_id>、proj:<project_id>）。

## 产物清单与验收证据

以下位于 `agent-delivery/工程过程/04-系统集成/07-图数据库集成/`：

- `KG-COMPLY-LOAD-T04-交付-20261112/T04-对账单-交T07.md`：应灌/实灌对账（交 T07）。
- `KG-COMPLY-LOAD-T04-交付-20261112/T04-对账框架.md`：执行纪律/坑档/进度日志。
- `KG-COMPLY-LOAD-T04-交付-20261112/T04-预检-实测.md`：预检七数。
- `KG-COMPLY-LOAD-T04-交付-20261112/t04_loader.py`、`t04_precheck.py`：灌数与预检脚本（定案版）。
- `T04T10-核验-实测.md` + `t04_t10_verify.py`：图内只读复测证据与脚本。

## 偏离、验证与架构合规

对账单自检 MATCH count 终态一致；2026-11-12 图内只读复测一致：M08 participate 17,426、M09 author_of 85,069（方向 person→patent 抽验=总数）、person 100,000 / research 83,745 / patent 70,496 / project 17,402 / paper 0、批号实测在 props；存量不动区 participates 213,500、depends_on 1,073 未动；禁区 M10–M14/M16 复核全 0。

注记：cooperate 6,062,884 与 belong 72,099 的漂移属 T03 在途灌数（cooperate 中 5,968,060 带批号、ent→ent 仍 94,824；belong 全为 M04 person→research、M05 research→research 仍 0），与本单无关。T03/T04 点接触面协调（INSERT VERTEX 整标签覆盖、勿双计）见对账单 §4。

## CI/CD 与 Cost

dev 分支，经 delivery/kg-comply-t04-t10-20261112 交付并入。无部署动作。

## 签收

登记册 review；待 coordinator 按 DoD 验收签 done，不代签。

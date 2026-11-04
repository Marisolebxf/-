# GDF-SVC-WORKPACK round1 答复与落地说明（round2）

> 对应：`round1/02-提问清单-服务机构-WP1-L1.ask.md`  
> 施工包：`agent-delivery/data/GDF/派单包/服务机构/GDF-SVC-WORKPACK/` v1.1（施工真源只放包内容；**我方答复材料归工程侧对接目录，不放派单包目录**）  
> 任务：`GDF-SVC-WORKPACK-R1A-L01` · 拍板 `human:徐滕强` 2026-11-04  
> 结构：上半 Q0–Q11 结论速览；下半逐条书面答复

## 一、结论速览（拍板 → 包内落点）

| qid | 结论 | 包内落点 |
|-----|------|----------|
| Q0 | 同意读 `gkxlumenx_ods`；禁止写 ODS、禁止 demo 库 | `00`/`01`/`06`/`08`/`13` |
| Q1 | `event_id`=复合键 md5；唯一键仅 `event_id` | `01`/`04`/`08`/`09`/`10`/`11` |
| Q2 | 金额统一元；万/亿按 1e4/1e8；外币不换汇；币种进 `ext`；不加币种列 | `08`/`09`/`04` |
| Q3 | 投资表 `org_id`=投资方；挂不上圈定则丢弃 | `08`/`09`/`11` |
| Q4 | 经营范围=`main_activities`；区县=`area` only | `08`/`09`/`12` |
| Q5 | 年报缺行留空，禁止合成；低覆盖可接受 | `04`/`08`/`09`/`11` |
| Q6 | `card.ext`、`fact.yoy` 本批占位 NULL | `09`/`12` |
| Q7 | 05 作业回签 ≠ registry 签收；签字栏仍由人补 | 流程（本单不代签） |
| Q8 | A1 六类+行业混写不加前缀；A5 `period=all` `slice_key=city` | `12` |
| Q9 | **取消** &lt;10 全库入池 | `08`/`12`/`11` + storage seeds |
| Q10 | 权威以本派单包为准 | `README`/`00` |
| Q11 | 正式表 GDF 接管；列一致；唯一键待 ALTER | `10`/`13` |

变更文件清单见包根 `CHANGELOG` v1.1 行。

## 二、逐条书面答复（可直接回填 ask JSON）

## Q0
选 **A**：同意改读平台 `gkxlumenx_ods`。包内禁读条款已删除；禁止写 ODS。

## Q1
选 **B**：`event_id = md5(复合键)`，规则见包 `08`§3。唯一键改为 `UNIQUE(event_id)`。不以裸 `dwd_id` 当 event_id。

## Q2
① 万=1e4、亿=1e8 折元；② 外币不换汇，可解析数字入库；③ 币种空/非空均不新建列，有币种进 `ext`；④ 不可解析置空。

## Q3
`org_id` = **投资方**。挂不上本批圈定的行丢弃。

## Q4
经营范围用 `dwd_org_org_product_info.main_activities`；区县只用主表 `area`（无 district 回退）。

## Q5
接受年报低覆盖为空的数据现状；禁止合成。

## Q6
确认本批不映射 `svc_org_card.ext`、`svc_metric_fact.yoy`（占位 NULL）。

## Q7
05 签字仍需人工补栏；本答复不代替签收。registry 签收走 `gkx-gdf-ddl-signoff` + 淮政玮。

## Q8
① A1：六类英文码 + 行业原文同列，不加 `IND:` 前缀；② A5：`period=all`，`slice_key=city`；③ yoy 见 Q6。

## Q9
**取消**「不足 10 家整表入池」。

## Q10
权威版本：本派单包现行目录（v1.1 / 2026-11-04）。变更经修订包 + CHANGELOG 通知。

## Q11
正式库七表同意按现存接管；`event_id` 唯一键需 ALTER；不 DROP。

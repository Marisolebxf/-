# round2 · 对 GDF round1 提问的书面答复

> 对应：`round1/02-提问清单-服务机构-WP1-L1.ask.md`  
> 施工包：`agent-delivery/data/GDF/派单包/服务机构/GDF-SVC-WORKPACK/` v1.1  
> 任务：`GDF-SVC-WORKPACK-R1A-L01`

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

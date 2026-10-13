# 环节服务机构数（M_SVC_CHAIN_SEGMENT_ORG_COUNT）

## 基本信息

- 指标ID: M_SVC_CHAIN_SEGMENT_ORG_COUNT
- 指标名称: 环节服务机构数
- 一级模块: 产业服务链分析
- 二级模块: 服务链分析
- 三级模块: 短板分析 / 生态地铁图
- 更新频率: 日
- 对齐状态判定: 已对齐目标口径（0.2.0；事实表缺口未闭合）
- 关联Q编号: Q-SVCCHAIN-08（缺机构×环节事实表）；供应方题 SVC-P0-3

## 口径定义

圈定池内，落在指定服务链环节的服务机构去重家数。

| 项 | 锁定值 |
|---|---|
| 人口 | `demo_gkxlumenx_dwd.svc_org_circle.org_id` |
| 环节字典 | CT-SVC-PT-01 六环节（唯一真源，见下） |
| 分组 | 按 `stage_id` 出六行（页面链路六站） |
| 计数 | `COUNT(DISTINCT org_id)`；同机构同环节多次服务只计 1 |
| 空环节 | 0 家返回 0；页面显示「暂无供给机构」，不伪造 |
| 选产业 | API 过滤（半连接），不进口径分母 |

### 环节字典（CT-SVC-PT-01）

`stage-research` 研发与科研合作 / `stage-ip` 知识产权与标准 / `stage-transfer` 技术转移与孵化 / `stage-pilot` 中试熟化 / `stage-testing` 检测认证 / `stage-market` 市场化服务。

语义 = **机构服务供给站位**，不是企业产业链归属、不是产业领域。

## 计算公式

```sql
-- 目标口径（当前无源表，不可执行）：
SELECT stage_id, COUNT(DISTINCT org_id) AS org_count
FROM <机构×服务链环节服务记录>          -- 缺口：待供方交付 SVC-P0-3
WHERE org_id IN (SELECT org_id FROM demo_gkxlumenx_dwd.svc_org_circle)
GROUP BY stage_id;
```

**当前无法执行**：机构×服务链环节服务记录在 ODS/DWD/ADS 均不存在。

禁止：产业链 `industry_link_code` / `node_stage`；服务六类 `FINANCE/IP/HR/MKT/CONSULT/INNOV`；国标 `industry` / `industry_l1..l4`；15 集群 `industry_cluster`；`svc_chain_gap.org_count_in_stage`（汇总壳，非成员事实）；前端 fixture `SERVICE_ORGS.segment`。

## 源库表字段

```
svc_org_circle
（缺口）机构×服务链环节服务记录 <- ods: 待供方交付（SVC-P0-3）
```

## 历史口径冲突（2026-10-13 排查）

- 算法侧 `svc_catalog.py` 曾把环节源写为 `dwd_org_industry_tags.industry_link_code` + `dwd_industry_chain_info`（产业链节点）。
- 产品 CT-SVC-PT-01 要求服务供给六站；Q-SVCCHAIN-08 明确禁止用产业链节点 / 15 集群冒充环节。
- 结论：产业链只能回答「企业挂哪个产业节点」，回答不了「机构提供哪类服务」；两套口径不可互换，本条按服务六环节。
- 算法侧 `svc_metrics.py` 仅直查 ADS（`svc_chain_gap` 现网 0 行 → 降级 mock），从未真从产业链算过环节家数。

## 参考文献 / 依据

`TRACE-SVCCHAIN-ECOSYSTEM.yaml`（REQ-SVC-ECO-CHAIN-VIS）；CT-SVC-PT-01；2026-10-13 human:徐滕强 拍板。

## 更新记录

- 2026-08-21: 初版
- 2026-10-13: 0.2.0 目标口径锁定（六环节 + 人口 circle + COUNT DISTINCT org）；环节字典与禁止项写死；事实表缺口保留

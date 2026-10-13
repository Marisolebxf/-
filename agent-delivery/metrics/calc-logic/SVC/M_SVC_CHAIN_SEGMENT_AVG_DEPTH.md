# 环节平均服务深度（M_SVC_CHAIN_SEGMENT_AVG_DEPTH）

## 基本信息

- 指标ID: M_SVC_CHAIN_SEGMENT_AVG_DEPTH
- 指标名称: 环节平均服务深度
- 一级模块: 产业服务链分析
- 二级模块: 服务链分析
- 三级模块: 短板分析 / 生态地铁图
- 更新频率: 日
- 对齐状态判定: 目标口径已锁（0.2.0；双缺口未闭合）
- 关联Q编号: Q-SVCCHAIN-08（成员表缺口）+ Q-SVCCHAIN-02（深度分口径未签）

## 口径定义

某服务链环节内，各机构在该环节的服务深度分的算术平均（0-100）。

| 项 | 锁定值 |
|---|---|
| 人口 | `demo_gkxlumenx_dwd.svc_org_circle.org_id` |
| 环节字典 | CT-SVC-PT-01 六环节（唯一真源） |
| 分组 | 按 `stage_id` 出六行 |
| 分子 | 机构在该环节的服务深度分（0-100）；沿 `M_SVC_ORG_COVERAGE_DEPTH`，**公式未签** |
| 空环节 | 无机构返回空；页面显示「—」，不伪造 0 |
| 选产业 | API 过滤（半连接），不进口径分母 |

### 环节字典（CT-SVC-PT-01）

`stage-research` / `stage-ip` / `stage-transfer` / `stage-pilot` / `stage-testing` / `stage-market`。

语义 = **环节内平均服务强度**，不是产业链节点覆盖比例。

## 计算公式

```sql
-- 目标口径（当前无源表 + 分子未签，不可执行）：
SELECT stage_id, AVG(depth) AS avg_depth
FROM <机构×服务链环节服务记录 + 机构服务深度分>   -- 缺口①：待供方交付 SVC-P0-3
WHERE org_id IN (SELECT org_id FROM demo_gkxlumenx_dwd.svc_org_circle)
GROUP BY stage_id;
```

**当前无法执行**：① 机构×服务链环节服务记录不存在；② 服务深度分口径未签（Q-SVCCHAIN-02）。

禁止：产业链 `industry_link_code` / `node_stage` / 覆盖节点比例（语义不同）；服务六类；国标 `industry`；15 集群；`svc_chain_gap.avg_depth`（汇总壳，现网 0 行）；前端 fixture 深度分。

## 依赖说明（2026-10-13 人拍：本条不写 metric: 引用）

- 分子本应来自 `M_SVC_ORG_COVERAGE_DEPTH`（MODEL，D1 draft，待唐绍祖会签）。
- 但该 MODEL 叶 seed 的 `source_tables` 把「环节」写成产业链 `dwd_org_industry_tags.industry_link_code` + `dwd_industry_chain_info`（产业链节点），与 CT-SVC-PT-01 服务六环节冲突（同 Q-SVCCHAIN-08 追记）。
- 若本条在 `source_tables` 写 `metric: M_SVC_ORG_COVERAGE_DEPTH`，会**继承错误环节轴**。故本条**只写目标口径与缺口，不写 `metric:` 引用**；待 MODEL 侧按六环节重判后再定是否转正式二次 STAT。

## 源库表字段

```
svc_org_circle
（缺口）机构×服务链环节服务记录 <- ods: 待供方交付（SVC-P0-3）
（缺口）机构服务深度分 <- metric: M_SVC_ORG_COVERAGE_DEPTH（未签；本条不写引用）
```

## 参考文献 / 依据

`TRACE-SVCCHAIN-ECOSYSTEM.yaml`；CT-SVC-PT-01；`M_SVC_CHAIN_SEGMENT_ORG_COUNT.md`（同环节轴）；2026-10-13 human:徐滕强 拍板。

## 更新记录

- 2026-08-21: 初版（演示态）
- 2026-10-13: 0.2.0 目标口径锁定（六环节 + circle 人口 + AVG(depth)）；不挂 MODEL 引用；双缺口写明

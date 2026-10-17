# 年度新增服务机构数（M_SVC_ORG_NEW_COUNT）

## 基本信息

- 指标ID: M_SVC_ORG_NEW_COUNT
- 指标名称: 年度新增服务机构数
- 一级模块: 产业服务链分析
- 二级模块: 服务机构分析
- 三级模块: 新增趋势分析
- 更新频率: 年度
- 对齐状态判定: 已对齐（2026-10-13 钉两层 SQL；2026-08-27 侯佳伟 1A2A3A）
- 是否在数据库: 序列在 ADS；正式编号现网 0 行（格子仍挂旧号，SEED 改挂）
- 关联Q编号: Q-SVC-010（入池规则 A，仍黄）。Q-SVCCHAIN-02 管深度/热度，不管本条

## 给实现 agent 的入口

两层禁止混写。看任务角色再选 SQL：

| 角色 | 只做 | 函数/入口建议 |
|---|---|---|
| 灌数 `svcseed` / GDF | `[SEED]` | `seed_org_new_count_series` |
| Java REST / Python `/internal` | `[SERVE]` | `serve_org_new_count` = 一条 SELECT |
| 前端趋势页 | `[PAGE]` | 环比用相邻两年 `value` 相减 |

`calc_org_new_count` 若仍 `GROUP BY` 成立年或读 `M_SVC_NEW_CNT`，按 `[SERVE]` 整段替换。

## 口径定义

圈定池 `svc_org_circle` 内，按工商成立年计的年度新增家数。新增 = `YEAR(dwd_org_base_info.incorporation_date)`。无成立日跳过。全库一条按年序列，不按领域切开。「首次开展服务」无源，不进本条。环比由页面用相邻两年差，不入库。旧号 `M_SVC_NEW_CNT` 不再承担本序列。不用空壳表 `svc_new_org_stat`。

## 计算公式

### [SEED] 仅 svcseed / GDF

```sql
INSERT INTO demo_gkxlumenx_ads.svc_metric_series (metric_id, period, value)
SELECT 'M_SVC_ORG_NEW_COUNT' AS metric_id,
       CAST(YEAR(o.incorporation_date) AS CHAR) AS period,
       COUNT(*) AS value
FROM demo_gkxlumenx_dwd.svc_org_circle c
INNER JOIN demo_gkxlumenx_ods.dwd_org_base_info o ON o.org_id = c.org_id
WHERE o.incorporation_date IS NOT NULL
GROUP BY YEAR(o.incorporation_date);
```

SEED 禁止：`metric_id` 写成 `M_SVC_NEW_CNT`；写入 `svc_new_org_stat`；`GROUP BY field_id`；把 `incorporation_*` 拷进 `svc_org_circle`。

### [SERVE] 前端 → Java REST → Python `/internal`

```sql
SELECT period, value
FROM demo_gkxlumenx_ads.svc_metric_series
WHERE metric_id = 'M_SVC_ORG_NEW_COUNT'
ORDER BY period;
```

SERVE 禁止：`JOIN` ODS；`JOIN svc_org_circle`；`GROUP BY` 成立年；`WHERE metric_id='M_SVC_NEW_CNT'`；只取近 5 年。

### [PAGE]

```text
yoy(year) = value(year) - value(year-1)
```

不写库，不另开 `metric_id`。

## 源库表字段

- 人口（SEED）：`demo_gkxlumenx_dwd.svc_org_circle.org_id`
- 成立日（仅 SEED JOIN）：`demo_gkxlumenx_ods.dwd_org_base_info.incorporation_date`
- 线上读（SERVE）：`demo_gkxlumenx_ads.svc_metric_series.metric_id / period / value`

## 待建表字段

无。领域切片以后另说（本表无 `slice_key`）。

## 参考文献 / 依据

`SVC-ALGO-STAT-21-L01` 序号 2；`storage/SVC/etl/ods-to-ads-mapping.md` A4。

## 更新记录

- 2026-08-21: 初版，模拟王惠调研产出
- 2026-10-13: 钉死工商成立年、全库一条按年
- 2026-10-13: formula 拆成 [SEED]/[SERVE]/[PAGE] 可执行 SQL，版本 0.2.1

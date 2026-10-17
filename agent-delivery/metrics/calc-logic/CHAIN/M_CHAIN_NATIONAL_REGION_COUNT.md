# 全国分布区域数（M_CHAIN_NATIONAL_REGION_COUNT）

## 基本信息

- 指标ID: M_CHAIN_NATIONAL_REGION_COUNT / 指标名称: 全国分布区域数
- 一级模块: 产业链分析；二级模块: 产业链全景；三级模块: 全国布局
- 更新频率: 日
- 对齐状态判定: 已对齐（0.2.0；2026-10-14 human:徐滕强 拍板）
- 关联Q编号: CHAIN-P0-5（挂链明细/桥灌数缺口）

## 口径定义

指定产业链的链上主体总部所在**省级行政区**去重数。链维 KPI，随链切换。

与 GLOBAL/SZ 同族三级自洽：GLOBAL=国家粒度（34 全集之上）、本条=省级粒度、SZ=深圳区县粒度。

| 项 | 锁定值 |
|---|---|
| 全集 | 全国 34 省级行政区（23 省 + 5 自治区 + 4 直辖市 + 港澳台），**不做选省过滤**（现稿 `scope='national'` 为无源伪条件，已删） |
| 真源 | dwd.enterprise_industry_chain（目标桥，现 0 行）/ dwd_org_industry_tags（过渡桥，228 万）→ dwd_org_base_info.province |
| 去重 | 主体先按 org_id 挂链，再对 province 去重计数 |
| 空值 | 空 province **不计数**（防虚高；不设「未分配」桶——省级层跟随全国字典，非 SZ 区县层先例） |
| 简称归一 | 自治区简称（新疆/广西/内蒙古/宁夏）按主档原值计数；归一全称走 **ETL 清洗项**，不进口径公式 |
| 港澳台 | 按主档 province 原值处理（现网 0 行） |
| 下钻 | 市级为下钻维度，不另开 metric_id |
| 当前真数 | 0（桥 0 行；灌数后即出真数），如实 0 + ⚠️ |

### 值域实核记录（2026-10-14 demo）

`dwd_org_base_info` 18.9 万行：province distinct=30；标准「×省」21 个 + 直辖市/自治区；残缺值：`新疆`(5)/`广西`(4)/`内蒙古`(3)/`宁夏`(2)；空串 1 行。残缺值本身仍是独立省级区划（仅命名不标准），计数不误——归一为 ETL 清洗项（D2 注记）。

## 计算公式

```sql
SELECT COUNT(DISTINCT b.province) AS prov_region_cnt
FROM demo_gkxlumenx_dwd.enterprise_industry_chain e
JOIN demo_gkxlumenx_ods.dwd_org_base_info b ON b.org_id = e.org_id
WHERE e.chain_code = :chain AND e.is_deleted = 0
  AND b.province IS NOT NULL AND b.province != '';

-- 过渡桥版（tags 228 万；credit_code ↔ external_id）
SELECT COUNT(DISTINCT b.province) AS prov_region_cnt
FROM demo_gkxlumenx_ods.dwd_org_industry_tags t
JOIN demo_gkxlumenx_ods.dwd_org_base_info b ON b.external_id = t.credit_code
WHERE t.industry_code = :chain
  AND b.province IS NOT NULL AND b.province != '';
```

禁止：`scope='national'` 伪条件；空 province 计数；公式内写 REPLACE 归一映射（走 ETL）；ads 壳；`dwd_org_reg_info`（未在现网确认）。

## 源库表字段

- dwd.enterprise_industry_chain / ods:dwd_org_industry_tags（国内桥）
- dwd_org_base_info（province 省级区域轴；org_id/external_id 双键）

## 参考文献 / 依据

CHAIN-METRIC-COVER-STAT-L01；G2 证据卡 §2；2026-10-14 demo province 值域实测；2026-10-14 human:徐滕强 拍板（省级默认粒度 + 空值不计数 + 简称 ETL 归一）。

## 更新记录

- 2026-08-21: 初版（模拟王惠调研；省市粒度混写 + scope 伪条件 + 老表漂移）
- 2026-10-14: 0.2.0 口径钉死（省级默认、市级下钻不另开 ID；空值不计数；简称 ETL 归一；province 值域实核入 D2 注记）；补矩阵行 aligned/D3=none。

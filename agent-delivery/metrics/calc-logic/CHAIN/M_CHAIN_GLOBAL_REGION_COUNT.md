# 全球分布区域数（M_CHAIN_GLOBAL_REGION_COUNT）

## 基本信息

- 指标ID: M_CHAIN_GLOBAL_REGION_COUNT / 指标名称: 全球分布区域数
- 一级模块: 产业链分析；二级模块: 产业链全景；三级模块: 全球布局
- 更新频率: 日
- 对齐状态判定: 已对齐（0.2.0；2026-10-14 human:徐滕强 拍板）
- 关联Q编号: CHAIN-P0-7（海外主体↔链挂接缺失，供应方待复）；Q-SVCCHAIN-07（全球名录待接入，SVC 先例挂点）

## 口径定义

指定产业链的链上主体（企业+机构）总部所在国家/地区去重数。链维 KPI，随链切换。

| 项 | 锁定值 |
|---|---|
| 语义 | 链上主体总部国家去重数（目标态含海外） |
| 现阶段实现 | **只算国内档**：国内主档现网全为中国 → 有链上主体即计 1（CN） |
| 国内桥 | dwd.enterprise_industry_chain（现 0 行）；过渡 dwd_org_industry_tags（228 万，credit_code ↔ external_id） |
| 当前真数 | 0（国内桥 0 行 → 无链上主体；如实 0 + ⚠️） |
| UI 呈现 | SVC GLOBAL 模式：「全球数据待接入」⚠️ 提醒常显，不造海外数 |

### 海外档缺口（保留描述，暂不实现）

海外主体库在库但**无产业链挂接概念**（2026-10-14 live 实核）：

- `dwd_forg_base_info`（国外企业）20,000 行，country_code 有值（GB 19,832 / US 159 / CA 9）但 `country` 列全空——用 code 不用 name
- `dwd_forg_research_org_info` + `dwd_forg_university_org_info`（院所/高校）合计覆盖 **222 国**
- 挂接缺失证据：forg_base_info.industry_code 为 4 位 SIC 行业码（7010/8299/…），**0 条 INB 链码**；院所/高校表无任何行业码字段

**拍板**（human:徐滕强 2026-10-14）：formula 不写海外 UNION（防后续实现误导）；海外档语义预留，待 CHAIN-P0-7 供应方明确挂接交付后再扩入公式。

## 计算公式

```sql
-- 现阶段国内档（唯一实现版）
SELECT COUNT(DISTINCT 'CN') AS global_region_cnt
FROM demo_gkxlumenx_dwd.enterprise_industry_chain
WHERE is_deleted = 0;
-- 桥有数即恒 1（CN）；当前桥 0 行 → 真数 0

-- 过渡桥版（tags 228 万）
SELECT COUNT(DISTINCT 'CN') AS global_region_cnt
FROM demo_gkxlumenx_ods.dwd_org_industry_tags t
JOIN demo_gkxlumenx_ods.dwd_org_base_info b ON b.external_id = t.credit_code
WHERE t.industry_code = :chain;
```

禁止：formula 写海外 forg UNION（现无挂接概念，写即误导实现）；province 代理国家粒度；造海外区域假数；`scope='global'` 伪条件；ads 壳。

## 源库表字段

- dwd.enterprise_industry_chain / ods:dwd_org_industry_tags（国内桥）
- dwd_org_base_info（国内主档；现网全为中国）
- 海外（缺口侧，暂不进公式）：dwd_forg_base_info（country_code）/ dwd_forg_university_org_info + dwd_forg_research_org_info（country，222 国）

## 参考文献 / 依据

CHAIN-METRIC-COVER-STAT-L01；G2 证据卡 §1；SVC `M_SVC_PT_GLOBAL_TOTAL` 全球档模式先例；2026-10-14 live forg 族实核记录；2026-10-14 human:徐滕强 拍板（现阶段只算国内 + formula 不体现海外 UNION）。

## 更新记录

- 2026-08-21: 初版（模拟王惠调研；region_code/scope 伪字段 + 老表漂移）
- 2026-10-14: 0.2.0 口径钉死（语义=链上主体总部国家去重数；现阶段国内档 CN 恒 1）；发现并实核海外主档族（2 万企业 3 国 + 222 国院所高校，零挂接）；开 CHAIN-P0-7；补矩阵行 aligned/D3=none。

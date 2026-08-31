# 企业总数（M_ENT_TOTAL_COUNT）

> 口径真源：王惠《企业分析模型指标字段清单》20260816 底稿（业务定义）→ 2026-08-27 `ENT-SYNTH-METRIC-COVER-STAT-L01` 按架构师口头：部分统计国内+国外一起算，本条按 **国内 ∪ 国外主档** 重写。
> 维护：data-agent · 8 件套摘要见 `cfg_metric-ENT-seed.yaml`。

## 元数据

- **指标ID**：`M_ENT_TOTAL_COUNT`
- **指标名称**：企业总数
- **一级模块**：企业分析
- **二级模块**：企业总览
- **三级模块**：企业整体概况
- **更新频率**：日
- **对齐状态**：已对齐（业务定义）；计算表已改挂项目 DWD；统计范围含国外主档
- **是否在数据库**：国内 ODS 有样例行；国外企业主档 `dwd_forg_base_info` 现网 **0 行**（2026-08-27 live `gkx`）；项目 DWD 待 GDF 灌数（D4 仍 mock）
- **是否在需求文档**：是
- **是否在原型页面**：是
- **是否在原型代码**：是
- **关联Q编号**：Q-E32

## 口径定义

在选定的未来产业范围内，国内机构 ∪ 国外机构按企业去重的数量。

- 国内：一企一码（统一社会信用代码）；`enterprise_base.enterprise_code` 与 `org_id` 1:1，对不上 drop。
- 国外：`enterprise_forg_base.enterprise_code` 为当地官方注册码；计算键同样是源表 `org_id`，不重新生成。
- 港澳台 **不等于** 国外，不并入本条国外侧。
- 国外高校 / 科研表（`dwd_forg_university_org_info` / `dwd_forg_research_org_info`）不是企业主档，不计入。

统计窗口：最新批次。去重：`COUNT(DISTINCT org_id)`，国内 ∪ 国外 UNION（两边 `org_id` 命名空间不同，UNION 即可）。

## 计算逻辑说明

未选产业（全量）：

```
COUNT(DISTINCT org_id)
FROM (
  SELECT org_id FROM enterprise_base
  UNION
  SELECT org_id FROM enterprise_forg_base
)
```

选定未来产业：

```
1. 国内：enterprise_industry_chain 按 chain_code / chain_name 过滤后 JOIN enterprise_base
2. 国外：无上链表（无 enterprise_forg_industry_chain），暂不能按产业并入
3. 计数：仅国内过滤结果的 COUNT(DISTINCT org_id)
```

现网 ODS 无 `dwd_org_industry_chain_dtl`；`enterprise_industry_chain` 不能用 tags 冒充正式链位。

对应 seed `formula`：COUNT(DISTINCT org_id) FROM (enterprise_base UNION enterprise_forg_base)；选产业时国内经 industry_chain 过滤，国外暂不纳入。

**计算公式文件**：`M_ENT_TOTAL_COUNT.md`

## 源表字段

8 件套 `source_tables` 写 **项目 DWD ← ODS** 血缘链（左端必须是 `gkxlumenx_dwd` 表，右端 ODS 表名不带 `gkx.`）：

```
enterprise_base <- ods: dwd_org_base_info
enterprise_forg_base <- ods: dwd_forg_base_info
enterprise_industry_chain <- ods: dwd_org_industry_tags
```

现网探针：国内主档有数；国外主档 `dwd_forg_base_info` 0 行；tags 非正式链位。计算 FROM 只用左端 DWD。

来源系统（`source_systems`）：国内机构要素库、国外机构要素库、产业链要素库。

## 待建 / 缺口

- 国外企业主档 live `gkx.dwd_forg_base_info` = 0 行（2026-08-27）；公式可 UNION，数灌不上。
- 国外无上链表：选未来产业时国外侧暂不能并入。
- ODS 无 `dwd_org_industry_chain_dtl`；tags 不能当正式链位。
- D3 维持 `pending_ods`；D4 维持 mock（`is_mock: true`）。

## 备注

bid `§1.1.1.2.4.2.3`；STAT。禁止把 `gkx.dwd_*` 写入 `source_tables` 主体。

---
*王惠 20260816 Excel 底稿正式化 2026-08-18；2026-08-26 改挂项目 DWD；2026-08-27 国内∪国外主档（COVER-STAT-L01）*

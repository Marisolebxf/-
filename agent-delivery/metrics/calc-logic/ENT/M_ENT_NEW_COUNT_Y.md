# 历年新增企业数（M_ENT_NEW_COUNT_Y）

> 口径真源：王惠《企业分析模型指标字段清单》20260816 底稿（按注册年分组）→ 2026-08-27 `ENT-SYNTH-METRIC-COVER-STAT-L01` 按架构师口头：有对等主档且国外有注册日，本条 **国内 ∪ 国外** 一起算。
> 维护：data-agent · 8 件套摘要见 `cfg_metric-ENT-seed.yaml`。

## 元数据

- **指标ID**：`M_ENT_NEW_COUNT_Y`
- **指标名称**：历年新增企业数
- **一级模块**：企业分析
- **二级模块**：企业总览
- **三级模块**：企业整体概况
- **更新频率**：日
- **对齐状态**：已对齐（业务定义）；计算表已改挂项目 DWD；统计范围含国外主档
- **是否在数据库**：国内 ODS 有样例行；国外企业主档 `dwd_forg_base_info` 现网 **0 行**（2026-08-27 live `gkx`）；项目 DWD 待 GDF 灌数（D4 仍 mock）
- **是否在需求文档**：是
- **是否在原型页面**：否（demo 以别名 `M_ENT_NEW_COUNT` 展示近 12 月窗口）
- **是否在原型代码**：是
- **关联Q编号**：Q-E32

## 口径定义

按注册年份分组的新登记企业数（国内机构 ∪ 国外机构），并给出累计 `cumulative_count`。

- 国内：一企一码；计算键 `org_id`，与 `enterprise_base.enterprise_code`（信用代码）1:1，对不上 drop。年份 = `YEAR(enterprise_base.registration_date)`。
- 国外：计算键同样是源表 `org_id`，不重新生成。年份 = `YEAR(enterprise_forg_base.registration_date)`。项目 DWD 国外表另有 `incorporation_year`，本条不混用，统一用日期派生，与国内同一套公式。
- 港澳台 **不等于** 国外，不并入国外侧。
- 国外高校 / 科研表不是企业主档，不计入。
- **不按产业过滤**（与企业总数「选产业」不同；本条是历年全量新登记）。

`registration_date` 为空的企业不进该年分组。

## 计算逻辑说明

```
1. 国内：enterprise_base，registration_date 非空；年 = YEAR(registration_date)
2. 国外：enterprise_forg_base，registration_date 非空；年 = YEAR(registration_date)
3. UNION 后 COUNT(DISTINCT org_id) GROUP BY 年份
4. 按年排序后计算累计 cumulative_count
```

对应 seed `formula`：COUNT(DISTINCT org_id) FROM (enterprise_base UNION enterprise_forg_base) GROUP BY YEAR(registration_date)，并计算累计 cumulative_count。

**计算公式文件**：`M_ENT_NEW_COUNT_Y.md`

## 源表字段

8 件套 `source_tables` 写 **项目 DWD ← ODS** 血缘链（左端必须是 `gkxlumenx_dwd` 表，右端 ODS 表名不带 `gkx.`）：

```
enterprise_base.registration_date <- ods: dwd_org_base_info.incorporation_date
enterprise_forg_base.registration_date <- ods: dwd_forg_base_info.incorporation_date
```

计算 FROM 只用左端 DWD。两边 ODS 字段名都是 `incorporation_date`，落到 DWD 都是 `registration_date`。

来源系统（`source_systems`）：国内机构要素库、国外机构要素库。

## 现网探针（live `gkx`，2026-08-27；不进 8 件套）

- 国内 `dwd_org_base_info`：40000 行 alive；`incorporation_date` 非空 39967；另有 `incorporation_year` 非空 19987（国内 DWD 无该列，不用它算）。
- 国外 `dwd_forg_base_info`：0 行。表上有 `incorporation_date` / `incorporation_year`，公式可 UNION，数灌不上。
- 不升 D3 `full` / D4 `live`。

## 待建 / 缺口

- 国外企业主档 live 0 行；GDF 未灌项目 DWD 前 `is_mock: true`。
- D3 维持 `pending_ods`；D4 维持 mock。

## 备注

bid `§1.1.1.2.4.2.3`；STAT。禁止把 `gkx.dwd_*` 写入 `source_tables` 主体。

---
*王惠 20260816 Excel 底稿正式化 2026-08-18；2026-08-27 COVER-STAT-L01 按注册日 UNION 国外主档*

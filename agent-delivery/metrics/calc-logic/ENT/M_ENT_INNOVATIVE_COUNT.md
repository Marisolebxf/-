# 创新型企业数（M_ENT_INNOVATIVE_COUNT）

> 口径真源：王惠《企业分析模型指标字段清单》20260816 底稿（四类并集）→ 2026-08-27 `ENT-SYNTH-METRIC-COVER-STAT-L01` 按国内外尺子回看：无对等国外标签表，本条只国内。
> Q011 仍 🟡 待甲方；团队临时默认采用王惠四类，不升 🟢。
> 维护：data-agent · 8 件套摘要见 `cfg_metric-ENT-seed.yaml`。

## 元数据

- **指标ID**：`M_ENT_INNOVATIVE_COUNT`
- **指标名称**：创新型企业数
- **一级模块**：企业分析
- **二级模块**：企业总览
- **三级模块**：企业整体概况
- **更新频率**：日
- **对齐状态**：未对齐（Q011）；计算表已改挂项目 DWD；统计范围只国内
- **是否在数据库**：live ODS 标签有样例行；项目 DWD 待 GDF 灌数（D4 仍 mock）
- **是否在需求文档**：是
- **是否在原型页面**：是
- **是否在原型代码**：是
- **关联Q编号**：Q011

## 口径定义

创新型企业数量。甲方口径待 Q011 确认。团队临时默认（王惠底稿）：专精特新 ∪ 小巨人 ∪ 制造业单项冠军 ∪ 创新型中小企业，四类标签并集后按企业去重。

- 只国内。项目 DWD 无 `enterprise_forg_tag`，live ODS 无 `dwd_forg_*tag*`，**不造表**。有对等国外标签表后再 UNION。
- 港澳台 ≠ 国外。国外高校 / 科研表不是企业主档，也不走本条。
- 业务一企一码；计算键 `org_id`，与 `enterprise_base.enterprise_code`（信用代码）1:1，对不上则 drop。
- 不含高企 / 瞪羚 / 独角兽（与 Q011 题面不同，以王惠底稿为准，待甲方）。

## 计算逻辑说明

未选产业：

```
1. enterprise_tag 按 tag_name 含：专精特新 / 小巨人 / 制造业单项冠军 / 创新型中小企业（OR 并集）
2. JOIN enterprise_base USING org_id
3. COUNT(DISTINCT enterprise_base.org_id)
```

选定未来产业：

```
1. 国内：上一步结果再经 enterprise_industry_chain 按 chain_code / chain_name 过滤
2. 国外：无标签表、无上链表，不并入
3. 计数：仅国内过滤结果
```

现网 ODS 无 `dwd_org_industry_chain_dtl`；`enterprise_industry_chain` 不能用 tags 冒充正式链位。

对应 seed `formula`：COUNT(DISTINCT org_id) FROM enterprise_tag JOIN enterprise_base WHERE tag_name 含四类（并集）；选产业时国内经 industry_chain 过滤。国外无标签表不并入。

**计算公式文件**：`M_ENT_INNOVATIVE_COUNT.md`

## 源表字段

8 件套 `source_tables` 写 **项目 DWD ← ODS** 血缘链（左端必须是 `gkxlumenx_dwd` 表，右端 ODS 表名不带 `gkx.`）：

```
enterprise_tag <- ods: dwd_org_tech_tag
enterprise_base <- ods: dwd_org_base_info
enterprise_industry_chain <- ods: dwd_org_industry_tags
```

计算 FROM 只用左端 DWD。`dwd_org_tech_tag.org_tag`（中文）落到 `enterprise_tag.tag_name`；GDF 派单包里 demo ODS 的 `dwd_org_tag_info` 现网 live `gkx` **没有这张表**，本条不改挂。

来源系统（`source_systems`）：国内机构要素库、产业链要素库。

## 现网探针（live `gkx`，2026-08-27；不进 8 件套）

- `dwd_org_tech_tag`：20000 行，`is_deleted=0` 全量；42 个 `org_tag`；18215 个 `org_id`。
- 四类中文在 ODS 有样例（含「省级/国家级」前缀；也有「曾获」「过期」变体）。当前 formula 用 **含**，会算进曾获/过期；字典未冻结前不收窄。
- 无国外标签表。`dwd_forg_base_info` 有表但不是本条计算源。
- 高企 / 瞪羚 / 独角兽在 ODS 也有标签，本条不计入。

## 待建 / 缺口

- D1 仍 draft（Q011）。D3 维持 pending_ods；D4 维持 mock（`is_mock: true`）。不因 ODS 有样例行升 full/live。
- 标签字典未冻结：四类中文命中、是否排除「曾获/过期」、tag_code 编码待 GDF/字典确认。
- 国外有对等标签表后再评估是否 UNION，本波不造 `enterprise_forg_tag`。

## 备注

bid `§1.1.1.2.4.2.3`；STAT。禁止把 `gkx.dwd_*` 写入 `source_tables` 主体。

---
*王惠 20260816 Excel 底稿正式化 2026-08-18；2026-08-27 COVER-STAT-L01 按国内外尺子回看只国内（无国外标签表）*

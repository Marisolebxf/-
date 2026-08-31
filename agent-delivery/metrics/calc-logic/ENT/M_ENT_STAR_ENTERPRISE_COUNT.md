# 明星企业数（M_ENT_STAR_ENTERPRISE_COUNT）

> 口径真源：Q048 PARTITION-L01 → 2026-08-31 `ENT-SYNTH-METRIC-COVER-STAT-L01`。  
> 「共 N 家」= 对 CMS 已发布名单的 APP COUNT，非算法 TopN。  
> **明星 ≠ 重点**（重点走 `M_ENT_KEY_TOTAL` 专利≥50）。Q048 / Q041 仍 🟡。  
> 维护：data-agent · 8 件套摘要见 `cfg_metric-ENT-seed.yaml`。

## 元数据

- 指标ID：`M_ENT_STAR_ENTERPRISE_COUNT`（不改名 `STAR_ROSTER_COUNT`）
- 名称：明星企业数
- 模块：E-34 / 门户「共 N 家」
- 更新频率：日（随 CMS 拉取）
- 关联Q：Q048（名单）；Q041（CMS 字段/授权，同名单）

## 口径定义

对 CMS `content_type=star_roster_item` **已发布**名单，按 `enterprise_code` 去重计数。

```
本条 = COUNT(DISTINCT enterprise_code)
FROM star_roster_item
WHERE 只收已发布
```

- 选产业 / 选集群是 API（按 `future_industry_code` / `cluster_id` 过滤后再 COUNT）。不把「当前所选产业」写进 8 件套。
- 名单里有谁算谁。本条不自己 UNION 国内外。
- 未发布 / 草稿 / 归档：**不进**。
- `sort_order`、入选理由、标准正文是 CMS，不进本条公式。
- **禁止** `M_ENT_KEY_TOTAL` / 专利≥50 当明星。
- **禁止** `enterprise_tag.tag_code='star_enterprise'`。
- **禁止** `dwd_org_honor_info` / `is_star` / 荣誉名含「明星」。
- **禁止**竞争力 / 推荐 TopN。
- **禁止**把 Q037 空态推荐 ≤30 当成「共 N 家」。

8 件套只留这条 COUNT。`publish_status` 只写在口径「已发布」，不进 `source_tables` 列清单。

## 两点分开（强制）

### ① 本条口径

公式完整：已发布名单去重家数。

### ② 当前无法执行

名单真源在 CMS（久新只读契约）。项目 DWD **无**独立名单结果表；`enterprise_star` 是配置、GDF 勿建 DWD。不拿荣誉标签顶替。Q050 联调未闭合。不进「口径未定」。

## 落表

| 角色 | 表 | 现网 |
|------|-----|------|
| 源 | CMS `star_roster_item`（契约 `CMS-read-contract-E31.md`） | 应用侧只消费已发布；不读久新内部库 |
| 目标 | `ads.ent_star_roster_count`（建议：产业键 + `star_cnt`） | **缺口：无此表** |

源 ≠ 目标。GDF 暂缓。Java 也可查询时 COUNT，仍须有建议目标名。

## 分场景 / 千万级（不进 8 件套）

- 场景 A · E-34 选择器「共 N 家」：当前产业已发布名单 COUNT。
- 场景 B · 未选产业：全量已发布去重（若产品要全球合计）。本波不把合计写进 8 件套。
- demo：固定 DEMO 名单不当接通。生产：跟 CMS 拉取；名单量级小，禁止用 ODS 全库扫冒充。

**计算公式文件**：`M_ENT_STAR_ENTERPRISE_COUNT.md`

## 源表字段

```
star_roster_item <- cms: E-34
```

无 ODS 右端。计算不 FROM `gkx.dwd_*`、不 FROM `enterprise_tag`。

来源系统：门户 CMS。

## 待建 / 缺口（不是口径没写）

1. 久新已发布名单 API（Q050）。
2. **无独立目标表**。
3. D3 / D4 本波不升。`is_mock: true`。Q048 / Q041 🟡。

## 备注

acceptance 改挂 Q048（原 `ENT-SEARCH-007` 是 SEARCH 空态错挂）。STAT。

---
*2026-08-31 COVER-STAT-L01：CMS 已发布名单 COUNT；≠ KEY_TOTAL / tag / honor / TopN；当前无法执行*

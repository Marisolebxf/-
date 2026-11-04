# 现网表状态（开工必读）

事实来自 2026-11-02 加工链路核对 + **2026-11-04** demo/正式库列与索引对照（`GDF-SVC-WORKPACK-R1A-L01`）。

| 库表 | 当时 / 现况 | 本包 |
|------|------|------|
| `gkxlumenx_dwd.svc_org_circle`、`svc_org_finance_event` | 已建；正式库曾 0 行 | 这一趟的写。结构见 `10/`。不 DROP。`finance_event` 唯一键改为 `event_id` 时用 ALTER |
| `gkxlumenx_ads.svc_org_card` 和四张指标表 | 已建 | 这一趟的写。不 DROP |
| `gkxlumenx_ods` 四表 + `dwd_org_org_product_info` | 平台贴源已承载；与供应方行数一致（round1 证据） | **本包可读**；不写 ODS |
| 谁建的正式库结果表 | 此前同步创建过 | **同意 GDF 按现存表接管**（Q11）；研发侧仍可用 demo 库 |

库名以 `demo_` 开头的库不在本趟开工写范围。七张交付表 demo 与正式库列类型/唯一索引已对照一致（除本包要求的 `event_id` 唯一键变更待 ALTER）。

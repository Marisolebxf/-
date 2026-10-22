# 对接三要素 · 对端对接文档

**只有 PM 落盘。** 对端发出的原文或导出放这里，文件名带收到日期。

监管人不往这里放文件。

## 索引

| 收到日期 | 来源方 | 文档 | 状态 |
|---|---|---|---|
| 2026-10-22 | 北京久新 | 本文「深圳国科信数据仓库只读账号」 | 已落盘。2026-10-22 只读账号测通。初始密码已从本文件撤出，不进 git |
| 2026-10-22 | 北京久新 | 数仓结构与指标计算方法 | 活文档，数据更新会同步改文档。schema **5.11.0**，提交 `345c0e02`。[ADS_SCHEMA.md](https://github.com/leonlee723/sz-gkx-data-warehouse-docs/blob/main/ADS_SCHEMA.md)。当日快照 [2026-10-22-ADS_SCHEMA-5.11.0.md](./2026-10-22-ADS_SCHEMA-5.11.0.md) |
| 2026-10-22 | 北京久新 | 各版本更新日志 | 活文档，当前最新 5.11.0（2026-10-22），提交 `fbc967ab`。[ADS_SCHEMA_RELEASE_NOTES.md](https://github.com/leonlee723/sz-gkx-data-warehouse-docs/blob/main/ADS_SCHEMA_RELEASE_NOTES.md)。当日快照 [2026-10-22-ADS_SCHEMA_RELEASE_NOTES.md](./2026-10-22-ADS_SCHEMA_RELEASE_NOTES.md) |

## 深圳国科信数据仓库只读账号

收到日期：2026-10-22。

久新提供的算法和当前数据都在数据库中。久新深圳国科信数据仓库相关信息如下。已在当前 Doris 4.1.0 实例创建只读用户：

| 项    | 值                                                |
| ---- | ------------------------------------------------ |
| 实例   | Doris 4.1.0                                      |
| 用户名  | `test2`                                          |
| 初始密码 | 不进 git。PM 另行保管 |
| 数据库  | `gkx_technology_analysis_dev`                    |

连接示例：

```text
mysql -h 47.93.119.170 -P 29030 -u test2 -p gkx_technology_analysis_dev
```

2026-10-22 用该账号测通：`SELECT 1` 成功，`version_comment` 为 `doris-4.1.0-rc03-5960d4cea0e`，库内 130 张表。结构与计算方法见上表两份 GitHub 文档。同一份连接也写在 [技术方案](../../技术方案.md) §3。字段级调研见 [调研记录](../../调研/调研记录.md)。

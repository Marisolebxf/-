# GDF-CHAIN-WORKPACK-v2

> **读者**：GDF 数据中台产线（不使用 Cursor）  
> **版本**：v2.2.6（2026-11-02 · 链树映射按真源实测重写；正式产业锚点在 Milvus 库 `gkxlumen`，集合 `gkxlumen_industry_anchor` 已建并 load、0 条，与 demo 的库 `default` 分开）· **可对外投递**  
> **承诺表真源**：`third-party-source/doc/` + `md-extract/`（产业链要素库 Sheet）  
> **Mapping 施工真源**：[09-产业链域-ETL-Mapping明细-源表到DWD.md](09-产业链域-ETL-Mapping明细-源表到DWD.md)  
> **建表 DDL 真源**：[10-DWD-MySQL-DDL/dwd-chain.md](10-DWD-MySQL-DDL/dwd-chain.md)（包内复制件，库名 `gkxlumenx_dwd`；v5 文档作废）
> **环境红线**：GDF 只读真源 `gkx` + `gkxlumenx_*` 正式库，禁读 demo（2026-11-02）  
> **本侧对接**：见 `00-派单说明书.md`

## 文件索引

| 文件 | 用途 |
|------|------|
| [00-派单说明书.md](00-派单说明书.md) | 目标、边界、Wave A/B、DoD |
| [01-命名与分层词典.md](01-命名与分层词典.md) | 命名对齐 |
| [02-WaveA-贴源表清单.yaml](02-WaveA-贴源表清单.yaml) | 贴源清单 |
| [03-连接与网络.md](03-连接与网络.md) | 连接元数据（密码线下） |
| [04-技术字段与过滤规则.md](04-技术字段与过滤规则.md) | 过滤规则 |
| [06-WaveB-Mapping派工.md](06-WaveB-Mapping派工.md) | Mapping 派工 |
| [09-产业链域-ETL-Mapping明细-源表到DWD.md](09-产业链域-ETL-Mapping明细-源表到DWD.md) | **正式 Mapping**（v2.2 重写链树） |
| [23-核对签收与答复.md](23-核对签收与答复.md) | **round1 核对签收与 20 题逐题答复** |
| [10-DWD-MySQL-DDL/](10-DWD-MySQL-DDL/) | 建表指针 |
| [11-作废与误源对照.md](11-作废与误源对照.md) | 误源对照 |
| [12-DWD后加工-产业链入向量库.md](12-DWD后加工-产业链入向量库.md) | DWD 成功后写入 Milvus 库 `gkxlumen` 的 `gkxlumen_industry_anchor`（**与上图无关**）。不写库 `default` |
| [script/](script/README.md) | 入向量库脚本。GDF 配置 `industry_embed.py`。入图两份不配置 |
| [CHANGELOG.md](CHANGELOG.md) | 版本 |

## 投递约定

- 本包已完成 Mapping 内审；下一步生成 DRAFT CDC 并由 GDF 导入核对后回签，**当前不代表已建表或已灌数**。  
- 当前通用 `parse_workpack.py` 尚未识别 CHAIN 字段矩阵（实测 Wave B=0）；自动预填前须补解析规则或由 GDF 按 09 人工配置，禁止把空 Wave B 当完成。  
- 建表认 `10` 指定真源；Mapping 只认本包 **09 明细**。  
- 密码不进本包。  
- **不要**用 Demo `gdf_sim` / `ods-to-dwd-mapping.md`（draft 模拟）当产线字段真源。

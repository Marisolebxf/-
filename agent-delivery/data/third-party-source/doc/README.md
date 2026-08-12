# 三方承诺数据源表（doc）

> **身份**：供应方/上总集**承诺交付**的要素库设计汇总（xlsx）。  
> **2026-07-31 口径**：企业方向相关源表清单以**本目录**为准（优先于仅基于 live `gkx` DDL 沙箱的推断清单）。

## 源文件（xlsx）

| 文件 | 内容域 |
|------|--------|
| `版权人才、企业机构、政策数据汇总表.xlsx` | **企业/机构**、人才、政策（国内机构 / 国外机构等） |
| `行业专题数据汇总表.xlsx` | 医药 / 化学 / 海洋 / **量子专题**（含部分企业工商簇） |
| `市场研究（金融、宏观行业、行业分析、产业链）数据汇总表.xlsx` | 金融、宏观行业、行业分析、产业链 |
| `论文、专利、项目、报告数据汇总表.xlsx` | 论文、专利、项目、报告及值域 |

## Markdown 要素库提取（便于检索）

路径：[md-extract/](md-extract/)

- **范围**：**仅** Sheet 名以「要素库」结尾（跳过场景汇总 / 需求字段 / 值域等）
- 每个 xlsx → 同名 `.md`（要素库 Sheet 单元格完整展开）
- `_csv/`：各要素库 Sheet CSV（与 MD 同内容，便于程序读）
- `_officecli-text/`：`officecli view text` 原文（**单元格值真源**）
- `_officecli-dumps/`：`officecli dump` JSON（样式 / merge；**勿**用其 import 文本当大表值真源，可能截断）
- 重跑：[`_extract_xlsx_to_md.py`](_extract_xlsx_to_md.py)（结束后会清理非要素库旧产物）

```text
py -3 agent-delivery/data/third-party-source/doc/_extract_xlsx_to_md.py
```

> outline 行数可能含尾部空行；提取结果以 nonempty 行为准。

## 与其它目录关系

| 目录 | 关系 |
|------|------|
| 本目录 `doc/` | **承诺表/字段设计真源（文档侧）** |
| `gkx-mysql-raw/` | live 库结构沙箱 + 连接；用于核验落库是否齐全 |
| `GDF/派单包/` | 对外贴源派单；企业 Wave A 表清单应对齐本目录承诺表后再定稿 |

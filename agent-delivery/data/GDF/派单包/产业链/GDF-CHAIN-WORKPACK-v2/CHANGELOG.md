# CHANGELOG — GDF-CHAIN-WORKPACK（v2 目录）

> v2 目录自 v2.0 起新记；v1.x 历史见 `../GDF-CHAIN-WORKPACK-v1/CHANGELOG.md`。

## v2.0 — 2026-10-20

- 基线对齐 **10-19 三方承诺清单**：四表全部在册、行数不变（链树 1,296 / tags 2,197,216 估 / 产品 73,313 / 资讯 94,997）。
- live 实证：`dwd_industry_chain_info` 真实含 `parent_name` 列（text）→ 09 §3.1/§3.2 加"不映射、JOIN 派生"注记；纪要所列 `t_id`/`id`/`code_company_count` **live 无此列，不作源**（Excel 说明领先于库，与 ENT v4 同一澄清）。
- 与 ENT v4.0 的拆分对称声明继续有效（按目标表拆责任；CHAIN 09 §1.3 ↔ ENT 02/09 §1.6）。
- 其余（INB 主键、B3 依赖 enterprise_base、B2 禁洗等）全部继承 v1.0。
- **全卷对齐补遗（2026-10-20 晚，审查发现）**：09 头部版本块 v1.0→v2.0 + 派单包指针改指本目录；06 派工标题 v2.0。逐卷扫描（00/02/03/04/06/09/10/11/README）：03/04/10/11 无受 10-19 变更影响引用，维持继承。

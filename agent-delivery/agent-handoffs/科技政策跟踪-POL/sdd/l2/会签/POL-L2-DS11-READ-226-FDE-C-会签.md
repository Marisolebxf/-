# 226 波次 C 会签稿

总单 `POL-L2-DS11-READ-226-FDE-L01`。起草：本会话按 B 定档回写。异议须非空。

## 已写入

见 `sdd/简报/2026-11-14-226-FDE-C-docs.md` 文件表。

## 对抗异议（本波自检 · 待监管人闭合）

| 编号 | 身份 | 问题 | 依据 | 建议 | 起草回应 |
|---|---|---|---|---|---|
| C-1 | arch | display「不直连 Python」与 Feign 到 Python 的表述是否冲突 | ARCH 铁律 + 本次 mermaid | 统一写成「经 Feign/内部客户端，浏览器不直连」 | **采纳**：ARCH 已改为「不直连 Python（经 Feign/内部客户端）」 |
| C-2 | data | 新表是否触 D16：有行才展示 vs 空表点生成 | D16 / DATA §5 | 空表允许点生成后 UPSERT；不是预灌 mock 行 | **采纳**：用例写「无缓存则点【智能摘要】」；不要求预灌 |
| C-3 | api | `policy_text_parse` jobs 键是否删白名单 | API §2 | 保留键给名单/其它，但 226 卡不走它 | **采纳**：API 已写明「不再作为 226 三区块正文口」 |
| C-4 | algorithm | D4 仍 mock 但已真 LLM，评审是否误以为 live | METRIC D4 | 明确：结果进 gapfill，D4 不升 live | **采纳**：METRIC/说明书已写 D4=mock |
| C-5 | product | 推送仅会话态，刷新丢失是否需规「推送管理层」不够 | 需规 226 / 决策卡推送 1 | 中档按决策卡；真消息中心另开 | **采纳**：会签记录中档边界；不升档 |

## 待签收

请监管人确认异议表已闭合后，开波次 D（data migration → algorithm → api → frontend）。

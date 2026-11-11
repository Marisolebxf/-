# 简报 · 214 优缺点改实时 LLM（不写 gapfill）

- 日期：2026-11-12
- 监管人纠偏：优缺点须对比时调 LLM 生成并直回 UI；不应经 gapfill

## 结论

废止「空则 LLM 写 `gapfill_policy_detail_compare` 再回读」。改为 Job `policy_detail_pros_cons` 读 DWD 正文 → LLM → `result_payload.items[].pros_text/cons_text` 直回；FE 用 `mapProsConsPayload` 填列。条件/材料仍可读 gapfill 附带列。

## 改动

| 仓 | 要点 |
|---|---|
| `lumen-algo-py` | `detail_pros_cons_job` 去掉读写 gapfill；板含正文；`harness_mode=detail_pros_cons_llm` |
| `lumen-ui-science-pc` | 开始对比必起 Job；指纹 `policy-detail-pros-cons-live:`；不从 detail 取优缺点 |
| ARCH / 合规用例 | §5.2 与 214 行期望已回写 |

## 自检

- `pytest tests/test_detail_pros_cons_job.py` 3 passed
- `node FE-POL-CMP-LIVE.test.mjs` 全绿

## 待发

Python + 前端需同发；前端仓待人工确认推送。

# POL-L2-DS10-CMP-PROS-LLM · E 波次 · 用例与自检

- 总单：`POL-L2-DS10-CMP-PROS-LLM-L01`
- 日期：2026-11-12

## 合规用例

已改 `POL-L2-DS10-CMP-合规演示用例.md` 214 行：
- 空优缺点路径：`POST .../jobs` `sub_type=policy_detail_pros_cons`
- 形态：列头/图例/总结为政策名称，禁「政策 #id」
- 已灌样例仍验冻结文案（Job 跳过）

## 自检证据

| 项 | 结果 |
|---|---|
| `FE-POL-CMP-LIVE.test.mjs` | 全绿 |
| `pnpm type-check`（lumen-ui-science-pc） | 绿 |
| `tests/test_detail_pros_cons_job.py` | 3 passed |
| Java 白名单单测 | 已扩（display + PolicyAnalysisTypes）；CI 跑 |

## §6.5 冒烟（待 CI 发版后）

1. 打开政策详情对比，选两策（其一标题较长），点开始对比 → 列头不得出现「政策 #」。
2. 对优缺点空的政策 → 对比后出现优点/缺点或诚实空态（无密钥）。
3. 已灌 `18363390`/`18407696` → 仍见冻结优缺点文案。

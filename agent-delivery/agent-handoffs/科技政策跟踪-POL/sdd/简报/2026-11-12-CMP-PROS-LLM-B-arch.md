# POL-L2-DS10-CMP-PROS-LLM · B 波次 · arch

- 总单：`POL-L2-DS10-CMP-PROS-LLM-L01`
- 日期：2026-11-12
- 档位：**中档**成立
- 子类型锁定：`policy_detail_pros_cons`

## 裁定

1. 调用链：FE → `POST /display/v1/policy/panorama/jobs` → topic-async → `POST /internal/policy/jobs/execute` → Python LLM → 写 `gapfill_policy_detail_compare` → FE 再 `GET .../detail`。
2. 空判定：该政策 `pros_text` 与 `cons_text` 去空白后皆空才生成；任一非空则跳过（不覆盖）。
3. 无密钥 / LLM 失败：不写假文；读面仍空；D4 仍 mock。
4. 不新表、不改主键；条件/材料列缺省写空串（INSERT）或不改（UPDATE 仅优缺点）。
5. 展示名：业务 DOM 禁止「政策 #」+ id。

## 白名单同步点

- `PolicyPanoramaService.JOB_SUB_TYPES`（display 放行）
- `PolicyAnalysisTypes.CANONICAL`（async 放行，跳过产业 VID XOR）
- `polan.job.JOB_SUB_TYPES` + `_NO_INDUSTRY_XOR`

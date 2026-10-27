# POLICY-SSB-DEMO-INGEST-L01

ponytail: full

## 范围

政策 Mock 页增加按钮「固态电池政策」。点击后把 `ssb-web-harvest` 已收录的 8 条追加进 Demo 库：国内 7 条进 `demo_gkxlumenx_ods.dwd_policy_base`，日本 1 条进 `dwd_global_policy_base`，再按 id 追加进 `demo_gkxlumenx_dwd.policy_base_info`。`policy_id` 用清单 id，`source=web-solid-battery`，`source_plane` 为 domestic / global。已存在的 id 跳过。不清空，不跑 replace，不跑全量重建。

## 偏离

验收要求 `source=web-solid-battery` 不少于 1000 条。公开原文只核到 8 条，本按钮只灌这 8 条，不补造。日本 `gl-meti-20220831` 原文页 403，正文空，只入库题录。任务因此停在 `in_progress`，不进待签收。

## 产物

- `repos/demo-ui-system-test`：`src/views/policy/pages/PolicyMockPage.vue`，`src/api/policy/index.ts`
- `repos/demo-algo-ent-analysis`：`polan/mockgen/ssb.py`，`polan/mockgen/ssb_data/`，`api/policy_routes.py` 的 `POST /v1/policy/mock/solid-battery`
- 清单正文：`agent-delivery/data/POLICY/ssb-web-harvest/content/`

## 验收

`python -m polan.mockgen.ssb`：第一次国内 7、国外 1、DWD 8；第二次全部跳过。`python -m polan.mockgen.incr` 仍通过。未对运行中的 Demo 页面点击（新接口尚未发布）。

## 架构合规

- 调用链：Mock 页 → `POST /policy/v1/policy/mock/solid-battery` → Python。前端不直连库。
- 只写 `demo_gkxlumenx_*`。`is_live(policy)` 为真则拒绝。
- 不写 `gkx`，不写正式 `gkxlumenx_*`，不打开 WBS-06-03G。
- 图谱未改。本按钮不算 ADS。

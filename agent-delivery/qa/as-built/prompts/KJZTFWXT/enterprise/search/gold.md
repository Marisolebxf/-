# 企业查询 P0 五条金样 · 执行提示词

先读 `prompts/_result.md` 与 `scripts/KJZTFWXT/enterprise/search/gold.yaml`。

全量 P0/P1 正向不要用本文件，改用 `prompts/KJZTFWXT/enterprise/search/full.md`。

环境：https://edu.itic-sci.com/tts/svcz/  
账号：`fixtures/testdata.yaml`  
顺序：**P0-01 → P0-02 → P0-03 → P0-04 → P0-05**（后者依赖结果列表）。

登录：若已在 `/enterprise/enterprise-search` 则不要反复登出。未登录则填 admin / 123456 点「登录」。

P0-02：只点示例「人工智能」，**不要**接着点搜索。  
P0-03：再点「搜索」，等「智能搜索结果」。  
P0-04：点第一张卡的企业名称按钮。  
P0-05：点「指标说明：综合竞争力得分」。

每条独立目录：`runs/{run-id}/scripts/P0-0x/`。最后写 `SUMMARY.md`。

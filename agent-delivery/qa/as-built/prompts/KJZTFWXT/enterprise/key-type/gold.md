# 重点企业类型分析 P0 五条金样 · 执行提示词

先读 `prompts/_result.md` 与 `scripts/KJZTFWXT/enterprise/key-type/gold.yaml`。

全量 P0/P1 不要用本文件，改用 `prompts/KJZTFWXT/enterprise/key-type/full.md`。

环境：https://edu.itic-sci.com/tts/svcz/  
账号：`fixtures/testdata.yaml`  
顺序：**P0-01 → P0-02 → P0-03 → P0-04 → P0-05**。

登录：若已在业务页且 URL 不含 `/login` 则不要反复登出。未登录则填 admin / 123456 点「登录」。

P0-01：侧栏「企业分析」→「重点企业类型分析」。不要点「重点企业领域分析」。若对比篮浮层挡住主区，先关。`ent_review_mode` 默认可能为 true，本条末关掉，方便后续业务态。  
P0-02：只核四组筛选默认，不要改条件。  
P0-03：三张 KPI；0 家记 observed，不 Fail。  
P0-04：默认地图 → 列表 → 再回地图。  
P0-05：点「查看企业清单（N）」；抽屉断言只在 `.arco-drawer` 内。

每条独立目录：`runs/{run-id}/scripts/P0-0x/`。最后写 `SUMMARY.md`。

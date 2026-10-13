# P1-05 · 未开通付费权益的账号在报告中下载入口禁用（00397）

1. 承接 P1-04 报告打开态（同链路，减少开关）。
2. snapshot 核验：「导出」button ref e80 states `[disabled]`。
3. CDP 复核：`exportBtn.disabled === true`。
4. 账号口径：persona 按钮（ref e0）文案含「未付费」徽标 → admin 未开通付费权益。
5. P1-04 已点「返回分析结果」关闭报告（无残留态）。

判定：唯一预期（下载入口禁用）成立 → Pass。

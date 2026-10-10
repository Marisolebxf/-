# P0-01 侧栏进入类型分析，URL 含 type，不落到领域看板

1. S1 goto `http://111.198.38.90:50892/` → 已登录，落到 `/enterprise/enterprise-search`，URL 不含 `/login`。
2. S2 login_if_needed：跳过（未登出）。
3. S3 侧栏「企业分析」已展开，点「重点企业类型分析」；未点「重点企业领域分析」。
4. 落地 URL：`/enterprise/key-enterprise-analysis?workspace=type&view=type`。H1「重点企业类型分析」。region「类型分析筛选」可见。主区无「尚未选择分析对象」「待选择分析对象」「前往对比篮选择企业」。
5. S4 「关闭对比篮」不可见（仅「打开对比篮，共 2 项」浮钮），未点。
6. S5 点顶栏人设。
7. S6 「内部评审模式」为开，点关；`localStorage ent_review_mode=false`。
8. S7 Escape 收起人设。
9. S8/S9 落盘 snapshot.yml。

判定：pass。

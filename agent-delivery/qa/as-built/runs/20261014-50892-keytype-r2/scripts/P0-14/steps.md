# P0-14 · 当前区域为深圳市时返回上一级按钮呈禁用（00395）

1. goto `/enterprise/key-enterprise-analysis?view=type`（默认区域=深圳）。
2. snapshot 核对「返回上一级」按钮可见：ref e10，states `[disabled]`。
3. CDP DOM 核验：`button.disabled === true`，class 含 `arco-btn-disabled`。
4. 区域口径核对：级联触发器 name =「全国热门科创城市 / 深圳 / 全部」，环境为深圳市单城。

判定：两条预期（按钮可见 / 深圳市态禁用）均成立 → Pass。

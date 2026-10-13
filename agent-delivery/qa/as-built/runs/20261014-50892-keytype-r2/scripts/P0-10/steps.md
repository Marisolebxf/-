# P0-10 · 区域洞察展示当前区域家数结构区块与清单入口（00385）

1. goto `/enterprise/key-enterprise-analysis?view=type`。
2. snapshot 核对 heading「区域洞察」（ref e23）与 button「查看企业清单（0）」（ref e17）在位。
3. CDP 定位区域洞察面板：文本含「当前区域 深圳市 0 家」。
4. CDP 核对「当前区域企业类型结构」区块标题存在（div.mt-4 text-[14px] font-medium）。
5. 核对清单入口文案 =「查看企业清单（0）」（含入口短语与数量）。

判定：三条预期（区域名+家数 / 结构区块 / 清单入口文案）均成立 → Pass。

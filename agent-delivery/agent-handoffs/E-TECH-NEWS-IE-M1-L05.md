# Handoff · E-TECH-NEWS-IE-M1-L05（前端门控 UX）

> **范围**：科技新闻复核页 — 文类门控 warning + impact 空文案  
> **仓**：`lumen-ui-science-pc`  
> **分支**：`feat/E-TECH-NEWS-IE-M1-L05` → 已合入并 push `origin/dev`  
> **日期**：2026-07-28  
> **依赖**：`E-TECH-NEWS-IE-M1-L04`（门控 HTTP 200 + error.code）

## 变更

| 项 | 行为 |
|----|------|
| 门控 | `opinion_or_commentary` / `policy_or_legal_noise` / `consumer_retail_noise` → Alert **warning** + Toast warning |
| 空事件 | 门控时 Empty「文类已拦截，无科技成果事件」 |
| impact | `null`/空 → 显示 **「暂无」**（不再字面 `null`） |
| flags | `gated_*` / finance 用 orangered；impact 相关 arcoblue |

## 文件

- `src/views/tech-news/index.vue`

## 验证

- 本地改动 diff 已提交；建议监管人打开 `/service/tech-news-review`，粘贴政策/开售样例看 warning。

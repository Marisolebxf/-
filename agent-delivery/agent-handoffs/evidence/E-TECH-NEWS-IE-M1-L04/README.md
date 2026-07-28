# Evidence · E-TECH-NEWS-IE-M1-L04

## Commits

| 仓 | 分支 | SHA |
|----|------|-----|
| demo-algo-science | origin/dev | `0ec4013` |

## Commands

```powershell
cd ${GKX_ROOT}/repos/demo-algo-science
.\scripts\tech-news-gold-eval.ps1 -Mode mock
# → 28/28 OK

.\.venv\Scripts\python.exe -m pytest tests/tech_news_ie/test_gold_regression.py tests/tech_news_ie/test_gate_dedup_time_v3.py -q
```

## LLM / Web（本机会话）

- LLM 金标初跑：26/27（G02 公司简称）→ 匹配放宽后 G02 PASS
- Web smoke 10 URL：门控 IPv6/剃须刀/GrapheneOS PASS；BYD impact 非空；Solidot 无效果句 + 财经上市过滤

## Gate contract for Java/UI

HTTP 200 + `error.code` in:

- `opinion_or_commentary`
- `policy_or_legal_noise`
- `consumer_retail_noise`

# Handoff — E-TECH-NEWS-ENTITY-M4-L02

> **status**: blocked  
> **claimed_by**: agent:frontend-agent  
> **supervised_by**: human:孙英哲  
> **claim_type**: pull  
> **blocked_by**: gateway/MySQL 环境不可达  
> **repo**: lumen-ui-science-pc  

---

## 阻塞说明

本机无法连通 `192.168.88.43:3306`（MySQL timeout），亦无可用登录态网关会话用于截图。

### 解阻后验收步骤

1. 算法侧：`TECH_NEWS_IE_STORE=mysql` + `INNOV_MYSQL_*`，确认 DDL 已落 `gkxlumenx_ads`
2. 登录 lumen PC → 科技新闻抽取复核 → 实体扩展 → 抽取并落库
3. 历史列表刷新 / 回看 / 筛选分页
4. 截图附本 handoff

### 复现命令（环境就绪后）

```powershell
# algo live smoke
$env:TECH_NEWS_IE_MYSQL_SMOKE=1
# + INNOV_MYSQL_*
cd repos/demo-algo-science
.\.venv\Scripts\python -m pytest tests/tech_news_ie/entity_ext/test_entity_m4_mysql_store.py -q
```

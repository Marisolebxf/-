# 数据写入 scope 确认记录（bug 7168664833）

- 会话：修7168664833（2026-11-15）
- 确认人：human:孔东（当前会话用户 / bug 当前处理人）
- 确认对象：demo_gkxlumenx_ads.svc_metric_fact 补种 M_SVC_ORG_CNT 行（period='all', slice_key='all', value=SELECT COUNT(*) FROM svc_org_card）
- 依据：缺陷 7168664833「门户，有新增机构数没有全球机构数」根因为该表缺行；补数 + Python 兜底回退双管齐下
- 政策：demo-2026-11-10（active-demo，demo_warehouse 组，writers=python）

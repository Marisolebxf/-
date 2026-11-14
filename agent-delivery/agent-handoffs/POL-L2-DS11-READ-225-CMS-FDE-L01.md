# Handoff · POL-L2-DS11-READ-225-CMS-FDE-L01

**标题**：225 多媒体辅助解读 · 专题 CMS 第 4 Tab + 展示改读  
**监管人**：human:淮政玮  
**裁定**：A1（展示改读、不改样式）/ B1 / C2（对象存储经 SysFile）  
**ponytail:** lite  

## 范围与实现

- 专题「政策新闻内容管理」新增 Tab「政策多媒体辅助解读」，CRUD + 草稿/发布  
- `content_type=policy_multimedia_assist`，表 `cms_pol_multimedia_assist`  
- 媒资：`/admin/sys-file/upload`，dir=`gkx-others/cms-multimedia`（D14 既有目录）  
- 展示：`GET /display/v1/policy/evaluation/multimedia` ← Feign CMS published；面板只换数据  

## 产物

| 仓 | 说明 |
|---|---|
| lumen-svc-platform | OpsContentType + migration + display 读口 |
| lumen-ui-topic | 第 4 Tab / schema / file 上传 |
| lumen-ui-science-pc | evaluationWiring + MultimediaAssistPanel src 绑定 |
| 简报 | `sdd/简报/2026-11-14-225-CMS-*` |

## 验收要点

1. CMS Tab 可见，可新建/编辑/发布/下架/删除  
2. 发布后展示选同一 `policy_id` 可见标题与说明；片源为 CMS `media_url`（失败回退动画舞台）  
3. 展示卡布局/按钮样式与改前一致  

## 运维

- 需在 `gkxlumenx_cms` 执行 `db/migration/20261114_cms_pol_multimedia_assist.sql`（若 CI 未自动跑）  
- 等 cms + display + 两前端 CI 绿后冒烟  

## 架构合规

- 调用链 FE→Java→（CMS/OSS）✅  
- D12 无 demo 服务 ✅  
- D14 未新桶/新顶层目录 ✅  
- 展示不改正文样式 ✅  

## cost（估）

actual_tokens / model / cost 待本会话收口回填。

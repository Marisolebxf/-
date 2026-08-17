# C1 · ServiceFacadeControllerTest CI 红修复（E0 连带）

> 日期：2026-08-17  
> 触发：`LUMEN-SVC-E-DEVOPS-L01` blocked · pipe [5110](https://gitlab.htmisoft.net/gkx-lumen/lumen-svc-platform/-/pipelines/5110)  
> 执行：`agent:api-agent` · 监管 `human:侯佳伟`

## 根因

`@WebMvcTest` 拉起 `GkxlumenTopicSvcApplication` + ResourceServer → `SpringContextHolder.getBeanFactory()` null。

## 修复

对齐 `IndustryFacadeControllerTest`：`MockMvcBuilders.standaloneSetup(...)`，不启 Security。

## 产物

- commit：`lumen-svc-platform` `796c21c`（rebase 后以 push SHA 为准）
- 下一步：等 `backend:build` 绿 → image → deploy async（自动）+ **play** `deploy:topic-svc` → 复测 E0

## Ponytail

`ponytail: full`

# Tasks · 专题系统接口携带 Authorization 即 424

> 对应 Spec：`spec.md`（同目录）
> **前置门禁**：用户已选「D 先只出结论、不改动」→ 下列 T3–T5 全部处于 **blocked（待批准）**，获批后才可执行。
> T1/T2 为只读排查项，本会话已完成。

## T1 · 运行时取证（已完成）

- [x] 无 token 请求基线：`POST /enterprise/topic/v1/search/meta/filters`（`systemCode: topic`） → 200
- [x] 同请求 + `Bearer FAKE-TOKEN-123` → 424 `{"code":1,"msg":"token expired"}`
- [x] `GET /innov/v1/health` + 假 token → 424（证实非 topic 独有）
- 证据：见 `spec.md` §2

## T2 · 静态根因定位（已完成）

- [x] 确认专题接口全部 `@Inner(value=false)` → permitAll（`CompareBasketController` 等）
- [x] 确认 F1 `ResourceAuthExceptionEntryPoint` HEAD 已 424→401（`c1b7a38`），线上为旧包
- [x] 确认 F2 `SsoProperties.enabled` 默认 true
- [x] 确认 lumen-svc-platform 全仓**无** `sso:` 配置块（F7 全部 yml）
- [x] 确认 F5/F6 `skipPublicUrl` 默认 false 且未被引用
- [x] 确认 F8 `request.ts` 现有规避（`ENABLE_MOCK_AUTH && !USE_MOCK` 时不带 Bearer）
- 证据：见 `spec.md` §3、§4

## T3 · 决策（blocked · 需 human:李伟 审批）

- [ ] 从 A / B / C 中选定执行路径
- [ ] 若选 A：确认用户中心注册应用（Client ID/Secret，联系人宋泉）的排期与获取方式
- [ ] 若选 A：确认重新部署范围（topic-* 全部 + innov + upms 是否一并 rollout）
- **产出**：Approve 记录写回本文件；未批准前不进入 T4/T5

## T4 · 实施（blocked · 依赖 T3）

- [ ] **A-1**：在 `repos/lumen-svc-platform/helm/gkxlumen-platform/configs/application-dev.yml` 补 `sso:` 共享块（`userCenterUrl` / `tenantId`），并在 `gkxlumen-topic-enterprise-biz-dev.yml`、`gkxlumen-topic-chain-biz-dev.yml`、`gkxlumen-topic-svc-biz-dev.yml`、`gkxlumen-topic-async-service-biz-dev.yml`、`gkxlumen-topic-policy-biz-dev.yml`、`gkxlumen-innov-dev.yml`、`gkxlumen-upms-biz-dev.yml` 的 `apps[]` 中登记 `code: <systemCode>`（至少 `topic`）+ `clientId` / `clientSecret`
- [ ] **A-2**：触发对应服务的 dev rollout，使 `c1b7a38` 及以后镜像生效
- [ ] **B-1**：在上述各资源服务 yml 追加 `security.oauth2.client.skip-public-url: true`（并同步 Nacos 灌配）
- [ ] **C-1**：如选 C，仅在 handoff 中登记「前端继续不传 Bearer」为已知取舍，不做代码改动
- [ ] 改动文件：F7（配置）为主；**不改** F1–F6 Java 逻辑

## T5 · 验证（blocked · 依赖 T4）

- [ ] `POST /enterprise/topic/v1/search/meta/filters`（`systemCode: topic`）无 Authorization → 200（回归）
- [ ] 同上 + 合法用户中心 token → 200（方案 A）
- [ ] 同上 + 假/过期 token → 401 `访问令牌不存在`（A）或 200（B）；**不得出现 424**
- [ ] 检查服务日志：无 `sso introspect: unknown systemCode=topic`
- [ ] 若走 A：前端恢复携带 `Bearer + systemCode=topic`，门户 iframe 联调路径复测
- [ ] 全仓 grep 复检 `FAILED_DEPENDENCY`（仅允许 demo 侧历史残留）

## T6 · 收口

- [ ] 更新 `agent-delivery/agent-handoffs/门户集成-PORTAL/LUMEN-PORTAL-IFRAME-L01.md` §6 遗留项 4
- [ ] 写回 handoff 摘要（含 spec 中「要求的审批」与验证证据）

---

### 当前状态

| 任务 | 状态 |
|---|---|
| T1 运行时取证 | ✅ 完成 |
| T2 静态根因定位 | ✅ 完成 |
| T3 决策 | ⏸ blocked（待 human:李伟 审批） |
| T4 实施 | ⏸ blocked（依赖 T3） |
| T5 验证 | ⏸ blocked（依赖 T4） |
| T6 收口 | ⏸ blocked |

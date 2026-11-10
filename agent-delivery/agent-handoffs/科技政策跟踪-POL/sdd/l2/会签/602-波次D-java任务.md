# 602 · 代码第一段 · Java 门面

仓：`repos/lumen-svc-platform`。只加 602 的新读口。不改 `GET /v1/policy/governance/results`，不改前端，不连库，不 commit。

## 调用链

浏览器打 display。display 只调 element。element 再 Feign `lumen-algo-py` 的两条新路由。禁止 Feign `RemotePolicySyncClient`，禁止任何 `demo-*` 服务名。Java 不写贴源 SQL。

## 新接口

display（网关会把 `/display` 去掉，控制器仍在 `/v1/policy/governance`）：

- `GET /v1/policy/governance/clean-candidates`
- `POST /v1/policy/governance/clean-execute`

element：

- 转发候选到 `GET /internal/policy/clean-candidates`
- 转发五条到 `POST /internal/policy/clean-judge`
- 准确性：只有请求带了「准确性校验」才读 `{ads}.policy_accuracy_demo`，按来源 + 贴源 id。对上的行返回 `demo_hit_count`，并带 `demo: true`。表在但没有行：`phrase` = 「这一条还没有演示数」，不要数，不要 0。表不存在或查询失败：`read_failed`，文案「读取失败」。不要把失败收成 `emptyResults()` 里的 0。

执行响应里：

- 批次条数等于勾选条数。
- 停用的规则标明停用，不计入。
- 有判定时 `judged_at` 用这次响应的时刻。无加工事实时 `hit` 为 null，`judged_at` 为空。
- 本批状态：能判定的都过了且没有失败样例 = 成功；夹着失败样例或无加工事实 = 部分；能判定的都带失败样例 = 失败。读取失败和无加工事实不写成这三句。

勾选为空：不返回批次明细，不造 0。

Feign 失败：该块 `read_failed`，不要吞成空 Map 再填 0。不要复用 `PolicyGovernanceService.emptyResults()`。

## 自检

编译所改模块。加一个不连库的测试：Feign 失败时响应不是 `totalPolicyCount: 0`，而是读取失败。

强度：ponytail full。

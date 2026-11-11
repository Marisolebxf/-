# Demo 阶段数据/Mock 例外决定

- 决定编号：`demo-phase-2026-11-10`
- 决定人：`human:徐滕强`
- 决定时间：2026-11-10
- 决定来源：Codex 对话中项目负责人明确说明当前 Demo 阶段可以制造和写入 Mock 数据，正式上线时会人工通知切换
- 批准来源标记：`codex_chat`（P0 采用会话记录作为人工决定引用；不是独立签名）
- 关联 policy：`demo-2026-11-10`

## 用户原始口径

- “demo库的dwd ads cms库也都是允许去mock数据的”
- “demo环境的cms就是现在正式的cms，这是业务库就当demo用，等真正上线了，我会人工通知你全改一下，禁止mock数据”
- “当前没有说就是可以mock数据，不然这个时间点不好评估”

## 决定内容

1. 当前 Demo 阶段，`demo_gkxlumenx_ods/dwd/ads/dim` 可在 run 级 scope 逐表确认后写入 Mock 数据。
2. 当前 `gkxlumenx_cms` 仍是正式 CMS 业务库，但项目负责人明确将其作为 Demo 使用；只允许通过 CMS 业务接口或已登记的受控脚本操作，不允许整库 SQL 放行。
3. 任何写入都必须命中 base policy 和当前 run 的 `data_policy.scope`，并记录 environment、host、database、schema、table、执行账号、确认人和证据。
4. 空 scope、未逐表枚举、未确认、无法核验执行账号或超出 D16/D18/仓库硬规则时，默认拒绝并进入 `BLOCKED`。
5. 以下任一条件先发生时，Demo 例外失效：
   - 项目负责人通知正式上线；
   - 2026-12-10 到期；
   - 数据/架构负责人撤销或收紧授权。
6. 2026-11-17 做一次试点复核；如仍未上线，由项目负责人决定是否创建新的 policy 版本续期。

## 说明

这是有范围的 Demo 例外，不是对正式 ODS/DWD/ADS 的长期写入授权，也不代表生产发布授权。密码、token、签名 URL 和敏感数据不得写入本文件、policy、state 或日志。

# POL-AUDIT-API-GAP-L03 · 政策跟踪后端接口缺口登记（B2/B3/B4）

> 来源：2026-11-05 科技政策跟踪模块需规符合性审核 · 偏差项 B2/B3/B4。
> 性质：**definition 单（只登记不实现）**。本文档为 api-agent 排期输入；实现时逐条建 FE/API 叶任务。
> 前端现状代码基线：`repos/lumen-ui-science-pc` @ dev（POL-AUDIT-FE-REFACTOR-L01 工作区之后）。

## 缺口总览

| # | 偏差 | 需规出处 | 前端现状 | 缺口类型 |
|---|------|---------|---------|---------|
| B2 | live 收藏无取消接口 | 原需规 1.1.1.1.4.2.1.5 收藏夹管理（新增/移除） | `toggleFavorite` live 分支已收藏时仅提示「收藏以服务端记录为准，本页不能在本地取消」（index.vue L569-571） | REST 接口缺失 |
| B3 | live 邮件分享通道不可用 | 原需规 1.1.1.1.4.2.1.6 检索结果导出与分享 | ShareModal live 分支邮件方式提示「邮件不可用，不发送邮件」（remoteNote 透传） | 外发通道缺失 |
| B4 | 订阅推送仅入库不外发 | 原需规 1.1.1.1.4.2.1.2.2 政策动向订阅推送 | 后端 `honesty.outbound = unavailable:no_send_channel`；前端诚实提示「通道接通后将按设定频率推送」 | 外发通道缺失 |

## B2 · 收藏取消接口

**需求**：live 模式下取消收藏（当前只有 `POST /display/v1/policy/panorama/favorites` 新增）。

**建议契约**（对齐既有 panorama 前缀风格）：

```
DELETE /display/v1/policy/panorama/favorites/{policy_id}
```

- 认证：需登录（匿名 200+anonymous 降级语义与既有 favorites 接口一致，前端已处理该分支）
- 返回：R 包裹 `{ code: 0, data: { item: { policy_id: string } | null }, honesty? }`
- honesty 语义：匿名时 `anonymous`；成功删除 `item.policy_id` 回显
- 前端接线点：`panorama/index.vue toggleFavorite` live 已收藏分支（替换「不能在本地取消」提示）；收藏抽屉「取消收藏」按钮（L1397）

**验收**：live 模式心形图标可在收藏/未收藏间双向切换，服务端收藏列表同步。

## B3 · 邮件分享外发通道

**需求**：检索结果分享的邮件方式真实发送（当前 live 仅生成链接，邮件方式提示不可用）。

**建议契约**：

```
POST /display/v1/policy/panorama/share/email
```

- 请求体：`{ share_url: string, recipients: string[], note?: string }`（recipients 前端已做多邮箱分号解析 + 格式校验）
- 依赖：SMTP/企业邮件网关等外发基础设施（与 B4 订阅推送 email 通道可共用）
- honesty 语义：通道未上线前保持现状（`unavailable:no_send_channel`），前端诚实提示不伪造发送成功
- 降级：通道未上线时前端维持现有「邮件不可用」提示（已实现，无需改动）

**验收**：live 模式邮件分享真实送达收件箱；通道未上线时提示与现状一致（不伪造）。

## B4 · 订阅推送外发通道

**需求**：政策动向订阅保存后按频率（daily/weekly/monthly）经通道（system/email/sms）外发命中摘要（当前仅入库，`honesty.outbound=unavailable:no_send_channel`）。

**要素**：

- 通道矩阵：`system`（站内收件箱）/ `email`（与 B3 共用 SMTP）/ `sms`（短信网关）
- 频率调度：day/week/month 定时任务扫库比对 `ingest_watermark` 增量
- honesty 语义：通道逐级上线时 `honesty.outbound` 由 `unavailable:no_send_channel` 改为 `partial:{channels}` → `ready`；前端 `pushChannelUnavailable` 已消费该字段自动切换提示
- 建议实现顺序：system（站内）→ email → sms（依赖外部网关）

**验收**：订阅保存后到期触发外发；`honesty.outbound` 如实反映通道就绪度；前端提示自动跟随。

## 排期建议

- B2 独立小接口，api-agent 可直接排（无外部依赖）
- B3/B4 依赖邮件/短信外发基础设施，建议与平台侧（网关/SMTP/短信）确认窗口后合并排期；通道上线前前端诚实提示已就位，不阻塞验收

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent`（代登记；实现归 api-agent） |
| supervised_by | `human:孔东` |
| claim_type | `pull` |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `N/A`（definition 单） |

## 测试结果

- 登记文档内容与前端代码现状逐条核对（toggleFavorite L556-571 / ShareModal L54-71 / subscriptionStore pushChannelUnavailable）
- 不涉及代码改动，无 CI 项

## 遗留风险

- B3/B4 外发基础设施窗口未定，排期依赖平台侧确认
- B2 契约冻结后须同步更新 `src/api/policy.ts`（当前无 DELETE 定义）

## 涉及文件

- `agent-delivery/agent-handoffs/科技政策跟踪-POL/POL-AUDIT-API-GAP-L03-接口缺口登记.md`（本文档）

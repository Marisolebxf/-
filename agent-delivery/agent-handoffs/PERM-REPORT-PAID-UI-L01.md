# PERM-REPORT-PAID-UI-L01 · handoff

> **状态**：in_progress（Wave 0 主体已落地，待监管人淮政玮走查）  
> **监管**：human:淮政玮  
> **执行**：agent:frontend-agent  
> **强度**：ponytail full  
> **仓**：demo-ui-topic  
> **真源**：`PLAN-报告创建与PDF付费权益-方案B.md` · `Q-REPORT-PAID-01`

## 范围与实现

方案 B Wave 0 **仅 UI 锁**：

1. `CurrentUser.paid`；`defaultPaidForLevel`：L3/L4=`true`，其余=`false`；`setLevel` 重置默认；`setPaid` 供演示  
2. 顶栏 `PersonaLevelSwitcher`：**能力角标 + 付费/未付费角标**；≥L2 菜单内「付费权益」Switch（L2 可演示 L2+付费）  
3. `ReportExportButton` / `useReportExportAccess`：≥L2 且 paid 才可「导出」  
4. `SystemReportReader`、企业评估/引育报告弹层、风险洞察弹层接入闸门；文案统一「导出」

## 天花板（诚实）

- 无服务端 PDF 鉴权；浏览器打印 HTML 可绕过（PLAN 已接受）  
- 未拆 `btn:common:report-pdf` 进 matrix/网关  

## 验收证据

```text
node --test tests/report-paid-export-ui.test.mjs
```

## 架构合规自检（摘）

| 铁律 | 结果 |
|---|---|
| 调用链 | ✅ 无越层 |
| 可观测 | ✅ Switch/级别沿用现有埋点 scope |
| D8/D10 | ✅ Arco Tag/Switch/Button；锁态可见不隐藏 |
| handoff | ✅ 本文件 |

## 开放项

- [ ] 监管人顶栏拨 L2 ↔ L2+付费，打开任一份 HTML 报告核对「导出」锁/开  
- [ ] Wave 1：服务端导出 + SSO paid 下发（不在本单）

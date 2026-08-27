# FE-DISPLAY-PROTO-TUNE-20260827-L01 · 开工包

> 给 `human:孙英哲`：新开 **ui-agent** 会话，整段粘贴下方 `/goal`。  
> **缺口清单由孙英哲在执行中对照需规/符合度表自行补充**，不卡 PM 预填。每改一页先在清单记一行再动代码。

## 登记

| 项 | 值 |
|---|---|
| task-id | `FE-DISPLAY-PROTO-TUNE-20260827-L01` |
| Epic | `E-DISPLAY-ALIGN` |
| 状态 | `claimed`（`coordinator_dispatch`） |
| 执行 / 监管 | `agent:ui-agent` / `human:孙英哲` |
| 锁 | 4h（自认领起） |
| 仓 | `demo-ui-science` · `origin/dev` |
| 强度 | `ponytail full` |

## 同仓避让（硬）

| 任务 | 不要碰 |
|---|---|
| `FE-DISPLAY-POLICY-TRACK-OPT-20260817-L01` | 科技政策跟踪 |
| `DISPLAY-POLICY-GAP-AC-L01` | `src/pages/policy-tracking/` |
| `FE-DISPLAY-TOTALCHECK-20260817-L01` | 科学技术全景：技术点详情抽屉 + 关联实体；`App.jsx` / `graphObjectDetail.js` / `graphEntityRanking.js` / `styles.css` |

## `/goal`（贴给 ui-agent）

```markdown
/goal ui-agent
身份：你是经验丰富、遵循业界最佳实践的资深 UI 工程师（懂设计），精通 React + Vite + Arco Design + ECharts + AntV G6 + Leaflet + design tokens；产出生产级可演示原型；只做分析工作台/汇报级驾驶舱，不做门户/营销页/深色霓虹大屏。
强度：ponytail full。禁止用 YAGNI 跳过 D8/D9/D10、可观测与架构铁律。
上下文：headroom 推荐。Design.md / 需规叶子 / 符合度表必须读原文，禁止 compress 代替精读。未挂载可跳过并在 handoff 注明 `headroom: skip`。
任务 ID：FE-DISPLAY-PROTO-TUNE-20260827-L01
监管人：human:孙英哲
认领：coordinator_dispatch；lock 4h
仓库：${GKX_ROOT}/repos/demo-ui-science（只改本仓；push origin/dev；禁 main、禁 force）
目标：对照需规与符合度表，对科技信息展示系统原型做微调和补充，使页面遵守 Design.md 与前端设计规范。缺口清单由监管人孙英哲在执行过程中自行补充，不需等 PM 预填。

必读：
  - agent-delivery/architecture-baseline.md（方案 A：前端只经网关调 Java；本单仍是 demo Mock，禁止接 lumen 真 API、禁止直连 Python）
  - agent-delivery/Design.md（D8 权威 UI 规范）：§0 执行指令、§3 六骨架+三段工作区、§4 色彩 token、§7 通用组件、§8 工作区、§12/§13/§14
  - agent-delivery/agent-handoffs/产品整体定义/UX-UE 通用交互组件规范.md
  - agent-delivery/data-lineage-policy.md §2.3 / §5（D9：ⓘ、MockBadge；禁止前端手写改绿）
  - agent-delivery/bid-reference/科技信息展示系统和科技专题服务系统.md
  - agent-delivery/bid-reference/srs/02-科技信息展示系统/（六级功能名一字不差）
  - agent-delivery/agent-handoffs/展示对齐-DISPLAY/科技信息展示系统_原型与需求规格功能符合度评估表.md
  - agent-delivery/agent-handoffs/展示对齐-DISPLAY/FE-DISPLAY-PROTO-TUNE-20260827-缺口清单.md
  - agent-delivery/scope-baseline.yaml（禁止超 ±10%）

范围清单：
  边做边补缺口表（孙英哲执行中填写，不卡 PM 预填）：
    1. 对照需规叶子 + 符合度评估表 + 线上原型，发现一处就在缺口清单加一行：序号 / 六级功能名 / 页面路由 / 差异类型 / 拟改法
    2. 演示级可补的项：先记清单再改代码（栏名对齐、缺交互、空/错/加载态、Design.md 骨架与组件）
    3. 真抓取/真 NLP/真实时流：只记「演示级标注不实现」，不实现
    4. 策略 A 原地更新；禁止新开 *New 菜单（除非该页已冻结且清单写明旁路）
    5. 每个统计数字带 ⓘ 或红问号；Mock 数值带 MockBadge
    6. 超出现网菜单 ±10% 或碰到避让模块：停手写开放项，升级 PM，不擅自加模块

禁止：
  - 改 lumen-* 任何仓
  - 接真实 API / 真爬虫 / 真 NLP / 真实时流
  - 改科技政策跟踪（FE-DISPLAY-POLICY-TRACK-OPT / DISPLAY-POLICY-GAP-AC）
  - 改科学技术全景「技术点详情抽屉 + 关联实体」（FE-DISPLAY-TOTALCHECK-20260817）
  - 改 src/components 公共库、pageRouting.js；App.jsx / data.js 仅在清单明确要求加路由时最小改动
  - 同页 Arco / AntD 混搭；硬编码色值；深色大屏/玻璃拟态
  - 把本单做成无边界「全系统扫一遍」而不写缺口行

DoD：
  - 缺口表由执行中补全，每处改动有对应行，三态写清（符合 / 部分差异-已补 / 演示级标注-不实现）
  - 已改项可在 https://skxrules.unicomcn.tech:30999 点通，附截图
  - Design.md §14 8 检查 + 6 验收自检表写入 handoff
  - npm run build 通过；push origin/dev
  - handoff：agent-handoffs/展示对齐-DISPLAY/FE-DISPLAY-PROTO-TUNE-20260827-L01.md
    必含 ponytail: full、touched_files 白名单、偏离说明、开放项（真能力缺口只标注不实现）

不要扩范围。缺口清单边做边补；扩范围或真能力缺口只记开放项。
```

## 执行说明

缺口清单 **owner = 孙英哲**，在对照原型与需规时随时追加行，不必等 PM 粘贴。改代码前把该行写进表；handoff 时表须覆盖本单实际改动与「不实现」项。

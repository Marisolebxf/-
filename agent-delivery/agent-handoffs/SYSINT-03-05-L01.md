# SYSINT-03-05-L01 · 企业发展可视化（阶段 1：能做的先做）

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:徐滕强` |
| claim_type | `pull` |
| 说明 | 分阶段交付：阶段 1 接 V-E 能出的块；缺口三件（散点/时间轴/SWOT）+ 导出待拍板，不造数 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 复用既有 `EnterpriseVizPage`（VIZ-FE 已建壳）与 `entProfileFinanceTrend/Competitiveness`；只新增 1 条 API 路径 + 1 个聚合接口函数 + 类型；零新依赖 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 《可视化四菜单-Java接口清单》V-E 段与《复用与新建清单》§3.2/§4.2 原文精读 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | `SYSINT-SCHEME-03-SEQ` |
| 图 diff | 未改图。页面→Java `POST /enterprise/topic/v1/profile/viz`（V-E，今日 integration），Python 计算块仍归算法侧 |
| 会签态 | 技术方案 draft |
| 说明 | 浏览器→网关→Java→Python /internal，未越层 |

## 范围与实现（阶段 1）

`lumen-ui-topic`（运维可视化菜单 `企业发发展可视化` 页，非门户四页）：

1. **接线 V-E**：`entProfileViz`（新 API）与既有 finance/competitiveness 三路并发；失败全清不残留旧企业数据。
2. **基本信息卡**：`USE_MOCK=false` 时渲染 V-E `card` 五列（名称/行业/地区/规模/竞争力分）；空态透出端点 `reason`。
3. **同行对比**：`peers` 块非空时行摘要（家数+名单+维度）；空态显示 `reason`（当前=待 Python 端点）。
4. **空态诚实**：散点/时间轴/SWOT 用 V-E 空块 `reason` 作描述；不引入新依赖、不造数。
5. mock 路径（`USE_MOCK=true`）原样保留，不受影响。

## 阶段 2 缺口清单（2026-11-04 14:46 用户拍板后状态更新）

| 项 | 拍板 | 状态 |
|---|---|---|
| 行业定位散点 | ✅ 先出效果（x=竞争力分 / y=专利总量 / 气泡=注册资本），维度后看再调 | Python 端点已落 `topic-py /stats/enterprise-scatter`（停本地） |
| 成长时间轴 | ✅ 三源聚合（融资事件 financings + 资讯 news + 注册时间 incorporation_date） | Python 端点已落 `topic-py /profile/timeline`（停本地） |
| SWOT | ✅ 方案 A（LLM 生成，01C 模式；失败整块隐藏；标「AI 生成」不冒充专家署名） | Python 端点已落 `algo-py /internal/enterprise/swot`（停本地） |
| 导出 | ✅ 销工作量：前端 Blob CSV 已有，换 V-E 数据源属前端顺手事，不算后端工作量 | 无需后端 |

**Java Feign 透传（3 条：timeline / enterprise-scatter / swot）与前端接线归属待徐滕强指派**（V-E 现有 Java 是 api-agent 写的；确认归我改即接）。

## 偏离

- V-E `finance.series` 在 dev 实测为「年份行齐全但数值全 null」（13 行 0 值），页面维持既有 `liveFinanceOption`（全 null → 不渲染图、出空态文案），未对 Java 契约提变更。
- 页面既有散点/时间轴/SWOT 空态文案改为携带 V-E `reason`，属展示层文案增强，不违反块级空态契约。

## 产物清单

| 仓 | 路径 |
|---|---|
| lumen-ui-topic | `src/api/enterprise/paths.ts`（+profileViz） |
| lumen-ui-topic | `src/api/enterprise/profileDetail.ts`（+entProfileViz） |
| lumen-ui-topic | `src/api/enterprise/types/profile.ts`（+EntProfileVizResponse 等 4 类型） |
| lumen-ui-topic | `src/api/enterprise/index.ts`（导出） |
| lumen-ui-topic | `src/views/viz/enterprise/EnterpriseVizPage.vue`（V-E 接线） |
| lumen-ui-topic | `scripts/selfcheck-ent-viz.mjs`（自检） |
| gkx-orchestration | 本 handoff |

## 验收证据

- `npx vue-tsc --noEmit` → 0 error
- `npx eslint`（5 个涉改文件）→ 0 error
- `node scripts/selfcheck-ent-viz.mjs` → **14 PASS**（路由注册/无直连 URL/失败清态/五列卡/reason 透出/缺口不造数/零新依赖/类型齐/USE_MOCK 门控）
- dev 实测 V-E 形状（14:26）：空参六块空态「未选择企业」；`org_id=25019826` card 有行（山东瑞宇蓄电池/其他电池制造/中型）；finance 13 行全 null；peers/scatter/timeline/swot 空态 reason=「暂无计算口径，待 Python 分析端点接入」

## 遗留风险

- peers/scatter/swot 等 Python 端点接入后块自动有数，页面无需再改（已按非空形状预留渲染）。
- finance 序列全 null 是否属数据面缺口（灌数即出图）待数据侧确认；页面已按「全 null 不画图」处理。

## 架构合规自检

| 项 | 结果 |
|---|---|
| 调用链 浏览器→Java→Python | ✅ |
| 不调 demo-* | ✅ |
| 缺口空态不造数 | ✅ selfcheck |
| D9 metric_id | N/A（V-E 块无统计口径挂载；Java 侧负责） |
| USE_MOCK=false 零 fixture | ✅ selfcheck |

## cost

| 字段 | 值 |
|---|---|
| actual_tokens | 约 110000（估） |
| model_used | composer |
| actual_cost | 约 0.6 |
| cost_warn | green |

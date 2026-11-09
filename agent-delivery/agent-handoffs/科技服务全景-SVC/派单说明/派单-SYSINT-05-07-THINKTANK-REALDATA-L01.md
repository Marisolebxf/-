# 派单说明 · SYSINT-05-07-L01 智库服务真实对接（8 子任务）

- **父任务**：`SYSINT-05-07-L01`（智库服务，WBS-05-07，**ready**）
- **子任务区间**：`WBS-05-07-01` ～ `WBS-05-07-08`
- **派单日期**：2026-11-06
- **监管人**：`human:李伟`（一律沿用；registry `supervised_by` 记李伟，`claimed_by` 一线记孔东）
- **执行优先级**：**A → B → D → C → E**（用户 2026-11-06 裁定）
- **派单依据**：
  - 对端 v1.1：`agent-delivery/工程过程/04-系统集成/05-展示系统集成/对接文档/对端/智库门户对接-API接口文档-v1.1.md`（4 GET）
  - 对端 docx：`agent-delivery/工程过程/04-系统集成/05-展示系统集成/对接文档/对端/门户智库外部接口文档.docx`（5 POST）
  - 三方比对清单：`对接文档/我方/2026-10-23-智库服务-三方比对与待智谱评估清单.md`
  - 需规：`bid-reference/srs/02-科技信息展示系统/科技服务全景/智库服务.md`（seq 566–574）
  - 边界：`agent-delivery/metrics/request/展示系统/pages/DS-30-THINKTANK.yaml`（`metric_open_status=missing`）
  - 父任务 DoD：调到智谱接口 / 接口未到空态 / 不按跳转（本批将"不跳转"细化为"不跳出新页签/新窗口，允许本系统内 iframe 弹框嵌入"，由 03 号单书面化）/ 不做高端智库后台

**契约稿（01 号单产物，已落盘 2026-11-06）**：`agent-delivery/工程过程/02-策划与监控/01-总集大项目整体计划/外部接口依赖/05-展示五大模块-第三方API接口清单.md` **§六 科技服务全景·智库服务** —— ZK-01～ZK-09 逐字段入册，接口包 **`EXT-B4-ZHIKU`**（4 GET + 5 POST，合计清单 62 条）。

---

## 0. 全局口径

1. **两套接口并列**：v1.1（zwrite-backend，`/admin-api/v1`，`Authorization: Bearer`）覆盖**报告 / 成果 / 筛选枚举 / 成果统计**；docx（topic-system，`/topic-system/uc-open-api/v1/portal`，`X-Portal-Access-Token`）覆盖**德尔菲问卷 / 专家 / Field 选项 / 重大事件**。
2. **服务类型主档对端不给**（B1 未决）：5 类（政策研究 / 战略咨询 / 评估评价 / 人才培训 / 学术交流）**用我方运营目录硬编码**，待对端补正式主档再换映射。
3. **专家 H 指数 / 引用量不展示**（D2 已定）：守住 `talent_ds13_16` 边界。
4. **成果集合收窄**（D4 已定）：接受"战略咨询案例"为唯一来源，"建议"由 `report_type` 派生。
5. **指标全走外部接口**：本页 25 条指标在久新库全部"三源调研批次产物 + 源表为空"，**不指望久新库供数**；前端按 D9 挂 ⓘ + 四维就绪度，**禁 MockBadge**。
6. **iframe 弹框是新主路径**：详情打开走 Arco Modal + iframe 加载 `detail_url`；空 `detail_url` 兜底回落现有抽屉（保留不删，延续 2026-10-24 裁定）。

---

## A · 契约与合规（2 张）

### 01 `SYSINT-05-07-01-L01` · 智库契约登记与 EXT-B4-ZHIKU 建包

| 项 | 值 |
|---|---|
| 名称 | 智库服务 9 端点契约登记 + EXT-B4-ZHIKU 包建号 |
| 监管 / 认领 | `human:李伟` / `human:孔东` |
| 执行 | `agent:architect-agent` |
| 仓 | `gkx-orchestration` |
| 依赖 | 无 |
| 优先级 | A 段第 1 张 |

**交付产物**
- 修订 `02-策划与监控/01-总集大项目整体计划/外部接口依赖/05-展示五大模块-第三方API接口清单.md`：新增智库 9 端点条目，字段级（路径 / 方法 / 鉴权 / 信封 / 必填可选 / 响应字段）。
- 新设 `EXT-B4-ZHIKU` 包编号（或经总集确认挂 `EXT-B2-RESULT`），回写比对清单第八章。
- 9 端点清单：v1.1 `/reports` `/achievements` `/enums` `/achievements/stats`；docx `/delphi-questionnaire/page` `/delphi-questionnaire/detail` `/expert/page` `/expert/field/options` `/major-event/page`。

**DoD**
1. 05-API 清单新增智库 3 段（报告 / 成果 / 门户活动专家事件），逐字段标注。
2. EXT 包编号落定并回写技术方案 §1.3 智谱行（把"智库接口还没有"改为"已有 9 端点，EXT-B4-ZHIKU"）。
3. 派单稿与契约稿交叉引用（本稿 ↔ 契约稿路径）。

---

### 02 `SYSINT-05-07-02-L01` · 智库鉴权打通（双 token）

| 项 | 值 |
|---|---|
| 名称 | v1.1 Bearer + docx X-Portal-Access-Token 双 token 申请与贯通 |
| 监管 / 认领 | `human:李伟` / `human:孔东` |
| 执行 | `agent:architect-agent` + `human:李伟`（向统一用户中心申请） |
| 仓 | `gkx-orchestration`（凭证不落盘） |
| 依赖 | 01 |
| 优先级 | A 段第 2 张 |

**交付产物**
- 鉴权方案 MD：两种 token 的申请流程、续期、失效处理（v1.1 `code=10001` / docx `code=401`）。
- 展示 Java 网关侧双头转发约定（不落码，先出契约）。
- 测试账号、测试地址、联调窗口三件套申请记录（按仓内铁律，**凭证具体值不进 git**）。

**DoD**
1. 两种 token 的申请流程有书面记录，凭证获取到人。
2. 401/10001 失效重取策略成文。
3. 网关双头转发契约冻结。

---

## B · 决策书面化（2 张）

### 03 `SYSINT-05-07-03-L01` · D1–D5 决策函 + B1–B5 冲突裁定

| 项 | 值 |
|---|---|
| 名称 | 智库服务五项内部决策 + 五项语义冲突裁定（含 B5 专家详情 iframe 弹框裁定） |
| 监管 / 认领 | `human:李伟` / `human:李伟`（PM 签字件） |
| 执行 | `human:李伟` + `agent:doc-agent` 起草 |
| 仓 | `gkx-orchestration` |
| 依赖 | 无（可与 A 段并行） |
| 优先级 | B 段第 1 张 |

**交付产物**
- `对接文档/我方/2026-11-06-智库服务-D1-D5-决策函.md`：D1 服务类型运营目录归属 / D2 不展示 H 指数 / D3 活动详情空态 / D4 接受成果收窄 / D5 服务类型计数前端派生。
- `对接文档/我方/2026-11-06-智库服务-B1-B5-裁定函.md`：B1 服务类型主档（我方目录+对端映射表）/ B2 活动仅德尔菲问卷 + 详情不公开 / B3 专家字段裁剪 / B4 成果集合收窄 / **B5 专家详情采用 iframe 弹框嵌入，不跳出新页签**。
- 技术方案 §2 调用方向智库行措辞修订：「不跳转」→「**不跳出新页签 / 新窗口，允许本系统内 iframe 弹框嵌入**」，由 `human:淮政玮` 重新签收。

**DoD**
1. 两份函件 PM 签字、归档到 `对接文档/我方/`。
2. 技术方案 §2 措辞修订并由淮政玮重新签收。
3. 函件要点回写比对清单第六、七章。

---

### 04 `SYSINT-05-07-04-L01` · iframe 嵌入白名单 + 成果敏感字段对外合规

| 项 | 值 |
|---|---|
| 名称 | `zk.example.com` / `edu.itic-sci.com` 嵌入白名单确认 + 投资额/ROI/满意度对外口径 |
| 监管 / 认领 | `human:李伟` / `human:李伟` |
| 执行 | `human:李伟`（对端书面） |
| 仓 | `gkx-orchestration` |
| 依赖 | 03 |
| 优先级 | B 段第 2 张 |

**交付产物**
- 对端书面回函：① `X-Frame-Options` / CSP `frame-ancestors` 允许本系统域嵌入；② `detail_url` 免登录公开可读；③ 两端 HTTPS 一致。
- 成果敏感字段（实际投资额 / ROI / 客户满意度）对外口径裁定：显示 / 脱敏区间 / 隐藏，三选一并签字。

**DoD**
1. 对端书面回函归档（允许嵌入 + 免登录 + HTTPS 三项齐备）。
2. 敏感字段对外口径裁定归档。
3. 任一一项不通过 → 立即升级（B5 回退 / 成果字段隐藏）。

---

## D · 后端实现（2 张）

### 05 `BE-DISPLAY-SVC-THINKTANK-GATEWAY-L01` · 展示 Java 网关双路由

| 项 | 值 |
|---|---|
| 名称 | 展示 Java 网关：zwrite-backend + topic-system 双 BASE_URL 路由 + 双鉴权头转发 + 信封规范化 |
| 监管 / 认领 | `human:李伟` / `human:孔东` |
| 执行 | `agent:backend-agent` |
| 仓 | `lumen-svc-platform` |
| 依赖 | 01、02、03 |
| 优先级 | D 段第 1 张 |

**交付产物**
- 网关路由配置：v1.1 `/admin-api/v1/**` → zwrite-backend；docx `/topic-system/uc-open-api/v1/portal/**` → topic-system。
- 鉴权拦截器：按目标系统自动切换 `Authorization: Bearer` / `X-Portal-Access-Token`。
- 信封规范化层：v1.1 `{code:0,message,data}` 与 docx `{code:200,success,data,msg}` 统一为展示标准信封（对外仍透传原 code 便于排查）。

**DoD**
1. 网关可分别路由两种 BASE_URL，双双调通（Postman 验证）。
2. 401 / 10001 / 400 错误码透传，前端可判。
3. 信封规范化单测覆盖两套原始结构。

---

### 06 `BE-DISPLAY-SVC-THINKTANK-API-L01` · 智库 9 端点业务转发

| 项 | 值 |
|---|---|
| 名称 | 智库 9 端点业务实现：报告 / 成果 / 问卷 / 专家 / 事件转发 + 字段映射 |
| 监管 / 认领 | `human:李伟` / `human:孔东` |
| 执行 | `agent:backend-agent` |
| 仓 | `lumen-svc-platform` |
| 依赖 | 05 |
| 优先级 | D 段第 2 张 |

**交付产物**
- 9 个展示侧端点：报告列表 / 成果列表 / 筛选枚举 / 成果统计 / 问卷分页 / 问卷详情 / 专家分页 / Field 选项 / 重大事件分页。
- 字段映射层：对端字段 → 展示侧 DTO（按 demo `thinkTankModel.js` 字段口径反推）。
- 空态约定落地：`total=0` / `records=[]` / `detail_url=""` 三态透传不吞。

**DoD**
1. 9 端点全部可调通，响应结构与对端文档一致。
2. 字段映射单测覆盖 demo 用到的全部字段（对照 `mockData.js` 现有键）。
3. 空态三态（空数组 / 空 detail_url / total=0）实测通过。

---

## C · 前端实现（1 张）

### 07 `FE-DISPLAY-SVC-THINKTANK-REPLICA-L01` · 智库 5 Tab 复刻 + IframeDetailModal + D9 血缘

| 项 | 值 |
|---|---|
| 名称 | demo `ThinkTankService.jsx` → `lumen-ui-science-pc` Vue + Arco 复刻；IframeDetailModal 公共组件；D9 血缘接入 |
| 监管 / 认领 | `human:李伟` / `human:孔东` |
| 执行 | `agent:frontend-agent` |
| 仓 | `lumen-ui-science-pc` |
| 依赖 | 03（服务类型裁定）、04（iframe 白名单）、06（后端可调） |
| 优先级 | C 段第 1 张（唯一） |

**交付产物**
- `src/views/tech-service/ThinkTankService/`：5 Tab（服务类型 / 智库报告 / 智库活动 / 智库专家 / 智库成果）+ 重大事件侧栏；样式与 demo `ad51a5e` 对齐。
- `src/components/IframeDetailModal/`：Arco Modal + iframe + loading 骨架 + 空 `detail_url` 兜底回落现有抽屉；`80vw × 80vh`；`sandbox="allow-scripts allow-same-origin"`；`referrerpolicy="no-referrer"`。
- 服务类型 Tab：运营目录硬编码 5 类（政策研究 / 战略咨询 / 评估评价 / 人才培训 / 学术交流），预留 `service_type` 字段待对端主档替换。
- D9 血缘：每个统计数字旁挂 ⓘ + 四维就绪度；本页**全走外部接口路径**，不入久新库血缘；**禁 MockBadge**；评审层集中 `src/review/`。

**DoD**
1. 5 Tab 全部接入真实接口，demo 现有功能（筛选 / 分页 / 排序 / 详情弹框）不缺失。
2. `pnpm type-check` / 自检 / build 三绿。
3. D9 附录 D 防漏扫描通过，handoff 附扫描摘要。
4. 评审模式关闭后 DOM 零泄漏（无 `metric_id` / `Q0xx` / `GAP-*` / 就绪度字样）。
5. iframe 弹框三态实测：有 `detail_url` 嵌入 / 空 `detail_url` 兜底抽屉 / 对端禁嵌时降级跳新页签（需 04 号单结论）。

---

## E · 联调与验收（1 张）

### 08 `SYSINT-05-07-08-L01` · 智库真联调与三方验收

| 项 | 值 |
|---|---|
| 名称 | 前端 + 展示 Java + 智谱三方 9 端点逐字段验收 |
| 监管 / 认领 | `human:李伟` / `human:李伟` + `human:孔东` |
| 执行 | `agent:qa-agent` + `human:李伟`（对端协调） |
| 仓 | `gkx-orchestration`（验收记录归档） |
| 依赖 | 04、06、07 |
| 优先级 | E 段第 1 张（唯一） |

**交付产物**
- 联调环境申请记录：测试地址 / 测试账号 / 联调窗口（凭证不落盘）。
- 9 端点逐字段验收表：每端点每字段标 实测值 / 文档值 / 差异 / 处置。
- 验收签字单：智谱 + 智树 + 总集三方会签。

**DoD**
1. 9 端点逐字段全绿，差异项逐条闭环。
2. 敏感字段对外口径按 04 号单裁定执行并验收。
3. 三方会签单归档 `对接文档/我方/`。

---

## 附 1 · 任务编号总表

| 子任务行 | 任务号 | 名称 | 仓 | 依赖 |
|---|---|---|---|---|
| WBS-05-07-01 | `SYSINT-05-07-01-L01` | 智库契约登记 + EXT-B4-ZHIKU 建包 | `gkx-orchestration` | — |
| WBS-05-07-02 | `SYSINT-05-07-02-L01` | 智库鉴权打通（双 token） | `gkx-orchestration` | 01 |
| WBS-05-07-03 | `SYSINT-05-07-03-L01` | D1–D5 + B1–B5 裁定函 | `gkx-orchestration` | — |
| WBS-05-07-04 | `SYSINT-05-07-04-L01` | iframe 白名单 + 敏感字段合规 | `gkx-orchestration` | 03 |
| WBS-05-07-05 | `BE-DISPLAY-SVC-THINKTANK-GATEWAY-L01` | 展示 Java 网关双路由 | `lumen-svc-platform` | 01、02、03 |
| WBS-05-07-06 | `BE-DISPLAY-SVC-THINKTANK-API-L01` | 智库 9 端点业务转发 | `lumen-svc-platform` | 05 |
| WBS-05-07-07 | `FE-DISPLAY-SVC-THINKTANK-REPLICA-L01` | 5 Tab 复刻 + IframeDetailModal + D9 | `lumen-ui-science-pc` | 03、04、06 |
| WBS-05-07-08 | `SYSINT-05-07-08-L01` | 智库真联调与三方验收 | `gkx-orchestration` | 04、06、07 |

## 附 2 · 依赖图

```
01 契约登记 ──┐
              ├─→ 05 网关双路由 ─→ 06 业务转发 ─┐
02 鉴权打通 ──┘                                 │
                                                ├─→ 08 真联调验收
03 D1-D5+B1-B5 ─→ 04 iframe 白名单+合规 ─┐      │
                  │                       ├─→ 07 前端复刻 ─┘
                  └───────────────────────┘
```

## 附 3 · 登记与状态同步

- 本稿经 PM 签字后：
  1. 8 张子任务落 `agent-delivery/task-registry.yaml`，状态初值 `ready`，`supervised_by: human:李伟`，`claimed_by: human:孔东`。
  2. `agent-delivery/工程过程/04-系统集成/05-展示系统集成/WBS.md` §1 智库服务行追加 8 子任务号；§4 新增 `WBS-05-07-0N` 子任务行区块（参照 WBS-05-23 拆法）。
  3. 主任务 `SYSINT-05-07-L01` 状态由 `ready` 升 `claimed`（首个子任务开工时）。
- 完成日期要求（11月倒排）由 PM 填，本稿不预填。

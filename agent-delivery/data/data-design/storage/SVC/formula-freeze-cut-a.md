# SVC 公式冻结清单（切法 A）

> **doc_id**：`SVC-FORMULA-FREEZE-CUT-A`  
> **日期**：2026-08-21  
> **拍板**：`human:淮政玮`（微信 · 2026-08-21 · **选 A · 否 C**）  
> **本叶**：`DEMO-SVC-LAB-GATE-L01`（F-GATE，现场只认 50100）  
> **用途**：给下一份 **P 总控**消费；**本文件不授权施工 50892**，不改 lumen 四仓。  
> **Q 项**：Q060 / Q062 / Q063 / Q-SVC-010 **不因本清单或开 P 变绿**。

---

## 0. 冻结范围

本清单冻结的是 **切法与对象**，不是把黄灯改绿。

| 站 | 本清单 |
|----|--------|
| 50100 产业服务算法库 | F 底座已施工；GATE 核现场 |
| 50892 专题 | **未开**；P 总控另写 |
| 30999 原型 | 只读对照；禁 merge 进 lumen |

禁止：两套 hang、第二张图空间、新建 Edge 类型、把迈瑞/华为 fixture 填回图、F 绿自动续 P。

---

## 1. 图谱：一张图两种滤镜

| 项 | 冻结 |
|----|------|
| 空间 | 只认 Demo `demo_gkx_chain`（决策 #7）。禁止 `gkx_service` / Neo4j / 正式 `gkx_chain` |
| hang | 服务机构点 `institution:{org_id}`，`props.role=service`。圈定全量 hang，不另造平行图 |
| 滤镜（P 才做 UI） | **同一 hang**：① 仅机构 ② 机构+关联主体。开关只滤显示，不换空间、不换 hang |
| 边类型 | 只用已有 `belongs_to` / `participates` / `supplies` / `depends_on`。禁止 CREATE `serve`/`coop`/`invest` |
| 30999 标签 | 合作/投资等映射到底图 `participates`；`mapped_from` 写在 hang.ext。禁止当新 Edge |
| 关联主体 | 一跳只复用 ENT 已 hang 到同一张 G 的点；对端不在 hang 里就诚实不画。禁止 GraphView 内置 22 点 / 迈瑞华为 fixture |
| F 现状 | 滤镜 ② **未施工**；50100 只保证滤镜 ① 或诚实空图 |

---

## 2. 关系链：双密度并排

公式一律：`density = 2E / (N*(N-1))`（N&lt;2 时记 0，不报假数）。

| 指标 | N | E | 展示 |
|------|---|---|------|
| 机构子网密度 | 圈定服务机构点数 | 机构↔机构边 | 现 ADS `SVC_SERVICE_RELATION_CHAIN` |
| 生态网密度 | 滤镜 ② 可见点（机构+已 hang 关联主体） | 对应可见边 | **P 才算**；与子网密度 **并排**，禁止默默切换 N |

口径仍挂 **Q062**，待甲方，UI「待核验」。P 不得用生态密度覆盖子网列而不改列名。

列表抽样 N=50；圈定 hang 仍全量。

---

## 3. 短板：对象仍是服务机构

| 项 | 冻结 |
|----|------|
| 运行时 | **Q-SVCCHAIN-03**：0 家空白 / ≤1 家薄弱 / 均深&lt;55 瓶颈 |
| 计数对象 | 环节里的 **服务机构**。企业/高校/资本 **不**计入空白/薄弱/瓶颈 |
| Q061 | 对照列 + `pending_client`。F 与 P 运行时 **不要切过去** |
| 模型 ID | `SVC_SERVICE_CHAIN_GAP` |

---

## 4. 六类技术力：对象仍是服务机构

| 项 | 冻结 |
|----|------|
| 六类 | `FINANCE` / `IP` / `HR` / `MKT` / `CONSULT` / `INNOV` |
| `(unclassified)` | **不是**第 7 类；不进雷达行 |
| 口径 | Q060 五维等权；待甲方，不伪闭合 live |
| 行对象 | 服务机构。禁止把企业写成技术力行 |
| 模型 ID | `SVC_*_TECH_POWER` × 6 |

---

## 5. 引入 / 培育：名单仍是机构

| 项 | 冻结 |
|----|------|
| 推荐行 | 服务机构 Top50（N=50） |
| 企业/资本 | 只当特征（如深圳连接度），**不**写成推荐行 |
| 口径 | Q063 待甲方；招引权重 35/30/20/15，培育 25/30/25/20（代理自 `service-center`） |
| 模型 ID | `SVC_ATTRACTION_RECOMMEND` / `SVC_CULTIVATION_RECOMMEND` |

---

## 6. 出数与黄灯（F/P 共用）

1. 读契约表 → Python 算 → 回写 Demo ADS/图。禁止 fixture / 前端目录充数。  
2. 线上名单 **不 JOIN ODS**；名称读 `svc_org_card`。  
3. Q-SVC-010 圈定规则 **始终** `pending_client_confirm=1`。  
4. 本机 Nebula 可诚实失败，不得报假成功。  
5. 调用链：F 沿 50100 → `demo-algo-ent-analysis` `/entan/internal/svc/*`；P 才走前端 → Java → Python `/internal/*`，且 lumen 不调 `demo-*`（D12）。

---

## 7. 本清单明确不施工

- 50892 / P 总控正文 / lumen 四仓  
- 双滤镜 UI、生态密度列、多元点 hang  
- 把 Q060/Q062/Q063/Q-SVC-010 改绿  

P 总控开工条件：**本 GATE 叶由 `human:淮政玮` 签收到 `done`** 之后，另写授权，不写「F 绿自动续 P」。

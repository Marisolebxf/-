# FUNC-DESIGN · E7 政策分析

> **状态**：draft（v0.2）· 派生自交互五件套 + 已批 DEC；接口字段待架构定稿回填  
> **日期**：2026-08-07  
> **Track**：Track-MS（专题）+ 门户展示承接  
> **derived_only**：`true`（禁止本文件扩 scope；冲突先回写五件套 / DEC）  
> **规程**：`产品定义评审规程.md` §3.5（v2.7）  
> **样例对照**：`E2-产业链分析/.../FUNC-DESIGN-CHAIN-TOPIC-DIAGNOSIS.md`、`FUNC-DESIGN-CHAIN-PORTAL-OVERVIEW-PANORAMA.md`

---

## 0. 权威与派生关系

| 类型 | 路径 / ID | 版本（填表时核对） |
| --- | --- | --- |
| IA | `IA-E7-政策分析.md`（同目录） | v1.4.5+ |
| TRACE | `TRACE-E7-政策分析.yaml`（同目录） | 与包同步 |
| USM | `USM-E7-政策分析.md`（同目录） | v1.4.8 |
| Wireframe | `Wireframe-E7-政策分析.md`（同目录） | 与包同步 |
| UX-SPEC | `UX-SPEC-E7-政策分析.md`（同目录） | 与包同步 |
| DEC（对象流） | `DEC-E7-POLICY-LAUNCH-FROM-INDUSTRY-BASKET-20260807` · `DEC-E7-POLICY-SCOPE-MUTEX-20260807` | 已批 |
| DEC（门户） | `DEC-E7-PORTAL-TAB-MERGE-A` · `NO-GLOBAL-FILTER` · `STATS-MAP-DENSITY` · `STATS-INDUSTRY-COMPARE` · `RANK-PRESENTATION` · `SHENZHEN-MIRROR` | 已批 |
| DEC（共享） | `DEC-E7-SEARCH-REUSE` · `SYSTEM-TASK-REUSE` · `REPORT-TEMPLATE-HTML-PDF` · `OPS-REUSE` | 已批 |
| Bid 专题 | `bid-reference/科技信息展示系统和科技专题服务系统.md` §1.1.1.2.4.2.6（P-70/P-72/P-73） | — |
| Bid 门户 | `bid-reference/智慧服务门户系统-要素相关.md`（P-17~P-22） | — |
| Demo 仓 | `${GKX_ROOT}/repos/demo-ui-topic` · `/policy/*` · `/policy-portal/*` | 实现证据，非需求源 |

**派生铁律**：本说明书只重组已批产品行为；不得新增 Bid 叶子、角色、metric 语义或验收范围。

---

## 1. 模块目标与不承接

### 1.1 目标

在「政策分析」二级菜单域内交付：

1. **门户政策扶持展示**（单壳四 Tab）：概览 / 产业覆盖 / 最新政策动态 / 深圳政策（P-17~P-22）。  
2. **政策查询**：智能检索 / 查政策 / 高级筛选；**仅语料核对与画像**，不入篮、不发起分析（US-E7-POL-01c）。  
3. **三项计算型分析**（配置 → 系统任务过程 → 显式查看不可变结果 → 可选报告）：  
   - 政策时序分析（P-70）  
   - 区域政策对比（P-72）  
   - 深圳政策现状分析 · 三维框架与指标体系构建（P-73）  
4. **维护管理**（复用 ENT-OPS 菜单形态，不承接企业字段硬套）。  
5. 接入共享：**系统对比篮·产业 Tab**、**SystemTaskLayer**、**ENT-EXPORT**（HTML→PDF）。

### 1.2 不承接

| 项 | 说明 |
| --- | --- |
| 对比篮「政策」文档 Tab | 已废止；三项分析不以政策文档为对象 |
| 查询/门户「深度分析」直达 | 禁止绕过对比篮/配置合同 |
| 展示系统 DS-10/11/12 与核增多维对比结果页 | 另包 |
| P-74 / P-75 独立报告页 | Wave2；本包结果页内嵌可视化，不宣称独立页关闭 |
| 对比篮/任务/报告壳层内部实现 | 归属 ENT-COMPARE / SystemTaskLayer / ENT-EXPORT |
| 前端 NLP / 图谱 / 杜撰生产公式 | 算法经 Java → Python `/internal/*`；Demo 得分仅演示聚合 |
| 统一智能检索全站页 | 其它厂商范围 |

---

## 2. 对象 / 身份 / 路由参数

### 2.1 对象合同（`DEC-E7-POLICY-SCOPE-MUTEX`）

| 对象 | 稳定身份 | 规则 | 禁止 |
| --- | --- | --- | --- |
| 产业 | `industry_id`（`object_type=industry`） | 恰好 **1**；可篮分发或页选 | 与技术领域同时生效 |
| 技术领域 | `tech_field_id[]`（`object_type=tech_field`） | 可多选 **≥1**；**仅页内**，不进篮 | 写入对比篮 |
| 政策文档 | `policy_id` | 查询/详情画像；可选核对语料 | 入篮发起三项分析 |
| 分析任务 / 结果 | 共享 `analysis_task` / `result_id` | 配置提交后快照冻结 | 页内私造任务中心 |
| 报告 | `report_template_id` + fingerprint | HTML 预览 → 同源 PDF | 跳过 HTML 直出 PDF |

### 2.2 路由

| 路由 | 职责 | Bid / 故事 |
| --- | --- | --- |
| `/policy-portal/overview?tab=&view=` | 门户单壳四 Tab | P-17~P-22 · US-08 |
| `/policy/search?mode=smart\|policy\|advanced` | 政策查询（核对语料） | US-01c · DEC-SEARCH-REUSE |
| `/policy/overview` | 时序分析工作区 | P-70 · US-02 |
| `/policy/analysis` | 区域对比工作区 | P-72 · US-03 |
| `/policy/recommendation` | 深圳三维工作区 | P-73 · US-04 |
| `/policy/maintenance` | 维护管理 | US-09 · DEC-OPS-REUSE |

### 2.3 工作区 URL 参数（分析页）

| 参数 | 说明 |
| --- | --- |
| `demo_state=config\|processing\|result` | 三段态 |
| `object_type` / `object_ids[]` / `object_names[]` | 锚点 |
| `source=compare-basket\|page` | 来源 |
| `analysis_type` | Registry key |
| `task_id` / `result_id` | 任务与结果 |
| `granularity` | 时序：year\|quarter\|month |
| `regions[]` / `dims[]` | 区域对比 |
| `weight_support\|fit\|effect` | 三维一级权重 |
| `indicators_support[]\|fit[]\|effect[]` | 二级入模指标 id |

---

## 3. 功能点清单

### 3.1 门户政策扶持（展示）

| # | 功能点 | Bid | 五件套锚点 | 工程备注 |
| --- | --- | --- | --- | --- |
| F-PT-01 | 单壳四 Tab | P-17~P-22 | DEC-TAB-MERGE-A · US-08 | `/policy-portal/overview` |
| F-PT-02 | 概览 stats/map/rank | P-17/18/20 | STATS-MAP-DENSITY · RANK | 无页级全局筛选 |
| F-PT-03 | 产业覆盖 / 最新动态 / 深圳 | P-19/21/22 | SHENZHEN-MIRROR | 深圳无力度榜；各区对照 |
| F-PT-04 | 浏览与详情 | — | Wireframe 门户 | **不**写政策文档入篮；不发起分析 |

### 3.2 政策查询

| # | 功能点 | Bid | 五件套锚点 | 工程备注 |
| --- | --- | --- | --- | --- |
| F-SQ-01 | ElementSearchWorkbench 同构 | 关联准备解释 | DEC-SEARCH-REUSE · US-01c | storage 与门户分轨 |
| F-SQ-02 | 智能 / 查政策 / 高级筛选 | — | Wireframe F-POL-00 | 高筛独立 mode 页 |
| F-SQ-03 | 结果画像 / 详情抽屉 | — | US-01c | 无「加入对比篮」「深度分析」 |

### 3.3 三项分析 · 公共壳

| # | 功能点 | 五件套锚点 | 工程备注 |
| --- | --- | --- | --- |
| F-AN-00 | 产业篮分发「政策分析」分组 | US-05 · DEC-LAUNCH-FROM-INDUSTRY | 恰好 1 产业 |
| F-AN-00b | 页内锚点 XOR | US-01b · SCOPE-MUTEX | 技术领域可多选不进篮 |
| F-AN-00c | 关联政策概要 | Bid `.6.1.1` | 配置态只读预览；系统自动关联 |
| F-AN-00d | 配置→生成分析→过程→显式查看结果 | US-02/03/04/06 | 复用 SystemTaskLayer |
| F-AN-00e | 有效结果生成报告 HTML→PDF | US-07 · DEC-REPORT | `policy:report:{templateId}` |

### 3.4 政策时序分析（P-70）

| # | 功能点 | 配置 | 结果 |
| --- | --- | --- | --- |
| F-TS-01 | 时序粒度 | year / quarter / month | 快照只读 |
| F-TS-02 | 密度 / 支持强度趋势 | — | 折线 + 堆叠面积 |
| F-TS-03 | 关键节点时间轴 + 明细表 | — | 点选打开政策详情 |
| F-TS-04 | 关键节点洞察 | — | 业务文案；连续性口径 Pending 仅评审态 |

过程阶段（可见）：`政策关联聚合 → 时序模型构建 → 窗口期识别 → 结果组装`。

### 3.5 区域政策对比（P-72）

| # | 功能点 | 配置 | 结果 |
| --- | --- | --- | --- |
| F-RG-01 | 对比区域 | ≥2 | 快照只读 |
| F-RG-02 | 评价维度 | ≥1 | 矩阵列 |
| F-RG-03 | 矩阵 / 雷达 / 热力 / 差异结论 | — | SecondaryAnalysisTabs |
| F-RG-04 | 条款溯源抽屉 | — | 单元点选；NLP 缺口仅评审注 |

过程阶段：`条件校验 → 区域对齐 → 多维对比 → 结果组装`。

### 3.6 深圳政策现状分析（P-73）

| # | 功能点 | 配置 | 结果 |
| --- | --- | --- | --- |
| F-SZ-01 | **指标体系构建（合并 UI）** | 每维：行内一级权重% + 下方二级指标卡片勾选 | 快照：一级权重 + 入模清单 |
| F-SZ-02 | 维内权重 | **等权自动均分**（方案 A）；只读标签 | 下钻仅入模指标 |
| F-SZ-03 | 一级权重校验 | 三项合计 = 100%；可一键均分 | — |
| F-SZ-04 | 入模校验 | 每维 ≥1 核心指标 | — |
| F-SZ-05 | 仪表盘 / 雷达 / 短板 / 策略 | — | 演示聚合；正式算分走 API |

过程阶段：`条件校验 → 三维评分 → 短板识别 → 结果组装`。

招标锚点：`§1.1.1.2.4.2.6.3.1 指标体系构建`（三维框架下自由选择核心指标）。

### 3.7 维护管理

| # | 功能点 | 五件套 | 备注 |
| --- | --- | --- | --- |
| F-OPS-01 | ENT-OPS 菜单形态复用 | US-09 · DEC-OPS-REUSE | 内容运营 / 图谱运营 / 分析配置；不硬套企业字段 |

---

## 4. 交互与控制边界

### 4.1 分析页状态机

```text
[config] 配置合法 → 点击「生成分析」
    ↓
创建 analysis_task + 配置快照冻结（URL / 任务）
    ↓
[processing] StageSteps（queued 可撤回；running 不可取消）
    ↓ succeeded 且用户显式「查看结果」
[result] 不可变结果 + 可选「生成报告」
    ↓
report 任务 → HTML 预览 → 同源 PDF
```

同类型已有 queued/running → **不**新建，引导恢复原任务。

### 4.2 发起边界

| 允许 | 禁止 |
| --- | --- |
| 产业篮勾选 1 产业 → 政策分析分组分发 | 政策文档入篮发起 |
| 配置页产业 XOR 技术领域 | 产业与技术领域同时生效 |
| 查询打开摘要核对语料 | 查询「深度分析」带对象直达配置发起 |
| 门户浏览 | 门户写政策文档入篮 / 跑分析任务 |

### 4.3 深圳合并配置区控制边界

| 区域 | 允许 | 禁止 |
| --- | --- | --- |
| 维度标题行 | 调一级权重；查看入模摘要 | 删除三维框架维度 |
| 二级指标卡片 | 勾选/取消入模 | 维内手调权重（方案 A） |
| 工具栏 | 一键均分一级权重；恢复默认模型 | 配置页导出报告 |

### 4.4 业务 / 评审双模

- 业务模式：不渲染 Trace / Mock / Pending / 开放项明文。  
- 评审模式：挂载 metric_spec / mock_badge / pending_badge / requirement_trace（见 Wireframe `review_trace_contract`）。

---

## 5. 参数 / 任务快照 / 导出

### 5.1 task_type（Demo / SYS-JOBS 约定）

| 分析 | analysis taskType | report templateId（示例） |
| --- | --- | --- |
| 时序 | `policy:overview:policy_timeseries` | `POL-TIMESERIES-PDF-v1` |
| 区域 | `policy:analysis:policy_region_compare` | `POL-REGION-COMPARE-PDF-v1` |
| 深圳三维 | `policy:recommendation:policy_sz_3d` | `POL-SZ-3D-PDF-v1` |
| 报告 | `policy:report:{templateId}` | — |

> TRACE 登记名：`policy_timeseries_analysis` / `policy_region_compare` / `policy_sz_3d_assessment`（产品语义）；实现键以上表 surface 约定为准，定稿后对齐。

### 5.2 快照规则

| 规则 | 说明 |
| --- | --- |
| 提交前 | 草稿可改；不写成功任务历史 |
| 提交后 | 对象、粒度/区域维度、一级权重、入模指标列表冻结 |
| 结果 | 不可变；「复制配置」开新草稿 |
| 维内权重 | 不单独持久化百分比字段；由入模列表推导等权 |

### 5.3 导出

- 仅有效结果可生成报告。  
- 统一模板：先 HTML 预览，再下载同源修订 PDF。  
- 政策模块只提供 `report_template_id`、章节 payload、fingerprint。

---

## 6. 接口与数据合同骨架

调用链铁律：**前端 → Java REST →（必要时）Python `/internal/*`**；前端不直连算法/图库；Java 不写 nGQL、不做 NLP。

| 能力 | 建议 Java 门面（TBD） | Python internal（TBD） |
| --- | --- | --- |
| 政策检索 | `GET/POST /topic/v1/policy/search` | 可选 `/internal/v1/policy/search` |
| 关联语料概要 | `GET .../policy/corpus-preview` | `/internal/v1/policy/associate` |
| 创建时序任务 | `POST .../policy/timeseries/tasks` | `/internal/v1/policy/timeseries/...` |
| 创建区域对比任务 | `POST .../policy/region-compare/tasks` | `/internal/v1/policy/region-compare/...` |
| 创建深圳三维任务 | `POST .../policy/sz-3d/tasks` | `/internal/v1/policy/sz-3d/...` |
| 查询任务/结果 | `GET .../tasks/{id}` · `.../result` | — |
| 报告导出 | 复用 ENT-EXPORT 合同 | — |
| 门户展示块 | `GET .../portal/policy/...` | — |

> TODO：请求/响应 JSON 示例、错误码、幂等与 fingerprint 字段（对齐诊断 FUNC-DESIGN 粒度）。

---

## 7. 权限与异常态

| 场景 | 行为 |
| --- | --- |
| 无锚点进分析页 | 可配置；引导打开产业篮或页内选产业/技术领域 |
| 一级权重 ≠100% / 任维 0 指标 | 「生成分析」禁用 |
| 同类型任务进行中 | 复用并恢复过程页 |
| queued | 可撤回 |
| running | 无取消 |
| 查询零命中 | 空态；不伪造推荐冒充命中 |
| 关联政策为空 | 分析区空态；更换锚点 |
| 无报告权限 | 生成/下载锁态；结果仍可读 |
| 过期结果点报告 | 失败关闭；可复制配置重跑 |
| 评审模式关闭 | 评审挂载完整隐藏 |

产品角色见 IA §2；前端不从 Mock 用户推断权限。

---

## 8. 开放项与待填

| ID | 问题 | 建议处置 |
| --- | --- | --- |
| POL-FDS-01 | Java/Python 路径与字段终表 | 架构 + API 定稿后回填 §6 |
| POL-FDS-02 | `task_type` 产品名 vs Demo surface 键对齐 | 与 SystemTaskLayer 枚举会签 |
| POL-FDS-03 | 政策密度指数正式公式（GAP-E7-01） | 甲方/算法；UI 代理件数 |
| POL-FDS-04 | 三维指标全集与一级默认权重（QPOL-02） | 客户决策清单；UI ⚠️ |
| POL-FDS-05 | 落地实效 ODS 缺口（GAP-E7-04） | 数据采购前 Mock + Pending |
| POL-FDS-06 | 技术领域正式分类体系 | 数据侧；Demo 单一 Mock 体系 |
| POL-FDS-07 | 维护管理字段与 ENT-OPS 映射表 | OPS-REUSE 落地清单 |
| POL-FDS-08 | 门户 CMS 文案是否拆 SPEC-CMS | 会议点名则另建附录 |

---

## 9. 填充检查清单（出 v1.0 前）

- [ ] TRACE `leaves_required` 与本 §3 功能点双向勾完（含门户 6 + 专题 3）  
- [ ] UX-SPEC 状态机 / 合并配置区与本 §4 无冲突句  
- [ ] USM v1.4.8+ 主路径 C 与 F-SZ-01 合并样式一致  
- [ ] §6 至少各分析 1 个创建任务接口有示例 JSON  
- [ ] 架构抽检：无前端直连 Nebula / Python；无 Java 内 NLP  
- [ ] 评审/业务双模：业务 DOM 无 QPOL / Mock / GAP 明文  

---

## 10. 修订记录

| 版本 | 日期 | 说明 |
| --- | --- | --- |
| v0.2 | 2026-08-07 | 首版汇编：对照产业链 FUNC-DESIGN 样例；纳入产业篮发起、SCOPE-MUTEX、查询仅核对语料、P-73 合并指标体系构建 |

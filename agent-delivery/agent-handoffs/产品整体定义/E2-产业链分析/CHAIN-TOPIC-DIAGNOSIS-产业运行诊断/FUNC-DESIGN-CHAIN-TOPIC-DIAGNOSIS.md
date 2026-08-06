# FUNC-DESIGN · 产业运行诊断

> **状态**：skeleton（v0.2）· 待按交互五件套填满工程章节  
> **日期**：2026-08-06  
> **Track**：Track-MS  
> **derived_only**：`true`  
> **规程**：`产品定义评审规程.md` §3.5（v2.7）  
> **会议对照**：功能设计说明文档 · 项 3（三报告入口 / 参数 / 任务快照 / 导出个人中心）  
> **修订**：对齐五件套 v1.13 瓶颈词汇分层。`DEC-CHAIN-DIAG-BOTTLENECK-VOCAB-LAYERS-20260806`。

---

## 0. 权威与派生关系

| 类型 | 路径 | 版本（核对） |
| --- | --- | --- |
| IA | `IA-CHAIN-TOPIC-DIAGNOSIS.md`（同目录） | v1.13-bottleneck-vocab-layers |
| TRACE | `TRACE-CHAIN-TOPIC-DIAGNOSIS.yaml`（同目录） | 1.13-bottleneck-vocab-layers |
| USM | `USM-CHAIN-TOPIC-DIAGNOSIS.md`（同目录） | 同版 |
| Wireframe | `Wireframe-CHAIN-TOPIC-DIAGNOSIS.md`（同目录） | 同版 |
| UX-SPEC | `UX-SPEC-CHAIN-TOPIC-DIAGNOSIS.md`（同目录） | 1.13-bottleneck-vocab-layers |
| DEC | `DEC-CHAIN-DIAG-BOTTLENECK-VOCAB-LAYERS-20260806`（及包内其他已批 DEC） | 已引用 |
| Bid 展示 | `1.1.1.2.4.2.2.2` / `.2.2.4` / `.2.2.5` | — |
| Bid 算法 | `1.1.1.1.1.1.1.3.6` / `.3.8` / `.3.9` | — |
| 复用 | `REUSE-MATRIX-CHAIN.md`（系统任务、报告阅读、个人资产） | — |

三项诊断**各自保留 Bid 叶子**；同工作空间 ≠ 合并需求。

---

## 1. 模块目标与不承接

### 1.1 目标

在 `/industry-center/diagnosis` 二级工作空间内完成：

1. **产业周期分析**（对象：`industry`）  
2. **产业关键环节识别**（对象：`industry_chain`）  
3. **产业瓶颈堵点五维诊断**（对象：`industry_chain`；维名含「资本」）  
4. 本工作空间 **诊断记录** 过滤与恢复  

统一壳：配置 → 点击生成 → **可视化过程阶段** → 显式查看不可变结果 → 可选导出/交接个人中心。

### 1.2 不承接

- 全景图谱、区域评价、深圳决策、门户总览改造  
- 关键/瓶颈正式可编辑权重或前端自定阈值  
- 页内 PDF 引擎、模型训练控制台、可操作联网检索控制台  
- 跨二级页自动继承对象  

---

## 2. 对象 / 身份 / 路由参数

| 对象 | 稳定身份 | 适用报告 | 禁止 |
| --- | --- | --- | --- |
| 产业 | `industry_id` | 周期 | 静默改成 chain |
| 产业链 | `chain_id`（兼容 `industry_id` 解析） | 关键 / 瓶颈 | 周期消费 chain |
| 参数快照 | `parameter_snapshot_id` | 全部 | 未提交写入任务历史 |
| 分析任务 / 结果 | 共享 `analysis_task` / result id | 全部 | 页内私造任务中心 |

| 路由 | Tab |
| --- | --- |
| `/industry-center/diagnosis` | `cycle` / `key-link` / `bottleneck` / `records` |

Tab 切换写 URL；**不共享**各 Tab 配置与结果焦点（UX-SPEC §5.1）。

---

## 3. 三大报告 · 功能点清单（骨架）

### 3.1 入口

| 报告 | Tab | 对象确认入口 | 生成 CTA |
| --- | --- | --- | --- |
| 周期分析 | `cycle` | 对比篮选产业 / 对象条 | 「生成分析」 |
| 关键环节 | `key-link` | 对比篮选产业链 | 「生成分析」 |
| 堵点五维 | `bottleneck` | 对比篮选产业链 | 「生成分析」 |
| 历史恢复 | `records` | 过滤本工作空间任务 | 打开结果 / 复制配置 |

### 3.2 参数配置项（骨架 · 细节回填 UX-SPEC / Wireframe）

| 报告 | 可配 | 只读确认 | 禁止 |
| --- | --- | --- | --- |
| 周期 | 市场规模 / 增长率 / 利润率 / 技术成熟度等注册参数（见 US-01） | 模型/数据版本 | 配置「如何联网」 |
| 关键 | — | 固定模型因子 | 伪编辑权重 |
| 瓶颈 | — | 五维定义（含资本） | 前端改阈值；维名不用错 |

> TODO：逐字段表（名 / 类型 / 范围 / 默认 / 校验错误码）。

### 3.3 过程阶段（Bid 能力词必须可见）

| 报告 | 过程要点（派生） |
| --- | --- |
| 周期 | 联网检索 → 大模型推理与周期阶段判断 → 趋势预测/驱动因素/拐点 → 报告组装 |
| 关键 | `.4.1`/`.4.2` 词汇阶段（全链结构、关键标注等） |
| 瓶颈 | `.5.1`/`.5.2` 词汇阶段（多维健康、卡脖子、成因与建议） |

### 3.4 结果阅读（骨架）

| 报告 | 结果区要点 |
| --- | --- |
| 周期 | 回溯—诊断—预测；**无**顶栏「阶段评分/技术成熟度」数值卡（DEC-HIDE-CYCLE-SCORE-KPIS） |
| 关键 | 全链结构化 + 关键标注；企业抽屉交接 |
| 瓶颈 | 五环节健康图谱（L1 分档）+ 瓶颈/卡脖子判定角标（L2/L2+）+ 详情归因；`卡脖子 ⊂ 瓶颈`；禁断链（DEC-BOTTLENECK-VOCAB-LAYERS） |

### 3.5 瓶颈词汇契约（工程字段建议）

| 字段 | 含义 | 规则 |
| --- | --- | --- |
| `link_health[].band` | L1 稳健/关注/薄弱 | 仅由健康度阈值；薄弱≠瓶颈 |
| `bottlenecks[]` | L2 瓶颈清单 | 算法主输出 |
| `bottlenecks[].is_choke` | L2+ 卡脖子 | Demo/临时默认：`severity=高`；正式阈值待算法表 |
| — | 断链 | 本模块不输出、不展示 |

---

## 4. 任务快照机制

```text
草稿配置（可改）
   ↓ 点击「生成分析」且校验通过
创建 analysis_task + 固化 parameter_snapshot（不可变）
   ↓
过程阶段事件流（可观察、可失败降级）
   ↓
result 文档（不可变）← 同指纹可复用（REUSE-MATRIX）
   ↓
records 可恢复；「复制配置」生成新草稿（新 snapshot）
```

| 规则 | 说明 |
| --- | --- |
| 提交前 | 不写任务历史 |
| 失败 | 不建成功任务；草稿可改 |
| 指纹 | CHAIN 独立 task_type / fingerprint；不读企业 storage key |
| task_type | `CHAIN_*`（具体枚举 TBD，对齐 system-tasks） |

---

## 5. 报告导出 → 个人中心

| 步骤 | 行为 |
| --- | --- |
| 发起 | 自**结果页**触发导出/交接（不在配置页） |
| 产物 | 系统报告文档 + 指纹；阅读器用共享 `SystemReportReader` |
| 落个人中心 | 经共享资产注册/投影；**禁止** CHAIN 直读企业 `PersonalAssets` storage key |
| 权限 | 服务端鉴权；失败关闭 |

> TODO：导出格式（PDF/站内报告）、个人中心分区名、API 合同。

---

## 6. 接口与数据合同骨架

调用链：前端 → Java → Python `/internal/*`（算法）；Java 不写 nGQL、不做 NLP。

| 能力 | 建议 Java 门面（TBD） | Python internal（TBD） |
| --- | --- | --- |
| 创建周期任务 | `POST /topic/v1/chain/diagnosis/cycle/tasks` | `/internal/v1/chain/cycle/...` |
| 创建关键任务 | `POST .../key-link/tasks` | `/internal/v1/chain/key-link/...` |
| 创建瓶颈任务 | `POST .../bottleneck/tasks` | `/internal/v1/chain/bottleneck/...` |
| 查询任务/过程 | `GET .../tasks/{id}` | — |
| 查询结果 | `GET .../tasks/{id}/result` | — |
| 导出交接 | `POST .../tasks/{id}/export` | — |
| 记录列表 | `GET .../diagnosis/records` | — |

> TODO：请求/响应 JSON、错误码、幂等与指纹字段。

---

## 7. 权限与异常态

| 场景 | 行为 |
| --- | --- |
| 无对象 | 配置区可见；生成禁用；引导打开对比篮 |
| 对象类型错误 | 禁止提交 + 说明 |
| 参数越界 | 定位字段 |
| 权限不足 | 锁态 + 原因 |
| 检索未接通 | 诚实降级文案（周期） |
| Mock / Pending | 评审模式标识；业务模式不泄露内部文案 |

产品角色映射见 IA §2（GOV/INNO×L*）；前端不从 Mock 用户推断权限。

---

## 8. 开放项与待填

| ID | 问题 | 建议处置 |
| --- | --- | --- |
| DIAG-FDS-01 | `CHAIN_*` task_type 枚举终表 | 与 system-tasks 对齐后回填 §4 |
| DIAG-FDS-02 | 个人中心资产分区与 API | 架构 + 前端；遵循 REUSE-MATRIX |
| DIAG-FDS-03 | 周期参数完整字段与校验 | 回写 Wireframe / UX-SPEC 后填 §3.2 |
| DIAG-FDS-04 | 专题 metric readiness 矩阵行 | 无行时不投影伪 D1–D4（UX-SPEC） |
| DIAG-FDS-05 | 导出文件格式与保留期 | 产品 + 合规 |

---

## 9. 填充检查清单（出 v1.0 前）

- [ ] US-CHAIN-DIAG-01～07 均有 §3/§4/§5 锚点  
- [ ] 三报告过程 Bid 词与 UX-SPEC §5 一致  
- [ ] 快照不可变规则有接口字段支撑  
- [ ] 导出→个人中心路径无企业 storage 耦合  
- [ ] 架构抽检：算法只在 Python；前端不直连  

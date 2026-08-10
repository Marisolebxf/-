# ENT-MOD-EXPORT：全局导出与报告模板升级

> 草案状态：待 PM 审阅；不构成 `task-registry.yaml` 建单、状态变更或任务认领。
>
> 发起体验 Owner：高颖；建议 PM：郭万迎；跨模块报告契约 Owner：侯佳伟。

## 1. 范围纠正

现有 `ENT-MOD-EXPORT-PDR-G1` 的台账状态为 `blocked`（“待门1 PDR”），但其关联说明存在“已通过/已完成”的表述。两者不能同时作为已闭合事实。本草案建议由 PM 先核验纪要、五件套和状态，得到以下二选一结论：

1. 证据齐全：纠正台账为已闭合，并将它作为本次升级的历史基线；
2. 证据不齐：保留阻塞并补齐/重新闭合 PDR，不把它当作可执行任务。

原始 Bid 可直接支撑“报告管理”这一系统管理能力（`bid-reference/智慧服务门户系统-要素相关.md` §1.1.1.1.3）。本次提出的跨模块统一模板、模板版本、来源快照、`report_fingerprint`、文件有效期和下载授权，超出该原始文字的细节范围；在 TRACE 中应标为 `product_enhancement`，获得 PM/决策 Owner 的 `approved_scope_change_ref` 后才进入活跃范围和正式任务台账。

## 2. 建议边界

### 纳入本轮（全局共用层）

- 统一导出入口、导出参数和产物元数据契约；
- 报告模板的最小模型：模板标识、版本、适用模块、章节映射、生成参数；
- 可追溯产物：来源快照、`report_fingerprint`、生成时间、文件有效期；
- 下载授权与审计字段的系统级约束；
- 至少一个企业模块作为 V1 体验验证入口，但不把该模块的业务指标写进全局模板。

### 明确不纳入本轮

- 企业、产业链、人才等各模块的专属报告内容、指标算法和叙事结论；
- 文件存储、保留时长、权限枚举、接口字段的最终取值（由报告契约评审决定）；
- 批量调度、运营后台、商业化配额或模板市场等新增能力。

## 3. 已有跨模块前置缺口

`SYS-ANALYSIS-JOBS` 的 `GAP-SYS-JOBS-REPORT-01` 已登记为红色缺口：跨模块报告模板、来源快照、`report_fingerprint` 和文件有效期契约；Owner 为侯佳伟，评审人为高颖、郭万迎，且阻塞 PDR-ready。

因此它不是可以绕开的新拆分项：全局导出产品包和 UX 可以并行梳理，但不能在该缺口未决时进入 PDR-ready、V1-FINAL 或 V2。

## 4. 待 PM 采纳的拆分建议

下列为建议任务，不写入注册表前均为 `backlog` 候选，且不得认领：

| 顺序 | 建议 ID | 目标与产物 | 建议负责 | 前置 |
|---|---|---|---|---|
| 0 | 纠正 `ENT-MOD-EXPORT-PDR-G1` | 核验历史 PDR、五件套与纪要，纠正“blocked/已通过”冲突 | 郭万迎 / product-agent | 无 |
| 1 | `ENT-MOD-EXPORT-PACK-L01` | IA、TRACE、USM、Wireframe：全局共用层边界及增强项清单 | product-agent，高颖共创 | 步骤 0 的结论 |
| 2a | `GAP-SYS-JOBS-REPORT-01` 闭合 | 报告契约：快照、指纹、有效期、下载授权、接口归属 | 侯佳伟 | 与步骤 1 并行；PDR 前必须闭合 |
| 2b | `ENT-MOD-EXPORT-UX-L01` | 导出入口、模板选择/预览、生成/失败/过期/无权状态与交互规格 | 高颖 / ux-agent | `PACK-L01` |
| 3 | `ENT-MOD-EXPORT-V1-HIFI-R1` | 以一个企业模块验证共用流程，不固化业务专属内容 | ui-agent | 2a、2b |
| 4 | `ENT-MOD-EXPORT-PDR-G1-RECLOSE` | 五件套、报告契约、V1 反馈和范围变更授权的门1完整闭合 | product-agent，郭万迎主持 | 2a、3、`approved_scope_change_ref` |
| 5 | `ENT-MOD-EXPORT-V1-FINAL` | 将 PDR 和 V1 反馈联合修订冻结 | product-agent + 高颖 | 4 |
| 6 | `ENT-MOD-EXPORT-V2-LUMEN` | 生产实现、联调与验收证据 | frontend/backend owners | 5 |

## 5. 需要拍板的最小决策

1. 全局模板升级是否作为 `product_enhancement` 获批，以及批准记录编号；
2. 首个 V1 验证模块：仅作为共用流程样本，不代表其业务报告模板已全局化；
3. 文件有效期、下载授权和指纹算法由谁作最终技术/业务确认；
4. 对现有 `ENT-MOD-EXPORT-PDR-G1` 采用“状态纠正”还是“重新闭合”。

## 6. 采纳后的操作纪律

- PM 先将本草案转入 `registry-gap-proposals.yaml` 审阅队列，再手工并入 `task-registry.yaml`；
- 新叶只以 `backlog` 入库，依 `scan → pending → confirm → ready` 解锁；
- 飞书表仅接收台账投影，不通过拖拽、改行或新建行创建/认领任务；
- 高颖可作为体验 Owner 审阅、共创和监管，不以本草案直接改变 PDR 状态或认领正式任务。

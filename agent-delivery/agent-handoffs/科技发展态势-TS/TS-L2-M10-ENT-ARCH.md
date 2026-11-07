# TS-L2-M10-ENT-ARCH · handoff

- 任务：`TS-L2-M10-ENT-ARCH`（definition · 关键实体与关系后台实现架构）
- 日期：2026-11-07 · 监管：`human:刘剑锋` · 认领：`agent:arch-agent`
- 状态：四角色会签完成（2026-11-07：ARCH 有条件 5 / API 有条件 1 / ALGO 同意 / DATA 有条件 2，无驳回），事实修正已回填稿；**待监管人签收**
- 开放条件（留 API 分册/PM 闭环）：① display 单入口 vs topic 直调二选一（ARCH-C1，最重）② A03 签收页加消费注记（C3）③ 序 42 自动建联缺口 PM 登记（C4）④ 全景现状读端点+发布动作落点（API 分册必答）⑤ 存量导入前置（首版无可挂技术点风险）

## 范围与实现

架构稿（真源）：[`sdd/l2/TS-L2-M10-ENT-ARCH.md`](./sdd/l2/TS-L2-M10-ENT-ARCH.md)

- 需规：全景序 41–47 七叶；34–40 报价划掉不碰；不重做 FE-TS-10A
- 核心架构：**消费 SCI-INT-A03 写回链路不重造**——四段链 FE→Java topic 门面（零写 nGQL）→Python `/internal/v1/tech/graph/changes`（单写者）→MySQL 变更三表/主表 + Nebula gkx_chain 投影 + ADS 投影（Java 只读）
- 关键裁定：§2 OI-A03-01 阻塞分档（自建主表+technology_id 首版先行 / 甲方拍板项不整体停摆）；§3 G1–G5 能力表（G2 智能关联首版不做、G5 键盘归接线单、G1/G3/G4 补齐）；VID 增量不迁移（OI-A03-02 留 C04）
- 发布流沿 A03 草案：草稿→审核(可选)→发布单事务语义（失败补偿 projection_pending）、manual>tombstone>auto 合并、base_version 乐观锁 409、回滚=反向变更集

## 偏离说明

- 对 A03 草案（draft 未评审）：本叶将其**链路/存储/版本/审计设计采纳为 M10-ENT 正式架构**——属升级引用非改写；A03 稿自身状态不变
- G2 首版不做（A03 卡有智能关联设计但 Python 无模型）——能力降级显式记录，留算法侧后续单

## 产物清单

- 新增：`sdd/l2/TS-L2-M10-ENT-ARCH.md`（调用链+数据流 Mermaid，图 ID `-SEQ`/`-DATA`）
- 调研：对照文档 A.3.1 ENT 详节（先行提交）

## 架构合规自检

| 铁律 | 状态 |
|---|---|
| 算法只在 Python / Java 零写 nGQL | ✅ §1 四段链，写全经 Python |
| 调用链 FE→Java→Python /internal | ✅ |
| Nebula TRSGraph 禁 Neo4j | ✅ 只 gkx_chain |
| D12 无 demo 依赖 | ✅ demo_gkx_chain 仅参照 |
| D15 display 不直连 | ✅ ENT 走 topic 侧 Java 门面（DN-07 模块实现单定） |
| D18 可实现 | ✅ §6 逐叶表（写目标/写者/接口）；无 mock 兜底需求（真写回） |
| 业务口径不替甲方拍板 | ✅ 9 条 DN/OI 在册，§2 分档不越权 |

## cost

- actual_tokens: ~45k
- model_used: glm-5.3（ZCode agent）
- actual_cost: <$1
- cost_warn: green

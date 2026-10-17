# CMS-JX-AUDIT-FIX-L01 · 原型符合性审计修复 handoff

- **执行**：agent:api-agent（监管人 human:徐滕强）
- **日期**：2026-10-17
- **类型**：bugfix（task_type=bugfix，P0）
- **仓**：lumen-svc-platform `origin/dev`，commit 链 `21b06c4 → 8255e4e → 3ab1234 → a1ae7e3 → 61f24d6`
- **强度**：ponytail full

---

## 1. 范围与实现

**背景**：交付久新前对 `CMS-JX-INT` 全部 19 张写侧工单做「久新原型（2026-10-17 线上版）↔ 接口规格书 ↔ 已实现代码」三方对照审计（三组并行审计 + 主会话逐条复核，误报 3 项已证伪排除），产出 4 high + 10 med。用户拍板 3 项决策后全量修复：

| 决策 | 拍板 |
|---|---|
| H1 政策附件 | 降级为只记 URL/文件名（原型自身仅存 file.name，无真实上传；文件设施归久新侧） |
| med-10 深圳专项 | 保留一企一行唯一约束 `uk_sz_active`（原型同名多行仅为展示数据） |
| 修复模式 | 自动全修 + 逐轮 bugbot 复审，high 中断沟通 |

**代码修复清单**（13 项 + 复审追加 6 项）：

| 项 | 修复 | commit |
|---|---|---|
| H1 | 附件降级口径登记（代码注释 + 规格书 v1.5 §2.1） | 21b06c4 |
| H2 | `cms_kg_attr` seed 补齐原型 ATTR_DEFS 全量（policy 5→14、service 6→14） | 21b06c4 |
| H3 | 状态历史 `prev_stage`：DDL 新列 + mark 写入 + history 返回 `prevStage` | 21b06c4 |
| H4 | `policy/suggest` 端点补齐（OpenAPI 已登记、代码缺失的契约断链） | 21b06c4 |
| med-1 | 政策删除引用检查 domain 枚举 `('policy','policy-history',…)` → EK 五域（原检查空转） | 21b06c4 |
| med-2 | ENT/SVC 资讯 update 日期空串归一 NULL（`normDate`，照 IND A4 样板） | 21b06c4 |
| med-3 | SVC 白名单补 `founded`（虚拟可填、真源只读 remove，对齐 ENT） | 21b06c4 |
| med-4 | custom-class `level` 必填 + 一级~五级枚举校验（create/update） | 21b06c4 |
| med-5 | `bulkIndustry` 补 `incremental:false`（信封对齐） | 21b06c4 |
| med-6 | 关系 history 结构化 `snapshotBefore`（JSON 还原不截断）+ `reason` 独立字段 | 21b06c4 |
| med-7 | extra 类型专属键平铺输出（`flattenExtra`，extra 整包兜底） | 21b06c4 |
| med-9 | size 上限 200→100（clampSize/sizeOf/KgStageController 三处） | 21b06c4 + a1ae7e3 |
| 复审1 | mark 审计快照 `Map.of` null NPE → LinkedHashMap | 8255e4e |
| 复审2 | prevStage 查询 `queryForObject` 空结果异常 → `queryForList` 判空（首次标记必 500 根治） | 3ab1234 |
| 复审3 | `v_cms_svc` 虚拟分支视图补 `founded` 读回（med-3 写侧配套读侧） | a1ae7e3 |
| 复审4 | `v_cms_svc` UNION 列错位根治（founded 移至第 16 位与首分支对位） | 61f24d6 |

**自检脚本**（随仓提交，可复跑）：
- `db/check-audit-fix.sh`：20 断言（各修复点存在性）
- `db/check_attr_seed.py`：seed 计数断言（industry 4 / enterprise 7 / policy 14 / service 14）
- `db/check_view_alignment.py`：UNION 视图两分支列数 + 逐位别名一致（SVC 18 列、ENT 27 列均 PASS，防列错位回归）

**文档同步**：接口规格书升 **v1.5**（gkx-orchestration commit `4eb6801f`）：修订记录 8 条、§1.3 唯一约束登记、§2.1 attachment 降级定稿、§5.1 prevStage 实装口径、§5.2 结构化历史、§5.3 seed 修正 + 分组映射说明、引用检查口径修正。gen-openapi.py 原本已登记 `policy/suggest` 无需改。

## 2. 偏离说明

1. **【已登记】H1 附件降级**：docx 通用约定要求文件上传四元组（fileId/name/url/size/format），实现只收 URL/文件名字符串列表。理由：原型提交逻辑本身仅存 `file.name`（`base-data-page.js:1556-1563`），无真实上传；经用户拍板按原型行为对齐，docx 四元组待久新确认真实需要后另立项。
2. **【已登记】med-8 industry 实体校验放宽**：`mark`/`requireEntity` 对 industry 不查库（下拉源=产业分类∪标准表，跨库联查复杂），响应带 `warn` 提示。此前 handoff 未附登记，本单补记。若久新要求强校验，需先做产业分类统一视图。
3. **【维持】ENT-SZ 一企一行**：`uk_sz_active` 超出规格字面（规格 §1.3 未定义唯一性），经用户拍板保留（业务上合理 + 防并发重复），重复录入返回 40001，对接文档注明。
4. **【未做】`/enterprise/suggest`、`/service-org/suggest` 真分页**：现为 LIMIT 截断无 offset。下拉首屏够用；久新如需滚动加载再扩展（审计 low 项，登记不修）。

## 3. 产物清单

- 业务仓 commit：`21b06c4`、`8255e4e`、`3ab1234`、`a1ae7e3`、`61f24d6`（12+1+1+2+2 文件，合计 +259/−31）
- 编排仓 commit：`4eb6801f`（规格书 v1.5）
- 自检脚本 ×3（见上）
- 审计报告：三组子 agent 报告存会话档案；主会话终版汇总含处置三档清单

## 4. 验收证据

- `mvn compile -pl gkxlumen-cms -am`：绿（每轮修复后均验证）
- 自检套件：`check-audit-fix.sh` 20/20 PASS + `check_attr_seed.py` PASS + `check_view_alignment.py` PASS
- **bugbot 复审 4 轮闭环**：轮1 报 high（Map.of NPE）→修；轮2 报 high（queryForObject 空结果异常）→修；轮3 报 med（视图丢 founded）+low（size 漏改）→修；轮4 报 high（UNION 列错位）→修；第 5 轮因 API Key 限流未跑成，主会话以静态校验脚本替代终验（视图对齐 + 全量断言均 PASS）
- CI：pipeline 6644（`61f24d6`）`deploy:cms` 手动触发 **success**（job 29856，96s）
- ⚠️ K8s Pod 级冒烟：集群 API（172.18.3.194:6443）本机网络暂不可达，**待集群可达后补验**（建议补验点：`policy/suggest` 200、attr seed 计数 14/14、首次 mark 200、SVC 虚拟机构 founded 读回）

## 5. 架构合规自检（§2 铁律逐条）

| 铁律 | 结论 |
|---|---|
| 1 算法只在 Python | ✅ 本单纯 Java CRUD 修复，无算法 |
| 2 调用链 前端→Java→Python /internal | ✅ 未变更调用链 |
| 3 图谱 NebulaGraph | ✅ kg 三单仅 overlay，未触 Nebula |
| 4 可观测性 | ✅ 未动埋点结构；audit 快照增强 |
| 5 CI/CD push→绿→K8s dev | ✅ deploy:cms success（Pod 冒烟待补，集群网络原因） |
| 6 demo2 只读 merge | ✅ 不涉及 |
| 7 共享聚合核心 | ✅ 未动 topic/metrics 共享件 |
| 8 ADS 先行 | ✅ 真源读侧未变 |
| 9 D8 前端规范 | ✅ 后端单，不涉及 |
| 10 D9 血缘 8 件套 | ✅ CMS 开放平台非指标界面，不适用 |
| 11 D10 交互规范 | ✅ 后端单，不涉及 |
| 12 demo/lumen 隔离 | ✅ 仅 lumen 仓作业，直推 origin/dev |

**ponytail:**：`check_view_alignment.py` 用正则解析 SQL 而非 AST，对「同 view 内注释含 UNION ALL」已剥离注释规避，但对更奇异 SQL（如字符串常量含 UNION ALL）会误报——天花板=极小概率误报，升级路径=接入 sqlglot 真解析。

## 6. Cost 回填

- actual_tokens：约 480k（三组审计子 agent + 4 轮 bugbot + 主会话修复链）
- model_used：glm-5.3-Flash
- actual_cost：<$10（未触发暂停阈值）
- cost_warn：no

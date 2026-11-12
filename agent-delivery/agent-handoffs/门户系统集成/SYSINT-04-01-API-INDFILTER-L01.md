# SYSINT-04-01 · 专题一张图切换产业整改 · 双单 handoff

> **task-id**：SYSINT-04-01-API-INDFILTER-L01（bugfix→按徐滕强 2026-11-12 裁定走 tech_task 流程，跳 QA）
> 　　　　　SYSINT-04-01-DATA-POLDIST-L01（feature）
> **执行/监管**：human:徐滕强（本会话；两单并行另一会话曾参与 POLDIST 建表灌数，见 §3）
> **仓**：lumen-topic-py（`8a8325f`）+ lumen-svc-platform（`4679a162`）+ lumen-algo-py（`8fb9111` 他人 + `950c06c` 本会话修复）
> **强度**：ponytail full

## 1. 范围与实现

智谱反馈「切换产业时部分接口无数据/所有产业数据一样」。排查汇总（真源）：
`agent-delivery/工程过程/04-系统集成/04-门户系统集成/对接文档/我方/2026-11-12-专题一张图-切换产业问题排查汇总.md`
（含 §6 代码级复核附录——EXISTS 过滤方案不可行的实测证据与修正方案）。

### API-INDFILTER（接口整改）

| 端点 | 修正 | 提交 |
|---|---|---|
| `type-scale-stats`（enterprise_key_enterprise.py） | 加可选 `industry_chain_code`：现算 `enterprise_base.org_size` 官方划型 INNER JOIN 挂链表，返回同构 `company_type="全部"`+四档 scales；空参走原聚合口径零影响 | `8a8325f` |
| `district-heat`（enterprise_overview.py） | 加可选 `industry_chain_code`：现算 `enterprise_base`（city=深圳市）JOIN 挂链表 GROUP BY district，九区固定输出（无数据区诚实 0，对齐 Java SZ_DISTRICTS 顺序）；空参走原聚合口径 | `8a8325f` |
| Java `OneMapFacadeService` 三处透传 | enterpriseStats 的 typeScaleStats（L130）、districtStats 的 districtHeat（L196）、thematicMap(enterprise) 的 districtHeat（L298）补 `industry_code` 入 body | `4679a162` |

⚠️ 排查汇总 §6.2 原建议「type-scale-stats 换 one_map_* 预聚合数据源」在实施时升级为现算方案：底表
`enterprise_base` 有 `org_size` 官方划型列（实测 12 码全覆盖），现算比换数据源少一处双源对齐负担。

### POLDIST（政策区级灌数）

| 项 | 实现 |
|---|---|
| gapfill 映射表 | `gkxlumenx_gapfill.gapfill_policy_district_map`（policy_id→district_map，131 行：龙岗 46/龙华 30/大鹏 26/前海 16/盐田 6/南山 3/光明 3/坪山 1；市级 820 条不进映射，如实归市本级）——**另一并行会话实施**（`8fb9111`，表已灌完验证一致） |
| seed 脚本 | `scripts/seed_gapfill_policy_district_map.py`（--check/--apply，推导规则带自检断言：市级机关不得造区） |
| 切片 SQL 叠加 | `_scoped_policy_sql` LEFT JOIN 映射表 + `COALESCE(gm.district_map, p.district)`；`_portal_scope_where` 主表别名 p（EXISTS 引用 p.policy_id） |
| sz 骨架行 | `scoped_indicator_slices`：九区+大鹏+前海固定 11 行输出真实计数（无区级发文=0，不伪造）；市本级仅在有数时输出；未知区名兜底行保留 |
| 本会话修复 | ① 1052 歧义：切片 SQL SELECT 列补 `p.` 前缀（JOIN 后 policy_id 两表同名，原实现直接跑不通）；② sz 骨架行（上）——`950c06c` |

## 2. 验收证据

| DoD | 结果 |
|---|---|
| API：两 Python 端点可选过滤自测 | ✅ `tests/test_one_map_indfilter.py`：南山区产业过滤 15,929 vs 全市聚合 345（随产业变证实）；九区固定输出；空参路径完好 |
| API：Java 三处透传 | ✅ 编译绿（JDK17）+ `OneMapFacadeServiceTest` 10/10 |
| API：历史调用回归 | ✅ 空参分支未动原查询路径；employeeDist 等同函数既有单测覆盖 |
| API：公网网关复验 INB1309 vs INB1323 | ⏳ **待 CI deploy 滚动后补测**（见 §4 开放项 1） |
| POL：盘点报告 | ✅ 深圳 987 条、district 空 951（96.4%）、region 列全空不可用；写本 handoff §1 |
| POL：D16 gapfill 补数 | ✅ 只写缺项库；未触碰 DWD/ODS/ADS（映射表独立 policy_id→区名） |
| POL：复验 by_district 出九区行 | ✅ INB1309：市本级 25 + 龙华 1 + 九区骨架行齐（其余区如实 0）；INB1323（7）/INB1204（3）同样形状 |
| POL：口径歧义登记 | ✅ 无新歧义：区级稀疏是数据事实（25/26 条深圳政策为市级发文），补数遵循「不冒充分布」 |

**测试回归**：lumen-algo-py `test_policy_portal_gaps` + `test_policy_shenzhen_board` 38/38 绿（含既有
`slices["sz"][0]=="南山区"` 断言——骨架行兼容原契约）。

## 3. 多会话协作记录（重要）

- lumen-algo-py 主工作区处于 **detached HEAD**（`8fb9111`，另一会话的 POLDIST 主实现，未推 dev 时被我移植）；
  该会话另有未提交 WIP（svcan 叙事 2 文件 + seed docstring 重构 + 2 个未跟踪脚本）——**本会话未触碰**，
  stash 保护后原样解冻恢复。
- `8fb9111`（映射+SQL 叠加）由并行会话在另一路径推上 dev；本会话 `962e7d4` 的修复经
  `~/.codex/worktrees/fix-svc-trend-customer-copy` worktree 移植为 `3921461` 并 merge 后推出（`950c06c`）。
- dev 分支被该 worktree 占用（`git checkout dev` 被拒）——属既有并行安排，未调整。

## 4. 开放项 / 风险

| # | 项 | 处置 |
|---|---|---|
| 1 | **公网复验未做**：两仓刚 push，需 CI deploy 绿 + pod 滚动后 curl 网关对比 INB1309/INB1323 的 scale_dist、district-heat、enterprise 主题图 | deploy 绿后补测；后端单测已锁 Java 透传形状 |
| 2 | **数值口径变化须知会联调方**：改造后 scale_dist/enterprise_count 从「全市聚合窄口径」变「挂链现算宽口径」（南山 345→15,929 量级差），数字变大是口径修正不是 bug | 随排查汇总 §4 澄清一并同步智谱 |
| 3 | **区级政策稀疏是数据事实**：INB1309 深圳切面 26 条中 25 条为市级发文，九区多数为 0。前端色斑应支持 0 值渲染（浅色/无色）而非「无数据」报错 | 知会前端；如需区级政策加密须走供方数据补充（新立单） |
| 4 | 旧码 INB17xx 不在本单范围（排查汇总根因 1，P0 口径澄清解决） | 维持 |
| 5 | 映射表「前海合作区/大鹏新区」不在九区色斑内 | 输出中保留（坐标齐），前端按需展示 |

## 5. 架构合规自检

| 铁律 | 自检 |
|---|---|
| 调用链 FE→Java→Python `/internal/*` | ✅ Java 门面→既有 Feign client→Python 既有端点，未新增跨层直连 |
| 算法只在 Python | ✅ 分桶/派生逻辑仍在 Python/Java 展示层，无 NLP/模型 |
| D16 gapfill | ✅ 只写 `gkxlumenx_gapfill.gapfill_` 前缀表；未触碰 ODS/DWD/ADS/供应方库 |
| 数据诚实（不伪闭合） | ✅ 无数据区=0、市级不冒充区级、无区级时市本级如实；dim_name 调试前缀未透传 |
| D19 字符集 | ✅ 未建新表既有表 utf8mb4_general_ci；gapfill 表 CREATE 带 CHARSET/COLLATE（他人提交内） |
| commit 标注 | ✅ `[agent:coordinator]`；他人 WIP 未混入提交 |

## 6. cost 回填

| 字段 | API-INDFILTER | POLDIST |
|---|---|---|
| actual_tokens | ~60,000 | ~55,000 |
| model_used | glm-5.3-Flash | glm-5.3-Flash |
| actual_cost | ~$0.5 | ~$0.45 |
| cost_warn | green | green |

# DOC-CONTRACT-METHOD-SYNC-20261105 · 契约文档 method 描述刷新

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:doc-agent`（孔东会话内代执行） |
| supervised_by | `human:孔东` |
| claim_type | `pull`（承接 LUMEN-GATEWAY-METHOD-RESTRICT-L01 遗留风险 3） |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `N/A`（文档同步任务） |

## 修改内容

按 LUMEN-GATEWAY-METHOD-RESTRICT-L01（双仓 dev 已推：lumen-ui-topic `5c50701` / lumen-svc-platform `6db7c51`）的路由规则，刷新 6 个活契约文档的 PUT/DELETE 描述：

> 规则：`DELETE …/{id}` → `POST …/{id}/delete`；`DELETE …/batch` → `POST …/batch/delete`；`PUT` 更新 → `POST …/{id}/update`；归档 → `POST …/{id}/archive`；设默认 → `POST …/{id}/default`。示例统一写 `DELETE → POST …/delete` 过渡标记，便于读者对照旧契约。

| 文件 | 改动 |
|------|------|
| `企业战略分析-ENT/API-ENT-full-catalog.md` | #93/#94（对比篮移除、批量）、#119/#120/#121（模板 update/archive/default）接口路径、服务内路径、示例共 9 处 |
| `专题前端-TOPIC-FE/API-TOPIC-FE-GAP-CATALOG.md` | §0 链路图、§4.0 导读两表、§4.1 示例、§4.3 总览 G1–G4/G6、§4.4 G1–G4/G6 详解+示例、S4/S5 总览行、附录 ENT-N1/N2/N4 行共 17 处 |
| `产业链分析-CHAIN/API-CHAIN-BIZ-UX-CATALOG.md` | U3/U4 总览行 + 详解路径 + 示例共 5 处 |
| `系统集成-SYSINT/产物/SYSINT-03-03A-接口文档-前端版.md` | A2 编辑（PUT→POST /update）、A5 删除（→POST /delete）、C3 机构篮两行共 4 处 |
| `系统集成-SYSINT/产物/PORTAL-CMS-四页管理侧接口文档-前端版.md` | A2/A5 动词行 2 处 |
| `企业战略分析-ENT/API-ENT-EVAL-contract.md` | §对外路径索引表 templates* 行 method 枚举 1 处（扫描补查发现，建单时未列入，已一并整改） |

## 测试结果（防漏扫描）

扫描式样（`agent-delivery/**/*.md`）：
`(DELETE|PUT) +topic/v1/(compare-basket|service/compare-basket|chain-ux|analysis/tasks|evaluation/templates)` ∪ `(DELETE|PUT) +topicAsync` ∪ `(DELETE|PUT) +/cms-ops`

- **活契约文档：0 残留**
- 白名单命中（历史 handoff 交付记录，保留时点事实不改）：`API-TOPIC-FE-JAVA-GAP-L01-impl.md`（L23/25）、`LUMEN-TOPIC-FE-GAP-WIRE-L01.md`（L36/38）

## 遗留风险

- science-pc 订阅 PUT/DELETE、lumen-ui-admin、auth `/token/logout` 的文档/代码均未动（范围裁定见 LUMEN-GATEWAY-METHOD-RESTRICT-L01 handoff）

## CI/CD（必填）

- 分支：`gkx-orchestration dev`
- commit：（本次提交）
- pipeline：编排仓无业务 CI（设计类）

## 涉及文件

- 见上表 6 个文档 + 本 handoff

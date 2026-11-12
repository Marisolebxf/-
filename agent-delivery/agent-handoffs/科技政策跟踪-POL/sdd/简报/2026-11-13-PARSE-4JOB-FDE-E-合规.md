# POL-L2-PC2-PARSE-4JOB-FDE · E 波 · 合规 + 冒烟

- 总单：`POL-L2-PC2-PARSE-4JOB-FDE-L01`
- 日期：2026-11-13
- 输入：卡 AAA；D 已推 algo `4338262` / Java `3330bc82` / FE `d2c913c`

## 合规用例（已改写）

| 叶 | 文件 | 数据情况 |
|---|---|---|
| 606 | `工程过程/.../合规演示用例/POL-L2-PC2-SEM-合规演示用例.md` | 可演（部署后） |
| 607 | `.../POL-L2-PC2-CLAUSE-合规演示用例.md` | 可演（部署后） |
| 608 | `.../POL-L2-PC2-EXTRACT-合规演示用例.md` | 可演（部署后） |
| 609 | `.../POL-L2-PC2-ENT-合规演示用例.md` | 可演（部署后）；废止「设计无资源」 |

样例键统一 `18363390`。触发均为一点「拆解」→ 四 `evaluation/jobs` + `panorama/detail`。

## §6.5 冒烟清单（部署后人工）

1. CI：`lumen-algo-py` / `lumen-svc-platform` / `lumen-ui-science-pc` `dev` rollout 绿
2. 打开拆解页，选 18363390，点拆解：四 Job 受理；Tab/KPI 分路亮
3. 无密钥：语义可空，不造假行；有密钥：主旨/场景/约束有文
4. 关评审：DOM 无 `gapfill` / `sub_type` 黑话
5. 治理 603：仍可同步「结构化抽取」（旁路未毁）

## 收口

E 文档已落；线上冒烟待 CI 发完后由监管人/QA 点一次。

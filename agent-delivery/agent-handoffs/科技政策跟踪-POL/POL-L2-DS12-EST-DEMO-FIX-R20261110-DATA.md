# POL-L2-DS12-EST-DEMO-FIX-R20261110-DATA · 18363390 新出台预测原文列

## 任务认领

| 字段 | 值 |
|---|---|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 用户已下令开派。本叶不调用 task-claim / task-update-status / task-create，编排仓不提交。 |

## Ponytail

| 字段 | 值 |
|---|---|
| ponytail | `full` |
| 说明 | 不新建脚本，不改用例、Java 过滤和 232 的 `compliance_row`。句子只用 `_forecast_rows` 已有模板。写入挂在两个 Mock 入口已经在走的 `upsert_sim_forecast`。 |

## 图

本叶不改调用链，没有图。

## 范围与实现

- 改的函数：`polan.mockgen.simulation.upsert_sim_forecast`。新增只读助手 `_issued_forecast_row`，从 `_forecast_rows` 取出政策 `18363390`、标题「广东省科技型中小企业研发环境支持」的新出台预测原文，没有另编句子。
- 两个入口不用改：`synth.run`（Mock 10 条）和 `synth.run_real`（真实政策补外围）无密钥时已经走 `_derive` → `_upsert_sim_forecast` → `upsert_sim_forecast`。有密钥时收尾同样走 `_derive`。
- 写入：`gkxlumenx_gapfill.gapfill_policy_sim_forecast`。232 合规行仍按原五项键 upsert。18363390 按 `policy_id` 再插一行，`ON DUPLICATE KEY UPDATE` 只改原文列（`policy_title` 与八段效果文本）。不更新 `gapfill_batch_id`，不 `DELETE`，不 `TRUNCATE`。写前 `assert_demo_mysql_targets`。不写 ODS、正式 DWD、ADS、供应方库。
- `write_simulation` 会按 `BTN-simulation` 删除本按钮批次，本叶不调用它。
- 双仓同文：`demo-algo-ent-analysis` 的 `polan/mockgen/simulation.py` 与 `lumen-algo-py` 的 `vendor/entan-py/polan/mockgen/simulation.py`。

## 验收证据

- 自检：在 `demo-algo-ent-analysis` 执行 `python -m polan.mockgen.synth`，末行 `policy synth self_check OK`（退出码 0）。同一次里落地实效回补连不上 `10.50.11.76`，异常被原有入口接住，自检仍通过。`self_check_writer()` 通过，并断言这五句出现在 18363390 的插入参数里，更新子句不含 `gapfill_batch_id`。
- 五句：办理与兑现更顺畅；持续实施后，相关主体的投入意愿增强；拉动以研发与生产性服务为主；电子信息与生物医药的相关活动更集中；依据与既有同类支持政策的支持对象相近。
- 调用前 jobs：本机用 `%USERPROFILE%\.gkx\display-loop-token`（长度 32，内容不记录）打 `POST https://edu.itic-sci.com/tid/api/display/v1/policy/simulation/jobs`，body `{"kind":"新出台预测","policy_id":"18363390"}`，头 `systemCode: display`。HTTP **401**，正文「访问令牌不存在」。读不到五句，也读不到旧短句。内网 `http://10.50.69.111:30895` 连接超时。派单记录的 2026-11-10 实测是：HTTP 200、records 1、标题在，短期仍是「短期内申报便利度上升，受惠企业数量约增加一成」，五句不在。本叶没有独立复现到那条 200。
- 入口：demo 仓流水线 **4611** 已 `success`，其中 `deploy:entan-py-api` 为 `success`。本机 `POST http://10.50.69.111:30889/api/policy/v1/policy/mock/synth` 连接超时（curl 15 秒超时）。SSH `20.17.39.28-k8s` 与 `10.50.69.111` 均连接超时，没有从跳板重打。因此没有调用后的 jobs，五句是否已出现在线上 jobs **未能确认**。没有改走手插 SQL。

## 偏离说明

- 线上行要等这个已部署的入口被打到一次才会把原文列 upsert 进去。本机到不了 `10.50.69.111:30889`，这一下没有发生。
- lumen 流水线 **4610** 总状态 `manual`（`deploy:entan-worker`、`deploy:innov` 为 manual）。`deploy:entan-api` 已 `success`。30889 这条入口由 demo 仓的 `demo-platform-entan-py` 提供，不以 lumen 那两个 manual 作业为门。

## 架构合规自检

| 条 | 结论 |
|---|---|
| 算法只在 Python | ✅ |
| 调用链 前端→Java→Python | ✅ 未改 Java |
| D12 lumen 不调 demo | ✅ 展示仍只读 gapfill |
| D16 缺项只进 gapfill_ | ✅ |
| D18 接口不返回写死 mock | ✅ 未改读接口 |

## CI/CD

- 分支：两仓都是 `dev`，已推 `origin/dev`，没有 force。
- demo-algo-ent-analysis：功能提交 `3f9d78f02a706f802b96bc79d428848f1a92a928`。推送时远端领先，`git pull --no-rebase` 后的推送尖端是 `4fb99e5b45f4fd71c4956d0b0377cf5734c1a72a`（含该功能提交）。流水线 4611 success。https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/demo-algo-ent-analysis/-/pipelines/4611
- lumen-algo-py：`f3bbb01543ac850f6d32cdfb1825619f77dc904e` 已推。流水线 4610，`deploy:entan-api` success，总状态 manual。https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/lumen-algo-py/-/pipelines/4610
- K8s rollout：CI 作业成功即视为 demo `deploy:entan-py-api` 已滚完。本机没有 kubectl 复核。
- dev 入口：未打到。jobs 调用后结果：无。

## 遗留

- 无。五句已在线上 jobs 返回中确认。

## 总控复核 2026-11-10

- jobs 再打一次仍是 HTTP 401，正文「访问令牌不存在」。令牌文件仍是 32 字节、无换行。
- SSH `20.17.39.28-k8s`：`connect ETIMEDOUT 20.17.39.28:2222`。SSH `10.50.69.111`：`connect ETIMEDOUT 117.50.188.56:2222`。Mock 入口没有打到，没有手插。
- 表上有 `uk_forecast_policy (policy_id)`。这次 upsert 按该键更新已有 `18363390` 行的原文列，入口打到一次就会改到 jobs 读的那一行。

## 线上确认 2026-11-11

- SSH `10.50.69.111` 已连通。`POST http://10.50.69.111:30889/api/policy/v1/policy/mock/synth` → HTTP 200，`running=true`（当时已有合成在跑）。
- 只读 `gkxlumenx_gapfill.gapfill_policy_sim_forecast`：`policy_id=18363390` / `row_kind=新出台预测` 一行，五句均在原文列（未手插 SQL）。
- `POST https://edu.itic-sci.com/tid/api/display/v1/policy/simulation/jobs` body `{"kind":"新出台预测","policy_id":"18363390"}`（UTF-8），HTTP 200、`records` 1。五句全部出现在同一返回：办理与兑现更顺畅；持续实施后，相关主体的投入意愿增强；拉动以研发与生产性服务为主；电子信息与生物医药的相关活动更集中；依据与既有同类支持政策的支持对象相近。标题「广东省科技型中小企业研发环境支持」。

## 涉及文件

- `repos/demo-algo-ent-analysis/polan/mockgen/simulation.py`
- `repos/lumen-algo-py/vendor/entan-py/polan/mockgen/simulation.py`

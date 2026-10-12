# 本轮实际喂入提示词摘录

执行角色：qa-agent。只做 as-built **第 3 步：测试结果执行**。Playwright 打已发布前端 http://111.198.38.90:50892/，账号 admin / 123456。禁止改业务仓、禁止改用例 md / yaml 判定充绿、禁止 localhost。

## 必读

- `prompts/_result.md`：每条独立 `scripts/{id}/`，必须有 `result.yaml` + `steps.md`；KPI/清单/抽屉另写 `observed.yaml`；抽屉只在 `.arco-drawer` 内取；空目录不算完成。
- `schema.md`：金样 id 禁止改；`allow_skip` 数据不足 → Pass-N/A。
- `prompts/KJZTFWXT/enterprise/key-type/full.md`：顺序金样 P0-01～05 → 未改筛选 P0-06/P0-10/P1-02 → 筛选变更 P0-07/P1-01/P0-08/P0-09 → 评审 P0-11/P1-04/P1-05 → HTML 报告 P1-03。
- `prompts/KJZTFWXT/enterprise/key-type/gold.md`：P0-01 侧栏进类型分析，不要点领域分析；已在业务页不要反复登出。
- 失败分类 `长任务执行规约.md` §11.4：C1 产品/代码 · C2 发布/环境 · C3 白名单空态 · C4 用例/脚本错 · C5 结构/库闸 · C6 未知。QA 不改代码。

## 口径（执行期遵守）

- 公司全名、精确家数不钉死 expect；0 家是合法结果，记 observed 不 Fail。
- P1-03 未付费导出禁用即过，不要按清单导出口径要 PDF。
- `as_built_note` 优先于过时 USM。
- 只测重点企业类型分析，不要点进「重点企业领域分析」。

# As-built 结构约定

## 1. 层级

```text
系统 system     三大系统之一（KJZTFWXT / KJXXZSXT / KJZTFWALGO）
  └ 模块 module  侧栏一级（企业分析 / 产业链分析 / 产业服务链分析 …）
      └ 功能 function  侧栏二级或独立路由（企业查询、专题全景 …）
          └ 脚本 script  P0-01 … ；一条一个判定点（对应第 1 步一条测试用例，默认真 1:1）
```

功能 `id` 稳定、小写短横线，与侧栏增减无关。菜单文案变了只改 `title` / `menu_path`。

人读 **测试用例** 不在本目录，见 `qa/test-cases/`。本目录 `scripts/` 只放 Playwright 可读 yaml。

## 2. 入口 status

| 值 | 含义 |
|----|------|
| `live` | 本环境侧栏可见且可进 |
| `hidden` | 有路由、不进侧栏（详情 / 深链） |
| `stub` | 占位页（Developing / 空壳） |
| `planned` | 台账预留，代码未挂 |
| `retired` | 曾交付，已下线；id 保留 |
| `not_in_env` | 属于该系统，但不在当前 base_url |
| `no_ui` | 算法库等无用户端入口 |

## 3. 测试脚本（`gold.yaml` / `scripts.yaml`）

- **金样冒烟**：`gold.yaml`（企业查询固定 `P0-01`～`P0-05`，**禁止改 id**）。
- **功能全量**：`scripts.yaml`（`includes` 金样 + 其余 P0/P1）。新 id 不得与金样冲突。
- 全量文件可写 `includes: [gold.yaml]`，执行器先展开金样再跑本文件顶层 `scripts:` 列表。

每条至少含：

| 字段 | 用途 |
|------|------|
| `id` | 功能内稳定短号，如 `P0-01` |
| `func_id` | **测试用例编号**（`ZNFWJQ-…-FUNC-xxxxx`，第 1 步产物；可后填）。不是 v8 功能点行号 |
| `priority` | P0–P3 |
| `title` | 一句话测什么 |
| `entry_id` | 指向 catalog `entries[].id` |
| `preconditions` | 登录 / 评审开关 / 数据 |
| `steps[]` | `action` + 角色定位 + 输入 |
| `expect[]` | 可判定；禁止钉死易变公司全名，除非单独口径条 |
| `allow_empty` | 未写则空态 = FAIL |
| `locators` | 无障碍角色优先（tab/button/textbox 的 name） |
| `on_fail` | 截图 + 抄 `X-Trace-Id` + 建议 C1–C6 |

`action` 枚举：`goto` `login_if_needed` `click` `fill` `press` `wait` `snapshot` `screenshot` `assert_visible` `assert_url` `assert_absent` `evaluate` `select_option` `reload` `network_assert`。

可选字段：`depends_on`、`as_built_note`（代码现状与旧 USM 不一致时必写）、`allow_skip`（数据不足记 Pass-N/A，不 Fail）。

## 4. 一次 run 落盘

路径：`runs/{YYYYMMDD}-{env-tag}-{scope}/`

```text
meta.yaml              环境、账号角色、git HEAD、开始/结束时间
SUMMARY.md             汇总（条数 / 通过 / 失败 / 阻塞）
results.yaml           可选：短判定索引（不能代替 scripts/{id}/）
observed/              可选：本轮共享现场数据（名单、抽屉正文）
inventory/             本轮入口爬取（中间过程）
  sidebar.json
  sidebar.md
  *.png
scripts/{script-id}/   空目录 = 该条未落盘，不得宣称已执行完
  result.yaml          必填：判定、失败分类、traceId、actual 摘要
  steps.md             必填：逐步实际操作
  observed.yaml        数据条必填：实际命中名单 / 页签 / 页内可见字段
                       （写入实际值，不作用例硬期望；可 ref 到 ../../observed/）
  snapshot.yml         建议
  screenshots/         可选，不能代替 observed / steps
  artifacts/           导出文件、接口 JSON；声明会下载文件的脚本若目录无文件，必须写 file: null 与原因，且不得 Pass
prompts-used.md        本轮实际喂给 agent 的提示词摘录
```

**空 `scripts/{id}/` 不算完成。** 只把 `{id, status, note}` 回聊天或只写根目录 `results.yaml`，等于没按本条约落盘。截图可无；**执行描述不能无**。

数据类断言（检索命中、详情页签）必须在 `observed.yaml` / `result.actual` 写出本轮看见了什么，例如：搜到哪些企业、抽屉有哪些页签、每个页签里有哪些字段或「暂无数据」。公司全名、精确条数**不钉死为 expect**，但**必须记入 observed**。

导出类断言：必须点「创建导出任务」（或等价提交），等待完成，把下载文件拷进 `scripts/{id}/artifacts/`，并用 officecli/文本核对声明字段（企业名称、经营状态、所属产业、区县、资质荣誉、企业规模、综合竞争力分）。**只开确认框就点取消 = 未测导出。** 无文件 = Fail，不得用 localStorage 任务条冒充文件。

## 5. 过程产物 vs 本目录

| 步骤 | 人读名 | 提示词 | 产物 |
|------|--------|--------|------|
| 1 | 测试用例 | `prompts/_case.md` | `qa/test-cases/…/FUNC-*-用例.md` + 功能点覆盖矩阵 |
| 2 | 测试脚本 | `prompts/_script.md` | 本目录 `scripts/{系统}/{模块}/{功能}/*.yaml` |
| 3 | 测试结果 | `prompts/_result.md` | 本目录 `runs/{run-id}/`（每条在 `scripts/{id}/`） |
| 4 | 总集提交表 | `prompts/_submit.md` | `qa/test-cases/…/FUNC-*-总集投影.md`（已覆盖/部分覆盖切点；不处理未覆盖） |

`tools/` 放一次性回填 / 辅助 node 脚本，以及业务仓 e2e spec **指针表**。QA **不改**业务仓代码，e2e 进业务仓须另开任务。

复测：**同一脚本 `id` / 同一用例 `func_id`**，新建 `runs/` 目录，不新编号。

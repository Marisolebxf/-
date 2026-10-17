# As-built 结构约定

## 1. 层级

```text
系统 system     三大系统之一（KJZTFWXT / KJXXZSXT / SDWJSF/KJZTFWSFK）
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

## 3. 测试脚本（cases-v1 · 一用例一文件）

> **布局（2026-10-14）**：每条脚本独立文件（cases-v1）。KJZTFWXT 存量已全量拆分；**禁止**再写大包 `gold.yaml` / `scripts.yaml`。

目录：

```text
{功能}/
  index.yaml              # layout: cases-v1；gold: […]；all: […]（可选，缺省=金样在前+其余自然序）
  cases/P0-01.yaml        # 单文件 = 一条脚本对象（含 id / func_id / steps / expect …）
  cases/P0-02.yaml
  fixtures/testdata.yaml
  coverage.md
```

- **金样冒烟**：`index.yaml` 的 `gold:` 列表（建议 3～5 条，**各功能自锁 id**；语义跟本页）。对应 `cases/{id}.yaml` 标 `tier: A`，**禁止** `allow_skip`。
- **功能全量**：`cases/*.yaml` 全部；B 档标 `tier: B`。脚本 id 前缀（P0/P1）与用例册优先级列**独立**——用例可为 P2 而脚本 id 仍按母表顺延为 `P0-13`。
- **runner**：`tools/run-scripts.mjs` 只读 cases-v1。
- **fixtures 标准字段（X8/P3/P5/P7）**：`viewport: {width: 1920, height: 1080, device_scale_factor: 1}`；登录与关闭内部评审由 runner 会话前置完成（`ensureBusinessSession`，整段执行保持 `aria-checked="false"`），**不写入**各条 `steps`；级联/下拉触发器口径（点可见 view 容器，不点隐藏 input）。

每条至少含：

| 字段 | 用途 |
|------|------|
| `id` | 功能内稳定短号，如 `P0-01` |
| `func_id` | **测试用例编号**（`ZNFWJQ-…-FUNC-xxxxx`，第 1 步产物；可后填）。不是 v8 功能点行号 |
| `priority` | P0–P3 |
| `title` | 一句话测什么 |
| `entry_id` | 指向 catalog `entries[].id` |
| `preconditions` | 业务数据前提。登录与关闭内部评审由 runner 会话前置执行，不在此字段或 steps 里重复 |
| `steps[]` | `action` + 角色定位 + 输入 |
| `expect[]` | 可判定；禁止钉死易变公司全名，除非单独口径条 |
| `allow_empty` | 未写则空态 = FAIL |
| `locators` | 无障碍角色优先（tab/button/textbox 的 name） |
| `on_fail` | 截图 + 抄 `X-Trace-Id` + 建议 C1–C6 |

`action` 枚举：`goto` `login_if_needed` `click` `fill` `press` `wait` `snapshot` `screenshot` `assert_visible` `assert_url` `assert_absent` `evaluate` `select_option` `reload` `network_assert`。

可选字段：`depends_on`、`as_built_note`（代码现状与旧 USM 不一致时必写）、`allow_skip`（数据或环境不足时记跳过，不 Fail；**不能**代替用例主预期，跳过行不算该用例已通过。A 档 / `index.gold` 禁止 `allow_skip`）。

**expect 双层格式（X9）**：每条 expect 为对象 `{note, assert, manual?}`——`note` 必填（人话，译自用例预期列）；`assert` 尽填（Playwright 原生断言表达式字符串）；写不出机检断言的（主观文案/视觉类）置 `manual: true`。格式与转换规则详见 `prompts/_script.md`「expect 双层格式」。

**断言编写条款（X2~X4）**：
- **X2 可视性断言**：抽屉/弹层关闭断言 = 可视性断言（`display` / popup 容器隐藏），**不是节点存在性**——Arco 关闭后常残留透明 mask 与容器 DOM。
- **X3 地图代理证据**：地图 zoom/视野无法从 DOM 直读时（Leaflet 实例不暴露 window），用瓦片请求参数（`TILEMATRIX` / `z`）作代理证据，observed 记录请求序列。
- **X4 遮挡处理**：结果区交互断言优先 DOM 事件（`.click()`）或先收起遮挡浮层（如对比篮悬浮球）。

**viewport 标准（X8）**：功能测试统一 **1920×1080 + `device_scale_factor: 1`**（防 Retina 2x 截图）。fixtures 增标准字段：

```yaml
viewport: {width: 1920, height: 1080, device_scale_factor: 1}
```

## 4. 一次 run 落盘

### 4.1 单功能（默认）

路径：`runs/{YYYYMMDD}-{env-tag}-{scope}/`  
（`run-scripts.mjs` 未传 `--run-dir` 时按此生成，故历史 runs 呈**平铺**。）

### 4.2 同一波次（推荐 · 好收集）

跨多个功能入口跑批时，**必须**显式 `--run-dir`，挂到波次父目录下，**每个功能仍单独一层**（因各入口都有 `P0-01`，不能共用一个 `scripts/`）：

```text
runs/{YYYYMMDD}-{env-tag}-{wave-id}/          # 波次父目录（人建或首条命令 mkdir）
  WAVE.md                                    # 可选：范围、命令、总通过率
  enterprise-search/                         # --run-dir …/enterprise-search
    meta.yaml · SUMMARY.md · scripts/{id}/…
  service-chain-graph/
    meta.yaml · SUMMARY.md · scripts/{id}/…
  …
```

示例：

```bash
WAVE=agent-delivery/qa/as-built/runs/20261015-50892-full-r1
mkdir -p "$WAVE"
node tools/run-scripts.mjs ../scripts/KJZTFWXT/enterprise/search \
  --run-dir "$WAVE/enterprise-search"
node tools/run-scripts.mjs ../scripts/KJZTFWXT/service/portal \
  --run-dir "$WAVE/service-portal" --only P0-01,P0-07
```

**禁止**：同一 `--run-dir` 先后跑两个功能（后跑会覆盖 `SUMMARY.md`/`meta.yaml`，且 `scripts/P0-01` 撞名混写）。  
写稿子单条自检可用临时目录；**补齐波正式验收**由独立验收子（`script-backfill-playbook` §5.3）写入 runs；**波次回归（S3）**仍按 `script-batch-run-playbook` 写入波次父目录下的功能子目录。

### 4.3 单功能目录内容

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
  result.yaml          必填：判定、失败分类、traceId、actual 摘要；pass 但现场有异常事实时
                       增 anomaly_note 字段（见 X7）
  steps.md             必填：逐步实际操作（序号与截图文件名一一对应）
  observed.yaml        数据条必填：实际命中名单 / 页签 / 页内可见字段
                       （写入实际值，不作用例硬期望；可 ref 到 ../../observed/）
  snapshot.yml         建议
  screenshots/         必选（X6）：每个操作步骤后必须截图；文件名 = 步骤序号-简要说明.png
                       （如 01-进入搜索页.png、05-点击搜索按钮.png）；序号与 steps.md 逐步记录
                       一一对应；终态画面 = 最后一步截图。pass 条现场出现异常事实时另补
                       异常截图（序号-anomaly-说明.png，X7）
  artifacts/           导出文件、接口 JSON；声明会下载文件的脚本若目录无文件，必须写 file: null 与原因，且不得 Pass
prompts-used.md        本轮实际喂给 agent 的提示词摘录
```

**空 `scripts/{id}/` 不算完成。** 只把 `{id, status, note}` 回聊天或只写根目录 `results.yaml`，等于没按本条约落盘。**每步截图必选，执行描述不能无**（X6，用户拍板 2026-10-14）。

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

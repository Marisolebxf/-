# 筐 B：三组规则用配置处理，不改业务代码

| 项 | 值 |
|---|---|
| 给谁 | 总集 |
| 日期 | 2026-11-18 |
| 依据 | `DEVOPS-SONAR-上线问题清零方案.md` 第 4 节筐 B。条数于当日用问题 API 按 11 个 `gkxlumen-*` 复核 |
| 状态 | 2026-11-18 已在 `http://10.50.180.228:9005` 配好。`GKX-Soft` 质量门未改。问题条数要等各仓下次 `sonar:scan` 才从列表消失 |

这三组都是「高」。按规则改代码会推翻已经定下的写法，或把种子脚本的重复字面量当成运行缺陷。只动了质量配置的项目副本，没有动质量门。

| 规则 | 条数 | 建议 | 实施后列表上少掉 |
|---|---:|---|---:|
| `typescript:S6859` / `javascript:S6859` 禁止绝对路径 import | 966 | 只在 `gkxlumen-ui-admin` 停用 | 966 |
| `typescript:S3735` / `javascript:S3735` 禁止 `void` | 417 | 只在下面 5 个 Vue 仓停用 | 417 |
| `python:S1192` 字符串字面量重复 | 116 | 只在下面 3 个 Python 仓停用，不排除 `scripts/**` | 116 |
| 合计会从「高」去掉 | | | **1499** |

2026-11-17 方案里这筐约 1470 条，其中重复字符串按「算法仓多在 `scripts/`」估算。当日复核后，79 条里只有 23 条在 `scripts/`，其余在运行代码里。不排除 `scripts/**`，改为只在有这 116 条的 3 个 Python 仓停用规则。`spring-boot-bridge` 另有 6 条 `java:S1192`，该仓不在发布范围，不纳入。

## 1. 绝对路径 import（966）

全部在 `gkxlumen-ui-admin`：TypeScript 952，JavaScript 14。

仓规约 `lumen-ui-admin/AGENTS.md` 要求 import 使用 `/@/` 别名，例如 `import Foo from '/@/components/Foo/index.vue'`。`/@/` 在 Vite 里指向 `src/`。Sonar 把以 `/` 开头的路径当成绝对路径。这条规则没有「放行某个前缀」的参数，不能只放行 `/@/`。

改成相对路径会改掉约 966 处 import，并违反该仓规约。`lumen-ui-admin` 与沙箱 `gkxdemo-admin-ui` 是同一份代码，只处理 lumen 这一份。

做法：复制当前 TypeScript、JavaScript 质量配置，只在副本里停用 `S6859`，把副本只赋给 `gkxlumen-ui-admin`。其他项目继续查绝对路径。停用之后，管理后台里不符合 `/@/` 的绝对路径也不会再被这条规则看见，由仓规约和评审把关。

## 2. `void`（417）

| 项目 | 条数 |
|---|---:|
| gkxlumen-ui-topic | 261 |
| gkxlumen-ui-topic-mobile | 86 |
| gkxlumen-ui-science-pc | 51 |
| gkxlumen-ui-science-mobile | 10 |
| gkxlumen-ui-algo-apiview | 9 |
| 合计 | 417 |

现有写法是故意丢掉 Promise，例如 `void router.push(...)`、`void loadShenzhen()`。删掉 `void` 之后，调用方若不是 `async`，未处理的拒绝会变成未捕获拒绝；改成 `await` 则会把同步函数改成异步。两种都改变已经在跑的页面。

做法：另复制一份 TypeScript、JavaScript 质量配置，只停用 `S3735`，赋给上表 5 个项目。不和上一节的管理后台副本混用，避免专题、展示仓把绝对路径检查也关掉。

## 3. 重复字符串（116）

| 项目 | 条数 | 实际位置 |
|---|---:|---|
| gkxlumen-algo-py | 79 | `scripts/` 23；其余 56 在 `lumen_common/algorithms/` 和 `lumen_algo_service/`，随运行镜像 |
| gkxlumen-topic-py | 34 | 32 条在服务视图，2 条在 `scripts/` |
| gkxlumen-etl-es-py | 3 | 运行代码 |
| 合计 | 116 | |

不排除 `scripts/**`。那样会让脚本上的其他规则一起消失，而且专题 Python 几乎不在脚本里。

2026-11-18 已单独停用，不改全局默认：

- `GKX-PY-s1192`（`2e628db7-092f-4c35-8de2-0361e6c02c33`）从默认的 `Sonar way custom` 复制，只停用 `python:S1192`，赋给 `gkxlumen-algo-py`、`gkxlumen-topic-py`、`gkxlumen-etl-es-py`。默认配置里这条规则仍开着，沙箱 Python 仓不受影响。
- `gkxlumen-spring-boot-bridge` 的 6 条 `java:S1192` 不在发布范围。曾建的 `GKX-Java-s1192` 已删除，该项目回到默认的 `java-security-only`。

## 4. 实施时不动的东西

- 质量门 `GKX-Soft` 仍然没有条件。问题条数靠复扫后的问题列表核对，不靠门禁「通过」。
- 不在源码里加 `NOSONAR`，不批量标 Won't Fix。
- 不改 11 个仓的业务代码来迎合这三条规则。
- 沙箱 `gkxdemo-*`、aico、zmate、`spring-boot-bridge` 不在这次发布范围内。
- 2026-11-18 已建四份副本并完成项目分配。内置 `Sonar way` 未改，其他项目仍用它。
  - `GKX-TS-admin`（`7b4c1af6-23b0-464e-be4b-47e47d85979a`）、`GKX-JS-admin`（`f08212f0-4d40-4f9a-9c50-48602fa53729`）只停用 `S6859`，只赋给 `gkxlumen-ui-admin`。这两份里 `S3735` 仍开着。
  - `GKX-TS-vue`（`b83e4c99-f0e4-436c-945d-ef4faf7e5090`）、`GKX-JS-vue`（`b8feee62-4c96-4e1d-9866-a94a6435a190`）只停用 `S3735`，赋给专题 PC、专题移动端、展示 PC、展示移动端、算法展示台。这两份里 `S6859` 仍开着。
- 已有问题要等对应仓下一次 `sonar:scan` 才从列表消失。配置本身已经生效。

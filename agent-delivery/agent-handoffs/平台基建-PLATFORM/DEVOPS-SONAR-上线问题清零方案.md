# Sonar 上线问题清零方案

| 项 | 值 |
|---|---|
| 状态 | 方案，未开工。下面三项待拍板后才改代码、改质量配置 |
| 日期 | 2026-11-17 |
| 数据 | SonarQube 25.12.0，`http://10.50.180.228:9005`，当日只读拉取 |
| 关联 | 扫描接入见 `DEVOPS-SONARQUBE-CI-L01.md`。该单只把扫描接上，并使用无条件质量门 `GKX-Soft`。自动修与编码约束见本文第 8、9 节 |

## 1. 要解决的事

总集要求问题列表里的阻塞、高、中清掉之后才能上线。

11 个 `gkxlumen-*` 项目的质量门现在都是通过。`GKX-Soft` 没有条件，`sonar:scan` 又是 `allow_failure: true`，扫描成功就会显示通过。验收看问题条数，不看质量门状态。

## 2. 范围

平台上共 79 个项目。本方案只覆盖国科信上线的 11 个正式仓：

| Sonar project key | 仓库 |
|---|---|
| `gkxlumen-svc-platform` | lumen-svc-platform |
| `gkxlumen-spring-boot-bridge` | spring-boot-bridge |
| `gkxlumen-algo-py` | lumen-algo-py |
| `gkxlumen-topic-py` | lumen-topic-py |
| `gkxlumen-etl-es-py` | lumen-etl-es-py |
| `gkxlumen-ui-science-pc` | lumen-ui-science-pc |
| `gkxlumen-ui-science-mobile` | lumen-ui-science-mobile |
| `gkxlumen-ui-topic` | lumen-ui-topic |
| `gkxlumen-ui-topic-mobile` | lumen-ui-topic-mobile |
| `gkxlumen-ui-admin` | lumen-ui-admin |
| `gkxlumen-ui-algo-apiview` | lumen-ui-algo-apiview |

`gkxdemo-*` 是沙箱。`lumen-ui-admin` 与 `gkxdemo-admin-ui` 的问题数、代码行数完全相同，只处理 lumen 这一份。aico、zmate、问数等其余项目不属于这套系统。

数字都是整体代码上的未关闭问题，与问题页默认列表一致。

## 3. 盘点（2026-11-17）

| 项目 | 阻塞 | 高 | 中 | 低 | 安全 | 可靠性 | 可维护性 |
|---|---:|---:|---:|---:|---:|---:|---:|
| gkxlumen-ui-science-pc | 3 | 149 | 1268 | 1793 | 0 | 448 | 2949 |
| gkxlumen-ui-admin | 0 | 1040 | 229 | 1436 | 0 | 1088 | 1666 |
| gkxlumen-ui-topic | 2 | 369 | 431 | 986 | 0 | 150 | 1720 |
| gkxlumen-algo-py | 11 | 133 | 66 | 47 | 0 | 33 | 224 |
| gkxlumen-topic-py | 3 | 77 | 41 | 33 | 0 | 9 | 147 |
| gkxlumen-ui-topic-mobile | 0 | 75 | 85 | 310 | 0 | 42 | 451 |
| gkxlumen-ui-science-mobile | 0 | 15 | 94 | 97 | 0 | 18 | 196 |
| gkxlumen-ui-algo-apiview | 0 | 28 | 48 | 91 | 0 | 18 | 156 |
| gkxlumen-svc-platform | 5 | 4 | 6 | 0 | 9 | 0 | 6 |
| gkxlumen-etl-es-py | 1 | 5 | 10 | 4 | 0 | 3 | 17 |
| gkxlumen-spring-boot-bridge | 0 | 6 | 3 | 19 | 1 | 1 | 28 |
| **合计** | **25** | **1901** | **2281** | | **10** | | |

阻塞 + 高 + 中合计 **4207** 条。安全软件质量只有 10 条，集中在 Java 平台和 bridge。截图那个算法仓（阻塞 11、高 133、中 66、低 47，安全 0、可靠性 33、可维护性 224）与上表一致。

安全热点是另一张表，清掉「问题」不会让热点消失。待评审合计 **415** 条：

| 项目 | 待评审热点 |
|---|---:|
| gkxlumen-ui-admin | 120 |
| gkxlumen-ui-science-pc | 62 |
| gkxlumen-ui-topic | 58 |
| gkxlumen-svc-platform | 55 |
| gkxlumen-algo-py | 44 |
| gkxlumen-topic-py | 28 |
| gkxlumen-etl-es-py | 19 |
| gkxlumen-ui-topic-mobile | 12 |
| gkxlumen-ui-science-mobile | 11 |
| gkxlumen-ui-algo-apiview | 6 |
| gkxlumen-spring-boot-bridge | 0 |

## 4. 做法：分三筐

按规则归堆，不按项目平均改，也不在界面上逐条点。

### 筐 A：改代码

量级几十条，确认方案后先做。

**安全 10 条（必须改）**

| 规则 | 条数 | 级别 | 位置 |
|---|---:|---|---|
| `java:S6437` 硬编码口令 | 3 | 阻塞 | `gkxlumen-svc-platform`：`application-local.yml` 两处、xxl-job 的 `application.yml` |
| `secrets:S6697` MySQL 口令进仓库 | 2 | 阻塞 | 同仓 `helm/gkxlumen-platform/templates/mysql.yaml` |
| `java:S2658` 动态类加载 | 4 | 高 | 同仓 Feign 注册器、定时任务实现 |
| `kubernetes:S6865` ServiceAccount 自动挂载过宽 | 1 | 中 | `gkxlumen-spring-boot-bridge` 的 `k8s/dev-sso-bridge.yaml` |

口令改成占位符，真实值放已有 Secret，不把口令写进本文档或 git。helm 变更遵守 Nacos / 模板规约，只动这份 MySQL 模板里的口令字段。

**可靠性高：排序缺少比较函数，约 49 条**

规则 `typescript:S2871` / `javascript:S2871`。展示 PC 20、专题 PC 19、专题移动端 10。`Array.sort()` 不传比较函数时，数字会按字符串排。这是行为缺陷，逐处补比较函数。

**阻塞 20 条里其余的逻辑问题**

25 条阻塞里，5 条是上面的口令，剩下 20 条：

| 规则 | 条数 | 说明 |
|---|---:|---|
| `python:S3516` / `typescript:S3516` 函数所有分支返回同一值 | 19 | 算法仓 10（含 6 个 `narrate_*`）、专题 Python 3、展示 PC 3、专题 PC 2、etl 1 |
| `python:S930` 实参个数与形参不符 | 1 | 算法仓 `scripts/seed_policy_news_page.py` |

`narrate_*` 这类要逐条看。分支写死、结果与输入无关的，改逻辑。函数本来就只产出固定结构的，改成总集能在问题列表里接受的写法。不在文件头加 `NOSONAR` 把整文件压掉。

### 筐 B：改质量配置或扫描范围，并给总集一页说明

这些规则和现有仓规约或脚本用途冲突。按当前规则改代码，会把已经定下的写法改掉。处理方式是调整质量配置或 `sonar.exclusions`，变更写进给总集的说明，让问题列表上的条数一起降下来。

| 规则 | 约略条数 | 级别 | 原因 |
|---|---:|---|---|
| `typescript:S6859` / `javascript:S6859` 禁止绝对路径 import | 966（管理后台 952 + 14） | 高 | `lumen-ui-admin` 规约要求 `/@/` 别名。该规则没有放行参数 |
| `typescript:S3735` / `javascript:S3735` 禁止 `void` | 约 382 | 高 | 专题 PC 261、专题移动端 51、展示 PC 51、展示移动端 10、算法展示台 9。Vue 里用 `void` 丢掉 Promise，删掉会改变未处理拒绝的行为 |
| `python:S1192` / `java:S1192` 字符串字面量重复 | 122 | 高 | 算法仓 79、专题 Python 34、etl 3、bridge 6。算法仓样本多在 `scripts/` 种子脚本，不进运行镜像 |

算法仓扫描已经排除 `vendor/`、`tests/`、`.venv`。筐 B 若采纳，再加 `scripts/**`。管理后台的绝对路径、前端的 `void`，在质量配置里降级或对相应项目停用该规则，并在说明里写明仓规约出处。

这一筐大约盖住 1901 条「高」里的 **1470** 条。

### 筐 C：待拍板后再定要不要做

**认知复杂度（`S3776`）的「高」约 276 条**，是真重构：

| 项目 | 条数 |
|---|---:|
| gkxlumen-ui-topic | 76 |
| gkxlumen-ui-science-pc | 61 |
| gkxlumen-algo-py | 52 |
| gkxlumen-topic-py | 41 |
| gkxlumen-ui-admin | 17 |
| gkxlumen-ui-algo-apiview | 12 |
| gkxlumen-ui-topic-mobile | 12 |
| gkxlumen-ui-science-mobile | 3 |
| gkxlumen-etl-es-py | 2 |

默认阈值 15。截图里 `lumen_algo_service/views/ent_viz.py` 的 `enterprise_peers`（复杂度 51）属于这一类：查询、财务年份、五维指标堆在一个路由函数里，要拆函数，注释压不掉。

**中级 2281 条**，大头在展示 PC（1268）和专题 PC（431）。展示 PC 的前几条规则：嵌套三元 `typescript:S3358` 303、颜色对比度 `css:S7924` 262、`Number` 静态方法 `typescript:S7773` 182、ARIA 角色 `Web:S6819` 165。对比度和 ARIA 会改到已经评审过的界面，要单独立项，不塞进这次清零。

算法仓的中级 66 条里，未使用参数 `python:S1172` 29、嵌套条件表达式 `python:S3358` 16、函数名 `python:S1542` 4。截图里的 `def R` 就是这 4 条里的命名问题，只在 `entan.py`、`evaluation.py` 等本文件使用，改名成本低，可随筐 A 顺手做，不单开一筐。

「高」里去掉筐 B 的 1470 条、复杂度 276 条、排序 49 条之后，还剩约 100 条（`const`/`let`、空函数、嵌套过深、位运算截断、动态类加载等），随筐 A 的同仓改动一起清。

## 5. 待拍板

1. **上线阻断收到哪一档。** 建议：安全 10 条清零，可靠性的阻塞和高清零（排序、复核后仍成立的「恒定返回」和参数个数）。可维护性的高和中不作为本次阻断。若总集书面要求「高也要为 0」或「中也要为 0」，筐 C 整筐纳入，展示 PC 的中级会成为工期大头。
2. **筐 B 用配置解决，还是改代码。** 建议：配置加一页说明。改代码会把 `/@/` 别名和 Vue 的 `void` 约定改掉。
3. **415 条待评审热点算不算本次。** 建议：与问题列表分开。总集若把热点也算上线条件，再单独排评审，不和改代码混在一个来回里。

## 6. 拍板后的顺序

1. 筐 A：口令出库，排序补比较函数，20 条阻塞逐条复核后修改。机械项按第 8 节交给模型，强度按第 9 节。
2. 同时写出筐 B 的质量配置 / `sonar.exclusions` 变更说明，给总集。配置在总集认可以前不动生产门禁。
3. 按第 5 节的选择排筐 C 和热点。
4. 各仓推 `dev` 后靠现有 `sonar:scan` 复扫。复测看问题列表条数，不看质量门「通过」。
5. 筐 A（及拍板纳入的部分）在列表上归零之后，再把 `GKX-Soft` 收成「新代码上阻塞和高为 0」。在那之前保持软门禁，避免风格问题堵住日常发布。

## 7. 边界

- 批量标记 Won't Fix、False Positive，总集对着问题列表仍能看到处理记录，不作为清零手段。
- 文件头 `NOSONAR` 不作为清零手段。
- 为对比度、ARIA 改已经评审过的界面，不放进本次，除非第 5 节把中级纳入阻断。
- demo 仓、平台上其他产品的项目，不在本次修改范围。

## 8. AI 自动修

2026-11-17 对照 Sonar 官方说明和公开的自动修复实验，补这一节。检测仍用 Sonar 的确定性规则。Sonar 的结论是：用大模型找问题会带进大量误报，所以分析器不用模型检测，模型只修已经编号的问题。

本机是 SonarQube Server 25.12.0。官方 AI CodeFix、Remediation Agent 属于 Enterprise / Data Center，并把代码片段送到配置的大模型。这批仓的修法是：问题清单从本机 Sonar 导出，在仓里用已批准的模型改，再推 `dev` 走现有 `sonar:scan`。不把源码交到 Sonar 的云端修复服务。

### 8.1 闭环

一次只修一条规则，一个小变更。Sonar 的 Remediation Agent 按「规则 + 文件类型」合成一个拉取请求；定时跑时每个仓每次最多 5 条，未合并的请求到上限就停（默认 3 个）。

看起来修好不算修好。CodeCureAgent 在 1000 条 Sonar 告警上，看起来修好的有 96.8%，人工判定真正正确的是 86.3%。Sonar 官方代理在沙箱里重跑的是它自己的引擎，不跑项目测试，并写明测试和评审仍要人做。静态分析发现不了「问题没了，但计算结果变了」。每一批过三关：

1. 该仓的编译或类型检查。
2. 按这一条规则复扫：旧问题没了，也没有新问题。
3. 已有测试。测试被删、被 skip、断言被放宽，算这一批失败。

模型不许自己销账。禁止 `NOSONAR`、`# noqa`、`eslint-disable`，禁止为了消告警去改质量配置或删函数。修不掉就停，把规则、文件、试过的改法交人决定。

通过标准用问题 API 的条数前后对比，加上该仓测试。`GKX-Soft` 上的「通过」说明不了条数少了。

### 8.2 哪些规则可以交给模型

对照 Sonar AI CodeFix 认证清单（文档版本 2026.4；本机 25.12 未核对该功能是否开通）。清单里没有的规则，官方也不自动修。

| 规则 | 交给模型？ | 依据 |
|---|---|---|
| 排序补比较函数 `S2871`、实参个数 `S930`、函数改名 `S1542`（4 处 `def R`） | 可以 | 改动局部。TypeScript 的 `S2871` 在认证清单里 |
| 重复字符串 `S1192`、未使用参数 `S1172` | 小批试 | Python / Java 的 `S1192` 在认证清单里。未使用参数可能是对外接口，改签名前要人看 |
| 硬编码口令 `S6437` / `S6697`、动态类加载 `S2658` | 人改 | 模型会把口令挪到另一个文件或写进日志。口令只换成占位符 |
| 恒定返回 `S3516` | 人先判，再决定改不改 | TypeScript 在认证清单里，Python 不在。叙述函数若被改成「返回值看起来不同」，问题消失，业务也变了 |
| 认知复杂度 `S3776` | 一次一个函数，且该函数有测试 | TypeScript 在清单里，Python 不在。拆成现有风格的辅助函数，公式保持原样 |
| 绝对路径 import `S6859`、`void` `S3735` | 不交给模型 | 两条都在认证清单里，模型会改掉。这会推翻 `/@/` 别名和 Vue 丢掉 Promise 的约定，仍属筐 B |

复杂度要带上静态指标，不要只写「降到 15 以下」。对照实验里，同一模型加上复杂度指标后再重构，平均多降约 7 个百分点。失败里，理解错上下文约占 24%，乱改名约占 15%，擅自加功能约占 14%。`enterprise_peers` 要写清抽出的块（读财务年份、算五维、组装行），并写上对外 JSON 字段不变。

和三筐的接法：筐 A 里机械的部分（排序、`S930`、`def R`）可以自动修；口令和动态类加载人改。筐 B 维持配置方案，不派模型去改 966 条 import 和约 382 处 `void`。筐 C 的复杂度等第 5 节拍板后，按函数开小变更。

来源：

- [Sonar：分析器不用大模型检测](https://community.sonarsource.com/t/webinar-introducing-sonar-ai-code-assurance-and-ai-codefix/127293)
- [AI CodeFix 规则清单（Server 2026.4）](https://docs.sonarsource.com/sonarqube-server/2026.4/quality-standards-administration/managing-rules/rules-for-ai-codefix)
- [Remediation Agent：按规则分组、沙箱复扫、不跑测试](https://www.sonarsource.com/blog/sonarqube-remediation-agent-is-now-available-on-sonarqube-server/)
- [CodeCureAgent](https://arxiv.org/html/2509.11787v5)（96.8% 看起来修好，86.3% 人工判定正确）
- [复杂度重构：静态指标加模型优于只靠模型](http://urn.kb.se/resolve?urn=urn%3Anbn%3Ase%3Amiun%3Adiva-55481)

## 9. 与 Ponytail 的关系

Ponytail 不管 Sonar 的问题清单，也不是自动修复器。它只在 coding agent 改代码时生效，默认 `full`：先读懂，再按懒阶梯写最短的有效 diff。真源是 `.cursor/rules/ponytail.mdc`，用法见 `agent-delivery/ponytail-usage.md`。本文、给总集的口径说明、质量配置变更，都不按「少写代码」来压篇幅。

对齐的地方：

- 一次只改一条规则、不顺手重构，就是最短 diff。
- 筐 B 的绝对路径和 `void`，阶梯第一问是要不要做。总集没要求改写法时，改 900 多处 import 就是不该写的代码。
- 口令、动态类加载不能靠少写跳过。护栏写明安全优先于懒。
- 改完留一个能失败的检查，和第 8.1 节的三关是同一件事。

派单时写死，避免 agent 用错懒法：

- Sonar 的认知复杂度要拆函数，行数会变多。这是点名要的改动，拆到阈值以下就停，不再包一层框架。`ponytail-review` 里的「复杂度」指过度设计，和 `S3776` 不是同一个词。
- 「删除优于新增」不能用来删分支、删参数、删测试来压低条数。未使用参数若是对外接口，删了会改契约。
- 重复字符串若认定脚本不算，就排除 `scripts/**`，不为种子脚本抽一套常量模块。

自动修开 `ponytail full`，并在派单里加一句：禁止 `NOSONAR`、禁止删逻辑销账、禁止改质量配置，除非这单明确是筐 B。不用 `ultra`：它会先质疑函数要不要拆，和总集要求相反。

## 10. 数字怎么复核

管理账号在本机执行（口令不进 git）。把 `componentKeys` 换成第 2 节的 key，逗号分隔即 11 个一起查：

```text
GET /api/measures/search
  ?projectKeys=<keys>
  &metricKeys=software_quality_blocker_issues,software_quality_high_issues,software_quality_medium_issues,software_quality_security_issues,alert_status

GET /api/issues/search
  ?componentKeys=<keys>&resolved=false&ps=1
  &facets=rules,impactSeverities,impactSoftwareQualities

GET /api/hotspots/search?projectKey=<key>&status=TO_REVIEW&ps=1
```

阻塞明细以 `impactSeverities=BLOCKER` 的问题列表为准，本文第 4 节是 2026-11-17 的快照。

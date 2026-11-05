# POL-NEWS-RUNTIME-20261105 · 扶持指标上线后整包空白回归

日期：2026-11-05。用户反馈补 mock 发布后，原有统计也全部为空。本任务修复回归并跟进实际 entan 镜像部署。

## 根因

- Java 政策门面实际调用 `gkxlumen-platform-entan-py:8000`，对应 `docker/Dockerfile.entan-api`。
- 该镜像只 COPY `vendor/entan-py` 下的 api/entan/polan/innov 等包，没有 lumen_common。
- 上次新增的 policy_indicators 分支导入 `lumen_common.algorithms.policy.news_demo`，只在完整本地仓可运行，独立 entan 镜像运行时会 ModuleNotFoundError；整个指标请求失败，Java 通过原 fail-soft 返回空包，导致所有卡片与排名空白。
- 上次 afaa26d 的 pipeline 3886 中 deploy:entan-api 成功，证明错误代码确已进入实际服务，不能归因于前端缓存或未补数据。

## 修复与防回归

- 将数据库演示读取实现移入实际随镜像打包的 `vendor/entan-py/polan/basic/news_demo.py`，路由只从 polan.basic 导入。
- lumen_common 只保留兼容导出，供本地补数脚本与既有调用方使用，不再作为 entan 路由依赖。
- 演示读取外围增加异常隔离，出现缺表/读取/可选模块异常时保留原 portal_gaps 与正式排名，不让演示模块拖空整包。
- 新增独立 Python 子进程测试：只允许 entan vendor 包与已装依赖，确认找不到 lumen_common；通过实际 FastAPI 路由验证10项统计、正常演示数据及强制演示异常后的统计保留。
- 全量 CI 暴露 tests 中 scripts 名称与 vendor 包冲突；改为 runpy 按明确脚本路径加载，避免测试收集依赖顺序。
- 不改前端、不改现有补数、不写数据库、不调整指标口径与评分。

## 过程与验证

- 相关回归35项通过，覆盖独立镜像包依赖与演示失败隔离。
- 本地按 CI 命令运行全量测试：754 passed、6 skipped，耗时230秒。
- 初始修复 pipeline 3895 被全量测试收集的 scripts 包冲突阻断，已读取任务日志并修复；不将该流水线记为绿。
- 最终修复提交 `8e6f195`，前置 `5cc01c8`（镜像包依赖修复）、`73f1a64`（可选演示异常隔离）；合并远端仅使用正常 merge，不改写历史。
- 跟踪最终 CI 的 py:test、image:entan-api、deploy:entan-api；最终结果在下方补充。

## 规范与限制

- 用户直接授权修复；claimed_by=agent:algorithm-agent；未提供监管人实名，不代填。追踪ID未通过registry MCP注册，当前工具未挂载；不直接修改注册表。
- ponytail: full。遵守主仓路径、团队/并行规则；仅改本任务文件，保留其他会话补数脚本。
- 架构仍为前端→Java→独立entan Python→原数据库，修复实际打包边界，不增加服务或依赖。
- 数据来源标记和演示/正式隔离保持原约定；前端视觉本次无变更。
- 当前没有可用 SSH MCP，无法执行 Pod 内请求或读运行日志；使用实际 CI job 状态确认镜像与 rollout，未宣称浏览器视觉验收完成。
- 已直接只读请求实际 Java 网关 `/tts/lumen/api/policy/topic/v1/policy/indicators?kind=all`：修复发布前 HTTP200/code=0，但 honesty.engine=unavailable:feign，portal_gaps和demo_support均缺失，复现截图整包空白；继续待最终部署后复查。
- cost 无环境统计，不臆造费用或验收状态。

## 最终线上验证

- 最终流水线：[3898](https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/lumen-algo-py/-/pipelines/3898)，提交 `8e6f195`。
- py:test、image:entan-api、deploy:entan-api 均 success；整条pipeline显示manual是因为非本任务的innov/entan-worker仍为manual，不代表目标服务未部署。
- 实际 Java 网关指标请求 HTTP200/code=0，返回 portal_gaps=10、demo_support.cards=10、province=12、city=10；原 unavailable:feign 消失。
- 使用当前前端 newsGapCards/newsDisplayRanks 转换上述线上真实响应，核对10项卡片均可展示、省市排名分别12/10项，演示来源标记保留；未凭本地函数结果替代线上服务恢复结论。
- 无需重灌数据或修改前端，刷新页面即可重新请求已恢复的服务。未完成浏览器截图级验收。

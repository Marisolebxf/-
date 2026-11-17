# KG-GRAPH-TRIPLE-03 · 两域本地实施阶段交接（整单未完成）

## 范围与认领

执行负责人宋飞扬；派单监管徐滕强。2026-11-17通过task-registry MCP认领并置in_progress，保留COVER-01依赖。依据唐绍祖11-16答复，先做PERSON 110/111与RESEARCH 114/115；TECH 104/105等待COVER-01。本handoff只记录阶段事实，不申请integration、不作为整单AV-0/签收证据。

## 已实现

- storage：PERSON与RESEARCH的etl/pipeline-to-nebula.md更新会签口径；TECH契约保留。PERSON=6、RESEARCH=6、TECH=9，总清单21未删减。
- lumen-algo-py：两域12操作/v1与/internal成对，默认dry_run=true。8实时只读操作+4完整索引消费；无索引诚实503。独立本地离线索引构建器不发网络请求，只接受已验证完整Nebula导出，原子发布内容寻址SQLite。
- lumen-svc-platform：gkxlumen-innov的EntityGraphController/Client/Feign配置，12操作白名单、HTTP错误原样透传；网关仅person/research graph/ops两条路径置catch-all前。模板未发布Nacos。
- lumen-ui-topic：两个页面入口，六操作入口、真实边权、分页、空态/501/不可用、每op实际调用apiview记录；前端只调用Java路径，无Mock。
- diagram_id：PERSON-GRAPH-TRIPLE、RESEARCH-GRAPH-TRIPLE；TECH-GRAPH-TRIPLE仍为设计。

## 验证与证据分层

详见主文同目录《KG-GRAPH-TRIPLE-03-两域本地实施与待发布.md》。Python小样本原始证据为KG-GRAPH-TRIPLE-03-two-domain-python-live.json。明确区分单元测试、本机Java/Python链路、正式K8s网关与发布页面；未获正式网关回执，不宣称线上通过。

## 数据及边界

零图/源库写入，零schema修改，未重启实例。人才强度固定co_paper_count，不用weight/collaboration_score；机构篇数和分年strength_by_year区分，禁跨年比较。research用inst:、服务机构用institution:；按两端Tag隔离cooperate、排除company。合作度为唯一邻居数。在线精确VID、查询3秒/总预算10秒、每进程最多4个实查、邻域501完整性探针、子图200点/500边/20查询。

## 未完成及依赖

1. TECH 9操作与技术机构完整验收等待COVER-01回执。
2. PERSON/RESEARCH名称检索、全域浏览需完整图库索引；目前没有可用的经验证图导出，不使用T03源表快照冒充（T04已覆盖节点props）。未启动全图库导出或全量排序作业。
3. 高连接实体完整邻域强度排序需离线邻接索引；>500候选返回503，子图截断并提示。完整邻接索引尚未实现。
4. 三个业务仓代码与编排变更尚未提交推送；前端AGENTS要求当前用户确认push。Nacos单dataId线上发布须当次会话用户批准，按gkx-nacos-shared-config执行，先读线上原文比对。
5. 正式CI、K8s部署、鉴权、真实Java网关curl及生产环境页面走查仍待执行；局部Java编译测试不替代全仓CI。

## 成本

执行工具标识Codex；实际模型账单、token及费用工具未提供，待平台回填，不填0或估算值冒充实耗。

## 下一执行入口

先审查本地补丁与本地验证证据，用户确认推送后按各仓dev流程推进。平台侧按单dataId发布网关路由，再经真实Java网关逐op留证。完整索引和TECH补齐前继续保持整单in_progress。

## 2026-11-17T19:09:52+08:00 · 用户已批准提交推送

当前会话用户明确授权“提交推送”，本机Git凭据已存macOS钥匙串（无密码落仓）。已提交的业务仓版本如下，均推送目标origin/dev：

- [lumen-algo-py 6fa198ca](https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/lumen-algo-py/-/commit/6fa198ca1a5878d7fce6d1a6dd17c12d3dc0ca6a)
- [lumen-svc-platform f5ae0e8d](https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/lumen-svc-platform/-/commit/f5ae0e8d69dc51f95493ded7ee70257433a31eda)
- [lumen-ui-topic cb6656d2](https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/lumen-ui-topic/-/commit/cb6656d2cb1c868c1122f7c35bdae4a7b9fe3d5d)

已同步编排仓最新dev并保留团队登记内容；任务仍in_progress，不标整单完成。CI状态另以各提交的流水线结果为准，未声称CI/正式网关联调已通过。本次执行提交推送；Nacos单dataId线上发布尚未执行，相关索引与TECH限制仍按前文。此前“尚未提交推送”描述为该阶段历史状态。

## 2026-11-17T19:20:26+08:00 · 推送与CI核验

四仓origin/dev推送已由GitLab提交refs API复核。Java CI首轮暴露Mockito旧版本不支持verifyNoInteractions，已改为兼容never断言并补推`7107ceee`；新流水线backend:build及deploy:innov通过。

- Python：948 passed、7 skipped；自动镜像/部署/路由smoke通过；deploy:innov与deploy:entan-worker保留手动。流水线：https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/lumen-algo-py/-/pipelines/5723
- Java：必需构建、测试与innov自动部署通过；可选sonar:scan（allow_failure=true）在记录时仍运行，不据此宣称整条流水线已成功；其他手动任务未触发。流水线：https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/lumen-svc-platform/-/pipelines/5726
- 前端：构建、扫描、镜像与自动部署全部成功。流水线：https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/lumen-ui-topic/-/pipelines/5725
- 编排仓：文档/任务登记变更按workflow过滤，不触发Feishu服务部署。

Git HTTPS凭据已按用户要求存macOS钥匙串，未写入仓库；网页会话与Git凭据独立。没有触发Nacos手动任务或单dataId发布，正式新增网关路由仍待发布，完整索引/TECH等限制继续保留，任务仍in_progress。

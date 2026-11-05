# CHAIN-PANORAMA-STRUCTURE-FIX-20261105 · 产业全景结构空白修复

日期：2026-11-05。范围：科技专题服务系统 / 可视化管理 / 产业全景可视化 / 结构。
需求依据：`bid-reference/srs/04-科技专题服务系统/门户内容运营中心/可视化管理.md` 中产业链层级图、产业分类饼图与行业/领域切换要求。

## 任务与执行规范

- 用户本会话直接授权排查、补充缺失 mock，并明确要求按主仓 Cursor 规范提交代码。
- claimed_by：agent:frontend-agent / agent:api-agent / agent:algorithm-agent，按仓职责标记提交。
- supervised_by：本会话未提供团队实名，不推断或代填。
- 本 ID 为本次交付追踪标识；当前会话未挂载 task-registry MCP，未直接读取或修改注册表，也未伪造认领或验收状态。
- ponytail: full。复用现有 Graph、ECharts 配置、Java 门面、Python 同步接口及 ADS 表，无新增依赖。
- 已核对 `00-path-resolution`、`00-team-constitution`、`multi-session-protection`、`frontend`、`api`、`algorithm`、`data`、`ponytail` 规则。

## 原因与实现

1. 画布已有数据，但普通 CSS 中使用了 Vue scoped 专用 `:deep()`，480px 高度未生效。改为普通后代选择器。
2. 前端真实模式固定显示分类空态，Java `buildMix` 也固定返回空数组。现由 Python 从既有 ADS 分布表读取，Java 转发，Vue 展示行业/领域两套分布。
3. 分类读取限定当前对象、全国范围、企业计数指标、已发布且未删除记录；按维度选择最近周期与批次，剔除空值和非正值。
4. 新增 `seed_panorama_mix.py`：默认 dry-run，显式 `--apply` 写入，只补缺失维度，不覆盖已有记录；仅写 demo ADS，无 DDL、无 DWD/ODS 写入。
5. 分类行透传 `source=mock/mysql`，前端沿用自带 review 门控的 MockBadge，不把演示计数当成真实统计。

## 数据与追溯

- 表：`demo_gkxlumenx_ads.industry_chain_metric_dist`，本次新增 407 行，覆盖 53 个产业及子链。
- 指标：复用 `M_CHAIN_ENTERPRISE_COUNT`；`bucket_code` 以 `industry:` / `domain:` 区分展示维度。
- 批次：`mock_panorama_mix_20261105`；版本：`mock-panorama-mix-v1`。
- 行业标签为合成演示分类；领域标签取目录的环节/领域名称，计数为合成演示值，不代表企业实际数量。
- 回读 `INB120401`：原快照 3 节点、2 关系；新增行业 4 类、领域 3 类。
- 再次 dry-run：`objects=53, missing_slices=0`，未重复写入。
- 既有表本来已有数千条其他指标分布；本次只补分类缺项，不为凑规模复制记录。

## 验证

- Python：`python3 -m pytest tests/test_chain_sync.py -q`，13 项通过；覆盖维度隔离、旧批次排除、非法数值和空数据库。
- Java：JDK 21 编译本次 DTO、服务及测试，JUnit 定向运行 `IndustryVizServiceImplTest`，6 项通过。
- Maven 标准测试未通过启动阶段：本机离线仓缺 git-commit-id 插件传递依赖；未将定向验证描述成完整 Maven 构建通过。
- 前端：`npm run type-check`、`npm run build-only` 通过；构建仍有既有 bundle 大小提示。
- 三仓 `git diff --check` 通过。
- 页面视觉复核未完成：浏览器自动审批拒绝访问本机验证 origin；临时验证页与临时服务已移除/停止。

## 架构、交互与范围自检

- D8 / Design：沿用 Arco、原页布局、G6、ECharts 和既有 480px 画布尺寸；无新配色、字体或组件体系。视觉验收未签收。
- D9：保留 Mock 来源、批次与 Review MockBadge；不修改指标口径或就绪度，不声称 D4 live。
- D10：沿用现有页签、Arco radio 切换、loading 与空态；键盘/无障碍走查与设计规范全量截图验收未执行。
- 调用链：Vue → `gkxlumen` Java → `lumen-algo-py` → 既有 ADS；无前端直连 Python，无新增 demo 服务回落。
- 可观测：沿用现有 request / Feign / Python trace 路径；未采集部署后的 traceId。
- 无新增模型、图谱协议变更或对象存储变更；无口径审批状态改写。
- 仅提交本次产业全景相关 9 个代码文件；工作区企业可视化等其他会话改动保持原样。

## CI/CD 与提交

- 分支：四仓均为 `dev`，按规范推送 `origin/dev`，不使用 force。
- 前端：`e4f66cc`。
- Python：`8d1928c`。
- Java：`80a2b61`。
- CI pipeline 与 K8s rollout：提交后另行查询；本记录不构成部署成功或线上 QA 验收。
- 本地验证不替代 CI、K8s rollout 和页面集成验收。
- cost：当前环境未提供本任务可核实的 token 用量与费用，未臆造 cost 字段或写注册表。

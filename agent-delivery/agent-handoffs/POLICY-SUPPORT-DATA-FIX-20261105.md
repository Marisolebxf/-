# POLICY-SUPPORT-DATA-FIX-20261105 · 扶持指标数据核查与客户空态修复

日期：2026-11-05。用户本轮改为处理扶持指标红框中的内部口径文案，并要求核实是否真实数据。影响深度不作为本次施工范围。

## 执行约束

- claimed_by：agent:frontend-agent / agent:algorithm-agent；用户会话直接授权。
- supervised_by：未提供实名，不推断。追踪 ID 未通过 registry MCP 注册，当前未挂载该工具；不直接读写注册表、不声称验收通过。
- ponytail: full。遵守主仓路径、团队公约、并行保护及相关前端/算法/数据规则；沿用现有组件、数据链路、评分公式，不增加依赖。

## 根因与数据证据

- 前端 `newsGapCards` 将后端 `portal_gaps[*].reason` 直接作为缺值卡片正文。该字段包含 pending_algorithm、natural_month、口径登记和拒绝替代指标的工程说明，不是统计结果。
- 远端只读核实：`demo_gkxlumenx_dwd.policy_base_info` 未删除行 20008，province 去重数 31；source_plane 为 domestic 20007 / global 1，etl_batch_id 均为空。city 为深圳前缀的行数 0。
- 20008 / 31 是现有库内统计结果，不代表已认证的生产真源或完整“数量及连续性”指标。库名是 demo，来源批次不足，不能笼统宣称全部是真实生产数据。
- 复跑现有 indicators：市级发布密度、深圳数量趋势、深圳各区发布等 value=null；后端将内部缺数原因回传，前端暴露了该说明。
- 原“省级发布密度 1932”是各省存量 Top10 第一条，并非区域逐月发布密度。市级也存在取存量最大值代替密度的路径。
- `demo_gkxlumenx_ads.policy_intensity` 中 policy 层 20008 条评分全部为 `mock_20260623`，ext.is_mock=true。原 API 查询只选 score/id，丢失来源；聚合排名因而错误表现为非 mock。

## 修复

- 扶持指标卡片有值照常展示（包括 0），缺值统一“暂无统计数据”，不透传内部 reason、不补 0 或造数。
- 移除扶持页“需规93–95、98……不用相近指标填数”等开发说明。
- 排名空态改为“暂无省级政策力度排名”“暂无城市政策力度排名”。
- Python 查询保留 ext、calc_batch_id；排名聚合排除明确 mock 来源和不可解析 ext，原评分及非 mock 聚合公式不变。
- 区域存量分布仍保留为明细，但不再填入省/市发布密度标量；没有密度计算结果时保持 null。
- 未补数、未写库、未变更 schema，未修改指标定义和就绪度。

## 修复后只读验证

- indicators 全量调用返回：全国数量 20008、覆盖省份数 31、全国月发布计数 1、节点覆盖 99.1、深圳节点覆盖 0；其余缺项为 null，省/市排名均 0 行。
- 该返回只验证读表和数据排除行为，不证明连续性、密度、节点覆盖等所有业务口径已完成治理。现有原料质量、city 缺失、全国月计数的时间范围等仍需数据侧处理，不在本次擅自定义。
- Python：`python3 -m pytest tests/test_policy_portal_gaps.py -q`，19 项通过。
- 前端：政策新闻 selfcheck、type-check、build-only 通过；构建有既有 bundle 大小提示。selfcheck 新增内部 reason 隔离、零值与 fabricated 包拦截覆盖。
- 两仓 diff-check 通过；未进行浏览器视觉或线上部署验收。

## 并行提交与交付

- 同仓另有影响深度会话修改相同页面/模型/自检文件。提交间发现并行更改后，保留影响深度实现，并以追加提交恢复本任务的扶持空态，未使用 reset/stash/revert 清理其他会话工作。
- 前端提交：`7a8c45a`、`47b9b68`；Python：`ff59975`。分支 dev，按规范推送 origin/dev。
- 调用链仍为前端 → Java → Python → 现有库；无前端直连 Python，无新 demo 服务回落；沿用 trace header。
- D8/D10：保留 Arco 卡片/表格和原交互，仅修客户文案；视觉及键盘全量走查未执行。
- D9：内部诊断保留后端/代码和本核查记录；不改指标口径，不以演示值伪装正式排名。
- CI pipeline、镜像和 K8s rollout 未确认，不等同于部署成功。cost 数据未由环境提供，不臆造 token/费用字段。

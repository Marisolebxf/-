# FE-TS-10C · handoff

- 任务：`FE-TS-10C`（implementation · 关键实体与关系前端接线）
- 日期：2026-11-08 · 监管：`human:刘剑锋` · 认领：`agent:frontend-agent`
- 状态：代码完成三绿（maintain 测试/type-check/build 1m19s），feat/m10-ent-wiring 本地提交待推（GitLab 403）；**mock 轨可验页面，real 轨联调待 Python 写侧**。不标 done

## 范围与实现

- api 层 `maintain-ent.ts`：**变更集模型**（不是立即生效——提交→发布→回读 R2 重组）；7 op 类型化构造器（GraphOp 联合）；R1 推荐（keyword/sortBy 三值）+R2 现状；409 diff→「他人已修改请刷新」、503 pending→「已受理投影中」行内文案；client_op_id 幂等键生成
- 面板 `EntityRelationPanel.vue`：六写操作双轨化（hang/update 分流 tech|thirdparty/unhang/delete_entity_edge/update_entity_edge 含 G1 强度+时间）；busy 防抖；**addRelation 函数+新增关系三 select 区整体移除**（超需规，API 册 §0 显式放弃）；R1 强度列加 ⓘ（title=M_TECH_GRAPH_105_1）；勾选纯函数保留（选择集是页面本地态）
- mock 轨 `maintain-ent.ts`+register 8 命中：demo 演示态纯函数透传（页面内存语义不变）

## 已知注记（联调时收口）

1. `technologyId` 暂硬编码 1（演示种子 ent-1=具身智能）——R2 现状接入后由「当前选点/唯一技术点」取
2. 人工强度标注「（人工）」：页面类型 PanoramaRelation 无 source 字段，R2 重组时带上再渲染（模板留注记位）
3. entity_type 映射：页面中文类型（人/机构/论文…）→ 契约 entity_type 的正式枚举对齐（C01/C03 主数据在册）联调定
4. real 轨依赖：ENT-JAVA 门面已就绪（8d90869）；**Python 写侧（ENT-PY-IMPL）未开工**（lumen-algo-py 仓 GitLab 403 无法 clone）——real 轨全链路联调阻塞中

## 验证

- `node --experimental-strip-types maintain.test.mjs` ok；`pnpm type-check` ✅（修 6 处：MaintainSeq 导源/导名/模板残余）；`pnpm build` ✅
- mock 轨页面可走查（USE_MOCK=true 演示态语义与 demo 冻结一致）

## cost

- actual_tokens: ~55k
- model_used: glm-5.3（ZCode agent）
- actual_cost: <$0.5
- cost_warn: green

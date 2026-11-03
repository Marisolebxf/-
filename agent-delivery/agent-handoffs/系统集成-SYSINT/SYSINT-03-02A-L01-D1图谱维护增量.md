# Handoff · SYSINT-03-02A-L01 产业全景运营正文 · D-1 产业链图谱维护增量

> **任务**：`SYSINT-03-02A-L01`（feature / P1 / L / 5分）· 执行 `agent:frontend-agent` · 监管 `human:孔东`
> **本轮范围**：D-1 拍板项（2026-11-03 human:孔东）——叶子 318 产业链图谱维护（结构绘制 + 关键环节标注）+ R-5「待确认」占位列替换。只动前端，数据走本机 mock。
> **前序**：`SYSINT-03-02A-L01.md`（主档）、`SYSINT-03-02A-L01-缺项修复增量.md`（319/A-3/C-2 轮）
> **代码基线**：`lumen-ui-topic` dev @ `05d7178` 之上，commit `c7bb081` **停在本地未 push**（人工验收闸门）
> **建档**：2026-11-03 · 强度 ponytail full

---

## 需规对照（叶子 318，需规 7775–7785）

| 需规要求 | 实现 |
|---|---|
| 产业链结构绘制维护：添加节点 | 「环节节点」`CmsRepeatRows`：环节名称（必填、唯一）+ 分段（上/中/下游）+ 标注 + 说明 |
| 定义上下游关系 | 「上下游关系」行编辑器：起点 → 关系（上游/下游/横向/关联）→ 终点，端点限已建环节（下拉） |
| 调整层级布局 | 分段（上/中/下游）驱动 G6 dagre LR 分层布局，与门户图谱一致 |
| 关键环节标注维护 | 节点标注 select：关键环节 / 瓶颈关注 / 活跃环节——与既有图谱 G6 描边样式语义一致（`industryStructureLabels`） |

## 修改清单

| 文件 | 改动 |
|---|---|
| `src/views/cms/panorama/panoramaChainGraphModel.ts` **新** | 纯逻辑层：rows→节点、chain_edges JSON→关系、双校验器（重名/空名/端点未建/自环）、记录→图谱一步出 |
| `src/views/cms/panorama/PanoramaChainGraphTab.vue` **新** | 编辑 Tab：左编辑右预览；预览复用门户 `IndustryPanoramaGraph`（@antv/g6，D-1 指名复用对象，零新依赖） |
| `src/components/cms/cmsTypeSchema.ts` | 新 content_type `pano_chain_graph`（4 列），BLOCKS 增第 7 块 |
| `src/components/cms/cmsMockSeeds.ts` | IC 种子：4 环节 + 3 关系（已发布） |
| `src/views/cms/panorama/PanoramaCmsWorkspace.vue` | R-5：列表「产业链图谱」列 待确认→真实状态 tag（点击进编辑）；编辑页「待确认」Tab → 真组件；删除 `explainGraphPending`/`GRAPH_PENDING`/pending 样式 |
| `src/views/cms/panorama/panoramaChainGraph.selfcheck.mjs` **新** | 自检：schema 落点 + 纯逻辑行为 + R-5 无「待确认」断言 |

## 校验闭环（保存前拦截）

- 环节：空名 / 重名（重名 = G6 id 冲突，必须拦）
- 关系：端点必填 / 端点须已建 / 禁自环
- 发布：至少 1 个环节
- 预览只画合法边（坏数据不伪造结构）

## ⚠️ 契约偏差声明（承接前轮）

`pano_chain_graph` 为**新 content_type**，契约草案（PORTAL-CMS-专题全景 5 类 pano_*）无对应类型；`fields.chain_edges` 存关系 JSON 属前端过渡形态。接 Java 前需契约确认会同步，Java 叶 `SYSINT-03-02A-JAVA-L01` 需增对应端点。

## 与 Java 图谱快照的关系（待确认，不阻塞本轮）

门户展示侧 `IndustryOverviewPage` 的图谱数据来自 Java snapshot 接口；CMS 维护数据（本机 mock）与 snapshot 的同步链路 = 契约确认会议题之一。本轮 UI 能力先行，不动门户展示链路。

## 测试结果

- `node --experimental-strip-types src/views/cms/panorama/panoramaChainGraph.selfcheck.mjs` ✅
- `node --experimental-strip-types src/views/cms/panorama/panoramaCmsGapFix.selfcheck.mjs` ✅（前轮无回归）
- `npm run type-check`：本轮文件 0 错误（`vite.config.ts` 存量、`CmsScalarField.vue` 2 错为另一会话在改文件，均非本轮引入）
- `npx eslint`（全景目录 + schema + seeds）✅ 0/0

## 验收建议（走查路径）

1. 列表：集成电路行「产业链图谱」列显示**已发布**（种子）；人工智能/生物医药 = 未维护（R-5 生效，全页无「待确认」）
2. 编辑集成电路 → 产业链图谱 Tab：左侧 4 环节 + 3 关系，右侧 G6 实时预览（EDA 设计蓝描边=关键、晶圆制造橙描边=瓶颈）
3. 加一个重名环节 → 保存 → 报「环节名称重复」
4. 关系选未建端点（先删环节再保存）→ 报「未建环节」
5. 改环节分段 上游→下游 → 预览布局随之变化
6. 人工智能 → 图谱 Tab → 空态「添加环节后此处预览图谱」→ 添 1 环节发布 → 列表该列变已发布

## 架构合规自检

- 调用链：纯前端 mock，无新接口，未越层 ✅
- 复用优先：G6 组件/行编辑器/标量字段/mock store 全部复用既有，零新依赖 ✅
- D8/D9/D10：CMS 管理页无统计数字，无 metric 角标义务 ✅
- 可观测：mock 阶段无请求 ✅
- 契约偏差已声明 ⚠️

## 任务剩余（03-02A）

- C-3 产业选择换 `IndustryThreeLevelCascader`（走主数据，CMS-JX-IND-TREE integration 中）
- B-1 多语言挂 D-3 待拍板
- 契约确认会：pano_* 全部偏差（前轮 5 类 + 本轮 chain_graph）一并同步

## cost

- actual_tokens: ~55000
- model_used: glm-5.3
- actual_cost: ~$0.45
- cost_warn: green

**ponytail**: full

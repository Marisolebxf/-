# `/goal` · LUMEN-POLICY-D-POL-01-SCOPE-L01

```
/goal LUMEN-POLICY-D-POL-01-SCOPE-L01
角色：frontend-agent
监管人：human:淮政玮
认领：coordinator_dispatch · lock 24h
仓：lumen-ui-topic · origin/dev
强度：ponytail full
复刻：布局+交互+样式+评审+Mock开关。必读 templates/fe-replica-visual-dod.md。
范围：三项分析共用配置页 PolicyAnalysisConfigPage 的产业锚点：集群(产业 map)→该 map 下 L0（恰好 1 个）；不强制对比篮。占位与只改 Hero 不算完成。
禁止：贴 JSX；页内 MOCK；自造 ⓘ；lumen 调 demo-* 服务（D12）；USE_MOCK=false 时 fixture 填数。
数仓：不换库。Java 读的就是 demo_gkxlumenx_*。
对照：demo-ui-topic PolicyAnalysisConfigPanel + IndustryAnalysisScopeFields + listClusterScopeOptions/listL0ScopeOptions。handoff 须 R1–R5 + W1/W4（V1–V7 本叶 N/A 并写明）。
图：POLICY-STORAGE-FLOW 产品链不改工厂拓扑；配置页提交仍只调 Java analysis/tasks。
```

## 人审拍板（2026-09-02 `human:淮政玮`）

1. **产业选择以 demo 为准**：先选**集群**（产业 map 表），再**直接选该 map 下 L0 产业**。
2. **不需要从对比篮选**。篮分发可保留为可选预填，不得再当主路径/唯一入口。
3. **政策三项分析菜单同一套**（时序 `/policy/overview`、区域对比 `/policy/analysis`、深圳三维 `/policy/recommendation` 共用 `PolicyAnalysisConfigPage`，改一处即三页）。
4. 政策查询 `/policy/search` 本叶不动（无集群级联）。扶持/维护仍 P1，不本叶。
5. 总控已改 §0 #10 + 金路径 #2；旧 POL-01「篮勾 1 产业当金路径」作废。

## Demo 真源（只对照语义，禁止贴 JSX / 禁止 Demo fixture 填数）

| 文件 | 用什么 |
|------|--------|
| `demo-ui-topic/src/app/pages/industry-center/IndustryAnalysisScopeFields.tsx` | 集群 Select → L0 Select；无集群禁用产业；无映射 `UNMAPPED_CLUSTER_MESSAGE` |
| `demo-ui-topic/src/app/pages/industry-center/industryObjectSelect.ts` | `listClusterScopeOptions()` → `listL0ScopeOptions(clusterId)`（L0 = 该 cluster.l0） |
| `demo-ui-topic/src/app/pages/policy/PolicyAnalysisConfigPanel.tsx` | `needsChain={false}` `showChain={false}`；文案「本页直接选择产业；单次恰好 1 个」；`fromBasket` 仅 Tag，非门闩 |
| `lumen-ui-topic/src/composables/useIndustryClusters.ts` | 已有 `l0Options(clusterId)`，L0 必须来自集群 map 的 `l0[]` |
| `lumen-ui-topic/src/components/form/IndustryClusterSelect.vue` | 已有级联 UI，本叶校正语义/校验/文案，禁止另造一套 |

## 必须改掉的现状（对照人审红框）

`PolicyAnalysisConfigPage.vue` 已有集群→产业下拉，但：

- 评审横幅仍写「产业可篮/页选」；`generateHint` / 空态仍把「从对比篮勾选 / 去产业查询」当主路径。
- `scopeReady` 绑 `toPolicyGraphVid`：L0 必须是图上链码（`INB`≥6 位 → `chain:INB…`）。**保留这条 Java 铁律**（总控 §0 #8），但 L0 **选项来源**必须是 map 的 `cluster.l0`，禁止用 ODS 短码 / 中文名 / `CL-*` 当选项值。
- 未选 L0 时出现「去产业查询」主按钮——本叶改为 demo 同款校验文案（尚未选择分析对象 / 请先选择集群 / 请选择产业），**去掉「必须入篮才能分析」**。篮带入仍显示「来自对比篮 · 产业」Tag。

## 区块清单（本叶）

1. 对象类型 Radio：产业 XOR 技术领域（已有，保持）。
2. 产业：集群* → 该集群 L0*（恰好 1 个）；无映射诚实错误、不可提交。
3. 技术领域：页内多选、不进篮（已有，保持；无数诚实空）。
4. 开始分析：切条件不自动 create（W4）；无集群/无 L0/无映射/`toPolicyGraphVid` 空 → disabled。
5. 三路由共用本页，禁止只改时序一页。

## 验收

- 不经对比篮：打开 `/policy/overview` → 选集群 → 选该 map 下 L0 → VID 形成 `chain:INB…` →「开始分析」可点（其余时序三维仍须全开）。
- `/policy/analysis`、`/policy/recommendation` 同一套级联。
- 对比篮仍可预填，但空篮也能页内直选。
- `npx vue-tsc --build` 零 error（必须 `--build`，禁止只 `--noEmit`）。
- handoff：`agent-delivery/agent-handoffs/政策模块-E7/LUMEN-POLICY-D-POL-01-SCOPE-L01.md` + ponytail: full + cost 四字段 + R1–R5 + W4。
- push `origin/dev`；commit `[agent:frontend-agent]`；禁止 force。

## 同仓 Convoy

`LUMEN-POLICY-D-POL-01C-DETAIL-L01` 仍占 `lumen-ui-topic`。本叶须等 DETAIL 交 handoff 并离开 `in_progress` 后再认领开工。同一会话可先交抽屉、再立刻认领本叶。

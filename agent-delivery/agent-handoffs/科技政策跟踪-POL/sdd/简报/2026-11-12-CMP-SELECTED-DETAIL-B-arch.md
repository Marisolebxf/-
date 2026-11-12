# POL-L2-DS10-CMP-SELECTED-DETAIL-FDE · B 波 · arch

- 总单：`POL-L2-DS10-CMP-SELECTED-DETAIL-FDE-L01`
- 日期：2026-11-12
- 身份：arch
- 对齐 A 波：`2026-11-12-CMP-SELECTED-DETAIL-A-product.md`

## 定档

**中档**。新增交互区块（已选列表 + 点开详情）；不增需规叶子编号以外的数据源；不退定义规程。

## 读法与调用链

| 项 | 裁定 |
|---|---|
| 对比读面 | 不变：search / `{id}/detail` / jobs（力度、优缺点） |
| 详情打开 | FE only：`ComparisonModal` → `emit('open-policy', {id,title,…})` → 全景 `openPolicyDetail` → 既有 `PolicyDetailDrawer`（内部仍走既有 detail 读面） |
| 禁止 | 浏览器直连 Python；弹窗内复制第二套详情读口；新路由页打断对比 |
| 接线修复 | 父层 `v-model:selected` 与子弹 prop 必须同名 `selected`（或显式 `:selected-policies` + `@update:selected`）；打开时把页内勾选种子进 `livePickedIds` / 已选列表 |

## 不动层

API / DATA / METRIC / gapfill / Job 白名单：本单不改。

## 会签要点（交 C）

- product：214-7 界面必见已落
- arch：中档、读口不变、抽屉复用
- data/api：知会无异议即可

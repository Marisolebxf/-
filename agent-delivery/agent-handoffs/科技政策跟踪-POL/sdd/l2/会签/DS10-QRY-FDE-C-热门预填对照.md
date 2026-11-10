# DS10-QRY-FDE · 热门 → 高级字段预填对照（短表）

- 日期：2026-11-10
- 用途：闭合 ARCH-4 / P1；实现段按本表预填，不新开热门读口
- 现状真源：展示仓 `lumen-ui-science-pc` → `src/views/policy/panorama/search/displayPolicySearchConfig.ts` → `DISPLAY_HOT_TAGS`
- 行为真源：说明书「#### 197」197-5；监管人决策卡 **1B**

## 行为规则

| `apply` | 点一条后看见什么 |
|---|---|
| `filter` | 切到「高级检索功能」；按 `fieldKey` / `value` 预填字段库；状态「待应用」；**不**立刻打 `search`、**不**偷偷改成关键词并出结果 |
| 非 `filter`（若后续增项） | **只**把文案填入当前 Tab 的关键词输入框；**不**自动搜、**不**立刻出结果（对齐 197-3） |

预填仍落既有 FilterDSL / 高级字段库；用户点应用后再打既有 `search`。禁止前端写死命中列表充数（D18）。

## 现行 `DISPLAY_HOT_TAGS`（均为 filter）

| 展示文案 `label` | `apply` | 预填 `fieldKey` | 常量 `value` | 高级字段库落点（短） |
|---|---|---|---|---|
| 科创政策 | filter | `category` | `sci-tech` | 经 `resolveHotTagFieldValue`：线上 options key=label → 预填「科创政策」；mock 仍可落 `sci-tech`。禁止裸露英文码 |
| 人工智能 | filter | `industry` | `['人工智能']` | 按 label/key 收到 industryFields 的 option.value |
| 深圳市 | filter | `region` | `shenzhen` | 地区 = 深圳（`shenzhen`） |
| 国家级 | filter | `level` | `national` | 效力级别 = 国家级（`national`） |
| 人才政策 | filter | `category` | `talent` | 同科创：映射到当前 POLICY_TYPE_OPTIONS 的 key |

说明：现状五行全是 filter；1B 允许以后加非 filter 项。预填条件 `negate: false`（不得带 NOT）。实现改热门常量时须同步改本短表或 as-built 回写。

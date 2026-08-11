# 派单包：FE-ENT-REGION-SCOPE-G20-COUNTRY-L01

> 当前状态：`backlog`（待本派单包人工审阅；未认领、未开工）  
> 执行角色：`frontend-agent`  
> 建议监管：`human:曹丽影` 或 `human:孔东`，派发时由前端团队确认  
> 仓库：`lumen-ui-topic`（正式派发后目标分支 `dev`）  
> 强度：`ponytail full`  
> 性质：实现类 `feature`，`cicd: required`

## 1. 任务目标

在既有 `region-scopes` 四根树和全国多级 path 接线基础上，补齐 G20 国家/城市节点的前端取码与查询接线：

1. Cascader 保留后端节点上的 `bind_admin_code`、`bind_country_code`、`bind_city_code`；
2. 将一次或多次区位选择统一拆为 `region_ids[]`、`country_codes[]`、`city_codes[]`；
3. 重点企业分析发送三数组；招引推荐把同一拆分结果放入 Python 已支持的区位入参；
4. 国内高筛 `/meta/regions` 保持原样，不混入全球/G20 运营树。

本单是 `FE-ENT-META-DICT-SCENE-WIRE` 的增量，不重复实现 chains、tags、场景裁剪或全国 path。

## 2. 范围与依据

- 范围基线：`bid-reference/科技信息展示系统和科技专题服务系统.md`
  - §1.1.1.2.4.2.3 企业分析；
  - §1.1.1.2.4.2.3.1 重点企业类型分析；
  - §1.1.1.2.4.2.3.6 招引企业推荐分析；
  - §1.1.1.2.4.2.3.7 培育企业推荐分析。
- 已确认业务口径：`客户决策清单跟踪表.md#Q056`。
- 地区树契约：`PY-ENT-REGION-SCOPE-G20-COUNTRY-L01.md`。
- 查询契约：`PY-ENT-KEYANALYSIS-RECOMMEND-COUNTRY-派单包.md`。
- 城市码真源：`agent-delivery/data/ddl/CITY-CODE-G20.md`。
- 前端规范：`Design.md §14`、D10 `§3.4/§5/§19`、`data-lineage-policy.md`。

本单仅调整同一企业分析叶子内的接口字段和筛选交互，不新增功能点，不触发范围 ±10% 变更。

## 3. 开工门禁与依赖

| 前置任务 | 当前用途 |
|---|---|
| `FE-ENT-META-DICT-SCENE-WIRE` | 既有 RegionSelect、四根树、全国 path；同文件集，必须先 `done` |
| `API-ENT-REGION-SCOPE-G20-COUNTRY-L01` | Java 返回 `bind_country_code` 并透传三数组 |
| `PY-ENT-KEYANALYSIS-COUNTRY-SCOPE-L01` | key-analysis 三分 OR |
| `PY-ENT-RECOMMEND-GEO-COUNTRY-L01` | recommend 区位分流与 ES 候选解析 |
| `DATA-ENT-CODE-COUNTRY-APPLY-L01` | G20 国家/城市树和编码已落库 |

Registry 依赖只登记前两项，Python/Data 由 API 单承接。全部依赖 `done`、本单转 `ready`、真人确认监管人并完成认领后才能开工。

额外 Convoy 门禁：`ENT-MOD-SEARCH-FE-WIRE-L01` 当前为 `ready`，可能触碰 search scaffold/meta bundle；本单认领前必须比较双方 `touched_files`，有重叠则串行或由同一执行人处理。

## 4. 当前代码基线与缺口

| 位置 | 当前行为 | 本单缺口 |
|---|---|---|
| `src/api/enterprise/types/search.ts` | `EntRegionScopeItem` 有 admin/city bind | 缺 `bind_country_code` |
| `src/components/search/regionOptions.ts` | 转换后只留 value/label/children | 丢失 node_kind 与三类 bind 元数据 |
| `src/components/search/RegionSelect.vue` | `RegionValue` 固定 level/scope/district 三段 | G20/全国树为可变深度，无法可靠按节点 bind 取码 |
| `src/stores/entRegionScopes.ts` | session cache v1 | 需 bump，防旧节点结构污染 |
| `src/utils/keyAnalysisParams.ts` | 只生成 `region_id`/`region_level` | 缺三数组和国家/海外城市分流 |
| `src/composables/useRecruit.ts` | 招引仅把单个 `draft.fourth` 放入 `geographicSources` | 缺与 RegionSelect 同源的三分取码、混选和去重 |
| `src/components/enterprise/recruit/recruitMeta.ts` | 地域选项为深圳/长三角/京津冀/大湾区硬编码文案 | 未消费 `region-scopes` 权威树 |
| `src/mock/enterprise/topicApi.ts` | global 分支仍是旧城市样例，缺三类 bind | 与 L04/L05 国家→城市树不一致 |

`FE-ENT-META-DICT-SCENE-WIRE-派单包.md` 中“全球 = G20 主要科创城市”的旧说明已被本单依据的 `PY-ENT-REGION-SCOPE-G20-COUNTRY-L01.md` 覆盖：现行结构为“全球 → G20 国家 → 国家下热门城市”。实现时不得按旧句回退为城市平铺。

## 5. 冻结契约

### 5.1 节点字段

`POST /enterprise/topic/v1/search/meta/region-scopes` 的每个节点可能包含：

```json
{
  "scope_code": "g20-c-jpn-tokyo",
  "node_kind": "city",
  "bind_admin_code": null,
  "bind_country_code": "JPN",
  "bind_city_code": "JPTYO",
  "children": []
}
```

Cascader 的 `value` 可继续使用 `scope_code` 做稳定路径键，但筛选参数必须取 bind 字段，禁止把 `scope_code` 当查询码。

### 5.2 三分取码规则

| 选中对象 | 取值 | 输出字段 |
|---|---|---|
| 国内省/市/区叶 | `bind_admin_code` | `region_ids[]` |
| 全国热门城市 | `bind_admin_code` | `region_ids[]` |
| G20 中国城市 | `bind_admin_code` | `region_ids[]` |
| G20 国家节点 | `bind_country_code`（ISO alpha-3） | `country_codes[]` |
| G20 海外城市节点 | `bind_city_code`（UN/LOCODE 五位紧凑码） | `city_codes[]` |
| `global` / `global-all` | 后代国家节点的有效 `bind_country_code` 去重合集 | `country_codes[]` |

约束：

- 选国家只提交国家 alpha-3，禁止展开为样例城市并集；
- 中国城市不得提交历史 `CN-*` 的 `bind_city_code`，只走 `bind_admin_code`；
- `JPN`、`JPTYO` 不得进入 `region_ids[]`；
- 混选为三分 OR；各数组内部去重并保持稳定顺序；
- 缺少应有 bind 的可选节点不得静默回退到 `scope_code`，应忽略并记录可观测事件，或按既有错误态提示。

### 5.3 查询接线

重点企业分析公共请求：

```json
{
  "region_ids": ["440300"],
  "country_codes": ["JPN"],
  "city_codes": ["USNYC"],
  "chain_codes": [],
  "tag_codes": [],
  "base_tag": "key_enterprise"
}
```

招引推荐 `selectionMode=filter`：

```json
{
  "filters": {
    "geographicSources": ["440300", "JPN", "USNYC"]
  }
}
```

如 API 联调最终采用结构化数组，前端仍须复用同一三分取码结果，禁止再写第二套正则分类逻辑。

## 6. 实现要求

1. 扩展节点类型，使转换后的 Cascader 节点保留原始 `scope_code`、`node_kind` 和三类 bind；
2. `RegionValue` 支持完整可变深度 `path` 或等价选中节点信息，不再假设最多三段；
3. 建一个可独立测试的统一取码纯函数，供 key-analysis 和 recruit 共用；
4. 选择国家父节点时立即按该节点取码，不受 `children` 是否存在影响；
5. `global/global-all` 的国家展开只遍历权威树，不读取本地 G20 硬编码列表；
6. `ent.regionScopes.cascader.v1` 升版；缓存数据结构与当前类型一致；
7. 招引地域选项改为消费 `region-scopes` 或由同一 resolver 生成，禁止继续把 `recruitMeta.ts` 的硬编码列表作为生产真源；
8. Mock 的 global 分支同步为国家→城市形态并补三类 bind，保证 Mock/真实接口同契约；
9. 保留 `/meta/regions` 国内高筛逻辑；不改 Java/Python，不直连 ES/Python；
10. 复用 Arco Cascader，覆盖 loading/empty/error/disabled、键盘选择、焦点和可访问名称；
11. 复用既有 observability 工具记录加载失败、缺 bind、选择变化和请求失败，不新增日志依赖。

## 7. 建议触达文件

- `src/api/enterprise/types/search.ts`
- `src/api/enterprise/types/keyAnalysis.ts`
- `src/api/enterprise/types/recruit.ts`
- `src/components/search/regionOptions.ts`
- `src/components/search/RegionSelect.vue`
- `src/stores/entRegionScopes.ts`
- `src/utils/keyAnalysisParams.ts`
- `src/composables/useKeyEnterpriseAnalysis.ts`
- `src/composables/useRecruit.ts`
- `src/components/enterprise/recruit/RecruitFilterPanel.vue`
- `src/components/enterprise/recruit/recruitMeta.ts`
- `src/fixtures/enterprise/keyAnalysisHelpers.ts`
- `src/mock/enterprise/topicApi.ts`
- 对应最小单测文件

若实际代码已有可复用 helper，以现有模式为准；不得为本单新建第三套地区组件。

## 8. 验收用例

| 场景 | 期望 |
|---|---|
| 深圳市 | `region_ids=["440300"]` |
| 南山区 | `region_ids=["440305"]` |
| 日本国家节点 | `country_codes=["JPN"]`，无 city 展开 |
| 东京 | `city_codes=["JPTYO"]` |
| G20 中国城市 | 只进 `region_ids[]` |
| global/global-all | 展开全部有效国家 alpha-3，去重 |
| 深圳 + 日本 + 东京 | 三数组分别有值，语义 OR |
| 节点缺 bind | 不发送 `scope_code`；有可观测记录/明确错误行为 |
| 清空/重置 | 恢复业务默认，不残留旧三数组 |
| 高筛企业所属地区 | 仍只使用 `/meta/regions` 国内国标树 |
| 缓存已有 v1 | 不读取旧结构，重新拉取权威树 |
| 键盘操作 | 可展开、选择、关闭，焦点和选中态可识别 |

## 9. DoD

1. Registry 中的 8 条 `definition_of_done` 全部满足；
2. 单测覆盖 §8，关键 mapper 不依赖页面组件即可测试；
3. `lint`、`typecheck`、`test`、`build` 全过；
4. CI 绿，K8s dev rollout 成功；
5. 联调证据至少包含一组国内、国家、海外城市和混选请求；
6. handoff：`agent-handoffs/企业战略分析-ENT/FE-ENT-REGION-SCOPE-G20-COUNTRY-L01.md`；
7. handoff 附 `Design.md §14`、D10 §3.4/§19、架构 D1–D10 对照，及 `ponytail`、cost 四字段。

## 10. 不做

- 不改 Python、Java、ES mapping 或 DIM 数据；
- 不把 G20 样例城市扩大成全球完整城市库；
- 不改高筛 `/meta/regions`；
- 不新增地区业务口径或替甲方拍板；
- 不在前端实现 OR 查询、ES DSL、推荐算法；
- 不硬编码 G20 国家/城市为生产真源。

## 11. 待审派单话术

```text
/goal FE-ENT-REGION-SCOPE-G20-COUNTRY-L01
强度：ponytail full
仓：lumen-ui-topic；目标分支 dev
监管：待前端团队确认（建议 human:曹丽影 或 human:孔东）
前置：FE-ENT-META-DICT-SCENE-WIRE + API-ENT-REGION-SCOPE-G20-COUNTRY-L01 均 done
目标：RegionSelect 保留三类 bind，按国家/海外城市/国内行政码三分取码，并接入 key-analysis 与招引推荐
硬边界：前端只调 Java；高筛 /meta/regions 不动；scope_code 不得作为筛码；不在前端写 ES/算法
必读：本派单包、PY-ENT-REGION-SCOPE-G20-COUNTRY-L01.md、CITY-CODE-G20.md、Design.md §14、D10 §3.4/§5/§19
Handoff：agent-handoffs/企业战略分析-ENT/FE-ENT-REGION-SCOPE-G20-COUNTRY-L01.md
```

> 本文件经用户审阅后才能正式派发；审阅前不得认领、编码或推送。

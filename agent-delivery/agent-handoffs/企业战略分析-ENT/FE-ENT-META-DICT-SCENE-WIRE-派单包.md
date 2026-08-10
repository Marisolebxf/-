# 派单包：FE-ENT-META-DICT-SCENE-WIRE

- **派单方**：`human:徐滕强`（2026-08-10）
- **监管人 / 认领人**：`human:曹丽影`（`supervised_by` + `claimed_by`）
- **执行**：`human:曹丽影`（前端实现；可辅以 `frontend-agent`）
- **仓**：`lumen-ui-topic`（push `origin/dev`）
- **性质**：实现类（`cicd: required`）
- **强度**：`ponytail full`
- **Java**：**本单不改**（门面已透传；见 §0）
- **合并**：吸收原草稿 `FE-ENT-REGION-SCOPES-PATH-FIX-派单草稿.md`（全国多级 path）

> **入库**：本机 Cursor 未挂载 `task-registry` MCP，需 coordinator `task-create` 后按下列人写入认领字段。  
> `supervised_by` / `claimed_by` = `human:曹丽影`；建议直接 `claimed`（或 `ready` 由曹认领）。依赖：Python expand_national + `chains.scope=future` 已部署。

---

## 0. Java 是否涉及？

| 项 | 结论 |
|----|------|
| 新接口 / 新 Controller | ❌ 不需要 |
| `/meta/chains` 增加 `scope` | ✅ Request DTO 已有 `scope` 透传（`all` \| `future`） |
| `/meta/region-scopes` 的 `expand_national` | ✅ 已可选透传；默认由 Python=true |
| `/meta/tags` / `filters` / `enterprise-scales` 等 | ✅ 早已透传 |

前端只调 Java：`POST {gateway}/enterprise/topic/v1/search/meta/**`（经 nginx 时浏览器可能带 `/api` 前缀，进网关前剥掉）。**禁止直连 Python `/internal/*`。**

若联调环境 Java 镜像偏旧、还没有 `scope` 字段透传，那是**部署回灌**，不是本单开发范围。

---

## 1. 目标（一句话）

把「码表怎么取 + 八大产业链 + 资质/规模标签 + 运营地域按场景裁剪 + 全国国标多级 path」在 `lumen-ui-topic` 一次接完，避免零散发版。

---

## 2. 码表速查（怎么取）

网关前缀：`/enterprise` · 服务内：`/topic/v1/search/meta/**`

| 场景 | 调哪个 | Body | 取字段 | 备注 |
|------|--------|------|--------|------|
| 运营地域级联（结果区 / 重点分析 RegionSelect） | `…/meta/region-scopes` | `{"mode":"tree","include_members":true}` | `data.items[]` | 全国下默认挂国标省→市→区；可选 `expand_national` |
| 高筛行政区划 | `…/meta/regions` | `{"mode":"tree"}` 或 children | `data.items[]` | **仅国内国标**；勿与 region-scopes 混用 |
| 产业链全量 | `…/meta/chains` | `{}` 或 `{"keyword":"…"}` | `items[].code/name` | 高筛 / 需全量时 |
| **八大未来产业** | `…/meta/chains` | `{"scope":"future"}` | 同上，固定 8 条 | **只认 `future`**，无别名 |
| 资质标签（高企/上市/专精特新…） | `…/meta/tags` | `{"category":"qualification"}` 或 `{}` | `items[].tag_code/name` | 入参一般用 `tag_code` → `tags_flat` |
| 小微（规模四档） | `…/meta/enterprise-scales` | `{}` | `items` + `is_above_scale` | 小型/微型；规上可叠加 |
| 小微（标签码，若 UI 当标签勾选） | `…/meta/tags` | `{"category":"scale"}` | `sme` 等 | 与规模四档**勿混为同一控件语义** |
| 工商企业类型 | `…/meta/company-types` | `{}` | 有限责任公司… | **不是**高企/上市 |
| 上市状态 | `…/meta/filters` | `{}` | `listing_statuses` | `上市/未上市/退市` |
| 高筛字段目录 | `…/meta/query-tree-schema` | `{}` | `fields[].value_source` | 再按指引调上表 |

配套契约长文（可同步补 `scope=future`）：  
`agent-handoffs/企业战略分析-ENT/API-ENT-META-DICT-FRONTEND.md`

### 2.1 `scope=future` 八大（顺序固定）

1. 集成电路 `IC001`  
2. 生物医药 `BIO01`  
3. 人工智能 `AI001`  
4. 新能源 `NEW_ENERGY`  
5. 低空经济 `LOW_ALTITUDE`  
6. 量子信息 `QUANTUM`  
7. 海洋经济 `OCEAN`（库中可能是 `COM01` 等实码，展示名统一「海洋经济」）  
8. 智能机器人 `ROBOT`（库中可能是 `ROB01`）

**页面约定（本单执行）**

| 页面 | chains 调用 |
|------|-------------|
| 深圳企业现状产业链下拉 | **必须** `{"scope":"future"}` |
| 重点企业分析产业链多选 | 默认 `future`（若产品要全量再改；勿写死本地八大） |
| 高筛 industry_chain / industry_chain_code | `all`（不传或 `scope` 省略） |

### 2.2 `/meta/tags` 示例形态（契约种子）

```json
{
  "code": 0,
  "data": {
    "items": [
      {"tag_code": "high_tech", "tag_name": "高新技术企业", "tag_category": "qualification", "tag_level": "national"},
      {"tag_code": "little_giant", "tag_name": "专精特新", "tag_category": "qualification", "tag_level": "national"},
      {"tag_code": "little_giant_pro", "tag_name": "小巨人", "tag_category": "qualification", "tag_level": "national"},
      {"tag_code": "gazelle", "tag_name": "瞪羚企业", "tag_category": "qualification", "tag_level": "national"},
      {"tag_code": "unicorn", "tag_name": "独角兽企业", "tag_category": "qualification", "tag_level": "national"},
      {"tag_code": "listed", "tag_name": "上市企业", "tag_category": "qualification", "tag_level": null},
      {"tag_code": "sme", "tag_name": "小微企业", "tag_category": "scale", "tag_level": null},
      {"tag_code": "sme_tech", "tag_name": "科技型中小企业", "tag_category": "qualification", "tag_level": null}
    ]
  }
}
```

「企业类型 = 高企 / 上市 / …」→ 用 **tags（qualification）**，不要用 `company-types`。

---

## 3. 地区：两套码表 + 场景删减（前端裁剪）

### 3.1 职责（勿混）

| 用途 | 接口 | 树内容 |
|------|------|--------|
| 结果区 / 重点分析 Cascader | `region-scopes` | 全球 · 全国 · 区域 · 全国热门科创城市（+ 深圳区县）；**全国下**为国标省→市→区 |
| 高筛「企业所属地区」 | `regions` | 仅国内省市区 |

- 全球 = G20 **主要科创城市**（不是国家列表）  
- 区域 = 京津冀 / 长三角 / 大湾区等运营包  
- **不要**把京津冀等写入高筛 `code_region`

一次拉全树，**按场景在前端删减根节点**（不要求后端再加 exclude API）。

### 3.2 场景删减矩阵（团队临时默认 · 本单按此做）

根节点 `scope_code` / Cascader 一级 value 以接口为准，常见：`global` / `national` / `regional` / `hot-city`（以实现返回为准）。

| 场景 | 保留 | 删除 / 隐藏 | 默认选中建议 |
|------|------|-------------|--------------|
| **查企业 · 结果区** RegionSelect | 四根全开 | — | 产品现状默认（常为热门科创/深圳） |
| **重点企业分析** | 四根全开 | — | 可与结果区一致；须支持全国→省→市→区 |
| **深圳企业现状**（若页内有地域控件） | 仅 `hot-city` → `shenzhen` → 区县 | 删 `global` / `national` / `regional`；热门下非深圳城市可删 | 深圳 / 全部区县 |

实现建议：

- `filterRegionCascaderByScene(tree, scene)` 纯前端过滤  
- `RegionSelect` 增加 `allowedRootCodes?: string[]` 或直接注入已过滤的 `cascaderOptions`  
- **不要**为删减再打后端

若产品改矩阵，只改常量表，不改接口。

### 3.3 全国多级 path（原 PATH-FIX）

后端「全国」已挂国标码（`node_kind=admin|district`，`scope_code`=6 位）。前端须：

1. Cascader 支持完整 `path`（≥4 段：`national / 省 / 市 / 区`）反显  
2. `regionValueToKeyAnalysisParams`（及同类 refine）把叶国标码映射为 `region_id` + `region_level`  
3. `ent.regionScopes.cascader.v1` **cache key bump**（如 `v2`），避免长期锁死旧 `china-all`  
4. mock `region-scopes` 全国样例与线上一致（可选，随本单）

`RegionValue` 仅 `{level,scope,district}` 不够时，扩展 `path?: string[]`（或等价），高筛 `RegionTreeSelect` **不在本单**。

---

## 4. 建议触达文件（按仓现状核对）

- `src/stores/entRegionScopes.ts` · `entMetaChains`（或等价）  
- `src/components/search/RegionSelect.vue` · `regionOptions.ts`  
- `src/utils/keyAnalysisParams.ts`  
- `src/views/enterprise/EnterpriseSzStatus.vue` · `useSzStatusAnalysis.ts`  
- `src/composables/useKeyEnterpriseAnalysis.ts` · `TypeRegionPanel.vue`  
- `src/api/enterprise/types/search.ts`（`scope?` / `expand_national?` 类型）  
- mock：`src/mock/enterprise/topicApi.ts`

---

## 5. DoD

1. 深圳现状产业链下拉请求带 `scope=future`，展示恰为八大规范名（顺序一致）  
2. 高企/上市等类型筛选用 `/meta/tags`（或已有 store），**未**误用 `company-types`  
3. 结果区 / 重点分析：region-scopes 四根可用；全国可选到区且反显正确；入参 `region_id` 正确  
4. 场景删减矩阵落地（至少：深圳现状裁剪；查企业/重点分析全开）  
5. region-scopes 缓存 key 已 bump  
6. 不直连 Python；不改 Java/Python 契约真源  
7. handoff：`agent-handoffs/企业战略分析-ENT/FE-ENT-META-DICT-SCENE-WIRE.md`  
8. push `origin/dev`；冒烟截图或步骤写入 handoff  

---

## 6. 不做

- 改 Java / Python 契约真源、新建第三套地区码表  
- 高筛 `/meta/regions` 大改  
- 后端 `exclude_scopes` 场景裁剪 API  
- demo-ui 仓改动  

---

## 7. 建议 registry 字段

| 字段 | 值 |
|------|-----|
| id | `FE-ENT-META-DICT-SCENE-WIRE` |
| title | 企业码表场景接线（八大 chains + tags + region-scopes 场景裁剪与全国 path） |
| task_type | `feature` |
| supervised_by | `human:曹丽影` |
| claimed_by | `human:曹丽影` |
| claim_type | `coordinator_dispatch`（或 pull，认领后写入） |
| agent | `frontend-agent`（辅；主执行人为曹丽影） |
| repo | `lumen-ui-topic` |
| epic | `E-ENT-SCRUM-PDR` |
| priority | `P1` |
| delivery_phase | `implementation` |
| depends_on | 联调环境已含 Python expand_national + chains.scope=future（无 registry 叶则 note 写明） |
| cicd | `required` |

---

## 8. 派单话术

```
/goal FE-ENT-META-DICT-SCENE-WIRE
强度：ponytail full
仓：lumen-ui-topic · push origin/dev
监管：human:曹丽影
认领：human:曹丽影
范围：码表接线（chains scope=future、tags 资质、region-scopes 场景裁剪 + 全国 path）
不做：改 Java/Python；高筛 regions；后端场景裁剪 API
契约：派单包 FE-ENT-META-DICT-SCENE-WIRE-派单包.md
架构铁律：前端→Java→Python；Design.md + D10；勿硬编码八大/地区树为权威
```

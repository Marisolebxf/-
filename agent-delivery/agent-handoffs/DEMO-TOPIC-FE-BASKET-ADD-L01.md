# DEMO-TOPIC-FE-BASKET-ADD-L01 · demo 对比篮·筛内新增弹窗智能检索（对齐 lumen-ui-topic）

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `human:孔东` |
| supervised_by | `human:孔东` |
| claim_type | `pull` |
| 说明 | 用户当面开工；demo 无接口，检索全走 mock |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 复用现有 compareBasket store + mock 名单；未新加依赖；未跳过 D8 交互对齐 |

## 修改内容

- 新增 `CompareBasketAddModal`：关键词 + 列表 + 分页；加入/移出走现有篮 store，关窗后列表当帧同步
- 新增 `compareBasketAddSearch`：企业 `ENTERPRISE_LIST` / 产业 `INDUSTRY_SEARCH_*` / 服务机构 `SERVICE_ORG_SEARCH_RECORDS` 纯 mock 检索
- 企业 / 产业 / 服务机构三 Tab：筛栏「重置」后增「新增」；空篮 CTA「去××查询」改为「新增」，同一弹窗，不跳转查询页
- 区域 Tab 仍为开发中空页，本单未接
- selfcheck：`node src/app/pages/enterprise/compareBasketAddSearch.selfcheck.mjs` 通过

## 测试结果

- [x] selfcheck ok
- [ ] 浏览器：企业空篮/有内容筛栏「新增」弹窗加删同步（待监管人本地 `pnpm dev` 点验）
- [ ] 产业 / 服务机构同上

## 遗留风险

- demo 智能检索为本地名称过滤，非 lumen 真实 `entSearchSmart` / `industrySearch` / `svcSearchOrgs`；交互对齐，数据深度不对齐生产
- demo-ui-topic `04909b9` 已推 `origin/dev`；孔东点测通过并签收 done

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 调用链 / D12 | ✅ demo 仓不调 lumen/demo 后端；仅 mock |
| D8 Design | ✅ Arco Modal/Table/Input，次操作 text 按钮 |
| D9 指标 | N/A（本叶无新 KPI） |
| D10 交互 | ✅ 对齐 lumen 篮内新增弹窗 |

## 产物清单

- `repos/demo-ui-topic/src/app/pages/enterprise/CompareBasketAddModal.tsx`
- `repos/demo-ui-topic/src/app/pages/enterprise/compareBasketAddSearch.ts`
- `repos/demo-ui-topic/src/app/pages/enterprise/compareBasketAddSearch.selfcheck.mjs`
- `repos/demo-ui-topic/src/app/pages/enterprise/EnterpriseCompareBasketPage.tsx`
- `repos/demo-ui-topic/src/app/pages/industry-center/IndustryCompareBasketPanel.tsx`
- `repos/demo-ui-topic/src/app/pages/service-center/ServiceOrgCompareBasketPanel.tsx`

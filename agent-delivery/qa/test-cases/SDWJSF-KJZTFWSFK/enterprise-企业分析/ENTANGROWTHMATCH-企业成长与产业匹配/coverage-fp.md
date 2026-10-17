# 企业成长与产业匹配 · 功能点覆盖（entan.growth-match）

> catalog `entan.growth-match` · 50897 · path `/entan/growth-match`  
> **用例册**：`API-企业成长与产业匹配-用例.md`（`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00249`～`00262`，共 **14** 条）  
> A 线真源：无独立 `work/Lxx.md`（`_l6-to-catalog-map.yaml`：`entan.growth-match` 不扩六级）；契约四行键由 `entan.json` + `fp-split-by-api-run/_catalog-snapshot.md` 对齐  
> 编排：`algo-lib-api-case-playbook.md` §编写细则 H  

---

## 1. endpoint → 用例

| endpoint_id | METHOD | path | 对应用例 | 备注 |
|-------------|--------|------|----------|------|
| entan.growth-match.potential | POST | /entan/v1/entan/metric/M_ENT_GROWTH_POTENTIAL/compute | API-00249～00253、00259、00260 | catalog `status=unavailable` |
| entan.growth-match.match | POST | /entan/v1/entan/metric/M_ENT_INDUSTRY_MATCH_SCORE/compute | API-00254～00258、00261、00262 | catalog `status=unavailable` |

---

## 2. 功能点 → 用例（catalog 契约行）

| 功能点键 | 规则来源 | 对应用例 | 状态 | 说明 |
|----------|----------|----------|------|------|
| catalog \| entan.growth-match.potential \| enterprise_codes \| 算法输入-enterprise_codes企业标识集合 | catalog enterprise_codes | API-00250、00251、00252、00253 | 部分覆盖 | 缺省/空集合/非法/类型；live 合法集合成功校验待 endpoint available 后补 |
| catalog \| entan.growth-match.potential \| value \| 算法输出-value成长潜力得分 | catalog value | API-00249、00260 | 契约占位 | unavailable；禁止 sample 嵌套 `value.value` 数值作通过条件 |
| catalog \| entan.growth-match.potential \| _empty \| 成长潜力无数据空态 | 契约空结果 | — | 未覆盖 | 未试调，无稳定「合法 codes 下 value 必空」构造证据 |
| catalog \| entan.growth-match.potential \| _fail \| 成长潜力计算失败 | 契约错误态 | API-00249、00250、00251、00252、00253 | 已覆盖 | 含 catalog 不可用与入参失败哨兵 |
| catalog \| entan.growth-match.match \| enterprise_codes \| 算法输入-enterprise_codes企业标识集合 | catalog enterprise_codes | API-00255、00256、00257、00258、00262 | 部分覆盖 | 含 null 单缺陷；live 合法集合待 available 后补 |
| catalog \| entan.growth-match.match \| value \| 算法输出-value产业匹配度 | catalog value | API-00254、00261 | 契约占位 | 禁止 sample 匹配度示例作通过条件 |
| catalog \| entan.growth-match.match \| _empty \| 产业匹配度无数据空态 | 契约空结果 | — | 未覆盖 | 同上 |
| catalog \| entan.growth-match.match \| _fail \| 产业匹配度计算失败 | 契约错误态 | API-00254、00255、00256、00257、00258、00262 | 已覆盖 | |

---

## 3. A 线 req_only / 未扩六级说明

| 项 | 状态 | 说明 |
|----|------|------|
| 独立 Lxx by-api 表 | 无 | `_l6-to-catalog-map` 未为 `entan.growth-match` 生成 work 行 |
| 成长潜力三维（市场扩张/利润增长/资产积累） | 无对应 HTTP 顶层字段 | catalog 样例在 `value.dimensions`；契约仅列 number 型 `value`，不发明拆分 endpoint |
| 产业匹配上游度/质心度/产业链相关性 | 无对应 HTTP 顶层字段 | 样例在 `value` 对象内；viz 字段不进 API 断言 |
| 投入产出表映射 / Q015 业务口径 | 无 catalog endpoint | catalog hint「Q015 待补」；待甲方决策与 A 线扩表后登记 req_only 反表 |
| 可视化 KPI / 报告导出 | 无 catalog endpoint | 同未扩六级策略 |

---

## 4. 统计

| 状态 | 条数 |
|------|------|
| 已覆盖 | 2（双 endpoint `_fail` 契约行） |
| 部分覆盖 | 2（双 endpoint `enterprise_codes`） |
| 契约占位 | 2（双 endpoint `value`） |
| 未覆盖 | 6（含 `_empty` 2 + req_only 口径 4 类合并登记） |

---

## 5. B 线交卷摘要

| 项 | 值 |
|----|-----|
| API 用例条数 | 14 |
| 编号 | API-00249～API-00262 |
| `_empty` 未覆盖 | 2 |
| 试调 | **未试调**（§0；金样执行期复核信封） |
| FUNC 条数 | 0 |

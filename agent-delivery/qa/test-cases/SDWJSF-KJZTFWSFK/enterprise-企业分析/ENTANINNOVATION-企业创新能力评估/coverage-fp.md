# 企业创新能力评估 · 功能点覆盖（entan.innovation）

> catalog `entan.innovation` · 50897 · path `/entan/innovation`  
> 用例册：`API-企业创新能力评估-用例.md`（API-00162～00166）  
> A 线真源：无独立 `work/Lxx.md`（`_l6-to-catalog-map.yaml`：与 L31 相邻不扩六级）；契约四行键由 `entan.json` + `L33.md` 形态对齐

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | 备注 |
|-------------|--------|------|----------|------|
| entan.innovation.rank | POST | /entan/v1/entan/metric/M_ENT_INNOVATION_INDEX/compute | API-00162～00166 | catalog `status=unavailable` |

---

## 功能点 → 用例矩阵（catalog 契约行）

| 功能点键 | 规则来源 | 对应用例编号 | 状态 | 说明 |
|----------|----------|--------------|------|------|
| catalog \| entan.innovation.rank \| enterprise_codes \| 算法输入-enterprise_codes企业编码集合 | catalog enterprise_codes | API-00162、00164、00165、00166 | 契约占位 / 入参异常 | endpoint unavailable；合法集合主路径待 available 后补 live 断言 |
| catalog \| entan.innovation.rank \| enterprises \| 算法输出-enterprises企业创新能力指数明细 | catalog enterprises | API-00162 | 契约占位 | 禁止 sample `innovation_index` 作通过条件；样例在 `value.enterprises` 不设失败条件 |
| catalog \| entan.innovation.rank \| _empty \| 创新能力指数无数据空态 | 契约空结果 | — | 未覆盖 | 未试调，无稳定「合法 codes 下 enterprises 必空」构造证据 |
| catalog \| entan.innovation.rank \| _fail \| 创新能力指数计算失败 | 契约错误态 | API-00162、00164、00165、00166 | 已覆盖 | 含 catalog 不可用与入参失败哨兵 |

---

## A 线 req_only / 未扩六级说明

| 项 | 状态 | 说明 |
|----|------|------|
| 独立 Lxx by-api 表 | 无 | `_l6-to-catalog-map` 未为 `entan.innovation` 生成 work 行 |
| 需规三准则层（创新投入/产出/可持续） | 无对应 HTTP 行 | catalog 入参仅 `enterprise_codes`；模型侧语义不发明 API 用例 |
| 数据源清洗 / 训练 / 报告导出等 | 无 catalog endpoint | 同 L33 req_only 策略：待 A 线扩表后再登记反表 |

---

## 计数

| 项 | 值 |
|----|-----|
| catalog endpoint 数 | 1 |
| API 用例数 | 5 |
| 契约 field 行（catalog 四行键） | 4 |
| 已覆盖（含契约占位） | 3 field 键（enterprise_codes、enterprises、_fail） |
| 未覆盖 | 1（_empty） |
| 编号 | API-00162～API-00166 |

# 引育推荐（异步） · 功能点覆盖（innov.recommend）

> catalog `innov.recommend` · 50897 · path `/innov/recommend`  
> 用例册：`API-引育推荐（异步）-用例.md`（API-00744～00753）  
> A 线真源：`fp-split-by-api-run/work/` **未收录** `innov.*`（`_l6-to-catalog-map.yaml`：创新监测不在本轮 60 六级）；矩阵键按 catalog `params` / `responseFields` + 契约 `_empty` / `_fail`  
> 编排：`algo-lib-api-case-playbook.md` §S1  

---

## 1. endpoint → 用例

| endpoint_id | METHOD | path | 对应用例 | 备注 |
|-------------|--------|------|----------|------|
| innov.recommend.attraction | POST | （空） | API-00744～00748 | catalog `status=unavailable` · `runtime=local_mock`；验收 **sub_type=attraction**；§0 **未试调** |
| innov.recommend.cultivation | POST | （空） | API-00749～00753 | catalog `status=unavailable` · `runtime=local_mock`；验收 **sub_type=cultivation**；§0 **未试调** |

---

## 2. 功能点 → 用例（主矩阵）

| 功能点键 | 规则来源 | 对应用例 | 状态 | 说明 |
|----------|----------|----------|------|------|
| innov.recommend \| innov.recommend.attraction \| sub_type \| 算法输入-sub_type招引子类型 | catalog sub_type | API-00744、00746、00747、00748 | 已覆盖 | REC-ATTR-01 主路径 + 缺省/非法/误挂 cultivation（00748）；空串 REC-ATTR-04 待 available 后补 |
| innov.recommend \| innov.recommend.attraction \| rankings \| 算法输出-rankings招引推荐榜 | catalog rankings | API-00744 | 契约占位 | unavailable，禁止 sample recommendation_score/企业名作通过条件 |
| innov.recommend \| innov.recommend.attraction \| _empty \| 招引推荐无榜单空态 | 契约空结果 | — | 未覆盖 | endpoint unavailable 且无稳定「合法 attraction 必空 rankings」试调证据 |
| innov.recommend \| innov.recommend.attraction \| _fail \| 招引推荐契约调用失败 | 契约错误态 | API-00744、00745、00746、00747、00748 | 已覆盖 | 含 catalog 不可用、path 空、鉴权与 sub_type 失败语义 |
| innov.recommend \| innov.recommend.cultivation \| sub_type \| 算法输入-sub_type培育子类型 | catalog sub_type | API-00749、00751、00752、00753 | 已覆盖 | REC-CULT-01 主路径 + 缺省/非法/误挂 attraction |
| innov.recommend \| innov.recommend.cultivation \| rankings \| 算法输出-rankings培育推荐榜 | catalog rankings | API-00749 | 契约占位 | unavailable，禁止 sample 瓶颈/规模字段作通过条件 |
| innov.recommend \| innov.recommend.cultivation \| _empty \| 培育推荐无榜单空态 | 契约空结果 | — | 未覆盖 | endpoint unavailable 且无稳定「合法 cultivation 必空 rankings」试调证据 |
| innov.recommend \| innov.recommend.cultivation \| _fail \| 培育推荐契约调用失败 | 契约错误态 | API-00749、00750、00751、00752、00753 | 已覆盖 | 含 catalog 不可用、鉴权与 sub_type 失败语义 |
| innov.recommend \| \| weights_q015 \| 招引权重配比语义 | 客户决策 Q015 🟡 | — | 未覆盖 | catalog summary 标注待甲方确认；无 REST 字段契约，req_only |
| innov.recommend \| \| async_task_pool \| 异步任务池单飞与复用 | 专题 I2-12/附录 E | — | 未覆盖 | 本页 path 未发布；归专题工作区，非本 API 册 |

---

## 3. 统计

| 状态 | 条数（契约 field + 哨兵） |
|------|---------------------------|
| 已覆盖 | 4（两处 `sub_type`、两处 `_fail`） |
| 契约占位 | 2（两处 `rankings`） |
| 未覆盖 | 4（`_empty`×2 + req_only×2） |

---

## 4. B 线交卷摘要

| 项 | 值 |
|----|-----|
| API 用例条数 | **10**（2 endpoint × 5） |
| 编号 | **API-00744**～**API-00753** |
| `_empty` 未覆盖 | **2** |
| 试调 | **未试调**（§0 未 curl） |
| FUNC | **0** |
| code-registry | **未改**（父控回写） |
| snapshot | `fp-split-by-api-run/_catalog-snapshot.md` 登记 2 endpoint、`unavailable`×2、`local_mock`×2 |

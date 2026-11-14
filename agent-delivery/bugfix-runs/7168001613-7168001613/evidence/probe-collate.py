# 7168001613 追加回归：COLLATE 修复后的 SQL 片段静态断言（无 DB 环境，最小可跑检查）
import sys

sys.path.insert(0, r"d:\web\gkx-lumen\repos\lumen-topic-py")
from gkx_search_service.views.enterprise_distribution import _chain_dimension_predicate

for dim in ("national", "regional", "city"):
    _, join = _chain_dimension_predicate(dim)
    assert "COLLATE utf8mb4_general_ci" in join, f"{dim} 缺少 D19 COLLATE 对齐"
    col = {"national": "province", "regional": "city", "city": "district"}[dim]
    assert f"cr.name COLLATE utf8mb4_general_ci = eb.{col}" in join, f"{dim} JOIN 目标列错"
sel, join = _chain_dimension_predicate("global")
assert "CHN" in sel and join == "", "global 单点分支被误改"
print("PASS: 3 维度列对列 JOIN 均显式 COLLATE utf8mb4_general_ci；global 单点不受影响")

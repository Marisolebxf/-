"""问 3 示例：企业名称唯一命中才得到 org_id。

本文件只说明核心逻辑。未接入写图，不读库，不加依赖。
我方菜单入口 entan/graph/ops.py 没有这段对齐，缺 partner_org_id 时直接跳过。
燕大 script/organization_relation_etl.py 的 ExactOrganizationResolver 是已实现对照：
名称在底表里只对应一个 org_id 才返回，否则返回空。本脚本不是那份代码的复制，
也不表示我方已经实现。
"""

from __future__ import annotations


def unique_org_id(name_to_ids: dict[str, set[str]], name: str) -> str | None:
    ids = name_to_ids.get(name.strip())
    if ids is None or len(ids) != 1:
        return None
    return next(iter(ids))


def _self_check() -> None:
    index = {"甲公司": {"org-1"}, "乙公司": {"org-2", "org-3"}}
    assert unique_org_id(index, "甲公司") == "org-1"
    assert unique_org_id(index, "乙公司") is None
    assert unique_org_id(index, "丙公司") is None


if __name__ == "__main__":
    _self_check()

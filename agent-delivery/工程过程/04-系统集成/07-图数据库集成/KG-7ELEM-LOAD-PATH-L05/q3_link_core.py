# 示例：服务机构上图第 3 问的核心判断。未实现。
# 不接数据库，不加依赖。不能当成 demo-algo-ent-analysis 里已经有的入口。

def link_industry_to_segment(industry_name, segments):
    """行业名只和已有环节名全等时返回 node_id。对不上返回 None，不造 VID。"""
    name = (industry_name or "").strip()
    if not name:
        return None
    hits = [s["node_id"] for s in segments if (s.get("name") or "").strip() == name and s.get("node_id")]
    if len(hits) != 1:
        return None
    return hits[0]


def phrase_served_enterprise(text):
    """从一句里取出「为X提供」的 X。返回短语，稳定企业 ID 恒为 None。"""
    raw = text or ""
    mark = "为"
    tail = "提供"
    if mark not in raw or tail not in raw:
        return None
    mid = raw.split(mark, 1)[1].split(tail, 1)[0].strip()
    if not mid:
        return None
    return {"phrase": mid, "org_id": None}


def _self_check():
    segments = [{"node_id": "N1", "name": "功率器件"}, {"node_id": "N2", "name": "功率器件"}]
    assert link_industry_to_segment("功率器件", [{"node_id": "N1", "name": "功率器件"}]) == "N1"
    assert link_industry_to_segment("功率器件", segments) is None
    assert link_industry_to_segment("封装", [{"node_id": "N1", "name": "功率器件"}]) is None
    got = phrase_served_enterprise("为华为提供检测")
    assert got == {"phrase": "华为", "org_id": None}
    assert phrase_served_enterprise("无服务对象") is None


if __name__ == "__main__":
    _self_check()

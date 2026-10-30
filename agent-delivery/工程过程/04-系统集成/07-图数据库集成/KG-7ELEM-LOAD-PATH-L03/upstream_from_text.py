"""未实现。不能当作产业链 depends_on 已经上图。

源表没有上下游边时，才需要先从正文判断两个环节名是否在同一句里。
父节点列是上下级，不是这条边。本文件不读库、不写图、不加依赖。
"""


def pair_from_sentence(sentence: str, names: list[str]) -> tuple[str, str] | None:
    """两个环节名同句，且句中有方向词，才返回一对名字。方向未判定。"""
    text = sentence or ""
    hits = [name for name in names if name and name in text]
    if len(hits) < 2:
        return None
    if "上游" in text or "下游" in text or "依赖" in text:
        return hits[0], hits[1]
    return None

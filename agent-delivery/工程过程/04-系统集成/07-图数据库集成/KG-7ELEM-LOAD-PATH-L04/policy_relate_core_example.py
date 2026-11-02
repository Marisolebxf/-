# 未实现示例。只说明：约定格式的 cite 与「没有外键时的 policy_relate」怎么分支。
# 不接数据库，不加依赖，不写 Nebula。跑本文件不能当成 M11 已上图。

def cite_pid(token: str):
    token = (token or "").strip()
    if token.startswith("上位政策:"):
        pid = token.split(":", 1)[1].strip()
        return pid or None
    return None


def relate_unimplemented(left: str, right: str) -> str:
    """政策—政策语义相似。仓库里没有这条写图。返回值只标记未实现。"""
    if not (left or "").strip() or not (right or "").strip():
        return "empty"
    return "policy_relate_unimplemented"


def branch(pedigree_token: str, this_text: str, other_text: str):
    pid = cite_pid(pedigree_token)
    if pid:
        return "cite_rule", pid
    return relate_unimplemented(this_text, other_text), None


def _check() -> None:
    assert cite_pid("上位政策:P1") == "P1"
    assert cite_pid("根据国发某某") is None
    assert branch("上位政策:P1", "甲", "乙") == ("cite_rule", "P1")
    assert branch("根据国发某某", "甲", "乙")[0] == "policy_relate_unimplemented"


if __name__ == "__main__":
    _check()

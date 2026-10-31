#!/usr/bin/env python3
"""tag_dict 三方标签种子自检：撞码 / 前缀规则 / 55 值全覆盖。stdlib only，无第三方依赖。

规则（2026-10-30 用户裁定）：
  - 字面完全一致才复用现有行；字不一样即独立标签（不做语义判断）
  - 曾获标签统一 former_ 前缀，正常标签码/名不得含「曾获」
  - 过期待复核标签统一 recheck_ 前缀
用法：python3 scripts/check_tag_dict_supplier_seed.py（在 gkx-orchestration 仓根执行）
"""
import re
import sys
from pathlib import Path

DDL = Path("agent-delivery/data/ddl")
SUPPLIER = DDL / "gkxlumenx_dwd_tag_dict_supplier_seed.sql"
ALIGN = DDL / "gkxlumenx_dwd_tag_dict_align.sql"

ROW = re.compile(r"^\s*\('([^']+)',\s*'([^']+)'", re.M)

# 三方真源 dwd_org_tech_tag.org_tag 全量 55 值（用户 2026-10-30 提供）
SUPPLIER_NAMES = [
    "GEI中国独角兽企业", "专精特新中小企业", "专精特新小巨人企业", "中国独角兽企业",
    "企业技术中心", "众创空间", "创新型中小企业", "制造业单项冠军企业",
    "国家级专精特新小巨人企业", "国家级企业技术中心", "国家级制造业单项冠军企业",
    "国家级技术创新示范企业", "国家级知识产权优势企业", "国家级知识产权示范企业",
    "国家级科技型中小企业", "国家级高新技术企业", "工程技术研究中心",
    "技术先进型服务企业", "技术创新示范企业",
    "曾获国家级专精特新小巨人企业", "曾获国家级企业技术中心", "曾获国家级制造业单项冠军企业",
    "曾获国家级科技型中小企业", "曾获国家级高新技术企业", "曾获省级专精特新中小企业",
    "曾获省级瞪羚企业", "曾获省级科技小巨人企业", "曾获瞪羚企业", "曾获胡润全球瞪羚企业",
    "民营科技企业", "独角兽企业", "省级专精特新中小企业", "省级专精特新小巨人企业",
    "省级创新型中小企业", "省级技术先进型服务企业", "省级民营科技企业", "省级瞪羚企业",
    "省级知识产权优势企业", "省级知识产权示范企业", "省级科技小巨人企业",
    "瞪羚企业", "知识产权优势企业", "知识产权示范企业", "科技企业孵化器",
    "科技型中小企业", "科技小巨人企业", "科改示范企业", "胡润全球独角兽企业",
    "胡润全球瞪羚企业", "过期待复核国家级专精特新小巨人企业",
    "过期待复核国家级制造业单项冠军企业", "过期待复核国家级技术创新示范企业",
    "隐形冠军企业", "雏鹰企业", "高新技术企业",
]

# lumen-topic-py gkx_common/dicts.py TAG_ZH 已占用的 code（静态兜底，运行时与 tag_dict 同源）
DICTS_PY_CODES = {
    "key_enterprise", "high_tech", "listed", "little_giant", "little_giant_pro",
    "specialized_new", "chain_leader", "foreign_invested", "foreign", "small_micro",
    "sme", "sme_tech", "gazelle", "unicorn", "software_top100",
    "tech_advanced_service", "honor_national", "honor_province", "honor_city",
    "honor_district", "certification",
}


def rows(path: Path) -> list[tuple[str, str]]:
    return ROW.findall(path.read_text(encoding="utf-8"))


def main() -> int:
    supplier = rows(SUPPLIER)
    align_names = {n for _, n in rows(ALIGN)}
    align_codes = {c for c, _ in rows(ALIGN)}

    # 1) 行数 = 51（55 值中字面命中现有行的复用，不新增）
    assert len(supplier) == 51, f"种子行数应为 51，实际 {len(supplier)}"

    # 2) 新种子内部 code 不重复
    codes = [c for c, _ in supplier]
    dup = sorted({c for c in codes if codes.count(c) > 1})
    assert not dup, f"新种子内部 code 重复: {dup}"

    # 3) code 不撞现有基线（align 17 行 + dicts.py 兜底；tech_advanced_service 为字面命中例外）
    clash_align = sorted(set(codes) & align_codes)
    assert not clash_align, f"code 与 align 种子撞车: {clash_align}"
    clash_dict = sorted(set(codes) & DICTS_PY_CODES - {"tech_advanced_service"})
    assert not clash_dict, f"code 与 dicts.py 兜底撞车(仅允许 tech_advanced_service): {clash_dict}"

    # 4) 复用规则：不在新种子的三方值必须字面命中 align 现有 tag_name
    supplier_names = {n for _, n in supplier}
    reused = set(SUPPLIER_NAMES) - supplier_names
    assert reused == {"高新技术企业", "瞪羚企业", "独角兽企业", "科技型中小企业"}, \
        f"复用集应恰为 4 个字面命中值，实际: {sorted(reused)}"
    assert reused <= align_names, f"复用值必须存在于 align 现有行: {sorted(reused - align_names)}"

    # 4b) tag_name 全表唯一：JOIN 键 org_tag = tag_name，新种子与现有行重名会串行
    name_clash = sorted(supplier_names & align_names)
    assert not name_clash, f"新种子 tag_name 与 align 现有行重名（JOIN 键冲突）: {name_clash}"

    # 5) 覆盖校验：55 值全覆盖，无多收
    covered = supplier_names | reused
    extra = sorted(covered - set(SUPPLIER_NAMES))
    assert not extra, f"种子出现三方 55 值之外的名字: {extra}"

    # 6) 前缀规则：曾获 ↔ former_ 双向唯一；过期待复核 ↔ recheck_；正常标签不得含「曾获」
    former_codes = {c for c in codes if c.startswith("former_")}
    former_names = {n for _, n in supplier if n.startswith("曾获")}
    assert len(former_codes) == len(former_names) == 10, \
        f"former_ 码应有 10 个/曾获名应有 10 个，实际 {len(former_codes)}/{len(former_names)}"
    for c in former_codes:
        n = dict(supplier)[c]
        assert n.startswith("曾获"), f"former_ 码 {c} 对应名不含「曾获」: {n}"
    for n in former_names:
        c = [c for c, x in supplier if x == n][0]
        assert c.startswith("former_"), f"曾获名 {n} 未用 former_ 前缀: {c}"
    bad_name = sorted(n for _, n in supplier if "曾获" in n and not n.startswith("曾获"))
    assert not bad_name, f"名称中段含「曾获」的异常标签: {bad_name}"
    other_former = sorted(c for c in codes if "former" in c and not c.startswith("former_"))
    assert not other_former, f"码内嵌 former 但非前缀: {other_former}"
    recheck_pairs = {c: n for c, n in supplier if c.startswith("recheck_")}
    assert len(recheck_pairs) == 3 and all(n.startswith("过期待复核") for n in recheck_pairs.values()), \
        f"recheck_ 前缀应恰 3 个且名以「过期待复核」开头: {recheck_pairs}"

    print(f"OK: 55 值全覆盖 = 51 新增 + 4 字面复用{sorted(reused)}；"
          f"code 零撞车；former_ 10 / recheck_ 3 前缀规则通过")
    return 0


if __name__ == "__main__":
    sys.exit(main())

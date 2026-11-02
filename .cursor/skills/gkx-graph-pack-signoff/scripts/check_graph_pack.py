"""Graph 派单包签收自检。只读。退出码 0 才是通过。不连图库，不打印口令。"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
GRAPH = ROOT / "agent-delivery" / "data" / "Graph"
PACKS = GRAPH / "入图需求和派单"
SCHEMA_NAME = "03-schema-gkx_chain.ngql"

TAGS = (
    "enterprise", "segment", "research", "paper", "patent", "project",
    "person", "institution", "policy",
)
EDGES = (
    "cooperate", "belong", "cite", "participate", "author_of", "publish",
    "policy_relate", "policy_apply_to", "depends_on", "participates",
    "research_coop", "talent_coop", "service_provide", "supply", "parent_sub",
)
FORBIDDEN_TAGS = ("technology", "tech_result", "service_institution", "chain", "talent")
ENT_FILES = (
    "README.md", "00-背景与派单说明.md", "01-企业维需求.md", "02-技术方案.md",
    "03-schema-gkx_chain.ngql", "04-环境.md", "05-回签.md", "06-GDF触发契约.md",
    "07-gapfill清单.md",
)
CHAIN_FILES = (
    "README.md", "00-派单说明.md", "01-产业链维需求.md", "05-回签.md",
    "06-GDF触发契约.md", "07-gapfill清单.md",
)
STALE = re.compile(r"data/Graph/入图(?!需求和派单)")


def read(path):
    return path.read_text(encoding="utf-8")


def need(path, failures, label):
    if not path.is_file():
        failures.append(f"缺少 {label}")
        return ""
    return read(path)


def names(text, kind):
    return re.findall(rf"CREATE\s+{kind}\s+IF\s+NOT\s+EXISTS\s+(\w+)", text, re.I)


def once(found, expected, label, failures):
    for name in expected:
        count = found.count(name)
        if count != 1:
            failures.append(f"schema {label} {name} 出现 {count} 次，应为 1")
    extra = sorted(set(found) - set(expected))
    if extra:
        failures.append(f"schema 多出 {label}：{', '.join(extra)}")


def contains(text, needle, failures, where):
    if needle not in text:
        failures.append(f"{where} 没有写明：{needle}")


def check_schema(text, failures):
    if re.search(r"\bDROP\b", text, re.I):
        failures.append("schema 含 DROP")
    if re.search(r"\bUNDIRECTED\b", text, re.I):
        failures.append("schema 含 UNDIRECTED")
    spaces = re.findall(r"CREATE\s+SPACE\s+IF\s+NOT\s+EXISTS\s+(\w+)", text, re.I)
    if spaces != ["gkx_chain"]:
        failures.append(f"CREATE SPACE 应为且只为 gkx_chain，实际 {spaces or '无'}")
    tags, edges = names(text, "TAG"), names(text, "EDGE")
    once(tags, TAGS, "TAG", failures)
    once(edges, EDGES, "EDGE", failures)
    for name in FORBIDDEN_TAGS:
        if name in tags:
            failures.append(f"schema 不应有 Tag {name}")
    part = re.search(r"CREATE\s+EDGE\s+IF\s+NOT\s+EXISTS\s+participates\s*\(([^)]*)\)", text, re.I)
    if part is None or part.group(1).strip():
        failures.append("participates 应是空属性")
    dep = re.search(r"CREATE\s+EDGE\s+IF\s+NOT\s+EXISTS\s+depends_on\s*\(([^)]*)\)", text, re.I)
    if dep is None or not all(col in dep.group(1) for col in ("dependency_type", "weight", "props")):
        failures.append("depends_on 应含 dependency_type、weight、props")


def check_enterprise(pack, failures):
    for name in ENT_FILES:
        if not (pack / name).is_file():
            failures.append(f"企业包缺少 {name}")
    note = need(pack / "00-背景与派单说明.md", failures, "企业派单说明")
    demand = need(pack / "01-企业维需求.md", failures, "企业维需求")
    for needle in ("对接文档/燕大", "不要 `DROP`", "在 `gkx_chain` 执行", "不写 `demo_gkx_chain`"):
        contains(note, needle, failures, "企业派单说明")
    for needle in ("Tag `enterprise`", "`supply`", "`parent_sub`", "enterprise_base"):
        contains(demand, needle, failures, "企业维需求")
    later = demand.split("不进第一批", 1)[-1] if "不进第一批" in demand else ""
    if "cooperate" not in later or "participates" not in later:
        failures.append("企业维需求未把 cooperate、participates 放在不进第一批")
    banned = demand.split("不要建", 1)[-1] if "不要建" in demand else ""
    for needle in ("科研机构", "技术", "人才", "INVESTS_IN", "SUBSIDIARY_OF"):
        contains(banned, needle, failures, "企业不要建")


def check_chain(pack, failures):
    for name in CHAIN_FILES:
        if not (pack / name).is_file():
            failures.append(f"产业链包缺少 {name}")
    for name in (SCHEMA_NAME, "04-环境.md", "02-技术方案.md"):
        if (pack / name).exists():
            failures.append(f"产业链包不应自带 {name}，共用部分看企业包")
    note = need(pack / "00-派单说明.md", failures, "产业链派单说明")
    demand = need(pack / "01-产业链维需求.md", failures, "产业链维需求")
    for needle in (
        "../KG-ENT-WORKPACK-v0.1/03-schema-gkx_chain.ngql",
        "../KG-ENT-WORKPACK-v0.1/04-环境.md",
        "对接文档/燕大",
        "不要 `DROP`",
        "不写 Tag `chain`",
        "不写 `depends_on`",
        "Tag `segment`",
    ):
        contains(note, needle, failures, "产业链派单说明")
    for needle in ("industry_chain_node", "segment:{node_id}", "parent_child"):
        contains(demand, needle, failures, "产业链维需求")
    later = demand.split("不进第一批", 1)[-1] if "不进第一批" in demand else ""
    if "depends_on" not in later or "participates" not in later:
        failures.append("产业链维需求未把 depends_on、participates 放在不进第一批")
    banned = demand.split("不要建", 1)[-1] if "不要建" in demand else ""
    for needle in ("科研机构", "技术", "人才", "政策", "CHILD_OF", "DOWNSTREAM_OF"):
        contains(banned, needle, failures, "产业链不要建")


def check_rules(which, failures):
    scripts = []
    if which in ("ent", "all"):
        scripts.append(GRAPH / "建图" / "企业" / "脚本" / "enterprise_rules.py")
    if which in ("chain", "all"):
        scripts.append(GRAPH / "建图" / "产业链" / "脚本" / "chain_rules.py")
    for path in scripts:
        if not path.is_file():
            failures.append(f"缺少规则脚本 {path.relative_to(ROOT)}")
            continue
        ran = subprocess.run([sys.executable, str(path)], cwd=ROOT, capture_output=True, text=True)
        if ran.returncode != 0:
            failures.append(f"规则自检失败 {path.name}")


def check_stale(failures):
    roots = [
        GRAPH,
        ROOT / "agent-delivery" / "agent-handoffs",
        ROOT / "agent-delivery" / "工程过程" / "04-系统集成" / "07-图数据库集成",
    ]
    for base in roots:
        if not base.exists():
            continue
        for path in base.rglob("*.md"):
            if STALE.search(read(path)):
                failures.append(f"仍指向旧目录 data/Graph/入图/：{path.relative_to(ROOT)}")


def latest(prefix):
    found = []
    for path in PACKS.glob(f"{prefix}-WORKPACK-v*"):
        if path.is_dir():
            match = re.search(r"-v(\d+(?:\.\d+)?)$", path.name, re.I)
            if not match:
                continue
            version = tuple(int(part) for part in match.group(1).split("."))
            found.append((version, path))
    if not found:
        return None
    return max(found)[1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--task")
    args = parser.parse_args()
    task = (args.task or "").upper()
    if task.startswith("KG-ENT-GRAPH"):
        which = "ent"
    elif task.startswith("KG-CHAIN-GRAPH"):
        which = "chain"
    elif task:
        sys.exit("task 需为 KG-ENT-GRAPH-LOAD-* 或 KG-CHAIN-GRAPH-LOAD-*")
    else:
        which = "all"
    failures = []
    schema_pack = latest("KG-ENT")
    if schema_pack is None:
        failures.append("没有企业派单包")
        schema = ""
    else:
        schema = need(schema_pack / SCHEMA_NAME, failures, "企业 schema")
    if schema:
        check_schema(schema, failures)
    if which in ("ent", "all") and schema_pack:
        check_enterprise(schema_pack, failures)
    if which in ("chain", "all"):
        chain = latest("KG-CHAIN")
        if chain is None:
            failures.append("没有产业链派单包")
        else:
            check_chain(chain, failures)
    check_rules(which, failures)
    if which == "all":
        check_stale(failures)
    print(f"检查 {which}")
    if failures:
        print("不通过")
        for item in failures:
            print(f"- {item}")
        return 1
    print("通过")
    return 0


if __name__ == "__main__":
    sys.exit(main())

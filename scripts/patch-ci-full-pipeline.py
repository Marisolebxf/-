#!/usr/bin/env python3
"""Safe .gitlab-ci.yml patches for dev default + FULL_PIPELINE."""

from pathlib import Path

REPOS = [
    "demo-algo-science",
    "demo-algo-ent-analysis",
    "demo-ui-science",
    "demo-ui-system-test",
    "demo-ui-topic",
    "demo-svc-platform",
    "lumen-svc-platform",
    "lumen-ui-science-pc",
    "lumen-ui-science-topic",
]
ROOT = Path(r"F:\gkx-lumen\repos")

WORKFLOW_OLD = """workflow:
  rules:
    - if: '$CI_COMMIT_BRANCH == "dev"'
    - when: never
"""

WORKFLOW_NEW = """# 完整流水线：CI/CD → Run pipeline → 分支 dev → 变量 FULL_PIPELINE=true
workflow:
  rules:
    - if: '$CI_COMMIT_BRANCH == "dev"'
    - when: never

"""

FULL_PIPELINE_SNIPPET = """  FULL_PIPELINE:
    value: "false"
    description: "Run pipeline 手动触发时设为 true，deploy 阶段自动执行"
"""

DEV_DEPLOY_OLD_1 = """    - if: '$CI_COMMIT_BRANCH == "dev"'
      variables: { DEPLOY_NAMESPACE: "dev" }
      when: manual
"""

DEV_DEPLOY_OLD_2 = """    - if: '$CI_COMMIT_BRANCH == "dev"'
      variables: { DEPLOY_NAMESPACE: "dev" }
      when: on_success
"""

DEV_DEPLOY_NEW = """    - if: '$CI_COMMIT_BRANCH == "dev" && $FULL_PIPELINE == "true"'
      variables: { DEPLOY_NAMESPACE: "dev" }
    - if: '$CI_COMMIT_BRANCH == "dev"'
      variables: { DEPLOY_NAMESPACE: "dev" }
      when: manual
"""


def read_text(p: Path) -> str:
    raw = p.read_bytes()
    for enc in ("utf-8", "utf-8-sig", "gbk", "cp936"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            pass
    return raw.decode("utf-8", errors="replace")


def patch(text: str) -> str:
    text = text.replace("\r\n", "\n")
    if "完整流水线" not in text:
        text = text.replace(WORKFLOW_OLD, WORKFLOW_NEW, 1)

    if "FULL_PIPELINE:" not in text:
        needle = "variables:\n"
        idx = text.find(needle)
        if idx == -1:
            raise ValueError("variables: block not found")
        insert = idx + len(needle)
        text = text[:insert] + FULL_PIPELINE_SNIPPET + "\n" + text[insert:]

    text = text.replace(
        "$CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH",
        '$CI_COMMIT_BRANCH == "dev"',
    )

    if DEV_DEPLOY_NEW not in text:
        text = text.replace(DEV_DEPLOY_OLD_1, DEV_DEPLOY_NEW)
        text = text.replace(DEV_DEPLOY_OLD_2, DEV_DEPLOY_NEW)

    # demo-ui-science build: dev only
    text = text.replace(
        '$CI_COMMIT_BRANCH == "dev" || $CI_COMMIT_BRANCH == "main"',
        '$CI_COMMIT_BRANCH == "dev"',
    )

    return text


def main() -> None:
    for name in REPOS:
        ci = ROOT / name / ".gitlab-ci.yml"
        if not ci.exists():
            print("SKIP", name)
            continue
        orig = read_text(ci)
        new = patch(orig)
        if new != orig:
            ci.write_bytes(new.replace("\r\n", "\n").encode("utf-8"))
            print("PATCHED", name)
        else:
            print("UNCHANGED", name)


if __name__ == "__main__":
    main()

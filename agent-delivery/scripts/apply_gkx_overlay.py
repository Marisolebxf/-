#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智谱项目 agent-delivery 同步到 E:\\gkx_src 后，运行本脚本恢复 gkx 专用路径配置。

用法（在 E:\\gkx_src\\agent-delivery\\scripts 下）:
  python apply_gkx_overlay.py

或从智谱项目一键同步:
  robocopy "e:\\实施\\2025\\智谱-深圳国科信\\5-实施和开发\\agent-delivery" "E:\\gkx_src\\agent-delivery" /E
  python E:\\gkx_src\\agent-delivery\\scripts\\apply_gkx_overlay.py
  python E:\\gkx_src\\agent-delivery\\scripts\\extract_feature_catalog.py
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
AD = SCRIPT_DIR.parent
DOCS = Path(r"e:/实施/2025/智谱-深圳国科信")

DEPRECATED_CATALOG = [
    AD / "acceptance-catalog" / "catalog-service-cluster.yaml",
    AD / "acceptance-catalog" / "catalog-cognitive-brain.yaml",
]


def patch_file(path: Path, replacements: list[tuple[str, str]]) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8")
    orig = text
    for old, new in replacements:
        text = text.replace(old, new)
    if text != orig:
        path.write_text(text, encoding="utf-8")
        print(f"patched: {path.name}")
        return True
    return False


def main() -> int:
    for p in DEPRECATED_CATALOG:
        if p.exists():
            p.unlink()
            print(f"removed deprecated: {p.name}")

    tr = AD / "task-registry.yaml"
    patch_file(tr, [
        (
            "system_wbs: 5-实施和开发/agent-delivery/system-wbs.yaml",
            "paths_config: agent-delivery/paths.yaml\n"
            "code_root: E:/gkx_src\n"
            "docs_root: e:/实施/2025/智谱-深圳国科信\n"
            "system_wbs: agent-delivery/system-wbs.yaml",
        ),
        ("database_design: 5-实施和开发/agent-delivery/数据库设计.md", "database_design: agent-delivery/数据库设计.md"),
        ("graph_engine: 5-实施和开发/agent-delivery/graph-engine.md", "graph_engine: agent-delivery/graph-engine.md"),
        ("local_docs: e:\\实施\\2025\\智谱-深圳国科信\n", ""),
        ("agent_reports: 5-实施和开发/agent-delivery/agent-handoffs", "agent_reports: agent-delivery/agent-handoffs"),
        ("acceptance_docs: 5-实施和开发/agent-delivery/验收文档", "acceptance_docs: agent-delivery/验收文档"),
        ("formal_docs_registry: 5-实施和开发/agent-delivery/formal-docs-registry.yaml", "formal_docs_registry: agent-delivery/formal-docs-registry.yaml"),
        ("officecli_workflow: 5-实施和开发/agent-delivery/officecli-doc-workflow.md", "officecli_workflow: agent-delivery/officecli-doc-workflow.md"),
        ("formal_dir: 5-实施和开发/详细设计/正式文件", f"formal_dir: {DOCS}/5-实施和开发/详细设计/正式文件"),
        ("doc_templates: 5-实施和开发/agent-delivery/templates", "doc_templates: agent-delivery/templates"),
        ("doc: 5-实施和开发/agent-delivery/cicd-pipeline.md", "doc: agent-delivery/cicd-pipeline.md"),
        ("doc: 5-实施和开发/agent-delivery/observability.md", "doc: agent-delivery/observability.md"),
        ("doc: 5-实施和开发/agent-delivery/graph-engine.md", "doc: agent-delivery/graph-engine.md"),
    ])

    # inject acceptance header fields if missing
    text = tr.read_text(encoding="utf-8")
    if "acceptance_policy:" not in text:
        text = text.replace(
            "acceptance_docs: agent-delivery/验收文档\n",
            "acceptance_docs: agent-delivery/验收文档\n"
            "acceptance_policy: agent-delivery/acceptance-compliance-policy.md\n"
            "acceptance_authority: agent-delivery/acceptance-authority.yaml\n"
            "acceptance_catalog: agent-delivery/acceptance-catalog/catalog-index.yaml\n",
        )
        text = text.replace(
            "formal_dir:",
            f"req_analysis_dir: {DOCS}/2-概要设计/2-1需求分析\nformal_dir:",
            1,
        )
        tr.write_text(text, encoding="utf-8")
        print("patched: task-registry.yaml (acceptance headers)")

    patch_file(AD / "system-wbs.yaml", [
        (
            "task_queue: 5-实施和开发/agent-delivery/task-registry.yaml",
            "paths_config: agent-delivery/paths.yaml\n"
            "code_root: E:/gkx_src\n"
            "docs_root: e:/实施/2025/智谱-深圳国科信\n"
            "req_analysis_dir: 2-概要设计/2-1需求分析\n"
            "task_queue: agent-delivery/task-registry.yaml",
        ),
        ("repo_map: 5-实施和开发/agent-delivery/repo-registry.yaml", "repo_map: agent-delivery/repo-registry.yaml"),
    ])

    fd = AD / "formal-docs-registry.yaml"
    text = fd.read_text(encoding="utf-8")
    if "bid_pdfs:" in text:
        text = re.sub(
            r"# 甲方验收.*?bid_pdfs:.*?\n    - .*?\n    - .*?\n",
            """# 甲方验收（2-1需求分析 功能点真源 · 不读招标 PDF）
acceptance_compliance:
  policy: agent-delivery/acceptance-compliance-policy.md
  authority: agent-delivery/acceptance-authority.yaml
  demo_registry: agent-delivery/demo-fallback-registry.yaml
  catalog_dir: agent-delivery/acceptance-catalog
  catalog_script: agent-delivery/scripts/extract_feature_catalog.py
  req_analysis_dir: 2-概要设计/2-1需求分析
  tiers: [FULL, INTEG, DEMO]
  deprecated_pdfs:
    - 1-招投标需求/五、实施方案-智能服务集群-ZP-2025-11-18.pdf
    - 1-招投标需求/五、实施方案-智慧认知大脑-ZP-2025-11-18.pdf
""",
            text,
            flags=re.DOTALL,
        )
        fd.write_text(text, encoding="utf-8")
        print("patched: formal-docs-registry.yaml")

    patch_file(AD / "repo-registry.yaml", [
        (
            "甲方验收：PDF 目录 100% 有入口",
            "甲方验收：2-1需求分析 功能点 100% 有入口",
        ),
        # gkx_demo_python 在源副本缺少 "- id:" 列表项标记，会被并入 ent_analysis
        # 造成重复键（ent_analysis.demo 被覆盖为 gkx_demo_python）。补回列表项。
        (
            "      平台 P-03 图谱引擎、E7/E1 垂向能力移植参考本仓；API 响应含 source:nebula|pg。\n"
            "    role: python_algorithm\n"
            "    demo:\n"
            "      name: gkx_demo_python",
            "      平台 P-03 图谱引擎、E7/E1 垂向能力移植参考本仓；API 响应含 source:nebula|pg。\n\n"
            "  - id: demo_python\n"
            "    role: python_algorithm\n"
            "    demo:\n"
            "      name: gkx_demo_python",
        ),
    ])

    # task-registry.yaml：YAML 列表项不能以 ** 开头（* 会被当成 alias 锚点），加引号
    patch_file(AD / "task-registry.yaml", [
        (
            "      - **OTel**：对齐 gkx_demo_python（opentelemetry-instrument + OTLP :4318）；响应头含 traceparent",
            '      - "**OTel**：对齐 gkx_demo_python（opentelemetry-instrument + OTLP :4318）；响应头含 traceparent"',
        ),
        (
            "      - **含** download-otel-agent.sh、Dockerfile JavaAgent、Deployment OTEL_* env",
            '      - "**含** download-otel-agent.sh、Dockerfile JavaAgent、Deployment OTEL_* env"',
        ),
        (
            "      - **Grafana 三联查**：抽样 traceId 在 Tempo 有完整链路、Loki 可搜到关联日志",
            '      - "**Grafana 三联查**：抽样 traceId 在 Tempo 有完整链路、Loki 可搜到关联日志"',
        ),
    ])

    extract = SCRIPT_DIR / "extract_feature_catalog.py"
    if extract.exists():
        subprocess.run([sys.executable, str(extract)], check=True)

    # DS-04 M1 anchor
    display = AD / "acceptance-catalog" / "catalog-display-7modules.yaml"
    if display.exists():
        t = display.read_text(encoding="utf-8")
        t = re.sub(
            r"(id: DS-04[\s\S]*?judgment: 不变\n  analysis:.*?\n)  tier: TBD\n  route: null\n  task_id: null",
            r"\1  tier: FULL\n  route: /innov\n  task_id: E-INNOV-M1-L08",
            t,
        )
        display.write_text(t, encoding="utf-8")
        print("patched: catalog-display-7modules.yaml#DS-04")

    print("OK apply_gkx_overlay complete")
    return 0


if __name__ == "__main__":
    sys.exit(main())

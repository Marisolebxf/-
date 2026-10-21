#!/usr/bin/env python3
"""Parent rewrite loop: if the ledger still has pending and the slot is not full, do not let the turn end."""
import csv
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path("/Users/roy/data/projects/zhipu/gkx/gkx-lumen/gkx-orchestration")
LEDGER = ROOT / "agent-delivery/qa/as-built/script-rewrite-ledger-KJZTFWXT.csv"
ARMED = ROOT / "agent-delivery/qa/as-built/.rewrite-loop-armed"
PARENT = "573eb243"


def main() -> None:
    raw = sys.stdin.read()
    try:
        data = json.loads(raw or "{}")
    except json.JSONDecodeError:
        data = {}
    if not ARMED.is_file():
        print("{}")
        return
    cid = str(data.get("conversation_id") or data.get("conversationId") or "")
    transcript = str(data.get("transcript_path") or data.get("transcriptPath") or "")
    # 只认父控对话 id。不要用正文里出现「父控」来判断，否则写手册的对话会被补派。
    ok = cid.startswith(PARENT) or f"/{PARENT}/" in transcript or transcript.endswith(f"{PARENT}.jsonl")
    if not ok:
        print("{}")
        return
    with LEDGER.open(encoding="utf-8", newline="") as f:
        counts = Counter((row.get("status") or "").strip() for row in csv.DictReader(f))
    pending = counts.get("pending", 0)
    running = counts.get("running", 0)
    if pending <= 0 or running >= 6:
        print("{}")
        return
    message = (
        f"编排表仍有 pending={pending} running={running}。"
        "禁止收尾，禁止写「无需再改表 / 说继续再派」。"
        "立刻把 running 补满到 6：优先 pending，派发前改成 running，"
        "子 agent 用 playbook「重写波 · 子 agent」原文，交卷前自己落表。"
        "本轮最后一个动作必须是派出子 agent。"
    )
    print(json.dumps({"followup_message": message}, ensure_ascii=False))


if __name__ == "__main__":
    main()

# 会后回写处置桶。规则真源 = T0X/ALGO-LIB-T0X-L01-minutes.md
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
YML = ROOT / "metrics" / "request" / "T0X" / "ALGO-LIB-T0X-L01-pre-meeting.yaml"

STAT = {
    "TOPIC-PAN-006": "原则2 链级计数，不扩05",
    "TOPIC-PAN-007": "原则2 链级计数，不映射技术链",
    "DS-04-CARRIER-RANK-002": "原则2 多维度排名",
    "DS-06-CARRIER-003": "原则2 创新价值排名",
}
NO_MODEL = {
    "DS-16-TALENT-RECRUIT-005",
    "DS-16-TALENT-RECRUIT-006",
    "DS-16-TALENT-RECRUIT-007",
    "DS-16-TALENT-RECRUIT-010",
    "DS-16-TALENT-RECRUIT-013",
    "DS-16-TALENT-RECRUIT-025",
}
TP = {134, 135, 136, 137, 138}


def main() -> None:
    lines = YML.read_text(encoding="utf-8").splitlines(keepends=True)
    out: list[str] = []
    section = ""
    row_id = ""
    req_id = ""
    seq: int | None = None
    pending_note: str | None = None
    n_fl = n_lf = 0
    for line in lines:
        if line.startswith("f_minus_l:"):
            section = "fl"
        elif line.startswith("l_minus_f:"):
            section = "lf"
        if "row_id:" in line:
            row_id = line.split(":", 1)[1].strip().strip("'\"")
        if "requirement_id:" in line:
            req_id = line.split(":", 1)[1].strip().strip("'\"")
        if line.strip().startswith("seq:"):
            seq = int(line.split(":", 1)[1].strip())
        if "处置桶:" in line and "未分拣" in line:
            if section == "fl":
                if row_id in STAT:
                    bucket, note = "① STAT", STAT[row_id]
                elif row_id in NO_MODEL:
                    bucket, note = "④ DEMO", "派单铁律不派③；不问九新假API"
                else:
                    bucket, note = "④ DEMO", "L02未覆盖；③宁可少"
                line = line.replace("未分拣", bucket)
                n_fl += 1
                pending_note = note
            elif section == "lf":
                if seq in TP:
                    bucket, note = "联调台DEMO", "仅third_party；九新消费；不当死叶；不派③"
                else:
                    bucket, note = "联调台DEMO", "原则3；不进专题/展示Sprint"
                line = line.replace("未分拣", bucket)
                n_lf += 1
                pending_note = note
            else:
                pending_note = None
            out.append(line)
            continue
        if "会中备注:" in line and line.strip().endswith("''") and pending_note:
            indent = line[: line.index("会中备注")]
            line = f"{indent}会中备注: {pending_note}\n"
            pending_note = None
        out.append(line)
    text = "".join(out)
    text = text.replace(
        "bucket_rule: 会前全部未分拣；禁止预填 ①STAT ②已有模型 ③新MODEL ④DEMO",
        "bucket_rule: 会后已分拣；真源 minutes.md；①4 ②0 ③0 ④73；L−F 22 联调台DEMO",
    )
    YML.write_text(text, encoding="utf-8")
    print(f"fl={n_fl} lf={n_lf}")
    if n_fl != 77 or n_lf != 22:
        raise SystemExit(f"count mismatch fl={n_fl} lf={n_lf}")


if __name__ == "__main__":
    main()

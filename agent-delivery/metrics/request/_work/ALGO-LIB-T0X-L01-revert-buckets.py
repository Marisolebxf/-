# -*- coding: utf-8 -*-
"""撤回提前分桶：处置桶回到未分拣。"""
from pathlib import Path

YML = Path(__file__).resolve().parents[3] / "metrics" / "request" / "T0X" / "ALGO-LIB-T0X-L01-pre-meeting.yaml"


def main() -> None:
    text = YML.read_text(encoding="utf-8")
    n_stat = text.count("处置桶: ① STAT")
    n_demo = text.count("处置桶: ④ DEMO")
    n_lf = text.count("处置桶: 联调台DEMO")
    text = text.replace("处置桶: ① STAT", "处置桶: 未分拣")
    text = text.replace("处置桶: ④ DEMO", "处置桶: 未分拣")
    text = text.replace("处置桶: 联调台DEMO", "处置桶: 未分拣")
    text = text.replace(
        "bucket_rule: 会后已分拣；真源 minutes.md；①4 ②0 ③0 ④73；L−F 22 联调台DEMO",
        "bucket_rule: 会前全部未分拣；禁止在指标未入 metrics/registry 之前预填四桶",
    )
    lines = []
    for line in text.splitlines(keepends=True):
        if "会中备注:" in line and "未分拣" not in line:
            indent = line[: line.index("会中备注")]
            line = f"{indent}会中备注: ''\n"
        lines.append(line)
    YML.write_text("".join(lines), encoding="utf-8")
    print(f"reverted stat={n_stat} demo={n_demo} lf={n_lf}")


if __name__ == "__main__":
    main()

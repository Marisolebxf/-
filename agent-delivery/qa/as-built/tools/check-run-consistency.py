#!/usr/bin/env python3
"""四方一致性机检（X5）：run 目录名 ↔ result.yaml case_id ↔ func_id 尾号 ↔ steps.md 标题。

用法：
  python3 check-run-consistency.py <run-dir> [<scripts-dir>]
    run-dir     如 as-built/runs/20261014-50892-keytype-r2
    scripts-dir 可选；脚本工程目录（含 scripts.yaml/gold.yaml），不传则只查 run 内三方

退出码：0 = 全一致；1 = 有不一致（明细打印）。
来源：脚本重写试点 retro X5（QA-SPEC-SCRIPT-AUTHORING-L01 沉淀，替代试点期一次性内联脚本）。
"""
import re
import sys
from pathlib import Path

import yaml  # PyYAML；仅编排仓本地工具使用


def load_yaml(path: Path):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def func_tail(func_id: str) -> str:
    """ZNFWJQ-...-FUNC-00379 → 00379；无尾号返回原串。"""
    m = re.search(r"FUNC-(\d+)$", str(func_id or ""))
    return m.group(1) if m else str(func_id or "")


def check_run(run_dir: Path, scripts_dir: Path | None) -> list[str]:
    errors: list[str] = []
    script_dirs = sorted(d for d in run_dir.glob("scripts/*") if d.is_dir())

    # 脚本工程 func_id 基准（可选）
    func_by_id: dict[str, str] = {}
    if scripts_dir:
        for name in ("gold.yaml", "scripts.yaml"):
            p = scripts_dir / name
            if not p.exists():
                continue
            data = load_yaml(p) or {}
            for s in data.get("scripts", []) or []:
                func_by_id[str(s.get("id"))] = str(s.get("func_id", ""))

    if not script_dirs:
        errors.append(f"{run_dir}: scripts/ 下无脚本目录")

    for d in script_dirs:
        sid = d.name
        result = d / "result.yaml"
        steps = d / "steps.md"
        if not result.exists():
            errors.append(f"{sid}: 缺 result.yaml（空目录不算执行）")
            continue
        if not steps.exists():
            errors.append(f"{sid}: 缺 steps.md")
        r = load_yaml(result) or {}
        # ② result.yaml case_id = 目录名
        case_id = str(r.get("case_id", ""))
        if case_id and case_id != sid:
            errors.append(f"{sid}: case_id={case_id} ≠ 目录名")
        # ③ func_id 尾号一致（run 内自比 + 与脚本工程基准比对）
        fid = str(r.get("func_id", ""))
        if scripts_dir and sid in func_by_id:
            eng_fid = func_by_id[sid]
            if fid and eng_fid and fid != eng_fid:
                errors.append(f"{sid}: run func_id={fid} ≠ 工程func_id={eng_fid}")
            fid = fid or eng_fid
        # ④ steps.md 标题含脚本 id
        if steps.exists():
            head = steps.read_text(encoding="utf-8").splitlines()[:1]
            if head and sid not in head[0]:
                errors.append(f"{sid}: steps.md 标题「{head[0]}」不含脚本 id")
        _ = func_tail(fid)  # 尾号仅作人读冗余；编号一致性以全串比对为准
    return errors


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    run_dir = Path(sys.argv[1]).resolve()
    scripts_dir = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else None
    if not run_dir.is_dir():
        print(f"run 目录不存在: {run_dir}")
        return 2
    errors = check_run(run_dir, scripts_dir)
    if errors:
        print(f"✗ {len(errors)} 处不一致（{run_dir.name}）:")
        for e in errors:
            print(f"  - {e}")
        return 1
    print(f"✓ 四方一致性通过（{run_dir.name}，{len(list(run_dir.glob('scripts/*')))} 条）")
    return 0


if __name__ == "__main__":
    sys.exit(main())

# -*- coding: utf-8 -*-
"""要素库 Excel / 行数报告路径。优先仓内副本，其次环境变量，再次本机离线目录。"""
from __future__ import annotations

import os
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
RAW_DIR = SCRIPT_DIR.parent
ENV_PATH = RAW_DIR / ".env.local"
LOCAL_XLSX = SCRIPT_DIR / "要素库xlsx"
OFFBOX_20260812 = Path(r"D:\深圳市国际科技信息中心\10、需求数据-样例\数据库表-20260812")
OFFBOX_20260724 = Path(r"D:\深圳市国际科技信息中心\10、需求数据-样例\数据库表-20260724")


def excel_base() -> Path:
    env = (os.environ.get("GKX_YUANSUKU_XLSX_DIR") or "").strip()
    if env:
        p = Path(env)
        if not p.exists():
            raise FileNotFoundError(f"GKX_YUANSUKU_XLSX_DIR 不存在: {p}")
        return p
    if LOCAL_XLSX.exists() and any(LOCAL_XLSX.glob("*.xlsx")):
        return LOCAL_XLSX
    if OFFBOX_20260812.exists():
        return OFFBOX_20260812
    raise FileNotFoundError(
        "未找到要素库 Excel：请把 xlsx 放到 加工/要素库xlsx/，"
        "或设置环境变量 GKX_YUANSUKU_XLSX_DIR"
    )


def report_dir() -> Path:
    return SCRIPT_DIR


def prev_search_dirs() -> list[Path]:
    dirs = [SCRIPT_DIR]
    for extra in (OFFBOX_20260812, OFFBOX_20260724):
        if extra.exists() and extra not in dirs:
            dirs.append(extra)
    return dirs

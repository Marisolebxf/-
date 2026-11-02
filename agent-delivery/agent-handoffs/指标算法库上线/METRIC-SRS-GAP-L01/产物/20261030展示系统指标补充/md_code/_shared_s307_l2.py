#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""S3-07 L2 仪器/转化族共享复算：gkx.dwd_medical_device 分类分布 + dev.dwd_patent_transfer 年度趋势。

服务 6 件薄壳：SOFTSCI_003/004/010/015、INCUB_007/008（+SOFTSCI_009 引用趋势面）。
产物：code/_snapshots/_s307_l2_shared_out.json
"""
from __future__ import annotations

import json
import sys
from collections import Counter

sys.path.insert(0, "/Users/samuel_tang/my_project/gkx-lumen/local-workspace/docs/tasks/investiage/20261030_展示系统指标补充/code")
from _gkxdb import gkx  # noqa: E402

import pymysql  # noqa: E402

OUT = "/Users/samuel_tang/my_project/gkx-lumen/local-workspace/docs/tasks/investiage/20261030_展示系统指标补充/code/_snapshots/_s307_l2_shared_out.json"

DEV = dict(
    host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
    charset="utf8mb4", connect_timeout=15, read_timeout=120, autocommit=True,
)


def main() -> None:
    out = {"generated": 20261102, "batch": "S3-07-L2"}

    # ---------- gkx.dwd_medical_device：仪器结构面 ----------
    cur = gkx()
    cur.execute("SELECT COUNT(*) FROM gkx.dwd_medical_device")
    out["gkx_medical_device_total"] = int(cur.fetchone()[0])
    # 分类分布（device_type）
    cur.execute(
        "SELECT device_type, COUNT(*) FROM gkx.dwd_medical_device "
        "GROUP BY device_type ORDER BY COUNT(*) DESC"
    )
    out["gkx_medical_device_type_dist_all"] = [
        {"device_type": r[0], "count": int(r[1])} for r in cur.fetchall()
    ]
    # 生产厂商分布 Top15（SOFTSCI_015 详情字段可用性证据）
    cur.execute(
        "SELECT company_name, COUNT(*) FROM gkx.dwd_medical_device "
        "WHERE company_name IS NOT NULL AND company_name != '' "
        "GROUP BY company_name ORDER BY COUNT(*) DESC LIMIT 15"
    )
    out["gkx_medical_device_company_top15"] = [
        {"company_name": r[0], "count": int(r[1])} for r in cur.fetchall()
    ]
    # 品牌分布 Top15
    cur.execute(
        "SELECT brand_name, COUNT(*) FROM gkx.dwd_medical_device "
        "WHERE brand_name IS NOT NULL AND brand_name != '' "
        "GROUP BY brand_name ORDER BY COUNT(*) DESC LIMIT 15"
    )
    out["gkx_medical_device_brand_top15"] = [
        {"brand_name": r[0], "count": int(r[1])} for r in cur.fetchall()
    ]
    # 运营流水四列 absence 计数（状态/机时/预约/评价）
    for col in ("device_name", "device_type", "brand_name", "company_name"):
        cur.execute(
            f"SELECT COUNT(*) FROM gkx.dwd_medical_device WHERE `{col}` IS NULL OR `{col}` = ''"
        )
        out[f"gkx_medical_device_{col}_nullcnt"] = int(cur.fetchone()[0])
    cur.close()

    # ---------- dev.dwd_patent_transfer：转化事件趋势面（SOFTSCI_009） ----------
    conn = pymysql.connect(**DEV)
    dcur = conn.cursor()
    dcur.execute(
        "SELECT YEAR(CAST(transfer_effective_date AS CHAR)), COUNT(*) "
        "FROM gkxlumenx_ods.dwd_patent_transfer "
        "GROUP BY YEAR(CAST(transfer_effective_date AS CHAR)) ORDER BY 1"
    )
    year_rows = dcur.fetchall()
    out["dev_patent_transfer_year_counts"] = {str(r[0]): int(r[1]) for r in year_rows}
    # 分类型样例（transfer_before/after 语义验证）
    dcur.execute(
        "SELECT transfer_before, transfer_after, COUNT(*) "
        "FROM gkxlumenx_ods.dwd_patent_transfer "
        "GROUP BY transfer_before, transfer_after ORDER BY 3 DESC LIMIT 8"
    )
    out["dev_patent_transfer_pair_top8"] = [
        {"before": r[0], "after": r[1], "count": int(r[2])} for r in dcur.fetchall()
    ]
    dcur.close(); conn.close()

    # Python 侧：分类大类归并（医疗器械分类代码规则：/ 前为大类）
    dist = out["gkx_medical_device_type_dist_all"]
    major = Counter()
    for row in dist:
        t = (row["device_type"] or "").strip()
        major_key = t.split("/")[0].strip() if t else "(空)"
        major[major_key] += row["count"]
    out["gkx_medical_device_major_type_dist_sorted"] = [
        {"major_type": k, "count": v} for k, v in sorted(major.items(), key=lambda x: (-x[1], x[0]))
    ]

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1, default=str)
    print("written:", OUT)
    print("total:", out["gkx_medical_device_total"])
    print("major types:", json.dumps(out["gkx_medical_device_major_type_dist_sorted"][:12], ensure_ascii=False))
    print("transfer years:", out["dev_patent_transfer_year_counts"])


if __name__ == "__main__":
    main()

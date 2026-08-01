# -*- coding: utf-8 -*-
"""One-shot live probe: gkx dwd_* vs enterprise promised tables. Read-only."""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

import pymysql
import yaml

ROOT = Path(__file__).resolve().parents[4]  # agent-delivery/
RAW = Path(__file__).resolve().parents[1]
ENV = RAW / ".env.local"
WP = ROOT / "data/GDF/派单包/企业/GDF-ENT-WORKPACK-v1/02-WaveA-贴源表清单.yaml"
OUT = Path(__file__).resolve().parent / "_live_dwd_enterprise_probe_2026-07-31.json"


def load_env(path: Path) -> dict:
    cfg = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        cfg[k.strip()] = v.strip().strip('"').strip("'")
    return cfg


def domain(n: str) -> str:
    if (
        n.startswith("dwd_org_")
        or n.startswith("dwd_special_")
        or n.startswith("dwd_research_")
        or n.startswith("dwd_bid_")
        or n.startswith("dwd_foreign_")
        or n.startswith("dwd_forg_")
        or n.startswith("dwd_company")
    ):
        return "enterprise_org"
    if (
        n.startswith("dwd_industry_")
        or "industry_chain" in n
        or n.endswith("_industry_tags")
        or "product_tags" in n
    ):
        return "industry_chain"
    if (
        n.startswith("dwd_author")
        or "paper" in n
        or "patent" in n
        or "project" in n
        or "report" in n
        or n.startswith("dwd_zh_")
        or n.startswith("dwd_en_")
        or n.startswith("dwd_global_")
    ):
        return "talent_paper_patent_project"
    if (
        n.startswith("dwd_drug")
        or n.startswith("dwd_clinical")
        or n.startswith("dwd_hycy")
        or n.startswith("dwd_crystal")
        or n.startswith("dwd_calculation")
        or n.startswith("dwd_company") is False
        and any(x in n for x in ("chem", "quantum", "medicine"))
    ):
        return "industry_topic"
    if (
        "financ" in n
        or "stock" in n
        or "market" in n
        or n.startswith("dwd_deal")
        or n.startswith("dwd_event")
        or n.startswith("dwd_job")
    ):
        return "finance_market"
    if "policy" in n or "zck" in n:
        return "policy"
    return "other"


ALIASES = {
    "dwd_org_base_info": ["dwd_org_reg_info"],
    "dwd_org_heis_info": ["dwd_org_hels_info"],
    "dwd_bid_base_out": ["dwd_org_bid_info"],
}


def main() -> None:
    cfg = load_env(ENV)
    conn = pymysql.connect(
        host=cfg["GKX_ODS_MYSQL_HOST"],
        port=int(cfg["GKX_ODS_MYSQL_PORT"]),
        user=cfg["GKX_ODS_MYSQL_USER"],
        password=cfg["GKX_ODS_MYSQL_PASSWORD"],
        database=cfg["GKX_ODS_MYSQL_DB"],
        connect_timeout=20,
        read_timeout=600,
        charset="utf8mb4",
    )
    cur = conn.cursor()
    cur.execute("SELECT VERSION()")
    version = cur.fetchone()[0]

    cur.execute(
        """
        SELECT table_name, table_rows,
               ROUND(data_length/1024/1024, 2),
               ROUND(index_length/1024/1024, 2),
               create_time, update_time, table_comment
        FROM information_schema.tables
        WHERE table_schema=%s AND table_type='BASE TABLE'
          AND table_name LIKE 'dwd\\_%%'
          AND table_name NOT LIKE '%%\\_bak\\_%%'
          AND table_name NOT LIKE '%%\\_bak'
        ORDER BY table_name
        """,
        (cfg["GKX_ODS_MYSQL_DB"],),
    )
    live = {}
    for r in cur.fetchall():
        live[r[0]] = {
            "approx_rows": int(r[1] or 0),
            "data_mb": float(r[2] or 0),
            "idx_mb": float(r[3] or 0),
            "create_time": str(r[4]) if r[4] else None,
            "update_time": str(r[5]) if r[5] else None,
            "comment": r[6] or "",
        }

    wp = yaml.safe_load(WP.read_text(encoding="utf-8"))
    promised = []
    for g in wp["groups"]:
        for t in g["tables"]:
            promised.append({**t, "group": g["id"], "group_title": g["title"]})

    need_exact = set()
    for t in promised:
        need_exact.add(t["name"])
    for a, alts in ALIASES.items():
        need_exact.add(a)
        need_exact.update(alts)
    for name in live:
        if domain(name) in ("enterprise_org", "industry_chain") or name.startswith(
            ("dwd_org_", "dwd_forg_", "dwd_bid_", "dwd_special_", "dwd_research_", "dwd_foreign_", "dwd_industry_", "dwd_company")
        ):
            need_exact.add(name)

    exact: dict[str, int | None | str] = {}
    for name in sorted(need_exact):
        cur.execute(
            """
            SELECT COUNT(*) FROM information_schema.tables
            WHERE table_schema=%s AND table_name=%s
            """,
            (cfg["GKX_ODS_MYSQL_DB"], name),
        )
        if cur.fetchone()[0] == 0:
            exact[name] = None
            continue
        try:
            cur.execute(f"SELECT COUNT(*) FROM `{name}`")
            exact[name] = int(cur.fetchone()[0])
        except Exception as e:  # noqa: BLE001
            exact[name] = f"ERR:{e}"

    by_dom: dict[str, dict] = defaultdict(lambda: {"tables": 0, "approx_rows": 0, "data_mb": 0.0})
    for n, v in live.items():
        d = domain(n)
        by_dom[d]["tables"] += 1
        by_dom[d]["approx_rows"] += v["approx_rows"]
        by_dom[d]["data_mb"] += v["data_mb"]

    ent_report = []
    for t in promised:
        name = t["name"]
        status = "MISSING"
        live_rows = None
        alias_hit = None
        if name in live:
            status = "PRESENT"
            live_rows = exact.get(name, live[name]["approx_rows"])
        else:
            for alt in ALIASES.get(name, []):
                if alt in live:
                    status = "ALIAS_ONLY"
                    alias_hit = alt
                    live_rows = exact.get(alt)
                    break
        ent_report.append(
            {
                "name": name,
                "cn": t.get("cn"),
                "priority": t["priority"],
                "group": t["group"],
                "status": status,
                "exact_rows": live_rows,
                "alias_hit": alias_hit,
                "approx_rows": (
                    live.get(name, {}).get("approx_rows")
                    if name in live
                    else (live.get(alias_hit, {}).get("approx_rows") if alias_hit else None)
                ),
                "data_mb": live.get(name, {}).get("data_mb") if name in live else None,
            }
        )

    promised_names = {t["name"] for t in promised}
    extra_ent = []
    for name, v in sorted(live.items()):
        if domain(name) in ("enterprise_org", "industry_chain"):
            if name not in promised_names:
                extra_ent.append(
                    {
                        "name": name,
                        "exact_rows": exact.get(name, v["approx_rows"]),
                        "approx_rows": v["approx_rows"],
                        "data_mb": v["data_mb"],
                    }
                )

    # top live tables by approx rows
    top = sorted(live.items(), key=lambda kv: -kv[1]["approx_rows"])[:40]
    top_list = [{"name": n, **v, "domain": domain(n)} for n, v in top]

    out = {
        "analyzed_at": "2026-07-31T20:10+08:00",
        "mysql_version": version,
        "source": "MySQL gkx live; approx=TABLE_ROWS; enterprise-related exact=COUNT(*)",
        "live_dwd_active_count": len(live),
        "live_dwd_approx_rows_sum": sum(v["approx_rows"] for v in live.values()),
        "live_dwd_data_mb_sum": round(sum(v["data_mb"] for v in live.values()), 2),
        "domain_approx": {k: dict(v) for k, v in sorted(by_dom.items())},
        "enterprise_promised_40": ent_report,
        "enterprise_summary": {
            "present": sum(1 for x in ent_report if x["status"] == "PRESENT"),
            "alias_only": sum(1 for x in ent_report if x["status"] == "ALIAS_ONLY"),
            "missing": sum(1 for x in ent_report if x["status"] == "MISSING"),
            "present_nonzero": sum(
                1
                for x in ent_report
                if x["status"] == "PRESENT" and isinstance(x["exact_rows"], int) and x["exact_rows"] > 0
            ),
            "present_empty": sum(
                1 for x in ent_report if x["status"] == "PRESENT" and x["exact_rows"] == 0
            ),
            "alias_nonzero": sum(
                1
                for x in ent_report
                if x["status"] == "ALIAS_ONLY" and isinstance(x["exact_rows"], int) and x["exact_rows"] > 0
            ),
            "P0_total": sum(1 for x in ent_report if x["priority"] == "P0"),
            "P0_present": sum(1 for x in ent_report if x["priority"] == "P0" and x["status"] == "PRESENT"),
            "P0_alias_only": sum(
                1 for x in ent_report if x["priority"] == "P0" and x["status"] == "ALIAS_ONLY"
            ),
            "P0_missing": sum(1 for x in ent_report if x["priority"] == "P0" and x["status"] == "MISSING"),
            "P0_usable_nonzero": sum(
                1
                for x in ent_report
                if x["priority"] == "P0"
                and x["status"] in ("PRESENT", "ALIAS_ONLY")
                and isinstance(x["exact_rows"], int)
                and x["exact_rows"] > 0
            ),
        },
        "extra_live_enterprise_like": extra_ent,
        "top40_approx": top_list,
        "key_exact_counts": {
            k: exact[k]
            for k in sorted(exact)
            if k.startswith(
                (
                    "dwd_org_",
                    "dwd_bid_",
                    "dwd_special_",
                    "dwd_forg_",
                    "dwd_research_",
                    "dwd_foreign_",
                    "dwd_industry_",
                    "dwd_company",
                )
            )
        },
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")

    print("mysql", version)
    print("live_dwd_active", out["live_dwd_active_count"], "approx_sum", out["live_dwd_approx_rows_sum"])
    print("enterprise_summary", json.dumps(out["enterprise_summary"], ensure_ascii=False, indent=2))
    print("--- promised ---")
    for x in ent_report:
        print(
            f"{x['priority']:2} {x['status']:10} rows={str(x['exact_rows']):>12}  {x['name']}"
            + (f"  via {x['alias_hit']}" if x["alias_hit"] else "")
        )
    print("--- domain ---")
    for k, v in sorted(by_dom.items(), key=lambda kv: -kv[1]["approx_rows"]):
        print(f"{k:30} tables={v['tables']:3} approx_rows={v['approx_rows']:>12} data_mb={v['data_mb']:.1f}")
    print("wrote", OUT)
    conn.close()


if __name__ == "__main__":
    main()

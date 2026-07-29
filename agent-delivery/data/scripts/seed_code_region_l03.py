# -*- coding: utf-8 -*-
"""DATA-ENT-DICT-REGION-SEED-L03

灌入 gkxlumenx_dim.code_region 全量国标省→市→区县，
校正 region_scope.bind_admin_code，扩种热门科创城市 / G20 Mock。

数据源：modood/Administrative-divisions-of-China dist/{provinces,cities,areas}.json
（已落盘 agent-delivery/data/seeds/admin-divisions/）
"""
from __future__ import annotations

import json
import os
import pathlib
from typing import Any

import pymysql

ROOT = pathlib.Path(__file__).resolve().parents[1]
SEED_DIR = ROOT / "seeds" / "admin-divisions"
DDL_DIR = ROOT / "ddl"


def mysql_conf() -> dict:
    """连接真源见 agent-handoffs/algo-mysql-connection-info.md；密码走环境变量。"""
    password = os.environ.get("INNOV_MYSQL_PASSWORD") or os.environ.get("GKX_MYSQL_PASSWORD")
    if not password:
        raise SystemExit(
            "缺少 INNOV_MYSQL_PASSWORD / GKX_MYSQL_PASSWORD（见 algo-mysql-connection-info.md）"
        )
    return dict(
        host=os.environ.get("INNOV_MYSQL_HOST", "192.168.88.43"),
        port=int(os.environ.get("INNOV_MYSQL_PORT", "3306")),
        user=os.environ.get("INNOV_MYSQL_USER", "gkxlumenx"),
        password=password,
        database=os.environ.get("INNOV_MYSQL_DIM_DB", "gkxlumenx_dim"),
        charset="utf8mb4",
        connect_timeout=15,
    )


def pad6(code: str) -> str:
    return code.ljust(6, "0")


def load_json(name: str) -> list[dict[str, Any]]:
    return json.loads((SEED_DIR / name).read_text(encoding="utf-8"))


def build_code_region_rows() -> list[tuple]:
    provinces = load_json("provinces.json")
    cities = load_json("cities.json")
    areas = load_json("areas.json")

    rows: list[tuple] = []
    # 国家根：供 region_scope national/china-all bind；Cascader 顶级同时含省
    rows.append(
        ("100000", "0", "中国", "1", "中华人民共和国", None, None, None, None, None)
    )

    prov_name: dict[str, str] = {}
    for p in provinces:
        code = pad6(p["code"])
        name = p["name"]
        prov_name[p["code"]] = name
        rows.append((code, "0", name, "1", name, None, None, None, None, None))

    city_name: dict[str, str] = {}
    for c in cities:
        code = pad6(c["code"])
        parent = pad6(c["provinceCode"])
        name = c["name"]
        # 直辖市「市辖区/县」展示为省级名，便于 Cascader
        if name in ("市辖区", "县"):
            name = prov_name.get(c["provinceCode"], name)
        city_name[c["code"]] = name
        rows.append((code, parent, name, "2", name, None, None, None, None, None))

    skipped_dup = 0
    for a in areas:
        code = a["code"]
        parent = pad6(a["cityCode"])
        if code == parent:
            # 东莞/中山等无下辖县级：区县码与市码相同，跳过避免 PK 冲突
            skipped_dup += 1
            continue
        name = a["name"]
        full = f"{city_name.get(a['cityCode'], '')}{name}"
        rows.append((code, parent, name, "3", full, None, None, None, None, None))

    # 去重（保序）
    seen: set[str] = set()
    uniq: list[tuple] = []
    for r in rows:
        if r[0] in seen:
            continue
        seen.add(r[0])
        uniq.append(r)
    print(f"built rows={len(uniq)} skipped_area_dup={skipped_dup}")
    return uniq


def seed_code_region(cur, rows: list[tuple]) -> None:
    cur.execute("DELETE FROM code_region")
    sql = (
        "INSERT INTO code_region "
        "(code, parent, name, level, fulltitle, zipcode, lnglat, tel, area, people) "
        "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    )
    batch = 500
    for i in range(0, len(rows), batch):
        cur.executemany(sql, rows[i : i + batch])
    print(f"inserted code_region={len(rows)}")


def write_sql_artifact(rows: list[tuple]) -> pathlib.Path:
    out = DDL_DIR / "gkxlumenx_dim_code_region_seed_l03.sql"
    lines = [
        "-- DATA-ENT-DICT-REGION-SEED-L03",
        "-- gkxlumenx_dim.code_region 全量国标省→市→区县（替换 11 行样例）",
        "-- 源：modood/Administrative-divisions-of-China dist provinces/cities/areas",
        "-- 生成：agent-delivery/data/scripts/seed_code_region_l03.py",
        "",
        "DELETE FROM `gkxlumenx_dim`.`code_region`;",
        "",
        "INSERT INTO `gkxlumenx_dim`.`code_region` "
        "(`code`,`parent`,`name`,`level`,`fulltitle`,`zipcode`,`lnglat`,`tel`,`area`,`people`) VALUES",
    ]
    value_lines = []
    for code, parent, name, level, fulltitle, *_rest in rows:
        def esc(s: str | None) -> str:
            if s is None:
                return "NULL"
            return "'" + s.replace("\\", "\\\\").replace("'", "''") + "'"

        value_lines.append(
            f"({esc(code)},{esc(parent)},{esc(name)},{esc(level)},{esc(fulltitle)},NULL,NULL,NULL,NULL,NULL)"
        )
    lines.append(",\n".join(value_lines) + ";")
    lines.append("")
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {out} ({out.stat().st_size} bytes)")
    return out


def patch_region_scope(cur) -> None:
    """校正 bind + 热门/G20 Mock 扩种（对齐 Q056）。"""
    # 南京补 bind；深圳区县备注去「暂估」；大鹏仍无国标码
    patches = [
        ("nanjing", "320100", "CN-3201", "Q056 热门城市 Mock；bind 南京市"),
        ("longhua", "440309", None, "国标 440309 龙华区"),
        ("guangming", "440311", None, "国标 440311 光明区"),
        ("pingshan", "440310", None, "国标 440310 坪山区"),
        ("longgang", "440307", None, "国标 440307 龙岗区"),
        ("yantian", "440308", None, "国标 440308 盐田区"),
        ("nanshan", "440305", None, None),
        ("futian", "440304", None, None),
        ("luohu", "440303", None, None),
        ("baoan", "440306", None, None),
        ("sz-all", "440300", "CN-4403", "选「全部」时等同市本级"),
        ("dapeng", None, None, "大鹏新区非民政部县级码；过滤策略待运营确认"),
    ]
    for scope_code, admin, city, remark in patches:
        if city is None and admin is not None:
            cur.execute(
                "UPDATE region_scope SET bind_admin_code=%s, remark=COALESCE(%s, remark) WHERE scope_code=%s",
                (admin, remark, scope_code),
            )
        elif admin is None and city is None:
            cur.execute(
                "UPDATE region_scope SET bind_admin_code=NULL, bind_city_code=NULL, remark=%s WHERE scope_code=%s",
                (remark, scope_code),
            )
        else:
            cur.execute(
                "UPDATE region_scope SET bind_admin_code=%s, bind_city_code=COALESCE(%s, bind_city_code), "
                "remark=COALESCE(%s, remark) WHERE scope_code=%s",
                (admin, city, remark, scope_code),
            )

    # 热门科创城市扩种
    hot_extra = [
        ("xian", "hot-city", "西安", "scope", 2, "610100", "CN-6101", 100, "Q056 热门城市 Mock 扩种"),
        ("hefei", "hot-city", "合肥", "scope", 2, "340100", "CN-3401", 110, "Q056 热门城市 Mock 扩种"),
        ("changsha", "hot-city", "长沙", "scope", 2, "430100", "CN-4301", 120, "Q056 热门城市 Mock 扩种"),
        ("qingdao", "hot-city", "青岛", "scope", 2, "370200", "CN-3702", 130, "Q056 热门城市 Mock 扩种"),
        ("xiamen", "hot-city", "厦门", "scope", 2, "350200", "CN-3502", 140, "Q056 热门城市 Mock 扩种"),
        ("tianjin", "hot-city", "天津", "scope", 2, "120000", "CN-1200", 150, "Q056 热门城市 Mock 扩种"),
        ("chongqing", "hot-city", "重庆", "scope", 2, "500000", "CN-5000", 160, "Q056 热门城市 Mock 扩种"),
        ("wuxi", "hot-city", "无锡", "scope", 2, "320200", "CN-3202", 170, "Q056 热门城市 Mock 扩种"),
        ("ningbo", "hot-city", "宁波", "scope", 2, "330200", "CN-3302", 180, "Q056 热门城市 Mock 扩种"),
        ("dongguan", "hot-city", "东莞", "scope", 2, "441900", "CN-4419", 190, "Q056 热门城市 Mock 扩种"),
    ]
    cur.executemany(
        "INSERT INTO region_scope "
        "(scope_code,parent_code,scope_name,node_kind,level,bind_admin_code,bind_city_code,sort_order,is_active,remark) "
        "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,1,%s) "
        "ON DUPLICATE KEY UPDATE scope_name=VALUES(scope_name), parent_code=VALUES(parent_code), "
        "bind_admin_code=VALUES(bind_admin_code), bind_city_code=VALUES(bind_city_code), "
        "sort_order=VALUES(sort_order), remark=VALUES(remark), is_active=1",
        hot_extra,
    )

    # G20 扩种（补齐未覆盖成员国主要科创城市）
    g20_extra = [
        ("g20-osaka", "global-all", "大阪", "scope", 3, None, "JP-OSA", 190, "G20 Mock JP"),
        ("g20-chicago", "global-all", "芝加哥", "scope", 3, None, "US-CHI", 200, "G20 Mock US"),
        ("g20-la", "global-all", "洛杉矶", "scope", 3, None, "US-LAX", 210, "G20 Mock US"),
        ("g20-milan", "global-all", "米兰", "scope", 3, None, "IT-MIL", 220, "G20 Mock IT"),
        ("g20-rome", "global-all", "罗马", "scope", 3, None, "IT-ROM", 230, "G20 Mock IT"),
        ("g20-moscow", "global-all", "莫斯科", "scope", 3, None, "RU-MOW", 240, "G20 Mock RU"),
        ("g20-mexicocity", "global-all", "墨西哥城", "scope", 3, None, "MX-MEX", 250, "G20 Mock MX"),
        ("g20-johannesburg", "global-all", "约翰内斯堡", "scope", 3, None, "ZA-JNB", 260, "G20 Mock ZA"),
        ("g20-buenosaires", "global-all", "布宜诺斯艾利斯", "scope", 3, None, "AR-BUE", 270, "G20 Mock AR"),
        ("g20-istanbul", "global-all", "伊斯坦布尔", "scope", 3, None, "TR-IST", 280, "G20 Mock TR"),
        ("g20-jakarta", "global-all", "雅加达", "scope", 3, None, "ID-JKT", 290, "G20 Mock ID"),
        ("g20-melbourne", "global-all", "墨尔本", "scope", 3, None, "AU-MEL", 300, "G20 Mock AU"),
    ]
    cur.executemany(
        "INSERT INTO region_scope "
        "(scope_code,parent_code,scope_name,node_kind,level,bind_admin_code,bind_city_code,sort_order,is_active,remark) "
        "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,1,%s) "
        "ON DUPLICATE KEY UPDATE scope_name=VALUES(scope_name), bind_city_code=VALUES(bind_city_code), "
        "sort_order=VALUES(sort_order), remark=VALUES(remark), is_active=1",
        g20_extra,
    )

    # dim.city 扩种（热门 + G20）
    city_extra = [
        ("CN-3201", "南京", "Nanjing", "CN", "320100", 118.796900, 32.060300, 1),
        ("CN-4301", "长沙", "Changsha", "CN", "430100", 112.938800, 28.228200, 1),
        ("CN-3702", "青岛", "Qingdao", "CN", "370200", 120.382600, 36.067100, 1),
        ("CN-3502", "厦门", "Xiamen", "CN", "350200", 118.089400, 24.479800, 1),
        ("CN-1200", "天津", "Tianjin", "CN", "120000", 117.201000, 39.084200, 1),
        ("CN-5000", "重庆", "Chongqing", "CN", "500000", 106.551600, 29.563000, 1),
        ("CN-3202", "无锡", "Wuxi", "CN", "320200", 120.311900, 31.491200, 0),
        ("CN-3302", "宁波", "Ningbo", "CN", "330200", 121.544000, 29.868300, 0),
        ("CN-4419", "东莞", "Dongguan", "CN", "441900", 113.746800, 23.046600, 1),
        ("JP-OSA", "大阪", "Osaka", "JP", None, 135.502300, 34.693700, 1),
        ("US-CHI", "芝加哥", "Chicago", "US", None, -87.629800, 41.878100, 1),
        ("US-LAX", "洛杉矶", "Los Angeles", "US", None, -118.243700, 34.052200, 1),
        ("IT-MIL", "米兰", "Milan", "IT", None, 9.190000, 45.464200, 1),
        ("IT-ROM", "罗马", "Rome", "IT", None, 12.496400, 41.902800, 0),
        ("RU-MOW", "莫斯科", "Moscow", "RU", None, 37.617300, 55.755800, 1),
        ("MX-MEX", "墨西哥城", "Mexico City", "MX", None, -99.133200, 19.432600, 1),
        ("ZA-JNB", "约翰内斯堡", "Johannesburg", "ZA", None, 28.047300, -26.204100, 1),
        ("AR-BUE", "布宜诺斯艾利斯", "Buenos Aires", "AR", None, -58.381600, -34.603700, 1),
        ("TR-IST", "伊斯坦布尔", "Istanbul", "TR", None, 28.978400, 41.008200, 1),
        ("ID-JKT", "雅加达", "Jakarta", "ID", None, 106.845600, -6.208800, 1),
        ("AU-MEL", "墨尔本", "Melbourne", "AU", None, 144.963100, -37.813600, 1),
    ]
    cur.executemany(
        "INSERT INTO city "
        "(city_code,name_zh,name_en,country_code,admin_code,lng,lat,is_benchmark) "
        "VALUES (%s,%s,%s,%s,%s,%s,%s,%s) "
        "ON DUPLICATE KEY UPDATE name_zh=VALUES(name_zh), name_en=VALUES(name_en), "
        "country_code=VALUES(country_code), admin_code=VALUES(admin_code), "
        "lng=VALUES(lng), lat=VALUES(lat), is_benchmark=VALUES(is_benchmark)",
        city_extra,
    )
    print("patched region_scope + city mocks")


def validate(cur) -> dict[str, Any]:
    report: dict[str, Any] = {}
    cur.execute("SELECT COUNT(*) FROM code_region")
    report["code_region_total"] = cur.fetchone()[0]
    cur.execute("SELECT level, COUNT(*) FROM code_region GROUP BY level ORDER BY level")
    report["by_level"] = {str(k): v for k, v in cur.fetchall()}

    cur.execute("SELECT COUNT(*) FROM code_region WHERE parent='0'")
    report["top_level"] = cur.fetchone()[0]

    # 树完整性：每个非顶级节点的 parent 必须存在
    cur.execute(
        "SELECT COUNT(*) FROM code_region c "
        "LEFT JOIN code_region p ON p.code=c.parent "
        "WHERE c.parent<>'0' AND p.code IS NULL"
    )
    report["orphan_parents"] = cur.fetchone()[0]

    # 深圳区县
    cur.execute(
        "SELECT code,name FROM code_region WHERE parent='440300' ORDER BY code"
    )
    report["shenzhen_districts"] = cur.fetchall()

    expect_sz = {
        "440303",
        "440304",
        "440305",
        "440306",
        "440307",
        "440308",
        "440309",
        "440310",
        "440311",
    }
    got_sz = {r[0] for r in report["shenzhen_districts"]}
    report["shenzhen_codes_ok"] = expect_sz.issubset(got_sz)

    # bind 全部能对齐（非空 bind）
    cur.execute(
        "SELECT rs.scope_code, rs.bind_admin_code, cr.name "
        "FROM region_scope rs "
        "LEFT JOIN code_region cr ON cr.code=rs.bind_admin_code "
        "WHERE rs.bind_admin_code IS NOT NULL AND cr.code IS NULL"
    )
    report["bind_miss"] = cur.fetchall()

    cur.execute(
        "SELECT m.scope_code, m.admin_code "
        "FROM region_scope_member m "
        "LEFT JOIN code_region cr ON cr.code=m.admin_code "
        "WHERE cr.code IS NULL"
    )
    report["member_miss"] = cur.fetchall()

    cur.execute("SELECT COUNT(*) FROM region_scope")
    report["region_scope_total"] = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM region_scope WHERE parent_code='hot-city'")
    report["hot_city_count"] = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM region_scope WHERE parent_code='global-all'")
    report["g20_count"] = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM city")
    report["city_total"] = cur.fetchone()[0]

    # 样例路径
    for label, code in [("广东", "440000"), ("深圳", "440300"), ("南京", "320100")]:
        cur.execute("SELECT code,parent,name,level FROM code_region WHERE code=%s", (code,))
        report[f"sample_{label}"] = cur.fetchone()

    return report


def main() -> None:
    rows = build_code_region_rows()
    write_sql_artifact(rows)

    conn = pymysql.connect(**mysql_conf())
    try:
        cur = conn.cursor()
        seed_code_region(cur, rows)
        patch_region_scope(cur)
        conn.commit()
        report = validate(cur)
        print("VALIDATION")
        for k, v in report.items():
            print(f"  {k}: {v}")
        ok = (
            report["code_region_total"] > 3000
            and report["orphan_parents"] == 0
            and report["shenzhen_codes_ok"]
            and not report["bind_miss"]
            and not report["member_miss"]
            and report["hot_city_count"] >= 15
            and report["g20_count"] >= 25
        )
        print("PASS" if ok else "FAIL")
        if not ok:
            raise SystemExit(1)
    finally:
        conn.close()


if __name__ == "__main__":
    main()

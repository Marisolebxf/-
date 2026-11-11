# -*- coding: utf-8 -*-
"""SVC-L2-ECO S4 部署态复核：网关全端点（基础 4 + trend/district/trend-indicators/talent-panorama）+ 9 行需规对账。只读。"""
import io, json, sys, time, urllib.request

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

GW = "http://10.50.69.111:30895"
TOK = open(r"C:\Users\35197\.gkx\display-loop-token", encoding="utf-8").read().strip().splitlines()[0]
HDR = {"Authorization": f"Bearer {TOK}", "systemCode": "display", "Content-Type": "application/json"}


def call(path, params=None):
    url = GW + path
    if params:
        from urllib.parse import urlencode
        url += "?" + urlencode(params)
    req = urllib.request.Request(url, headers=HDR)
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=60) as r:
        body = json.loads(r.read().decode("utf-8"))
    return body.get("data", body), (time.time() - t0) * 1000


ok, warn, fail = [], [], []


def check(name, cond, detail=""):
    (ok if cond else fail).append(f"{name} {detail}")
    print(("PASS " if cond else "FAIL ") + name + (" | " + detail if detail else ""))


# ---- meta ----
meta, ms = call("/display/v1/service/ecology/meta")
check("meta 200", meta.get("empty") is False, f"{ms:.0f}ms")
check("meta 一致性", meta.get("consistency", {}).get("metaTotal") == 4984, str(meta.get("consistency")))
mf = meta.get("missingFilters", {})
check("562 规模/状态无源声明", "scale" in mf and "operateStatus" in mf, ",".join(mf.keys()))
check("meta yearRange", meta.get("yearRange", {}).get("min") == 1996, str(meta.get("yearRange")))

# ---- overview ----
ov, ms2 = call("/display/v1/service/ecology/overview")
kpi = ov.get("kpi", {})
check("overview total=4984", kpi.get("total") == 4984, f"{ms2:.0f}ms")
check("559 KPI 分层", kpi.get("innovationCount") == 4376 and kpi.get("incubationCount") == 608)
check("559 级别", kpi.get("nationalCount") == 445 and kpi.get("provincialCount") == 2473 and kpi.get("cityCount") == 2066)
check("559 区定位/坐标", kpi.get("districtLocatedCount") == 3075 and kpi.get("geoLocatedCount") == 3592,
      "districtLocated=全量 district_name 非空（深圳 2,851 + 其他地区 224），located+missing=total")
check("559 类型分布非空", len(ov.get("typeDist", [])) >= 10)
check("559 年度序列", ov.get("yearSeries") and ov["yearSeries"][0]["year"] == 1996)
dd = {d["district"]: d["count"] for d in ov.get("districtDist", []) if d.get("isShenzhen")}
check("560 深圳九区", dd.get("南山区") == 1118 and dd.get("宝安区") == 500, str(len(dd)) + "区")
check("565 一致性三元组", ov.get("consistency", {}).get("carriersTotal") == ov.get("consistency", {}).get("overviewTotal") == 4984)

# ---- carriers：联动筛选逐项 ----
cl, ms3 = call("/display/v1/service/ecology/carriers", {"page": 1, "pageSize": 5})
check("561 全量分页 total", cl.get("total") == 4984, f"{ms3:.0f}ms")
first = (cl.get("items") or [{}])[0]
check("561 行字段", all(k in first for k in ("carrierId", "carrierName", "carrierLevel", "districtSource", "lng")))

for name, params, expect in [
    ("562 层筛选 incubation=608", {"layer": "incubation"}, 608),
    ("562 级别筛选 国家级=445", {"level": "国家级"}, 445),
    ("562 类型筛选 重点实验室=561", {"type": "重点实验室"}, 561),
    ("562 区筛选 南山区=1118", {"district": "南山区"}, 1118),
    ("562 年度筛选 2025", {"yearFrom": 2025, "yearTo": 2025}, None),
    ("562 关键词 南方科技大学", {"keyword": "南方科技大学"}, None),
]:
    d, m = call("/display/v1/service/ecology/carriers", dict(params, pageSize=3))
    got = d.get("total")
    check(name, expect is None or got == expect, f"total={got} {m:.0f}ms")

d, _ = call("/display/v1/service/ecology/carriers", {"district": "南山区", "pageSize": 3})
geo_rows = [r for r in d.get("items", []) if r.get("lng") is not None]
check("560 南山区点位带真坐标", len(geo_rows) > 0, f"{len(geo_rows)}/3 rows geo")
if geo_rows:
    r0 = geo_rows[0]
    check("560 坐标在深圳界内", 113.7 < r0["lng"] < 114.7 and 22.4 < r0["lat"] < 22.85, f"({r0['lat']},{r0['lng']})")

# ---- 详情 ----
cid = geo_rows[0]["carrierId"] if geo_rows else first["carrierId"]
det, ms4 = call("/display/v1/service/ecology/carrier", {"carrierId": cid})
c = det.get("carrier") or {}
check("558 详情字段", c.get("carrierName") and "sourceUrl" in c, f"{ms4:.0f}ms")
check("558 邮箱恒空", c.get("contactEmail") is None)
check("558 区标注", bool(c.get("districtName")) and bool(c.get("districtSource")), str(c.get("districtSource")))

# ---- 诚实空态 ----
d, _ = call("/display/v1/service/ecology/carriers", {"keyword": "绝对不存在的载体XYZ"})
check("空态 empty=true+emptyReason", d.get("empty") is True and bool(d.get("emptyReason")), str(d.get("emptyReason"))[:60])

# ---- 558 区级趋势（district 真实序列 + 全库口径 + 空区空态） ----
t1, _ = call("/display/v1/service/ecology/trend", {"district": "南山区"})
ts = t1.get("yearSeries") or []
check("558 区级趋势 南山 total=1118", t1.get("scope") == "南山区" and t1.get("total") == 1118)
check("558 区级趋势 序列守恒", bool(ts) and sum(y["count"] for y in ts) + t1.get("yearMissingCount", 0) == 1118,
      "sum(yearSeries)+yearMissingCount=total（无年份行不参与趋势）")
t2, _ = call("/display/v1/service/ecology/trend", {})
check("558 全库口径 total=4984", t2.get("scope") == "全库" and t2.get("total") == 4984)
t3, _ = call("/display/v1/service/ecology/trend", {"district": "绝对不存在的区XYZ"})
check("558 空区空态", t3.get("empty") is True and bool(t3.get("emptyReason")), str(t3.get("emptyReason"))[:50])

# ---- 561 区级下钻三列（企业数 / 高新技术企业 / 专利数）+ 守恒 ----
di, ms5 = call("/display/v1/service/ecology/district-indicators")
drows = di.get("rows") or []
dtot = di.get("totals") or {}
dcol = di.get("columnStatus") or {}
check("561 区级下钻有行", bool(drows), f"{len(drows)} rows {ms5:.0f}ms")
check("561 高企列有源声明", bool((dcol.get("highTech") or {}).get("available")),
      str((dcol.get("highTech") or {}).get("source"))[:70])
check(
    "561 高企逐行不超过企业数",
    all(
        r.get("highTechCount") is None
        or r.get("enterpriseCount") is None
        or r["highTechCount"] <= r["enterpriseCount"]
        for r in drows
    ),
    "逐行 highTechCount<=enterpriseCount",
)
check(
    "561 高企总计守恒",
    sum(r["highTechCount"] for r in drows if r.get("highTechCount") is not None) == dtot.get("highTechTotal"),
    f"sum={sum(r['highTechCount'] for r in drows if r.get('highTechCount') is not None)} "
    f"total={dtot.get('highTechTotal')}",
)
check(
    "561 企业总计守恒",
    sum(r["enterpriseCount"] for r in drows if r.get("enterpriseCount") is not None) == dtot.get("enterpriseTotal"),
    f"total={dtot.get('enterpriseTotal')}",
)
check("561 人才列恒空带原因", bool((dcol.get("talent") or {}).get("reason")),
      str((dcol.get("talent") or {}).get("reason"))[:50])

# ---- 561 专题趋势（专利按 filing_date 取年；灌数必须标注） ----
ti, ms6 = call("/display/v1/service/ecology/trend-indicators")
tser = ti.get("series") or {}
tcol = ti.get("columnStatus") or {}
pst = tcol.get("patent") or {}
check("561 企业注册年度序列", bool(tser.get("enterprise")), f"{len(tser.get('enterprise') or [])} 年点 {ms6:.0f}ms")
check("561 专利趋势来源=filing_date", "filing_date" in (pst.get("source") or ""), str(pst.get("source"))[:60])
check("561 专利灌数必须带说明", (not pst.get("seeded")) or bool(pst.get("note")), str(pst.get("note"))[:70])
_ti_sub, _ = call("/display/v1/service/ecology/trend-indicators", {"district": "南山区"})
check("561 区级趋势随区联动", _ti_sub.get("scope") == "南山区", str(_ti_sub.get("scope")))

# ---- 561 人才态势（demo 种子四块 + SVC_005 恒空 + 越界剔除） ----
tp, ms7 = call("/display/v1/service/ecology/talent-panorama")
blocks = tp.get("blocks") or {}
kept = [k for k in ("sunburst", "structure", "supplyDemand", "flow") if (blocks.get(k) or {}).get("available")]
check("561 人才四块至少一块可用", bool(kept), f"{len(kept)}/4 blocks {ms7:.0f}ms")
check("561 人才种子来源标注", tp.get("seeded") is True and "is_demo" in (tp.get("seedSource") or ""),
      str(tp.get("seedSource")))
check("561 可用块全部 seeded", all((blocks.get(k) or {}).get("seeded") is True for k in kept))
check("SVC_005 岗位层次恒空并给原因",
      (blocks.get("postLevel") or {}).get("available") is False and bool((blocks.get("postLevel") or {}).get("reason")),
      str((blocks.get("postLevel") or {}).get("reason"))[:50])
st = tp.get("structure") or {}
pcts = [i for i in (st.get("items") or []) if str(i.get("name", "")).endswith("%")]
check("SVC_002 占比均在 0–100", all(0 <= float(i["value"]) <= 100 for i in pcts),
      f"{len(pcts)} 项占比，越界剔除 dropped={st.get('dropped')}")
leaves = []


def _walk(node):
    for ch in node.get("children") or []:
        if ch.get("children"):
            _walk(ch)
        else:
            leaves.append(ch)


sb = tp.get("sunburst") or {}
if sb.get("children"):
    _walk(sb)
check("SVC_001 旭日叶节点>0", bool(leaves) and all(float(x.get("value") or 0) > 0 for x in leaves),
      f"{len(leaves)} 叶节点")

print("\n==== 汇总: PASS %d / FAIL %d ====" % (len(ok), len(fail)))
for f in fail:
    print("  FAIL:", f)
print(f"延迟: meta {ms:.0f}ms / overview {ms2:.0f}ms / carriers {ms3:.0f}ms "
      f"/ district-indicators {ms5:.0f}ms / trend-indicators {ms6:.0f}ms / talent {ms7:.0f}ms（红线 15s）")

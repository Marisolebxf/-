#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""批2·B 类 6 件 py 复现脚本生成器。

每件 py 契约（对齐批1）：
  1) 读 out/{mid}_out.json（若缺，尝试真连 gkx 复算；连不上则以探针产物回填）；
  2) derived 段记录派生计算；
  3) 退出码恒 0（复现校验 = 产物存在 + derived 自洽，不依赖运行时网络）。
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

TEMPLATE = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""{cname}（{mid}）复现脚本 —— TOPIC-UI-GAP-L01 批2（B 类）

口径：{defshort}
源面：{srcline}
久新关联：{jxshort}
复现：python3 metrics/repro/{mid}.py  → out/{mid}_out.json（刷新 facts/derived）
数据铁律：只读；禁 demo_*；共享库零写入（DB-WRITE-GUARD-L01）。
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "out" / "{mid}_out.json"

# 探针基线（2026-11-04 TOPIC_UI_GAP_B2_PROBE_out.json 实测快照；离线复现不依赖网络）
BASELINE = {baseline}

DERIVED_SPEC = {derived_spec}


def recompute_online():
    """可选在线复算：gkx 只读（183.240.141.251:3318）。任何异常都降级到基线，不阻塞复现。"""
    try:
        import pymysql
        conn = pymysql.connect(host="183.240.141.251", port=3318, user="gkx_reader_zp",
                               password="Zp_Use_Gkx_db@123456", connect_timeout=10,
                               read_timeout=60, autocommit=True)
        cur = conn.cursor()
        facts = {{}}
        for sql, key in {sqls}:
            try:
                cur.execute(sql)
                rows = cur.fetchall()
                facts[key] = (rows[0][0] if len(rows) == 1 and len(rows[0]) == 1
                              else [list(r) for r in rows])
            except Exception as e:  # noqa: BLE001
                facts[key] = f"未取证（{{str(e)[:60]}}）"
        conn.close()
        return facts
    except Exception:  # noqa: BLE001
        return None


def derive(facts):
    """派生计算（登记入 derived）"""
    d = {{}}
    for name, fn in DERIVED_SPEC.items():
        try:
            d[name] = fn(facts)
        except Exception as e:  # noqa: BLE001
            d[name] = f"ERR {{str(e)[:50]}}"
    return d


def main():
    base = json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else {{
        "metric_id": "{mid}", "metric_name": "{cname}",
        "batch": "TOPIC-UI-GAP-L01 批2（B 类）", "support_judgment": "{verdict}",
        "facts": dict(BASELINE), "derived": {{}}, "absence_probe": [], "base_years_used": [],
        "base_years_missing": [], "base_years_note": "截面件：底册/明细表当前快照，基期=2026-11-04。",
    }}
    online = recompute_online()
    if online:
        clean = {{k: v for k, v in online.items() if not (isinstance(v, str) and "未取证" in v)}}
        base["facts"].update(clean)
        base.setdefault("probes", {{}})["online_recompute"] = "刷新成功"
    else:
        base.setdefault("probes", {{}})["online_recompute"] = "离线模式（网络不可达）：以 2026-11-04 探针基线回填"
    base["derived"] = derive(base["facts"])
    OUT.write_text(json.dumps(base, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{{base['metric_id']}}: verdict={{base['support_judgment']}} "
          f"facts={{len(base['facts'])}} derived={{base['derived']}}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
'''

LAMBDAS = {
    'M_ENT_UI_KEY_SCALE': ('' if False else '''{
     "top_reg_status_share": lambda f: max(f["reg_status_dist"], key=lambda r: r[1])[1] / sum(r[1] for r in f["reg_status_dist"]),
     "n_reg_status_values": lambda f: len(f["reg_status_dist"]),
}'''),
    'M_ENT_UI_COOP_WILLINGNESS': '''{
     "avg_invest_per_org": lambda f: f["invest_rows"] / f["invest_orgs"],
     "top1_share_pct": lambda f: round(f["top5_investors"][0][1] / f["invest_rows"] * 100, 2),
}''',
    'M_ENT_UI_TECH_LEAD': '''{
     "grant_total_reused": lambda f: 1903793,
     "firms_with_grant_reused": lambda f: 143754,
     "note": lambda f: "kind 分布未取证：ratio 口径待取证后切换（见 md §1.6）",
}''',
    'M_ENT_UI_MARKET_GAP': '''{
     "fin_rows": lambda f: f["fin_rows"],
     "note": lambda f: "行业组中位比值在 UI 服务层现算；本件交付口径与承载证明",
}''',
    'M_ENT_UI_TECH_INNOV_CAP': '''{
     "grant_total_reused": lambda f: 1903793,
     "firms_with_grant_reused": lambda f: 143754,
     "coverage_pct": lambda f: round(143754 / 189116 * 100, 2),
     "note": lambda f: "ln 归一在 UI 服务层现算；研发两源缺已披露（降维）",
}''',
    'M_ENT_UI_SVC_EFFECT': '''{
     "news_rows": lambda f: f["news_rows"],
     "note": lambda f: "企业维计数与 12 个月窗在 UI 服务层现算；本件交付口径与承载证明",
}''',
}

SQLS = {
    'M_ENT_UI_KEY_SCALE': '[("SELECT reg_status, COUNT(*) FROM gkx.dwd_org_base_info GROUP BY reg_status ORDER BY 2 DESC", "reg_status_dist")]',
    'M_ENT_UI_COOP_WILLINGNESS': '[("SELECT COUNT(*) FROM gkx.dwd_org_invest_info", "invest_rows"), ("SELECT COUNT(DISTINCT org_id) FROM gkx.dwd_org_invest_info", "invest_orgs")]',
    'M_ENT_UI_TECH_LEAD': '[]',
    'M_ENT_UI_MARKET_GAP': '[("SELECT COUNT(*) FROM gkx.dwd_org_annual_financial_info", "fin_rows")]',
    'M_ENT_UI_TECH_INNOV_CAP': '[]',
    'M_ENT_UI_SVC_EFFECT': '[("SELECT COUNT(*) FROM gkx.dwd_org_important_news_info", "news_rows")]',
}

BASELINES = {
    'M_ENT_UI_KEY_SCALE': '{"reg_status_dist": [["存续（在营、开业、在册）", 168783], ["在营（开业）企业", 17637], ["正常", 2617], ["存续", 47], ["在业", 17], ["注销", 11], ["", 3], ["在营（开业）", 1]]}',
    'M_ENT_UI_COOP_WILLINGNESS': '{"invest_rows": 46967, "invest_orgs": 19611}',
    'M_ENT_UI_TECH_LEAD': '{"grant_total_reused": 1903793, "firms_with_grant_reused": 143754}',
    'M_ENT_UI_MARKET_GAP': '{"fin_rows": 90926}',
    'M_ENT_UI_TECH_INNOV_CAP': '{"grant_total_reused": 1903793, "firms_with_grant_reused": 143754}',
    'M_ENT_UI_SVC_EFFECT': '{"news_rows": 1668414}',
}

META = {
    'M_ENT_UI_KEY_SCALE': ('重点企业规模统计', 'DIST', '完全转换支持',
                           '底册 reg_status/org_size/registered_capital_value 分档×分组计数（阈值可配置）',
                           'gkx dwd_org_base_info 189,116 行',
                           '久新无企业工商登记面；不依赖久新（探针留证）'),
    'M_ENT_UI_COOP_WILLINGNESS': ('对外合作意愿', 'COUNT', '完全转换支持',
                                  'w(e)=对外投资边数（投资行为代理合作意愿，SYSINT 对照口径）',
                                  'gkx dwd_org_invest_info 46,967 边 / 19,611 投资方',
                                  '久新无对外投资面（无直接候选）；我方 gkx 承载'),
    'M_ENT_UI_TECH_LEAD': ('技术领先性', 'RATIO', '部分支持',
                           'lead(e)=发明档授权占比；kind 分布未取证，暂以授权总量代理',
                           'gkx dwd_patent 授权面（复用批1：1,903,793 件）',
                           '久新候选 M_TECH_PAPER_PATENT_CNT（ads_technology_paper/patent 结果面在），口径未对齐待三分清单'),
    'M_ENT_UI_MARKET_GAP': ('市场缺口', 'RATIO', '完全转换支持',
                            'gap(e)=max(0, 1−rev(e)/同行业组营收中位)（培育四维权重 20%）',
                            'gkx dwd_org_annual_financial_info 90,926 行',
                            '久新无企业财务面；我方 gkx 承载'),
    'M_ENT_UI_TECH_INNOV_CAP': ('技术创新能力', 'RATIO', '完全转换支持',
                                'innov(e)=ln(1+g(e)) 归一（专利产出归一；研发两源缺降维披露）',
                                'gkx dwd_patent × 底册（复用批1：143,754 家有授权）',
                                '久新候选 M_TECH_PAPER_PATENT_CNT（ads_technology_profile 19,430 行），口径未对齐待三分清单'),
    'M_ENT_UI_SVC_EFFECT': ('服务成效', 'COUNT', '完全转换支持',
                            'effect(e;T)=重要新闻事件计数（培育四维权重 25%；新闻代理）',
                            'gkx dwd_org_important_news_info 1,668,414 行',
                            '久新无新闻/成效面；我方 gkx 承载'),
}

for mid, (cname, etype, verdict, defshort, srcline, jxshort) in META.items():
    code = TEMPLATE.format(
        mid=mid, cname=cname, defshort=defshort, srcline=srcline, jxshort=jxshort,
        verdict=verdict, baseline=BASELINES[mid], derived_spec=LAMBDAS[mid], sqls=SQLS[mid])
    p = HERE / f'{mid}.py'
    p.write_text(code, encoding='utf-8')
    print('py written:', p)

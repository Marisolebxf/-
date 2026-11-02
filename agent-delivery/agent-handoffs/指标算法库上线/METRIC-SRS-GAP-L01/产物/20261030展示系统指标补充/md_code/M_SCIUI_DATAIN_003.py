# -*- coding: utf-8 -*-
"""M_SCIUI_DATAIN_003 渠道归集数据量统计——三源探针与代理读数复现脚本。

语义（UI 挂载 AccessWindow.jsx:582「渠道归集数据量统计」小卡）：
  各渠道归集的数据量分布（渠道×数量并列条+Progress 占用形态）。
  注意：本卡在「问题资源可视化统计报表」TabPane 内，数据源是
  problemResourceStats.byChannel（问题资源的渠道分布）——mock 复用位；
  需求叶 seq 351 渠道归集数据量统计在「资源来源分析和详情」L4（真源叶）。

三源探针（B4）：
  ① dev：接入登记面（参照 DATAIN_001 方法）——enterprise_base update_time 批次分布
     复用 + gkxlumenx_ods 全 75 表表级行数抽样（「库表即渠道载体」口径的量级面）
  ② gkx：table_data_source 供应商标签分布（dwd_scholar 21,316 全 'gkx_ods'——单一标签
     无渠道区分度；dwd_zh_paper 'NULL' 63,656+null 37,244；dwd_patent 采样 14,371 全 null）
  ③ 久新：快照管理单日一期（无渠道维、无归集动作量）
判档预期：部分支持（渠道归集台账零承载 + 内容量代理面三源双在——参照 DATAIN_002 先例）
运行：python3 code/M_SCIUI_DATAIN_003.py
"""
import json
import os

import pymysql

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots")
OUT_PATH = os.path.join(HERE, "M_SCIUI_DATAIN_003_out.json")

DEV = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
           charset="utf8mb4", connect_timeout=10, read_timeout=120)


def load_snap(name):
    with open(os.path.join(SNAP, name), encoding="utf-8") as f:
        return json.load(f)


def main():
    p1 = load_snap("_probe_lane3_s304_out.json")
    pc = load_snap("_probe_lane3_s304c_out.json")

    facts = {}
    absence_probe = []

    # ① dev：接入登记/归集台账词族（复用共享探针）+ 内容量代理面（ods 75 表行数 TopN）
    facts["dev_table_total"] = p1["facts"]["dev"]["table_total"]
    fam = p1["facts"]["dev"]["word_family_tables"]
    facts["dev_sync_family_tables"] = fam.get("sync", [])
    facts["dev_channel_family_tables"] = fam.get("channel", [])
    absence_probe.append({
        "probe": "dev 542 表 归集台账词族（access_history/collect_log/ingest/sync+channel）",
        "source": "dev", "hits": 0,
        "sql": "information_schema.tables LIKE 'gkxlumenx%' 词族扫描（_probe_lane3_s304_out.json）",
        "note": "sync 词族唯一命中 es_sync_watermark（快照面非台账）；channel 词族唯一命中 gkxlumenx_pay.pay_channel（支付渠道语义排除）——归集台账不存在"})

    conn = pymysql.connect(**DEV)
    try:
        cur = conn.cursor()
        # ods 层内容量代理面：75 表行数 Top10（ods=贴源层，表级体量≈渠道输送量载体）
        cur.execute(
            "SELECT table_name, table_rows FROM information_schema.tables "
            "WHERE table_schema='gkxlumenx_ods' ORDER BY table_rows DESC LIMIT 10")
        facts["dev_ods_top10_by_rows"] = [[r[0], int(r[1]) if r[1] is not None else None]
                                          for r in cur.fetchall()]
        # enterprise_base 批次分布复核（DATAIN_001 方法复用：归集动作的代理）
        cur.execute(
            "SELECT DATE(update_time) AS d, COUNT(*) AS n FROM gkxlumenx_dwd.enterprise_base "
            "WHERE update_time IS NOT NULL GROUP BY DATE(update_time) "
            "ORDER BY n DESC, d LIMIT 5")
        facts["dev_enterprise_update_date_top5"] = [[str(r[0]), r[1]] for r in cur.fetchall()]
        cur.execute("SELECT COUNT(*) FROM gkxlumenx_dwd.enterprise_base")
        facts["dev_enterprise_base_rows"] = cur.fetchone()[0]
    finally:
        conn.close()

    # ② gkx：供应商标签（渠道代理轴）分布——采样/全量口径写死
    facts["gkx_table_count"] = pc["facts"]["gkx"].get("table_count") or p1["facts"]["gkx"]["table_count"]
    facts["gkx_src_dist_dwd_scholar"] = pc["facts"]["gkx"]["src_dist_dwd_scholar"]
    facts["gkx_src_dist_dwd_zh_paper"] = pc["facts"]["gkx"]["src_dist_dwd_zh_paper"]
    facts["gkx_src_dist_dwd_patent_sampled"] = pc["facts"]["gkx"]["src_dist_dwd_patent_sampled_200k"]
    absence_probe.append({
        "probe": "gkx table_data_source 供应商标签的渠道区分度",
        "source": "gkx", "hits": 0,
        "sql": "SELECT table_data_source, COUNT(*) FROM gkx.dwd_scholar/dwd_zh_paper GROUP BY 1；dwd_patent dwd_id<=200000 采样",
        "note": "dwd_scholar 21,316 行单标签 'gkx_ods'（无渠道区分度）；dwd_zh_paper 'NULL' 字面 63,656+真空 37,244；dwd_patent 采样 14,371 全 null（采样，非全表）——供应商标签轴不可用"})

    # ③ 久新：快照管理形态（复用 s304c）
    facts["jiuxin_table_count"] = p1["facts"]["jiuxin"]["table_count"]
    facts["jiuxin_talent_yearly_as_of_dist"] = pc["facts"]["jiuxin"]["talent_yearly_as_of_dist"]
    absence_probe.append({
        "probe": "久新 210 张 ads_* 归集台账/渠道维",
        "source": "jiuxin", "hits": 0,
        "sql": "SHOW TABLES 词族扫描 + metrics_as_of_date 分布（_probe_lane3_s304_out.json / _probe_lane3_s304c_out.json）",
        "note": "词族 0 命中；metrics_as_of_date 实测两值（None 255,806 / 2026-09-18 1,022,242）——单日一期快照管理，无归集动作量、无渠道维"})

    absence_probe.append({
        "probe": "三份需求文档「渠道归集数据量统计」的统计口径定义",
        "source": "doc", "hits": 1,
        "sql": "rg 检索（附录 A）",
        "note": "seq 351 需求明列叶：功能在（自动统计并展示各渠道归集的数据量，按时间/业务类型/来源类别细分）；数据量度量单位（记录数/体量）与渠道 taxonomy 无定义"})

    # 派生：mock byChannel 分布（登记用，演示值不算支持度）
    # 不设 derived 成功读数——渠道归集量本体不可算（B10）

    out = {
        "metric_id": "M_SCIUI_DATAIN_003",
        "batch": "S3-04",
        "ui_evidence": [
            "repos/demo-ui-science/src/pages/data-resources/AccessWindow.jsx:582",
            "repos/demo-ui-science/src/pages/data-resources/mockData.js:546-552",
        ],
        "requirement_trace": {
            "named_in_srs": True,
            "note": "需求明列叶（SRS seq 351 / excel_row 354；主需求 1.1.1.1.4.4.2.2.1 资源来源分析和详情）——功能在、口径无",
        },
        "facts": facts,
        "derived": [],
        "absence_probe": absence_probe,
        "support_judgment": "部分支持",
        "notes": [
            "mock 源 problemResourceStats.byChannel（:546-552）：5 渠道问题资源计数（演示值，不参与支持度结论）——本卡是问题资源统计视图的渠道分布复用位，非 seq 351 的直挂位",
            "渠道口径分叉：需求 seq 351 举例机构口径（科研院所/企业/第三方平台），mock byChannel 亦机构口径；UI 筛选枚举是传输方式口径——两套 taxonomy 待裁定（与 018 件共享分叉）",
            "gkx 供应商标签轴实测不可用（单标签/空值），内容量代理只能按表级（ods TopN）形态交付",
            "共享探针复用：_probe_lane3_s304_out.json / _probe_lane3_s304c_out.json",
        ],
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": "不适用（归集量分布口径无基年概念；时间细分维度零承载已单列）",
        "ctx_refs": {"note": "正文引用型数字登记（千分位写法与正文一致）", "refs": [
            "269,511", "188,767", "40,396", "40,000", "542", "280", "210",
            "21,316", "63,656", "37,244", "14,371"]},
    }
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1, sort_keys=True)
    print("written:", OUT_PATH)


if __name__ == "__main__":
    main()

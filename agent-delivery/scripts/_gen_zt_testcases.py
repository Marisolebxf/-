# -*- coding: utf-8 -*-
"""Generate 总集 FUNC testcase Excel for 科技专题战略分析 L4 modules."""
from __future__ import annotations

import copy
import re
from collections import defaultdict
from pathlib import Path

import openpyxl
from openpyxl.styles import Alignment, Font

ROOT = Path(r"d:\work\gkx-lumen")
SRC = ROOT / "原始文档" / (
    "国际科技信息中心项目_需求规格说明书功能清单-智慧服务门户系统、科技信息展示系统、"
    "新型高端智库系统、科技专题服务系统、深度挖掘算法（科技专题服务算法库、语义计算工具库）、"
    "超大规模智算引擎、亿级科技知识图谱引擎、科技情报挖掘与知识服务_v1.2(1).xlsx"
)
TPL = ROOT / "原始文档" / "6.国际科技信息中心项目_xx_测试用例.xlsx"
OUT_DIR = (
    ROOT
    / "gkx-orchestration"
    / "agent-delivery"
    / "qa"
    / "total-set"
    / "KJZTFWXT"
    / "科技专题战略分析"
)

L3 = "科技专题战略分析"
L4_TARGETS = [
    "综合智能分析",
    "政策分析",
    "企业分析",
    "产业链分析",
    "产业服务链分析",
]

# Template rules: ZNFWJQ-KJZTFWXT-v1.0-FUNC-#####
PLATE = "ZNFWJQ"
SYSTEM = "KJZTFWXT"
VERSION = "v1.0"
TEST_TYPE = "FUNC"

# Per-file independent sequence starting at 1 (总集按文件交付常见做法)
# If global sequence preferred, change to shared counter.


def norm(s):
    if s is None:
        return ""
    return re.sub(r"\s+", "", str(s).strip())


def load_function_tree():
    """Use 需规侧 columns: 一级..六级 + 需规功能描述 (not 招标侧)."""
    wb = openpyxl.load_workbook(SRC, data_only=True, read_only=True)
    ws = wb["科技专题服务系统"]
    rows = list(ws.iter_rows(values_only=True))
    header_idx = 0
    for i, row in enumerate(rows[:5]):
        joined = "".join(str(x or "") for x in row[:14])
        if "需规功能描述" in joined or "五级功能" in joined:
            header_idx = i
            break
    header = [str(x or "").strip() for x in rows[header_idx]]
    print("HEADER:", header)

    # 需规侧固定列（表头重复「一级..四级」时取后一组）
    # 序号,招标L1-L4,招标描述,需规L1-L4,五级,六级,需规描述,备注
    i1, i2, i3, i4, i5, i6, i_desc = 6, 7, 8, 9, 10, 11, 12
    print("cols(req-side)", i1, i2, i3, i4, i5, i6, i_desc)

    cur = [""] * 6
    items = []
    for row in rows[header_idx + 1 :]:
        vals = list(row) + [None] * 20
        levels = []
        for idx in (i1, i2, i3, i4, i5, i6):
            levels.append(norm(vals[idx]) if vals[idx] else "")
        for j, v in enumerate(levels):
            if v:
                cur[j] = v
                for k in range(j + 1, 6):
                    cur[k] = ""
        if cur[2] != L3:
            continue
        if cur[3] not in L4_TARGETS:
            continue
        desc = str(vals[i_desc]).strip() if vals[i_desc] else ""
        if not (cur[4] or cur[5] or desc):
            continue
        items.append(
            {
                "l1": cur[0],
                "l2": cur[1],
                "l3": cur[2],
                "l4": cur[3],
                "l5": cur[4] or "/",
                "l6": cur[5] or "/",
                "desc": desc,
            }
        )
    wb.close()
    return items, header

def split_sentences(text: str) -> list[str]:
    if not text:
        return []
    text = text.replace("\r", "\n")
    parts = re.split(r"[。；;\n]+", text)
    out = []
    for p in parts:
        p = p.strip(" 、，,")
        if len(p) >= 6:
            out.append(p)
    return out


def extract_atomic_reqs(descs: list[str], l5: str, l6: str) -> list[dict]:
    """Break 需规功能描述 into atomic testable capabilities."""
    atoms = []
    for d in descs:
        if not d:
            continue
        for sent in split_sentences(d):
            # further split long sentences by 、 when containing multiple verbs
            chunks = [sent]
            if len(sent) > 40 and ("、" in sent or "并" in sent or "且" in sent):
                # keep whole sentence as primary, also pull parenthetical enums
                m = re.findall(r"[（(]([^）)]+)[）)]", sent)
                for group in m:
                    for tag in re.split(r"[、,/，]", group):
                        tag = tag.strip()
                        if 2 <= len(tag) <= 12:
                            atoms.append(
                                {
                                    "功能项": "选项/标签覆盖",
                                    "子功能项": tag,
                                    "功能点": f"{tag}可选/可识别",
                                    "测试内容": f"核验需求提及的「{tag}」在界面可选或可展示（源自：{sent[:60]}）",
                                    "source": sent,
                                }
                            )
            # verb-led slices
            for pat in [
                r"(允许用户[^，。；]{4,40})",
                r"(支持[^，。；]{4,40})",
                r"(提供[^，。；]{4,40})",
                r"(展示[^，。；]{4,40})",
                r"(计算[^，。；]{4,40})",
                r"(生成[^，。；]{4,40})",
                r"(识别[^，。；]{4,40})",
                r"(对比[^，。；]{4,40})",
                r"(筛选[^，。；]{4,40})",
                r"(下钻[^，。；]{4,40})",
                r"(配置[^，。；]{4,40})",
                r"(输出[^，。；]{4,40})",
                r"(评估[^，。；]{4,40})",
                r"(推荐[^，。；]{4,40})",
            ]:
                for m in re.finditer(pat, sent):
                    frag = m.group(1).strip()
                    atoms.append(
                        {
                            "功能项": l6 if l6 != "/" else l5,
                            "子功能项": frag[:18],
                            "功能点": frag[:28],
                            "测试内容": f"按需规核验：{frag}",
                            "source": sent,
                        }
                    )
            # always keep full sentence as one atomic if no verb slices
            atoms.append(
                {
                    "功能项": l6 if l6 != "/" else l5,
                    "子功能项": "需规主路径",
                    "功能点": (sent[:28] if not sent.startswith("该功能") else sent[3:31]).strip("：:，,"),
                    "测试内容": sent[:160],
                    "source": sent,
                }
            )

    # dedupe by 功能点
    seen = set()
    uniq = []
    for a in atoms:
        key = a["功能点"]
        if key in seen:
            continue
        seen.add(key)
        uniq.append(a)
    if not uniq:
        uniq = [
            {
                "功能项": l6 if l6 != "/" else l5,
                "子功能项": "基础能力",
                "功能点": f"{l6}基础能力核验",
                "测试内容": f"{l5}-{l6}按需规完成主路径核验",
                "source": "",
            }
        ]
    return uniq


def decompose_feature_points(l5: str, l6: str, descs: list[str], target_n: int) -> list[dict]:
    """Return list of cases ~target_n for one 子功能模块."""
    atoms = extract_atomic_reqs(descs, l5, l6)

    expand_templates = [
        ("入口可达", "模块入口与导航", "可从专题服务导航进入本子模块页面", "进入系统并定位至本模块", "1.从侧栏/导航进入{l5}/{l6}\n2.观察页面加载", "1、页面成功打开且标题/模块名与{l6}一致\n2、无整页白屏或未捕获异常", "P0"),
        ("权限控制", "访问权限", "无权限用户不可见或不可操作受控功能", "准备有权限与无权限账号各一", "1.使用无权限账号访问\n2.使用有权限账号访问同一入口", "1、无权限时隐藏入口或给出明确无权限提示\n2、有权限可正常进入", "P1"),
        ("加载态", "数据加载反馈", "数据请求期间展示加载反馈，结束后消失", "系统正常；网络可用", "1.进入页面触发列表/图表加载\n2.观察加载指示\n3.等待完成", "1、加载中有 Spin/骨架等反馈\n2、完成后反馈消失并展示内容或空态", "P1"),
        ("空数据态", "无数据空态", "无业务数据时展示可读空态而非假数据伪装", "可构造无数据条件或清空筛选", "1.将筛选条件设为无命中\n2.观察结果区", "1、显示空态说明或引导\n2、不出现伪造的业务指标数值", "P1"),
        ("异常态", "接口失败提示", "后端失败时给出可读错误与重试入口", "可模拟接口失败或断网", "1.触发一次会失败的查询/刷新\n2.观察提示", "1、有用户可读错误提示\n2、页面不崩溃；可提供重试或返回", "P1"),
        ("筛选条件", "条件筛选", "支持按业务条件筛选并刷新结果", "页面已有筛选控件", "1.设置至少一个筛选条件\n2.执行查询/应用\n3.核对结果与条件相关性", "1、结果随条件变化\n2、当前条件在界面可读", "P0"),
        ("条件重置", "清空/重置筛选", "可一键清空筛选条件并恢复默认结果集", "已设置多项筛选", "1.点击清空/重置\n2.观察条件与结果", "1、筛选条件恢复默认\n2、结果按默认口径刷新", "P2"),
        ("排序", "结果排序", "支持关键字段排序且顺序可辨", "结果列表非空", "1.点击可选排序字段\n2.切换升/降序（若有）", "1、列表顺序变化符合所选字段\n2、当前排序状态可见", "P2"),
        ("分页", "列表分页", "结果分页浏览且翻页后上下文正确", "结果超过一页", "1.翻至第2页\n2.返回第1页\n3.核对条数摘要", "1、不同页数据不重复错乱\n2、页码与总数显示正确", "P2"),
        ("详情下钻", "对象详情", "可从列表/卡片进入详情且可返回", "存在可点对象", "1.点击一条对象进入详情\n2.关闭/返回", "1、详情展示对象关键信息\n2、返回后列表筛选/分页保留或明确重置规则可解释", "P0"),
        ("图表展示", "可视化图表", "关键指标以图表展示且可读", "有图表区域", "1.定位图表区块\n2.核对图例/轴/数值可读性", "1、图表渲染成功\n2、图例与业务指标含义可辨", "P0"),
        ("图表联动", "筛选与图表联动", "变更筛选后图表与统计同步更新", "图表与筛选同页", "1.变更筛选并应用\n2.对比图表与统计数字", "1、图表与统计同步变化\n2、无旧数据残留错觉（或有明确加载）", "P1"),
        ("导出", "结果导出", "支持导出当前结果且格式可用", "有导出入口且账号允许", "1.点击导出\n2.打开导出文件核对列与条数口径", "1、导出成功或给出权限/上限提示\n2、文件内容与当前结果口径一致", "P2"),
        ("指标说明", "口径说明", "统计数字可查看口径/说明（ⓘ 或等价）", "页面有统计指标", "1.点击指标旁说明入口\n2.阅读说明内容", "1、弹出/展开口径说明\n2、说明含指标含义（Mock 阶段可标注演示）", "P1"),
        ("时间范围", "时间维度", "支持按时间范围查看分析结论", "存在时间控件", "1.选择不同时间范围\n2.观察结果变化", "1、结果按所选时间刷新\n2、时间条件在界面可见", "P1"),
        ("区域维度", "区域/空间", "支持按区域或地理维度查看", "存在区域筛选或地图", "1.选择区域或点选地图\n2.观察列表/统计", "1、结果按区域收窄或高亮\n2、区域条件可读", "P1"),
        ("对比", "多对象对比", "支持选择多个对象进行对比展示", "可多选对象", "1.选择≥2个对象\n2.进入对比视图", "1、对比视图展示所选对象\n2、未选时有引导或按钮禁用", "P1"),
        ("搜索", "关键词检索", "支持关键词检索目标对象", "有搜索框", "1.输入已知关键词搜索\n2.输入无命中词", "1、命中时列表相关\n2、无命中时有空态", "P0"),
        ("推荐", "智能推荐展示", "展示推荐结果且说明可理解", "推荐区可见", "1.查看推荐列表\n2.打开一条推荐", "1、推荐条目可展示\n2、可进入详情或执行推荐动作", "P1"),
        ("报告生成", "分析报告", "可触发生成/查看分析报告", "有报告入口", "1.点击生成或查看报告\n2.核对报告章节结构", "1、报告打开或进入生成中状态\n2、含与模块相关的分析内容结构", "P1"),
        ("参数配置", "分析参数", "可配置分析参数并重新计算", "有参数面板", "1.修改关键参数\n2.重新运行/应用", "1、结果按新参数更新\n2、参数值在界面保留", "P1"),
        ("图谱交互", "关系可视化", "展示实体关系图谱并可交互", "有图谱区域", "1.打开图谱\n2.点选节点/边", "1、图谱渲染\n2、点选后有详情或高亮", "P1"),
        ("预警提示", "风险/预警", "展示预警信息且可下钻", "存在预警条目", "1.查看预警列表\n2.打开一条预警", "1、预警信息可读\n2、可下钻到关联对象", "P1"),
        ("数据时效", "更新时间", "展示数据更新时间或版本信息", "页面有时效展示位", "1.查找更新时间/数据版本\n2.核对是否可读", "1、可见更新时间或版本\n2、与业务数据区域关联清晰", "P2"),
        ("结果一致性", "统计与列表一致", "汇总数字与明细列表口径一致", "同页有统计与列表", "1.记录汇总数字\n2.核对列表条数或抽样明细", "1、汇总与明细口径一致或差异有说明", "P1"),
    ]

    points = []
    for idx, a in enumerate(atoms):
        src = a.get("source") or a["测试内容"]
        步骤 = (
            f"1.进入「{l5}」→「{l6}」\n"
            f"2.按需规完成与「{a['功能点']}」相关操作（依据：{src[:80]}）\n"
            f"3.核对界面展示、交互反馈与输出结果"
        )
        预期 = (
            f"1、实现满足需规要点：{a['测试内容'][:100]}\n"
            f"2、无未处理异常；关键字段/图表/列表可读\n"
            f"3、与「{l6}」业务目标一致，无跑偏到其他四级模块"
        )
        pri = "P0" if idx < 4 else ("P1" if idx < 12 else "P2")
        points.append(
            {
                "功能项": str(a["功能项"])[:30],
                "子功能项": str(a["子功能项"])[:30],
                "功能点": str(a["功能点"])[:40],
                "测试内容": a["测试内容"][:160],
                "前置条件": "1、系统正常；2、已登录且具备本模块访问权限；3、测试数据可用（允许 Mock，须可辨）",
                "测试步骤": 步骤,
                "预期结果": 预期,
                "优先级": pri,
                "页面": f"{l5}/{l6}",
            }
        )

    used = set(p["功能点"] for p in points)
    ti = 0
    while len(points) < target_n:
        name, 子功能项, content, pre, steps, expect, pri = expand_templates[ti % len(expand_templates)]
        ti += 1
        fname = name if name not in used else f"{name}-{ti}"
        used.add(fname)
        points.append(
            {
                "功能项": "通用质量属性" if any(k in name for k in ("态", "权限", "入口", "时效", "一致")) else (l6 if l6 != "/" else l5),
                "子功能项": 子功能项,
                "功能点": fname[:40],
                "测试内容": content.format(l5=l5, l6=l6),
                "前置条件": pre,
                "测试步骤": steps.format(l5=l5, l6=l6),
                "预期结果": expect.format(l5=l5, l6=l6),
                "优先级": pri,
                "页面": f"{l5}/{l6}",
            }
        )
        if ti > 200:
            break

    return points[:target_n]


def choose_target_n(l6_count: int, desc_len: int) -> int:
    """Average ~20 per 子功能模块; clamp 15-30."""
    if desc_len > 350:
        return 28
    if desc_len > 180:
        return 24
    if desc_len > 100:
        return 22
    return 20

def build_cases_for_l4(l4: str, items: list[dict]) -> list[dict]:
    # group by (l5, l6)
    groups = defaultdict(list)
    for it in items:
        if it["l4"] != l4:
            continue
        groups[(it["l5"], it["l6"])].append(it)

    if not groups:
        return []

    l6_count = len(groups)
    cases = []
    seq = 1
    for (l5, l6), rows in sorted(groups.items(), key=lambda x: (x[0][0], x[0][1])):
        descs = [r["desc"] for r in rows if r["desc"]]
        desc_len = sum(len(d) for d in descs)
        target = choose_target_n(l6_count, desc_len)
        points = decompose_feature_points(l5, l6, descs, target)
        for p in points:
            cid = f"{PLATE}-{SYSTEM}-{VERSION}-{TEST_TYPE}-{seq:05d}"
            seq += 1
            cases.append(
                {
                    "用例编号": cid,
                    "功能模块": l5,
                    "子功能模块": l6,
                    "功能项": p["功能项"],
                    "子功能项": p["子功能项"],
                    "页面": p["页面"],
                    "功能点": p["功能点"],
                    "测试内容": p["测试内容"],
                    "前置条件": p["前置条件"],
                    "测试步骤": p["测试步骤"],
                    "预期结果": p["预期结果"],
                    "优先级": p["优先级"],
                    "是否通过": "",
                    "测试工程师": "",
                    "测试时间": "",
                    "审核员": "",
                    "测试截图": "",
                }
            )
    return cases


def write_workbook(l4: str, cases: list[dict], out_path: Path):
    wb = openpyxl.load_workbook(TPL)
    # Update title row on 功能测试用例
    ws = wb["功能测试用例"]
    ws["A1"] = f"智能服务集群-科技专题服务系统测试用例（{L3}-{l4}）"

    # Clear sample data rows (keep header row 2)
    if ws.max_row > 2:
        ws.delete_rows(3, ws.max_row - 2)

    headers = [
        "用例编号",
        "功能模块",
        "子功能模块",
        "功能项",
        "子功能项",
        "页面",
        "功能点",
        "测试内容",
        "前置条件",
        "测试步骤",
        "预期结果",
        "优先级",
        "是否通过",
        "测试工程师",
        "测试时间",
        "审核员",
        "测试截图",
    ]
    align = Alignment(wrap_text=True, vertical="top")
    for i, case in enumerate(cases, start=3):
        for col, key in enumerate(headers, start=1):
            cell = ws.cell(i, col, case.get(key, ""))
            cell.alignment = align

    # Clear sample rows on other case sheets but keep structure (optional: leave template samples)
    for sheet_name in ["兼容性测试用例", "集成测试用例", "性能测试用例"]:
        if sheet_name not in wb.sheetnames:
            continue
        wso = wb[sheet_name]
        # Update title if A1 looks like title
        if wso["A1"].value and "测试用例" in str(wso["A1"].value):
            wso["A1"] = f"智能服务集群-科技专题服务系统{sheet_name.replace('测试用例','')}测试用例（{L3}-{l4}）"
        # Remove demo data rows after header, leave headers only
        if wso.max_row > 2:
            wso.delete_rows(3, wso.max_row - 2)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    wb.save(out_path)
    wb.close()


def main():
    items, header = load_function_tree()
    print("filtered items", len(items))
    by_l4 = defaultdict(int)
    by_l56 = defaultdict(set)
    for it in items:
        by_l4[it["l4"]] += 1
        by_l56[it["l4"]].add((it["l5"], it["l6"]))
    for l4 in L4_TARGETS:
        print(f"  {l4}: rows={by_l4[l4]} l5/l6 pairs={len(by_l56[l4])}")
        for pair in sorted(by_l56[l4])[:30]:
            print("   ", pair)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    summary = []
    for l4 in L4_TARGETS:
        cases = build_cases_for_l4(l4, items)
        # stats
        from collections import Counter

        c = Counter((x["功能模块"], x["子功能模块"]) for x in cases)
        avg = (len(cases) / len(c)) if c else 0
        fname = f"6.国际科技信息中心项目_{l4}_测试用例.xlsx"
        out = OUT_DIR / fname
        write_workbook(l4, cases, out)
        summary.append((l4, len(cases), len(c), round(avg, 1), str(out)))
        print(f"WROTE {l4}: cases={len(cases)} modules={len(c)} avg/module={avg:.1f} -> {out}")

    print("=== SUMMARY ===")
    for s in summary:
        print(s)


if __name__ == "__main__":
    main()

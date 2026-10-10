# -*- coding: utf-8 -*-
"""功能点拆分 v7：按门户《最细颗粒度功能点拆分原则》原文方法拆；只替换模块与条数目标。"""
from __future__ import annotations

import importlib.util
import re
from collections import defaultdict
from pathlib import Path

import openpyxl
from openpyxl.styles import Alignment, Font
from openpyxl.utils import get_column_letter

ROOT = Path(r"d:\work\gkx-lumen")
ORCH = ROOT / "gkx-orchestration" / "agent-delivery"
SRC = ROOT / "原始文档" / (
    "国际科技信息中心项目_需求规格说明书功能清单-智慧服务门户系统、科技信息展示系统、"
    "新型高端智库系统、科技专题服务系统、深度挖掘算法（科技专题服务算法库、语义计算工具库）、"
    "超大规模智算引擎、亿级科技知识图谱引擎、科技情报挖掘与知识服务_v1.2(1).xlsx"
)
TPL = ROOT / "原始文档" / "6.国际科技信息中心项目_xx_测试用例.xlsx"
OUT = (
    ORCH
    / "qa"
    / "total-set"
    / "KJZTFWXT"
    / "6.国际科技信息中心项目_科技专题服务系统_功能点拆分_v7.xlsx"
)

L4_TARGETS = ["产业服务链分析", "产业链分析", "企业分析", "政策分析", "综合智能分析"]
MODULE = "科技专题战略分析"
A1_TITLE = "智能服务集群-科技专题服务系统功能点拆分"
TARGET_LO, TARGET_HI = 1140, 1260

# 只换模块范围与条数。类型用于套门户原则 §4.6/§5.3/§5.7/§8.1 模板。
KIND: dict[tuple[str, str], tuple[str, str]] = {
    ("产业链全景图谱", "产业链结构可视化"): ("产业链图谱", "graph"),
    ("产业链全景图谱", "节点深度下钻与动态演进"): ("环节下钻", "graph"),
    ("产业周期分析", "周期模型自定义与报告生成"): ("周期分析报告", "report"),
    ("产业周期分析", "周期趋势模拟预测"): ("周期预测", "model"),
    ("区域产业指数评价", "评价体系构建与指标配置"): ("区域产业指数", "config"),
    ("区域产业指数评价", "多区域多产业对比与结果呈现"): ("区域产业对比", "compare"),
    ("产业关键环节识别", "全链路环节结构化展示"): ("标准环节图谱", "graph"),
    ("产业关键环节识别", "关键环节智能标注与分析"): ("关键环节报告", "report"),
    ("产业瓶颈堵点识别", "多维度瓶颈综合分析"): ("环节健康度", "detect"),
    ("产业瓶颈堵点识别", "瓶颈智能识别与归因建议"): ("产业瓶颈", "detect"),
    ("深圳产业情况分析对比", "深圳数据专项提取与多维对标"): ("深圳产业对标", "compare"),
    ("深圳产业情况分析对比", "深圳产业化潜力与发展阶段综合判断"): ("深圳产业阶段", "report"),
    ("深圳产业发展分析", "智能建议推荐与发展路径规划"): ("产业发展路径", "list"),
    ("区域产业竞争力评价", "多维竞争力指标体系构建"): ("区域竞争力指标", "config"),
    ("区域产业竞争力评价", "综合竞争力计算与横向排名"): ("区域竞争力排名", "compare"),
    ("重点企业类型分析", "产业与企业类型筛选"): ("企业类型筛选", "list"),
    ("重点企业类型分析", "三级地理透视与可视化呈现"): ("企业地理分布", "graph"),
    ("重点企业领域分布分析", "企业业务关联与领域覆盖计算"): ("企业领域覆盖", "model"),
    ("企业技术力评估对比分析", "技术力模型构建与参数自定义"): ("技术力指标", "config"),
    ("企业技术力评估对比分析", "多企业技术力对比分析"): ("企业技术力对比", "compare"),
    ("企业商业力评估对比分析", "商业力模型配置与指标选择"): ("商业力指标", "config"),
    ("企业商业力评估对比分析", "商业竞争力对标分析"): ("企业商业力对标", "compare"),
    ("深圳企业现状分析", "深圳企业产业链定位"): ("深圳企业定位", "list"),
    ("深圳企业现状分析", "多城市横向对标分析"): ("深圳企业城市对标", "compare"),
    ("招引企业推荐分析", "高潜力企业智能挖掘"): ("招引企业挖掘", "model"),
    ("招引企业推荐分析", "招引名单与价值分析"): ("招引企业名单", "list"),
    ("培育企业推荐分析", "本地潜力企业识别模型"): ("培育企业识别", "model"),
    ("培育企业推荐分析", "培育建议清单生成"): ("培育企业名单", "list"),
    ("企业供应链关系分析", "供应链图谱构建与多级下钻"): ("供应链图谱", "graph"),
    ("企业供应链关系分析", "关键节点与断链风险识别"): ("断链风险", "detect"),
    ("企业发展痛难点分析", "智能痛难点诊断模型"): ("痛难点诊断", "detect"),
    ("企业发展痛难点分析", "分析建议报告输出"): ("痛难点报告", "report"),
    ("企业竞争力分析", "综合评估框架与指标库"): ("企业竞争力指标", "config"),
    ("企业竞争力分析", "个性化竞争力评价与输出"): ("企业竞争力评价", "compare"),
    ("政策时序分析", "政策数据自动关联"): ("政策数据关联", "data"),
    ("政策时序分析", "时序模型智能分析"): ("政策时序", "model"),
    ("区域政策对比", "跨区域政策采集"): ("区域政策采集", "data"),
    ("区域政策对比", "标准化对比分析"): ("区域政策对比", "compare"),
    ("深圳政策现状分析", "指标体系构建"): ("深圳政策指标", "config"),
    ("深圳政策现状分析", "深圳政策对标"): ("深圳政策报告", "report"),
    ("深圳政策现状分析", "结果可视化输出"): ("深圳政策仪表盘", "viz"),
    ("服务机构产业领域分析", "服务机构产业领域覆盖分析"): ("机构覆盖分析", "model"),
    ("服务机构产业领域分析", "服务机构产业领域分析结果呈现"): ("机构覆盖图", "viz"),
    ("服务机构新增趋势分析", "趋势可视化呈现"): ("机构新增趋势", "viz"),
    ("服务机构新增趋势分析", "市场热度判断"): ("服务市场热度", "detect"),
    ("服务机构技术力评估分析", "多维度评价模型"): ("机构技术力指标", "config"),
    ("服务机构技术力评估分析", "自定义对比分析"): ("机构技术力对比", "compare"),
    ("服务链短板分析", "全链路可视化呈现"): ("服务链全链路", "graph"),
    ("服务链短板分析", "瓶颈堵点智能识别"): ("服务链堵点", "detect"),
    ("服务链图谱分析", "关系网络构建"): ("服务机构关系图谱", "graph"),
    ("服务链图谱分析", "图谱探索与统计"): ("服务网络统计", "graph"),
    ("引入服务机构推荐分析", "招引模型与指标"): ("机构招引指标", "config"),
    ("引入服务机构推荐分析", "推荐名单生成"): ("引进机构名单", "list"),
    ("培育服务机构推荐分析", "培育模型与筛选"): ("机构培育指标", "config"),
    ("培育服务机构推荐分析", "培育名单与建议"): ("机构培育名单", "list"),
    ("深圳服务链现状分析", "统一评价框架"): ("服务链评价口径", "framework"),
    ("深圳服务链现状分析", "横向对比分析"): ("深圳服务链对标", "compare"),
    ("区域创新活力分析", "指标体系构建"): ("创新活力指标", "config"),
    ("区域创新活力分析", "综合评价模型"): ("创新活力模型", "model"),
    ("区域创新活力分析", "区域指数计算与可视化"): ("创新活力指数", "compare"),
    ("区域创新要素分析", "创新要素数据汇聚"): ("创新要素汇聚", "data"),
    ("区域创新要素分析", "要素评价模型构建"): ("创新要素评价", "config"),
    ("区域创新要素分析", "要素影响关联分析"): ("创新要素影响", "detect"),
    ("区域创新协同分析", "创新主体关系图谱"): ("创新协同图谱", "graph"),
    ("区域创新协同分析", "协同度计算模型"): ("创新协同指数", "model"),
    ("区域创新协同分析", "协同效果评估"): ("协同效率报告", "report"),
}


def load_v5_cores() -> dict[tuple[str, str], list[str]]:
    p = Path(__file__).with_name("_gen_zt_fp_split_v5.py")
    spec = importlib.util.spec_from_file_location("fpv5", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.HAND_SPLITS


def infer_dim(fp: str) -> str:
    """对齐门户原则 §7 / §8.1 拆分维度用词。"""
    pairs = (
        ("校验", "校验"),
        ("清空", "筛选"),
        ("重置", "筛选"),
        ("筛选", "筛选"),
        ("选择", "筛选"),
        ("选定", "筛选"),
        ("选取", "筛选"),
        ("勾选", "筛选"),
        ("升序", "排序"),
        ("降序", "排序"),
        ("倒序", "排序"),
        ("失败", "异常"),
        ("为空提示", "空态"),
        ("无匹配", "空态"),
        ("暂无", "空态"),
        ("加载状态", "状态"),
        ("生成中", "状态"),
        ("计算中", "状态"),
        ("处理中", "状态"),
        ("进度", "状态"),
        ("页码", "查询"),
        ("每页", "查询"),
        ("点击", "定位"),
        ("下钻", "定位"),
        ("定位", "定位"),
        ("高亮", "展示规则"),
        ("截断", "展示规则"),
        ("展开", "展示规则"),
        ("限制", "展示规则"),
        ("图例", "展示"),
        ("展示单条", "展示"),
        ("展示", "展示"),
        ("呈现", "展示"),
        ("可视化", "展示"),
        ("抓取", "数据"),
        ("提取", "数据"),
        ("采集", "数据"),
        ("汇聚", "数据"),
        ("计算", "算法"),
        ("评估", "算法"),
        ("分析", "算法"),
        ("识别", "算法"),
        ("判断", "算法"),
        ("预测", "算法"),
        ("过滤", "算法"),
        ("生成完整", "输出"),
        ("生成报告", "输出"),
        ("导出", "输出"),
        ("给出", "输出"),
        ("提供", "字段"),
        ("纳入", "字段"),
        ("回显", "字段"),
        ("赋权", "字段"),
        ("权重", "字段"),
        ("默认", "排序"),
        ("记录", "日志"),
        ("提交", "动作"),
        ("保存", "动作"),
        ("组合", "动作"),
        ("查看", "展示"),
        ("输出", "输出"),
    )
    for k, dim in pairs:
        if k in fp:
            return dim
    return "动作"


def portal_extras(label: str, kind: str) -> list[tuple[str, str, str]]:
    """
    门户原则：
    - §4.6 规则层 / §4.8 隐含验收 / §5.13 空态异常
    - §5.3 展示类字段、点击明细
    - §5.7 对象+指标+维度+展示+下钻+输出；交互含筛选/排序/下钻/高亮/重置
    - §8.1 搜索结果展示样例密度（加载/空/失败/总数/单条/升序/降序/截断）
    升序、降序分别计数（§5.1）。
    不补收藏/订阅/分享等原文未涉及业务（§4.8 不允许）。
    """
    rows = [
        (f"展示{label}加载状态", "状态", "验收补充"),
        (f"展示{label}为空提示", "空态", "验收补充"),
        (f"展示{label}加载失败提示", "异常", "验收补充"),
        (f"展示单条{label}结果", "展示", "原文隐含"),
        (f"展示{label}结果总数", "展示", "原文隐含"),
        (f"高亮{label}选中项", "展示规则", "原文隐含"),
        (f"限制{label}超长内容截断展示", "展示规则", "验收补充"),
        (f"展开查看完整{label}内容", "展示规则", "验收补充"),
        (f"记录{label}操作日志", "日志", "原文隐含"),
    ]
    by_kind = {
        "graph": [
            (f"展示{label}图例", "展示", "原文隐含"),
            (f"展示{label}节点名称", "字段展示", "原文隐含"),
            (f"点击{label}节点查看明细", "定位", "原文隐含"),
            (f"高亮{label}断点或选中节点", "展示规则", "原文隐含"),
            (f"导出{label}数据", "输出", "原文隐含"),
        ],
        "viz": [
            (f"展示{label}图例", "展示", "原文隐含"),
            (f"点击{label}数据点查看明细", "定位", "原文隐含"),
            (f"展示{label}坐标或刻度", "字段展示", "原文隐含"),
            (f"导出{label}数据", "输出", "原文隐含"),
        ],
        "compare": [
            (f"默认按得分倒序展示{label}", "排序", "验收补充"),
            (f"按得分升序排序{label}", "排序", "验收补充"),
            (f"按得分降序排序{label}", "排序", "验收补充"),
            (f"清空{label}对比对象", "筛选", "原文隐含"),
            (f"重置{label}筛选条件", "筛选", "原文隐含"),
        ],
        "list": [
            (f"默认按得分倒序展示{label}", "排序", "验收补充"),
            (f"按得分升序排序{label}", "排序", "验收补充"),
            (f"按得分降序排序{label}", "排序", "验收补充"),
            (f"清空{label}筛选条件", "筛选", "原文隐含"),
            (f"重置{label}筛选条件", "筛选", "原文隐含"),
            (f"切换{label}结果页码", "查询", "验收补充"),
            (f"设置{label}每页显示条数", "查询", "验收补充"),
        ],
        "config": [
            (f"校验{label}不能为空", "校验", "原文隐含"),
            (f"校验{label}权重取值范围", "校验", "验收补充"),
            (f"回显{label}已配置参数", "字段", "原文隐含"),
            (f"展示{label}保存失败提示", "异常", "验收补充"),
        ],
        "report": [
            (f"校验{label}必要章节齐全", "校验", "原文隐含"),
            (f"展示{label}章节标题", "字段展示", "原文隐含"),
            (f"未完成分析时不可生成{label}", "校验", "原文隐含"),
        ],
        "detect": [
            (f"高亮{label}识别标记", "展示规则", "原文隐含"),
            (f"展示{label}识别结果列表", "展示", "原文隐含"),
        ],
        "model": [
            (f"接收{label}输入参数", "动作", "原文隐含"),
            (f"过滤{label}无效结果", "算法", "原文隐含"),
            (f"生成{label}分析结论", "算法", "原文隐含"),
            (f"校验{label}输入参数完整", "校验", "原文隐含"),
        ],
        "data": [
            (f"展示{label}采集进度", "状态", "验收补充"),
            (f"展示{label}采集失败提示", "异常", "验收补充"),
            (f"展示{label}入库条数", "展示", "原文隐含"),
            (f"校验{label}数据源可用", "校验", "原文隐含"),
        ],
        "framework": [
            (f"展示{label}口径说明", "展示", "原文隐含"),
            (f"校验对比分析前口径一致", "校验", "原文隐含"),
            (f"展示口径不一致不可比提示", "异常", "验收补充"),
        ],
    }
    rows.extend(by_kind.get(kind, []))
    return rows


def too_similar(fp: str, existing: list[str]) -> bool:
    n = re.sub(r"\s+", "", fp)
    for e in existing:
        en = re.sub(r"\s+", "", e)
        if n == en:
            return True
        if len(n) >= 10 and (n in en or en in n):
            return True
    return False


def expand_one(key: tuple[str, str], cores: list[str]) -> list[tuple[str, str, str]]:
    label, kind = KIND[key]
    rows: list[tuple[str, str, str]] = []
    existing: list[str] = []
    for fp in cores:
        item = (fp, infer_dim(fp), "原文直接")
        rows.append(item)
        existing.append(fp)
    for fp, dim, src in portal_extras(label, kind):
        if too_similar(fp, existing):
            continue
        rows.append((fp, dim, src))
        existing.append(fp)
    return rows


def norm(s: str) -> str:
    return re.sub(r"\s+", "", str(s or "").strip())


def load_function_tree() -> list[dict]:
    wb = openpyxl.load_workbook(SRC, data_only=True, read_only=True)
    ws = wb["科技专题服务系统"]
    rows = list(ws.iter_rows(values_only=True))
    header_idx = 0
    for i, row in enumerate(rows[:5]):
        if "需规功能描述" in "".join(str(x or "") for x in row[:14]):
            header_idx = i
            break
    cur = [""] * 6
    items = []
    for row in rows[header_idx + 1 :]:
        vals = list(row) + [None] * 20
        levels = [norm(vals[idx]) if vals[idx] else "" for idx in (6, 7, 8, 9, 10, 11)]
        for j, v in enumerate(levels):
            if v:
                cur[j] = v
                for k in range(j + 1, 6):
                    cur[k] = ""
        if cur[3] not in L4_TARGETS:
            continue
        desc = str(vals[12]).strip() if vals[12] else ""
        if not (cur[4] or cur[5] or desc):
            continue
        items.append({"l4": cur[3], "l5": cur[4] or "/", "l6": cur[5] or "/", "desc": desc})
    wb.close()
    return items


def build_rows(items: list[dict], v5: dict) -> list[dict]:
    rows = []
    missing = []
    for it in items:
        key = (it["l5"], it["l6"])
        if key not in KIND:
            missing.append(key)
            continue
        cores = v5.get(key) or []
        for fp, dim, src in expand_one(key, cores):
            rows.append(
                {
                    "功能模块": MODULE,
                    "子功能模块": it["l4"],
                    "功能项": it["l5"],
                    "子功能项": it["l6"],
                    "页面": it["l5"],
                    "功能点": fp,
                    "拆分维度": dim,
                    "规则来源": src,
                    "需规描述": it["desc"],
                }
            )
    if missing:
        raise SystemExit("缺少 KIND: " + "; ".join(f"{a}/{b}" for a, b in missing))
    n = len(rows)
    if not (TARGET_LO <= n <= TARGET_HI):
        print(f"WARN count={n} not in {TARGET_LO}-{TARGET_HI}")
    return rows


def write_excel(rows: list[dict]) -> None:
    wb = openpyxl.load_workbook(TPL)
    ws = wb["功能测试用例"]
    ws["A1"] = A1_TITLE
    if ws.max_row > 2:
        ws.delete_rows(3, ws.max_row - 2)
    for rng in list(ws.merged_cells.ranges):
        if str(rng).startswith("A1:"):
            ws.unmerge_cells(str(rng))
    ws.insert_cols(8, amount=3)
    ws.merge_cells("A1:T1")
    ws["A1"] = A1_TITLE
    headers = [
        "用例编号",
        "功能模块",
        "子功能模块",
        "功能项",
        "子功能项",
        "页面",
        "功能点",
        "拆分维度",
        "规则来源",
        "需规描述",
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
    for col, h in enumerate(headers, start=1):
        cell = ws.cell(2, col, h)
        cell.font = Font(bold=True)
    align = Alignment(wrap_text=True, vertical="top")
    for i, r in enumerate(rows, start=1):
        rec = {"用例编号": f"ZNFWJQ-KJZTFWXT-v1.0-FUNC-{i:05d}", **r}
        for col, h in enumerate(headers, start=1):
            cell = ws.cell(i + 2, col, rec.get(h, "") or "")
            cell.alignment = align
    widths = [36, 18, 16, 22, 22, 20, 36, 12, 12, 56]
    for col, w in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(col)].width = w
    for name in wb.sheetnames:
        if name in ("功能测试用例", "规则 -0529"):
            continue
        wso = wb[name]
        if wso.max_row > 2:
            wso.delete_rows(3, wso.max_row - 2)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    wb.save(OUT)
    wb.close()


def main():
    v5 = load_v5_cores()
    items = load_function_tree()
    rows = build_rows(items, v5)
    write_excel(rows)
    by_l4 = defaultdict(int)
    by_src = defaultdict(int)
    for r in rows:
        by_l4[r["子功能模块"]] += 1
        by_src[r["规则来源"]] += 1
    print(f"src={len(items)} fps={len(rows)} -> {OUT}")
    for k in L4_TARGETS:
        print(f"  {k}: {by_l4.get(k, 0)}")
    print("来源", dict(by_src))


if __name__ == "__main__":
    main()

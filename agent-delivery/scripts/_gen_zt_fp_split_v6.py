# -*- coding: utf-8 -*-
"""功能点拆分 v6：按《科技专题战略分析-最细颗粒度功能点拆分原则-v1》扩到约 1200 条。"""
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
    / "6.国际科技信息中心项目_科技专题服务系统_功能点拆分_v6.xlsx"
)

L4_TARGETS = ["产业服务链分析", "产业链分析", "企业分析", "政策分析", "综合智能分析"]
MODULE = "科技专题战略分析"
A1_TITLE = "智能服务集群-科技专题服务系统功能点拆分"
TARGET_LO, TARGET_HI = 1140, 1260


def load_v5_cores() -> dict[tuple[str, str], list[str]]:
    p = Path(__file__).with_name("_gen_zt_fp_split_v5.py")
    spec = importlib.util.spec_from_file_location("fpv5", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.HAND_SPLITS


# 六级 → (短对象名, 类型)
KIND: dict[tuple[str, str], tuple[str, str]] = {
    ("产业链全景图谱", "产业链结构可视化"): ("产业链图谱", "graph"),
    ("产业链全景图谱", "节点深度下钻与动态演进"): ("环节下钻", "graph"),
    ("产业周期分析", "周期模型自定义与报告生成"): ("产业周期", "report"),
    ("产业周期分析", "周期趋势模拟预测"): ("周期预测", "model"),
    ("区域产业指数评价", "评价体系构建与指标配置"): ("区域产业指数", "config"),
    ("区域产业指数评价", "多区域多产业对比与结果呈现"): ("区域产业对比", "compare"),
    ("产业关键环节识别", "全链路环节结构化展示"): ("标准环节图谱", "graph"),
    ("产业关键环节识别", "关键环节智能标注与分析"): ("关键环节", "report"),
    ("产业瓶颈堵点识别", "多维度瓶颈综合分析"): ("环节健康度", "detect"),
    ("产业瓶颈堵点识别", "瓶颈智能识别与归因建议"): ("产业瓶颈", "detect"),
    ("深圳产业情况分析对比", "深圳数据专项提取与多维对标"): ("深圳产业对标", "compare"),
    ("深圳产业情况分析对比", "深圳产业化潜力与发展阶段综合判断"): ("深圳产业阶段", "report"),
    ("深圳产业发展分析", "智能建议推荐与发展路径规划"): ("深圳发展路径", "list"),
    ("区域产业竞争力评价", "多维竞争力指标体系构建"): ("区域竞争力指标", "config"),
    ("区域产业竞争力评价", "综合竞争力计算与横向排名"): ("区域竞争力排名", "compare"),
    ("重点企业类型分析", "产业与企业类型筛选"): ("企业类型筛选", "list"),
    ("重点企业类型分析", "三级地理透视与可视化呈现"): ("企业地理分布", "graph"),
    ("重点企业领域分布分析", "企业业务关联与领域覆盖计算"): ("企业领域覆盖", "model"),
    ("企业技术力评估对比分析", "技术力模型构建与参数自定义"): ("技术力模型", "config"),
    ("企业技术力评估对比分析", "多企业技术力对比分析"): ("企业技术力对比", "compare"),
    ("企业商业力评估对比分析", "商业力模型配置与指标选择"): ("商业力模型", "config"),
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
    ("深圳政策现状分析", "深圳政策对标"): ("深圳政策对标", "report"),
    ("深圳政策现状分析", "结果可视化输出"): ("深圳政策仪表盘", "viz"),
    ("服务机构产业领域分析", "服务机构产业领域覆盖分析"): ("机构覆盖分析", "model"),
    ("服务机构产业领域分析", "服务机构产业领域分析结果呈现"): ("机构覆盖呈现", "viz"),
    ("服务机构新增趋势分析", "趋势可视化呈现"): ("机构新增趋势", "viz"),
    ("服务机构新增趋势分析", "市场热度判断"): ("服务市场热度", "detect"),
    ("服务机构技术力评估分析", "多维度评价模型"): ("机构技术力模型", "config"),
    ("服务机构技术力评估分析", "自定义对比分析"): ("机构技术力对比", "compare"),
    ("服务链短板分析", "全链路可视化呈现"): ("服务链全链路", "graph"),
    ("服务链短板分析", "瓶颈堵点智能识别"): ("服务链堵点", "detect"),
    ("服务链图谱分析", "关系网络构建"): ("服务机构关系图谱", "graph"),
    ("服务链图谱分析", "图谱探索与统计"): ("服务网络统计", "graph"),
    ("引入服务机构推荐分析", "招引模型与指标"): ("机构招引模型", "config"),
    ("引入服务机构推荐分析", "推荐名单生成"): ("引进机构名单", "list"),
    ("培育服务机构推荐分析", "培育模型与筛选"): ("机构培育模型", "config"),
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

# 原则 §8 样例：这些六级用样例条目替换 v5 核心，避免与规则层叠床架屋。
SAMPLE_CORES: dict[tuple[str, str], list[tuple[str, str, str]]] = {
    ("企业技术力评估对比分析", "技术力模型构建与参数自定义"): [
        ("展示技术力指标库", "展示", "原文直接"),
        ("提供专利数量指标", "字段", "原文直接"),
        ("提供专利引用指标", "字段", "原文直接"),
        ("提供研发人员占比指标", "字段", "原文直接"),
        ("提供核心技术覆盖度指标", "字段", "原文直接"),
        ("组合已选技术力指标", "动作", "原文直接"),
        ("为已选指标设置权重", "字段", "原文直接"),
        ("校验至少选择一个指标", "校验", "原文隐含"),
        ("校验指标权重之和为100%", "校验", "原文隐含"),
        ("实时计算技术力得分", "算法", "原文直接"),
        ("展示技术力得分", "展示", "原文隐含"),
        ("未选指标时不可计算得分", "校验", "原文隐含"),
        ("展示指标库为空提示", "空态", "验收补充"),
        ("展示技术力计算中状态", "状态", "验收补充"),
        ("展示技术力计算失败提示", "异常", "验收补充"),
        ("默认勾选预设技术力指标", "默认", "验收补充"),
    ],
    ("企业发展痛难点分析", "分析建议报告输出"): [
        ("分析企业发展痛难点问题", "算法", "原文直接"),
        ("分析问题成因", "算法", "原文直接"),
        ("参考行业最佳实践", "算法", "原文直接"),
        ("推荐解决方案", "算法", "原文直接"),
        ("在报告中展示问题描述", "展示", "原文直接"),
        ("在报告中展示成因分析", "展示", "原文直接"),
        ("在报告中展示行业最佳实践", "展示", "原文直接"),
        ("在报告中展示解决方案", "展示", "原文直接"),
        ("生成分析结果的完整报告", "输出", "原文直接"),
        ("校验报告四段内容齐全", "校验", "原文隐含"),
        ("展示报告生成中状态", "状态", "验收补充"),
        ("展示报告生成失败提示", "异常", "验收补充"),
        ("展示暂无痛难点分析数据", "空态", "验收补充"),
        ("未完成诊断时不可生成报告", "校验", "原文隐含"),
    ],
}


def infer_dim(fp: str) -> str:
    pairs = (
        ("校验", "校验"),
        ("默认", "默认"),
        ("失败", "异常"),
        ("暂无", "空态"),
        ("为空", "空态"),
        ("进行中", "状态"),
        ("生成中", "状态"),
        ("计算中", "状态"),
        ("加载", "状态"),
        ("降序", "排序"),
        ("升序", "排序"),
        ("对齐", "排序"),
        ("导出", "输出"),
        ("生成完整", "输出"),
        ("生成周期", "输出"),
        ("生成差距", "输出"),
        ("生成关键", "输出"),
        ("生成政策", "输出"),
        ("生成引进", "输出"),
        ("生成协同", "输出"),
        ("抓取", "数据"),
        ("提取", "数据"),
        ("采集", "数据"),
        ("汇聚", "数据"),
        ("建立动态", "数据"),
        ("点击", "定位"),
        ("下钻", "定位"),
        ("展开", "定位"),
        ("钻取", "定位"),
        ("筛选", "筛选"),
        ("选择", "筛选"),
        ("选定", "筛选"),
        ("选取", "筛选"),
        ("勾选", "筛选"),
        ("计算", "算法"),
        ("评估", "算法"),
        ("分析", "算法"),
        ("识别", "算法"),
        ("判断", "算法"),
        ("预测", "算法"),
        ("标注", "算法"),
        ("诊断", "算法"),
        ("统计", "算法"),
        ("量化", "算法"),
        ("展示", "展示"),
        ("呈现", "展示"),
        ("以雷达", "展示"),
        ("以图表", "展示"),
        ("以柱状", "展示"),
        ("可视化", "展示"),
        ("提供", "字段"),
        ("纳入", "字段"),
        ("构建", "字段"),
        ("设置", "字段"),
        ("设定", "字段"),
        ("组合", "动作"),
        ("重置", "动作"),
        ("输入", "动作"),
        ("查看", "展示"),
        ("输出", "输出"),
        ("给出", "输出"),
        ("绘制", "展示"),
        ("拆解", "动作"),
        ("形成", "展示"),
        ("跟踪", "动作"),
        ("更新图谱", "数据"),
        ("高亮", "展示"),
    )
    for k, dim in pairs:
        if k in fp:
            return dim
    return "动作"


def base_rules(obj: str) -> list[tuple[str, str, str]]:
    return [
        (f"选择{obj}作为分析对象", "筛选", "原文隐含"),
        (f"校验必须选择{obj}", "校验", "原文隐含"),
        (f"未选择{obj}时不可开始分析", "校验", "原文隐含"),
        (f"展示当前{obj}分析范围", "展示", "原文隐含"),
        (f"展示{obj}分析结果", "展示", "原文隐含"),
        (f"展示{obj}暂无数据提示", "空态", "验收补充"),
        (f"展示{obj}分析进行中状态", "状态", "验收补充"),
        (f"展示{obj}分析失败提示", "异常", "验收补充"),
        (f"默认使用预设{obj}分析参数", "默认", "验收补充"),
        (f"重置{obj}分析条件", "动作", "原文隐含"),
    ]


def kind_rules(kind: str, obj: str) -> list[tuple[str, str, str]]:
    extra = {
        "graph": [
            (f"展示{obj}图例", "展示", "原文隐含"),
            (f"高亮选中{obj}节点", "展示", "原文隐含"),
            (f"未选中节点时不可下钻", "校验", "原文隐含"),
            (f"展示{obj}图谱加载失败提示", "异常", "验收补充"),
            (f"展示{obj}节点数量", "展示", "原文隐含"),
        ],
        "config": [
            (f"组合已选{obj}指标", "动作", "原文直接"),
            (f"为{obj}指标设置权重", "字段", "原文直接"),
            (f"校验至少选择一项{obj}指标", "校验", "原文隐含"),
            (f"校验{obj}权重之和为100%", "校验", "原文隐含"),
            (f"未配置指标时不可计算{obj}", "校验", "原文隐含"),
            (f"默认勾选预设{obj}指标", "默认", "验收补充"),
        ],
        "compare": [
            (f"校验{obj}对比对象不少于两项", "校验", "原文隐含"),
            (f"展示{obj}对比结果数量", "展示", "原文隐含"),
            (f"按得分降序排列{obj}对比结果", "排序", "验收补充"),
            (f"按得分升序排列{obj}对比结果", "排序", "验收补充"),
        ],
        "list": [
            (f"展示{obj}名单条数", "展示", "原文隐含"),
            (f"按综合得分降序排列{obj}", "排序", "验收补充"),
            (f"按综合得分升序排列{obj}", "排序", "验收补充"),
            (f"限制{obj}最大展示条数", "展示", "验收补充"),
        ],
        "report": [
            (f"校验{obj}报告必要内容齐全", "校验", "原文隐含"),
            (f"未完成分析时不可生成{obj}报告", "校验", "原文隐含"),
            (f"展示{obj}报告生成中状态", "状态", "验收补充"),
            (f"展示{obj}报告生成失败提示", "异常", "验收补充"),
        ],
        "detect": [
            (f"展示{obj}识别结果列表", "展示", "原文隐含"),
            (f"高亮{obj}识别标记", "展示", "原文隐含"),
            (f"展示未识别到{obj}结果提示", "空态", "验收补充"),
            (f"展示{obj}识别结果数量", "展示", "原文隐含"),
        ],
        "model": [
            (f"提交{obj}计算请求", "动作", "原文隐含"),
            (f"展示{obj}计算依据或分项", "展示", "原文隐含"),
            (f"校验{obj}输入参数完整", "校验", "原文隐含"),
            (f"展示{obj}模型计算失败提示", "异常", "验收补充"),
        ],
        "data": [
            (f"校验{obj}数据源可用", "校验", "原文隐含"),
            (f"展示{obj}采集进度", "状态", "验收补充"),
            (f"展示{obj}采集失败提示", "异常", "验收补充"),
            (f"展示{obj}入库条数", "展示", "原文隐含"),
        ],
        "viz": [
            (f"展示{obj}图表", "展示", "原文隐含"),
            (f"展示{obj}图例", "展示", "原文隐含"),
            (f"展示{obj}图表加载失败提示", "异常", "验收补充"),
            (f"点击{obj}数据点查看明细", "定位", "原文隐含"),
        ],
        "framework": [
            (f"展示{obj}口径说明", "展示", "原文隐含"),
            (f"校验对比分析前口径一致", "校验", "原文隐含"),
            (f"展示口径不一致不可比提示", "异常", "验收补充"),
        ],
    }
    return extra.get(kind, [])


def cores_have_select(cores: list[str]) -> bool:
    return any(any(k in c for k in ("选择", "选定", "勾选", "筛选", "选取", "设定")) for c in cores)


def too_similar(fp: str, existing: list[str]) -> bool:
    n = re.sub(r"\s+", "", fp)
    for e in existing:
        en = re.sub(r"\s+", "", e)
        if n == en:
            return True
        if len(n) >= 8 and (n in en or en in n):
            return True
    return False


def expand_one(key: tuple[str, str], v5: list[str]) -> list[tuple[str, str, str]]:
    obj, kind = KIND[key]
    rows: list[tuple[str, str, str]] = []
    existing: list[str] = []
    if key in SAMPLE_CORES:
        return list(SAMPLE_CORES[key])
    dated = [(fp, infer_dim(fp), "原文直接") for fp in v5]
    for item in dated:
        rows.append(item)
        existing.append(item[0])
    extras = base_rules(obj) + kind_rules(kind, obj)
    skip_select = cores_have_select(existing)
    for fp, dim, src in extras:
        if skip_select and fp.startswith(("选择", "校验必须选择", "未选择")):
            continue
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
    missing_kind = []
    missing_v5 = []
    for it in items:
        key = (it["l5"], it["l6"])
        if key not in KIND:
            missing_kind.append(key)
            continue
        cores = v5.get(key)
        if cores is None and key not in SAMPLE_CORES:
            missing_v5.append(key)
            cores = []
        for fp, dim, src in expand_one(key, cores or []):
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
    if missing_kind:
        raise SystemExit("缺少 KIND: " + "; ".join(f"{a}/{b}" for a, b in missing_kind))
    if missing_v5:
        raise SystemExit("缺少 v5 核心: " + "; ".join(f"{a}/{b}" for a, b in missing_v5))
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
    # 功能点后插入：拆分维度、规则来源、需规描述
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

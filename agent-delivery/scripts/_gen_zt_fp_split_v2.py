# -*- coding: utf-8 -*-
"""功能点拆分 v2：更细拆分 + 通用中文表述；只填到功能点，不写用例步骤；只做正向。"""
from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path

import openpyxl
import yaml
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
QA_DIR = ORCH / "qa" / "total-set" / "KJZTFWXT"
CATALOG = QA_DIR / "prototype-catalog-zt-strategy.yaml"
PACK_INDEX = QA_DIR / "product-pack-index-zt-strategy.yaml"
PACK_ROOT = ORCH / "agent-handoffs" / "产品整体定义"
OUT = QA_DIR / "6.国际科技信息中心项目_科技专题服务系统_功能点拆分_v2.xlsx"

L4_TARGETS = ["产业服务链分析", "产业链分析", "企业分析", "政策分析", "综合智能分析"]
MODULE = "科技专题战略分析"
A1_TITLE = "智能服务集群-科技专题服务系统功能点拆分"

SKIP_TEXT = re.compile(
    r"评审模式|内部禁用|Frame|DOM|review mount|有效高度|像素|review_copy|"
    r"内部禁用词|产品解释作为需求|业务模式禁止|不得把|不得用|不得在|"
    r"异常|空态|无匹配|无效|失败|缺数据|缺坐标|非法|阻塞|降级|"
    r"Q0\d+|GAP-|metric_id|MockBadge|Pending|calc_batch"
)
GENERIC_FOCUS = {"区域", "分析", "企业", "选择", "查看", "系统", "页面"}

# 复合控件 → 细拆原子
CONTROL_EXPAND = {
    "区域与企业类型": ["区域选择", "企业类型选择"],
    "匹配企业数/覆盖类型数/覆盖区域数": ["匹配企业数指标", "覆盖企业类型数指标", "覆盖区域数指标"],
    "地图视图与列表视图": ["地图视图", "列表视图"],
    "数量/占比/集聚指数": ["按数量查看", "按占比查看", "按集聚指数查看"],
    "国家/省/市/区县层级": ["国家级浏览", "省级下钻", "市级下钻", "区县点位查看"],
    "企业/高校科研机构/人才/资本 四卡片": ["企业要素卡片", "高校科研机构要素卡片", "人才要素卡片", "资本要素卡片"],
    "主体类型 Checkbox": ["企业主体勾选", "高校主体勾选", "人才主体勾选", "服务机构主体勾选"],
    "领域覆盖/新增趋势/技术力评估": ["领域覆盖页签", "新增趋势页签", "技术力评估页签"],
    "链路短板/生态图谱/深圳现状对比": ["链路短板页签", "生态图谱页签", "深圳现状对比页签"],
    "链位分析 | 城市对标": ["链位分析页签", "城市对标页签"],
    "产业周期/关键环节/瓶颈堵点/诊断记录": ["产业周期页签", "关键环节页签", "瓶颈堵点页签", "诊断记录页签"],
    "外企/高企/小微/上市": ["外企类型", "高企类型", "小微类型", "上市类型"],
}

# 重点企业类型等：八件套/原型正向细拆补点（catalog 未拆到的控件）
EXTRA_ATOMS = {
    "重点企业类型分析": [
        ("产业与企业类型筛选", "在顶部筛选区选择区域范围"),
        ("产业与企业类型筛选", "在顶部筛选区选择时间范围"),
        ("产业与企业类型筛选", "在顶部筛选区多选产业"),
        ("产业与企业类型筛选", "在顶部筛选区勾选企业类型（外企）"),
        ("产业与企业类型筛选", "在顶部筛选区勾选企业类型（高企）"),
        ("产业与企业类型筛选", "在顶部筛选区勾选企业类型（小微）"),
        ("产业与企业类型筛选", "在顶部筛选区勾选企业类型（上市）"),
        ("产业与企业类型筛选", "确认筛选条件后刷新匹配企业集合"),
        ("产业与企业类型筛选", "重置筛选条件恢复默认"),
        ("三级地理透视与可视化呈现", "在地图上从国家下钻到省级"),
        ("三级地理透视与可视化呈现", "在地图上从省下钻到市级"),
        ("三级地理透视与可视化呈现", "在市层继续查看区县企业点位"),
        ("三级地理透视与可视化呈现", "通过面包屑或返回上一级回到上级区域"),
        ("三级地理透视与可视化呈现", "切换到地图视图查看空间分布"),
        ("三级地理透视与可视化呈现", "切换到列表视图查看同层区域明细"),
        ("三级地理透视与可视化呈现", "按企业数量查看地图着色与列表"),
        ("三级地理透视与可视化呈现", "按企业占比查看地图着色与列表"),
        ("三级地理透视与可视化呈现", "按集聚指数查看地图着色与列表"),
        ("三级地理透视与可视化呈现", "查看匹配企业数指标"),
        ("三级地理透视与可视化呈现", "查看覆盖企业类型数指标"),
        ("三级地理透视与可视化呈现", "查看覆盖区域数指标"),
        ("三级地理透视与可视化呈现", "查看当前区域企业类型结构饼图"),
        ("三级地理透视与可视化呈现", "对区域企业列表排序"),
        ("三级地理透视与可视化呈现", "对区域企业列表翻页"),
        ("三级地理透视与可视化呈现", "打开当前区域企业清单"),
        ("三级地理透视与可视化呈现", "在企业清单中搜索或筛选企业"),
        ("三级地理透视与可视化呈现", "在企业清单中多选企业"),
        ("三级地理透视与可视化呈现", "将选中企业加入对比篮"),
        ("三级地理透视与可视化呈现", "打开企业详情侧滑面板"),
    ],
    "重点企业领域分布分析": [
        ("企业业务关联与领域覆盖计算", "从对比篮选择一家或多家企业作为分析对象"),
        ("企业业务关联与领域覆盖计算", "查看已选企业摘要"),
        ("企业业务关联与领域覆盖计算", "打开对比篮调整分析对象"),
        ("企业业务关联与领域覆盖计算", "查看领域布局概览"),
        ("企业业务关联与领域覆盖计算", "查看企业领域覆盖"),
        ("企业业务关联与领域覆盖计算", "查看跨领域布局"),
        ("企业业务关联与领域覆盖计算", "查看重点领域分布"),
        ("企业业务关联与领域覆盖计算", "打开领域识别依据"),
        ("企业业务关联与领域覆盖计算", "从领域依据打开企业详情"),
    ],
    "区域创新活力分析": [
        ("区域创新活力指数测算", "在顶部筛选选择目标区域"),
        ("区域创新活力指数测算", "在顶部筛选选择对比范围"),
        ("区域创新活力指数测算", "在顶部筛选选择时间窗"),
        ("区域创新活力指数测算", "查看创新活力综合指数仪表盘"),
        ("区域创新活力指数测算", "查看梯队评级"),
        ("区域创新活力指数测算", "查看同比变化"),
        ("多区域创新活力对比", "查看区域排名榜"),
        ("多区域创新活力对比", "点击排名卡片切换当前区域"),
        ("多区域创新活力对比", "展开或折叠分层指标"),
        ("多区域创新活力对比", "生成分析报告"),
    ],
    "区域创新要素分析": [
        ("创新要素结构分析", "查看企业要素卡片"),
        ("创新要素结构分析", "查看高校科研机构要素卡片"),
        ("创新要素结构分析", "查看人才要素卡片"),
        ("创新要素结构分析", "查看资本要素卡片"),
        ("创新要素结构分析", "打开要素详情"),
        ("创新要素结构分析", "查看四维评价雷达图"),
        ("创新要素结构分析", "浏览要素影响关联路径"),
    ],
    "区域创新协同分析": [
        ("创新主体协同网络构建", "按产业筛选协同网络"),
        ("创新主体协同网络构建", "勾选企业主体类型"),
        ("创新主体协同网络构建", "勾选高校主体类型"),
        ("创新主体协同网络构建", "勾选人才主体类型"),
        ("创新主体协同网络构建", "勾选服务机构主体类型"),
        ("创新主体协同网络构建", "点击图谱节点查看详情"),
        ("创新主体协同网络构建", "查看协同度指标"),
    ],
    "政策时序分析": [
        ("政策数据自动关联", "选择目标产业或技术领域"),
        ("政策数据自动关联", "查看自动关联的政策文件列表"),
        ("时序模型智能分析", "按发布时间查看政策时序"),
        ("时序模型智能分析", "查看政策密度指数"),
        ("时序模型智能分析", "查看支持强度趋势图"),
        ("时序模型智能分析", "打开政策详情"),
    ],
    "区域政策对比": [
        ("多区域政策采集与标准化", "选择两个及以上对比区域"),
        ("多区域政策采集与标准化", "查看多区域标准化对比图"),
        ("多区域政策采集与标准化", "查看对比指标说明"),
    ],
    "深圳政策现状分析": [
        ("深圳政策三维可视化", "查看政策数量指标"),
        ("深圳政策三维可视化", "查看覆盖领域指标"),
        ("深圳政策三维可视化", "选择对标城市"),
        ("深圳政策三维可视化", "查看城市对标表或雷达图"),
    ],
    "产业链全景图谱": [
        ("产业链结构可视化", "选择要查看的产业链"),
        ("产业链结构可视化", "在图谱中查看环节节点与连线"),
        ("节点深度下钻与动态演进", "点击环节节点下钻查看关联企业"),
        ("节点深度下钻与动态演进", "点击环节节点查看主流技术路线"),
        ("节点深度下钻与动态演进", "点击环节节点查看市场规模"),
        ("节点深度下钻与动态演进", "按时间或版本查看图谱演进"),
    ],
    "产业周期分析": [
        ("周期模型自动导入与报告输出", "填写市场规模参数"),
        ("周期模型自动导入与报告输出", "填写增长率参数"),
        ("周期模型自动导入与报告输出", "提交参数启动周期分析"),
        ("多情景模拟预测", "查看周期趋势图"),
        ("多情景模拟预测", "查看未来产业预测结果"),
        ("多情景模拟预测", "查看关键驱动因素"),
        ("多情景模拟预测", "查看潜在拐点"),
        ("多情景模拟预测", "导出或打开分析报告"),
    ],
    "深圳企业现状分析": [
        ("产业链角色标注与企业清单", "切换到链位分析"),
        ("产业链角色标注与企业清单", "选择产业链"),
        ("产业链角色标注与企业清单", "查看企业清单及链角色标注"),
        ("产业链角色标注与企业清单", "全选当前结果企业"),
        ("产业链角色标注与企业清单", "批量加入对比篮"),
        ("产业链角色标注与企业清单", "打开企业详情"),
        ("多城市企业生态对标", "切换到城市对标"),
        ("多城市企业生态对标", "选择对标城市"),
        ("多城市企业生态对标", "查看雷达图或对标表"),
    ],
    "企业技术力评估对比分析": [
        ("技术力评估模型选择与参数配置", "进入企业技术力评估对比分析"),
        ("技术力评估模型选择与参数配置", "选择或切换技术力评估模型"),
        ("技术力评估模型选择与参数配置", "查看技术力评估维度说明"),
        ("多企业技术力雷达对比", "查看多企业技术力雷达图"),
        ("多企业技术力雷达对比", "打开参评企业详情"),
    ],
    "企业商业力评估对比分析": [
        ("商业力评估指标体系构建", "选择商业力评估指标"),
        ("商业力评估指标体系构建", "查看商业力得分卡"),
        ("多企业商业竞争力对比", "开展多企业商业力对比"),
        ("多企业商业竞争力对比", "查看对标结果说明"),
    ],
    "企业竞争力分析": [
        ("综合竞争力评估框架", "进入企业竞争力分析"),
        ("综合竞争力评估框架", "查看综合评估指标库"),
        ("综合竞争力评估框架", "输出个性化评价结果"),
    ],
    "招引企业推荐分析": [
        ("高潜力企业挖掘模型", "进入招引企业推荐分析"),
        ("高潜力企业挖掘模型", "调整招引条件"),
        ("高潜力企业挖掘模型", "查看招引推荐名单"),
        ("高潜力企业挖掘模型", "查看推荐价值依据"),
        ("高潜力企业挖掘模型", "将推荐企业加入对比篮"),
    ],
    "培育企业推荐分析": [
        ("本地潜力企业识别", "切换到培育企业推荐"),
        ("本地潜力企业识别", "调整培育条件"),
        ("本地潜力企业识别", "查看培育建议名单"),
    ],
    "企业供应链关系分析": [
        ("供应链图谱构建与多级下钻", "进入企业供应链关系分析"),
        ("供应链图谱构建与多级下钻", "选择 1 到 2 家企业作为分析对象"),
        ("供应链图谱构建与多级下钻", "查看供应商关系"),
        ("供应链图谱构建与多级下钻", "查看客户关系"),
        ("供应链图谱构建与多级下钻", "查看合作伙伴关系"),
        ("供应链图谱构建与多级下钻", "点击节点展开下一级关系"),
        ("断链风险识别与预警", "查看关键节点标识"),
        ("断链风险识别与预警", "查看断链风险提示"),
    ],
    "企业发展痛难点分析": [
        ("痛难点智能诊断模型", "进入企业发展痛难点分析"),
        ("痛难点智能诊断模型", "发起痛难点诊断"),
        ("痛难点智能诊断模型", "查看问题清单"),
        ("痛难点智能诊断模型", "查看分析建议报告"),
    ],
    "产业关键环节识别": [
        ("全链路环节结构图展示", "切换到关键环节分析"),
        ("全链路环节结构图展示", "查看研发、制造、流通等标准环节结构图"),
        ("关键环节智能标注与解析", "查看高亮的关键环节"),
        ("关键环节智能标注与解析", "查看环节功能边界说明"),
        ("关键环节智能标注与解析", "查看环节经济贡献或企业清单"),
    ],
    "产业瓶颈堵点识别": [
        ("五维瓶颈扫描与归因", "切换到瓶颈堵点分析"),
        ("五维瓶颈扫描与归因", "按技术维度查看堵点"),
        ("五维瓶颈扫描与归因", "按人才维度查看堵点"),
        ("五维瓶颈扫描与归因", "按市场维度查看堵点"),
        ("五维瓶颈扫描与归因", "按资本维度查看堵点"),
        ("五维瓶颈扫描与归因", "按政策维度查看堵点"),
        ("五维瓶颈扫描与归因", "查看堵点归因建议"),
    ],
    "区域产业指数评价": [
        ("可配置指标体系与指数计算", "进入区域产业指数评价"),
        ("可配置指标体系与指数计算", "展开或配置指标树"),
        ("可配置指标体系与指数计算", "查看指标权重与得分"),
        ("多区域产业指数对比与报告", "选择对比区域"),
        ("多区域产业指数对比与报告", "查看雷达图或对比表"),
    ],
    "区域产业竞争力评价": [
        ("多维竞争力评估模型", "查看综合竞争力排名"),
        ("多维竞争力评估模型", "切换竞争力评价维度"),
        ("多维竞争力评估模型", "查看维度得分卡"),
    ],
    "深圳产业情况分析对比": [
        ("多维对标分析", "进入深圳产业情况分析对比"),
        ("多维对标分析", "选择对比城市或产业"),
        ("多维对标分析", "查看深圳专项数据与对标结果"),
    ],
    "深圳产业发展分析": [
        ("智能建议与路径规划", "查看发展路径或阶段节点"),
        ("智能建议与路径规划", "查看智能建议"),
        ("智能建议与路径规划", "导出或打开报告"),
    ],
    "服务机构产业领域分析": [
        ("服务机构领域覆盖分析", "切换到领域覆盖"),
        ("服务机构领域覆盖分析", "选择待分析机构"),
        ("服务机构领域覆盖分析", "查看领域覆盖结果"),
    ],
    "服务机构新增趋势分析": [
        ("服务机构新增趋势分析", "切换到新增趋势"),
        ("服务机构新增趋势分析", "查看趋势图"),
        ("服务机构新增趋势分析", "查看市场热度判断"),
    ],
    "服务机构技术力评估分析": [
        ("服务机构技术力多维评价", "切换到技术力评估"),
        ("服务机构技术力多维评价", "选择机构进行对比"),
        ("服务机构技术力多维评价", "查看多维评价结果"),
    ],
    "服务链短板分析": [
        ("服务链全链路瓶颈识别", "切换到链路短板"),
        ("服务链全链路瓶颈识别", "查看全链路图谱"),
        ("服务链全链路瓶颈识别", "查看短板或堵点标识"),
    ],
    "服务链图谱分析": [
        ("服务生态网络图谱构建", "切换到生态图谱"),
        ("服务生态网络图谱构建", "点击环节节点查看详情"),
        ("服务生态网络图谱构建", "查看节点与关系统计"),
    ],
    "引入服务机构推荐分析": [
        ("服务机构招引推荐", "填写引入需求或招引指标"),
        ("服务机构招引推荐", "查看推荐机构名单"),
        ("服务机构招引推荐", "查看匹配理由"),
    ],
    "培育服务机构推荐分析": [
        ("本地服务机构培育建议", "调整培育模型条件"),
        ("本地服务机构培育建议", "查看培育名单与建议"),
    ],
    "深圳服务链现状分析": [
        ("深圳服务链横向对比", "切换到深圳现状对比"),
        ("深圳服务链横向对比", "选择对比城市"),
        ("深圳服务链横向对比", "在统一评价框架下查看对比结果"),
    ],
}


def norm(s: str) -> str:
    return re.sub(r"\s+", "", str(s or "").strip())


def biz_text(s: str) -> str:
    """通用中文：去掉内部编号、组件名、URL/参数、Given/When/Then。"""
    if not s:
        return ""
    t = str(s)
    # 先去掉代码式片段
    t = re.sub(r"`+", "", t)
    t = re.sub(r"\*{1,2}([^*]+)\*{1,2}", r"\1", t)
    t = re.sub(r"GOV\s*[×xX]\s*L\d+", "政府用户权限", t)
    t = re.sub(r"INNO\s*[×xX]\s*L\d+", "创新用户权限", t)
    t = re.sub(r"[A-Z]{2,}\s*[×xX]\s*L\d+", "", t)
    t = re.sub(r"\bK-O\d+\b", "", t)
    t = re.sub(r"USM-\d+", "", t)
    t = re.sub(r"DEC-[A-Z0-9\-]+", "", t)
    t = re.sub(r"PI-\d+", "", t)
    t = re.sub(r"F-\d+", "", t)
    t = re.sub(r"Q0\d+", "", t)
    t = re.sub(r"GAP-[A-Z0-9\-]+", "", t)
    t = re.sub(r"metric_id", "指标说明", t)
    t = re.sub(r"Given\s*", "在", t)
    t = re.sub(r"When\s*", "当", t)
    t = re.sub(r"Then\s*", "则", t)
    t = re.sub(r"workspace=[\w\-&=]+", "对应分析页", t)
    t = re.sub(r"recommendation_tab=[\w\-]+", "对应推荐页签", t)
    t = re.sub(r"\?tab=[\w\-]+|tab=[\w\-/]+", "对应页签", t)
    t = re.sub(r"URL\s*/[^\s；。,，]*", "进入对应页面", t)
    t = re.sub(r"URL\s*", "", t)
    t = re.sub(r"source=cleared", "清空后", t)
    t = re.sub(r"enterprise_codes(?:\[\])?", "当前所选企业", t)
    repls = [
        (r"ContextBar", "顶部筛选"),
        (r"Cascader", "级联选择"),
        (r"Checkbox", "复选框"),
        (r"\bSelect\b", "下拉选择"),
        (r"DatePicker", "日期选择"),
        (r"\bRadio\b", "单选"),
        (r"\bTable\b", "列表"),
        (r"\bDrawer\b", "侧滑详情"),
        (r"ForceGraph", "关系图谱"),
        (r"\bG6\s*", ""),
        (r"OrgPickerModal", "机构选择窗"),
        (r"\bModal\b", "弹窗"),
        (r"placeholder", "提示文字"),
        (r"processing", "计算中"),
        (r"StageDetailDrawer", "环节详情"),
        (r"emptyGate", "未选对象提示"),
        (r"Mock\s*", ""),
        (r"aria-current/?", ""),
        (r"两个分析类型\s*Tab|分析类型\s*Tab|页内Tab「?类型与区域分析」?", "侧栏「重点企业类型分析」"),
        (r"点击[“\"]?领域分布分析[”\"]?\s*Tab", "侧栏「重点企业领域分析」"),
        (r"\[原型\]\s*|\[USM[^\]]*\]\s*|\[需规\]\s*|\[IA\]\s*|\[UX\]\s*", ""),
    ]
    for pat, repl in repls:
        t = re.sub(pat, repl, t)
    t = re.sub(r"\s+", " ", t)
    t = re.sub(r"[；;]{2,}", "；", t)
    return t.strip(" ；;、，./|")


def is_positive(text: str) -> bool:
    if not text:
        return False
    if SKIP_TEXT.search(text):
        return False
    # 残留内部编号
    if re.search(
        r"用户权限$|认证后|级产业 \+|配置任务 \+|采用标签|查看画像”|内部编号|数据截至",
        text,
    ):
        return False
    if re.search(r"[A-Z]{2,}[×xX]L\d+|workspace=|tab=|source=|`|\*\*|placeholder|Modal", text):
        return False
    return True


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


def load_catalog() -> dict:
    data = yaml.safe_load(CATALOG.read_text(encoding="utf-8"))
    return {
        "pages": data.get("pages") or {},
        "overlays": data.get("l6_overlays") or {},
        "nav_prefix": data.get("nav_prefix") or {},
    }


def load_pack_index() -> dict:
    return (yaml.safe_load(PACK_INDEX.read_text(encoding="utf-8")) or {}).get("l5") or {}


def resolve_page(catalog: dict, l5: str) -> dict | None:
    pages = catalog["pages"]
    if l5 in pages:
        return pages[l5]
    for k, v in pages.items():
        if norm(k) == norm(l5) or k in l5 or l5 in k:
            return v
    return None


def page_name(catalog: dict, l5: str) -> str:
    p = resolve_page(catalog, l5)
    if p and p.get("menu"):
        return str(p["menu"])
    return l5


def split_desc(desc: str) -> list[str]:
    """需规长句拆成多条可验收能力点。"""
    if not desc:
        return []
    text = desc.replace("\r", "\n")
    # 先按句号/分号
    chunks = re.split(r"[。；;\n]+", text)
    out: list[str] = []
    for chunk in chunks:
        chunk = chunk.strip(" 、，,")
        if len(chunk) < 6:
            continue
        # 并列连接
        pieces = re.split(
            r"(?:同时，?|并且|以及，?|并支持|还支持|此外，?|另外，?)",
            chunk,
        )
        for p in pieces:
            p = re.sub(
                r"^(该功能|本功能|此功能|用户可以|用户可|系统将|系统可|系统能够|系统应|系统)",
                "",
                p,
            ).strip(" 、，,")
            if len(p) < 6:
                continue
            # 「包含A与B」「展示A、B、C」继续拆
            m = re.search(r"(包含|含有|展示|呈现|支持|提供|输出)([^，。；]{8,})", p)
            if m and ("、" in m.group(2) or "与" in m.group(2) or "和" in m.group(2)):
                head = p[: m.start()].strip(" ，,")
                verb = m.group(1)
                items = re.split(r"[、，,/]|与|和", m.group(2))
                items = [x.strip() for x in items if len(x.strip()) >= 2]
                if len(items) >= 2:
                    if head and len(head) >= 6:
                        out.append(head)
                    for it in items:
                        out.append(f"{verb}{it}")
                    # 尾巴（如「支撑…」）
                    tail = p[m.end() :].strip(" ，,")
                    if len(tail) >= 6:
                        out.append(tail)
                    continue
            # 长句按逗号拆成「动作 + 结果」
            if len(p) > 48 and p.count("，") >= 1:
                parts = [x.strip() for x in p.split("，") if len(x.strip()) >= 6]
                if len(parts) >= 2:
                    out.extend(parts)
                    continue
            out.append(p)
    seen, uniq = set(), []
    for x in out:
        x = biz_text(x)
        if not is_positive(x) or len(x) < 6:
            continue
        k = norm(x)
        if k in seen:
            continue
        seen.add(k)
        uniq.append(x)
    return uniq


def keyword_score(text: str, key: str) -> int:
    if not key or key in ("/", ""):
        return 0
    t, k = text or "", key
    n = 0
    if k in t:
        n += 3
    for ch in re.findall(r"[\u4e00-\u9fff]{2,}", k):
        if ch in t:
            n += 1
    return n


def pick_l6(l6s: list[str], text: str) -> str:
    if not l6s:
        return "/"
    ranked = sorted(l6s, key=lambda x: keyword_score(text, x), reverse=True)
    if keyword_score(text, ranked[0]) > 0:
        return ranked[0]
    return l6s[0]


def expand_control(control: str) -> list[str]:
    c = (control or "").strip()
    if not c:
        return []
    if c in CONTROL_EXPAND:
        return CONTROL_EXPAND[c]
    # A/B/C 或 A | B
    if "/" in c or "|" in c:
        parts = re.split(r"[/|]", c)
        parts = [p.strip() for p in parts if len(p.strip()) >= 2]
        if len(parts) >= 2:
            return parts
    # 「区域与企业类型」类
    if "与" in c and 4 <= len(c) <= 20:
        parts = [p.strip() for p in c.split("与") if len(p.strip()) >= 2]
        if len(parts) == 2:
            return [f"{parts[0]}选择", f"{parts[1]}选择"]
    return [c]


def zone_to_fps(z: dict) -> list[str]:
    """原型 zone → 多条正向功能点。"""
    zone = biz_text(z.get("zone") or "")
    control = z.get("control") or zone
    action = biz_text(z.get("action") or "")
    expect = biz_text(z.get("expect") or "")
    if SKIP_TEXT.search(str(z.get("expect") or "") + str(z.get("action") or "")):
        # 空态/异常类期望跳过
        if re.search(r"空态|无匹配|无效|非法|失败|暂无", str(z.get("expect") or "")):
            return []
    fps = []
    controls = expand_control(str(control))
    for ctl in controls:
        ctl = biz_text(ctl)
        if not ctl:
            continue
        # 控件本身作为可操作元素
        if action:
            fps.append(f"在「{zone or '页面'}」使用「{ctl}」完成：{action}")
        else:
            fps.append(f"在「{zone or '页面'}」提供「{ctl}」")
        if expect and len(expect) >= 6:
            # 期望再拆短句
            for e in re.split(r"[；;]", expect):
                e = biz_text(e)
                if len(e) >= 6 and is_positive(e):
                    fps.append(f"「{ctl}」操作后：{e}")
    return fps


def gwt_to_plain(body: str) -> list[str]:
    """Given/When/Then → 正向业务描述，尽量拆开。"""
    body = biz_text(body)
    if not is_positive(body):
        return []
    # 已转成 在…当…则…
    parts = re.split(r"(?=在|当|则)", body)
    out = []
    for p in parts:
        p = p.strip(" ，,")
        if len(p) < 8:
            continue
        p = re.sub(r"^在", "支持在", p)
        p = re.sub(r"^当", "当用户", p)
        p = re.sub(r"^则", "系统", p)
        if is_positive(p):
            out.append(p)
    if not out and 8 <= len(body) <= 160 and is_positive(body):
        out.append(body)
    return out


def extract_usm_points(md: str) -> list[str]:
    pts: list[str] = []
    # 跳过「异常与降级」「业务模式禁止」整段
    skip_sec = False
    for line in md.splitlines():
        if re.match(r"^##+\s*(异常|业务模式禁止|需求拆分|USM 自检)", line):
            skip_sec = True
            continue
        if skip_sec and re.match(r"^##+\s+", line) and not re.match(
            r"^##+\s*(异常|业务模式禁止|需求拆分|USM 自检)", line
        ):
            skip_sec = False
        if skip_sec:
            continue
        # 验收表
        if line.startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) < 3:
                continue
            if cells[0] in ("ID", "用户故事", "场景") or set(cells[0]) <= {"-", ":"}:
                continue
            body = cells[2]
            for p in gwt_to_plain(body):
                pts.append(p)
            continue
    return pts


def load_pack_points(l5: str, index: dict) -> list[str]:
    meta = index.get(l5)
    if not meta:
        for k, v in index.items():
            if norm(k) == norm(l5) or k in l5 or l5 in k:
                meta = v
                break
    if not meta:
        return []
    d = PACK_ROOT / meta["dir"]
    if not d.is_dir():
        return []
    pts = []
    focus = [k for k in (meta.get("focus") or []) if k and k not in GENERIC_FOCUS]
    for usm in sorted(d.glob("USM-*.md")):
        text = usm.read_text(encoding="utf-8")
        for p in extract_usm_points(text):
            if focus and not any(k in p for k in focus):
                continue
            pts.append(p)
    seen, uniq = set(), []
    for p in pts:
        p = biz_text(p)
        if not is_positive(p):
            continue
        k = norm(p)
        if k in seen:
            continue
        seen.add(k)
        uniq.append(p)
    return uniq


def overlay_points(catalog: dict, l6: str) -> list[str]:
    ov = catalog["overlays"].get(l6) or {}
    out = []
    for p in ov.get("points") or []:
        fp = biz_text(p.get("功能点") or "")
        content = biz_text(p.get("测试内容") or "")
        if fp and is_positive(fp):
            out.append(fp)
        if content and is_positive(content) and content != fp:
            out.append(content)
        # 步骤里的控件也可拆（仅正向动词行）
        steps = str(p.get("步骤") or "")
        for line in steps.split("\n"):
            line = biz_text(re.sub(r"^\d+[\.、]\s*", "", line))
            if re.search(r"登录|进入侧栏", line):
                continue
            if is_positive(line) and 6 <= len(line) <= 80:
                out.append(line)
    return out


def build_rows(items: list[dict], catalog: dict, index: dict) -> list[dict]:
    by_l5 = defaultdict(list)
    for it in items:
        by_l5[(it["l4"], it["l5"])].append(it)

    rows = []
    seen = set()

    def add(l4, l5, l6, page, fp):
        fp = biz_text(fp)
        if not is_positive(fp) or len(fp) < 6:
            return
        if len(fp) > 120:
            # 过长叙述再按逗号切开，避免整句堆在一条
            parts = [x.strip() for x in re.split(r"[，,]", fp) if len(x.strip()) >= 8]
            if len(parts) >= 2:
                for p in parts:
                    add(l4, l5, l6, page, p)
                return
        # 过短碎片
        if len(fp) < 8 and not re.search(r"[\u4e00-\u9fff]{4,}", fp):
            return
        key = (l4, l5, l6, norm(fp))
        if key in seen:
            return
        seen.add(key)
        rows.append(
            {
                "功能模块": MODULE,
                "子功能模块": l4,
                "功能项": l5,
                "子功能项": l6,
                "页面": page,
                "功能点": fp,
            }
        )

    for (l4, l5), group in by_l5.items():
        page = page_name(catalog, l5)
        l6s = [g["l6"] for g in group]
        proto = resolve_page(catalog, l5)

        # 1) 需规细拆（必须覆盖）
        for g in group:
            clauses = split_desc(g["desc"]) or (
                [biz_text(g["desc"])] if g["desc"] else [g["l6"]]
            )
            for c in clauses:
                add(l4, l5, g["l6"], page, c)
            for ov in overlay_points(catalog, g["l6"]):
                add(l4, l5, g["l6"], page, ov)

        # 2) 原型 zone 细拆
        if proto:
            for z in proto.get("zones") or []:
                blob = " ".join(str(z.get(k) or "") for k in ("zone", "control", "action", "expect"))
                l6 = pick_l6(l6s, blob)
                for fp in zone_to_fps(z):
                    add(l4, l5, l6, page, fp)

        # 3) 八件套正向（验收/主路径/控件），不含异常
        for p in load_pack_points(l5, index):
            add(l4, l5, pick_l6(l6s, p), page, p)

        # 4) 补点：已知高频页面控件
        for l6_hint, fp in EXTRA_ATOMS.get(l5, []):
            l6 = l6_hint if l6_hint in l6s else pick_l6(l6s, fp)
            add(l4, l5, l6, page, fp)

        # 5) 通用正向壳：侧栏进入
        add(l4, l5, l6s[0] if l6s else "/", page, f"从侧栏进入「{page}」页面并展示分析主区")

    return rows


def write_excel(rows: list[dict]) -> None:
    wb = openpyxl.load_workbook(TPL)
    ws = wb["功能测试用例"]
    ws["A1"] = A1_TITLE
    if ws.max_row > 2:
        ws.delete_rows(3, ws.max_row - 2)
    align = Alignment(wrap_text=True, vertical="top")
    headers = [ws.cell(2, c).value for c in range(1, 18)]
    for i, r in enumerate(rows, start=1):
        row_i = i + 2
        rec = {
            "用例编号": f"ZNFWJQ-KJZTFWXT-v1.0-FUNC-{i:05d}",
            "功能模块": r["功能模块"],
            "子功能模块": r["子功能模块"],
            "功能项": r["功能项"],
            "子功能项": r["子功能项"],
            "页面": r["页面"],
            "功能点": r["功能点"],
        }
        for col, h in enumerate(headers, start=1):
            val = rec.get(h, "") if h else ""
            cell = ws.cell(row_i, col, val)
            cell.alignment = align
    for col, w in enumerate([36, 18, 16, 22, 22, 20, 56], start=1):
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
    items = load_function_tree()
    catalog = load_catalog()
    index = load_pack_index()
    rows = build_rows(items, catalog, index)
    write_excel(rows)
    by_l4 = defaultdict(int)
    by_l5 = defaultdict(int)
    for r in rows:
        by_l4[r["子功能模块"]] += 1
        by_l5[r["功能项"]] += 1
    print(f"src_rows={len(items)} fps={len(rows)} -> {OUT}")
    for k in L4_TARGETS:
        print(f"  {k}: {by_l4.get(k, 0)}")
    print("top_l5:")
    for k, v in sorted(by_l5.items(), key=lambda x: -x[1])[:12]:
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()

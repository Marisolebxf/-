import json
import re
from pathlib import Path

repo = Path(r"E:\gkx-lumen\repos\demo-ui-science")
plan = Path(
    r"E:\gkx-lumen\gkx-orchestration\agent-delivery\designs\tech-dev-trend-and-policy-l6-rename-plan.md"
)
out = Path(r"E:\gkx-lumen\gkx-orchestration\scripts\_scan_add_title_result.json")

content = plan.read_text(encoding="utf-8")
pattern = r"\|\s*\d+\s*\|\s*`(1\.1\.1\.1\.4\.[^`]+)`\s*\|\s*\*\*([^*]+)\*\*\s*\|\s*ADD_TITLE"
items = re.findall(pattern, content)

scoped = []
for p in [
    repo / "src" / "App.jsx",
    repo / "src" / "BayAreaInnovation.jsx",
    repo / "src" / "ShenzhenInnovation.tsx",
    repo / "src" / "techDevelopmentTracking.js",
]:
    if p.exists():
        scoped.append(p)

for d in [
    "src/pages/global-innovation",
    "src/pages/tech-index",
    "src/pages/tech-index-new",
    "src/pages/tech-innovation-evaluation",
    "src/pages/tech-innovation-evaluation-new",
    "src/pages/policy-tracking",
    "src/pages/tech-knowledge-graph",
    "src/pages/tech-situation-maintain",
]:
    dp = repo / d
    if dp.exists():
        for f in dp.rglob("*"):
            if f.is_file() and f.suffix in {".js", ".jsx", ".ts", ".tsx", ".vue", ".json"}:
                scoped.append(f)

file_contents = {str(f): f.read_text(encoding="utf-8", errors="ignore") for f in scoped}

MODULE_MAP = [
    ("1.1.1.1.4.1.1", "科技全域态势", ["src/App.jsx", "src/pages/tech-situation-maintain"]),
    ("1.1.1.1.4.1.2", "科学技术全景", ["src/pages/tech-knowledge-graph", "src/App.jsx"]),
    ("1.1.1.1.4.1.3", "技术发展跟踪", ["src/techDevelopmentTracking.js", "src/App.jsx"]),
    ("1.1.1.1.4.1.4", "全球创新监测", ["src/pages/global-innovation"]),
    ("1.1.1.1.4.1.5", "湾区创新监测", ["src/BayAreaInnovation.jsx", "src/pages/global-innovation"]),
    ("1.1.1.1.4.1.6", "深圳创新监测", ["src/ShenzhenInnovation.tsx", "src/pages/global-innovation"]),
    ("1.1.1.1.4.1.7", "科技创新评估", ["src/pages/tech-innovation-evaluation", "src/pages/tech-innovation-evaluation-new"]),
    ("1.1.1.1.4.1.8", "科技指数", ["src/pages/tech-index", "src/pages/tech-index-new"]),
    ("1.1.1.1.4.1.9", "科技发展规划", ["src/App.jsx"]),
    ("1.1.1.1.4.2.1", "科创政策全景", ["src/pages/policy-tracking"]),
    ("1.1.1.1.4.2.2", "政策分析评价", ["src/pages/policy-tracking"]),
    ("1.1.1.1.4.2.3", "政策效果推演", ["src/pages/policy-tracking"]),
    ("1.1.1.1.4.2.4", "政策对比核增", ["src/pages/policy-tracking"]),
]

# keyword hints to locate nearest file for missing titles
HINTS = {
    "放大/缩小": ["zoom", "缩放", "ZoomIn", "ZoomOut"],
    "复位": ["reset", "复位", "归位", "fitBounds"],
    "搜索要素定位": ["search", "定位", "要素", "geocode"],
    "实时数据监控": ["实时", "监控", "monitor", "live"],
    "基础信息查看功能": ["基础信息", "basicInfo", "要素详情"],
    "分析数据展示功能": ["分析数据", "analytics"],
    "监测数据趋势变化查看功能": ["趋势", "trend", "监测"],
    "地图可视化展示功能": ["地图", "map", "MapContainer", "Leaflet"],
    "图结构自动生成": ["自动生成", "autoGenerate", "generateGraph"],
    "默认实体展示": ["默认实体", "defaultEntity", "实体展示"],
    "节点点击交互": ["onClick", "节点点击", "nodeClick"],
    "实体关联关系展示": ["关联关系", "relation", "edge"],
    "关键路径数据接收与处理": ["关键路径", "keyPath", "pathData"],
    "关键节点识别与标记": ["关键节点", "keyNode", "highlight"],
    "路径比较分析": ["路径比较", "pathCompare", "comparePath"],
    "节点属性编辑操作": ["节点属性", "nodeEdit", "属性编辑"],
    "实体关系删除操作": ["关系删除", "deleteRelation", "removeEdge"],
    "实体属性编辑功能": ["实体属性", "entityEdit", "editEntity"],
    "实体关系编辑功能": ["关系编辑", "editRelation", "editEdge"],
    "实体及关系批量管理": ["批量", "batch", "bulk"],
    "地理位置可视化": ["地理位置", "geo", "地图", "map"],
    "实时更新展示": ["实时更新", "liveUpdate", "refresh"],
    "地理标注展示": ["标注", "marker", "annotation"],
    "订阅监测功能": ["订阅", "subscribe", "监测"],
    "数据指标分类展示": ["指标分类", "category", "分类展示"],
    "可视化数据呈现": ["可视化", "chart", "visual"],
    "实时数据更新": ["实时数据", "dataUpdate", "refresh"],
    "城市订阅功能": ["城市订阅", "citySubscribe", "subscribeCity"],
    "地理位置落点展示": ["落点", "marker", "scatter", "地图"],
    "多样化可视化效果": ["可视化效果", "visualEffect", "chartType"],
    "指标预警功能": ["预警", "alert", "warning"],
    "SWOT分析展示": ["SWOT", "swot", "优势", "威胁"],
    "指标体系管理": ["指标体系", "indicatorSystem", "指标管理"],
    "数据计算方式说明": ["计算方式", "calculation", "口径"],
    "多层级地理展示": ["多层级", "层级", "district", "行政区"],
    "指标数据可视化": ["指标数据", "indicatorChart", "可视化"],
    "城市选择功能": ["城市选择", "citySelect", "选择城市"],
    "城市排名展示": ["城市排名", "cityRank", "排名"],
    "指标概述查看": ["指标概述", "overview", "概述"],
    "指标计算方法说明": ["计算方法", "formula", "计算说明"],
    "指标意义解读": ["指标意义", "interpret", "解读"],
    "大屏导航切换": ["大屏", "导航", "screenNav", "dashboard"],
    "可视化结果导出": ["导出", "export", "download"],
    "分类排名展示": ["分类排名", "categoryRank", "rankCategory"],
    "排名历史变化": ["历史变化", "history", "trend"],
    "排名结果导出": ["排名导出", "exportRank"],
    "多维度指标体系展示": ["指标体系", "indicator", "规划"],
    "科创资源整合与推送": ["资源整合", "推送", "resource"],
    "多维度检索条件设置": ["检索条件", "searchCondition", "filter"],
    "洞察结论自动提炼": ["洞察", "insight", "结论提炼"],
    "模块化研报自动撰写": ["研报", "report", "自动撰写"],
}

UI_NOTES = {
    "放大/缩小": "地图工具栏缩放按钮区",
    "复位": "地图复位/归位按钮",
    "搜索要素定位": "地图要素搜索定位输入框",
    "实时数据监控": "图层实时数据监控区",
    "基础信息查看功能": "科创要素基础信息面板",
    "分析数据展示功能": "科创要素分析数据区",
    "监测数据趋势变化查看功能": "监测趋势图表区标题",
    "地图可视化展示功能": "地图可视化主视图区",
    "图结构自动生成": "图谱自动生成操作区",
    "默认实体展示": "关联实体默认展示面板",
    "节点点击交互": "图谱节点点击交互说明/区",
    "实体关联关系展示": "实体关系展示面板",
    "关键路径数据接收与处理": "关键路径数据处理区",
    "关键节点识别与标记": "关键节点标记面板",
    "路径比较分析": "路径对比分析区",
    "节点属性编辑操作": "图谱节点属性编辑面板",
    "实体关系删除操作": "实体关系删除操作区",
    "实体属性编辑功能": "实体属性编辑面板",
    "实体关系编辑功能": "实体关系编辑面板",
    "实体及关系批量管理": "批量管理工具区",
    "地理位置可视化": "创新成果地图可视化",
    "实时更新展示": "实时更新状态/展示区",
    "地理标注展示": "地图标注图层",
    "订阅监测功能": "成果订阅监测面板",
    "数据指标分类展示": "实时数据指标分类Tab",
    "可视化数据呈现": "数据可视化图表区",
    "实时数据更新": "实时数据刷新区",
    "城市订阅功能": "城市订阅面板",
    "地理位置落点展示": "湾区成果地图落点",
    "多样化可视化效果": "可视化效果切换区",
    "指标预警功能": "指标预警提示区",
    "SWOT分析展示": "SWOT四象限分析面板",
    "指标体系管理": "指标体系管理面板",
    "数据计算方式说明": "指标计算说明弹窗/区",
    "多层级地理展示": "深圳载体多层级地图",
    "指标数据可视化": "科技发展指标图表区",
    "城市选择功能": "城市发展分析城市选择器",
    "城市排名展示": "城市排名列表/图表",
    "指标概述查看": "科技指数指标概述",
    "指标计算方法说明": "指数计算方法说明",
    "指标意义解读": "指标意义解读面板",
    "大屏导航切换": "指数大屏导航Tab",
    "可视化结果导出": "可视化导出按钮区",
    "分类排名展示": "排行榜分类Tab",
    "排名历史变化": "排名历史趋势图",
    "排名结果导出": "排名导出按钮",
    "多维度指标体系展示": "发展规划指标体系",
    "科创资源整合与推送": "资源整合推送面板",
    "多维度检索条件设置": "政策检索条件表单",
    "洞察结论自动提炼": "洞察结论提炼面板",
    "模块化研报自动撰写": "研报自动撰写区",
}


def module_for(code):
    for prefix, name, paths in MODULE_MAP:
        if code.startswith(prefix):
            return name, paths
    return "unknown", []


def rel(p):
    return str(Path(p).relative_to(repo)).replace("\\", "/")


def guess_files(title, module_paths):
    hints = HINTS.get(title, [])
    candidates = []
    for fp, text in file_contents.items():
        rp = rel(fp)
        if not any(rp.startswith(mp.replace("src/", "src/")) or rp == mp for mp in module_paths):
            # looser: path contains module segment
            seg = module_paths[0].split("/")[-1] if module_paths else ""
            if seg and seg not in rp and not any(mp in rp for mp in module_paths):
                continue
        score = 0
        for h in hints:
            if h.lower() in text.lower() or h in text:
                score += 1
        if score:
            candidates.append((score, rp))
    candidates.sort(key=lambda x: (-x[0], x[1]))
    if candidates:
        return [c[1] for c in candidates[:3]]
    return module_paths[:2]


results = []
for code, title in items:
    present = title in "\n".join(file_contents.values())
    hit_files = [rel(f) for f, c in file_contents.items() if title in c]
    mod, paths = module_for(code)
    row = {
        "code": code,
        "title": title,
        "present": present,
        "module": mod,
        "suggested_files": hit_files if present else guess_files(title, paths),
        "ui_note": UI_NOTES.get(title, "需增加可见栏目标题"),
    }
    results.append(row)

out.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
missing = [r for r in results if not r["present"]]
print(json.dumps({"total": len(items), "present": len(results)-len(missing), "missing": len(missing), "missing_titles": [r["title"] for r in missing]}, ensure_ascii=False))

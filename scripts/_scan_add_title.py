import re
from pathlib import Path

repo = Path(r"E:\gkx-lumen\repos\demo-ui-science")
plan = Path(
    r"E:\gkx-lumen\gkx-orchestration\agent-delivery\designs\tech-dev-trend-and-policy-l6-rename-plan.md"
)
content = plan.read_text(encoding="utf-8")

pattern = r"\|\s*\d+\s*\|\s*`(1\.1\.1\.1\.4\.[^`]+)`\s*\|\s*\*\*([^*]+)\*\*\s*\|\s*ADD_TITLE"
items = re.findall(pattern, content)
print(f"ADD_TITLE count: {len(items)}")

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

print(f"Scoped files: {len(scoped)}")

file_contents = {}
for f in scoped:
    try:
        file_contents[str(f)] = f.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        pass

all_text = "\n".join(file_contents.values())

MODULE_MAP = [
    ("1.1.1.1.4.1.1", "科技全域态势", "src/App.jsx, src/pages/tech-situation-maintain/**"),
    ("1.1.1.1.4.1.2", "科学技术全景", "src/pages/tech-knowledge-graph/**, src/App.jsx"),
    ("1.1.1.1.4.1.3", "技术发展跟踪", "src/techDevelopmentTracking.js, src/App.jsx"),
    ("1.1.1.1.4.1.4", "全球创新监测", "src/pages/global-innovation/**"),
    ("1.1.1.1.4.1.5", "湾区创新监测", "src/BayAreaInnovation.jsx, src/pages/global-innovation/**"),
    ("1.1.1.1.4.1.6", "深圳创新监测", "src/ShenzhenInnovation.tsx, src/pages/global-innovation/**"),
    ("1.1.1.1.4.1.7", "科技创新评估", "src/pages/tech-innovation-evaluation*/**"),
    ("1.1.1.1.4.1.8", "科技指数", "src/pages/tech-index*/**"),
    ("1.1.1.1.4.1.9", "科技发展规划", "src/App.jsx"),
    ("1.1.1.1.4.2.1", "科创政策全景", "src/pages/policy-tracking/**"),
    ("1.1.1.1.4.2.2", "政策分析评价", "src/pages/policy-tracking/**"),
    ("1.1.1.1.4.2.3", "政策效果推演", "src/pages/policy-tracking/**"),
    ("1.1.1.1.4.2.4", "政策对比核增", "src/pages/policy-tracking/**"),
]

UI_NOTES = {
    "放大/缩小": "地图工具栏缩放按钮区",
    "复位": "地图复位/归位按钮",
    "搜索要素定位": "地图要素搜索定位输入框",
    "多对象图层管理": "图层管理面板标题",
    "实时数据监控": "图层实时数据监控区",
    "数据源灵活配置": "图层数据源配置面板",
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
    "地理分布图展示": "技术评估地理分布图",
    "评估方法详解": "评估方法说明面板",
    "评估参数配置": "评估参数配置表单",
    "地理位置可视化": "创新成果地图可视化",
    "实时更新展示": "实时更新状态/展示区",
    "地理标注展示": "地图标注图层",
    "订阅监测功能": "成果订阅监测面板",
    "数据指标分类展示": "实时数据指标分类Tab",
    "可视化数据呈现": "数据可视化图表区",
    "实时数据更新": "实时数据刷新区",
    "监测模型设置": "创新监测模型配置",
    "城市订阅功能": "城市订阅面板",
    "地理位置落点展示": "湾区成果地图落点",
    "多样化可视化效果": "可视化效果切换区",
    "指标构成分析": "指标构成分析图表",
    "指标预警功能": "指标预警提示区",
    "SWOT分析展示": "SWOT四象限分析面板",
    "指标体系管理": "指标体系管理面板",
    "数据计算方式说明": "指标计算说明弹窗/区",
    "多层级地理展示": "深圳载体多层级地图",
    "指标数据可视化": "科技发展指标图表区",
    "城市选择功能": "城市发展分析城市选择器",
    "城市排名展示": "城市排名列表/图表",
    "经费支持分析": "政策保障经费分析图表",
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
    "检索结果智能排序": "检索结果排序控件",
    "标杆比对功能": "政策标杆比对入口",
    "对标结果可视化展示": "对标结果可视化图表",
    "多维结构关联图": "政策分析关联图",
    "热点问题分析看板": "热点问题看板",
    "分主题分指标互动解读": "分主题解读交互区",
    "多媒体辅助解读": "多媒体解读组件",
    "方案参数自定义模拟": "方案参数模拟面板",
    "可视化分析呈现": "政策对比可视化区",
    "结果智能输出": "对比结果智能输出区",
    "洞察结论自动提炼": "洞察结论提炼面板",
    "模块化研报自动撰写": "研报自动撰写区",
    "研报溯源展示": "研报溯源引用展示",
}


def module_for(code: str):
    for prefix, name, files in MODULE_MAP:
        if code.startswith(prefix):
            return name, files
    return "unknown", "unknown"


results = []
for code, title in items:
    present = title in all_text
    hit_files = [f for f, c in file_contents.items() if title in c]
    mod, files = module_for(code)
    results.append(
        {
            "code": code,
            "title": title,
            "present": present,
            "module": mod,
            "files": files,
            "hit_files": hit_files,
            "ui_note": UI_NOTES.get(title, "需增加可见栏目标题"),
        }
    )

missing = [r for r in results if not r["present"]]
present = [r for r in results if r["present"]]
print(f"Present: {len(present)}, Missing: {len(missing)}")
print()
print("=== PRESENT ===")
for r in present:
    hits = "; ".join(Path(h).name for h in r["hit_files"][:2])
    print(f"YES | {r['code']} | {r['title']} | {hits}")
print()
print("=== MISSING (all) ===")
for r in missing:
    print(f"NO | {r['module']} | {r['code']} | {r['title']} | {r['files']}")

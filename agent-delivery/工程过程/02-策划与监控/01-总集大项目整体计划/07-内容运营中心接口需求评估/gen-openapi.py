#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CMS-JX OpenAPI v1.0 生成器：从《CMS-JX接口规格书.md》v1.5 冻结内容机械转换。
真源 = 规格书 + A5 冻结决策。改契约改本表后重跑：python3 gen-openapi.py > CMS-JX-OpenAPI-v1.0.json
ponytail: 无第三方依赖，输出 JSON（OpenAPI 3.0 兼容，Apifox/Postman/Swagger 可直接导入）。

两档输出（2026-10-19 拆分，久新先接已上线部分）：
  全量版（默认）      ：python3 gen-openapi.py > CMS-JX-OpenAPI-v1.0.json          # 含预告端点
  已上线 live 版      ：LIVE_ONLY=1 python3 gen-openapi.py > CMS-JX-OpenAPI-v1.0-live.json  # 仅已实现端点
未实现端点登记在 PENDING 集合：淮政玮的 EXPIRED + 门户/可视化顺延组。实现合入后从 PENDING 移除并重跑全量版。
"""
import json
import os

# 未实现端点（live 版剔除）：顺延组 TOPN/STATS/PANO/ROSTER 等（POL-EXPIRED 已上线 c18060c，移出）
PENDING = {
    "/api/open/cms/v1/policy/topn",
    "/api/open/cms/v1/policy/stats",
    "/api/open/cms/v1/enterprise/profile",
    "/api/open/cms/v1/enterprise/topn",
    "/api/open/cms/v1/enterprise/panorama",
    "/api/open/cms/v1/enterprise/star-roster",
    "/api/open/cms/v1/enterprise/sz-focus",
    "/api/open/cms/v1/service-org/topn",
}
LIVE_ONLY = os.environ.get("LIVE_ONLY") == "1"

# ---------- 字段定义工具 ----------
def F(name, typ="string", req=False, enum=None, fmt=None, desc=""):
    return {"name": name, "type": typ, "req": req, "enum": enum, "fmt": fmt, "desc": desc}

ARR = "array<string>"

def prop(f):
    t = f["type"]
    p = {}
    if t == ARR:
        p["type"] = "array"; p["items"] = {"type": "string"}
    elif t == "integer":
        p["type"] = "integer"
    elif t == "object":
        p["type"] = "object"; p["additionalProperties"] = True
    else:
        p["type"] = "string"
    if f["fmt"]: p["format"] = f["fmt"]
    if f["enum"]: p["enum"] = f["enum"]
    if f["desc"]: p["description"] = f["desc"]
    return p

def schema_of(fields, include_id=False, readonly=()):
    props, req = {}, []
    if include_id:
        props["id"] = {"type": "string", "description": "业务 ID；真源实体=真源主键；虚拟=cms:{TYPE}-{uuid8}"}
    for f in fields:
        props[f["name"]] = prop(f)
        if f["req"]: req.append(f["name"])
    for r in readonly:
        props[r] = {"type": "string", "description": f"只读回显（不可改）"}
    s = {"type": "object", "properties": props}
    if req: s["required"] = req
    return s

def page_props(fields, readonly=()):
    """list body：筛选 + 分页"""
    return fields, readonly

spec = {
    "openapi": "3.0.3",
    "info": {
        "title": "CMS-JX 内容运营中心接口（智树侧）",
        "version": "1.0.0",
        "description": (
            "契约真源：《CMS-JX接口规格书.md》v1.5 + CMS-JX-OVERLAY-A5-L01 冻结决策。\n"
            "访问：K8s ClusterIP Service gkxlumen-cms（网关不注册 /cms 路由；无用户态流量）。\n"
            "鉴权：全部请求头 X-CMS-Api-Key（必填，缺失/错误→40101 CMS_AUTH_FAILED）；写操作另带 X-CMS-Operator（操作人，缺省 unknown）。\n"
            "动词铁律：全 POST + JSON body，禁止路径参数（业务 id 一律在 body；{entityType}/{domain} 为有限枚举段例外）。\n"
            "响应信封：{code:0,msg:'ok',data:...}；列表 data={total,page,size,records[]}。\n"
            "写语义：实体资源=overlay 覆盖（真源零写）+软删；内容资源=纯 overlay 行。删除被引用→40901 CMS_DELETE_REFUSED（data.reasons 列引用来源）。全部写操作落 cms_op_audit 留痕。"
        ),
    },
    "servers": [{"url": "http://gkxlumen-cms.{namespace}.svc.cluster.local", "description": "集群内 ClusterIP（dev）"}],
    "tags": [],
    "paths": {},
    "components": {
        "schemas": {
            "R": {"type": "object", "properties": {"code": {"type": "integer", "example": 0}, "msg": {"type": "string"}, "data": {}}},
            "PageData": {"type": "object", "properties": {"total": {"type": "integer"}, "page": {"type": "integer"}, "size": {"type": "integer"}, "records": {"type": "array", "items": {}}}},
            "DeleteBody": {"type": "object", "required": ["id", "reason"], "properties": {"id": {"type": "string"}, "reason": {"type": "string", "description": "删除原因（必填，入审计）"}}},
            "DetailBody": {"type": "object", "required": ["id"], "properties": {"id": {"type": "string"}}},
        }
    },
}

paths = spec["paths"]
schemas = spec["components"]["schemas"]

def op(tag, summary, body_schema=None, resp_ref=None, resp_is_page=False, extra_responses=""):
    """构造一个 POST operation"""
    op_obj = {
        "tags": [tag], "summary": summary, "operationId": summary,
        "parameters": [
            {"name": "X-CMS-Api-Key", "in": "header", "required": True, "schema": {"type": "string"}, "description": "静态 API Key（nacos 加密配置）"},
        ],
        "responses": {
            "200": {"description": "成功（信封 R；错误码见 info.description）" + extra_responses,
                    "content": {"application/json": {"schema": {"$ref": "#/components/schemas/R"}}}},
        },
    }
    if body_schema:
        op_obj["parameters"].append({"name": "X-CMS-Operator", "in": "header", "required": False, "schema": {"type": "string"}, "description": "操作人（写操作审计归属；缺省 unknown）"})
        op_obj["requestBody"] = {"required": True, "content": {"application/json": {"schema": body_schema}}}
    if resp_ref:
        op_obj["responses"]["200"]["content"]["application/json"]["schema"] = {
            "type": "object",
            "properties": {"code": {"type": "integer"}, "msg": {"type": "string"},
                           "data": {"$ref": resp_ref} if not resp_is_page else {"$ref": "#/components/schemas/PageData"}},
        }
        if resp_is_page:
            # PageData.records item 指向资源 schema
            pass
    return op_obj

def crud(path, tag, fields, filters=(), readonly=(), list_item_ref=None, create_no_id=False):
    """挂 5 个标准动作。fields=写侧字段；filters=list 筛选；readonly=响应只读回显列"""
    sch_name = path.replace("/", "_").replace("-", "_")
    item_schema = schema_of(fields, include_id=True, readonly=readonly)
    schemas[sch_name] = item_schema
    # list
    list_body = {"type": "object", "properties": {"page": {"type": "integer", "default": 1}, "size": {"type": "integer", "default": 20, "maximum": 100}}}
    for fl in filters:
        list_body["properties"][fl["name"]] = prop(fl)
    paths[f"/api/open/cms/v1/{path}/list"] = {"post": op(tag, f"{tag}·列表", list_body, "#/components/schemas/PageData")}
    paths[f"/api/open/cms/v1/{path}/list"]["post"]["responses"]["200"]["content"]["application/json"]["schema"]["properties"]["data"] = {
        "allOf": [{"$ref": "#/components/schemas/PageData"}], "properties": {"records": {"type": "array", "items": {"$ref": f"#/components/schemas/{sch_name}"}}}}
    # detail
    paths[f"/api/open/cms/v1/{path}/detail"] = {"post": op(tag, f"{tag}·详情", schemas["DetailBody"], f"#/components/schemas/{sch_name}")}
    # create（实体资源 id 服务端生成 → body 不含 id）
    create_body = schema_of(fields)
    paths[f"/api/open/cms/v1/{path}/create"] = {"post": op(tag, f"{tag}·新增", create_body)}
    # update（id + 任意被改字段）
    upd = schema_of(fields); upd["properties"]["id"] = {"type": "string"}; upd["required"] = ["id"]
    paths[f"/api/open/cms/v1/{path}/update"] = {"post": op(tag, f"{tag}·编辑（body 只带被改字段，字段级合并）", upd)}
    # delete
    paths[f"/api/open/cms/v1/{path}/delete"] = {"post": op(tag, f"{tag}·删除（软删+审计；被引用返回 40901）", schemas["DeleteBody"])}

# ================= 写侧 19 单 =================
# §1.1 企业实体
crud("enterprise", "企业实体",
     fields=[F("name", req=True, desc="企业名称；覆盖写 overlay"),
             F("regInfo", desc="工商注册信息摘录"),
             F("founded", fmt="date", desc="成立时间"),
             F("capital", desc="注册资本"),
             F("type", enum=["高新技术企业", "专精特新", "上市公司", "初创企业"], desc="运营分类标签"),
             F("industry", enum=["人工智能", "生物医药", "高端装备", "新能源"], desc="运营行业标签"),
             F("scale", enum=["大型", "中型", "小型"]),
             F("isKey", enum=["是", "否"], desc="是否重点企业"),
             F("flag", enum=["龙头", "潜力", "观察", "风险关注"]),
             F("priority", enum=["P0", "P1", "P2", "P3"]),
             F("reason", desc="标识原因")],
     filters=[F("keyword", desc="模糊搜索（命中 name）"), F("isKey"), F("flag"), F("priority")],
     readonly=["external_id", "province", "city", "area", "org_type", "reg_status", "industry_l1_name", "industry_code", "is_high_tech", "is_little_giant", "is_listed", "is_unicorn", "is_gazelle"])
# §1.2 企业动态
crud("enterprise/news", "企业动态资讯",
     fields=[F("title", req=True), F("company", ARR, req=True, desc="关联企业 org_id 数组（多选）"),
             F("kind", enum=["新闻公告", "财报摘要", "法律诉讼", "行政处罚", "舆情事件"]),
             F("content", req=True), F("risk", enum=["低", "中", "高"]),
             F("status", enum=["有效", "已过期", "已归档"]), F("date", fmt="date"), F("sourceUrl")],
     filters=[F("keyword"), F("kind"), F("risk"), F("status")])
# §1.3 企业专项
crud("enterprise/sz", "深圳企业专项",
     fields=[F("name", req=True, desc="企业 org_id（下拉回填，响应回显名称）"),
             F("district", enum=["南山", "福田", "宝安", "龙岗", "龙华", "光明"]),
             F("industry", req=True), F("park"), F("szNote", desc="docx 扩展字段")],
     filters=[F("keyword"), F("district")])
# §2.1 政策
crud("policy", "政策条目",
     fields=[F("title", req=True), F("body", req=True, desc="正文/粘贴文本"),
             F("attachment", desc="附件 fileId（PDF，上传后引用）"),
             F("publisher", req=True), F("pubDate", fmt="date"), F("docNo"),
             F("sourceUrl"), F("industryTag", ARR, enum=["人工智能", "绿色低碳", "生物医药", "低空经济"]),
             F("regionTag", ARR, enum=["深圳", "广东", "全国"]),
             F("reviewStatus", enum=["待审核", "已校正", "需复核"])],
     filters=[F("keyword"), F("reviewStatus"), F("industryTag", ARR), F("regionTag", ARR), F("status")],
     readonly=["status", "level", "source", "region"])
paths["/api/open/cms/v1/policy/audit-logs/list"] = {"post": op("政策条目", "删除操作审计·列表（只读，含全部写操作留痕）",
    {"type": "object", "properties": {"keyword": {}, "page": {"type": "integer"}, "size": {"type": "integer"}}}, "#/components/schemas/PageData")}
schemas["policy_audit_item"] = {"type": "object", "properties": {"time": {}, "operator": {}, "action": {"description": "CREATE|UPDATE|DELETE..."}, "title": {}, "reason": {}}}
paths["/api/open/cms/v1/policy/audit-logs/list"]["post"]["responses"]["200"]["content"]["application/json"]["schema"]["properties"]["data"] = {
    "allOf": [{"$ref": "#/components/schemas/PageData"}], "properties": {"records": {"type": "array", "items": {"$ref": "#/components/schemas/policy_audit_item"}}}}
# §3.1 服务机构
crud("service-org", "服务机构实体",
     fields=[F("name", req=True), F("founded", fmt="date"), F("contact"),
             F("flag", enum=["是", "否"]), F("priority", enum=["P0", "P1", "P2", "—"]),
             F("type", enum=["孵化器", "加速器", "咨询公司", "检测机构", "路演平台"]),
             F("scope"), F("cert"), F("ability"), F("domain")],
     filters=[F("keyword"), F("type"), F("flag"), F("priority")],
     readonly=["province", "city", "area", "org_size", "phone_num"])
# §3.2/3.3 服务机构资讯/专项
crud("service-org/news", "服务机构动态",
     fields=[F("title", req=True), F("kind", enum=["服务案例", "客户反馈", "培训活动", "路演对接会"]),
             F("org", ARR, req=True, desc="所属机构 org_id 数组"), F("content"), F("date", fmt="date"), F("sourceUrl")],
     filters=[F("keyword"), F("kind")])
crud("service-org/sz", "深圳服务机构专项",
     fields=[F("name", req=True, desc="机构 org_id（下拉回填）"),
             F("type", enum=["孵化器", "加速器", "咨询公司", "检测机构"]), F("domain", req=True),
             F("cert"), F("district", enum=["南山", "福田", "宝安", "龙岗", "龙华"]),
             F("cases", desc="docx 扩展"), F("evaluation", desc="docx 扩展"), F("szNote", desc="docx 扩展")],
     filters=[F("keyword"), F("type"), F("district")])
# §4.1 产品
crud("product", "产品实体",
     fields=[F("name", req=True), F("orgId", desc="归属企业 org_id（虚拟产品必填）"),
             F("models", desc="多型号，逗号分隔"), F("params"), F("chain", desc="环节编码（标准∪自定义）")],
     filters=[F("keyword"), F("chain")])
# §4.2 自定义分类/环节
crud("industry/custom-class", "自定义产业分类",
     fields=[F("code", req=True, desc="建议 CUS-{seq}"), F("name", req=True),
             F("level", enum=["一级", "二级", "三级", "四级", "五级"]), F("parent", desc="上级自定义分类 code；一级为空"), F("order", "integer")])
crud("industry/custom-link", "自定义产业链环节",
     fields=[F("code", req=True, desc="建议 CUS-CHAIN-{seq}"), F("name", req=True), F("definition", req=True), F("order", "integer")])
paths["/api/open/cms/v1/industry/tree-merged"] = {"post": op("自定义产业分类", "合并树（标准只读+自定义，自定义可覆盖排序）", {"type": "object", "properties": {}})}
paths["/api/open/cms/v1/industry/chain-links-merged"] = {"post": op("自定义产业链环节", "合并环节下拉（标准∪自定义）", {"type": "object", "properties": {}})}
# §4.3/4.4 产业资讯/区域名录
crud("industry/news", "产业动态资讯",
     fields=[F("title", req=True), F("kind", enum=["政策", "报告", "重大事件", "市场动态"]),
             F("content", req=True), F("date", fmt="date"), F("status", enum=["有效", "归档"]), F("sourceUrl")],
     filters=[F("keyword"), F("kind"), F("status")])
crud("industry/region-roster", "区域企业名录",
     fields=[F("name", req=True, desc="企业名称（下拉回填或手填）"), F("industry", req=True),
             F("district", enum=["南山", "福田", "宝安", "龙岗", "龙华", "光明"]),
             F("scale", enum=["大型", "中型", "小型", "微型企业"])],
     filters=[F("keyword"), F("district"), F("scale")])

# ================= 图谱三单（{entityType} 有限枚举段） =================
ET = {"name": "entityType", "in": "path", "required": True, "schema": {"type": "string", "enum": ["industry", "enterprise", "policy", "service"]}}
def kg_path(sub):
    return f"/api/open/cms/v1/kg/{{entityType}}/{sub}"
def kg_op(sub, tag, summary, body=None):
    o = op(tag, summary, body)
    o["parameters"].append(ET)
    paths[kg_path(sub)] = {"post": o}

kg_op("stages/list", "图谱·阶段定义", "阶段定义·列表（类型级通用配置）",
      {"type": "object", "properties": {"page": {"type": "integer"}, "size": {"type": "integer"}}})
kg_op("stages/create", "图谱·阶段定义", "阶段定义·新增", schema_of([F("stageName", req=True), F("feature", req=True), F("metric", desc="衡量指标，如：产值增速 > 25%"), F("order", "integer")]))
kg_op("stages/update", "图谱·阶段定义", "阶段定义·编辑", {**schema_of([F("stageName"), F("feature"), F("metric"), F("order", "integer")]), "required": ["id"]})
kg_op("stages/delete", "图谱·阶段定义", "阶段定义·删除", schemas["DeleteBody"])
kg_op("entities", "图谱·实体生命周期", "实体能量列表（实体 join 当前状态）",
      {"type": "object", "properties": {"keyword": {}, "stage": ARR, "page": {"type": "integer"}, "size": {"type": "integer"}}})
kg_op("status/mark", "图谱·实体生命周期", "状态标记（新增或更新当前状态；extra 按类型装专属字段）",
      schema_of([F("entityId", req=True), F("stage", req=True), F("since", fmt="date", req=True), F("event", req=True, desc="关键事件"),
                 F("extra", "object", desc="类型专属：enterprise=financing/operation；industry=stageInfo/linkedMetric；policy=scope/effect；service=scale/customers")]))
kg_op("status/history", "图谱·实体生命周期", "状态历史（时间倒序）",
      {"type": "object", "required": ["entityId"], "properties": {"entityId": {}, "page": {"type": "integer"}, "size": {"type": "integer"}}})
# 关系链
crud_rel_fields = [F("fromEntityId", req=True), F("type", req=True, desc="自由文本：上游供给/合作/竞争（建议从 relation-types 字典取）"), F("toEntityId", req=True),
                   F("status", enum=["新建", "稳定", "强化中", "演进中"], desc="已断裂仅 break 动作置入"), F("since", fmt="date"),
                   F("remark", desc="关系说明（久新前端弹窗必填展示项）")]
kg_op("relations/list", "图谱·关系链", "关系·列表", {"type": "object", "properties": {"keyword": {"description": "命中源/目标实体名"}, "status": {}, "page": {"type": "integer"}, "size": {"type": "integer"}}})
kg_op("relations/detail", "图谱·关系链", "关系·详情", schemas["DetailBody"])
kg_op("relations/create", "图谱·关系链", "关系·新建", schema_of(crud_rel_fields))
_rel_upd = schema_of(crud_rel_fields); _rel_upd["required"] = ["id"]
kg_op("relations/update", "图谱·关系链", "关系·编辑", _rel_upd)
kg_op("relations/delete", "图谱·关系链", "关系·删除（软删+审计；误建清理用）", schemas["DeleteBody"])
kg_op("relations/break", "图谱·关系链", "关系·标记断裂（不物理删，badge 灰化）",
      {"type": "object", "required": ["id", "reason"], "properties": {"id": {}, "reason": {}}})
kg_op("relations/history", "图谱·关系链", "关系·演变历史", schemas["DetailBody"])
kg_op("relation-types/list", "图谱·关系类型字典", "关系类型·列表（该类型全量，order_no ASC）", {"type": "object", "properties": {}})
kg_op("relation-types/create", "图谱·关系类型字典", "关系类型·新增（name 必填；同类型下不可重名）",
      schema_of([F("name", req=True), F("order", "integer")]))
kg_op("relation-types/update", "图谱·关系类型字典", "关系类型·编辑", {**schema_of([F("name"), F("order", "integer")]), "required": ["id"]})
kg_op("relation-types/delete", "图谱·关系类型字典", "关系类型·删除（软删；被关系引用时 40901 拒删）", {**schemas["DeleteBody"], "required": ["id", "reason"]})
kg_op("rel-defs/list", "图谱·关系定义层", "关系定义·列表（含 extra 家族专属字段对象）", {"type": "object", "properties": {}})
kg_op("rel-defs/create", "图谱·关系定义层", "关系定义·新增（name 必填；同类型下不可重名）",
      schema_of([F("name", req=True), F("definition"), F("extra", desc="家族专属字段对象：enterprise=mode/terms; policy=effect/feedback; service=content/effect; industry=participants"), F("order", "integer")]))
kg_op("rel-defs/update", "图谱·关系定义层", "关系定义·编辑", {**schema_of([F("name"), F("definition"), F("extra"), F("order", "integer")]), "required": ["id"]})
kg_op("rel-defs/delete", "图谱·关系定义层", "关系定义·删除（软删；被关系实例引用时 40901 拒删）", {**schemas["DeleteBody"], "required": ["id", "reason"]})
kg_op("relations/insight", "图谱·关系链", "关系·LLM 策略/分析意见（结果落库缓存；关系内容变更自动失效；force=true 强制重生成）",
      {"type": "object", "properties": {"id": {"type": "string", "description": "关系行 id（必填）"}, "force": {"type": "boolean", "description": "true=忽略缓存强制重新生成"}}, "required": ["id"]})
# 属性
kg_op("attrs/list", "图谱·实体属性", "属性·列表（扁平+base/dyn 双分组）",
      {"type": "object", "properties": {"group": {"enum": ["base", "dyn"]}, "page": {"type": "integer"}, "size": {"type": "integer"}}})
kg_op("attrs/create", "图谱·实体属性", "属性·新增",
      schema_of([F("name", req=True), F("group", enum=["base", "dyn"]), F("dtype", enum=["文本", "数值", "整数", "枚举", "日期", "百分比", "多值"]), F("definition", desc="属性业务含义与使用说明"), F("unit", desc="单位；无单位可空"), F("constraint"), F("value")]))
_attr_upd = schema_of([F("name"), F("group", enum=["base", "dyn"]), F("dtype"), F("definition"), F("unit"), F("constraint"), F("value")]); _attr_upd["required"] = ["id"]
kg_op("attrs/update", "图谱·实体属性", "属性·编辑", _attr_upd)
kg_op("attrs/delete", "图谱·实体属性", "属性·删除", schemas["DeleteBody"])
kg_op("attrs/history", "图谱·实体属性", "属性·变更记录/多版本管理（审计倒序；含 version 快照）",
      {"type": "object", "properties": {
          "attrId": {"type": "string", "description": "只看某属性行"},
          "name": {"type": "string", "description": "按属性名精确"},
          "group": {"type": "string", "enum": ["base", "dyn", "basic"], "description": "base/dyn；basic 视同 base（兼容前端）"},
          "page": {"type": "integer"}, "size": {"type": "integer"}}})
kg_op("attrs/current", "图谱·实体属性", "属性·当前值+版本号",
      {"type": "object", "required": ["attrId"], "properties": {"attrId": {"type": "string", "description": "属性行 id"}}})
kg_op("attrs/template", "图谱·实体属性", "属性·下载 CSV 导入模板（属性名称/属性定义/数据类型/单位）",
      {"type": "object", "properties": {}})
kg_op("attrs/import", "图谱·实体属性", "属性·批量导入（rows 或 csv；四列必填；同名更新否则新增）",
      {"type": "object", "properties": {
          "group": {"type": "string", "enum": ["base", "dyn"], "description": "缺省 base"},
          "rows": {"type": "array", "items": {"type": "object", "properties": {
              "name": {"type": "string"}, "definition": {"type": "string"},
              "dtype": {"type": "string"}, "unit": {"type": "string"}}}},
          "csv": {"type": "string", "description": "CSV 原文（含表头；与 rows 二选一）"}}})

kg_op("smart-search/enterprise", "智能搜索", "企业智能搜索（keyword 必填；page/size 可选；转发专题门面原样透传）",
      {"type": "object", "required": ["keyword"], "properties": {"keyword": {"type": "string"}, "country_location_ids": {"type": "array", "items": {"type": "string"}, "description": "久新地区码数组（live-1.6）；不传=不过滤"}, "page": {"type": "integer"}, "size": {"type": "integer"}}})
kg_op("smart-search/industry", "智能搜索", "产业智能搜索（keyword 必填；下游 mode=smart；country_location_ids 收下忽略）",
      {"type": "object", "required": ["keyword"], "properties": {"keyword": {"type": "string"}, "country_location_ids": {"type": "array", "items": {"type": "string"}, "description": "久新地区码数组（live-1.6）；不传=不过滤"}, "page": {"type": "integer"}, "size": {"type": "integer"}}})
kg_op("smart-search/policy", "智能搜索", "政策智能搜索（keyword 必填；page/size 自动换算 limit/offset；仅中国放行）",
      {"type": "object", "required": ["keyword"], "properties": {"keyword": {"type": "string"}, "country_location_ids": {"type": "array", "items": {"type": "string"}, "description": "久新地区码数组（live-1.6）；不传=不过滤"}, "page": {"type": "integer"}, "size": {"type": "integer"}}})
kg_op("smart-search/service", "智能搜索", "服务机构智能搜索（keyword 必填；仅中国放行）",
      {"type": "object", "required": ["keyword"], "properties": {"keyword": {"type": "string"}, "country_location_ids": {"type": "array", "items": {"type": "string"}, "description": "久新地区码数组（live-1.6）；不传=不过滤"}, "page": {"type": "integer"}, "size": {"type": "integer"}}})

# ================= 专家知识（{domain} 有限枚举段） =================
DM = {"name": "domain", "in": "path", "required": True, "schema": {"type": "string", "enum": ["industry", "enterprise", "policy", "service", "region"]}}
ek_fields = [F("sectionId", req=True, desc="section 标识（12 个，见规格 §6.1–§6.5）"), F("title", req=True),
             F("entity", "object", req=True, desc="{entityType, entityId, name}；region 为自由文本"),
             F("expert"), F("content", "object", req=True, desc="按 section 字段定义的有序键值对（键=拼音蛇形）"),
             F("view", desc="缺省取 content 首个非空值"), F("conclusion", desc="缺省取 content 末字段"),
             F("evidence"), F("sourceType"), F("source"), F("advice")]
schemas["expert_item"] = schema_of(ek_fields, include_id=True)
ek_list = {"type": "object", "properties": {"keyword": {}, "sectionId": {}, "page": {"type": "integer"}, "size": {"type": "integer"}}}
for sub, summ, body in [
    ("list", "专家知识·列表", ek_list), ("detail", "专家知识·详情", schemas["DetailBody"]),
    ("create", "专家知识·新增", schema_of(ek_fields)),
    ("update", "专家知识·编辑", {**schema_of(ek_fields), "required": ["id"]}),
    ("delete", "专家知识·删除", schemas["DeleteBody"]),
    ("sections", "section 元数据（id/名称/字段定义有序数组，供前端动态渲染表单）", {"type": "object", "properties": {}}),
]:
    o = op("专家知识", f"专家知识·{summ.split('·')[1] if '·' in summ else summ}", body)
    o["parameters"].append(DM)
    paths[f"/api/open/cms/v1/expert/{{domain}}/{sub}"] = {"post": o}

# ================= 读侧 16 接口（A5-6 全 POST 化） =================
def rd(path, tag, summary, body_props=None):
    body = {"type": "object", "properties": body_props or {}}
    paths[f"/api/open/cms/v1/{path}"] = {"post": op(tag, summary, body)}

rd("enterprise/list", "读侧·企业", "企业列表（join 视角：真源∪虚拟，软删剔除）", {"keyword": {}, "page": {"type": "integer"}, "size": {"type": "integer"}})
_ent_list_schema = paths["/api/open/cms/v1/enterprise/list"]["post"]["responses"]["200"]["content"]["application/json"]["schema"]
_ent_list_schema["properties"] = {"code": {"type": "integer"}, "msg": {"type": "string"},
    "data": {"allOf": [{"$ref": "#/components/schemas/PageData"}], "properties": {"records": {"type": "array", "items": {"$ref": "#/components/schemas/enterprise"}}}}}
rd("enterprise/detail", "读侧·企业", "企业详情", {"id": {}})
rd("enterprise/suggest", "读侧·企业", "企业下拉", {"keyword": {}, "limit": {"type": "integer", "default": 10}})
rd("enterprise/profile", "读侧·企业", "企业基础档案", {"id": {}})
rd("enterprise/products", "读侧·企业", "企业产品名称（真源∪overlay 合并）", {"id": {}})
rd("enterprise/topn", "读侧·企业", "企业技术力/商业力 TopN（算法榜单）", {"keyword": {}, "size": {"type": "integer"}})
rd("enterprise/panorama", "读侧·企业", "企业全景事实包", {"id": {}})
rd("enterprise/star-roster", "读侧·企业", "明星企业名单（CMS 自管语义）", {"page": {"type": "integer"}, "size": {"type": "integer"}})
rd("enterprise/sz-focus", "读侧·企业", "深圳聚焦企业", {"page": {"type": "integer"}, "size": {"type": "integer"}})  # 顺延：门户可视化（live 剔除，见 PENDING）
rd("industry/tree", "读侧·产业", "标准产业分类树", {})
rd("industry/chain-links", "读侧·产业", "标准产业链环节", {})
rd("service-org/list", "读侧·服务机构", "服务机构列表（join 视角：圈定池∪虚拟）", {"keyword": {}, "page": {"type": "integer"}, "size": {"type": "integer"}})
rd("service-org/detail", "读侧·服务机构", "服务机构详情", {"id": {}})
rd("service-org/suggest", "读侧·服务机构", "服务机构下拉", {"keyword": {}, "limit": {"type": "integer"}})
rd("service-org/topn", "读侧·服务机构", "服务机构技术力 TopN", {"size": {"type": "integer"}})
rd("policy/list", "读侧·政策", "政策列表（join 视角；默认过滤失效+软删）", {"keyword": {}, "status": {}, "page": {"type": "integer"}, "size": {"type": "integer"}})
rd("policy/detail", "读侧·政策", "政策详情", {"id": {}})
rd("policy/suggest", "读侧·政策", "政策下拉", {"keyword": {}, "limit": {"type": "integer"}})
rd("policy/topn", "读侧·政策", "政策力度榜单", {"size": {"type": "integer"}})
rd("policy/stats", "读侧·政策", "政策统计与区域关联", {})
rd("policy/expired", "读侧·政策", "已失效政策列表（updated_after 增量水位，T+1 拉取）", {"updated_after": {"type": "string", "description": "增量水位，如 2026-10-18 02:00:00；不传=全量"}, "page": {"type": "integer"}, "size": {"type": "integer"}})
rd("bulk/entities", "读侧·批量", "实体基础信息批量查询（ids；不返关系/属性）", {"ids": {"type": "array", "items": {"type": "string"}}})

# tags 汇总
if LIVE_ONLY:
    # live 版：剔除未实现端点（PENDING 登记），仅保留已上线契约
    for p in PENDING:
        paths.pop(p, None)
for p in paths.values():
    for method, o in p.items():
        for t in o.get("tags", []):
            if t not in [x["name"] for x in spec["tags"]]:
                spec["tags"].append({"name": t})

print(json.dumps(spec, ensure_ascii=False, indent=1))

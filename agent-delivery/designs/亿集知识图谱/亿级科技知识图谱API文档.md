# 亿级科技知识图谱API文档

> API 版本：`0.1.0`  
> 
> 最后核对日期：`2026-08-04` 
> 
> 

\> 当前共注册 **76 个路径、84 个 HTTP 操作**。

系统还在开发中，当前API文档非最终版，API大致功能基本确定，但是具体的参数、返回值可能会发生变化。

## **1\. 接入信息**



### **1\.1 基础地址**



除健康检查和内部算子重载接口外，业务 API 的统一前缀为：



```Plain Text
/api/v1
```



在线接口定义：



|用途|路径|
|---|---|
|Swagger UI|`/docs`|
|ReDoc|`/redoc`|
|OpenAPI JSON|`/openapi.json`|



### **1\.2 Content\-Type**



|请求类型|Content\-Type|
|---|---|
|普通 JSON 请求|`application/json`|
|Schema 或 Python 工作流脚本上传|`multipart/form-data`|
|Schema 脚本下载|脚本原始 `contentType`，通常为 `text/x-python`|



### **1\.3 认证与请求头**



当前工程没有统一登录鉴权中间件。



|请求头|使用范围|说明|
|---|---|---|
|`X-User-Id`|Schema 管理|Schema 写接口必传；读接口可选，用于计算 `canDelete`。生产环境应由认证网关注入并清除客户端伪造的同名头。|
|`X-Operator-Reload-Token`|`/internal/operators/reload`|当服务端配置 `OPERATOR_RELOAD_TOKEN` 时必传。|



### **1\.4 统一响应与例外**



大部分业务接口返回：



```JSON
{
  "code": 200,
  "success": true,
  "data": {},
  "msg": "success"
}
```



字段含义：



|字段|类型|说明|
|---|---|---|
|`code`|integer|业务状态码，`200` 表示成功。|
|`success`|boolean|业务是否成功。|
|`data`|any|业务数据。|
|`msg`|string|提示、失败原因或降级说明。|



当前实现存在以下响应差异，调用方必须同时检查 HTTP 状态码和响应体：



1\. Pydantic 路由参数校验失败由全局处理器转换为 **HTTP 200**，响应体中 \`code=422\`、\`success=false\`。

2. 业务代码主动抛出的 `HTTPException` 使用真实 HTTP `4xx/5xx`，响应通常为 `{"detail": "..."}`。

3. 图谱搜索及部分知识图谱构建接口会使用 HTTP 200 返回 `ApiResponse(code=404/500, success=false)`。

4. 公共能力、模块目录和算子接口中的部分端点不使用统一包装，直接返回业务 JSON。

5. 下游图仓库异常经全局处理时返回 HTTP 502：`{"status":"error","message":"..."}`。

参数校验失败示例：



```JSON
{
  "code": 422,
  "success": false,
  "data": [
    {
      "loc": ["body", "entities"],
      "msg": "Input should be a valid list",
      "type": "list_type"
    }
  ],
  "msg": "请求参数校验失败"
}
```



### **1\.5 同步与异步语义**



本文中的“同步/异步”指业务语义，而不是 Python 函数是否使用 `async def`。



|类型|行为|
|---|---|
|同步结果接口|HTTP 返回前已经完成查询、保存、脚本校验或业务计算，并返回最终结果。|
|异步受理接口|HTTP 只完成任务下发或本地待下发记录保存，不等待工作流运行完成。|



当前异步受理接口仍返回 HTTP 200，而不是 HTTP 202，主要包括：



- `POST /api/v1/task-center/trigger`

- `POST /api/v1/workflow-system/definitions/{definition_id}/execute`

- `POST /api/v1/workflow-system/schedules/{schedule_id}/trigger`

- `POST /api/v1/manual-reviews/{review_id}/retry`

- `POST /api/v1/manual-reviews/{review_id}/actions` 且 `rerun=true`

## **2\. Schema 到任务触发的完整调用链**



### **2\.1 当前实际链路**



```Plain Text
flowchart LR
    A[查询实体 Schema] --> B[创建实体/关系 Schema]
    B --> C[上传并保存 Schema Python 脚本]
    C --> D{选择执行方式}
    D --> E[创建声明式工作流定义]
    D --> F[上传独立的 Python 工作流脚本]
    D --> G[直接触发内置 graph-build]
    E --> H[执行工作流定义]
    F --> H
    G --> I[返回 taskId + executionId + workflowId]
    H --> J[返回 executionId + workflowId]
    I --> K[查询任务详情]
    J --> L[查询执行下发记录]
```



\> **重要能力边界**：当前没有 \`POST /schemas/\{id\}/trigger\`，也没有自动把 Schema 脚本注册为工作流。Schema 脚本和 Python 工作流脚本是两个独立资源：

> - Schema 脚本仅保存到 S3/MinIO，并校验扩展名、大小、UTF\-8 和 Python 语法。
> 
> - Python 工作流脚本保存到 `WORKFLOW_SCRIPT_DIR`，必须提供指定的 `workflow(payload)` 函数，执行时由 Temporal Activity 子进程调用。
> 
> - 触发任务时可以在 `payload.schemaId` 中携带 Schema ID，但当前内置工作流不会自动读取或执行对应 Schema 脚本。
> 
> 



### **2\.2 第一步：查询 Schema**



#### **查询 Schema 列表**



- 路径：`GET /api/v1/schema-management/schemas`

- 类型：同步

- 用例：获取实体/关系 Schema ID，供关系 Schema 创建或前端目录展示使用。

查询参数：



|参数|位置|类型|必填|默认值|说明|
|---|---|---|---|---|---|
|`kind`|query|string|否|\-|`entity` 或 `relation`。|
|`keyword`|query|string|否|\-|名称、标签等关键字，最长 128。|
|`page`|query|integer|否|`1`|最小 1。|
|`pageSize`|query|integer|否|`20`|1～100。|
|`includeDetails`|query|boolean|否|`false`|是否返回属性和脚本详情。|
|`X-User-Id`|header|string|否|\-|用于判断当前用户能否删除 Schema。|



请求示例：



```Bash
curl 'http://localhost:8001/api/v1/schema-management/schemas?kind=entity&page=1&pageSize=20&includeDetails=true' \
  -H 'X-User-Id: user-a'
```



响应示例：



```JSON
{
  "code": 200,
  "success": true,
  "data": {
    "items": [
      {
        "id": "6b7e62f2-f6af-4a59-a472-d72fc5ccda62",
        "key": "expert",
        "kind": "entity",
        "kindLabel": "实体",
        "name": "Expert",
        "label": "专家",
        "version": "v1.0",
        "isSystem": true,
        "canDelete": false,
        "properties": [
          {
            "name": "expert_id",
            "dataType": "string",
            "required": true,
            "rule": "全局唯一",
            "category": "core"
          }
        ],
        "script": null
      }
    ],
    "total": 14,
    "page": 1,
    "pageSize": 20
  },
  "msg": "success"
}
```



#### **查询单个 Schema**



- 路径：`GET /api/v1/schema-management/schemas/{schema_id}`

- 类型：同步

- 主要参数：路径参数 `schema_id`；可选请求头 `X-User-Id`。

- 失败：Schema 不存在时 HTTP 404，响应 `{"detail":"Schema 不存在: ..."}`。

### **2\.3 第二步：创建实体 Schema**



- 路径：`POST /api/v1/schema-management/schemas/entities`

- 方法：`POST`

- 类型：同步；数据库记录和脚本对象保存成功后才返回。

- Content\-Type：`multipart/form-data`

- 成功 HTTP 状态：`201`

- 必传请求头：`X-User-Id`

表单参数：



|参数|类型|必填|说明|
|---|---|---|---|
|`metadata`|string|是|JSON 字符串，结构见下表。|
|`script`|file|是|`.py` 文件；默认最大 10 MiB；必须为 UTF\-8 且语法有效。|



`metadata` 公共字段：



|字段|类型|必填|默认值|规则/说明|
|---|---|---|---|---|
|`schemaKey`|string|是|\-|1～64；以小写字母开头，只能含小写字母、数字、`-`、`_`。|
|`name`|string|是|\-|1～128；实体名必须是 `PascalCase`。|
|`label`|string|是|\-|中文或展示名称，1～128。|
|`description`|string|否|`""`|最长 4000。|
|`identityKey`|string|否|`""`|身份标识说明，最长 512。|
|`properties`|array|是|\-|1～200 个属性，属性名不能重复。|
|`mappings`|string\[\]|否|`[]`|最多 100 个来源映射，不能重复，单项最长 255。|
|`isCore`|boolean|否|`false`|是否核心 Schema。|
|`version`|string|否|`v1.0`|1～32。|



属性字段：



|字段|类型|必填|默认值|说明|
|---|---|---|---|---|
|`name`|string|是|\-|字母或下划线开头，只能含字母、数字、下划线。|
|`dataType`|string|是|\-|数据类型描述，最长 128。|
|`required`|boolean|否|`false`|是否必填。|
|`rule`|string|否|`""`|约束说明，最长 512。|
|`category`|string|否|`core`|`core` 或 `dynamic`。|



请求示例：



```Bash
curl -X POST 'http://localhost:8001/api/v1/schema-management/schemas/entities' \
  -H 'X-User-Id: user-a' \
  -F 'metadata={"schemaKey":"technology","name":"Technology","label":"技术","description":"技术实体","identityKey":"technology_id","properties":[{"name":"technology_id","dataType":"string","required":true,"rule":"全局唯一","category":"core"},{"name":"name","dataType":"string","required":true,"category":"core"}],"mappings":["technology_profile"],"isCore":false,"version":"v1.0"}' \
  -F 'script=@./technology.py;type=text/x-python'
```



响应示例：



```JSON
{
  "code": 200,
  "success": true,
  "data": {
    "id": "79bb38b0-2b5c-4c9d-a44e-4a9918cbd840",
    "key": "technology",
    "kind": "entity",
    "kindLabel": "实体",
    "name": "Technology",
    "label": "技术",
    "description": "技术实体",
    "identityKey": "technology_id",
    "version": "v1.0",
    "isCore": false,
    "isSystem": false,
    "createdBy": "user-a",
    "canDelete": true,
    "mappings": ["technology_profile"],
    "properties": [
      {
        "name": "technology_id",
        "dataType": "string",
        "required": true,
        "rule": "全局唯一",
        "category": "core"
      }
    ],
    "script": {
      "filename": "technology.py",
      "contentType": "text/x-python",
      "sizeBytes": 43,
      "sha256": "<64位十六进制摘要>",
      "uploadedBy": "user-a",
      "uploadedAt": "2026-08-04T10:00:00+08:00",
      "downloadUrl": "/api/v1/schema-management/schemas/79bb38b0-2b5c-4c9d-a44e-4a9918cbd840/script"
    }
  },
  "msg": "实体 Schema 创建成功"
}
```



错误码：



|HTTP/业务码|场景|
|---|---|
|400|非 `.py`、空脚本、超限、非 UTF\-8、Python 语法错误。|
|403|`X-User-Id` 无效或无权限。|
|409|`schemaKey`、Schema 名称或属性冲突。|
|422|`metadata` JSON 解析或字段规则校验失败。|
|502|S3/MinIO 脚本上传失败。|



### **2\.4 第三步：创建关系 Schema**



- 路径：`POST /api/v1/schema-management/schemas/relations`

- 方法：`POST`

- 类型：同步

- Content\-Type：`multipart/form-data`

- 成功 HTTP 状态：`201`

- 必传请求头：`X-User-Id`

除实体 Schema 的公共字段外，还需提供：



|字段|类型|必填|默认值|说明|
|---|---|---|---|---|
|`sourceSchemaId`|string|实际必填|\-|起点实体 Schema ID，最长 36。服务层要求必须引用现有实体。|
|`targetSchemaId`|string|实际必填|\-|终点实体 Schema ID，最长 36。服务层要求必须引用现有实体。|
|`sourceExpression`|string/null|否|起点 Schema 名|展示用复合表达式。|
|`targetExpression`|string/null|否|终点 Schema 名|展示用复合表达式。|
|`relationCategory`|string|否|`fact`|`fact` 或 `inferred`。|
|`name`|string|是|\-|必须使用 `UPPER_SNAKE_CASE`。|



请求示例：



```Bash
curl -X POST 'http://localhost:8001/api/v1/schema-management/schemas/relations' \
  -H 'X-User-Id: user-a' \
  -F 'metadata={"schemaKey":"uses-technology","name":"USES_TECHNOLOGY","label":"使用技术","description":"专家使用某项技术","sourceSchemaId":"6b7e62f2-f6af-4a59-a472-d72fc5ccda62","targetSchemaId":"79bb38b0-2b5c-4c9d-a44e-4a9918cbd840","relationCategory":"fact","properties":[{"name":"source","dataType":"Expert ID","required":true},{"name":"target","dataType":"Technology ID","required":true}]}' \
  -F 'script=@./uses_technology.py;type=text/x-python'
```



响应中的 `data` 与实体 Schema 基本一致，并额外包含：



```JSON
{
  "sourceSchemaId": "6b7e62f2-f6af-4a59-a472-d72fc5ccda62",
  "sourceSchemaName": "Expert",
  "targetSchemaId": "79bb38b0-2b5c-4c9d-a44e-4a9918cbd840",
  "targetSchemaName": "Technology",
  "relationCategory": "fact"
}
```



关系端点不存在或不是实体 Schema 时返回 HTTP 409。



### **2\.5 第四步：绑定或更换 Schema 脚本**



- 路径：`PUT /api/v1/schema-management/schemas/{schema_id}/script`

- 类型：同步

- Content\-Type：`multipart/form-data`

- 参数：路径参数 `schema_id`、请求头 `X-User-Id`、文件字段 `script`。

- 权限：用户 Schema 仅创建者可更换；系统 Schema 仅 `SCHEMA_ADMIN_USER_IDS` 中的用户可更换。

- 返回：完整 Schema 详情和 `previousScriptCleanupSucceeded`。

下载脚本：



```Plain Text
GET /api/v1/schema-management/schemas/{schema_id}/script
```



下载响应头包含：



- `Content-Disposition`

- `Content-Length`

- `X-Content-SHA256`

### **2\.6 第五步：创建可执行工作流定义**



#### **方式 A：声明式工作流**



- 路径：`POST /api/v1/workflow-system/definitions`

- 类型：同步保存定义，不执行任务。

请求参数：



|字段|类型|必填|默认值|说明|
|---|---|---|---|---|
|`id`|string|是|\-|3～64；正则 `^[a-z0-9][a-z0-9_-]{2,63}$`。|
|`name`|string|是|\-|1～100。|
|`category`|string|否|`custom`|`entity`、`relation`、`graph`、`custom`。|
|`steps`|array|是|\-|至少一个字符串或对象步骤。|
|`taskQueue`|string|否|`tech-kg-workflows`|Temporal Task Queue。|
|`active`|boolean|否|`true`|是否启用。当前执行接口未额外阻止 `active=false` 的定义。|



请求示例：



```JSON
{
  "id": "technology-ingest",
  "name": "技术实体入图工作流",
  "category": "entity",
  "steps": ["load_increment", "schema_mapping", "validate", "persist"],
  "taskQueue": "tech-kg-workflows",
  "active": true
}
```



响应示例：



```JSON
{
  "code": 200,
  "success": true,
  "data": {
    "id": "technology-ingest",
    "name": "技术实体入图工作流",
    "workflowType": "kg.custom.configurable",
    "category": "entity",
    "taskQueue": "tech-kg-workflows",
    "active": true,
    "sourceKind": "declarative",
    "steps": ["load_increment", "schema_mapping", "validate", "persist"],
    "createdAt": "2026-08-04 10:10:00"
  },
  "msg": "自定义工作流定义已保存"
}
```



#### **方式 B：上传 Python 工作流**



- 路径：`POST /api/v1/workflow-system/definitions/python`

- 类型：同步上传和校验，不执行任务。

- Content\-Type：`multipart/form-data`

|表单字段|类型|必填|默认值|说明|
|---|---|---|---|---|
|`file`|file|是|\-|Python 文件，最大 1 MiB。|
|`function_name`|string|否|`workflow`|脚本中必须定义的同步或异步函数名。|
|`definition_id`|string|否|根据文件名生成|规则同声明式定义 ID。|
|`name`|string|否|文件名|展示名称。|



脚本示例：



```Python
def workflow(payload):
    return {
        "schemaId": payload.get("schemaId"),
        "processed": True,
        "recordCount": len(payload.get("records", [])),
    }
```



上传示例：



```Bash
curl -X POST 'http://localhost:8001/api/v1/workflow-system/definitions/python' \
  -F 'definition_id=technology-python-workflow' \
  -F 'function_name=workflow' \
  -F 'name=技术实体 Python 工作流' \
  -F 'file=@./technology_workflow.py;type=text/x-python'
```



失败场景：文件非 UTF\-8、Python 语法错误、函数不存在、ID 非法或超过 1 MiB时返回 HTTP 400。



### **2\.7 第六步：触发任务**



#### **方式 A：触发内置图谱构建总工作流**



- 路径：`POST /api/v1/task-center/trigger`

- 方法：`POST`

\- 类型：**异步受理**

- HTTP 状态：当前实现返回 `200`

- 用例：按实体类型和关系类型启动 `kg.graph.build`，并同时在任务中心创建可查询任务。

请求参数：



|字段|类型|必填|默认值|说明|
|---|---|---|---|---|
|`domains`|string\[\]|否|`[]`|业务域，当前会透传到总工作流。|
|`entities`|string\[\]|否|`[]`|支持的内置值：`paper`、`scholar`、`patent`、`organization`。空数组表示全部默认实体。|
|`relations`|string\[\]|否|`[]`|支持的内置值：`authorship`、`employment`、`citation`、`cooperation`。空数组表示全部默认关系。|
|`since`|string/null|否|`null`|增量游标或时间，当前未强制格式。|
|`reason`|string|否|`客户端立即触发`|触发原因。|
|`payload`|object|否|`{}`|自定义透传字段；可携带 `schemaId`，但不会自动执行 Schema 脚本。|



请求示例：



```JSON
{
  "domains": ["论文"],
  "entities": ["paper"],
  "relations": ["authorship"],
  "since": "2026-08-01 00:00:00",
  "reason": "新论文数据入库",
  "payload": {
    "schemaId": "79bb38b0-2b5c-4c9d-a44e-4a9918cbd840",
    "sourceTable": "technology_profile"
  }
}
```



成功响应示例：



```JSON
{
  "code": 200,
  "success": true,
  "data": {
    "task": {
      "id": "PI-20260804-A1B2C3",
      "batchId": "UPD-20260804",
      "stage": "图谱构建",
      "kind": "实体",
      "objectId": "graph-build-b7d6c9d38c1c45bd86cd8108290ec9af",
      "objectName": "立即触发图谱构建",
      "status": "处理中",
      "taskStatus": "执行中",
      "currentStep": "数据接入",
      "workflowType": "kg.graph.build",
      "workflowId": "graph-build-b7d6c9d38c1c45bd86cd8108290ec9af",
      "runId": "48bdf9b2-9153-47c3-973d-3a1ce9d8f7b8",
      "input": {
        "domains": ["论文"],
        "entities": ["paper"],
        "relations": ["authorship"],
        "since": "2026-08-01 00:00:00",
        "reason": "新论文数据入库",
        "schemaId": "79bb38b0-2b5c-4c9d-a44e-4a9918cbd840",
        "sourceTable": "technology_profile"
      },
      "output": null,
      "logs": ["工作流已下发"]
    },
    "execution": {
      "id": "EXEC-AB12CD34EF56A789",
      "definitionId": "graph-build",
      "workflowId": "graph-build-b7d6c9d38c1c45bd86cd8108290ec9af",
      "runId": "48bdf9b2-9153-47c3-973d-3a1ce9d8f7b8",
      "status": "RUNNING",
      "startedAt": "2026-08-04 10:20:00",
      "completedAt": null,
      "dispatchMode": "TEMPORAL",
      "message": "工作流已下发"
    }
  },
  "msg": "图谱构建任务已创建"
}
```



Temporal 不可用时不会直接返回失败，而是保存本地下发记录：



```JSON
{
  "status": "QUEUED",
  "dispatchMode": "LOCAL_FALLBACK",
  "workflowId": "queued-graph-build-1a2b3c4d5e6f",
  "runId": null,
  "message": "Temporal 暂不可用，已保存待下发记录: <原因>"
}
```



调用方应把 `QUEUED + LOCAL_FALLBACK` 视为“尚未进入 Temporal”，而不是执行成功。



触发接口错误/降级语义：



|HTTP/业务码|场景|
|---|---|
|200 / 200|工作流已下发，`execution.status=RUNNING`。|
|200 / 200|Temporal 不可用但已保存本地记录，`execution.status=QUEUED`、`dispatchMode=LOCAL_FALLBACK`。|
|200 / 422|请求字段类型校验失败。|
|500|内置 `graph-build` 定义缺失或出现未捕获的服务异常。|



#### **方式 B：执行指定工作流定义**



- 路径：`POST /api/v1/workflow-system/definitions/{definition_id}/execute`

\- 类型：**异步受理**

- 用例：执行声明式或上传的 Python 工作流。

- 返回：执行记录，不创建任务中心 `taskId`。

请求参数：



|字段|类型|必填|默认值|说明|
|---|---|---|---|---|
|`payload`|object|否|`{}`|传给工作流的输入。|
|`workflowId`|string/null|否|自动生成|客户端指定 Temporal Workflow ID；必须自行保证唯一。|



请求示例：



```JSON
{
  "payload": {
    "schemaId": "79bb38b0-2b5c-4c9d-a44e-4a9918cbd840",
    "records": [{"technology_id": "T-001", "name": "知识图谱"}]
  },
  "workflowId": "technology-ingest-20260804-001"
}
```



响应示例：



```JSON
{
  "code": 200,
  "success": true,
  "data": {
    "id": "EXEC-90AE12BC34DE56F7",
    "definitionId": "technology-ingest",
    "workflowId": "technology-ingest-20260804-001",
    "runId": "f22b8fca-027d-450e-9ba9-8aefae96cb32",
    "status": "RUNNING",
    "startedAt": "2026-08-04 10:30:00",
    "completedAt": null,
    "payload": {
      "schemaId": "79bb38b0-2b5c-4c9d-a44e-4a9918cbd840"
    },
    "dispatchMode": "TEMPORAL",
    "message": "工作流已下发"
  },
  "msg": "工作流执行请求已受理"
}
```



定义不存在时返回 HTTP 404。



### **2\.8 ID 格式**



|ID|格式|示例|生成位置|
|---|---|---|---|
|Schema ID|UUID v4 字符串|`79bb38b0-2b5c-4c9d-a44e-4a9918cbd840`|创建实体/关系 Schema。|
|任务 ID `taskId`|`PI-YYYYMMDD-` \+ 6 位大写十六进制|`PI-20260804-A1B2C3`|`/task-center/trigger`。|
|批次 ID|`UPD-YYYYMMDD`|`UPD-20260804`|`/task-center/trigger`。同一天立即触发的任务会共享该格式的批次 ID。|
|执行记录 ID|`EXEC-` \+ 16 位大写十六进制|`EXEC-AB12CD34EF56A789`|任意工作流执行下发。|
|Workflow ID|客户端传入，或 `<definition-id>-` \+ 32 位小写十六进制|`graph-build-b7d6...`|Temporal 正常下发。|
|降级 Workflow ID|`queued-<definition-id>-` \+ 12 位小写十六进制|`queued-graph-build-1a2b3c4d5e6f`|Temporal 不可用时。|
|Run ID|Temporal 返回值，通常为 UUID；降级时为 `null`|`48bdf9b2-...`|Temporal。|
|人工审核 ID|当前与任务 ID 相同|`PI-20260714-0003`|人工审核仓库。|
|Schedule ID|3～128 位字母、数字、`_`、`-`|`auto-graph-build`|创建 Schedule。|



### **2\.9 查询任务状态**



#### **查询任务详情**



- 路径：`GET /api/v1/task-center/tasks/{task_id}`

- 类型：同步查询

- 用例：查询任务快照、步骤、日志、输入输出、关联批次和人工审核信息。

```Bash
curl 'http://localhost:8001/api/v1/task-center/tasks/PI-20260804-A1B2C3'
```



重点字段：



|字段|说明|
|---|---|
|`taskStatus`|页面级任务状态：`执行中`、`执行出错`、`等待人工审核`、`执行完成`。|
|`status`|对象处理状态，如 `处理中`、`已完成`。|
|`currentStep`|当前或阻断步骤。|
|`steps`|全部步骤及每步状态、异常数、耗时。|
|`result`|简要结果或下发说明。|
|`logs`|日志文本数组。|
|`output`|任务输出；当前立即触发任务初始为 `null`。|
|`workflowId` / `runId`|Temporal 标识。|
|`review`|如果任务进入人工审核，返回关联审核记录。|



任务不存在时返回 HTTP 404：



```JSON
{"detail":"任务不存在"}
```



#### **查询执行下发记录**



- 路径：`GET /api/v1/workflow-system/executions/{execution_id}`

- 类型：同步查询

- 用例：通过 `EXEC-*` 查询工作流下发记录。

```Bash
curl 'http://localhost:8001/api/v1/workflow-system/executions/EXEC-AB12CD34EF56A789'
```



执行记录不存在时返回 HTTP 404。



### **2\.10 状态值与失败原因**



#### **执行记录状态**



|状态|含义|
|---|---|
|`RUNNING`|已成功下发给 Temporal。只表示开始运行，不表示最终成功。|
|`QUEUED`|Temporal 不可用，当前仅保存本地待下发记录。|
|`COMPLETED`|数据结构支持该状态，但当前 HTTP 下发链路不会等待工作流完成后再写入。|



#### **任务中心状态**



|状态|含义|
|---|---|
|`执行中`|任务正在执行或刚刚完成下发。|
|`执行出错`|任务步骤失败。|
|`等待人工审核`|自动流程被质量规则阻断，需要人工处理。|
|`执行完成`|任务完成。|



#### **失败原因读取优先级**



1. `task.logs`：任务日志和错误文本。

2. `task.result`：任务结果或下发失败说明。

3. `task.steps[].status`、`description`、`abnormal`：定位失败步骤。

4. `task.review.evidence`、`ruleId`、`suggestion`：人工审核原因和处置建议。

5. `execution.message`：Temporal 不可用等下发阶段原因。

6. HTTP 错误的 `detail` 或统一响应的 `msg`。

\> **当前状态查询限制**：\`GET /workflow\-system/executions/\{execution\_id\}\` 和 \`GET /task\-center/tasks/\{task\_id\}\` 读取的是本地 SQLite 中的记录。当前代码没有在查询时调用 Temporal Describe API，也没有工作流完成回调去持续更新 \`RUNNING\`、\`taskStatus\`、\`output\`、\`completedAt\` 和最终失败堆栈。因此，这两个接口目前属于“下发/任务快照查询”，不是完整的实时运行状态查询。需要最终运行状态时，应查看 Temporal UI，默认地址为 \`http://localhost:8233\`。



### **2\.11 推荐的客户端轮询逻辑**



```Plain Text
1. 调用 /task-center/trigger。
2. 保存 data.task.id、data.execution.id、workflowId、runId。
3. 如果 execution.status == QUEUED：提示调度服务不可用，不进入成功轮询。
4. 否则轮询 /task-center/tasks/{taskId}，读取 taskStatus、steps、logs。
5. 若需要 Temporal 最终状态，使用 workflowId/runId 查询 Temporal UI 或后续补充的实时状态接口。
```



## **3\. 完整 API 目录**



### **3\.1 系统健康**



|方法|路径|说明与主要参数|同步性|典型用例|
|---|---|---|---|---|
|GET|`/health`|无参数，返回 `{"status":"ok"}`。|同步|容器健康检查、负载均衡探针。|



### **3\.2 公共知识图谱/NLP 能力**



这些端点直接返回业务 JSON，不使用统一 `ApiResponse`。



|方法|路径|说明与主要参数|同步性|典型用例|
|---|---|---|---|---|
|GET|`/api/v1/common-capabilities/metadata`|返回能力列表、实体抽取场景和关系抽取方法。|同步|前端动态展示可用能力。|
|POST|`/api/v1/common-capabilities/entity-extraction`|JSON：`text` 必填；`source_type=work/education/abstract/general`，默认 `general`。|同步|从履历、教育经历或摘要中抽取实体。|
|POST|`/api/v1/common-capabilities/entity-alignment`|JSON：`kg_a`、`kg_b` 可空；`top_k` 1～50，默认 3。空列表使用内置演示数据。|同步|跨图谱实体候选召回与对齐。|
|POST|`/api/v1/common-capabilities/entity-disambiguation`|JSON：`text`、`mention` 必填；`kb` 可空；`top_k` 1～50，默认 5。|同步|将文本中的实体提及链接到知识库实体。|
|POST|`/api/v1/common-capabilities/relation-extraction`|JSON：`text` 必填；`method=rule/llm/hybrid`，默认 `rule`。`llm/hybrid` 依赖模型配置。|同步|从单段文本抽取关系三元组。|
|POST|`/api/v1/common-capabilities/relation-extraction/batch`|JSON：`texts` 非空数组；`method` 同上。空白文本会被过滤。|同步|批量抽取并合并关系。|
|GET|`/api/v1/common-capabilities/relation-extraction/examples`|无参数，返回内置示例。|同步|测试页面填充样例。|



实体抽取请求示例：



```JSON
{
  "text": "2010年至今，北京大学计算机科学与技术系，教授",
  "source_type": "work"
}
```



关系抽取请求示例：



```JSON
{
  "text": "马云创立了阿里巴巴集团，阿里巴巴集团位于浙江省杭州市。",
  "method": "rule"
}
```



### **3\.3 平台总览、模块目录与选项**



|方法|路径|说明与主要参数|同步性|典型用例|
|---|---|---|---|---|
|GET|`/api/v1/platform/overview`|无参数；返回平台状态、资产统计、最新变更、风险、实体和关系结构。|同步|平台首页仪表盘。|
|GET|`/api/v1/kg-construction/modules`|无参数；返回 12 个知识图谱构建模块。|同步|构建功能目录。|
|GET|`/api/v1/kg-construction/modules/{module_code}`|路径参数 `module_code`。不存在时 HTTP 404。|同步|查询单个模块说明。|
|GET|`/api/v1/kg-construction/options`|无参数；聚合学者、企业、关系边、关系类型、角色、分析维度、技术领域、CPC。单个数据源失败时对应列表为空。|同步|前端测试参数下拉框。|



### **3\.4 知识图谱构建业务接口**



“说明接口”当前仅返回模块元信息，不能触发任务。



|方法|路径|说明与主要参数|同步性|典型用例|
|---|---|---|---|---|
|GET|`/api/v1/kg-construction/expert-direct-relations`|无参数；返回专家直接关系模块说明。|同步|功能介绍。|
|GET|`/api/v1/kg-construction/expert-direct-relations/query`|Query：`dataSource=all`、`expertAId`、`expertBId`、`institution`、`startTime`、`endTime`、`limit` 默认 10、最大 100。|同步|通过 URL 查询专家直接关系。|
|POST|`/api/v1/kg-construction/expert-direct-relations/query`|JSON 参数同 GET 版本。|同步|复杂条件查询专家直接关系。|
|GET|`/api/v1/kg-construction/expert-indirect-relations`|无参数；仅模块说明。|同步|查看间接关系能力说明。|
|GET|`/api/v1/kg-construction/expert-cooperation-achievements`|无参数；仅模块说明。|同步|查看合作成果能力说明。|
|GET|`/api/v1/kg-construction/expert-colleague-relations`|无参数；仅模块说明。|同步|查看同事关系能力说明。|
|GET|`/api/v1/kg-construction/expert-alumni-relations`|无参数；仅模块说明。|同步|查看校友关系能力说明。|
|GET|`/api/v1/kg-construction/expert-paper-cooperation-relations`|无参数；返回专家论文合作模块说明。|同步|功能介绍。|
|POST|`/api/v1/kg-construction/expert-paper-cooperation-relations/demo/structured-result`|JSON：`dataSource`、`expertAId`、`expertBId` 必填；`startTime/endTime` 为 `YYYY-MM-DD`。两位专家不能相同。|同步|生成两位专家论文合作结构化统计。|
|GET|`/api/v1/kg-construction/expert-enterprise-relations`|无参数；返回专家企业关系模块说明。|同步|功能介绍。|
|POST|`/api/v1/kg-construction/expert-enterprise-relations/build`|JSON：`scholarId`、`enterpriseId`、`relationTypes`。关系类型见下表。|同步|创建或合并 `EMPLOYED_BY` 边。|
|GET|`/api/v1/kg-construction/relation-detail-annotations`|无参数；返回关系详情标注模块说明。|同步|功能介绍。|
|POST|`/api/v1/kg-construction/relation-detail-annotations/annotate`|JSON：`relationId`、`roleType` 必填；`techField`、`period.start/end` 可选。|同步|补充角色、技术领域和任职时段。|
|GET|`/api/v1/kg-construction/enterprise-background-analyses`|无参数；返回企业背景分析模块说明。|同步|功能介绍。|
|POST|`/api/v1/kg-construction/enterprise-background-analyses/analyze`|JSON：`enterpriseId`、`analysisDimensions` 必填；`patentCPC` 可选。|同步|聚合企业行业、技术、财务和专利信息。|
|GET|`/api/v1/kg-construction/expert-enterprise-mining`|无参数；返回专家企业关系挖掘模块说明。|同步|功能介绍。|
|POST|`/api/v1/kg-construction/expert-enterprise-mining/mine`|JSON：`scholarId` 必填；`topN=5`；`analysisDimensions` 默认三个维度；`regenerate=false`。|同步|从专家传记挖掘并构建企业关系。|
|GET|`/api/v1/kg-construction/industry-chain-topn-event-relations`|无参数；仅模块说明。|同步|查看产业链 TOP\-N 事件能力。|
|GET|`/api/v1/kg-construction/industry-chain-panorama`|无参数；仅模块说明。|同步|查看产业链全景能力。|



专家企业关系类型：



|编码|中文含义|
|---|---|
|`employment`|任职|
|`advisor`|顾问|
|`rd_cooperation`|研发合作|
|`project_cooperation`|项目合作|
|`tech_cooperation`|技术合作|



企业分析维度：`industry_status`、`core_tech`、`financial`。



推荐角色编码：`chief_scientist`、`cto`、`technical_advisor`、`rd_lead`、`engineer`。当前服务也允许其他真实职位字符串，并将等级留空。



专家企业关系构建请求示例：



```JSON
{
  "scholarId": "007Rb117",
  "enterpriseId": "ORG-001",
  "relationTypes": ["employment", "tech_cooperation"]
}
```



关系标注请求示例：



```JSON
{
  "relationId": "007Rb117->ORG-001@0",
  "roleType": "chief_scientist",
  "techField": "人工智能",
  "period": {
    "start": "2022-01",
    "end": null
  }
}
```



### **3\.5 图谱查询**



所有端点都可通过 `space` 选择图空间；不传时使用 `TRS_GRAPH_SPACE`。异常通常以 HTTP 200 \+ `ApiResponse(code=500, success=false)` 返回。



|方法|路径|说明与主要参数|同步性|典型用例|
|---|---|---|---|---|
|GET|`/api/v1/graph-search/nodes/{node_id}`|`node_id` 必填；Query `space` 可选。|同步|按 VID 查询节点详情。|
|GET|`/api/v1/graph-search/nodes`|Query：`label` 必填；`limit` 1～500 默认 20；`offset>=0`；`space`。|同步|按标签分页列出节点。|
|POST|`/api/v1/graph-search/nodes/search`|Query：`label` 必填、`limit`、`space`；Body：属性对象。|同步|按 DOI、名称等属性查节点。|
|GET|`/api/v1/graph-search/subgraph/{node_id}`|`depth` 1～3；`limit` 1～200；`edge_type`；`direction=out/in/both`；`space`。|同步|获取 N 跳子图供前端渲染。|
|GET|`/api/v1/graph-search/node/{node_id}/edges`|`direction`、`edge_type`、`limit` 1～200、`space`。|同步|轻量查询节点相关边。|
|GET|`/api/v1/graph-search/node/{node_id}/neighbours`|参数同边查询，返回邻居节点属性。|同步|展开节点邻居。|
|GET|`/api/v1/graph-search/shortest-path`|Query：`source`、`target` 必填；`max_depth` 1～20 默认 10；`space`。|同步|查询两个节点最短路径。|
|GET|`/api/v1/graph-search/spaces`|无参数。|同步|列出可用图空间。|
|GET|`/api/v1/graph-search/stats`|Query：`space` 可选。|同步|获取各标签节点数和各边类型数量。|



节点响应结构：



```JSON
{
  "id": "node-vid",
  "labels": ["Paper"],
  "properties": {
    "title": "知识图谱研究"
  }
}
```



边响应结构：



```JSON
{
  "id": "source->target@0",
  "type": "AUTHORED_BY",
  "source": "source",
  "target": "target",
  "properties": {}
}
```



### **3\.6 Schema 管理**



|方法|路径|说明与主要参数|同步性|典型用例|
|---|---|---|---|---|
|GET|`/api/v1/schema-management/overview`|无参数；返回版本、实体/关系/属性/约束/映射统计。|同步|Schema 管理页总览。|
|GET|`/api/v1/schema-management/schemas`|`kind`、`keyword`、`page`、`pageSize`、`includeDetails`；可选 `X-User-Id`。|同步|Schema 目录、搜索和分页。|
|GET|`/api/v1/schema-management/schemas/topology`|可选 `X-User-Id`。|同步|返回实体节点和关系边拓扑。|
|GET|`/api/v1/schema-management/schemas/{schema_id}`|路径参数 `schema_id`；可选 `X-User-Id`。|同步|查看属性、映射和脚本元数据。|
|POST|`/api/v1/schema-management/schemas/entities`|`multipart`：`metadata`、`script`；请求头 `X-User-Id`。|同步|创建实体 Schema。|
|POST|`/api/v1/schema-management/schemas/relations`|参数同上，metadata 增加关系端点。|同步|创建关系 Schema。|
|PUT|`/api/v1/schema-management/schemas/{schema_id}/script`|`multipart` 文件 `script`；请求头 `X-User-Id`。|同步|上传或替换 Schema 脚本。|
|GET|`/api/v1/schema-management/schemas/{schema_id}/script`|路径参数 `schema_id`。|同步流式下载|下载 Schema 脚本。|
|DELETE|`/api/v1/schema-management/schemas/{schema_id}`|请求头 `X-User-Id`。系统 Schema 不可删；被关系引用的实体不可删。|同步|删除当前用户创建的 Schema。|



### **3\.7 任务中心与数据源**



|方法|路径|说明与主要参数|同步性|典型用例|
|---|---|---|---|---|
|GET|`/api/v1/task-center/overview`|无参数；返回最新批次、状态统计、变化汇总、更新策略和数据源状态。|同步|任务中心首页。|
|GET|`/api/v1/task-center/batches`|无参数。|同步|查询更新批次。|
|GET|`/api/v1/task-center/tasks`|Query：`stage`、`status`、`domain`、`kind`、`batchId`、`startTime`、`endTime`、`keyword`、`page`、`pageSize`。服务实际将 `pageSize` 限制为 1～200。|同步|任务筛选和分页。|
|GET|`/api/v1/task-center/tasks/{task_id}`|路径参数 `task_id`。|同步|查询任务详情、步骤、日志、输入输出和人工审核。|
|GET|`/api/v1/task-center/data-sources/health`|无参数；当前 MySQL/图库为仓库探针数据，Temporal 状态提示通过工作流健康接口查询。|同步|数据源健康面板。|
|GET|`/api/v1/task-center/data-sources/updates`|Query：`domain`、`since`、`until`、`page`、`pageSize`。|同步|查询源数据增量。|
|GET|`/api/v1/task-center/update-policy`|无参数。|同步|获取自动建图策略。|
|PUT|`/api/v1/task-center/update-policy`|JSON：`enabled`、`frequency`、`executionTime`、`timezone`、`skipWhenNoChanges`。|同步保存/异步调度|保存策略并创建或更新 Temporal Schedule。Temporal 失败时保存本地记录。|
|POST|`/api/v1/task-center/trigger`|JSON：`domains`、`entities`、`relations`、`since`、`reason`、`payload`。|异步受理|立即启动图谱构建并创建任务中心任务。|



更新策略请求示例：



```JSON
{
  "enabled": true,
  "frequency": "每6小时",
  "executionTime": "03:30",
  "timezone": "Asia/Shanghai",
  "skipWhenNoChanges": true
}
```



可选频率：`每天`、`每12小时`、`每6小时`、`每周`。



### **3\.8 人工审核**



|方法|路径|说明与主要参数|同步性|典型用例|
|---|---|---|---|---|
|GET|`/api/v1/manual-reviews`|Query：`status`、`domain`、`category`、`batchId`、`startTime`、`endTime`、`keyword`、`page`、`pageSize`。|同步|查询待处理、已完成、已撤销审核。|
|GET|`/api/v1/manual-reviews/{review_id}`|路径参数 `review_id`。|同步|查看证据、规则、原结果、关联任务和批次。|
|GET|`/api/v1/manual-reviews/{review_id}/flow`|路径参数 `review_id`。|同步|查看阻断步骤和处理流程。|
|POST|`/api/v1/manual-reviews/{review_id}/actions`|JSON：`actionId` 必填；`note`、`result`、`handler`、`rerun` 可选。|同步处置；`rerun=true` 时异步下发|完成人工裁决并可从流程重跑。|
|PUT|`/api/v1/manual-reviews/{review_id}/result`|JSON：`result` 必填；`note`、`handler` 可选。|同步|修改任务结果但不结束审核。|
|POST|`/api/v1/manual-reviews/{review_id}/retry`|JSON：`note`、`payload` 可选。|异步受理|重试关联图谱构建工作流。|
|POST|`/api/v1/manual-reviews/{review_id}/revoke`|JSON：`reason` 必填；`handler` 可选。|同步|撤销人工任务。|



人工处置请求示例：



```JSON
{
  "actionId": "pass-rerun",
  "note": "补充证据后通过",
  "result": {
    "approved": true
  },
  "handler": "reviewer-a",
  "rerun": true
}
```



只有 `待处理` 状态可以提交处置；重复处置返回 HTTP 409。



### **3\.9 工作流定义、执行与调度**



内置工作流类型：



|类别|Workflow Type|
|---|---|
|实体|`kg.entity.paper`、`kg.entity.scholar`、`kg.entity.patent`、`kg.entity.organization`|
|关系|`kg.relation.authorship`、`kg.relation.employment`、`kg.relation.citation`、`kg.relation.cooperation`|
|总流程|`kg.graph.build`|
|自定义|`kg.custom.configurable`、`kg.custom.python`|



|方法|路径|说明与主要参数|同步性|典型用例|
|---|---|---|---|---|
|GET|`/api/v1/workflow-system/health`|无参数；返回 Temporal 地址、命名空间、Task Queue 和连接状态。|同步探测|调度服务健康检查。|
|GET|`/api/v1/workflow-system/definitions`|无参数。|同步|查询内置及自定义工作流定义。|
|POST|`/api/v1/workflow-system/definitions`|JSON：`id`、`name`、`steps` 必填；`category`、`taskQueue`、`active` 可选。|同步|创建声明式工作流。|
|POST|`/api/v1/workflow-system/definitions/python`|`multipart`：`file` 必填；`function_name`、`definition_id`、`name` 可选。|同步|上传 Python 工作流。|
|GET|`/api/v1/workflow-system/definitions/{definition_id}`|路径参数 `definition_id`。|同步|查询定义详情。|
|POST|`/api/v1/workflow-system/definitions/{definition_id}/execute`|JSON：`payload`、`workflowId`。|异步受理|运行指定定义。|
|GET|`/api/v1/workflow-system/executions/{execution_id}`|路径参数 `execution_id`。|同步|查询本地下发记录快照。|
|GET|`/api/v1/workflow-system/schedules`|无参数。|同步|查询 Schedule。|
|POST|`/api/v1/workflow-system/definitions/{definition_id}/schedules`|JSON：`id`、`cron` 必填；`timezone`、`active`、`payload` 可选。|同步创建调度|创建 Temporal Schedule；失败时本地保存为 `LOCAL_SAVED`。|
|PUT|`/api/v1/workflow-system/schedules/{schedule_id}/state`|JSON：`active` 必填。|同步更新调度|暂停或恢复 Schedule。|
|POST|`/api/v1/workflow-system/schedules/{schedule_id}/trigger`|无 Body。|异步触发|立即触发 Schedule。仅返回 Schedule ID，不返回 taskId/executionId。|
|DELETE|`/api/v1/workflow-system/schedules/{schedule_id}`|路径参数 `schedule_id`。|同步|删除 Temporal 和本地 Schedule；Temporal 删除失败会被忽略，本地仍删除。|



Schedule 请求示例：



```JSON
{
  "id": "technology-daily",
  "cron": "0 2 * * *",
  "timezone": "Asia/Shanghai",
  "active": true,
  "payload": {
    "schemaId": "79bb38b0-2b5c-4c9d-a44e-4a9918cbd840"
  }
}
```



Schedule 下发状态：



|值|含义|
|---|---|
|`TEMPORAL_CREATED`|已在 Temporal 创建。|
|`TEMPORAL_UPDATED`|暂停/恢复状态已同步到 Temporal。|
|`TRIGGERED`|已请求立即触发。|
|`LOCAL_SAVED`|Temporal 操作失败，仅保存本地配置；具体原因在 `message`。|



### **3\.10 算子注册、热更新与调用**



算子统一函数签名：



```Python
def operator(data: list[dict], ctx: dict) -> list[dict]:
    ...
```



算子类型：



- `data_processing`

- `entity_extraction`

- `relation_extraction`

- `entity_ingestion`

- `relation_ingestion`

|方法|路径|说明与主要参数|同步性|典型用例|
|---|---|---|---|---|
|GET|`/api/v1/operators`|Query：`kind` 可选。直接返回 `{"items": [...]}`。|同步|查询内置和用户算子。|
|POST|`/api/v1/operators`|JSON：`name`、`version`、`kind`、`source` 必填；`description` 可选。成功 HTTP 201。|同步|上传新算子并立即加载。|
|GET|`/api/v1/operators/{name}`|路径参数 `name`。|同步|查询算子清单。|
|PUT|`/api/v1/operators/{name}`|JSON：`version`、`kind`、`source` 必填；`description` 可选。|同步|热更新用户算子。|
|DELETE|`/api/v1/operators/{name}`|路径参数 `name`。成功 HTTP 204，无响应体。|同步|删除用户算子；内置算子不可删除。|
|POST|`/api/v1/operators/{name}/invoke`|JSON：`data` 对象数组必填；`ctx` 默认 `{}`。|同步|调用算子并获取最终处理结果。|
|POST|`/internal/operators/reload`|可选 Body：`operators`、`replace`；可选/条件必填头 `X-Operator-Reload-Token`。|同步|Worker 重载或安装算子快照。|



算子名称服务层规则：`^[a-zA-Z][a-zA-Z0-9_.-]{0,127}$`。



上传示例：



```JSON
{
  "name": "user.add_score",
  "version": "1.0.0",
  "kind": "data_processing",
  "description": "给记录增加分数",
  "source": "def operator(data, ctx):\n    score = ctx.get('score', 1)\n    return [{**item, 'score': score} for item in data]\n"
}
```



调用示例：



```JSON
{
  "data": [{"name": "Alice"}],
  "ctx": {"score": 10}
}
```



成功响应：



```JSON
{
  "operator": {
    "name": "user.add_score",
    "version": "1.0.0",
    "kind": "data_processing",
    "description": "给记录增加分数",
    "builtin": false,
    "updated_at": "2026-08-04T02:00:00+00:00"
  },
  "data": [{"name": "Alice", "score": 10}],
  "count": 1
}
```



算子错误码：



|HTTP 状态|场景|
|---|---|
|401|内部重载令牌无效。|
|404|算子不存在。|
|409|算子已存在、尝试覆盖/修改/删除内置算子。|
|422|源码无有效 `operator` 函数、执行失败、返回值不是对象数组或请求参数非法。|
|503|S3/RustFS 算子存储异常。|
|500|未分类算子内部错误。|



> 安全提示：用户算子和 Python 工作流脚本拥有服务进程权限，必须仅向受信任管理员开放。Python 语法检查不是安全沙箱。
> 
> 



## **4\. 常见业务用例**



### **4\.1 创建 Schema 后立即触发图谱构建**



1. `GET /schema-management/schemas?kind=entity` 获取关系端点 ID。

2. `POST /schema-management/schemas/entities` 创建实体 Schema 并上传脚本。

3. 如有关系，再调用 `POST /schema-management/schemas/relations`。

4. 调用 `POST /task-center/trigger`，在 `payload.schemaId` 中携带目标 Schema ID。

5. 保存响应中的 `task.id`、`execution.id`、`workflowId` 和 `runId`。

6. 调用 `GET /task-center/tasks/{taskId}` 查询任务快照。

7. 使用 Temporal UI 查询最终运行状态。

注意：第 4 步只透传 `schemaId`，不会自动运行第 2/3 步上传的 Schema 脚本。



### **4\.2 执行自定义 Python 数据处理工作流**



1. 准备包含 `workflow(payload)` 的 Python 文件。

2. 调用 `POST /workflow-system/definitions/python` 上传并校验。

3. 调用 `POST /workflow-system/definitions/{definitionId}/execute` 下发任务。

4. 通过 `GET /workflow-system/executions/{executionId}` 查询下发快照。

5. 通过 Temporal UI 查询脚本最终返回值或失败堆栈。



### **4\.3 排查图谱构建失败并人工重跑**



1. `GET /task-center/tasks?status=执行出错` 筛选失败任务。

2. `GET /task-center/tasks/{taskId}` 查看 `steps`、`result` 和 `logs`。

3. 若存在审核记录，调用 `GET /manual-reviews/{taskId}` 查看 `ruleId`、`evidence`、`suggestion`。

4. `PUT /manual-reviews/{taskId}/result` 修正结果。

5. `POST /manual-reviews/{taskId}/actions`，设置 `rerun=true` 完成裁决并重跑。

### **4\.4 查询并展示图谱子图**



1. `POST /graph-search/nodes/search?label=Paper` 按 DOI 或标题查中心节点。

2. 读取节点 `id`。

3. `GET /graph-search/subgraph/{nodeId}?depth=2&direction=both` 获取点边数据。

4. 前端使用 `data.nodes` 和 `data.edges` 渲染。


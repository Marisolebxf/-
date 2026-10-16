# SSO 开放接口 — 前端 API 参考

> 适用：国科信业务系统（前端经网关/直连调 upms-biz）。  
> 三个端点：1.4 获得授权信息、1.5 登出、2.4 获取菜单权限资源。  
> **鉴权**：所有接口必须带 `Authorization: Bearer <access_token>`；token 失效返 `HTTP 401 + {code:401, msg:"访问令牌不存在"}`。

## 1. 通用约定

### 1.1 基础地址

| 环境 | 地址 |
| --- | --- |
| 本地调试 | `http://127.0.0.1:4000/admin` |
| 生产 | 由网关层转发，前端按网关文档 |

> **请求 URL 必带 `/admin` 前缀**。

### 1.2 公共请求头

| 头部 | 必填 | 示例 | 说明 |
| --- | --- | --- | --- |
| `Authorization` | 是 | `Bearer <access_token>` | 登录后下发的 access_token |
| `systemCode` | 是 | `topic` | 业务系统标识，按后端分配的值填 |
| `Content-Type` | 2.4 必填 | `application/json` | 仅 2.4 需要 |

### 1.3 通用响应结构 `R<T>`

```json
{
  "code": 0,
  "msg": "",
  "data": {}
}
```

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `code` | Integer | `0` 成功；`1` 业务失败；`401` token 失效（HTTP 也是 401）；`5xx` 系统异常 |
| `msg` | String | 错误描述；成功为 `""` |
| `data` | Object / Boolean / 数组 | 业务数据，失败时为 `null` |

### 1.4 错误码

| HTTP | code | 含义 | 前端处理 |
| --- | --- | --- | --- |
| 200 | 0 | 成功 | 正常 |
| 200 | 1 | 业务失败（参数错、权限不足等）| 按 `msg` 提示 |
| 401 | 401 | token 失效 / 过期 | 跳登录页 |
| 500 | 500 | 后端系统异常 | 提示"系统异常，请稍后再试" |

---

## 2. 接口 1.4 获得授权信息

> 返回用户主体、角色、菜单、权限标识、关联机构。  
> **用途**：登录后调一次拿用户信息、菜单树、按钮权限。

### 2.1 请求

| 项目 | 值 |
| --- | --- |
| 方法 | `GET` |
| 路径 | `/admin/get-permission-info` |
| Content-Type | 不需要 |

### 2.2 Query 参数

| 参数名 | 必填 | 类型 | 说明 |
| --- | --- | --- | --- |
| `orgId` | 否 | Long | 机构编号；不传按 token 所属默认 |
| `include_role_menu` | 否 | Boolean | 是否返回角色与菜单的映射列表；默认 `false` |

### 2.3 请求头

| 头部 | 必填 | 说明 |
| --- | --- | --- |
| `Authorization` | 是 | `Bearer <access_token>` |
| `systemCode` | 是 | 业务系统标识，如 `topic` |

### 2.4 响应 `data` 字段

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `userId` | Long | 用户编号 |
| `username` | String | 登录名 |
| `realName` | String | 姓名 |
| `orgId` | Long | 当前机构编号 |
| `orgName` | String | 当前机构名 |
| `roleIds` | Array<Long> | 角色编号列表 |
| `roleNames` | Array<String> | 角色名列表 |
| `menus` | Array<Object> | 菜单树（结构见 2.4.1）|
| `permissions` | Array<String> | 按钮权限标识集合 |
| `roleMenus` | Array<Object> | 角色与菜单映射列表（`include_role_menu=true` 时返回）|

#### 2.4.1 菜单节点 `menus[].*`

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | Long | 菜单编号 |
| `parentId` | Long | 父菜单编号，`0` 表示根 |
| `name` | String | 菜单名 |
| `code` | String | 菜单标识 |
| `type` | Integer | `1` 目录 / `2` 菜单 / `3` 按钮 |
| `path` | String | 路由 path |
| `component` | String | 前端组件路径 |
| `componentName` | String | 组件名 |
| `icon` | String | 图标 |
| `permission` | String | 按钮权限标识（`type=3` 时）|
| `visible` | Boolean | 是否显示 |
| `keepAlive` | Boolean | 是否缓存 |
| `alwaysShow` | Boolean | 是否始终显示 |
| `sort` | Integer | 排序 |
| `children` | Array<Object> | 子菜单，递归同结构 |

### 2.5 请求示例

#### curl

```bash
curl -X GET "http://127.0.0.1:4000/admin/get-permission-info?include_role_menu=true" \
  -H "Authorization: Bearer <access_token>" \
  -H "systemCode: <systemCode>"
```

#### Postman

| 字段 | 值 |
| --- | --- |
| Method | `GET` |
| URL | `http://127.0.0.1:4000/admin/get-permission-info?include_role_menu=true` |
| Headers → `Authorization` | `Bearer <access_token>` |
| Headers → `systemCode` | `<systemCode>` |
| Body | none |

### 2.6 成功响应示例

```json
{
  "code": 0,
  "msg": "",
  "data": {
    "userId": 1001,
    "username": "zhangsan",
    "realName": "张三",
    "orgId": 10,
    "orgName": "国科信总部",
    "roleIds": [1, 2],
    "roleNames": ["管理员", "审核员"],
    "menus": [
      {
        "id": 1,
        "parentId": 0,
        "name": "用户管理",
        "code": "system:user",
        "type": 2,
        "path": "/user",
        "component": "system/user/index",
        "componentName": "SystemUser",
        "icon": "user",
        "permission": "system:user:query",
        "visible": true,
        "keepAlive": false,
        "alwaysShow": false,
        "sort": 1,
        "children": []
      }
    ],
    "permissions": [
      "system:user:query",
      "system:user:create",
      "system:user:update",
      "system:user:delete"
    ],
    "roleMenus": [
      { "roleId": 1, "menuIds": [1, 2, 3] },
      { "roleId": 2, "menuIds": [2, 3] }
    ]
  }
}
```

---

## 3. 接口 1.5 登出系统

> 撤销当前 token。  
> **用途**：前端退出登录时调，调完丢弃本地 token。

### 3.1 请求

| 项目 | 值 |
| --- | --- |
| 方法 | `GET` |
| 路径 | `/admin/logout` |
| Content-Type | 不需要 |

### 3.2 Query 参数

无。

### 3.3 请求头

| 头部 | 必填 | 说明 |
| --- | --- | --- |
| `Authorization` | 是 | `Bearer <access_token>` |
| `systemCode` | 是 | 业务系统标识，如 `topic` |

### 3.4 响应 `data` 字段

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `data` | Boolean | `true` 撤销成功；`false` 失败 |

### 3.5 请求示例

#### curl

```bash
curl -X GET "http://127.0.0.1:4000/admin/logout" \
  -H "Authorization: Bearer <access_token>" \
  -H "systemCode: <systemCode>"
```

#### Postman

| 字段 | 值 |
| --- | --- |
| Method | `GET` |
| URL | `http://127.0.0.1:4000/admin/logout` |
| Headers → `Authorization` | `Bearer <access_token>` |
| Headers → `systemCode` | `<systemCode>` |
| Body | none |

### 3.6 成功响应示例

```json
{
  "code": 0,
  "msg": "",
  "data": true
}
```

---

## 4. 接口 2.4 获取菜单权限资源

> 按 menuId 拿菜单子树 + 按钮权限集合（POST）。  
> **用途**：动态加载单模块菜单。`clientId / timestamp / nonce / signature / token` 由**服务端注入**，前端只传 `menuId`。

### 4.1 请求

| 项目 | 值 |
| --- | --- |
| 方法 | `POST` |
| 路径 | `/admin/page-permission` |
| Content-Type | `application/json` |

### 4.2 Query 参数

| 参数名 | 必填 | 类型 | 说明 |
| --- | --- | --- | --- |
| `menuId` | 是 | Long | 菜单编号（根菜单传根 id）|

### 4.3 请求头

| 头部 | 必填 | 说明 |
| --- | --- | --- |
| `Authorization` | 是 | `Bearer <access_token>` |
| `systemCode` | 是 | 业务系统标识，如 `topic` |
| `Content-Type` | 是 | `application/json` |

### 4.4 请求体

**留空（不传任何字段）**。`clientId / timestamp / nonce / signature / token` 由服务端自动追加。

### 4.5 响应 `data` 字段

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `menus` | Array<Object> | 指定 menuId 下的菜单子树，结构同 1.4 菜单节点 |
| `permissions` | Array<String> | 该菜单下的按钮权限标识集合 |

### 4.6 请求示例

#### curl

```bash
curl -X POST "http://127.0.0.1:4000/admin/page-permission?menuId=1" \
  -H "Authorization: Bearer <access_token>" \
  -H "systemCode: <systemCode>" \
  -H "Content-Type: application/json"
```

#### Postman

| 字段 | 值 |
| --- | --- |
| Method | `POST` |
| URL | `http://127.0.0.1:4000/admin/page-permission?menuId=1` |
| Params → `menuId` | `<menuId>` |
| Headers → `Authorization` | `Bearer <access_token>` |
| Headers → `systemCode` | `<systemCode>` |
| Headers → `Content-Type` | `application/json` |
| Body | **none**（不要填 JSON）|

### 4.7 成功响应示例

```json
{
  "code": 0,
  "msg": "",
  "data": {
    "menus": [
      {
        "id": 10,
        "parentId": 1,
        "name": "用户列表",
        "code": "system:user:list",
        "type": 2,
        "path": "list",
        "component": "system/user/list",
        "componentName": "SystemUserList",
        "icon": "list",
        "permission": "system:user:list",
        "visible": true,
        "keepAlive": true,
        "alwaysShow": false,
        "sort": 1,
        "children": []
      }
    ],
    "permissions": [
      "system:user:list",
      "system:user:create",
      "system:user:update",
      "system:user:delete"
    ]
  }
}
```

---

## 5. 完整 curl 一览

```bash
TOKEN="<access_token>"
HOST="http://127.0.0.1:4000/admin"
SC="<systemCode>"

# 1.4 获得授权信息
curl -X GET "$HOST/get-permission-info?include_role_menu=true" \
  -H "Authorization: Bearer $TOKEN" \
  -H "systemCode: $SC"

# 1.5 登出
curl -X GET "$HOST/logout" \
  -H "Authorization: Bearer $TOKEN" \
  -H "systemCode: $SC"

# 2.4 菜单权限资源
curl -X POST "$HOST/page-permission?menuId=1" \
  -H "Authorization: Bearer $TOKEN" \
  -H "systemCode: $SC" \
  -H "Content-Type: application/json"
```

---

## 6. 排错速查

| 现象 | 原因 | 处理 |
| --- | --- | --- |
| HTTP 401 + `code:401, msg:"访问令牌不存在"` | token 失效 / 过期 | 跳登录页 |
| HTTP 200 + `code:1, msg:"sso get-permission-info failed"` | 1.4 业务失败（参数错 / 用户无权限）| 按 `msg` 提示 |
| HTTP 200 + `code:1, msg:"sso page-permission failed"` | 2.4 业务失败（签名 / 参数 / 无菜单权限）| 检查 `menuId` 是否有效 |
| HTTP 500 + `code:500, msg:"系统异常"` | 后端系统异常 | 提示"系统异常，请稍后再试" |
| 缺 `systemCode` 头 | 业务系统标识缺失 → 业务失败 | 按后端分配填 `topic` / `display` 等 |

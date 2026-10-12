# 国科信项目统一门户 iframe 集成技术方案

**文档版本：** V1\.1
**编写日期：** 2026\-08\-06
**适用范围：** 国科信项目统一门户、统一用户中心及各业务子系统接入
**方案类型：** 统一门户 \+ 统一用户中心 \+ iframe 子系统集成

## 修订记录

|**版本**|**日期**|**修订人**|**修订内容**|
|---|---|---|---|
|V1\.0|2026\-08\-06|李占伟，李瑞|初稿|
|v1\.1|2026\-08\-19|李占伟|添加门户本地部署与配置指南<br>Cookie 键名统一为 portal\_access\_token|

# 项目背景

当前科研业务系统由多个子系统组成，各子系统可能由不同团队独立建设，存在技术栈不统一、页面入口分散、菜单体系不一致、权限维护分散、页面风格不统一等问题。

为了提升整个系统整体使用体验，降低用户在多个系统之间切换的成本，现建设统一门户。统一门户通过统一用户中心获取当前登录用户信息、用户权限及菜单树，并根据菜单节点配置的 URL，通过 iframe 方式嵌入各业务子系统页面，从而实现统一入口、统一菜单、统一登录、统一鉴权和统一页面框架。

本方案采用 iframe 集成方式，主要考虑到各子系统开发团队、技术栈、建设周期和改造能力可能存在差异。iframe 方案对子系统侵入性较低，适合多团队、多系统、异构技术栈场景下的系统集成。

# 建设目标

本方案建设目标如下：

|**序号**|**目标**|**说明**|
|---|---|---|
|1|统一系统入口|用户通过统一门户访问科研大系统下的各业务子系统，无需分别记忆和访问多个系统地址。|
|2|统一登录认证|用户登录由统一用户中心负责。门户接入统一用户中心完成用户身份认证，各子系统共享统一认证能力，避免用户重复登录。|
|3|统一菜单权限|统一用户中心维护用户、角色、权限、菜单树及子系统访问地址。门户根据当前用户权限获取并渲染可访问菜单。|
|4|统一页面框架|门户统一渲染顶部导航、左侧菜单、用户信息区、搜索入口、内容区等公共布局，保证整体访问体验一致。|
|5|子系统低成本接入|子系统只需提供可访问的业务页面 URL，并满足统一登录、iframe 嵌入、安全策略等基本规范，即可接入统一门户。|
|6|系统间低耦合|门户与子系统通过菜单 URL、iframe 及标准通信协议集成，避免对子系统前端技术栈、构建方式和工程结构提出强约束。|
|7|保留后续演进能力|当前阶段采用 iframe 作为主方案。后续对于新建、可控或高频核心子系统，可根据实际情况逐步演进为微前端或其他深度集成模式。|

# 方案选型

## 3\.1 可选方案对比

|**方案**|**优点**|**缺点**|**适用情况**|
|---|---|---|---|
|iframe 集成|接入成本低；技术栈无关；系统隔离性强；适合历史系统和第三方系统|页面深度融合有限；跨页面通信需使用 postMessage；iframe 内外路由需单独处理|适合当前多系统、多团队、弱约束场景|
|微前端|页面体验更融合；可共享状态；适合组件级集成|对子系统工程、路由、构建、样式、生命周期要求较高；需要较强团队协作和治理能力|适合团队可控、技术栈较统一的新系统|
|完全重构统一前端|体验最统一；工程标准最高|成本高、周期长、风险大；对现有系统改造大|当前阶段不建议采用|

## 3\.2 选择 iframe 的原因

结合当前项目实际情况，选择 iframe 方案的主要原因如下：

1. 各子系统可能由不同团队建设，门户团队无法强约束其前端技术栈和工程规范。

2. 子系统技术栈可能不一致，可能包含 Vue、React、传统 Web 页面、第三方系统等。

3. 当前阶段建设目标以统一入口、统一菜单、统一认证和统一鉴权为主。

4. iframe 对子系统改造成本低，子系统只需提供可访问 URL。

5. iframe 具备浏览器原生隔离能力，可避免样式、脚本、依赖之间相互冲突。

6. 子系统可保持独立部署、独立发布，降低系统集成风险。

7. 后续仍可对可控核心子系统逐步演进为微前端模式。

因此，本阶段采用：

> **统一门户 \+ 统一用户中心 \+ iframe 子系统集成** 的总体技术方案。
> 
> 

# 总体架构设计

## 4\.1 架构概述

系统整体由以下部分组成：

1. **统一门户**
负责用户访问入口、顶部导航、左侧菜单、iframe 容器、页面加载状态、异常兜底、子系统页面嵌入等能力。

2. **统一用户中心**
负责用户登录、身份认证、用户信息、角色权限、菜单树、子系统访问地址配置等能力。

3. **业务子系统**
负责各自业务页面和业务接口，支持被统一门户通过 iframe 嵌入访问。

4. **统一网关或后端服务**
负责接口转发、Token 校验、服务鉴权、安全控制、日志审计等能力。

## 4\.2 总体架构图

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=NmI4M2M4MzU1NmQyOTUxZjI0NTAwMTc1MDdiMjk5ZDRfODliMmYwOWM1Mzk0MWQ5ODAxNzJjY2E5NzQ3OGU2MDhfSUQ6NzY3MDgzNDcyMjc5MDA2NzQyMl8xNzkxNzkwNTk0OjE3OTE4NzY5OTRfVjM)

## 4\.3 系统职责划分

|**模块**|**主要职责**|
|---|---|
|统一用户中心|用户登录、认证鉴权、用户信息、角色权限、菜单树、子系统 URL 配置|
|统一门户|获取菜单树、渲染顶部导航和左侧菜单、维护门户布局、加载 iframe、处理页面状态|
|业务子系统|提供业务页面、支持统一登录态、允许被门户 iframe 嵌入、处理自身业务权限|

# 核心业务流程

## 5\.1 用户登录流程

用户访问统一门户时，如未登录，用户点击登录则跳转至统一用户中心登录页。用户登录成功后，统一用户中心签发登录凭证，用户返回统一门户。门户获取当前用户信息及用户可访问菜单树，完成页面初始化。

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=ZDIyMjkwZmRiMmEwZjk4MTNmNTJlY2FhZGEyOTk0OWNfNzhlMjhjM2UzY2I5ODE5NzdiMDUwMzAzODdiN2QzYzJfSUQ6NzY3MDg0NDM4NTYyNzg1MTk4Nl8xNzkxNzkwNTk0OjE3OTE4NzY5OTRfVjM)

流程如下：

1. 用户访问统一门户。

2. 门户检测当前登录态。

3. 如未登录，用户点击登录则跳转统一用户中心登录页。

4. 用户在统一用户中心完成登录认证。

5. 统一用户中心签发 Token ，用户跳转回统一门户，并携带授权码。

6. 门户换取 Token 后写入登录 Cookie。

7. 门户获取当前用户信息。

8. 门户获取当前用户可访问菜单树。

9. 门户渲染顶部导航和左侧菜单。

10. 用户进入系统首页。

## 5\.2 菜单加载流程

门户登录成功后，调用统一用户中心菜单接口。统一用户中心根据当前用户角色和权限返回菜单树。门户根据菜单类型、层级、排序和权限信息渲染顶部导航和左侧菜单。

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=MzY3ZWJhYTg1ZTFjM2MzODhkYWEyOGRjYmIzNTU2NzdfNDkyNzk1N2UwYTBjZWM5OWY1YjlmNjU0YjNkMzc5NTlfSUQ6NzY3MDg0MDA2MjEyOTYyMjMwMl8xNzkxNzkwNTk0OjE3OTE4NzY5OTRfVjM)

流程如下：

1. 门户调用统一用户中心菜单接口。

2. 用户中心根据用户权限返回菜单树。

3. 门户解析菜单树。

4. 门户渲染顶部导航和左侧菜单。

5. 菜单节点中包含子系统页面 URL。

6. 用户点击菜单。

7. 门户读取菜单节点 URL。

8. 门户通过 iframe 加载对应子系统页面。

## 5\.3 子系统页面访问流程

用户点击菜单后，门户获取菜单配置的 URL，并为 URL 附加必要参数，例如 `embed=true`、`menuId`、`systemCode` 等。随后设置 iframe 地址，加载子系统页面。

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=NGYyODZlMjk0ZjY3OWIxYWZlM2Q4MTYwZjUzOGIxNmVfNDcxNTg5ZGI1YThhOWYyMjg5OGNkZjkxNTBiZmRjMGVfSUQ6NzY3MDg0MDgwOTcxNzU5OTQ1NF8xNzkxNzkwNTk0OjE3OTE4NzY5OTRfVjM)

流程如下：

1. 用户点击门户左侧菜单。

2. 门户获取菜单节点对应 URL。

3. 门户拼接必要参数。

4. 门户设置 iframe\.src。

5. iframe 加载子系统页面。

6. 子系统识别当前用户登录态。

7. 子系统校验页面访问权限。

8. 子系统渲染业务页面。

示例：

```Plain Text
菜单名称：科技发展规划
配置 URL：https://tech.example.com/plan

最终 iframe 地址：
https://tech.example.com/plan?embed=true&menuId=tech-development-plan&systemCode=tech-info
```

# 菜单模型设计

## 6\.1 菜单字段说明

统一用户中心负责维护菜单树，建议菜单模型包含以下字段：

|**字段**|**类型**|**是否必填**|**说明**|
|---|---|---|---|
|id|string|是|菜单唯一 ID|
|parentId|string|否|父级菜单 ID|
|name|string|是|菜单名称|
|code|string|是|菜单编码|
|type|string|是|Integer：`1`=目录 / `2`=菜单 / `3`=按钮,增加 0=应用|
|icon|string|否|菜单图标|
|path|string|是|菜单访问地址，叶子菜单通常配置|
|openType|string|是|打开方式，如 iframe、newWindow、innerRoute|
|systemCode|string|否|所属子系统编码|
|permission|string|否|权限编码|
|sort|number|否|排序号|
|visible|boolean|否|是否显示|
|enabled|boolean|否|是否启用|
|keepAlive|boolean|否|是否缓存 iframe 页面|
|children|array|否|子菜单列表|
|component|string|否|组件路径，如 `system/user/index`|
|componentName|string|否<br>|组件名，如 `SystemUser`|
|alwaysShow|string|否|是否总是显示|
|~~url~~|~~string~~|~~是~~|~~子系统服务地址~~|
|~~systemType~~|~~string~~|~~是~~|~~Spa 项目，多路由应用~~|
|activeTab|string|否|需要高亮的菜单导航栏|

## 6\.2 菜单数据示例

```JSON
[
  {
    "id": "science-research",
    "name": "科学研究",
    "code": "science-research",
    "type": "directory",
    "icon": "science",
    "sort": 1,
    "children": [
      {
        "id": "tech-info-system",
        "name": "科技信息展示系统",
        "code": "tech-info-system",
        "type": "system",
        "icon": "dashboard",
        "systemCode": "tech-info",
        "children": [
          {
            "id": "tech-development-plan",
            "name": "科技发展规划",
            "code": "tech-development-plan",
            "type": "menu",
            "openType": "iframe",
            "url": "https://tech.example.com/plan",
            "systemCode": "tech-info",
            "permissionCode": "tech-info:plan:view",
            "sort": 10,
            "visible": true,
            "enabled": true
          }
        ]
      }
    ]
  }
]
```

# 统一门户前端设计

## 7\.1 页面布局

统一门户页面主要由以下区域组成：

1. 顶部导航区；

2. 左侧菜单区；

3. 用户信息区；

4. iframe 内容区；

5. 全局 loading；

6. 全局异常提示页；

7. 无权限提示页。

页面布局示意如下：

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=YzlhN2U2Y2RmZDNlZTE1MWMwNWYwN2U2YWVkYjgzZTlfY2Q2ODU3Nzk1NWRiNzI4ZmU5ZGFmNDFiZTlmY2IxMjNfSUQ6NzY3MDgzMzU5OTM0Mzk3MTI5NF8xNzkxNzkwNTk0OjE3OTE4NzY5OTRfVjM)

## 7\.2 iframe 加载逻辑

用户点击菜单后，门户判断菜单打开方式。如果 `openType` 为 `iframe`，则将菜单 URL 设置为 iframe 地址。如果 `openType` 为 `newWindow`，则在新窗口打开。

处理逻辑如下：

1. 用户点击菜单。

2. 判断菜单 openType。

3. 如果是 iframe，则拼接 iframe URL。

4. 设置当前菜单状态。

5. 更新浏览器路由参数 menuId。

6. 显示 loading。

7. 加载 iframe。

8. iframe 加载完成后隐藏 loading。

## 7\.3 iframe 内容区样式

推荐采用固定内容区高度，由 iframe 内部自行滚动。该方式实现简单、稳定，适合后台管理类系统。

示例样式：

```CSS
.portal-layout {
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.portal-body {
  flex: 1;
  display: flex;
  min-height: 0;
}

.portal-content {
  flex: 1;
  overflow: hidden;
  position: relative;
}

.portal-iframe {
  width: 100%;
  height: 100%;
  border: none;
}
```

# 统一认证与鉴权设计

## 8\.1 认证职责划分

|**环节**|**责任方**|
|---|---|
|用户登录|统一用户中心|
|Token 签发|统一用户中心|
|用户信息获取|统一用户中心|
|菜单权限过滤|统一用户中心|
|门户菜单渲染|统一门户|
|子系统页面鉴权|子系统|
|子系统接口鉴权|子系统后端或统一网关|

## 8\.2 登录态传递方式

优先采用**统一认证 Cookie ** 方案。

### 8\.2\.1 方案一：统一主域 Cookie 

如果门户和子系统部署在同一主域名下，例如：

```Plain Text
portal.example.com
auth.example.com
tech.example.com
research.example.com
research.example.com/app
```

可采用统一 Cookie 共享登录态。

Cookie 建议配置如下：

```Plain Text
Domain=.example.com
Secure=true
SameSite=None
```

子系统页面在 iframe 中加载时，可通过 Cookie 识别当前用户登录态。

### 8\.2\.2 方案二：OIDC / OAuth2 SSO

如果门户和子系统跨域较多，建议采用统一 SSO 模式。

流程如下：

1. 用户登录统一门户。

2. 用户点击菜单访问子系统 iframe。

3. 子系统检测自身登录态。

4. 如未登录，跳转统一认证中心。

5. 统一认证中心基于已有登录态完成静默认证。

6. 子系统获取自身登录态。

7. 子系统页面正常渲染。

## 8\.3 不推荐方式

不建议将长期 Token 直接拼接在 URL 中，例如：

https://tech\.example\.com/page?token=xxxx

原因如下：

1. URL 可能被浏览器历史记录保存；

2. URL 可能被代理服务器或网关日志记录；

3. URL 可能通过 Referer 泄露；

4. 长期 Token 暴露后存在较高安全风险。

如确需通过 URL 传递凭证，应仅传递短期、一次性 ticket，并由子系统服务端换取登录态。

# 权限控制设计

权限控制应分为三层，不应只依赖前端菜单隐藏。

|**权限**|**说明**|
|---|---|
|菜单权限|统一用户中心根据用户角色和权限返回用户可见菜单。门户只渲染用户有权限访问的菜单。|
|页面权限|用户点击菜单进入子系统页面后，子系统需要校验当前用户是否具备该页面访问权限。|
|接口权限|子系统后端接口必须进行权限校验，防止用户绕过门户直接访问接口。|

权限控制流程如下：

```Plain Text
用户登录
↓
统一用户中心返回用户权限
↓
统一用户中心返回可访问菜单
↓
门户渲染菜单
↓
用户点击菜单
↓
iframe 加载子系统页面
↓
子系统校验页面权限
↓
子系统接口校验数据权限
```

# iframe 安全设计

## 10\.1 iframe 嵌入控制

子系统需要允许被统一门户 iframe 嵌入，但不能允许任意网站嵌入。

不建议使用：X\-Frame\-Options: ALLOWALL

不允许设置：X\-Frame\-Options: DENY

如果配置：X\-Frame\-Options: SAMEORIGIN

则仅在门户和子系统同源时可以被嵌入。

推荐使用 CSP：

Content\-Security\-Policy: frame\-ancestors https://portal\.example\.com;

如果存在多个环境，可配置多个允许来源：

Content\-Security\-Policy: frame\-ancestors https://portal\.example\.com https://test\-portal\.example\.com;

## 10\.2 postMessage 安全

门户与子系统使用 `postMessage` 通信时，必须校验消息来源。

门户侧需要维护允许通信的子系统域名白名单。例如：

https://tech\.example\.com

https://research\.example\.com

https://example\.com/evaluation

处理要求：

1. 门户必须校验 `event.origin`；

2. 子系统发送消息时必须指定明确目标域名；

3. 生产环境禁止使用 `*` 作为目标域名；

4. 消息体应遵循统一格式；

5. 对消息类型和参数进行校验。

## 10\.3 iframe sandbox

如需进一步控制 iframe 权限，可考虑使用 sandbox 属性。

```Plain Text
<iframe
src="..."
sandbox="allow-scripts allow-same-origin allow-forms allow-downloads">
</iframe>
```

但 sandbox 限制较多，可能影响子系统正常运行，需要根据具体子系统逐一验证后启用。

# 门户与子系统通信设计

## 11\.1 通信方式

门户与 iframe 子系统之间采用浏览器标准 `postMessage` 进行通信。

主要用于以下场景：

1. 子系统通知门户页面加载完成；

2. 子系统通知门户登录过期；

3. 子系统通知门户无权限；

4. 子系统请求门户跳转菜单；

5. 子系统通知门户修改页面标题；

6. 子系统通知门户展示或隐藏全局 loading；

7. 门户通知子系统退出登录

## 11\.2 消息格式

统一消息格式建议如下：

```JSON
{
    protocol: 'iframe-bridge',   // 协议标识，用于过滤无关 message
    version: '1.0',              // 协议版本
    id: 'msg_1719700000000_0',   // 消息唯一 ID（时间戳+自增）
    action: 'page.ready',        // 具体动作（点分命名空间）
    data: { }                    // 载荷，结构由 action 定义
  }
```

## 11\.3 消息类型定义

|**消息类型**|**方向**|**说明**|
|---|---|---|
|READY|子系统 → 门户|子系统页面加载完成|
|SHOW\_LOADING|子系统 → 门户|显示全局 loading|
|HIDE\_LOADING|子系统 → 门户|隐藏全局 loading|
|SESSION\_EXPIRED|子系统 → 门户|登录态过期|
|ROUTE\_CHANGE|子系统 → 门户|*子系统路由变化*|

## 11\.4 通信示例

子系统通知门户页面加载完成：

```Plain Text
window.parent.postMessage({
    action: 'page.ready',
    protocol: 'iframe-bridge',   // 协议标识，用于过滤无关 message
    version: '1.0',              // 协议版本
    id: 'msg_1719700000000_0'
}, 'https://portal.example.com')
```

门户接收消息：

```JavaScript
window.addEventListener('message', function(event) {
  const allowOrigins = [
    'https://tech.example.com',
    'https://research.example.com'
  ]

  if (!allowOrigins.includes(event.origin)) {
    return
  }

  const data = event.data

  switch (data.type) {
    case 'READY':
      // 隐藏 loading
      break
    case 'SET_TITLE':
      // 设置标题
      break
    case 'SESSION_EXPIRED':
      // 跳转登录
      break
    case 'NO_PERMISSION':
      // 展示无权限页面
      break
  }
})
```

# 子系统接入规范

为了保证各子系统能够稳定接入统一门户，需要制定最小接入规范。

## 12\.1 URL 规范

子系统应提供可配置的页面 URL。

## 12\.2 嵌入模式规范

子系统应支持嵌入模式。

嵌入模式下隐藏以下内容：

1. 子系统自身顶部导航；

2. 子系统自身左侧菜单；

3. 子系统登录入口；

4. 子系统用户信息区；

5. 重复面包屑；

6. 重复页脚。

## 12\.3 登录规范

子系统应接入统一用户中心或统一 SSO，不应要求用户在 iframe 内重复登录。

## 12\.4 安全规范

子系统必须允许指定门户嵌入，推荐配置：

Content\-Security\-Policy: frame\-ancestors https://portal\.example\.com;

同时不得允许任意第三方站点嵌入。

## 12\.5 通信规范

子系统如需与门户交互，应使用统一 `postMessage` 协议，并遵循统一消息格式。

## 12\.6 页面适配规范

子系统页面应适配门户内容区尺寸。

建议：

```Plain Text
html,
body,
#app {
  width: 100%;
  min-height: 100%;
}
```

子系统不应强依赖浏览器全屏高度，也不应在 iframe 内重复实现门户主导航。

# 异常处理设计

## 13\.1 iframe 加载中

用户点击菜单后，门户应展示统一 loading 状态。

流程如下：

```Plain Text
菜单点击
  ↓
设置 iframe.src
  ↓
显示 loading
  ↓
iframe onload 或子系统 READY
  ↓
隐藏 loading
```

## 13\.2 iframe 加载失败

由于跨域限制，门户无法直接感知 iframe 内部错误。可采用 iframe `onload`、子系统 `READY` 消息和超时机制组合判断。

建议机制：

1. 设置 iframe 地址后启动计时器。

2. 若指定时间内未收到 onload 或 READY 消息，则认为加载异常。

3. 展示统一加载失败提示。

4. 提供重新加载按钮。

## 13\.3 无权限处理

如果子系统判断当前用户无权限，应通过 postMessage 通知门户：

```Plain Text
{
  "action": "NO_PERMISSION",
  "data": {
    "message": "当前用户无权限访问该页面"
  }
}
```

门户展示统一无权限页面。

## 13\.4 登录过期处理

如果子系统检测到登录过期，应通知门户：

```Plain Text
{
  "action": "SESSION_EXPIRED"
}
```

门户统一处理登录过期逻辑，例如跳转登录页或刷新登录态。

## 13\.5 子系统不可用处理

当子系统页面无法访问时，门户应展示统一异常页，提示：

“页面暂时无法访问，请稍后重试或联系管理员。”。

# 性能设计

## 14\.1 iframe 加载策略

采用单 iframe 模式，即当前只加载用户正在访问的菜单页面。

可选策略如下：

|**策略**|**说明**|**适用场景**|
|---|---|---|
|单 iframe|每次菜单切换重新加载 iframe|实现简单，适合初期建设|
|按需缓存|根据菜单 cache 字段决定是否缓存|适合后续优化|

## 14\.2 loading 优化

门户应统一展示 loading 状态，避免 iframe 页面加载期间出现长时间空白，提升用户体验。

# 部署设计

## 15\.1 域名规划

建议门户、用户中心和子系统部署在同一主域名下，便于统一认证和 Cookie 共享。

示例：

```Plain Text
统一门户：
https://portal.example.com
或 https://example.com/portal

统一用户中心：
https://auth.example.com

业务子系统：
https://tech.example.com
https://research.example.com
https://example.com/research
https://evaluation.example.com
https://example.com/evaluation
```

## 15\.2 网关规划

建议接口通过统一网关访问，例如：

/api/auth/\*\*

/api/tech/\*\*

/api/research/\*\*

/api/evaluation/\*\*

前端页面访问独立域名，后端接口访问统一网关。

# 接入步骤

体验环境地址： https://edu\.itic\-sci\.com/portal

1，初始化通信机制

- 发送消息  window\.parent\.postMessage\(data\)

- 接收消息:window\.addEventListener\('message', listener\)

    - 可参考下面例子，使用发布订阅模式做代码解耦

2，**重要！！！： 子页面必须通知门户PAGE\_READY**

```JSON
function ready(source, title) {
    send(Action.PAGE_READY, { source, title })  // send 是 createSubsystemMessenger 返回值
}
```



3，当前支持消息类型

```C++
LocalStorage里有存储菜单树的完整数据，key为 portal_permission_info，里面有菜单的所有信息（code，path，permissions等）

/**
 * 消息动作（点分命名空间）
 */
export const Action = {
  /** 子系统页面加载完成 */
  PAGE_READY: 'page.ready',
  /** 显示全局 loading */
  LOADING_SHOW: 'loading.show',
  /** 隐藏全局 loading */
  LOADING_HIDE: 'loading.hide',
  */***
*   * 子系统路由变化（双向）*
*   * 上行 data: { code?: string; subPath?: string }*
*   *   - code：门户在 PAGE_READY 后下发的菜单 code，子应用透传回来（无需自行获取）*
*   *   - subPath：子应用传递的路径参数，写入门户 ?subPath=，刷新时透传回子应用*
*   * 下行 data: { code?: string; subPath?: string; isMobile?: boolean }
   *   - PAGE_READY 后至少下发 code + isMobile；有深链时带 subPath；前进/后退亦同
**   *   - isMobile：是否移动端*
  */
  ROUTE_CHANGE: 'route.change',
  /** 登录过期 */
  SESSION_EXPIRED: 'session_expired',
  */***
*   * 设备形态变化（门户 → 子系统，可选）*
*   * 下行 data: { isMobile: boolean }*
*   *   - 窗口尺寸变化时下发*
*   */*
  DEVICE_CHANGE: 'device.change',
  */***
*   * 门户当前完整 URL（双向）*
*   * 上行：子系统主动请求（data 可空）*
*   * 下行 data: { href: string } — 顶层窗口 window.location.href（含 path/query/hash）*
*   */*
  PORTAL_HREF: 'portal.href',
}
```

4，登录信息

采用同源部署策略，将登录信息存储在主域名下的 Cookie 中。各子系统可直接读取该 Cookie 获取认证状态，Cookie 键名统一为 portal\_access\_token。

## 16\.1 子应用通信例子

```JavaScript
/**
 * iframe-bridge 通信 SDK（统一门户与子系统 postMessage 通信）
 *
 * 统一消息格式：
 * {
 *   protocol: 'iframe-bridge',   // 协议标识，用于过滤无关 message
 *   version: '1.0',              // 协议版本
 *   id: 'msg_1719700000000_0',   // 消息唯一 ID（时间戳+自增）
 *   action: 'page.ready',        // 具体动作（点分命名空间）
 *   data: { }                    // 载荷，结构由 action 定义
 * }
 *

 *   子系统端：
 *     import { createSubsystemMessenger } from '@/messenger'
 *     const msger = createSubsystemMessenger()
 *     msger.ready('app-a', '首页')          // 上报 page.ready
 */

/* ----------------------------- 子系统端 messenger ----------------------------- */

/**
 * 创建子系统端 messenger
 * 向门户 window.parent 发送上行消息，接收门户下行消息。
 * 仅在 iframe 嵌入环境下生效。
 */
export function createSubsystemMessenger() {
  const handlers = {}

  /** 是否处于 iframe 嵌入环境 */
  const isInIframe = window.parent !== window

  /** 注册动作处理器（按 action 匹配），返回注销函数 */
  function on(action, handler) {
    handlers[action] = handler
    return () => {
      if (handlers[action] === handler) {
        delete handlers[action]
      }
    }
  }

  function listener(event) {

    const handler = handlers[event.data.action]
    if (handler) handler(event.data.data, event.data)
  }

  if (isInIframe) {
    window.addEventListener('message', listener)
  }

  /** 向门户发送上行消息 */
  function send(action, data = {}) {
    if (!isInIframe) return
    window.parent.postMessage(createMessage(action, data), targetOrigin)
  }

  /** 发送 PAGE_READY 事件（便捷方法） */
  function ready(source, title) {
    send(Action.PAGE_READY, { source, title })
  }

  /** 销毁 messenger，移除事件监听 */
  function destroy() {
    window.removeEventListener('message', listener)
  }

  return { on, send, ready, destroy, isInIframe, Action }
}

```

# 门户本地部署与配置指南

## 部署前端门户

门户应用统一使用 /portal 作为根路径进行部署。Nginx 配置可参考以下示例：

```Bash
server {
    # 应用整体挂在 /portal/ 下（与 Vite base 一致）
    location /portal/ {
        alias /dist/;
        try_files $uri $uri/ /portal/index.html;
    }
    # /portal（无尾斜杠）→ /portal/
    location = /portal {
        return 301 /portal/;
    }
    # 其他路径统一重定向到门户入口
    location / {
        return 301 /portal/;
    }
}
```

注：

1，后端服务已采用统一集中部署，无需在本地额外部署。

2，前端输出物portal\-demo\.zip

## 统一用户中心注册应用

到统一用户中心注册应用，并获取Client ID，Client Secret，访问地址

## 修改 config\.js 配置文件

在前端项目的 config\.js 中，填入统一用户中心注册应用的相关信息：

```JavaScript
window.**APP_CONFIG** = {
  VITE_PORTAL_CLIENT_ID: '',    // 统一用户中心注册应用 CLIENT_ID
  VITE_PORTAL_REDIRECT_URI: '', // 统一用户中心注册应用 REDIRECT_URI
  VITE_COOKIE_DOMAIN: '.itic-sci.com', // Cookie 主域
};
```

## 后端添加 Client 秘钥

请联系后端同学（@宋泉）协助在服务端添加对应的 Client Secret（客户端秘钥）。

## 部署子应用至同源环境

请确保所有子应用均部署在与门户同源的运行环境中，以保障系统的正常通信与数据交互。

## 统一用户中心菜单配置

登录统一用户中心，完成相关应用菜单的路由配置与权限分配。












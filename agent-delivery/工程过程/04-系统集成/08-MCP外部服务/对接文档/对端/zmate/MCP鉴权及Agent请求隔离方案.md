<!-- feishu-doc {"doc": "RoGTd0sY2omXzexTL08cl9IEnVf"} 只改标记下面的文字；不要删改 <!-- b:... --> 标记 -->
<!-- b:UlCidZoDMoaTE6xRl8LcOhaNnMc heading1 -->
鉴权方案
<!-- b:DlQFd3yTEoZccDx3u1RcsxR8ncd ordered -->
MCP网络鉴权：统一在MCP中进行，在注册MCP时初始化鉴权头
<!-- b:D6o8dBMDUoPupOxFgaActYffnVb code -->
"servers": {
      "media-api": {
        "url": "http://127.0.0.1:3000/mcp",
        "transport": "streamable-http",
        "connectTimeout": 10,
        "timeout": 30,
        "headers": {
          "Authorization": "Bearer <token>"
        }
      }
    }
<!-- b:Vs5Vdi67OoxrOkxtNr4cZaOknCh text -->

<!-- b:JmgodiFOHoaWPxxANzocZjZBnFd heading1 -->
Agent隔离方案
<!-- b:VeGudJenvohRzkxJb7LcUisLndb text -->

<!-- b:Q44Kd0H31ozFuQxy2WncIzf7nOL heading2 -->
【可行选项】修改MCP sdk源码-直接将SessionKey加入请求头 agent:agentID:sessionID
<!-- b:NdVxd5PmLo7zerx80xucYGoJn9v text -->
MCP被调用--》硬编码sessionkey请求头--〉mcp server获取请求--》解析请求头，拿到全局唯一agentID--〉agentID和后续的用户ID做关联（中间层自动解析）"X-Session-Key": "agent:main:97819c94-0bd4-42b6-b621-477af42632c1"
<!-- b:NCXndvBG8ops46xsM5wc7i6PnEg text -->
通过agentID反向获取用户ID，从而实现用户隔离和鉴权
<!-- b:FVswdcyTWoJ6OixdRGGcrM2Cnug text -->


# P0-01 登录后企业查询默认智能搜索，四层主视觉可见

1. goto /enterprise/enterprise-search（脚本进入时已在该路由，未重复登录）
2. 断言 URL 含 enterprise-search
3. tab「智能搜索」aria-selected=true
4. 可见长占位搜索框与「搜索」按钮
5. 可见独立区块「示例查询」「热门场景」
6. 截图 after-land.png

判定：pass。

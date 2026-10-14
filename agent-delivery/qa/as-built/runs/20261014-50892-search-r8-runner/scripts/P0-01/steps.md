# P0-01 逐步实际操作（playwright-runner）

1. **goto** /enterprise/enterprise-search ✓
2. **assert_url** /enterprise/enterprise-search ✓
3. **assert_visible** tab「智能搜索」 ✓

## expect 逐条

- ✓ 路由为企业查询页且智能搜索为选中态
- ✓ 顶部自上而下依次为检索模式、搜索框、示例查询、热门场景
- ⚠ 示例查询与热门场景各占独立一行
- ✓ 蓝色搜索主视觉可见

判定：**pass**

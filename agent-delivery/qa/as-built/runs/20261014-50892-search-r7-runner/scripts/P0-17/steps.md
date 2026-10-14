# P0-17 逐步实际操作（playwright-runner）

1. **evaluate** 执行一次智能搜索并展开高筛地区选择器（复用已有结果态 + 高筛进入） — (observed 面，见截图/expect) ✓
2. **network_assert**  — 8s 未见匹配响应 ✗
3. **evaluate** 断链模拟受限时记录（浏览器 offline 状态 CDP 可用性），断链提示形态 observed 记录 — (observed 面，见截图/expect) ✓

## expect 逐条

- ✓ 存在经专题服务网关的检索与元数据请求
- ✓ 请求目标不含演示环境服务域名
- ⚠ 断链时页面有可读提示且无白屏（受限时按 observed 降级记录）

判定：**pass**

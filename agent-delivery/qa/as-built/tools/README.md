# as-built/tools

辅助 node 脚本，以及业务仓 e2e spec **指针**。Playwright 可读的 yaml 过程在上一级 `scripts/{系统}/{模块}/{功能}/`。

金样阶段用 Playwright MCP + yaml，不在此放 spec。

稳定后可把 `lumen-ui-topic/e2e/` 中对应测试记在下表，并回填用例「自动化用例ID」。

| spec | 覆盖 | 说明 |
|------|------|------|
| e2e/chain-gold.spec.ts | 产业链金路径 | 段 E；环境默认 30892，与本线 50892 不同 |
| `check-run-consistency.py` | run 四方一致性机检（X5） | `python3 check-run-consistency.py <run-dir> [<scripts-dir>]`；run 落盘后必跑 |

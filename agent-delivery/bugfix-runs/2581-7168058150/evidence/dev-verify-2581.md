# 2581 dev 部署核验（2026-11-14）

- 候选提交：7425806e1193fb34491a1ea73ea0874b7cfbc0da（fix(policy): 政策舆情评估新增政策受众反馈收集工具，评审修复统计口径）
- dev HEAD：8e123e3d2dd9a0dce1724bd2a4c8c4b0fe0699d4（merge-base --is-ancestor 已验证包含候选）
- 流水线：5436 status=success https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/lumen-ui-science-pc/-/pipelines/5436
- 部署链：push → CI 绿 → K8s dev 自动 rollout（铁律 §2.5）；末点流水线绿即部署绿
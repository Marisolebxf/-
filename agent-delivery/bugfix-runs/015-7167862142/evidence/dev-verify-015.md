# 015 dev 部署核验（2026-11-14）

- 候选提交：5e96b09d8badd432e0d14264bfebd25d60565a35（fix(policy): 241 实施路径预测补关键节点说明显式区块）
- dev HEAD：187099b95c7cb5a35b692cdbe8abf2ffb270f928（merge-base --is-ancestor 已验证包含候选）
- 流水线：5386 status=success https://aminer-edu-gitlab.jyzhang.cn/sz-gkx/gkx-lumen/lumen-ui-science-pc/-/pipelines/5386
- 部署链：push → CI 绿 → K8s dev 自动 rollout（铁律 §2.5）；末点流水线绿即部署绿
- 中间 failed 流水线 5376/5377 属并行会话中间提交，非本单候选引入
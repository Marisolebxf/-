# devops 日常规约

> 维护：devops。改集群配置或发布步骤时，先改本目录，再改集群。  
> 索引页：[工程过程/部署.md](../工程过程/部署.md)。流水线阶段仍以 [cicd-pipeline.md](../cicd-pipeline.md) 为准。

| 页 | 写什么 |
|---|---|
| [环境说明.md](./环境说明.md) | 现网集群、命名空间、发布入口。组件清单不在这里复制 |
| [发布注意事项.md](./发布注意事项.md) | 发布前要核对的事。模型配置怎么进集群写在这里 |
| [集群Secret.md](./集群Secret.md) | Secret 名叫什么、有哪些键、谁引用。不写口令 |

密钥、kubeconfig、Harbor 口令只放 GitLab Masked 变量或集群 Secret，不进 git，不进本文。

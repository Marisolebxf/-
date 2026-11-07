# -*- coding: utf-8 -*-
# TA 联调 · show_py 启动器：自读 WORKPACK README 提取久新凭据，程序化起 uvicorn
import os
import re
import sys

README = (r"e:\work\上达通\项目\深圳GKX\gkx-lumen\gkx-orchestration\agent-delivery"
          r"\data\GDF\派单包\技术节点产业映射\GDF-TECH-NODE-WORKPACK\README.md")
raw = open(README, encoding="utf-8").read()
pwd = re.search(r"密码 \| \`(.+?)\`。", raw).group(1)

os.environ.update({
    "GKX_JIUXIN_ENABLED": "1",
    "GKX_JIUXIN_HOST": "47.93.119.170",
    "GKX_JIUXIN_PORT": "29030",
    "GKX_JIUXIN_USER": "test2",
    "GKX_JIUXIN_PASSWORD": pwd,
    "GKX_JIUXIN_DATABASE": "gkx_technology_analysis_dev",
    "GKX_JIUXIN_READ_TIMEOUT": "300",
    "GKX_JIUXIN_CACHE_TTL_SECONDS": "3600",
})
os.chdir(r"e:\work\上达通\项目\深圳GKX\gkx-lumen\repos\lumen-topic-py")
sys.path.insert(0, os.getcwd())
print("starting uvicorn :8082, pwd_len=%d" % len(pwd), flush=True)

import uvicorn  # noqa: E402
from gkx_show_service.main import app  # noqa: E402

uvicorn.run(app, host="0.0.0.0", port=8082, log_level="info")

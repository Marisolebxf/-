# -*- coding: utf-8 -*-
"""复跑 Z01 判据，不写文件。"""
import importlib.util
from pathlib import Path

path = Path(__file__).with_name("Z01-merge.py")
spec = importlib.util.spec_from_file_location("z01merge", path)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
mod.verify_outputs()
print("OK")

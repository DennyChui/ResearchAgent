#!/usr/bin/env python3
"""
ResearchAgent CLI 入口点

这是新的统一命令行入口点，替代旧的main.py。
"""

import sys
import os

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from cli.cli import main

if __name__ == "__main__":
    sys.exit(main())
#!/usr/bin/env python3
"""
ResearchAgent CLI Package

提供统一的命令行接口，支持所有ResearchAgent功能。
"""

from .cli import ResearchAgentCLI
from .commands import *

__version__ = "0.2.0"
__all__ = ["ResearchAgentCLI"]
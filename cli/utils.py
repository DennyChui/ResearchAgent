#!/usr/bin/env python3
"""
CLI工具函数

提供日志、显示等通用功能。
"""

import logging
import sys
from typing import Optional


def setup_logging(level: int = logging.INFO) -> None:
    """设置日志配置"""
    # 创建日志格式
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )

    # 控制台处理器
    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setFormatter(formatter)

    # 根日志器配置
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.addHandler(console_handler)


def print_banner() -> None:
    """打印欢迎横幅"""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                     ResearchAgent CLI                        ║
║                   AI研究助手命令行工具                        ║
║                                                              ║
║  版本: 0.2.0                                               ║
║  功能: 搜索 | 研究 | 测试 | 示例 | 交互                      ║
╚══════════════════════════════════════════════════════════════╝

使用 'researchagent --help' 查看详细帮助
使用 'researchagent <command> --help' 查看命令帮助
"""
    print(banner)


def print_help() -> None:
    """打印帮助信息"""
    help_text = """
🤖 ResearchAgent CLI - AI研究助手

用法:
  researchagent <command> [options]

可用命令:
  search <query>       - 执行搜索查询
  research <question>  - 使用ReAct Agent进行深度研究
  test                 - 运行测试套件
  example [name]       - 运行使用示例
  interactive          - 启动交互式模式

全局选项:
  --debug             - 启用调试模式
  --version           - 显示版本信息
  --help              - 显示帮助信息

示例:
  researchagent search "Python编程教程"
  researchagent search "机器学习" --type scholar
  researchagent research "量子计算的应用前景"
  researchagent test --tool search
  researchagent interactive --mode research
  researchagent example react

更多信息请访问: https://github.com/DennyChui/ResearchAgent
"""
    print(help_text)


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """截断文本到指定长度"""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def format_time(seconds: float) -> str:
    """格式化时间显示"""
    if seconds < 1:
        return f"{int(seconds * 1000)}ms"
    elif seconds < 60:
        return f"{seconds:.1f}s"
    else:
        minutes = int(seconds // 60)
        remaining = seconds % 60
        return f"{minutes}m {remaining:.1f}s"


def validate_url(url: str) -> bool:
    """验证URL格式"""
    try:
        from urllib.parse import urlparse
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def get_terminal_width() -> int:
    """获取终端宽度"""
    try:
        import shutil
        return shutil.get_terminal_size().columns
    except Exception:
        return 80
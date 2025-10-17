#!/usr/bin/env python3
"""
ResearchAgent CLI 主入口

提供现代化的命令行界面，支持所有ResearchAgent功能。
"""

import sys
import argparse
from typing import List, Optional
import logging

from .commands import (
    SearchCommand,
    ResearchCommand,
    TestCommand,
    ExampleCommand,
    InteractiveCommand
)
from .utils import setup_logging, print_banner, print_help


class ResearchAgentCLI:
    """ResearchAgent 命令行接口主类"""

    def __init__(self, debug: bool = False):
        self.debug = debug
        self.commands = {
            'search': SearchCommand(),
            'research': ResearchCommand(),
            'test': TestCommand(),
            'example': ExampleCommand(),
            'interactive': InteractiveCommand()
        }

        # 设置日志
        level = logging.DEBUG if debug else logging.INFO
        setup_logging(level)

    def create_parser(self) -> argparse.ArgumentParser:
        """创建命令行参数解析器"""
        parser = argparse.ArgumentParser(
            prog="researchagent",
            description="ResearchAgent - AI研究助手",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
示例用法:
  researchagent search "Python编程教程"
  researchagent research "量子计算的最新发展"
  researchagent test
  researchagent interactive
            """
        )

        # 全局选项
        parser.add_argument(
            '--debug',
            action='store_true',
            help='启用调试模式'
        )
        parser.add_argument(
            '--version',
            action='version',
            version='%(prog)s 0.2.0'
        )

        # 子命令
        subparsers = parser.add_subparsers(
            dest='command',
            help='可用命令',
            metavar='COMMAND'
        )

        # 为每个命令创建子解析器
        for name, command in self.commands.items():
            command.create_parser(subparsers)

        return parser

    def run(self, args: Optional[List[str]] = None) -> int:
        """运行CLI"""
        try:
            # 显示欢迎信息
            if args is None or len(args) <= 1:
                print_banner()

            parser = self.create_parser()
            parsed_args = parser.parse_args(args)

            # 设置调试模式
            if parsed_args.debug:
                self.debug = True
                logging.getLogger().setLevel(logging.DEBUG)

            # 执行命令
            if not hasattr(parsed_args, 'command') or not parsed_args.command:
                print_help()
                return 0

            command = self.commands.get(parsed_args.command)
            if not command:
                print(f"❌ 未知命令: {parsed_args.command}")
                return 1

            return command.execute(parsed_args)

        except KeyboardInterrupt:
            print("\n👋 操作已取消")
            return 130
        except Exception as e:
            print(f"❌ 执行出错: {e}")
            if self.debug:
                import traceback
                traceback.print_exc()
            return 1


def main() -> int:
    """CLI主入口点"""
    cli = ResearchAgentCLI()
    return cli.run()


if __name__ == "__main__":
    sys.exit(main())
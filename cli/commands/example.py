#!/usr/bin/env python3
"""
示例命令实现

运行使用示例。
"""

import argparse
import subprocess
import sys
import os
from typing import List, Optional

from .base import BaseCommand


class ExampleCommand(BaseCommand):
    """示例命令"""

    def __init__(self):
        super().__init__(
            name="example",
            description="运行使用示例"
        )

    def create_parser(self, subparsers: argparse._SubParsersAction) -> argparse.ArgumentParser:
        """创建示例命令的参数解析器"""
        parser = subparsers.add_parser(
            'example',
            help=self.description,
            description=self.description
        )

        parser.add_argument(
            'name',
            nargs='?',
            choices=['basic', 'react', 'tools'],
            default='basic',
            help='示例名称 (默认: basic)'
        )

        parser.add_argument(
            '--list',
            action='store_true',
            help='列出所有可用示例'
        )

        return parser

    def execute(self, args: argparse.Namespace) -> int:
        """执行示例命令"""
        try:
            if args.list:
                return self._list_examples()

            example_files = {
                'basic': 'examples/basic_usage.py',
                'react': 'examples/react_agent_demo.py',
                'tools': 'examples/tools_demo.py'
            }

            example_descriptions = {
                'basic': '基础工具使用示例',
                'react': 'ReAct Agent智能研究示例',
                'tools': '所有工具功能演示'
            }

            example_file = example_files.get(args.name)
            if not example_file:
                self.print_error(f"未知示例: {args.name}")
                return 1

            if not os.path.exists(example_file):
                self.print_error(f"示例文件不存在: {example_file}")
                return 1

            print(f"📚 运行示例: {example_descriptions[args.name]}")
            print(f"📄 文件: {example_file}")
            print("=" * 60)

            # 运行示例
            cmd = ['uv', 'run', 'python', example_file]
            try:
                result = subprocess.run(cmd, cwd=".")

                if result.returncode == 0:
                    self.print_success("示例运行完成")
                    return 0
                else:
                    self.print_error("示例运行失败")
                    return 1

            except Exception as e:
                self.print_error(f"运行示例时出错: {e}")
                return 1

        except Exception as e:
            self.print_error(f"示例执行失败: {e}")
            return 1

    def _list_examples(self) -> int:
        """列出所有可用示例"""
        print("📋 可用示例:")
        print("=" * 60)

        examples = [
            ('basic', '基础工具使用示例', 'examples/basic_usage.py'),
            ('react', 'ReAct Agent智能研究示例', 'examples/react_agent_demo.py'),
            ('tools', '所有工具功能演示', 'examples/tools_demo.py')
        ]

        for name, description, file_path in examples:
            exists = "✅" if os.path.exists(file_path) else "❌"
            print(f"  {name:<10} - {description:<30} {exists}")

        print("\n使用方法:")
        print("  researchagent example <name>")
        print("  researchagent example --list")
        return 0
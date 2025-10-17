#!/usr/bin/env python3
"""
测试命令实现

运行项目测试套件。
"""

import argparse
import subprocess
import sys
from typing import List, Optional

from .base import BaseCommand


class TestCommand(BaseCommand):
    """测试命令"""

    def __init__(self):
        super().__init__(
            name="test",
            description="运行测试套件"
        )

    def create_parser(self, subparsers: argparse._SubParsersAction) -> argparse.ArgumentParser:
        """创建测试命令的参数解析器"""
        parser = subparsers.add_parser(
            'test',
            help=self.description,
            description=self.description
        )

        parser.add_argument(
            '--type',
            choices=['all', 'unit', 'integration'],
            default='all',
            help='测试类型 (默认: all)'
        )

        parser.add_argument(
            '--tool',
            choices=['search', 'scholar', 'jina', 'react'],
            help='测试特定工具'
        )

        parser.add_argument(
            '--verbose',
            action='store_true',
            help='详细输出'
        )

        parser.add_argument(
            '--coverage',
            action='store_true',
            help='生成覆盖率报告'
        )

        return parser

    def execute(self, args: argparse.Namespace) -> int:
        """执行测试命令"""
        try:
            print("🧪 运行测试套件...")
            print("=" * 60)

            # 构建测试命令
            test_commands = []

            if args.tool:
                # 测试特定工具
                tool_tests = {
                    'search': 'tests/test_google_search.py',
                    'scholar': 'tests/test_google_scholar.py',
                    'jina': 'tests/test_jina_url_visit.py',
                    'react': 'tests/test_react_agent.py'
                }
                if args.tool in tool_tests:
                    test_commands.append([
                        'uv', 'run', 'python', tool_tests[args.tool]
                    ])
            else:
                # 根据类型选择测试
                if args.type in ['all', 'unit']:
                    test_commands.append([
                        'uv', 'run', 'python', 'test.py', 'quick'
                    ])

                if args.type in ['all', 'integration']:
                    test_commands.append([
                        'uv', 'run', 'python', 'test.py', 'all'
                    ])

            # 执行测试
            total_passed = 0
            total_failed = 0

            for i, cmd in enumerate(test_commands, 1):
                print(f"\n📋 运行测试 {i}/{len(test_commands)}:")
                print(f"命令: {' '.join(cmd)}")
                print("-" * 40)

                try:
                    result = subprocess.run(
                        cmd,
                        capture_output=not args.verbose,
                        text=True,
                        cwd="."
                    )

                    if result.returncode == 0:
                        self.print_success("测试通过")
                        total_passed += 1
                        if result.stdout:
                            print(result.stdout)
                    else:
                        self.print_error("测试失败")
                        total_failed += 1
                        if result.stderr:
                            print(result.stderr)

                except Exception as e:
                    self.print_error(f"运行测试时出错: {e}")
                    total_failed += 1

            # 输出总结
            print("\n" + "=" * 60)
            print(f"📊 测试总结:")
            print(f"   ✅ 通过: {total_passed}")
            print(f"   ❌ 失败: {total_failed}")
            print(f"   📈 总计: {total_passed + total_failed}")

            if total_failed == 0:
                self.print_success("所有测试都通过了!")
                return 0
            else:
                self.print_error(f"{total_failed} 个测试失败")
                return 1

        except Exception as e:
            self.print_error(f"测试执行失败: {e}")
            return 1
#!/usr/bin/env python3
"""
搜索命令实现

支持Google搜索和Google学术搜索。
"""

import argparse
import sys
from typing import Optional

from .base import BaseCommand

try:
    from inference import GoogleSearchTool, GoogleScholarTool
except ImportError:
    print("❌ 无法导入工具模块")
    sys.exit(1)


class SearchCommand(BaseCommand):
    """搜索命令"""

    def __init__(self):
        super().__init__(
            name="search",
            description="执行搜索查询"
        )

    def create_parser(self, subparsers: argparse._SubParsersAction) -> argparse.ArgumentParser:
        """创建搜索命令的参数解析器"""
        parser = subparsers.add_parser(
            'search',
            help=self.description,
            description=self.description
        )

        parser.add_argument(
            'query',
            help='搜索查询内容'
        )

        parser.add_argument(
            '--type',
            choices=['web', 'scholar'],
            default='web',
            help='搜索类型: web (网络搜索) 或 scholar (学术搜索)'
        )

        parser.add_argument(
            '--limit',
            type=int,
            default=10,
            help='结果数量限制 (默认: 10)'
        )

        parser.add_argument(
            '--output',
            choices=['text', 'json'],
            default='text',
            help='输出格式 (默认: text)'
        )

        return parser

    def execute(self, args: argparse.Namespace) -> int:
        """执行搜索命令"""
        try:
            print(f"🔍 搜索: {args.query}")
            print(f"📊 类型: {args.type}")
            print("=" * 60)

            # 选择工具
            if args.type == 'scholar':
                tool = GoogleScholarTool()
                search_type = "Google Scholar"
            else:
                tool = GoogleSearchTool()
                search_type = "Google"

            # 执行搜索
            result = tool.call({"query": args.query})

            # 输出结果
            if args.output == 'json':
                import json
                print(json.dumps({
                    "query": args.query,
                    "type": args.type,
                    "source": search_type,
                    "result": result
                }, ensure_ascii=False, indent=2))
            else:
                print(result)

            self.print_success(f"{search_type}搜索完成")
            return 0

        except Exception as e:
            self.print_error(f"搜索失败: {e}")
            return 1
#!/usr/bin/env python3
"""
研究命令实现

使用ReAct Agent进行深度研究。
"""

import argparse
import sys
from typing import Optional

from .base import BaseCommand

try:
    from inference.react_agent import ReActAgent
except ImportError:
    print("❌ 无法导入ReAct Agent模块")
    sys.exit(1)


class ResearchCommand(BaseCommand):
    """研究命令"""

    def __init__(self):
        super().__init__(
            name="research",
            description="使用ReAct Agent进行深度研究"
        )

    def create_parser(self, subparsers: argparse._SubParsersAction) -> argparse.ArgumentParser:
        """创建研究命令的参数解析器"""
        parser = subparsers.add_parser(
            'research',
            help=self.description,
            description=self.description
        )

        parser.add_argument(
            'question',
            help='研究问题'
        )

        parser.add_argument(
            '--max-steps',
            type=int,
            default=10,
            help='最大推理步骤数 (默认: 10)'
        )

        parser.add_argument(
            '--timeout',
            type=int,
            default=300,
            help='超时时间，秒 (默认: 300)'
        )

        parser.add_argument(
            '--save',
            help='保存结果到文件'
        )

        parser.add_argument(
            '--quiet',
            action='store_true',
            help='静默模式，只输出最终结果'
        )

        return parser

    def execute(self, args: argparse.Namespace) -> int:
        """执行研究命令"""
        try:
            if not args.quiet:
                print(f"🤖 ReAct Agent 研究: {args.question}")
                print("=" * 60)

            # 创建ReAct Agent
            agent = ReActAgent()

            # 执行研究
            result = agent.research(question=args.question)

            # 输出结果
            if not args.quiet:
                print("\n📋 研究结果:")
                print("=" * 60)

            print(result)
            print("=" * 60)

            if not args.quiet:
                print(f"\n📊 研究统计:")
                print(f"   - LLM调用次数: {getattr(agent, 'llm_calls', 'N/A')}")
                print(f"   - 消息总数: {len(getattr(agent, 'messages', []))}")
                print(f"   - 推理步骤: {getattr(agent, 'step_count', 'N/A')}")

            # 保存结果
            if args.save:
                with open(args.save, 'w', encoding='utf-8') as f:
                    f.write(f"研究问题: {args.question}\n")
                    f.write("=" * 60 + "\n")
                    f.write(result + "\n")
                    f.write("=" * 60 + "\n")

                    if not args.quiet:
                        f.write(f"\n研究统计:\n")
                        f.write(f"- LLM调用次数: {getattr(agent, 'llm_calls', 'N/A')}\n")
                        f.write(f"- 消息总数: {len(getattr(agent, 'messages', []))}\n")
                        f.write(f"- 推理步骤: {getattr(agent, 'step_count', 'N/A')}\n")

                self.print_success(f"结果已保存到: {args.save}")

            self.print_success("研究完成")
            return 0

        except Exception as e:
            self.print_error(f"研究失败: {e}")
            return 1
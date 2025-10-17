#!/usr/bin/env python3
"""
交互式命令实现

启动交互式模式。
"""

import argparse
import sys
from typing import Optional

from .base import BaseCommand

try:
    from inference import GoogleSearchTool, GoogleScholarTool, JinaURLVisitTool, ReActAgent
except ImportError:
    print("❌ 无法导入工具模块")
    sys.exit(1)


class InteractiveCommand(BaseCommand):
    """交互式命令"""

    def __init__(self):
        super().__init__(
            name="interactive",
            description="启动交互式模式"
        )

    def create_parser(self, subparsers: argparse._SubParsersAction) -> argparse.ArgumentParser:
        """创建交互式命令的参数解析器"""
        parser = subparsers.add_parser(
            'interactive',
            help=self.description,
            description=self.description
        )

        parser.add_argument(
            '--mode',
            choices=['search', 'research', 'tools'],
            default='search',
            help='交互模式类型 (默认: search)'
        )

        return parser

    def execute(self, args: argparse.Namespace) -> int:
        """执行交互式命令"""
        try:
            if args.mode == 'search':
                return self._search_interactive()
            elif args.mode == 'research':
                return self._research_interactive()
            elif args.mode == 'tools':
                return self._tools_interactive()

            return 0

        except KeyboardInterrupt:
            print("\n👋 再见!")
            return 0
        except Exception as e:
            self.print_error(f"交互模式出错: {e}")
            return 1

    def _search_interactive(self) -> int:
        """搜索交互模式"""
        print("🤖 ResearchAgent 交互式搜索模式")
        print("可用命令: help, quit, scholar <query>, visit <url>")
        print("=" * 60)

        search_tool = GoogleSearchTool()
        scholar_tool = GoogleScholarTool()
        visit_tool = JinaURLVisitTool()

        while True:
            try:
                user_input = input("\n🔍 请输入搜索查询或命令: ").strip()

                if not user_input:
                    continue

                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 再见!")
                    break

                if user_input.lower() == 'help':
                    self._print_search_help()
                    continue

                if user_input.startswith('scholar '):
                    query = user_input[7:].strip()
                    if query:
                        print(f"🎓 学术搜索: {query}")
                        print("-" * 40)
                        result = scholar_tool.call({"query": query})
                        print(result)
                    continue

                if user_input.startswith('visit '):
                    url = user_input[6:].strip()
                    if url:
                        print(f"🌐 访问网页: {url}")
                        print("-" * 40)
                        goal = input("请输入访问目标: ").strip()
                        result = visit_tool.call({"url": url, "goal": goal})
                        print(result)
                    continue

                # 默认执行网络搜索
                print(f"🔍 搜索: {user_input}")
                print("-" * 40)
                result = search_tool.call({"query": user_input})
                print(result)

            except KeyboardInterrupt:
                print("\n👋 再见!")
                break
            except Exception as e:
                self.print_error(f"搜索出错: {e}")

        return 0

    def _research_interactive(self) -> int:
        """研究交互模式"""
        print("🤖 ResearchAgent 智能研究模式")
        print("输入研究问题，ReAct Agent将进行深度分析")
        print("可用命令: help, quit, reset")
        print("=" * 60)

        agent = ReActAgent()

        while True:
            try:
                user_input = input("\n🤔 请输入研究问题: ").strip()

                if not user_input:
                    continue

                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 再见!")
                    break

                if user_input.lower() == 'help':
                    self._print_research_help()
                    continue

                if user_input.lower() == 'reset':
                    print("🔄 重置代理状态")
                    agent.reset()
                    continue

                # 执行研究
                print(f"🔬 开始研究: {user_input}")
                print("=" * 60)
                result = agent.research(user_input)

                print("\n📋 研究结果:")
                print("=" * 60)
                print(result)
                print("=" * 60)

                print(f"\n📊 研究统计:")
                print(f"   - LLM调用次数: {getattr(agent, 'llm_calls', 'N/A')}")
                print(f"   - 消息总数: {len(getattr(agent, 'messages', []))}")

            except KeyboardInterrupt:
                print("\n👋 再见!")
                break
            except Exception as e:
                self.print_error(f"研究出错: {e}")

        return 0

    def _tools_interactive(self) -> int:
        """工具演示交互模式"""
        print("🛠️  ResearchAgent 工具演示模式")
        print("选择要演示的工具功能")
        print("=" * 60)

        while True:
            try:
                print("\n可用工具:")
                print("  1. Google搜索")
                print("  2. Google学术搜索")
                print("  3. Jina网页访问")
                print("  4. ReAct智能研究")
                print("  q. 退出")

                choice = input("\n请选择工具 (1-4): ").strip()

                if choice.lower() == 'q':
                    print("👋 再见!")
                    break

                if choice == '1':
                    query = input("请输入搜索查询: ").strip()
                    if query:
                        tool = GoogleSearchTool()
                        result = tool.call({"query": query})
                        print(result)

                elif choice == '2':
                    query = input("请输入学术查询: ").strip()
                    if query:
                        tool = GoogleScholarTool()
                        result = tool.call({"query": query})
                        print(result)

                elif choice == '3':
                    url = input("请输入URL: ").strip()
                    goal = input("请输入访问目标: ").strip()
                    if url and goal:
                        tool = JinaURLVisitTool()
                        result = tool.call({"url": url, "goal": goal})
                        print(result)

                elif choice == '4':
                    question = input("请输入研究问题: ").strip()
                    if question:
                        agent = ReActAgent()
                        result = agent.research(question)
                        print(result)

                else:
                    print("❌ 无效选择")

            except KeyboardInterrupt:
                print("\n👋 再见!")
                break
            except Exception as e:
                self.print_error(f"工具演示出错: {e}")

        return 0

    def _print_search_help(self):
        """打印搜索模式帮助"""
        help_text = """
🔍 搜索模式帮助:
  <query>           - 执行网络搜索
  scholar <query>   - 执行学术搜索
  visit <url>       - 访问网页内容
  help              - 显示此帮助
  quit              - 退出程序
        """
        print(help_text)

    def _print_research_help(self):
        """打印研究模式帮助"""
        help_text = """
🔬 研究模式帮助:
  <question>    - 输入研究问题，ReAct Agent将进行深度分析
  reset        - 重置代理状态，清除历史对话
  help         - 显示此帮助
  quit         - 退出程序
        """
        print(help_text)
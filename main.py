#!/usr/bin/env python3
"""
ResearchAgent 主程序

提供统一的入口点来运行不同的工具和示例。
"""

import sys
import argparse
from typing import Optional

from inference import GoogleSearchTool


def run_search_tool(query: str):
    """运行Google搜索工具"""
    print(f"🔍 搜索: {query}")
    print("=" * 50)

    tool = GoogleSearchTool()
    result = tool.call({"query": query})
    print(result)


def run_tests():
    """运行所有测试"""
    print("🧪 运行测试套件...")
    print("=" * 50)

    try:
        import subprocess
        result = subprocess.run([
            "uv", "run", "python", "tests/test_google_search.py"
        ], capture_output=True, text=True, cwd=".")

        if result.returncode == 0:
            print(result.stdout)
            print("✅ 所有测试通过!")
        else:
            print("❌ 测试失败:")
            print(result.stderr)

    except Exception as e:
        print(f"❌ 运行测试时出错: {e}")


def run_examples():
    """运行使用示例"""
    print("📚 运行使用示例...")
    print("=" * 50)

    try:
        import subprocess
        result = subprocess.run([
            "uv", "run", "python", "example_usage.py"
        ], capture_output=True, text=True, cwd=".")

        if result.returncode == 0:
            print(result.stdout)
        else:
            print("❌ 运行示例失败:")
            print(result.stderr)

    except Exception as e:
        print(f"❌ 运行示例时出错: {e}")


def interactive_mode():
    """交互式模式"""
    print("🤖 ResearchAgent 交互式模式")
    print("输入 'help' 查看帮助，输入 'quit' 退出")
    print("=" * 50)

    tool = GoogleSearchTool()

    while True:
        try:
            user_input = input("\n🔍 请输入搜索查询: ").strip()

            if user_input.lower() in ['quit', 'exit', 'q']:
                print("👋 再见!")
                break
            elif user_input.lower() == 'help':
                print_help()
            elif not user_input:
                print("❌ 请输入有效的搜索查询")
                continue
            else:
                result = tool.call({"query": user_input})
                print(result)

        except KeyboardInterrupt:
            print("\n👋 再见!")
            break
        except Exception as e:
            print(f"❌ 搜索出错: {e}")


def print_help():
    """显示帮助信息"""
    help_text = """
🤖 ResearchAgent 帮助信息

命令行参数:
  python main.py search <query>    - 执行Google搜索
  python main.py test             - 运行测试套件
  python main.py example          - 运行使用示例
  python main.py interactive      - 进入交互式模式
  python main.py help             - 显示此帮助信息

交互式模式命令:
  help     - 显示帮助信息
  quit     - 退出程序
  其他输入 - 执行Google搜索

示例:
  python main.py search "Python编程教程"
  python main.py interactive
"""
    print(help_text)


def main():
    """主程序入口"""
    parser = argparse.ArgumentParser(
        description="ResearchAgent - AI研究助手",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_subparsers(dest='command', help='可用命令')

    # 搜索命令
    search_parser = subparsers.add_parser('search', help='执行Google搜索')
    search_parser.add_argument('query', help='搜索查询')

    # 测试命令
    subparsers.add_parser('test', help='运行测试套件')

    # 示例命令
    subparsers.add_parser('example', help='运行使用示例')

    # 交互模式命令
    subparsers.add_parser('interactive', help='进入交互式模式')

    # 帮助命令
    subparsers.add_parser('help', help='显示帮助信息')

    # 如果没有参数，显示帮助
    if len(sys.argv) == 1:
        print_help()
        return

    args = parser.parse_args()

    if args.command == 'search':
        run_search_tool(args.query)
    elif args.command == 'test':
        run_tests()
    elif args.command == 'example':
        run_examples()
    elif args.command == 'interactive':
        interactive_mode()
    elif args.command == 'help':
        print_help()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

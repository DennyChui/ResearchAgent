#!/usr/bin/env python3
"""
ResearchAgent 基础使用示例

演示如何单独使用各种工具。
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from inference import GoogleSearchTool, GoogleScholarTool, JinaURLVisitTool


def example_google_search():
    """Google搜索示例"""
    print("🔍 Google搜索示例")
    print("=" * 50)

    search_tool = GoogleSearchTool()

    # 示例查询
    queries = [
        "Python编程最佳实践",
        "机器学习最新进展",
        "人工智能伦理问题"
    ]

    for query in queries:
        print(f"\n搜索: {query}")
        print("-" * 40)
        try:
            result = search_tool.call({"query": query})
            print(result[:500] + "..." if len(result) > 500 else result)
        except Exception as e:
            print(f"❌ 搜索失败: {e}")


def example_google_scholar():
    """Google学术搜索示例"""
    print("\n🎓 Google学术搜索示例")
    print("=" * 50)

    scholar_tool = GoogleScholarTool()

    # 学术查询示例
    academic_queries = [
        "deep learning",
        "quantum computing applications",
        "climate change research 2024"
    ]

    for query in academic_queries:
        print(f"\n学术搜索: {query}")
        print("-" * 40)
        try:
            result = scholar_tool.call({"query": query})
            print(result[:500] + "..." if len(result) > 500 else result)
        except Exception as e:
            print(f"❌ 学术搜索失败: {e}")


def example_jina_url_visit():
    """Jina网页访问示例"""
    print("\n🌐 Jina网页访问示例")
    print("=" * 50)

    visit_tool = JinaURLVisitTool()

    # 网页访问示例
    urls_goals = [
        ("https://www.python.org/about/", "了解Python的历史和特点"),
        ("https://github.com/QwenLM/Qwen-Agent", "了解Qwen-Agent项目"),
        ("https://serper.dev/", "了解Serper搜索API")
    ]

    for url, goal in urls_goals:
        print(f"\n访问: {url}")
        print(f"目标: {goal}")
        print("-" * 40)
        try:
            result = visit_tool.call({"url": url, "goal": goal})
            print(result[:400] + "..." if len(result) > 400 else result)
        except Exception as e:
            print(f"❌ 网页访问失败: {e}")


def interactive_demo():
    """交互式演示"""
    print("\n🎮 交互式工具演示")
    print("=" * 50)

    # 创建工具实例
    search_tool = GoogleSearchTool()
    scholar_tool = GoogleScholarTool()
    visit_tool = JinaURLVisitTool()

    while True:
        print("\n选择要演示的功能:")
        print("1. Google搜索")
        print("2. Google学术搜索")
        print("3. Jina网页访问")
        print("q. 退出")

        choice = input("\n请选择 (1-3): ").strip()

        if choice.lower() == 'q':
            print("👋 再见!")
            break

        try:
            if choice == '1':
                query = input("请输入搜索查询: ").strip()
                if query:
                    print(f"\n🔍 搜索: {query}")
                    result = search_tool.call({"query": query})
                    print(result)

            elif choice == '2':
                query = input("请输入学术查询: ").strip()
                if query:
                    print(f"\n🎓 学术搜索: {query}")
                    result = scholar_tool.call({"query": query})
                    print(result)

            elif choice == '3':
                url = input("请输入URL: ").strip()
                goal = input("请输入访问目标: ").strip()
                if url and goal:
                    print(f"\n🌐 访问: {url}")
                    print(f"目标: {goal}")
                    result = visit_tool.call({"url": url, "goal": goal})
                    print(result)

            else:
                print("❌ 无效选择")

        except Exception as e:
            print(f"❌ 执行失败: {e}")


def main():
    """主函数"""
    print("📚 ResearchAgent 基础工具使用示例")
    print("=" * 60)

    print("选择示例类型:")
    print("1. Google搜索示例")
    print("2. Google学术搜索示例")
    print("3. Jina网页访问示例")
    print("4. 交互式演示")
    print("5. 运行所有示例")

    choice = input("\n请选择 (1-5): ").strip()

    if choice == '1':
        example_google_search()
    elif choice == '2':
        example_google_scholar()
    elif choice == '3':
        example_jina_url_visit()
    elif choice == '4':
        interactive_demo()
    elif choice == '5':
        example_google_search()
        example_google_scholar()
        example_jina_url_visit()
    else:
        print("❌ 无效选择，运行所有示例...")
        example_google_search()
        example_google_scholar()
        example_jina_url_visit()

    print("\n✅ 示例演示完成!")


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
ResearchAgent 工具完整演示

展示所有工具的完整功能和使用方法。
"""

import sys
import os
import time
from typing import Dict, Any

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from inference import GoogleSearchTool, GoogleScholarTool, JinaURLVisitTool, ReActAgent


def demo_google_search():
    """演示Google搜索功能"""
    print("🔍 Google搜索工具演示")
    print("=" * 60)

    tool = GoogleSearchTool()

    # 测试不同类型的查询
    test_queries = [
        "最新人工智能技术趋势",
        "Python编程语言特点",
        "量子计算商业应用"
    ]

    for i, query in enumerate(test_queries, 1):
        print(f"\n📋 查询 {i}: {query}")
        print("-" * 40)

        try:
            start_time = time.time()
            result = tool.call({"query": query})
            end_time = time.time()

            print(f"⏱️  用时: {end_time - start_time:.2f}秒")
            print(f"📊 结果长度: {len(result)} 字符")

            # 显示摘要
            if len(result) > 300:
                print(result[:300] + "...\n[结果已截断]")
            else:
                print(result)

        except Exception as e:
            print(f"❌ 搜索失败: {e}")


def demo_google_scholar():
    """演示Google学术搜索功能"""
    print("\n🎓 Google学术搜索工具演示")
    print("=" * 60)

    tool = GoogleScholarTool()

    # 学术研究查询
    academic_queries = [
        "deep learning neural networks",
        "quantum computing algorithms",
        "renewable energy storage"
    ]

    for i, query in enumerate(academic_queries, 1):
        print(f"\n📋 学术查询 {i}: {query}")
        print("-" * 40)

        try:
            start_time = time.time()
            result = tool.call({"query": query})
            end_time = time.time()

            print(f"⏱️  用时: {end_time - start_time:.2f}秒")
            print(f"📊 结果长度: {len(result)} 字符")

            # 显示摘要
            if len(result) > 300:
                print(result[:300] + "...\n[结果已截断]")
            else:
                print(result)

        except Exception as e:
            print(f"❌ 学术搜索失败: {e}")


def demo_jina_url_visit():
    """演示Jina网页访问功能"""
    print("\n🌐 Jina网页访问工具演示")
    print("=" * 60)

    tool = JinaURLVisitTool()

    # 网页访问测试
    url_tests = [
        {
            "url": "https://www.python.org/about/",
            "goal": "获取Python编程语言的介绍和历史信息"
        },
        {
            "url": "https://github.com/QwenLM/Qwen-Agent",
            "goal": "了解Qwen-Agent项目的功能和特点"
        },
        {
            "url": "https://serper.dev/",
            "goal": "获取Serper搜索API的使用信息"
        }
    ]

    for i, test in enumerate(url_tests, 1):
        print(f"\n📋 网页访问 {i}: {test['url']}")
        print(f"🎯 目标: {test['goal']}")
        print("-" * 40)

        try:
            start_time = time.time()
            result = tool.call({
                "url": test["url"],
                "goal": test["goal"]
            })
            end_time = time.time()

            print(f"⏱️  用时: {end_time - start_time:.2f}秒")
            print(f"📊 结果长度: {len(result)} 字符")

            # 显示摘要
            if len(result) > 300:
                print(result[:300] + "...\n[结果已截断]")
            else:
                print(result)

        except Exception as e:
            print(f"❌ 网页访问失败: {e}")


def demo_react_agent():
    """演示ReAct Agent功能"""
    print("\n🤖 ReAct Agent智能研究演示")
    print("=" * 60)

    agent = ReActAgent()

    # 研究问题测试
    research_questions = [
        "人工智能在医疗诊断中的应用",
        "量子计算对未来科技的影响",
        "可持续能源技术发展趋势"
    ]

    for i, question in enumerate(research_questions, 1):
        print(f"\n📋 研究问题 {i}: {question}")
        print("-" * 40)

        try:
            start_time = time.time()
            result = agent.research(question)
            end_time = time.time()

            print(f"⏱️  用时: {end_time - start_time:.2f}秒")
            print(f"📊 结果长度: {len(result)} 字符")
            print(f"🧠 LLM调用次数: {getattr(agent, 'llm_calls', 'N/A')}")
            print(f"💬 消息总数: {len(getattr(agent, 'messages', []))}")

            # 显示摘要
            if len(result) > 400:
                print(result[:400] + "...\n[结果已截断]")
            else:
                print(result)

            # 重置代理状态以进行下一次研究
            agent.reset()

        except Exception as e:
            print(f"❌ 研究失败: {e}")


def demo_integration():
    """演示工具集成使用"""
    print("\n🔗 工具集成使用演示")
    print("=" * 60)

    print("演示如何结合多个工具完成复杂任务")
    print("任务: 研究某个技术领域的最新进展")

    topic = input("\n请输入研究主题 (例: 机器学习): ").strip()

    if not topic:
        topic = "机器学习"
        print(f"使用默认主题: {topic}")

    print(f"\n🎯 研究主题: {topic}")
    print("=" * 60)

    # 步骤1: 基础搜索
    print("\n📝 步骤1: 基础网络搜索")
    print("-" * 40)
    search_tool = GoogleSearchTool()

    try:
        basic_info = search_tool.call({"query": f"{topic} 最新发展 2024"})
        print(basic_info[:300] + "...")
    except Exception as e:
        print(f"❌ 基础搜索失败: {e}")
        return

    # 步骤2: 学术研究
    print("\n📚 步骤2: 学术文献搜索")
    print("-" * 40)
    scholar_tool = GoogleScholarTool()

    try:
        academic_info = scholar_tool.call({"query": f"{topic} research papers 2024"})
        print(academic_info[:300] + "...")
    except Exception as e:
        print(f"❌ 学术搜索失败: {e}")

    # 步骤3: 深度研究
    print("\n🔬 步骤3: ReAct Agent深度研究")
    print("-" * 40)
    agent = ReActAgent()

    try:
        research_result = agent.research(f"分析{topic}技术的最新进展、应用前景和未来趋势")
        print(f"🧠 LLM调用: {getattr(agent, 'llm_calls', 'N/A')}次")
        print(research_result[:400] + "...")
    except Exception as e:
        print(f"❌ 深度研究失败: {e}")

    print("\n✅ 集成演示完成!")


def performance_benchmark():
    """性能基准测试"""
    print("\n📊 工具性能基准测试")
    print("=" * 60)

    tools = {
        "Google搜索": GoogleSearchTool(),
        "Google学术": GoogleScholarTool(),
        "Jina访问": JinaURLVisitTool()
    }

    test_cases = {
        "Google搜索": {"query": "Python编程"},
        "Google学术": {"query": "machine learning"},
        "Jina访问": {"url": "https://www.python.org", "goal": "了解Python"}
    }

    results: Dict[str, Dict[str, Any]] = {}

    for tool_name, tool in tools.items():
        print(f"\n🧪 测试 {tool_name}")
        print("-" * 30)

        times = []
        success_count = 0

        for i in range(3):  # 每个工具测试3次
            try:
                start_time = time.time()
                result = tool.call(test_cases[tool_name])
                end_time = time.time()

                times.append(end_time - start_time)
                success_count += 1
                print(f"  测试 {i+1}: {end_time - start_time:.2f}s ✅")

            except Exception as e:
                print(f"  测试 {i+1}: 失败 ❌ ({e})")

        if times:
            avg_time = sum(times) / len(times)
            min_time = min(times)
            max_time = max(times)

            results[tool_name] = {
                "success_rate": success_count / 3 * 100,
                "avg_time": avg_time,
                "min_time": min_time,
                "max_time": max_time
            }

            print(f"  📊 成功率: {success_count}/3 ({success_count/3*100:.1f}%)")
            print(f"  ⏱️  平均用时: {avg_time:.2f}s")
            print(f"  ⚡ 最快: {min_time:.2f}s")
            print(f"  🐌 最慢: {max_time:.2f}s")

    print("\n📈 性能总结:")
    print("-" * 30)
    for tool_name, stats in results.items():
        print(f"{tool_name}: {stats['success_rate']:.0f}%成功率, {stats['avg_time']:.2f}s平均")


def main():
    """主函数"""
    print("🛠️  ResearchAgent 完整工具演示")
    print("=" * 60)

    demos = {
        '1': ("Google搜索", demo_google_search),
        '2': ("Google学术搜索", demo_google_scholar),
        '3': ("Jina网页访问", demo_jina_url_visit),
        '4': ("ReAct Agent", demo_react_agent),
        '5': ("工具集成使用", demo_integration),
        '6': ("性能基准测试", performance_benchmark),
        '7': ("运行所有演示", None)
    }

    print("选择演示类型:")
    for key, (name, _) in demos.items():
        print(f"{key}. {name}")

    choice = input("\n请选择 (1-7): ").strip()

    if choice in demos:
        name, func = demos[choice]

        if choice == '7':
            # 运行所有演示
            for key, (demo_name, demo_func) in demos.items():
                if key != '7' and demo_func:
                    demo_func()
                    input("\n按Enter继续下一个演示...")
        else:
            func()
    else:
        print("❌ 无效选择")

    print("\n🎉 演示完成!")
    print("感谢使用 ResearchAgent! 🚀")


if __name__ == "__main__":
    main()
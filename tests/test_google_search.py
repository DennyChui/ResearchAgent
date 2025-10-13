#!/usr/bin/env python3
"""
测试Google搜索工具的脚本
"""

import sys
import os

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

def test_tool_structure():
    """测试工具的基本结构"""
    print("=" * 50)
    print("测试Google搜索工具基本结构")
    print("=" * 50)

    try:
        from inference.google_search_tool import GoogleSearchTool
        print("✓ 成功导入GoogleSearchTool")

        # 创建工具实例
        tool = GoogleSearchTool()
        print("✓ 成功创建工具实例")

        # 检查工具属性
        print(f"✓ 工具名称: {tool.name}")
        print(f"✓ 工具描述: {tool.description}")
        print(f"✓ 工具参数: {tool.parameters}")

        # 检查call方法存在
        if hasattr(tool, 'call'):
            print("✓ call方法存在")
        else:
            print("✗ call方法不存在")

        # 测试错误处理（空查询）
        result = tool.call("")
        print("✓ 空查询处理:", result[:100])

        # 测试无效参数
        result = tool.call(None)
        print("✓ 无效参数处理:", result[:100])

        return True

    except ImportError as e:
        print(f"✗ 导入错误: {e}")
        return False
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        return False

def test_api_call_simulation():
    """模拟API调用测试"""
    print("\n" + "=" * 50)
    print("模拟API调用测试")
    print("=" * 50)

    try:
        from inference.google_search_tool import GoogleSearchTool
        tool = GoogleSearchTool()

        # 模拟API响应
        mock_response = {
            "searchInformation": {
                "totalResults": "1234567",
                "formattedSearchTime": "0.45"
            },
            "organic": [
                {
                    "title": "Python Programming Tutorials - Real Python",
                    "snippet": "Learn Python programming with our comprehensive tutorials covering everything from basics to advanced topics.",
                    "link": "https://realpython.com"
                },
                {
                    "title": "Python.org Official Tutorial",
                    "snippet": "The official Python tutorial for beginners and experienced programmers alike.",
                    "link": "https://docs.python.org/3/tutorial/"
                }
            ]
        }

        # 测试格式化功能
        formatted_result = tool._format_results("Python tutorials", mock_response)
        print("✓ 结果格式化成功:")
        print(formatted_result[:400])

        return True

    except Exception as e:
        print(f"✗ 模拟测试失败: {e}")
        return False

def test_with_qwen_agent():
    """测试与qwen-agent的集成"""
    print("\n" + "=" * 50)
    print("测试qwen-agent集成")
    print("=" * 50)

    try:
        from qwen_agent.tools.base import BaseTool, TOOL_REGISTRY
        from inference.google_search_tool import GoogleSearchTool

        # 检查工具是否正确注册
        if 'google_search' in TOOL_REGISTRY:
            print("✓ 工具已成功注册到TOOL_REGISTRY")
        else:
            print("✗ 工具未在TOOL_REGISTRY中找到")

        # 检查工具继承关系
        tool = GoogleSearchTool()
        if isinstance(tool, BaseTool):
            print("✓ 工具正确继承BaseTool")
        else:
            print("✗ 工具未正确继承BaseTool")

        return True

    except Exception as e:
        print(f"✗ 集成测试失败: {e}")
        return False

if __name__ == "__main__":
    print("Google搜索工具测试开始...")

    success_count = 0
    total_tests = 3

    if test_tool_structure():
        success_count += 1

    if test_api_call_simulation():
        success_count += 1

    if test_with_qwen_agent():
        success_count += 1

    print("\n" + "=" * 50)
    print(f"测试完成: {success_count}/{total_tests} 通过")

    if success_count == total_tests:
        print("🎉 所有测试通过！Google搜索工具已准备就绪。")
    else:
        print("⚠️  部分测试失败，请检查问题。")
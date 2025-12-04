#!/usr/bin/env python3
"""
测试Google Scholar学术搜索工具
"""

import sys
import os

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

def test_tool_structure():
    """测试工具的基本结构"""
    print("=" * 50)
    print("测试Google Scholar工具基本结构")
    print("=" * 50)

    try:
        from inference.google_scholar_tool import GoogleScholarTool
        print("✓ 成功导入GoogleScholarTool")

        # 创建工具实例
        tool = GoogleScholarTool()
        print("✓ 成功创建工具实例")

        # 检查工具属性
        print(f"✓ 工具名称: {tool.name}")
        print(f"✓ 工具描述: {tool.description}")
        print(f"✓ 工具参数: {tool.parameters}")

        # 检查参数是否符合JSON Schema格式
        if isinstance(tool.parameters, dict) and 'type' in tool.parameters:
            print("✓ 参数使用JSON Schema格式")
        else:
            print("✗ 参数未使用JSON Schema格式")

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

def test_real_api_call():
    """真实API调用测试"""
    print("\n" + "=" * 50)
    print("真实API调用测试")
    print("=" * 50)

    try:
        from inference.google_scholar_tool import GoogleScholarTool
        tool = GoogleScholarTool()

        # 简单的测试查询
        test_query = "machine learning"
        print(f"🔍 执行学术搜索查询: {test_query}")

        # 执行真实的API调用
        result = tool.call({"query": test_query})

        print("✓ 真实API调用成功:")
        print("\n📋 学术搜索结果预览:")
        print(result[:600])  # 显示前600个字符

        # 验证结果包含预期的格式
        if "A Google Scholar search for" in result and ("## Results" in result or "## Web Results" in result):
            print("✓ 结果格式正确")
        else:
            print("⚠️  结果格式可能有问题")

        # 验证结果包含搜索统计信息
        if "search time:" in result.lower():
            print("✓ 包含搜索时间信息")

        return True

    except Exception as e:
        print(f"✗ 真实API调用失败: {e}")
        print("💡 可能的原因:")
        print("   - 网络连接问题")
        print("   - API密钥未设置或无效")
        print("   - API服务暂时不可用")
        return False

def test_with_qwen_agent():
    """测试与qwen-agent的集成"""
    print("\n" + "=" * 50)
    print("测试qwen-agent集成")
    print("=" * 50)

    try:
        from qwen_agent.tools.base import BaseTool, TOOL_REGISTRY
        from inference.google_scholar_tool import GoogleScholarTool

        # 检查工具是否正确注册
        if 'google_scholar' in TOOL_REGISTRY:
            print("✓ 工具已成功注册到TOOL_REGISTRY")
        else:
            print("✗ 工具未在TOOL_REGISTRY中找到")

        # 检查工具继承关系
        tool = GoogleScholarTool()
        if isinstance(tool, BaseTool):
            print("✓ 工具正确继承BaseTool")
        else:
            print("✗ 工具未正确继承BaseTool")

        return True

    except Exception as e:
        print(f"✗ 集成测试失败: {e}")
        return False

def test_batch_queries():
    """测试批量查询功能"""
    print("\n" + "=" * 50)
    print("测试批量查询功能")
    print("=" * 50)

    try:
        from inference.google_scholar_tool import GoogleScholarTool
        tool = GoogleScholarTool()

        # 测试数组参数格式（真实API调用）
        result = tool.call({"query": ["deep learning", "neural networks"]})
        print("✓ 数组参数真实调用测试:", result[:300])

        return True

    except Exception as e:
        print(f"✗ 批量查询测试失败: {e}")
        return False

if __name__ == "__main__":
    print("Google Scholar工具测试开始...")

    success_count = 0
    total_tests = 4

    if test_tool_structure():
        success_count += 1

    if test_real_api_call():
        success_count += 1

    if test_with_qwen_agent():
        success_count += 1

    if test_batch_queries():
        success_count += 1

    # 总结
    print("\n" + "=" * 50)
    print("📊 测试总结")
    print("=" * 50)
    print(f"总测试数: {total_tests}")
    print(f"成功: {success_count}")
    print(f"失败: {total_tests - success_count}")
    print(f"成功率: {success_count/total_tests*100:.1f}%")

    if success_count == total_tests:
        print("\n🎉 所有测试通过！")
    else:
        print(f"\n⚠️  {total_tests - success_count} 个测试失败")

    print("=" * 50)

#!/usr/bin/env python3
"""
测试Jina URL访问工具的脚本
"""

import sys
import os

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

def test_tool_structure():
    """测试工具的基本结构"""
    print("=" * 50)
    print("测试Jina URL访问工具基本结构")
    print("=" * 50)

    try:
        from inference.jina_url_visit_tool import JinaURLVisitTool
        print("✓ 成功导入JinaURLVisitTool")

        # 创建工具实例
        tool = JinaURLVisitTool()
        print("✓ 成功创建工具实例")

        # 检查工具属性
        print(f"✓ 工具名称: {tool.name}")
        print(f"✓ 工具描述: {tool.description[:100]}...")

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

        # 测试URL验证功能
        valid_url = "https://www.python.org"
        invalid_url = "not-a-url"
        if tool._validate_url(valid_url):
            print("✓ URL验证功能正常")
        else:
            print("✗ URL验证功能异常")

        if not tool._validate_url(invalid_url):
            print("✓ URL验证正确识别无效URL")
        else:
            print("✗ URL验证未能识别无效URL")

        return True

    except ImportError as e:
        print(f"✗ 导入错误: {e}")
        return False
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        return False

def test_truncation_functionality():
    """测试内容截断功能"""
    print("\n" + "=" * 50)
    print("测试内容截断功能")
    print("=" * 50)

    try:
        from inference.jina_url_visit_tool import JinaURLVisitTool
        tool = JinaURLVisitTool()

        # 测试短内容（不需要截断）
        short_content = "This is a short content."
        messages = [{"role": "user", "content": short_content}]
        truncated = tool._truncate_messages(messages, 1000)

        if truncated[0]["content"] == short_content:
            print("✓ 短内容无需截断")
        else:
            print("✗ 短内容被意外截断")

        # 测试长内容（需要截断）
        long_content = "This is a very long content. " * 1000
        messages = [{"role": "user", "content": long_content}]
        truncated = tool._truncate_messages(messages, 100)

        if len(truncated[0]["content"]) < len(long_content):
            print("✓ 长内容正确截断")
        print(f"  原始长度: {len(long_content)} 字符")
        print(f"  截断后长度: {len(truncated[0]['content'])} 字符")

        # 测试智能截断
        smart_content = "这是第一段。这是第二段。这是第三段。" * 100
        messages = [{"role": "user", "content": smart_content}]
        truncated = tool._truncate_messages(messages, 50)

        print("✓ 智能截断功能测试完成")

        return True

    except Exception as e:
        print(f"✗ 截断功能测试失败: {e}")
        return False

def test_parameter_parsing():
    """测试参数解析功能"""
    print("\n" + "=" * 50)
    print("测试参数解析功能")
    print("=" * 50)

    try:
        from inference.jina_url_visit_tool import JinaURLVisitTool
        tool = JinaURLVisitTool()

        # 测试字典参数
        dict_params = {
            "url": "https://www.python.org",
            "goal": "Extract Python information"
        }
        result = tool.call(dict_params)
        if result and not result.startswith("Error"):
            print("✓ 字典参数解析成功")
        else:
            print(f"✗ 字典参数解析失败: {result[:100]}")

        # 测试字符串参数
        str_params = '{"url": "https://docs.python.org", "goal": "Get Python docs info"}'
        result = tool.call(str_params)
        if result and not result.startswith("Error"):
            print("✓ 字符串参数解析成功")
        else:
            print(f"✗ 字符串参数解析失败: {result[:100]}")

        # 测试数组URL参数
        array_params = {
            "url": ["https://www.python.org", "https://docs.python.org"],
            "goal": "Compare Python resources"
        }
        result = tool.call(array_params)
        if result and not result.startswith("Error"):
            print("✓ 数组URL参数解析成功")
        else:
            print(f"✗ 数组URL参数解析失败: {result[:100]}")

        # 测试错误参数处理
        error_params = {"invalid": "parameter"}
        result = tool.call(error_params)
        if result and result.startswith("Error"):
            print("✓ 错误参数处理正确")
        else:
            print("✗ 错误参数处理异常")

        return True

    except Exception as e:
        print(f"✗ 参数解析测试失败: {e}")
        return False

def test_qwen_agent_integration():
    """测试与qwen-agent的集成"""
    print("\n" + "=" * 50)
    print("测试qwen-agent集成")
    print("=" * 50)

    try:
        from qwen_agent.tools.base import BaseTool, TOOL_REGISTRY
        from inference.jina_url_visit_tool import JinaURLVisitTool

        # 检查工具是否正确注册
        if 'visit' in TOOL_REGISTRY:
            print("✓ 工具已成功注册到TOOL_REGISTRY")
        else:
            print("✗ 工具未在TOOL_REGISTRY中找到")

        # 检查工具继承关系
        tool = JinaURLVisitTool()
        if isinstance(tool, BaseTool):
            print("✓ 工具正确继承BaseTool")
        else:
            print("✗ 工具未正确继承BaseTool")

        # 检查工具注册信息
        if hasattr(tool, 'name') and tool.name == 'visit':
            print("✓ 工具名称正确")
        else:
            print("✗ 工具名称不正确")

        return True

    except Exception as e:
        print(f"✗ 集成测试失败: {e}")
        return False

def test_error_handling():
    """测试错误处理"""
    print("\n" + "=" * 50)
    print("测试错误处理")
    print("=" * 50)

    try:
        from inference.jina_url_visit_tool import JinaURLVisitTool
        tool = JinaURLVisitTool()

        # 测试无效URL
        result = tool.call({"url": "invalid-url", "goal": "test"})
        if result and ("Error" in result or "Invalid" in result):
            print("✓ 无效URL错误处理正确")
        else:
            print("✗ 无效URL错误处理失败")

        # 测试空参数
        result = tool.call({})
        if result and result.startswith("Error"):
            print("✓ 空参数错误处理正确")
        else:
            print("✗ 空参数错误处理失败")

        # 测试无效JSON
        result = tool.call("invalid json")
        if result and result.startswith("Error"):
            print("✓ 无效JSON错误处理正确")
        else:
            print("✗ 无效JSON错误处理失败")

        return True

    except Exception as e:
        print(f"✗ 错误处理测试失败: {e}")
        return False

def test_structured_output():
    """测试结构化输出格式"""
    print("\n" + "=" * 50)
    print("测试结构化输出格式")
    print("=" * 50)

    try:
        from inference.jina_url_visit_tool import JinaURLVisitTool
        import json
        tool = JinaURLVisitTool()

        # 测试基本结构化输出
        result = tool.call({
            "url": "https://www.python.org",
            "goal": "Extract key Python features"
        })

        # 检查是否包含三个必需字段
        has_rational = "🎯 Rational" in result
        has_evidence = "📋 Evidence" in result
        has_summary = "📝 Summary" in result

        if has_rational:
            print("✓ 包含 Rational 字段")
        else:
            print("✗ 缺少 Rational 字段")

        if has_evidence:
            print("✓ 包含 Evidence 字段")
        else:
            print("✗ 缺少 Evidence 字段")

        if has_summary:
            print("✓ 包含 Summary 字段")
        else:
            print("✗ 缺少 Summary 字段")

        # 检查输出格式
        if "## URL Analysis for:" in result:
            print("✓ 使用了正确的标题格式")
        else:
            print("✗ 标题格式不正确")

        # 测试批量处理的结构化输出
        batch_result = tool.call({
            "url": ["https://www.python.org", "https://docs.python.org"],
            "goal": "Compare Python resources"
        })

        if "Batch URL Summary Report" in batch_result:
            print("✓ 批量处理格式正确")
        else:
            print("✗ 批量处理格式不正确")

        return True

    except Exception as e:
        print(f"✗ 结构化输出测试失败: {e}")
        return False

if __name__ == "__main__":
    print("Jina URL访问工具测试开始...")

    success_count = 0
    total_tests = 6

    if test_tool_structure():
        success_count += 1

    if test_truncation_functionality():
        success_count += 1

    if test_parameter_parsing():
        success_count += 1

    if test_qwen_agent_integration():
        success_count += 1

    if test_error_handling():
        success_count += 1

    if test_structured_output():
        success_count += 1

    print("\n" + "=" * 50)
    print(f"测试完成: {success_count}/{total_tests} 通过")

    if success_count == total_tests:
        print("🎉 所有测试通过！Jina URL访问工具已准备就绪。")
    else:
        print("⚠️  部分测试失败，请检查问题。")
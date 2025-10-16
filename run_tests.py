#!/usr/bin/env python3
"""
ResearchAgent 统一测试脚本

这个脚本整合了所有测试功能，包括：
1. 工具基础功能测试
2. ReAct Agent集成测试
3. 演示和验证功能
4. 性能和兼容性测试

使用方法:
    python run_tests.py [test_type]
    
test_type 可选:
    - all: 运行所有测试 (默认)
    - tools: 仅测试工具基础功能
    - agent: 仅测试ReAct Agent
    - demo: 仅运行演示
    - quick: 快速检查核心功能
"""

import sys
import os
import json
import time
import traceback
from typing import Dict, List, Any, Tuple, Optional
from datetime import datetime

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# 测试结果类
class TestResult:
    def __init__(self, name: str, passed: bool, message: str = "", duration: float = 0.0):
        self.name = name
        self.passed = passed
        self.message = message
        self.duration = duration
        self.timestamp = datetime.now()

# 测试套件类
class TestSuite:
    def __init__(self):
        self.results: List[TestResult] = []
        self.total_start_time = time.time()
    
    def add_result(self, result: TestResult):
        self.results.append(result)
        status = "✅" if result.passed else "❌"
        print(f"{status} {result.name} ({result.duration:.2f}s)")
        if result.message:
            print(f"    {result.message}")
    
    def run_test(self, name: str, test_func):
        """运行单个测试并记录结果"""
        print(f"\n🧪 {name}")
        start_time = time.time()
        
        try:
            result_data = test_func()
            if isinstance(result_data, tuple):
                passed, message = result_data
            else:
                passed, message = result_data, ""
            
            duration = time.time() - start_time
            self.add_result(TestResult(name, passed, message, duration))
            
        except Exception as e:
            duration = time.time() - start_time
            error_msg = f"Exception: {str(e)}"
            print(f"❌ {name} ({duration:.2f}s) - {error_msg}")
            self.add_result(TestResult(name, False, error_msg, duration))
    
    def print_summary(self):
        """打印测试总结"""
        total_time = time.time() - self.total_start_time
        passed = sum(1 for r in self.results if r.passed)
        total = len(self.results)
        
        print("\n" + "=" * 70)
        print("测试总结")
        print("=" * 70)
        print(f"总测试数: {total}")
        print(f"通过: {passed}")
        print(f"失败: {total - passed}")
        print(f"成功率: {passed/total*100:.1f}%")
        print(f"总耗时: {total_time:.2f}s")
        
        if total - passed > 0:
            print("\n失败的测试:")
            for result in self.results:
                if not result.passed:
                    print(f"  ❌ {result.name}: {result.message}")

# 全局测试套件
test_suite = TestSuite()

def check_environment():
    """检查环境配置"""
    issues = []
    
    # 检查Python版本
    if sys.version_info < (3, 8):
        issues.append("Python版本需要 >= 3.8")
    
    # 检查环境变量
    required_env_vars = ['GLM_API_KEY', 'SERPER_KEY_ID', 'JINA_API_KEY']
    for var in required_env_vars:
        if not os.getenv(var):
            issues.append(f"环境变量 {var} 未设置")
    
    # 检查项目依赖
    try:
        import qwen_agent
        from qwen_agent.tools.base import BaseTool
    except ImportError:
        issues.append("qwen-agent 包未正确安装")
    
    try:
        import sandbox_fusion
    except ImportError:
        issues.append("sandbox-fusion 包未正确安装")
    
    return len(issues) == 0, issues if issues else "环境检查通过"

def test_python_sandbox_tool():
    """测试Python sandbox工具基础功能"""
    from inference.python_sandbox_tool import PythonSandboxTool
    
    # 创建工具实例
    tool = PythonSandboxTool()
    
    # 检查工具属性
    assert hasattr(tool, 'name'), "工具缺少name属性"
    assert hasattr(tool, 'description'), "工具缺少description属性"
    assert hasattr(tool, 'parameters'), "工具缺少parameters属性"
    assert hasattr(tool, 'call'), "工具缺少call方法"
    
    # 检查参数schema
    params = tool.parameters
    assert isinstance(params, dict), "参数应该是字典类型"
    assert 'properties' in params, "参数schema缺少properties"
    assert 'code' in params['properties'], "缺少code参数定义"
    
    # 测试简单代码执行
    result = tool.call({"code": "print('Hello, World!')"})
    assert "Hello, World!" in result, "简单代码执行失败"
    
    # 测试数学计算
    result = tool.call({"code": "print(2 + 3)"})
    assert "5" in result, "数学计算失败"
    
    # 测试错误处理
    result = tool.call({"code": "print(undefined_variable)"})
    assert "NameError" in result or "undefined" in result.lower(), "错误处理失败"
    
    return True, "Python sandbox工具所有基础功能正常"

def test_react_agent_tools():
    """测试ReAct Agent工具集成"""
    from inference.react_agent import ReActAgent
    
    # 创建agent实例
    agent = ReActAgent()
    
    # 检查工具是否正确加载
    expected_tools = ['search', 'google_scholar', 'visit', 'python_sandbox']
    available_tools = list(agent.tools.keys())
    
    for tool in expected_tools:
        if tool not in available_tools:
            return False, f"缺少工具: {tool}"
    
    # 测试工具调用检测
    test_cases = [
        ('{"name": "python_sandbox", "arguments": {"code": "print(1+1)"}}', 'python_sandbox'),
        ('{"name": "search", "arguments": {"query": "test"}}', 'search'),
        ('{"name": "visit", "arguments": {"url": "http://example.com"}}', 'visit'),
    ]
    
    for test_call, expected_tool in test_cases:
        detected = agent._detect_tool_calls(test_call)
        if not detected:
            return False, f"工具调用检测失败: {expected_tool}"
        
        if detected[0]['name'] != expected_tool:
            return False, f"工具名称检测错误: 期望 {expected_tool}, 得到 {detected[0]['name']}"
    
    # 测试Python sandbox工具执行
    result = agent._execute_tool('python_sandbox', {'code': 'print("Agent test")'})
    assert "Agent test" in result, "Agent中Python sandbox工具执行失败"
    
    return True, "ReAct Agent工具集成正常"

def test_system_prompt_integration():
    """测试系统提示集成"""
    from inference.react_agent import ReActAgent
    
    agent = ReActAgent()
    system_prompt = agent._create_system_prompt()
    
    # 检查关键内容
    required_content = [
        'python_sandbox',
        'print()',
        'mathematical',
        'import math',
    ]
    
    for content in required_content:
        if content not in system_prompt:
            return False, f"系统提示缺少关键内容: {content}"
    
    # 检查工具签名
    if 'python_sandbox' not in agent._get_tools_signatures():
        return False, "工具签名中缺少python_sandbox"
    
    return True, "系统提示集成正常"

def test_mathematical_research():
    """测试数学研究能力"""
    from inference import PythonSandboxTool
    
    tool = PythonSandboxTool()
    
    # 测试黄金分割比例计算
    golden_ratio_code = '''
import math

# 黄金分割比例
phi = (1 + math.sqrt(5)) / 2
print(f"黄金分割比例 φ = {phi:.10f}")

# 验证性质: φ² = φ + 1
phi_squared = phi ** 2
phi_plus_1 = phi + 1
difference = abs(phi_squared - phi_plus_1)
print(f"φ² - (φ + 1) = {difference:.2e}")
print(f"验证通过: {difference < 1e-10}")
'''
    
    result = tool.call({"code": golden_ratio_code})
    
    # 检查计算结果
    checks = [
        ("1.618" in result, "黄金分割比例计算"),
        ("0.00e" in result or "验证通过" in result, "黄金分割比例性质验证"),
    ]
    
    for check, description in checks:
        if not check:
            return False, f"数学计算测试失败: {description}"
    
    return True, "数学研究能力测试通过"

def test_data_analysis():
    """测试数据分析能力"""
    from inference import PythonSandboxTool
    
    tool = PythonSandboxTool()
    
    # 模拟数据分析
    data_analysis_code = '''
# 模拟销售数据分析
import math

data = [100, 120, 115, 130, 125, 140, 135, 150, 145, 160]
n = len(data)

mean = sum(data) / n
print(f"平均值: {mean:.1f}")

variance = sum((x - mean) ** 2 for x in data) / n
std_dev = math.sqrt(variance)
print(f"标准差: {std_dev:.1f}")

# 简单趋势分析
growth = (data[-1] - data[0]) / data[0] * 100
print(f"增长率: {growth:.1f}%")
'''
    
    result = tool.call({"code": data_analysis_code})
    
    # 检查分析结果
    required_elements = ["平均值", "标准差", "增长率"]
    for element in required_elements:
        if element not in result:
            return False, f"数据分析缺少元素: {element}"
    
    return True, "数据分析能力测试通过"

def test_scientific_computation():
    """测试科学计算能力"""
    from inference import PythonSandboxTool
    
    tool = PythonSandboxTool()
    
    # 抛体运动计算
    physics_code = '''
import math

g = 9.8  # 重力加速度
v0 = 20   # 初速度
angle = 45  # 发射角度

angle_rad = math.radians(angle)

# 计算飞行时间
t_flight = 2 * v0 * math.sin(angle_rad) / g

# 计算最大高度
h_max = (v0 * math.sin(angle_rad)) ** 2 / (2 * g)

# 计算射程
range_x = v0 ** 2 * math.sin(2 * angle_rad) / g

print(f"飞行时间: {t_flight:.2f}s")
print(f"最大高度: {h_max:.2f}m")
print(f"射程: {range_x:.2f}m")
'''
    
    result = tool.call({"code": physics_code})
    
    # 检查计算结果
    numeric_values = []
    import re
    numbers = re.findall(r'\d+\.\d+', result)
    
    if len(numbers) < 3:
        return False, "科学计算结果不完整"
    
    return True, "科学计算能力测试通过"

def test_edge_cases():
    """测试边界情况和错误处理"""
    from inference import PythonSandboxTool
    
    tool = PythonSandboxTool()
    
    test_cases = [
        # 空代码
        ({"code": ""}, "空代码处理"),
        
        # 长代码
        ({"code": "x = " + "+ ".join(["1"] * 50)}, "长代码处理"),
        
        # Unicode字符
        ({"code": "print('Hello 世界 🌍')"}, "Unicode字符处理"),
        
        # 多行代码
        ({"code": '''
def func():
    return "test"
print(func())
'''.strip()}, "多行代码处理"),
    ]
    
    for args, description in test_cases:
        try:
            result = tool.call(args)
            
            # 空代码应该返回错误
            if description == "空代码处理":
                if "Error:" not in result or "cannot be empty" not in result:
                    return False, f"{description} 应该返回错误但没有"
            # 其他情况不应该有错误
            else:
                if "Error:" in result:
                    return False, f"{description} 导致意外错误: {result[:100]}"
                    
        except Exception as e:
            return False, f"{description} 导致异常: {str(e)}"
    
    return True, "边界情况测试通过"

def run_unit_tests():
    """运行单元测试"""
    print("🧪 运行单元测试...")
    
    tests = [
        ("环境检查", check_environment),
        ("Python Sandbox工具基础功能", test_python_sandbox_tool),
        ("ReAct Agent工具集成", test_react_agent_tools),
        ("系统提示集成", test_system_prompt_integration),
        ("边界情况和错误处理", test_edge_cases),
    ]
    
    for test_name, test_func in tests:
        test_suite.run_test(test_name, test_func)

def run_integration_tests():
    """运行集成测试"""
    print("🧪 运行集成测试...")
    
    tests = [
        ("数学研究能力", test_mathematical_research),
        ("数据分析能力", test_data_analysis),
        ("科学计算能力", test_scientific_computation),
    ]
    
    for test_name, test_func in tests:
        test_suite.run_test(test_name, test_func)

def run_demo():
    """运行演示"""
    print("🚀 运行演示...")
    
    demo_code = '''
# ResearchAgent Python Sandbox 演示
import math
import random

print("🎯 ResearchAgent Python Sandbox 演示")
print("=" * 50)

# 1. 数学计算演示
print("\\n1. 数学计算演示:")
print(f"圆周率 π = {math.pi:.6f}")
print(f"自然常数 e = {math.e:.6f}")
print(f"黄金比例 φ = {(1 + math.sqrt(5))/2:.6f}")

# 2. 数据分析演示
print("\\n2. 数据分析演示:")
data = [random.randint(1, 100) for _ in range(10)]
print(f"随机数据: {data}")
print(f"平均值: {sum(data)/len(data):.1f}")
print(f"最大值: {max(data)}")
print(f"最小值: {min(data)}")

# 3. 算法演示
print("\\n3. 算法演示:")
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

fib_10 = fibonacci(10)
print(f"斐波那契数列第10项: {fib_10}")

# 4. 字符串处理演示
print("\\n4. 字符串处理演示:")
text = "ResearchAgent Python Sandbox Demo"
print(f"原文: {text}")
print(f"长度: {len(text)}")
print(f"反转: {text[::-1]}")
print(f"单词数: {len(text.split())}")

print("\\n✅ 演示完成！Python Sandbox 工具运行正常。")
'''
    
    try:
        from inference import PythonSandboxTool
        tool = PythonSandboxTool()
        result = tool.call({"code": demo_code})
        
        print(result)
        
        if "演示完成" in result:
            return True, "演示运行成功"
        else:
            return False, "演示未正常完成"
            
    except Exception as e:
        return False, f"演示运行失败: {str(e)}"

def run_quick_check():
    """快速检查核心功能"""
    print("⚡ 快速检查核心功能...")
    
    try:
        # 检查基础导入
        from inference import PythonSandboxTool, ReActAgent
        print("✅ 基础导入正常")
        
        # 检查工具创建
        tool = PythonSandboxTool()
        agent = ReActAgent()
        print("✅ 工具创建正常")
        
        # 检查简单执行
        result = tool.call({"code": "print('Quick check passed')"})
        if "Quick check passed" in result:
            print("✅ Python代码执行正常")
        else:
            return False, "Python代码执行异常"
        
        # 检查工具集成
        if 'python_sandbox' in agent.tools:
            print("✅ ReAct Agent集成正常")
        else:
            return False, "ReAct Agent集成异常"
        
        return True, "所有核心功能正常"
        
    except Exception as e:
        return False, f"快速检查失败: {str(e)}"

def main():
    """主函数"""
    # 解析命令行参数
    test_type = sys.argv[1] if len(sys.argv) > 1 else 'all'
    
    print("🧪 ResearchAgent 统一测试脚本")
    print(f"测试类型: {test_type}")
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    # 根据测试类型运行相应的测试
    if test_type == 'all':
        run_unit_tests()
        run_integration_tests()
        run_demo()
    elif test_type == 'tools':
        run_unit_tests()
    elif test_type == 'agent':
        run_integration_tests()
    elif test_type == 'demo':
        test_suite.run_test("演示功能", run_demo)
    elif test_type == 'quick':
        test_suite.run_test("快速检查", run_quick_check)
    else:
        print(f"❌ 未知的测试类型: {test_type}")
        print("可用类型: all, tools, agent, demo, quick")
        sys.exit(1)
    
    # 打印测试总结
    test_suite.print_summary()
    
    # 根据测试结果设置退出码
    failed_count = sum(1 for r in test_suite.results if not r.passed)
    sys.exit(0 if failed_count == 0 else 1)

if __name__ == "__main__":
    main()

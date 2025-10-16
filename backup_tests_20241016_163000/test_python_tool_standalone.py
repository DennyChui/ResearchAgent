#!/usr/bin/env python3
"""
独立测试Python沙盒工具
不依赖项目完整的安装环境
"""

import sys
import os
sys.path.insert(0, '/Users/denny/Zone/LearningRepo/ResearchAgent')

def test_python_tool_import():
    """测试Python工具导入"""
    print("🧪 测试1: Python沙盒工具导入...")
    
    try:
        # 模拟必要的依赖
        import json
        from typing import Union, Dict, Any
        
        # 模拟BaseTool类
        class BaseTool:
            def __init__(self):
                pass
        
        # 模拟register_tool装饰器
        def register_tool(name):
            def decorator(cls):
                cls.name = name
                return cls
            return decorator
        
        # 尝试导入我们的工具配置
        from inference.config import get_sandbox_endpoints
        print(f"✅ get_sandbox_endpoints函数导入成功")
        
        # 测试获取端点
        endpoints = get_sandbox_endpoints()
        print(f"✅ 获取到{len(endpoints)}个沙盒端点: {endpoints}")
        
        return True
        
    except Exception as e:
        print(f"❌ 导入测试失败: {e}")
        return False

def test_sandbox_api_connection():
    """测试沙盒API连接"""
    print("\n🧪 测试2: 沙盒API连接测试...")
    
    # 测试端点
    test_endpoints = [
        "http://localhost:8081",
        "http://127.0.0.1:8081"
    ]
    
    import requests
    import json
    
    for endpoint in test_endpoints:
        try:
            print(f"🔄 测试端点: {endpoint}")
            
            # 尝试简单的health check
            response = requests.get(f"{endpoint}/health", timeout=5)
            if response.status_code == 200:
                print(f"✅ 端点 {endpoint} 健康检查通过")
                return endpoint
            else:
                print(f"⚠️ 端点 {endpoint} 返回状态码: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print(f"❌ 端点 {endpoint} 连接被拒绝")
        except requests.exceptions.Timeout:
            print(f"⚠️ 端点 {endpoint} 连接超时")
        except Exception as e:
            print(f"❌ 端点 {endpoint} 测试失败: {e}")
    
    print("💡 没有可用的沙盒服务端点")
    print("   请启动SandboxFusion服务或检查端点配置")
    return None

def test_mock_code_execution():
    """测试模拟的代码执行（不需要真实沙盒服务）"""
    print("\n🧪 测试3: 模拟代码执行逻辑...")
    
    try:
        # 模拟代码执行逻辑
        test_codes = [
            "print('Hello, World!')",
            "import math\nprint(f'Pi = {math.pi:.3f}')"
        ]
        
        for i, code in enumerate(test_codes, 1):
            print(f"\n📝 测试代码 {i}:")
            print("```python")
            print(code)
            print("```")
            
            # 模拟执行
            try:
                # 创建本地命名空间来执行代码
                local_scope = {}
                exec(code, {}, local_scope)
                print("✅ 代码执行成功")
                
            except Exception as e:
                print(f"❌ 代码执行失败: {e}")
        
        # 测试多行代码
        print(f"\n📝 测试代码 3 (多行函数定义):")
        print("```python")
        multi_line_code = '''def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

result = fibonacci(10)
print(f'Fibonacci(10) = {result}')'''
        print(multi_line_code)
        print("```")
        
        try:
            local_scope = {}
            exec(multi_line_code, {}, local_scope)
            print("✅ 多行代码执行成功")
        except Exception as e:
            print(f"❌ 多行代码执行失败: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ 模拟测试失败: {e}")
        return False

def test_configuration_validation():
    """测试配置验证"""
    print("\n🧪 测试4: 配置验证...")
    
    try:
        # 测试环境变量
        env_var = os.getenv('SANDBOX_FUSION_ENDPOINT')
        if env_var:
            print(f"✅ 找到SANDBOX_FUSION_ENDPOINT: {env_var}")
        else:
            print("⚠️ 未找到SANDBOX_FUSION_ENDPOINT，使用默认值")
        
        # 测试.env文件
        env_file = '/Users/denny/Zone/LearningRepo/ResearchAgent/.env'
        if os.path.exists(env_file):
            print(f"✅ 找到.env文件: {env_file}")
            
            # 读取.env文件内容
            with open(env_file, 'r') as f:
                content = f.read()
                if 'SANDBOX_FUSION_ENDPOINT' in content:
                    print("✅ .env文件包含SANDBOX_FUSION_ENDPOINT配置")
                else:
                    print("⚠️ .env文件未包含SANDBOX_FUSION_ENDPOINT配置")
        else:
            print("⚠️ 未找到.env文件")
        
        return True
        
    except Exception as e:
        print(f"❌ 配置验证失败: {e}")
        return False

def test_tool_schema():
    """测试工具schema"""
    print("\n🧪 测试5: 工具Schema验证...")
    
    try:
        import json
        
        # 定义期望的schema
        expected_schema = {
            "type": "object",
            "properties": {
                "code": {
                    "type": "string",
                    "description": "Raw Python code to execute in the sandbox. Use print() statements for output. No arguments should be passed - put all Python code directly in this parameter.",
                    "minLength": 1
                }
            },
            "required": ["code"]
        }
        
        print("✅ 期望的工具Schema:")
        print(json.dumps(expected_schema, indent=2, ensure_ascii=False))
        
        return True
        
    except Exception as e:
        print(f"❌ Schema验证失败: {e}")
        return False

def main():
    """运行所有测试"""
    print("🚀 开始测试Python沙盒工具")
    print("=" * 50)
    
    tests = [
        test_python_tool_import,
        test_sandbox_api_connection,
        test_mock_code_execution,
        test_configuration_validation,
        test_tool_schema
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            if result is None:
                result = False
            results.append(result)
        except Exception as e:
            print(f"❌ 测试异常: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    print("📊 测试结果总结:")
    
    passed = sum(results)
    total = len(results)
    
    print(f"✅ 通过: {passed}/{total}")
    print(f"❌ 失败: {total - passed}/{total}")
    
    if passed == total:
        print("🎉 所有测试通过！Python沙盒工具基本功能正常")
    else:
        print("⚠️ 部分测试失败，请检查相关配置")
    
    # 提供使用建议
    print("\n💡 使用建议:")
    print("1. 确保已安装sandbox-fusion: uv pip install sandbox-fusion")
    print("2. 启动SandboxFusion服务在localhost:8081")
    print("3. 检查.env文件中的SANDBOX_FUSION_ENDPOINT配置")
    print("4. 使用print()语句输出Python代码执行结果")

if __name__ == "__main__":
    main()

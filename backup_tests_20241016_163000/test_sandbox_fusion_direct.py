#!/usr/bin/env python3
"""
直接测试SandboxFusion API
"""

import sys
import os

def test_sandbox_fusion_direct():
    """直接测试SandboxFusion SDK"""
    print("🧪 直接测试SandboxFusion API...")
    
    try:
        from sandbox_fusion import run_code, RunCodeRequest, set_sandbox_endpoint
        print("✅ sandbox-fusion 导入成功")
        
        # 设置端点
        endpoint = "http://localhost:8081"
        set_sandbox_endpoint(endpoint)
        print(f"✅ 设置端点: {endpoint}")
        
        # 测试简单的代码执行
        print("\n📝 测试1: 简单打印")
        request = RunCodeRequest(code='print("Hello from SandboxFusion!")', language='python')
        
        try:
            result = run_code(request, max_attempts=1, client_timeout=10)
            print(f"✅ 执行成功: {result.success}")
            if result.stdout:
                print(f"📤 输出: {result.stdout.strip()}")
            if result.stderr:
                print(f"⚠️ 错误: {result.stderr.strip()}")
        except Exception as e:
            print(f"❌ 执行失败: {e}")
            return False
        
        # 测试数学计算
        print("\n📝 测试2: 数学计算")
        request = RunCodeRequest(code='''
import math
result = math.pi * 2
print(f"2π = {result:.4f}")
''', language='python')
        
        try:
            result = run_code(request, max_attempts=1, client_timeout=10)
            print(f"✅ 执行成功: {result.success}")
            if result.stdout:
                print(f"📤 输出: {result.stdout.strip()}")
        except Exception as e:
            print(f"❌ 执行失败: {e}")
        
        # 测试错误处理
        print("\n📝 测试3: 错误处理")
        request = RunCodeRequest(code='print(undefined_variable)', language='python')
        
        try:
            result = run_code(request, max_attempts=1, client_timeout=10)
            print(f"✅ 执行成功: {result.success}")
            if result.stderr:
                print(f"⚠️ 预期错误: {result.stderr.strip()}")
        except Exception as e:
            print(f"❌ 执行失败: {e}")
        
        return True
        
    except ImportError as e:
        print(f"❌ sandbox-fusion 导入失败: {e}")
        print("💡 请运行: uv pip install sandbox-fusion")
        return False
    except Exception as e:
        print(f"❌ 其他错误: {e}")
        return False

def test_environment_config():
    """测试环境配置"""
    print("\n🧪 测试环境配置...")
    
    # 检查环境变量
    endpoint = os.getenv('SANDBOX_FUSION_ENDPOINT')
    if endpoint:
        print(f"✅ SANDBOX_FUSION_ENDPOINT: {endpoint}")
    else:
        print("⚠️ 未设置 SANDBOX_FUSION_ENDPOINT，使用默认值")
    
    # 测试端点连通性
    import requests
    
    test_endpoints = [
        endpoint or "http://localhost:8081",
        "http://127.0.0.1:8081"
    ]
    
    for test_endpoint in test_endpoints:
        try:
            print(f"\n🔄 测试端点连通性: {test_endpoint}")
            response = requests.get(f"{test_endpoint}/", timeout=5)
            print(f"✅ 端点响应: {response.status_code}")
        except requests.exceptions.ConnectionError:
            print(f"❌ 端点连接被拒绝")
        except requests.exceptions.Timeout:
            print(f"⚠️ 端点连接超时")
        except Exception as e:
            print(f"❌ 端点测试失败: {e}")

def main():
    """主测试函数"""
    print("🚀 Python沙盒工具直接测试")
    print("=" * 50)
    
    # 测试环境配置
    test_environment_config()
    
    # 测试SandboxFusion
    success = test_sandbox_fusion_direct()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 SandboxFusion API测试成功！")
        print("💡 Python沙盒工具已准备就绪")
    else:
        print("⚠️ SandboxFusion API测试失败")
        print("💡 请检查:")
        print("   1. sandbox-fusion是否已安装: uv pip install sandbox-fusion")
        print("   2. Sandbox服务是否运行在localhost:8081")
        print("   3. 网络连接是否正常")

if __name__ == "__main__":
    main()

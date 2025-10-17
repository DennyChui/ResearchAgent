#!/usr/bin/env python3
"""
测试配置文件

提供统一的测试配置管理，支持不同的测试环境和API可用性检测。
"""

import os
import sys
from typing import Dict, Any, Optional

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)


class TestConfig:
    """测试配置管理类"""
    
    def __init__(self):
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """加载测试配置"""
        return {
            # API配置
            'apis': {
                'glm': {
                    'required': True,
                    'env_key': 'GLM_API_KEY',
                    'description': 'GLM-4.5-air LLM API for ReAct Agent',
                    'test_endpoint': 'https://open.bigmodel.cn/api/paas/v4/chat/completions'
                },
                'serper': {
                    'required': False,
                    'env_key': 'SERPER_KEY_ID',
                    'description': 'Google Search API',
                    'default_key': '2fb71d719108d02677a2d8492809a4922e766c3c',
                    'test_endpoint': 'https://google.serper.dev/search'
                },
                'jina': {
                    'required': False,
                    'env_key': 'JINA_API_KEY',
                    'description': 'Jina URL content extraction API',
                    'default_key': 'jina_0b07d5982d6f4ee287de16cc4b32981fTBZpS-i7feuvLyPdauhoeeIjX0XZ',
                    'test_endpoint': 'https://r.jina.ai/http://example.com'
                },
                'sandbox': {
                    'required': False,
                    'env_key': 'SANDBOX_FUSION_ENDPOINT',
                    'description': 'Python code execution sandbox',
                    'default_endpoint': 'http://localhost:8081',
                    'local_service': True
                }
            },
            
            # 测试配置
            'testing': {
                'timeout': 30,
                'retry_attempts': 3,
                'parallel_tests': False,  # 避免API限制
                'verbose_output': True,
                'skip_real_api_tests': os.getenv('SKIP_REAL_API_TESTS', 'false').lower() == 'true'
            },
            
            # 测试数据
            'test_data': {
                'search_queries': [
                    'Python programming basics',
                    'machine learning tutorial',
                    'web development frameworks'
                ],
                'urls': [
                    'https://www.python.org',
                    'https://docs.python.org',
                    'https://github.com/python/cpython'
                ],
                'code_snippets': [
                    'print("Hello, World!")',
                    'x = sum(range(1, 11)); print(f"Sum: {x}")',
                    'def factorial(n): return 1 if n <= 1 else n * factorial(n-1); print(factorial(5))'
                ]
            }
        }
    
    def check_api_availability(self) -> Dict[str, bool]:
        """检查所有API的可用性"""
        availability = {}
        
        for api_name, api_config in self.config['apis'].items():
            if api_name == 'sandbox':
                # 沙箱服务需要特殊检查
                availability[api_name] = self._check_sandbox_availability(api_config)
            else:
                # 其他API检查环境变量
                env_key = api_config['env_key']
                api_key = os.getenv(env_key)
                
                if api_key:
                    availability[api_name] = True
                elif 'default_key' in api_config:
                    availability[api_name] = True
                else:
                    availability[api_name] = False
        
        return availability
    
    def _check_sandbox_availability(self, sandbox_config: Dict[str, Any]) -> bool:
        """检查沙箱服务可用性"""
        endpoint = os.getenv(sandbox_config['env_key'], sandbox_config.get('default_endpoint'))
        
        try:
            # 首先检查沙箱包是否可用
            from sandbox_fusion import run_code, RunCodeRequest
            
            # 执行一个简单的测试代码来验证服务可用性
            test_request = RunCodeRequest(
                code='print("health_check")',
                language='python'
            )
            
            response = run_code(test_request, max_attempts=1, client_timeout=5)
            return True
            
        except ImportError:
            # 如果包不可用，服务不可用
            return False
        except Exception:
            # 如果执行失败，服务可能不可用
            return False
    
    def get_test_status(self) -> Dict[str, Any]:
        """获取测试状态报告"""
        availability = self.check_api_availability()
        skip_real_tests = self.config['testing']['skip_real_api_tests']
        
        status = {
            'ready_for_real_tests': not skip_real_tests and all(availability.values()),
            'skip_real_tests': skip_real_tests,
            'api_availability': availability,
            'missing_apis': [name for name, available in availability.items() if not available],
            'recommendations': []
        }
        
        # 生成建议
        if skip_real_tests:
            status['recommendations'].append("Real API tests are skipped. Set SKIP_REAL_API_TESTS=false to enable.")
        
        missing_required = [name for name, config in self.config['apis'].items() 
                          if config['required'] and not availability.get(name, False)]
        
        if missing_required:
            status['recommendations'].append(f"Missing required APIs: {', '.join(missing_required)}")
        
        if not availability.get('sandbox', False):
            status['recommendations'].append("Python sandbox service not available. Some tests will be skipped.")
        
        return status
    
    def should_skip_api_test(self, api_name: str) -> bool:
        """判断是否应该跳过特定API的测试"""
        if self.config['testing']['skip_real_api_tests']:
            return True
        
        availability = self.check_api_availability()
        return not availability.get(api_name, False)
    
    def get_safe_test_params(self, api_name: str) -> Dict[str, Any]:
        """获取安全的测试参数"""
        test_data = self.config['test_data']
        
        if api_name == 'search' or api_name == 'serper':
            return {
                'query': test_data['search_queries'][0],
                'limit': 5  # 限制结果数量
            }
        elif api_name == 'jina':
            return {
                'url': test_data['urls'][0],
                'goal': 'Extract key information'
            }
        elif api_name == 'sandbox':
            return {
                'code': test_data['code_snippets'][0]
            }
        elif api_name == 'react_agent':
            return {
                'question': 'What is 2+2?',
                'max_steps': 3,
                'timeout': 60
            }
        else:
            return {}
    
    def print_status_report(self):
        """打印测试状态报告"""
        status = self.get_test_status()
        
        print("=" * 60)
        print("🧪 ResearchAgent 测试配置状态报告")
        print("=" * 60)
        
        # API可用性
        print("\n📡 API可用性状态:")
        for api_name, available in status['api_availability'].items():
            status_icon = "✅" if available else "❌"
            api_config = self.config['apis'][api_name]
            print(f"   {status_icon} {api_name.upper()}: {api_config['description']}")
        
        # 测试状态
        print(f"\n🎯 测试配置:")
        print(f"   实时API测试: {'✅ 启用' if not status['skip_real_tests'] else '⏸️  跳过'}")
        print(f"   整体就绪状态: {'✅ 就绪' if status['ready_for_real_tests'] else '⚠️  部分就绪'}")
        
        # 建议
        if status['recommendations']:
            print(f"\n💡 建议:")
            for i, rec in enumerate(status['recommendations'], 1):
                print(f"   {i}. {rec}")
        
        print("=" * 60)


# 全局测试配置实例
test_config = TestConfig()


def setup_test_environment():
    """设置测试环境"""
    # 加载环境变量
    env_file = os.path.join(project_root, '.env')
    if os.path.exists(env_file):
        from dotenv import load_dotenv
        load_dotenv(env_file)
    
    # 打印状态报告
    test_config.print_status_report()


def skip_if_api_unavailable(api_name: str):
    """装饰器：如果API不可用则跳过测试"""
    def decorator(test_func):
        def wrapper(*args, **kwargs):
            if test_config.should_skip_api_test(api_name):
                import unittest
                unittest.skip(f"{api_name.upper()} API not available, skipping test")(test_func)(*args, **kwargs)
            else:
                return test_func(*args, **kwargs)
        return wrapper
    return decorator


if __name__ == "__main__":
    # 运行状态检查
    setup_test_environment()
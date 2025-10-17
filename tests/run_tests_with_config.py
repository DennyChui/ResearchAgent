#!/usr/bin/env python3
"""
使用配置的测试运行器

统一的测试运行器，支持配置管理和智能测试选择。
"""

import sys
import os
import unittest
import argparse
from typing import List, Dict, Any

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from tests.test_config import test_config, setup_test_environment


class ConfiguredTestRunner:
    """配置化的测试运行器"""
    
    def __init__(self):
        self.test_config = test_config
        setup_test_environment()
    
    def discover_tests(self) -> List[unittest.TestCase]:
        """发现所有测试用例"""
        loader = unittest.TestLoader()
        suite = loader.discover('tests', pattern='test_*.py')
        return suite
    
    def run_specific_test(self, test_module: str, test_class: str = None, test_method: str = None):
        """运行特定测试"""
        loader = unittest.TestLoader()
        
        if test_method:
            # 运行特定方法
            suite = loader.loadTestsFromName(f'{test_module}.{test_class}.{test_method}')
        elif test_class:
            # 运行特定类
            suite = loader.loadTestsFromName(f'{test_module}.{test_class}')
        else:
            # 运行整个模块
            suite = loader.loadTestsFromName(test_module)
        
        return self._run_suite(suite)
    
    def run_all_tests(self, skip_real_api: bool = False) -> Dict[str, Any]:
        """运行所有测试"""
        print("🧪 开始运行 ResearchAgent 测试套件")
        print("=" * 60)
        
        # 发现所有测试
        suite = self.discover_tests()
        
        # 运行测试
        return self._run_suite(suite)
    
    def run_api_tests(self, api_name: str) -> Dict[str, Any]:
        """运行特定API相关的测试"""
        test_mapping = {
            'search': ['tests.test_google_search.TestGoogleSearchTool'],
            'serper': ['tests.test_google_search.TestGoogleSearchTool'],
            'glm': ['tests.test_react_agent.TestReActAgent'],
            'react_agent': ['tests.test_react_agent.TestReActAgent'],
            'jina': ['tests.test_jina_url_visit'],
            'sandbox': ['tests.test_python_sandbox.TestPythonSandboxToolIntegration']
        }
        
        if api_name not in test_mapping:
            print(f"❌ 未知的API名称: {api_name}")
            return {'success': False, 'error': f'Unknown API: {api_name}'}
        
        print(f"🔍 运行 {api_name.upper()} API 相关测试...")
        
        loader = unittest.TestLoader()
        suite = unittest.TestSuite()
        
        for test_class in test_mapping[api_name]:
            try:
                suite.addTest(loader.loadTestsFromName(test_class))
            except Exception as e:
                print(f"⚠️  无法加载测试类 {test_class}: {e}")
        
        return self._run_suite(suite)
    
    def _run_suite(self, suite: unittest.TestSuite) -> Dict[str, Any]:
        """运行测试套件"""
        runner = unittest.TextTestRunner(
            verbosity=2,
            stream=sys.stdout,
            buffer=True,
            failfast=False
        )
        
        result = runner.run(suite)
        
        return {
            'tests_run': result.testsRun,
            'failures': len(result.failures),
            'errors': len(result.errors),
            'skipped': len(result.skipped) if hasattr(result, 'skipped') else 0,
            'success': result.wasSuccessful(),
            'details': {
                'failures': result.failures,
                'errors': result.errors
            }
        }
    
    def print_test_summary(self, result: Dict[str, Any]):
        """打印测试结果摘要"""
        print("\\n" + "=" * 60)
        print("📊 测试结果摘要")
        print("=" * 60)
        
        print(f"总测试数: {result['tests_run']}")
        print(f"✅ 成功: {result['tests_run'] - result['failures'] - result['errors']}")
        print(f"❌ 失败: {result['failures']}")
        print(f"🚫 错误: {result['errors']}")
        print(f"⏭️  跳过: {result['skipped']}")
        
        if result['success']:
            print("\\n🎉 所有测试通过！")
        else:
            print("\\n⚠️  部分测试失败，请检查详细信息。")
            
            # 显示失败详情
            if result['details']['failures']:
                print("\\n❌ 失败的测试:")
                for test, traceback in result['details']['failures']:
                    print(f"   - {test}")
            
            if result['details']['errors']:
                print("\\n🚫 错误的测试:")
                for test, traceback in result['details']['errors']:
                    print(f"   - {test}")
        
        print("=" * 60)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='ResearchAgent 测试运行器')
    parser.add_argument('--all', action='store_true', help='运行所有测试')
    parser.add_argument('--module', help='运行特定测试模块 (例: test_google_search)')
    parser.add_argument('--test-class', dest='test_class', help='运行特定测试类 (例: TestGoogleSearchTool)')
    parser.add_argument('--method', help='运行特定测试方法 (例: test_tool_structure)')
    parser.add_argument('--api', help='运行特定API相关测试 (例: search, glm, jina, sandbox)')
    parser.add_argument('--skip-real-api', action='store_true', help='跳过实时API测试')
    parser.add_argument('--config-only', action='store_true', help='仅显示配置状态，不运行测试')
    
    args = parser.parse_args()
    
    runner = ConfiguredTestRunner()
    
    # 仅显示配置
    if args.config_only:
        return
    
    # 运行测试
    result = None
    
    if args.all:
        result = runner.run_all_tests(skip_real_api=args.skip_real_api)
    elif args.api:
        result = runner.run_api_tests(args.api)
    elif args.module:
        if args.method:
            if args.test_class:
                test_name = f"{args.module}.{args.test_class}.{args.method}"
            else:
                test_name = f"{args.module}.{args.method}"
            result = runner.run_specific_test(test_name)
        elif args.test_class:
            test_name = f"{args.module}.{args.test_class}"
            result = runner.run_specific_test(test_name)
        else:
            result = runner.run_specific_test(args.module)
    else:
        # 默认运行快速测试（跳过实时API）
        print("🏃 运行快速测试套件（跳过实时API）...")
        os.environ['SKIP_REAL_API_TESTS'] = 'true'
        result = runner.run_all_tests(skip_real_api=True)
    
    # 打印结果
    if result:
        runner.print_test_summary(result)
        
        # 设置退出码
        sys.exit(0 if result['success'] else 1)


if __name__ == "__main__":
    main()
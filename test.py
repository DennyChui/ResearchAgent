#!/usr/bin/env python3
"""
ResearchAgent 简化测试入口

这是一个简化的测试脚本，提供快速访问常用测试功能。
使用方法:
    python test.py [选项]
"""

import sys
import os

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def print_help():
    """打印帮助信息"""
    print("ResearchAgent 测试工具")
    print()
    print("用法:")
    print("  python test.py [选项]")
    print()
    print("选项:")
    print("  all, -a     运行所有测试")
    print("  quick, -q   快速检查核心功能")
    print("  tools, -t   仅测试工具基础功能")
    print("  agent, -g   仅测试ReAct Agent")
    print("  demo, -d    仅运行演示")
    print("  help, -h    显示此帮助信息")
    print()
    print("示例:")
    print("  python test.py")
    print("  python test.py quick")
    print("  python test.py demo")

def main():
    """主函数"""
    if len(sys.argv) <= 1:
        # 默认运行快速检查
        test_type = 'quick'
    else:
        arg = sys.argv[1].lower()
        
        if arg in ['help', '-h', '--help']:
            print_help()
            return
        elif arg in ['all', '-a']:
            test_type = 'all'
        elif arg in ['quick', '-q']:
            test_type = 'quick'
        elif arg in ['tools', '-t']:
            test_type = 'tools'
        elif arg in ['agent', '-g']:
            test_type = 'agent'
        elif arg in ['demo', '-d']:
            test_type = 'demo'
        else:
            print(f"未知选项: {arg}")
            print("使用 'python test.py help' 查看帮助")
            sys.exit(1)
    
    # 导入并运行统一测试脚本
    try:
        import run_tests
        sys.argv = ['run_tests.py', test_type]
        run_tests.main()
    except ImportError as e:
        print(f"❌ 导入测试模块失败: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 测试运行失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

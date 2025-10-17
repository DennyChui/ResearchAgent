#!/usr/bin/env python3
"""
ResearchAgent 简化测试入口

这是一个简化的测试脚本，提供快速访问常用测试功能。
使用方法:
    python test.py [选项]
"""

import sys
import os

# 尝试加载python-dotenv来读取.env文件
try:
    from dotenv import load_dotenv
    # 加载.env文件（如果存在）
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_path):
        load_dotenv(env_path)
        print("✅ 已加载.env文件")
except ImportError:
    # 如果没有python-dotenv，手动读取.env文件
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_path):
        print("✅ 发现.env文件，手动加载中...")
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()
        print("✅ .env文件加载完成")
    else:
        print("⚠️  未找到.env文件")

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
    print("环境变量:")
    print("  测试脚本会自动加载同目录下的.env文件")
    print("  需要的环境变量包括:")
    print("    GLM_API_KEY          - GLM-4.5-air API密钥 (必需)")
    print("    SERPER_KEY_ID        - Google搜索API密钥")
    print("    JINA_API_KEY         - Jina网页提取API密钥")
    print("    SANDBOX_FUSION_ENDPOINT - Python sandbox端点")
    print()
    print("示例:")
    print("  python test.py")
    print("  python test.py quick")
    print("  python test.py demo")

def check_env_status():
    """检查关键环境变量状态"""
    print("\n🔍 环境变量状态检查:")
    
    key_env_vars = {
        'GLM_API_KEY': 'GLM-4.5-air API密钥',
        'SERPER_KEY_ID': 'Google搜索API密钥', 
        'JINA_API_KEY': 'Jina网页提取API密钥',
        'SANDBOX_FUSION_ENDPOINT': 'Python sandbox端点'
    }
    
    missing_required = []
    
    for var_name, description in key_env_vars.items():
        value = os.getenv(var_name)
        if value:
            if var_name.endswith('_KEY'):
                # 对API密钥进行脱敏显示
                masked_value = value[:4] + '*' * (len(value) - 8) + value[-4:] if len(value) > 8 else '*' * len(value)
                print(f"  ✅ {var_name}: {masked_value} ({description})")
            else:
                print(f"  ✅ {var_name}: {value} ({description})")
        else:
            status = "❌ (必需)" if var_name == 'GLM_API_KEY' else "⚠️  (可选)"
            print(f"  {status} {var_name}: 未设置 ({description})")
            if var_name == 'GLM_API_KEY':
                missing_required.append(var_name)
    
    if missing_required:
        print(f"\n❌ 缺少必需的环境变量: {', '.join(missing_required)}")
        print("💡 请在.env文件中设置这些变量，或手动设置环境变量")
        return False
    else:
        print("\n✅ 所有必要的环境变量已设置")
        return True

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
    
    # 检查环境变量状态
    env_ok = check_env_status()
    
    # 如果缺少必需的环境变量且不是help命令，给出提示
    if not env_ok and test_type not in ['help']:
        print(f"\n⚠️  检测到环境配置问题，但将尝试运行测试...")
        print(f"   某些测试可能会失败。建议先配置.env文件。")
        print(f"   运行 'python test.py help' 查看详细说明。\n")
    
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

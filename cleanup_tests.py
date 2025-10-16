#!/usr/bin/env python3
"""
测试文件清理脚本

清理和整理旧的测试文件，将测试功能集中到统一测试脚本中。
"""

import os
import shutil
from datetime import datetime

def create_backup():
    """创建备份目录"""
    backup_dir = f"backup_tests_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
        print(f"创建备份目录: {backup_dir}")
    
    return backup_dir

def backup_file(filepath, backup_dir):
    """备份文件到指定目录"""
    if os.path.exists(filepath):
        filename = os.path.basename(filepath)
        backup_path = os.path.join(backup_dir, filename)
        shutil.copy2(filepath, backup_path)
        print(f"备份文件: {filename} -> {backup_dir}/{filename}")
        return True
    return False

def list_test_files():
    """列出需要清理的测试文件"""
    test_files = [
        "test_python_tool_standalone.py",
        "test_react_python_sandbox.py", 
        "test_sandbox_fusion_direct.py",
        "demo_react_python_sandbox.py",
    ]
    
    existing_files = []
    for file in test_files:
        if os.path.exists(file):
            existing_files.append(file)
    
    return existing_files

def main():
    """主函数"""
    print("🧹 测试文件清理脚本")
    print("=" * 50)
    
    # 列出要清理的文件
    test_files = list_test_files()
    
    if not test_files:
        print("✅ 没有需要清理的测试文件")
        return
    
    print(f"发现 {len(test_files)} 个需要清理的测试文件:")
    for file in test_files:
        print(f"  - {file}")
    
    print()
    
    # 询问用户是否继续
    response = input("是否继续清理? (y/N): ").strip().lower()
    
    if response != 'y':
        print("❌ 清理操作已取消")
        return
    
    # 创建备份
    backup_dir = create_backup()
    
    # 备份文件
    backed_up = 0
    for file in test_files:
        if backup_file(file, backup_dir):
            backed_up += 1
    
    print(f"\n✅ 已备份 {backed_up} 个文件到 {backup_dir}/")
    
    # 删除旧文件
    deleted = 0
    for file in test_files:
        try:
            os.remove(file)
            print(f"删除文件: {file}")
            deleted += 1
        except Exception as e:
            print(f"❌ 删除文件失败 {file}: {e}")
    
    print(f"\n✅ 清理完成!")
    print(f"  备份文件: {backed_up} 个")
    print(f"  删除文件: {deleted} 个")
    print(f"  备份目录: {backup_dir}/")
    print()
    print("现在可以使用以下方式运行测试:")
    print("  python test.py        # 快速检查")
    print("  python test.py all    # 完整测试")
    print("  python test.py demo   # 运行演示")

if __name__ == "__main__":
    main()

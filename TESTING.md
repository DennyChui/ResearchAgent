# ResearchAgent 测试指南

本文档介绍如何使用 ResearchAgent 的测试系统。

## 🧪 测试概览

ResearchAgent 提供了统一的测试框架，包含以下测试类型：

- **单元测试**: 测试各个工具的基础功能
- **集成测试**: 测试工具间的协作和整体功能
- **演示测试**: 展示系统能力的实际演示
- **快速检查**: 快速验证核心功能是否正常

## 🚀 快速开始

### 基本用法

```bash
# 快速检查核心功能（推荐）
python test.py

# 或者
python test.py quick
```

### 完整测试

```bash
# 运行所有测试
python test.py all

# 仅测试工具基础功能
python test.py tools

# 仅测试 ReAct Agent
python test.py agent

# 仅运行演示
python test.py demo
```

### 直接使用统一测试脚本

```bash
# 运行所有测试
python run_tests.py

# 指定测试类型
python run_tests.py tools
python run_tests.py agent
python run_tests.py demo
python run_tests.py quick
```

## 📋 测试内容详解

### 1. 环境检查
- Python 版本验证
- 环境变量检查
- 依赖包安装验证

### 2. 工具基础功能测试
- **Python Sandbox 工具**
  - 工具属性和方法检查
  - 参数 schema 验证
  - 基础代码执行测试
  - 错误处理验证

### 3. ReAct Agent 集成测试
- 工具加载验证
- 工具调用检测测试
- 系统提示集成检查
- 实际工具执行验证

### 4. 能力演示测试
- **数学研究能力**
  - 黄金分割比例计算
  - 数学公式验证
- **数据分析能力**
  - 统计计算
  - 趋势分析
- **科学计算能力**
  - 物理模拟
  - 算法实现

### 5. 边界情况测试
- 空代码处理
- 长代码处理
- Unicode 字符支持
- 多行代码支持

## 🔧 环境配置

### 必需的环境变量

```bash
# GLM-4.5-air LLM API (用于 ReAct Agent)
export GLM_API_KEY=your_glm_api_key

# Serper Search API (用于搜索功能)
export SERPER_KEY_ID=your_serper_api_key

# Jina API (用于网页内容提取)
export JINA_API_KEY=your_jina_api_key

# Sandbox Fusion (用于 Python 代码执行)
export SANDBOX_FUSION_ENDPOINT=http://localhost:8081
```

### 依赖包安装

```bash
# 安装所有依赖
uv sync

# 或者使用 pip
pip install -r requirements.txt
```

## 📊 测试结果解读

### 成功示例
```
✅ Python Sandbox工具基础功能 (0.45s)
    Python sandbox工具所有基础功能正常
✅ ReAct Agent工具集成 (0.23s)
    ReAct Agent工具集成正常
```

### 失败示例
```
❌ 环境检查 (0.01s)
    Exception: 环境变量 GLM_API_KEY 未设置
```

### 测试总结
```
==================================================
测试总结
==================================================
总测试数: 8
通过: 7
失败: 1
成功率: 87.5%
总耗时: 2.34s
```

## 🛠️ 测试开发

### 添加新测试

1. 在 `run_tests.py` 中添加新的测试函数
2. 确保函数返回 `(bool, str)` 格式
3. 在相应的测试套件中调用

```python
def test_new_feature():
    """测试新功能"""
    try:
        # 测试逻辑
        return True, "新功能测试通过"
    except Exception as e:
        return False, f"新功能测试失败: {str(e)}"

# 在主函数中添加
test_suite.run_test("新功能测试", test_new_feature)
```

### 测试函数规范

- 函数名以 `test_` 开头
- 包含清晰的文档字符串
- 返回 `(passed: bool, message: str)` 元组
- 使用断言或异常处理进行验证
- 提供有意义的错误信息

## 🔍 故障排除

### 常见问题

1. **环境变量未设置**
   ```
   ❌ 环境检查 (0.01s)
       Exception: 环境变量 GLM_API_KEY 未设置
   ```
   解决方案: 设置相应的环境变量

2. **依赖包缺失**
   ```
   ❌ Python Sandbox工具基础功能 (0.01s)
       Exception: No module named 'sandbox_fusion'
   ```
   解决方案: 安装缺失的依赖包

3. **Sandbox 服务连接失败**
   ```
   ❌ Python Sandbox工具基础功能 (0.01s)
       Exception: Failed to set sandbox endpoint
   ```
   解决方案: 确保 Sandbox Fusion 服务运行在指定端口

### 调试模式

运行单个测试进行调试：
```python
# 在 run_tests.py 中直接调用测试函数
if __name__ == "__main__":
    # 只运行特定测试
    test_suite.run_test("特定测试", test_specific_function)
    test_suite.print_summary()
```

## 📝 更新日志

### v1.0.0 (2024-10-16)
- 创建统一测试框架
- 整合所有测试功能
- 添加详细文档和示例

### 旧测试文件处理

旧的测试文件已通过 `cleanup_tests.py` 脚本进行清理：
- `test_python_tool_standalone.py`
- `test_react_python_sandbox.py`
- `test_sandbox_fusion_direct.py`
- `demo_react_python_sandbox.py`

这些文件的内容已经整合到新的统一测试框架中。

## 🤝 贡献指南

1. 新增功能时，请添加相应的测试
2. 确保所有测试通过后再提交代码
3. 遵循现有的测试代码风格
4. 为复杂的测试添加详细的文档说明

## 📞 支持

如果遇到测试相关问题，请：
1. 检查本文档的故障排除部分
2. 查看测试输出中的错误信息
3. 在项目中创建 issue 并提供详细的错误信息

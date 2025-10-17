# Contributing to ResearchAgent

感谢您对 ResearchAgent 项目的关注！我们欢迎各种形式的贡献。

## 🤝 如何贡献

### 报告问题
- 使用 [GitHub Issues](https://github.com/DennyChui/ResearchAgent/issues) 报告bug
- 提供详细的问题描述、复现步骤和环境信息
- 包含相关的错误日志和截图

### 提出功能请求
- 在 [GitHub Discussions](https://github.com/DennyChui/ResearchAgent/discussions) 中讨论新功能想法
- 描述功能的使用场景和预期行为
- 考虑是否可以通过现有工具组合实现

### 代码贡献
1. **Fork** 本仓库
2. **创建分支**: `git checkout -b feature/amazing-feature`
3. **提交更改**: `git commit -m 'Add amazing feature'`
4. **推送分支**: `git push origin feature/amazing-feature`
5. **创建 Pull Request**

## 🛠️ 开发环境设置

### 环境要求
- Python 3.12+
- UV 包管理器
- Git

### 设置步骤
```bash
# 1. 克隆仓库
git clone https://github.com/DennyChui/ResearchAgent.git
cd ResearchAgent

# 2. 安装依赖
uv install

# 3. 设置环境变量
cp .env.example .env
# 编辑 .env 文件，添加必要的API密钥

# 4. 运行测试确保环境正常
uv run python researchagent.py test

# 5. 启动开发模式
uv run python researchagent.py interactive
```

### 环境变量配置
创建 `.env` 文件并设置以下变量：
```bash
GLM_API_KEY=your_glm_api_key_here
SERPER_KEY_ID=your_serper_api_key_here
JINA_API_KEY=your_jina_api_key_here
SANDBOX_FUSION_ENDPOINT=your_sandbox_endpoint
```

## 📝 代码规范

### Python 代码风格
- 遵循 [PEP 8](https://pep8.org/) Python代码规范
- 使用 4 个空格缩进
- 行长度限制为 88 字符
- 使用 Black 进行代码格式化

### 命名规范
- **类名**: `PascalCase` (例: `GoogleSearchTool`)
- **函数/变量名**: `snake_case` (例: `call_search_api`)
- **常量**: `UPPER_SNAKE_CASE` (例: `DEFAULT_TIMEOUT`)
- **私有成员**: 前缀单下划线 (例: `_internal_method`)

### 文档字符串
```python
def search_google(query: str, limit: int = 10) -> str:
    """执行Google搜索并返回格式化结果。

    Args:
        query: 搜索查询字符串
        limit: 返回结果数量限制

    Returns:
        格式化的搜索结果字符串

    Raises:
        ValueError: 当查询为空时
        APIError: 当API调用失败时
    """
    pass
```

### 类型注解
- 所有公共函数和方法必须有类型注解
- 使用 `typing` 模块的类型提示
- 复杂类型使用 `Optional`、`Union`、`List` 等

```python
from typing import Optional, Union, List, Dict, Any

def process_results(
    data: Dict[str, Any],
    filters: Optional[List[str]] = None
) -> Union[str, None]:
    pass
```

## 🧪 测试指南

### 运行测试
```bash
# 运行所有测试
uv run python researchagent.py test

# 运行特定测试
uv run python tests/test_google_search.py

# 运行测试并生成覆盖率报告
uv run python researchagent.py test --coverage
```

### 编写测试
- 测试文件命名: `test_*.py`
- 测试类命名: `TestClassName`
- 测试方法命名: `test_method_name`

```python
import unittest
from inference.google_search_tool import GoogleSearchTool

class TestGoogleSearchTool(unittest.TestCase):
    def setUp(self):
        self.tool = GoogleSearchTool()

    def test_search_with_valid_query(self):
        result = self.tool.call({"query": "Python"})
        self.assertIsInstance(result, str)
        self.assertIn("Python", result)
```

## 📚 项目结构

```
ResearchAgent/
├── inference/           # 核心工具模块
├── cli/                # 命令行接口
├── examples/           # 使用示例
├── tests/              # 测试代码
├── docs/               # 文档
└── scripts/            # 开发脚本
```

### 添加新工具
1. 在 `inference/` 目录创建工具文件
2. 继承 `BaseTool` 类
3. 实现必要的方法
4. 添加对应的测试文件
5. 更新文档

### 添加新CLI命令
1. 在 `cli/commands/` 目录创建命令文件
2. 继承 `BaseCommand` 类
3. 实现参数解析和执行逻辑
4. 在 `cli/cli.py` 中注册命令

## 🔄 提交流程

### 提交前检查
- [ ] 代码通过所有测试
- [ ] 代码符合项目规范
- [ ] 添加了必要的测试
- [ ] 更新了相关文档
- [ ] 提交信息清晰描述更改

### 提交信息格式
```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**类型说明:**
- `feat`: 新功能
- `fix`: 修复bug
- `docs`: 文档更改
- `style`: 代码格式化
- `refactor`: 重构代码
- `test`: 添加或修改测试
- `chore`: 构建过程或辅助工具的变动

**示例:**
```
feat(search): add Google Scholar search support

- Implement GoogleScholarTool class
- Add scholarly query formatting
- Update CLI with --type scholar option

Closes #123
```

## 🐛 Bug 报告

使用以下模板报告bug：

```markdown
**Bug 描述**
简要描述bug

**复现步骤**
1. 执行命令 '...'
2. 点击 '....'
3. 滚动到 '....'
4. 看到错误

**预期行为**
描述您期望发生的情况

**实际行为**
描述实际发生的情况

**环境信息**
- OS: [例如 macOS 14.0]
- Python版本: [例如 3.12.0]
- ResearchAgent版本: [例如 0.3.0]

**附加信息**
添加任何其他有助于解决问题的信息
```

## 💡 功能请求

使用以下模板提出功能请求：

```markdown
**功能描述**
清晰简洁地描述您想要的功能

**问题解决**
描述这个功能解决了什么问题

**建议的解决方案**
描述您希望如何实现这个功能

**替代方案**
描述您考虑过的其他替代解决方案

**附加信息**
添加任何其他相关信息或截图
```

## 📖 文档贡献

- 改进现有文档的清晰度和准确性
- 添加缺失的文档
- 翻译文档到其他语言
- 添加更多使用示例

文档文件位于：
- `README.md` - 主要文档
- `docs/` - 详细文档
- 代码中的docstring - API文档

## 🏷️ 发布流程

1. 更新版本号
2. 更新 `CHANGELOG.md`
3. 创建 Git 标签
4. 构建和发布

## 🤝 社区

- GitHub: [ResearchAgent](https://github.com/DennyChui/ResearchAgent)
- Discussions: [GitHub Discussions](https://github.com/DennyChui/ResearchAgent/discussions)
- Issues: [GitHub Issues](https://github.com/DennyChui/ResearchAgent/issues)

## 📄 许可证

通过贡献代码，您同意您的贡献将在 [MIT 许可证](LICENSE) 下授权。

---

感谢您的贡献！🚀
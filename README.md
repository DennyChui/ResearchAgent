# ResearchAgent - AI 研究助手

这是一个基于 Qwen-Agent 框架的 AI 研究助手项目，集成了多种工具来支持信息检索、分析和处理。

## 功能特性

- ✅ **Google搜索**: 使用Serper API进行实时网络搜索
- ✅ **Google学术搜索**: 学术文献和论文检索
- ✅ **Jina网页访问**: 智能网页内容提取和摘要
- ✅ **ReAct Agent**: 基于推理和行动的智能研究代理
- ✅ **Qwen-Agent集成**: 完全兼容Qwen-Agent的BaseTool接口
- ✅ **智能格式化**: 将搜索结果格式化为易读的字符串
- ✅ **错误处理**: 完善的网络错误和API错误处理
- ✅ **超时控制**: 内置请求超时机制，防止长时间阻塞

## 文件结构

```
├── inference/               # 核心推理工具
│   ├── __init__.py         # 包初始化文件
│   ├── google_search_tool.py    # Google搜索工具实现
│   ├── google_scholar_tool.py   # Google学术搜索工具
│   ├── jina_url_visit_tool.py   # Jina网页访问工具
│   └── react_agent.py          # ReAct Agent实现
├── tests/                   # 测试脚本
│   ├── __init__.py         # 测试包初始化
│   ├── test_google_search.py    # Google搜索工具测试
│   ├── test_jina_url_visit.py   # Jina网页访问工具测试
│   └── test_react_agent.py      # ReAct Agent测试
├── main.py                  # 项目主入口
├── example_usage.py         # 工具使用示例
├── example_react_agent.py   # ReAct Agent使用示例
└── README.md               # 文档
```

## 安装依赖

```bash
# 使用uv安装依赖
uv add qwen-agent python-dateutil openai
```

## 快速开始

### 1. 直接使用工具

```python
from inference.google_search_tool import GoogleSearchTool

# 创建工具实例
tool = GoogleSearchTool()

# 执行搜索
result = tool.call({"query": "Python编程教程"})
print(result)
```

### 2. 使用 ReAct Agent 进行智能研究

```python
from inference.react_agent import ReActAgent

# 创建ReAct Agent实例
agent = ReActAgent()

# 进行深度研究
question = "量子计算在医疗领域的应用前景如何？"
result = agent.research(question)
print(result)
```

### 3. 命令行使用

```bash
# Google搜索
uv run python main.py search "Python编程教程"

# ReAct Agent深度研究
uv run python main.py research "量子计算的发展历史"

# 运行测试
uv run python main.py test

# 交互式模式
uv run python main.py interactive

# 查看帮助
uv run python main.py help
```

### 4. 与Qwen-Agent Assistant集成

```python
from qwen_agent.agents import Assistant

# 配置LLM
llm_cfg = {
    'model': 'qwen-max',
    'model_type': 'qwen_dashscope',
    'api_key': 'YOUR_DASHSCOPE_API_KEY'
}

# 创建Assistant，包含Google搜索工具
assistant = Assistant(
    llm=llm_cfg,
    function_list=['google_search'],  # 使用注册的工具名称
    system_message="你是一个智能助手，可以使用Google搜索获取最新信息。"
)

# 使用助手进行搜索
messages = [{'role': 'user', 'content': '请搜索最新的AI发展趋势'}]
for response in assistant.run(messages=messages):
    print(response)
```

### 3. 自定义Agent集成

```python
from qwen_agent import Agent
from inference.google_search_tool import GoogleSearchTool

class SearchAgent(Agent):
    def _run(self, messages, **kwargs):
        # 使用Google搜索工具
        search_results = self._call_tool('google_search', {
            'query': messages[-1]['content']
        })

        # 返回搜索结果
        yield [{'role': 'assistant', 'content': search_results}]

# 创建Agent
agent = SearchAgent(
    function_list=[GoogleSearchTool()]
)
```

## API配置

### 环境变量
- `SERPER_KEY_ID`: Serper API密钥 (默认: `2fb71d719108d02677a2d8492809a4922e766c3c`)

### API信息
- **服务提供商**: Serper API
- **API端点**: `https://google.serper.dev/search`
- **请求方法**: POST
- **返回格式**: JSON

## 工具接口

### 属性
- `name`: `google_search`
- `description`: "Search Google for information using Serper API. Returns organic search results with titles, snippets, and links."
- `parameters`:
  ```json
  [
    {
      "name": "query",
      "type": "string",
      "description": "The search query to perform on Google",
      "required": true
    }
  ]
  ```

### 方法
- `call(params: Union[str, dict]) -> str`: 执行Google搜索

## 输出格式

搜索结果按以下格式返回：

```
A Google search for 'query' found N results (search time: X.XXs):

## Web Results

### 1. 结果标题
结果描述片段
🔗 结果链接

### 2. 结果标题
结果描述片段
🔗 结果链接
...
```

## 错误处理

工具包含完善的错误处理机制：

- **网络错误**: 连接超时、DNS解析失败等
- **API错误**: 认证失败、请求限制等
- **参数错误**: 空查询、无效参数格式等
- **数据错误**: JSON解析失败、数据格式异常等

## ReAct Agent 智能研究代理

### 特性

ReAct Agent 是一个基于推理和行动模式的智能研究代理，具备以下特性：

- 🧠 **智能推理**: 使用 GLM-4.5-air 模型进行复杂推理
- 🔍 **多工具协作**: 自动选择合适的工具组合
- 📚 **深度研究**: 系统性收集和分析信息
- 🔄 **迭代优化**: 基于 ReAct 循环不断改进研究质量
- 📊 **上下文管理**: 智能管理对话历史和上下文

### 工作流程

1. **理解问题**: 分析用户的研究需求
2. **制定策略**: 确定搜索策略和工具选择
3. **执行搜索**: 使用 Google 搜索、学术搜索、网页访问等工具
4. **分析结果**: 整合和分析收集到的信息
5. **生成答案**: 提供全面、准确的研究报告

### 使用示例

```python
from inference.react_agent import ReActAgent

# 初始化代理
agent = ReActAgent()

# 研究复杂问题
question = "人工智能在医疗诊断中的最新进展和应用案例"
result = agent.research(question)

print(result)
```

## 测试

运行测试脚本验证工具功能：

```bash
# 运行所有测试
uv run python main.py test

# 运行特定测试
uv run python tests/test_google_search.py
uv run python tests/test_react_agent.py
```

测试包括：
- ✅ 工具基本结构测试
- ✅ 参数处理测试
- ✅ 结果格式化测试
- ✅ Qwen-Agent集成测试
- ✅ ReAct Agent 完整流程测试

## 使用示例

查看完整的使用示例：

```bash
uv run python example_usage.py
```

示例包括：
- 直接工具调用
- Assistant集成
- 自定义Agent开发

## 注意事项

1. **网络连接**: 工具需要稳定的网络连接来访问Serper API
2. **API限制**: Serper API可能有请求频率限制
3. **API密钥**: 生产环境中建议设置环境变量`SERPER_KEY_ID`
4. **超时设置**: 默认超时时间为10秒，可根据需要调整

## 开发说明

### 核心实现
- 继承`qwen_agent.tools.base.BaseTool`
- 使用`@register_tool('google_search')`装饰器注册工具
- 实现`call`方法处理搜索请求
- 使用Python标准库`http.client`进行HTTPS请求

### 设计原则
- **简洁性**: 代码结构清晰，易于理解和维护
- **健壮性**: 完善的错误处理和异常捕获
- **兼容性**: 完全兼容Qwen-Agent框架规范
- **性能**: 合理的超时控制和资源管理

## 许可证

本项目采用MIT许可证。

## 贡献

欢迎提交Issue和Pull Request来改进这个工具！
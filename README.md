# Google搜索工具 (Qwen-Agent)

这是一个为Qwen-Agent框架开发的Google搜索工具，使用Serper API提供网络搜索功能。

## 功能特性

- ✅ **Google搜索**: 使用Serper API进行实时网络搜索
- ✅ **Qwen-Agent集成**: 完全兼容Qwen-Agent的BaseTool接口
- ✅ **智能格式化**: 将搜索结果格式化为易读的字符串
- ✅ **错误处理**: 完善的网络错误和API错误处理
- ✅ **超时控制**: 内置请求超时机制，防止长时间阻塞

## 文件结构

```
├── inference/               # 核心推理工具
│   ├── __init__.py         # 包初始化文件
│   └── google_search_tool.py    # Google搜索工具实现
├── tests/                   # 测试脚本
│   ├── __init__.py         # 测试包初始化
│   └── test_google_search.py    # 测试脚本
├── example_usage.py         # 使用示例
└── README.md               # 文档
```

## 安装依赖

```bash
# 使用uv安装依赖
uv init
uv add qwen-agent python-dateutil
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

### 2. 与Qwen-Agent Assistant集成

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

## 测试

运行测试脚本验证工具功能：

```bash
uv run python tests/test_google_search.py
```

测试包括：
- ✅ 工具基本结构测试
- ✅ 参数处理测试
- ✅ 结果格式化测试
- ✅ Qwen-Agent集成测试

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
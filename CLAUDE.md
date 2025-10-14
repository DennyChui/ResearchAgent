# ResearchAgent - Claude Code 项目配置

## 项目概述

ResearchAgent 是一个基于 Qwen-Agent 框架的 AI 研究助手项目，集成了多种工具来支持信息检索、分析和处理。

## 核心架构

### 目录结构

```
ResearchAgent/
├── inference/               # 核心推理工具
│   ├── __init__.py         # 包初始化文件，导出核心工具
│   └── google_search_tool.py    # Google搜索工具实现
├── tests/                   # 测试套件
│   ├── __init__.py         # 测试包初始化
│   └── test_google_search.py    # Google搜索工具测试
├── main.py                  # 项目主入口（如果需要）
├── CLAUDE.md               # Claude Code 配置文档
├── README.md               # 项目文档
├── pyproject.toml          # Python 项目配置
└── uv.lock                 # 依赖锁定文件
```

### 核心组件

#### 1. 搜索工具 (`inference/google_search_tool.py`)

- **功能**: 使用 Serper API 提供 Google 搜索能力
- **接口**: 继承 Qwen-Agent 的 `BaseTool`
- **注册**: 使用 `@register_tool('search')` 装饰器
- **特性**:
  - 实时网络搜索
  - 支持单查询和批量查询
  - 智能结果格式化
  - 完善的错误处理
  - 超时控制机制
  - JSON Schema 参数格式

#### 2. Google Scholar 工具 (`inference/google_scholar_tool.py`)

- **功能**: 使用 Serper API 提供 Google Scholar 学术搜索能力
- **接口**: 继承 Qwen-Agent 的 `BaseTool`
- **注册**: 使用 `@register_tool('google_scholar')` 装饰器
- **特性**:
  - 学术文献搜索
  - 支持单查询和批量查询
  - 出版信息和引用数据
  - PDF 链接提取
  - 完善的错误处理
  - JSON Schema 参数格式

#### 3. Jina URL 访问工具 (`inference/jina_url_visit_tool.py`)

- **功能**: 使用 Jina API 提取网页内容并使用 LLM 生成智能摘要
- **接口**: 继承 Qwen-Agent 的 `BaseTool`
- **注册**: 使用 `@register_tool('jina_url_visit')` 装饰器
- **特性**:
  - 网页内容结构化提取
  - 支持单 URL 和批量 URL 处理
  - 基于 Goal 的智能摘要生成
  - 内容智能截断和 Token 管理
  - 完善的错误处理和重试机制
  - JSON Schema 参数格式

#### 4. 测试框架 (`tests/`)

- **结构测试**: 验证工具基本结构和接口
- **功能测试**: 模拟 API 调用和结果格式化
- **集成测试**: 验证与 Qwen-Agent 框架的兼容性
- **运行命令**: `uv run python tests/test_google_search.py`


## 技术栈

- **核心框架**: Qwen-Agent
- **语言**: Python 3.12+
- **包管理**: UV
- **API 服务**: Serper Search API
- **HTTP 客户端**: Python 标准库 `http.client`

## 开发环境

### 依赖管理

使用 UV 进行依赖管理：

```bash
# 安装依赖
uv add qwen-agent python-dateutil

# 运行测试
uv run python tests/test_google_search.py
```

### 核心依赖

- `qwen-agent`: AI Agent 框架
- `python-dateutil`: 日期时间处理
- `http.client`: HTTP 请求（Python 标准库）
- `json`: JSON 处理（Python 标准库）
- `urllib.parse`: URL 编码（Python 标准库）

## API 配置

### LLM config openai兼容
- **模型**: glm-4.5-air
- **model_server**:https://open.bigmodel.cn/api/paas/v4       
- **api_key**: `69b6cf3268474acf8c3d0d1898faee85.YNWhmxkqgoDQj67n`

### Serper API

- **API 密钥**: `SERPER_KEY_ID` 环境变量
- **默认密钥**: `2fb71d719108d02677a2d8492809a4922e766c3c`
- **端点**: `https://google.serper.dev/search`
- **方法**: POST
- **超时**: 10秒

### Jina API

- **API 密钥**: `JINA_API_KEY` 环境变量
- **默认密钥**: `jina_0b07d5982d6f4ee287de16cc4b32981fTBZpS-i7feuvLyPdauhoeeIjX0XZ`
- **端点**: `https://r.jina.ai/{url}`
- **方法**: GET
- **超时**: 10秒
- **重试**: 5次重试，每次超时2秒

## 工具接口规范

### 搜索工具 (SearchTool)

```python
@register_tool('search')
class GoogleSearchTool(BaseTool):
    name = 'search'
    description = 'Search Google for information using Serper API...'
    parameters = {
        "type": "object",
        "properties": {
            "query": {
                "type": ["string", "array"],
                "description": "Search query(s) - can be a single query string or array of queries",
                "minItems": 1,
                "items": {"type": "string"}
            }
        },
        "required": ["query"]
    }

    def call(self, params: Union[str, dict]) -> str:
        # 实现搜索逻辑，支持单查询和批量查询
```

### Google Scholar 工具 (GoogleScholarTool)

```python
@register_tool('google_scholar')
class GoogleScholarTool(BaseTool):
    name = 'google_scholar'
    description = 'Search Google Scholar for academic literature...'
    parameters = {
        "type": "object",
        "properties": {
            "query": {
                "type": ["string", "array"],
                "description": "Search query(s) - can be a single query string or array of queries",
                "minItems": 1,
                "items": {"type": "string"}
            }
        },
        "required": ["query"]
    }

    def call(self, params: Union[str, dict]) -> str:
        # 实现学术搜索逻辑，支持单查询和批量查询
```

### Jina URL 访问工具 (JinaURLVisitTool)

```python
@register_tool('jina_url_visit')
class JinaURLVisitTool(BaseTool):
    name = 'jina_url_visit'
    description = 'Visit web pages using Jina API to extract structured content and generate intelligent summaries...'
    parameters = {
        "type": "object",
        "properties": {
            "url": {
                "type": ["string", "array"],
                "description": "URL(s) to visit and extract content from - can be single URL or array of URLs",
                "minItems": 1,
                "maxItems": 5,
                "items": {"type": "string", "format": "uri"}
            },
            "goal": {
                "type": "string",
                "description": "The goal or objective for summarizing the web page content",
                "minLength": 5,
                "maxLength": 200
            }
        },
        "required": ["url", "goal"]
    }

    def call(self, params: Union[str, dict]) -> str:
        # 实现网页内容提取和智能摘要，支持单URL和批量URL处理
        # 包含Jina API调用、内容截断、LLM摘要等功能
```

## 输出格式

搜索结果采用标准化格式：

```
A Google search for '{query}' found {total} results (search time: {time}s):

## Web Results

### 1. 标题
描述片段
🔗 链接

### 2. 标题
描述片段
🔗 链接
...
```

## 错误处理策略

1. **网络错误**: 连接超时、DNS 失败
2. **API 错误**: 认证失败、请求限制
3. **参数错误**: 空查询、无效格式
4. **数据错误**: JSON 解析失败

## 扩展指南

### 添加新工具

1. 在 `inference/` 目录创建新工具文件
2. 继承 `BaseTool` 并实现 `call` 方法
3. 使用 `@register_tool()` 装饰器注册
4. 在 `inference/__init__.py` 中导出新工具
5. 在 `tests/` 中添加对应测试

### 测试新功能

1. 在 `tests/` 目录创建测试文件
2. 遵循现有测试模式：结构测试、功能测试、集成测试
3. 使用 `uv run python tests/` 运行测试

## 开发工作流

1. **功能开发**: 在 `inference/` 中实现核心功能
2. **测试验证**: 在 `tests/` 中编写和运行测试
3. **文档更新**: 更新 `README.md` 和 `CLAUDE.md`

## 部署注意事项

1. **环境变量**: 确保设置正确的 API 密钥
2. **网络连接**: 确保可访问 Serper API
3. **依赖版本**: 使用 `uv.lock` 锁定依赖版本
4. **错误监控**: 监控 API 调用失败率

## 贡献指南

1. 遵循现有代码结构和命名规范
2. 为新功能添加完整测试
3. 更新相关文档
4. 确保所有测试通过后提交

## 版本历史

- **v0.1.0**: 初始版本，包含 Google 搜索工具
- 后续版本按需更新
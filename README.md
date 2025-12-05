# ResearchAgent - AI 研究助手

基于 Qwen-Agent 框架的智能研究助手，集成了多种工具来支持信息检索、分析和处理。

## ✨ 功能特性

- 🔍 **Google搜索**: 实时网络搜索
- 🎓 **Google学术搜索**: 学术文献和论文检索
- 🌐 **Jina网页访问**: 智能网页内容提取和摘要
- 🤖 **ReAct Agent**: 基于推理和行动的智能研究代理
- 🐍 **Python沙箱**: 安全的代码执行环境
- 🛠️ **Qwen-Agent集成**: 完全兼容Qwen-Agent的BaseTool接口

## 🚀 快速开始

### 环境准备

```bash
# 克隆项目
git clone https://github.com/DennyChui/ResearchAgent.git
cd ResearchAgent

# 安装依赖
uv install

# 设置API密钥
export GLM_API_KEY="your_glm_api_key_here"
```

### 快速测试

```bash
# 搜索功能
uv run python researchagent.py search "人工智能最新发展"

# 智能研究
uv run python researchagent.py research "区块链技术发展"

# 交互式模式
uv run python researchagent.py interactive
```

## 📁 项目结构

```
ResearchAgent/
├── inference/               # 核心推理工具
│   ├── google_search_tool.py    # Google搜索工具
│   ├── google_scholar_tool.py   # Google学术搜索
│   ├── jina_url_visit_tool.py   # Jina网页访问工具
│   ├── python_sandbox_tool.py   # Python沙箱工具
│   ├── react_agent.py          # ReAct Agent实现
│   └── research_tool.py        # 研究工具
├── cli/                     # 命令行接口模块
├── tests/                  # 测试脚本
└── researchagent.py        # CLI入口点
```

## 🛠️ CLI 工具使用

### 基础命令

```bash
# 搜索功能
uv run python researchagent.py search "查询关键词"

# 学术搜索
uv run python researchagent.py search "深度学习" --type scholar

# 智能研究
uv run python researchagent.py research "研究问题"
```

### 高级选项

```bash
# 设置搜索结果数量
uv run python researchagent.py search "Python" --limit 20

# JSON格式输出
uv run python researchagent.py search "AI" --output json

# 保存研究结果
uv run python researchagent.py research "问题" --save results.txt

# 查看帮助
uv run python researchagent.py --help
```

## 🔧 编程接口

### 单独使用工具

```python
from inference import GoogleSearchTool, GoogleScholarTool, JinaURLVisitTool

# Google搜索
search_tool = GoogleSearchTool()
result = search_tool.call({"query": "Python编程教程"})

# 学术搜索
scholar_tool = GoogleScholarTool()
papers = scholar_tool.call({"query": "machine learning research 2024"})

# 网页访问
visit_tool = JinaURLVisitTool()
content = visit_tool.call({
    "url": "https://www.python.org/about/",
    "goal": "了解Python的历史和特点"
})
```

### ReAct Agent 智能研究

```python
from inference.react_agent import ReActAgent

# 创建智能研究代理
agent = ReActAgent()

# 进行深度研究
question = "分析量子计算在医疗诊断领域的最新进展"
result = agent.research(question)

print("📋 研究报告:")
print("=" * 60)
print(result)

# 查看研究统计
print(f"📊 LLM调用次数: {agent.llm_calls}")
print(f"📊 消息总数: {len(agent.messages)}")
```

## ⚙️ 环境配置

### 必需环境变量

```bash
# LLM API (必需)
export LLM_API_KEY="your_llm_api_key_here"

# 搜索服务API密钥 (可选，有默认值)
export SERPER_KEY_ID="your_serper_api_key_here"

# Jina API密钥 (可选，有默认值)
export JINA_API_KEY="your_jina_api_key_here"

# Python沙箱服务端点
export SANDBOX_FUSION_ENDPOINT="http://localhost:8081"
```

### API 配置详情

| 服务 | 端点 | 免费额度 | 必需性 |
|------|------|----------|--------|
| **LLM** | [智谱AI](https://open.bigmodel.cn/) | 按token计费 | ✅ 必需 |
| **Serper Search** | [Serper](https://serper.dev/) | 2,500次/月 | ❌ 可选 |
| **Jina API** | [Jina AI](https://jina.ai/) | 200,000次/月 | ❌ 可选 |
| **Sandbox Fusion** | 本地服务 | 无限制 | ❌ 可选 |

## 🧪 测试系统

### 运行测试

```bash
# 检查配置状态
uv run python tests/test_config.py

# 运行特定测试模块
uv run python tests/test_google_search.py
uv run python tests/test_google_scholar_tool.py
uv run python tests/test_jina_url_visit.py
uv run python tests/test_python_sandbox.py
uv run python tests/test_react_agent.py
uv run python tests/test_research_tool.py
```

### 测试配置

项目使用真实API调用进行测试，提供最可靠的验证：

- ✅ **36/36 测试通过** (100% 成功率)
- ✅ **真实API集成** - 所有测试使用实际API
- ✅ **智能跳过机制** - API不可用时优雅跳过
- ✅ **完整覆盖** - 单元测试、集成测试、边界测试

## 📊 性能和限制

### ReAct Agent 性能
- **最大LLM调用次数**: 100次
- **上下文窗口管理**: 12,000 tokens
- **支持工具**: Google搜索、Google学术、Jina网页访问、Python沙箱
- **平均响应时间**: 3-10秒

### API 限制
- **Serper API**: 每月2,500次免费请求
- **LLM**: 按token计费
- **Jina API**: 每月200,000次免费请求

## 🔧 开发指南

### 代码规范
- 遵循 [PEP 8](https://pep8.org/) Python代码规范
- 使用 4 个空格缩进
- 所有公共函数和方法必须有类型注解
- 添加适当的文档字符串

### 添加新工具

1. 在 `inference/` 目录创建工具文件
2. 继承 `BaseTool` 类
3. 实现必要的方法
4. 使用 `@register_tool()` 装饰器注册
5. 添加对应的测试文件

### 贡献流程

```bash
# 1. Fork 本仓库
git clone https://github.com/DennyChui/ResearchAgent.git

# 2. 创建特性分支
git checkout -b feature/amazing-feature

# 3. 提交更改
git commit -m 'Add amazing feature'

# 4. 推送分支
git push origin feature/amazing-feature

# 5. 创建 Pull Request
```

## 📝 版本历史

### v0.3.0 (2024-10-17) - 最新版本
- 🚀 **重构**: 全新CLI系统，模块化命令行接口
- 🧪 **测试重构**: 所有测试使用真实API调用，36/36测试通过
- 📁 **重组**: 优化项目结构，简化目录结构
- 🗑️ **清理**: 移除冗余文件，精简代码库
- 🔧 **增强**: 统一的入口点和丰富的CLI选项

### v0.2.0 (2024-10-14)
- ✨ **新增**: ReAct Agent智能研究代理
- ✨ **新增**: GLM-4.5-air LLM集成
- ✨ **新增**: Google学术搜索工具
- ✨ **新增**: Jina网页访问工具
- ✨ **新增**: Python沙箱工具集成

### v0.1.0 (2024-10-13)
- 🎉 **初始版本**: 基础Google搜索工具
- 🔧 **集成**: Qwen-Agent框架

## 🗺️ 开发路线图

### 即将推出
- 🤖 **多模态支持**: 图像理解和生成
- 📊 **数据可视化**: 自动生成图表和报告
- 🔍 **高级搜索**: 语义搜索和知识图谱
- 💾 **本地存储**: 研究结果持久化

### 长期规划
- 🧠 **自定义Agent**: 用户可训练的专用代理
- 🔗 **API集成**: 更多第三方服务集成
- 📱 **Web界面**: 图形化用户界面
- ⚡ **性能优化**: 缓存和并发处理

## 📄 许可证

本项目采用 [MIT 许可证](LICENSE)。

## 🤝 贡献

我们欢迎各种形式的贡献！

- **Bug修复**: 修复现有功能问题
- **新功能**: 添加新的工具或功能
- **文档**: 改进文档和示例
- **测试**: 增加测试覆盖率
- **代码质量**: 代码重构和优化

## 📞 联系方式

- **项目主页**: [https://github.com/DennyChui/ResearchAgent](https://github.com/DennyChui/ResearchAgent)
- **问题反馈**: [GitHub Issues](https://github.com/DennyChui/ResearchAgent/issues)
- **功能建议**: [GitHub Discussions](https://github.com/DennyChui/ResearchAgent/discussions)

## 🙏 致谢

感谢以下开源项目和服务：
- [Qwen-Agent](https://github.com/QwenLM/Qwen-Agent) - AI Agent框架
- [Serper](https://serper.dev/) - 搜索API服务
- [Jina AI](https://jina.ai/) - 网页内容提取
- [智谱AI](https://open.bigmodel.cn/) - GLM模型服务

---

**🎉 让 ResearchAgent 成为您的智能研究助手！**
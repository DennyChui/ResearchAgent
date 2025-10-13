GLM-4.5-Air LLM 配置信息：

模型配置：
- model: glm-4.5-air
- model_server: https://open.bigmodel.cn/api/paas/v4  
- api_key: 69b6cf3268474acf8c3d0d1898faee85.YNWhmxkqgoDQj67n
- model_type: openai_compat

API特性：
- 支持OpenAI兼容接口
- 基于智谱AI的GLM-4.5-Air模型
- 适合轻量级推理任务

使用方式：
在qwen_agent中配置为：
llm_cfg = {
    'model': 'glm-4.5-air',
    'model_server': 'https://open.bigmodel.cn/api/paas/v4',
    'api_key': '69b6cf3268474acf8c3d0d1898faee85.YNWhmxkqgoDQj67n',
    'model_type': 'openai_compat'
}
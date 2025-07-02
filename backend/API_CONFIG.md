# API配置说明

本系统支持三种不同的LLM API配置，用户可以在前端选择使用不同的模型和API服务。

## 配置选项

### API1: OpenAI API
- **模型名称**: GPT-4o-mini
- **描述**: OpenAI官方API
- **环境变量**:
  - `OPENAI_API_KEY`: OpenAI API密钥
  - `OPENAI_API_BASE`: OpenAI API基础URL (可选，默认为 https://api.openai.com/v1)

### API2: Anthropic Claude API
- **模型名称**: Deepseek-r1:70b
- **描述**: Anthropic Claude API
- **环境变量**:
  - `ANTHROPIC_API_KEY`: Anthropic API密钥

### API3: Google Gemini API
- **模型名称**: Qwen/QwQ-32B
- **描述**: Google Gemini API
- **环境变量**:
  - `GOOGLE_API_KEY`: Google API密钥

## 环境变量配置

在 `backend/.env` 文件中配置以下环境变量：

```bash
# OpenAI API配置 (api1)
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_API_BASE=https://api.openai.com/v1

# Anthropic Claude API配置 (api2)
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Google Gemini API配置 (api3)
GOOGLE_API_KEY=your_google_api_key_here

# 服务器配置
HOST=0.0.0.0
PORT=2024
```

## 使用方法

1. 在前端界面中选择对应的API配置
2. 系统会根据选择的配置自动使用相应的LLM服务
3. 每个API配置都有对应的模型和参数设置

## 注意事项

- 确保配置了正确的API密钥
- 不同API的模型名称和参数可能不同
- 建议在生产环境中使用环境变量而不是硬编码
- 可以根据需要添加更多的API配置选项 
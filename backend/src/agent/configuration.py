import os
from typing import Any, Optional
from dataclasses import dataclass

from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI


@dataclass
class Configuration:
    """Configuration for the agent."""
    
    # 论文Framework配置
    framework_refinement_loops: int = 2
    include_few_shot_examples: bool = True
    max_framework_length: int = 3000
    
    # API配置
    openai_api_key: Optional[str] = None
    openai_api_base: Optional[str] = None
    gemini_api_key: Optional[str] = None



def get_llm_by_config(api_config: str, model: str):
    """根据API配置获取对应的LLM实例"""
    if api_config == "api1":
        # OpenAI API
        return ChatOpenAI(
            model=model,
            temperature=0.7,
            openai_api_base=os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1"),
            openai_api_key=os.getenv("OPENAI_API_KEY"),
        )
    elif api_config == "api2":
        # Anthropic Claude API
        return ChatAnthropic(
            model=model,
            temperature=0.7,
            anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
        )
    elif api_config == "api3":
        # Google Gemini API
        return ChatGoogleGenerativeAI(
            model=model,
            temperature=0.7,
            google_api_key=os.getenv("GOOGLE_API_KEY"),
        )
    else:
        # 默认使用OpenAI
        return ChatOpenAI(
            model=model,
            temperature=0.7,
            openai_api_base=os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1"),
            openai_api_key=os.getenv("OPENAI_API_KEY"),
        )

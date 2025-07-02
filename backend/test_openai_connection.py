#!/usr/bin/env python3
"""
测试OpenAI API连接的脚本
"""

import os
import sys
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

def test_openai_connection():
    """测试OpenAI API连接"""
    load_dotenv()
    
    # 获取环境变量
    api_key = os.getenv("OPENAI_API_KEY")
    api_base = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
    
    if not api_key:
        print("❌ 错误: 未设置 OPENAI_API_KEY 环境变量")
        print("请在 .env 文件中设置您的 OpenAI API Key")
        return False
    
    print(f"🔧 配置信息:")
    print(f"   API Key: {api_key[:8]}...{api_key[-4:]}")
    print(f"   API Base: {api_base}")
    print()
    
    try:
        # 创建OpenAI客户端
        llm = ChatOpenAI(
            model="deepseek-r1:70b",
            temperature=0,
            max_retries=1,
            api_key=api_key,
            base_url=api_base,
        )
        
        print("🔄 正在测试API连接...")
        
        # 发送测试请求
        response = llm.invoke("请回复'连接成功'")
        
        print("✅ 连接成功!")
        print(f"   模型响应: {response.content}")
        return True
        
    except Exception as e:
        print("❌ 连接失败!")
        print(f"   错误信息: {str(e)}")
        print()
        print("🔍 可能的解决方案:")
        print("   1. 检查 OPENAI_API_KEY 是否正确")
        print("   2. 检查 OPENAI_API_BASE 是否正确")
        print("   3. 检查网络连接")
        print("   4. 检查API配额是否充足")
        return False

def main():
    """主函数"""
    print("🚀 OpenAI API 连接测试")
    print("=" * 50)
    
    success = test_openai_connection()
    
    print("=" * 50)
    if success:
        print("🎉 测试通过! 您可以开始使用论文Framework生成器了。")
        sys.exit(0)
    else:
        print("💥 测试失败! 请检查配置后重试。")
        sys.exit(1)

if __name__ == "__main__":
    main() 
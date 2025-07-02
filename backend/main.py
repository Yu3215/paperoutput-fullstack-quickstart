from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langchain_core.messages import HumanMessage, AIMessage
from langgraph_sdk import RemoteRunnable
from paper_framework.graph import paper_framework_app
import os

app = FastAPI()

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Paper Framework API is running"}

@app.post("/paper-framework/stream")
async def stream_paper_framework(
    messages: list,
    paper_topic: str,
    methodology: str,
    journal_requirements: str,
    framework_refinement_loops: int,
    framework_model: str,
    api_config: str
):
    """流式生成论文框架"""
    
    # 初始化状态
    initial_state = {
        "messages": messages,
        "paper_topic": paper_topic,
        "methodology": methodology,
        "journal_requirements": journal_requirements,
        "framework_refinement_loops": framework_refinement_loops,
        "framework_model": framework_model,
        "api_config": api_config,
        "current_framework": "",
        "refinement_count": 0,
        "final_framework": ""
    }
    
    # 创建流式响应
    async def generate():
        async for event in paper_framework_app.astream(initial_state):
            if "generate_framework" in event:
                yield f"data: {event['generate_framework']}\n\n"
            elif "refine_framework" in event:
                yield f"data: {event['refine_framework']}\n\n"
            elif "validate_framework" in event:
                yield f"data: {event['validate_framework']}\n\n"
            elif "messages" in event:
                # 发送最新的消息
                latest_message = event["messages"][-1]
                if isinstance(latest_message, AIMessage):
                    yield f"data: {latest_message.content}\n\n"
    
    return generate()

@app.post("/paper-framework/invoke")
async def invoke_paper_framework(
    messages: list,
    paper_topic: str,
    methodology: str,
    journal_requirements: str,
    framework_refinement_loops: int,
    framework_model: str,
    api_config: str
):
    """同步调用生成论文框架"""
    
    # 初始化状态
    initial_state = {
        "messages": messages,
        "paper_topic": paper_topic,
        "methodology": methodology,
        "journal_requirements": journal_requirements,
        "framework_refinement_loops": framework_refinement_loops,
        "framework_model": framework_model,
        "api_config": api_config,
        "current_framework": "",
        "refinement_count": 0,
        "final_framework": ""
    }
    
    # 执行工作流
    result = paper_framework_app.invoke(initial_state)
    
    return {
        "messages": result["messages"],
        "final_framework": result["final_framework"],
        "refinement_count": result["refinement_count"]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=2024) 
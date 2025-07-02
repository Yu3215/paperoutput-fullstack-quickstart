# mypy: disable - error - code = "no-untyped-def,misc"
import pathlib
from fastapi import FastAPI, Response
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from langchain_core.messages import HumanMessage, AIMessage
from agent.graph import paper_framework_graph

# Define the FastAPI app
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

# 使用sse技术，前端可以接受生成过程的每个步骤
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
        async for event in paper_framework_graph.astream(initial_state):
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
    result = paper_framework_graph.invoke(initial_state)
    
    return {
        "messages": result["messages"],
        "final_framework": result["final_framework"],
        "refinement_count": result["refinement_count"]
    }


def create_frontend_router(build_dir="../frontend/dist"):
    """Creates a router to serve the React frontend.

    Args:
        build_dir: Path to the React build directory relative to this file.

    Returns:
        A Starlette application serving the frontend.
    """
    build_path = pathlib.Path(__file__).parent.parent.parent / build_dir

    if not build_path.is_dir() or not (build_path / "index.html").is_file():
        print(
            f"WARN: Frontend build directory not found or incomplete at {build_path}. Serving frontend will likely fail."
        )
        # Return a dummy router if build isn't ready
        from starlette.routing import Route

        async def dummy_frontend(request):
            return Response(
                "Frontend not built. Run 'npm run build' in the frontend directory.",
                media_type="text/plain",
                status_code=503,
            )

        return Route("/{path:path}", endpoint=dummy_frontend)

    return StaticFiles(directory=build_path, html=True)


# Mount the frontend under /app to not conflict with the LangGraph API routes
app.mount(
    "/app",
    create_frontend_router(),
    name="frontend",
)

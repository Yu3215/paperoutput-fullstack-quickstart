
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage
from langgraph.graph import StateGraph, START, END
from langchain_core.prompts import ChatPromptTemplate

from agent.state import PaperFrameworkState
from agent.configuration import get_llm_by_config
from agent.prompts import (
    framework_generation_instructions,
    framework_refinement_instructions,
    framework_validation_instructions,
)
from agent.tools_and_schemas import get_journal_examples

load_dotenv()


def generate_framework(state: PaperFrameworkState) -> PaperFrameworkState:
    """生成初始理论框架"""
    # 获取期刊示例
    journal_examples = get_journal_examples(state["journal_requirements"])
    
    # 构建提示词
    prompt = ChatPromptTemplate.from_messages([
        ("system", framework_generation_instructions),
        ("human", "请为以下研究生成理论框架：\n\n研究主题：{paper_topic}\n研究方法：{methodology}\n目标期刊：{journal_requirements}")
    ])
    
    # 根据API配置获取LLM
    llm = get_llm_by_config(state["api_config"], state["framework_model"])
    
    # 生成框架
    chain = prompt | llm
    response = chain.invoke({
        "paper_topic": state["paper_topic"],
        "methodology": state["methodology"],
        "journal_requirements": state["journal_requirements"],
        "journal_examples": journal_examples
    })
    
    framework = response.content
    
    # 更新状态
    new_messages = list(state["messages"]) + [
        HumanMessage(content=f"请为我的研究生成理论框架：\n主题：{state['paper_topic']}\n方法：{state['methodology']}\n期刊：{state['journal_requirements']}"),
        AIMessage(content=framework)
    ]
    
    return {
        **state,
        "messages": new_messages,
        "current_framework": framework,
        "refinement_count": 0
    }


def refine_framework(state: PaperFrameworkState) -> PaperFrameworkState:
    """精炼理论框架"""
    if state["refinement_count"] >= state["framework_refinement_loops"]:
        return state
    
    # 获取期刊示例
    journal_examples = get_journal_examples(state["journal_requirements"])
    
    # 构建精炼提示词
    prompt = ChatPromptTemplate.from_messages([
        ("system", framework_refinement_instructions),
        ("human", "请对以下理论框架进行精炼改进：\n\n研究主题：{paper_topic}\n研究方法：{methodology}\n目标期刊：{journal_requirements}\n当前框架：{current_framework}")
    ])
    
    # 根据API配置获取LLM
    llm = get_llm_by_config(state["api_config"], state["framework_model"])
    
    # 精炼框架
    chain = prompt | llm
    response = chain.invoke({
        "paper_topic": state["paper_topic"],
        "methodology": state["methodology"],
        "journal_requirements": state["journal_requirements"],
        "current_framework": state["current_framework"],
        "journal_examples": journal_examples
    })
    
    refined_framework = response.content
    
    # 更新状态
    new_messages = list(state["messages"]) + [
        HumanMessage(content="请对当前框架进行精炼改进"),
        AIMessage(content=refined_framework)
    ]
    
    return {
        **state,
        "messages": new_messages,
        "current_framework": refined_framework,
        "refinement_count": state["refinement_count"] + 1
    }


def validate_framework(state: PaperFrameworkState) -> PaperFrameworkState:
    """验证框架质量"""
    # 获取期刊示例
    journal_examples = get_journal_examples(state["journal_requirements"])
    
    # 构建验证提示词
    prompt = ChatPromptTemplate.from_messages([
        ("system", framework_validation_instructions),
        ("human", "请评估以下理论框架的质量：\n\n研究主题：{paper_topic}\n研究方法：{methodology}\n目标期刊：{journal_requirements}\n理论框架：{current_framework}")
    ])
    
    # 根据API配置获取LLM
    llm = get_llm_by_config(state["api_config"], state["framework_model"])
    
    # 验证框架
    chain = prompt | llm
    response = chain.invoke({
        "paper_topic": state["paper_topic"],
        "methodology": state["methodology"],
        "journal_requirements": state["journal_requirements"],
        "current_framework": state["current_framework"],
        "journal_examples": journal_examples
    })
    
    validation_result = response.content
    
    # 更新状态
    new_messages = list(state["messages"]) + [
        HumanMessage(content="请评估当前框架的质量"),
        AIMessage(content=validation_result)
    ]
    
    return {
        **state,
        "messages": new_messages,
        "final_framework": state["current_framework"]
    }


def should_continue_refining(state: PaperFrameworkState) -> str:
    """决定是否继续精炼"""
    if state["refinement_count"] < state["framework_refinement_loops"]:
        return "refine"
    else:
        return "validate"


# 创建论文Framework生成图
def create_paper_framework_graph():
    """创建论文Framework生成的状态图"""
    workflow = StateGraph(PaperFrameworkState)
    
    # 添加节点
    workflow.add_node("generate_framework", generate_framework)
    workflow.add_node("refine_framework", refine_framework)
    workflow.add_node("validate_framework", validate_framework)
    
    # 设置入口点
    workflow.set_entry_point("generate_framework")
    
    # 添加条件边
    workflow.add_conditional_edges(
        "generate_framework",
        should_continue_refining,
        {
            "refine": "refine_framework",
            "validate": "validate_framework"
        }
    )
    
    workflow.add_conditional_edges(
        "refine_framework",
        should_continue_refining,
        {
            "refine": "refine_framework",
            "validate": "validate_framework"
        }
    )
    
    # 设置结束点
    workflow.add_edge("validate_framework", END)
    
    return workflow.compile()


# 创建图实例
paper_framework_graph = create_paper_framework_graph() 
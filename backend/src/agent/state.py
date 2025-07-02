from __future__ import annotations

from dataclasses import dataclass, field
from typing import TypedDict, List, Dict, Any

from langgraph.graph import add_messages
from typing_extensions import Annotated
from typing_extensions import Annotated

@dataclass(kw_only=True)


class PaperWritingState(TypedDict):
    messages: Annotated[list, add_messages]
    research_topic: str
    journal_requirements: Dict[str, Any]
    paper_outline: List[Dict[str, Any]]
    literature_review: List[Dict[str, Any]]
    methodology: Dict[str, Any]
    results: List[Dict[str, Any]]
    discussion: Dict[str, Any]
    conclusion: Dict[str, Any]
    references: List[Dict[str, Any]]
    current_section: str
    writing_progress: float
    quality_score: float
    revision_notes: List[str]
    final_paper: str


# 新增论文Framework生成相关状态
class PaperFrameworkState(TypedDict):
    messages: Annotated[list, add_messages]
    paper_topic: str
    methodology: str
    journal_requirements: str
    framework_refinement_loops: int
    framework_model: str
    api_config: str
    current_framework: str
    refinement_count: int
    final_framework: str


class FrameworkGenerationState(TypedDict):
    framework_content: str
    section_breakdown: dict[str, str]
    citations: list[dict]

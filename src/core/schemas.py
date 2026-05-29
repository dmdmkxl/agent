"""Shared Pydantic schemas."""

from typing import Literal

from pydantic import BaseModel, Field


class AgentOutput(BaseModel):
    task_type: Literal["chat", "qa", "search", "extract"] = Field(
        description="任务类型，例如 chat、qa、search、extract"
    )
    confidence: float = Field(
        ge=0,
        le=1,
        description="模型对本次判断的置信度，范围 0 到 1",
    )
    answer: str = Field(description="对用户输入的简洁回答")


class ToolDecision(BaseModel):
    need_tool: bool = Field(description="是否需要调用工具")
    tool_name: Literal["get_weather", "search_notes"] | None = Field(
        default=None,
        description="需要调用工具时选择的工具名",
    )
    tool_args: dict[str, str] = Field(
        default_factory=dict,
        description="工具参数，例如 city 或 keyword",
    )
    direct_answer: str = Field(
        default="",
        description="不需要调用工具时的直接回答",
    )

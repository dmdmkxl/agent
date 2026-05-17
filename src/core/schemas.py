"""Shared Pydantic schemas."""

from typing import Literal

from pydantic import BaseModel, Field


class AgentOutput(BaseModel):
    task_type: Literal["chat", "qa", "search", "extract"] = Field(
        description="任务类型，如 chat、qa、search、extract"
    )
    confidence: float = Field(
        ge=0,
        le=1,
        description="模型对本次判断的置信度，范围 0 到 1",
    )
    answer: str = Field(description="对用户输入的简洁回答")


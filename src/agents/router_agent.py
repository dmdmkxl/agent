"""Router agent implementation."""

from src.core.llm import get_client, get_model_name
from src.core.schemas import AgentOutput


ROUTER_SYSTEM_PROMPT = """
你是一个最小 Router Agent。

你的职责不是直接完成任务，而是判断用户输入属于哪一类任务。

请只输出 JSON 对象，字段必须包含：
- task_type: 只能是 chat、qa、search、extract 之一
- confidence: 0 到 1 之间的小数，表示你对分类的置信度
- answer: 用一句话说明你为什么这样分类

分类规则：
- chat: 闲聊、打招呼、表达情绪、开放式聊天
- qa: 用户提出可以直接回答的问题
- search: 用户需要查找最新信息、外部资料、网页或资料库
- extract: 用户要求总结、提取字段、解析文本、整理要点
"""


def route_task(user_input: str) -> AgentOutput:
    """Use the LLM to classify the user's task."""
    client = get_client()
    model = get_model_name()

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": ROUTER_SYSTEM_PROMPT},
            {"role": "user", "content": user_input},
        ],
        response_format={"type": "json_object"},
    )

    content = response.choices[0].message.content
    if not content:
        raise RuntimeError("Model returned empty content")

    return AgentOutput.model_validate_json(content)


def handle_chat(user_input: str) -> str:
    return f"这是聊天任务，我会用轻量方式回应：{user_input}"


def handle_qa(user_input: str) -> str:
    return f"这是问答任务，我会尝试直接回答：{user_input}"


def handle_search(user_input: str) -> str:
    return f"这是搜索任务。Day 2 先做路由占位，真实搜索会在后续工具阶段接入：{user_input}"


def handle_extract(user_input: str) -> str:
    return f"这是提取任务，我会从输入中提取或整理关键信息：{user_input}"


def dispatch_task(route_result: AgentOutput, user_input: str) -> str:
    """Dispatch the task to a simple handler based on task_type."""
    if route_result.task_type == "chat":
        return handle_chat(user_input)
    if route_result.task_type == "qa":
        return handle_qa(user_input)
    if route_result.task_type == "search":
        return handle_search(user_input)
    if route_result.task_type == "extract":
        return handle_extract(user_input)

    raise ValueError(f"Unsupported task_type: {route_result.task_type}")


def run_router_agent(user_input: str) -> tuple[AgentOutput, str]:
    route_result = route_task(user_input)
    final_answer = dispatch_task(route_result, user_input)
    return route_result, final_answer


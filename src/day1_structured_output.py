"""Day 1: structured output examples."""

from openai import AuthenticationError

from src.core.llm import get_client, get_model_name
from src.core.schemas import AgentOutput


SYSTEM_PROMPT = """
你是一个最小 Agent 原型中的任务分析助手。

你的职责：
1. 理解用户输入的意图
2. 给出任务类型 task_type
3. 给出 0 到 1 的 confidence
4. 给出简洁 answer

要求：
- 只输出 JSON 对象
- JSON 必须包含 task_type、confidence、answer
- confidence 取值在 0 到 1 之间
- task_type 必须从以下类型中选择：chat、qa、search、extract
- answer 尽量简洁清楚
"""


def run_agent(user_input: str) -> AgentOutput:
    client = get_client()
    model = get_model_name()

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input},
        ],
        response_format={"type": "json_object"},
    )

    content = response.choices[0].message.content
    if not content:
        raise RuntimeError("Model returned empty content")

    return AgentOutput.model_validate_json(content)


def main() -> None:
    user_input = input("请输入一句话：").strip()

    try:
        result = run_agent(user_input)
    except AuthenticationError as exc:
        raise RuntimeError(
            "认证失败：请检查 .env 里的 OPENAI_API_KEY 是否有效，"
            "以及 OPENAI_BASE_URL 是否指向对应服务商。"
        ) from exc

    print("\n结构化输出结果：")
    print(result.model_dump_json(indent=2))


if __name__ == "__main__":
    main()


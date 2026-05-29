"""Day 4: minimal single agent tool loop."""

from openai import AuthenticationError

from src.core.llm import get_client, get_model_name
from src.core.schemas import ToolDecision
from src.day3_tools import get_weather, search_notes


TOOL_DECISION_PROMPT = """
你是一个最小 Single Agent。
你的任务是判断用户问题是否需要调用工具，并输出 JSON。

可用工具：
1. get_weather
   - 作用：查询城市天气
   - 参数：city，支持北京、上海、深圳
2. search_notes
   - 作用：搜索本地 notes 目录里的学习笔记
   - 参数：keyword，表示要搜索的关键词

输出要求：
- 只能输出 JSON 对象
- JSON 字段必须包含 need_tool、tool_name、tool_args、direct_answer
- 如果需要工具：
  - need_tool 为 true
  - tool_name 是 get_weather 或 search_notes
  - tool_args 填入工具参数
  - direct_answer 为空字符串
- 如果不需要工具：
  - need_tool 为 false
  - tool_name 为 null
  - tool_args 为空对象
  - direct_answer 写出可以直接给用户的回答
"""


FINAL_ANSWER_PROMPT = """
你是一个学习 AI Agent 开发的导师。
请根据用户原始问题和工具返回结果，用中文给出简洁、自然的最终回答。
不要编造工具结果里没有的信息。
"""


def decide_tool(user_input: str) -> ToolDecision:
    """Ask the LLM whether a tool is needed."""
    client = get_client()
    model = get_model_name()

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": TOOL_DECISION_PROMPT},
            {"role": "user", "content": user_input},
        ],
        response_format={"type": "json_object"},
    )

    content = response.choices[0].message.content
    if not content:
        raise RuntimeError("Model returned empty content")

    return ToolDecision.model_validate_json(content)


def execute_tool(decision: ToolDecision) -> str:
    """Run the Python tool selected by the LLM."""
    if not decision.need_tool:
        return ""

    if decision.tool_name == "get_weather":
        city = decision.tool_args.get("city")
        if not city:
            return "工具调用失败：缺少参数 city"
        return get_weather(city)

    if decision.tool_name == "search_notes":
        keyword = decision.tool_args.get("keyword")
        if not keyword:
            return "工具调用失败：缺少参数 keyword"
        results = search_notes(keyword)
        if not results:
            return f"没有找到包含关键词 {keyword} 的笔记"
        return "找到这些笔记：" + "、".join(results)

    return f"工具调用失败：不支持的工具 {decision.tool_name}"


def summarize_with_tool_result(user_input: str, tool_result: str) -> str:
    """Ask the LLM to write the final answer after observing the tool result."""
    client = get_client()
    model = get_model_name()

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": FINAL_ANSWER_PROMPT},
            {
                "role": "user",
                "content": f"用户问题：{user_input}\n工具结果：{tool_result}",
            },
        ],
    )

    content = response.choices[0].message.content
    if not content:
        raise RuntimeError("Model returned empty content")

    return content


def run_single_agent_loop(user_input: str) -> tuple[ToolDecision, str, str]:
    """Run one complete tool loop."""
    decision = decide_tool(user_input)

    if not decision.need_tool:
        return decision, "", decision.direct_answer

    tool_result = execute_tool(decision)
    final_answer = summarize_with_tool_result(user_input, tool_result)
    return decision, tool_result, final_answer


def main() -> None:
    user_input = input("请输入一句话：").strip()

    try:
        decision, tool_result, final_answer = run_single_agent_loop(user_input)
    except AuthenticationError as exc:
        raise RuntimeError(
            "认证失败：请检查 .env 里的 OPENAI_API_KEY 是否有效，"
            "以及 OPENAI_BASE_URL 是否指向 DeepSeek 等对应服务商。"
        ) from exc

    print("\nAgent 工具决策：")
    print(decision.model_dump_json(indent=2))

    if tool_result:
        print("\n工具返回结果：")
        print(tool_result)

    print("\n最终回答：")
    print(final_answer)


if __name__ == "__main__":
    main()

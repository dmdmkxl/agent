"""Day 5: minimal chat memory loop."""

from openai import AuthenticationError

from src.core.llm import get_client, get_model_name


SYSTEM_PROMPT = """
你是一个学习 AI Agent 开发的中文导师。
请基于当前对话上下文回答用户问题。
如果用户说“刚才”“上一个”“再短一点”“换个说法”，你需要结合最近对话理解指代。
回答要简洁、清楚，不要编造上下文里没有的信息。
"""

MAX_TURNS = 5


def trim_messages(messages: list[dict[str, str]], max_turns: int = MAX_TURNS) -> list[dict[str, str]]:
    """Keep the system message and the most recent user/assistant turns."""
    system_messages = messages[:1]
    chat_messages = messages[1:]
    max_chat_messages = max_turns * 2

    if len(chat_messages) <= max_chat_messages:
        return messages

    return system_messages + chat_messages[-max_chat_messages:]


def chat_once(messages: list[dict[str, str]], user_input: str) -> tuple[str, list[dict[str, str]]]:
    """Append one user message, ask the model, then append the assistant reply."""
    client = get_client()
    model = get_model_name()

    request_messages = messages + [{"role": "user", "content": user_input}]

    response = client.chat.completions.create(
        model=model,
        messages=request_messages,
    )

    assistant_reply = response.choices[0].message.content
    if not assistant_reply:
        raise RuntimeError("Model returned empty content")

    messages = request_messages + [{"role": "assistant", "content": assistant_reply}]
    messages = trim_messages(messages)

    return assistant_reply, messages


def main() -> None:
    messages: list[dict[str, str]] = [
        {"role": "system", "content": SYSTEM_PROMPT.strip()},
    ]

    print("Day 5: chat memory")
    print("输入 exit 退出。")

    while True:
        user_input = input("\n你：").strip()
        if user_input.lower() in {"exit", "quit"}:
            print("已退出。")
            break

        if not user_input:
            continue

        try:
            assistant_reply, messages = chat_once(messages, user_input)
        except AuthenticationError as exc:
            raise RuntimeError(
                "认证失败：请检查 .env 里的 OPENAI_API_KEY 是否有效，"
                "以及 OPENAI_BASE_URL 是否指向 DeepSeek 等对应服务商。"
            ) from exc

        print(f"\nAgent：{assistant_reply}")
        print(f"\n[debug] 当前保存消息数：{len(messages)}，最多保留最近 {MAX_TURNS} 轮。")


if __name__ == "__main__":
    main()


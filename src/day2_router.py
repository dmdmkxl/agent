"""Day 2: router examples."""

from openai import AuthenticationError

from src.agents.router_agent import run_router_agent


def main() -> None:
    user_input = input("请输入一句话：").strip()

    try:
        route_result, final_answer = run_router_agent(user_input)
    except AuthenticationError as exc:
        raise RuntimeError(
            "认证失败：请检查 .env 里的 OPENAI_API_KEY 是否有效，"
            "以及 OPENAI_BASE_URL 是否指向 DeepSeek 等对应服务商。"
        ) from exc

    print("\nRouter 判断结果：")
    print(route_result.model_dump_json(indent=2))

    print("\n最终处理结果：")
    print(final_answer)


if __name__ == "__main__":
    main()


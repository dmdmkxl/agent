"""Day 6: logging examples."""

import json
from pathlib import Path
from src.day4_single_agent_loop import (
    decide_tool,
    execute_tool,
    summarize_with_tool_result,
)


def append_trace(trace: dict, log_path: str = "logs/day6_traces.jsonl") -> None:
    path = Path(log_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    line = json.dumps(trace, ensure_ascii=False)

    with path.open("a", encoding="utf-8") as file:
        file.write(line + "\n")

def build_trace(
    user_input: str,
    tool_decision: dict | None = None,
    tool_args: dict | None = None,
    tool_result: str | None = None,
    final_output: str | None = None,
    error: str | None = None,
) -> dict:
    return {
        "user_input": user_input,
        "tool_decision": tool_decision,
        "tool_args": tool_args or {},
        "tool_result": tool_result,
        "final_output": final_output,
        "error": error,
    }

def run_single_agent_loop_with_trace(user_input: str, log_path: str = "logs/day6_traces.jsonl") -> tuple:
    # 初始化
    decision = None
    tool_result = None
    final_answer = None
    error = None

    try:
        decision = decide_tool(user_input)
        if decision.need_tool:
            tool_result = execute_tool(decision)
            final_answer = summarize_with_tool_result(user_input, tool_result)
        else:
            final_answer = decision.direct_answer
    except Exception as exc:
        error = str(exc)

    finally:
        trace = build_trace(
            user_input=user_input,
            tool_decision=decision.model_dump() if decision else None,
            tool_args=decision.tool_args if decision else None,
            tool_result=tool_result,
            final_output=final_answer,
            error=error,
        )
        append_trace(trace, log_path)
    return decision, tool_result, final_answer, error, trace

def main() -> None:
    print("Day 6: logging")
    log_path = "logs/day6_traces.jsonl"
    user_input = input("请输入一句话：").strip()

    decision, tool_result, final_answer, error, trace = run_single_agent_loop_with_trace(user_input, log_path)
    if decision:
        print("\nAgent 工具决策：")
        print(decision.model_dump_json(indent=2))

    if tool_result:
        print("\n工具返回结果：")
        print(tool_result)

    print("\n最终回答：")
    print(final_answer)
if __name__ == "__main__":
    main()


"""Day 3: tool calling examples."""

from pathlib import Path


def get_weather(city: str) -> str:
    weather_data = {
        "北京": "晴，26°C",
        "上海": "多云，24°C",
        "深圳": "小雨，29°C",
    }

    if city in weather_data:
        return f"{city}：{weather_data[city]}"

    return f"暂时没有 {city} 的天气数据"


def is_weather_request(user_input: str) -> bool:
    weather_keywords = ["天气", "多少度", "气温", "冷不冷", "热不热"]
    return any(keyword in user_input for keyword in weather_keywords)


def extract_city(user_input: str) -> str | None:
    supported_cities = ["北京", "上海", "深圳"]

    for city in supported_cities:
        if city in user_input:
            return city

    return None


def handle_weather_question(user_input: str) -> str:
    if not is_weather_request(user_input):
        return "这不是天气查询，不调用天气工具。"

    city = extract_city(user_input)
    if city is None:
        return "你想查询哪个城市的天气？"

    return get_weather(city)


def search_notes(keyword: str) -> list[str]:
    notes_dir = Path("notes")
    results: list[str] = []

    for path in notes_dir.glob("*.md"):
        text = path.read_text(encoding="utf-8", errors="ignore")
        if keyword.lower() in text.lower():
            results.append(path.name)

    return results


def is_notes_search_request(user_input: str) -> bool:
    scope_keywords = ["笔记", "notes"]
    action_keywords = ["查一下", "搜一下", "搜索", "有没有"]

    has_scope = any(keyword in user_input for keyword in scope_keywords)
    has_action = any(keyword in user_input for keyword in action_keywords)

    return has_scope and has_action


def choose_tool(user_input: str) -> str | None:
    if is_weather_request(user_input) and extract_city(user_input) is not None:
        return "get_weather"

    if is_notes_search_request(user_input):
        return "search_notes"

    return None


def main() -> None:
    print("Day 3: tools")


if __name__ == "__main__":
    main()

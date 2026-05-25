# Day 3 Notes

## 1. 今天学了什么

今天的主题是 Tool Calling，也就是让 Agent 不只是生成文本，而是能在合适的时候调用程序里的工具函数。

Day 1 重点是结构化输出：

```text
用户输入 -> 模型输出结构化 JSON
```

Day 2 重点是任务路由：

```text
用户输入 -> 判断 task_type -> 分发到不同 handler
```

Day 3 开始进入工具调用：

```text
用户输入 -> 判断是否需要工具 -> 准备参数 -> 调用工具 -> 返回工具结果
```

## 2. Tool 是什么

Tool 本质上是 Agent 可以调用的一个函数能力。

例如：

```python
get_weather("北京")
```

它和 prompt、最终回答不是一回事：

- prompt 是给模型看的行为说明
- tool 是程序真正执行的函数能力
- 最终回答是给用户看的自然语言结果

今天写的两个本地假工具是：

```python
get_weather(city: str) -> str
search_notes(keyword: str) -> list[str]
```

## 3. 工具调用的最小流程

一个最小工具调用流程可以拆成五步：

```text
1. 判断意图
2. 提取参数
3. 校验参数
4. 执行工具
5. 处理工具结果
```

天气工具的例子：

```text
用户输入：北京今天多少度？
判断意图：这是天气查询
提取参数：city = 北京
校验参数：city 不为空，并且是支持城市
执行工具：get_weather("北京")
工具结果：北京：晴，26°C
```

## 4. 为什么工具参数要严格约束

工具通常是固定程序，不是大模型。

例如 `get_weather(city: str)` 期待的是一个城市名，而不是一整句自然语言：

```python
get_weather("北京")
```

如果让模型自由构造参数，可能会传入：

```python
get_weather("帮我查一下北京今天多少度，顺便建议穿什么")
```

这样会带来几个问题：

- 工具接口不匹配，容易执行失败
- 同一个任务每次参数不同，稳定性差
- 调试困难，不知道是模型错了还是工具错了
- 如果工具有权限或副作用，可能带来安全风险

所以更可靠的原则是：

```text
模型可以建议调用什么工具、传什么参数；
程序必须校验参数，再决定是否真正执行工具。
```

## 5. ToolSpec / ToolCall / ToolResult

今天区分了三个概念。

### ToolSpec

ToolSpec 是工具说明书，描述当前系统有哪些工具可用。

它通常包含：

```text
工具名
工具描述
参数名
参数类型
参数说明
```

例如：

```text
name: search_notes
description: 搜索本地 notes 笔记中是否包含某个关键词
parameters:
  keyword: str
```

### ToolCall

ToolCall 是一次工具调用请求。

它描述这一次是否要调用工具、调用哪个工具、传什么参数。

例如：

```text
need_tool = true
tool_name = "search_notes"
arguments = {"keyword": "DeepSeek"}
reason = "用户询问 notes 里是否提到 DeepSeek"
```

### ToolResult

ToolResult 是工具实际执行后的结果。

例如：

```text
["day1_notes.md", "day2_notes.md"]
```

最终回答要基于 ToolResult 组织，而不是把 ToolResult 和最终回答混在一起。

## 6. 今天手写的规则版逻辑

天气工具链路：

```text
is_weather_request(user_input)
extract_city(user_input)
handle_weather_question(user_input)
get_weather(city)
```

笔记搜索工具链路：

```text
is_notes_search_request(user_input)
search_notes(keyword)
choose_tool(user_input)
```

规则版的好处是简单、稳定、容易理解。

规则版的局限是覆盖不全，容易被自然语言变化影响。

例如：

```text
天气这个词是什么意思？
```

它包含“天气”，但并不是天气查询。

真实工程中，更常见的做法是：

```text
LLM 负责整体语义判断和参数抽取；
程序负责参数校验和工具执行。
```

## 7. 今日复盘

今天最重要的收获：

- Tool 是可调用函数，不是 prompt，也不是最终回答
- Tool Calling 不是直接让模型执行函数，而是模型或规则生成调用计划，程序执行工具
- 工具调用前必须做参数校验
- ToolSpec 是工具说明书
- ToolCall 是一次调用请求
- ToolResult 是工具执行结果
- 工具结果只是 Agent 后续回答的材料，不等于最终回答

下一步可以把 `choose_tool()` 从只返回工具名，升级成返回结构化 ToolCall：

```python
{
    "need_tool": True,
    "tool_name": "search_notes",
    "arguments": {"keyword": "DeepSeek"},
    "reason": "用户询问 notes 里是否提到 DeepSeek",
}
```

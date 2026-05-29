# Day 4 Notes

## 1. 今天学了什么

今天的主题是完整 Tool Loop，也就是让 Agent 形成一个闭环：

```text
用户输入
-> LLM 判断是否需要工具
-> 如果需要，LLM 选择工具并提取参数
-> Python 程序执行工具函数
-> 工具结果返回给 LLM
-> LLM 生成最终回答
```

Day 3 只是有了工具函数和简单规则判断；Day 4 开始，LLM 会参与“是否调用工具、调用哪个工具、参数是什么”的决策。

## 2. Tool Loop 和 Day 3 的区别

Day 3：

```text
用户输入 -> 程序规则判断 -> 调用工具 -> 返回工具结果
```

Day 4：

```text
用户输入 -> LLM 决策 -> 程序执行工具 -> LLM 根据工具结果总结
```

关键区别是：工具不是模型自己执行的，模型只负责输出结构化的行动决策；真正调用函数的是 Python 程序。

## 3. 本次新增的结构

新增了 `ToolDecision`：

```python
class ToolDecision(BaseModel):
    need_tool: bool
    tool_name: Literal["get_weather", "search_notes"] | None
    tool_args: dict[str, str]
    direct_answer: str
```

它用来约束模型输出，避免模型随意返回不稳定文本。

## 4. 最小 Single Agent Loop

核心函数是：

```python
run_single_agent_loop(user_input)
```

它内部分三步：

```text
decide_tool()
execute_tool()
summarize_with_tool_result()
```

如果 `need_tool` 为 false，就直接返回 `direct_answer`。

如果 `need_tool` 为 true，就执行工具，再让模型根据工具结果生成最终回答。

## 5. 今天遇到的环境问题

运行时一开始报错：

```text
ModuleNotFoundError: No module named 'openai'
```

原因不是项目没有安装 openai，而是运行时使用了 base Python：

```text
F:\anaconda3\python.exe
```

真正有依赖的是 agent 环境：

```text
F:\anaconda3\envs\agent\python.exe
```

以后运行项目时，要确认当前解释器和安装依赖的环境一致。

## 6. 今天遇到的编码问题

从 PowerShell 管道传入中文时，中文可能会变成问号：

```text
深圳天气怎么样？ -> ????????
```

这说明文本在进入 Python 前已经被终端编码破坏了。测试时可以用正常交互输入，或用 Unicode 转义绕开管道编码问题。

## 7. 我的理解

完整 Agent 不是“模型直接做所有事”，而是：

```text
模型负责决策和总结
程序负责执行真实动作
结构化输出负责连接两者
```

这是从普通 LLM 应用走向 Agent 的关键一步。

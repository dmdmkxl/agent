# Day 6 Notes

## 1. 今天学了什么

今天学了 Agent 调试能力中的重要一环：日志和 trace。

重点不是做复杂日志系统，而是理解 Agent 每次运行时，为什么要把关键节点的信息抽取出来，并保存成一条可复盘的 JSONL trace。

## 2. 为什么 Agent 需要日志和 trace

因为 Agent 的核心流程里包含 LLM 决策，LLM 可能幻觉，也可能选错工具、提取错参数、错误总结工具结果。

当 Agent 出错时，如果只有最终回答，就很难判断问题发生在哪一步。

日志和 trace 的作用是记录 Agent 运行流程中各关键节点的重要信息，让我们可以复盘：

```text
它看到了什么？
它决定了什么？
它调用了什么？
工具返回了什么？
最终输出了什么？
哪里报错了？
```

## 3. Day 6 和 Day 4/5 的关系

Day 4 实现了最小 Single Agent Tool Loop：

```text
decide_tool -> execute_tool -> summarize_with_tool_result
```

Day 6 主要是在 Day 4 的工具循环外面加 trace，让每一步都有记录，可以判断错误到底发生在决策、参数、工具执行，还是最终总结阶段。

Day 5 学的是 Chat Memory。Memory 会让 Agent 具备多轮上下文，但也会让调试更复杂。因为出错时需要判断：错误来自当前 user_input，还是来自历史 messages 的干扰。

所以 Day 6 可以理解为：给 Day 4/5 的 Agent 行为加上可观测能力。

## 4. 最小 JSONL trace 应该记录什么

最小 JSONL trace 应该记录：

```text
user_input
tool_decision
tool_args
tool_result
final_output
error
```

## 5. 每个字段为什么重要

user_input：记录用户原始输入。没有它，就无法判断后面的工具选择和最终回答是否符合用户真实问题。

tool_decision：记录 Agent 是否决定调用工具，以及调用哪个工具。它可以帮助判断错误是不是发生在模型决策阶段。

tool_args：记录传给工具的参数。工具选对了不代表参数正确，例如用户问深圳天气，但参数可能被提取成北京。

tool_result：记录工具真实返回结果。它可以帮助区分“工具返回错了”和“模型总结错了”。

final_output：记录最终给用户的回答。它是用户实际看到的内容，也是复盘时必须检查的结果。

error：记录程序运行中捕获到的真实异常，例如模型调用失败、JSON 解析失败、工具执行失败等。error 不应该主要依赖 LLM 自己判断，而应该来自程序的 try/except 或校验逻辑。

决策原因 reason 以后可以扩展，但今天的最小版本先只记录事实链路。

## 6. 今天实现的核心函数

今天实现了三个核心函数：

```text
build_trace
append_trace
run_single_agent_loop_with_trace
```

build_trace 用于把 user_input、tool_decision、tool_args、tool_result、final_output、error 统一组装成 trace dict。

append_trace 用于把 trace 追加写入 JSONL 文件，每一行是一条完整 JSON。

run_single_agent_loop_with_trace 是 Day 4 工具循环的包装函数。它不破坏原来的 run_single_agent_loop，而是在外层增加 trace 记录能力。

## 7. 成功路径、不使用工具路径、错误路径如何记录

成功路径、不使用工具路径、错误路径都应该走同一套 trace 管线：

```text
try:
    执行 Agent 主流程
except:
    记录 error
finally:
    build_trace
    append_trace
```

成功时，error 为 None。

不使用工具时，tool_result 可以为空，final_output 来自 direct_answer。

错误时，已经拿到的字段仍然保留，没有执行到的字段用 None 或空对象，error 记录异常信息。

## 8. 今天遇到的调试点

今天遇到的主要调试点：

```text
1. 不同路径如何保持同一 trace 结构
2. build_trace 应该放在 try/except 之后统一执行
3. append_trace 只负责写文件，不负责理解 Agent 流程
4. 中文在 IDE、终端、文件中的显示可能不同，乱码不一定代表文件真实内容损坏
```

## 9. 我的理解

Agent 也像普通程序一样会出错，也需要调试和维护。

但 Agent 的特殊之处在于，它中间有 LLM 决策。很多错误不能只靠看代码定位，必须记录模型当时做了什么决定、传了什么参数、工具返回了什么结果。

日志和 trace 的作用，就是为 Agent 的调试和维护提供依据。今天的关键理解是：

```text
Agent 不仅要能运行，还要能被复盘。
```

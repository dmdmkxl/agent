# Day 5 Notes

## 1. 今天学了什么

今天的主题是 Chat Memory，也就是让 Agent 支持多轮对话。

Day 4 的 Single Agent Tool Loop 每次只处理一轮输入：

```text
用户输入 -> LLM 决策 -> Python 执行 -> LLM 总结 -> 程序结束
```

Day 5 开始，程序会保存最近几轮对话，让下一次调用 LLM 时能看到前面的上下文：

```text
历史 messages
+ 当前用户输入
-> LLM 基于上下文回答
-> 保存 assistant 回复
-> 裁剪历史
-> 进入下一轮
```

## 2. 什么是 Chat Memory

Chat Memory 不是模型自己自动拥有的记忆，而是 Agent 程序保存并传给模型的上下文。

API 调用里的 LLM 更像一个无状态函数：

```text
输入 messages -> 输出 assistant 回复
```

如果程序没有把上一轮对话放进 `messages`，模型就不知道上一轮聊过什么。

## 3. 短期 Memory 和长期 Memory

短期 memory 保存当前会话里的最近上下文，适合处理：

```text
刚才那个结果换个说法
只保留重点
基于上一个结果继续
```

长期 memory 保存跨会话、长期稳定的信息，例如：

```text
用户偏好中文教学
用户正在学习 AI Agent
用户喜欢先提问再解释
```

Day 5 只实现短期 memory，不引入数据库、向量库或复杂框架。

## 4. 为什么不能把所有历史都塞进 messages

不能无限保存所有历史，主要原因是：

```text
1. 输入 token 会越来越多，成本上升
2. 上下文窗口有限，太长会放不下
3. 无关信息会干扰模型判断重点
4. 响应速度会变慢
5. 历史里的错误信息可能持续影响后续回答
```

所以 Day 5 使用最近 N 轮对话作为最小方案。

## 5. 本次实现的核心结构

新增文件：

```text
src/day5_chat_memory.py
```

核心变量：

```python
MAX_TURNS = 5
```

表示最多保留最近 5 轮对话。

一轮对话包含：

```text
1 条 user 消息 + 1 条 assistant 消息
```

所以最多保留：

```text
system + 5 轮 user/assistant = 11 条 messages
```

## 6. 核心函数

`trim_messages()` 负责裁剪历史：

```python
def trim_messages(messages, max_turns=MAX_TURNS):
    system_messages = messages[:1]
    chat_messages = messages[1:]
    max_chat_messages = max_turns * 2
    return system_messages + chat_messages[-max_chat_messages:]
```

它始终保留第一条 `system` 消息，只裁剪后面的聊天历史。

`chat_once()` 负责完成一轮对话：

```text
构造 request_messages
-> 调用 LLM
-> 得到 assistant 回复
-> user 和 assistant 成对写入 memory
-> 裁剪 messages
```

这样可以避免模型调用失败时，只保存 user 消息而没有 assistant 回复。

## 7. 今天的关键理解

Chat Memory 的本质是：

```text
由 Agent 程序管理 messages，把需要的历史上下文重新传给 LLM。
```

LLM 不是天然记住 API 调用历史。

ChatGPT 这类产品看起来有多轮上下文，是因为产品层帮用户保存、筛选并重新传入了历史消息。

## 8. 当前版本的限制

当前版本只保留最近 5 轮。

如果用户第 1 轮说：

```text
我叫小明。
```

后面聊了 20 轮以后再问：

```text
我叫什么？
```

当前 Agent 很可能答不上来，因为第 1 轮已经被裁剪掉了。

这说明短期 memory 适合最近上下文，不适合长期保存重要信息。

后续可以继续学习：

```text
摘要 memory
长期 memory
文件或数据库存储
把 Day 4 tool loop 接入多轮 memory
```

## 9. 验收方式

运行：

```powershell
F:\anaconda3\envs\agent\python.exe src/day5_chat_memory.py
```

测试 5 轮：

```text
我叫小明，正在学习 AI Agent。
我今天学习的是 chat memory。
刚才我说我叫什么？
把刚才那个答案换个更正式的说法。
只保留重点。
exit
```

如果 Agent 能记住“小明”，能理解“刚才那个答案”，并且连续 5 轮不明显自相矛盾，就说明 Day 5 最小版本通过。


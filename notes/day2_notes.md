# Day 2 Notes

## 1. Router Agent 是什么

Router Agent 像一个任务分诊台。它接收用户自然语言输入，先判断任务属于哪一类，再把任务交给对应的处理函数。

最小流程：

```text
用户输入 -> 判断 task_type -> 分发到 handler -> 输出最终结果
```

常见任务类型：

- `chat`: 闲聊、打招呼、开放式聊天
- `qa`: 可以直接回答的问题
- `search`: 需要查找外部资料或最新信息
- `extract`: 总结、提取字段、整理要点、解析文本

## 2. 和 Day 1 Structured Output 的关系

Day 1 解决的是：让模型稳定输出结构化 JSON，并用 Pydantic schema 校验。

Day 2 解决的是：把结构化输出真正用于程序控制流。

```text
Day 1: 自然语言 -> JSON -> AgentOutput
Day 2: 自然语言 -> AgentOutput -> 根据 task_type 分发任务
```

所以 `AgentOutput` 是数据结构，`route_task()` 是产生这个结构的动作，`dispatch_task()` 是使用这个结构做决策的动作。

## 3. 今天实现的核心函数

`route_task(user_input)`:

- 调用 LLM
- 判断用户输入的 `task_type`
- 返回 `AgentOutput(task_type, confidence, answer)`

`dispatch_task(route_result, user_input)`:

- 读取 `route_result.task_type`
- 根据任务类型调用不同 handler

`handle_chat()` / `handle_qa()` / `handle_search()` / `handle_extract()`:

- 目前是最小占位处理函数
- Day 2 重点是路由结构，不是实现所有工具能力

## 4. 当前最小 Router Agent 架构

```text
src/day2_router.py
  -> 命令行入口
  -> 接收用户输入
  -> 调用 run_router_agent()

src/agents/router_agent.py
  -> ROUTER_SYSTEM_PROMPT
  -> route_task()
  -> dispatch_task()
  -> handler 函数
```

## 5. DeepSeek OpenAI-compatible API 配置

使用 DeepSeek 时，`.env` 里需要让 API key、base_url、model 三者匹配。

```env
OPENAI_API_KEY=你的 DeepSeek API key
OPENAI_BASE_URL=https://api.deepseek.com
MODEL_NAME=deepseek-v4-pro
```

如果 API key 是 DeepSeek 的，但 `OPENAI_BASE_URL` 没有指向 DeepSeek，就可能出现认证失败或请求发错平台的问题。

## 6. 今天遇到的调试点

1. 默认 Python 环境没有安装 `openai`，需要使用项目的 conda `agent` 环境。
2. 当前环境使用 SOCKS 代理，缺少 `socksio` 会导致 OpenAI client 初始化失败。
3. PowerShell 管道传中文时可能出现编码问题，导致中文变成问号，从而影响模型判断。
4. 使用 `python -m src.day2_router` 比直接运行 `python src/day2_router.py` 更适合当前包结构。

推荐运行方式：

```powershell
F:\anaconda3\envs\agent\python.exe -m src.day2_router
```

## 7. Day 2 复盘

今天学到的关键点：

- Router Agent 的核心是“先判断任务类型，再分发任务”
- Structured output 可以作为路由决策的数据基础
- `task_type` 不只是展示字段，它可以驱动程序进入不同分支
- handler 在 Day 2 可以先做占位，后续再逐步接入真实工具
- 一个 Agent 系统可以从很小的控制流开始，而不是一开始就做复杂框架

下一步可以进入 Day 3：把某些 handler 升级成真实 tool，例如天气查询、笔记搜索或简单计算工具。

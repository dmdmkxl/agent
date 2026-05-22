# Day 1 Notes

## 1. 结构化输出是什么

结构化输出是让模型不要只返回适合人类阅读的自然语言，而是尽量按照固定格式返回数据，例如 JSON。

这样程序可以稳定读取字段，例如 `task_type`、`confidence`、`answer`，并继续执行后续逻辑。

Day 1 的核心流程：

```text
用户输入自然语言 -> prompt 引导模型输出 JSON -> Pydantic schema 校验 JSON -> 程序拿到可继续处理的 AgentOutput
```

## 2. 为什么需要 schema

schema 的目的是定义模型输出的标准结构，并在程序侧校验模型返回结果是否符合要求。

例如 `AgentOutput` 要求模型输出：

- `task_type`：任务类型
- `confidence`：置信度，范围 0 到 1
- `answer`：简洁回答

schema 有利于 Agent 稳定运行。模型可能会输出错误格式、少字段、字段类型错误，schema 可以及时拦住这些不合格结果。

## 3. prompt 和 schema 的区别

`SYSTEM_PROMPT` 是给模型看的，是模型输出前的任务说明和行为约束。它会告诉模型角色是什么、要做什么、应该按什么格式输出。

schema 是给程序看的，是模型输出后的验收标准。它负责检查模型输出是否符合结构化要求。

可以理解为：

```text
prompt = 事前引导模型
schema = 事后校验结果
```

在当前代码里，schema 主要负责程序侧校验，并不能保证模型一定会听话输出正确格式。不过在一些 OpenAI 官方结构化输出接口中，schema 也可能参与约束模型输出。

## 4. `.env` / API key / base_url 的作用

`.env` 是本地环境变量文件，用来存储运行项目需要的配置项，例如 API key、模型名、base_url 等。

API key 是调用模型服务的凭证，不能上传到 GitHub。

base_url 是模型服务的接口地址。使用 OpenAI-compatible API 时，需要确认：

- API key 是哪家平台的
- base_url 指向哪家平台
- model 名字是不是这家平台支持的
- 当前 SDK 接口是不是这家平台兼容的

## 5. 今天遇到的 401 报错原因和解决方法

今天的 401 报错原因是 API key 和 base_url 不匹配。

具体来说，我使用的是 DeepSeek 的 API key 和模型名，但一开始没有正确设置 `OPENAI_BASE_URL=https://api.deepseek.com`。程序使用 OpenAI SDK 时默认请求 OpenAI 官方接口，结果把 DeepSeek 的 key 发到了 OpenAI，所以 OpenAI 不认识这个 key，返回了 401 AuthenticationError。

解决方法是让 API key、base_url、model 三者匹配：

```env
OPENAI_API_KEY=你的 DeepSeek API key
OPENAI_BASE_URL=https://api.deepseek.com
MODEL_NAME=deepseek-v4-pro
```

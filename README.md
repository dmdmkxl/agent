# AI Agent 学习项目 / AI Agent Learning Project

这是一个面向 AI Agent 学习与实践的项目骨架，按阶段组织结构化输出、路由器、工具调用、单 Agent 循环、聊天记忆、日志、RAG、工作流、评测和应用入口等内容。

This is a staged AI Agent learning project scaffold covering structured output, routing, tool calling, single-agent loops, chat memory, logging, RAG, workflows, evaluation, and app entry points.

## 项目结构 / Project Layout

- `src/`：核心源码与每日练习示例 / Source code and daily examples
- `src/core/`：LLM、配置、提示词、Schema 和通用工具 / LLM helpers, config, prompts, schemas, and utilities
- `src/agents/`：路由、RAG、工作流等 Agent 实现 / Router, RAG, and workflow agents
- `src/tools/`：天气、笔记搜索、文档检索等工具 / Weather, note search, and document retrieval tools
- `src/rag/`：加载、切分、嵌入、索引和检索模块 / Loading, chunking, embedding, indexing, and retrieval
- `src/workflow/`：工作流状态、节点、边和图定义 / Workflow state, nodes, edges, and graph definitions
- `src/eval/`：评测器、指标和测试案例加载 / Evaluators, metrics, and case loading
- `src/app/`：FastAPI 与 Streamlit 应用入口 / FastAPI and Streamlit app entry points
- `data/`：原始数据、处理后数据、向量库和评测数据 / Raw, processed, vector store, and evaluation data
- `logs/`：trace、运行日志和错误日志 / Traces, run logs, and error logs
- `notes/`：学习笔记与复盘 / Learning notes and reviews
- `demo/`：截图、录屏和示例输入 / Screenshots, recordings, and sample inputs
- `tests/`：pytest 测试用例 / pytest test suite
- `scripts/`：环境配置、启动和索引构建脚本 / Setup, run, and index-building scripts

## 快速开始 / Quick Start

### 使用 venv

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

### 使用 Conda

```bash
conda env create -f environment.yml
conda activate agent
cp .env.example .env
```

## 常用命令 / Common Commands

启动 API 服务 / Run the API server:

```bash
uvicorn src.app.api:app --reload
```

启动 Streamlit Demo / Run the Streamlit demo:

```bash
streamlit run src/app/streamlit_app.py
```

运行测试 / Run tests:

```bash
pytest
```

## 学习路线 / Learning Path

1. `src/day1_structured_output.py`：结构化输出 / Structured output
2. `src/day2_router.py`：任务路由 / Task routing
3. `src/day3_tools.py`：工具调用 / Tool calling
4. `src/day4_single_agent_loop.py`：单 Agent 循环 / Single-agent loop
5. `src/day5_chat_memory.py`：聊天记忆 / Chat memory
6. `src/day6_logging.py`：日志与可观测性 / Logging and observability

后续可以继续扩展 RAG、工作流、多 Agent 协作、评测和 Demo 应用。

Later stages can expand into RAG, workflows, multi-agent collaboration, evaluation, and demo applications.

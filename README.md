# LLM Function Calling Demo

A portfolio project demonstrating how a Large Language Model selects and executes tools using Python, FastAPI, OpenAI APIs, and structured JSON arguments.

## Features

- OpenAI function calling
- Intelligent tool selection
- JSON arguments and results
- Multi-turn session memory
- FastAPI REST endpoint
- Email draft tool
- Mock meeting tool
- Mock weather tool
- Safe calculator
- Unit tests

## Architecture

```text
User -> FastAPI -> LLM -> Tool selection -> JSON arguments
     -> Python function -> Tool result -> Final AI response
```

## Folder structure

```text
llm-function-calling-demo/
├── app/
│   ├── __init__.py
│   ├── assistant.py
│   ├── config.py
│   ├── functions.py
│   ├── main.py
│   └── prompts.py
├── tests/
│   └── test_functions.py
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

## Setup

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and add your key:

```env
OPENAI_API_KEY=your_real_key
OPENAI_MODEL=gpt-4o-mini
```

Run:

```bash
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

Test request:

```json
{
  "session_id": "demo",
  "message": "Calculate 25 * 8."
}
```

## Resume bullet

Developed an LLM function-calling application using Python, FastAPI, OpenAI APIs, and structured JSON schemas. Implemented intelligent tool selection for meeting scheduling, email drafting, weather retrieval, and calculations while supporting multi-turn context and safe function execution.

## Author

Gunashekar Kandi

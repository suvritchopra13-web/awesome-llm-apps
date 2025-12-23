# AI Agent Instructions: awesome-llm-apps

This repository is a curated monorepo of many independent LLM apps (RAG, AI Agents, multi-agent teams, MCP, Voice). Each app lives in its own folder with its own `README.md` and `requirements.txt`. Work is scoped per app—avoid cross-app changes unless clearly intentional.

## Big Picture
- Categories map to folders: `starter_ai_agents/`, `advanced_ai_agents/`, `advanced_llm_apps/`, `rag_tutorials/`, `voice_ai_agents/`, `mcp_ai_agents/`, `ai_agent_framework_crash_course/`.
- Most apps are Streamlit frontends with agent/back-end logic in the same script. Entry points commonly include `app.py`, `main.py`, or a task-specific script (e.g., `travel_agent.py`).
- Multiple agent frameworks are used: OpenAI Agents SDK, Google ADK, Agno, MCP-Agent; local models via Ollama.

## Architecture Patterns (with examples)
- Streamlit UI + Agent orchestration:
  - Travel planning: [starter_ai_agents/ai_travel_agent/travel_agent.py](starter_ai_agents/ai_travel_agent/travel_agent.py)
  - Voice RAG: [voice_ai_agents/voice_rag_openaisdk/rag_voice.py](voice_ai_agents/voice_rag_openaisdk/rag_voice.py)
  - Tarot chat: [advanced_llm_apps/chat-with-tarots/app.py](advanced_llm_apps/chat-with-tarots/app.py)
- RAG flow (Voice RAG example): PDF upload → chunk with LangChain `RecursiveCharacterTextSplitter` → embed with FastEmbed → store in Qdrant → retrieve → generate response → TTS via OpenAI. See [voice_ai_agents/voice_rag_openaisdk/README.md](voice_ai_agents/voice_rag_openaisdk/README.md).
- Multi-agent teams (Agno): Coordinated specialized agents producing structured itineraries. See [advanced_ai_agents/multi_agent_apps/agent_teams/ai_travel_planner_agent_team/backend/agents/README.md](advanced_ai_agents/multi_agent_apps/agent_teams/ai_travel_planner_agent_team/backend/agents/README.md).
- MCP browser agent: Streamlit + MCP-Agent + Playwright, requires Node.js. See [mcp_ai_agents/browser_mcp_agent/README.md](mcp_ai_agents/browser_mcp_agent/README.md).

## Developer Workflow
- Per-app environment:
  - Create venv and install deps:
    - Windows PowerShell:
      ```powershell
      python -m venv .venv
      .\.venv\Scripts\Activate.ps1
      pip install -r requirements.txt
      ```
  - Secrets via `.env` or Streamlit inputs. Many apps provide `env.example`; typical keys: `OPENAI_API_KEY`, `QDRANT_URL`, `QDRANT_API_KEY`, `SERPAPI_API_KEY`, `FIRECRAWL_API_KEY`.
  - Run Streamlit apps:
    ```powershell
    streamlit run <entry_script.py>
    ```
- Local LLMs with Ollama in some apps:
  - Install Ollama and pull a model (e.g., `llama3.2`, `phi4`), then run local variants. See examples in [starter_ai_agents/ai_travel_agent/README.md](starter_ai_agents/ai_travel_agent/README.md) and [advanced_llm_apps/chat-with-tarots/README.md](advanced_llm_apps/chat-with-tarots/README.md).
- MCP/Playwright apps need Node.js; verify with:
  ```powershell
  node --version
  npm --version
  ```

## Conventions & Patterns
- Streamlit scripts collect API keys via `st.text_input` or `.env` and set `os.environ["OPENAI_API_KEY"]` when needed (e.g., [voice_ai_agents/voice_rag_openaisdk/rag_voice.py](voice_ai_agents/voice_rag_openaisdk/rag_voice.py)).
- Agents are typically created with `OpenAIChat` for cloud or `Ollama` for local inference, with tools like `SerpApiTools`, `FirecrawlTools`, `ExaTools` attached as needed (e.g., [starter_ai_agents/ai_travel_agent/travel_agent.py](starter_ai_agents/ai_travel_agent/travel_agent.py)).
- Vector stores: Qdrant is preferred where specified; configure via URL/API key and create collections before use (see Voice RAG code).
- Each app folder is self-contained: keep new code, data files, and README updates within that folder.

## Integration Points
- OpenAI SDK for chat, structured outputs, TTS; keys read from env/UI.
- LangChain for chunking and pipeline composition in RAG apps.
- Qdrant for embeddings storage and retrieval (cloud URL + API key).
- Playwright via MCP-Agent for browser automation in MCP apps.

## Quick-Run Examples
- Travel Agent (cloud):
  ```powershell
  cd starter_ai_agents/ai_travel_agent
  pip install -r requirements.txt
  streamlit run travel_agent.py
  ```
- Voice RAG (Qdrant + OpenAI):
  ```powershell
  cd voice_ai_agents/voice_rag_openaisdk
  pip install -r requirements.txt
  # create .env with OPENAI_API_KEY, QDRANT_URL, QDRANT_API_KEY
  streamlit run rag_voice.py
  ```
- Browser MCP Agent:
  ```powershell
  cd mcp_ai_agents/browser_mcp_agent
  pip install -r requirements.txt
  streamlit run main.py
  ```

## Where to Look First
- Catalog: [README.md](README.md) for the full project index.
- App docs: Each app’s `README.md` for its exact setup, entry script, and requirements.
- Env templates: Search for `env.example` within relevant app folders.

If any section here feels incomplete or unclear for your current task, tell us what you’re building and which folder you’re working in—we’ll refine these instructions to fit that app’s patterns.
# Architecture

## Decision

JARVIS uses a modular monolith: one deployable application with explicit boundaries between domain modules. This keeps the system easy to run and debug while allowing modules to evolve independently.

Microservices are deferred until the system has a proven need for independent scaling or deployment.

## Module Map

```text
JARVIS
├── core/        orchestration and interaction lifecycle
├── ai/          LLMs, embeddings, structured output, and RAG
├── voice/       STT, TTS, wake word, and VAD
├── memory/      session, short-term, long-term, and semantic memory
├── tools/       validated executable capabilities
├── computer/    operating system control
├── music/       playback and audio devices
├── devices/     Home Assistant and IoT integrations
├── automation/  routines, scenes, and schedules
├── vision/      images, OCR, screenshots, and documents
├── database/    persistence and migrations
├── api/         external REST and WebSocket interfaces
└── interface/   terminal and future web interfaces
```

The current repository uses Django as its web foundation. The assistant domain code lives under `jarvis/app/core` so the web layer does not own the business logic.

## Voice Flow

```text
Microphone → Wake Word → VAD → STT → JARVIS CORE → LLM → Tools → TTS → Speaker
```

Wake word detection and VAD should run locally whenever possible. Cloud services are used for STT, TTS, and LLM capabilities when configured.

## Text Interaction Flow

```text
User input
    ↓
Pre-processing
    ↓
Relevant memory retrieval
    ↓
LLM context construction
    ↓
LLM response
    ↓
Direct answer or validated tool call
    ↓
Final response
    ↓
Persistence and audit log
```

## Core Responsibilities

1. Receive text or transcribed voice input.
2. Build context from the current session and relevant memories.
3. Invoke the configured LLM.
4. Validate and execute requested tools.
5. Handle failures and produce a safe fallback.
6. Return text or trigger TTS.
7. Persist the interaction and audit information.

## Tool Contract

Every tool should expose a consistent contract:

```python
class BaseTool:
    name: str
    description: str
    risk_level: str
    requires_confirmation: bool
    parameters: dict

    def execute(self, **kwargs) -> dict:
        ...
```

The core should discover tools through a registry rather than importing each implementation directly. This keeps new tools replaceable and testable.

The chat API accepts a structured call in this shape:

```json
{
    "message": "What time is it?",
    "tool_call": {
        "name": "get_current_time",
        "arguments": {}
    }
}
```

The registry rejects unknown tools and parameters before execution. Automatic
tool selection by the LLM is a separate milestone and is not assumed to be
implemented by this request format alone.

## Planned Data Flow

PostgreSQL stores conversations, messages, memories, tasks, devices, tool calls, logs, and preferences. Redis is reserved for fast session state and queues. `pgvector` is planned for semantic memory and RAG.

## Architecture Decisions

- Python is the primary language because of its AI and automation ecosystem.
- FastAPI is planned for the external real-time API, while Django currently provides the project foundation.
- PostgreSQL is planned for production persistence; SQLite remains useful for local Django checks and tests.
- Cloud LLM APIs are the initial integration path; Ollama is a future local-model option.
- Home Assistant is the planned abstraction layer for smart home protocols.

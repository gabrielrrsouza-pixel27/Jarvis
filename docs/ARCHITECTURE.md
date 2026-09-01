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

The current voice slice is adapter-based: `VoicePipeline` accepts an STT
adapter, sends the transcript through `JarvisOrchestrator`, and passes the
answer to a TTS adapter. UTF-8 adapters provide an offline test path. Real
microphone capture, Whisper, VAD, and cloud TTS remain separate integrations.

The first VAD implementation is local and dependency-free. `EnergyVAD` accepts
signed 16-bit PCM mono frames and classifies them by average sample energy. It
is a foundation for a streaming capture adapter, not a replacement for a
production noise-robust VAD such as Silero or WebRTC VAD.

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

The registry rejects unknown tools and parameters before execution. The LLM
adapter can now return the same structured `tool_call` shape automatically.
Regardless of whether the call came from the API or the provider, the
orchestrator sends it through the local registry and confirmation policy.

## Planned Data Flow

The database backend is selected through `DB_URL`. SQLite is the default for
local development and tests; PostgreSQL is supported for deployment with the
same Django models and migrations. Redis is reserved for fast session state and
queues. `pgvector` is planned for semantic memory and RAG.

Current memory recall uses normalized topic-word overlap with a five-record
limit. This is intentionally lightweight and local; embedding-based semantic
retrieval is reserved for the RAG milestone.

## Architecture Decisions

- Python is the primary language because of its AI and automation ecosystem.
- FastAPI is planned for the external real-time API, while Django currently provides the project foundation.
- PostgreSQL is planned for production persistence; SQLite remains useful for local Django checks and tests.
- Cloud LLM APIs are the initial integration path; Ollama is a future local-model option.
- Home Assistant is the planned abstraction layer for smart home protocols.

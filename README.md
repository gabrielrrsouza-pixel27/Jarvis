# JARVIS

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.12+" />
  <img src="https://img.shields.io/badge/Django-6.1-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django 6.1" />
  <img src="https://img.shields.io/badge/AI-Agent-Assistant-4B8BBE?style=for-the-badge" alt="AI assistant" />
  <img src="https://img.shields.io/badge/Status-Portfolio%20Project-00C853?style=for-the-badge" alt="Status" />
</p>

A personal AI assistant project designed to combine voice, reasoning, tools, memory, automation, and smart home control in a single modular system.

JARVIS is being developed as a portfolio project to demonstrate architecture, AI integration, automation workflows, and full-stack engineering with Python.

## Overview

JARVIS is a modular monolith composed of independent functional modules responsible for different layers of the assistant lifecycle:

- Core: orchestration, execution flow, and control systems
- AI: LLM integration, tool calling, embeddings, and RAG
- Voice: wake word detection, VAD, STT, TTS, and audio processing
- Memory: short-term and long-term contextual memory
- Tools: automation modules for web, files, productivity, music, and system control
- Computer: OS-level control and automation
- Devices: IoT and smart home integration
- API: backend interfaces for external interaction

## Architecture

```text
Microphone → Wake Word → VAD → STT → JARVIS CORE → LLM → Tools → TTS → Speaker

↓

┌──────────────────────────────────────────────┐
│ Computer │ Music │ Web │ Files │ Memory │   │
│ Smart Home │ Vision │ Automation │ IoT │    │
└──────────────────────────────────────────────┘
```

### System flow

1. Audio is captured from the microphone.
2. The wake word engine detects activation.
3. Voice activity detection filters speech segments.
4. Speech-to-text converts the spoken command.
5. The JARVIS core routes the request.
6. The LLM interprets the intent and decides whether tools are needed.
7. Tools execute system actions or retrieve information.
8. The result is synthesized back to audio or returned through the API.

## Tech Stack

| Area | Technology |
|---|---|
| Language | Python 3.12+ |
| Web Framework | Django 6.1 |
| API Layer | FastAPI + Uvicorn |
| Database | PostgreSQL 15+ |
| Cache | Redis |
| ORM | SQLAlchemy + Alembic |
| LLM | OpenAI GPT-4o |
| STT | Whisper API |
| TTS | OpenAI TTS |
| Wake Word | Porcupine (Picovoice) |
| Vector DB | pgvector |
| IoT | Home Assistant REST API |
| Containers | Docker + Docker Compose |

## Repository Structure

```text
Jarvis.0_1/
├── jarvis/
│   └── app/
│       └── core/
│           ├── ai/
│           │   └── llm.py
│           ├── api/
│           ├── database/
│           ├── docs/
│           ├── memory/
│           │   └── session.py
│           ├── scripts/
│           │   └── setup.py
│           ├── tests/
│           ├── tools/
│           │   ├── automation/
│           │   ├── computer/
│           │   ├── files/
│           │   ├── music/
│           │   ├── productivity/
│           │   ├── smart_home/
│           │   └── web/
│           ├── vision/
│           └── voice/
├── jarvis_project/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── manage.py
├── .venv/
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
├── Dockerfile
├── docker-compose.yml
├── LICENSE
├── SECURITY.md
└── .github/
```

## Key Features

- Voice-driven AI assistant workflow
- Modular tool architecture
- Automated file, web, and system actions
- Context memory for conversational continuity
- Future integration with music, smart home, and IoT devices
- Portfolio-ready Python project structure
- Extensible backend for experimentation and growth

## Current Status

The current release is a local, testable foundation. It includes a Django web layer, conversation and memory persistence, a tool registry, safe starter tools, risk metadata, database and JSON audit logging with sensitive-field redaction, an offline fallback, and an OpenAI-compatible LLM adapter with automatic tool selection. Voice, smart home, and deployment integrations remain tracked in the roadmap rather than being presented as completed features.

## Prerequisites

- Python 3.12+
- Docker and Docker Compose
- OpenAI API access
- PostgreSQL 15+

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-username/jarvis.git
cd jarvis
```

### 2. Create a virtual environment

```bash
python -m venv .venv

# Linux / macOS
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

Then update the file with your credentials, such as:

```env
OPENAI_API_KEY=your_api_key_here
DB_URL=postgresql://jarvis:jarvis@localhost/jarvis
```

### 5. Start the database

```bash
docker-compose up -d postgres
```

### 6. Run database migrations

```bash
alembic upgrade head
```

### 7. Start the application

```bash
python manage.py runserver
```

To start a terminal conversation with the offline fallback or configured LLM:

```powershell
python manage.py jarvis_chat
```

Type `:quit` or `:exit` to close the session. The command reuses the same
orchestrator and conversation persistence used by the HTTP API.

To call the protected chat endpoint from PowerShell, create a session first so
Django can issue the CSRF cookie:

```powershell
$session = New-Object Microsoft.PowerShell.Commands.WebRequestSession
Invoke-WebRequest `
  -UseBasicParsing `
  -Uri http://127.0.0.1:8000/ `
  -WebSession $session | Out-Null

$csrf = $session.Cookies.GetCookies('http://127.0.0.1:8000/')['csrftoken'].Value
$body = @{ message = 'Hello, JARVIS' } | ConvertTo-Json

Invoke-RestMethod `
  -Uri http://127.0.0.1:8000/api/chat/ `
  -WebSession $session `
  -Headers @{ 'X-CSRFToken' = $csrf; Referer = 'http://127.0.0.1:8000/' } `
  -Method Post `
  -ContentType 'application/json' `
  -Body $body
```

For the Python package-based runtime version:

```bash
python -m app.main
```

## Environment Configuration

The project uses environment variables for sensitive configuration.

Make sure to keep the following in a `.env` file and never commit it to version control:

- OpenAI key
- database credentials
- Redis configuration
- third-party service tokens

## Documentation

The project is documented as it evolves from the first prototype to deployment:

- [Project vision](docs/PROJECT_VISION.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Security model](docs/SECURITY.md)
- [Testing strategy](docs/TESTING.md)
- [Requirements specification](docs/REQUIREMENTS.md)
- [Roadmap](docs/ROADMAP.md)
- [Changelog and learning notes](CHANGELOG.md)

## Testing

```powershell
# Validate Django configuration
python manage.py check

# Run the core application tests
python manage.py test core
```

The implementation history and learning notes are maintained in [CHANGELOG.md](CHANGELOG.md).

If the provider returns a rate-limit or quota error, JARVIS records a sanitized
`llm_error` event and uses the local fallback instead of terminating the
terminal session. Check the OpenAI account limits before retrying repeatedly.

## Roadmap

- [x] Project documentation
- [ ] v0.1 — Terminal + AI
- [ ] v0.2 — Conversation memory
- [ ] v0.3 — Tools system
- [ ] v0.4 — Speech recognition and synthesis
- [ ] v0.5 — Wake word detection
- [ ] v0.6 — Computer control
- [ ] v0.7 — Music playback integration
- [ ] v0.8 — JBL integration
- [ ] v0.9 — Smart home automation
- [ ] v1.0 — Full assistant release

## Security

- Never commit `.env`
- Store all API keys in environment variables
- Require explicit confirmation for destructive or high-risk actions
- Maintain tool execution auditing
- Follow secure development practices for all integrations

## Contributing

This project is intended as a personal portfolio project. Suggestions and feedback are welcome.

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to your fork
5. Open a pull request

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Author

Gabriel Roberto Ribeiro de Souza

- GitHub: [@gabriel-r-souza](https://github.com/gabriel-r-souza)
- Email: gabriel.r.r.souza@academico.unirv.edu.br

---

<p align="center">
  <strong>Built with ❤️ and Python by Gabriel Souza</strong>
</p>

<p align="center">
  <em>"The best way to predict the future is to build it."</em>
</p>

# Changelog

All notable changes to JARVIS are documented here.

The project follows a practical versioning model:

- `0.x`: experimentation and MVP development
- `1.x`: stable assistant capabilities
- `2.x`: local models and advanced autonomy

## [Unreleased]

### Planned

- Connect the orchestrator to a configured LLM provider
- Add voice input and output adapters
- Add deployment configuration

## [0.1.8] - 2026-09-01

### Added

- Interactive `python manage.py jarvis_chat` command
- Shared conversation state across terminal messages
- `:quit` and `:exit` session commands
- Graceful handling of Ctrl+C and end-of-input
- Integration test for the offline terminal workflow

### Why

The terminal is the simplest interface for validating the assistant before voice and web interfaces add more moving parts. Reusing the existing orchestrator keeps behavior consistent across interfaces.

### Learning Notes

- User interfaces should call domain services instead of duplicating assistant logic.
- A session needs explicit exit and interruption behavior for reliable local use.
- Offline execution makes the terminal loop useful before API credentials are configured.

### Verification

- `python manage.py check`
- `python manage.py test core` — 11 tests passed

## [0.1.7] - 2026-09-01

### Added

- Automatic LLM tool selection through the provider's structured function-call response
- Tool definitions sent to the provider as JSON-schema-compatible function definitions
- End-to-end orchestrator test for a provider-selected tool

### Security

- Automatic tool calls still pass through the local registry, parameter validation, risk policy, and audit logging.
- The LLM cannot bypass confirmation requirements by choosing a tool automatically.

### Why

Manual tool calls proved the execution contract. This increment connects the provider's decision to that contract without allowing model output to execute directly.

### Learning Notes

- Model output is untrusted input even when it follows a provider schema.
- A single execution gateway keeps manual and automatic calls consistent.
- Provider integration should be tested with a fake selector before any paid network call.

### Verification

- `python manage.py check`
- `python manage.py test core` — 10 tests passed

## [0.1.6] - 2026-09-01

### Added

- Structured `tool_call` request support in the chat API
- Parameter schemas on registered tools
- Rejection of unknown tool parameters before execution
- Tool definition export for future LLM provider integration
- Tests for structured calls and invalid parameter rejection

### Changed

- Tool execution now initializes failed audit results safely when a handler raises an exception.
- Requirements and architecture docs distinguish validated tool calls from future automatic LLM tool selection.

### Why

The assistant needs a strict boundary between model output and executable actions. Validating the tool name and arguments before execution reduces accidental or malicious parameter injection.

### Learning Notes

- A structured payload is a contract, not proof that an LLM selected the action correctly.
- Parameter validation belongs before the handler runs and must not rely only on prompt instructions.
- Failure paths need the same audit guarantees as successful tool calls.

### Verification

- `python manage.py check`
- `python manage.py test core` — 9 tests passed

## [0.1.5] - 2026-09-01

### Fixed

- Homepage now issues the CSRF cookie required by protected JSON requests.
- README now documents a working PowerShell API request with CSRF handling.

### Security

- Kept CSRF protection enabled for chat and memory state-changing endpoints.
- Added a real end-to-end check proving the protected chat request succeeds with a valid token.

### Why

The first command-line example reached Django but received `403` because it did not establish a CSRF session. The fix preserves the security boundary and makes the documented client flow usable.

### Learning Notes

- Activating a virtual environment and starting a server are separate operations.
- A protected API example must show the complete cookie and header exchange, not only the POST body.
- Security failures should be fixed at the client workflow or authentication boundary, not bypassed in production code.

### Verification

- `python manage.py check`
- `python manage.py test core` — 7 tests passed
- Real PowerShell request to `/api/chat/` — returned `conversation_id` and offline response

## [0.1.4] - 2026-09-01

### Added

- Provider-agnostic `LLMService` with OpenAI Chat Completions support
- Offline fallback when `OPENAI_API_KEY` is not configured
- Conversation history passed to the configured LLM
- Automatic loading of local `.env` configuration
- `OPENAI_MODEL` configuration option
- Tests proving the offline path does not require network access

### Changed

- The orchestrator now uses the LLM adapter for normal text responses.
- The README and requirements specification distinguish the LLM adapter from future tool calling.

### Why

The roadmap requires an LLM connection, but development and tests must remain deterministic and usable without paid cloud access. The adapter boundary allows the provider to be replaced later without changing the core orchestrator.

### Learning Notes

- External services need a local fallback before they become part of the default execution path.
- API credentials must be loaded from the environment and never embedded in source code.
- LLM tool calling is a separate milestone from basic LLM text generation and should not be marked complete prematurely.

### Verification

- `python manage.py check`
- `python manage.py test core` — 7 tests passed

## [0.1.3] - 2026-09-01

### Added

- Formal functional and non-functional requirements specification
- `MemoryService` for saving, searching, and forgetting memories
- `GET` and `POST /api/memories/` endpoints
- `DELETE /api/memories/<id>/` endpoint
- Automated memory lifecycle test

### Changed

- The README links to the requirements specification.
- The roadmap marks verified memory and tool capabilities as complete.

### Why

The assistant needs an explicit memory contract before adding an LLM. This lets the future model use memory through a tested service instead of writing directly to the database.

### Learning Notes

- Persistence needs a user-facing lifecycle: save, retrieve, and forget.
- Requirements should distinguish implemented behavior from planned integrations.
- API validation and business rules belong in a service boundary reusable by HTTP, terminal, and voice interfaces.

### Verification

- `python manage.py check`
- `python manage.py test core` — 5 tests passed

## [0.1.1] - 2026-09-01

### Added

- Conversation, message, memory, and tool-audit models
- Tool registry with risk metadata and confirmation policy
- Safe `get_current_time` and `get_system_stats` tools
- Orchestrator service for text interactions
- CSRF-protected JSON endpoint at `/api/chat/`
- Four integration tests for the core application
- Environment-based Django settings
- Dependency manifest and public `.env.example`

### Changed

- The README now distinguishes implemented capabilities from roadmap items.
- The roadmap marks persistence, audit logging, safe tools, and the chat endpoint as complete.

### Learning Notes

- The domain workflow must be testable without an external LLM before cloud integration is added.
- Risk metadata belongs to the tool contract, but the execution service must enforce it independently of model output.
- CSRF protection should not be disabled just because an endpoint is intended for local use.
- A release is easier to explain when documentation states exactly what is implemented and what is planned.

### Verification

- `python manage.py check`
- `python manage.py makemigrations core`
- `python manage.py migrate`
- `python manage.py test core`

## [0.1.0] - 2026-09-01

### Added

- Initial Django project and `core` application
- Modular JARVIS package structure under `jarvis/app/core`
- Homepage route and starter template
- English portfolio README at the repository root
- Git repository with `main` branch and GitHub remote
- Initial security, architecture, roadmap, and testing documentation

### Changed

- Registered the `core` Django application in project settings
- Added repository hygiene rules in `.gitignore`

### Learning Notes

- A Django project provides the web foundation, but the assistant's domain modules should remain separated from the web layer.
- A modular monolith is a good starting point for a solo portfolio project because it keeps deployment and debugging simple.
- Documentation and version history should evolve with the implementation, not be postponed until the end.
- GitHub publication requires both a clean local history and a correctly authenticated remote.

### Verification

- `python manage.py check`
- `python manage.py test core`
- GitHub `main` branch synchronized with the local repository

## Release Notes Template

Copy this template when starting a new version:

```markdown
## [0.x.0] - YYYY-MM-DD

### Added

- 

### Changed

- 

### Fixed

- 

### Security

- 

### Learning Notes

- What was learned:
- What was difficult:
- What will change in the next version:

### Verification

- Command:
- Result:
```

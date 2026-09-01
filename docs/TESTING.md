# Testing Strategy

A task is complete only when its tests pass. Tests are part of the definition of done, not a final decoration.

## Test Pyramid

```text
       /\\
      /E2E\\       few, slow, critical
     /------\\
    /Integration\\  module boundaries
   /------------\\
  /   Unit tests  \\ fast and focused
 /__________________\\
```

## Test Types

| Type | Purpose | Tools | Frequency |
|---|---|---|---|
| Unit | Isolated functions and classes | pytest | Every commit |
| Integration | Modules working together | pytest + test database | Every pull request |
| API | REST and WebSocket contracts | httpx + TestClient | Every pull request |
| Tool | Valid and invalid tool execution | pytest | Every pull request |
| Voice | STT/TTS pipeline behavior | Audio fixtures | Per release |
| Security | Confirmation and validation rules | pytest | Per release |
| Load | Stability under sustained use | Locust or k6 | Major versions |

## Critical Coverage

### Core

- Complete interaction lifecycle
- LLM failure fallback
- Tool failure fallback
- Session history preservation

### Tools

- Valid parameter execution
- Invalid parameter rejection
- Confirmation for high-risk actions
- Audit record creation

### Memory and Database

- Memory persistence and retrieval
- Conversation and message CRUD
- Migration execution
- Referential integrity

### Security

- High-risk actions cannot run without confirmation
- Secrets never appear in logs
- Invalid parameters are rejected

## Definition of Done

- Code implements the requirement.
- Focused tests are written and passing.
- No new errors or warnings are introduced.
- Documentation is updated when behavior changes.
- Errors are handled at the correct boundary.
- Security impact has been reviewed.
- The change is recorded in `CHANGELOG.md`.

## Current Verification

The current Django foundation is verified with:

```powershell
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py test core
```

The first command validates Django configuration. The second validates the starter application and homepage behavior.

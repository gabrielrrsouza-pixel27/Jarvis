# Roadmap

The roadmap is incremental. Each version adds a capability on top of a verified previous version. Dates are intentionally omitted so the project can prioritize quality over artificial deadlines.

## 0.1 — Terminal and AI foundation

- [x] Create GitHub repository
- [x] Configure Python environment
- [x] Create modular project structure
- [x] Add Django foundation and homepage
- [ ] Add dependency manifest
- [ ] Add `.env.example`
- [ ] Integrate an LLM provider
- [ ] Add a terminal conversation loop
- [ ] Add structured logging

## 0.2 — Conversation memory

- [ ] Store session message history
- [ ] Persist conversations and messages
- [ ] Add PostgreSQL configuration
- [ ] Add SQLAlchemy and Alembic where required
- [ ] Create the first database migration

## 0.3 — Tools and MVP

- [ ] Define `BaseTool`
- [ ] Create a tool registry
- [ ] Add safe time and system-stat tools
- [ ] Add long-term memory storage
- [ ] Add structured tool-call audit logs
- [ ] Add confirmation policy for risky actions

## 0.4 — Voice

- [ ] Integrate Whisper STT
- [ ] Integrate TTS
- [ ] Capture microphone input
- [ ] Add VAD
- [ ] Complete microphone-to-speaker pipeline

## 0.5 — Wake word

- [ ] Add local Porcupine or Vosk detection
- [ ] Implement waiting and active states
- [ ] Add activation feedback
- [ ] Add keyboard shortcut fallback

## 0.6 — Computer control

- [ ] Open and close authorized applications
- [ ] Read CPU and memory usage
- [ ] Control system volume
- [ ] Capture screenshots
- [ ] Enforce risk confirmation

## 0.7 — Music

- [ ] Integrate a streaming provider
- [ ] Play, pause, resume, and skip tracks
- [ ] Select an output device

## 0.8 — Audio devices

- [ ] Detect connected output devices
- [ ] Add JBL device selection
- [ ] Add a disconnected-device fallback

## 0.9 — Smart home

- [ ] Integrate Home Assistant
- [ ] Control lights, switches, TV, and climate
- [ ] Add scenes such as movie mode and good night
- [ ] Read sensor state

## 1.0 — Complete assistant

- [ ] Tasks and reminders
- [ ] Web search
- [ ] Proactive notifications
- [ ] Integration and security test suite
- [ ] Stable documented release

## Future

- `1.1`: vision and document processing
- `1.2`: RAG and pgvector knowledge base
- `1.5`: web dashboard and WebSocket interface
- `2.0`: local models through Ollama
- `2.5`: multi-step autonomous agents

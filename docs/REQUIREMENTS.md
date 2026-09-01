# Requirements Specification

This document turns the project vision into testable requirements. A feature is only considered complete when its implementation, tests, documentation, and security review are present.

## Functional Requirements

| ID | Requirement | Release | Status |
|---|---|---:|---|
| FR-001 | Accept a text message and return an assistant response | 0.1 | Implemented |
| FR-002 | Persist user and assistant messages in a conversation | 0.1 | Implemented |
| FR-003 | Register tools through a common contract | 0.1 | Implemented |
| FR-004 | Execute approved low-risk tools | 0.1 | Implemented |
| FR-005 | Audit every tool execution | 0.1 | Implemented |
| FR-006 | Store, search, and delete persistent memories | 0.2 | Implemented |
| FR-007 | Connect the orchestrator to an LLM provider | 0.1 | Planned |
| FR-008 | Preserve session context across requests | 0.2 | In progress |
| FR-009 | Add structured LLM tool calling | 0.3 | Planned |
| FR-010 | Require confirmation for high-risk actions | 0.3 | Partially implemented |
| FR-011 | Capture and transcribe microphone input | 0.4 | Planned |
| FR-012 | Synthesize assistant responses to audio | 0.4 | Planned |
| FR-013 | Detect a local wake word | 0.5 | Planned |
| FR-014 | Control authorized computer actions | 0.6 | Planned |
| FR-015 | Control music playback and output devices | 0.7-0.8 | Planned |
| FR-016 | Integrate Home Assistant devices and scenes | 0.9 | Planned |
| FR-017 | Provide web search, vision, documents, and RAG | 1.0-1.2 | Planned |
| FR-018 | Provide a deployable production configuration | 1.0 | Planned |

## Non-Functional Requirements

| ID | Requirement | Acceptance target | Status |
|---|---|---|---|
| NFR-001 | Security | High-risk actions require explicit confirmation | Design implemented; high-risk tools pending |
| NFR-002 | Privacy | Secrets remain in environment variables and sensitive values stay out of logs | Implemented for current code |
| NFR-003 | Modularity | Domain services do not depend on HTTP request objects | Implemented in core services |
| NFR-004 | Testability | Critical behavior has automated tests | Implemented for current MVP |
| NFR-005 | Reliability | Tool failures become controlled responses and audit records | Partially implemented |
| NFR-006 | Performance | Simple text response target under 2 seconds locally | To be measured after LLM integration |
| NFR-007 | Voice latency | Start spoken response under 4 seconds | To be measured in release 0.4 |
| NFR-008 | Availability | Stable continuous use for 8 hours | To be tested before 1.0 |
| NFR-009 | Compatibility | Support Windows and Linux for portable modules | Windows foundation verified; Linux pending |
| NFR-010 | Observability | Structured logs and tool metrics support diagnosis | Audit database implemented; structured logger pending |
| NFR-011 | Maintainability | New tools follow one documented interface | Implemented through `Tool` and `ToolRegistry` |
| NFR-012 | Data integrity | Schema changes use versioned Django migrations | Implemented |

## Requirement Workflow

For every new requirement:

1. Add or update its row in this document.
2. Identify dependencies and risk level.
3. Implement the smallest vertical slice.
4. Add a behavior-focused test.
5. Update the relevant architecture or security documentation.
6. Add a changelog entry with what changed, why, and what was learned.
7. Tag and publish the release only after validation passes.

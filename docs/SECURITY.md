# Security Model

Security is a design principle in JARVIS. Every new module, tool, or integration must be evaluated before implementation.

## Principles

1. **Least privilege:** each module receives only the access required for its task.
2. **Explicit confirmation:** irreversible or high-risk actions require confirmation.
3. **Transparency:** executable actions produce auditable records.
4. **Isolation:** a module failure should not compromise unrelated modules.
5. **Privacy:** sensitive data stays local unless the user has consented to external processing.
6. **Defense in depth:** validation, authorization, confirmation, and logging work together.

## Risk Levels

| Level | Meaning | Examples | Required action |
|---|---|---|---|
| Low | Read-only or low-impact | Time, CPU, sensors, opening an app | Direct execution |
| Medium | Reversible side effect | Volume, closing an app, saving a file | Log; confirmation when appropriate |
| High | Irreversible or powerful action | Shell commands, deleting files, critical settings | Explicit confirmation every time |

## Credentials

Secrets must be stored in environment variables, never in source code or logs:

```env
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
HOME_ASSISTANT_TOKEN=your_token_here
DB_URL=postgresql://user:password@localhost/jarvis
SPOTIFY_CLIENT_ID=your_client_id
SPOTIFY_CLIENT_SECRET=your_client_secret
```

Rules:

- Keep `.env` in `.gitignore`.
- Commit `.env.example` with placeholders only.
- Rotate credentials immediately if they are exposed.
- Never print API keys, passwords, or access tokens.
- If a credential is exposed, revoke it before continuing development; replacing
	the value in a local file is not sufficient.

## Prompt Injection

User content and retrieved documents are untrusted input. The system must not treat text such as "ignore previous instructions" as permission to bypass security controls.

Required protections:

- Explicitly define allowed tools and actions.
- Validate tool names and parameters before execution.
- Apply risk checks independently of the LLM response.
- Require confirmation for destructive operations.
- Record tool calls for later review.

## Audit Logging

A tool audit record should include the module, action, sanitized parameters, result status, risk level, confirmation status, and duration. Logs must exclude secrets and sensitive personal data.

## Database Security

- Use a database account with minimum required permissions.
- Use SSL in production.
- Use parameterized queries.
- Encrypt and test backups.
- Apply schema changes through versioned migrations.

## API Requests

The JSON API keeps Django CSRF protection enabled. A browser must send the
`X-CSRFToken` header, and command-line clients should first request the home
page to receive the CSRF cookie before making a state-changing request.

## Release Checklist

- [ ] No secrets in source code or Git history
- [ ] `.env` is ignored and `.env.example` has placeholders
- [ ] High-risk tools require explicit confirmation
- [ ] Logs are sanitized
- [x] Tool parameters are validated
- [x] Structured audit events redact sensitive fields
- [ ] Dependencies are checked for known vulnerabilities
- [ ] Infrastructure details are not unnecessarily exposed

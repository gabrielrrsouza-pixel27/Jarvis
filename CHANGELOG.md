# Changelog

All notable changes to JARVIS are documented here.

The project follows a practical versioning model:

- `0.x`: experimentation and MVP development
- `1.x`: stable assistant capabilities
- `2.x`: local models and advanced autonomy

## [Unreleased]

### Planned

- Add the first real AI conversation flow
- Add a terminal interface for text commands
- Add environment configuration with `.env.example`
- Add automated checks to the development workflow

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

# AudioHardcore — Four-AI Continuation & GitHub Publishing Protocol

## Purpose

This document keeps AudioHardcore continuous across ChatGPT, GitHub Copilot, Grok, and Perplexity. The repository is the source of truth for code; `AH_PROJECT_STATE.md` is the portable project-state summary.

## Mandatory startup sequence for every AI

1. Inspect the repository before proposing a restart or rewrite.
2. Read `README.md`, `AH_PROJECT_STATE.md`, `CHANGELOG.md`, `VERSION`, and relevant files for the requested task.
3. Identify what is **implemented**, **tested**, **verified**, and **planned**.
4. Preserve explicit product-owner decisions unless there is a documented reason to change them.
5. Never claim a build, test, APK, installer, deployment, or integration was completed unless it was actually executed or verified.
6. Keep the project free/open-source where practical and avoid introducing paid services unless the user explicitly approves them.
7. Never commit personal music, local databases, credentials, private keys, signing keys, `.env` files, API tokens, or machine-specific build output.

## Shared project mission

AudioHardcore is a free/local-first cross-platform music ecosystem targeting Windows, macOS, Android, and Amazon Fire. It supports an existing 1,800+ MP3 library, metadata preservation and controlled write-back, playlists, favorites, ratings, artwork, filesystem monitoring, backups/restores, desktop and Android clients, WordPress integration, and a future account/sync/community layer.

The UX direction may draw inspiration from the information density and navigation patterns of YouTube Music and Facebook, but must not copy proprietary branding, artwork, code, or other protected assets.

## AI roles

### ChatGPT — Architect / integrator / release coordinator

Use ChatGPT for:
- architecture decisions and reconciliation
- converting research and review into implementation tasks
- coordinating the overall roadmap
- integrating work from the other AIs
- testing and release-state management
- updating `AH_PROJECT_STATE.md` and `CHANGELOG.md`

ChatGPT must not silently replace established architecture.

### GitHub Copilot — in-repository implementation engineer

Use Copilot directly against the checked-out repository for:
- code completion and refactoring
- tests
- bug fixes
- migrations
- CI/workflow changes
- platform-specific implementation
- small, reviewable commits

Copilot should obey `.github/copilot-instructions.md` and the repository's existing architecture. It should inspect nearby code before creating new abstractions.

### Grok — engineering challenger / product reviewer

Use Grok for:
- adversarial architecture review
- implementation alternatives
- UI/UX critique
- performance and edge-case analysis
- identifying unnecessary complexity
- reviewing changes before they are merged

Grok should challenge assumptions with concrete reasons and should distinguish verified behavior from speculation.

### Perplexity — current research / source verification

Use Perplexity for facts that may have changed:
- current Android/Google requirements
- current Windows/macOS packaging requirements
- Amazon Fire compatibility
- WordPress APIs and plugin guidance
- SMF integration options
- licensing
- hosting/cloud options
- current library/framework versions and policies

Prefer official documentation and primary sources. Return the source, claim, date, and confidence when practical.

## Standard four-AI workflow

```text
USER REQUEST
    ↓
CHATGPT — define task and acceptance criteria
    ↓
PERPLEXITY — current research / official-source verification when needed
    ↓
GROK — adversarial engineering + UX review
    ↓
COPILOT — implement inside repository
    ↓
CHATGPT — run/inspect tests, reconcile, update project state
    ↓
GITHUB — commit/push verified change
```

For a code-only task where research is unnecessary, skip Perplexity. For a small implementation, Copilot can act directly after ChatGPT defines the task.

## GitHub publishing rules

### Repository

`https://github.com/anastaysia94-sudo/AudioHardcore`

### Branching

- `main` should remain releasable.
- Use a feature branch for substantial or risky changes.
- Prefer small, descriptive commits.
- Do not force-push `main` unless explicitly authorized.

### Commit format

Use clear conventional-style messages where practical:

```text
feat: add Android queue persistence
fix: repair database migration compatibility
ci: build Android debug APK
 docs: update WordPress installation guide
 test: add sync conflict coverage
```

### Before publishing

Run the relevant checks, normally:

```bash
python -m compileall -q .
pytest -q
```

For Android changes, also run the appropriate Gradle build/tests. For WordPress PHP changes, run `php -l` on changed PHP files and, when available, WordPress plugin tests.

### After publishing

Update:
- `VERSION` for release-level changes
- `CHANGELOG.md`
- `AH_PROJECT_STATE.md`
- relevant docs

Then verify `main` points to the intended commit and that the repository contains the changed files.

## Portable handoff format

Every AI completing meaningful work should return:

```text
AUDIOHARDCORE HANDOFF

Current version:
Current phase:
Task:

Implemented:

Tested:

Verified externally:

Files changed:

Decisions made:

Open issues:

Risks:

Recommended next action:

Git commit / branch:
```

## Rules for source-of-truth conflicts

Priority order:

1. Actual repository code and tests
2. Verified official documentation
3. Explicit user decisions
4. `AH_PROJECT_STATE.md`
5. Other AI recommendations
6. Unverified assumptions

If two AI outputs conflict, do not average them. Identify the conflict, verify it, and record the resulting decision.

## Definition of complete

A task is complete only when the requested behavior exists in source, the applicable tests/builds pass, documentation is updated, and the change is published to GitHub when GitHub publication is requested.

A production service is not considered deployed merely because deployment code exists.

A signed APK/EXE is not considered released merely because build instructions exist.

## Current product boundaries

The repository is a source/build foundation. External operator actions may still be required for:
- production cloud hosting and database
- domain/TLS
- Android release signing
- app-store submission
- email delivery
- billing provider
- production monitoring
- SMF server configuration

Do not invent credentials or claim those environments are configured without evidence.

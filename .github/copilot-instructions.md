# GitHub Copilot Instructions — AudioHardcore

## Read first

Before editing code, inspect:

- `README.md`
- `AH_PROJECT_STATE.md`
- `CHANGELOG.md`
- `VERSION`
- `docs/AI_CONTINUATION.md`
- the relevant module, tests, and build workflow

## Architecture rules

AudioHardcore is local-first and cross-platform. Keep these boundaries:

- `core/` = reusable library/metadata/watcher/sync logic
- `backend/` = API and persistence boundary
- `desktop/` = native desktop UI
- `android/` = Android client/service
- `clients/flutter/` = future shared client work
- `wordpress/` = WordPress integration
- `docs/` = operational/project documentation
- `tests/` = automated verification

Do not put machine-specific paths, user music, credentials, database files, signing keys, or generated binaries into source control.

## Implementation rules

1. Prefer the smallest maintainable change that satisfies the task.
2. Preserve compatibility with existing public functions and environment variables unless deliberately versioning a breaking change.
3. Add or update tests for behavior changes.
4. Keep filesystem operations safe and explicit.
5. Do not destructively rewrite music metadata without the existing backup/write-back safeguards.
6. Do not claim an API, APK, installer, or deployment works without actually building/testing it.
7. Avoid introducing a paid dependency when a free/local alternative is practical.
8. Reuse existing helpers before creating parallel abstractions.

## Validation

For Python changes:

```bash
python -m compileall -q .
pytest -q
```

For Android changes, run the appropriate Gradle build/test task.

For PHP changes:

```bash
php -l path/to/file.php
```

## Git

Use descriptive commits. Avoid force-pushing `main`. Substantial work should use a feature branch and a reviewable pull request.

## Handoff

After meaningful work, update `AH_PROJECT_STATE.md` and `CHANGELOG.md` and provide a handoff containing the current version, task, implementation, tests, files changed, decisions, risks, and recommended next action.

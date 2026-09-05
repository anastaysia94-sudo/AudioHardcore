# AudioHardcore Project State

Project: AudioHardcore
Release: 1.1.0
Architecture: AH-ARCH-1.0
Status: Complete source/deployment foundation; operator-specific production deployment remains.
Owner: Product owner (user)
Cost target: Free/open development stack.

## Implemented
- Recursive multi-format audio scanner with SHA-256 identity.
- Mutagen metadata extraction and controlled write-back with timestamped backups.
- SQLite persistence, migrations/versioning, WAL and busy-timeout.
- Search, pagination, favorites, ratings, history, playlists and duplicate detection.
- Native Tkinter desktop client with browse/search/queue/watch/backup/restore.
- Account registration/login using scrypt password hashing and signed access tokens.
- Device registration and authenticated sync-change journal.
- Deterministic sync merge policies (latest/local/remote).
- Android Studio project with MediaStore discovery and foreground playback-service foundation.
- GitHub Actions workflows for Android debug APK and Windows builds.
- WordPress connector plugin + shortcode/settings documentation.
- Dockerfile and Docker Compose deployment.
- SMF integration contract/documentation.
- Four-AI continuation protocol for ChatGPT, GitHub Copilot, Grok and Perplexity.
- Copilot-specific repository instructions.
- Ready-to-paste prompts and GitHub publishing protocol in `docs/AI_PROMPTS.md`.

## Verification
- `python -m compileall -q .` -> success
- `pytest -q` -> 12 passed
- WordPress connector PHP syntax check -> no syntax errors

## Release/build paths
- Android debug APK: GitHub Actions workflow or Android Studio/Gradle; see `docs/ANDROID_APK_BUILD.md`.
- Windows package: GitHub Actions or `build_windows.ps1`.
- WordPress: ZIP `wordpress/audiohardcore-integration/`, install via Plugins > Add New > Upload Plugin; configure Settings > AudioHardcore; use `[audiohardcore_library]`.
- Docker: `docker compose up --build -d` with `AUDIOHARDCORE_AUTH_SECRET` set.

## Four-AI synchronization
Read `docs/AI_CONTINUATION.md` first.
- ChatGPT = architecture reconciliation, implementation/testing coordination, release state.
- GitHub Copilot = in-repository implementation, tests, refactors and CI/platform work.
- Grok = adversarial engineering review, UX critique, alternatives and edge cases.
- Perplexity = current technical research and primary-source verification.

`docs/AI_PROMPTS.md` contains ready-to-paste prompts for all four systems plus the shared continuation and GitHub publishing commands.

## Operator-specific production steps
- HTTPS/TLS and DNS.
- Managed backups/monitoring.
- Android release signing key for public distribution.
- Target-device QA on Windows/macOS/Android/Fire.
- Email verification/password reset/refresh-token rotation/rate limiting for a public SaaS deployment.
- Production cloud database/object storage if cloud media is desired.
- Payments/subscriptions only if commercial features are enabled.
- Version-specific SMF connector implementation.

Truth labels: Implemented = code exists; Tested = automated/manual test executed; Verified = externally confirmed; Operator step = requires deployment credentials/hardware/environment.

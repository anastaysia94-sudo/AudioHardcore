# AudioHardcore Project State

Project: AudioHardcore
Release: 1.0.0
Architecture: AH-ARCH-1.0
Status: 1.0.0 foundation release / active platform development
Owner: Product owner (user)

## Verified baseline
- 1,800+ MP3 target library.
- Windows, macOS, Android, Amazon Fire targets.
- Local/offline-first music library.
- SHA-256 track identity and recursive scanner.
- Mutagen metadata extraction and controlled write-back with backups.
- SQLite persistence with schema migrations/versioning and WAL/busy-timeout foundation.
- Search, favorites, ratings, history, playlists, duplicate detection.
- Native Tkinter desktop client with browse/search/queue/watch/backup/restore foundations.
- Android Studio project with MediaStore discovery/search and foreground playback-service foundation.
- WordPress connector and installation documentation.
- GitHub Actions Android debug APK and Windows build workflows.
- Account registration/login foundation with scrypt password hashing and signed access tokens.
- Device registration and append-only sync-change API.
- Deterministic latest/local/remote merge utility.

## Tested in the development environment
- python -m compileall -q . -> success
- pytest -q -> 12 passed

## Deliberate boundaries
- No personal music library or local DB in source control.
- No signing keys or generated binaries committed.
- Hosted cloud authentication/sync is a foundation, not a production Internet service.
- Full Android background/media-session feature parity is not yet complete.
- SMF integration and commercial billing are not yet implemented.

## Build instructions
- Android: GitHub Actions workflow `.github/workflows/android-apk.yml` or local Gradle/Android Studio; see `docs/ANDROID_APK_BUILD.md`.
- Windows: GitHub Actions workflow `.github/workflows/windows-build.yml` or local `build_windows.ps1`; see `docs/WINDOWS_RELEASE.md`.
- WordPress: install `wordpress/audiohardcore-integration/` as a ZIP; configure **Settings > AudioHardcore**; use `[audiohardcore_library]`; see `docs/WORDPRESS_INSTALL.md`.

## 1.0 platform foundation
- Account registration/login.
- Device registration.
- Append-only sync change journal.
- Deterministic conflict merge helper.
- Versioned schema foundation.
- CI source/test workflow.

## Remaining production work
- Production hosted API/database deployment.
- Email verification/password reset/refresh-token rotation/rate limiting/audit logs.
- Real client-side multi-device sync application logic.
- Full Android background playback/media controls and feature parity.
- Signed Windows/macOS production installers and updater.
- Full WordPress administration/content integration.
- Stable SMF integration.
- Payments/subscriptions.
- Optional cloud/off-device audio storage.

## Three-AI synchronization
Perplexity = current technical research/source verification.
Grok = engineering challenge/review and alternative implementation analysis.
ChatGPT = architecture reconciliation, implementation, testing, and project-state authority.

Truth labels: Implemented = code exists; Tested = automated/manual test executed; Verified = externally confirmed; Planned = not implemented.

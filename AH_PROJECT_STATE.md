# AudioHardcore Project State

Project: AudioHardcore
Release: 0.9.0
Architecture: AH-ARCH-1.0
Status: Active development / local-first release candidate
Owner: Product owner (user)

## Verified baseline
- 1,800+ MP3 target library.
- Windows, macOS, Android, Amazon Fire targets.
- Local/offline-first music library.
- SHA-256 track identity and recursive scanner.
- Mutagen metadata extraction and controlled write-back with backups.
- SQLite persistence with schema migrations/versioning and WAL mode.
- Search, favorites, ratings, history, playlists, duplicate detection.
- Native Tkinter desktop client with browse/search/queue/watch/backup/restore foundations.
- Android Studio project with MediaStore discovery/search and foreground playback-service foundation.
- WordPress connector and installation documentation.
- GitHub Actions Android debug APK and Windows build workflows.

## Tested in the development environment
- python -m compileall -q .
- pytest -q -> 9 passed

## Deliberate boundaries
- No personal music library or local DB in source control.
- No signing keys or generated binaries committed.
- Cloud authentication/sync is not yet a production service.
- SMF integration and commercial billing are not yet implemented.

## Build instructions
- Android: GitHub Actions workflow `.github/workflows/android-apk.yml` or local Gradle/Android Studio; see `docs/ANDROID_APK_BUILD.md`.
- Windows: GitHub Actions workflow `.github/workflows/windows-build.yml` or local `build_windows.ps1`.
- WordPress: install `wordpress/audiohardcore-integration/` as a ZIP; configure **Settings > AudioHardcore**; use `[audiohardcore_library]`; see `docs/WORDPRESS_INSTALL.md`.

## Next production milestone
- Complete Android background/media-session controls and feature parity.
- Add authenticated accounts and device registration.
- Add cloud sync and deterministic conflict resolution.
- Expand WordPress connector and add stable SMF integration.
- Add signed release packaging and update mechanism.

## Three-AI synchronization
Perplexity = current technical research/source verification.
Grok = engineering challenge/review and alternative implementation analysis.
ChatGPT = architecture reconciliation, implementation, testing, and project-state authority.

Truth labels: Implemented = code exists; Tested = automated/manual test executed; Verified = externally confirmed; Planned = not implemented.

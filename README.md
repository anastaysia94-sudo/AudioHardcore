# AudioHardcore

AudioHardcore is a free, local-first music library and media application in active development.

Current release: **AudioHardcore 1.0.0 foundation**

The project targets Windows, macOS, Android, and Amazon Fire, with a local/offline-first library, metadata preservation and controlled write-back, playlists, favorites, artwork, filesystem change detection, backups/restores, and a future synchronized cloud/account layer.

## Current source tree

- Python/FastAPI local API
- SQLite library database with migration/versioning and WAL foundation
- Recursive audio scanner with SHA-256 identity
- Mutagen metadata engine
- Native Tkinter desktop client foundation
- Polling filesystem watcher
- Safe MP3 metadata write-back with timestamped backups
- Artwork extraction endpoint
- Playlist/favorite/rating/history foundations
- Album/artist/recently-played/queue desktop features
- Android Studio project with MediaStore discovery/search and foreground playback foundation
- GitHub Actions Android debug APK and Windows build workflows
- Android APK instructions in `docs/ANDROID_APK_BUILD.md`
- WordPress connector plugin and setup instructions
- Account registration/login foundation using scrypt password hashing and signed access tokens
- Device registration and append-only sync-change API
- Deterministic latest/local/remote sync merge helper
- Free Windows build/install scripts
- Portable project state for ChatGPT, Grok, and Perplexity

See `AH_PROJECT_STATE.md`, `docs/`, `CHANGELOG.md`, and `SECURITY.md` for the authoritative development state.

## Verification

The 1.0.0 foundation passes **12 automated tests** and Python source compilation in the development environment. Generated Android APKs and Windows executables are not committed as source artifacts; use the documented local builds or GitHub Actions workflows.

## Free/open development

The current core requires no paid API, subscription, or cloud service. Hosted cloud deployment, TLS, cloud storage, payments, and production identity infrastructure are separate deployment concerns.

Do not commit personal music libraries, credentials, generated local databases, signing keys, or build artifacts.

## Android

Open `android/` in Android Studio for local development, or use **Actions → AudioHardcore Android APK → Run workflow** to generate a debug APK artifact on a GitHub-hosted runner. See `docs/ANDROID_APK_BUILD.md`.

## WordPress

Package `wordpress/audiohardcore-integration/` as a ZIP, install it under **Plugins → Add New → Upload Plugin**, configure **Settings → AudioHardcore**, and add `[audiohardcore_library]` to a page/post. See `docs/WORDPRESS_INSTALL.md`.

## 1.0 platform foundation

Account registration/login, device registration, append-only synchronization records, deterministic conflict utilities, schema migration versioning, security guidance, and CI source checks are included. See `docs/RELEASE_1_0.md` and `docs/SYNC_1_0.md`.

# AudioHardcore

AudioHardcore is a free, local-first music library and media application in active development.

Current release: **AH-MVP-0.9.0**

The project targets Windows, macOS, Android, and Amazon Fire, with a local/offline-first library, metadata preservation and controlled write-back, playlists, favorites, artwork, filesystem change detection, backups/restores, and a future cloud synchronization/community layer.

## Current source tree

- Python/FastAPI local API
- SQLite library database with schema migration/versioning
- Recursive audio scanner with SHA-256 identity
- Mutagen metadata engine
- Native Tkinter desktop client foundation
- Polling filesystem watcher
- Safe MP3 metadata write-back with timestamped backups
- Artwork extraction endpoint
- Playlist/favorite/rating/history foundations
- Album/artist/recently-played/queue desktop features
- Android Studio project with MediaStore discovery/search
- Android foreground playback-service foundation
- GitHub Actions workflow for debug APK builds
- GitHub Actions workflow for Windows builds
- Android APK build instructions in `docs/ANDROID_APK_BUILD.md`
- WordPress connector plugin in `wordpress/audiohardcore-integration/`
- WordPress setup instructions in `docs/WORDPRESS_INSTALL.md`
- Free Windows install/build scripts
- Portable project state for ChatGPT, Grok, and Perplexity

See `AH_PROJECT_STATE.md`, `docs/`, `CHANGELOG.md`, and `RELEASE_MANIFEST_0.9.json` for the authoritative development state.

## Build status

Automated Python tests: **9 passed** in the AH-MVP-0.9.0 development environment.

Generated Android APKs and Windows executables are intentionally not committed as source artifacts. GitHub Actions can build them as workflow artifacts; see the Android and Windows workflows under `.github/workflows/`.

## Free/open development

The current local-first MVP requires no paid API, subscription, or cloud service. Public hosting, TLS, cloud storage, payment processing, and production identity infrastructure are optional deployment concerns.

Do not commit personal music libraries, credentials, generated local databases, signing keys, or build artifacts.

## Android

Open `android/` in Android Studio for local development, or use **Actions → AudioHardcore Android APK → Run workflow** to generate a free debug APK artifact on GitHub-hosted runners.

## WordPress

Package `wordpress/audiohardcore-integration/` as a ZIP, then install it under **Plugins → Add New → Upload Plugin**. Configure the API under **Settings → AudioHardcore**, verify the connection, and add `[audiohardcore_library]` to a page/post. See `docs/WORDPRESS_INSTALL.md`.

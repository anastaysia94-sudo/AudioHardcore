# AudioHardcore

AudioHardcore is a free, local-first music library and media application in active development.

Current release: **AH-MVP-0.8.0**

The project targets Windows, macOS, Android, and Amazon Fire, with a local/offline-first library, metadata preservation and controlled write-back, playlists, favorites, artwork, filesystem change detection, backups/restores, and a future cloud synchronization/community layer.

## Current source tree

- Python/FastAPI local API
- SQLite library database
- Recursive audio scanner with SHA-256 identity
- Mutagen metadata engine
- Native Tkinter desktop client foundation
- Polling filesystem watcher
- Safe MP3 metadata write-back with timestamped backups
- Artwork extraction endpoint
- Playlist/favorite/rating/history foundations
- Album/artist/recently-played/queue desktop features
- Android Studio project with MediaStore discovery/playback
- Android APK build and release instructions in `docs/ANDROID_APK_BUILD.md`
- WordPress connector plugin in `wordpress/audiohardcore-integration/`
- WordPress setup instructions in `docs/WORDPRESS_INSTALL.md`
- Free Windows install/build scripts
- Portable project state for ChatGPT, Grok, and Perplexity

See `AH_PROJECT_STATE.md`, `docs/`, and `CHANGELOG.md` for the authoritative development state.

## Build status

Automated Python tests: **9 passed** in the AH-MVP-0.8 development environment.

Generated Android APKs and Windows executables are intentionally not committed as source artifacts. Build them locally using the documented scripts/toolchains.

## Free/open development

The current MVP requires no paid API, subscription, or cloud service. Do not commit personal music libraries, credentials, generated local databases, signing keys, or build artifacts.

## Android

Open `android/` in Android Studio. Use the debug APK flow for local testing or the signed release flow for distribution. See `docs/ANDROID_APK_BUILD.md`.

## WordPress

Install the connector under `wordpress/audiohardcore-integration/`, configure the AudioHardcore API URL under **Settings > AudioHardcore**, and add `[audiohardcore_library]` to a page/post. See `docs/WORDPRESS_INSTALL.md`.

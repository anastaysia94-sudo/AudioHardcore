# AudioHardcore

AudioHardcore is a free, local-first music library and media application in active development.

Current release: **AH-MVP-0.6**

The project targets Windows, macOS, Android, and Amazon Fire, with a local/offline-first library, metadata preservation and controlled write-back, playlists, favorites, artwork, filesystem change detection, backups/restores, and a future cloud synchronization/community layer.

## Current development package

- Python/FastAPI local API
- SQLite library database
- Recursive audio scanner with SHA-256 identity
- Mutagen metadata engine
- Native Tkinter desktop client foundation
- Polling filesystem watcher
- Safe MP3 metadata write-back with timestamped backups
- Artwork extraction endpoint
- Playlist/favorite/rating/history foundations
- Android Studio project with MediaStore discovery/playback
- Free Windows install/build scripts
- Portable project state for ChatGPT, Grok, and Perplexity

See `AH_PROJECT_STATE.md` and `docs/` for architecture and roadmap.

## Build status

Automated Python tests: **9 passed** in the AH-MVP-0.6 development environment.

The Android APK and Windows executable are not checked in as generated binaries; the project includes source and build instructions/scripts for producing them locally.

## Free/open development

The current MVP requires no paid API, subscription, or cloud service. Do not commit personal music libraries, credentials, generated local databases, or build artifacts.

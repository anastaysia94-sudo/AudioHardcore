# AudioHardcore Project State

**Project:** AudioHardcore  
**Architecture:** AH-ARCH-1.0  
**Build:** AH-MVP-0.8.0  
**Date:** 2026-09-05  
**Status:** Active development  
**Cost target:** 100% free/open-source development stack; no paid API/service is required by the current MVP.

## Confirmed requirements
- 1,800+ MP3 initial collection
- Windows, macOS, Android, Amazon Fire targets
- Metadata preservation and controlled write-back
- Local/offline-first library
- Future multi-device synchronization
- Website
- WordPress integration
- SMF/community integration
- Future monetization
- Modern music/social UX direction inspired by YouTube Music + Facebook information density/navigation without copying proprietary branding/assets

## Implemented
- SQLite local persistence
- Recursive audio scanner
- SHA-256 content identity
- Mutagen metadata extraction
- FastAPI local API
- Search, pagination, favorites, ratings
- Local media streaming
- Browser library UI
- Duplicate detection endpoint/UI
- Playlist CRUD + track management
- Safe MP3 metadata write-back with timestamped backups
- Embedded artwork endpoint
- Automatic re-scan after MP3 write-back
- Play-count/history foundation
- Dependency-free polling filesystem watcher
- Native Tkinter desktop client shell
- Desktop library search/filtering and context actions
- Album/artist/recently-played browse views
- Queue/next-track controls
- Metadata editor, playlist-add, folder-import, backup/restore UI
- Free Windows install script
- Free Windows PyInstaller build script
- Unified desktop launcher
- Native Android Studio project with MediaStore discovery/search/playback
- Android APK build/release documentation
- WordPress integration plugin foundation with settings and shortcode
- WordPress installation/integration documentation

## Tested
- `python -m compileall -q .`
- `pytest -q` → 9 passed

## Not yet production-complete
- Compiled Android APK artifact from this environment
- Production Windows/macOS packaging and signing
- Authentication/accounts
- Cloud backend
- Multi-device sync/conflict resolution
- Cloud/off-device music storage
- Full Android feature parity/background playback/media session
- Full WordPress administration/content integration
- SMF connector
- Payments/subscriptions
- Production updater

## Immediate next build
AH-MVP-0.9: Android feature parity, database migrations/versioning, production packaging workflows, authenticated cloud-sync API, richer WordPress integration, and SMF/account integration design.

## Truth labels
Implemented = code exists.  
Tested = automated/manual test executed.  
Verified = confirmed against external official source, device, or service.  
Planned = not implemented.

## Cross-AI handoff rule
ChatGPT, Grok, and Perplexity treat this file as the portable project state. Preserve explicit user decisions, distinguish facts from recommendations, and append meaningful changes after substantive development work.

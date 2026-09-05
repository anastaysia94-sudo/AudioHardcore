# AudioHardcore 0.9 Release

AudioHardcore 0.9 is a free/local-first release candidate with stronger reliability and build automation.

## Delivered

- SQLite schema migration/versioning.
- SQLite WAL mode for local concurrency.
- Android foreground playback service foundation.
- Android library filtering that preserves the full indexed dataset.
- GitHub Actions debug APK workflow.
- GitHub Actions Windows build workflow.
- WordPress connector and installation documentation.
- Free production-stack/deployment boundary documentation.

## Android APK

Use **Actions → AudioHardcore Android APK → Run workflow** and download the `audiohardcore-debug-apk` artifact. Or build locally from `android/` with Android Studio or Gradle; see `docs/ANDROID_APK_BUILD.md`.

## WordPress

Package `wordpress/audiohardcore-integration/` as a ZIP, upload it under **Plugins → Add New → Upload Plugin**, activate it, configure **Settings → AudioHardcore**, and use `[audiohardcore_library]`; see `docs/WORDPRESS_INSTALL.md`.

## Product boundary

Authentication/accounts, production cloud sync, SMF integration, signed release binaries, hosted deployment, and commercial billing are intentionally separate milestones. The source release does not pretend those operational services are already deployed.

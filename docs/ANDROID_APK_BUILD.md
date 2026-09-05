# AudioHardcore Android APK Build & Install

## Fastest free path: GitHub Actions

The repository includes `.github/workflows/android-apk.yml`.

1. Open the AudioHardcore GitHub repository.
2. Open **Actions**.
3. Select **AudioHardcore Android APK**.
4. Click **Run workflow**.
5. Open the completed workflow run.
6. Download the `audiohardcore-debug-apk` artifact.
7. Transfer `app-debug.apk` to your Android device and install it.

The workflow uses a GitHub-hosted runner with Java 17 and a pinned Gradle distribution. No paid build service is required.

## Local Android Studio build

Prerequisites:

- Android Studio with the Android SDK installed.
- A compatible JDK, using the version supported by the Android Gradle Plugin in `android/settings.gradle`.
- Internet access on the build machine for Gradle/Android dependencies.

Open the `android/` directory in Android Studio and let Gradle sync. Use **Build > Generate Bundle(s) / APK(s) > Generate APK(s)** for a debug build.

The output is normally:

```text
android/app/build/outputs/apk/debug/app-debug.apk
```

## Local command-line build

From `android/`:

```powershell
# Windows PowerShell
gradle assembleDebug
```

```bash
# macOS/Linux
gradle assembleDebug
```

The repository intentionally does not check in a downloaded Gradle distribution or Android SDK.

## Install with ADB

```bash
adb install -r app/build/outputs/apk/debug/app-debug.apk
```

Enable Developer Options and USB debugging first.

## Release APK / Play Store

1. Create and protect a private signing keystore.
2. Keep signing credentials outside source control.
3. In Android Studio choose **Build > Generate Signed Bundle / APK**.
4. Choose **APK** for direct distribution, or **AAB** for Google Play.
5. Store the signing key securely.

## Background playback

The Android source declares `mediaPlayback` foreground-service support. Android 14+ requires a matching foreground-service type and `FOREGROUND_SERVICE_MEDIA_PLAYBACK` permission for this use case. The current source includes that declaration and a playback-service foundation. citeturn242605search0turn242605search1

## Official references

- https://developer.android.com/build/build-for-release
- https://developer.android.com/build/building-cmdline
- https://developer.android.com/studio/run
- https://developer.android.com/develop/background-work/services/fgs/service-types

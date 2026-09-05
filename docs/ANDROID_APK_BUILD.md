# AudioHardcore Android APK Build & Install

## Prerequisites

- Android Studio with the Android SDK and a compatible JDK installed.
- Open the `android/` directory as an Android Studio project.
- Let Android Studio install/sync the required Gradle and Android Gradle Plugin components if prompted.

## Debug APK (free/local testing)

### Android Studio

1. Open `android/` in Android Studio.
2. Select the `app` module and a debug build variant.
3. Use **Build > Generate Bundle(s) / APK(s) > Generate APK(s)**.
4. The debug APK will be placed under `android/app/build/outputs/apk/`.

A debug APK is signed with the SDK debug key and can be installed directly on a device.

### Command line

From the `android/` directory:

```powershell
# Windows PowerShell
.\gradlew.bat assembleDebug
```

```bash
# macOS/Linux
./gradlew assembleDebug
```

If this repository checkout does not contain a Gradle wrapper yet, use the Gradle installation configured by Android Studio or generate the wrapper on the development machine with:

```bash
gradle wrapper
```

Then rerun `assembleDebug`.

## Install on a connected Android device

Enable Developer Options and USB debugging, connect the device, then:

```bash
adb install -r app/build/outputs/apk/debug/app-debug.apk
```

## Release APK

1. Create and protect a private signing keystore.
2. Keep signing credentials outside source control.
3. In Android Studio choose **Build > Generate Signed Bundle / APK**.
4. Choose APK for direct distribution.
5. Store the signing key securely.

For Google Play distribution, build an Android App Bundle (AAB) and use Play Console; Google Play generates optimized APKs for supported device configurations.

## AudioHardcore note

The current Android client is a local-library foundation. Cloud synchronization, unified accounts, background playback/media-session integration, richer artwork, and full desktop feature parity remain later release work.

## Official references

- https://developer.android.com/build/build-for-release
- https://developer.android.com/build/building-cmdline
- https://developer.android.com/studio/run

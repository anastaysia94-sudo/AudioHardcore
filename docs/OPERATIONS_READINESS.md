# AudioHardcore operations readiness

Snapshot: 2026-09-08

This document separates repository-controlled readiness from operator/device work. A green build does not prove that a specific Windows PC, Android phone, Fire tablet, DNS zone or backup destination behaves correctly.

## Already implemented

- `GET /health` opens the SQLite database and reports service/version/track count.
- `POST /backup` copies the current SQLite library database to an operator-selected destination.
- `POST /restore` creates a timestamped pre-restore copy before replacing the active database.
- SQLite uses migrations/versioning, WAL and a busy timeout.
- `scripts/verify_backup.py` opens a backup read-only, runs `PRAGMA integrity_check`, checks required tables and can enforce a maximum backup age.

## Production backup contract

A production operator should:

1. Create at least one automatic database backup on a predictable schedule.
2. Store at least one copy outside the application host/device.
3. Run `python scripts/verify_backup.py /path/to/backup.sqlite --max-age-hours 26` after the copy.
4. Alert when the verifier exits non-zero.
5. Perform a restore drill into a disposable environment after schema-changing releases and at least quarterly.
6. Never call a backup strategy complete merely because a file exists. A backup that cannot pass SQLite integrity checks or be restored is decorative storage.

## Monitoring contract

Minimum checks:

- `/health` returns HTTP 200 and `status=ok`.
- storage volume has adequate free space.
- automatic backup is recent and verified.
- process restart does not lose database state.
- media roots remain readable.
- auth/sync errors are monitored if public multi-user mode is enabled.

## Target-device QA matrix

| Target | Automated repo gate | Physical/operator gate |
|---|---|---|
| Windows | Windows packaging workflow | Launch package, scan real folder, play, edit, backup/restore |
| macOS | Python/core tests | Launch supported Python/Desktop path; media and permission QA |
| Android | Gradle APK workflow | Install, MediaStore scan, foreground playback, interruption/headphone QA |
| Fire OS | Android-compatible source path | Install on supported Fire hardware, storage/media permissions, playback QA |
| Linux | Python/core tests and Docker | Desktop audio backend and filesystem/media QA |
| Docker/server | Python tests + container config | HTTPS, durable volume, restart, backup/restore, monitoring |

## Release evidence

For each physical test record:

- device/model and OS version;
- build SHA/version;
- install/start result;
- library scan result;
- playback result;
- edit/write-back result where supported;
- backup + verifier result;
- restore-drill result where safe;
- known defects and screenshots/logs.

Do not label a target `Verified` until that evidence exists for a real device/environment.

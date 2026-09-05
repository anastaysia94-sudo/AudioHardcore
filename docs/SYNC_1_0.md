# AudioHardcore 1.0 synchronization foundation

AudioHardcore remains local-first. The sync service exchanges account/application state records, not raw music files.

Each change contains user, device, entity type, entity ID, field, JSON value, and timestamp.

Conflict policies supported by `core/sync.py`:
- `latest`
- `local`
- `remote`

Before public hosted rollout, add HTTPS, managed database infrastructure, refresh-token rotation, email verification/reset, rate limiting, audit logs, device revocation, retry/backoff, idempotency, monitoring, and complete client-side sync application logic.

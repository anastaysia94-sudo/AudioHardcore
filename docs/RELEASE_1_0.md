# AudioHardcore 1.0.0 foundation

AudioHardcore 1.0.0 establishes the account and synchronization foundation while preserving the local-first rule.

## Account endpoints
- `POST /auth/register`
- `POST /auth/login`
- `GET /account/me`
- `POST /devices`
- `GET /sync/changes`
- `POST /sync/changes`

Set `AUDIOHARDCORE_AUTH_SECRET` to a strong random value in any hosted deployment. The development fallback is not suitable for production.

Passwords use Python `hashlib.scrypt`. Access tokens are HMAC-signed project tokens.

## Sync model
Sync changes are append-only records keyed by user/device/entity/field and timestamp. `core/sync.py` supplies deterministic latest/local/remote conflict resolution helpers.

## Production hardening still required
HTTPS termination, managed production database, refresh-token rotation, email verification, password reset, rate limiting, audit logging, device revocation, idempotency and retry handling, monitoring, and full client-side sync application logic.

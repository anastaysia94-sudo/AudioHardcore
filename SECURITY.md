# Security

AudioHardcore is local-first and designed to be free to develop.

Never commit passwords, API secrets, signing keystores, personal music libraries, local SQLite databases, or production configuration containing credentials.

For hosted deployments:
- set `AUDIOHARDCORE_AUTH_SECRET` to a strong random secret
- terminate TLS at a trusted reverse proxy
- use a production database rather than exposing local SQLite
- add rate limiting, account recovery, audit logging, and device revocation before public launch

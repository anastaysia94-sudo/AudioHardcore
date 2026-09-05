# AudioHardcore Free Production Baseline

AudioHardcore is designed to be usable without paid APIs or subscriptions. The local-first desktop/mobile clients can operate against the local library and SQLite data store. A public cloud deployment is optional and requires a server/hosting environment of the operator's choice.

## Free local operation

- Python 3.11+
- SQLite
- Mutagen
- FastAPI/Uvicorn
- Tkinter desktop client
- Android Studio / Android SDK for Android builds
- GitHub for source control and optional CI

No paid API key is required for the current application.

## Production boundary

Public hosting, domain/DNS, TLS, transactional email, payment processing, cloud storage, and public authentication infrastructure are operational deployment concerns rather than mandatory local-MVP dependencies.

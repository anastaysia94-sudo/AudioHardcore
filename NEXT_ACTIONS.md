# NEXT ACTIONS

Updated: 2026-09-26 America/Los_Angeles

## Smallest next execution block
1. Locate the active Resonance staging PR and inspect/run `Resonance v0.1 PR Acceptance TEMP` against current main workflow source `c9bc513477c33a0e26521ef89b338270ab101d07`.
2. Verify checksum reconstruction, Rust fmt/tests/clippy, Flutter-Rust bridge generation, Flutter analysis/tests, Android APK/AAB, and Windows x64 release packaging.
3. Capture workflow/run and artifact evidence.
4. Keep the temporary harness until a green replacement or durable CI migration is verified.
5. If acceptance is green, run one real library-management workflow end to end and update STATUS.md.

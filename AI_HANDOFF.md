# AI Handoff — AudioHardcore / Resonance

Updated: 2026-09-26 America/Los_Angeles

## Identity

- Canonical repository: `anastaysia94-sudo/AudioHardcore`
- Master project reference: P036
- Portfolio index: `anastaysia94-sudo/anastaysia94-sudo` → `CROSS_LLM_BOOTSTRAP.md`
- Machine-readable register: `portfolio/PROJECTS.json`

## Purpose

Current repository home for Resonance Digital Audio OS / Collector and related audio-library work.

## Continuity rules

- Keep Resonance continuity here unless an explicit migration is completed.
- Preserve the temporary PR acceptance harness until a verified replacement/durable CI path exists; do not remove it merely because it is labeled TEMP.
- Historical chat summaries are context, not current verification.
- Inspect current PR/workflow state before changing the acceptance harness.
- Record changed files, exact workflow evidence, blockers, and rollback risk.

## Current source checkpoint

Current observed main head: `c9bc513477c33a0e26521ef89b338270ab101d07`.

Changes since the prior continuity snapshot are all in the temporary Resonance PR acceptance workflow:
- FRB `NoopSink` compatibility normalization was added/refined.
- `FilePicker.platform` compatibility is normalized to the newer API shape in the reconstructed source.
- `cargo-expand` is installed before Flutter-Rust bridge generation.
- Flutter analysis keeps informational lints non-fatal.
- The earlier fix that avoids re-running FRB project integration before generation remains intact.

The harness still builds/tests Rust + Flutter and attempts Android APK/AAB plus Windows x64 release artifacts from the fixed source payload.

## Verification boundary

The current Linux/Android and Windows acceptance results were not verified in this continuity refresh.

## Smallest next execution block

1. Inspect the active Resonance staging PR and run/result for the current temporary acceptance workflow.
2. Verify source checksum reconstruction, Rust quality gates, FRB generation, Flutter tests, Android APK/AAB build, and Windows x64 build.
3. Preserve the temporary harness until these checks are green or a verified replacement exists.
4. If green, verify one library-management workflow end to end and record implemented functions.

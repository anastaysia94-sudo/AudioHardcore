# DECISIONS

Updated: 2026-09-26

## Standing project decisions
- Resonance remains here unless deliberately split later.
- Do not remove the temporary acceptance workflow until a verified green replacement or durable CI migration exists.
- Compatibility normalization performed inside the temporary workflow is test/build scaffolding; do not silently treat it as canonical product-source repair without an explicit source change.
- Preserve checksum reconstruction and artifact evidence for Android and Windows acceptance.
- Another LLM or developer must begin with AI_HANDOFF.md and repository evidence.
- Never commit credentials, tokens, private customer data, or secrets.
- Record what changed, why, verification evidence, remaining blocker, and rollback risk after material work.

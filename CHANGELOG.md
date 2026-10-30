# Changelog

## 1.2.0 — 2026-10-31

- Clarified the Level 1/Level 2 boundary: Level 1 is strictly non-mutating across the complete request path; every test-data/state mutation requires Level 2.
- Required separate explicit approval for provider calls, invoice/payment creation, notifications, and other external effects.
- Added dependency-free automated Skill validation for required files, frontmatter, internal Markdown links, permission-policy wording, and permission-gate scenario outcomes.
- Added machine-readable permission-gate scenarios and a deterministic policy simulation harness.
- Added explicit reporting distinction between static validation, simulated policy tests, native Skill runtime execution, and Edge Function runtime tests.
- Updated README, core Skill policy, staged workflow, implementation/testing workflow, acceptance checklist, and verification report template.

## 1.1.0 — 2026-10-31

- Added a four-level, non-inheriting permission model for Supabase Edge Function audit, testing, test-data mutation, and implementation/deployment.
- Added a dedicated Edge Function testing workflow with explicit approval scope, invocation capability checks, side-effect classification, production safeguards, and evidence requirements.
- Updated the main skill, staged workflow, implementation/testing guidance, acceptance checklist, README, and verification report.

## 1.0.0 — 2026-10-31

- Initial modular Duitku POP + Supabase backend skill.
- Added staged, incremental official documentation audit workflow.
- Added six-area read-only Supabase audit scope.
- Added explicit approval gates for GitHub, Database, Edge Functions, secrets/configuration, and deployment/production changes.
- Added implementation, testing, security audit, and final verification workflows.
- Added audit, requirements, and verification report templates.
- Added mandatory Backend Ready acceptance checklist.

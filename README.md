# Duitku POP + Supabase Backend Skill

A modular Agent Skill for evidence-based, staged auditing and development of the Asri Collection Supabase backend for Duitku POP payments.

**Skill version:** 1.2.0

## Source of truth

- Duitku POP documentation (Indonesian): https://docs.duitku.com/pop/id/
- Duitku POP documentation (English): https://docs.duitku.com/pop/en/

Always re-check the current official documentation for the relevant contract before making implementation decisions.

## Repository structure

```text
.
├── SKILL.md
├── README.md
├── CHANGELOG.md
├── references/
│   ├── official-duitku-pop.md
│   └── supabase-audit-scope.md
├── workflows/
│   ├── staged-workflow.md
│   ├── documentation-audit.md
│   ├── supabase-audit.md
│   ├── edge-function-testing.md
│   └── implementation-testing.md
├── templates/
│   ├── audit-report.md
│   ├── requirements-report.md
│   └── verification-report.md
├── scripts/
│   └── validate_skill.py
└── tests/
    ├── acceptance-checklist.md
    └── permission-gate-scenarios.json
```

## Operating sequence

Documentation audit → Supabase audit → Requirements → Recommendations → Explicit approval → Implementation → Testing → Security audit → Final verification.

Audits are read-only by default. Changes to GitHub, Supabase Database, Edge Functions, secrets/configuration, and deployment/production integration require explicit, scope-specific approval.

## Edge Function testing permissions

The skill uses four separate, non-inheriting permission levels:

| Level | Mode | Boundary |
|---|---|---|
| 0 | Audit | Read-only inspection; no function invocation |
| 1 | Testing | Only demonstrably non-mutating invocation; existing fixture reads are allowed only when the full request stays read-only |
| 2 | Data Testing | Explicitly approved writes/updates/deletes to identified isolated test data |
| 3 | Implementation & Deployment | Only individually approved source/configuration changes and deployment actions |

**Level 1 vs Level 2:** classify the complete request path by actual side effects. Any database/application-state mutation requires Level 2, including temporary fixture writes and planned cleanup. Merely reading an existing fixture can remain Level 1 if the request does not mutate anything. Provider calls, invoice/payment creation, notifications, and other external effects require separate explicit approval.

Before invoking a function, approval must identify the project/ref, environment, function/endpoint, method, authentication, payload, test cases, side effects, and data/cleanup scope. Production tests and real external effects require separate explicit approval. Level 1 does not authorize mutation; Level 2 does not authorize source changes or deployment.

## Automated validation

Run with Python 3.9+ and no third-party dependencies:

```bash
python scripts/validate_skill.py
```

The validator checks required files, Skill frontmatter, internal Markdown links, key permission-boundary statements, scenario schema, and all permission-gate scenario outcomes. A successful result is static/documentation and policy-harness validation; it is not proof of native Agent Skill runtime behavior, Edge Function invocation, or backend readiness.

## Permission gate scenarios

The machine-readable cases are in `tests/permission-gate-scenarios.json`. They exercise read-only access, Level 0 invocation denial, Level 1 mutation denial, Level 2 isolated test-data writes, production restrictions, external-effect approval, and Level 3 scoped implementation/deployment.

## Use

Load `SKILL.md` as the skill entry point. Follow links to supporting references and workflow files as needed. Do not assume that the presence of this documentation proves the live Supabase project or Duitku configuration is ready.

## Readiness

Use the acceptance checklist in `tests/acceptance-checklist.md`. The status can be **Backend Ready** only when every mandatory criterion is verified with evidence.

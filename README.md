# Duitku POP + Supabase Backend Skill

A modular Agent Skill for evidence-based, staged auditing and development of the Asri Collection Supabase backend for Duitku POP payments.

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
│   └── implementation-testing.md
├── templates/
│   ├── audit-report.md
│   ├── requirements-report.md
│   └── verification-report.md
└── tests/
    └── acceptance-checklist.md
```

## Operating sequence

Documentation audit → Supabase audit → Requirements → Recommendations → Explicit approval → Implementation → Testing → Security audit → Final verification.

Audits are read-only by default. Changes to GitHub, Supabase Database, Edge Functions, secrets/configuration, and deployment/production integration require explicit, scope-specific approval.

## Use

Load `SKILL.md` as the skill entry point. Follow links to supporting references and workflow files as needed. Do not assume that the presence of this documentation proves the live Supabase project or Duitku configuration is ready.

## Readiness

Use the acceptance checklist in `tests/acceptance-checklist.md`. The status can be **Backend Ready** only when every mandatory criterion is verified with evidence.

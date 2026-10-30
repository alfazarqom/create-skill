---
name: duitku-pop-supabase-backend
description: Audit, design, implement with explicit approval, test, secure, and verify an Asri Collection Supabase backend for Duitku POP payments. Use when working on official Duitku POP documentation, Supabase Database, RLS, SQL functions/RPC, Edge Functions, secrets/configuration, callback processing, invoice creation, payment reconciliation, or backend readiness.
---

# Duitku POP + Supabase Backend Skill

## Purpose

Guide the user through evidence-based, staged work to audit and prepare the Asri Collection Supabase backend for Duitku POP until it meets the agreed **Backend Ready** criteria. The official Duitku POP documentation is the provider-contract source of truth:

- Indonesian: https://docs.duitku.com/pop/id/
- English: https://docs.duitku.com/pop/en/

Do not treat this skill, prior chat context, examples, or existing code as a substitute for checking the current official documentation.

## Agreed operating model

- Use a **modular skill**: this file is the entry point; detailed procedures live in `references/`, `workflows/`, `templates/`, and `tests/`.
- Audit the official documentation **incrementally**, one contract area at a time. Record evidence and resolve material ambiguities before marking an area verified.
- Audit all six Supabase areas: Database; Security & RLS; Database Functions & RPC; Edge Functions; Secrets & Configuration; Testing & Logs.
- Follow the staged workflow: documentation audit → Supabase audit → requirements → recommendations → explicit approval → implementation → testing → security audit → final verification.
- Default to read-only. Never infer approval.
- Explicit approval is required before any change to GitHub repository files, Supabase database, Edge Functions, secrets/configuration, deployment, or production integration.
- Approval applies only to the named change group and scope. Stop and request new approval if scope expands.
- Never expose secret values, API keys, signatures containing sensitive data, access tokens, raw authorization headers, or unnecessary customer/payment data.
- Never claim an audit, test, fix, or deployment succeeded without observable evidence.

## Required initial checks

At the beginning of each task:

1. Identify the requested stage and expected output. Do not silently skip stages.
2. Confirm the authenticated GitHub repository, owner/name, branch, and commit when repository work is involved.
3. Confirm the active Supabase connection and exact project ref before any Supabase inspection or action. Do not rely on remembered project identifiers as proof of current connection.
4. Determine whether the integration uses the Duitku POP embedded JavaScript flow or payment URL/window redirection. Do not silently switch modes.
5. Confirm the intended environment (Sandbox or Production). Prefer Sandbox for tests.
6. Open the current official Duitku POP documentation sections relevant to the task. Record URL, section, date checked, and exact contract evidence.
7. If required GitHub or Supabase access fails, stop the audit dependent on that access and report the failure. Do not infer missing state.

## Workflow

Follow `workflows/staged-workflow.md`. Detailed stage procedures:

- Documentation: `workflows/documentation-audit.md`
- Supabase: `workflows/supabase-audit.md`
- Implementation, testing, and verification: `workflows/implementation-testing.md`

Do not proceed to implementation merely because an audit is complete. First present verified findings, recommendations, exact requirements, and a scoped change plan; then wait for explicit approval.

## Six Supabase audit areas

Inspect all areas within the authorized audit scope:

1. **Database** — actual tables, columns, types, relationships, constraints, indexes, views, migration history, and relevant data invariants.
2. **Security & RLS** — RLS enabled state, policies, grants, roles, exposed schemas, least privilege, and guest/customer access boundaries.
3. **Database Functions & RPC** — functions, triggers, RPCs, execution grants, `SECURITY DEFINER`, fixed `search_path`, authorization, atomicity, and state transitions.
4. **Edge Functions** — inventory, source, config, JWT behavior, callers, request validation, provider requests, callback handling, error handling, and deployment state where observable.
5. **Secrets & Configuration** — names, presence/absence, environment mapping, and safe usage only. Never retrieve, print, copy, or request secret values in chat.
6. **Testing & Logs** — available logs, sanitized error patterns, test coverage, sandbox results, negative cases, and evidence limits.

Discover the actual schema and function names. Do not assume tables or functions exist because a prior plan mentioned them. Do not create duplicate payment tables, RPCs, inventory ledgers, or Edge Functions without evidence and approval.

## Payment security invariants

Apply the current official POP contract and the project's verified data model. At minimum:

- Generate provider request signatures only on the server using the current documented HMAC-SHA256 contract. Never place the API key in frontend code.
- Parse the documented callback content type correctly and verify its signature server-side before processing.
- Match callback merchant code, merchant order ID, amount, provider reference, environment, and existing transaction.
- Do not trust browser JS callbacks, return URL query parameters, or redirects as proof of payment. Use them only for customer-facing navigation/status refresh.
- Make callback handling idempotent and protect state changes against duplicate and concurrent events.
- Apply payment/order/inventory transitions atomically where practical, or document a durable retry/reconciliation strategy.
- Keep order, payment, and shipment states distinct.
- Derive authoritative prices and totals from trusted backend/database data, not client-supplied totals.
- Fail closed when required credentials are absent or signature validation fails.
- Do not invent undocumented status endpoints, fields, response codes, retry behavior, or expiry semantics.
- Do not perform real payments or production mutations without explicit, specific approval.

See `references/official-duitku-pop.md` and `references/supabase-audit-scope.md`.

## Evidence and reporting

Use Indonesian by default. Label every finding:

- **Terverifikasi** — directly supported by current source/tool evidence.
- **Indikasi** — plausible interpretation that needs further confirmation.
- **Belum terverifikasi** — access, evidence, or test is unavailable.

Separate repository state from deployed state; static inspection from runtime tests; Sandbox from Production; and facts from hypotheses. Use the report templates in `templates/`.

## Backend Ready gate

The backend may be declared **Backend Ready** only when every required criterion passes with evidence:

1. Relevant official Duitku POP documentation has been audited and verified, including material ambiguities.
2. Database structure and invariants match approved requirements.
3. Edge Functions implement the verified provider contract and expected business behavior.
4. Request and callback HMAC-SHA256 signature handling is correct for the current documented contract.
5. Callback processing is secure, correctly matched, idempotent, and concurrency-safe.
6. RLS, grants, RPC privileges, secrets, and environment configuration pass security review.
7. Required tests pass, including negative, duplicate, replay, and failure-path tests.
8. Security audit has no unresolved blocking findings.
9. Final verification records reproducible evidence and clearly lists any non-blocking limitations.

If any required criterion is failed or unverified, report **Belum Backend Ready**. Do not downgrade a required criterion to make the status pass. Production readiness and real-payment proof are separate release activities and require explicit authorization.

## Boundaries

This skill audits and prepares the Supabase backend for Duitku POP. Do not change frontend architecture, business rules, shipping, stock, checkout, or order behavior unless those are explicitly included in an approved change scope. Do not deploy, rotate secrets, run destructive SQL, alter production data, or execute real payments without specific approval.

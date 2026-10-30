# Staged Workflow

Follow the stages in order. A stage may be repeated if findings require it. Do not skip an approval gate.

## Stage 0 — Access and scope confirmation

- Confirm task scope, repository, branch, Supabase project ref, environment, and access.
- Confirm the current POP integration mode (embedded JS or payment URL redirection).
- Record unavailable tools/access.
- Do not start mutations.

**Exit:** scope and access are recorded; required access is available.

## Stage 1 — Incremental official documentation audit

- Audit one POP contract area at a time using `documentation-audit.md`.
- Map each provider rule to the existing implementation or mark it missing/unknown.
- Record ambiguities and resolve them before relying on an assumption.

**Exit:** all documentation areas relevant to the requested payment flow are verified or explicitly blocked with an open question.

## Stage 2 — Supabase audit

- Inspect all six areas in `references/supabase-audit-scope.md`.
- Discover actual schema, policies, functions, Edge Functions, safe configuration metadata, tests, and logs.
- Compare GitHub source/migrations with connected project state where access permits.

**Exit:** current-state inventory and evidence-based findings are complete; unavailable checks are identified.

## Stage 3 — Requirements

- Convert verified documentation and audit findings into testable backend requirements.
- Distinguish mandatory provider contract, existing business rules, technical design choices, and unresolved questions.
- Do not invent business rules or silently alter approved behavior.

**Exit:** requirements are traceable to official docs, verified current state, or explicit user decisions.

## Stage 4 — Recommendations

- Present minimal practical options and a preferred recommendation.
- Explain impact, risks, dependencies, and what remains unverified.
- No implementation in this stage.

**Exit:** a scoped implementation plan is ready for approval.

## Stage 5 — Explicit approval gate

For each change group, list exact files, SQL objects, Edge Functions, secrets/configuration, environment, tests, risks, and rollback/recovery plan.

Approval must be explicit and scoped. The following always require approval:
- GitHub repository changes.
- Supabase Database changes.
- Edge Function changes.
- Secrets and configuration changes.
- Deployment or production integration.
- Edge Function invocation when it may cause writes or external side effects.

Approval for one group does not authorize another. Apply the permission levels in `edge-function-testing.md`:
- Level 0: audit/read-only; no invocation.
- Level 1: invoke only approved non-mutating tests or use an already-approved isolated test fixture.
- Level 2: approved test-data writes/updates/deletes and tests that produce those test-data side effects.
- Level 3: specifically approved source/configuration changes and deployment.

Before Level 1 or higher, record project/ref, environment, function/endpoint, method, auth, payload, test cases, side effects, and data/cleanup scope. Production tests and real external effects require separate explicit approval. Permissions are non-inheriting.

**Exit:** exact proposed action and permission level are approved.

## Stage 6 — Implementation

- Implement only the approved scope.
- Keep changes small and reviewable.
- Preserve existing architecture and business rules unless explicitly included.
- Never expose secrets or add credentials to the repository.
- Do not deploy unless deployment is separately approved under Level 3.

**Exit:** approved changes are complete and diff is reviewable.

## Stage 7 — Testing

- Follow `edge-function-testing.md` before invoking any Edge Function.
- Start from Level 0; use Sandbox and isolated test fixtures by default.
- Level 1 permits only approved non-mutating tests or tests using already-approved isolated fixtures. Any test that writes test data requires Level 2.
- Production invocation, real payments, provider-side invoice creation, notifications, and other external effects require separate explicit approval naming the exact action and impact.
- Use only a supported invocation mechanism. If none is available, mark runtime test **Not Run** and explain the limitation.
- Test positive, negative, duplicate, replay, concurrency, and partial-failure paths as relevant.
- Record expected/actual results, environment, redacted request/response evidence, observed side effects, and cleanup status.
- Stop if actual effects exceed the approved scope. Do not clean up test data unless cleanup was approved.

**Exit:** actual results and evidence are recorded; failures are not hidden.

## Stage 8 — Security audit

- Re-check RLS, grants, RPC privileges, secrets handling, callback verification, idempotency, authorization, logs, and environment separation.
- Verify no unapproved scope drift occurred.

**Exit:** no unresolved blocking security finding; otherwise report blocked.

## Stage 9 — Final verification and readiness

- Verify the approved diff, actual database/function state, test results, and official POP contract mapping.
- Use `tests/acceptance-checklist.md`.
- Report **Backend Ready** only if every mandatory criterion is verified.

**Exit:** a final report includes evidence, limitations, and a truthful readiness status.

## Stop conditions

Stop the affected workflow and report when:
- Required GitHub or Supabase access fails.
- The official documentation is unavailable or materially ambiguous.
- The live project/environment cannot be identified.
- An unapproved change is required.
- A test would cause a real payment or production mutation without approval.
- No supported invocation mechanism is available for a requested runtime test.
- A critical mismatch or security issue makes continued execution unsafe.

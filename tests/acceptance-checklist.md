# Backend Ready Acceptance Checklist

All mandatory items must be checked with evidence. An unchecked or unverified mandatory item means **Belum Backend Ready**.

## Permission and authorization

- [ ] Permission level (0–3) is recorded and matches the action performed.
- [ ] Level 1+ approval identifies project/ref, environment, function/endpoint, method, auth, payload, test cases, side effects, and data/cleanup scope.
- [ ] Permission levels are separate and non-inheriting.
- [ ] Level 1 request paths are demonstrably non-mutating, including no external effects; existing fixture reads are allowed only when read-only.
- [ ] Every test-data write/change has explicit Level 2 approval and an identified isolated data boundary.
- [ ] Planned cleanup is explicitly included in Level 2 approval; cleanup is not assumed.
- [ ] Provider calls, invoice/payment creation, notifications, and other external effects have separate explicit approval.
- [ ] Source/configuration changes and deployment actions have separate, specific Level 3 approval.
- [ ] Production tests have separate per-test explicit approval.
- [ ] No secrets or unnecessary personal/payment data were exposed.

## Skill repository validation

- [ ] `python scripts/validate_skill.py` passes.
- [ ] Required Skill files and frontmatter are present.
- [ ] Internal Markdown links resolve.
- [ ] Permission gate scenarios pass the automated policy harness.
- [ ] Simulation results are not represented as native Skill runtime or Edge Function runtime evidence.

## Documentation contract

- [ ] Current official Duitku POP documentation reviewed for every relevant flow.
- [ ] Create Invoice endpoint, method, content type, headers, fields, and response verified.
- [ ] Request signature formula, timestamp, key, encoding, and parameter order verified.
- [ ] HTTP callback content type, fields, signature, and acknowledgement verified.
- [ ] JS callback and return URL are not treated as payment proof.
- [ ] Status-code ambiguity and undocumented behavior are resolved or explicitly block readiness.
- [ ] Error, retry, duplicate request, and expiry behavior are mapped from current docs.

## Database

- [ ] Actual schema matches approved requirements.
- [ ] Constraints/indexes enforce critical uniqueness and consistency.
- [ ] Order/payment/inventory relationships and state transitions are understood.
- [ ] No duplicate or unused payment mechanisms were introduced.
- [ ] Repository migrations and deployed database state are reconciled.

## Edge Functions

- [ ] Invoice creation validates inputs and derives amount from trusted state.
- [ ] Request signature and environment selection match official docs.
- [ ] Provider HTTP status and business status are handled separately.
- [ ] Callback parser matches documented content type.
- [ ] Callback verifies signature and transaction mapping before mutation.
- [ ] Browser return/JS callback cannot mutate authoritative payment state.
- [ ] Failures are safely handled and recoverable.
- [ ] Invocation mechanism was available and documented for every claimed runtime test.
- [ ] Tests not actually invoked are marked **Not Run**, not Pass.
- [ ] Observed side effects match approved scope; test data cleanup status is recorded.

## Security & RLS

- [ ] RLS policies and grants are least-privilege.
- [ ] RPC execution privileges and SECURITY DEFINER functions are safe.
- [ ] Callback processing is idempotent and concurrency-safe.
- [ ] Customer/guest access is limited to authorized data.
- [ ] Secrets remain server-side and are not exposed in logs/repository/frontend.
- [ ] Rate limiting and abuse protections are verified where required.

## Testing

- [ ] Positive Sandbox invoice flow tested.
- [ ] Valid and invalid signature cases tested.
- [ ] Invalid amount/order/reference/merchant cases tested.
- [ ] Duplicate, replay, and concurrent callback cases tested.
- [ ] Provider/database partial failure cases tested.
- [ ] Expiry/cancellation/payment race tested where relevant.
- [ ] Inventory side effects occur at most once and follow approved business rules.
- [ ] Actual results and reproducible evidence recorded.

## Security audit and final verification

- [ ] No unresolved blocking security findings.
- [ ] Approved change scope matches actual diff and deployed state.
- [ ] Tests and environment clearly identified.
- [ ] Rollback/recovery path documented for consequential changes.
- [ ] All remaining limitations and unverified items disclosed.

## Decision

- [ ] **Backend Ready** — every mandatory criterion passed with evidence.
- [ ] **Belum Backend Ready** — at least one mandatory criterion failed or remains unverified.

Do not mark Backend Ready based only on code generation, a successful build, an HTTP 200 response, or a browser redirect.

# Backend Ready Acceptance Checklist

All mandatory items must be checked with evidence. An unchecked or unverified mandatory item means **Belum Backend Ready**.

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

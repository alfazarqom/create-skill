# Implementation, Testing, and Verification

## Before implementation

Produce a scoped plan containing:
- Verified problem statement and evidence.
- Exact files and repository branch.
- Exact database objects/migrations.
- Exact Edge Functions and endpoint behavior.
- Provider contract references and API fields affected.
- Security/business impact.
- Tests and expected outcomes.
- Rollback/recovery plan.
- Environment and whether any provider call or customer data is involved.

Wait for explicit approval of this exact scope.

## Implementation rules

- Change only approved files/objects.
- Preserve existing schema and naming conventions where sound.
- Do not add duplicate payment tables, functions, or stock mechanisms.
- Keep provider network calls outside database transactions unless a documented architecture specifically requires otherwise.
- Persist provider references and payment state consistently.
- Use integer IDR amounts; do not use floating-point currency arithmetic.
- Keep API credentials server-side.
- Validate request data and derive authoritative totals from trusted database state.
- Validate callbacks before state mutation.
- Use atomic, conditional state transitions and idempotency protections.
- Do not silently change customer checkout, shipping, stock, or order business rules.
- Do not deploy without separate explicit deployment approval.

## Minimum invoice tests

- Valid Sandbox request and provider response.
- Correct request signature using current docs.
- Missing/invalid credentials fail closed.
- Invalid payload and invalid amount rejected.
- Duplicate/concurrent requests for same merchant order ID.
- Provider HTTP error vs provider business error handled distinctly.
- Provider success followed by local persistence failure is recoverable and not represented as a fabricated success.
- No secrets or internal diagnostics returned to the browser.

## Minimum callback tests

- Correct content-type parsing.
- Valid signature accepted.
- Missing/invalid signature rejected.
- Wrong merchant code, amount, merchant order ID, reference, or environment rejected.
- Unknown transaction rejected safely.
- Duplicate callback and replay do not apply effects twice.
- Concurrent callbacks cannot double-transition state.
- Invalid/unsupported result code does not get guessed.
- Correct documented acknowledgement only after safe processing.
- Database/RPC failure remains retryable/reconcilable.

## State and inventory tests

Where the existing business model includes inventory effects:
- Payment success updates the correct order/payment once.
- Failed/expired/cancelled flow follows the approved stock model.
- Callback vs expiry/cancellation race is safe.
- Concurrent purchases cannot oversell.
- Refund status is not treated as proof that a provider refund occurred.
- Order, payment, and shipment states remain separate.

## Security verification

- RLS and grants are least-privilege.
- RPC execute permissions and SECURITY DEFINER functions are reviewed.
- Secrets are server-side and values are never exposed.
- Browser callback/redirect cannot mark an order paid.
- Guest tracking reveals only approved minimal data.
- Rate limiting and abuse protections are verified where required.
- Logs do not contain secrets or unnecessary personal data.

## Final verification

Re-run the acceptance checklist. Report exact tests run, environment, expected/actual result, logs or command evidence, commit SHA, migration/function deployment evidence where applicable, and remaining limitations.

A code change is not proof of deployment. A successful HTTP request is not proof of provider payment success. A Sandbox pass is not proof of Production readiness.

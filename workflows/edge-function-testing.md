# Supabase Edge Function Testing & Permission Levels

## Purpose

Define permission gates for invoking Supabase Edge Functions during tests. This workflow governs test execution only; it does not grant permission to edit source, change configuration, mutate production data, deploy, or cause external effects.

## Permission levels

Permissions are separate and non-inheriting. Approval for one level does not authorize another.

| Level | Mode | Allowed actions | Not included |
|---|---|---|---|
| 0 | Audit | Read project/function metadata, source, safe configuration metadata, and available logs | Any function invocation; data/source/configuration changes |
| 1 | Testing | Invoke an identified function only for a request proven non-mutating, with no external side effect, under an approved request/test scope | Any database/state write, fixture creation/update/deletion, provider call, invoice/payment, notification, source/configuration change, or deployment |
| 2 | Data Testing | Create/update/delete only identified isolated test records and invoke approved tests whose only state mutations are confined to those records | Production data, unlisted records, source/configuration changes, deployment, or external effects not separately approved |
| 3 | Implementation & Deployment | Perform only individually listed source changes, configuration changes, and/or deployment actions in the named environment | Any unlisted file, function, project, environment, production action, data mutation, or real payment |

### Decisive Level 1 vs Level 2 rule

Classify by the **actual side effect of the request**, not by the test's label or intention:

- **Level 1:** the complete request path is demonstrably read-only/non-mutating. It may read an already-existing fixture, but must not create, update, delete, reserve, consume, or otherwise change any record or state. It must not call an external provider or trigger a notification.
- **Level 2:** the request path writes or changes any database record or other application state, even when the target is a test fixture, the change is temporary, or cleanup is planned. Level 2 approval must identify the exact isolated test records/data boundary and explicitly include each write operation and any cleanup.
- Merely using an existing isolated fixture does **not** make a mutating request Level 1. Reading an existing fixture is Level 1 only when the entire request remains non-mutating.
- If side effects are unknown, cannot be ruled out, or extend beyond the approved test-data boundary, do not invoke. Resolve the uncertainty or report **Blocked**.
- Provider calls, invoice creation, payments, notifications, and other external effects require separate explicit approval naming the exact effect, provider/environment, and expected impact. Level 2 alone does not authorize them.

Level 3 is not blanket authorization. Source changes, configuration changes, and deployment must each be listed in the approved scope. Secret values must never be retrieved, displayed, copied into chat, or committed.

## Required approval record before Level 1 or higher

Obtain explicit user approval that identifies:

1. Supabase project name/ref and authenticated connection.
2. Environment: local, development, staging, Sandbox, or Production.
3. Exact Edge Function name and endpoint.
4. HTTP method, required headers/authentication method, and payload/test fixture.
5. Exact test cases and expected outcomes.
6. Whether the function can write data, call external providers, send messages, create invoices, or trigger other side effects.
7. Data scope and cleanup plan, if any.
8. Any external provider call or customer data involved.

If any item is unknown and materially affects safety, stop and clarify. Do not infer approval from a general request to audit, test the repository, or make the backend ready.

## Execution rules

- Start at Level 0. Confirm project identity, function existence, source, auth/JWT behavior, environment, and available invocation mechanism.
- Use Sandbox or an isolated non-production environment by default.
- Use only an available, supported HTTP invocation mechanism. A Supabase management tool that can list/read/deploy functions does not by itself prove runtime invocation is available.
- Classify the complete request path before invocation. If it mutates database/application state, require Level 2 and identified isolated test data. If it causes external effects, require separate explicit approval for each effect.
- Level 1 must not bypass RLS, authorization, rate limits, or normal request validation.
- Never use real customer records or real payment credentials for routine tests. Never initiate a real payment without separate explicit approval naming provider, environment, amount, and transaction purpose.
- Production tests require separate, per-test explicit approval naming production project, function, exact request, expected impact, monitoring, and recovery plan. A generic Level 1 or Level 2 approval is not production authorization.
- Never print secrets, access tokens, raw authorization headers, full signatures containing sensitive material, or unnecessary personal/payment data. Use redacted evidence.
- Record timestamp, project ref, environment, function, redacted request/response, observed side effects, expected vs actual result, and evidence source.
- Stop on unexpected writes, unexpected provider calls, wrong environment, authentication bypass, data leakage, or any impact outside approved scope.
- Do not clean up test data unless cleanup was explicitly included in Level 2 approval.

## Decision and reporting

For every test, report:
- Permission level and exact approval scope.
- Project/environment/function and invocation mechanism.
- Test case, expected result, actual result, and Pass/Fail/Blocked/Not Run.
- Side effects observed and test-data cleanup status.
- Redactions and evidence limitations.

A request that was not actually invoked is **Not Run**, not Pass. Static source inspection and simulated permission-policy tests are not Edge Function runtime tests. HTTP 2xx alone is not proof that the business operation succeeded.

## Stop conditions

Stop and request new approval when:
- Project, environment, function, or endpoint differs from approved scope.
- A request may write data but only Level 1 is approved.
- The test may create a real invoice/payment, send an external notification, or affect a customer without separate approval.
- No supported invocation mechanism is available.
- Function side effects cannot be determined with reasonable confidence.
- A test requires source/configuration changes or deployment.

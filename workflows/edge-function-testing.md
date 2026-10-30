# Supabase Edge Function Testing & Permission Levels

## Purpose

Define the permission gates for invoking Supabase Edge Functions during tests. This workflow governs test execution only; it does not grant permission to edit source, change configuration, mutate production data, or deploy.

## Permission levels

Permissions are separate and non-inheriting. Approval for one level does not authorize another.

| Level | Mode | Allowed actions | Not included |
|---|---|---|---|
| 0 | Audit | Read project/function metadata, source, safe configuration metadata, and available logs | Invoking functions; changing data, source, or configuration |
| 1 | Testing | Invoke an identified function with an approved test request when the test is demonstrably non-mutating or uses an already-approved isolated test fixture | Creating/changing/deleting database records; source/configuration changes; deployment; real payments |
| 2 | Data Testing | Create, update, or delete explicitly identified test records and run approved tests that produce those test-data side effects | Production data changes unless separately and explicitly authorized; source/configuration changes; deployment |
| 3 | Implementation & Deployment | Change approved source/configuration and deploy the specifically named function to the specifically named environment | Any unlisted file, function, project, environment, production action, or real payment |

Level 3 is not a blanket authorization. Source changes, configuration changes, and deployment must each be listed in the approved change scope. Secret values must never be retrieved, displayed, copied into chat, or committed.

## Required approval record before Level 1 or higher

Obtain explicit user approval that identifies:

1. Supabase project name/ref and the authenticated connection.
2. Environment: local, development, staging, Sandbox, or Production.
3. Exact Edge Function name and endpoint.
4. HTTP method, required headers/authentication method, and payload/test fixture.
5. Exact test cases and expected outcomes.
6. Whether the function can write data, call external providers, send messages, create invoices, or trigger other side effects.
7. Data scope and cleanup plan, if any.
8. Whether any external provider call or customer data is involved.

If any item is unknown and materially affects safety, stop and clarify. Do not infer approval from a general request to audit, test the repository, or make the backend ready.

## Execution rules

- Start at Level 0. Confirm project identity, function existence, source, auth/JWT behavior, environment, and available invocation mechanism.
- Use Sandbox or an isolated non-production environment by default.
- Use only an available, supported HTTP invocation mechanism. A Supabase management tool that can list/read/deploy functions does not by itself prove that it can invoke them. If no invocation tool is available, report the limitation; do not claim a runtime test.
- Before invoking, classify the function's side effects. If it can mutate database records or other state, Level 2 approval and isolated test data are required. If it can call a payment provider, send notifications, or cause other external effects, obtain specific approval for that effect as well.
- Level 1 must not be used to bypass RLS, authorization, rate limits, or normal request validation.
- Never use real customer records or real payment credentials for routine tests. Never initiate a real payment without a separate explicit approval naming the provider, environment, amount, and transaction purpose.
- Production tests require a separate, per-test explicit approval naming the production project, function, exact request, expected impact, monitoring, and recovery plan. A generic Level 1 or Level 2 approval is not production authorization.
- Never print secrets, access tokens, raw authorization headers, full signatures containing sensitive material, or unnecessary personal/payment data. Use redacted evidence.
- Record timestamp, project ref, environment, function, request case (redacted), response status/body (redacted), observed side effects, expected vs actual result, and evidence source.
- Stop on unexpected writes, unexpected provider calls, wrong environment, authentication bypass, data leakage, or any impact outside the approved scope.
- Do not clean up test data unless cleanup was explicitly included in the Level 2 approval.

## Decision and reporting

For every test, report:
- Permission level and the exact approval scope.
- Project/environment/function and invocation mechanism.
- Test case, expected result, actual result, and Pass/Fail/Blocked.
- Side effects observed and test-data cleanup status.
- Redactions and evidence limitations.

A request that was not actually invoked is **Not Run**, not Pass. Static source inspection is not runtime testing. HTTP 2xx alone is not proof that the business operation succeeded.

## Stop conditions

Stop and request new approval when:
- The project, environment, function, or endpoint differs from the approved scope.
- The test requires writes but only Level 1 is approved.
- The test may create a real invoice/payment, send an external notification, or affect a customer.
- No supported invocation mechanism is available.
- The function's side effects cannot be determined with reasonable confidence.
- A test would require source/configuration changes or deployment.

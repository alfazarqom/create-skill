# Supabase Audit Scope

Audit the connected Supabase project in read-only mode by default. Confirm the exact project ref and connection before querying. The actual connected database is the source of truth for live schema and policies; repository migrations are evidence of intended/committed changes, not proof of deployed state.

## 1. Database

Inventory the actual objects relevant to orders and payments:

- Tables, columns, data types, nullability, defaults, generated columns.
- Primary keys, foreign keys, unique/check constraints, indexes.
- Views and materialized views.
- Migration history and schema drift against repository migrations.
- Relevant enums/domains and extensions.
- Data invariants and relationships among orders, order items, payment transactions, stock, and reservations if those objects exist.

Do not assume names or create a parallel schema. Discover the current model first.

## 2. Security & RLS

Inspect:

- RLS enabled/forced state for relevant tables.
- Policies by command, role, predicate, and check expression.
- Grants to PUBLIC, anon, authenticated, service roles, and custom roles.
- Exposed schemas and views.
- Guest checkout/tracking access boundaries and object-level authorization.
- Whether customer-facing endpoints can read or mutate another customer's order.
- Whether service-role credentials remain server-side.

Do not disable RLS or broaden grants to bypass an error.

## 3. Database Functions & RPC

Inspect:

- SQL and PL/pgSQL functions, triggers, RPC entry points, and dependencies.
- Function owner, volatility, argument/result types, and execution privileges.
- `SECURITY DEFINER` use, fixed `search_path`, schema qualification, and authorization checks.
- Atomic payment/order/inventory state transitions.
- Idempotency and concurrency controls.
- Whether privileged functions are callable by unintended roles.

Do not introduce RPCs or triggers until existing behavior and grants are understood.

## 4. Edge Functions

Inventory relevant functions and callers:

- Invoice creation and order/payment initialization.
- Duitku HTTP callback receiver.
- Status display or reconciliation, if present and documented.
- Expiry, cancellation, refund, and tracking flows if in scope.
- Request validation, body parsing, error handling, CORS, JWT verification configuration, and rate limiting.
- Provider URL/environment selection and secret access.
- Database writes and RPC invocation.
- Frontend or other backend callers and response assumptions.

A deployed function is not proof of correct behavior. Compare source, deployed version/configuration, logs, and actual tests where access permits.

## 5. Secrets & Configuration

Only inspect safe metadata:

- Expected secret/configuration names.
- Presence/absence when the platform exposes safe presence metadata.
- Sandbox/Production environment mapping.
- Whether secrets are referenced only in server-side code.
- Whether frontend build variables, logs, repository files, migrations, or reports expose credentials.

Never retrieve or print values. Never ask the user to paste a secret into chat. Never rotate, replace, add, or delete secrets without explicit approval.

## 6. Testing & Logs

Inspect only logs and records necessary for the task, and redact sensitive data:

- Edge Function invocation/error logs.
- Database logs and available advisor findings.
- Build, lint, type-check, and automated test results where applicable.
- Sandbox invoice and callback evidence.
- Failure, replay, concurrency, and retry cases.
- Timestamp range, environment, and correlation identifiers.

Absence of logs is not proof of success. If access is unavailable, mark the check **Belum terverifikasi**.

## Required evidence labels

- **Terverifikasi** — directly observed in the connected project, repository, official docs, or executed test.
- **Indikasi** — inferred from partial evidence; needs confirmation.
- **Belum terverifikasi** — unavailable or not yet tested.

## Minimum security invariants

- Merchant API key is server-only.
- Provider request and callback signatures follow the current POP documentation exactly.
- Callback validation includes signature and transaction association checks.
- Browser callback/redirect cannot directly mutate authoritative payment state.
- Amount and merchant order ID are matched against trusted database state.
- Duplicate/replayed callbacks cannot apply payment or inventory effects twice.
- Privileged database functions have narrow grants and explicit authorization.
- No secrets or unnecessary personal data appear in logs or reports.

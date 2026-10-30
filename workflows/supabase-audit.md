# Supabase Read-only Audit Workflow

## Preconditions

- Confirm active Supabase connection and exact project ref.
- Confirm audit environment and read-only scope.
- Identify the available Supabase tools and their limitations.
- If connection or project identity cannot be verified, stop and report.

## Audit sequence

### A. Database inventory

1. List relevant schemas and objects.
2. Inspect tables/columns/types/nullability/defaults.
3. Inspect primary/foreign/unique/check constraints and indexes.
4. Inspect views, enums, triggers, and migration history.
5. Map actual order, item, payment, stock, and reservation relationships if present.
6. Compare deployed state with repository migrations; report drift without changing it.

### B. Security & RLS

1. Check RLS enabled/forced state.
2. List policies and their commands, roles, USING and WITH CHECK expressions.
3. Inspect grants and exposed schemas.
4. Test or reason about anon/guest and authenticated access boundaries without modifying policies.
5. Review access to order tracking and customer/payment details.

### C. Database Functions & RPC

1. Inventory relevant functions and triggers.
2. Inspect definitions, owners, privileges, execution grants, and dependencies.
3. Review SECURITY DEFINER functions, fixed search_path, schema qualification, and authorization.
4. Trace payment/order/inventory transitions and transaction boundaries.
5. Identify duplicate/replay/concurrency risks.

### D. Edge Functions

1. Inventory relevant functions and deployment metadata.
2. Read source and configuration where available.
3. Trace callers, request/response contracts, provider requests, callback parsing, and DB writes.
4. Inspect JWT behavior, CORS, rate limits, validation, error handling, and logging.
5. Compare source to deployed behavior only when deployment metadata/logs are available.

### E. Secrets & Configuration

1. Inspect only safe names and presence metadata.
2. Map expected values to Sandbox/Production configuration without retrieving values.
3. Search repository/frontend output for accidental credential exposure.
4. Record missing/unknown metadata.
5. Never print or request actual secret values.

### F. Testing & Logs

1. Inspect relevant logs for a bounded time range.
2. Redact identifiers and personal data not needed for diagnosis.
3. Separate static checks from executed runtime tests.
4. Record command/query, environment, time, expected result, actual result, and evidence.
5. Do not treat missing logs as proof of success.

## Findings

Classify severity P0/P1/P2/P3 and evidence state Terverifikasi/Indikasi/Belum terverifikasi. For each finding include impact, affected objects, evidence, recommendation, and whether a change is required.

## Prohibited during audit

No INSERT/UPDATE/DELETE, DDL, migration execution, policy/grant changes, function deployment, secret mutation, production test payment, or repository write. These require a separate approved implementation scope.

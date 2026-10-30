# Official Duitku POP Documentation Reference

## Authoritative sources

- Indonesian POP documentation: https://docs.duitku.com/pop/id/
- English POP documentation: https://docs.duitku.com/pop/en/

These URLs are the provider-contract source of truth. This file is an audit guide, not a permanent substitute for the live documentation. Documentation can change; re-open the relevant page during every task and record the date checked.

## Incremental audit units

Audit and verify one unit at a time:

1. Integration mode and end-to-end flow.
2. Create Invoice endpoint, method, content type, headers, and request fields.
3. Request signature formula, timestamp units, encoding, and merchant identification.
4. Create Invoice response and provider-level status handling.
5. HTTP callback method, content type, parameters, and signature.
6. Callback response/acknowledgement and retry behavior.
7. Browser JS callback semantics.
8. Return URL / window redirection semantics.
9. Provider errors, duplicate invoice behavior, expiry, and any supported reconciliation/inquiry contract.
10. Supported payment methods and optional fields actually used by the merchant.

Do not mark a unit verified until its relevant official page content has been inspected and the contract is mapped to the implementation or requirements.

## Contract observations from the documentation checked for the initial skill draft

Checked: 2026-10-31. Source: https://docs.duitku.com/pop/id/

The current page content observed during initial drafting states:

### Create Invoice

- HTTP method: POST.
- Content type: application/json.
- Production endpoint: `https://api-prod.duitku.com/api/merchant/createInvoice`.
- Sandbox endpoint: `https://api-sandbox.duitku.com/api/merchant/createInvoice`.
- Required headers include `Content-Type`, `x-duitku-timestamp`, `x-duitku-signature`, and `x-duitku-merchantcode`.
- Timestamp is described as a Unix timestamp in milliseconds.
- Request signature formula shown:
  - `stringToSign = merchantCode + timestamp`
  - `signature = HMAC_SHA256(stringToSign, apiKey)`
- Required request parameters shown include `paymentAmount` (integer), `merchantOrderId`, `productDetails`, `email`, `callbackUrl`, and `returnUrl`. Optional parameters must be checked against the live docs and merchant account capability.
- Response fields shown include `merchantCode`, `reference`, `paymentUrl`, `statusCode`, and `statusMessage`.
- The page says requests using the same order ID can return the same response for five minutes, and concurrent/repeated requests may produce an in-progress or amount-different error. Re-check this behavior before relying on it.

### HTTP callback

- The callback is documented as HTTP POST with `application/x-www-form-urlencoded`.
- The callback example calculates:
  - `stringToSign = merchantCode + amount + merchantOrderId`
  - `signature = HMAC_SHA256(stringToSign, apiKey)`
- Callback parameters include merchant code, amount, merchant order ID, result code, reference, and signature, with additional optional provider/payment metadata.
- The callback parameter table describes `resultCode=00` as success and `resultCode=01` as failed.
- The page says the callback endpoint must be publicly reachable and return HTTP 200 after successful handling. It describes callback retries up to five attempts and a dashboard resend facility. Re-check retry/acknowledgement details at task time.
- Validate the callback signature and transaction mapping; do not use an IP allowlist as a substitute for cryptographic verification.

### Browser callbacks and redirects

- Duitku JS callback is for customer-facing notification and must not be used to update the merchant's authoritative payment status.
- Return URL query parameters may be changed by the customer and must not be used as proof of payment.
- Use the server-to-server HTTP callback and/or a currently documented authoritative reconciliation mechanism to establish payment state.

### Important ambiguity to resolve

The current POP page includes multiple callback-related status descriptions in different contexts. The HTTP callback parameter table describes `00` success and `01` failed. The JavaScript event descriptions separately refer to success `00`, pending `01`, and close `02`. Do not conflate these interfaces. If a callback response-code table or another section appears inconsistent or incomplete, record the exact conflicting text, ask for clarification from authoritative Duitku support where needed, and do not invent a mapping.

## Required contract mapping

For each audited unit, record:

| Field | Required evidence |
|---|---|
| Documentation URL and section | Exact official page/heading |
| Date checked | Current check date |
| Method and content type | Exact provider statement |
| Endpoint/environment | Sandbox vs Production |
| Required fields | Names, types, constraints |
| Signature | Exact string-to-sign, algorithm, key, encoding |
| Provider response | HTTP status vs provider business status |
| Retry/idempotency | Exact documented behavior |
| Implementation mapping | File/function/database object or “not implemented” |
| Verification | Static inspection, runtime test, or “not verified” |
| Open questions | Ambiguities and unresolved details |

## Rules

- Prefer POP documentation over generic Duitku API documentation for POP-specific behavior.
- Do not borrow contracts from Duitku API, Subscription, Account Linking, or other products unless the POP documentation explicitly points to them.
- Never assume an example value is a production credential or a valid test fixture.
- Never hardcode secrets or provider keys in this reference.
- Re-check current docs before implementing, changing, or verifying provider-facing behavior.

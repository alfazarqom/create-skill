# Incremental Duitku POP Documentation Audit

## Objective

Verify the current official POP contract in small, reviewable units before mapping or changing backend behavior.

## Procedure

1. Open https://docs.duitku.com/pop/id/ and, when useful, compare https://docs.duitku.com/pop/en/.
2. Confirm the page is POP documentation, not generic Duitku API, Subscription, or another product.
3. Select one audit unit only.
4. Capture the exact heading/section, URL, date checked, and relevant field/formula/statement.
5. Record required and optional fields, types, constraints, content type, endpoint, and environment as applicable.
6. Identify differences between Indonesian and English pages or between sections describing the same event.
7. Map the rule to the current backend/frontend caller only after repository evidence is available.
8. Mark the unit Terverifikasi, Indikasi, or Belum terverifikasi.
9. Present findings and open questions before moving to the next unit if the user expects incremental review.

## Audit units

- Integration mode and flow.
- Create Invoice request endpoint and HTTP contract.
- Request headers and request signature.
- Request body fields and validation.
- Create Invoice response and provider-level status.
- HTTP callback method, content type, parameters, signature.
- Callback acknowledgement and retry behavior.
- JavaScript callback.
- Return URL / redirect.
- Errors, duplicate request behavior, expiry.
- Reconciliation/inquiry capability, only if explicitly documented for the selected POP flow.

## Signature audit

For every signature formula, record:
- Exact ordered string-to-sign.
- HMAC/hash algorithm.
- Secret/key used.
- Character encoding and output encoding/case.
- Timestamp unit and permitted clock skew, if documented.
- Exact request/callback context.

Do not assume request and callback signatures use the same input. Do not use obsolete SHA256/MD5 examples or formulas from another Duitku product.

## Ambiguity handling

If docs conflict, are incomplete, or describe separate interfaces differently:
- Quote only the minimal field names/status values needed to identify the conflict.
- Record the page section and exact context.
- Keep the affected contract unverified.
- Do not invent a resolution.
- Seek an authoritative clarification from Duitku support or merchant documentation if needed.
- Add a test only after the expected behavior is authoritative.

## Output

Use `templates/audit-report.md`. Include a contract mapping table and an explicit list of verified, indicated, unverified, and unresolved items.

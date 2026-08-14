# Architecture

```text
Browser
  │ HTTPS / CSRF-protected forms
  ▼
Django Auth + Vault Views
  │  ├─ object-level user filtering
  │  ├─ password strength analysis
  │  └─ audit events
  ▼
Crypto layer
  │  ├─ Fernet encrypt/decrypt
  │  └─ HMAC-SHA256 reuse fingerprint
  ▼
SQLite
  ├─ encrypted credential fields
  ├─ password fingerprints
  └─ audit metadata (never plaintext passwords)
```

## Main components
- `vault/models.py`: credential and audit data model.
- `vault/crypto.py`: encryption and keyed fingerprint functions.
- `vault/security.py`: password-health and entropy heuristics.
- `vault/views.py`: authenticated CRUD, scoped authorization and Security Center.
- `vault/middleware.py`: defensive response headers.
- `vault/tests.py`: encryption-at-rest and cross-user authorization tests.
